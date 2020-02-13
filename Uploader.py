import utilities
import os
import numpy as np
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def main(id, key):
    images = sorted(os.listdir("FromPhone"))
    for i in images:
        utilities.uploadFileAtLocation(str(key) +"-"+ i,os.path.join("FromPhone", i),'image/jpeg',"1abenXCfjjheG3YertatxFYeGd3J4kjsC")
    images = sorted(os.listdir("Foto"))
    b = np.load("info.npy")
    parent = b[id,-1]
    ids =[]
    for i in images:
        ids.append(utilities.uploadFileAtLocation(str(key) +"-"+ i,os.path.join("Foto", i),'image/jpeg',parent))
    


    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    
    id = int(id)    
    if id ==0:
        sheet = client.open("GenericForm").sheet1
    elif (id ==1):
        sheet = client.open("MedicalForm").sheet1    
    
    txt = np.load("results.npy")
    txt = txt.tolist()    
    
    cnt=0    
    for row in txt:
        
        row.insert(0, key)        
        row.append('=IMAGE(SUBSTITUTE("https://drive.google.com/open?id='+ids[cnt]+'","https://drive.google.com/open?id=","https://docs.google.com/uc?export=download&id="))')
        cnt+=1        
        sheet.insert_row(row, 2)            

