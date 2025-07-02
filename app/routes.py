from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, make_response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, Expense
from collections import defaultdict
from io import StringIO
import csv

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password.')
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            flash('Email already registered.')
            return redirect(url_for('main.register'))

        hashed_pw = generate_password_hash(password, method='sha256')
        new_user = User(name=name, email=email, password=hashed_pw)

        db.session.add(new_user)
        db.session.commit()
        flash('Account created. Please log in.')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    expenses = current_user.expenses
    category_totals = defaultdict(float)
    total_spent = 0.0

    for e in expenses:
        category_totals[e.category] += e.amount
        total_spent += e.amount

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    user_budget = current_user.budget or 1000.0

    return render_template(
        'dashboard.html',
        user=current_user,
        categories=categories,
        amounts=amounts,
        total_spent=total_spent,
        user_budget=user_budget
    )

@main.route('/add-expense', methods=['POST'])
@login_required
def add_expense():
    date = request.form.get('date')
    category = request.form.get('category')
    amount = float(request.form.get('amount'))

    new_expense = Expense(
        date=date,
        category=category,
        amount=amount,
        user_id=current_user.id
    )
    db.session.add(new_expense)
    db.session.commit()
    flash('Expense added!')
    return redirect(url_for('main.dashboard'))

@main.route('/edit-expense/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    if expense.user_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        expense.date = request.form.get('date')
        expense.category = request.form.get('category')
        expense.amount = float(request.form.get('amount'))
        db.session.commit()
        flash('Expense updated.')
        return redirect(url_for('main.dashboard'))

    return render_template('edit_expense.html', expense=expense)

@main.route('/delete-expense/<int:id>', methods=['POST'])
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    if expense.user_id != current_user.id:
        abort(403)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted.')
    return redirect(url_for('main.dashboard'))

@main.route('/set-budget', methods=['POST'])
@login_required
def set_budget():
    new_budget = request.form.get('budget')
    current_user.budget = float(new_budget)
    db.session.commit()
    flash('Budget updated!')
    return redirect(url_for('main.dashboard'))

@main.route('/export-csv')
@login_required
def export_csv():
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(['Date', 'Category', 'Amount'])

    for e in current_user.expenses:
        writer.writerow([e.date, e.category, f'{e.amount:.2f}'])

    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=expenses.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response
