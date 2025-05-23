import json
import os
import datetime
import uuid
import hashlib


class User:
    def __init__(self, username, email, password_hash):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_active = True
        self.created_at = datetime.datetime.now().isoformat()
        self.last_login = self.created_at
    
    def to_dict(self):
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
    def from_dict(cls, data):
        user = cls(data['username'], data['email'], data['password_hash'])
        user.id = data['id']
        user.is_active = data['is_active']
        user.created_at = data['created_at']
        user.last_login = data['last_login']
        return user


class Account:
    def __init__(self, user_id, name, account_type, initial_balance, currency="USD"):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.name = name
        self.type = account_type
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.currency = currency
        self.is_active = True
        self.created_at = datetime.datetime.now().isoformat()
    
    def to_dict(self):
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
    def from_dict(cls, data):
        account = cls(data['user_id'], data['name'], data['type'], 
                     data['initial_balance'], data['currency'])
        account.id = data['id']
        account.current_balance = data['current_balance']
        account.is_active = data['is_active']
        account.created_at = data['created_at']
        return account


class Category:
    def __init__(self, user_id, name, category_type, icon="", color="#000000"):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.name = name
        self.type = category_type
        self.icon = icon
        self.color = color
        self.is_default = False
    
    def to_dict(self):
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
    def from_dict(cls, data):
        category = cls(data['user_id'], data['name'], data['type'], 
                      data['icon'], data['color'])
        category.id = data['id']
        category.is_default = data['is_default']
        return category


class Transaction:
    def __init__(self, account_id, category_id, amount, description="", payment_method=""):
        self.id = str(uuid.uuid4())
        self.account_id = account_id
        self.category_id = category_id
        self.amount = amount
        self.transaction_date = datetime.datetime.now().isoformat()
        self.description = description
        self.is_recurring = False
        self.payment_method = payment_method
    
    def to_dict(self):
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
    def from_dict(cls, data):
        transaction = cls(data['account_id'], data['category_id'], 
                         data['amount'], data['description'], data['payment_method'])
        transaction.id = data['id']
        transaction.transaction_date = data['transaction_date']
        transaction.is_recurring = data['is_recurring']
        return transaction


class Budget:
    def __init__(self, user_id, category_id, name, amount, start_date, end_date):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.category_id = category_id
        self.name = name
        self.amount = amount
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = True
        self.recurrent = 'no'  # 'no', 'monthly', 'quarterly', 'yearly'
        self.notification = 'none'  # 'none', '50', '80', '100'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'name': self.name,
            'amount': self.amount,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'is_active': self.is_active,
            'recurrent': self.recurrent,
            'notification': self.notification
        }
    
    @classmethod
    def from_dict(cls, data):
        budget = cls(data['user_id'], data['category_id'], data['name'],
                    data['amount'], data['start_date'], data['end_date'])
        budget.id = data['id']
        budget.is_active = data['is_active']
        budget.recurrent = data.get('recurrent', 'no')
        budget.notification = data.get('notification', 'none')
        return budget


class DataManager:
    def __init__(self, data_file="finance_data.json"):
        self.data_file = data_file
        self.users = {}
        self.accounts = {}
        self.categories = {}
        self.transactions = {}
        self.budgets = {}
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                
                self.users = {id: User.from_dict(user_data) 
                             for id, user_data in data.get('users', {}).items()}
                self.accounts = {id: Account.from_dict(account_data) 
                               for id, account_data in data.get('accounts', {}).items()}
                self.categories = {id: Category.from_dict(category_data) 
                                 for id, category_data in data.get('categories', {}).items()}
                self.transactions = {id: Transaction.from_dict(transaction_data) 
                                   for id, transaction_data in data.get('transactions', {}).items()}
                self.budgets = {id: Budget.from_dict(budget_data) 
                              for id, budget_data in data.get('budgets', {}).items()}
            except Exception as e:
                print(f"Error loading data: {e}")
    
    def save_data(self):
        try:
            data = {
                'users': {id: user.to_dict() for id, user in self.users.items()},
                'accounts': {id: account.to_dict() for id, account in self.accounts.items()},
                'categories': {id: category.to_dict() for id, category in self.categories.items()},
                'transactions': {id: transaction.to_dict() for id, transaction in self.transactions.items()},
                'budgets': {id: budget.to_dict() for id, budget in self.budgets.items()}
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False


def hash_password(password):
    """Utility function to hash passwords"""
    return hashlib.sha256(password.encode()).hexdigest()