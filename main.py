import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import csv
from datetime import datetime
import matplotlib.pyplot as plt


class MoneySpendingTrackerApp:
    def __init__(self, root):
        self.category_entry = None
        self.date_entry = None
        self.amount_entry = None
        self.root = root
        self.root.title("Money Spending Tracker")

        # Expense List to store data temporarily
        self.expenses = []

        # Setting up the GUI layout
        self.setup_ui()

    def setup_ui(self):
        # Labels and Entry fields for Category, Amount, Date
        tk.Label(self.root, text="Category:").grid(row=0, column=0, padx=5, pady=5)
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Date:").grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = DateEntry(self.root, date_pattern="yyyy-MM-dd")
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        # Buttons for Add, Total, Save, Delete, Budget Table, and Pie Chart
        tk.Button(self.root, text="Add", command=self.add_expense, bg="#4CAF50", fg="white")\
            .grid(row=3, column=0, padx=5, pady=5)

        tk.Button(self.root, text="Total", command=self.show_total, bg="#008CBA", fg="white")\
            .grid(row=3, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Save", command=self.save_to_csv, bg="#FFC107", fg="black")\
            .grid(row=4, column=0, padx=5, pady=5)

        tk.Button(self.root, text="Delete", command=self.delete_last_expense, bg="#F44336", fg="white")\
            .grid(row=4, column=1, padx=5,  pady=5)

        tk.Button(self.root, text="Show Budget", command=self.show_budget_table, bg="#9C27B0", fg="white")\
            .grid(row=5, column=0, columnspan=2, pady=10)

        tk.Button(self.root, text="Show Pie Chart", command=self.show_pie_chart, bg="#FF5722", fg="white")\
            .grid(row=6, column=0, columnspan=2, pady=10)

    def add_expense(self):
        # Fetch data from entries and validate
        category = self.category_entry.get().strip()
        amount = self.amount_entry.get().strip()
        date = self.date_entry.get().strip()

        try:
            # Validate amount
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")

            # Validate date
            datetime.strptime(date, "%Y-%m-%d")

            # Validate category
            if not category:
                raise ValueError("Category cannot be empty.")

            # Add expense to the list
            expense = {"Category": category, "Amount": amount, "Date": date}
            self.expenses.append(expense)
            messagebox.showinfo("Success", "Expense added successfully!")

            # Clear entry fields
            self.category_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
        # (Code for add_expense as in the original)
        pass

    def show_total(self):
        # (Code for show_total as in the original)
        pass

    def save_to_csv(self):
        if not self.expenses:
            messagebox.showwarning("No Data", "No expenses to save.")
            return

        try:
            with open("expenses.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["Category", "Amount", "Date"])
                writer.writeheader()
                writer.writerows(self.expenses)
            messagebox.showinfo("Success", "Expenses saved to expenses.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save expenses: {e}")
        # (Code for save_to_csv as in the original)
        pass

    def delete_last_expense(self):
        # (Code for delete_last_expense as in the original)
        pass

    def show_budget_table(self):
        # Data for the budget
        budget_data = [
            ("Rent", 900, 2200),
            ("Transport", 50, 200),
            ("Food", 300, 500),
            ("Activities", 100, 300),
            ("Miscellaneous", 50, 150),
            ("Total", 1400, 3350),
        ]

        # Create a new window to show the budget table
        table_window = tk.Toplevel(self.root)
        table_window.title("Estimated Budget")

        # Define columns for the Treeview
        columns = ("Category", "Cost (Low)", "Cost (High)")

        # Create the Treeview
        tree = ttk.Treeview(table_window, columns=columns, show="headings")
        tree.heading("Category", text="Category")
        tree.heading("Cost (Low)", text="Cost (Low)")
        tree.heading("Cost (High)", text="Cost (High)")
        tree.column("Category", width=200)
        tree.column("Cost (Low)", width=100, anchor="center")
        tree.column("Cost (High)", width=100, anchor="center")

        # Insert data into the table
        for row in budget_data:
            tree.insert("", tk.END, values=row)

        # Pack the Treeview into the window
        tree.pack(padx=10, pady=10)

        # Add a scrollbar for better navigation (optional)
        scrollbar = ttk.Scrollbar(table_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        pass

    def show_pie_chart(self):
        if not self.expenses:
            messagebox.showwarning("No Data", "No expenses available to display.")
            return

        # Calculate total spending per category
        category_totals = {}
        for expense in self.expenses:
            category_totals[expense["Category"]] = category_totals.get(expense["Category"], 0) + expense["Amount"]

        # Data for the pie chart
        categories = list(category_totals.keys())
        amounts = list(category_totals.values())

        # Generate the pie chart
        fig, ax = plt.subplots()
        ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        ax.set_title("Spending by Category")

        # Display the pie chart
        plt.show()


# Running the application
root = tk.Tk()
app = MoneySpendingTrackerApp(root)
root.mainloop()
