"""
Week 4.2: Modules and Packages
Concepts: import, creating modules, __name__
"""

import math
import random
import datetime
from collections import Counter, defaultdict
import os
import sys

print("="*60)
print("WEEK 4.2: MODULES AND PACKAGES - TUTORIAL AND SOLUTIONS")
print("="*60)

print("\n" + "="*40)
print("TUTORIAL: Organizing Code with Modules")
print("="*40)

print("""
Modules help organize and reuse code:
- A module is a Python file containing code
- Packages are directories containing modules
- import statement loads modules

Import methods:
- import module
- from module import function
- from module import *
- import module as alias
""")

print("\n" + "="*40)
print("BUILT-IN MODULES")
print("="*40)

print("Math module examples:")
print(f"  Pi: {math.pi:.6f}")
print(f"  Square root of 16: {math.sqrt(16)}")
print(f"  Sine of 90 degrees: {math.sin(math.radians(90))}")
print(f"  10 factorial: {math.factorial(10)}")

print("\nRandom module examples:")
print(f"  Random float [0,1): {random.random():.4f}")
print(f"  Random int [1,10]: {random.randint(1, 10)}")
print(f"  Random choice: {random.choice(['apple', 'banana', 'cherry'])}")
numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)
print(f"  Shuffled list: {numbers}")

print("\nDatetime module examples:")
now = datetime.datetime.now()
print(f"  Current time: {now}")
print(f"  Date only: {now.date()}")
print(f"  Time only: {now.time()}")
print(f"  Formatted: {now.strftime('%B %d, %Y at %I:%M %p')}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 1: Math Utility Module")
print("="*40)

class MathUtils:
    """Math utility module with various mathematical functions"""

    @staticmethod
    def is_prime(n):
        """Check if a number is prime"""
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def gcd(a, b):
        """Calculate greatest common divisor"""
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def lcm(a, b):
        """Calculate least common multiple"""
        return abs(a * b) // MathUtils.gcd(a, b)

    @staticmethod
    def prime_factors(n):
        """Find all prime factors of a number"""
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return factors

    @staticmethod
    def is_perfect_square(n):
        """Check if a number is a perfect square"""
        if n < 0:
            return False
        root = int(n ** 0.5)
        return root * root == n

    @staticmethod
    def distance_2d(x1, y1, x2, y2):
        """Calculate Euclidean distance between two points"""
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    def quadratic_formula(a, b, c):
        """Solve quadratic equation ax^2 + bx + c = 0"""
        discriminant = b ** 2 - 4 * a * c
        if discriminant < 0:
            return None
        elif discriminant == 0:
            return -b / (2 * a)
        else:
            root1 = (-b + math.sqrt(discriminant)) / (2 * a)
            root2 = (-b - math.sqrt(discriminant)) / (2 * a)
            return root1, root2

print("Testing MathUtils module:")
print(f"Is 17 prime? {MathUtils.is_prime(17)}")
print(f"Is 20 prime? {MathUtils.is_prime(20)}")
print(f"GCD of 48 and 18: {MathUtils.gcd(48, 18)}")
print(f"LCM of 12 and 15: {MathUtils.lcm(12, 15)}")
print(f"Prime factors of 60: {MathUtils.prime_factors(60)}")
print(f"Is 64 a perfect square? {MathUtils.is_perfect_square(64)}")
print(f"Distance between (0,0) and (3,4): {MathUtils.distance_2d(0, 0, 3, 4)}")
print(f"Quadratic x^2 - 5x + 6 = 0: {MathUtils.quadratic_formula(1, -5, 6)}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 2: Date Calculator Module")
print("="*40)

class DateCalculator:
    """Date calculation utilities"""

    @staticmethod
    def days_between(date1, date2):
        """Calculate days between two dates"""
        if isinstance(date1, str):
            date1 = datetime.datetime.strptime(date1, "%Y-%m-%d").date()
        if isinstance(date2, str):
            date2 = datetime.datetime.strptime(date2, "%Y-%m-%d").date()
        return abs((date2 - date1).days)

    @staticmethod
    def add_days(date, days):
        """Add days to a date"""
        if isinstance(date, str):
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        return date + datetime.timedelta(days=days)

    @staticmethod
    def get_weekday(date):
        """Get weekday name from date"""
        if isinstance(date, str):
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday",
                   "Friday", "Saturday", "Sunday"]
        return weekdays[date.weekday()]

    @staticmethod
    def is_weekend(date):
        """Check if date is weekend"""
        if isinstance(date, str):
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        return date.weekday() >= 5

    @staticmethod
    def age_in_days(birthdate):
        """Calculate age in days"""
        if isinstance(birthdate, str):
            birthdate = datetime.datetime.strptime(birthdate, "%Y-%m-%d").date()
        today = datetime.date.today()
        return (today - birthdate).days

    @staticmethod
    def business_days_between(date1, date2):
        """Calculate business days between two dates"""
        if isinstance(date1, str):
            date1 = datetime.datetime.strptime(date1, "%Y-%m-%d").date()
        if isinstance(date2, str):
            date2 = datetime.datetime.strptime(date2, "%Y-%m-%d").date()

        if date1 > date2:
            date1, date2 = date2, date1

        business_days = 0
        current = date1
        while current <= date2:
            if current.weekday() < 5:
                business_days += 1
            current += datetime.timedelta(days=1)
        return business_days

print("Testing DateCalculator module:")
today = datetime.date.today().strftime("%Y-%m-%d")
print(f"Today: {today}")
print(f"Days between 2024-01-01 and 2024-12-31: {DateCalculator.days_between('2024-01-01', '2024-12-31')}")
print(f"10 days from today: {DateCalculator.add_days(today, 10)}")
print(f"Today is: {DateCalculator.get_weekday(today)}")
print(f"Is today weekend? {DateCalculator.is_weekend(today)}")
print(f"Business days in January 2024: {DateCalculator.business_days_between('2024-01-01', '2024-01-31')}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 3: Text Processing Toolkit")
print("="*40)

class TextProcessor:
    """Text processing utilities"""

    @staticmethod
    def word_count(text):
        """Count words in text"""
        return len(text.split())

    @staticmethod
    def character_count(text, include_spaces=True):
        """Count characters in text"""
        if include_spaces:
            return len(text)
        return len(text.replace(" ", ""))

    @staticmethod
    def sentence_count(text):
        """Count sentences in text"""
        import re
        sentences = re.split(r'[.!?]+', text)
        return len([s for s in sentences if s.strip()])

    @staticmethod
    def most_common_words(text, n=5):
        """Find most common words"""
        words = text.lower().split()
        words = [w.strip('.,!?";') for w in words]
        return Counter(words).most_common(n)

    @staticmethod
    def remove_punctuation(text):
        """Remove punctuation from text"""
        import string
        return text.translate(str.maketrans('', '', string.punctuation))

    @staticmethod
    def reverse_words(text):
        """Reverse order of words"""
        return ' '.join(text.split()[::-1])

    @staticmethod
    def extract_emails(text):
        """Extract email addresses from text"""
        import re
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(pattern, text)

    @staticmethod
    def extract_urls(text):
        """Extract URLs from text"""
        import re
        pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(pattern, text)

    @staticmethod
    def readability_score(text):
        """Calculate simple readability score"""
        words = text.split()
        sentences = TextProcessor.sentence_count(text)
        if sentences == 0:
            return 0

        avg_words_per_sentence = len(words) / sentences
        avg_word_length = sum(len(w) for w in words) / len(words)

        score = 206.835 - 1.015 * avg_words_per_sentence - 84.6 * (avg_word_length / 4.7)
        return max(0, min(100, score))

sample_text = """
Python is a powerful programming language. It's used for web development,
data science, and more! Contact us at info@example.com or visit
https://python.org for more information. Python makes coding fun.
"""

print("Testing TextProcessor module:")
print(f"Word count: {TextProcessor.word_count(sample_text)}")
print(f"Character count (with spaces): {TextProcessor.character_count(sample_text)}")
print(f"Character count (no spaces): {TextProcessor.character_count(sample_text, False)}")
print(f"Sentence count: {TextProcessor.sentence_count(sample_text)}")
print(f"Most common words: {TextProcessor.most_common_words(sample_text)}")
print(f"Emails found: {TextProcessor.extract_emails(sample_text)}")
print(f"URLs found: {TextProcessor.extract_urls(sample_text)}")
print(f"Readability score: {TextProcessor.readability_score(sample_text):.2f}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 4: File Operations Module")
print("="*40)

class FileOperations:
    """File operation utilities"""

    @staticmethod
    def get_file_info(filepath):
        """Get information about a file"""
        if not os.path.exists(filepath):
            return None

        stats = os.stat(filepath)
        return {
            'path': filepath,
            'size': stats.st_size,
            'modified': datetime.datetime.fromtimestamp(stats.st_mtime),
            'created': datetime.datetime.fromtimestamp(stats.st_ctime),
            'is_file': os.path.isfile(filepath),
            'is_directory': os.path.isdir(filepath)
        }

    @staticmethod
    def list_files(directory, extension=None):
        """List files in directory"""
        if not os.path.exists(directory):
            return []

        files = []
        for item in os.listdir(directory):
            filepath = os.path.join(directory, item)
            if os.path.isfile(filepath):
                if extension is None or item.endswith(extension):
                    files.append(item)
        return files

    @staticmethod
    def create_backup_name(filename):
        """Create backup filename with timestamp"""
        name, ext = os.path.splitext(filename)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{name}_backup_{timestamp}{ext}"

    @staticmethod
    def safe_create_directory(path):
        """Safely create directory if it doesn't exist"""
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating directory: {e}")
            return False

    @staticmethod
    def get_file_extension(filename):
        """Get file extension"""
        return os.path.splitext(filename)[1].lower()

    @staticmethod
    def format_file_size(size_bytes):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

print("Testing FileOperations module:")
current_file = __file__
print(f"Current file: {current_file}")

info = FileOperations.get_file_info(current_file)
if info:
    print(f"File size: {FileOperations.format_file_size(info['size'])}")
    print(f"Modified: {info['modified']}")

print(f"Backup name: {FileOperations.create_backup_name('data.txt')}")
print(f"Extension of 'document.pdf': {FileOperations.get_file_extension('document.pdf')}")

print("\n" + "="*40)
print("MODULE IMPORT PATTERNS")
print("="*40)

print("Different import styles:")
print("1. import math - Access as math.pi")
print("2. from math import pi - Access as pi")
print("3. from math import * - Imports all (not recommended)")
print("4. import math as m - Access as m.pi")
print("5. from math import pi as PI - Access as PI")

print("\n" + "="*40)
print("THE __name__ VARIABLE")
print("="*40)

def main():
    """Main function to run when module is executed directly"""
    print("This module is being run directly")

if __name__ == "__main__":
    print(f"Module name when run directly: {__name__}")
    print("The if __name__ == '__main__' block executes only when")
    print("the module is run directly, not when imported")
else:
    print(f"Module name when imported: {__name__}")

print("\n" + "="*40)
print("KEY TAKEAWAYS")
print("="*40)
print("""
1. Modules help organize and reuse code
2. Python has many built-in modules
3. Custom modules are just Python files
4. Use if __name__ == "__main__" for module testing
5. Different import styles for different needs
6. Packages are directories with __init__.py
7. Good module design improves code maintainability
""")