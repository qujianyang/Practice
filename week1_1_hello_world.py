"""
Week 1.1: Hello, World!
Concepts: First program, print statement, basic syntax
"""

print("="*60)
print("WEEK 1.1: HELLO, WORLD! - TUTORIAL AND SOLUTIONS")
print("="*60)

print("\n" + "="*40)
print("TUTORIAL: Understanding Python Environment")
print("="*40)

print("""
The print() function is the most basic way to output text in Python.
Syntax: print("Your text here")

Key Points:
1. Python is case-sensitive (print not Print)
2. Strings can use single ('') or double ("") quotes
3. The print() function automatically adds a newline at the end
4. You can print multiple items separated by commas
""")

print("\n" + "="*40)
print("PRACTICE PROBLEM 1: Print Your Name")
print("="*40)

print("My name is John Doe")
print("I am learning Python!")

print("\n" + "="*40)
print("PRACTICE PROBLEM 2: Multiple Lines with Single Print")
print("="*40)

print("Line 1\nLine 2\nLine 3")

print("\nAlternative using triple quotes:")
print("""First line
Second line
Third line""")

print("\n" + "="*40)
print("PRACTICE PROBLEM 3: ASCII Art Pattern")
print("="*40)

print("   /\\_/\\  ")
print("  ( o.o ) ")
print("   > ^ <  ")
print("  /|   |\\ ")
print(" (_|   |_)")
print("\nSimple pyramid:")
print("    *")
print("   ***")
print("  *****")
print(" *******")
print("*********")

print("\n" + "="*40)
print("PRACTICE PROBLEM 4: Fix Buggy Code")
print("="*40)

print("Original buggy code: print(\"Hello World')")
print("Problem: Mismatched quotes (starts with \" ends with ')")
print("\nCorrected versions:")
print("Hello World")
print('Hello World')

print("\n" + "="*40)
print("ADDITIONAL EXAMPLES")
print("="*40)

print("Printing numbers:", 42)
print("Printing multiple items:", "Age:", 25, "Height:", 175.5)
print("Empty line below:")
print()
print("Line after empty line")

print("Using sep parameter:", "apple", "banana", "orange", sep=" | ")
print("Using end parameter:", "No newline", end=" -> ")
print("This continues on same line")

print("\n\n" + "="*40)
print("KEY TAKEAWAYS")
print("="*40)
print("""
1. print() is the basic output function
2. Use \\n for newlines within a string
3. Triple quotes preserve formatting
4. sep and end parameters customize output
5. Always match your quote types
""")