"""
Week 5.1: Classes and Objects
Concepts: class definition, __init__, self, attributes, methods
"""

from datetime import datetime, timedelta
import random

print("="*60)
print("WEEK 5.1: CLASSES AND OBJECTS - TUTORIAL AND SOLUTIONS")
print("="*60)

print("\n" + "="*40)
print("TUTORIAL: Introduction to Object-Oriented Programming")
print("="*40)

print("""
Classes are blueprints for creating objects:
- Class: Template defining attributes and methods
- Object: Instance of a class
- Attributes: Data stored in objects
- Methods: Functions defined in a class
- self: Reference to the current instance

OOP Concepts:
- Encapsulation: Bundling data and methods
- Abstraction: Hiding complex implementation
- Inheritance: Creating new classes from existing ones
- Polymorphism: Same interface, different implementations
""")

print("\n" + "="*40)
print("BASIC CLASS EXAMPLE")
print("="*40)

class Person:
    """Basic Person class"""

    def __init__(self, name, age):
        """Constructor method"""
        self.name = name
        self.age = age

    def greet(self):
        """Instance method"""
        return f"Hello, I'm {self.name} and I'm {self.age} years old"

    def have_birthday(self):
        """Method that modifies state"""
        self.age += 1
        print(f"Happy birthday {self.name}! Now {self.age} years old")

person1 = Person("Alice", 25)
person2 = Person("Bob", 30)

print(f"Person 1: {person1.greet()}")
print(f"Person 2: {person2.greet()}")
person1.have_birthday()

print("\n" + "="*40)
print("PRACTICE PROBLEM 1: BankAccount Class")
print("="*40)

class BankAccount:
    """Bank account with deposit/withdraw functionality"""

    account_count = 0

    def __init__(self, account_holder, initial_balance=0):
        """Initialize a new bank account"""
        BankAccount.account_count += 1
        self.account_number = f"ACC{BankAccount.account_count:04d}"
        self.account_holder = account_holder
        self._balance = initial_balance
        self.transactions = []
        self._record_transaction("Account opened", initial_balance)

    def _record_transaction(self, description, amount):
        """Private method to record transactions"""
        transaction = {
            'date': datetime.now(),
            'description': description,
            'amount': amount,
            'balance': self._balance
        }
        self.transactions.append(transaction)

    def deposit(self, amount):
        """Deposit money into account"""
        if amount <= 0:
            print("Deposit amount must be positive")
            return False

        self._balance += amount
        self._record_transaction(f"Deposit", amount)
        print(f"Deposited ${amount:.2f}. New balance: ${self._balance:.2f}")
        return True

    def withdraw(self, amount):
        """Withdraw money from account"""
        if amount <= 0:
            print("Withdrawal amount must be positive")
            return False

        if amount > self._balance:
            print(f"Insufficient funds. Available: ${self._balance:.2f}")
            return False

        self._balance -= amount
        self._record_transaction(f"Withdrawal", -amount)
        print(f"Withdrew ${amount:.2f}. New balance: ${self._balance:.2f}")
        return True

    def get_balance(self):
        """Get current balance"""
        return self._balance

    def transfer(self, recipient, amount):
        """Transfer money to another account"""
        if self.withdraw(amount):
            recipient.deposit(amount)
            print(f"Transferred ${amount:.2f} to {recipient.account_holder}")
            return True
        return False

    def get_statement(self, num_transactions=5):
        """Get recent account statement"""
        print(f"\nAccount Statement for {self.account_holder}")
        print(f"Account Number: {self.account_number}")
        print(f"Current Balance: ${self._balance:.2f}")
        print("\nRecent Transactions:")
        print("-" * 60)

        recent = self.transactions[-num_transactions:] if len(self.transactions) > num_transactions else self.transactions
        for trans in recent:
            date_str = trans['date'].strftime("%Y-%m-%d %H:%M")
            amount_str = f"${abs(trans['amount']):.2f}"
            if trans['amount'] >= 0:
                amount_str = "+" + amount_str
            else:
                amount_str = "-" + f"${abs(trans['amount']):.2f}"

            print(f"{date_str} | {trans['description']:<15} | {amount_str:>10} | ${trans['balance']:.2f}")

    def __str__(self):
        """String representation"""
        return f"BankAccount({self.account_number}, {self.account_holder}, ${self._balance:.2f})"

account1 = BankAccount("Alice Johnson", 1000)
account2 = BankAccount("Bob Smith", 500)

print(f"Account 1: {account1}")
print(f"Account 2: {account2}")

account1.deposit(500)
account1.withdraw(200)
account1.transfer(account2, 300)

account1.get_statement()
account2.get_statement()

print("\n" + "="*40)
print("PRACTICE PROBLEM 2: Student Class")
print("="*40)

class Student:
    """Student class with grade management"""

    def __init__(self, name, student_id, major="Undeclared"):
        """Initialize a student"""
        self.name = name
        self.student_id = student_id
        self.major = major
        self.courses = {}
        self.grades = {}

    def enroll_course(self, course_code, course_name, credits):
        """Enroll in a course"""
        if course_code in self.courses:
            print(f"Already enrolled in {course_code}")
            return False

        self.courses[course_code] = {
            'name': course_name,
            'credits': credits,
            'grade': None
        }
        print(f"Enrolled in {course_code}: {course_name}")
        return True

    def add_grade(self, course_code, grade):
        """Add grade for a course"""
        if course_code not in self.courses:
            print(f"Not enrolled in {course_code}")
            return False

        grade_points = {
            'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0
        }

        if grade not in grade_points:
            print("Invalid grade. Use A, B, C, D, or F")
            return False

        self.courses[course_code]['grade'] = grade
        self.grades[course_code] = grade_points[grade]
        print(f"Grade {grade} recorded for {course_code}")
        return True

    def calculate_gpa(self):
        """Calculate GPA"""
        if not self.grades:
            return 0.0

        total_points = 0
        total_credits = 0

        for course_code, grade_point in self.grades.items():
            credits = self.courses[course_code]['credits']
            total_points += grade_point * credits
            total_credits += credits

        return total_points / total_credits if total_credits > 0 else 0.0

    def get_transcript(self):
        """Display student transcript"""
        print(f"\n{'='*50}")
        print(f"TRANSCRIPT")
        print(f"{'='*50}")
        print(f"Student: {self.name}")
        print(f"ID: {self.student_id}")
        print(f"Major: {self.major}")
        print(f"\nCourses:")
        print(f"{'Code':<10} {'Name':<20} {'Credits':<8} {'Grade':<6}")
        print("-" * 50)

        for code, info in self.courses.items():
            grade = info['grade'] if info['grade'] else 'IP'
            print(f"{code:<10} {info['name']:<20} {info['credits']:<8} {grade:<6}")

        gpa = self.calculate_gpa()
        print(f"\nGPA: {gpa:.2f}")

    def dean_list(self):
        """Check if student qualifies for dean's list"""
        gpa = self.calculate_gpa()
        return gpa >= 3.5

    def __str__(self):
        return f"Student({self.name}, {self.student_id}, {self.major})"

student1 = Student("Alice Chen", "S12345", "Computer Science")
student1.enroll_course("CS101", "Intro to Programming", 3)
student1.enroll_course("MATH201", "Calculus II", 4)
student1.enroll_course("PHYS101", "Physics I", 3)

student1.add_grade("CS101", "A")
student1.add_grade("MATH201", "B")
student1.add_grade("PHYS101", "A")

student1.get_transcript()
if student1.dean_list():
    print(f"\nCongratulations! {student1.name} made the Dean's List!")

print("\n" + "="*40)
print("PRACTICE PROBLEM 3: Library Management System")
print("="*40)

class Book:
    """Book class for library system"""

    def __init__(self, isbn, title, author, year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.available = True
        self.borrowed_by = None
        self.due_date = None

    def __str__(self):
        status = "Available" if self.available else f"Borrowed by {self.borrowed_by}"
        return f"{self.title} by {self.author} ({self.year}) - {status}"

class Library:
    """Library management system"""

    def __init__(self, name):
        self.name = name
        self.books = {}
        self.members = {}
        self.transactions = []

    def add_book(self, book):
        """Add a book to library"""
        if book.isbn in self.books:
            print(f"Book with ISBN {book.isbn} already exists")
            return False

        self.books[book.isbn] = book
        print(f"Added: {book.title}")
        return True

    def register_member(self, member_id, name):
        """Register a library member"""
        if member_id in self.members:
            print(f"Member {member_id} already registered")
            return False

        self.members[member_id] = {
            'name': name,
            'books_borrowed': [],
            'history': []
        }
        print(f"Registered member: {name} (ID: {member_id})")
        return True

    def borrow_book(self, isbn, member_id):
        """Borrow a book"""
        if isbn not in self.books:
            print(f"Book with ISBN {isbn} not found")
            return False

        if member_id not in self.members:
            print(f"Member {member_id} not registered")
            return False

        book = self.books[isbn]
        if not book.available:
            print(f"{book.title} is currently unavailable")
            return False

        book.available = False
        book.borrowed_by = member_id
        book.due_date = datetime.now() + timedelta(days=14)

        self.members[member_id]['books_borrowed'].append(isbn)
        self.transactions.append({
            'date': datetime.now(),
            'type': 'borrow',
            'isbn': isbn,
            'member_id': member_id
        })

        print(f"{self.members[member_id]['name']} borrowed {book.title}")
        print(f"Due date: {book.due_date.strftime('%Y-%m-%d')}")
        return True

    def return_book(self, isbn, member_id):
        """Return a book"""
        if isbn not in self.books:
            print(f"Book with ISBN {isbn} not found")
            return False

        book = self.books[isbn]
        if book.available or book.borrowed_by != member_id:
            print("Invalid return request")
            return False

        book.available = True
        book.borrowed_by = None
        book.due_date = None

        self.members[member_id]['books_borrowed'].remove(isbn)
        self.members[member_id]['history'].append(isbn)

        self.transactions.append({
            'date': datetime.now(),
            'type': 'return',
            'isbn': isbn,
            'member_id': member_id
        })

        print(f"{self.members[member_id]['name']} returned {book.title}")
        return True

    def search_books(self, query):
        """Search for books by title or author"""
        results = []
        query_lower = query.lower()

        for book in self.books.values():
            if query_lower in book.title.lower() or query_lower in book.author.lower():
                results.append(book)

        return results

    def display_available_books(self):
        """Display all available books"""
        print(f"\nAvailable Books in {self.name}:")
        print("-" * 60)
        available = [book for book in self.books.values() if book.available]

        if not available:
            print("No books available")
        else:
            for book in available:
                print(f"  {book}")

library = Library("City Library")

library.add_book(Book("978-0-13-110362-7", "The Pragmatic Programmer", "David Thomas", 2019))
library.add_book(Book("978-0-596-00712-6", "Learning Python", "Mark Lutz", 2013))
library.add_book(Book("978-1-59327-603-4", "Python Crash Course", "Eric Matthes", 2015))

library.register_member("M001", "John Doe")
library.register_member("M002", "Jane Smith")

library.display_available_books()

library.borrow_book("978-0-13-110362-7", "M001")
library.borrow_book("978-0-596-00712-6", "M002")

library.display_available_books()

library.return_book("978-0-13-110362-7", "M001")

search_results = library.search_books("Python")
print(f"\nSearch results for 'Python':")
for book in search_results:
    print(f"  {book}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 4: Car Class")
print("="*40)

class Car:
    """Car class with various properties"""

    total_cars = 0

    def __init__(self, make, model, year, color="Black"):
        """Initialize a car"""
        Car.total_cars += 1
        self.car_id = f"CAR{Car.total_cars:04d}"
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.mileage = 0
        self.fuel_level = 100
        self.is_running = False
        self.maintenance_log = []

    def start(self):
        """Start the car"""
        if self.is_running:
            print(f"{self.make} {self.model} is already running")
        elif self.fuel_level <= 0:
            print("Cannot start - no fuel")
        else:
            self.is_running = True
            print(f"{self.make} {self.model} started")

    def stop(self):
        """Stop the car"""
        if not self.is_running:
            print(f"{self.make} {self.model} is not running")
        else:
            self.is_running = False
            print(f"{self.make} {self.model} stopped")

    def drive(self, miles):
        """Drive the car"""
        if not self.is_running:
            print("Start the car first")
            return

        fuel_needed = miles * 0.05
        if fuel_needed > self.fuel_level:
            max_miles = self.fuel_level / 0.05
            print(f"Not enough fuel. Can only drive {max_miles:.1f} miles")
            return

        self.mileage += miles
        self.fuel_level -= fuel_needed
        print(f"Drove {miles} miles. Mileage: {self.mileage}, Fuel: {self.fuel_level:.1f}%")

    def refuel(self, amount=None):
        """Refuel the car"""
        if amount is None:
            amount = 100 - self.fuel_level

        if self.fuel_level + amount > 100:
            amount = 100 - self.fuel_level

        self.fuel_level += amount
        print(f"Refueled {amount:.1f}%. Fuel level: {self.fuel_level:.1f}%")

    def service(self, service_type):
        """Service the car"""
        self.maintenance_log.append({
            'date': datetime.now(),
            'mileage': self.mileage,
            'service': service_type
        })
        print(f"Service completed: {service_type}")

    def get_info(self):
        """Display car information"""
        print(f"\n{self.year} {self.make} {self.model}")
        print(f"Color: {self.color}")
        print(f"Mileage: {self.mileage} miles")
        print(f"Fuel Level: {self.fuel_level:.1f}%")
        print(f"Status: {'Running' if self.is_running else 'Stopped'}")
        print(f"Services: {len(self.maintenance_log)}")

    def __str__(self):
        return f"{self.year} {self.make} {self.model} ({self.car_id})"

car1 = Car("Toyota", "Camry", 2022, "Silver")
car2 = Car("Tesla", "Model 3", 2023, "White")

print(f"Car 1: {car1}")
print(f"Car 2: {car2}")

car1.get_info()

car1.start()
car1.drive(50)
car1.drive(100)
car1.refuel(30)
car1.service("Oil Change")
car1.stop()

car1.get_info()

print(f"\nTotal cars created: {Car.total_cars}")

print("\n" + "="*40)
print("KEY TAKEAWAYS")
print("="*40)
print("""
1. Classes define the structure and behavior of objects
2. __init__ is the constructor method
3. self refers to the instance being operated on
4. Instance attributes store object-specific data
5. Methods define object behavior
6. Class attributes are shared by all instances
7. Encapsulation hides implementation details
""")