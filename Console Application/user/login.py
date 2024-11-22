from db.db_connector import get_db_connection
from library.session import SessionLander
from library.attendance import Attendance

import mysql.connector
import time

import pwinput
import re
from datetime import datetime
from tabulate import tabulate


# Object for Signed in User
class Intern:
    def __init__(self, id, first_name, last_name, mobile_number, blood_group, created_at, username, password):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.mobile_number = mobile_number
        self.blood_group = blood_group
        self.created_at = created_at
        self.username = username
        self.password = password

    def get_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_mobile_number(self):
        return self.mobile_number

    def get_blood_group(self):
        return self.blood_group

    def get_username(self):
        return self.username

    def __str__(self):
        return f"Intern ID: {self.id}, Name: {self.get_name()}, Mobile: {self.mobile_number}, Blood Group: {self.blood_group}, Username: {self.username}"


class Login:

    # Default Constructor
    def __init__(self):
        self.db_connection = None
        self.session_manager = None
        self.current_user = None
        self.db_connection = get_db_connection()
        cursor = self.db_connection.cursor()

        # Login Table
        query = """CREATE TABLE IF NOT EXISTS login (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(15) NOT NULL,
                    login_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )"""
        cursor.execute(query)
        self.db_connection.commit()
        cursor.close()

    # Login
    def login(self):
        username = input("Enter your username: ")
        password = pwinput.pwinput(prompt='Enter your Password: ', mask='*')

        intern = self.authenticate_user(username, password)
        time.sleep(1)
        if intern:
            print("\nAuthentication successful. Welcome,", intern.get_name())
            self.db_connection = get_db_connection()
            cursor = self.db_connection.cursor()
            query = """INSERT INTO login (username, login_timestamp) VALUES (%s, %s)"""
            data = (username, datetime.now())
            cursor.execute(query, data)
            self.db_connection.commit()
            cursor.close()
            self.current_user = True
            while True:
                time.sleep(1)
                choice = int(input("1. View Sessions\n2. Mark your Attendance\n3. Sign Out\n Enter your choice: "))
                if choice == 1:
                    session = SessionLander()
                    session.home(intern.get_name())
                elif choice == 2:
                    mark_attendance = Attendance()
                    mark_attendance.attendance_option(username)
                elif choice == 3:
                    self.signout()
                    break
                else:
                    print("Invalid Choice. Try Again.")
        else:
            print("Authentication failed. Invalid username or password.")
            time.sleep(1)
            return None

    # Sign In User Landing Page
    def user(self):
        while True:
            choice = int(input("1. Login\n2. View Details\n3. Landing Page\nEnter your choice: "))
            if choice == 1:
                time.sleep(1)
                Login.login(self)
            elif choice == 2:
                time.sleep(1)
                View_Details.details(self)
            elif choice == 3:
                print("Returning to Home Screen")
                time.sleep(1)
                break
            else:
                print("Invalid Choice. Try Again!")

    # User Authentication
    def authenticate_user(self, username, password):
        try:
            self.db_connection = get_db_connection()
            cursor = self.db_connection.cursor()

            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            data = (username, password)
            cursor.execute(query, data)

            user_data = cursor.fetchone()

            cursor.close()
            self.db_connection.close()

            if user_data:
                # If a user with the given username and password exists, create and return an Intern object
                intern = Intern(
                    user_data[0],
                    user_data[1],
                    user_data[2],
                    user_data[3],
                    user_data[4],
                    user_data[5],
                    user_data[6],
                    user_data[7]
                )
                return intern
            else:
                return None

        except mysql.connector.Error as e:
            print(f"Error occurred during database operation: {e}")
            time.sleep(1)
            return None

    # Sign-out
    def signout(self):
        self.current_user = None
        print("Sign-out successful. You have been logged out.")
        time.sleep(1)


class SignUp:
    def __init__(self):
        # Create a Table for storing user details
        self.db_connection = get_db_connection()
        cursor = self.db_connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            first_name VARCHAR(255) NOT NULL, 
            last_name VARCHAR(255) NOT NULL, 
            mobile_number VARCHAR(10) UNIQUE, 
            blood_group VARCHAR(3) NOT NULL, 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            username VARCHAR(15) NOT NULL,
            password VARCHAR(15) NOT NULL,
            passcode VARCHAR(4) NOT NULL)
            """
        cursor.execute(query)
        self.db_connection.commit()
        cursor.close()

    def create_account(self):
        first_name = input("Enter your First Name:")
        last_name = input("Enter your Last Name: ")

        # Mobile Number Validation
        while True:
            mobile_number = input("Enter your Mobile Number (Ex: 9894969290): ")
            if not re.match(r'^\d{10}$', mobile_number):
                print("Invalid mobile number format. Please enter a 10-digit number.")
            else:
                break

        # Blood Group Validation
        while True:
            blood_group = input("Enter your BloodGroup (Ex: AB+ or AB-): ")
            if not re.match(r'^(A|B|AB|O)[+-]$', blood_group.upper()):
                print("Invalid blood group format. Please enter a valid blood group (Ex: AB+ or AB-).")
            else:
                break

        # Passcode Validation
        while True:
            passcode = pwinput.pwinput(prompt='Enter a 4 digit passcode: ', mask='*')
            if not re.match(r'^\d{4}$', passcode):
                print("Invalid passcode format. Please enter a 4-digit passcode.")
            else:
                break
        username = first_name[0:4] + '.' + last_name[0:3] + '@' + mobile_number[6:9]
        password = first_name[0:4] + '.' + mobile_number[6:10]

        try:
            self.db_connection = get_db_connection()
            cursor = self.db_connection.cursor()

            # Execute the INSERT query to store the new user account
            created_at = datetime.now()
            query = """INSERT INTO users (
                first_name, 
                last_name, 
                mobile_number, 
                blood_group, 
                created_at, 
                username,
                password,
                passcode) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
            data = (first_name, last_name, mobile_number, blood_group, created_at, username, password, passcode)
            cursor.execute(query, data)

            self.db_connection.commit()
            cursor.close()

        except mysql.connector.Error as e:
            print(f"Error occurred: {e}")

        time.sleep(1)
        print("Account created successfully!")
        return

# Inherited Class View_Details from Login
class View_Details(Login):
    def details(self):
        while True:
            mobile_number = input("Enter your Mobile Number (Ex: 9894969290): ")
            if not re.match(r'^\d{10}$', mobile_number):
                print("Invalid mobile number format. Please enter a 10-digit number.")
            else:
                break
        while True:
            passcode = pwinput.pwinput(prompt='Enter your Passcode to view details: ', mask='*')
            if not re.match(r'^\d{4}$', passcode):
                print("Invalid passcode format. Please enter a 4-digit passcode.")
            else:
                break
        try:
            db_connection = get_db_connection()
            cursor = db_connection.cursor()

            query = """SELECT id, first_name, last_name, username, password FROM users WHERE mobile_number = %s AND passcode = %s"""
            cursor.execute(query, (mobile_number, passcode))
            intern_data = cursor.fetchone()

            if intern_data:
                headers = ["ID", "First Name", "Last Name", "Username", "Password"]
                data = [intern_data]

                print("Intern Details:")
                print(tabulate(data, headers=headers, tablefmt="grid"))
                return None
            else:
                print("Intern with the given mobile number not found.")

            cursor.close()

        except mysql.connector.Error as e:
            print(f"Error occurred: {e}")
