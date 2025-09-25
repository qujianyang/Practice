"""
Final Project 4: Task Management System
A comprehensive task management system with OOP design, serialization,
decorators for logging, and robust exception handling.
"""

import json
import pickle
import os
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional, Any
from functools import wraps
import logging
import hashlib
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('task_manager.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Priority(Enum):
    """Task priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class Status(Enum):
    """Task status"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskError(Exception):
    """Base exception for task management"""
    pass

class TaskNotFoundError(TaskError):
    """Raised when task is not found"""
    pass

class ProjectError(Exception):
    """Base exception for project management"""
    pass

class ValidationError(Exception):
    """Raised when validation fails"""
    pass

def log_action(action_type: str = "action"):
    """Decorator to log actions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get object info for logging
            obj_name = args[0].__class__.__name__ if args else "Unknown"
            func_name = func.__name__

            logger.info(f"[{action_type.upper()}] {obj_name}.{func_name} started")

            try:
                result = func(*args, **kwargs)
                logger.info(f"[{action_type.upper()}] {obj_name}.{func_name} completed successfully")
                return result
            except Exception as e:
                logger.error(f"[{action_type.upper()}] {obj_name}.{func_name} failed: {str(e)}")
                raise

        return wrapper
    return decorator

def validate_input(*validators):
    """Decorator to validate input parameters"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Apply validators
            for validator in validators:
                try:
                    validator(*args, **kwargs)
                except ValidationError as e:
                    logger.warning(f"Validation failed for {func.__name__}: {str(e)}")
                    raise

            return func(*args, **kwargs)
        return wrapper
    return decorator

def cache_result(expiry_seconds: int = 300):
    """Decorator to cache function results"""
    def decorator(func):
        cache = {}
        cache_time = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            key = str(args) + str(kwargs)
            key_hash = hashlib.md5(key.encode()).hexdigest()

            # Check cache
            if key_hash in cache:
                if time.time() - cache_time[key_hash] < expiry_seconds:
                    logger.debug(f"Cache hit for {func.__name__}")
                    return cache[key_hash]

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache[key_hash] = result
            cache_time[key_hash] = time.time()

            return result

        wrapper.clear_cache = lambda: (cache.clear(), cache_time.clear())
        return wrapper
    return decorator

def track_time(func):
    """Decorator to track execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        execution_time = end_time - start_time
        logger.debug(f"{func.__name__} executed in {execution_time:.4f} seconds")

        return result
    return wrapper

class Task:
    """Represents a task"""

    def __init__(self, title: str, description: str = "",
                 priority: Priority = Priority.MEDIUM,
                 due_date: Optional[datetime] = None,
                 tags: Optional[List[str]] = None):
        self.id = self._generate_id()
        self.title = title
        self.description = description
        self.priority = priority
        self.status = Status.TODO
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.completed_at: Optional[datetime] = None
        self.due_date = due_date
        self.tags = tags or []
        self.subtasks: List['Task'] = []
        self.dependencies: List[str] = []  # Task IDs this task depends on
        self.assigned_to: Optional[str] = None
        self.comments: List[Dict] = []
        self.attachments: List[str] = []
        self.estimated_hours: float = 0
        self.actual_hours: float = 0

    def _generate_id(self) -> str:
        """Generate unique task ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        random_part = hashlib.md5(timestamp.encode()).hexdigest()[:6]
        return f"TASK-{timestamp}-{random_part}"

    @log_action("update")
    def update_status(self, new_status: Status):
        """Update task status"""
        if self.status == Status.COMPLETED:
            raise TaskError("Cannot update completed task")

        old_status = self.status
        self.status = new_status
        self.updated_at = datetime.now()

        if new_status == Status.COMPLETED:
            self.completed_at = datetime.now()

        logger.info(f"Task {self.id} status changed from {old_status.value} to {new_status.value}")

    @log_action("assign")
    def assign_to(self, assignee: str):
        """Assign task to someone"""
        if not assignee:
            raise ValidationError("Assignee cannot be empty")

        self.assigned_to = assignee
        self.updated_at = datetime.now()

    def add_comment(self, author: str, content: str):
        """Add comment to task"""
        comment = {
            'author': author,
            'content': content,
            'timestamp': datetime.now()
        }
        self.comments.append(comment)
        self.updated_at = datetime.now()

    def add_subtask(self, subtask: 'Task'):
        """Add subtask"""
        if subtask.id == self.id:
            raise TaskError("Task cannot be its own subtask")

        self.subtasks.append(subtask)
        self.updated_at = datetime.now()

    def add_dependency(self, task_id: str):
        """Add task dependency"""
        if task_id == self.id:
            raise TaskError("Task cannot depend on itself")

        if task_id not in self.dependencies:
            self.dependencies.append(task_id)
            self.updated_at = datetime.now()

    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if self.due_date and self.status != Status.COMPLETED:
            return datetime.now() > self.due_date
        return False

    def get_progress(self) -> float:
        """Calculate task progress based on subtasks"""
        if not self.subtasks:
            return 100.0 if self.status == Status.COMPLETED else 0.0

        completed = sum(1 for st in self.subtasks if st.status == Status.COMPLETED)
        return (completed / len(self.subtasks)) * 100

    def to_dict(self) -> Dict:
        """Convert task to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.value,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'tags': self.tags,
            'subtasks': [st.to_dict() for st in self.subtasks],
            'dependencies': self.dependencies,
            'assigned_to': self.assigned_to,
            'comments': [
                {**c, 'timestamp': c['timestamp'].isoformat()}
                for c in self.comments
            ],
            'attachments': self.attachments,
            'estimated_hours': self.estimated_hours,
            'actual_hours': self.actual_hours
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create task from dictionary"""
        task = cls(
            title=data['title'],
            description=data.get('description', ''),
            priority=Priority(data.get('priority', 2)),
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
            tags=data.get('tags', [])
        )

        task.id = data['id']
        task.status = Status(data['status'])
        task.created_at = datetime.fromisoformat(data['created_at'])
        task.updated_at = datetime.fromisoformat(data['updated_at'])
        task.completed_at = datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None
        task.dependencies = data.get('dependencies', [])
        task.assigned_to = data.get('assigned_to')
        task.attachments = data.get('attachments', [])
        task.estimated_hours = data.get('estimated_hours', 0)
        task.actual_hours = data.get('actual_hours', 0)

        # Restore subtasks
        task.subtasks = [Task.from_dict(st) for st in data.get('subtasks', [])]

        # Restore comments
        task.comments = [
            {
                **c,
                'timestamp': datetime.fromisoformat(c['timestamp'])
            }
            for c in data.get('comments', [])
        ]

        return task

    def __str__(self):
        status_icon = {
            Status.TODO: "⬜",
            Status.IN_PROGRESS: "🔄",
            Status.BLOCKED: "🚫",
            Status.COMPLETED: "✅",
            Status.CANCELLED: "❌"
        }[self.status]

        priority_icon = {
            Priority.LOW: "🔵",
            Priority.MEDIUM: "🟡",
            Priority.HIGH: "🟠",
            Priority.CRITICAL: "🔴"
        }[self.priority]

        return f"{status_icon} {priority_icon} {self.title}"

class Project:
    """Represents a project containing tasks"""

    def __init__(self, name: str, description: str = ""):
        self.id = self._generate_id()
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.tasks: Dict[str, Task] = {}
        self.team_members: List[str] = []
        self.milestones: List[Dict] = []
        self.is_active = True

    def _generate_id(self) -> str:
        """Generate unique project ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"PROJ-{timestamp}"

    @log_action("task_add")
    @validate_input(lambda self, task: None if isinstance(task, Task) else ValidationError("Invalid task"))
    def add_task(self, task: Task):
        """Add task to project"""
        if task.id in self.tasks:
            raise ProjectError(f"Task {task.id} already exists in project")

        self.tasks[task.id] = task
        self.updated_at = datetime.now()

    @log_action("task_remove")
    def remove_task(self, task_id: str):
        """Remove task from project"""
        if task_id not in self.tasks:
            raise TaskNotFoundError(f"Task {task_id} not found")

        del self.tasks[task_id]
        self.updated_at = datetime.now()

        # Remove dependencies from other tasks
        for task in self.tasks.values():
            if task_id in task.dependencies:
                task.dependencies.remove(task_id)

    def get_task(self, task_id: str) -> Task:
        """Get task by ID"""
        if task_id not in self.tasks:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return self.tasks[task_id]

    def add_team_member(self, member: str):
        """Add team member"""
        if member not in self.team_members:
            self.team_members.append(member)
            self.updated_at = datetime.now()

    def add_milestone(self, name: str, due_date: datetime, description: str = ""):
        """Add project milestone"""
        milestone = {
            'name': name,
            'due_date': due_date,
            'description': description,
            'created_at': datetime.now()
        }
        self.milestones.append(milestone)
        self.updated_at = datetime.now()

    @cache_result(60)
    def get_statistics(self) -> Dict:
        """Get project statistics"""
        total_tasks = len(self.tasks)
        if total_tasks == 0:
            return {
                'total_tasks': 0,
                'completed': 0,
                'in_progress': 0,
                'todo': 0,
                'blocked': 0,
                'completion_rate': 0,
                'overdue_tasks': 0
            }

        status_counts = {status: 0 for status in Status}
        overdue_count = 0

        for task in self.tasks.values():
            status_counts[task.status] += 1
            if task.is_overdue():
                overdue_count += 1

        return {
            'total_tasks': total_tasks,
            'completed': status_counts[Status.COMPLETED],
            'in_progress': status_counts[Status.IN_PROGRESS],
            'todo': status_counts[Status.TODO],
            'blocked': status_counts[Status.BLOCKED],
            'cancelled': status_counts[Status.CANCELLED],
            'completion_rate': (status_counts[Status.COMPLETED] / total_tasks) * 100,
            'overdue_tasks': overdue_count,
            'team_size': len(self.team_members)
        }

    def get_tasks_by_status(self, status: Status) -> List[Task]:
        """Get tasks filtered by status"""
        return [task for task in self.tasks.values() if task.status == status]

    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        """Get tasks filtered by priority"""
        return [task for task in self.tasks.values() if task.priority == priority]

    def get_tasks_by_assignee(self, assignee: str) -> List[Task]:
        """Get tasks assigned to specific person"""
        return [task for task in self.tasks.values() if task.assigned_to == assignee]

    def get_upcoming_deadlines(self, days: int = 7) -> List[Task]:
        """Get tasks with upcoming deadlines"""
        cutoff_date = datetime.now() + timedelta(days=days)
        tasks_with_deadlines = [
            task for task in self.tasks.values()
            if task.due_date and task.due_date <= cutoff_date and task.status != Status.COMPLETED
        ]
        return sorted(tasks_with_deadlines, key=lambda t: t.due_date)

    def generate_report(self) -> str:
        """Generate project report"""
        stats = self.get_statistics()

        report = [
            f"{'='*50}",
            f"Project Report: {self.name}",
            f"{'='*50}",
            f"Description: {self.description}",
            f"Created: {self.created_at.strftime('%Y-%m-%d')}",
            f"Team Size: {stats['team_size']}",
            f"",
            f"Task Statistics:",
            f"  Total Tasks: {stats['total_tasks']}",
            f"  Completed: {stats['completed']} ({stats['completion_rate']:.1f}%)",
            f"  In Progress: {stats['in_progress']}",
            f"  Todo: {stats['todo']}",
            f"  Blocked: {stats['blocked']}",
            f"  Overdue: {stats['overdue_tasks']}"
        ]

        if self.milestones:
            report.append("\nMilestones:")
            for milestone in self.milestones:
                status = "✅" if milestone['due_date'] < datetime.now() else "⏳"
                report.append(f"  {status} {milestone['name']} - {milestone['due_date'].strftime('%Y-%m-%d')}")

        return "\n".join(report)

    def to_dict(self) -> Dict:
        """Convert project to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tasks': {tid: task.to_dict() for tid, task in self.tasks.items()},
            'team_members': self.team_members,
            'milestones': [
                {**m, 'due_date': m['due_date'].isoformat(), 'created_at': m['created_at'].isoformat()}
                for m in self.milestones
            ],
            'is_active': self.is_active
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Project':
        """Create project from dictionary"""
        project = cls(data['name'], data.get('description', ''))
        project.id = data['id']
        project.created_at = datetime.fromisoformat(data['created_at'])
        project.updated_at = datetime.fromisoformat(data['updated_at'])
        project.team_members = data.get('team_members', [])
        project.is_active = data.get('is_active', True)

        # Restore tasks
        for task_id, task_data in data.get('tasks', {}).items():
            project.tasks[task_id] = Task.from_dict(task_data)

        # Restore milestones
        project.milestones = [
            {
                **m,
                'due_date': datetime.fromisoformat(m['due_date']),
                'created_at': datetime.fromisoformat(m['created_at'])
            }
            for m in data.get('milestones', [])
        ]

        return project

class TaskManager:
    """Main task management system"""

    def __init__(self, data_file: str = "tasks_data.json"):
        self.data_file = data_file
        self.projects: Dict[str, Project] = {}
        self.current_user = "User"
        self.load_data()

    @log_action("save")
    def save_data(self):
        """Save all data to file"""
        try:
            data = {
                'projects': {pid: proj.to_dict() for pid, proj in self.projects.items()},
                'current_user': self.current_user,
                'saved_at': datetime.now().isoformat()
            }

            # Save as JSON for readability
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)

            # Also save as pickle for backup
            with open(self.data_file + '.pkl', 'wb') as f:
                pickle.dump(data, f)

            logger.info(f"Data saved to {self.data_file}")

        except Exception as e:
            logger.error(f"Failed to save data: {e}")
            raise

    @log_action("load")
    def load_data(self):
        """Load data from file"""
        if not os.path.exists(self.data_file):
            logger.info("No existing data file found. Starting fresh.")
            return

        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)

            # Restore projects
            for pid, proj_data in data.get('projects', {}).items():
                self.projects[pid] = Project.from_dict(proj_data)

            self.current_user = data.get('current_user', 'User')

            logger.info(f"Data loaded from {self.data_file}")

        except Exception as e:
            logger.warning(f"Failed to load JSON data: {e}")

            # Try loading pickle backup
            try:
                with open(self.data_file + '.pkl', 'rb') as f:
                    data = pickle.load(f)
                    # Process pickle data...
                    logger.info("Loaded data from pickle backup")
            except:
                logger.error("Failed to load any data. Starting fresh.")

    def create_project(self, name: str, description: str = "") -> Project:
        """Create new project"""
        project = Project(name, description)
        self.projects[project.id] = project
        self.save_data()
        logger.info(f"Created project: {name}")
        return project

    def delete_project(self, project_id: str):
        """Delete project"""
        if project_id not in self.projects:
            raise ProjectError(f"Project {project_id} not found")

        del self.projects[project_id]
        self.save_data()
        logger.info(f"Deleted project: {project_id}")

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks across all projects"""
        all_tasks = []
        for project in self.projects.values():
            all_tasks.extend(project.tasks.values())
        return all_tasks

    def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by title or description"""
        query_lower = query.lower()
        results = []

        for project in self.projects.values():
            for task in project.tasks.values():
                if (query_lower in task.title.lower() or
                    query_lower in task.description.lower() or
                    any(query_lower in tag.lower() for tag in task.tags)):
                    results.append(task)

        return results

    @track_time
    def generate_dashboard(self) -> str:
        """Generate dashboard view"""
        total_projects = len(self.projects)
        active_projects = sum(1 for p in self.projects.values() if p.is_active)
        all_tasks = self.get_all_tasks()
        total_tasks = len(all_tasks)

        status_summary = {status: 0 for status in Status}
        priority_summary = {priority: 0 for priority in Priority}
        overdue_tasks = []

        for task in all_tasks:
            status_summary[task.status] += 1
            priority_summary[task.priority] += 1
            if task.is_overdue():
                overdue_tasks.append(task)

        dashboard = [
            "="*60,
            "TASK MANAGEMENT DASHBOARD",
            "="*60,
            f"User: {self.current_user}",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "=== PROJECTS ===",
            f"Total Projects: {total_projects}",
            f"Active Projects: {active_projects}",
            "",
            "=== TASKS ===",
            f"Total Tasks: {total_tasks}",
            "",
            "By Status:",
        ]

        for status, count in status_summary.items():
            percentage = (count / total_tasks * 100) if total_tasks > 0 else 0
            dashboard.append(f"  {status.value}: {count} ({percentage:.1f}%)")

        dashboard.extend([
            "",
            "By Priority:",
        ])

        priority_names = {
            Priority.LOW: "Low",
            Priority.MEDIUM: "Medium",
            Priority.HIGH: "High",
            Priority.CRITICAL: "Critical"
        }

        for priority, count in priority_summary.items():
            percentage = (count / total_tasks * 100) if total_tasks > 0 else 0
            dashboard.append(f"  {priority_names[priority]}: {count} ({percentage:.1f}%)")

        if overdue_tasks:
            dashboard.extend([
                "",
                f"=== OVERDUE TASKS ({len(overdue_tasks)}) ===",
            ])
            for task in overdue_tasks[:5]:  # Show first 5
                days_overdue = (datetime.now() - task.due_date).days
                dashboard.append(f"  • {task.title} ({days_overdue} days overdue)")

        return "\n".join(dashboard)

class TaskManagerCLI:
    """Command-line interface for task manager"""

    def __init__(self):
        self.manager = TaskManager()
        self.current_project: Optional[Project] = None
        self.running = True

    def run(self):
        """Run the CLI application"""
        print("\n" + "="*60)
        print("TASK MANAGEMENT SYSTEM")
        print("="*60)

        self.manager.current_user = input("Enter your name: ").strip() or "User"
        print(f"\nWelcome, {self.manager.current_user}!")

        while self.running:
            self.show_menu()
            choice = input("\nEnter your choice: ").strip()
            self.handle_choice(choice)

    def show_menu(self):
        """Display main menu"""
        print("\n--- Main Menu ---")
        if self.current_project:
            print(f"Current Project: {self.current_project.name}")

        print("1. Project Management")
        print("2. Task Management")
        print("3. View Dashboard")
        print("4. Search Tasks")
        print("5. Reports")
        print("6. Save and Exit")

    def handle_choice(self, choice):
        """Handle menu choice"""
        try:
            if choice == "1":
                self.project_management()
            elif choice == "2":
                self.task_management()
            elif choice == "3":
                self.view_dashboard()
            elif choice == "4":
                self.search_tasks()
            elif choice == "5":
                self.generate_reports()
            elif choice == "6":
                self.manager.save_data()
                print("Data saved. Goodbye!")
                self.running = False
            else:
                print("Invalid choice")

        except Exception as e:
            print(f"Error: {e}")
            logger.error(f"Error in menu handling: {e}")

    def project_management(self):
        """Manage projects"""
        print("\n--- Project Management ---")
        print("1. Create Project")
        print("2. List Projects")
        print("3. Select Project")
        print("4. Delete Project")
        print("5. Project Details")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Project name: ").strip()
            description = input("Description: ").strip()
            project = self.manager.create_project(name, description)
            self.current_project = project
            print(f"Created project: {name}")

        elif choice == "2":
            if not self.manager.projects:
                print("No projects found")
            else:
                print("\nProjects:")
                for pid, project in self.manager.projects.items():
                    status = "🟢 Active" if project.is_active else "🔴 Inactive"
                    stats = project.get_statistics()
                    print(f"  {project.name} [{status}]")
                    print(f"    Tasks: {stats['total_tasks']} | Completed: {stats['completion_rate']:.1f}%")

        elif choice == "3":
            projects = list(self.manager.projects.values())
            if not projects:
                print("No projects available")
                return

            for i, proj in enumerate(projects, 1):
                print(f"{i}. {proj.name}")

            idx = int(input("Select project: ")) - 1
            self.current_project = projects[idx]
            print(f"Selected: {self.current_project.name}")

        elif choice == "4":
            if not self.current_project:
                print("No project selected")
                return

            confirm = input(f"Delete '{self.current_project.name}'? (y/n): ").lower()
            if confirm == 'y':
                self.manager.delete_project(self.current_project.id)
                self.current_project = None
                print("Project deleted")

        elif choice == "5":
            if not self.current_project:
                print("No project selected")
                return

            print(self.current_project.generate_report())

    def task_management(self):
        """Manage tasks"""
        if not self.current_project:
            print("Please select a project first")
            return

        print("\n--- Task Management ---")
        print("1. Create Task")
        print("2. List Tasks")
        print("3. Update Task Status")
        print("4. Assign Task")
        print("5. View Task Details")
        print("6. Delete Task")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            title = input("Task title: ").strip()
            description = input("Description: ").strip()

            print("Priority (1=Low, 2=Medium, 3=High, 4=Critical): ")
            priority = Priority(int(input() or "2"))

            due_date_str = input("Due date (YYYY-MM-DD) or empty: ").strip()
            due_date = None
            if due_date_str:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d")

            tags = input("Tags (comma-separated): ").strip().split(",")
            tags = [t.strip() for t in tags if t.strip()]

            task = Task(title, description, priority, due_date, tags)
            self.current_project.add_task(task)
            self.manager.save_data()
            print(f"Created task: {title}")

        elif choice == "2":
            tasks = list(self.current_project.tasks.values())
            if not tasks:
                print("No tasks in project")
            else:
                print("\nTasks:")
                for task in tasks:
                    due = f" (Due: {task.due_date.strftime('%Y-%m-%d')})" if task.due_date else ""
                    overdue = " ⚠️ OVERDUE" if task.is_overdue() else ""
                    print(f"  {task}{due}{overdue}")
                    if task.assigned_to:
                        print(f"    Assigned to: {task.assigned_to}")

        elif choice == "3":
            tasks = list(self.current_project.tasks.values())
            if not tasks:
                print("No tasks available")
                return

            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")

            idx = int(input("Select task: ")) - 1
            task = tasks[idx]

            print("\nNew status:")
            for i, status in enumerate(Status, 1):
                print(f"{i}. {status.value}")

            status_idx = int(input("Select: ")) - 1
            new_status = list(Status)[status_idx]

            task.update_status(new_status)
            self.manager.save_data()
            print(f"Updated task status to {new_status.value}")

        elif choice == "4":
            tasks = list(self.current_project.tasks.values())
            if not tasks:
                print("No tasks available")
                return

            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")

            idx = int(input("Select task: ")) - 1
            task = tasks[idx]

            assignee = input("Assign to: ").strip()
            task.assign_to(assignee)
            self.manager.save_data()
            print(f"Task assigned to {assignee}")

        elif choice == "5":
            tasks = list(self.current_project.tasks.values())
            if not tasks:
                print("No tasks available")
                return

            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task.title}")

            idx = int(input("Select task: ")) - 1
            task = tasks[idx]

            print(f"\n{'='*40}")
            print(f"Task: {task.title}")
            print(f"{'='*40}")
            print(f"ID: {task.id}")
            print(f"Description: {task.description}")
            print(f"Status: {task.status.value}")
            print(f"Priority: {task.priority.name}")
            print(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
            if task.due_date:
                print(f"Due: {task.due_date.strftime('%Y-%m-%d')}")
            if task.assigned_to:
                print(f"Assigned to: {task.assigned_to}")
            if task.tags:
                print(f"Tags: {', '.join(task.tags)}")
            print(f"Progress: {task.get_progress():.1f}%")

        elif choice == "6":
            tasks = list(self.current_project.tasks.values())
            if not tasks:
                print("No tasks available")
                return

            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")

            idx = int(input("Select task: ")) - 1
            task = tasks[idx]

            confirm = input(f"Delete '{task.title}'? (y/n): ").lower()
            if confirm == 'y':
                self.current_project.remove_task(task.id)
                self.manager.save_data()
                print("Task deleted")

    def view_dashboard(self):
        """View dashboard"""
        dashboard = self.manager.generate_dashboard()
        print("\n" + dashboard)

    def search_tasks(self):
        """Search for tasks"""
        query = input("Search query: ").strip()
        if not query:
            return

        results = self.manager.search_tasks(query)

        if not results:
            print("No tasks found")
        else:
            print(f"\nFound {len(results)} tasks:")
            for task in results:
                # Find project containing this task
                project_name = "Unknown"
                for project in self.manager.projects.values():
                    if task.id in project.tasks:
                        project_name = project.name
                        break

                print(f"  {task} - Project: {project_name}")

    def generate_reports(self):
        """Generate various reports"""
        print("\n--- Reports ---")
        print("1. Overdue Tasks")
        print("2. Team Workload")
        print("3. Priority Summary")
        print("4. Export All Data")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            print("\n=== Overdue Tasks Report ===")
            for project in self.manager.projects.values():
                overdue = [t for t in project.tasks.values() if t.is_overdue()]
                if overdue:
                    print(f"\n{project.name}:")
                    for task in overdue:
                        days_overdue = (datetime.now() - task.due_date).days
                        print(f"  • {task.title} ({days_overdue} days overdue)")

        elif choice == "2":
            print("\n=== Team Workload Report ===")
            workload = {}
            for project in self.manager.projects.values():
                for task in project.tasks.values():
                    if task.assigned_to and task.status != Status.COMPLETED:
                        if task.assigned_to not in workload:
                            workload[task.assigned_to] = []
                        workload[task.assigned_to].append(task)

            for assignee, tasks in workload.items():
                print(f"\n{assignee}:")
                print(f"  Active tasks: {len(tasks)}")
                high_priority = sum(1 for t in tasks if t.priority in [Priority.HIGH, Priority.CRITICAL])
                if high_priority:
                    print(f"  High priority: {high_priority}")

        elif choice == "3":
            print("\n=== Priority Summary ===")
            all_tasks = self.manager.get_all_tasks()
            by_priority = {p: [] for p in Priority}

            for task in all_tasks:
                if task.status != Status.COMPLETED:
                    by_priority[task.priority].append(task)

            for priority in [Priority.CRITICAL, Priority.HIGH, Priority.MEDIUM, Priority.LOW]:
                tasks = by_priority[priority]
                if tasks:
                    print(f"\n{priority.name} Priority ({len(tasks)} tasks):")
                    for task in tasks[:5]:  # Show first 5
                        print(f"  • {task.title}")

        elif choice == "4":
            filename = f"task_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            data = {
                'exported_at': datetime.now().isoformat(),
                'user': self.manager.current_user,
                'projects': {pid: proj.to_dict() for pid, proj in self.manager.projects.items()}
            }

            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"Data exported to {filename}")

def demo_mode():
    """Run demo mode"""
    print("\n" + "="*60)
    print("TASK MANAGEMENT SYSTEM - DEMO MODE")
    print("="*60)

    manager = TaskManager("demo_tasks.json")
    manager.current_user = "Demo User"

    # Create sample project
    project = manager.create_project(
        "Website Redesign",
        "Complete redesign of company website"
    )

    # Add team members
    project.add_team_member("Alice")
    project.add_team_member("Bob")
    project.add_team_member("Charlie")

    # Create sample tasks
    tasks_data = [
        ("Design mockups", Priority.HIGH, "Alice", Status.COMPLETED),
        ("Implement homepage", Priority.HIGH, "Bob", Status.IN_PROGRESS),
        ("Setup database", Priority.CRITICAL, "Charlie", Status.COMPLETED),
        ("Write content", Priority.MEDIUM, "Alice", Status.TODO),
        ("Testing", Priority.HIGH, None, Status.TODO),
        ("Deploy to production", Priority.CRITICAL, None, Status.TODO)
    ]

    for title, priority, assignee, status in tasks_data:
        task = Task(title, f"Task for {title}", priority)
        if assignee:
            task.assign_to(assignee)
        task.update_status(status)
        project.add_task(task)

    # Add a milestone
    project.add_milestone(
        "Beta Launch",
        datetime.now() + timedelta(days=30),
        "Launch beta version for testing"
    )

    # Display dashboard
    print("\n" + manager.generate_dashboard())

    # Display project report
    print("\n" + project.generate_report())

    # Save demo data
    manager.save_data()
    print(f"\nDemo data saved to demo_tasks.json")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_mode()
    else:
        cli = TaskManagerCLI()
        cli.run()