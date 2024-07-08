from main.spread_sheet import Spreadsheet
from main.const import SS_FOLDER_ID, GOOGLE_CREDENTIAL_JSON
from tests.data import test_data


def test_update():
    spreadsheet = Spreadsheet(GOOGLE_CREDENTIAL_JSON, test_data, SS_FOLDER_ID)
    spreadsheet.update()