import pytz
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from logging import config, getLogger

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
            "https://www.googleapis.com/auth/drive.file"
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
        prior_date = today_jst - timedelta(days=10)

        # Format the spreadsheet name and sheet name
        self.spreadsheet_name = f"land_{prior_date.strftime('%Y%m')}"
        self.sheet_name = prior_date.strftime('%m%d')

    def get_or_create_spreadsheet(self):
        # Try to open the existing spreadsheet, if it does not exist, create a new one
        try:
            spreadsheet = self.client.open(self.spreadsheet_name)
            logger.info(f"Use existing spreadsheet: {self.spreadsheet_name}")
        except gspread.SpreadsheetNotFound:
            spreadsheet = self.client.create(self.spreadsheet_name)
            logger.info(f"Created new spreadsheet: {self.spreadsheet_name}")
            if self.folder_id:
                # Move the spreadsheet to the specified folder
                file_id = spreadsheet.id

                try:
                    # Verify if the file is already in the folder
                    file = self.drive_service.files().get(fileId=file_id, fields='parents').execute()
                    previous_parents = ",".join(file.get('parents', []))
                    if previous_parents != self.folder_id:
                        self.drive_service.files().update(
                            fileId=file_id,
                            addParents=self.folder_id,
                            removeParents=previous_parents,
                            fields='id, parents'
                        ).execute()
                        logger.info(f"Moved spreadsheet to folder: {self.folder_id}")
                except Exception as e:
                    logger.error(f"Error moving spreadsheet to folder: {e}")
                                
            # Share the spreadsheet with the service account
            try:
                self.drive_service.permissions().create(
                    fileId=spreadsheet.id,
                    body={
                        'type': 'user',
                        'role': 'writer',
                        'emailAddress': self.service_account_email
                    },
                    fields='id'
                ).execute()
                
                logger.info(f"Shared spreadsheet with service account: {self.service_account_email}")
            except Exception as e:
                logger.error(f"Error sharing spreadsheet with service account: {e}")
        return spreadsheet

    def get_or_create_sheet(self, spreadsheet):
        # Try to find the existing sheet, if it does not exist, create a new one
        try:
            sheet = spreadsheet.worksheet(self.sheet_name)
            sheet.clear()
            logger.info(f"Updating existing sheet: {self.sheet_name}")
        except gspread.WorksheetNotFound:
            sheet = spreadsheet.add_worksheet(title=self.sheet_name, rows=str(len(self.data)), cols=str(len(self.data[0])))
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

    def update(self):
        self.authenticate()
        self.get_date_info()
        spreadsheet = self.get_or_create_spreadsheet()
        sheet = self.get_or_create_sheet(spreadsheet)
        self.update_sheet(sheet)
