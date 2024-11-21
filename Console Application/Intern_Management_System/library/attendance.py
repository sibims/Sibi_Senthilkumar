from db.db_connector import get_db_connection
from datetime import datetime, time
from tabulate import tabulate


# Polymorphism for class ForenoonAttendance and class AfternoonAttendance
class ForenoonAttendance:
    @staticmethod
    def is_attendance_open(current_time):
        forenoon_start_time = time(8, 45)
        forenoon_end_time = time(9, 30)
        return forenoon_start_time <= current_time <= forenoon_end_time

    @staticmethod
    def get_attendance_type():
        return 'FN'


class AfternoonAttendance:
    @staticmethod
    def is_attendance_open(current_time):
        afternoon_start_time = time(12, 30, 00)
        afternoon_end_time = time(13, 30, 00)
        return afternoon_start_time <= current_time <= afternoon_end_time

    @staticmethod
    def get_attendance_type():
        return 'AN'


class Attendance:
    def __init__(self, attendance_type=None):
        self.db_connection = get_db_connection()
        self.attendance_type = attendance_type
        self.create_attendance_table()

    def create_attendance_table(self):
        cursor = self.db_connection.cursor()
        query = """CREATE TABLE IF NOT EXISTS attendance (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            username VARCHAR(15) NOT NULL,
                            attendance_date DATE NOT NULL,
                            attendance_time TIME NOT NULL,
                            attendance_type VARCHAR(2) NOT NULL
                        )"""
        cursor.execute(query)
        self.db_connection.commit()
        cursor.close()

    def attendance_option(self, username):
        while True:
            print("Attendance")
            choice = int(
                input("1. Record your Attendance\n2. View Attendance History\n3. MainMenu\nEnter your choice: "))
            if choice == 1:
                print("Record Attendance")
                self.record_attendance(username)
            elif choice == 2:
                print("View Attendance")
                self.view_attendance(username)
            elif choice == 3:
                print("Getting Back to MainMenu")
                break
            else:
                print("Invalid Choice. Try Again!")

    def record_attendance(self, username):
        cursor = self.db_connection.cursor()
        current_time = datetime.now().time()

        if not self.attendance_type:
            self.attendance_type = ForenoonAttendance.get_attendance_type() if ForenoonAttendance.is_attendance_open(
                current_time) else AfternoonAttendance.get_attendance_type()

        allowed_to_record = False

        if self.attendance_type == ForenoonAttendance.get_attendance_type():
            allowed_to_record = ForenoonAttendance.is_attendance_open(current_time)
        elif self.attendance_type == AfternoonAttendance.get_attendance_type():
            allowed_to_record = AfternoonAttendance.is_attendance_open(current_time)

        if allowed_to_record:
            query = """INSERT INTO attendance (username, attendance_date, attendance_time, attendance_type) 
                               VALUES (%s, %s, %s, %s)"""
            data = (username, datetime.now().date(), current_time, self.attendance_type)
            cursor.execute(query, data)
            self.db_connection.commit()
            print(f"Current time is {current_time.strftime('%H:%M:%S')}")
            print("Attendance recorded successfully.")
        else:
            print("Attendance is not opened.")
        cursor.close()

    def view_attendance(self, username):
        cursor = self.db_connection.cursor()
        query = """SELECT attendance_date, attendance_time, attendance_type FROM attendance 
                   WHERE username = %s"""
        cursor.execute(query, (username,))
        attendance_data = cursor.fetchall()

        if attendance_data:
            headers = ["Date", "Time", "Attendance Type"]
            print("Attendance Records:")
            print(tabulate(attendance_data, headers=headers, tablefmt="grid", colalign=("left", "left", "center")))
        else:
            print("No attendance records found for the given username.")
