import Cleaner
import sys
import gspread
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials

def main(id, key):
    id = int(id)
    # use creds to create a client to interact with the Google Drive API
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    txt = list(np.load("results.npy"))
    a,b = [],[]
    for t in txt:
        for q in t:
            a.append(q)
        b.append(a)
        a = []
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    if id ==0:
        sheet = client.open("GenericForm").sheet1
    elif (id ==1):

        sheet = client.open("MedicalForm").sheet1

    #for k in b :
        #print(type(b), b)
    #    sheet.insert_row(k, 2)
    sheet.insert_row([key, ], 2)


        #print(r)
    # Extract and print all of the values
    #list_of_hashes = sheet.get_all_records()
    #print(list_of_hashes)

    #row = ["I'm","inserting","a","row","into","a,","Spreadsheet","with","=IMAGE('FromPhone\\img2.jpg')"]
    #sheet.insert_row(row, 1)
    Cleaner.main()
if __name__ == "__main__":
    main(sys.argv[1], 5)
