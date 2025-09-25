"""
Week 9: Practical Applications
Concepts: Multiple function arguments, Serialization, CSV parsing, Advanced topics
"""

import json
import csv
import pickle
from functools import partial
import inspect
from typing import Any, Dict, List

print("="*60)
print("WEEK 9: PRACTICAL APPLICATIONS - TUTORIAL AND SOLUTIONS")
print("="*60)

print("\n" + "="*40)
print("9.1: MULTIPLE FUNCTION ARGUMENTS")
print("="*40)

print("""
Advanced function signatures:
- *args: Variable positional arguments
- **kwargs: Variable keyword arguments
- Unpacking with * and **
- Flexible function interfaces
""")

print("\nPRACTICE PROBLEM 1: Flexible Configuration System")
print("-" * 40)

class ConfigSystem:
    """Flexible configuration management"""

    def __init__(self, **defaults):
        self.config = defaults

    def update(self, *configs, **overrides):
        """Update configuration from multiple sources"""
        for config in configs:
            if isinstance(config, dict):
                self.config.update(config)

        self.config.update(overrides)

    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)

    def configure_function(self, func):
        """Create configured version of function"""
        def wrapper(*args, **kwargs):
            merged_kwargs = {**self.config, **kwargs}
            return func(*args, **merged_kwargs)
        return wrapper

config = ConfigSystem(debug=False, timeout=30, retries=3)

file_config = {'debug': True, 'log_level': 'INFO'}
cli_config = {'timeout': 60}

config.update(file_config, cli_config, retries=5)

print(f"Final configuration: {config.config}")

@config.configure_function
def api_call(endpoint, **settings):
    return f"Calling {endpoint} with settings: {settings}"

result = api_call("/users", cache=True)
print(f"API call result: {result}")

print("\nPRACTICE PROBLEM 2: Function Chain Executor")
print("-" * 40)

def chain_functions(*functions):
    """Chain multiple functions together"""
    def chained(*args, **kwargs):
        result = args[0] if args else None

        for func in functions:
            if result is not None:
                result = func(result)
            else:
                result = func(**kwargs)

        return result
    return chained

def validate_data(data):
    """Validate data"""
    if not data:
        raise ValueError("Empty data")
    print(f"  Validated: {len(data)} items")
    return data

def transform_data(data):
    """Transform data"""
    transformed = [item.upper() if isinstance(item, str) else item for item in data]
    print(f"  Transformed: {transformed}")
    return transformed

def filter_data(data):
    """Filter data"""
    filtered = [item for item in data if len(str(item)) > 2]
    print(f"  Filtered: {filtered}")
    return filtered

pipeline = chain_functions(validate_data, transform_data, filter_data)
result = pipeline(["a", "hello", "world", "hi"])
print(f"Pipeline result: {result}")

print("\nPRACTICE PROBLEM 3: Command-Line Parser")
print("-" * 40)

class CommandParser:
    """Simple command-line argument parser"""

    def __init__(self):
        self.commands = {}

    def command(self, *names, **options):
        """Decorator to register commands"""
        def decorator(func):
            for name in names:
                self.commands[name] = {
                    'func': func,
                    'options': options
                }
            return func
        return decorator

    def parse_and_execute(self, command_string):
        """Parse and execute command"""
        parts = command_string.split()
        if not parts:
            return "No command provided"

        cmd = parts[0]
        args = []
        kwargs = {}

        i = 1
        while i < len(parts):
            if parts[i].startswith('--'):
                key = parts[i][2:]
                if i + 1 < len(parts) and not parts[i + 1].startswith('--'):
                    kwargs[key] = parts[i + 1]
                    i += 2
                else:
                    kwargs[key] = True
                    i += 1
            else:
                args.append(parts[i])
                i += 1

        if cmd in self.commands:
            return self.commands[cmd]['func'](*args, **kwargs)
        else:
            return f"Unknown command: {cmd}"

parser = CommandParser()

@parser.command('greet', 'hello')
def greet_command(name="World", **kwargs):
    excited = kwargs.get('excited', False)
    greeting = f"Hello, {name}{'!' if excited else '.'}"
    return greeting

@parser.command('calc')
def calc_command(*numbers, operation='add', **kwargs):
    nums = [float(n) for n in numbers]
    if operation == 'add':
        return sum(nums)
    elif operation == 'multiply':
        result = 1
        for n in nums:
            result *= n
        return result
    return "Unknown operation"

commands = [
    "greet Alice",
    "hello --excited",
    "calc 5 3 2 --operation multiply"
]

for cmd in commands:
    print(f"Command: {cmd}")
    print(f"  Result: {parser.parse_and_execute(cmd)}")

print("\nPRACTICE PROBLEM 4: Dynamic API Wrapper")
print("-" * 40)

class APIWrapper:
    """Dynamic API wrapper with flexible arguments"""

    def __init__(self, base_url, **default_headers):
        self.base_url = base_url
        self.default_headers = default_headers

    def __getattr__(self, name):
        """Dynamically create API methods"""
        def method(*path_params, **kwargs):
            endpoint = f"{self.base_url}/{name}"

            if path_params:
                endpoint += "/" + "/".join(str(p) for p in path_params)

            headers = {**self.default_headers, **kwargs.get('headers', {})}

            params = kwargs.get('params', {})
            data = kwargs.get('data', None)

            return {
                'endpoint': endpoint,
                'headers': headers,
                'params': params,
                'data': data
            }
        return method

api = APIWrapper("https://api.example.com", authorization="Bearer token")

print("Dynamic API calls:")
print(f"GET users: {api.users()}")
print(f"GET user 123: {api.users(123)}")
print(f"POST data: {api.posts(data={'title': 'New Post'})}")

print("\n" + "="*40)
print("9.2: SERIALIZATION")
print("="*40)

print("""
Data persistence and serialization:
- JSON: Human-readable, cross-language
- Pickle: Python-specific, handles complex objects
- Custom serialization strategies
""")

print("\nPRACTICE PROBLEM 1: Settings Manager")
print("-" * 40)

class SettingsManager:
    """Manage application settings with persistence"""

    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.settings = self.load()

    def load(self):
        """Load settings from file"""
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save(self):
        """Save settings to file"""
        with open(self.filename, 'w') as f:
            json.dump(self.settings, f, indent=2)

    def get(self, key, default=None):
        """Get setting value"""
        keys = key.split('.')
        value = self.settings

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

        return value if value is not None else default

    def set(self, key, value):
        """Set setting value"""
        keys = key.split('.')
        target = self.settings

        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]

        target[keys[-1]] = value
        self.save()

    def __repr__(self):
        return f"SettingsManager({json.dumps(self.settings, indent=2)})"

settings = SettingsManager("demo_settings.json")
settings.set("app.name", "MyApp")
settings.set("app.version", "1.0.0")
settings.set("database.host", "localhost")
settings.set("database.port", 5432)

print(f"App name: {settings.get('app.name')}")
print(f"DB host: {settings.get('database.host')}")
print(f"All settings: {settings.settings}")

print("\nPRACTICE PROBLEM 2: Game Save System")
print("-" * 40)

class GameSaveSystem:
    """Save and load game state"""

    def __init__(self):
        self.saves = {}

    def save_game(self, slot, game_state):
        """Save game state to slot"""
        serialized = pickle.dumps(game_state)
        self.saves[slot] = {
            'data': serialized,
            'timestamp': json.dumps({'saved': 'now'}),
            'metadata': {
                'level': game_state.get('level', 1),
                'player_name': game_state.get('player_name', 'Unknown')
            }
        }
        print(f"Game saved to slot {slot}")

    def load_game(self, slot):
        """Load game state from slot"""
        if slot not in self.saves:
            return None

        save = self.saves[slot]
        game_state = pickle.loads(save['data'])
        print(f"Game loaded from slot {slot}")
        return game_state

    def list_saves(self):
        """List all save slots"""
        for slot, save in self.saves.items():
            meta = save['metadata']
            print(f"  Slot {slot}: {meta['player_name']} - Level {meta['level']}")

game_state = {
    'player_name': 'Hero',
    'level': 5,
    'inventory': ['sword', 'shield', 'potion'],
    'position': (10, 20),
    'stats': {'health': 100, 'mana': 50}
}

save_system = GameSaveSystem()
save_system.save_game(1, game_state)

game_state['level'] = 6
game_state['inventory'].append('magic_ring')
save_system.save_game(2, game_state)

print("\nAvailable saves:")
save_system.list_saves()

loaded = save_system.load_game(1)
print(f"Loaded game state: Level {loaded['level']}, Inventory: {loaded['inventory']}")

print("\nPRACTICE PROBLEM 3: Cache System")
print("-" * 40)

class CacheSystem:
    """Multi-backend cache system"""

    def __init__(self, backend='memory'):
        self.backend = backend
        self.memory_cache = {}
        self.file_cache_dir = "cache"

    def _get_file_path(self, key):
        """Get file path for key"""
        return f"{self.file_cache_dir}/{key}.cache"

    def set(self, key, value, ttl=None):
        """Set cache value"""
        if self.backend == 'memory':
            self.memory_cache[key] = {
                'value': value,
                'ttl': ttl
            }
        elif self.backend == 'file':
            data = {'value': value, 'ttl': ttl}
            filename = self._get_file_path(key)
            with open(filename, 'wb') as f:
                pickle.dump(data, f)

        print(f"Cached: {key}")

    def get(self, key, default=None):
        """Get cache value"""
        if self.backend == 'memory':
            if key in self.memory_cache:
                return self.memory_cache[key]['value']
        elif self.backend == 'file':
            try:
                filename = self._get_file_path(key)
                with open(filename, 'rb') as f:
                    data = pickle.load(f)
                return data['value']
            except:
                pass

        return default

    def invalidate(self, key):
        """Invalidate cache entry"""
        if self.backend == 'memory':
            self.memory_cache.pop(key, None)
        print(f"Invalidated: {key}")

cache = CacheSystem('memory')
cache.set('user_123', {'name': 'Alice', 'role': 'admin'})
cache.set('product_456', {'name': 'Laptop', 'price': 999})

print(f"User from cache: {cache.get('user_123')}")
print(f"Missing key: {cache.get('nonexistent', 'Not found')}")

print("\n" + "="*40)
print("9.3: PARSING CSV FILES")
print("="*40)

print("\nPRACTICE PROBLEM 1: Grade Book Analyzer")
print("-" * 40)

class GradeBookAnalyzer:
    """Analyze student grades from CSV"""

    def __init__(self):
        self.students = []

    def create_sample_csv(self, filename="grades.csv"):
        """Create sample gradebook CSV"""
        headers = ["Student", "Math", "Science", "English", "History"]
        data = [
            ["Alice", "90", "85", "92", "88"],
            ["Bob", "78", "92", "85", "90"],
            ["Charlie", "95", "88", "78", "85"],
            ["Diana", "82", "95", "90", "92"]
        ]

        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data)

        return filename

    def load_grades(self, filename):
        """Load grades from CSV"""
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            self.students = list(reader)

        for student in self.students:
            for key in student:
                if key != "Student":
                    student[key] = float(student[key])

    def calculate_averages(self):
        """Calculate student averages"""
        for student in self.students:
            grades = [v for k, v in student.items() if k != "Student"]
            student['Average'] = sum(grades) / len(grades)

    def get_top_students(self, n=3):
        """Get top n students by average"""
        self.calculate_averages()
        sorted_students = sorted(self.students, key=lambda x: x['Average'], reverse=True)
        return sorted_students[:n]

    def subject_statistics(self):
        """Calculate statistics per subject"""
        subjects = [k for k in self.students[0].keys() if k != "Student"]
        stats = {}

        for subject in subjects:
            grades = [s[subject] for s in self.students]
            stats[subject] = {
                'mean': sum(grades) / len(grades),
                'min': min(grades),
                'max': max(grades)
            }

        return stats

analyzer = GradeBookAnalyzer()
csv_file = analyzer.create_sample_csv()
analyzer.load_grades(csv_file)

print("Top students:")
for i, student in enumerate(analyzer.get_top_students(), 1):
    print(f"  {i}. {student['Student']}: {student['Average']:.1f}")

stats = analyzer.subject_statistics()
print("\nSubject statistics:")
for subject, stat in stats.items():
    print(f"  {subject}: Mean={stat['mean']:.1f}, Min={stat['min']}, Max={stat['max']}")

print("\nPRACTICE PROBLEM 2: Sales Report Generator")
print("-" * 40)

class SalesReportGenerator:
    """Generate sales reports from CSV data"""

    def process_sales_data(self, data):
        """Process sales data"""
        summary = {}

        for row in data:
            product = row['product']
            quantity = int(row['quantity'])
            price = float(row['price'])
            revenue = quantity * price

            if product not in summary:
                summary[product] = {
                    'total_quantity': 0,
                    'total_revenue': 0,
                    'transactions': 0
                }

            summary[product]['total_quantity'] += quantity
            summary[product]['total_revenue'] += revenue
            summary[product]['transactions'] += 1

        return summary

    def generate_report(self, summary):
        """Generate formatted report"""
        print("\nSales Report")
        print("=" * 60)
        print(f"{'Product':<15} {'Quantity':<10} {'Revenue':<12} {'Avg Sale':<10}")
        print("-" * 60)

        total_revenue = 0
        for product, data in sorted(summary.items()):
            avg_sale = data['total_revenue'] / data['transactions']
            print(f"{product:<15} {data['total_quantity']:<10} "
                  f"${data['total_revenue']:<11.2f} ${avg_sale:<9.2f}")
            total_revenue += data['total_revenue']

        print("-" * 60)
        print(f"{'TOTAL':<15} {'':<10} ${total_revenue:<11.2f}")

sales_data = [
    {'product': 'Widget A', 'quantity': '10', 'price': '15.99'},
    {'product': 'Widget B', 'quantity': '5', 'price': '29.99'},
    {'product': 'Widget A', 'quantity': '7', 'price': '15.99'},
    {'product': 'Widget C', 'quantity': '3', 'price': '45.50'},
    {'product': 'Widget B', 'quantity': '8', 'price': '29.99'}
]

reporter = SalesReportGenerator()
summary = reporter.process_sales_data(sales_data)
reporter.generate_report(summary)

print("\n" + "="*40)
print("9.4: ADVANCED TOPICS REVIEW")
print("="*40)

print("\nClosures:")
print("-" * 40)

def make_multiplier(n):
    """Create multiplier function (closure)"""
    def multiplier(x):
        return x * n
    return multiplier

times_3 = make_multiplier(3)
times_5 = make_multiplier(5)

print(f"times_3(4) = {times_3(4)}")
print(f"times_5(4) = {times_5(4)}")

print("\nPartial Functions:")
print("-" * 40)

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(f"square(5) = {square(5)}")
print(f"cube(3) = {cube(3)}")

print("\nCode Introspection:")
print("-" * 40)

def sample_function(a: int, b: str = "default") -> str:
    """Sample function for introspection"""
    return f"{a}: {b}"

print(f"Function name: {sample_function.__name__}")
print(f"Docstring: {sample_function.__doc__}")
print(f"Signature: {inspect.signature(sample_function)}")
print(f"Annotations: {sample_function.__annotations__}")

print("\nPlugin System:")
print("-" * 40)

class PluginSystem:
    """Simple plugin system"""

    def __init__(self):
        self.plugins = {}

    def register(self, name):
        """Decorator to register plugins"""
        def decorator(plugin_class):
            self.plugins[name] = plugin_class
            return plugin_class
        return decorator

    def get_plugin(self, name):
        """Get plugin by name"""
        return self.plugins.get(name)

    def list_plugins(self):
        """List all plugins"""
        return list(self.plugins.keys())

plugins = PluginSystem()

@plugins.register("logger")
class LoggerPlugin:
    def execute(self):
        return "Logging data..."

@plugins.register("validator")
class ValidatorPlugin:
    def execute(self):
        return "Validating data..."

print(f"Available plugins: {plugins.list_plugins()}")

for name in plugins.list_plugins():
    plugin = plugins.get_plugin(name)()
    print(f"  {name}: {plugin.execute()}")

import os
if os.path.exists("demo_settings.json"):
    os.remove("demo_settings.json")
if os.path.exists("grades.csv"):
    os.remove("grades.csv")

print("\n" + "="*40)
print("KEY TAKEAWAYS")
print("="*40)
print("""
1. *args and **kwargs enable flexible functions
2. JSON for human-readable serialization
3. Pickle for Python-specific object serialization
4. CSV for tabular data exchange
5. Closures capture surrounding scope
6. Partial functions for specialized versions
7. Introspection for runtime code analysis
8. Plugin systems for extensible architectures
""")