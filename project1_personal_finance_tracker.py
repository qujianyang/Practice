"""
Final Project 1: Personal Finance Tracker
A comprehensive personal finance management system with OOP design,
file persistence, exception handling, and data visualization.
"""

import json
import os
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional
import random

class TransactionType(Enum):
    """Transaction types enumeration"""
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"

class Category(Enum):
    """Expense/Income categories"""
    # Income categories
    SALARY = "salary"
    FREELANCE = "freelance"
    INVESTMENT = "investment"
    OTHER_INCOME = "other_income"

    # Expense categories
    FOOD = "food"
    TRANSPORT = "transport"
    UTILITIES = "utilities"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    HEALTH = "health"
    EDUCATION = "education"
    OTHER_EXPENSE = "other_expense"

class FinanceError(Exception):
    """Base exception for finance tracker"""
    pass

class InsufficientFundsError(FinanceError):
    """Raised when account has insufficient funds"""
    pass

class InvalidTransactionError(FinanceError):
    """Raised when transaction is invalid"""
    pass

class Transaction:
    """Represents a financial transaction"""

    def __init__(self, amount: float, transaction_type: TransactionType,
                 category: Category, description: str = "", date: datetime = None):
        if amount <= 0:
            raise InvalidTransactionError("Transaction amount must be positive")

        self.amount = amount
        self.type = transaction_type
        self.category = category
        self.description = description
        self.date = date or datetime.now()
        self.id = self._generate_id()

    def _generate_id(self):
        """Generate unique transaction ID"""
        return f"{self.date.strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"

    def to_dict(self):
        """Convert transaction to dictionary"""
        return {
            'id': self.id,
            'amount': self.amount,
            'type': self.type.value,
            'category': self.category.value,
            'description': self.description,
            'date': self.date.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create transaction from dictionary"""
        transaction = cls(
            amount=data['amount'],
            transaction_type=TransactionType(data['type']),
            category=Category(data['category']),
            description=data['description'],
            date=datetime.fromisoformat(data['date'])
        )
        transaction.id = data['id']
        return transaction

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')} | {self.type.value:8} | ${self.amount:8.2f} | {self.category.value}"

class Account:
    """Represents a financial account"""

    def __init__(self, name: str, initial_balance: float = 0, account_type: str = "checking"):
        self.name = name
        self.balance = initial_balance
        self.account_type = account_type
        self.transactions: List[Transaction] = []
        self.created_at = datetime.now()

    def add_income(self, amount: float, category: Category, description: str = ""):
        """Add income to account"""
        transaction = Transaction(amount, TransactionType.INCOME, category, description)
        self.balance += amount
        self.transactions.append(transaction)
        return transaction

    def add_expense(self, amount: float, category: Category, description: str = ""):
        """Add expense from account"""
        if amount > self.balance:
            raise InsufficientFundsError(f"Insufficient funds: Balance ${self.balance:.2f}, Requested ${amount:.2f}")

        transaction = Transaction(amount, TransactionType.EXPENSE, category, description)
        self.balance -= amount
        self.transactions.append(transaction)
        return transaction

    def get_transactions_by_date_range(self, start_date: datetime, end_date: datetime):
        """Get transactions within date range"""
        return [t for t in self.transactions if start_date <= t.date <= end_date]

    def get_transactions_by_type(self, transaction_type: TransactionType):
        """Get transactions by type"""
        return [t for t in self.transactions if t.type == transaction_type]

    def get_transactions_by_category(self, category: Category):
        """Get transactions by category"""
        return [t for t in self.transactions if t.category == category]

    def to_dict(self):
        """Convert account to dictionary"""
        return {
            'name': self.name,
            'balance': self.balance,
            'account_type': self.account_type,
            'created_at': self.created_at.isoformat(),
            'transactions': [t.to_dict() for t in self.transactions]
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create account from dictionary"""
        account = cls(data['name'], data['balance'], data['account_type'])
        account.created_at = datetime.fromisoformat(data['created_at'])
        account.transactions = [Transaction.from_dict(t) for t in data['transactions']]
        return account

class Budget:
    """Budget management for categories"""

    def __init__(self, month: int, year: int):
        self.month = month
        self.year = year
        self.category_limits: Dict[Category, float] = {}
        self.category_spent: Dict[Category, float] = {}

    def set_limit(self, category: Category, limit: float):
        """Set spending limit for category"""
        if limit <= 0:
            raise ValueError("Budget limit must be positive")
        self.category_limits[category] = limit
        if category not in self.category_spent:
            self.category_spent[category] = 0

    def add_spending(self, category: Category, amount: float):
        """Add spending to category"""
        if category not in self.category_spent:
            self.category_spent[category] = 0
        self.category_spent[category] += amount

    def get_remaining(self, category: Category):
        """Get remaining budget for category"""
        limit = self.category_limits.get(category, 0)
        spent = self.category_spent.get(category, 0)
        return limit - spent

    def is_over_budget(self, category: Category):
        """Check if category is over budget"""
        return self.get_remaining(category) < 0

    def get_budget_status(self):
        """Get status of all budget categories"""
        status = {}
        for category in self.category_limits:
            limit = self.category_limits[category]
            spent = self.category_spent.get(category, 0)
            remaining = limit - spent
            percentage = (spent / limit * 100) if limit > 0 else 0

            status[category.value] = {
                'limit': limit,
                'spent': spent,
                'remaining': remaining,
                'percentage': percentage,
                'over_budget': remaining < 0
            }
        return status

class FinanceTracker:
    """Main finance tracker application"""

    def __init__(self, data_file: str = "finance_data.json"):
        self.data_file = data_file
        self.accounts: Dict[str, Account] = {}
        self.budgets: Dict[str, Budget] = {}  # key: "YYYY-MM"
        self.load_data()

    def create_account(self, name: str, initial_balance: float = 0, account_type: str = "checking"):
        """Create a new account"""
        if name in self.accounts:
            raise ValueError(f"Account '{name}' already exists")

        account = Account(name, initial_balance, account_type)
        self.accounts[name] = account
        self.save_data()
        return account

    def delete_account(self, name: str):
        """Delete an account"""
        if name not in self.accounts:
            raise ValueError(f"Account '{name}' not found")

        del self.accounts[name]
        self.save_data()

    def transfer_between_accounts(self, from_account: str, to_account: str, amount: float):
        """Transfer money between accounts"""
        if from_account not in self.accounts:
            raise ValueError(f"Account '{from_account}' not found")
        if to_account not in self.accounts:
            raise ValueError(f"Account '{to_account}' not found")

        try:
            # Withdraw from source account
            self.accounts[from_account].add_expense(
                amount, Category.OTHER_EXPENSE, f"Transfer to {to_account}"
            )
            # Deposit to destination account
            self.accounts[to_account].add_income(
                amount, Category.OTHER_INCOME, f"Transfer from {from_account}"
            )
            self.save_data()
        except InsufficientFundsError as e:
            raise e

    def set_budget(self, month: int, year: int, category: Category, limit: float):
        """Set budget for a category"""
        key = f"{year:04d}-{month:02d}"
        if key not in self.budgets:
            self.budgets[key] = Budget(month, year)

        self.budgets[key].set_limit(category, limit)
        self.save_data()

    def get_monthly_summary(self, month: int, year: int):
        """Get financial summary for a month"""
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)

        summary = {
            'total_income': 0,
            'total_expenses': 0,
            'net_savings': 0,
            'income_by_category': {},
            'expenses_by_category': {},
            'account_balances': {}
        }

        for account_name, account in self.accounts.items():
            transactions = account.get_transactions_by_date_range(start_date, end_date)

            for transaction in transactions:
                if transaction.type == TransactionType.INCOME:
                    summary['total_income'] += transaction.amount
                    cat = transaction.category.value
                    summary['income_by_category'][cat] = summary['income_by_category'].get(cat, 0) + transaction.amount
                elif transaction.type == TransactionType.EXPENSE:
                    summary['total_expenses'] += transaction.amount
                    cat = transaction.category.value
                    summary['expenses_by_category'][cat] = summary['expenses_by_category'].get(cat, 0) + transaction.amount

            summary['account_balances'][account_name] = account.balance

        summary['net_savings'] = summary['total_income'] - summary['total_expenses']

        # Add budget status if exists
        budget_key = f"{year:04d}-{month:02d}"
        if budget_key in self.budgets:
            summary['budget_status'] = self.budgets[budget_key].get_budget_status()

        return summary

    def generate_report(self, start_date: datetime, end_date: datetime):
        """Generate detailed financial report"""
        report = {
            'period': f"{start_date.date()} to {end_date.date()}",
            'accounts': {},
            'total_income': 0,
            'total_expenses': 0,
            'net_change': 0,
            'top_expenses': [],
            'category_breakdown': {}
        }

        all_transactions = []

        for account_name, account in self.accounts.items():
            transactions = account.get_transactions_by_date_range(start_date, end_date)
            all_transactions.extend(transactions)

            account_income = sum(t.amount for t in transactions if t.type == TransactionType.INCOME)
            account_expenses = sum(t.amount for t in transactions if t.type == TransactionType.EXPENSE)

            report['accounts'][account_name] = {
                'balance': account.balance,
                'income': account_income,
                'expenses': account_expenses,
                'transaction_count': len(transactions)
            }

            report['total_income'] += account_income
            report['total_expenses'] += account_expenses

        report['net_change'] = report['total_income'] - report['total_expenses']

        # Get top expenses
        expense_transactions = [t for t in all_transactions if t.type == TransactionType.EXPENSE]
        expense_transactions.sort(key=lambda x: x.amount, reverse=True)
        report['top_expenses'] = [
            {'amount': t.amount, 'category': t.category.value, 'description': t.description, 'date': t.date.isoformat()}
            for t in expense_transactions[:5]
        ]

        # Category breakdown
        for transaction in all_transactions:
            cat = transaction.category.value
            if cat not in report['category_breakdown']:
                report['category_breakdown'][cat] = {'income': 0, 'expenses': 0}

            if transaction.type == TransactionType.INCOME:
                report['category_breakdown'][cat]['income'] += transaction.amount
            elif transaction.type == TransactionType.EXPENSE:
                report['category_breakdown'][cat]['expenses'] += transaction.amount

        return report

    def visualize_expenses(self, month: int = None, year: int = None):
        """Create simple text-based visualization of expenses"""
        if month and year:
            summary = self.get_monthly_summary(month, year)
            expenses = summary['expenses_by_category']
            title = f"Expenses for {year}-{month:02d}"
        else:
            # Get all-time expenses
            expenses = {}
            for account in self.accounts.values():
                for transaction in account.transactions:
                    if transaction.type == TransactionType.EXPENSE:
                        cat = transaction.category.value
                        expenses[cat] = expenses.get(cat, 0) + transaction.amount
            title = "All-Time Expenses"

        if not expenses:
            print(f"\n{title}: No expenses found")
            return

        # Create bar chart
        print(f"\n{title}")
        print("=" * 60)

        max_amount = max(expenses.values())
        max_bar_width = 40

        for category, amount in sorted(expenses.items(), key=lambda x: x[1], reverse=True):
            bar_width = int((amount / max_amount) * max_bar_width)
            bar = "█" * bar_width
            print(f"{category:15} {bar} ${amount:,.2f}")

        print("=" * 60)
        print(f"Total: ${sum(expenses.values()):,.2f}")

    def save_data(self):
        """Save all data to file"""
        try:
            data = {
                'accounts': {name: acc.to_dict() for name, acc in self.accounts.items()},
                'budgets': {
                    key: {
                        'month': budget.month,
                        'year': budget.year,
                        'limits': {cat.value: limit for cat, limit in budget.category_limits.items()},
                        'spent': {cat.value: spent for cat, spent in budget.category_spent.items()}
                    }
                    for key, budget in self.budgets.items()
                }
            }

            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)

            print(f"Data saved to {self.data_file}")

        except Exception as e:
            raise FinanceError(f"Failed to save data: {e}")

    def load_data(self):
        """Load data from file"""
        if not os.path.exists(self.data_file):
            print(f"No existing data file found. Starting fresh.")
            return

        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)

            # Load accounts
            for name, acc_data in data.get('accounts', {}).items():
                self.accounts[name] = Account.from_dict(acc_data)

            # Load budgets
            for key, budget_data in data.get('budgets', {}).items():
                budget = Budget(budget_data['month'], budget_data['year'])
                for cat_str, limit in budget_data.get('limits', {}).items():
                    budget.category_limits[Category(cat_str)] = limit
                for cat_str, spent in budget_data.get('spent', {}).items():
                    budget.category_spent[Category(cat_str)] = spent
                self.budgets[key] = budget

            print(f"Data loaded from {self.data_file}")

        except Exception as e:
            print(f"Warning: Failed to load data: {e}")
            print("Starting with empty data.")

class FinanceTrackerCLI:
    """Command-line interface for finance tracker"""

    def __init__(self):
        self.tracker = FinanceTracker()
        self.running = True

    def run(self):
        """Run the CLI application"""
        print("\n" + "="*60)
        print("PERSONAL FINANCE TRACKER")
        print("="*60)

        while self.running:
            self.show_menu()
            choice = input("\nEnter your choice: ").strip()
            self.handle_choice(choice)

    def show_menu(self):
        """Display main menu"""
        print("\n--- Main Menu ---")
        print("1. Account Management")
        print("2. Add Transaction")
        print("3. View Reports")
        print("4. Budget Management")
        print("5. Visualize Expenses")
        print("6. Save and Exit")

    def handle_choice(self, choice):
        """Handle menu choice"""
        try:
            if choice == "1":
                self.account_management()
            elif choice == "2":
                self.add_transaction()
            elif choice == "3":
                self.view_reports()
            elif choice == "4":
                self.budget_management()
            elif choice == "5":
                self.visualize_expenses()
            elif choice == "6":
                self.tracker.save_data()
                print("Goodbye!")
                self.running = False
            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            print(f"Error: {e}")

    def account_management(self):
        """Manage accounts"""
        print("\n--- Account Management ---")
        print("1. Create Account")
        print("2. View Accounts")
        print("3. Transfer Between Accounts")
        print("4. Delete Account")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Account name: ").strip()
            balance = float(input("Initial balance: $"))
            acc_type = input("Account type (checking/savings): ").strip() or "checking"

            account = self.tracker.create_account(name, balance, acc_type)
            print(f"Account '{name}' created successfully!")

        elif choice == "2":
            if not self.tracker.accounts:
                print("No accounts found.")
            else:
                print("\nYour Accounts:")
                for name, account in self.tracker.accounts.items():
                    print(f"  {name} ({account.account_type}): ${account.balance:,.2f}")

        elif choice == "3":
            if len(self.tracker.accounts) < 2:
                print("Need at least 2 accounts for transfer.")
                return

            from_acc = input("From account: ").strip()
            to_acc = input("To account: ").strip()
            amount = float(input("Amount: $"))

            self.tracker.transfer_between_accounts(from_acc, to_acc, amount)
            print(f"Transferred ${amount:.2f} from {from_acc} to {to_acc}")

        elif choice == "4":
            name = input("Account name to delete: ").strip()
            self.tracker.delete_account(name)
            print(f"Account '{name}' deleted.")

    def add_transaction(self):
        """Add a transaction"""
        if not self.tracker.accounts:
            print("Please create an account first.")
            return

        print("\n--- Add Transaction ---")

        # Select account
        print("Available accounts:")
        accounts = list(self.tracker.accounts.keys())
        for i, name in enumerate(accounts, 1):
            print(f"{i}. {name}")

        acc_idx = int(input("Select account: ")) - 1
        account_name = accounts[acc_idx]
        account = self.tracker.accounts[account_name]

        # Transaction type
        print("\n1. Income")
        print("2. Expense")
        trans_type = input("Transaction type: ").strip()

        # Category
        if trans_type == "1":
            categories = [c for c in Category if "INCOME" in c.value.upper() or c.value == "salary" or c.value == "freelance" or c.value == "investment"]
        else:
            categories = [c for c in Category if "EXPENSE" in c.value.upper() or c.value in ["food", "transport", "utilities", "entertainment", "shopping", "health", "education"]]

        print("\nCategories:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat.value}")

        cat_idx = int(input("Select category: ")) - 1
        category = categories[cat_idx]

        # Amount and description
        amount = float(input("Amount: $"))
        description = input("Description (optional): ").strip()

        # Add transaction
        if trans_type == "1":
            transaction = account.add_income(amount, category, description)
        else:
            transaction = account.add_expense(amount, category, description)

        print(f"Transaction added: {transaction}")

        # Update budget if expense
        if trans_type == "2":
            now = datetime.now()
            budget_key = f"{now.year:04d}-{now.month:02d}"
            if budget_key in self.tracker.budgets:
                self.tracker.budgets[budget_key].add_spending(category, amount)

        self.tracker.save_data()

    def view_reports(self):
        """View financial reports"""
        print("\n--- View Reports ---")
        print("1. Monthly Summary")
        print("2. Custom Period Report")
        print("3. Account Transactions")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            month = int(input("Month (1-12): "))
            year = int(input("Year: "))

            summary = self.tracker.get_monthly_summary(month, year)

            print(f"\n=== Monthly Summary for {year}-{month:02d} ===")
            print(f"Total Income: ${summary['total_income']:,.2f}")
            print(f"Total Expenses: ${summary['total_expenses']:,.2f}")
            print(f"Net Savings: ${summary['net_savings']:,.2f}")

            if summary['income_by_category']:
                print("\nIncome by Category:")
                for cat, amount in summary['income_by_category'].items():
                    print(f"  {cat}: ${amount:,.2f}")

            if summary['expenses_by_category']:
                print("\nExpenses by Category:")
                for cat, amount in summary['expenses_by_category'].items():
                    print(f"  {cat}: ${amount:,.2f}")

            if 'budget_status' in summary:
                print("\nBudget Status:")
                for cat, status in summary['budget_status'].items():
                    symbol = "⚠️" if status['over_budget'] else "✓"
                    print(f"  {symbol} {cat}: ${status['spent']:.2f} / ${status['limit']:.2f} ({status['percentage']:.1f}%)")

        elif choice == "2":
            start_date = datetime.strptime(input("Start date (YYYY-MM-DD): "), "%Y-%m-%d")
            end_date = datetime.strptime(input("End date (YYYY-MM-DD): "), "%Y-%m-%d")

            report = self.tracker.generate_report(start_date, end_date)

            print(f"\n=== Financial Report ===")
            print(f"Period: {report['period']}")
            print(f"Total Income: ${report['total_income']:,.2f}")
            print(f"Total Expenses: ${report['total_expenses']:,.2f}")
            print(f"Net Change: ${report['net_change']:,.2f}")

            if report['top_expenses']:
                print("\nTop Expenses:")
                for exp in report['top_expenses']:
                    print(f"  ${exp['amount']:,.2f} - {exp['category']} - {exp['description']}")

        elif choice == "3":
            if not self.tracker.accounts:
                print("No accounts found.")
                return

            print("Available accounts:")
            accounts = list(self.tracker.accounts.keys())
            for i, name in enumerate(accounts, 1):
                print(f"{i}. {name}")

            acc_idx = int(input("Select account: ")) - 1
            account = self.tracker.accounts[accounts[acc_idx]]

            print(f"\n=== Transactions for {accounts[acc_idx]} ===")
            print(f"Current Balance: ${account.balance:,.2f}")
            print("\nRecent Transactions:")

            for transaction in account.transactions[-10:]:
                print(f"  {transaction}")

    def budget_management(self):
        """Manage budgets"""
        print("\n--- Budget Management ---")
        print("1. Set Budget")
        print("2. View Budget Status")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            month = int(input("Month (1-12): "))
            year = int(input("Year: "))

            categories = [c for c in Category if "EXPENSE" in c.value.upper() or c.value in ["food", "transport", "utilities", "entertainment", "shopping", "health", "education"]]

            print("\nCategories:")
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat.value}")

            cat_idx = int(input("Select category: ")) - 1
            category = categories[cat_idx]

            limit = float(input("Budget limit: $"))

            self.tracker.set_budget(month, year, category, limit)
            print(f"Budget set for {category.value}: ${limit:.2f}")

        elif choice == "2":
            month = int(input("Month (1-12): "))
            year = int(input("Year: "))

            budget_key = f"{year:04d}-{month:02d}"
            if budget_key not in self.tracker.budgets:
                print("No budget set for this month.")
                return

            budget = self.tracker.budgets[budget_key]
            status = budget.get_budget_status()

            print(f"\n=== Budget Status for {year}-{month:02d} ===")
            for cat, info in status.items():
                symbol = "⚠️" if info['over_budget'] else "✓"
                bar_width = int((info['percentage'] / 100) * 30)
                bar = "█" * bar_width + "░" * (30 - bar_width)

                print(f"\n{cat}:")
                print(f"  {symbol} {bar} {info['percentage']:.1f}%")
                print(f"  Spent: ${info['spent']:.2f} / Limit: ${info['limit']:.2f}")
                print(f"  Remaining: ${info['remaining']:.2f}")

    def visualize_expenses(self):
        """Visualize expenses"""
        print("\n--- Visualize Expenses ---")
        print("1. Current Month")
        print("2. Specific Month")
        print("3. All Time")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            now = datetime.now()
            self.tracker.visualize_expenses(now.month, now.year)
        elif choice == "2":
            month = int(input("Month (1-12): "))
            year = int(input("Year: "))
            self.tracker.visualize_expenses(month, year)
        elif choice == "3":
            self.tracker.visualize_expenses()

def demo_mode():
    """Run demo mode with sample data"""
    print("\n" + "="*60)
    print("PERSONAL FINANCE TRACKER - DEMO MODE")
    print("="*60)

    tracker = FinanceTracker("demo_finance.json")

    # Create accounts
    print("\nCreating demo accounts...")
    checking = tracker.create_account("Checking", 5000, "checking")
    savings = tracker.create_account("Savings", 10000, "savings")

    # Add sample transactions
    print("Adding sample transactions...")

    # Add income
    checking.add_income(3000, Category.SALARY, "Monthly salary")
    checking.add_income(500, Category.FREELANCE, "Web design project")

    # Add expenses
    checking.add_expense(1200, Category.UTILITIES, "Rent payment")
    checking.add_expense(450, Category.FOOD, "Groceries")
    checking.add_expense(100, Category.TRANSPORT, "Gas and parking")
    checking.add_expense(200, Category.ENTERTAINMENT, "Movies and dining")
    checking.add_expense(150, Category.SHOPPING, "Clothing")

    # Set budgets
    now = datetime.now()
    tracker.set_budget(now.month, now.year, Category.FOOD, 500)
    tracker.set_budget(now.month, now.year, Category.ENTERTAINMENT, 300)
    tracker.set_budget(now.month, now.year, Category.TRANSPORT, 200)

    # Display summary
    summary = tracker.get_monthly_summary(now.month, now.year)

    print("\n=== Current Month Summary ===")
    print(f"Total Income: ${summary['total_income']:,.2f}")
    print(f"Total Expenses: ${summary['total_expenses']:,.2f}")
    print(f"Net Savings: ${summary['net_savings']:,.2f}")

    print("\nAccount Balances:")
    for name, balance in summary['account_balances'].items():
        print(f"  {name}: ${balance:,.2f}")

    # Visualize expenses
    tracker.visualize_expenses(now.month, now.year)

    # Save data
    tracker.save_data()
    print("\nDemo data saved to demo_finance.json")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_mode()
    else:
        cli = FinanceTrackerCLI()
        cli.run()