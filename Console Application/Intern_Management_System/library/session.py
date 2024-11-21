from db.db_connector import get_db_connection

from tabulate import tabulate
from datetime import datetime, timedelta

import time


class SessionLander:
    @staticmethod
    def home(intern):
        while True:
            # choice = int(input(
            #     "Sessions\n1. View All Sessions\n2. View Upcoming Sessions\n3. View On-Going Sessions\n4. Completed "
            #     "Sessions\n5. Back\nEnter your choice: "))
            choice = int(input(
                "Sessions\n1. View All Sessions\n2. View Upcoming Sessions\n3. Back\nEnter your choice: "))
            if choice == 1:
                print("View All Sessions")
                time.sleep(1)
                session = ScheduleManager()
                session.view_schedule(intern)
            elif choice == 2:
                print("View Upcoming Sessions")
                time.sleep(1)
                session = ScheduleManager()
                session.upcoming_schedule(intern)
            # elif choice == 3:
            #     print("View On-Going Sessions")
            #     time.sleep(1)
            #     session = ScheduleManager()
            #     session.ongoing_schedule(intern)
            # elif choice == 4:
            #     print("View Completed Sessions")
            #     time.sleep(1)
            #     session = ScheduleManager()
            #     session.completed_schedule(intern)
            elif choice == 3:
                print("Getting Back")
                time.sleep(1)
                break
            else:
                print("Invalid Choice. Try Again!")


class ScheduleManager:
    def __init__(self):
        self.current_time = None
        self.db_connection = get_db_connection()

    def get_session_status(self, time_begin, time_end):
        self.current_time = datetime.now().time()
        today = datetime.now().date()

        session_start_time = (datetime.min + time_begin).time()
        session_end_time = (datetime.min + time_end).time()

        session_start_datetime = datetime.combine(today, session_start_time)
        session_end_datetime = datetime.combine(today, session_end_time)

        if self.current_time < session_start_datetime.time():
            return 'Upcoming'
        elif self.current_time > session_end_datetime.time():
            return 'Completed'
        else:
            return 'On-Going'

    def view_schedule(self, intern):
        cursor = self.db_connection.cursor()

        query = """SELECT session_id, session_title, handled_by, time_begin, time_end, duration FROM schedules"""
        cursor.execute(query)
        sessions = cursor.fetchall()

        if sessions:
            headers = ["Session ID", "Title", "Handled By", "Time Begin", "Time End", "Duration", "Status"]
            display_sessions = []

            for session in sessions:
                session_id, session_title, handled_by, time_begin, time_end, duration = session
                status = self.get_session_status(time_begin, time_end)
                display_sessions.append((session_id, session_title, handled_by, time_begin, time_end, duration, status))

            print(f"The sessions for {intern}")
            print(tabulate(display_sessions, headers=headers, tablefmt="grid"))
        else:
            print("No sessions found in the database.")

        cursor.close()

    def upcoming_schedule(self, intern):
        current_time = datetime.now().time()
        current_time = timedelta(hours=current_time.hour, minutes=current_time.minute, seconds=current_time.second)
        cursor = self.db_connection.cursor()

        query = """SELECT session_id, session_title, handled_by, time_begin, time_end, duration FROM schedules"""

        cursor.execute(query)
        sessions = cursor.fetchall()
        print(f"The upcoming sessions for {intern}")

        upcoming_sessions = []
        for session in sessions:
            session_time_begin = session[3]
            if session_time_begin > current_time:
                upcoming_sessions.append(session)

        if upcoming_sessions:
            headers = ["Session ID", "Title", "Handled By", "Time Begin", "Time End", "Duration"]
            print(tabulate(upcoming_sessions, headers=headers, tablefmt="grid"))
        else:
            print("No upcoming sessions found in the database.")
        print("\n")
        cursor.close()

    def ongoing_schedule(self, intern):
        print("Working on it")
        return

    def completed_schedule(self, intern):
        print("Working on it")
        return
