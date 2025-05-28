import json
import os
import datetime
import uuid
import hashlib


class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        instance = object.__new__(cls)
        instance.id = data['id']
        instance.created_at = data.get('created_at', datetime.datetime.now().isoformat())
        return instance


class User(BaseModel):
    def __init__(self, username, email, password_hash):
        super().__init__()
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_active = True
        self.last_login = self.created_at
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'is_active': self.is_active,
            'last_login': self.last_login
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        instance = super().from_dict(data)
        instance.username = data['username']
        instance.email = data['email']
        instance.password_hash = data['password_hash']
        instance.is_active = data['is_active']
        instance.last_login = data['last_login']
        return instance


class Account(BaseModel):
    def __init__(self, user_id, name, account_type, initial_balance, currency="EUR"):
        super().__init__()
        self.user_id = user_id
        self.name = name
        self.type = account_type
        self.initial_balance = float(initial_balance)
        self.current_balance = float(initial_balance)
        self.currency = currency
        self.is_active = True
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'user_id': self.user_id,
            'name': self.name,
            'type': self.type,
            'initial_balance': self.initial_balance,
            'current_balance': self.current_balance,
            'currency': self.currency,
            'is_active': self.is_active
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        instance = super().from_dict(data)
        instance.user_id = data['user_id']
        instance.name = data['name']
        instance.type = data['type']
        instance.initial_balance = float(data['initial_balance'])
        instance.current_balance = float(data['current_balance'])
        instance.currency = data['currency']
        instance.is_active = data['is_active']
        return instance


class Category(BaseModel):
    def __init__(self, user_id, name, category_type, icon="", color="#000000"):
        super().__init__()
        self.user_id = user_id
        self.name = name
        self.type = category_type
        self.icon = icon
        self.color = color
        self.is_default = False
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'user_id': self.user_id,
            'name': self.name,
            'type': self.type,
            'icon': self.icon,
            'color': self.color,
            'is_default': self.is_default
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        instance = super().from_dict(data)
        instance.user_id = data['user_id']
        instance.name = data['name']
        instance.type = data['type']
        instance.icon = data['icon']
        instance.color = data['color']
        instance.is_default = data['is_default']
        return instance


class Transaction(BaseModel):
    def __init__(self, account_id, category_id, amount, description="", payment_method=""):
        super().__init__()
        self.account_id = account_id
        self.category_id = category_id
        self.amount = float(amount)
        self.transaction_date = self.created_at
        self.description = description
        self.is_recurring = False
        self.payment_method = payment_method
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'account_id': self.account_id,
            'category_id': self.category_id,
            'amount': self.amount,
            'transaction_date': self.transaction_date,
            'description': self.description,
            'is_recurring': self.is_recurring,
            'payment_method': self.payment_method
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        instance = super().from_dict(data)
        instance.account_id = data['account_id']
        instance.category_id = data['category_id']
        instance.amount = float(data['amount'])
        instance.transaction_date = data['transaction_date']
        instance.description = data['description']
        instance.is_recurring = data['is_recurring']
        instance.payment_method = data['payment_method']
        return instance


class Budget(BaseModel):
    def __init__(self, user_id, category_id, name, amount, start_date, end_date):
        super().__init__()
        self.user_id = user_id
        self.category_id = category_id
        self.name = name
        self.amount = float(amount)
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = True
        self.recurrent = 'no'  # 'no', 'monthly', 'quarterly', 'yearly'
        self.notification = 'none'  # 'none', '50', '80', '100'
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'user_id': self.user_id,
            'category_id': self.category_id,
            'name': self.name,
            'amount': self.amount,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'is_active': self.is_active,
            'recurrent': self.recurrent,
            'notification': self.notification
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        instance = super().from_dict(data)
        instance.user_id = data['user_id']
        instance.category_id = data['category_id']
        instance.name = data['name']
        instance.amount = float(data['amount'])
        instance.start_date = data['start_date']
        instance.end_date = data['end_date']
        instance.is_active = data['is_active']
        instance.recurrent = data.get('recurrent', 'no')
        instance.notification = data.get('notification', 'none')
        return instance


class Notification(BaseModel):
    def __init__(self, user_id, type, message, budget_id=None, read=False):
        super().__init__()
        self.user_id = user_id
        self.type = type  # 'budget_exceeded' or 'budget_warning'
        self.message = message
        self.budget_id = budget_id
        self.read = read
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'user_id': self.user_id,
            'type': self.type,
            'message': self.message,
            'budget_id': self.budget_id,
            'read': self.read
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        instance = super().from_dict(data)
        instance.user_id = data['user_id']
        instance.type = data['type']
        instance.message = data['message']
        instance.budget_id = data.get('budget_id')
        instance.read = data.get('read', False)
        return instance


class DataManager:
    def __init__(self, data_file="data/finance_data.json"):
        self.data_file = data_file
        self.users = {}
        self.accounts = {}
        self.categories = {}
        self.transactions = {}
        self.budgets = {}
        self.notifications = {}
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
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
                self.notifications = {id: Notification.from_dict(notification_data)
                                   for id, notification_data in data.get('notifications', {}).items()}
            except Exception as e:
                print(f"Error loading data: {e}")
    
    def save_data(self):
        try:
            data = {
                'users': {id: user.to_dict() for id, user in self.users.items()},
                'accounts': {id: account.to_dict() for id, account in self.accounts.items()},
                'categories': {id: category.to_dict() for id, category in self.categories.items()},
                'transactions': {id: transaction.to_dict() for id, transaction in self.transactions.items()},
                'budgets': {id: budget.to_dict() for id, budget in self.budgets.items()},
                'notifications': {id: notification.to_dict() for id, notification in self.notifications.items()}
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def check_budget_notifications(self, user_id):
        """Vérifie les budgets et crée des notifications si nécessaire"""
        user_budgets = {id: budget for id, budget in self.budgets.items() 
                       if budget.user_id == user_id and budget.is_active}
        
        for budget_id, budget in user_budgets.items():
            # Calculer le total des dépenses pour ce budget
            category_transactions = [t for t in self.transactions.values() 
                                   if t.category_id == budget.category_id]
            total_spent = sum(abs(t.amount) for t in category_transactions)
            
            # Vérifier si le budget est dépassé
            if total_spent > budget.amount:
                # Créer une notification de budget dépassé
                message = f"Vous avez dépassé votre budget '{budget.name}' de {budget.amount}€"
                notification = Notification(user_id, 'budget_exceeded', message, budget_id)
                self.notifications[notification.id] = notification
            
            # Vérifier les seuils d'alerte
            elif budget.notification != 'none':
                threshold = float(budget.notification) / 100
                if total_spent >= budget.amount * threshold:
                    message = f"Vous avez atteint {budget.notification}% de votre budget '{budget.name}'"
                    notification = Notification(user_id, 'budget_warning', message, budget_id)
                    self.notifications[notification.id] = notification
        
        self.save_data()
    
    def get_user_notifications(self, user_id, unread_only=False):
        """Récupère les notifications d'un utilisateur"""
        notifications = [n for n in self.notifications.values() 
                        if n.user_id == user_id and (not unread_only or not n.read)]
        return sorted(notifications, key=lambda x: x.created_at, reverse=True)
    
    def mark_notification_as_read(self, notification_id):
        """Marque une notification comme lue"""
        if notification_id in self.notifications:
            self.notifications[notification_id].read = True
            self.save_data()
            return True
        return False


def hash_password(password):
    """Utility function to hash passwords"""
    return hashlib.sha256(password.encode()).hexdigest()