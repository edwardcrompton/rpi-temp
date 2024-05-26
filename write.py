import gspread
import random
import time
from oauth2client.service_account import ServiceAccountCredentials

def main():
    temp = random.randrange(40)
    timestamp = time.time()
    print(temp)
    print(timestamp)
    write(timestamp, temp);

def write(timestamp, temperature):
    CREDENTIALS_FILE = "sapient-logic-424419-a5-b926e91862ed.json"
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

# Function Call
if __name__ == '__main__':
    main()
