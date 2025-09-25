"""
Week 7: Functional Programming
Concepts: List comprehensions, lambda functions, map/filter/reduce
"""

from functools import reduce
import operator

print("="*60)
print("WEEK 7: FUNCTIONAL PROGRAMMING - TUTORIAL AND SOLUTIONS")
print("="*60)

print("\n" + "="*40)
print("7.1: LIST COMPREHENSIONS")
print("="*40)

print("""
List comprehensions provide concise list creation:
- Basic: [expression for item in iterable]
- With condition: [expr for item in iterable if condition]
- Nested: [expr for x in iter1 for y in iter2]
""")

print("\nPRACTICE PROBLEM 1: Filter and Transform Data")
print("-" * 40)

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

squares = [x**2 for x in data]
print(f"Squares: {squares}")

evens = [x for x in data if x % 2 == 0]
print(f"Even numbers: {evens}")

even_squares = [x**2 for x in data if x % 2 == 0]
print(f"Squares of even numbers: {even_squares}")

transformed = [x/2 if x % 2 == 0 else x*3 for x in data]
print(f"Conditional transformation: {transformed}")

print("\nPRACTICE PROBLEM 2: Matrix Transpose")
print("-" * 40)

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

transpose = [[row[i] for row in matrix] for i in range(len(matrix[0]))]

print("Original matrix:")
for row in matrix:
    print(f"  {row}")

print("\nTransposed matrix:")
for row in transpose:
    print(f"  {row}")

print("\nPRACTICE PROBLEM 3: Generate Primes with Comprehension")
print("-" * 40)

def primes_comprehension(limit):
    """Generate primes using list comprehension"""
    return [n for n in range(2, limit + 1)
            if all(n % i != 0 for i in range(2, int(n**0.5) + 1))]

primes = primes_comprehension(50)
print(f"Primes up to 50: {primes}")

print("\nPRACTICE PROBLEM 4: Flatten Nested Lists")
print("-" * 40)

nested = [[1, 2, 3], [4, 5], [6, 7, 8, 9], [10]]
flattened = [item for sublist in nested for item in sublist]
print(f"Nested: {nested}")
print(f"Flattened: {flattened}")

deeply_nested = [[1, [2, 3]], [4, [5, [6, 7]]], 8]

def flatten_deep(lst):
    """Recursively flatten deeply nested lists"""
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten_deep(item))
        else:
            result.append(item)
    return result

print(f"\nDeeply nested: {deeply_nested}")
print(f"Flattened: {flatten_deep(deeply_nested)}")

print("\n" + "="*40)
print("7.2: LAMBDA FUNCTIONS")
print("="*40)

print("""
Lambda functions are anonymous inline functions:
- Syntax: lambda arguments: expression
- Single expression only
- Useful for short operations
""")

print("\nPRACTICE PROBLEM 1: Sort Complex Data")
print("-" * 40)

students = [
    {'name': 'Alice', 'grade': 85, 'age': 20},
    {'name': 'Bob', 'grade': 92, 'age': 22},
    {'name': 'Charlie', 'grade': 78, 'age': 21},
    {'name': 'Diana', 'grade': 95, 'age': 19}
]

by_grade = sorted(students, key=lambda x: x['grade'], reverse=True)
print("Sorted by grade (descending):")
for s in by_grade:
    print(f"  {s['name']}: {s['grade']}")

by_age = sorted(students, key=lambda x: x['age'])
print("\nSorted by age (ascending):")
for s in by_age:
    print(f"  {s['name']}: {s['age']}")

print("\nPRACTICE PROBLEM 2: Expression Evaluator")
print("-" * 40)

operations = {
    'add': lambda x, y: x + y,
    'subtract': lambda x, y: x - y,
    'multiply': lambda x, y: x * y,
    'divide': lambda x, y: x / y if y != 0 else 'Error',
    'power': lambda x, y: x ** y,
    'modulo': lambda x, y: x % y
}

a, b = 10, 3
for op_name, op_func in operations.items():
    result = op_func(a, b)
    print(f"  {op_name}({a}, {b}) = {result}")

print("\nPRACTICE PROBLEM 3: Functional Calculators")
print("-" * 40)

def make_calculator(operation):
    """Create calculator functions using lambdas"""
    ops = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y if y != 0 else float('inf'),
        '**': lambda x, y: x ** y
    }
    return ops.get(operation, lambda x, y: None)

add = make_calculator('+')
multiply = make_calculator('*')

print(f"add(5, 3) = {add(5, 3)}")
print(f"multiply(4, 7) = {multiply(4, 7)}")

print("\nPRACTICE PROBLEM 4: Custom Filters")
print("-" * 40)

numbers = list(range(1, 21))

filters = {
    'even': lambda x: x % 2 == 0,
    'odd': lambda x: x % 2 != 0,
    'prime': lambda x: x > 1 and all(x % i != 0 for i in range(2, int(x**0.5) + 1)),
    'perfect_square': lambda x: int(x**0.5) ** 2 == x,
    'multiple_of_3': lambda x: x % 3 == 0
}

for filter_name, filter_func in filters.items():
    filtered = list(filter(filter_func, numbers))
    print(f"{filter_name}: {filtered}")

print("\n" + "="*40)
print("7.3: MAP, FILTER, REDUCE")
print("="*40)

print("""
Higher-order functions for functional programming:
- map(): Apply function to all items
- filter(): Select items based on condition
- reduce(): Aggregate items to single value
""")

print("\nPRACTICE PROBLEM 1: Process Large Dataset")
print("-" * 40)

sales_data = [
    {'product': 'A', 'quantity': 10, 'price': 15.50},
    {'product': 'B', 'quantity': 5, 'price': 25.00},
    {'product': 'C', 'quantity': 8, 'price': 10.75},
    {'product': 'D', 'quantity': 12, 'price': 8.25},
    {'product': 'E', 'quantity': 3, 'price': 45.00}
]

totals = list(map(lambda x: x['quantity'] * x['price'], sales_data))
print(f"Sale totals: {[f'${t:.2f}' for t in totals]}")

high_value = list(filter(lambda x: x['quantity'] * x['price'] > 100, sales_data))
print(f"High-value sales (>$100): {[x['product'] for x in high_value]}")

total_revenue = reduce(lambda acc, x: acc + x['quantity'] * x['price'], sales_data, 0)
print(f"Total revenue: ${total_revenue:.2f}")

print("\nPRACTICE PROBLEM 2: Data Pipeline")
print("-" * 40)

def create_pipeline(*functions):
    """Create a data processing pipeline"""
    def pipeline(data):
        result = data
        for func in functions:
            result = func(result)
        return result
    return pipeline

numbers = list(range(1, 11))

pipeline = create_pipeline(
    lambda x: map(lambda n: n ** 2, x),
    lambda x: filter(lambda n: n > 20, x),
    lambda x: map(lambda n: n / 2, x),
    list
)

result = pipeline(numbers)
print(f"Original: {numbers}")
print(f"After pipeline (square -> filter >20 -> divide by 2): {result}")

print("\nPRACTICE PROBLEM 3: Statistical Functions")
print("-" * 40)

data = [23, 45, 67, 89, 12, 34, 56, 78, 90, 21]

mean = reduce(lambda a, b: a + b, data) / len(data)
print(f"Data: {data}")
print(f"Mean: {mean:.2f}")

squared_diffs = list(map(lambda x: (x - mean) ** 2, data))
variance = reduce(lambda a, b: a + b, squared_diffs) / len(data)
std_dev = variance ** 0.5
print(f"Variance: {variance:.2f}")
print(f"Standard deviation: {std_dev:.2f}")

median_sorted = sorted(data)
n = len(median_sorted)
median = median_sorted[n//2] if n % 2 else (median_sorted[n//2-1] + median_sorted[n//2]) / 2
print(f"Median: {median}")

print("\nPRACTICE PROBLEM 4: Functional Text Processor")
print("-" * 40)

text = "The quick brown fox jumps over the lazy dog"

words = text.split()
print(f"Original: {text}")

word_lengths = list(map(len, words))
print(f"Word lengths: {word_lengths}")

long_words = list(filter(lambda w: len(w) > 3, words))
print(f"Words longer than 3 chars: {long_words}")

uppercase = list(map(str.upper, words))
print(f"Uppercase: {' '.join(uppercase)}")

reversed_words = list(map(lambda w: w[::-1], words))
print(f"Reversed words: {' '.join(reversed_words)}")

total_chars = reduce(operator.add, map(len, words))
print(f"Total characters (no spaces): {total_chars}")

print("\n" + "="*40)
print("ADVANCED FUNCTIONAL PATTERNS")
print("="*40)

def compose(*functions):
    """Compose multiple functions"""
    def inner(x):
        for f in reversed(functions):
            x = f(x)
        return x
    return inner

def curry(func):
    """Convert function to curried form"""
    def curried(x):
        def inner(y):
            return func(x, y)
        return inner
    return curried

def memoize(func):
    """Cache function results"""
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

add_10 = compose(
    lambda x: x + 5,
    lambda x: x + 5
)
print(f"Composed function add_10(5): {add_10(5)}")

@curry
def multiply(x, y):
    return x * y

times_5 = multiply(5)
print(f"Curried multiply: times_5(3) = {times_5(3)}")

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(f"Memoized Fibonacci(10): {fibonacci(10)}")

print("\nDictionary and Set Comprehensions:")
print("-" * 40)

words = ['apple', 'banana', 'cherry', 'date']
word_lengths = {word: len(word) for word in words}
print(f"Word lengths dict: {word_lengths}")

numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_squares = {x**2 for x in numbers}
print(f"Unique squares set: {unique_squares}")

matrix_dict = {(i, j): i * j for i in range(1, 4) for j in range(1, 4)}
print(f"Multiplication table dict: {matrix_dict}")

print("\nGenerator Expressions:")
print("-" * 40)

sum_of_squares = sum(x**2 for x in range(1, 11))
print(f"Sum of squares 1-10: {sum_of_squares}")

any_negative = any(x < 0 for x in [1, 2, -3, 4])
print(f"Any negative numbers: {any_negative}")

all_positive = all(x > 0 for x in [1, 2, 3, 4])
print(f"All positive numbers: {all_positive}")

print("\n" + "="*40)
print("KEY TAKEAWAYS")
print("="*40)
print("""
1. List comprehensions are more Pythonic than loops
2. Lambda functions are useful for short operations
3. map/filter/reduce enable functional programming
4. Generator expressions save memory
5. Functional programming can make code more concise
6. Combine functional tools for powerful data pipelines
7. Dict/set comprehensions extend the pattern
""")