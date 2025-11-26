"""
Task Manager Module
Handles todo list and task management
"""

import json
import os
from datetime import datetime
from src.display import Display

class TaskManager:
    """Manage tasks and todo list"""
    
    def __init__(self, data_file='data/tasks.json'):
        """Initialize task manager"""
        self.data_file = data_file
        self.tasks = self._load_tasks()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        os.makedirs('data', exist_ok=True)
    
    def _load_tasks(self):
        """Load tasks from JSON file"""
        self._ensure_data_directory()
        
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_tasks(self):
        """Save tasks to JSON file"""
        self._ensure_data_directory()
        
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def add_task(self, task_name, priority='medium'):
        """
        Add a new task
        
        Args:
            task_name: Name of the task
            priority: Priority level ('high', 'medium', 'low')
        """
        task = {
            'id': len(self.tasks) + 1,
            'name': task_name,
            'priority': priority,
            'completed': False,
            'created_at': datetime.now().isoformat(),
            'completed_at': None,
            'pomodoros_spent': 0
        }
        
        self.tasks.append(task)
        self._save_tasks()
        return task
    
    def get_all_tasks(self):
        """Get all tasks"""
        return self.tasks
    
    def get_pending_tasks(self):
        """Get all pending (not completed) tasks"""
        return [t for t in self.tasks if not t.get('completed', False)]
    
    def get_completed_tasks(self):
        """Get all completed tasks"""
        return [t for t in self.tasks if t.get('completed', False)]
    
    def get_task_by_index(self, index):
        """Get task by index"""
        if 0 <= index < len(self.tasks):
            return self.tasks[index]
        return None
    
    def complete_task(self, index):
        """
        Mark task as completed
        
        Args:
            index: Index of the task in the list
        """
        if 0 <= index < len(self.tasks):
            self.tasks[index]['completed'] = True
            self.tasks[index]['completed_at'] = datetime.now().isoformat()
            self._save_tasks()
            return True
        return False
    
    def uncomplete_task(self, index):
        """
        Mark task as incomplete
        
        Args:
            index: Index of the task in the list
        """
        if 0 <= index < len(self.tasks):
            self.tasks[index]['completed'] = False
            self.tasks[index]['completed_at'] = None
            self._save_tasks()
            return True
        return False
    
    def delete_task(self, index):
        """
        Delete a task
        
        Args:
            index: Index of the task in the list
        """
        if 0 <= index < len(self.tasks):
            deleted = self.tasks.pop(index)
            self._save_tasks()
            return deleted
        return None
    
    def edit_task(self, index, new_name):
        """
        Edit task name
        
        Args:
            index: Index of the task
            new_name: New name for the task
        """
        if 0 <= index < len(self.tasks):
            self.tasks[index]['name'] = new_name
            self._save_tasks()
            return True
        return False
    
    def set_priority(self, index, priority):
        """
        Set task priority
        
        Args:
            index: Index of the task
            priority: Priority level ('high', 'medium', 'low')
        """
        if 0 <= index < len(self.tasks) and priority in ['high', 'medium', 'low']:
            self.tasks[index]['priority'] = priority
            self._save_tasks()
            return True
        return False
    
    def increment_pomodoro(self, task):
        """
        Increment pomodoro count for a task
        
        Args:
            task: Task dictionary
        """
        for t in self.tasks:
            if t['id'] == task['id']:
                t['pomodoros_spent'] = t.get('pomodoros_spent', 0) + 1
                self._save_tasks()
                break
    
    def display_tasks(self):
        """Display all tasks with formatting"""
        Display.show_task_list(self.tasks)
    
    def display_tasks_detailed(self):
        """Display tasks with detailed information"""
        if not self.tasks:
            Display.show_info("No tasks yet. Add some tasks to get started!")
            return
        
        pending = self.get_pending_tasks()
        completed = self.get_completed_tasks()
        
        print(f"\n{Display.Colors.BOLD}📝 Detailed Task List{Display.Colors.ENDC}")
        Display.show_separator()
        
        if pending:
            print(f"\n{Display.Colors.YELLOW}⏳ Pending Tasks:{Display.Colors.ENDC}")
            for idx, task in enumerate(pending, 1):
                priority_color = {
                    'high': Display.Colors.RED,
                    'medium': Display.Colors.YELLOW,
                    'low': Display.Colors.GREEN
                }.get(task.get('priority', 'medium'), Display.Colors.YELLOW)
                
                priority_icon = {
                    'high': '🔴',
                    'medium': '🟡',
                    'low': '🟢'
                }.get(task.get('priority', 'medium'), '🟡')
                
                pomodoros = task.get('pomodoros_spent', 0)
                created = datetime.fromisoformat(task['created_at']).strftime('%Y-%m-%d')
                
                print(f"\n  {idx}. {priority_icon} {task['name']}")
                print(f"     Priority: {priority_color}{task.get('priority', 'medium').upper()}{Display.Colors.ENDC}")
                print(f"     Pomodoros: 🍅 {pomodoros}")
                print(f"     Created: {created}")
        
        if completed:
            print(f"\n{Display.Colors.GREEN}✅ Completed Tasks:{Display.Colors.ENDC}")
            for idx, task in enumerate(completed, 1):
                pomodoros = task.get('pomodoros_spent', 0)
                completed_date = datetime.fromisoformat(task['completed_at']).strftime('%Y-%m-%d')
                
                print(f"\n  {idx}. ✓ {task['name']}")
                print(f"     Pomodoros: 🍅 {pomodoros}")
                print(f"     Completed: {completed_date}")
        
        Display.show_separator()
        print(f"\nTotal: {len(self.tasks)} tasks ({len(pending)} pending, {len(completed)} completed)")
    
    def get_task_stats(self):
        """Get task statistics"""
        total = len(self.tasks)
        pending = len(self.get_pending_tasks())
        completed = len(self.get_completed_tasks())
        
        total_pomodoros = sum(t.get('pomodoros_spent', 0) for t in self.tasks)
        
        return {
            'total': total,
            'pending': pending,
            'completed': completed,
            'completion_rate': (completed / total * 100) if total > 0 else 0,
            'total_pomodoros': total_pomodoros
        }
    
    def clear_completed_tasks(self):
        """Remove all completed tasks"""
        self.tasks = [t for t in self.tasks if not t.get('completed', False)]
        self._save_tasks()
    
    def clear_all_tasks(self):
        """Clear all tasks (use with caution!)"""
        self.tasks = []
        self._save_tasks()
    
    def export_tasks(self, filename='tasks_export.json'):
        """Export tasks to file"""
        self._ensure_data_directory()
        
        export_data = {
            'exported_at': datetime.now().isoformat(),
            'total_tasks': len(self.tasks),
            'tasks': self.tasks,
            'stats': self.get_task_stats()
        }
        
        filepath = f"data/{filename}"
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filepath
    
    def search_tasks(self, keyword):
        """
        Search tasks by keyword
        
        Args:
            keyword: Search keyword
        """
        keyword = keyword.lower()
        return [
            t for t in self.tasks
            if keyword in t['name'].lower()
        ]
    
    def sort_tasks_by_priority(self):
        """Sort tasks by priority (high -> medium -> low)"""
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        self.tasks.sort(key=lambda x: (
            x.get('completed', False),
            priority_order.get(x.get('priority', 'medium'), 1)
        ))
        self._save_tasks()
    
    def sort_tasks_by_date(self):
        """Sort tasks by creation date (newest first)"""
        self.tasks.sort(
            key=lambda x: x.get('created_at', ''),
            reverse=True
        )
        self._save_tasks()