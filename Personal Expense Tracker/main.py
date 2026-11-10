from expenses import ExpenseTracker
from validation import Validation
from datetime import datetime

categories = [
    "food",
    "transport",
    "education",
    "shopping",
    "healthcare",
    "entertainment",
    "bills & utilities",
    "rent",
    "personal care",
    "other"
]

def add_expense(tracker, validator):
    while True:
        print("\n========== ADD NEW EXPENSE ==========")
        title = input("Enter expense title: ")
        is_valid, result = validator.validate_title(title)

        if not is_valid:
            print(result)
            return

        title = result
        amount = input("Enter expense amount: ")
        is_valid, result = validator.validate_amount(amount)

        if not is_valid:
            print(result)
            return

        amount = result
        print("\nAvailable categories:")
        for category in categories:
            print(f"- {category.title()}")

        category = input("Enter expense category: ")
        is_valid, result = validator.validate_category(
            category, categories
        )

        if not is_valid:
            print(result)
            return

        category = result
        tracker.add_expense(title, amount, category)
        print("\nExpense added successfully!")
        tracker.save_data()

        choice = input(
            "Do you want to add another expense? (y/n): "
        )

        if choice.lower() == 'n':
            break

def edit_expense(tracker, validator):
    print("\n========== EDIT EXPENSE ==========")

    # Ask for expense ID
    try:
        expense_id = int(input("Enter expense ID: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    # Ask for new amount
    new_amount = input("Enter new amount: ")

    is_valid, result = validator.validate_amount(new_amount)

    if not is_valid:
        print(result)
        return

    new_amount = result

    # Update expense
    is_updated = tracker.edit_expense(expense_id, new_amount)

    if is_updated:
        tracker.save_data()
        print("Expense updated successfully!")
    else:
        print("Expense ID not found.")
        
def delete_expense(tracker):
    print("\n========== DELETE EXPENSE ==========")

    try:
        expense_id = int(input("Enter expense ID: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    is_deleted = tracker.delete_expense(expense_id)

    if is_deleted:
        tracker.save_data()
        print("Expense deleted successfully!")
    else:
        print("Expense ID not found.")
        
def show_total_expenses(tracker):
    total = tracker.calculate_total()
    print(f"\nTotal Expenses: ৳{total:.2f}")


def show_category_summary(tracker):
    category_totals = tracker.calculate_category_totals()

    if not category_totals:
        print("\nNo expenses recorded yet.")
        return

    print("\n========== CATEGORY SUMMARY ==========")

    for category, total in category_totals.items():
        print(f"{category}: ৳{total:.2f}")
        

def show_monthly_summary(tracker):
    print("\n========== MONTHLY EXPENSE SUMMARY ==========")

    month = input("Enter month (01-12): ").strip()
    year = input("Enter year (e.g. 2026): ").strip()

    if not month.isdigit() or not year.isdigit():
        print("Invalid month or year.")
        return

    if len(month) == 1:
        month = "0" + month

    if len(month) != 2 or not 1 <= int(month) <= 12 or len(year) != 4:
        print("Invalid month or year.")
        return

    total = tracker.calculate_monthly_total(month, year)

    print(f"\nTotal expenses for {year}-{month}: ৳{total:.2f}")
    

def manage_monthly_budget(tracker, validator):
    print("\n========== MONTHLY BUDGET MANAGEMENT ==========")

    month = input("Enter month (01-12): ").strip()
    year = input("Enter year (e.g. 2026): ").strip()

    if not month.isdigit() or not year.isdigit():
        print("Invalid month or year.")
        return

    if len(month) == 1:
        month = "0" + month

    if len(month) != 2 or not 1 <= int(month) <= 12 or len(year) != 4:
        print("Invalid month or year.")
        return

    print("\n1. Set Monthly Budget")
    print("2. View Budget Summary")

    choice = input("Choose an option: ").strip()

    if choice == '1':
        amount = input("Enter monthly budget amount: ")

        is_valid, result = validator.validate_amount(amount)

        if not is_valid:
            print(result)
            return

        tracker.set_monthly_budget(month, year, result)
        tracker.save_data()
        print(f"\nMonthly budget set to ৳{result:.2f} successfully!")

    elif choice == '2':
        budget = tracker.get_monthly_budget(month, year)
        spending = tracker.calculate_monthly_total(month, year)
        remaining = tracker.calculate_remaining_budget(month, year)
        usage = tracker.calculate_budget_usage(month, year)
        status = tracker.get_budget_status(month, year)

        print(f"\n========== BUDGET SUMMARY: {year}-{month} ==========")
        print(f"Monthly Budget: ৳{budget:.2f}")
        print(f"Total Spending: ৳{spending:.2f}")
        print(f"Remaining Budget: ৳{remaining:.2f}")
        print(f"Budget Usage: {usage:.2f}%")
        print(f"Status: {status}")

    else:
        print("Invalid option.")
        
def search_expenses(tracker):
    keyword = input("Enter title or keyword to search: ").strip()

    results = tracker.search_expenses(keyword)

    if not results:
        print("\nNo matching expenses found.")
        return

    print("\n========== SEARCH RESULTS ==========")

    for expense in results:
        print(f"\nID: {expense['id']}")
        print(f"Title: {expense['title']}")
        print(f"Amount: ৳{expense['amount']:.2f}")
        print(f"Category: {expense['category']}")
        print(f"Date: {expense['date']}")
        print("------------------------------------")
        
def filter_expenses_by_category(tracker):
    category = input("Enter category to filter: ").strip()

    results = tracker.filter_by_category(category)

    if not results:
        print("\nNo expenses found in this category.")
        return

    print("\n========== FILTERED EXPENSES ==========")

    for expense in results:
        print(f"\nID: {expense['id']}")
        print(f"Title: {expense['title']}")
        print(f"Amount: ৳{expense['amount']:.2f}")
        print(f"Category: {expense['category']}")
        print(f"Date: {expense['date']}")
        print("--------------------------------------")
        
def filter_expenses_by_date(tracker):
    target_date = input("Enter date (YYYY-MM-DD): ").strip()
    try: 
        datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        print('Invalid Date')
        return 
    results = tracker.filter_by_date(target_date)

    if not results:
        print("\nNo expenses found for this date.")
        return

    print("\n========== DATE FILTER RESULTS ==========")

    for expense in results:
        print(f"\nID: {expense['id']}")
        print(f"Title: {expense['title']}")
        print(f"Amount: ৳{expense['amount']:.2f}")
        print(f"Category: {expense['category']}")
        print(f"Date: {expense['date']}")
        print("----------------------------------------")
        

def filter_expenses_combined(tracker):
    keyword = input("Enter title keyword: ").strip()
    category = input("Enter category: ").strip()
    target_date = input("Enter date (YYYY-MM-DD): ").strip()
    try: 
        datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        print('Invalid Date')
        return 
    
    results = tracker.filter_expenses(
        keyword,
        category,
        target_date
    )

    if not results:
        print("\nNo matching expenses found.")
        return

    print("\n========== COMBINED FILTER RESULTS ==========")

    for expense in results:
        print(f"\nID: {expense['id']}")
        print(f"Title: {expense['title']}")
        print(f"Amount: ৳{expense['amount']:.2f}")
        print(f"Category: {expense['category']}")
        print(f"Date: {expense['date']}")
        print("--------------------------------------------")


def show_comprehensive_report(tracker):
    print("\n========== COMPREHENSIVE EXPENSE REPORT ==========")

    month = input("Enter month (1-12): ").strip()
    year = input("Enter year (YYYY): ").strip()

    # Validate month
    if not month.isdigit() or not 1 <= int(month) <= 12:
        print("Invalid month. Please enter a month from 1 to 12.")
        return

    # Validate year
    if not year.isdigit() or len(year) != 4:
        print("Invalid year. Please enter a four-digit year.")
        return

    month = month.zfill(2)

    # Generate report
    report = tracker.generate_monthly_report(month, year)

    print("\n==============================================")
    print(f"       EXPENSE REPORT - {month}/{year}")
    print("==============================================")

    print(f"Total spending       : ৳{report['total_expenses']:.2f}")
    print(f"Number of expenses   : {report['expense_count']}")
    print(f"Average expense      : ৳{report['average_expense']:.2f}")

    # Highest expense
    print("\n--- Highest Expense ---")

    if report['highest_expense'] is not None:
        highest = report['highest_expense']
        print(f"Title    : {highest['title']}")
        print(f"Category : {highest['category']}")
        print(f"Amount   : ৳{highest['amount']:.2f}")
    else:
        print("No expenses found for this month.")

    # Lowest expense
    print("\n--- Lowest Expense ---")

    if report['lowest_expense'] is not None:
        lowest = report['lowest_expense']
        print(f"Title    : {lowest['title']}")
        print(f"Category : {lowest['category']}")
        print(f"Amount   : ৳{lowest['amount']:.2f}")
    else:
        print("No expenses found for this month.")

    # Category-wise spending
    print("\n--- Category-wise Spending ---")

    if report['category_totals']:
        for category, amount in report['category_totals'].items():
            print(f"{category:<20}: ৳{amount:.2f}")
    else:
        print("No category spending available.")

    # Budget information
    print("\n--- Monthly Budget Analysis ---")

    print(f"Monthly budget       : ৳{report['monthly_budget']:.2f}")
    print(f"Total spending       : ৳{report['total_expenses']:.2f}")
    print(f"Remaining budget     : ৳{report['remaining_budget']:.2f}")
    print(f"Budget usage         : {report['budget_usage']:.2f}%")
    print(f"Budget status        : {report['budget_status']}")

    print("\n==============================================")

def export_expenses_to_csv(tracker):
    print("\n========== EXPORT EXPENSES TO CSV ==========")

    is_exported = tracker.export_to_csv()

    if is_exported:
        print("Expenses exported successfully!")
        print("File location: data/expenses.csv")
    else:
        print("No expenses available to export.")

def display_expenses(tracker):
    if not tracker.expenses:
        print("\nNo expenses recorded yet.")
        return

    print("\n========== EXPENSE LIST ==========")

    for expense in tracker.expenses:
        print(f"\nID: {expense['id']}")
        print(f"Title: {expense['title']}")
        print(f"Amount: ৳{expense['amount']:.2f}")
        print(f"Category: {expense['category']}")
        print(f"Date: {expense['date']}")
        print("----------------------------------")


def main():
    tracker = ExpenseTracker()
    tracker.load_data()
    validator = Validation()

    print("====================================")
    print("Welcome to the Personal Expense Tracker!")
    print("====================================")

    while True:
        print("\n========== MAIN MENU ==========")
        print("1. Add Expense")
        print("2. View All Expenses")
        print('3. Edit Expense')
        print('4. Delete Expense')
        print('5. Show Total Expenses')
        print('6. Show Category-Wise Summary')
        print('7. Show Monthly Summary')
        print('8. Monthly Budget Management')
        print('9. Search Expenses')
        print('10. Filter Expenses by category')
        print('11. Filter Expenses by date')
        print('12. Filter Expenses (Combined)')
        print('13. Show Comprehensive Report')
        print('14. Export to CSV file')
        print("15. Exit")
        print("===============================")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_expense(tracker, validator)
        elif choice == "2":
            display_expenses(tracker)
        elif choice == '3':
            edit_expense(tracker, validator)
        elif choice == '4':
            delete_expense(tracker)
        elif choice == '5':
            show_total_expenses(tracker)
        elif choice == '6':
            show_category_summary(tracker)
        elif choice == '7':
            show_monthly_summary(tracker)
        elif choice == '8':
            manage_monthly_budget(tracker, validator)
        elif choice == '9':
            search_expenses(tracker)
        elif choice == '10':
            filter_expenses_by_category(tracker)
        elif choice == '11':
            filter_expenses_by_date(tracker)
        elif choice == '12':
            filter_expenses_combined(tracker)
        elif choice == '13':
            show_comprehensive_report(tracker)
        elif choice == '14':
            export_expenses_to_csv(tracker)
        elif choice == "15":
            print("\nThank you for using Personal Expense Tracker!")
            print("Goodbye!")
            break
        else:
            print("\nInvalid choice. Please select 1, 2, 3, 4, 5, 6, 7, 8,9,10,11,12,13,14 or 15.")

if __name__ == '__main__':
    main()