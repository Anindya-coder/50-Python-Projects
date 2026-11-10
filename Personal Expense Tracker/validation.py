from datetime import datetime

class Validation:
    @staticmethod
    def validate_amount(amount):
        try:
            amount = float(amount)
            if amount <= 0:
                return False, 'Amount must be greater than zero'
            return True, amount
        except ValueError:
            return False, 'Invalid amount. Please enter a valid number.'
    
    @staticmethod
    def validate_title(title):
        if title.strip() == '':
            return False, 'Title cannot be empty'
        return True, title.strip()
    
    @staticmethod
    def validate_category(category, categories):
        if category.strip().lower() in categories:
            return True, category.strip().title()
        return False, 'Invalid category. Please choose from available categories.'
    
    @staticmethod
    def validate_date(target_date):
        try:
            datetime.strptime(target_date, '%Y-%m-%d')
            return True, target_date

        except ValueError:
            return False, 'Invalid date. Please use YYYY-MM-DD format.'