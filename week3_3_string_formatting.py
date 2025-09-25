"""
Week 3.3: String Formatting
Concepts: f-strings, format(), % formatting
"""

from datetime import datetime
import math

print("="*60)
print("WEEK 3.3: STRING FORMATTING - TUTORIAL AND SOLUTIONS")
print("="*60)

print("\n" + "="*40)
print("TUTORIAL: Different String Formatting Methods")
print("="*40)

print("""
Python offers several string formatting methods:

1. % formatting (old style)
   "Hello %s" % name

2. .format() method
   "Hello {}".format(name)

3. f-strings (Python 3.6+) - RECOMMENDED
   f"Hello {name}"

4. Template strings (rare)
   Template("Hello $name").substitute(name=value)
""")

print("\n" + "="*40)
print("F-STRINGS (Recommended)")
print("="*40)

name = "Alice"
age = 30
height = 165.5
balance = 1234.56789

print(f"Basic: My name is {name}")
print(f"Multiple: {name} is {age} years old")
print(f"Expression: In 5 years, {name} will be {age + 5}")
print(f"Method call: Name in uppercase: {name.upper()}")
print(f"Format specs: Height: {height:.1f}cm")
print(f"Currency: Balance: ${balance:,.2f}")
print(f"Padding: |{name:10}| (left aligned)")
print(f"Padding: |{name:>10}| (right aligned)")
print(f"Padding: |{name:^10}| (centered)")
print(f"Zero padding: {42:05d}")

print("\n" + "="*40)
print("FORMAT() METHOD")
print("="*40)

template = "Hello, {}! You are {} years old."
print(template.format("Bob", 25))

template2 = "Hello, {name}! You are {age} years old."
print(template2.format(name="Charlie", age=35))

template3 = "{0} {1} {0}"
print(template3.format("Hello", "World"))

print("Formatting: {:.2f}".format(3.14159))
print("Percentage: {:.1%}".format(0.25))
print("Binary: {:b}".format(42))
print("Hex: {:x}".format(255))

print("\n" + "="*40)
print("% FORMATTING (Old Style)")
print("="*40)

print("String: %s" % "Hello")
print("Integer: %d" % 42)
print("Float: %.2f" % 3.14159)
print("Multiple: %s is %d years old" % ("David", 40))
print("Padding: |%10s|" % "test")
print("Zero padding: %05d" % 42)

print("\n" + "="*40)
print("PRACTICE PROBLEM 1: Receipt Printer")
print("="*40)

def print_receipt(items):
    store_name = "Python Mart"
    width = 50

    print("=" * width)
    print(f"{store_name:^{width}}")
    print("=" * width)
    print(f"{'Item':<20} {'Qty':>8} {'Price':>10} {'Total':>10}")
    print("-" * width)

    subtotal = 0
    for item, qty, price in items:
        total = qty * price
        subtotal += total
        print(f"{item:<20} {qty:>8} ${price:>9.2f} ${total:>9.2f}")

    tax_rate = 0.08
    tax = subtotal * tax_rate
    total = subtotal + tax

    print("-" * width)
    print(f"{'Subtotal':>{width-11}} ${subtotal:>9.2f}")
    print(f"{'Tax (8%)':>{width-11}} ${tax:>9.2f}")
    print(f"{'Total':>{width-11}} ${total:>9.2f}")
    print("=" * width)
    print(f"{'Thank you for shopping!':^{width}}")
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M'):^{width}}")
    print("=" * width)

items = [
    ("Apple", 5, 0.99),
    ("Banana", 3, 0.59),
    ("Orange Juice", 2, 3.49),
    ("Bread", 1, 2.99),
    ("Cheese", 2, 4.99),
    ("Milk", 1, 3.79)
]

print_receipt(items)

print("\n" + "="*40)
print("PRACTICE PROBLEM 2: Mad Libs Game")
print("="*40)

def mad_libs_demo():
    templates = [
        "The {adjective1} {noun1} {verb} over the {adjective2} {noun2}.",
        "Once upon a time, a {adjective} {creature} lived in a {place}.",
        "To make a {food}, you need {number} {ingredient} and lots of {emotion}.",
        "The {occupation} {adverb} {past_verb} the {object} in the {location}."
    ]

    stories = [
        {
            'template': templates[0],
            'words': {
                'adjective1': 'quick',
                'noun1': 'fox',
                'verb': 'jumps',
                'adjective2': 'lazy',
                'noun2': 'dog'
            }
        },
        {
            'template': templates[1],
            'words': {
                'adjective': 'mysterious',
                'creature': 'dragon',
                'place': 'enchanted forest'
            }
        },
        {
            'template': templates[2],
            'words': {
                'food': 'pizza',
                'number': '5',
                'ingredient': 'tomatoes',
                'emotion': 'patience'
            }
        },
        {
            'template': templates[3],
            'words': {
                'occupation': 'scientist',
                'adverb': 'carefully',
                'past_verb': 'examined',
                'object': 'specimen',
                'location': 'laboratory'
            }
        }
    ]

    print("Mad Libs Stories:\n")
    for i, story in enumerate(stories, 1):
        result = story['template'].format(**story['words'])
        print(f"Story {i}: {result}")

mad_libs_demo()

print("\n" + "="*40)
print("PRACTICE PROBLEM 3: Currency Formatter")
print("="*40)

def format_currency(amount, currency="USD"):
    formats = {
        "USD": ("$", "", 2),
        "EUR": ("€", "", 2),
        "GBP": ("£", "", 2),
        "JPY": ("¥", "", 0),
        "INR": ("₹", "", 2),
        "CNY": ("¥", "", 2)
    }

    if currency not in formats:
        return f"{amount:.2f} {currency}"

    symbol, suffix, decimals = formats[currency]

    if decimals == 0:
        formatted = f"{amount:,.0f}"
    else:
        formatted = f"{amount:,.{decimals}f}"

    return f"{symbol}{formatted}{suffix}"

amounts = [1234.56, 9999.99, 150000, 42.5, 0.99]
currencies = ["USD", "EUR", "GBP", "JPY", "INR"]

print("Currency formatting examples:")
for amount in amounts:
    print(f"\nAmount: {amount}")
    for currency in currencies:
        formatted = format_currency(amount, currency)
        print(f"  {currency}: {formatted}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 4: Progress Bar Display")
print("="*40)

def create_progress_bar(percentage, width=50, style="default"):
    styles = {
        "default": ("█", "░"),
        "arrows": (">", "-"),
        "dots": ("●", "○"),
        "blocks": ("■", "□"),
        "ascii": ("#", "-")
    }

    if style not in styles:
        style = "default"

    filled_char, empty_char = styles[style]

    percentage = max(0, min(100, percentage))

    filled_width = int(width * percentage / 100)
    empty_width = width - filled_width

    bar = filled_char * filled_width + empty_char * empty_width

    return f"[{bar}] {percentage:3.0f}%"

print("Different progress bar styles:\n")

percentages = [0, 25, 50, 75, 100]
styles = ["default", "arrows", "dots", "blocks", "ascii"]

for style in styles:
    print(f"{style.capitalize()} style:")
    for percent in percentages:
        bar = create_progress_bar(percent, width=30, style=style)
        print(f"  {bar}")
    print()

print("Simulating download progress:")
for i in range(0, 101, 10):
    bar = create_progress_bar(i, width=40)
    print(f"Downloading: {bar}")

print("\n" + "="*40)
print("ADVANCED FORMATTING")
print("="*40)

print("Number formatting:")
num = 1234567.89
print(f"Default: {num}")
print(f"Thousands separator: {num:,}")
print(f"Fixed decimals: {num:.2f}")
print(f"Scientific: {num:.2e}")
print(f"Percentage: {0.856:.1%}")

print("\nAlignment and padding:")
text = "Python"
print(f"|{text:<15}| Left aligned")
print(f"|{text:>15}| Right aligned")
print(f"|{text:^15}| Centered")
print(f"|{text:*^15}| Centered with fill")

print("\nDate/time formatting:")
now = datetime.now()
print(f"Default: {now}")
print(f"Date only: {now:%Y-%m-%d}")
print(f"Time only: {now:%H:%M:%S}")
print(f"Full: {now:%A, %B %d, %Y at %I:%M %p}")

print("\nConditional formatting:")
scores = [95, 82, 67, 55, 100]
for score in scores:
    grade = "PASS" if score >= 60 else "FAIL"
    color = "🟢" if score >= 60 else "🔴"
    print(f"Score: {score:3} - {grade:<4} {color}")

print("\n" + "="*40)
print("FORMAT SPECIFICATION MINI-LANGUAGE")
print("="*40)

value = 42.123456789
print(f"Value: {value}")
print(f"Width 10: |{value:10}|")
print(f"Width 10, 2 decimals: |{value:10.2f}|")
print(f"Zero-padded: {value:010.2f}")
print(f"Sign always: {value:+.2f}")
print(f"Sign for negative: {-value:+.2f}")
print(f"Space for positive: {value: .2f}")

print("\nBase conversions:")
num = 255
print(f"Decimal: {num}")
print(f"Binary: {num:b} or 0b{num:b}")
print(f"Octal: {num:o} or 0o{num:o}")
print(f"Hexadecimal: {num:x} or 0x{num:X}")

print("\n" + "="*40)
print("DYNAMIC FORMATTING")
print("="*40)

def create_table(headers, data):
    col_widths = []
    for i, header in enumerate(headers):
        max_width = len(header)
        for row in data:
            max_width = max(max_width, len(str(row[i])))
        col_widths.append(max_width + 2)

    separator = "+" + "+".join("-" * w for w in col_widths) + "+"

    print(separator)
    header_row = "|"
    for header, width in zip(headers, col_widths):
        header_row += f" {header:^{width-2}} |"
    print(header_row)
    print(separator)

    for row in data:
        data_row = "|"
        for item, width in zip(row, col_widths):
            if isinstance(item, (int, float)):
                data_row += f" {item:>{width-2}} |"
            else:
                data_row += f" {item:<{width-2}} |"
        print(data_row)

    print(separator)

headers = ["Name", "Age", "Score", "Grade"]
data = [
    ["Alice", 25, 95.5, "A"],
    ["Bob", 30, 82.3, "B"],
    ["Charlie", 22, 77.8, "C"],
    ["Diana", 28, 91.2, "A"]
]

create_table(headers, data)

print("\n" + "="*40)
print("KEY TAKEAWAYS")
print("="*40)
print("""
1. f-strings are the most readable and efficient
2. Use format specs for alignment and precision
3. .format() is good for template reuse
4. % formatting is legacy but still seen
5. Format specs work in f-strings and .format()
6. Dynamic formatting enables flexible output
""")