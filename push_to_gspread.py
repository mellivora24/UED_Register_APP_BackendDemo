import sys
import gspread
from serial import Serial
from datetime import datetime
from gspread.exceptions import WorksheetNotFound
from gspread.exceptions import SpreadsheetNotFound

# !importan
arduino = Serial(port='COM?', baudrate=9600)  # Replace by COM available
google_sheet = gspread.service_account(filename='service_account.json')
your_mail = "email_user_for_api@gmail.com"

sheet_name = "Class " + str(input("Nhập lớp: "))
try:
    sheet = google_sheet.open(sheet_name)
except SpreadsheetNotFound:
    sheet = google_sheet.create(sheet_name)
    sheet.share(your_mail, perm_type='user', role='writer')
    print("Vui lòng điền thông tin lớp học vào bảng tính 'DATA' trước!")
    sys.exit()


def get_current_time():
    date_time = datetime.now()
    month = date_time.month
    day = date_time.day
    year = date_time.year
    time = date_time.strftime("%H:%M:%S")
    return time, day, month, year


def get_information(finger_id):
    try:
        data_base = sheet.worksheet("DATA")
        student_id = data_base.cell(finger_id+1, 2).value
        student_name = data_base.cell(finger_id+1, 3).value
        return student_id, student_name
    except SpreadsheetNotFound:
        print("Vui lòng điền thông tin lớp học vào bảng tính 'DATA' trước!")
        sys.exit()
        return None


def push_2_gspread(finger_id):
    time, day, month, year = get_current_time()
    current_time = str(time)
    current_date = str(day) + "/" + str(month) + "/" + str(year)

    student_id, student_name = get_information(finger_id)

    try:
        work_sheet = sheet.worksheet("Điểm danh ngày " + str(current_date))
    except WorksheetNotFound:
        work_sheet = sheet.add_worksheet("Điểm danh ngày " + str(current_date), rows=130, cols=3)

    work_sheet.update_cell(finger_id, 1, student_id)
    work_sheet.update_cell(finger_id, 2, student_name)
    work_sheet.update_cell(finger_id, 3, current_time)


while True:
    incoming_data = int(arduino.readline().decode())
    if incoming_data > 0:
        push_2_gspread(incoming_data)
