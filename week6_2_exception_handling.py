"""
Week 6.2: Exception Handling
Concepts: try, except, finally, raise
"""

import sys
import traceback
from typing import Optional

print("="*60)
print("WEEK 6.2: EXCEPTION HANDLING - TUTORIAL AND SOLUTIONS")
print("="*60)

print("\n" + "="*40)
print("TUTORIAL: Managing Errors Gracefully")
print("="*40)

print("""
Exception handling prevents program crashes:
- try: Code that might raise exception
- except: Handle specific exceptions
- else: Execute if no exception
- finally: Always execute (cleanup)
- raise: Manually raise exception

Common exceptions:
- ValueError: Invalid value
- TypeError: Wrong type
- KeyError: Missing dict key
- IndexError: Invalid list index
- FileNotFoundError: File doesn't exist
- ZeroDivisionError: Division by zero
""")

print("\n" + "="*40)
print("BASIC EXCEPTION HANDLING")
print("="*40)

def basic_examples():
    """Demonstrate basic exception handling"""

    print("Example 1: Division by zero")
    try:
        result = 10 / 0
    except ZeroDivisionError:
        print("  Error: Cannot divide by zero!")

    print("\nExample 2: Invalid type conversion")
    try:
        number = int("abc")
    except ValueError as e:
        print(f"  Error: {e}")

    print("\nExample 3: List index out of range")
    try:
        my_list = [1, 2, 3]
        item = my_list[10]
    except IndexError:
        print("  Error: Index out of range!")

    print("\nExample 4: Multiple exceptions")
    try:
        value = int(input("  Enter a number (demo: using 'abc'): "))
        result = 10 / value
        print(f"  Result: {result}")
    except ValueError:
        print("  Error: Please enter a valid number")
    except ZeroDivisionError:
        print("  Error: Cannot divide by zero")
    except Exception as e:
        print(f"  Unexpected error: {e}")

basic_examples()

print("\n" + "="*40)
print("PRACTICE PROBLEM 1: Robust Calculator")
print("="*40)

class RobustCalculator:
    """Calculator with comprehensive error handling"""

    def __init__(self):
        self.history = []
        self.error_log = []

    def calculate(self, expression):
        """Evaluate mathematical expression safely"""
        try:
            allowed_names = {
                k: v for k, v in vars(__builtins__).items()
                if k in ['abs', 'round', 'min', 'max', 'sum', 'pow']
            }

            for char in expression:
                if char.isalpha() and char not in str(allowed_names):
                    raise ValueError(f"Invalid character: {char}")

            result = eval(expression, {"__builtins__": {}}, allowed_names)

            self.history.append({
                'expression': expression,
                'result': result,
                'success': True
            })

            return result

        except ZeroDivisionError:
            self._log_error("Division by zero", expression)
            return "Error: Division by zero"

        except SyntaxError:
            self._log_error("Invalid syntax", expression)
            return "Error: Invalid expression syntax"

        except ValueError as e:
            self._log_error(str(e), expression)
            return f"Error: {e}"

        except Exception as e:
            self._log_error(f"Unexpected error: {e}", expression)
            return f"Error: {type(e).__name__}: {e}"

    def _log_error(self, error_msg, expression):
        """Log error for analysis"""
        self.error_log.append({
            'expression': expression,
            'error': error_msg
        })

    def safe_divide(self, a, b):
        """Safe division with detailed error handling"""
        try:
            if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
                raise TypeError("Both arguments must be numbers")

            if b == 0:
                raise ZeroDivisionError("Cannot divide by zero")

            result = a / b

            if result == float('inf'):
                raise OverflowError("Result is infinity")

            return result

        except TypeError as e:
            return f"Type Error: {e}"
        except ZeroDivisionError as e:
            return f"Math Error: {e}"
        except OverflowError as e:
            return f"Overflow Error: {e}"

    def get_statistics(self):
        """Get calculator usage statistics"""
        if not self.history:
            return "No calculations performed yet"

        successful = sum(1 for h in self.history if h.get('success'))
        total = len(self.history)

        return {
            'total_calculations': total,
            'successful': successful,
            'errors': len(self.error_log),
            'success_rate': f"{(successful/total)*100:.1f}%"
        }

calc = RobustCalculator()

test_expressions = [
    "2 + 2",
    "10 / 2",
    "10 / 0",
    "5 * (3 + 2)",
    "invalid",
    "abs(-10)",
    "max(1, 2, 3)",
]

print("Testing calculator with various expressions:")
for expr in test_expressions:
    result = calc.calculate(expr)
    print(f"  {expr} = {result}")

print(f"\nSafe division tests:")
print(f"  10 / 2 = {calc.safe_divide(10, 2)}")
print(f"  10 / 0 = {calc.safe_divide(10, 0)}")
print(f"  'a' / 2 = {calc.safe_divide('a', 2)}")

stats = calc.get_statistics()
print(f"\nCalculator statistics:")
for key, value in stats.items():
    print(f"  {key}: {value}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 2: File Reader with Fallbacks")
print("="*40)

class RobustFileReader:
    """File reader with multiple fallback strategies"""

    def __init__(self):
        self.encoding_fallbacks = ['utf-8', 'latin-1', 'cp1252', 'ascii']
        self.read_attempts = []

    def read_file(self, filepath, fallback_files=None):
        """Read file with multiple fallback options"""
        content = self._try_read_primary(filepath)

        if content is not None:
            return content

        if fallback_files:
            for fallback in fallback_files:
                print(f"  Trying fallback: {fallback}")
                content = self._try_read_primary(fallback)
                if content is not None:
                    return content

        return self._create_default_content()

    def _try_read_primary(self, filepath):
        """Try to read file with encoding fallbacks"""
        for encoding in self.encoding_fallbacks:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    content = f.read()

                self.read_attempts.append({
                    'file': filepath,
                    'encoding': encoding,
                    'success': True
                })

                print(f"  Successfully read {filepath} with {encoding} encoding")
                return content

            except FileNotFoundError:
                self.read_attempts.append({
                    'file': filepath,
                    'error': 'File not found',
                    'success': False
                })
                print(f"  File not found: {filepath}")
                break

            except UnicodeDecodeError:
                self.read_attempts.append({
                    'file': filepath,
                    'encoding': encoding,
                    'error': 'Encoding error',
                    'success': False
                })
                continue

            except PermissionError:
                self.read_attempts.append({
                    'file': filepath,
                    'error': 'Permission denied',
                    'success': False
                })
                print(f"  Permission denied: {filepath}")
                break

            except Exception as e:
                self.read_attempts.append({
                    'file': filepath,
                    'error': str(e),
                    'success': False
                })
                print(f"  Unexpected error: {e}")
                break

        return None

    def _create_default_content(self):
        """Create default content when all reads fail"""
        print("  Creating default content")
        return "Default content - original file could not be read"

    def read_json_safely(self, filepath):
        """Read JSON file with error handling"""
        import json

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return data

        except FileNotFoundError:
            print(f"  JSON file not found: {filepath}")
            return {}

        except json.JSONDecodeError as e:
            print(f"  Invalid JSON in {filepath}: {e}")
            return {}

        except Exception as e:
            print(f"  Error reading JSON: {e}")
            return {}

reader = RobustFileReader()

content = reader.read_file("nonexistent.txt", ["backup.txt", "default.txt"])
print(f"Content: {content[:50]}...")

json_data = reader.read_json_safely("config.json")
print(f"JSON data: {json_data}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 3: Input Validation System")
print("="*40)

class InputValidator:
    """Comprehensive input validation with error handling"""

    @staticmethod
    def validate_email(email):
        """Validate email address"""
        try:
            if not email or not isinstance(email, str):
                raise ValueError("Email must be a non-empty string")

            if '@' not in email:
                raise ValueError("Email must contain @")

            local, domain = email.rsplit('@', 1)

            if not local or not domain:
                raise ValueError("Invalid email format")

            if '.' not in domain:
                raise ValueError("Domain must contain a dot")

            if len(email) > 254:
                raise ValueError("Email too long (max 254 characters)")

            return True, "Valid email"

        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Unexpected error: {e}"

    @staticmethod
    def validate_age(age):
        """Validate age input"""
        try:
            if isinstance(age, str):
                age = int(age)

            if not isinstance(age, int):
                raise TypeError("Age must be an integer")

            if age < 0:
                raise ValueError("Age cannot be negative")

            if age > 150:
                raise ValueError("Age seems unrealistic (>150)")

            return True, age

        except ValueError as e:
            if "invalid literal" in str(e):
                return False, "Age must be a valid number"
            return False, str(e)
        except TypeError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Unexpected error: {e}"

    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        errors = []

        try:
            if not password:
                raise ValueError("Password cannot be empty")

            if not isinstance(password, str):
                raise TypeError("Password must be a string")

            if len(password) < 8:
                errors.append("At least 8 characters required")

            if not any(c.isupper() for c in password):
                errors.append("At least one uppercase letter required")

            if not any(c.islower() for c in password):
                errors.append("At least one lowercase letter required")

            if not any(c.isdigit() for c in password):
                errors.append("At least one number required")

            special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            if not any(c in special_chars for c in password):
                errors.append("At least one special character required")

            if errors:
                raise ValueError("; ".join(errors))

            return True, "Strong password"

        except (ValueError, TypeError) as e:
            return False, str(e)
        except Exception as e:
            return False, f"Unexpected error: {e}"

validator = InputValidator()

test_emails = ["user@example.com", "invalid", "", "user@", "@domain.com"]
print("Email validation:")
for email in test_emails:
    valid, msg = validator.validate_email(email)
    status = "✓" if valid else "✗"
    print(f"  {status} {email}: {msg}")

test_ages = [25, "30", -5, 200, "abc", None]
print("\nAge validation:")
for age in test_ages:
    valid, msg = validator.validate_age(age)
    status = "✓" if valid else "✗"
    print(f"  {status} {age}: {msg}")

test_passwords = ["Pass123!", "weak", "NoNumbers!", "nouppercase1!", ""]
print("\nPassword validation:")
for pwd in test_passwords:
    valid, msg = validator.validate_password(pwd)
    status = "✓" if valid else "✗"
    print(f"  {status} {'*' * len(pwd) if pwd else '(empty)'}: {msg}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 4: Custom Exceptions for Banking")
print("="*40)

class BankingError(Exception):
    """Base exception for banking operations"""
    pass

class InsufficientFundsError(BankingError):
    """Raised when account has insufficient funds"""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Insufficient funds: balance ${balance:.2f}, requested ${amount:.2f}")

class InvalidAccountError(BankingError):
    """Raised when account is invalid"""
    pass

class TransactionLimitError(BankingError):
    """Raised when transaction exceeds limits"""
    def __init__(self, limit, amount):
        self.limit = limit
        self.amount = amount
        super().__init__(f"Transaction limit exceeded: limit ${limit:.2f}, requested ${amount:.2f}")

class AccountFrozenError(BankingError):
    """Raised when account is frozen"""
    pass

class SecureBankAccount:
    """Bank account with custom exception handling"""

    def __init__(self, account_number, initial_balance=0):
        self.account_number = account_number
        self.balance = initial_balance
        self.is_frozen = False
        self.daily_limit = 5000
        self.daily_withdrawn = 0
        self.transaction_history = []

    def withdraw(self, amount):
        """Withdraw money with comprehensive error checking"""
        try:
            if self.is_frozen:
                raise AccountFrozenError(f"Account {self.account_number} is frozen")

            if amount <= 0:
                raise ValueError("Withdrawal amount must be positive")

            if amount > self.balance:
                raise InsufficientFundsError(self.balance, amount)

            if self.daily_withdrawn + amount > self.daily_limit:
                raise TransactionLimitError(
                    self.daily_limit - self.daily_withdrawn,
                    amount
                )

            self.balance -= amount
            self.daily_withdrawn += amount
            self._log_transaction("withdrawal", amount, True)

            return f"Withdrawn ${amount:.2f}. New balance: ${self.balance:.2f}"

        except BankingError:
            self._log_transaction("withdrawal", amount, False)
            raise
        except Exception as e:
            self._log_transaction("withdrawal", amount, False)
            raise BankingError(f"Unexpected error: {e}")

    def deposit(self, amount):
        """Deposit money with error checking"""
        try:
            if self.is_frozen:
                raise AccountFrozenError(f"Account {self.account_number} is frozen")

            if amount <= 0:
                raise ValueError("Deposit amount must be positive")

            if amount > 10000:
                raise TransactionLimitError(10000, amount)

            self.balance += amount
            self._log_transaction("deposit", amount, True)

            return f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}"

        except BankingError:
            self._log_transaction("deposit", amount, False)
            raise
        except Exception as e:
            self._log_transaction("deposit", amount, False)
            raise BankingError(f"Unexpected error: {e}")

    def freeze_account(self):
        """Freeze the account"""
        self.is_frozen = True
        print(f"Account {self.account_number} has been frozen")

    def unfreeze_account(self):
        """Unfreeze the account"""
        self.is_frozen = False
        print(f"Account {self.account_number} has been unfrozen")

    def _log_transaction(self, type, amount, success):
        """Log transaction for audit"""
        self.transaction_history.append({
            'type': type,
            'amount': amount,
            'success': success,
            'balance_after': self.balance if success else None
        })

account = SecureBankAccount("ACC123", 1000)

operations = [
    ("deposit", 500),
    ("withdraw", 200),
    ("withdraw", 2000),
    ("deposit", -100),
    ("withdraw", 6000),
]

print("Testing banking operations with custom exceptions:")
for operation, amount in operations:
    try:
        if operation == "deposit":
            result = account.deposit(amount)
        else:
            result = account.withdraw(amount)
        print(f"  ✓ {operation.capitalize()} ${amount}: {result}")

    except InsufficientFundsError as e:
        print(f"  ✗ {operation.capitalize()} ${amount}: {e}")
    except TransactionLimitError as e:
        print(f"  ✗ {operation.capitalize()} ${amount}: {e}")
    except ValueError as e:
        print(f"  ✗ {operation.capitalize()} ${amount}: Invalid amount - {e}")
    except BankingError as e:
        print(f"  ✗ {operation.capitalize()} ${amount}: Banking error - {e}")

print("\nTesting frozen account:")
account.freeze_account()
try:
    account.deposit(100)
except AccountFrozenError as e:
    print(f"  ✗ Cannot deposit: {e}")

account.unfreeze_account()

print("\n" + "="*40)
print("ADVANCED: Context Manager for Error Handling")
print("="*40)

class ErrorHandler:
    """Context manager for error handling"""

    def __init__(self, suppress_errors=False, log_errors=True):
        self.suppress_errors = suppress_errors
        self.log_errors = log_errors
        self.errors = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            error_info = {
                'type': exc_type.__name__,
                'message': str(exc_val),
                'traceback': traceback.format_exc() if self.log_errors else None
            }
            self.errors.append(error_info)

            if self.log_errors:
                print(f"  Error logged: {error_info['type']}: {error_info['message']}")

            return self.suppress_errors

        return False

print("Using error handler context manager:")

with ErrorHandler(suppress_errors=True) as handler:
    print("  Attempting division by zero...")
    result = 10 / 0

print(f"  Errors captured: {len(handler.errors)}")

print("\n" + "="*40)
print("KEY TAKEAWAYS")
print("="*40)
print("""
1. Always handle expected exceptions specifically
2. Use finally for cleanup operations
3. Create custom exceptions for domain-specific errors
4. Log errors for debugging and monitoring
5. Provide meaningful error messages
6. Don't catch Exception unless necessary
7. Use context managers for resource management
""")