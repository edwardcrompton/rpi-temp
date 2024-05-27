import gspread

from oauth2client.service_account import ServiceAccountCredentials
from persistenceinterface import PersistenceInterface

class PersistToGoogleSheets(PersistenceInterface):
    def write(timestamp, temperature):
        CREDENTIALS_FILE = "key.json"
        TEMPERATURE_DOC = "TemperatureLL208DY"

        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive.file',
                'https://www.googleapis.com/auth/drive']
        # Reading Credentails from ServiceAccount Keys file
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
        # intitialize authorization object
        gc = gspread.authorize(credentials)
        # Open Google Sheets file
        sheet = gc.open(TEMPERATURE_DOC).sheet1
        try:
            sheet.append_row([timestamp, temperature])
        except Exception as e: print(e)
        return