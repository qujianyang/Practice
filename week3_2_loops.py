"""
Week 3.2: Loops
Concepts: for loops, while loops, break, continue
"""

print("="*60)
print("WEEK 3.2: LOOPS - TUTORIAL AND SOLUTIONS")
print("="*60)

print("\n" + "="*40)
print("TUTORIAL: Iteration with Loops")
print("="*40)

print("""
Python has two main loop types:

1. for loop: Iterate over sequences
   - Lists, strings, ranges, dictionaries
   - Known number of iterations

2. while loop: Repeat while condition is True
   - Unknown number of iterations
   - Condition-based repetition

Control statements:
- break: Exit the loop
- continue: Skip to next iteration
- else: Execute after normal loop completion
""")

print("\n" + "="*40)
print("FOR LOOP EXAMPLES")
print("="*40)

print("Iterating over a list:")
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"  {fruit}")

print("\nIterating with index using enumerate:")
for i, fruit in enumerate(fruits):
    print(f"  {i}: {fruit}")

print("\nIterating over a range:")
for i in range(5):
    print(f"  {i}", end=" ")
print()

print("\nIterating over a string:")
word = "Python"
for char in word:
    print(f"  {char}", end=" ")
print()

print("\nIterating over dictionary:")
person = {"name": "Alice", "age": 30, "city": "NYC"}
for key, value in person.items():
    print(f"  {key}: {value}")

print("\n" + "="*40)
print("WHILE LOOP EXAMPLES")
print("="*40)

count = 0
print("Count to 5:")
while count < 5:
    print(f"  {count}", end=" ")
    count += 1
print()

print("\nFind first power of 2 greater than 1000:")
power = 1
exponent = 0
while power <= 1000:
    power *= 2
    exponent += 1
print(f"  2^{exponent} = {power}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 1: Multiplication Tables")
print("="*40)

def print_multiplication_tables(max_num=12):
    for i in range(1, max_num + 1):
        print(f"\nMultiplication table for {i}:")
        for j in range(1, 11):
            result = i * j
            print(f"  {i:2} × {j:2} = {result:3}")

print("Multiplication tables from 1 to 5:")
for num in range(1, 6):
    print(f"\nTable for {num}:")
    for mult in range(1, 6):
        print(f"  {num} × {mult} = {num * mult}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 2: Find Prime Numbers")
print("="*40)

def find_primes(limit):
    primes = []

    for num in range(2, limit + 1):
        is_prime = True

        for divisor in range(2, int(num ** 0.5) + 1):
            if num % divisor == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(num)

    return primes

def sieve_of_eratosthenes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

    return [i for i in range(2, limit + 1) if is_prime[i]]

limit = 100
primes = find_primes(limit)
print(f"Prime numbers up to {limit}:")
for i, prime in enumerate(primes):
    print(f"{prime:3}", end=" ")
    if (i + 1) % 10 == 0:
        print()
print(f"\n\nFound {len(primes)} prime numbers")

print("\nUsing Sieve of Eratosthenes:")
sieve_primes = sieve_of_eratosthenes(50)
print(f"Primes up to 50: {sieve_primes}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 3: Pyramid Pattern Printer")
print("="*40)

def print_pyramid(height):
    print(f"\nPyramid with height {height}:")
    for i in range(1, height + 1):
        spaces = " " * (height - i)
        stars = "*" * (2 * i - 1)
        print(spaces + stars)

def print_inverted_pyramid(height):
    print(f"\nInverted pyramid with height {height}:")
    for i in range(height, 0, -1):
        spaces = " " * (height - i)
        stars = "*" * (2 * i - 1)
        print(spaces + stars)

def print_diamond(height):
    print(f"\nDiamond with height {height}:")
    for i in range(1, height + 1):
        spaces = " " * (height - i)
        stars = "*" * (2 * i - 1)
        print(spaces + stars)

    for i in range(height - 1, 0, -1):
        spaces = " " * (height - i)
        stars = "*" * (2 * i - 1)
        print(spaces + stars)

def print_number_pyramid(height):
    print(f"\nNumber pyramid with height {height}:")
    for i in range(1, height + 1):
        spaces = " " * (height - i)
        numbers = ""
        for j in range(1, i + 1):
            numbers += str(j)
        for j in range(i - 1, 0, -1):
            numbers += str(j)
        print(spaces + numbers)

print_pyramid(5)
print_inverted_pyramid(5)
print_diamond(4)
print_number_pyramid(5)

print("\n" + "="*40)
print("PRACTICE PROBLEM 4: Menu-Driven Program")
print("="*40)

def calculator_menu():
    print("\nSimple Calculator Demo")
    operations = {
        '1': ('Addition', lambda x, y: x + y),
        '2': ('Subtraction', lambda x, y: x - y),
        '3': ('Multiplication', lambda x, y: x * y),
        '4': ('Division', lambda x, y: x / y if y != 0 else "Error: Division by zero"),
        '5': ('Power', lambda x, y: x ** y)
    }

    demo_calculations = [
        ('1', 10, 5),
        ('2', 20, 8),
        ('3', 7, 6),
        ('4', 15, 3),
        ('5', 2, 8)
    ]

    for choice, num1, num2 in demo_calculations:
        if choice in operations:
            name, operation = operations[choice]
            result = operation(num1, num2)
            print(f"{name}: {num1} and {num2} = {result}")

calculator_menu()

print("\n" + "="*40)
print("BREAK AND CONTINUE EXAMPLES")
print("="*40)

print("Using break to exit early:")
for i in range(10):
    if i == 5:
        print(f"  Breaking at {i}")
        break
    print(f"  {i}", end=" ")
print()

print("\nUsing continue to skip iterations:")
for i in range(10):
    if i % 2 == 0:
        continue
    print(f"  {i}", end=" ")
print()

print("\n\nFinding first number divisible by both 7 and 11:")
for num in range(1, 100):
    if num % 7 == 0 and num % 11 == 0:
        print(f"  Found: {num}")
        break

print("\n" + "="*40)
print("NESTED LOOPS")
print("="*40)

print("Matrix creation:")
rows, cols = 3, 4
matrix = []
for i in range(rows):
    row = []
    for j in range(cols):
        row.append(i * cols + j + 1)
    matrix.append(row)

for row in matrix:
    for element in row:
        print(f"{element:3}", end=" ")
    print()

print("\nPattern with nested loops:")
for i in range(1, 6):
    for j in range(1, i + 1):
        print(j, end=" ")
    print()

print("\n" + "="*40)
print("LOOP WITH ELSE CLAUSE")
print("="*40)

print("Search with else clause:")
numbers = [2, 4, 6, 8, 10]
search_for = 7

for num in numbers:
    if num == search_for:
        print(f"Found {search_for}!")
        break
else:
    print(f"{search_for} not found in list")

print("\nPrime check with else:")
num = 29
for i in range(2, int(num ** 0.5) + 1):
    if num % i == 0:
        print(f"{num} is not prime (divisible by {i})")
        break
else:
    print(f"{num} is prime!")

print("\n" + "="*40)
print("INFINITE LOOPS (with safety limit)")
print("="*40)

print("Collatz sequence (3n+1 problem):")
def collatz_sequence(n, max_steps=100):
    steps = 0
    sequence = [n]

    while n != 1 and steps < max_steps:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        sequence.append(n)
        steps += 1

    return sequence, steps

start_num = 27
sequence, steps = collatz_sequence(start_num)
print(f"Starting with {start_num}:")
print(f"Sequence: {sequence[:10]}...")
print(f"Reached 1 in {steps} steps")

print("\n" + "="*40)
print("LIST COMPREHENSION vs LOOPS")
print("="*40)

print("Traditional loop:")
squares_loop = []
for i in range(1, 6):
    squares_loop.append(i ** 2)
print(f"  {squares_loop}")

print("\nList comprehension:")
squares_comp = [i ** 2 for i in range(1, 6)]
print(f"  {squares_comp}")

print("\nFiltered with loop:")
evens_loop = []
for i in range(1, 11):
    if i % 2 == 0:
        evens_loop.append(i)
print(f"  {evens_loop}")

print("\nFiltered with comprehension:")
evens_comp = [i for i in range(1, 11) if i % 2 == 0]
print(f"  {evens_comp}")

print("\n" + "="*40)
print("KEY TAKEAWAYS")
print("="*40)
print("""
1. Use for loops for known iterations
2. Use while loops for condition-based repetition
3. break exits the loop entirely
4. continue skips to next iteration
5. else clause executes if loop completes normally
6. Nested loops for multi-dimensional iteration
7. List comprehensions are often more Pythonic
""")