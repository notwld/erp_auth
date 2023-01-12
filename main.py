import requests
from bs4 import BeautifulSoup
import json,os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

def login(username, password):
    req = requests.Session()
    payload = json.load(open('payload.json'))

    url = 'http://erp.uit.edu:803/StudentPortal/Student/EDU_EBS_STU_Login.aspx'

    payload['ctl00$ContentPlaceHolder1$txtRegistrationNo_cs'] = username
    payload['ctl00$ContentPlaceHolder1$txtPassword_m6cs'] = password
    payload['ctl00$ContentPlaceHolder1$btnlgn']= 'Login'
    
    req.post(url, data=payload)
    res = req.get('http://erp.uit.edu:803/StudentPortal/Student/EDU_EBS_STU_Dashboard.aspx')
        
    return res.text

soup = BeautifulSoup(login(os.environ.get("rollno"), os.environ.get("password")), 'html.parser')
print(soup.find('span', {'id': 'ctl00_user_name'}).text)
