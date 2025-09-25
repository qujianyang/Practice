"""
Week 6.1: File Input and Output
Concepts: File operations, read/write modes
"""

import os
import json
import csv
from datetime import datetime

print("="*60)
print("WEEK 6.1: FILE INPUT AND OUTPUT - TUTORIAL AND SOLUTIONS")
print("="*60)

print("\n" + "="*40)
print("TUTORIAL: Working with Files")
print("="*40)

print("""
File operations in Python:
- open(): Open a file
- read(): Read entire file
- readline(): Read one line
- readlines(): Read all lines into list
- write(): Write to file
- close(): Close file (or use 'with' statement)

File modes:
- 'r': Read (default)
- 'w': Write (overwrites)
- 'a': Append
- 'x': Exclusive create
- 'b': Binary mode
- '+': Read and write
""")

print("\n" + "="*40)
print("PRACTICE PROBLEM 1: Note-Taking Application")
print("="*40)

class NoteApp:
    """Simple note-taking application"""

    def __init__(self, filename="notes.txt"):
        self.filename = filename
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Create file if it doesn't exist"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                f.write("=== Notes ===\n")
            print(f"Created new notes file: {self.filename}")

    def add_note(self, note, category="General"):
        """Add a new note"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.filename, 'a') as f:
            f.write(f"\n[{timestamp}] [{category}]\n")
            f.write(f"{note}\n")
            f.write("-" * 40 + "\n")

        print(f"Note added to {self.filename}")

    def read_notes(self):
        """Read all notes"""
        with open(self.filename, 'r') as f:
            content = f.read()
        return content

    def search_notes(self, keyword):
        """Search notes for keyword"""
        results = []
        with open(self.filename, 'r') as f:
            lines = f.readlines()

        current_note = []
        for line in lines:
            if line.startswith('[') and current_note:
                note_text = ''.join(current_note)
                if keyword.lower() in note_text.lower():
                    results.append(note_text)
                current_note = [line]
            else:
                current_note.append(line)

        if current_note:
            note_text = ''.join(current_note)
            if keyword.lower() in note_text.lower():
                results.append(note_text)

        return results

    def get_stats(self):
        """Get statistics about notes"""
        with open(self.filename, 'r') as f:
            lines = f.readlines()

        note_count = sum(1 for line in lines if line.startswith('['))
        word_count = sum(len(line.split()) for line in lines)

        return {
            'notes': note_count - 1,  # Subtract header
            'lines': len(lines),
            'words': word_count,
            'file_size': os.path.getsize(self.filename)
        }

    def backup_notes(self):
        """Create a backup of notes"""
        backup_name = f"notes_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        with open(self.filename, 'r') as source:
            with open(backup_name, 'w') as backup:
                backup.write(source.read())

        print(f"Backup created: {backup_name}")
        return backup_name

app = NoteApp("demo_notes.txt")

app.add_note("Remember to study Python file I/O operations", "Study")
app.add_note("Meeting with team at 3 PM tomorrow", "Work")
app.add_note("Buy groceries: milk, bread, eggs", "Personal")

print("\nAll Notes:")
print(app.read_notes())

search_term = "Python"
results = app.search_notes(search_term)
print(f"\nSearch results for '{search_term}':")
for result in results:
    print(result)

stats = app.get_stats()
print(f"\nNote Statistics:")
for key, value in stats.items():
    print(f"  {key}: {value}")

print("\n" + "="*40)
print("PRACTICE PROBLEM 2: CSV Data Analyzer")
print("="*40)

class CSVAnalyzer:
    """Analyze CSV data files"""

    def __init__(self):
        self.data = []
        self.headers = []

    def create_sample_csv(self, filename="sample_data.csv"):
        """Create a sample CSV file"""
        headers = ["Name", "Age", "Department", "Salary"]
        data = [
            ["Alice Johnson", "28", "Engineering", "75000"],
            ["Bob Smith", "35", "Marketing", "65000"],
            ["Charlie Brown", "42", "Sales", "80000"],
            ["Diana Prince", "31", "Engineering", "78000"],
            ["Eve Wilson", "29", "HR", "60000"]
        ]

        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data)

        print(f"Created sample CSV: {filename}")
        return filename

    def load_csv(self, filename):
        """Load CSV file"""
        self.data = []

        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            self.headers = reader.fieldnames
            for row in reader:
                self.data.append(row)

        print(f"Loaded {len(self.data)} records from {filename}")

    def analyze_numeric_column(self, column):
        """Analyze a numeric column"""
        values = []
        for row in self.data:
            try:
                values.append(float(row[column]))
            except (ValueError, KeyError):
                continue

        if not values:
            return None

        return {
            'count': len(values),
            'sum': sum(values),
            'average': sum(values) / len(values),
            'min': min(values),
            'max': max(values)
        }

    def filter_data(self, column, condition):
        """Filter data based on condition"""
        filtered = []

        for row in self.data:
            if column in row:
                value = row[column]

                try:
                    value = float(value)
                    if eval(f"{value} {condition}"):
                        filtered.append(row)
                except:
                    if eval(f"'{value}' {condition}"):
                        filtered.append(row)

        return filtered

    def group_by(self, column):
        """Group data by column value"""
        groups = {}

        for row in self.data:
            if column in row:
                key = row[column]
                if key not in groups:
                    groups[key] = []
                groups[key].append(row)

        return groups

    def export_to_json(self, filename="output.json"):
        """Export data to JSON"""
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=2)

        print(f"Exported data to {filename}")

    def generate_report(self):
        """Generate analysis report"""
        print("\nData Analysis Report")
        print("=" * 40)
        print(f"Total Records: {len(self.data)}")
        print(f"Columns: {', '.join(self.headers)}")

        for column in self.headers:
            analysis = self.analyze_numeric_column(column)
            if analysis:
                print(f"\n{column} Statistics:")
                for key, value in analysis.items():
                    print(f"  {key}: {value:.2f}" if isinstance(value, float) else f"  {key}: {value}")

analyzer = CSVAnalyzer()

csv_file = analyzer.create_sample_csv()
analyzer.load_csv(csv_file)

analyzer.generate_report()

high_earners = analyzer.filter_data("Salary", "> 70000")
print(f"\nHigh earners (Salary > 70000): {len(high_earners)}")
for person in high_earners:
    print(f"  {person['Name']}: ${person['Salary']}")

departments = analyzer.group_by("Department")
print(f"\nEmployees by Department:")
for dept, employees in departments.items():
    print(f"  {dept}: {len(employees)} employees")

print("\n" + "="*40)
print("PRACTICE PROBLEM 3: Log File Parser")
print("="*40)

class LogParser:
    """Parse and analyze log files"""

    def __init__(self):
        self.entries = []

    def create_sample_log(self, filename="app.log"):
        """Create a sample log file"""
        log_entries = [
            "2024-01-15 10:30:15 INFO Application started",
            "2024-01-15 10:30:16 DEBUG Loading configuration",
            "2024-01-15 10:30:17 INFO Connected to database",
            "2024-01-15 10:31:45 WARNING High memory usage detected",
            "2024-01-15 10:32:10 ERROR Failed to fetch user data",
            "2024-01-15 10:32:11 ERROR Database connection timeout",
            "2024-01-15 10:32:30 INFO Reconnecting to database",
            "2024-01-15 10:32:31 INFO Connection restored",
            "2024-01-15 10:45:00 WARNING Slow query detected",
            "2024-01-15 11:00:00 INFO Backup completed successfully"
        ]

        with open(filename, 'w') as f:
            for entry in log_entries:
                f.write(entry + '\n')

        print(f"Created sample log: {filename}")
        return filename

    def parse_log(self, filename):
        """Parse log file"""
        self.entries = []

        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(' ', 3)
                    if len(parts) >= 4:
                        entry = {
                            'date': parts[0],
                            'time': parts[1],
                            'level': parts[2],
                            'message': parts[3]
                        }
                        self.entries.append(entry)

        print(f"Parsed {len(self.entries)} log entries")

    def filter_by_level(self, level):
        """Filter logs by level"""
        return [e for e in self.entries if e['level'] == level]

    def count_by_level(self):
        """Count entries by log level"""
        counts = {}
        for entry in self.entries:
            level = entry['level']
            counts[level] = counts.get(level, 0) + 1
        return counts

    def find_errors(self):
        """Find all error entries"""
        errors = self.filter_by_level('ERROR')
        return errors

    def get_time_range(self):
        """Get time range of logs"""
        if not self.entries:
            return None

        first = f"{self.entries[0]['date']} {self.entries[0]['time']}"
        last = f"{self.entries[-1]['date']} {self.entries[-1]['time']}"

        return {'start': first, 'end': last}

    def save_filtered_log(self, entries, filename="filtered.log"):
        """Save filtered entries to new log file"""
        with open(filename, 'w') as f:
            for entry in entries:
                line = f"{entry['date']} {entry['time']} {entry['level']} {entry['message']}\n"
                f.write(line)

        print(f"Saved {len(entries)} entries to {filename}")

    def generate_summary(self):
        """Generate log summary"""
        print("\nLog File Summary")
        print("=" * 40)

        time_range = self.get_time_range()
        if time_range:
            print(f"Time Range: {time_range['start']} to {time_range['end']}")

        print(f"Total Entries: {len(self.entries)}")

        counts = self.count_by_level()
        print("\nEntries by Level:")
        for level, count in sorted(counts.items()):
            print(f"  {level}: {count}")

        errors = self.find_errors()
        if errors:
            print(f"\nError Messages ({len(errors)}):")
            for error in errors:
                print(f"  [{error['time']}] {error['message']}")

parser = LogParser()

log_file = parser.create_sample_log()
parser.parse_log(log_file)

parser.generate_summary()

warnings = parser.filter_by_level('WARNING')
print(f"\nWarning entries: {len(warnings)}")

errors = parser.find_errors()
if errors:
    parser.save_filtered_log(errors, "errors_only.log")

print("\n" + "="*40)
print("PRACTICE PROBLEM 4: Simple File Database")
print("="*40)

class FileDatabase:
    """Simple database using text files"""

    def __init__(self, db_dir="file_db"):
        self.db_dir = db_dir
        self.ensure_db_exists()

    def ensure_db_exists(self):
        """Create database directory if it doesn't exist"""
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)
            print(f"Created database directory: {self.db_dir}")

    def _get_table_path(self, table):
        """Get file path for table"""
        return os.path.join(self.db_dir, f"{table}.json")

    def create_table(self, table_name):
        """Create a new table (file)"""
        table_path = self._get_table_path(table_name)

        if os.path.exists(table_path):
            print(f"Table '{table_name}' already exists")
            return False

        with open(table_path, 'w') as f:
            json.dump([], f)

        print(f"Created table: {table_name}")
        return True

    def insert(self, table, record):
        """Insert a record into table"""
        table_path = self._get_table_path(table)

        if not os.path.exists(table_path):
            self.create_table(table)

        with open(table_path, 'r') as f:
            data = json.load(f)

        record['_id'] = len(data) + 1
        data.append(record)

        with open(table_path, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"Inserted record with ID {record['_id']} into {table}")
        return record['_id']

    def select(self, table, condition=None):
        """Select records from table"""
        table_path = self._get_table_path(table)

        if not os.path.exists(table_path):
            print(f"Table '{table}' does not exist")
            return []

        with open(table_path, 'r') as f:
            data = json.load(f)

        if condition:
            filtered = []
            for record in data:
                if condition(record):
                    filtered.append(record)
            return filtered

        return data

    def update(self, table, record_id, updates):
        """Update a record"""
        table_path = self._get_table_path(table)

        if not os.path.exists(table_path):
            print(f"Table '{table}' does not exist")
            return False

        with open(table_path, 'r') as f:
            data = json.load(f)

        for record in data:
            if record.get('_id') == record_id:
                record.update(updates)

                with open(table_path, 'w') as f:
                    json.dump(data, f, indent=2)

                print(f"Updated record {record_id} in {table}")
                return True

        print(f"Record {record_id} not found in {table}")
        return False

    def delete(self, table, record_id):
        """Delete a record"""
        table_path = self._get_table_path(table)

        if not os.path.exists(table_path):
            print(f"Table '{table}' does not exist")
            return False

        with open(table_path, 'r') as f:
            data = json.load(f)

        original_length = len(data)
        data = [r for r in data if r.get('_id') != record_id]

        if len(data) < original_length:
            with open(table_path, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"Deleted record {record_id} from {table}")
            return True

        print(f"Record {record_id} not found in {table}")
        return False

    def list_tables(self):
        """List all tables in database"""
        tables = []
        for file in os.listdir(self.db_dir):
            if file.endswith('.json'):
                tables.append(file[:-5])
        return tables

db = FileDatabase()

db.create_table("users")
db.create_table("products")

user_id = db.insert("users", {"name": "Alice", "email": "alice@example.com", "age": 28})
db.insert("users", {"name": "Bob", "email": "bob@example.com", "age": 35})
db.insert("users", {"name": "Charlie", "email": "charlie@example.com", "age": 42})

db.insert("products", {"name": "Laptop", "price": 999.99, "stock": 10})
db.insert("products", {"name": "Mouse", "price": 29.99, "stock": 50})

print("\nAll users:")
users = db.select("users")
for user in users:
    print(f"  {user}")

print("\nUsers over 30:")
older_users = db.select("users", lambda u: u.get('age', 0) > 30)
for user in older_users:
    print(f"  {user}")

db.update("users", user_id, {"age": 29})

print(f"\nTables in database: {db.list_tables()}")

# Clean up demo files
for file in ["demo_notes.txt", "sample_data.csv", "app.log", "errors_only.log"]:
    if os.path.exists(file):
        os.remove(file)

if os.path.exists("file_db"):
    import shutil
    shutil.rmtree("file_db")

print("\n" + "="*40)
print("KEY TAKEAWAYS")
print("="*40)
print("""
1. Always use 'with' statement for file operations
2. Choose appropriate file mode (r, w, a)
3. Handle file exceptions properly
4. JSON is great for structured data
5. CSV is ideal for tabular data
6. Binary mode for non-text files
7. Always close files or use context managers
""")