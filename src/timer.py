"""
Pomodoro Timer
Handles the core timer logic and session management
"""

import time
import os
from datetime import datetime
from src.notifier import Notifier
from src.display import Display
from src.stats import Stats

class PomodoroTimer:
    def __init__(self):
        """Initialize timer with default durations"""
        self.pomodoro_duration = 25 * 60  # 25 minutes in seconds
        self.short_break_duration = 5 * 60  # 5 minutes
        self.long_break_duration = 15 * 60  # 15 minutes
        self.pomodoros_until_long_break = 4
        
        self.current_pomodoros = 0
        self.notifier = Notifier()
        self.stats = Stats()
        
    def reset_to_default(self):
        """Reset timer settings to default values"""
        self.pomodoro_duration = 25 * 60
        self.short_break_duration = 5 * 60
        self.long_break_duration = 15 * 60
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def format_time(self, seconds):
        """Convert seconds to MM:SS format"""
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"
    
    def countdown(self, duration, session_type, task=None):
        """
        Run countdown timer with live display
        
        Args:
            duration: Duration in seconds
            session_type: 'pomodoro', 'short_break', or 'long_break'
            task: Optional task being worked on
        """
        start_time = datetime.now()
        end_time = time.time() + duration
        
        while time.time() < end_time:
            remaining = int(end_time - time.time())
            
            # Display timer
            self.clear_screen()
            Display.show_header()
            
            if session_type == 'pomodoro':
                print("\n🍅 POMODORO SESSION")
                print("=" * 40)
                if task:
                    print(f"📝 Working on: {task['name']}")
            elif session_type == 'short_break':
                print("\n☕ SHORT BREAK")
                print("=" * 40)
                print("Take a quick rest!")
            else:
                print("\n🌟 LONG BREAK")
                print("=" * 40)
                print("Great job! Take a longer break!")
            
            print(f"\n⏱️  Time remaining: {self.format_time(remaining)}")
            print(f"⏰ Started at: {start_time.strftime('%H:%M:%S')}")
            print(f"🎯 Pomodoros completed today: {self.current_pomodoros}")
            
            print("\n" + "=" * 40)
            print("Press Ctrl+C to pause/stop")
            
            time.sleep(1)
        
        # Timer finished
        return True
    
    def start_pomodoro(self, task=None):
        """
        Start a complete pomodoro cycle
        
        Args:
            task: Optional task to work on
        """
        try:
            # Pomodoro session
            self.notifier.notify("Pomodoro Started!", "Time to focus! 🍅")
            completed = self.countdown(self.pomodoro_duration, 'pomodoro', task)
            
            if completed:
                self.current_pomodoros += 1
                
                # Save session to stats
                self.stats.add_session({
                    'type': 'pomodoro',
                    'task': task['name'] if task else 'General work',
                    'duration': self.pomodoro_duration,
                    'completed': True,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Celebration message
                self.clear_screen()
                Display.show_header()
                Display.show_success("\n🎉 Pomodoro Complete!")
                print(f"\nYou've completed {self.current_pomodoros} pomodoro(s) today!")
                
                self.notifier.notify("Pomodoro Complete!", "Great work! Time for a break! 🎉")
                
                # Determine break type
                if self.current_pomodoros % self.pomodoros_until_long_break == 0:
                    print("\nTime for a LONG BREAK! 🌟")
                    input("\nPress ENTER to start long break...")
                    self.start_break('long')
                else:
                    print("\nTime for a short break! ☕")
                    input("\nPress ENTER to start short break...")
                    self.start_break('short')
                
                # Ask for another pomodoro
                print("\n" + "=" * 40)
                choice = input("\nStart another pomodoro? (y/n): ").strip().lower()
                if choice == 'y':
                    self.start_pomodoro(task)
                    
        except KeyboardInterrupt:
            # Handle manual stop
            self.clear_screen()
            Display.show_header()
            print("\n⏸️  Timer paused!")
            choice = input("\nDo you want to mark this session as complete? (y/n): ").strip().lower()
            
            if choice == 'y':
                self.current_pomodoros += 1
                self.stats.add_session({
                    'type': 'pomodoro',
                    'task': task['name'] if task else 'General work',
                    'duration': self.pomodoro_duration,
                    'completed': True,
                    'timestamp': datetime.now().isoformat()
                })
                Display.show_success("Session marked as complete!")
            else:
                Display.show_error("Session cancelled.")
            
            input("\nPress ENTER to return to menu...")
    
    def start_break(self, break_type='short'):
        """
        Start break session
        
        Args:
            break_type: 'short' or 'long'
        """
        try:
            duration = self.short_break_duration if break_type == 'short' else self.long_break_duration
            session_type = 'short_break' if break_type == 'short' else 'long_break'
            
            completed = self.countdown(duration, session_type)
            
            if completed:
                self.clear_screen()
                Display.show_header()
                Display.show_success("\n✅ Break Complete!")
                print("\nTime to get back to work! 💪")
                self.notifier.notify("Break Over!", "Ready for another pomodoro? 🍅")
                input("\nPress ENTER to continue...")
                
        except KeyboardInterrupt:
            self.clear_screen()
            Display.show_header()
            Display.show_error("\n⏸️  Break interrupted!")
            input("\nPress ENTER to return to menu...")
    
    def get_stats_summary(self):
        """Get current session statistics"""
        return {
            'pomodoros_today': self.current_pomodoros,
            'next_break': 'long' if self.current_pomodoros % self.pomodoros_until_long_break == 0 else 'short'
        }