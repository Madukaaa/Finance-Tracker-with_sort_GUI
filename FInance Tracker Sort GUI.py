import tkinter as tk
from tkinter import ttk
import json

class FinanceTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("650x650")   #Define the size of the window
        self.root.resizable(False,False)    #Set the resizable to the false
        self.create_widgets()   #Call the create widget function inside of the constructor
        self.transactions = {} #Define the empty transaction dictionary in the constructor
        self.load_transactions("CW_Part_C.json")


    def create_widgets(self):
        # frame for the top search bar and search button
        self.frame_search = tk.Frame(self.root,bg = "#088F8F")
        self.frame_search.pack(ipady = 10, fill = 'x')

        #Frame for the treevire table
        self.frame_table = tk.Frame(self.root, bg = "white")
        self.frame_table.pack(fill = "both", expand = True)

        #Top Lable "Personal Finance tracker"
        search_label = tk.Label(self.frame_search,
                                text = "Personal Finance Tracker",
                                font = ("Helvetica", 23),
                                bg = "#088F8F",
                                fg = "white")
        search_label.pack(side = "left", expand = True) #Pack the lable to the widget

        #Lable "Transaction list"
        label_transactions = tk.Label(self.frame_table,
                                      text = "Transactions List",
                                      font = ("calibri", 18),
                                      bg = "white",
                                      fg = "black")
        label_transactions.pack(ipady = 5)  #Pack the lable to the widget

        # Treeview for displaying transactions
        self.treeview = ttk.Treeview(self.frame_table, height = 25, columns = ("Date", "Category", "Amount"), show = "headings")
        #Style the columns
        self.treeview.column("Date", anchor = 'w', width = 120, minwidth = 100)
        self.treeview.column("Category", anchor = 'w', width = 120, minwidth = 100)
        self.treeview.column("Amount", anchor = 'w', width = 120, minwidth = 100)
        
        #Style the headings and give the click commands to the heading
        self.treeview.heading("Date", text = "Date", command = lambda : self.sort_by_column("Date"))    
        self.treeview.heading("Category", text = "Category", command = lambda : self.sort_by_column("Category"))
        self.treeview.heading("Amount", text = "Amount",  command = lambda : self.sort_by_column("Amount"))
        self.treeview.pack(fill = "x", padx = 20)

        # Scrollbar for the Treeview
        scroll_bar = ttk.Scrollbar(self.treeview, orient = "vertical", command = self.treeview.yview)
        scroll_bar.pack(side = "right", ipady = 50)
        self.treeview.configure(yscrollcommand = scroll_bar.set)    #Configure the scroll bar to scroll through the tree view

        # Search bar and button
        self.search_button = tk.StringVar()
        search_button = ttk.Button(self.frame_search, text = "Search", command = self.search_transactions)
        search_button.pack(side = "right", padx = 25) #Pack the search button

        self.search_bar = ttk.Entry(self.frame_search)
        self.search_bar.pack(side = "right")    #Pack the search bar

        #Reset button
        reset_button = ttk.Button(self.frame_table, text = "Reset", command = self.reset_transactions)
        reset_button.pack(pady = 10)

    def reset_transactions(self):
        self.search_bar.delete(0, 'end')  # Clear the search bar
        self.display_transactions()  # Display all transactions

    def load_transactions(self, file_name):
        try:
            with open(file_name, "r") as f:
                self.transactions = json.load(f)
        except FileNotFoundError:
            self.transactions = {}

    def display_transactions(self):
        #Remove existing entries
        for item in self.treeview.get_children():
            self.treeview.delete(item)
            
        # Add transactions to the treeview
        for category, transactions in self.transactions.items():
            for transaction in transactions:
                self.treeview.insert("", "end", values = (transaction["date"], category, transaction["amount"]))

    def search_transactions(self):
        search = self.search_bar.get().lower()  #Get the input of the search bar

        # Clear the current entries
        self.treeview.delete(*self.treeview.get_children())

        for category,transactions in self.transactions.items():
            for transaction in transactions:\
                # Check if the search string is found in any of the transaction details
                if (search in str(transaction["amount"]).lower() or search in (transaction["date"]).lower() or search in category.lower()):
                    self.treeview.insert("", "end", values =( transaction["date"], category, transaction["amount"]))
                
    def sort_by_column(self, col, reverse=False):
        # Get data from the table
        data = [(self.treeview.set(child, col), child) for child in self.treeview.get_children("")]
        
        # Sort the data
        if col == "Amount":
            data.sort(key=lambda x: float(x[0]), reverse=reverse)
        else:
            data.sort(reverse=reverse)
        
        # Rearrange the rows in the table
        for index, (val, child) in enumerate(data):
            self.treeview.move(child, "", index)
        
        new_reverse = not reverse
        self.treeview.heading(col, command=lambda: self.sort_by_column(col, reverse=new_reverse))

def main():
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    app.display_transactions()
    root.mainloop()

if __name__ == "__main__":
    main()
