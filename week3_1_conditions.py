"""
Week 3.1: Conditions
Concepts: if, elif, else, nested conditions
"""

import random

print("="*60)
print("WEEK 3.1: CONDITIONS - TUTORIAL AND SOLUTIONS")
print("="*60)

print("\n" + "="*40)
print("TUTORIAL: Decision Making with Conditions")
print("="*40)

print("""
Conditional statements control program flow:
- if: Execute code if condition is True
- elif: Check another condition if previous was False
- else: Execute if all conditions were False

Conditions can be:
- Comparison: ==, !=, <, >, <=, >=
- Logical: and, or, not
- Membership: in, not in
- Identity: is, is not
""")

print("\n" + "="*40)
print("BASIC CONDITIONAL EXAMPLES")
print("="*40)

age = 18
print(f"Age: {age}")

if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")

score = 85
print(f"\nScore: {score}")

if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
elif score >= 70:
    grade = 'C'
elif score >= 60:
    grade = 'D'
else:
    grade = 'F'

print(f"Grade: {grade}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 1: Number Guessing Game")
print("="*40)

def number_guessing_game():
    secret = random.randint(1, 100)
    max_attempts = 7
    attempts = 0

    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100")
    print(f"You have {max_attempts} attempts to guess it")

    while attempts < max_attempts:
        attempts += 1

        try:
            guess = int(input(f"\nAttempt {attempts}: Enter your guess: "))
        except ValueError:
            print("Please enter a valid number!")
            continue

        if guess < 1 or guess > 100:
            print("Please guess a number between 1 and 100!")
            continue

        if guess == secret:
            print(f"Congratulations! You guessed it in {attempts} attempts!")
            return True
        elif guess < secret:
            if secret - guess > 20:
                print("Too low! (Way off)")
            else:
                print("Too low! (Getting warm)")
        else:
            if guess - secret > 20:
                print("Too high! (Way off)")
            else:
                print("Too high! (Getting warm)")

        remaining = max_attempts - attempts
        if remaining > 0:
            print(f"Attempts remaining: {remaining}")

    print(f"\nSorry! The number was {secret}")
    return False

print("\nDemo mode (automatic play):")
secret = random.randint(1, 100)
print(f"Secret number for demo: {secret}")

demo_guesses = [50, 75, 62, 68, secret]
for i, guess in enumerate(demo_guesses, 1):
    print(f"\nGuess {i}: {guess}")
    if guess == secret:
        print("Correct! You win!")
        break
    elif guess < secret:
        print("Too low!")
    else:
        print("Too high!")

print("\n" + "="*40)
print("PRACTICE PROBLEM 2: ATM Machine Simulation")
print("="*40)

class ATM:
    def __init__(self, initial_balance=1000):
        self.balance = initial_balance
        self.pin = "1234"
        self.attempts = 0
        self.locked = False

    def authenticate(self, pin):
        if self.locked:
            print("Account is locked. Please contact customer service.")
            return False

        if pin == self.pin:
            self.attempts = 0
            return True
        else:
            self.attempts += 1
            if self.attempts >= 3:
                self.locked = True
                print("Too many incorrect attempts. Account locked.")
            else:
                print(f"Incorrect PIN. {3 - self.attempts} attempts remaining.")
            return False

    def check_balance(self):
        print(f"Current balance: ${self.balance:.2f}")

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid amount")
        elif amount > self.balance:
            print("Insufficient funds")
        elif amount > 500:
            print("Daily withdrawal limit is $500")
        else:
            self.balance -= amount
            print(f"Withdrew ${amount:.2f}")
            print(f"New balance: ${self.balance:.2f}")

    def deposit(self, amount):
        if amount <= 0:
            print("Invalid amount")
        elif amount > 10000:
            print("Deposit limit is $10,000. Please see teller.")
        else:
            self.balance += amount
            print(f"Deposited ${amount:.2f}")
            print(f"New balance: ${self.balance:.2f}")

atm = ATM(1500)

print("ATM Demo:")
print("Attempting wrong PIN twice:")
atm.authenticate("0000")
atm.authenticate("1111")

print("\nCorrect PIN:")
if atm.authenticate("1234"):
    print("Authentication successful!")

    atm.check_balance()

    print("\nTrying to withdraw $2000:")
    atm.withdraw(2000)

    print("\nWithdrawing $200:")
    atm.withdraw(200)

    print("\nDepositing $500:")
    atm.deposit(500)

    atm.check_balance()

print("\n" + "="*40)
print("PRACTICE PROBLEM 3: Triangle Type Determiner")
print("="*40)

def determine_triangle_type(a, b, c):
    if a <= 0 or b <= 0 or c <= 0:
        return "Invalid", "Sides must be positive"

    if a + b <= c or a + c <= b or b + c <= a:
        return "Invalid", "Does not satisfy triangle inequality"

    if a == b == c:
        triangle_type = "Equilateral"
    elif a == b or b == c or a == c:
        triangle_type = "Isosceles"
    else:
        triangle_type = "Scalene"

    if a**2 + b**2 == c**2 or a**2 + c**2 == b**2 or b**2 + c**2 == a**2:
        angle_type = "Right"
    elif (a**2 + b**2 < c**2) or (a**2 + c**2 < b**2) or (b**2 + c**2 < a**2):
        angle_type = "Obtuse"
    else:
        angle_type = "Acute"

    return triangle_type, angle_type

test_triangles = [
    (3, 3, 3),
    (3, 4, 5),
    (5, 5, 8),
    (2, 3, 10),
    (6, 8, 10),
    (5, 12, 13),
    (-1, 2, 3),
    (7, 10, 12)
]

for sides in test_triangles:
    a, b, c = sides
    result = determine_triangle_type(a, b, c)
    print(f"Sides: {sides}")
    if result[0] == "Invalid":
        print(f"  Result: {result[0]} - {result[1]}")
    else:
        print(f"  Type: {result[0]} {result[1]} triangle")

print("\n" + "="*40)
print("PRACTICE PROBLEM 4: Rock-Paper-Scissors Game")
print("="*40)

def play_rock_paper_scissors():
    choices = ["rock", "paper", "scissors"]
    rules = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper"
    }

    def determine_winner(player, computer):
        if player == computer:
            return "tie"
        elif rules[player] == computer:
            return "player"
        else:
            return "computer"

    print("Rock-Paper-Scissors Game Demo")

    rounds = 5
    player_score = 0
    computer_score = 0

    for round_num in range(1, rounds + 1):
        print(f"\nRound {round_num}:")

        player_choice = random.choice(choices)
        computer_choice = random.choice(choices)

        print(f"Player: {player_choice}")
        print(f"Computer: {computer_choice}")

        winner = determine_winner(player_choice, computer_choice)

        if winner == "tie":
            print("It's a tie!")
        elif winner == "player":
            print("Player wins this round!")
            player_score += 1
        else:
            print("Computer wins this round!")
            computer_score += 1

        print(f"Score: Player {player_score} - {computer_score} Computer")

    print("\n" + "="*20)
    print("FINAL RESULTS:")
    print(f"Player: {player_score}")
    print(f"Computer: {computer_score}")

    if player_score > computer_score:
        print("Player wins the game!")
    elif computer_score > player_score:
        print("Computer wins the game!")
    else:
        print("The game is a tie!")

play_rock_paper_scissors()

print("\n" + "="*40)
print("NESTED CONDITIONS")
print("="*40)

def check_eligibility(age, income, credit_score):
    print(f"Applicant: Age={age}, Income=${income:,}, Credit={credit_score}")

    if age >= 18:
        if income >= 30000:
            if credit_score >= 700:
                print("  ✓ Approved for premium loan")
            elif credit_score >= 600:
                print("  ✓ Approved for standard loan")
            else:
                print("  ✗ Denied - credit score too low")
        else:
            if credit_score >= 750:
                print("  ✓ Approved for limited loan")
            else:
                print("  ✗ Denied - insufficient income")
    else:
        print("  ✗ Denied - must be 18 or older")

applicants = [
    (25, 50000, 750),
    (17, 30000, 800),
    (30, 25000, 700),
    (22, 35000, 650),
    (40, 60000, 550),
    (35, 20000, 780)
]

for applicant in applicants:
    check_eligibility(*applicant)

print("\n" + "="*40)
print("CONDITIONAL EXPRESSIONS (Ternary)")
print("="*40)

x = 10
result = "positive" if x > 0 else "non-positive"
print(f"x = {x}, result = {result}")

age = 20
status = "adult" if age >= 18 else "minor"
print(f"age = {age}, status = {status}")

score = 75
passed = "Pass" if score >= 60 else "Fail"
print(f"score = {score}, result = {passed}")

print("\n" + "="*40)
print("KEY TAKEAWAYS")
print("="*40)
print("""
1. Use if/elif/else for decision making
2. Conditions evaluate to True or False
3. Multiple conditions can be combined with and/or
4. Nested conditions handle complex logic
5. Ternary operator for simple conditional assignments
6. Order of elif matters - first True condition wins
""")