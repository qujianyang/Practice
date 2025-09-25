"""
Week 1.3: Basic Operators
Concepts: Arithmetic, comparison, logical operators
"""

print("="*60)
print("WEEK 1.3: BASIC OPERATORS - TUTORIAL AND SOLUTIONS")
print("="*60)

print("\n" + "="*40)
print("TUTORIAL: Python Operators")
print("="*40)

print("""
Python has three main types of operators:

1. Arithmetic Operators:
   +  Addition       -  Subtraction    *  Multiplication
   /  Division       // Floor Division  %  Modulo
   ** Exponentiation

2. Comparison Operators:
   == Equal to       != Not equal      >  Greater than
   <  Less than      >= Greater/equal   <= Less/equal

3. Logical Operators:
   and  Logical AND  or  Logical OR    not  Logical NOT
""")

print("\n" + "="*40)
print("ARITHMETIC OPERATORS EXAMPLES")
print("="*40)

a = 10
b = 3

print(f"a = {a}, b = {b}")
print(f"Addition: {a} + {b} = {a + b}")
print(f"Subtraction: {a} - {b} = {a - b}")
print(f"Multiplication: {a} * {b} = {a * b}")
print(f"Division: {a} / {b} = {a / b:.2f}")
print(f"Floor Division: {a} // {b} = {a // b}")
print(f"Modulo: {a} % {b} = {a % b}")
print(f"Exponentiation: {a} ** {b} = {a ** b}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 1: Basic Calculator")
print("="*40)

def basic_calculator(num1, num2):
    print(f"\nCalculator for {num1} and {num2}:")
    print(f"Sum: {num1} + {num2} = {num1 + num2}")
    print(f"Difference: {num1} - {num2} = {num1 - num2}")
    print(f"Product: {num1} * {num2} = {num1 * num2}")
    if num2 != 0:
        print(f"Division: {num1} / {num2} = {num1 / num2:.2f}")
        print(f"Floor Division: {num1} // {num2} = {num1 // num2}")
        print(f"Remainder: {num1} % {num2} = {num1 % num2}")
    else:
        print("Division by zero is not allowed!")
    print(f"Power: {num1} ** {num2} = {num1 ** num2}")

basic_calculator(15, 4)
basic_calculator(7.5, 2.5)

print("\n" + "="*40)
print("PRACTICE PROBLEM 2: Leap Year Checker")
print("="*40)

def is_leap_year(year):
    """
    A year is a leap year if:
    - Divisible by 4 AND
    - (Not divisible by 100 OR divisible by 400)
    """
    is_leap = (year % 4 == 0) and (year % 100 != 0 or year % 400 == 0)
    return is_leap

test_years = [2000, 2020, 2021, 2024, 1900, 2100]
for year in test_years:
    if is_leap_year(year):
        print(f"{year} is a leap year")
    else:
        print(f"{year} is not a leap year")

print("\n" + "="*40)
print("PRACTICE PROBLEM 3: BMI Calculator")
print("="*40)

def calculate_bmi(weight_kg, height_m):
    bmi = weight_kg / (height_m ** 2)

    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal weight"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return bmi, category

weight = 70
height = 1.75
bmi, category = calculate_bmi(weight, height)
print(f"Weight: {weight} kg, Height: {height} m")
print(f"BMI: {bmi:.2f}")
print(f"Category: {category}")

print("\nTesting multiple cases:")
test_cases = [(50, 1.70), (75, 1.75), (90, 1.80), (100, 1.65)]
for w, h in test_cases:
    bmi, cat = calculate_bmi(w, h)
    print(f"Weight: {w}kg, Height: {h}m -> BMI: {bmi:.1f} ({cat})")

print("\n" + "="*40)
print("PRACTICE PROBLEM 4: Grade Calculator")
print("="*40)

def calculate_grade(homework, midterm, final, participation):
    """
    Calculate weighted grade:
    - Homework: 20%
    - Midterm: 30%
    - Final: 40%
    - Participation: 10%
    """
    weights = {
        'homework': 0.20,
        'midterm': 0.30,
        'final': 0.40,
        'participation': 0.10
    }

    weighted_score = (
        homework * weights['homework'] +
        midterm * weights['midterm'] +
        final * weights['final'] +
        participation * weights['participation']
    )

    if weighted_score >= 90:
        letter_grade = 'A'
    elif weighted_score >= 80:
        letter_grade = 'B'
    elif weighted_score >= 70:
        letter_grade = 'C'
    elif weighted_score >= 60:
        letter_grade = 'D'
    else:
        letter_grade = 'F'

    return weighted_score, letter_grade

print("Grade calculation with weighted scores:")
print("Weights: Homework(20%), Midterm(30%), Final(40%), Participation(10%)")

hw, mid, final, part = 85, 78, 92, 95
score, grade = calculate_grade(hw, mid, final, part)
print(f"\nScores: HW={hw}, Midterm={mid}, Final={final}, Participation={part}")
print(f"Weighted Score: {score:.2f}")
print(f"Letter Grade: {grade}")

print("\nTesting different scenarios:")
scenarios = [
    (95, 95, 95, 95),
    (80, 85, 82, 90),
    (70, 75, 72, 80),
    (60, 65, 58, 70)
]

for hw, mid, fin, part in scenarios:
    score, grade = calculate_grade(hw, mid, fin, part)
    print(f"Scores: {hw}/{mid}/{fin}/{part} -> {score:.1f} ({grade})")

print("\n" + "="*40)
print("COMPARISON OPERATORS EXAMPLES")
print("="*40)

x = 10
y = 20

print(f"x = {x}, y = {y}")
print(f"x == y: {x == y}")
print(f"x != y: {x != y}")
print(f"x > y: {x > y}")
print(f"x < y: {x < y}")
print(f"x >= 10: {x >= 10}")
print(f"y <= 20: {y <= 20}")

print("\n" + "="*40)
print("LOGICAL OPERATORS EXAMPLES")
print("="*40)

age = 25
has_license = True
is_insured = False

print(f"age = {age}, has_license = {has_license}, is_insured = {is_insured}")
print(f"Can drive (age >= 18 AND has_license): {age >= 18 and has_license}")
print(f"Can rent car (age >= 21 AND has_license AND is_insured): {age >= 21 and has_license and is_insured}")
print(f"Needs training (NOT has_license): {not has_license}")
print(f"Eligible for discount (age < 25 OR is_insured): {age < 25 or is_insured}")

print("\n" + "="*40)
print("OPERATOR PRECEDENCE")
print("="*40)

print("""
Order of operations (highest to lowest):
1. ()          Parentheses
2. **          Exponentiation
3. *, /, //, % Multiplication, Division, Floor, Modulo
4. +, -        Addition, Subtraction
5. <, <=, >, >=, ==, != Comparison
6. not         Logical NOT
7. and         Logical AND
8. or          Logical OR
""")

print("Examples:")
result1 = 2 + 3 * 4
print(f"2 + 3 * 4 = {result1} (multiplication first)")

result2 = (2 + 3) * 4
print(f"(2 + 3) * 4 = {result2} (parentheses first)")

result3 = 2 ** 3 * 4
print(f"2 ** 3 * 4 = {result3} (exponent first, then multiply)")

result4 = True or False and False
print(f"True or False and False = {result4} (and before or)")

print("\n" + "="*40)
print("KEY TAKEAWAYS")
print("="*40)
print("""
1. Arithmetic operators follow mathematical precedence
2. Use parentheses to control order of operations
3. Comparison operators return boolean values
4. Logical operators combine boolean expressions
5. Remember: and requires all conditions True, or needs just one
""")