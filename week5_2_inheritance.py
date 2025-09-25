"""
Week 5.2: Inheritance and Polymorphism
Concepts: Inheritance, method overriding, super()
"""

from abc import ABC, abstractmethod
import math

print("="*60)
print("WEEK 5.2: INHERITANCE AND POLYMORPHISM - TUTORIAL AND SOLUTIONS")
print("="*60)

print("\n" + "="*40)
print("TUTORIAL: Advanced OOP Concepts")
print("="*40)

print("""
Inheritance allows creating new classes from existing ones:
- Parent/Base class: The class being inherited from
- Child/Derived class: The class that inherits
- super(): Access parent class methods
- Override: Redefine parent methods in child

Polymorphism: Same interface, different implementations
- Method overriding
- Abstract classes
- Duck typing in Python
""")

print("\n" + "="*40)
print("PRACTICE PROBLEM 1: Animal Hierarchy")
print("="*40)

class Animal:
    """Base Animal class"""

    def __init__(self, name, species, age):
        self.name = name
        self.species = species
        self.age = age
        self.is_alive = True
        self.energy = 100

    def make_sound(self):
        """Generic animal sound"""
        return "Some generic animal sound"

    def eat(self, food):
        """Eat food to gain energy"""
        self.energy = min(100, self.energy + 20)
        return f"{self.name} ate {food}. Energy: {self.energy}"

    def sleep(self):
        """Sleep to restore energy"""
        self.energy = 100
        return f"{self.name} is sleeping... Energy restored!"

    def info(self):
        """Display animal information"""
        return f"{self.name} ({self.species}), Age: {self.age}, Energy: {self.energy}"

class Dog(Animal):
    """Dog class inheriting from Animal"""

    def __init__(self, name, age, breed):
        super().__init__(name, "Canine", age)
        self.breed = breed
        self.tricks = []

    def make_sound(self):
        """Override parent method"""
        return "Woof! Woof!"

    def learn_trick(self, trick):
        """Dog-specific method"""
        self.tricks.append(trick)
        return f"{self.name} learned {trick}!"

    def perform_tricks(self):
        """Show all learned tricks"""
        if not self.tricks:
            return f"{self.name} doesn't know any tricks yet"
        return f"{self.name} can: " + ", ".join(self.tricks)

    def fetch(self):
        """Play fetch"""
        self.energy -= 10
        return f"{self.name} fetched the ball! Energy: {self.energy}"

class Cat(Animal):
    """Cat class inheriting from Animal"""

    def __init__(self, name, age, indoor=True):
        super().__init__(name, "Feline", age)
        self.indoor = indoor
        self.mood = "neutral"

    def make_sound(self):
        """Override parent method"""
        return "Meow!"

    def purr(self):
        """Cat-specific method"""
        self.mood = "happy"
        return f"{self.name} is purring... Mood: {self.mood}"

    def scratch(self):
        """Cat scratching behavior"""
        self.mood = "playful"
        return f"{self.name} is scratching. Mood: {self.mood}"

    def hunt(self):
        """Hunting behavior"""
        if self.indoor:
            return f"{self.name} is hunting toys indoors"
        else:
            self.energy -= 20
            return f"{self.name} is hunting outside. Energy: {self.energy}"

class Bird(Animal):
    """Bird class inheriting from Animal"""

    def __init__(self, name, age, can_fly=True):
        super().__init__(name, "Avian", age)
        self.can_fly = can_fly
        self.altitude = 0

    def make_sound(self):
        """Override parent method"""
        return "Tweet tweet!"

    def fly(self, height):
        """Bird flying behavior"""
        if not self.can_fly:
            return f"{self.name} cannot fly"

        self.altitude = height
        self.energy -= 15
        return f"{self.name} is flying at {height}m. Energy: {self.energy}"

    def land(self):
        """Land from flight"""
        if self.altitude == 0:
            return f"{self.name} is already on the ground"

        self.altitude = 0
        return f"{self.name} has landed"

    def sing(self):
        """Bird singing"""
        return f"{self.name} is singing a beautiful melody"

dog = Dog("Buddy", 3, "Golden Retriever")
cat = Cat("Whiskers", 2, indoor=True)
bird = Bird("Tweety", 1, can_fly=True)

animals = [dog, cat, bird]

print("Animal sounds (Polymorphism):")
for animal in animals:
    print(f"  {animal.name}: {animal.make_sound()}")

print(f"\n{dog.learn_trick('sit')}")
print(f"{dog.learn_trick('roll over')}")
print(dog.perform_tricks())

print(f"\n{cat.purr()}")
print(cat.hunt())

print(f"\n{bird.fly(50)}")
print(bird.sing())

print("\n" + "="*40)
print("PRACTICE PROBLEM 2: Shape Classes")
print("="*40)

class Shape(ABC):
    """Abstract base class for shapes"""

    def __init__(self, color="black"):
        self.color = color

    @abstractmethod
    def area(self):
        """Calculate area - must be implemented by subclasses"""
        pass

    @abstractmethod
    def perimeter(self):
        """Calculate perimeter - must be implemented by subclasses"""
        pass

    def describe(self):
        """Describe the shape"""
        return f"{self.color} {self.__class__.__name__}"

class Circle(Shape):
    """Circle shape"""

    def __init__(self, radius, color="black"):
        super().__init__(color)
        self.radius = radius

    def area(self):
        """Calculate circle area"""
        return math.pi * self.radius ** 2

    def perimeter(self):
        """Calculate circle circumference"""
        return 2 * math.pi * self.radius

    def diameter(self):
        """Get circle diameter"""
        return 2 * self.radius

    def __str__(self):
        return f"Circle(r={self.radius}, color={self.color})"

class Rectangle(Shape):
    """Rectangle shape"""

    def __init__(self, width, height, color="black"):
        super().__init__(color)
        self.width = width
        self.height = height

    def area(self):
        """Calculate rectangle area"""
        return self.width * self.height

    def perimeter(self):
        """Calculate rectangle perimeter"""
        return 2 * (self.width + self.height)

    def is_square(self):
        """Check if rectangle is a square"""
        return self.width == self.height

    def diagonal(self):
        """Calculate diagonal length"""
        return math.sqrt(self.width ** 2 + self.height ** 2)

    def __str__(self):
        shape_type = "Square" if self.is_square() else "Rectangle"
        return f"{shape_type}(w={self.width}, h={self.height}, color={self.color})"

class Triangle(Shape):
    """Triangle shape"""

    def __init__(self, a, b, c, color="black"):
        super().__init__(color)
        self.a = a
        self.b = b
        self.c = c

        if not self._is_valid():
            raise ValueError("Invalid triangle sides")

    def _is_valid(self):
        """Check if sides form a valid triangle"""
        return (self.a + self.b > self.c and
                self.a + self.c > self.b and
                self.b + self.c > self.a)

    def area(self):
        """Calculate triangle area using Heron's formula"""
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self):
        """Calculate triangle perimeter"""
        return self.a + self.b + self.c

    def type(self):
        """Determine triangle type"""
        if self.a == self.b == self.c:
            return "Equilateral"
        elif self.a == self.b or self.b == self.c or self.a == self.c:
            return "Isosceles"
        else:
            return "Scalene"

    def __str__(self):
        return f"Triangle({self.a}, {self.b}, {self.c}, color={self.color})"

shapes = [
    Circle(5, "red"),
    Rectangle(4, 6, "blue"),
    Rectangle(5, 5, "green"),
    Triangle(3, 4, 5, "yellow")
]

print("Shape calculations:")
for shape in shapes:
    print(f"\n{shape}")
    print(f"  Description: {shape.describe()}")
    print(f"  Area: {shape.area():.2f}")
    print(f"  Perimeter: {shape.perimeter():.2f}")

    if isinstance(shape, Circle):
        print(f"  Diameter: {shape.diameter():.2f}")
    elif isinstance(shape, Rectangle):
        print(f"  Is square: {shape.is_square()}")
        print(f"  Diagonal: {shape.diagonal():.2f}")
    elif isinstance(shape, Triangle):
        print(f"  Type: {shape.type()}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 3: Employee Management System")
print("="*40)

class Employee:
    """Base Employee class"""

    employee_count = 0

    def __init__(self, name, employee_id, department, base_salary):
        Employee.employee_count += 1
        self.name = name
        self.employee_id = employee_id
        self.department = department
        self.base_salary = base_salary
        self.performance_rating = 3

    def calculate_salary(self):
        """Calculate monthly salary"""
        return self.base_salary

    def annual_review(self, rating):
        """Set performance rating"""
        if 1 <= rating <= 5:
            self.performance_rating = rating
            return f"{self.name}'s rating updated to {rating}"
        return "Invalid rating (use 1-5)"

    def get_info(self):
        """Get employee information"""
        return {
            'Name': self.name,
            'ID': self.employee_id,
            'Department': self.department,
            'Base Salary': self.base_salary,
            'Performance': self.performance_rating
        }

class Manager(Employee):
    """Manager class with team management"""

    def __init__(self, name, employee_id, department, base_salary, team_size=0):
        super().__init__(name, employee_id, department, base_salary)
        self.team_size = team_size
        self.team_members = []

    def calculate_salary(self):
        """Manager salary includes team bonus"""
        team_bonus = self.team_size * 500
        performance_bonus = self.base_salary * (self.performance_rating - 3) * 0.1
        return self.base_salary + team_bonus + performance_bonus

    def add_team_member(self, employee):
        """Add employee to team"""
        self.team_members.append(employee)
        self.team_size = len(self.team_members)
        return f"{employee.name} added to {self.name}'s team"

    def team_report(self):
        """Generate team report"""
        if not self.team_members:
            return f"{self.name} has no team members"

        report = f"{self.name}'s Team:\n"
        for member in self.team_members:
            report += f"  - {member.name} ({member.department})\n"
        return report

class Developer(Employee):
    """Developer class with technical skills"""

    def __init__(self, name, employee_id, base_salary, languages=None):
        super().__init__(name, employee_id, "Engineering", base_salary)
        self.languages = languages if languages else []
        self.projects_completed = 0

    def calculate_salary(self):
        """Developer salary includes skill bonus"""
        skill_bonus = len(self.languages) * 300
        project_bonus = self.projects_completed * 200
        performance_bonus = self.base_salary * (self.performance_rating - 3) * 0.15
        return self.base_salary + skill_bonus + project_bonus + performance_bonus

    def learn_language(self, language):
        """Add new programming language"""
        if language not in self.languages:
            self.languages.append(language)
            return f"{self.name} learned {language}"
        return f"{self.name} already knows {language}"

    def complete_project(self):
        """Mark project as completed"""
        self.projects_completed += 1
        return f"{self.name} completed project #{self.projects_completed}"

class SalesPerson(Employee):
    """Sales person with commission"""

    def __init__(self, name, employee_id, base_salary, commission_rate=0.05):
        super().__init__(name, employee_id, "Sales", base_salary)
        self.commission_rate = commission_rate
        self.monthly_sales = 0

    def calculate_salary(self):
        """Sales salary includes commission"""
        commission = self.monthly_sales * self.commission_rate
        performance_bonus = self.base_salary * (self.performance_rating - 3) * 0.2
        return self.base_salary + commission + performance_bonus

    def record_sale(self, amount):
        """Record a sale"""
        self.monthly_sales += amount
        return f"{self.name} recorded sale of ${amount:.2f}"

    def reset_monthly_sales(self):
        """Reset sales for new month"""
        total = self.monthly_sales
        self.monthly_sales = 0
        return f"Monthly sales reset. Last month: ${total:.2f}"

manager = Manager("Alice Johnson", "M001", "Operations", 80000)
dev1 = Developer("Bob Smith", "D001", 70000, ["Python", "JavaScript"])
dev2 = Developer("Charlie Brown", "D002", 65000, ["Java"])
sales = SalesPerson("Diana Prince", "S001", 50000, 0.08)

manager.add_team_member(dev1)
manager.add_team_member(dev2)
manager.add_team_member(sales)

dev1.learn_language("React")
dev1.complete_project()
dev1.complete_project()

sales.record_sale(50000)
sales.record_sale(30000)

employees = [manager, dev1, dev2, sales]

print("Employee Salary Report:")
print("-" * 50)
for emp in employees:
    info = emp.get_info()
    salary = emp.calculate_salary()
    print(f"{info['Name']} ({info['ID']})")
    print(f"  Department: {info['Department']}")
    print(f"  Monthly Salary: ${salary:,.2f}")

    if isinstance(emp, Manager):
        print(f"  Team Size: {emp.team_size}")
    elif isinstance(emp, Developer):
        print(f"  Languages: {', '.join(emp.languages)}")
        print(f"  Projects: {emp.projects_completed}")
    elif isinstance(emp, SalesPerson):
        print(f"  Monthly Sales: ${emp.monthly_sales:,.2f}")

print(f"\n{manager.team_report()}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 4: Game Character System")
print("="*40)

class Character:
    """Base character class for game"""

    def __init__(self, name, health=100, level=1):
        self.name = name
        self.health = health
        self.max_health = health
        self.level = level
        self.experience = 0
        self.is_alive = True

    def take_damage(self, damage):
        """Take damage"""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            return f"{self.name} has been defeated!"
        return f"{self.name} took {damage} damage. HP: {self.health}/{self.max_health}"

    def heal(self, amount):
        """Heal character"""
        if not self.is_alive:
            return f"{self.name} is defeated and cannot heal"

        self.health = min(self.max_health, self.health + amount)
        return f"{self.name} healed for {amount}. HP: {self.health}/{self.max_health}"

    def gain_experience(self, exp):
        """Gain experience points"""
        self.experience += exp
        if self.experience >= self.level * 100:
            self.level_up()
        return f"{self.name} gained {exp} XP"

    def level_up(self):
        """Level up character"""
        self.level += 1
        self.max_health += 10
        self.health = self.max_health
        self.experience = 0
        return f"{self.name} leveled up to {self.level}!"

    def attack(self):
        """Basic attack"""
        return self.level * 5

class Warrior(Character):
    """Warrior class - high health, melee combat"""

    def __init__(self, name):
        super().__init__(name, health=150, level=1)
        self.strength = 10
        self.armor = 5

    def attack(self):
        """Warrior attack based on strength"""
        return self.strength * 2 + self.level * 3

    def shield_bash(self):
        """Special warrior ability"""
        return f"{self.name} uses Shield Bash! Damage: {self.strength}"

    def battle_cry(self):
        """Boost strength temporarily"""
        self.strength += 2
        return f"{self.name} uses Battle Cry! Strength increased to {self.strength}"

class Mage(Character):
    """Mage class - low health, magic attacks"""

    def __init__(self, name):
        super().__init__(name, health=70, level=1)
        self.mana = 100
        self.max_mana = 100
        self.spell_power = 15

    def attack(self):
        """Magic attack"""
        if self.mana >= 10:
            self.mana -= 10
            return self.spell_power * 2 + self.level * 5
        return 5

    def fireball(self):
        """Cast fireball spell"""
        if self.mana >= 20:
            self.mana -= 20
            damage = self.spell_power * 3
            return f"{self.name} casts Fireball! Damage: {damage}"
        return f"{self.name} doesn't have enough mana"

    def restore_mana(self):
        """Restore mana"""
        self.mana = self.max_mana
        return f"{self.name} restored mana. MP: {self.mana}/{self.max_mana}"

class Rogue(Character):
    """Rogue class - moderate health, high damage"""

    def __init__(self, name):
        super().__init__(name, health=90, level=1)
        self.agility = 12
        self.stealth = False

    def attack(self):
        """Rogue attack with possible critical"""
        import random
        base_damage = self.agility * 1.5 + self.level * 4

        if random.random() < 0.3:
            return base_damage * 2
        return base_damage

    def enter_stealth(self):
        """Enter stealth mode"""
        self.stealth = True
        return f"{self.name} vanished into shadows"

    def backstab(self):
        """Backstab from stealth"""
        if self.stealth:
            self.stealth = False
            damage = self.agility * 4
            return f"{self.name} uses Backstab from stealth! Damage: {damage}"
        return f"{self.name} must be in stealth to backstab"

warrior = Warrior("Thorin")
mage = Mage("Gandalf")
rogue = Rogue("Shadow")

print("Game Characters:")
characters = [warrior, mage, rogue]

for char in characters:
    print(f"\n{char.name} (Level {char.level} {char.__class__.__name__})")
    print(f"  HP: {char.health}/{char.max_health}")
    print(f"  Attack Power: {char.attack()}")

print(f"\n{warrior.battle_cry()}")
print(f"{mage.fireball()}")
print(f"{rogue.enter_stealth()}")
print(f"{rogue.backstab()}")

print("\nCombat Simulation:")
print(mage.take_damage(warrior.attack()))
print(mage.heal(30))
print(warrior.gain_experience(150))

print("\n" + "="*40)
print("KEY TAKEAWAYS")
print("="*40)
print("""
1. Inheritance creates "is-a" relationships
2. Child classes inherit parent attributes and methods
3. Override methods to customize behavior
4. super() accesses parent class functionality
5. Abstract classes define interfaces
6. isinstance() checks object type
7. Polymorphism enables flexible code design
""")