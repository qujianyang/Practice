"""
Week 6.3: Sets
Concepts: Set operations, uniqueness
"""

print("="*60)
print("WEEK 6.3: SETS - TUTORIAL AND SOLUTIONS")
print("="*60)

print("\n" + "="*40)
print("TUTORIAL: Working with Sets")
print("="*40)

print("""
Sets are unordered collections of unique elements:
- Created with {} or set()
- No duplicate values
- Unordered (no indexing)
- Mutable (can add/remove)
- frozenset for immutable sets

Set operations:
- Union (|): All elements from both sets
- Intersection (&): Common elements
- Difference (-): Elements in first but not second
- Symmetric difference (^): Elements in either but not both
""")

print("\n" + "="*40)
print("BASIC SET OPERATIONS")
print("="*40)

set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}

print(f"Set 1: {set1}")
print(f"Set 2: {set2}")

print(f"\nUnion (set1 | set2): {set1 | set2}")
print(f"Intersection (set1 & set2): {set1 & set2}")
print(f"Difference (set1 - set2): {set1 - set2}")
print(f"Difference (set2 - set1): {set2 - set1}")
print(f"Symmetric difference (set1 ^ set2): {set1 ^ set2}")

print("\nSet methods:")
set3 = {1, 2, 3}
set3.add(4)
print(f"After add(4): {set3}")

set3.discard(2)
print(f"After discard(2): {set3}")

set3.update([5, 6, 7])
print(f"After update([5, 6, 7]): {set3}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 1: Find Common Elements")
print("="*40)

def find_common_elements(*lists):
    """Find common elements between multiple lists"""
    if not lists:
        return set()

    sets = [set(lst) for lst in lists]

    common = sets[0]
    for s in sets[1:]:
        common = common.intersection(s)

    return common

def find_unique_elements(*lists):
    """Find elements unique to each list"""
    if not lists:
        return []

    all_sets = [set(lst) for lst in lists]
    unique_per_list = []

    for i, current_set in enumerate(all_sets):
        other_sets = all_sets[:i] + all_sets[i+1:]

        union_of_others = set()
        for other in other_sets:
            union_of_others = union_of_others.union(other)

        unique = current_set - union_of_others
        unique_per_list.append(unique)

    return unique_per_list

def analyze_list_overlap(list1, list2):
    """Analyze overlap between two lists"""
    set1 = set(list1)
    set2 = set(list2)

    return {
        'list1_size': len(list1),
        'list2_size': len(list2),
        'unique_in_list1': len(set1),
        'unique_in_list2': len(set2),
        'common': set1 & set2,
        'only_in_list1': set1 - set2,
        'only_in_list2': set2 - set1,
        'all_unique': set1 | set2,
        'jaccard_similarity': len(set1 & set2) / len(set1 | set2) if set1 | set2 else 0
    }

list1 = [1, 2, 3, 4, 5, 5]
list2 = [4, 5, 6, 7, 8]
list3 = [5, 6, 9, 10]

print("Finding common elements:")
print(f"Lists: {list1}, {list2}, {list3}")
common = find_common_elements(list1, list2, list3)
print(f"Common elements: {common}")

unique = find_unique_elements(list1, list2, list3)
print(f"\nUnique elements per list:")
for i, u in enumerate(unique, 1):
    print(f"  List {i}: {u}")

analysis = analyze_list_overlap(list1, list2)
print(f"\nOverlap analysis between list1 and list2:")
for key, value in analysis.items():
    if isinstance(value, float):
        print(f"  {key}: {value:.3f}")
    else:
        print(f"  {key}: {value}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 2: Remove Duplicates")
print("="*40)

def remove_duplicates_preserve_order(lst):
    """Remove duplicates while preserving order"""
    seen = set()
    result = []

    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result

def remove_duplicates_multiple_lists(*lists):
    """Remove duplicates across multiple lists"""
    all_unique = set()
    for lst in lists:
        all_unique.update(lst)

    return list(all_unique)

def find_duplicate_items(lst):
    """Find which items are duplicated"""
    seen = set()
    duplicates = set()

    for item in lst:
        if item in seen:
            duplicates.add(item)
        seen.add(item)

    return duplicates

def count_duplicates(lst):
    """Count occurrences of each duplicate"""
    from collections import Counter
    counts = Counter(lst)
    return {item: count for item, count in counts.items() if count > 1}

test_list = [1, 2, 3, 2, 4, 3, 5, 1, 6, 4, 7]
print(f"Original list: {test_list}")
print(f"Without duplicates (order preserved): {remove_duplicates_preserve_order(test_list)}")
print(f"Without duplicates (set): {list(set(test_list))}")
print(f"Duplicate items: {find_duplicate_items(test_list)}")
print(f"Duplicate counts: {count_duplicates(test_list)}")

lists = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
print(f"\nMultiple lists: {lists}")
print(f"All unique elements: {remove_duplicates_multiple_lists(*lists)}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 3: Recommendation System")
print("="*40)

class RecommendationSystem:
    """Simple recommendation system using sets"""

    def __init__(self):
        self.user_preferences = {}
        self.item_categories = {}

    def add_user_preference(self, user, items):
        """Add user preferences"""
        if user not in self.user_preferences:
            self.user_preferences[user] = set()
        self.user_preferences[user].update(items)

    def add_item_category(self, item, categories):
        """Add item to categories"""
        if item not in self.item_categories:
            self.item_categories[item] = set()
        self.item_categories[item].update(categories)

    def find_similar_users(self, user):
        """Find users with similar preferences"""
        if user not in self.user_preferences:
            return []

        user_prefs = self.user_preferences[user]
        similarities = []

        for other_user, other_prefs in self.user_preferences.items():
            if other_user != user:
                common = len(user_prefs & other_prefs)
                total = len(user_prefs | other_prefs)
                similarity = common / total if total > 0 else 0

                similarities.append((other_user, similarity, common))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities

    def recommend_items(self, user, exclude_owned=True):
        """Recommend items based on similar users"""
        if user not in self.user_preferences:
            return []

        user_items = self.user_preferences[user]
        recommendations = set()

        similar_users = self.find_similar_users(user)

        for similar_user, similarity, _ in similar_users[:3]:
            other_items = self.user_preferences[similar_user]
            new_items = other_items - user_items if exclude_owned else other_items
            recommendations.update(new_items)

        return list(recommendations)

    def recommend_by_category(self, user):
        """Recommend items based on category preferences"""
        if user not in self.user_preferences:
            return []

        user_items = self.user_preferences[user]
        user_categories = set()

        for item in user_items:
            if item in self.item_categories:
                user_categories.update(self.item_categories[item])

        recommendations = set()
        for item, categories in self.item_categories.items():
            if item not in user_items:
                if categories & user_categories:
                    recommendations.add(item)

        return list(recommendations)

recommender = RecommendationSystem()

recommender.add_user_preference("Alice", ["Book1", "Book2", "Movie1"])
recommender.add_user_preference("Bob", ["Book2", "Book3", "Movie1", "Movie2"])
recommender.add_user_preference("Charlie", ["Book1", "Book3", "Movie3"])
recommender.add_user_preference("Diana", ["Book2", "Movie1", "Movie3"])

recommender.add_item_category("Book1", ["Fiction", "Adventure"])
recommender.add_item_category("Book2", ["Fiction", "Mystery"])
recommender.add_item_category("Book3", ["Non-fiction", "Science"])
recommender.add_item_category("Movie1", ["Action", "Adventure"])
recommender.add_item_category("Movie2", ["Comedy"])
recommender.add_item_category("Movie3", ["Drama", "Mystery"])

print("Recommendation System:")
for user in ["Alice", "Bob"]:
    print(f"\n{user}:")
    print(f"  Current preferences: {recommender.user_preferences[user]}")

    similar = recommender.find_similar_users(user)
    if similar:
        best_match = similar[0]
        print(f"  Most similar user: {best_match[0]} (similarity: {best_match[1]:.2f})")

    recommendations = recommender.recommend_items(user)
    print(f"  Recommended items: {recommendations}")

    category_recs = recommender.recommend_by_category(user)
    print(f"  Category-based recommendations: {category_recs}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 4: Venn Diagram Calculator")
print("="*40)

class VennDiagramCalculator:
    """Calculate Venn diagram regions for sets"""

    def __init__(self, set_a, set_b, set_c=None):
        self.set_a = set(set_a)
        self.set_b = set(set_b)
        self.set_c = set(set_c) if set_c else None

    def two_set_venn(self):
        """Calculate regions for two-set Venn diagram"""
        only_a = self.set_a - self.set_b
        only_b = self.set_b - self.set_a
        both = self.set_a & self.set_b

        return {
            'only_A': only_a,
            'only_B': only_b,
            'A_and_B': both,
            'total_unique': len(self.set_a | self.set_b)
        }

    def three_set_venn(self):
        """Calculate regions for three-set Venn diagram"""
        if not self.set_c:
            return None

        only_a = self.set_a - self.set_b - self.set_c
        only_b = self.set_b - self.set_a - self.set_c
        only_c = self.set_c - self.set_a - self.set_b

        a_and_b = (self.set_a & self.set_b) - self.set_c
        a_and_c = (self.set_a & self.set_c) - self.set_b
        b_and_c = (self.set_b & self.set_c) - self.set_a

        all_three = self.set_a & self.set_b & self.set_c

        return {
            'only_A': only_a,
            'only_B': only_b,
            'only_C': only_c,
            'A_and_B_only': a_and_b,
            'A_and_C_only': a_and_c,
            'B_and_C_only': b_and_c,
            'A_and_B_and_C': all_three,
            'total_unique': len(self.set_a | self.set_b | self.set_c)
        }

    def visualize_two_sets(self):
        """Create text visualization of two sets"""
        regions = self.two_set_venn()

        print("\nTwo-Set Venn Diagram:")
        print("     Set A              Set B")
        print(f"  [{len(regions['only_A'])}]    [{len(regions['A_and_B'])}]    [{len(regions['only_B'])}]")
        print(f"\nOnly A: {regions['only_A']}")
        print(f"A ∩ B: {regions['A_and_B']}")
        print(f"Only B: {regions['only_B']}")

students_math = {"Alice", "Bob", "Charlie", "Diana", "Eve"}
students_science = {"Bob", "Charlie", "Frank", "Grace"}
students_english = {"Alice", "Charlie", "Diana", "Frank", "Helen"}

venn2 = VennDiagramCalculator(students_math, students_science)
print("Students in Math and Science classes:")
results2 = venn2.two_set_venn()
venn2.visualize_two_sets()

venn3 = VennDiagramCalculator(students_math, students_science, students_english)
print("\nStudents in Math, Science, and English classes:")
results3 = venn3.three_set_venn()
for region, students in results3.items():
    if isinstance(students, set):
        print(f"  {region}: {students if students else '∅'}")
    else:
        print(f"  {region}: {students}")

print("\n" + "="*40)
print("ADVANCED SET OPERATIONS")
print("="*40)

def powerset(s):
    """Generate power set of a set"""
    s = list(s)
    power = [[]]

    for elem in s:
        power.extend([subset + [elem] for subset in power])

    return [set(subset) for subset in power]

def is_subset_sum(numbers, target):
    """Check if any subset sums to target"""
    for subset in powerset(numbers):
        if sum(subset) == target:
            return True, subset
    return False, None

def set_partition(s, n):
    """Check if set can be partitioned into n equal sum subsets"""
    total = sum(s)
    if total % n != 0:
        return False

    target = total // n
    return target

sample_set = {1, 2, 3}
print(f"Set: {sample_set}")
print(f"Power set: {powerset(sample_set)}")

numbers = {1, 3, 5, 7, 9}
target = 12
exists, subset = is_subset_sum(numbers, target)
print(f"\nNumbers: {numbers}")
print(f"Subset that sums to {target}: {subset if exists else 'None'}")

print("\n" + "="*40)
print("FROZENSETS")
print("="*40)

frozen1 = frozenset([1, 2, 3])
frozen2 = frozenset([2, 3, 4])

print(f"Frozenset 1: {frozen1}")
print(f"Frozenset 2: {frozen2}")
print(f"Union: {frozen1 | frozen2}")
print(f"Intersection: {frozen1 & frozen2}")

set_of_sets = {frozen1, frozen2, frozenset([3, 4, 5])}
print(f"\nSet of frozensets: {set_of_sets}")

print("\n" + "="*40)
print("KEY TAKEAWAYS")
print("="*40)
print("""
1. Sets store unique elements only
2. Sets are unordered (no indexing)
3. Set operations are fast for membership testing
4. Use frozenset for immutable sets
5. Sets are great for removing duplicates
6. Set operations simplify complex comparisons
7. Sets can't contain mutable elements (lists, dicts)
""")