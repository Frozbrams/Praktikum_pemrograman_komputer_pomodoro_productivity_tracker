"""
Pomodoro CLI Package
A command-line Pomodoro timer for productivity tracking
"""

__version__ = '1.0.0'
__author__ = 'Your Name'
__description__ = 'A CLI-based Pomodoro timer with task management and statistics tracking'

# Import main components for easier access
from src.timer import PomodoroTimer
from src.task_manager import TaskManager
from src.stats import Stats
from src.display import Display
from src.notifier import Notifier

__all__ = [
    'PomodoroTimer',
    'TaskManager',
    'Stats',
    'Display',
    'Notifier'
]