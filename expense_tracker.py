import pandas as pd
import hashlib
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime 
from tkinter import *
import tkinter as tk
from tkinter import ttk,messagebox,simpledialog

class LoginWindow:
    def __init__(self, users_filename='users.csv'):
        self.users_filename = users_filename
        self.users=pd.DataFrame(columns=["First Name","Last Name","Username","Email","Password"])
        self.load_users()

        self.root=root
        
        self.show_login_screen()
    def show_login_screen(self):
        self.root.geometry("400x400")
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack()

        tk.Label(self.login_frame, text="Username:").pack(pady=5)
        self.entry_username = tk.Entry(self.login_frame)
        self.entry_username.pack(pady=5)

        tk.Label(self.login_frame, text="Password:").pack(pady=5)
        self.entry_password = tk.Entry(self.login_frame, show="*")
        self.entry_password.pack(pady=5)

        tk.Button(self.login_frame, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.login_frame, text="Register", command=self.show_registration_screen).pack(pady=5)

    def show_registration_screen(self):
        self.login_frame.pack_forget()
        self.registration_frame = tk.Frame(self.root)
        self.registration_frame.pack()

        tk.Label(self.registration_frame, text="First Name:").pack(pady=5)
        self.entry_first_name = tk.Entry(self.registration_frame)
        self.entry_first_name.pack(pady=5)

        tk.Label(self.registration_frame, text="Last Name:").pack(pady=5)
        self.entry_last_name = tk.Entry(self.registration_frame)
        self.entry_last_name.pack(pady=5)

        tk.Label(self.registration_frame, text="Username:").pack(pady=5)
        self.entry_reg_username = tk.Entry(self.registration_frame)
        self.entry_reg_username.pack(pady=5)

        tk.Label(self.registration_frame, text="Email:").pack(pady=5)
        self.entry_email = tk.Entry(self.registration_frame)
        self.entry_email.pack(pady=5)

        tk.Label(self.registration_frame, text="Password:").pack(pady=5)
        self.entry_reg_password = tk.Entry(self.registration_frame, show="*")
        self.entry_reg_password.pack(pady=5)

        tk.Button(self.registration_frame, text="Register", command=self.register).pack(pady=10)
        tk.Button(self.registration_frame, text="Back to Login", command=self.back_to_login).pack(pady=5)

    def register(self):
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()
        username = self.entry_reg_username.get()
        email = self.entry_email.get()
        password = self.entry_reg_password.get()

        if not all([first_name, last_name, username, email, password]):
            messagebox.showerror("Error", "All fields are required.")
            return

        if username in self.users['Username'].values:
            messagebox.showerror("Error", "Username already exists.")
            
            return

        new_user = {
            "First Name": first_name,
            "Last Name": last_name,
            "Username": username,
            "Email": email,
            "Password": password
        }

        self.users = self.users._append(new_user, ignore_index=True)
        self.save_users()
        messagebox.showinfo("Success", "Registration successful! Please log in.")
        self.back_to_login()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        user = self.users[(self.users['Username'] == username) & (self.users['Password'] == password)]

        if not user.empty:
            self.current_user = username
            self.salary = 100000  # Default salary; could be adjusted per user if needed
            self.login_frame.pack_forget()
            Expense_tracker(self.root,username)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def back_to_login(self):
        self.registration_frame.pack_forget()
        self.show_login_screen()

    def load_users(self):
        self.users_filename="users.csv"
        if os.path.exists(self.users_filename):
            self.users = pd.read_csv(self.users_filename)
        else:
            
            self.users = pd.DataFrame(columns=["First Name", "Last Name", "Username", "Email", "Password"])
            self.users.to_csv(self.users_filename,index=False)
        
    def save_users(self):
        self.users.to_csv(self.users_filename, index=False)
class Expense_tracker:
    def __init__(self,root,username,):
        self.username=username
        self.root = root
        self.root.title("Expense Tracker")
        
        self.salary = 100000  # Default salary
        self.filename = 'expenses.csv'
        self.emi_filename = 'emis.csv'
        self.filename= f"{username}_{self.filename}"
        self.emi_filename = f"{username}_{self.emi_filename}"

        # Load existing data
        self.expenses = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
        self.emis = pd.DataFrame(columns=['EMI Name', 'Principal', 'Interest Rate', 'Tenure (Months)', 'Monthly EMI', 'Start Date', 'End Date'])
        self.load_data()
        self.create_widgets()
    def create_widgets(self):
        
    
        self.root.geometry("400x400")
        tk.Button(self.root,text="ADD EXPENSES", command=self.add).grid(row=4,columnspan=2,pady=20,padx=50)
        tk.Button(self.root,text="Add EMI", command=self.addemi).grid(row=5, columnspan=2,pady=20,padx=50)
        tk.Button(self.root,text="VIEW EXPENSES FILE",command=self.view_file).grid(row=6, columnspan=2,pady=20,padx=50)
        tk.Button(self.root,text="VIEW EMIS FILE",command=self.view_emifile).grid(row=7, columnspan=2,pady=20,padx=50)
        # Generate Report Button
        tk.Button(self.root, text="VISUALISATION OF EXPENSES", command=self.visualisation).grid(row=8, columnspan=2,pady=20,padx=50)
        # View Expenses Button
        tk.Button(self.root, text="MODIFY SALARY..?", command=self.modify_salary).grid(row=9500, columnspan=2,pady=20,padx=50)
    def add(self):
        self.root.withdraw()
        self.win=Toplevel(root)
        self.win.title("adding expenses")
        self.win.geometry("400x400")
        tk.Label(self.win, text="Amount:").grid(row=0, column=0,padx=50,pady=20)
        self.entry_amount = tk.Entry(self.win)
        self.entry_amount.grid(row=0, column=1)

        tk.Label(self.win, text="Date (dd-mm-yyyy):").grid(row=1, column=0,padx=50,pady=20)
        self.entry_date = tk.Entry(self.win)
        self.entry_date.grid(row=1, column=1)

        tk.Label(self.win, text="Category:").grid(row=2, column=0,padx=50,pady=20)
        self.combo_category = ttk.Combobox(self.win, values=["Food", "Travel", "Outing", "Shopping"])
        self.combo_category.grid(row=2, column=1)

        tk.Label(self.win, text="Description:").grid(row=3, column=0,padx=50,pady=20)
        self.entry_description = tk.Entry(self.win)
        self.entry_description.grid(row=3, column=1) 
        tk.Button(self.win, text="Add Expense", command=self.add_expense).grid(row=4, columnspan=2,padx=50,pady=20)
        tk.Button(self.win,text="GO BACK",command=self.go_back).grid(row=5,columnspan=2,padx=50,pady=20)
    def go_back(self):
        self.win.withdraw()
        self.root.deiconify()

    def add_expense(self):

        try:
            amount = float(self.entry_amount.get())
            date = datetime.strptime(self.entry_date.get(), "%d-%m-%Y")
            category = self.combo_category.get()
            description = self.entry_description.get()

            new_expense = {'Date': date, 'Category': category, 'Amount': amount, 'Description': description}
            self.expenses = self.expenses._append(new_expense, ignore_index=True)
            self.save_expenses()

            messagebox.showinfo("Success", "Expense added successfully!")
            self.clear_expense_fields()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please check your entries.")

    def clear_expense_fields(self):
        self.entry_amount.delete(0, tk.END)
        self.entry_date.delete(0, tk.END)
        self.combo_category.set('')
        self.entry_description.delete(0, tk.END)
    def addemi(self):
        self.root.withdraw()
        self.win=Toplevel(root)
        self.win.title("Adding emis")
        self.win.geometry("500x500")
        tk.Label(self.win, text="EMI Name:").grid(row=0, column=0,padx=50,pady=20)
        self.entry_emi_name = tk.Entry(self.win)
        self.entry_emi_name.grid(row=0, column=1)

        tk.Label(self.win, text="Principal:").grid(row=1, column=0,padx=50,pady=20)
        self.entry_principal = tk.Entry(self.win)
        self.entry_principal.grid(row=1, column=1)

        tk.Label(self.win, text="Interest Rate (%):").grid(row=2, column=0,padx=50,pady=20)
        self.entry_interest_rate = tk.Entry(self.win)
        self.entry_interest_rate.grid(row=2, column=1)

        tk.Label(self.win, text="Tenure (Months):").grid(row=3, column=0,padx=50,pady=20)
        self.entry_tenure = tk.Entry(self.win)
        self.entry_tenure.grid(row=3, column=1)

        tk.Label(self.win, text="Start Date (dd-mm-yyyy):").grid(row=4, column=0,padx=50,pady=20)
        self.entry_start_date = tk.Entry(self.win)
        self.entry_start_date.grid(row=4, column=1)
        tk.Button(self.win, text="Add EMI", command=self.add_emi).grid(row=5, columnspan=2,padx=50,pady=20)
        tk.Button(self.win,text="GO BACK",command=self.go_back).grid(row=6,columnspan=2,padx=50,pady=20)
        
    def add_emi(self):
        try:        
            emi_name = self.entry_emi_name.get()        
            principal = float(self.entry_principal.get())        
            interest_rate = float(self.entry_interest_rate.get())        
            tenure_months = int(self.entry_tenure.get())
            start_date = self.entry_start_date.get()        
            monthly_rate = interest_rate / (12 * 100)  
            emi_amount = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / ((1 + monthly_rate) ** tenure_months - 1)   
            end_date = datetime.strptime(start_date, '%d-%m-%Y') + pd.DateOffset(months=tenure_months)  \

            new_emi = {
                'EMI Name': emi_name,
                'Principal': principal,
                'Interest Rate': interest_rate,
                'Tenure (Months)': tenure_months,
                'Monthly EMI': round(emi_amount, 2),
                'Start Date': start_date,
                'End Date': end_date.strftime('%d-%m-%Y')
            }

            self.emis = self.emis._append(new_emi, ignore_index=True)
            self.save_emis()

            messagebox.showinfo("Success", f"Added EMI: {emi_name} with Monthly EMI: ${round(emi_amount, 2)}")
            self.clear_emi_fields()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please check your entries.")

    def clear_emi_fields(self):
        self.entry_emi_name.delete(0, tk.END)
        self.entry_principal.delete(0, tk.END)
        self.entry_interest_rate.delete(0, tk.END)
        self.entry_tenure.delete(0, tk.END)
        self.entry_start_date.delete(0, tk.END)
    def generate_report(self):
        total_expenses = self.expenses["Amount"].sum()
        total_emi = self.calculate_total_emi()
        savings = self.salary - total_expenses - total_emi
        report = f"Total Expenses: ${total_expenses:.2f}\nTotal EMIs: ${total_emi:.2f}\nTotal Savings: ${savings:.2f}"
        messagebox.showinfo("Expense Report", report)
    def calculate_total_emi(self):
        return self.emis['Monthly EMI'].sum() if not self.emis.empty else 0

    def view_file(self):
        self.root.withdraw()
        self.win=tk.Toplevel(self.root)
        self.win.title("expenses list")
        
        if self.expenses.empty:
            tk.Label(self.win,text="NO EXPENSES RECORDED").pack()
        else:
            text=tk.Text(self.win,wrap=tk.WORD)
            text.insert(tk.END,self.expenses.to_string(index=False))
            text.pack(expand=True,fill=tk.BOTH)
           # text.grid(row=0,column=0,columnspan=2)
            scrollbar=tk.Scrollbar(self.win,command=text.yview)
            text.config(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
           # scrollbar.grid(row=0,column=2,sticky='ns')
           # tk.Button(self.win,text="GOBACK",command=self.go_back).grid(row=9, columnspan=4,padx=20, pady=20)
        tk.Button(self.win,text="GOBACK",command=self.go_back).pack(pady=20)
            
    def view_emifile(self):
        self.root.withdraw()
        self.win=Toplevel(self.root)
        self.win.title=("emi's list:")
        if self.emis.empty:
            tk.Label(self.win,text="NO EMIS RECOREDED").pack()
        else:
            text=tk.Text(self.win,wrap=tk.WORD)
            text.insert(tk.END,self.emis.to_string(index=False))
            text.pack(expand=True,fill=tk.BOTH)
            scrollbar=tk.Scrollbar(self.win,command=text.yview)
            text.config(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        tk.Button(self.win,text="GOBACK",command=self.go_back).pack(pady=20)
    def emi(self):
     
        current_month = datetime.today().month
        current_year = datetime.today().year
        emi_deduction = self.calculate_monthly_emi(current_month, current_year)
        
        # Calculate monthly salary after EMI deductions
        salary_after_emi = self.salary - emi_deduction
        monthly_expenses = self.expenses[
            (pd.to_datetime(self.expenses['Date'], errors='coerce').dt.month == current_month) &
            (pd.to_datetime(self.expenses['Date'], errors='coerce').dt.year == current_year)
        ]
        total_expenses = monthly_expenses['Amount'].sum()
        remaining_balance = salary_after_emi - total_expenses

        messagebox.showinfo(
            "Monthly EMI Deductions",
            f"Month: {current_month}/{current_year}\n"
            f"Total EMI Deductions: ${emi_deduction:.2f}\n"
            f"Salary After EMI: ${salary_after_emi:.2f}\n"
            f"Total Expenses: ${total_expenses:.2f}\n"
            f"Remaining Balance: ${remaining_balance:.2f}"
        )
    def calculate_monthly_emi(self, month, year):
        """Calculate total EMI deduction for a given month and year."""
        monthly_emi_total = 0
        for _, emi in self.emis.iterrows():
            start_date = datetime.strptime(emi['start_date'], '%d-%m-%Y')
            end_date = datetime.strptime(emi['end_date'], '%d-%m-%Y')
            # EMI is applicable if the date is within the start and end date
            if start_date.year <= year <= end_date.year and (
                start_date.month <= month or start_date.year < year
            ) and (
                end_date.month >= month or end_date.year > year
            ):
                monthly_emi_total += emi['monthly_emi']
        return monthly_emi_total
        
    def save_expenses(self):
        self.expenses.to_csv(self.filename, index=False)

    def save_emis(self):
        self.emis.to_csv(self.emi_filename, index=False)
    def load_data(self):
        try:
            self.expenses = pd.read_csv(self.filename)
        except FileNotFoundError:
            self.expenses = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

        try:
            self.emis = pd.read_csv(self.emi_filename)
        except FileNotFoundError:
            self.emis = pd.DataFrame(columns=['EMI Name', 'Principal', 'Interest Rate', 'Tenure (Months)', 'Monthly EMI', 'Start Date', 'End Date'])
    def visualisation(self):
        self.root.withdraw()
        self.win=Toplevel(root)
        self.win.title("VISUALISATION OF EXPENSES")
        self.win.geometry("400x600")

        tk.Button(self.win,text="TOTAL EXPENSES AND SAVINGS",command=self.generate_report).grid(row=2,padx=20,columnspan=3,pady=20)
        tk.Button(self.win,text="emi overview",command=self.emi).grid(row=3,padx=20,columnspan=3,pady=20)
        tk.Button(self.win, text="Monthly Expense Report", command=self.get_monthly_expenses).grid(row=4, columnspan=3, padx=20, pady=20)
        tk.Button(self.win, text="Yearly Expense Report", command=self.get_yearly_expenses).grid(row=5, columnspan=3, padx=20, pady=20)
        tk.Button(self.win, text="View Category-wise bar chart", command=self.view_category_report).grid(row=6, columnspan=3,padx=20, pady=20)
        tk.Button(self.win, text="category-wise pie_chart ", command=self.pie_chart).grid(row=7, columnspan=3,padx=20, pady=20)
        tk.Button(self.win, text="Average daily expenses based graph", command=self.line_graph).grid(row=8, columnspan=3,padx=20, pady=20)
        tk.Button(self.win, text="monthly expenses graph", command=self.plot_monthly_expenses).grid(row=9, columnspan=3,padx=20, pady=20)
        
        tk.Button(self.win,text="GOBACK",command=self.go_back).grid(row=10, columnspan=4,padx=20, pady=20)
    def plot_monthly_expenses(self):
        try:
            
           
        # Get the year from the input
            self.win.withdraw()
            try:
                df= pd.read_csv(self.filename)
            except FileNotFoundError:
                self.expenses = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

            year = simpledialog.askinteger("Year", "Enter the year (YYYY):")
            if year is None:
                messagebox.showinfo("cancelled","the operation was cancelled")
                
                
            else:
            #   messagebox.showinfo("year",f"you entered:{year}")
          #      win.destroy()
                df['Date']=pd.to_datetime(df['Date'])
                df['Month']= df['Date'].dt.month_name()
                monthly=df.groupby('Month')['Amount'].sum()

                months_order=[
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
                ]
                monthly_expenses=monthly.reindex(months_order)
        # Create a bar plot for monthly expenses
                plt.figure(figsize=(10, 6))
                plt.bar(monthly.index,monthly.values, color='skyblue', edgecolor='black')
                plt.title(f'Monthly Expenses for the Year {year}')
                plt.xlabel('Month')
                plt.ylabel(' Expenses')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
            self.win.deiconify()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid year.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")    
    def get_monthly_expenses(self):
        self.win.withdraw()
        month = simpledialog.askinteger("Month", "Enter the month (MM):")
        if month is None:
            messagebox.showinfo("cancelled","the operation was cancelled")
            self.win.deiconify()
                
        else:
            year = simpledialog.askinteger("Year", "Enter the year (YYYY):")
            if year is None:
                messagebox.showinfo("cancelled","the operation was cancelled")
                self.win.deiconify()
            else:
              #  messagebox.showinfo("month",f"you entered:{month}")
     
                monthly_expenses = self.expenses[
                    (pd.to_datetime(self.expenses['Date'], errors='coerce').dt.month == month) &
                    (pd.to_datetime(self.expenses['Date'], errors='coerce').dt.year == year)]
                total = monthly_expenses['Amount'].sum()
                savings = self.salary - total
                messagebox.showinfo("Monthly Expenses", f"Total Expenses: ${total:.2f}\nSavings: ${savings:.2f}")
                self.win.deiconify()
                
    def get_yearly_expenses(self):
        year = simpledialog.askinteger("Year", "Enter the year:")
        if year is None:
            messagebox.showinfo("cancelled","the operation was cancelled")
            self.win.deiconify()
                
        else:
          #  messagebox.showinfo("year",f"you entered:{year}")
            yearly_expenses = self.expenses[
               pd.to_datetime(self.expenses['Date'], errors='coerce').dt.year == year]
               
            total = yearly_expenses['Amount'].sum()
            savings = 12 * self.salary - total
            messagebox.showinfo("Yearly Expenses", f"Total Expenses: ${total:.2f}\nSavings: ${savings:.2f}")
            self.win.deiconify()
    def view_category_report(self):
        if self.expenses.empty:
            messagebox.showinfo("Info", "No expenses recorded.")
            return

        category_expenses = self.expenses.groupby('Category')['Amount'].sum()
        category_expenses.plot(kind="bar", color="skyblue", edgecolor="black")
        plt.title("Category-wise Expenses")
        plt.xlabel("Category")
        plt.ylabel("Amount ($)")
        plt.tight_layout()
        plt.show()   
    def pie_chart(self):
        """Creates a pie chart for category-wise expenses."""
        if self.expenses.empty:
            messagebox.showinfo("Info", "No expenses recorded.")
            return

        category_expenses = self.expenses.groupby("Category")["Amount"].sum()
        category_expenses.plot(kind="pie", autopct='%1.1f%%')
        plt.title("Category-wise Expenses")
        plt.axis("equal")
        plt.tight_layout()
        plt.show()

    def line_graph(self):
        """Creates a line graph for average daily expenses."""
        if self.expenses.empty:
            messagebox.showinfo("Info", "No expenses recorded.")
            return

        daily_expenses = self.expenses.groupby("Date")["Amount"].mean()
        daily_expenses.plot(kind="line")
        plt.title("Average Daily Expenses")
        plt.xlabel("Date")
        plt.ylabel("Average Amount ($)")
        plt.tight_layout()
        plt.show()


   # def show_plot(self, fig):
    #    """Displays the given matplotlib figure in a new window."""
      #  plot_window = tk.Toplevel(self.root)
     #   plot_window.title("Expense Chart")

       # canvas = FigureCanvasTkAgg(fig, master=plot_window)
        #canvas.draw()
        #canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    def modify_salary(self):
        self.root.withdraw()
    # Create a new pop-up window for salary modification
        self.win = Toplevel(self.root)
        self.win.title("Modify Salary")
        self.win.geometry("300x200")

    # Label and Entry field for entering the new salary
        tk.Label(self.win, text="Enter New Salary:").pack(pady=10)
        self.entry_new_salary = tk.Entry(self.win)
        self.entry_new_salary.pack(pady=10)

    # Button to update the salary
        tk.Button(self.win, text="Update Salary", command=self.update_salary).pack(pady=20)
        tk.Button(self.win,text="GOBACK",command=self.go_back).pack(pady=20)        
    def update_salary(self):
        try:
        # Get the new salary from the input field
            new_salary = float(self.entry_new_salary.get())

        # Update the salary attribute
            self.salary = new_salary

        # Show a confirmation message
            messagebox.showinfo("Success", f"Salary updated to ${self.salary:.2f}")

        # Close the salary window
           # self.salary_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric salary.")
       # tk.Button(self.win,text="GOBACK",command=self.go_back).grid(row=10, columnspan=4,padx=20, pady=2   
        
if __name__=="__main__":
    root=tk.Tk()
    login_window=LoginWindow(root)
    root.mainloop()