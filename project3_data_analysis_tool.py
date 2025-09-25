"""
Final Project 3: Data Analysis Tool
A comprehensive data analysis tool with CSV parsing, generators for large datasets,
list comprehensions for transformation, and statistical functions using map/filter/reduce.
"""

import csv
import json
import os
import random
from datetime import datetime, timedelta
from functools import reduce
from typing import Dict, List, Any, Generator, Optional, Tuple
import operator
import math

class DataGenerator:
    """Generate sample datasets for analysis"""

    @staticmethod
    def generate_sales_data(num_records: int = 1000) -> Generator[Dict, None, None]:
        """Generate sales data using generator for memory efficiency"""
        products = ['Laptop', 'Phone', 'Tablet', 'Headphones', 'Speaker', 'Monitor', 'Keyboard', 'Mouse']
        regions = ['North', 'South', 'East', 'West', 'Central']
        categories = ['Electronics', 'Accessories', 'Computing', 'Audio', 'Display']

        start_date = datetime(2024, 1, 1)

        for i in range(num_records):
            yield {
                'id': i + 1,
                'date': (start_date + timedelta(days=random.randint(0, 364))).strftime('%Y-%m-%d'),
                'product': random.choice(products),
                'category': random.choice(categories),
                'region': random.choice(regions),
                'quantity': random.randint(1, 50),
                'price': round(random.uniform(10, 2000), 2),
                'customer_age': random.randint(18, 70),
                'customer_satisfaction': random.randint(1, 5),
                'discount_percent': random.choice([0, 5, 10, 15, 20, 25])
            }

    @staticmethod
    def generate_employee_data(num_employees: int = 200) -> Generator[Dict, None, None]:
        """Generate employee data"""
        departments = ['IT', 'Sales', 'HR', 'Marketing', 'Finance', 'Operations']
        positions = ['Junior', 'Mid', 'Senior', 'Lead', 'Manager', 'Director']

        for i in range(num_employees):
            department = random.choice(departments)
            position = random.choice(positions)
            base_salary = {
                'Junior': 40000, 'Mid': 60000, 'Senior': 80000,
                'Lead': 100000, 'Manager': 120000, 'Director': 150000
            }[position]

            yield {
                'employee_id': f'EMP{i+1:04d}',
                'age': random.randint(22, 65),
                'department': department,
                'position': position,
                'years_of_service': random.randint(0, 20),
                'salary': base_salary + random.randint(-10000, 20000),
                'performance_rating': round(random.uniform(2.0, 5.0), 1),
                'projects_completed': random.randint(0, 50)
            }

class DataProcessor:
    """Process and transform data using functional programming"""

    @staticmethod
    def filter_by_condition(data: List[Dict], **conditions) -> List[Dict]:
        """Filter data using multiple conditions"""
        result = data

        for key, value in conditions.items():
            if callable(value):
                result = list(filter(lambda x: value(x.get(key)), result))
            else:
                result = list(filter(lambda x: x.get(key) == value, result))

        return result

    @staticmethod
    def transform_with_comprehension(data: List[Dict], transformations: Dict) -> List[Dict]:
        """Transform data using list comprehensions"""
        return [
            {
                **record,
                **{
                    new_key: transform(record) if callable(transform) else transform
                    for new_key, transform in transformations.items()
                }
            }
            for record in data
        ]

    @staticmethod
    def aggregate_by_key(data: List[Dict], group_key: str, value_key: str,
                        operation: str = 'sum') -> Dict:
        """Aggregate data by a key using reduce"""
        grouped = {}

        for record in data:
            key = record.get(group_key)
            value = record.get(value_key, 0)

            if key not in grouped:
                grouped[key] = []

            grouped[key].append(value)

        operations = {
            'sum': lambda values: reduce(operator.add, values, 0),
            'mean': lambda values: reduce(operator.add, values, 0) / len(values) if values else 0,
            'max': lambda values: reduce(max, values) if values else 0,
            'min': lambda values: reduce(min, values) if values else 0,
            'count': lambda values: len(values)
        }

        agg_func = operations.get(operation, operations['sum'])

        return {key: agg_func(values) for key, values in grouped.items()}

    @staticmethod
    def calculate_statistics(values: List[float]) -> Dict[str, float]:
        """Calculate comprehensive statistics using map/filter/reduce"""
        if not values:
            return {}

        n = len(values)

        # Mean using reduce
        mean = reduce(operator.add, values) / n

        # Variance using map and reduce
        squared_diffs = map(lambda x: (x - mean) ** 2, values)
        variance = reduce(operator.add, squared_diffs) / n

        # Standard deviation
        std_dev = math.sqrt(variance)

        # Median
        sorted_values = sorted(values)
        median = sorted_values[n // 2] if n % 2 else \
                (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2

        # Mode (most frequent value)
        frequency = {}
        for value in values:
            frequency[value] = frequency.get(value, 0) + 1
        mode = max(frequency, key=frequency.get) if frequency else None

        # Quartiles
        def percentile(data, p):
            k = (len(data) - 1) * p / 100
            f = int(k)
            c = k - f
            if f < len(data) - 1:
                return data[f] * (1 - c) + data[f + 1] * c
            return data[f]

        q1 = percentile(sorted_values, 25)
        q3 = percentile(sorted_values, 75)
        iqr = q3 - q1

        return {
            'count': n,
            'sum': reduce(operator.add, values),
            'mean': mean,
            'median': median,
            'mode': mode,
            'std_dev': std_dev,
            'variance': variance,
            'min': reduce(min, values),
            'max': reduce(max, values),
            'range': reduce(max, values) - reduce(min, values),
            'q1': q1,
            'q3': q3,
            'iqr': iqr
        }

class CSVHandler:
    """Handle CSV file operations"""

    @staticmethod
    def read_csv_generator(filepath: str, chunk_size: int = 100) -> Generator[List[Dict], None, None]:
        """Read CSV in chunks using generator"""
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            chunk = []

            for row in reader:
                # Convert numeric strings to appropriate types
                for key, value in row.items():
                    try:
                        if '.' in value:
                            row[key] = float(value)
                        else:
                            row[key] = int(value)
                    except (ValueError, AttributeError):
                        pass  # Keep as string

                chunk.append(row)

                if len(chunk) >= chunk_size:
                    yield chunk
                    chunk = []

            if chunk:
                yield chunk

    @staticmethod
    def write_csv(filepath: str, data: List[Dict]):
        """Write data to CSV file"""
        if not data:
            return

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def create_sample_csv(filepath: str, num_records: int = 100):
        """Create sample CSV for testing"""
        generator = DataGenerator.generate_sales_data(num_records)
        data = list(generator)
        CSVHandler.write_csv(filepath, data)
        return filepath

class DataAnalyzer:
    """Main data analysis engine"""

    def __init__(self):
        self.data: List[Dict] = []
        self.metadata: Dict = {}

    def load_data(self, source: str, data_type: str = 'csv'):
        """Load data from various sources"""
        if data_type == 'csv':
            if os.path.exists(source):
                self.data = []
                for chunk in CSVHandler.read_csv_generator(source):
                    self.data.extend(chunk)
                self.update_metadata()
                return f"Loaded {len(self.data)} records from {source}"
            else:
                return f"File {source} not found"
        elif data_type == 'generator':
            if source == 'sales':
                self.data = list(DataGenerator.generate_sales_data(1000))
            elif source == 'employee':
                self.data = list(DataGenerator.generate_employee_data(200))
            self.update_metadata()
            return f"Generated {len(self.data)} {source} records"

    def update_metadata(self):
        """Update metadata about loaded data"""
        if not self.data:
            self.metadata = {}
            return

        self.metadata = {
            'record_count': len(self.data),
            'columns': list(self.data[0].keys()),
            'column_types': {}
        }

        # Detect column types
        for col in self.metadata['columns']:
            sample_values = [row[col] for row in self.data[:10] if col in row]
            if sample_values:
                types = set(type(v).__name__ for v in sample_values)
                self.metadata['column_types'][col] = list(types)

    def filter_data(self, **conditions) -> 'DataAnalyzer':
        """Filter data and return new analyzer instance"""
        filtered_analyzer = DataAnalyzer()
        filtered_analyzer.data = DataProcessor.filter_by_condition(self.data, **conditions)
        filtered_analyzer.update_metadata()
        return filtered_analyzer

    def transform_data(self, transformations: Dict) -> 'DataAnalyzer':
        """Transform data with new calculated fields"""
        transformed_analyzer = DataAnalyzer()
        transformed_analyzer.data = DataProcessor.transform_with_comprehension(
            self.data, transformations
        )
        transformed_analyzer.update_metadata()
        return transformed_analyzer

    def aggregate(self, group_by: str, value_column: str, operation: str = 'sum') -> Dict:
        """Aggregate data by grouping"""
        return DataProcessor.aggregate_by_key(self.data, group_by, value_column, operation)

    def get_column_statistics(self, column: str) -> Dict[str, float]:
        """Get statistics for a numeric column"""
        values = [row[column] for row in self.data if column in row and isinstance(row[column], (int, float))]
        return DataProcessor.calculate_statistics(values)

    def correlation(self, col1: str, col2: str) -> float:
        """Calculate correlation between two columns"""
        pairs = [(row[col1], row[col2]) for row in self.data
                 if col1 in row and col2 in row
                 and isinstance(row[col1], (int, float))
                 and isinstance(row[col2], (int, float))]

        if not pairs:
            return 0

        x_values, y_values = zip(*pairs)

        x_mean = sum(x_values) / len(x_values)
        y_mean = sum(y_values) / len(y_values)

        numerator = sum((x - x_mean) * (y - y_mean) for x, y in pairs)
        denominator = math.sqrt(
            sum((x - x_mean) ** 2 for x in x_values) *
            sum((y - y_mean) ** 2 for y in y_values)
        )

        return numerator / denominator if denominator else 0

    def outlier_detection(self, column: str, method: str = 'iqr') -> List[Dict]:
        """Detect outliers in a column"""
        values = [(i, row[column]) for i, row in enumerate(self.data)
                  if column in row and isinstance(row[column], (int, float))]

        if not values:
            return []

        _, nums = zip(*values)
        stats = DataProcessor.calculate_statistics(list(nums))

        outliers = []

        if method == 'iqr':
            q1 = stats['q1']
            q3 = stats['q3']
            iqr = stats['iqr']
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            outliers = [self.data[i] for i, v in values
                       if v < lower_bound or v > upper_bound]

        elif method == 'zscore':
            mean = stats['mean']
            std_dev = stats['std_dev']
            threshold = 3

            outliers = [self.data[i] for i, v in values
                       if abs((v - mean) / std_dev) > threshold]

        return outliers

    def time_series_analysis(self, date_column: str, value_column: str) -> Dict:
        """Analyze time series data"""
        # Convert dates and sort
        time_data = [
            {
                'date': datetime.strptime(row[date_column], '%Y-%m-%d')
                        if isinstance(row[date_column], str) else row[date_column],
                'value': row[value_column]
            }
            for row in self.data
            if date_column in row and value_column in row
        ]

        time_data.sort(key=lambda x: x['date'])

        if len(time_data) < 2:
            return {}

        # Calculate moving average
        window_size = min(7, len(time_data) // 3)
        moving_avg = []
        for i in range(len(time_data) - window_size + 1):
            window = time_data[i:i + window_size]
            avg = sum(w['value'] for w in window) / window_size
            moving_avg.append(avg)

        # Calculate trend
        values = [d['value'] for d in time_data]
        n = len(values)
        x_sum = n * (n - 1) / 2
        y_sum = sum(values)
        xy_sum = sum(i * v for i, v in enumerate(values))
        x_squared_sum = n * (n - 1) * (2 * n - 1) / 6

        slope = (n * xy_sum - x_sum * y_sum) / (n * x_squared_sum - x_sum ** 2) if n > 1 else 0

        return {
            'start_date': time_data[0]['date'].strftime('%Y-%m-%d'),
            'end_date': time_data[-1]['date'].strftime('%Y-%m-%d'),
            'data_points': len(time_data),
            'trend_slope': slope,
            'trend_direction': 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'flat',
            'moving_average': moving_avg,
            'min_value': min(values),
            'max_value': max(values),
            'range': max(values) - min(values)
        }

    def generate_report(self) -> str:
        """Generate comprehensive analysis report"""
        if not self.data:
            return "No data loaded for analysis"

        report = ["=" * 60]
        report.append("DATA ANALYSIS REPORT")
        report.append("=" * 60)

        # Dataset overview
        report.append(f"\nDataset Overview:")
        report.append(f"  Records: {self.metadata['record_count']}")
        report.append(f"  Columns: {', '.join(self.metadata['columns'])}")

        # Numeric column statistics
        numeric_cols = [col for col in self.metadata['columns']
                       if any(isinstance(row.get(col), (int, float)) for row in self.data[:10])]

        if numeric_cols:
            report.append(f"\nNumeric Column Statistics:")
            for col in numeric_cols:
                stats = self.get_column_statistics(col)
                if stats:
                    report.append(f"\n  {col}:")
                    report.append(f"    Mean: {stats['mean']:.2f}")
                    report.append(f"    Median: {stats['median']:.2f}")
                    report.append(f"    Std Dev: {stats['std_dev']:.2f}")
                    report.append(f"    Range: [{stats['min']:.2f}, {stats['max']:.2f}]")

        # Categorical column analysis
        categorical_cols = [col for col in self.metadata['columns']
                           if not any(isinstance(row.get(col), (int, float)) for row in self.data[:10])]

        if categorical_cols:
            report.append(f"\nCategorical Column Analysis:")
            for col in categorical_cols[:3]:  # Limit to first 3
                unique_values = set(row.get(col) for row in self.data if col in row)
                report.append(f"  {col}: {len(unique_values)} unique values")
                if len(unique_values) <= 5:
                    report.append(f"    Values: {', '.join(map(str, unique_values))}")

        # Correlations (for first few numeric columns)
        if len(numeric_cols) >= 2:
            report.append(f"\nCorrelations:")
            for i, col1 in enumerate(numeric_cols[:3]):
                for col2 in numeric_cols[i+1:4]:
                    corr = self.correlation(col1, col2)
                    report.append(f"  {col1} vs {col2}: {corr:.3f}")

        return "\n".join(report)

    def export_results(self, filepath: str, filtered_data: bool = False):
        """Export analysis results"""
        data_to_export = self.data if not filtered_data else self.data

        if filepath.endswith('.csv'):
            CSVHandler.write_csv(filepath, data_to_export)
        elif filepath.endswith('.json'):
            with open(filepath, 'w') as f:
                json.dump(data_to_export, f, indent=2, default=str)

        return f"Exported {len(data_to_export)} records to {filepath}"

class DataAnalysisCLI:
    """Command-line interface for data analysis"""

    def __init__(self):
        self.analyzer = DataAnalyzer()
        self.running = True

    def run(self):
        """Run the CLI application"""
        print("\n" + "="*60)
        print("DATA ANALYSIS TOOL")
        print("="*60)

        while self.running:
            self.show_menu()
            choice = input("\nEnter your choice: ").strip()
            self.handle_choice(choice)

    def show_menu(self):
        """Display main menu"""
        print("\n--- Main Menu ---")
        print("1. Load/Generate Data")
        print("2. View Data Info")
        print("3. Filter Data")
        print("4. Transform Data")
        print("5. Statistical Analysis")
        print("6. Aggregation")
        print("7. Advanced Analysis")
        print("8. Generate Report")
        print("9. Export Data")
        print("0. Exit")

    def handle_choice(self, choice):
        """Handle menu choice"""
        try:
            if choice == "1":
                self.load_data()
            elif choice == "2":
                self.view_data_info()
            elif choice == "3":
                self.filter_data()
            elif choice == "4":
                self.transform_data()
            elif choice == "5":
                self.statistical_analysis()
            elif choice == "6":
                self.aggregation()
            elif choice == "7":
                self.advanced_analysis()
            elif choice == "8":
                self.generate_report()
            elif choice == "9":
                self.export_data()
            elif choice == "0":
                print("Goodbye!")
                self.running = False
            else:
                print("Invalid choice")

        except Exception as e:
            print(f"Error: {e}")

    def load_data(self):
        """Load or generate data"""
        print("\n--- Load/Generate Data ---")
        print("1. Load from CSV file")
        print("2. Generate sales data")
        print("3. Generate employee data")
        print("4. Create and load sample CSV")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            filepath = input("Enter CSV filepath: ").strip()
            result = self.analyzer.load_data(filepath, 'csv')
            print(result)
        elif choice == "2":
            result = self.analyzer.load_data('sales', 'generator')
            print(result)
        elif choice == "3":
            result = self.analyzer.load_data('employee', 'generator')
            print(result)
        elif choice == "4":
            filepath = "sample_data.csv"
            CSVHandler.create_sample_csv(filepath, 500)
            result = self.analyzer.load_data(filepath, 'csv')
            print(f"Created sample CSV and {result}")

    def view_data_info(self):
        """View information about loaded data"""
        if not self.analyzer.data:
            print("No data loaded")
            return

        print("\n--- Data Information ---")
        print(f"Records: {len(self.analyzer.data)}")
        print(f"Columns: {', '.join(self.analyzer.metadata['columns'])}")

        print("\nColumn Types:")
        for col, types in self.analyzer.metadata['column_types'].items():
            print(f"  {col}: {', '.join(types)}")

        print("\nFirst 5 records:")
        for i, record in enumerate(self.analyzer.data[:5], 1):
            print(f"{i}. {record}")

    def filter_data(self):
        """Filter data"""
        if not self.analyzer.data:
            print("No data loaded")
            return

        print("\n--- Filter Data ---")
        column = input("Enter column name: ").strip()

        if column not in self.analyzer.metadata['columns']:
            print(f"Column '{column}' not found")
            return

        print("Filter type:")
        print("1. Exact match")
        print("2. Greater than")
        print("3. Less than")
        print("4. Contains (for text)")

        filter_type = input("Enter choice: ").strip()

        if filter_type == "1":
            value = input("Enter value: ").strip()
            try:
                value = float(value)
            except ValueError:
                pass
            filtered = self.analyzer.filter_data(**{column: value})
        elif filter_type == "2":
            value = float(input("Enter value: "))
            filtered = self.analyzer.filter_data(**{column: lambda x: x > value})
        elif filter_type == "3":
            value = float(input("Enter value: "))
            filtered = self.analyzer.filter_data(**{column: lambda x: x < value})
        elif filter_type == "4":
            value = input("Enter text: ").strip()
            filtered = self.analyzer.filter_data(**{column: lambda x: value in str(x)})
        else:
            print("Invalid choice")
            return

        print(f"Filtered: {len(filtered.data)} records (from {len(self.analyzer.data)})")

        if input("Use filtered data? (y/n): ").lower() == 'y':
            self.analyzer = filtered

    def transform_data(self):
        """Transform data"""
        if not self.analyzer.data:
            print("No data loaded")
            return

        print("\n--- Transform Data ---")
        print("Available transformations:")
        print("1. Calculate total (multiply columns)")
        print("2. Add percentage column")
        print("3. Extract year from date")
        print("4. Custom calculation")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            col1 = input("First column: ").strip()
            col2 = input("Second column: ").strip()
            new_col = input("New column name: ").strip()

            transformations = {
                new_col: lambda row: row.get(col1, 0) * row.get(col2, 0)
            }

        elif choice == "2":
            value_col = input("Value column: ").strip()
            total_col = input("Total column: ").strip()
            new_col = input("New column name: ").strip()

            transformations = {
                new_col: lambda row: (row.get(value_col, 0) / row.get(total_col, 1)) * 100 if row.get(total_col) else 0
            }

        elif choice == "3":
            date_col = input("Date column: ").strip()
            transformations = {
                'year': lambda row: row.get(date_col, '').split('-')[0] if isinstance(row.get(date_col), str) else None
            }

        else:
            return

        transformed = self.analyzer.transform_data(transformations)
        print(f"Transformation complete. New columns added.")

        if input("Use transformed data? (y/n): ").lower() == 'y':
            self.analyzer = transformed

    def statistical_analysis(self):
        """Perform statistical analysis"""
        if not self.analyzer.data:
            print("No data loaded")
            return

        print("\n--- Statistical Analysis ---")
        numeric_cols = [col for col in self.analyzer.metadata['columns']
                       if any(isinstance(row.get(col), (int, float)) for row in self.analyzer.data[:10])]

        if not numeric_cols:
            print("No numeric columns found")
            return

        print("Numeric columns:")
        for i, col in enumerate(numeric_cols, 1):
            print(f"{i}. {col}")

        idx = int(input("Select column: ")) - 1
        column = numeric_cols[idx]

        stats = self.analyzer.get_column_statistics(column)

        print(f"\nStatistics for '{column}':")
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.2f}")
            else:
                print(f"  {key}: {value}")

    def aggregation(self):
        """Perform aggregation"""
        if not self.analyzer.data:
            print("No data loaded")
            return

        print("\n--- Aggregation ---")
        group_col = input("Group by column: ").strip()
        value_col = input("Value column: ").strip()

        print("Aggregation operation:")
        print("1. Sum")
        print("2. Mean")
        print("3. Count")
        print("4. Max")
        print("5. Min")

        op_choice = input("Enter choice: ").strip()
        operations = {'1': 'sum', '2': 'mean', '3': 'count', '4': 'max', '5': 'min'}
        operation = operations.get(op_choice, 'sum')

        result = self.analyzer.aggregate(group_col, value_col, operation)

        print(f"\n{operation.title()} of '{value_col}' by '{group_col}':")
        for key, value in sorted(result.items())[:10]:  # Show first 10
            if isinstance(value, float):
                print(f"  {key}: {value:.2f}")
            else:
                print(f"  {key}: {value}")

    def advanced_analysis(self):
        """Advanced analysis options"""
        if not self.analyzer.data:
            print("No data loaded")
            return

        print("\n--- Advanced Analysis ---")
        print("1. Correlation Analysis")
        print("2. Outlier Detection")
        print("3. Time Series Analysis")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            numeric_cols = [col for col in self.analyzer.metadata['columns']
                           if any(isinstance(row.get(col), (int, float)) for row in self.analyzer.data[:10])]

            if len(numeric_cols) < 2:
                print("Need at least 2 numeric columns")
                return

            print("Select two columns for correlation:")
            for i, col in enumerate(numeric_cols, 1):
                print(f"{i}. {col}")

            idx1 = int(input("First column: ")) - 1
            idx2 = int(input("Second column: ")) - 1

            corr = self.analyzer.correlation(numeric_cols[idx1], numeric_cols[idx2])
            print(f"\nCorrelation between '{numeric_cols[idx1]}' and '{numeric_cols[idx2]}': {corr:.3f}")

            if abs(corr) > 0.7:
                print("Strong correlation detected!")
            elif abs(corr) > 0.3:
                print("Moderate correlation detected.")
            else:
                print("Weak or no correlation.")

        elif choice == "2":
            numeric_cols = [col for col in self.analyzer.metadata['columns']
                           if any(isinstance(row.get(col), (int, float)) for row in self.analyzer.data[:10])]

            print("Select column for outlier detection:")
            for i, col in enumerate(numeric_cols, 1):
                print(f"{i}. {col}")

            idx = int(input("Column: ")) - 1
            column = numeric_cols[idx]

            method = input("Method (iqr/zscore): ").strip() or 'iqr'

            outliers = self.analyzer.outlier_detection(column, method)
            print(f"\nFound {len(outliers)} outliers in '{column}' using {method} method")

            if outliers and len(outliers) <= 10:
                print("Outlier records:")
                for outlier in outliers:
                    print(f"  {outlier}")

        elif choice == "3":
            date_cols = [col for col in self.analyzer.metadata['columns']
                        if 'date' in col.lower()]

            if not date_cols:
                print("No date columns found")
                return

            date_col = date_cols[0] if len(date_cols) == 1 else \
                      input(f"Date column ({', '.join(date_cols)}): ").strip()

            numeric_cols = [col for col in self.analyzer.metadata['columns']
                           if any(isinstance(row.get(col), (int, float)) for row in self.analyzer.data[:10])]

            print("Select value column:")
            for i, col in enumerate(numeric_cols, 1):
                print(f"{i}. {col}")

            idx = int(input("Column: ")) - 1
            value_col = numeric_cols[idx]

            result = self.analyzer.time_series_analysis(date_col, value_col)

            if result:
                print(f"\nTime Series Analysis:")
                print(f"  Period: {result['start_date']} to {result['end_date']}")
                print(f"  Data points: {result['data_points']}")
                print(f"  Trend: {result['trend_direction']} (slope: {result['trend_slope']:.4f})")
                print(f"  Value range: [{result['min_value']:.2f}, {result['max_value']:.2f}]")

    def generate_report(self):
        """Generate analysis report"""
        if not self.analyzer.data:
            print("No data loaded")
            return

        report = self.analyzer.generate_report()
        print("\n" + report)

        if input("\nSave report to file? (y/n): ").lower() == 'y':
            with open("analysis_report.txt", 'w') as f:
                f.write(report)
            print("Report saved to analysis_report.txt")

    def export_data(self):
        """Export data"""
        if not self.analyzer.data:
            print("No data loaded")
            return

        print("\n--- Export Data ---")
        print("1. Export to CSV")
        print("2. Export to JSON")

        choice = input("Enter choice: ").strip()
        filepath = input("Enter filepath: ").strip()

        if choice == "1" and not filepath.endswith('.csv'):
            filepath += '.csv'
        elif choice == "2" and not filepath.endswith('.json'):
            filepath += '.json'

        result = self.analyzer.export_results(filepath)
        print(result)

def demo_mode():
    """Run demo analysis"""
    print("\n" + "="*60)
    print("DATA ANALYSIS TOOL - DEMO MODE")
    print("="*60)

    analyzer = DataAnalyzer()

    # Generate sample data
    print("\nGenerating sample sales data...")
    analyzer.load_data('sales', 'generator')

    # Show data info
    print(f"\nLoaded {len(analyzer.data)} records")
    print(f"Columns: {', '.join(analyzer.metadata['columns'])}")

    # Perform analysis
    print("\n=== Statistical Analysis ===")
    stats = analyzer.get_column_statistics('price')
    print(f"Price statistics:")
    for key, value in list(stats.items())[:5]:
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")

    print("\n=== Aggregation ===")
    region_sales = analyzer.aggregate('region', 'price', 'sum')
    print("Total sales by region:")
    for region, total in region_sales.items():
        print(f"  {region}: ${total:,.2f}")

    print("\n=== Filtering ===")
    high_value = analyzer.filter_data(price=lambda x: x > 1000)
    print(f"High-value transactions (>$1000): {len(high_value.data)} records")

    print("\n=== Transformation ===")
    transformed = analyzer.transform_data({
        'total_value': lambda row: row.get('quantity', 0) * row.get('price', 0),
        'discount_amount': lambda row: row.get('price', 0) * row.get('discount_percent', 0) / 100
    })
    print(f"Added calculated columns: total_value, discount_amount")

    print("\n=== Correlation Analysis ===")
    corr = analyzer.correlation('quantity', 'customer_satisfaction')
    print(f"Correlation between quantity and satisfaction: {corr:.3f}")

    # Generate report
    print("\n=== Summary Report ===")
    report_lines = analyzer.generate_report().split('\n')
    for line in report_lines[:20]:  # Show first 20 lines
        print(line)

    print("\nDemo completed!")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_mode()
    else:
        cli = DataAnalysisCLI()
        cli.run()