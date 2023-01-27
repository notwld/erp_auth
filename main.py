import requests
from bs4 import BeautifulSoup
import json,os
from dotenv import load_dotenv
from rich.table import Table
from rich.console import Console

console = Console()


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
    # res = req.get('http://erp.uit.edu:803/StudentPortal/Student/EDU_EBS_STU_ACD_StudentCourseHistory.aspx')
    res = req.get('http://erp.uit.edu:803/StudentPortal/Student/EDU_EBS_STU_Attendance.aspx')
    return res.text

soup = BeautifulSoup(login(os.environ.get("rollno"), os.environ.get("password")), 'html.parser')
# print(soup.find('span', {'id': 'ctl00_user_name'}).text)

# table_class = "rgMasterTable"

# table = soup.find('table', attrs={'class': table_class})
# table_body = table.find('tbody')

# rows = table_body.find_all('tr')
# data = []
# for row in rows:
#     cols = row.find_all('td')
#     cols = [ele.text.strip() for ele in cols]
#     data.append([ele for ele in cols if ele])

# table = Table(show_header=True, header_style="bold magenta", show_lines=True)
# table.add_column("Course Code", style="dim", width=12)
# table.add_column("Course Title", style="dim", width=12)
# table.add_column("Credit Hours", style="dim", width=12)
# table.add_column("Grade", style="dim", width=12)
# table.add_column("Grade Point", style="dim", width=12)
# table.add_column("Semester", style="dim", width=12)
# table.add_column("Year", style="dim", width=12)

# for i in range(len(data)):
#     table.add_row(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6])


# console.print(table)

table = "rgMasterTable"

table = soup.find('table', attrs={'class': table})
table_body = table.find('tbody')

rows = table_body.find_all('tr')
data = []
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

table = Table(show_header=True, header_style="bold magenta", show_lines=True)
table.add_column("Course Code", style="dim", width=12)
table.add_column("Section Code", style="dim", width=12)
table.add_column("Total Classes", style="dim", width=12)
table.add_column("Taken Classes", style="dim", width=12)

table.add_column("Attended Classes", style="dim", width=12)
table.add_column("Percentage", style="dim", width=12)

for i in range(len(data)):
    table.add_row(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5])

console.print(table)



    