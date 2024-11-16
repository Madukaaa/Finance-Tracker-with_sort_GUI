import json
import subprocess
from datetime import datetime

transactions = {} # Define transactions as a dictionary

path = "CW_Part_C.json"

# File handling functi5ons
def load_transactions():
    global transactions# Use global keyword to modify the global transactions variable
    try:
        with open(path, "r") as f:
            transactions = json.load(f)  # Load transactions from the file
    except FileNotFoundError:
        # If the file doesn't exist, initialize an empty dictionary
        transactions = {}

def save_transactions():
    with open(path, "w") as f:
        json.dump(transactions, f, indent = 4)  # Save transactions to the file

def read_bulk_transactions_from_file(filename):
    global transactions# Use global keyword to modify the global transactions variable
    try:
        with open(filename, 'r') as file:
            # Read the first line to determine the category
            first_line = file.readline().strip().split(',')
            if len(first_line) == 3:
                category, amount, date = first_line
                category = category.capitalize()
                amount = float(amount)
                # Check if the category already exists in transactions dictionary
                if category in transactions:
                    transactions[category].append({"amount": amount, "date": date})
                else:
                    # If the category doesn't exist, create a new one
                    transactions[category] = [{"amount": amount, "date": date}]
                    
            # Read subsequent lines and append to the corresponding dictionary
            for line in file:
                line_parts = line.strip().split(',')
                if len(line_parts) == 3:
                    category, amount, date = line_parts
                    # Capitalize the category
                    category = category.capitalize()
                    amount = float(amount)
                    if category in transactions:
                        transactions[category].append({"amount": amount, "date": date})
                    else:
                        transactions[category] = [{"amount": amount, "date": date}]
                else:
                    print("Invalid format in line:", line)
                    
        print("Bulk transactions added successfully.")
        save_transactions()  # Save the updated transactions to the file
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

def add_transaction():
    while True:
        t_name = input("Enter the name of the transaction you want to add: ").capitalize() # Getting the transaction name as a user input
        while True:
            try:
                t_amount = float(input(f"Enter the {t_name} amount: "))  # Getting the amount as a user input and correct conversion to float
                break
            except ValueError:
                print("Invalid amount entered. Please enter a valid number.")
                
        while True: 
            try:
                t_date = input(f"Enter the date you made the above transaction ({t_name}) (YYYY-MM-DD): ") #Getting the date as a user input
                datetime.strptime(t_date, "%Y-%m-%d")#Validate the date format
                break
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

        print("Transaction added successfully")    
        transactions.setdefault(t_name, []).append({"amount": t_amount, "date": t_date})#append the entered values to the dictionary
        break
    save_transactions() # Save the updated transactions to the file

def view_transactions():
    if not transactions:
        print("There are no transactions")
    else:
        count = 1 #Start a counter
        for t_name, sub_transactions in transactions.items(): #Collecting all the data from the dictionary
            print(f"\nTransaction: {t_name}")
            count=1
            
            for sub_transaction in sub_transactions:
                print(f"{count}.amount: {sub_transaction['amount']}, date: {sub_transaction['date']}")
                count+=1 #Increase the counter
                
def update_transactions():
    view_transactions() #calling the view transaction function
    while True:
        if not transactions:       
            view_transactions()
        while True:
                update_name = input("Enter the name of the transaction which you want to update : ").capitalize() #Get the name of the transaction user want to update
                if update_name in transactions:
                    print(f"{update_name} : {transactions[update_name]}")
                    break
                else:
                    print("No transactions")
        while True:
            #Getting the update category as a user input
            update_category = input(f"Enter the category whice you want to update in {update_name} (Amount/Date) : ").capitalize()
            if update_category == "Amount":
                #Getting the transaction index number user wish to update
                try:
                    update_number = int(input("Enter the number of the selected transaction list which you want to update : "))
                    if 0<=update_number<=len(transactions[update_name]): #Check whether the entered index number in range                    
                        try:
                            new_amount = float(input(f"Enter the amount that you have to update in {update_name} : ")) #Getting the new amount as a user input
                            transactions[update_name][update_number-1]['amount'] = new_amount
                            print("Amount updated successfully")#Update the amount
                            break
                        except ValueError:
                            print("Invalid input enter an integer")
                    else:
                        print("Invalid length please try again")
                except:
                    print("Invalid input,Enter integers only")

            elif update_category == "Date":
                #Getting the transaction index number user wish to update
                try:
                    update_number = int(input("Enter the number of the selected transaction list which you want to update : "))
                    if 0<=update_number<=len(transactions[update_name]):#Check whether the entered index number in range
                        try:
                            new_date = input("Enter the new date (YYYY-MM-DD) : ") #Getting the new date as a user input
                            datetime.strptime(new_date,"%Y-%m-%d") #Validating the new date
                            transactions[update_name][update_number-1]['date'] = new_date #Update the date
                            print("Date updated successfully")
                            break
                        except ValueError:
                            print("Invalid Input date (YYYY-MM-DD)")
                    else:
                        print("Invalid Input date (YYYY-MM-DD)")
                except:
                    print("Invalid input,Enter integers only")
            else:
                print("invalid input")
                continue
        break
    
    save_transactions()# Save the updated transactions to the file

def delete_transactions():
    view_transactions()   #calling view transactions function to view transactions
    if not transactions:
        view_transactions()
            
    while True:  #when untill argument is true
        delete_name = input("Enter the name of the transaction you wish to delete : ").capitalize()  #getting the name of transation as a user input
        if delete_name in  transactions:
            print(f"{delete_name} : {transactions[delete_name]}")
            break
        else:
            print("No transactions!")

    while True:
        try:
            delete_number = int(input("Enter the number you wish to delete : ")) #Getting the index of the transaction as a user input
            if 0 <= delete_number <= len(transactions[delete_name]):
                del transactions[delete_name][delete_number-1]#deleting the chosen number
                if len (transactions[delete_name])<1:
                    del transactions[delete_name]
                break
            else:
                print("Invalid input!")
                continue
        except ValueError:
            print("Invalid input ,Enter an integer")
            continue
        break
    print("Delete successfully done !") 
    save_transactions()  # Save the updated transactions to the file

def display_summary():
    view_transactions()#calling the view transaction function
    max_amount=0 #set the max amount to zero
    for category, items in transactions.items():
        for transaction in items:
            if transaction["amount"] > max_amount: #checking the new max amount
                max_amount = transaction["amount"]
                
    print("\nMaximum Transaction Amount: ",max_amount)#printing the max amount

def open_gui():
    try:
        print("Opening G.U.I....")
        subprocess.run(["python", "20230590_CW_C_GUI.py"])
    except FileNotFoundError:
        print("Error: GUI file not found.")
            
def main_menu():
    load_transactions()  # Load transactions at the start
    while True: #creating a loop till the value is true

        #printing the main out put of the code
        print("\nWelcome to Personal Finance Tracker!")
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. Bulk Reading")
        print("3. View Transactions")
        print("4. Update Transaction")
        print("5. Delete Transaction")
        print("6. Display Summary")
        print("7. Open G.U.I")
        print("8. Exit")
        choice = input("Enter your choice: ")
        
        #Conditions
        
        if choice == "1":
            add_transaction()#calling the add function
        elif choice == "2":
            file = input("Enter the file name to read the transactions: ")
            read_bulk_transactions_from_file(file)#calling the read_bulk transaction from file
        elif choice == "3":
            view_transactions()#calling the view function
        elif choice == "4":
            update_transactions()#calling the update function
        elif choice == "5":
            delete_transactions()#calling the delete function 
        elif choice == "6":
            display_summary()#calling the summary function
        elif choice == "7":
            open_gui()  # Call the function to open the GUI
        elif choice == "8": 
            print("\nExiting program.")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()#calling the main function
