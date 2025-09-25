"""
Week 2.3: Dictionaries
Concepts: Key-value pairs, methods, nested dictionaries
"""

print("="*60)
print("WEEK 2.3: DICTIONARIES - TUTORIAL AND SOLUTIONS")
print("="*60)

print("\n" + "="*40)
print("TUTORIAL: Understanding Dictionaries")
print("="*40)

print("""
Dictionaries store key-value pairs:
- Created with curly braces {} or dict()
- Keys must be immutable (strings, numbers, tuples)
- Values can be any type
- Unordered before Python 3.7, ordered after
- Fast lookups by key

Common methods:
keys(), values(), items(), get(), pop()
update(), clear(), copy(), setdefault()
""")

print("\n" + "="*40)
print("BASIC DICTIONARY OPERATIONS")
print("="*40)

person = {
    "name": "John Doe",
    "age": 30,
    "city": "New York",
    "hobbies": ["reading", "coding", "hiking"]
}

print(f"Dictionary: {person}")
print(f"Name: {person['name']}")
print(f"Age: {person['age']}")
print(f"Hobbies: {person['hobbies']}")

person["email"] = "john@example.com"
print(f"After adding email: {person}")

person["age"] = 31
print(f"After updating age: {person}")

city = person.pop("city")
print(f"Popped city: {city}")
print(f"After pop: {person}")

print(f"\nKeys: {list(person.keys())}")
print(f"Values: {list(person.values())}")
print(f"Items: {list(person.items())}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 1: Phone Book Application")
print("="*40)

class PhoneBook:
    def __init__(self):
        self.contacts = {}

    def add_contact(self, name, phone, email=None):
        self.contacts[name] = {
            'phone': phone,
            'email': email if email else 'N/A'
        }
        print(f"Added {name} to phone book")

    def remove_contact(self, name):
        if name in self.contacts:
            del self.contacts[name]
            print(f"Removed {name} from phone book")
        else:
            print(f"{name} not found")

    def search_contact(self, name):
        if name in self.contacts:
            info = self.contacts[name]
            print(f"\nContact: {name}")
            print(f"  Phone: {info['phone']}")
            print(f"  Email: {info['email']}")
        else:
            print(f"{name} not found in phone book")

    def display_all(self):
        if not self.contacts:
            print("Phone book is empty")
        else:
            print(f"\nPhone Book ({len(self.contacts)} contacts):")
            for name, info in sorted(self.contacts.items()):
                print(f"  {name}: {info['phone']} | {info['email']}")

    def update_contact(self, name, phone=None, email=None):
        if name in self.contacts:
            if phone:
                self.contacts[name]['phone'] = phone
            if email:
                self.contacts[name]['email'] = email
            print(f"Updated {name}'s information")
        else:
            print(f"{name} not found")

phone_book = PhoneBook()

phone_book.add_contact("Alice", "123-456-7890", "alice@email.com")
phone_book.add_contact("Bob", "987-654-3210")
phone_book.add_contact("Charlie", "555-0123", "charlie@work.com")

phone_book.display_all()

phone_book.search_contact("Alice")
phone_book.search_contact("David")

phone_book.update_contact("Bob", email="bob@email.com")
phone_book.display_all()

phone_book.remove_contact("Charlie")
phone_book.display_all()

print("\n" + "="*40)
print("PRACTICE PROBLEM 2: Word Frequency Counter")
print("="*40)

def count_word_frequency(text):
    words = text.lower().split()

    cleaned_words = []
    for word in words:
        clean_word = ''.join(c for c in word if c.isalnum())
        if clean_word:
            cleaned_words.append(clean_word)

    frequency = {}
    for word in cleaned_words:
        frequency[word] = frequency.get(word, 0) + 1

    return frequency

def display_frequency(freq_dict, top_n=5):
    sorted_items = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)

    print(f"Total unique words: {len(freq_dict)}")
    print(f"Top {top_n} most frequent words:")
    for word, count in sorted_items[:top_n]:
        print(f"  '{word}': {count} times")

paragraph = """
Python is a powerful programming language. Python is used for web development,
data science, machine learning, and more. Learning Python opens many doors
in the programming world. Python's simple syntax makes it great for beginners.
"""

frequency = count_word_frequency(paragraph)
display_frequency(frequency)

print("\nAll word frequencies:")
for word in sorted(frequency.keys()):
    print(f"  {word}: {frequency[word]}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 3: Inventory Management System")
print("="*40)

class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item_name, quantity, price):
        if item_name in self.items:
            self.items[item_name]['quantity'] += quantity
            print(f"Updated {item_name}: new quantity = {self.items[item_name]['quantity']}")
        else:
            self.items[item_name] = {
                'quantity': quantity,
                'price': price
            }
            print(f"Added new item: {item_name}")

    def remove_item(self, item_name, quantity):
        if item_name not in self.items:
            print(f"Error: {item_name} not in inventory")
            return False

        if self.items[item_name]['quantity'] < quantity:
            print(f"Error: Not enough {item_name} (have {self.items[item_name]['quantity']}, need {quantity})")
            return False

        self.items[item_name]['quantity'] -= quantity
        print(f"Removed {quantity} {item_name}(s)")

        if self.items[item_name]['quantity'] == 0:
            del self.items[item_name]
            print(f"{item_name} out of stock - removed from inventory")

        return True

    def check_stock(self, item_name):
        if item_name in self.items:
            return self.items[item_name]['quantity']
        return 0

    def get_inventory_value(self):
        total = 0
        for item, details in self.items.items():
            total += details['quantity'] * details['price']
        return total

    def display_inventory(self):
        if not self.items:
            print("Inventory is empty")
        else:
            print("\nCurrent Inventory:")
            print(f"{'Item':<15} {'Quantity':<10} {'Price':<10} {'Total':<10}")
            print("-" * 45)
            for item, details in sorted(self.items.items()):
                total = details['quantity'] * details['price']
                print(f"{item:<15} {details['quantity']:<10} ${details['price']:<9.2f} ${total:<9.2f}")
            print("-" * 45)
            print(f"Total inventory value: ${self.get_inventory_value():.2f}")

inventory = Inventory()

inventory.add_item("Apple", 50, 0.5)
inventory.add_item("Banana", 30, 0.3)
inventory.add_item("Orange", 25, 0.6)
inventory.add_item("Apple", 20, 0.5)

inventory.display_inventory()

inventory.remove_item("Banana", 10)
inventory.remove_item("Grape", 5)

print(f"\nApples in stock: {inventory.check_stock('Apple')}")
print(f"Grapes in stock: {inventory.check_stock('Grape')}")

inventory.display_inventory()

print("\n" + "="*40)
print("PRACTICE PROBLEM 4: List to Dictionary Conversion")
print("="*40)

def list_to_dict_indexed(lst):
    """Convert list to dict with indices as keys"""
    return {i: value for i, value in enumerate(lst)}

def list_to_dict_paired(lst):
    """Convert list of pairs to dictionary"""
    return dict(lst)

def lists_to_dict(keys, values):
    """Combine two lists into a dictionary"""
    return dict(zip(keys, values))

def group_by_length(words):
    """Group words by their length"""
    grouped = {}
    for word in words:
        length = len(word)
        if length not in grouped:
            grouped[length] = []
        grouped[length].append(word)
    return grouped

fruits = ["apple", "banana", "cherry"]
indexed = list_to_dict_indexed(fruits)
print(f"List: {fruits}")
print(f"Indexed dict: {indexed}")

pairs = [("a", 1), ("b", 2), ("c", 3)]
paired_dict = list_to_dict_paired(pairs)
print(f"\nPairs: {pairs}")
print(f"Paired dict: {paired_dict}")

keys = ["name", "age", "city"]
values = ["Alice", 25, "NYC"]
combined = lists_to_dict(keys, values)
print(f"\nKeys: {keys}")
print(f"Values: {values}")
print(f"Combined: {combined}")

words = ["cat", "elephant", "dog", "bird", "butterfly", "ant", "lion"]
grouped = group_by_length(words)
print(f"\nWords: {words}")
print("Grouped by length:")
for length in sorted(grouped.keys()):
    print(f"  {length} letters: {grouped[length]}")

print("\n" + "="*40)
print("NESTED DICTIONARIES")
print("="*40)

company = {
    "employees": {
        "john": {
            "age": 30,
            "department": "IT",
            "salary": 70000
        },
        "jane": {
            "age": 28,
            "department": "HR",
            "salary": 65000
        },
        "bob": {
            "age": 35,
            "department": "IT",
            "salary": 75000
        }
    },
    "departments": {
        "IT": {"budget": 500000, "head": "bob"},
        "HR": {"budget": 200000, "head": "jane"}
    }
}

print("Company structure:")
print(f"Employees: {list(company['employees'].keys())}")
print(f"Departments: {list(company['departments'].keys())}")

print("\nJohn's details:")
john = company['employees']['john']
for key, value in john.items():
    print(f"  {key}: {value}")

print("\nIT department:")
it_dept = company['departments']['IT']
print(f"  Budget: ${it_dept['budget']:,}")
print(f"  Head: {it_dept['head']}")

print("\n" + "="*40)
print("DICTIONARY COMPREHENSIONS")
print("="*40)

squares = {x: x**2 for x in range(1, 6)}
print(f"Squares: {squares}")

word_lengths = {word: len(word) for word in ["python", "java", "javascript"]}
print(f"Word lengths: {word_lengths}")

filtered = {k: v for k, v in squares.items() if v > 10}
print(f"Filtered squares (>10): {filtered}")

print("\n" + "="*40)
print("KEY TAKEAWAYS")
print("="*40)
print("""
1. Dictionaries provide fast key-based lookups
2. Keys must be immutable, values can be any type
3. Use get() to safely access keys that might not exist
4. Dictionary comprehensions offer concise creation
5. Nested dictionaries help organize complex data
6. items(), keys(), values() for iteration
""")