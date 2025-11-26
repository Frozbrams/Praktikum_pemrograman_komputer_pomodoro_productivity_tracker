"""
Pomodoro CLI - Productivity Timer
Main entry point for the application
"""

# Set UTF-8 encoding FIRST before any other imports
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import sys
from src.display import Display
from src.timer import PomodoroTimer
from src.task_manager import TaskManager
from src.stats import Stats

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    """Display main menu"""
    Display.show_header()
    print("\nMAIN MENU")
    print("=" * 40)
    print("1. Start Pomodoro Timer")
    print("2. Manage Tasks")
    print("3. View Statistics")
    print("4. Settings")
    print("5. Exit")
    print("=" * 40)

def start_timer_menu(timer, task_manager):
    """Start pomodoro timer with task selection"""
    clear_screen()
    Display.show_header()
    
    # Show pending tasks
    tasks = task_manager.get_pending_tasks()
    if tasks:
        print("\nYour Tasks:")
        for idx, task in enumerate(tasks, 1):
            print(f"{idx}. {task['name']}")
        print(f"{len(tasks) + 1}. Work without specific task")
        
        try:
            choice = int(input("\nSelect task to work on (or enter number): "))
            if 1 <= choice <= len(tasks):
                selected_task = tasks[choice - 1]
                print(f"\nWorking on: {selected_task['name']}")
            else:
                selected_task = None
        except:
            selected_task = None
    else:
        print("\nNo tasks yet. Starting general pomodoro session.")
        selected_task = None
    
    # Start timer
    input("\nPress ENTER to start timer...")
    timer.start_pomodoro(selected_task)

def manage_tasks_menu(task_manager):
    """Task management menu"""
    while True:
        clear_screen()
        Display.show_header()
        print("\nTASK MANAGEMENT")
        print("=" * 40)
        print("1. View All Tasks")
        print("2. Add New Task")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Back to Main Menu")
        print("=" * 40)
        
        choice = input("\nChoose option: ").strip()
        
        if choice == "1":
            task_manager.display_tasks()
            input("\nPress ENTER to continue...")
        elif choice == "2":
            task_name = input("\nEnter task name: ").strip()
            if task_name:
                task_manager.add_task(task_name)
                Display.show_success("Task added successfully!")
            else:
                Display.show_error("Task name cannot be empty!")
            input("Press ENTER to continue...")
        elif choice == "3":
            task_manager.display_tasks()
            try:
                task_id = int(input("\nEnter task number to complete: "))
                task_manager.complete_task(task_id - 1)
                Display.show_success("Task marked as complete!")
            except:
                Display.show_error("Invalid task number!")
            input("Press ENTER to continue...")
        elif choice == "4":
            task_manager.display_tasks()
            try:
                task_id = int(input("\nEnter task number to delete: "))
                task_manager.delete_task(task_id - 1)
                Display.show_success("Task deleted!")
            except:
                Display.show_error("Invalid task number!")
            input("Press ENTER to continue...")
        elif choice == "5":
            break

def view_stats_menu(stats):
    """Display statistics menu"""
    clear_screen()
    Display.show_header()
    stats.display_stats()
    input("\nPress ENTER to continue...")

def settings_menu(timer):
    """Settings menu for customizing timer durations"""
    while True:
        clear_screen()
        Display.show_header()
        print("\nSETTINGS")
        print("=" * 40)
        print(f"1. Pomodoro Duration (current: {timer.pomodoro_duration // 60} min)")
        print(f"2. Short Break Duration (current: {timer.short_break_duration // 60} min)")
        print(f"3. Long Break Duration (current: {timer.long_break_duration // 60} min)")
        print("4. Reset to Default")
        print("5. Back to Main Menu")
        print("=" * 40)
        
        choice = input("\nChoose option: ").strip()
        
        if choice == "1":
            try:
                minutes = int(input("Enter pomodoro duration (minutes): "))
                timer.pomodoro_duration = minutes * 60
                Display.show_success("Pomodoro duration updated!")
            except:
                Display.show_error("Invalid input!")
            input("Press ENTER to continue...")
        elif choice == "2":
            try:
                minutes = int(input("Enter short break duration (minutes): "))
                timer.short_break_duration = minutes * 60
                Display.show_success("Short break duration updated!")
            except:
                Display.show_error("Invalid input!")
            input("Press ENTER to continue...")
        elif choice == "3":
            try:
                minutes = int(input("Enter long break duration (minutes): "))
                timer.long_break_duration = minutes * 60
                Display.show_success("Long break duration updated!")
            except:
                Display.show_error("Invalid input!")
            input("Press ENTER to continue...")
        elif choice == "4":
            timer.reset_to_default()
            Display.show_success("Settings reset to default!")
            input("Press ENTER to continue...")
        elif choice == "5":
            break

def main():
    """Main application loop"""
    # Initialize components
    timer = PomodoroTimer()
    task_manager = TaskManager()
    stats = Stats()
    
    # Main loop
    while True:
        clear_screen()
        show_menu()
        
        choice = input("\nChoose option: ").strip()
        
        if choice == "1":
            start_timer_menu(timer, task_manager)
        elif choice == "2":
            manage_tasks_menu(task_manager)
        elif choice == "3":
            view_stats_menu(stats)
        elif choice == "4":
            settings_menu(timer)
        elif choice == "5":
            clear_screen()
            Display.show_success("Thank you for using Pomodoro CLI! Stay productive!")
            sys.exit(0)
        else:
            Display.show_error("Invalid option! Please choose 1-5.")
            input("Press ENTER to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        Display.show_success("\n\nGoodbye!")
        sys.exit(0) 