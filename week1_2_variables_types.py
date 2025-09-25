"""
Week 1.2: Variables and Types
Concepts: int, float, str, bool, type conversion
"""

print("="*60)
print("WEEK 1.2: VARIABLES AND TYPES - TUTORIAL AND SOLUTIONS")
print("="*60)

print("\n" + "="*40)
print("TUTORIAL: Understanding Data Types")
print("="*40)

print("""
Python has several built-in data types:
1. int     - Whole numbers (42, -10, 0)
2. float   - Decimal numbers (3.14, -0.5, 2.0)
3. str     - Text/strings ("Hello", 'Python')
4. bool    - True or False values

Variables store values and don't need type declaration.
Python automatically determines the type based on the value.
""")

print("\n" + "="*40)
print("BASIC EXAMPLES")
print("="*40)

my_integer = 42
my_float = 3.14159
my_string = "Python"
my_boolean = True

print(f"Integer: {my_integer}, Type: {type(my_integer)}")
print(f"Float: {my_float}, Type: {type(my_float)}")
print(f"String: {my_string}, Type: {type(my_string)}")
print(f"Boolean: {my_boolean}, Type: {type(my_boolean)}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 1: Personal Info Variables")
print("="*40)

name = "Alice Johnson"
age = 25
height = 165.5
is_student = True

print(f"Name: {name}")
print(f"Age: {age} years")
print(f"Height: {height} cm")
print(f"Is Student: {is_student}")

print("\nUsing type() to verify:")
print(f"name is {type(name).__name__}")
print(f"age is {type(age).__name__}")
print(f"height is {type(height).__name__}")
print(f"is_student is {type(is_student).__name__}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 2: Temperature Conversion")
print("="*40)

celsius = 25.0
fahrenheit = (celsius * 9/5) + 32

print(f"Temperature in Celsius: {celsius}°C")
print(f"Temperature in Fahrenheit: {fahrenheit}°F")

celsius_from_fahrenheit = (fahrenheit - 32) * 5/9
print(f"Converting back: {celsius_from_fahrenheit}°C")

print("\n" + "="*40)
print("PRACTICE PROBLEM 3: Compound Interest Calculator")
print("="*40)

principal = 1000.0
rate = 5.5
time = 2
n = 12

amount = principal * (1 + rate/(100*n))**(n*time)
compound_interest = amount - principal

print(f"Principal Amount: ${principal:.2f}")
print(f"Interest Rate: {rate}%")
print(f"Time Period: {time} years")
print(f"Compounding Frequency: {n} times per year")
print(f"Final Amount: ${amount:.2f}")
print(f"Compound Interest: ${compound_interest:.2f}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 4: Debug String + Number Error")
print("="*40)

print("Original problematic code: \"3\" + 4")
print("This causes TypeError because you can't add string to integer")

print("\nSolution 1: Convert string to int")
result1 = int("3") + 4
print(f"int(\"3\") + 4 = {result1}")

print("\nSolution 2: Convert number to string (concatenation)")
result2 = "3" + str(4)
print(f"\"3\" + str(4) = {result2}")

print("\n" + "="*40)
print("TYPE CONVERSION EXAMPLES")
print("="*40)

str_num = "42"
int_from_str = int(str_num)
print(f"String '{str_num}' converted to int: {int_from_str}")

float_num = 3.14
int_from_float = int(float_num)
print(f"Float {float_num} converted to int: {int_from_float} (truncates)")

int_val = 10
float_from_int = float(int_val)
print(f"Int {int_val} converted to float: {float_from_int}")

bool_from_int = bool(1)
bool_from_zero = bool(0)
print(f"bool(1) = {bool_from_int}, bool(0) = {bool_from_zero}")

bool_from_str = bool("Hello")
bool_from_empty = bool("")
print(f"bool(\"Hello\") = {bool_from_str}, bool(\"\") = {bool_from_empty}")

print("\n" + "="*40)
print("VARIABLE NAMING RULES")
print("="*40)

print("""
Valid variable names:
- my_variable (snake_case - Python convention)
- myVariable (camelCase - less common in Python)
- _private_var (starts with underscore)
- var123 (contains numbers)

Invalid variable names:
- 123var (can't start with number)
- my-var (no hyphens allowed)
- my var (no spaces)
- class (reserved keyword)
""")

valid_name = "user_age"
another_valid = "userName"
_private = "internal use"
var123 = 456

print(f"Examples of valid names: {valid_name}, {another_valid}, {_private}, {var123}")

print("\n" + "="*40)
print("KEY TAKEAWAYS")
print("="*40)
print("""
1. Variables don't need type declaration
2. Use type() to check variable type
3. Convert between types using int(), float(), str(), bool()
4. Be careful with type mismatches in operations
5. Follow Python naming conventions (snake_case)
""")