import random
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime, timedelta


# Admin Login Screen
class AdminLoginScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Admin Login")
        self.geometry("1550x850")
        self.configure(bg="black")

        # Title Label
        title_label = tk.Label(
            self, 
            text="ADMIN LOGIN", 
            font=("Times New Roman", 48, "bold"), 
            bg='black', 
            fg='white'
        )
        title_label.pack(pady=(50, 20))

        # Admin Username Field
        tk.Label(self, text="USERNAME", font=("Times New Roman", 24, "bold"), bg='black', fg='white').place(x=685, y=200)
        self.username_entry = tk.Entry(self, font=("Times New Roman", 20), justify=tk.CENTER)
        self.username_entry.place(x=550, y=240, width=450, height=40)

        # Admin Password Field
        tk.Label(self, text="PASSWORD", font=("Times New Roman", 24, "bold"), bg='black', fg='white').place(x=685, y=300)
        self.password_entry = tk.Entry(self, font=("Times New Roman", 20), show="*", justify=tk.CENTER)
        self.password_entry.place(x=550, y=340, width=450, height=40)

        # Login Button
        tk.Button(self, text="LOG IN", font=("Times New Roman", 24, "bold"), command=self.handle_admin_login).place(x=700, y=450, width=170, height=60)

    def handle_admin_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            db_connection = mysql.connector.connect(
                host ="localhost",
                user="root",
                password="1234",
                database="gym_python"
            )
            cursor = db_connection.cursor()

            # Query to check admin credentials
            query = "SELECT * FROM admins WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                # Admin is authenticated, redirect to the Admin Dashboard
                self.destroy()
                AdminDashboard().mainloop()
            else:
                messagebox.showerror("Login Failed", "Invalid admin credentials")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            db_connection.close()

# Admin Dashboard Screen

class AdminDashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Admin Dashboard")
        self.geometry("1550x850")
        self.configure(bg='black')

        # Title Label
        title_label = tk.Label(
            self, 
            text="ADMIN DASHBOARD", 
            font=("Times New Roman", 48, "bold"), 
            bg='black', 
            fg='white'
        )
        title_label.pack(pady=(50, 20))

        # Manage Users Button
        tk.Button(self, text="MANAGE USERS", font=("Times New Roman", 24, "bold"), command=self.manage_users).place(x=600, y=250, width=350, height=50)

        # Logout Button
        tk.Button(self, text="LOG OUT", font=("Times New Roman", 24, "bold"), command=self.confirm_logout).place(x=600, y=350, width=350, height=50)

    def manage_users(self):
        # Open the Manage Users Screen
        self.destroy()  # Close the AdminDashboard
        ManageUsersScreen().mainloop()  # Open ManageUsersScreen

    def confirm_logout(self):
        # Show a confirmation dialog
        response = messagebox.askquestion("Confirm Logout", "Are you sure you want to logout?")
        if response == 'yes':
            self.destroy()  # Close the AdminDashboard
            LoginScreen().mainloop()  # Open the LoginScreen

class ManageUsersScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Manage Users")
        self.geometry("1550x850")
        self.configure(bg='black')

        # Title Label
        title_label = tk.Label(
            self, 
            text="USER MANAGEMENT", 
            font=("Times New Roman", 48, "bold"), 
            bg='black', 
            fg='white'
        )
        title_label.pack(pady=(50, 20))

        # Table header for user data
        header = tk.Label(self, text="USERNAME\t|\tPROMO\t\tasa|\tEXPIRATION DATE", font=("Times New Roman", 24, "bold"), bg='black', fg='white')
        header.place(x=200, y=110)

        # Scrollable canvas for user list
        self.canvas = tk.Canvas(self, bg='black')
        self.canvas.place(x=200, y=170, width=1150, height=600)

        self.scroll_y = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.scroll_y.pack(side="right", fill="y")

        # Create a frame to hold user data inside the canvas
        self.user_frame = tk.Frame(self.canvas, bg='black')
        self.canvas.create_window((0, 0), window=self.user_frame, anchor="nw")
        self.canvas.config(yscrollcommand=self.scroll_y.set)

        # Fetch users and display
        self.load_user_data()

        # Back Button to go back to Admin Dashboard
        tk.Button(self, text="BACK", font=("Times New Roman", 24, "bold"), command=self.handle_back).place(x=700, y=700, width=170, height=60)

        # Update the scroll region to accommodate all user entries
        self.user_frame.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def load_user_data(self):
        try:
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="gym_python"
            )
            cursor = db_connection.cursor()

            # Query to fetch all users' info (username, promo, expiration date)
            query = """
                SELECT u.username, p.promo_name, DATE_ADD(CURRENT_DATE, INTERVAL p.duration_days DAY) AS expiration_date
                FROM users u
                LEFT JOIN promos p ON u.promo_id = p.promo_id
            """
            cursor.execute(query)
            users = cursor.fetchall()

            # Populate the user data in a table format
            for user in users:
                username, promo_name, expiration_date = user
                user_label = tk.Label(self.user_frame, text=f"{username} | {promo_name if promo_name else 'No Promo'} | {expiration_date}", font=("Times New Roman", 20), bg='black', fg='white')
                user_label.pack(anchor="w", pady=10)

                # View Receipt Button for each user
                view_receipt_button = tk.Button(self.user_frame, text="VIEW RECEIPT", font=("Times New Roman", 18, "bold"),
                                                 command=lambda u=username, p=promo_name: self.open_receipt(u, p))
                view_receipt_button.pack(anchor="w", pady=(0, 0))

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            db_connection.close()

    def open_receipt(self, username, promo):
        # Here you can define the status as needed; for example, you can fetch it from the database or set it to a default value.
        status = "Approved"  # Example status
        receipt_screen = ReceiptScreen(username, promo, status)
        receipt_screen.mainloop()

    def handle_back(self):
        self.destroy()  # Close the ManageUsersScreen
        AdminDashboard().mainloop()  # Open AdminDashboard

# Assuming the ReceiptScreen and AdminDashboard classes are defined elsewhere in your code.

class ReceiptScreen(tk.Tk):
    def __init__(self, username, promo, status):
        super().__init__()
        self.username = username
        self.promo = promo
        self.status = status

        # Set up the Tkinter window
        self.title("Receipt")
        self.geometry("500x700")
        self.configure(bg="white")

        # Create main frame
        main_frame = tk.Frame(self, bg="white")
        main_frame.pack(pady=20)

        # Title Section
        title_label1 = tk.Label(main_frame, text="SHAPE-UP GYM", font=("Times New Roman", 24, "bold"), bg="white", fg="black")
        title_label1.pack()

        title_label2 = tk.Label(main_frame, text="AND FITNESS CENTER", font=("Times New Roman", 24, "bold"), bg="white", fg="black")
        title_label2.pack(pady=15)

        # Receipt Title Section
        receipt_label = tk.Label(main_frame, text="RECEIPT", font=("Times New Roman", 24, "bold"), bg="white", fg="black")
        receipt_label.pack(pady=15)

        # User Info Section
        hello_label = tk.Label(main_frame, text=f"Hello, {self.username}!", font=("Times New Roman", 18, "bold"), bg="white", fg="black")
        hello_label.pack(pady=10)

        promo_label = tk.Label(main_frame, text=f"Promo Availed: {self.promo}", font=("Times New Roman", 18, "bold"), bg="white", fg="black")
        promo_label.pack(pady=10)

        status_label = tk.Label(main_frame, text=f"Status: {self.status}", font=("Times New Roman", 18, "bold"), bg="white", fg="black")
        status_label.pack(pady=10)

        # Date and Receipt Number
        date = datetime.now().strftime("%d/%m/%Y")
        receipt_number = f"No. { random.randint(0, 999999)}"  # Random receipt number

        date_label = tk.Label(main_frame, text=f"Date: {date}", font=("Times New Roman", 14, "bold"), bg="white", fg="black")
        date_label.pack(pady=10)

        receipt_no_label = tk.Label(main_frame, text=f"Receipt {receipt_number}", font=("Times New Roman", 14, "bold"), bg="white", fg="black")
        receipt_no_label.pack(pady=10)

        # Thank You Message
        thank_you_label = tk.Label(main_frame, text="THANK YOU FOR CHOOSING US!", font=("Times New Roman", 20, "bold"), bg="white", fg="black")
        thank_you_label.pack(pady=20)

        # Close Button
        close_button = tk.Button(self, text="CLOSE", font=("Times New Roman", 14), command=self.close_receipt)
        close_button.pack(side=tk.RIGHT, padx=20, pady=20)

    def close_receipt(self):
        self.destroy()  # Close the receipt screen

# User Login Screen
class LoginScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gym Management System")
        self.geometry("1550x850")
        self.configure(bg='black')

        # Title Label
        title_label = tk.Label(
            self, 
            text="SHAPE-UP GYM AND\nFITNESS MANAGEMENT", 
            font=("Times New Roman", 48, "bold"), 
            bg='black', 
            fg='white'
        )
        title_label.pack(pady=(50, 20))

        # Username Field
        tk.Label(self, text="USERNAME", font=("Times New Roman", 24, "bold"), bg='black', fg='white').place(x=690, y=230)
        self.username_entry =tk.Entry(self, font=("Times New Roman", 20), justify=tk.CENTER)
        self.username_entry.place(x=530, y=270, width=500, height=40)

        # Password Field
        tk.Label(self, text="PASSWORD", font=("Times New Roman", 24, "bold"), bg='black', fg='white').place(x=690, y=330)
        self.password_entry = tk.Entry(self, font=("Times New Roman", 20), show="*", justify=tk.CENTER)
        self.password_entry.place(x=530, y=370, width=500, height=40)

        # Login Button
        tk.Button(self, text="LOG IN", font=("Times New Roman", 24, "bold"), command=self.handle_login).place(x=700, y=480, width=170, height=60)


        separator_frame = tk.Frame(self, bg='black', highlightbackground='white', highlightthickness=2)
        separator_frame.place(x=530, y=560, width=500, height=2)

        # Sign Up Button
        self.sign_up_button = tk.Button(self, text="SIGN UP", font=("Times New Roman", 24, "bold"), command=self.handle_signup)
        self.sign_up_button.place(x=700, y=580, width=170, height=60)

        # Admin Button
        self.admin_button = tk.Button(self, text="ADMIN", font=("Times New Roman", 24, "bold"), command=self.handle_admin)
        self.admin_button.place(x=200, y=650, width=170, height=75)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="gym_python"
            )
            cursor = db_connection.cursor()

            # Query to fetch user details and promo info
            query = """
                SELECT u.username, p.promo_name, p.duration_days, p.price 
                FROM users u
                LEFT JOIN promos p ON u.promo_id = p.promo_id
                WHERE u.username = %s AND u.password = %s
            """
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                # Calculate expiration date
                promo_name, duration_days, price = result[1], result[2], result[3]
                expiration_date = datetime.now() + timedelta(days=duration_days) if duration_days else "N/A"
                expiration_date_str = expiration_date.strftime("%Y-%m-%d") if duration_days else "N/A"

                # Open User Dashboard Screen
                self.destroy()  # Close LoginScreen
                UserDashboardScreen(username, promo_name, price, expiration_date_str).mainloop()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            db_connection.close()

    def handle_signup(self):
        self.destroy()  # Close the LoginScreen
        RegisterScreen().mainloop()  # Open the RegisterScreen

    def handle_admin(self):
        self.destroy()  # Close the LoginScreen
        AdminLoginScreen().mainloop()  # Open the AdminLoginScreen

# Register Screen
class RegisterScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Register")
        self.geometry("1550x850")
        self.configure(bg="black")

        # Username Label and Entry
        tk.Label(self, text="USERNAME", font=("Times New Roman", 24, "bold"), bg="black", fg="white").place(x=720, y=150)
        self.username_field = tk.Entry(self, font=("Times New Roman", 24), justify=tk.CENTER)
        self.username_field.place(x=550, y=200, width=500, height=50)

        # Password Label and Entry
        tk.Label(self, text="PASSWORD", font=("Times New Roman", 24, "bold"), bg="black", fg="white").place(x=720, y=250)
        self.password_field = tk.Entry(self, font=("Times New Roman", 24), show="*", justify=tk.CENTER)
        self.password_field.place(x=550, y=300, width=500, height=50)

        # Re-enter Password Label and Entry
        tk.Label(self, text="RE-ENTER PASSWORD", font=("Times New Roman", 24, "bold"), bg="black", fg="white").place(x=630, y=350)
        self.repassword_field = tk.Entry(self, font=("Times New Roman", 24), show="*", justify=tk.CENTER)
        self.repassword_field.place(x=550, y=400, width=500, height=50)

        # Next Button
        tk.Button(self, text="NEXT", font=("Times New Roman",  24, "bold"), bg="white", fg="black", command=self.handle_next).place(x=650, y=550, width=300, height=50)

    def handle_next(self):
        username = self.username_field.get()
        password = self.password_field.get()
        repassword = self.repassword_field.get()

        if password != repassword:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        try:
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="gym_python"
            )
            cursor = db_connection.cursor()

            # Insert new user into the database (no promo_id assigned yet)
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password))
            db_connection.commit()

            messagebox.showinfo("Success", "Registration Successful!")
            self.destroy()  # Close Register Screen
            PromoSelectionScreen(username).mainloop()  # Open PromoSelectionScreen

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            db_connection.close()

# Promo Selection Screen
class PromoSelectionScreen(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title("Choose a Promo")
        self.geometry("1550x850")
        self.configure(bg='black')

        # Title Label
        title_label = tk.Label(
            self, 
            text="CHOOSE A PROMO TO AVAIL", 
            font=("Times New Roman", 48, "bold"), 
            bg='black', 
            fg='white'
        )
        title_label.pack(pady=(50, 20))

        # Promo Buttons in a Frame for better management
        promo_frame = tk.Frame(self, bg='black')
        promo_frame.pack(pady=100)

        # Promo Buttons
        self.promo_buttons = {
            1: tk.Button(promo_frame, text="1 DAY (40 PESOS)", font=("Times New Roman", 24, "bold"), command=lambda: self.highlight_button(1)),
            2: tk.Button(promo_frame, text="7 DAYS (220 PESOS)", font=("Times New Roman", 24, "bold"), command=lambda: self.highlight_button(2)),
            3: tk.Button(promo_frame, text="30 DAYS (950 PESOS)", font=("Times New Roman", 24, "bold"), command=lambda: self.highlight_button(3)),
        }

        # Place buttons in a column within the frame
        for button in self.promo_buttons.values():
            button.pack(pady=20, padx=50, fill="x")

        # Sign Up Button
        sign_up_button = tk.Button(self, text="SIGN UP", font=("Times New Roman", 24, "bold"), command=self.handle_sign_up)
        sign_up_button.pack(pady=50)

        self.selected_promo = None  # No promo selected initially

    def highlight_button(self, promo_id):
        # Reset the background color of all buttons
        for button in self.promo_buttons.values():
            button.config(bg="SystemButtonFace")  # Default button color
        
        # Highlight the selected button
        self.promo_buttons[promo_id].config(bg="yellow")  # Highlight color
        self.selected_promo = promo_id  # Store the selected promo

    def handle_sign_up(self):
        if not self.selected_promo:
            messagebox.showerror("Error", "Please select a promo first!")
            return
        
        try:
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="gym_python"
            )
            cursor = db_connection.cursor()

            # Check if the promo ID exists in the promos table
            query = "SELECT promo_id FROM promos WHERE promo_id = %s"
            cursor.execute(query, (self.selected_promo,))
            if cursor.fetchone():
                # Update the user's promo selection in the database
                query = "UPDATE users SET promo_id = %s WHERE username = %s"
                cursor.execute(query, (self.selected_promo, self.username))
                db_connection.commit()

                messagebox.showinfo("Promo Signup", f"Successfully signed up for Promo {self.selected_promo}!")
                self.destroy()  # Close PromoSelectionScreen
                LoginScreen().mainloop()  # Open the LoginScreen again
            else:
                messagebox.showerror("Error", "Invalid promo ID. Please try again!")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            db_connection.close()

# User Dashboard Screen
class UserDashboardScreen(tk.Tk):
    def __init__(self, username, promo_name, price, expiration_date):
        super().__init__()
        self.username = username
        self.promo_name = promo_name
        self.price = price
        self.expiration_date = expiration_date

        self.title(f"{username}'s Dashboard")
        self.geometry("1550x850")
        self.configure(bg='black')

        # Title Label
        title_label = tk.Label(
            self, 
            text=f"{username}'s DASHBOARD", 
            font=("Times New Roman", 48, "bold"), 
            bg='black', 
            fg='white'
        )
        title_label.pack(pady=(50, 20))

        # Promo Details
        promo_label = tk.Label(
            self, 
            text=f"Promo: {self.promo_name}\nPrice: {self.price}\nExpiration: {self.expiration_date}", 
            font=("Times New Roman", 30, "bold"), 
            bg='black', 
            fg='white'
        )
        promo_label.pack(pady=(50, 20))

        # Log out Button
        tk.Button(self, text="LOG OUT", font=("Times New Roman", 24, "bold"), command=self.handle_logout).place(x=700, y=500, width=170, height=60)

    def handle_logout(self):
        self.destroy()
        LoginScreen().mainloop()

if __name__ == "__main__":
    LoginScreen().mainloop()
