"""
Week 2.2: Basic String Operations
Concepts: String methods, concatenation, slicing
"""

print("="*60)
print("WEEK 2.2: BASIC STRING OPERATIONS - TUTORIAL AND SOLUTIONS")
print("="*60)

print("\n" + "="*40)
print("TUTORIAL: String Manipulation")
print("="*40)

print("""
Strings are immutable sequences of characters.

Common methods:
- upper(), lower(), title(), capitalize()
- strip(), lstrip(), rstrip()
- split(), join()
- replace(), find(), count()
- startswith(), endswith()
- isalpha(), isdigit(), isalnum()
""")

print("\n" + "="*40)
print("BASIC STRING OPERATIONS")
print("="*40)

text = "  Hello, Python World!  "
print(f"Original: '{text}'")
print(f"Strip whitespace: '{text.strip()}'")
print(f"Uppercase: '{text.upper()}'")
print(f"Lowercase: '{text.lower()}'")
print(f"Title case: '{text.title()}'")
print(f"Replace: '{text.replace('Python', 'Amazing Python')}'")

words = text.strip().split()
print(f"Split into words: {words}")
print(f"Join with '-': '{'-'.join(words)}'")

print(f"\nString length: {len(text)}")
print(f"Count 'o': {text.count('o')}")
print(f"Find 'Python': index {text.find('Python')}")
print(f"Starts with '  Hello': {text.startswith('  Hello')}")
print(f"Ends with '!  ': {text.endswith('!  ')}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 1: Password Strength Checker")
print("="*40)

def check_password_strength(password):
    strength_score = 0
    feedback = []

    if len(password) >= 8:
        strength_score += 1
        feedback.append("✓ At least 8 characters")
    else:
        feedback.append("✗ Should be at least 8 characters")

    if any(c.isupper() for c in password):
        strength_score += 1
        feedback.append("✓ Contains uppercase letter")
    else:
        feedback.append("✗ Add uppercase letter")

    if any(c.islower() for c in password):
        strength_score += 1
        feedback.append("✓ Contains lowercase letter")
    else:
        feedback.append("✗ Add lowercase letter")

    if any(c.isdigit() for c in password):
        strength_score += 1
        feedback.append("✓ Contains number")
    else:
        feedback.append("✗ Add number")

    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if any(c in special_chars for c in password):
        strength_score += 1
        feedback.append("✓ Contains special character")
    else:
        feedback.append("✗ Add special character")

    if strength_score <= 2:
        strength = "Weak"
    elif strength_score <= 3:
        strength = "Medium"
    elif strength_score <= 4:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return strength, strength_score, feedback

test_passwords = [
    "password",
    "Password1",
    "Pass@123",
    "MyP@ssw0rd!",
    "abc",
    "ThisIsALongPasswordWithoutNumbers"
]

for pwd in test_passwords:
    strength, score, feedback = check_password_strength(pwd)
    print(f"\nPassword: '{pwd}'")
    print(f"Strength: {strength} (Score: {score}/5)")
    for item in feedback:
        print(f"  {item}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 2: Count Vowels and Consonants")
print("="*40)

def count_vowels_consonants(sentence):
    vowels = "aeiouAEIOU"
    vowel_count = 0
    consonant_count = 0
    digit_count = 0
    special_count = 0

    for char in sentence:
        if char.isalpha():
            if char in vowels:
                vowel_count += 1
            else:
                consonant_count += 1
        elif char.isdigit():
            digit_count += 1
        elif not char.isspace():
            special_count += 1

    return {
        'vowels': vowel_count,
        'consonants': consonant_count,
        'digits': digit_count,
        'special': special_count,
        'spaces': sentence.count(' ')
    }

test_sentences = [
    "Hello World!",
    "Python Programming 123",
    "The quick brown fox jumps over the lazy dog.",
    "Testing @ 2024!"
]

for sentence in test_sentences:
    counts = count_vowels_consonants(sentence)
    print(f"\nSentence: '{sentence}'")
    print(f"  Vowels: {counts['vowels']}")
    print(f"  Consonants: {counts['consonants']}")
    print(f"  Digits: {counts['digits']}")
    print(f"  Special chars: {counts['special']}")
    print(f"  Spaces: {counts['spaces']}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 3: Caesar Cipher")
print("="*40)

def caesar_cipher(text, shift):
    result = ""

    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            shifted = (ord(char) - ascii_offset + shift) % 26
            result += chr(shifted + ascii_offset)
        else:
            result += char

    return result

def caesar_decipher(text, shift):
    return caesar_cipher(text, -shift)

original = "Hello, World! Python 123"
shift = 3

encrypted = caesar_cipher(original, shift)
decrypted = caesar_decipher(encrypted, shift)

print(f"Original: {original}")
print(f"Encrypted (shift {shift}): {encrypted}")
print(f"Decrypted: {decrypted}")

print("\nTesting different shifts:")
message = "Secret Message"
for s in [1, 5, 13, 25]:
    enc = caesar_cipher(message, s)
    print(f"Shift {s:2}: {enc}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 4: Extract Email Domain")
print("="*40)

def extract_email_domain(email):
    if '@' not in email:
        return None

    parts = email.split('@')
    if len(parts) != 2:
        return None

    domain = parts[1]

    if '.' not in domain:
        return None

    return domain

def extract_all_domains(email_list):
    domains = {}
    for email in email_list:
        domain = extract_email_domain(email.strip())
        if domain:
            domains[domain] = domains.get(domain, 0) + 1
    return domains

emails = [
    "user@gmail.com",
    "admin@company.co.uk",
    "info@website.org",
    "support@gmail.com",
    "invalid-email",
    "test@domain",
    "another@company.co.uk",
    "contact@website.org"
]

print("Individual email domain extraction:")
for email in emails:
    domain = extract_email_domain(email)
    if domain:
        print(f"{email:25} -> {domain}")
    else:
        print(f"{email:25} -> Invalid email format")

print("\nDomain frequency analysis:")
domain_counts = extract_all_domains(emails)
for domain, count in sorted(domain_counts.items()):
    print(f"  {domain}: {count} email(s)")

print("\n" + "="*40)
print("STRING SLICING AND INDEXING")
print("="*40)

sample = "Python Programming"
print(f"String: '{sample}'")
print(f"Length: {len(sample)}")
print(f"First character: '{sample[0]}'")
print(f"Last character: '{sample[-1]}'")
print(f"First 6 chars: '{sample[:6]}'")
print(f"Last 11 chars: '{sample[-11:]}'")
print(f"Characters 7-17: '{sample[7:18]}'")
print(f"Every 2nd char: '{sample[::2]}'")
print(f"Reversed: '{sample[::-1]}'")

print("\n" + "="*40)
print("STRING FORMATTING METHODS")
print("="*40)

name = "alice"
age = 25
height = 165.5

print("Different formatting methods:")
print("1. Concatenation: " + "Name is " + name.title() + " and age is " + str(age))
print("2. % formatting: Name is %s and age is %d" % (name.title(), age))
print("3. format(): Name is {} and age is {}".format(name.title(), age))
print("4. f-string: Name is %s and age is %d" % (name.title(), age))
print(f"5. f-string: Name is {name.title()}, age is {age}, height is {height:.1f}cm")

print("\n" + "="*40)
print("STRING VALIDATION METHODS")
print("="*40)

test_strings = ["hello", "Hello123", "123", "  ", "", "ABC", "user@email"]

for s in test_strings:
    print(f"\n'{s}':")
    print(f"  isalpha(): {s.isalpha()}")
    print(f"  isdigit(): {s.isdigit()}")
    print(f"  isalnum(): {s.isalnum()}")
    print(f"  isspace(): {s.isspace()}")
    print(f"  isupper(): {s.isupper()}")
    print(f"  islower(): {s.islower()}")

print("\n" + "="*40)
print("KEY TAKEAWAYS")
print("="*40)
print("""
1. Strings are immutable - methods return new strings
2. Use string methods for common operations
3. String slicing works like list slicing
4. f-strings provide the most readable formatting
5. Validation methods help check string properties
6. join() and split() are powerful for processing
""")