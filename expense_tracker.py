import csv
from datetime import datetime

expenses = []

def add_expense():
    date = input("Enter the date of the expense (YYYY-MM-DD): ")
    category = input("Enter the category of the expense: ")
    amount = float(input("Enter the amount spent: "))
    description = input("Enter a brief description of the expense: ")

    expense = {
        'date': date,
        'category': category,
        'amount': amount,
        'description': description
    }
    expenses.append(expense)

def view_expenses():
    for expense in expenses:
        if all(key in expense for key in ['date', 'category', 'amount', 'description']):
            print(expense)
        else:
            print("Incomplete expense entry, skipping...")

def set_budget():
    global budget
    budget = float(input("Enter your monthly budget: "))
    total_expenses = 0
    for expense in expenses:
        total_expenses+= expense['amount']
    
    if total_expenses > budget:
        print("You have exceeded your budget!")
    else:
        remaining = budget - total_expenses
        print(f"You have {remaining} left for the month.")

def save_expenses():
    with open('expenses.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['date', 'category', 'amount', 'description'])
        writer.writeheader()
        writer.writerows(expenses)
    print("Expenses saved")

def load_expenses():
    global expenses
    try:
        with open('expenses.csv', mode='r') as file:
            reader = csv.DictReader(file)
            expenses = [row for row in reader]
            for expense in expenses:
                expense['amount'] = float(expense['amount']) 
    except FileNotFoundError:
        print("No previous expenses found.")

def display_menu():
    while True:
        print("\n Menu \n")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Track Budget")
        print("4. Save Expenses")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ")
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            set_budget()
        elif choice == '4':
            save_expenses()
        elif choice == '5':
            save_expenses()
            break
        else:
            print("Invalid choice, please try again.")

load_expenses()
display_menu()