import json
import csv
import os
import datetime
import uuid
from datetime import date
from typing import Dict, List, Optional, Any


class User:
    def __init__(self, username: str, email: str, password_hash: str):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_active = True
        self.created_at = datetime.datetime.now().isoformat()
        self.last_login = self.created_at
    
    def enable_two_factor_auth(self) -> bool:
        # Implementation for enabling 2FA
        print("Two factor authentication enabled")
        return True
    
    def reset_password(self, new_password_hash: str) -> bool:
        # Implementation for password reset
        self.password_hash = new_password_hash
        print("Password has been reset")
        return True
    
    def update_profile(self, **kwargs) -> bool:
        # Update user profile fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        print("Profile updated successfully")
        return True
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'last_login': self.last_login
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        user = cls(data['username'], data['email'], data['password_hash'])
        user.id = data['id']
        user.is_active = data['is_active']
        user.created_at = data['created_at']
        user.last_login = data['last_login']
        return user


class Profile:
    def __init__(self, user_id: str, first_name: str = "", last_name: str = ""):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.preference_theme = "light"
        self.notification_settings = "all"
    
    def update_preferences(self, theme: str = None, notification_settings: str = None) -> bool:
        if theme:
            self.preference_theme = theme
        if notification_settings:
            self.notification_settings = notification_settings
        print("Preferences updated successfully")
        return True
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'preference_theme': self.preference_theme,
            'notification_settings': self.notification_settings
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Profile':
        profile = cls(data['user_id'], data['first_name'], data['last_name'])
        profile.id = data['id']
        profile.preference_theme = data['preference_theme']
        profile.notification_settings = data['notification_settings']
        return profile


class Account:
    def __init__(self, user_id: str, name: str, account_type: str, initial_balance: float, currency: str = "USD"):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.name = name
        self.type = account_type
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.currency = currency
        self.is_active = True
        self.created_at = datetime.datetime.now().isoformat()
    
    def update_balance(self, amount: float) -> bool:
        self.current_balance += amount
        print(f"Balance updated to {self.current_balance} {self.currency}")
        return True
    
    def deactivate(self) -> bool:
        self.is_active = False
        print(f"Account {self.name} has been deactivated")
        return True
    
    def calculate_balance(self, transactions: List['Transaction']) -> float:
        # Recalculate balance based on transactions
        calculated_balance = self.initial_balance
        for transaction in transactions:
            if transaction.account_id == self.id:
                if transaction.amount > 0:  # Income
                    calculated_balance += transaction.amount
                else:  # Expense
                    calculated_balance += transaction.amount  # Amount is negative for expenses
        
        self.current_balance = calculated_balance
        return self.current_balance
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'type': self.type,
            'initial_balance': self.initial_balance,
            'current_balance': self.current_balance,
            'currency': self.currency,
            'is_active': self.is_active,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Account':
        account = cls(data['user_id'], data['name'], data['type'], data['initial_balance'], data['currency'])
        account.id = data['id']
        account.current_balance = data['current_balance']
        account.is_active = data['is_active']
        account.created_at = data['created_at']
        return account


class Category:
    def __init__(self, user_id: str, name: str, category_type: str, icon: str = "", color: str = "#000000"):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.name = name
        self.type = category_type  # income, expense, etc.
        self.icon = icon
        self.color = color
        self.is_default = False
    
    def create_subcategory(self, name: str) -> 'Category':
        # Create a subcategory
        # In a real application, this would likely establish a parent-child relationship
        subcategory = Category(self.user_id, name, self.type, self.icon, self.color)
        print(f"Subcategory {name} created under {self.name}")
        return subcategory
    
    def merge(self, other_category: 'Category') -> bool:
        # Merge another category into this one
        # In a real application, this would move all transactions from other_category to this one
        print(f"Category {other_category.name} merged into {self.name}")
        return True
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'type': self.type,
            'icon': self.icon,
            'color': self.color,
            'is_default': self.is_default
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Category':
        category = cls(data['user_id'], data['name'], data['type'], data['icon'], data['color'])
        category.id = data['id']
        category.is_default = data['is_default']
        return category


class Transaction:
    def __init__(self, account_id: str, category_id: str, amount: float, description: str = "",
                 payment_method: str = ""):
        self.id = str(uuid.uuid4())
        self.account_id = account_id
        self.category_id = category_id
        self.amount = amount
        self.transaction_date = datetime.datetime.now().isoformat()
        self.description = description
        self.is_recurring = False
        self.payment_method = payment_method
    
    def update_details(self, **kwargs) -> bool:
        # Update transaction details
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        print("Transaction details updated")
        return True
    
    def categorize(self, new_category_id: str) -> bool:
        # Change the category of this transaction
        self.category_id = new_category_id
        print(f"Transaction categorized with ID {new_category_id}")
        return True
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'account_id': self.account_id,
            'category_id': self.category_id,
            'amount': self.amount,
            'transaction_date': self.transaction_date,
            'description': self.description,
            'is_recurring': self.is_recurring,
            'payment_method': self.payment_method
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Transaction':
        transaction = cls(
            data['account_id'], 
            data['category_id'], 
            data['amount'], 
            data['description'], 
            data['payment_method']
        )
        transaction.id = data['id']
        transaction.transaction_date = data['transaction_date']
        transaction.is_recurring = data['is_recurring']
        return transaction


class Budget:
    def __init__(self, user_id: str, category_id: str, name: str, amount: float, 
                 start_date: str, end_date: str):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.category_id = category_id
        self.name = name
        self.amount = amount
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = True
    
    def calculate_progress(self, transactions: List[Transaction]) -> float:
        # Calculate how much of the budget has been used
        spent = 0
        for transaction in transactions:
            if (transaction.category_id == self.category_id and 
                transaction.transaction_date >= self.start_date and 
                transaction.transaction_date <= self.end_date):
                spent += abs(transaction.amount) if transaction.amount < 0 else 0
        
        progress = (spent / self.amount) * 100 if self.amount > 0 else 0
        print(f"Budget progress: {progress:.2f}%")
        return progress
    
    def reset(self) -> bool:
        # Reset the budget, perhaps for a new period
        self.start_date = datetime.datetime.now().isoformat()
        # Set end date to one month from now
        end_date = datetime.datetime.now() + datetime.timedelta(days=30)
        self.end_date = end_date.isoformat()
        print(f"Budget {self.name} reset for new period")
        return True
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'name': self.name,
            'amount': self.amount,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'is_active': self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Budget':
        budget = cls(
            data['user_id'],
            data['category_id'],
            data['name'],
            data['amount'],
            data['start_date'],
            data['end_date']
        )
        budget.id = data['id']
        budget.is_active = data['is_active']
        return budget


class FinancialGoal:
    def __init__(self, user_id: str, name: str, description: str, target_amount: float, 
                 start_date: str = None, target_date: str = None, priority: str = "medium"):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.name = name
        self.description = description
        self.target_amount = target_amount
        self.current_amount = 0.0
        self.start_date = start_date or datetime.datetime.now().isoformat()
        self.target_date = target_date
        self.is_achieved = False
        self.priority = priority
    
    def update_progress(self, amount: float) -> float:
        # Update progress towards goal
        self.current_amount += amount
        if self.current_amount >= self.target_amount:
            self.is_achieved = True
            print(f"Goal {self.name} achieved!")
        else:
            progress = (self.current_amount / self.target_amount) * 100
            print(f"Goal progress: {progress:.2f}%")
        return self.current_amount
    
    def calculate_time_left(self) -> int:
        # Calculate days left to reach goal
        if not self.target_date:
            return -1  # No target date set
        
        target = datetime.datetime.fromisoformat(self.target_date)
        now = datetime.datetime.now()
        days_left = (target - now).days
        print(f"Days left to reach goal: {days_left}")
        return days_left
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'target_amount': self.target_amount,
            'current_amount': self.current_amount,
            'start_date': self.start_date,
            'target_date': self.target_date,
            'is_achieved': self.is_achieved,
            'priority': self.priority
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'FinancialGoal':
        goal = cls(
            data['user_id'],
            data['name'],
            data['description'],
            data['target_amount'],
            data['start_date'],
            data['target_date'],
            data['priority']
        )
        goal.id = data['id']
        goal.current_amount = data['current_amount']
        goal.is_achieved = data['is_achieved']
        return goal


class Report:
    def __init__(self, user_id: str, name: str, report_type: str):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.name = name
        self.type = report_type
        self.date_generated = datetime.datetime.now().isoformat()
        self.format = "json"
        self.parameters = {}
    
    def generate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Generate report based on type and parameters
        print(f"Generating {self.type} report: {self.name}")
        report_data = {
            "report_id": self.id,
            "name": self.name,
            "type": self.type,
            "generated_at": self.date_generated,
            "data": data
        }
        return report_data
    
    def export(self, file_path: str, format: str = None) -> bool:
        # Export report to a file
        if format:
            self.format = format
        
        print(f"Exporting report to {file_path} in {self.format} format")
        # Implementation would depend on the format
        return True
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'type': self.type,
            'date_generated': self.date_generated,
            'format': self.format,
            'parameters': self.parameters
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Report':
        report = cls(data['user_id'], data['name'], data['type'])
        report.id = data['id']
        report.date_generated = data['date_generated']
        report.format = data['format']
        report.parameters = data['parameters']
        return report


class Notification:
    def __init__(self, user_id: str, title: str, message: str, notification_type: str = "info"):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.title = title
        self.message = message
        self.type = notification_type
        self.is_read = False
        self.created_at = datetime.datetime.now().isoformat()
    
    def mark_as_read(self) -> bool:
        self.is_read = True
        print(f"Notification {self.title} marked as read")
        return True
    
    def delete(self) -> bool:
        # Mark for deletion
        print(f"Notification {self.title} deleted")
        return True
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'type': self.type,
            'is_read': self.is_read,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Notification':
        notification = cls(data['user_id'], data['title'], data['message'], data['type'])
        notification.id = data['id']
        notification.is_read = data['is_read']
        notification.created_at = data['created_at']
        return notification


class AIRecommendation:
    def __init__(self, user_id: str, title: str, description: str, recommendation_type: str, potential_saving: float = 0.0):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.title = title
        self.description = description
        self.type = recommendation_type
        self.potential_saving = potential_saving
        self.created_at = datetime.datetime.now().isoformat()
        self.is_applied = False
    
    def apply(self) -> bool:
        self.is_applied = True
        print(f"Recommendation {self.title} applied")
        return True
    
    def dismiss(self) -> bool:
        # Mark recommendation as dismissed/ignored
        print(f"Recommendation {self.title} dismissed")
        return True
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'type': self.type,
            'potential_saving': self.potential_saving,
            'created_at': self.created_at,
            'is_applied': self.is_applied
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AIRecommendation':
        recommendation = cls(
            data['user_id'],
            data['title'],
            data['description'],
            data['type'],
            data['potential_saving']
        )
        recommendation.id = data['id']
        recommendation.created_at = data['created_at']
        recommendation.is_applied = data['is_applied']
        return recommendation


class FinanceTracker:
    def __init__(self, data_file: str = "finance_data.json"):
        self.data_file = data_file
        self.users = {}
        self.profiles = {}
        self.accounts = {}
        self.categories = {}
        self.transactions = {}
        self.budgets = {}
        self.goals = {}
        self.reports = {}
        self.notifications = {}
        self.recommendations = {}
        
        # Only load data if file exists, otherwise start with empty collections
        if os.path.exists(self.data_file):
            self.load_data()
        else:
            print(f"No existing data file found. Starting with empty data. A new file will be created at {self.data_file} when you save data.")
    
    def load_data(self) -> bool:
        """Load data from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                
                # Load each data type
                self.users = {id: User.from_dict(user_data) for id, user_data in data.get('users', {}).items()}
                self.profiles = {id: Profile.from_dict(profile_data) for id, profile_data in data.get('profiles', {}).items()}
                self.accounts = {id: Account.from_dict(account_data) for id, account_data in data.get('accounts', {}).items()}
                self.categories = {id: Category.from_dict(category_data) for id, category_data in data.get('categories', {}).items()}
                self.transactions = {id: Transaction.from_dict(transaction_data) for id, transaction_data in data.get('transactions', {}).items()}
                self.budgets = {id: Budget.from_dict(budget_data) for id, budget_data in data.get('budgets', {}).items()}
                self.goals = {id: FinancialGoal.from_dict(goal_data) for id, goal_data in data.get('goals', {}).items()}
                self.reports = {id: Report.from_dict(report_data) for id, report_data in data.get('reports', {}).items()}
                self.notifications = {id: Notification.from_dict(notification_data) for id, notification_data in data.get('notifications', {}).items()}
                self.recommendations = {id: AIRecommendation.from_dict(recommendation_data) for id, recommendation_data in data.get('recommendations', {}).items()}
                
                print(f"Data loaded successfully from {self.data_file}")
                return True
            except Exception as e:
                print(f"Error loading data: {str(e)}")
                return False
        else:
            print(f"Data file {self.data_file} does not exist. Starting with empty data.")
            return False
    
    def save_data(self) -> bool:
        """Save data to JSON file."""
        try:
            data = {
                'users': {id: user.to_dict() for id, user in self.users.items()},
                'profiles': {id: profile.to_dict() for id, profile in self.profiles.items()},
                'accounts': {id: account.to_dict() for id, account in self.accounts.items()},
                'categories': {id: category.to_dict() for id, category in self.categories.items()},
                'transactions': {id: transaction.to_dict() for id, transaction in self.transactions.items()},
                'budgets': {id: budget.to_dict() for id, budget in self.budgets.items()},
                'goals': {id: goal.to_dict() for id, goal in self.goals.items()},
                'reports': {id: report.to_dict() for id, report in self.reports.items()},
                'notifications': {id: notification.to_dict() for id, notification in self.notifications.items()},
                'recommendations': {id: recommendation.to_dict() for id, recommendation in self.recommendations.items()},
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4)
            
            print(f"Data saved successfully to {self.data_file}")
            return True
        except Exception as e:
            print(f"Error saving data: {str(e)}")
            return False
    
    def register_user(self, username: str, email: str, password_hash: str) -> User:
        """Register a new user."""
        # Check if username or email already exists
        for user in self.users.values():
            if user.username == username:
                print("Username already exists")
                return None
            if user.email == email:
                print("Email already exists")
                return None
        
        # Create new user
        user = User(username, email, password_hash)
        self.users[user.id] = user
        
        # Create profile for user
        profile = Profile(user.id)
        self.profiles[profile.id] = profile
        
        # Save data
        self.save_data()
        
        return user
    
    def authenticate_user(self, username_or_email: str, password_hash: str) -> Optional[User]:
        """Authenticate a user."""
        for user in self.users.values():
            if (user.username == username_or_email or user.email == username_or_email) and user.password_hash == password_hash:
                if user.is_active:
                    user.last_login = datetime.datetime.now().isoformat()
                    self.save_data()
                    return user
                else:
                    print("User account is not active")
                    return None
        
        print("Invalid username/email or password")
        return None
    
    def create_account(self, user_id: str, name: str, account_type: str, initial_balance: float, currency: str = "USD") -> Account:
        """Create a new account for a user."""
        if user_id not in [user.id for user in self.users.values()]:
            print("User does not exist")
            return None
        
        account = Account(user_id, name, account_type, initial_balance, currency)
        self.accounts[account.id] = account
        self.save_data()
        
        return account
    
    def create_category(self, user_id: str, name: str, category_type: str, icon: str = "", color: str = "#000000") -> Category:
        """Create a new category for a user."""
        if user_id not in [user.id for user in self.users.values()]:
            print("User does not exist")
            return None
        
        category = Category(user_id, name, category_type, icon, color)
        self.categories[category.id] = category
        self.save_data()
        
        return category
    
    def add_transaction(self, account_id: str, category_id: str, amount: float, description: str = "", payment_method: str = "") -> Transaction:
        """Add a new transaction."""
        if account_id not in self.accounts:
            print("Account does not exist")
            return None
        
        if category_id not in self.categories:
            print("Category does not exist")
            return None
        
        transaction = Transaction(account_id, category_id, amount, description, payment_method)
        self.transactions[transaction.id] = transaction
        
        # Update account balance
        account = self.accounts[account_id]
        account.update_balance(amount)
        
        self.save_data()
        
        return transaction
    
    def create_budget(self, user_id: str, category_id: str, name: str, amount: float, start_date: str, end_date: str) -> Budget:
        """Create a new budget."""
        if user_id not in [user.id for user in self.users.values()]:
            print("User does not exist")
            return None
        
        if category_id not in self.categories:
            print("Category does not exist")
            return None
        
        budget = Budget(user_id, category_id, name, amount, start_date, end_date)
        self.budgets[budget.id] = budget
        self.save_data()
        
        return budget
    
    def create_financial_goal(self, user_id: str, name: str, description: str, target_amount: float, 
                            start_date: str = None, target_date: str = None, priority: str = "medium") -> FinancialGoal:
        """Create a new financial goal."""
        if user_id not in [user.id for user in self.users.values()]:
            print("User does not exist")
            return None
        
        goal = FinancialGoal(user_id, name, description, target_amount, start_date, target_date, priority)
        self.goals[goal.id] = goal
        self.save_data()
        
        return goal
    
    def generate_report(self, user_id: str, name: str, report_type: str, data: Dict[str, Any]) -> Report:
        """Generate a new report."""
        if user_id not in [user.id for user in self.users.values()]:
            print("User does not exist")
            return None
        
        report = Report(user_id, name, report_type)
        report_data = report.generate(data)
        self.reports[report.id] = report
        self.save_data()
        
        return report
    
    def add_notification(self, user_id: str, title: str, message: str, notification_type: str = "info") -> Notification:
        """Add a new notification for a user."""
        if user_id not in [user.id for user in self.users.values()]:
            print("User does not exist")
            return None
        
        notification = Notification(user_id, title, message, notification_type)
        self.notifications[notification.id] = notification
        self.save_data()
        
        return notification
    
    def add_recommendation(self, user_id: str, title: str, description: str, recommendation_type: str, potential_saving: float = 0.0) -> AIRecommendation:
        """Add a new AI recommendation for a user."""
        if user_id not in [user.id for user in self.users.values()]:
            print("User does not exist")
            return None
        
        recommendation = AIRecommendation(user_id, title, description, recommendation_type, potential_saving)
        self.recommendations[recommendation.id] = recommendation
        self.save_data()
        
        return recommendation
    
    def get_user_transactions(self, user_id: str) -> List[Transaction]:
        """Get all transactions for a user."""
        user_accounts = [account.id for account in self.accounts.values() if account.user_id == user_id]
        
        if not user_accounts:
            print("No accounts found for this user")
            return []
        
        user_transactions = [transaction for transaction in self.transactions.values() 
                            if transaction.account_id in user_accounts]
        
        return user_transactions
    
    def get_account_balance(self, account_id: str) -> float:
        """Get the current balance of an account."""
        if account_id not in self.accounts:
            print("Account does not exist")
            return None
        
        account = self.accounts[account_id]
        return account.current_balance
    
    def get_spending_by_category(self, user_id: str, start_date: str = None, end_date: str = None) -> Dict[str, float]:
        """Get spending by category for a user."""
        transactions = self.get_user_transactions(user_id)
        category_spending = {}
        
        for transaction in transactions:
            # Only include expenses (negative amounts)
            if transaction.amount < 0:
                # Check date range if provided
                transaction_date = datetime.datetime.fromisoformat(transaction.transaction_date)
                
                if start_date:
                    start = datetime.datetime.fromisoformat(start_date)
                if transaction_date < start:
                        continue
                
                if end_date:
                    end = datetime.datetime.fromisoformat(end_date)
                    if transaction_date > end:
                        continue
                
                # Add to category total
                category = self.categories[transaction.category_id]
                if category.name not in category_spending:
                    category_spending[category.name] = 0.0
                category_spending[category.name] += abs(transaction.amount)
        
        return category_spending
    
    def get_income_vs_expenses(self, user_id: str, start_date: str = None, end_date: str = None) -> Dict[str, float]:
        """Get total income and expenses for a user."""
        transactions = self.get_user_transactions(user_id)
        totals = {'income': 0.0, 'expenses': 0.0}
        
        for transaction in transactions:
            # Check date range if provided
            transaction_date = datetime.datetime.fromisoformat(transaction.transaction_date)
            
            if start_date:
                start = datetime.datetime.fromisoformat(start_date)
                if transaction_date < start:
                    continue
            
            if end_date:
                end = datetime.datetime.fromisoformat(end_date)
                if transaction_date > end:
                    continue
            
            # Categorize as income or expense
            if transaction.amount > 0:
                totals['income'] += transaction.amount
            else:
                totals['expenses'] += abs(transaction.amount)
        
        return totals
    
    def get_budget_progress(self, user_id: str) -> Dict[str, Dict[str, float]]:
        """Get progress for all budgets of a user."""
        user_budgets = [budget for budget in self.budgets.values() if budget.user_id == user_id]
        progress = {}
        
        for budget in user_budgets:
            if budget.is_active:
                transactions = self.get_user_transactions(user_id)
                progress[budget.name] = {
                    'budget_amount': budget.amount,
                    'spent': 0.0,
                    'remaining': budget.amount,
                    'percentage': 0.0
                }
                
                for transaction in transactions:
                    if (transaction.category_id == budget.category_id and 
                        transaction.amount < 0 and  # Only expenses
                        transaction.transaction_date >= budget.start_date and 
                        transaction.transaction_date <= budget.end_date):
                        progress[budget.name]['spent'] += abs(transaction.amount)
                
                progress[budget.name]['remaining'] = max(0, budget.amount - progress[budget.name]['spent'])
                progress[budget.name]['percentage'] = (progress[budget.name]['spent'] / budget.amount) * 100 if budget.amount > 0 else 0
        
        return progress
    
    def get_goal_progress(self, user_id: str) -> Dict[str, Dict[str, Any]]:
        """Get progress for all financial goals of a user."""
        user_goals = [goal for goal in self.goals.values() if goal.user_id == user_id]
        progress = {}
        
        for goal in user_goals:
            progress[goal.name] = {
                'target_amount': goal.target_amount,
                'current_amount': goal.current_amount,
                'remaining': goal.target_amount - goal.current_amount,
                'percentage': (goal.current_amount / goal.target_amount) * 100 if goal.target_amount > 0 else 0,
                'is_achieved': goal.is_achieved,
                'days_left': goal.calculate_time_left() if goal.target_date else None
            }
        
        return progress
    
    def export_to_csv(self, user_id: str, file_path: str, data_type: str = "transactions") -> bool:
        """Export user data to CSV file."""
        if user_id not in [user.id for user in self.users.values()]:
            print("User does not exist")
            return False
        
        try:
            if data_type == "transactions":
                transactions = self.get_user_transactions(user_id)
                fieldnames = ['id', 'account_id', 'category_id', 'amount', 'transaction_date', 
                            'description', 'is_recurring', 'payment_method']
                
                with open(file_path, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for transaction in transactions:
                        writer.writerow(transaction.to_dict())
                
                print(f"Transactions exported to {file_path}")
                return True
            
            elif data_type == "accounts":
                user_accounts = [account for account in self.accounts.values() if account.user_id == user_id]
                fieldnames = ['id', 'user_id', 'name', 'type', 'initial_balance', 'current_balance', 
                            'currency', 'is_active', 'created_at']
                
                with open(file_path, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for account in user_accounts:
                        writer.writerow(account.to_dict())
                
                print(f"Accounts exported to {file_path}")
                return True
            
            else:
                print(f"Unsupported data type: {data_type}")
                return False
                
        except Exception as e:
            print(f"Error exporting to CSV: {str(e)}")
            return False
    
    def generate_monthly_summary(self, user_id: str, year: int, month: int) -> Dict[str, Any]:
        """Generate a monthly summary report for a user."""
        start_date = datetime.datetime(year, month, 1).isoformat()
        if month == 12:
            end_date = datetime.datetime(year + 1, 1, 1).isoformat()
        else:
            end_date = datetime.datetime(year, month + 1, 1).isoformat()
        
        # Get income vs expenses
        income_expenses = self.get_income_vs_expenses(user_id, start_date, end_date)
        
        # Get spending by category
        spending_by_category = self.get_spending_by_category(user_id, start_date, end_date)
        
        # Get budget progress
        budget_progress = self.get_budget_progress(user_id)
        
        # Get goal progress
        goal_progress = self.get_goal_progress(user_id)
        
        # Get account balances
        account_balances = {
            account.name: account.current_balance 
            for account in self.accounts.values() 
            if account.user_id == user_id
        }
        
        summary = {
            'month': month,
            'year': year,
            'income': income_expenses['income'],
            'expenses': income_expenses['expenses'],
            'net_income': income_expenses['income'] - income_expenses['expenses'],
            'spending_by_category': spending_by_category,
            'budget_progress': budget_progress,
            'goal_progress': goal_progress,
            'account_balances': account_balances,
            'generated_at': datetime.datetime.now().isoformat()
        }
        
        return summary
    
    def delete_user(self, user_id: str) -> bool:
        """Delete a user and all associated data."""
        if user_id not in self.users:
            print("User does not exist")
            return False
        
        # Delete all user-related data
        self.users.pop(user_id, None)
        
        # Delete profiles
        profile_ids = [pid for pid, profile in self.profiles.items() if profile.user_id == user_id]
        for pid in profile_ids:
            self.profiles.pop(pid, None)
        
        # Delete accounts
        account_ids = [aid for aid, account in self.accounts.items() if account.user_id == user_id]
        for aid in account_ids:
            self.accounts.pop(aid, None)
        
        # Delete categories
        category_ids = [cid for cid, category in self.categories.items() if category.user_id == user_id]
        for cid in category_ids:
            self.categories.pop(cid, None)
        
        # Delete transactions for user's accounts
        transaction_ids = [
            tid for tid, transaction in self.transactions.items() 
            if transaction.account_id in account_ids
        ]
        for tid in transaction_ids:
            self.transactions.pop(tid, None)
        
        # Delete budgets
        budget_ids = [bid for bid, budget in self.budgets.items() if budget.user_id == user_id]
        for bid in budget_ids:
            self.budgets.pop(bid, None)
        
        # Delete goals
        goal_ids = [gid for gid, goal in self.goals.items() if goal.user_id == user_id]
        for gid in goal_ids:
            self.goals.pop(gid, None)
        
        # Delete reports
        report_ids = [rid for rid, report in self.reports.items() if report.user_id == user_id]
        for rid in report_ids:
            self.reports.pop(rid, None)
        
        # Delete notifications
        notification_ids = [nid for nid, notification in self.notifications.items() if notification.user_id == user_id]
        for nid in notification_ids:
            self.notifications.pop(nid, None)
        
        # Delete recommendations
        recommendation_ids = [recid for recid, rec in self.recommendations.items() if rec.user_id == user_id]
        for recid in recommendation_ids:
            self.recommendations.pop(recid, None)
        
        self.save_data()
        print(f"User {user_id} and all associated data deleted")
        return True
    
    def backup_data(self, backup_file: str = None) -> bool:
        """Create a backup of the data file."""
        if not backup_file:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"depense_backup_{timestamp}.json"
        
        try:
            with open(self.data_file, 'r') as source:
                with open(backup_file, 'w') as target:
                    target.write(source.read())
            
            print(f"Data backed up to {backup_file}")
            return True
        except Exception as e:
            print(f"Error creating backup: {str(e)}")
            return False
    
    def restore_data(self, backup_file: str) -> bool:
        """Restore data from a backup file."""
        if not os.path.exists(backup_file):
            print("Backup file does not exist")
            return False
        
        try:
            # Create a backup of current data first
            self.backup_data()
            
            # Load the backup data
            with open(backup_file, 'r') as f:
                data = json.load(f)
            
            # Replace current data with backup data
            self.users = {id: User.from_dict(user_data) for id, user_data in data.get('users', {}).items()}
            self.profiles = {id: Profile.from_dict(profile_data) for id, profile_data in data.get('profiles', {}).items()}
            self.accounts = {id: Account.from_dict(account_data) for id, account_data in data.get('accounts', {}).items()}
            self.categories = {id: Category.from_dict(category_data) for id, category_data in data.get('categories', {}).items()}
            self.transactions = {id: Transaction.from_dict(transaction_data) for id, transaction_data in data.get('transactions', {}).items()}
            self.budgets = {id: Budget.from_dict(budget_data) for id, budget_data in data.get('budgets', {}).items()}
            self.goals = {id: FinancialGoal.from_dict(goal_data) for id, goal_data in data.get('goals', {}).items()}
            self.reports = {id: Report.from_dict(report_data) for id, report_data in data.get('reports', {}).items()}
            self.notifications = {id: Notification.from_dict(notification_data) for id, notification_data in data.get('notifications', {}).items()}
            self.recommendations = {id: AIRecommendation.from_dict(recommendation_data) for id, recommendation_data in data.get('recommendations', {}).items()}
            
            # Save the restored data
            self.save_data()
            
            print(f"Data restored from {backup_file}")
            return True
        except Exception as e:
            print(f"Error restoring data: {str(e)}")
            return False
def display_menu(title, options):
    print(f"\n=== {title} ===")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print("0. Back to previous menu" if title != "Main Menu" else "0. Exit")

def get_user_choice(max_option):
    while True:
        try:
            choice = int(input("\nEnter your choice: "))
            if 0 <= choice <= max_option:
                return choice
            print(f"Please enter a number between 0 and {max_option}")
        except ValueError:
            print("Please enter a valid number")

def main():
    print("\n=== Personal Finance Tracker ===")
    print("Welcome to your personal finance management system!")
    
    # Initialize tracker - will use existing file if present
    tracker = FinanceTracker("finance_data.json")
    current_user = None
    
    def display_menu(title, options):
        print(f"\n=== {title} ===")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print("0. Back to previous menu" if title != "Main Menu" else "0. Exit")

    def get_user_choice(max_option):
        while True:
            try:
                choice = input("\nEnter your choice: ")
                if choice == "":
                    continue
                choice = int(choice)
                if 0 <= choice <= max_option:
                    return choice
                print(f"Please enter a number between 0 and {max_option}")
            except ValueError:
                print("Please enter a valid number")

    try:
        while True:
            if current_user is None:
                display_menu("Main Menu", [
                    "Login",
                    "Register",
                    "Exit"
                ])
                choice = get_user_choice(3)
                
                if choice == 1:  # Login
                    username = input("Enter username/email: ")
                    password = input("Enter password: ")
                    current_user = tracker.authenticate_user(username, password)
                    if current_user:
                        print(f"\nWelcome back, {current_user.username}!")
                    else:
                        print("Invalid credentials. Please try again.")
                
                elif choice == 2:  # Register
                    username = input("Choose a username: ")
                    email = input("Enter your email: ")
                    password = input("Choose a password: ")
                    current_user = tracker.register_user(username, email, password)
                    if current_user:
                        print(f"\nAccount created successfully! Welcome, {current_user.username}")
                        tracker.save_data()
                    else:
                        print("Registration failed. Username or email may already exist.")
                
                elif choice == 0:  # Exit
                    print("\nThank you for using the Finance Tracker. Goodbye!")
                    break
            
            else:
                # User is logged in - show main user menu
                display_menu("Dashboard", [
                    "Accounts",
                    "Transactions",
                    "Categories",
                    "Budgets",
                    "Financial Goals",
                    "Reports",
                    "Profile Settings",
                    "Logout"
                ])
                choice = get_user_choice(8)
                
                if choice == 0:  # Logout
                    tracker.save_data()
                    current_user = None
                    print("\nYou have been logged out successfully.")
                    continue
                
                elif choice == 1:  # Accounts
                    while True:
                        user_accounts = [a for a in tracker.accounts.values() if a.user_id == current_user.id]
                        display_menu("Accounts", [
                            "View All Accounts",
                            "Add New Account",
                            "View Account Details",
                            "Update Account Balance"
                        ])
                        sub_choice = get_user_choice(4)
                        
                        if sub_choice == 0:
                            break
                        
                        elif sub_choice == 1:  # View All
                            print("\nYour Accounts:")
                            if not user_accounts:
                                print("No accounts found.")
                                continue
                            for account in user_accounts:
                                print(f"- {account.name}: ${account.current_balance:.2f} ({account.type})")
                        
                        elif sub_choice == 2:  # Add New
                            name = input("Account name: ")
                            acc_type = input("Account type (checking/savings/credit): ")
                            while True:
                                try:
                                    balance = float(input("Initial balance: "))
                                    break
                                except ValueError:
                                    print("Please enter a valid number")
                            currency = input("Currency (USD, EUR, etc.): ") or "USD"
                            tracker.create_account(current_user.id, name, acc_type, balance, currency)
                            tracker.save_data()
                            print("Account created successfully!")
                        
                        elif sub_choice == 3:  # View Details
                            if not user_accounts:
                                print("No accounts found.")
                                continue
                            print("\nYour Accounts:")
                            for i, account in enumerate(user_accounts, 1):
                                print(f"{i}. {account.name}")
                            acc_choice = get_user_choice(len(user_accounts))
                            if acc_choice == 0:
                                continue
                            account = user_accounts[acc_choice-1]
                            print(f"\nAccount Details:")
                            print(f"Name: {account.name}")
                            print(f"Type: {account.type}")
                            print(f"Balance: ${account.current_balance:.2f}")
                            print(f"Currency: {account.currency}")
                            print(f"Created: {account.created_at[:10]}")
                        
                        elif sub_choice == 4:  # Update Balance
                            if not user_accounts:
                                print("No accounts found.")
                                continue
                            print("\nYour Accounts:")
                            for i, account in enumerate(user_accounts, 1):
                                print(f"{i}. {account.name}")
                            acc_choice = get_user_choice(len(user_accounts))
                            if acc_choice == 0:
                                continue
                            account = user_accounts[acc_choice-1]
                            while True:
                                try:
                                    new_balance = float(input("Enter new balance: "))
                                    break
                                except ValueError:
                                    print("Please enter a valid number")
                            account.current_balance = new_balance
                            tracker.save_data()
                            print("Balance updated successfully!")
                
                elif choice == 2:  # Transactions
                    while True:
                        display_menu("Transactions", [
                            "View All Transactions",
                            "Add New Transaction",
                            "View by Category",
                            "View by Account"
                        ])
                        sub_choice = get_user_choice(4)
                        
                        if sub_choice == 0:
                            break
                        
                        elif sub_choice == 1:  # View All
                            transactions = tracker.get_user_transactions(current_user.id)
                            if not transactions:
                                print("No transactions found.")
                                continue
                            print("\nYour Transactions:")
                            for t in transactions[-10:]:  # Show last 10 transactions
                                account = tracker.accounts[t.account_id].name
                                category = tracker.categories[t.category_id].name
                                print(f"- {t.transaction_date[:10]}: {account} | {category} | ${t.amount:.2f} | {t.description}")
                        
                        elif sub_choice == 2:  # Add New
                            user_accounts = [a for a in tracker.accounts.values() if a.user_id == current_user.id]
                            if not user_accounts:
                                print("Please create an account first.")
                                break
                            
                            print("\nAvailable Accounts:")
                            for i, acc in enumerate(user_accounts, 1):
                                print(f"{i}. {acc.name} (${acc.current_balance:.2f})")
                            
                            acc_choice = get_user_choice(len(user_accounts))
                            if acc_choice == 0:
                                continue
                            account = user_accounts[acc_choice-1]
                            
                            user_categories = [c for c in tracker.categories.values() if c.user_id == current_user.id]
                            if not user_categories:
                                print("Please create a category first.")
                                break
                            
                            print("\nAvailable Categories:")
                            for i, cat in enumerate(user_categories, 1):
                                print(f"{i}. {cat.name} ({cat.type})")
                            
                            cat_choice = get_user_choice(len(user_categories))
                            if cat_choice == 0:
                                continue
                            category = user_categories[cat_choice-1]
                            
                            while True:
                                try:
                                    amount = float(input("Amount (positive for income, negative for expense): "))
                                    break
                                except ValueError:
                                    print("Please enter a valid number")
                            description = input("Description: ")
                            method = input("Payment method (optional): ")
                            
                            tracker.add_transaction(account.id, category.id, amount, description, method)
                            tracker.save_data()
                            print("Transaction added successfully!")
                
                elif choice == 7:  # Profile Settings
                    profile = next(p for p in tracker.profiles.values() if p.user_id == current_user.id)
                    
                    while True:
                        display_menu("Profile Settings", [
                            "View Profile",
                            "Update Personal Info",
                            "Change Preferences",
                            "Change Password"
                        ])
                        sub_choice = get_user_choice(4)
                        
                        if sub_choice == 0:
                            break
                        
                        elif sub_choice == 1:  # View Profile
                            print("\nYour Profile:")
                            print(f"Username: {current_user.username}")
                            print(f"Email: {current_user.email}")
                            print(f"Name: {profile.first_name} {profile.last_name}")
                            print(f"Preferences: Theme={profile.preference_theme}, Notifications={profile.notification_settings}")
                        
                        elif sub_choice == 2:  # Update Personal Info
                            first = input(f"First name (current: {profile.first_name}): ") or profile.first_name
                            last = input(f"Last name (current: {profile.last_name}): ") or profile.last_name
                            profile.first_name = first
                            profile.last_name = last
                            tracker.save_data()
                            print("Profile updated successfully!")
                        
                        elif sub_choice == 3:  # Change Preferences
                            theme = input(f"Theme (current: {profile.preference_theme}): ") or profile.preference_theme
                            notifs = input(f"Notifications (current: {profile.notification_settings}): ") or profile.notification_settings
                            profile.update_preferences(theme=theme, notification_settings=notifs)
                            tracker.save_data()
                            print("Preferences updated successfully!")
                        
                        elif sub_choice == 4:  # Change Password
                            current_pass = input("Current password: ")
                            if current_user.password_hash != current_pass:  # Note: In real app, compare hashes
                                print("Incorrect current password")
                                continue
                            
                            new_pass = input("New password: ")
                            confirm = input("Confirm new password: ")
                            
                            if new_pass != confirm:
                                print("Passwords don't match")
                                continue
                            
                            current_user.reset_password(new_pass)
                            tracker.save_data()
                            print("Password changed successfully!")
    
    except KeyboardInterrupt:
        print("\nSaving data before exiting...")
        tracker.save_data()
        print("Data saved successfully. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("Attempting to save data before exiting...")
        tracker.save_data()
        print("Data saved successfully.")

if __name__ == "__main__":
    import datetime
    main()