import gspread
from pathlib import Path
from redis import Redis
from rq import Queue
from rq import Retry
    
from oauth2client.service_account import ServiceAccountCredentials
from persistenceinterface import PersistenceInterface

class PersistToGoogleSheets(PersistenceInterface):
    def process(timestamp, datapoint):
        CREDENTIALS_FILE = "key.json"
        TEMPERATURE_DOC = "TemperatureLL208DY"

        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive.file',
                'https://www.googleapis.com/auth/drive']
        # Reading Credentials from ServiceAccount Keys file
        credentialsPath = str(Path(__file__).parent.resolve()) + '/' + CREDENTIALS_FILE
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentialsPath, scope)
        # intitialize authorization object
        gc = gspread.authorize(credentials)
        # Open Google Sheets file
        sheet = gc.open(TEMPERATURE_DOC).sheet1
        try:
            sheet.append_row([timestamp, datapoint])
        except Exception as e: print(e)
        return

    def write(self, timestamp, datapoint):
        q = Queue(connection=Redis())
        result = q.enqueue(self.process, timestamp, datapoint, retry=Retry(max=3, interval=[60, 600, 3600]))
