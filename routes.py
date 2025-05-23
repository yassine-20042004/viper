from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import datetime
from functools import wraps
from models import DataManager, User, Account, Category, Transaction, Budget, hash_password
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize data manager
data_manager = DataManager(app.config['DATA_FILE'])


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    if 'user_id' in session:
        return data_manager.users.get(session['user_id'])
    return None


@app.route('/')
def index():
    # Si l'utilisateur est déjà connecté, ne pas rediriger vers le dashboard
    # Laisser l'utilisateur voir la landing page
    return render_template('landing.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si l'utilisateur est déjà connecté, rediriger vers le dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hash_password(password)
        
        # Find user
        user = None
        for u in data_manager.users.values():
            if (u.username == username or u.email == username) and u.password_hash == password_hash:
                user = u
                break
        
        if user and user.is_active:
            session['user_id'] = user.id
            user.last_login = datetime.datetime.now().isoformat()
            data_manager.save_data()
            flash('Connexion réussie!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Identifiants invalides', 'error')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Si l'utilisateur est déjà connecté, rediriger vers le dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_hash = hash_password(password)
        
        # Check if user exists
        for user in data_manager.users.values():
            if user.username == username or user.email == email:
                flash('Le nom d\'utilisateur ou l\'email existe déjà', 'error')
                return render_template('register.html')
        
        # Create new user
        user = User(username, email, password_hash)
        data_manager.users[user.id] = user
        
        # Create default categories
        default_categories = [
            ('Food & Dining', 'expense', '🍽️', '#FF6B6B'),
            ('Transportation', 'expense', '🚗', '#4ECDC4'),
            ('Shopping', 'expense', '🛍️', '#45B7D1'),
            ('Salary', 'income', '💰', '#96CEB4'),
            ('Other Income', 'income', '💵', '#FECA57')
        ]
        
        for name, cat_type, icon, color in default_categories:
            category = Category(user.id, name, cat_type, icon, color)
            category.is_default = True
            data_manager.categories[category.id] = category
        
        data_manager.save_data()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/dashboard')
@login_required
def dashboard():
    user = get_current_user()
    user_accounts = [a for a in data_manager.accounts.values() if a.user_id == user.id]
    user_transactions = [t for t in data_manager.transactions.values() 
                        if any(t.account_id == acc.id for acc in user_accounts)]
    
    # Calculate totals
    total_balance = sum(acc.current_balance for acc in user_accounts)
    recent_transactions = sorted(user_transactions, 
                               key=lambda x: x.transaction_date, reverse=True)[:5]
    
    # Monthly income/expense
    current_month = datetime.datetime.now().strftime('%Y-%m')
    monthly_income = sum(t.amount for t in user_transactions 
                        if t.amount > 0 and t.transaction_date.startswith(current_month))
    monthly_expense = sum(abs(t.amount) for t in user_transactions 
                         if t.amount < 0 and t.transaction_date.startswith(current_month))
    
    return render_template('dashboard.html', 
                         user=user,
                         accounts=user_accounts,
                         total_balance=total_balance,
                         recent_transactions=recent_transactions,
                         monthly_income=monthly_income,
                         monthly_expense=monthly_expense)


@app.route('/accounts')
@login_required
def accounts():
    user = get_current_user()
    user_accounts = [a for a in data_manager.accounts.values() if a.user_id == user.id]
    return render_template('accounts.html', accounts=user_accounts)


@app.route('/accounts/add', methods=['GET', 'POST'])
@login_required
def add_account():
    if request.method == 'POST':
        user = get_current_user()
        name = request.form['name']
        account_type = request.form['type']
        initial_balance = float(request.form['balance'])
        currency = request.form.get('currency', 'USD')
        
        account = Account(user.id, name, account_type, initial_balance, currency)
        data_manager.accounts[account.id] = account
        data_manager.save_data()
        
        flash('Account created successfully!', 'success')
        return redirect(url_for('accounts'))
    
    return render_template('add_account.html')


@app.route('/transactions')
@login_required
def transactions():
    user = get_current_user()
    user_accounts = [a for a in data_manager.accounts.values() if a.user_id == user.id]
    user_transactions = []
    
    for transaction in data_manager.transactions.values():
        if any(transaction.account_id == acc.id for acc in user_accounts):
            # Add account and category names for display
            transaction.account_name = next((a.name for a in user_accounts 
                                           if a.id == transaction.account_id), 'Unknown')
            transaction.category_name = next((c.name for c in data_manager.categories.values() 
                                            if c.id == transaction.category_id), 'Unknown')
            user_transactions.append(transaction)
    
    user_transactions.sort(key=lambda x: x.transaction_date, reverse=True)
    return render_template('transactions.html', transactions=user_transactions)


@app.route('/transactions/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    user = get_current_user()
    user_accounts = [a for a in data_manager.accounts.values() if a.user_id == user.id]
    user_categories = [c for c in data_manager.categories.values() if c.user_id == user.id]
    
    if request.method == 'POST':
        account_id = request.form['account_id']
        category_id = request.form['category_id']
        amount = float(request.form['amount'])
        description = request.form['description']
        payment_method = request.form.get('payment_method', '')
        
        transaction = Transaction(account_id, category_id, amount, description, payment_method)
        data_manager.transactions[transaction.id] = transaction
        
        # Update account balance
        account = data_manager.accounts[account_id]
        account.current_balance += amount
        
        data_manager.save_data()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('transactions'))
    
    return render_template('add_transaction.html', 
                         accounts=user_accounts, 
                         categories=user_categories)


@app.route('/categories')
@login_required
def categories():
    user = get_current_user()
    user_categories = [c for c in data_manager.categories.values() if c.user_id == user.id]
    return render_template('categories.html', categories=user_categories)


@app.route('/categories/add', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        user = get_current_user()
        name = request.form['name']
        category_type = request.form['type']
        icon = request.form.get('icon', '')
        color = request.form.get('color', '#000000')
        
        category = Category(user.id, name, category_type, icon, color)
        data_manager.categories[category.id] = category
        data_manager.save_data()
        
        flash('Category created successfully!', 'success')
        return redirect(url_for('categories'))
    
    return render_template('add_category.html')


@app.route('/budgets')
@login_required
def budgets():
    user = get_current_user()
    user_budgets = [b for b in data_manager.budgets.values() if b.user_id == user.id]
    
    # Calculate budget progress
    for budget in user_budgets:
        spent = 0
        user_accounts = [a for a in data_manager.accounts.values() if a.user_id == user.id]
        
        # Add category information
        budget.category = next((c for c in data_manager.categories.values() 
                              if c.id == budget.category_id), None)
        
        for transaction in data_manager.transactions.values():
            if (any(transaction.account_id == acc.id for acc in user_accounts) and
                transaction.category_id == budget.category_id and
                transaction.amount < 0 and
                budget.start_date <= transaction.transaction_date <= budget.end_date):
                spent += abs(transaction.amount)
        
        budget.spent = spent
        budget.remaining = max(0, budget.amount - spent)
        budget.progress = (spent / budget.amount) * 100 if budget.amount > 0 else 0
        budget.category_name = next((c.name for c in data_manager.categories.values() 
                                   if c.id == budget.category_id), 'Unknown')
    
    return render_template('budgets.html', budgets=user_budgets)


@app.route('/budgets/add', methods=['GET', 'POST'])
@login_required
def add_budget():
    user = get_current_user()
    user_categories = [c for c in data_manager.categories.values() if c.user_id == user.id]
    
    # Get today's date and end of month for default values
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    end_of_month = (datetime.datetime.now().replace(day=1) + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
    end_of_month = end_of_month.strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        category_id = request.form['category_id']
        amount = float(request.form['amount'])
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        recurrent = request.form.get('recurrent', 'no')
        notification = request.form.get('notification', 'none')
        
        # Use category name as budget name
        category = next((c for c in data_manager.categories.values() if c.id == category_id), None)
        name = f"Budget {category.name}" if category else "Nouveau budget"
        
        budget = Budget(user.id, category_id, name, amount, start_date, end_date)
        budget.recurrent = recurrent
        budget.notification = notification
        data_manager.budgets[budget.id] = budget
        data_manager.save_data()
        
        flash('Budget créé avec succès!', 'success')
        return redirect(url_for('budgets'))
    
    return render_template('add_budget.html', 
                         categories=user_categories,
                         today=today,
                         end_of_month=end_of_month)


@app.route('/budgets/edit/<budget_id>', methods=['GET', 'POST'])
@login_required
def edit_budget(budget_id):
    user = get_current_user()
    budget = data_manager.budgets.get(budget_id)
    if not budget or budget.user_id != user.id:
        flash('Budget introuvable.', 'danger')
        return redirect(url_for('budgets'))

    user_categories = [c for c in data_manager.categories.values() if c.user_id == user.id and c.type == 'expense']

    if request.method == 'POST':
        budget.category_id = request.form['category_id']
        budget.amount = float(request.form['amount'])
        budget.start_date = request.form['start_date']
        budget.end_date = request.form['end_date']
        budget.recurrent = request.form.get('recurrent', 'no')
        budget.notification = request.form.get('notification', 'none')
        data_manager.save_data()
        flash('Budget modifié avec succès!', 'success')
        return redirect(url_for('budgets'))

    return render_template('edit_budget.html', budget=budget, categories=user_categories)


@app.route('/budgets/delete/<budget_id>', methods=['GET'])
@login_required
def delete_budget(budget_id):
    user = get_current_user()
    budget = data_manager.budgets.get(budget_id)
    
    if not budget or budget.user_id != user.id:
        flash('Budget introuvable.', 'danger')
        return redirect(url_for('budgets'))
    
    # Delete the budget
    del data_manager.budgets[budget_id]
    data_manager.save_data()
    
    flash('Budget supprimé avec succès!', 'success')
    return redirect(url_for('budgets'))


@app.route('/logout')
def logout():
    # Clear the entire session
    session.clear()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('index'))


# API endpoints for AJAX requests
@app.route('/api/account_balance/<account_id>')
@login_required
def get_account_balance(account_id):
    account = data_manager.accounts.get(account_id)
    if account and account.user_id == get_current_user().id:
        return jsonify({'balance': account.current_balance})
    return jsonify({'error': 'Account not found'}), 404


@app.route('/api/monthly_data')
@login_required
def get_monthly_data():
    user = get_current_user()
    user_accounts = [a for a in data_manager.accounts.values() if a.user_id == user.id]
    
    monthly_data = {}
    for transaction in data_manager.transactions.values():
        if any(transaction.account_id == acc.id for acc in user_accounts):
            month = transaction.transaction_date[:7]  # YYYY-MM
            if month not in monthly_data:
                monthly_data[month] = {'income': 0, 'expense': 0}
            
            if transaction.amount > 0:
                monthly_data[month]['income'] += transaction.amount
            else:
                monthly_data[month]['expense'] += abs(transaction.amount)
    
    return jsonify(monthly_data)


if __name__ == '__main__':
    app.run(debug=True)