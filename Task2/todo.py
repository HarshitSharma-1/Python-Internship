import json
import os
from datetime import datetime, timedelta
import sys

class TodoList:
    def __init__(self, filename="todo_data.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    self.tasks = data.get('tasks', [])
                    # Convert string dates back to datetime objects
                    for task in self.tasks:
                        if task.get('due_date'):
                            task['due_date'] = datetime.fromisoformat(task['due_date'])
            else:
                self.tasks = []
        except (json.JSONDecodeError, KeyError):
            self.tasks = []
        except Exception as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            # Convert datetime objects to strings for JSON serialization
            tasks_to_save = []
            for task in self.tasks:
                task_copy = task.copy()
                if task_copy.get('due_date') and isinstance(task_copy['due_date'], datetime):
                    task_copy['due_date'] = task_copy['due_date'].isoformat()
                tasks_to_save.append(task_copy)
            
            with open(self.filename, 'w') as file:
                json.dump({'tasks': tasks_to_save}, file, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def add_task(self, description, category="General", priority="Medium", due_date=None):
        """Add a new task to the list"""
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'category': category,
            'priority': priority,
            'completed': False,
            'created_at': datetime.now().isoformat(),
            'due_date': due_date
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"✓ Task added successfully (ID: {task['id']})")
    
    def remove_task(self, task_id):
        """Remove a task by ID"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                removed_task = self.tasks.pop(i)
                # Reassign IDs to maintain sequence
                for j in range(i, len(self.tasks)):
                    self.tasks[j]['id'] = j + 1
                self.save_tasks()
                print(f"✓ Task '{removed_task['description']}' removed successfully")
                return True
        print(f"✗ Task with ID {task_id} not found")
        return False
    
    def mark_completed(self, task_id):
        """Mark a task as completed"""
        for task in self.tasks:
            if task['id'] == task_id:
                if not task['completed']:
                    task['completed'] = True
                    task['completed_at'] = datetime.now().isoformat()
                    self.save_tasks()
                    print(f"✓ Task '{task['description']}' marked as completed")
                else:
                    print(f"ℹ Task '{task['description']}' is already completed")
                return True
        print(f"✗ Task with ID {task_id} not found")
        return False
    
    def mark_pending(self, task_id):
        """Mark a completed task as pending"""
        for task in self.tasks:
            if task['id'] == task_id:
                if task['completed']:
                    task['completed'] = False
                    task.pop('completed_at', None)
                    self.save_tasks()
                    print(f"✓ Task '{task['description']}' marked as pending")
                else:
                    print(f"ℹ Task '{task['description']}' is already pending")
                return True
        print(f"✗ Task with ID {task_id} not found")
        return False
    
    def view_tasks(self, filter_type="all", category=None):
        """View tasks with various filters"""
        if not self.tasks:
            print("No tasks found. Add some tasks to get started!")
            return
        
        filtered_tasks = self.tasks.copy()
        
        # Apply filters
        if filter_type == "completed":
            filtered_tasks = [task for task in filtered_tasks if task['completed']]
        elif filter_type == "pending":
            filtered_tasks = [task for task in filtered_tasks if not task['completed']]
        
        if category and category != "all":
            filtered_tasks = [task for task in filtered_tasks if task['category'].lower() == category.lower()]
        
        if not filtered_tasks:
            print("No tasks match the current filter")
            return
        
        # Display tasks
        print("\n" + "="*80)
        print(f"{'TO-DO LIST':^80}")
        print("="*80)
        print(f"{'ID':<4} {'Status':<10} {'Priority':<8} {'Category':<12} {'Description':<30} {'Due Date':<12}")
        print("-"*80)
        
        for task in filtered_tasks:
            status = "✓" if task['completed'] else "◯"
            priority = task['priority']
            due_date = task.get('due_date', '')
            if due_date and isinstance(due_date, str):
                due_date = datetime.fromisoformat(due_date).strftime('%Y-%m-%d')
            elif due_date and isinstance(due_date, datetime):
                due_date = due_date.strftime('%Y-%m-%d')
            
            # Color coding for priority and overdue tasks
            if task['completed']:
                status_display = f"\033[92m{status}\033[0m"  # Green
            else:
                if due_date and datetime.now().date() > datetime.fromisoformat(task.get('due_date', datetime.now().isoformat())).date():
                    status_display = f"\033[91m{status}\033[0m"  # Red for overdue
                else:
                    status_display = status
            
            if priority == "High":
                priority_display = f"\033[91m{priority}\033[0m"  # Red
            elif priority == "Medium":
                priority_display = f"\033[93m{priority}\033[0m"  # Yellow
            else:
                priority_display = f"\033[92m{priority}\033[0m"  # Green
            
            print(f"{task['id']:<4} {status_display:<10} {priority_display:<8} {task['category']:<12} {task['description'][:28]:<30} {str(due_date):<12}")
        
        print("="*80)
        print(f"Total tasks: {len(filtered_tasks)} (Pending: {len([t for t in filtered_tasks if not t['completed']])})")
    
    def get_statistics(self):
        """Display statistics about tasks"""
        if not self.tasks:
            print("No tasks available for statistics")
            return
        
        total = len(self.tasks)
        completed = len([task for task in self.tasks if task['completed']])
        pending = total - completed
        
        # Tasks by priority
        high_priority = len([task for task in self.tasks if task['priority'] == "High"])
        medium_priority = len([task for task in self.tasks if task['priority'] == "Medium"])
        low_priority = len([task for task in self.tasks if task['priority'] == "Low"])
        
        # Overdue tasks
        overdue = len([task for task in self.tasks 
                      if not task['completed'] and task.get('due_date') 
                      and datetime.now().date() > datetime.fromisoformat(task['due_date']).date()])
        
        print("\n" + "="*50)
        print("TASK STATISTICS")
        print("="*50)
        print(f"Total tasks: {total}")
        print(f"Completed: {completed} ({completed/total*100:.1f}%)")
        print(f"Pending: {pending} ({pending/total*100:.1f}%)")
        print(f"Overdue: {overdue}")
        print(f"High priority: {high_priority}")
        print(f"Medium priority: {medium_priority}")
        print(f"Low priority: {low_priority}")
        print("="*50)
    
    def clear_completed(self):
        """Remove all completed tasks"""
        completed_count = len([task for task in self.tasks if task['completed']])
        if completed_count == 0:
            print("No completed tasks to clear")
            return
        
        self.tasks = [task for task in self.tasks if not task['completed']]
        # Reassign IDs
        for i, task in enumerate(self.tasks):
            task['id'] = i + 1
        self.save_tasks()
        print(f"✓ Removed {completed_count} completed tasks")
    
    def edit_task(self, task_id, new_description=None, new_category=None, new_priority=None, new_due_date=None):
        """Edit an existing task"""
        for task in self.tasks:
            if task['id'] == task_id:
                if new_description:
                    task['description'] = new_description
                if new_category:
                    task['category'] = new_category
                if new_priority:
                    task['priority'] = new_priority
                if new_due_date:
                    task['due_date'] = new_due_date
                
                self.save_tasks()
                print(f"✓ Task ID {task_id} updated successfully")
                return True
        print(f"✗ Task with ID {task_id} not found")
        return False

def display_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("TO-DO LIST APPLICATION")
    print("="*50)
    print("1. View all tasks")
    print("2. Add new task")
    print("3. Mark task as completed")
    print("4. Mark task as pending")
    print("5. Remove task")
    print("6. Edit task")
    print("7. View completed tasks")
    print("8. View pending tasks")
    print("9. View tasks by category")
    print("10. Task statistics")
    print("11. Clear completed tasks")
    print("12. Exit")
    print("="*50)

def get_user_choice():
    """Get user choice with validation"""
    try:
        choice = input("Enter your choice (1-12): ").strip()
        return int(choice)
    except ValueError:
        return -1

def get_task_details():
    """Get task details from user"""
    description = input("Enter task description: ").strip()
    while not description:
        print("Description cannot be empty!")
        description = input("Enter task description: ").strip()
    
    print("Select category:")
    print("1. Work    2. Personal    3. Shopping    4. Health    5. Other")
    category_choice = input("Enter category (1-5) or custom category: ").strip()
    categories = {"1": "Work", "2": "Personal", "3": "Shopping", "4": "Health", "5": "Other"}
    category = categories.get(category_choice, category_choice if category_choice else "General")
    
    print("Select priority:")
    print("1. High    2. Medium    3. Low")
    priority_choice = input("Enter priority (1-3): ").strip()
    priorities = {"1": "High", "2": "Medium", "3": "Low"}
    priority = priorities.get(priority_choice, "Medium")
    
    due_date = None
    set_due_date = input("Set due date? (y/n): ").strip().lower()
    if set_due_date == 'y':
        try:
            date_str = input("Enter due date (YYYY-MM-DD): ").strip()
            due_date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Using today's date.")
            due_date = datetime.now()
    
    return description, category, priority, due_date

def main():
    """Main function to run the To-Do List application"""
    todo_list = TodoList()
    
    print("Welcome to the To-Do List Application!")
    print("Your tasks are automatically saved to 'todo_data.json'")
    
    while True:
        display_menu()
        choice = get_user_choice()
        
        if choice == 1:  # View all tasks
            todo_list.view_tasks()
        
        elif choice == 2:  # Add new task
            description, category, priority, due_date = get_task_details()
            todo_list.add_task(description, category, priority, due_date)
        
        elif choice == 3:  # Mark task as completed
            todo_list.view_tasks("pending")
            try:
                task_id = int(input("Enter task ID to mark as completed: "))
                todo_list.mark_completed(task_id)
            except ValueError:
                print("Invalid task ID!")
        
        elif choice == 4:  # Mark task as pending
            todo_list.view_tasks("completed")
            try:
                task_id = int(input("Enter task ID to mark as pending: "))
                todo_list.mark_pending(task_id)
            except ValueError:
                print("Invalid task ID!")
        
        elif choice == 5:  # Remove task
            todo_list.view_tasks()
            try:
                task_id = int(input("Enter task ID to remove: "))
                todo_list.remove_task(task_id)
            except ValueError:
                print("Invalid task ID!")
        
        elif choice == 6:  # Edit task
            todo_list.view_tasks()
            try:
                task_id = int(input("Enter task ID to edit: "))
                print("Leave blank to keep current value:")
                new_description = input("New description: ").strip()
                new_category = input("New category: ").strip()
                new_priority = input("New priority (High/Medium/Low): ").strip()
                
                new_due_date = None
                change_due_date = input("Change due date? (y/n): ").strip().lower()
                if change_due_date == 'y':
                    try:
                        date_str = input("Enter new due date (YYYY-MM-DD): ").strip()
                        new_due_date = datetime.strptime(date_str, '%Y-%m-%d')
                    except ValueError:
                        print("Invalid date format. Keeping current due date.")
                
                # Only update if new values are provided
                todo_list.edit_task(
                    task_id,
                    new_description if new_description else None,
                    new_category if new_category else None,
                    new_priority if new_priority else None,
                    new_due_date
                )
            except ValueError:
                print("Invalid task ID!")
        
        elif choice == 7:  # View completed tasks
            todo_list.view_tasks("completed")
        
        elif choice == 8:  # View pending tasks
            todo_list.view_tasks("pending")
        
        elif choice == 9:  # View tasks by category
            category = input("Enter category to filter by (or 'all' for all categories): ").strip()
            todo_list.view_tasks("all", category)
        
        elif choice == 10:  # Task statistics
            todo_list.get_statistics()
        
        elif choice == 11:  # Clear completed tasks
            confirm = input("Are you sure you want to clear all completed tasks? (y/n): ").strip().lower()
            if confirm == 'y':
                todo_list.clear_completed()
        
        elif choice == 12:  # Exit
            print("Thank you for using the To-Do List Application!")
            print("Your tasks have been saved automatically.")
            break
        
        else:
            print("Invalid choice! Please enter a number between 1 and 12.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()