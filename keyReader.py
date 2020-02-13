import gspread
from oauth2client.service_account import ServiceAccountCredentials


def main():
    # use creds to create a client to interact with the Google Drive API
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("SessionKey").sheet1

    # Extract and print all of the values
    #list_of_hashes = sheet.get_all_records()
    #print(list_of_hashes)

    #row = ["I'm","inserting","a","row","into","a,","Spreadsheet","with","=IMAGE('FromPhone\\img2.jpg')"]
    #sheet.insert_row(row, 1)

    key = int(sheet.cell(1,1).value)
    print(key)
    sheet.update_cell(1,1, str(key+1))

    return key

