"""
Week 8: Advanced Features
Concepts: Generators, Decorators, Regular Expressions
"""

import time
import re
from functools import wraps
import random

print("="*60)
print("WEEK 8: ADVANCED FEATURES - TUTORIAL AND SOLUTIONS")
print("="*60)

print("\n" + "="*40)
print("8.1: GENERATORS")
print("="*40)

print("""
Generators are memory-efficient iterators:
- Use yield instead of return
- Generate values on-the-fly
- Maintain state between calls
- Useful for large datasets
""")

print("\nPRACTICE PROBLEM 1: Infinite Sequence Generator")
print("-" * 40)

def infinite_counter(start=0, step=1):
    """Generate infinite sequence of numbers"""
    current = start
    while True:
        yield current
        current += step

counter = infinite_counter(10, 2)
print("First 10 values from infinite counter:")
for _ in range(10):
    print(f"  {next(counter)}", end=" ")
print()

print("\nPRACTICE PROBLEM 2: Large File Reader")
print("-" * 40)

def read_large_file_simulator(num_lines=1000000):
    """Simulate reading a large file line by line"""
    for i in range(num_lines):
        yield f"Line {i+1}: Sample data {random.randint(1, 100)}"

def process_file_in_chunks(generator, chunk_size=100):
    """Process file in chunks to save memory"""
    chunk = []
    for line in generator:
        chunk.append(line)
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk

file_gen = read_large_file_simulator(1000)
chunk_processor = process_file_in_chunks(file_gen, 250)

print("Processing simulated large file in chunks:")
for i, chunk in enumerate(chunk_processor, 1):
    print(f"  Chunk {i}: {len(chunk)} lines")
    print(f"    First line: {chunk[0]}")
    print(f"    Last line: {chunk[-1]}")

print("\nPRACTICE PROBLEM 3: Fibonacci Generator")
print("-" * 40)

def fibonacci_generator():
    """Generate Fibonacci sequence"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def fibonacci_up_to(limit):
    """Generate Fibonacci numbers up to a limit"""
    fib = fibonacci_generator()
    for num in fib:
        if num > limit:
            break
        yield num

print("Fibonacci numbers up to 100:")
for num in fibonacci_up_to(100):
    print(f"  {num}", end=" ")
print()

print("\nPRACTICE PROBLEM 4: Prime Number Generator")
print("-" * 40)

def prime_generator():
    """Generate prime numbers infinitely"""
    yield 2
    primes = [2]
    candidate = 3

    while True:
        is_prime = True
        for prime in primes:
            if prime * prime > candidate:
                break
            if candidate % prime == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(candidate)
            yield candidate

        candidate += 2

def first_n_primes(n):
    """Get first n prime numbers"""
    gen = prime_generator()
    return [next(gen) for _ in range(n)]

primes = first_n_primes(20)
print(f"First 20 primes: {primes}")

print("\n" + "="*40)
print("8.2: DECORATORS")
print("="*40)

print("""
Decorators modify function behavior:
- Function that takes a function
- Returns modified function
- @ syntax for application
- Can stack multiple decorators
""")

print("\nPRACTICE PROBLEM 1: Timing Decorator")
print("-" * 40)

def timer(func):
    """Measure function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"  {func.__name__} took {end - start:.6f} seconds")
        return result
    return wrapper

@timer
def slow_function(n):
    """Simulate slow function"""
    total = 0
    for i in range(n):
        total += i ** 2
    return total

result = slow_function(100000)
print(f"  Result: {result}")

print("\nPRACTICE PROBLEM 2: Authentication Decorator")
print("-" * 40)

def require_auth(role=None):
    """Decorator to check authentication"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get('user', {})

            if not user.get('authenticated'):
                return "Error: Authentication required"

            if role and user.get('role') != role:
                return f"Error: Role '{role}' required"

            return func(*args, **kwargs)
        return wrapper
    return decorator

@require_auth(role='admin')
def admin_function(user):
    return f"Admin access granted for {user.get('name')}"

@require_auth()
def user_function(user):
    return f"User access granted for {user.get('name')}"

users = [
    {'name': 'Alice', 'authenticated': True, 'role': 'admin'},
    {'name': 'Bob', 'authenticated': True, 'role': 'user'},
    {'name': 'Charlie', 'authenticated': False, 'role': 'user'}
]

for user in users:
    print(f"{user['name']}:")
    print(f"  Admin function: {admin_function(user=user)}")
    print(f"  User function: {user_function(user=user)}")

print("\nPRACTICE PROBLEM 3: Caching Decorator")
print("-" * 40)

def cache(func):
    """Cache function results"""
    cached_results = {}

    @wraps(func)
    def wrapper(*args):
        if args in cached_results:
            print(f"  Cache hit for {args}")
            return cached_results[args]

        print(f"  Computing for {args}")
        result = func(*args)
        cached_results[args] = result
        return result

    wrapper.cache_clear = lambda: cached_results.clear()
    wrapper.cache_info = lambda: f"Cache size: {len(cached_results)}"

    return wrapper

@cache
def expensive_computation(n):
    """Simulate expensive computation"""
    time.sleep(0.1)
    return n ** 3

print("Testing cache decorator:")
print(f"First call: {expensive_computation(5)}")
print(f"Second call (cached): {expensive_computation(5)}")
print(f"New computation: {expensive_computation(7)}")
print(expensive_computation.cache_info())

print("\nPRACTICE PROBLEM 4: Logging Decorator")
print("-" * 40)

def log_calls(log_args=True, log_result=True):
    """Log function calls"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log_msg = f"Calling {func.__name__}"

            if log_args:
                log_msg += f" with args={args}, kwargs={kwargs}"

            print(f"  LOG: {log_msg}")

            result = func(*args, **kwargs)

            if log_result:
                print(f"  LOG: {func.__name__} returned {result}")

            return result
        return wrapper
    return decorator

@log_calls(log_args=True, log_result=True)
def add(a, b):
    return a + b

@log_calls(log_args=False, log_result=True)
def multiply(x, y):
    return x * y

add(5, 3)
multiply(4, 7)

print("\n" + "="*40)
print("8.3: REGULAR EXPRESSIONS")
print("="*40)

print("""
Regular expressions for pattern matching:
- Pattern matching in strings
- Search, match, replace operations
- Powerful text processing
- Groups for extraction
""")

print("\nPRACTICE PROBLEM 1: Validate Email Addresses")
print("-" * 40)

def validate_email(email):
    """Validate email using regex"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

emails = [
    "user@example.com",
    "john.doe+filter@company.co.uk",
    "invalid@",
    "@invalid.com",
    "no-at-sign.com",
    "spaces in@email.com"
]

print("Email validation:")
for email in emails:
    valid = validate_email(email)
    status = "✓" if valid else "✗"
    print(f"  {status} {email}")

print("\nPRACTICE PROBLEM 2: Extract Phone Numbers")
print("-" * 40)

def extract_phone_numbers(text):
    """Extract various phone number formats"""
    patterns = [
        r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        r'\(\d{3}\)\s*\d{3}[-.]?\d{4}',
        r'\b\d{3}\s\d{3}\s\d{4}\b'
    ]

    combined_pattern = '|'.join(patterns)
    return re.findall(combined_pattern, text)

text = """
Contact us at 555-123-4567 or (555) 987-6543.
Alternative numbers: 555.246.8901 and 555 369 2580.
Invalid: 12345 or 555-12-345.
"""

phone_numbers = extract_phone_numbers(text)
print(f"Found phone numbers: {phone_numbers}")

print("\nPRACTICE PROBLEM 3: Simple Markdown Parser")
print("-" * 40)

class MarkdownParser:
    """Parse basic markdown syntax"""

    @staticmethod
    def parse(text):
        """Parse markdown to HTML"""
        text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)

        text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)

        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)

        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)

        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

        return text

markdown = """# Main Title
This is **bold text** and this is *italic text*.
Here's a [link](https://example.com) and some `inline code`.
## Subtitle
More content here."""

html = MarkdownParser.parse(markdown)
print("Markdown:")
print(markdown)
print("\nConverted HTML:")
print(html)

print("\nPRACTICE PROBLEM 4: Log File Analyzer")
print("-" * 40)

def analyze_log_file(log_text):
    """Extract information from log entries"""
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ips = re.findall(ip_pattern, log_text)

    date_pattern = r'\d{4}-\d{2}-\d{2}'
    dates = re.findall(date_pattern, log_text)

    error_pattern = r'ERROR:?\s*(.+?)(?:\n|$)'
    errors = re.findall(error_pattern, log_text, re.IGNORECASE)

    url_pattern = r'(?:GET|POST)\s+([^\s]+)'
    urls = re.findall(url_pattern, log_text)

    return {
        'ip_addresses': list(set(ips)),
        'dates': list(set(dates)),
        'errors': errors,
        'urls': urls
    }

log_sample = """
2024-01-15 10:30:15 - 192.168.1.100 - GET /api/users - 200
2024-01-15 10:30:16 - 192.168.1.101 - GET /api/products - 200
2024-01-15 10:30:17 - 192.168.1.100 - POST /api/login - 401
2024-01-15 10:30:18 - ERROR: Database connection timeout
2024-01-15 10:30:19 - 192.168.1.102 - GET /api/orders - 500
2024-01-15 10:30:20 - ERROR: Invalid user credentials
"""

analysis = analyze_log_file(log_sample)
print("Log analysis:")
for key, value in analysis.items():
    print(f"  {key}: {value}")

print("\n" + "="*40)
print("ADVANCED PATTERNS")
print("="*40)

def generator_decorator(func):
    """Decorator for generators"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        print(f"  Starting generator: {func.__name__}")
        for value in gen:
            print(f"    Yielding: {value}")
            yield value
        print(f"  Generator exhausted: {func.__name__}")
    return wrapper

@generator_decorator
def countdown(n):
    """Countdown generator"""
    while n > 0:
        yield n
        n -= 1

print("Decorated generator:")
for num in countdown(3):
    print(f"  Got: {num}")

print("\nClass decorators:")

def add_repr(cls):
    """Add __repr__ method to class"""
    def __repr__(self):
        attrs = ', '.join(f'{k}={v}' for k, v in self.__dict__.items())
        return f"{cls.__name__}({attrs})"
    cls.__repr__ = __repr__
    return cls

@add_repr
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(3, 4)
print(f"Point with auto-generated repr: {p}")

print("\nProperty decorators:")

class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self._celsius = (value - 32) * 5/9

temp = Temperature()
temp.celsius = 25
print(f"25°C = {temp.fahrenheit}°F")
temp.fahrenheit = 86
print(f"86°F = {temp.celsius}°C")

print("\n" + "="*40)
print("KEY TAKEAWAYS")
print("="*40)
print("""
1. Generators save memory for large datasets
2. yield maintains state between calls
3. Decorators modify function behavior cleanly
4. Multiple decorators can be stacked
5. Regex is powerful for text processing
6. Compile regex patterns for better performance
7. Use raw strings (r'') for regex patterns
""")