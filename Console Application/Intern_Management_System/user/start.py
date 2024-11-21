from user.login import Login
from user.login import SignUp


class Start:
    @staticmethod
    # Login
    def login():
        signin = Login()
        signin.user()

    @staticmethod
    # Create Account
    def signup():
        create_account = SignUp()
        create_account.create_account()

    @staticmethod
    # Dashboard
    def display_dashboard():
        while True:
            print("Welcome to the Intern Management System!")
            print("1. Sign In")
            print("2. Sign Up")
            print("3. Exit")
            choice = int(input("Enter your choice (1 or 2 or 3): "))
            if choice == 1:
                Start().login()
            elif choice == 2:
                Start().signup()
            elif choice == 3:
                print("Quitting Application")
                break
            else:
                print("Invalid Choice Try Again!")
