from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from .models import Expense, db
from collections import defaultdict

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

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
