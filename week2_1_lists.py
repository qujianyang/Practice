"""
Week 2.1: Lists
Concepts: Creating, indexing, slicing, methods
"""

print("="*60)
print("WEEK 2.1: LISTS - TUTORIAL AND SOLUTIONS")
print("="*60)

print("\n" + "="*40)
print("TUTORIAL: Understanding Lists")
print("="*40)

print("""
Lists are ordered, mutable collections in Python.
- Created with square brackets []
- Can contain mixed data types
- Zero-indexed (first element is at index 0)
- Support negative indexing (last element is -1)

Common methods:
append(), extend(), insert(), remove(), pop(), clear()
index(), count(), sort(), reverse(), copy()
""")

print("\n" + "="*40)
print("BASIC LIST OPERATIONS")
print("="*40)

fruits = ["apple", "banana", "cherry", "date"]
print(f"Original list: {fruits}")

print(f"First element (index 0): {fruits[0]}")
print(f"Last element (index -1): {fruits[-1]}")
print(f"Slice [1:3]: {fruits[1:3]}")
print(f"Slice [:2]: {fruits[:2]}")
print(f"Slice [2:]: {fruits[2:]}")

fruits.append("elderberry")
print(f"After append('elderberry'): {fruits}")

fruits.insert(2, "blueberry")
print(f"After insert(2, 'blueberry'): {fruits}")

removed = fruits.pop()
print(f"After pop() - removed '{removed}': {fruits}")

fruits.remove("banana")
print(f"After remove('banana'): {fruits}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 1: Shopping Cart System")
print("="*40)

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        print(f"Added '{item}' to cart")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"Removed '{item}' from cart")
        else:
            print(f"'{item}' not found in cart")

    def display_cart(self):
        if self.items:
            print(f"Cart contains: {', '.join(self.items)}")
            print(f"Total items: {len(self.items)}")
        else:
            print("Cart is empty")

    def clear_cart(self):
        self.items.clear()
        print("Cart cleared")

cart = ShoppingCart()
cart.display_cart()

cart.add_item("Milk")
cart.add_item("Bread")
cart.add_item("Eggs")
cart.add_item("Cheese")
cart.display_cart()

cart.remove_item("Bread")
cart.display_cart()

cart.remove_item("Juice")

cart.add_item("Butter")
cart.display_cart()

print("\n" + "="*40)
print("PRACTICE PROBLEM 2: Find Second Largest Number")
print("="*40)

def find_second_largest(numbers):
    if len(numbers) < 2:
        return None

    unique_sorted = sorted(set(numbers), reverse=True)

    if len(unique_sorted) < 2:
        return None

    return unique_sorted[1]

test_lists = [
    [10, 20, 4, 45, 99],
    [1, 2, 3, 4, 5],
    [5, 5, 5, 5],
    [100],
    [50, 50, 100, 100]
]

for lst in test_lists:
    result = find_second_largest(lst)
    print(f"List: {lst}")
    print(f"Second largest: {result}\n")

print("\n" + "="*40)
print("PRACTICE PROBLEM 3: Reverse List Without reverse()")
print("="*40)

def reverse_list_manual(lst):
    reversed_list = []
    for i in range(len(lst) - 1, -1, -1):
        reversed_list.append(lst[i])
    return reversed_list

def reverse_list_slicing(lst):
    return lst[::-1]

def reverse_list_swap(lst):
    result = lst.copy()
    left = 0
    right = len(result) - 1

    while left < right:
        result[left], result[right] = result[right], result[left]
        left += 1
        right -= 1

    return result

original = [1, 2, 3, 4, 5]
print(f"Original list: {original}")
print(f"Manual reverse: {reverse_list_manual(original)}")
print(f"Slicing reverse: {reverse_list_slicing(original)}")
print(f"Swap reverse: {reverse_list_swap(original)}")
print(f"Original unchanged: {original}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 4: Merge Two Sorted Lists")
print("="*40)

def merge_sorted_lists(list1, list2):
    merged = []
    i, j = 0, 0

    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            merged.append(list1[i])
            i += 1
        else:
            merged.append(list2[j])
            j += 1

    merged.extend(list1[i:])
    merged.extend(list2[j:])

    return merged

list1 = [1, 3, 5, 7, 9]
list2 = [2, 4, 6, 8, 10]
print(f"List 1: {list1}")
print(f"List 2: {list2}")
print(f"Merged: {merge_sorted_lists(list1, list2)}")

list3 = [1, 4, 7]
list4 = [2, 3, 8, 9]
print(f"\nList 3: {list3}")
print(f"List 4: {list4}")
print(f"Merged: {merge_sorted_lists(list3, list4)}")

print("\n" + "="*40)
print("LIST METHODS DEMONSTRATION")
print("="*40)

demo_list = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"Original: {demo_list}")

print(f"Count of 1: {demo_list.count(1)}")
print(f"Index of 5: {demo_list.index(5)}")

demo_copy = demo_list.copy()
demo_copy.sort()
print(f"Sorted copy: {demo_copy}")
print(f"Original unchanged: {demo_list}")

demo_list.sort(reverse=True)
print(f"Sorted descending (in-place): {demo_list}")

numbers = [1, 2, 3]
more_numbers = [4, 5, 6]
numbers.extend(more_numbers)
print(f"\nExtend [1, 2, 3] with [4, 5, 6]: {numbers}")

print("\n" + "="*40)
print("LIST COMPREHENSIONS PREVIEW")
print("="*40)

squares = [x**2 for x in range(1, 6)]
print(f"Squares of 1-5: {squares}")

evens = [x for x in range(1, 11) if x % 2 == 0]
print(f"Even numbers 1-10: {evens}")

words = ["hello", "world", "python"]
upper_words = [w.upper() for w in words]
print(f"Uppercase words: {upper_words}")

print("\n" + "="*40)
print("NESTED LISTS")
print("="*40)

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print("Matrix:")
for row in matrix:
    print(row)

print(f"\nElement at row 1, col 2: {matrix[1][2]}")

flattened = []
for row in matrix:
    for element in row:
        flattened.append(element)
print(f"Flattened matrix: {flattened}")

print("\n" + "="*40)
print("KEY TAKEAWAYS")
print("="*40)
print("""
1. Lists are mutable and ordered
2. Use indexing and slicing to access elements
3. Many built-in methods for list manipulation
4. Lists can contain mixed data types
5. Negative indexing counts from the end
6. List comprehensions provide concise syntax
""")