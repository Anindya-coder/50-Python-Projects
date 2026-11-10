from datetime import date 
import json 
import os 
import pandas as pd 

DATA_DIR = "Project by me/Python/Personal Expense Tracker/data"
DATA_FILE = os.path.join(DATA_DIR, "expenses.json")
DATA_FILE_1 = os.path.join(DATA_DIR, "expenses.csv")

class ExpenseTracker: 
    def __init__(self):
        self.expenses = []
        self.next_id = 1
        self.monthly_budgets = {}
        
    def add_expense(self, title, amount, category):
        expense = {
            'id': self.next_id,
            'title': title,
            'amount': amount,
            'category': category,
            'date': date.today().strftime('%Y-%m-%d')
        }
        self.expenses.append(expense)
        self.next_id += 1
        
    def edit_expense(self, expense_id, new_amount):
        for expense in self.expenses:
            if expense['id'] == expense_id:
                expense['amount'] = new_amount
                return True
        
        return False 
    
    def delete_expense(self, expense_id):
        for expense in self.expenses:
            if expense['id'] == expense_id:
                self.expenses.remove(expense)
                return True 
        return False 
    
    def calculate_total (self):
        return sum(expense['amount'] for expense in self.expenses)
    
    def calculate_category_totals(self):
        category_totals = {}
        for expense in self.expenses:
            amount = expense['amount']
            category = expense['category']
            
            category_totals[category] = category_totals.get(category,0)+amount 
        return category_totals
    
    def calculate_monthly_total(self,month,year):
        monthly_total = 0
        for expense in self.expenses:
            expense_month = expense['date'][5:7]
            expense_year = expense['date'][:4]
            
            if expense_month == month and expense_year == year:
                monthly_total += expense['amount']
        return monthly_total
    
    
    def get_monthly_budget(self, month, year):
        budget_key = f"{year}-{month}"
        return self.monthly_budgets.get(budget_key, 0)
    
    
    def calculate_remaining_budget(self, month, year):
        budget = self.get_monthly_budget(month, year)
        spending = self.calculate_monthly_total(month, year)

        remaining = budget - spending

        return remaining

    def calculate_budget_usage(self, month, year):
        budget = self.get_monthly_budget(month, year)

        if budget == 0:
            return 0

        spending = self.calculate_monthly_total(month, year)

        return (spending / budget) * 100


    def get_budget_status(self, month, year):
        usage = self.calculate_budget_usage(month, year)

        if usage >= 100:
            return "Budget exceeded"
        elif usage >= 80:
            return "Warning: You have used 80% or more of your budget."
        else:
            return "Within budget"
    
    def set_monthly_budget(self, month, year, amount):
        budget_key = f"{year}-{month}"
        self.monthly_budgets[budget_key] = amount
        return True

    def save_data(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        
        data = {
            "expenses": self.expenses,
            "next_id": self.next_id,
            "monthly_budgets": self.monthly_budgets
        }

        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

    def load_data(self):
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)

            # Validate JSON structure
            if not isinstance(data, dict):
                raise ValueError("Invalid JSON structure.")

            if not all(key in data for key in
                    ["expenses", "next_id", "monthly_budgets"]):
                raise ValueError("Required data is missing.")

            if not isinstance(data["expenses"], list):
                raise ValueError("Expenses must be a list.")

            if not isinstance(data["next_id"], int):
                raise ValueError("Invalid next_id.")

            if not isinstance(data["monthly_budgets"], dict):
                raise ValueError("Monthly budgets must be a dictionary.")

            # Restore data only after validation
            self.expenses = data["expenses"]
            self.next_id = data["next_id"]
            self.monthly_budgets = data["monthly_budgets"]

            print("Expense data loaded successfully.")

        except FileNotFoundError:
            print("No saved expense data found. Starting fresh.")

        except json.JSONDecodeError:
            print("Error: The expense JSON file is corrupted.")

        except ValueError as error:
            print(f"Invalid expense data: {error}")
            
    def search_expenses(self, keyword):
        matched_expenses = []
        keyword = keyword.lower()
        for expense in self.expenses:
            title = expense['title'].lower()
            if keyword in title:
                matched_expenses.append(expense)
        return matched_expenses
    
    def filter_by_category(self, category):
        filtered_expenses = []
        category = category.lower()
        for expense in self.expenses:
            desired_category = expense['category'].lower()
            if category == desired_category:
                filtered_expenses.append(expense)
        return filtered_expenses
    
    def filter_by_date(self, target_date):
        date_expenses = []
        for expense in self.expenses:
            if target_date == expense['date']:
                date_expenses.append(expense)
        return date_expenses
    
    
    def filter_expenses(self, keyword, category, target_date):
        filtered_expenses = []

        keyword = keyword.lower()
        category = category.lower()

        for expense in self.expenses:

            title = expense['title'].lower()
            expense_category = expense['category'].lower()
            expense_date = expense['date']

            if (keyword in title and
                category == expense_category and
                target_date == expense_date):

                filtered_expenses.append(expense)

        return filtered_expenses
    

    def generate_monthly_report(self, month, year):
        # Get expenses for the selected month
        monthly_expenses = []

        for expense in self.expenses:
            expense_month = expense['date'][5:7]
            expense_year = expense['date'][:4]

            if expense_month == month and expense_year == year:
                monthly_expenses.append(expense)

        # Calculate basic statistics
        total_expenses = sum(
            expense['amount'] for expense in monthly_expenses
        )

        expense_count = len(monthly_expenses)

        if expense_count > 0:
            average_expense = total_expenses / expense_count

            highest_expense = max(
                monthly_expenses,
                key=lambda expense: expense['amount']
            )

            lowest_expense = min(
                monthly_expenses,
                key=lambda expense: expense['amount']
            )
        else:
            average_expense = 0
            highest_expense = None
            lowest_expense = None

        # Calculate category-wise spending
        category_totals = {}

        for expense in monthly_expenses:
            category = expense['category']
            amount = expense['amount']

            category_totals[category] = (
                category_totals.get(category, 0) + amount
            )

        # Get budget information
        monthly_budget = self.get_monthly_budget(month, year)

        remaining_budget = self.calculate_remaining_budget(
            month, year
        )

        budget_usage = self.calculate_budget_usage(month, year)

        budget_status = self.get_budget_status(month, year)

        # Return the complete report
        report = {
            "month": month,
            "year": year,
            "total_expenses": total_expenses,
            "expense_count": expense_count,
            "average_expense": average_expense,
            "highest_expense": highest_expense,
            "lowest_expense": lowest_expense,
            "category_totals": category_totals,
            "monthly_budget": monthly_budget,
            "remaining_budget": remaining_budget,
            "budget_usage": budget_usage,
            "budget_status": budget_status
        }

        return report
    
    def export_to_csv(self):
        if not self.expenses:
            return False 
        
        df = pd.DataFrame(self.expenses)
        df.to_csv(DATA_FILE_1, index=False)
        return True 