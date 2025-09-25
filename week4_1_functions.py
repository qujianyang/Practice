"""
Week 4.1: Functions
Concepts: def, parameters, return, scope
"""

import math

print("="*60)
print("WEEK 4.1: FUNCTIONS - TUTORIAL AND SOLUTIONS")
print("="*60)

print("\n" + "="*40)
print("TUTORIAL: Creating Reusable Code with Functions")
print("="*40)

print("""
Functions are reusable blocks of code:
- Defined with 'def' keyword
- Can accept parameters (inputs)
- Can return values (outputs)
- Have their own scope

Benefits:
- Code reusability
- Better organization
- Easier testing
- Modularity
""")

print("\n" + "="*40)
print("BASIC FUNCTION EXAMPLES")
print("="*40)

def greet():
    """Simple function with no parameters"""
    print("Hello from a function!")

def greet_person(name):
    """Function with one parameter"""
    print(f"Hello, {name}!")

def add_numbers(a, b):
    """Function with return value"""
    return a + b

def get_info():
    """Function returning multiple values"""
    return "Python", 3.9, True

greet()
greet_person("Alice")
result = add_numbers(5, 3)
print(f"5 + 3 = {result}")

lang, version, is_awesome = get_info()
print(f"Language: {lang}, Version: {version}, Awesome: {is_awesome}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 1: Geometric Calculations")
print("="*40)

def calculate_circle_area(radius):
    """Calculate the area of a circle"""
    return math.pi * radius ** 2

def calculate_circle_perimeter(radius):
    """Calculate the perimeter (circumference) of a circle"""
    return 2 * math.pi * radius

def calculate_rectangle_area(length, width):
    """Calculate the area of a rectangle"""
    return length * width

def calculate_rectangle_perimeter(length, width):
    """Calculate the perimeter of a rectangle"""
    return 2 * (length + width)

def calculate_triangle_area(base, height):
    """Calculate the area of a triangle"""
    return 0.5 * base * height

def calculate_triangle_perimeter(a, b, c):
    """Calculate the perimeter of a triangle"""
    return a + b + c

def calculate_sphere_volume(radius):
    """Calculate the volume of a sphere"""
    return (4/3) * math.pi * radius ** 3

def calculate_sphere_surface_area(radius):
    """Calculate the surface area of a sphere"""
    return 4 * math.pi * radius ** 2

print("Circle with radius 5:")
print(f"  Area: {calculate_circle_area(5):.2f}")
print(f"  Perimeter: {calculate_circle_perimeter(5):.2f}")

print("\nRectangle 10x5:")
print(f"  Area: {calculate_rectangle_area(10, 5)}")
print(f"  Perimeter: {calculate_rectangle_perimeter(10, 5)}")

print("\nTriangle with base 8, height 6:")
print(f"  Area: {calculate_triangle_area(8, 6)}")
print(f"  Perimeter (sides 3,4,5): {calculate_triangle_perimeter(3, 4, 5)}")

print("\nSphere with radius 3:")
print(f"  Volume: {calculate_sphere_volume(3):.2f}")
print(f"  Surface Area: {calculate_sphere_surface_area(3):.2f}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 2: Unit Converter")
print("="*40)

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius"""
    return (fahrenheit - 32) * 5/9

def meters_to_feet(meters):
    """Convert meters to feet"""
    return meters * 3.28084

def feet_to_meters(feet):
    """Convert feet to meters"""
    return feet / 3.28084

def kg_to_pounds(kg):
    """Convert kilograms to pounds"""
    return kg * 2.20462

def pounds_to_kg(pounds):
    """Convert pounds to kilograms"""
    return pounds / 2.20462

def liters_to_gallons(liters):
    """Convert liters to gallons"""
    return liters * 0.264172

def gallons_to_liters(gallons):
    """Convert gallons to liters"""
    return gallons / 0.264172

print("Temperature Conversions:")
temps = [0, 25, 100]
for temp in temps:
    f = celsius_to_fahrenheit(temp)
    print(f"  {temp}°C = {f:.1f}°F")

print("\nLength Conversions:")
lengths = [1, 5, 10]
for length in lengths:
    feet = meters_to_feet(length)
    print(f"  {length}m = {feet:.2f}ft")

print("\nWeight Conversions:")
weights = [1, 50, 100]
for weight in weights:
    pounds = kg_to_pounds(weight)
    print(f"  {weight}kg = {pounds:.2f}lbs")

print("\n" + "="*40)
print("PRACTICE PROBLEM 3: Recursive Functions")
print("="*40)

def factorial_iterative(n):
    """Calculate factorial using iteration"""
    if n < 0:
        return None
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def factorial_recursive(n):
    """Calculate factorial using recursion"""
    if n < 0:
        return None
    if n == 0 or n == 1:
        return 1
    return n * factorial_recursive(n - 1)

def fibonacci_iterative(n):
    """Generate nth Fibonacci number using iteration"""
    if n <= 0:
        return None
    if n == 1:
        return 0
    if n == 2:
        return 1

    a, b = 0, 1
    for _ in range(2, n):
        a, b = b, a + b
    return b

def fibonacci_recursive(n):
    """Generate nth Fibonacci number using recursion"""
    if n <= 0:
        return None
    if n == 1:
        return 0
    if n == 2:
        return 1
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

def fibonacci_memoized(n, memo={}):
    """Optimized recursive Fibonacci with memoization"""
    if n <= 0:
        return None
    if n == 1:
        return 0
    if n == 2:
        return 1
    if n in memo:
        return memo[n]

    memo[n] = fibonacci_memoized(n - 1, memo) + fibonacci_memoized(n - 2, memo)
    return memo[n]

print("Factorial calculations:")
for n in [0, 5, 10]:
    iter_result = factorial_iterative(n)
    rec_result = factorial_recursive(n)
    print(f"  {n}! = {iter_result} (iterative) = {rec_result} (recursive)")

print("\nFibonacci sequence:")
print("First 10 Fibonacci numbers:")
for i in range(1, 11):
    fib = fibonacci_memoized(i)
    print(f"  F({i}) = {fib}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 4: Luhn Algorithm (Credit Card Validation)")
print("="*40)

def validate_credit_card(card_number):
    """
    Validate credit card number using Luhn algorithm
    """
    card_str = str(card_number).replace(" ", "").replace("-", "")

    if not card_str.isdigit():
        return False

    digits = [int(d) for d in card_str]

    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9

    return sum(digits) % 10 == 0

def get_card_type(card_number):
    """Determine credit card type from number"""
    card_str = str(card_number).replace(" ", "").replace("-", "")

    if card_str.startswith('4'):
        return "Visa"
    elif card_str[:2] in ['51', '52', '53', '54', '55']:
        return "MasterCard"
    elif card_str[:2] in ['34', '37']:
        return "American Express"
    elif card_str.startswith('6011'):
        return "Discover"
    else:
        return "Unknown"

test_cards = [
    "4532015112830366",
    "5425233430109903",
    "374245455400126",
    "6011000990139424",
    "1234567890123456",
    "4111111111111111"
]

print("Credit Card Validation:")
for card in test_cards:
    is_valid = validate_credit_card(card)
    card_type = get_card_type(card)
    status = "✓ Valid" if is_valid else "✗ Invalid"
    print(f"  {card}: {card_type} - {status}")

print("\n" + "="*40)
print("FUNCTION PARAMETERS")
print("="*40)

def demonstrate_parameters(required, default="default", *args, **kwargs):
    """Demonstrate different parameter types"""
    print(f"Required parameter: {required}")
    print(f"Default parameter: {default}")
    print(f"Additional positional args: {args}")
    print(f"Keyword arguments: {kwargs}")

print("Different ways to call the function:")
demonstrate_parameters("value1")
print()
demonstrate_parameters("value1", "custom")
print()
demonstrate_parameters("value1", "custom", "extra1", "extra2")
print()
demonstrate_parameters("value1", key1="val1", key2="val2")

print("\n" + "="*40)
print("SCOPE AND GLOBAL VARIABLES")
print("="*40)

global_var = "I'm global"

def demonstrate_scope():
    local_var = "I'm local"
    print(f"Inside function - local: {local_var}")
    print(f"Inside function - global: {global_var}")

    def nested_function():
        nested_var = "I'm nested"
        print(f"Inside nested - nested: {nested_var}")
        print(f"Inside nested - can access local: {local_var}")
        print(f"Inside nested - can access global: {global_var}")

    nested_function()
    return local_var

def modify_global():
    global global_var
    global_var = "Modified global"
    print(f"Modified global variable: {global_var}")

print(f"Before function call: {global_var}")
result = demonstrate_scope()
print(f"After function call: {global_var}")
modify_global()
print(f"After modification: {global_var}")

print("\n" + "="*40)
print("LAMBDA FUNCTIONS")
print("="*40)

square = lambda x: x ** 2
add = lambda x, y: x + y
is_even = lambda x: x % 2 == 0

print(f"Square of 5: {square(5)}")
print(f"Add 3 and 7: {add(3, 7)}")
print(f"Is 4 even? {is_even(4)}")
print(f"Is 5 even? {is_even(5)}")

numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(f"\nSquares of {numbers}: {squared}")

evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Even numbers from {numbers}: {evens}")

print("\n" + "="*40)
print("FUNCTION DOCUMENTATION")
print("="*40)

def well_documented_function(param1, param2=10):
    """
    This is a well-documented function.

    Args:
        param1 (int): The first parameter
        param2 (int, optional): The second parameter. Defaults to 10.

    Returns:
        int: The sum of param1 and param2

    Example:
        >>> well_documented_function(5)
        15
        >>> well_documented_function(5, 20)
        25
    """
    return param1 + param2

print(f"Function name: {well_documented_function.__name__}")
print(f"Function docstring: {well_documented_function.__doc__}")
print(f"Result: {well_documented_function(5)}")

print("\n" + "="*40)
print("KEY TAKEAWAYS")
print("="*40)
print("""
1. Functions provide code reusability and organization
2. Parameters can be required, default, *args, or **kwargs
3. Functions can return single or multiple values
4. Recursion is powerful but can be memory-intensive
5. Lambda functions are useful for simple operations
6. Scope determines variable accessibility
7. Good documentation improves code maintainability
""")