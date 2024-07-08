import pytz
from datetime import datetime, timedelta
import time

import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from gspread_formatting import CellFormat, Color, set_frozen, format_cell_range
from logging import getLogger
from const import RIGHT_ALIGNED_COLUMNS_INDICES

logger = getLogger(__name__)

class Spreadsheet:
    def __init__(self, credentials_file, data, folder_id=None):
        self.credentials_file = credentials_file
        self.data = data
        self.folder_id = folder_id
        self.client = None
        self.drive_service = None
        self.spreadsheet_name = None
        self.sheet_name = None
        self.service_account_email = None

    def authenticate(self):
        # Use the JSON file for authentication
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/spreadsheets"
        ]
        creds = Credentials.from_service_account_file(self.credentials_file, scopes=scope)
        self.client = gspread.authorize(creds)
        self.drive_service = build('drive', 'v3', credentials=creds)

        # Get the service account email
        with open(self.credentials_file) as f:
            import json
            self.service_account_email = json.load(f)['client_email']
        logger.info("Authorized the service account")

    def get_date_info(self):
        # Get the current date in JST timezone
        jst = pytz.timezone('Asia/Tokyo')
        today_jst = datetime.now(jst)

        # Get the prior date
        prior_date = today_jst - timedelta(days=1)

        # Format the spreadsheet name and sheet name
        self.spreadsheet_name = f"land_{prior_date.strftime('%Y%m')}"
        self.sheet_name = prior_date.strftime('%m%d')

    def get_or_create_spreadsheet(self):
        # List files in the specified folder to check if the spreadsheet already exists
        query = f"'{self.folder_id}' in parents and mimeType='application/vnd.google-apps.spreadsheet'"

        results = self.drive_service.files().list(
            q=query,
            spaces='drive',
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
            corpora='allDrives',
            fields='files(id, name)'
        ).execute()
        items = results.get('files', [])
        logger.info(f'Existing spreadsheets: {items}')
        
        spreadsheet = None

        for item in items:
            if item['name'] == self.spreadsheet_name:
                file_id = item['id']
                spreadsheet = self.client.open_by_key(file_id)
                logger.info(f"Using existing spreadsheet: {self.spreadsheet_name}")
                break

        if not spreadsheet:
            # Spreadsheet does not exist, create a new one in the specified folder
            file_metadata = {
                'name': self.spreadsheet_name,
                'mimeType': 'application/vnd.google-apps.spreadsheet',
                'parents': [self.folder_id]
            }
            try:
                file = self.drive_service.files().create(body=file_metadata, fields='id', supportsAllDrives=True).execute()
                file_id = file.get('id')
                spreadsheet = self.client.open_by_key(file_id)
                logger.info(f"Created new spreadsheet in folder: {self.spreadsheet_name}")

                # Wait for a short period to ensure the file is available
                time.sleep(5)

                # Verify the file ID before sharing
                file = self.drive_service.files().get(fileId=file_id, fields='id', supportsAllDrives=True).execute()
                if file and file.get('id') == file_id:
                    # Share the spreadsheet with the service account
                    self.drive_service.permissions().create(
                        fileId=file_id,
                        body={
                            'type': 'user',
                            'role': 'writer',
                            'emailAddress': self.service_account_email
                        },
                        fields='id',
                        supportsAllDrives=True
                    ).execute()
                    logger.info(f"Shared spreadsheet with service account: {self.service_account_email}")
                else:
                    logger.error(f"File verification failed for file ID: {file_id}")

            except Exception as e:
                logger.error(f"Error creating or sharing spreadsheet: {e}")

        return spreadsheet

    def get_or_create_sheet(self, spreadsheet):
        # Try to find the existing sheet, if it does not exist, create a new one
        try:
            sheet = spreadsheet.worksheet(self.sheet_name)
            sheet.clear()
            logger.info(f"Updating existing sheet: {self.sheet_name}")
        except gspread.WorksheetNotFound:
            sheet = spreadsheet.add_worksheet(title=self.sheet_name, rows=str(len(self.data)+1), cols=str(len(self.data[0])+3))
            logger.info(f"created sheet: {self.sheet_name}")
        return sheet

    def update_sheet(self, sheet):
        # Insert data into the sheet
        sheet.clear()  # Clear the sheet before inserting new data
        cell_list = sheet.range(1, 1, len(self.data), len(self.data[0]))
        for cell, value in zip(cell_list, [item for sublist in self.data for item in sublist]):
            cell.value = value
        sheet.update_cells(cell_list)
        
        logger.info("Updated the spreadsheet")
        

    def format_sheet(self, spreadsheet, sheet):
        set_frozen(sheet, rows=1)

        header_format = CellFormat(
            backgroundColor=Color(0.8, 0.9, 1),  # Pale blue color
            # textFormat={'bold': True}
        )

        # Apply the format to the first row
        format_cell_range(sheet, '1:1', header_format)

        # Add auto filter to the first row
        spreadsheet.batch_update({
            'requests': [{
                'setBasicFilter': {
                    'filter': {
                        'range': {
                            'sheetId': sheet.id,
                            'startRowIndex': 0,
                            'endRowIndex': 1
                        }
                    }
                }
            }]
        })
        self.auto_resize_columns(spreadsheet, sheet)        
        self.format_columns_with_right_alignment(sheet, RIGHT_ALIGNED_COLUMNS_INDICES)
        
        logger.info("Formatted sheet")

    def auto_resize_columns(self, spreadsheet, sheet):
        sheet_data = sheet.get_all_values()
        if not sheet_data:
            return

        # Initialize a list to store the maximum length of each column
        max_lengths = [0] * len(sheet_data[0])
        
        # Calculate the maximum length of values in each column
        for row in sheet_data:
            for col_idx, cell in enumerate(row):
                max_lengths[col_idx] = max(max_lengths[col_idx], len(str(cell)) + 4)
        
        # Create batch update requests for resizing columns
        requests = []
        for col_idx, max_length in enumerate(max_lengths):
            requests.append({
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet.id,
                        "dimension": "COLUMNS",
                        "startIndex": col_idx,
                        "endIndex": col_idx + 1
                    },
                    "properties": {
                        "pixelSize": max(40, max_length * 10)  # Set minimum width to 100 pixels
                    },
                    "fields": "pixelSize"
                }
            })

        # Send batch update request
        spreadsheet.batch_update({"requests": requests})
        logger.debug('columns size updated')

    def format_columns_with_right_alignment(self, sheet, column_indices):
        right_align_format = CellFormat(
            horizontalAlignment='RIGHT'
        )

        # Apply the format to each specified column
        for col_idx in column_indices:
            col_letter = chr(col_idx + ord('A'))
            format_cell_range(sheet, f'{col_letter}:{col_letter}', right_align_format)

    def update(self):
        self.authenticate()
        self.get_date_info()
        spreadsheet = self.get_or_create_spreadsheet()
        sheet = self.get_or_create_sheet(spreadsheet)
        self.update_sheet(sheet)
        self.format_sheet(spreadsheet, sheet)
        
        # Delete the default sheet if it exists after creating a new sheet
        default_sheet = spreadsheet.sheet1
        if default_sheet.title == 'Sheet1' and len(spreadsheet.worksheets()) > 1:
            spreadsheet.del_worksheet(default_sheet)
            logger.info("Deleted default blank sheet")
