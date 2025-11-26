"""
Statistics Module
Tracks and displays productivity statistics
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
from src.display import Display

class Stats:
    """Manage and display productivity statistics"""
    
    def __init__(self, data_file='data/sessions.json'):
        """Initialize stats manager"""
        self.data_file = data_file
        self.sessions = self._load_sessions()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        os.makedirs('data', exist_ok=True)
    
    def _load_sessions(self):
        """Load sessions from JSON file"""
        self._ensure_data_directory()
        
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_sessions(self):
        """Save sessions to JSON file"""
        self._ensure_data_directory()
        
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.sessions, f, indent=2)
        except Exception as e:
            print(f"Error saving sessions: {e}")
    
    def add_session(self, session_data):
        """
        Add a new session to statistics
        
        Args:
            session_data: Dictionary containing session info
        """
        self.sessions.append(session_data)
        self._save_sessions()
    
    def get_today_sessions(self):
        """Get sessions from today"""
        today = datetime.now().date()
        return [
            s for s in self.sessions
            if datetime.fromisoformat(s['timestamp']).date() == today
        ]
    
    def get_week_sessions(self):
        """Get sessions from this week"""
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        return [
            s for s in self.sessions
            if datetime.fromisoformat(s['timestamp']).date() >= week_start
        ]
    
    def get_pomodoro_count(self, sessions):
        """Count completed pomodoros in sessions"""
        return sum(
            1 for s in sessions
            if s.get('type') == 'pomodoro' and s.get('completed', False)
        )
    
    def get_total_focus_time(self, sessions):
        """Calculate total focus time from sessions"""
        total_seconds = sum(
            s.get('duration', 0) for s in sessions
            if s.get('type') == 'pomodoro' and s.get('completed', False)
        )
        
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    
    def get_streak(self):
        """Calculate current daily streak"""
        if not self.sessions:
            return 0
        
        # Get all unique dates with pomodoros
        dates = set()
        for session in self.sessions:
            if session.get('type') == 'pomodoro' and session.get('completed', False):
                date = datetime.fromisoformat(session['timestamp']).date()
                dates.add(date)
        
        if not dates:
            return 0
        
        # Sort dates
        sorted_dates = sorted(dates, reverse=True)
        
        # Calculate streak from today
        today = datetime.now().date()
        streak = 0
        current_date = today
        
        for date in sorted_dates:
            if date == current_date:
                streak += 1
                current_date -= timedelta(days=1)
            elif date == current_date:
                continue
            else:
                break
        
        return streak
    
    def get_best_day(self):
        """Get the most productive day"""
        if not self.sessions:
            return None
        
        # Group pomodoros by date
        daily_counts = defaultdict(int)
        for session in self.sessions:
            if session.get('type') == 'pomodoro' and session.get('completed', False):
                date = datetime.fromisoformat(session['timestamp']).date()
                daily_counts[date] += 1
        
        if not daily_counts:
            return None
        
        # Find best day
        best_date = max(daily_counts, key=daily_counts.get)
        return {
            'date': best_date.strftime('%A, %B %d, %Y'),
            'pomodoros': daily_counts[best_date]
        }
    
    def get_task_stats(self):
        """Get statistics by task"""
        task_stats = defaultdict(lambda: {'count': 0, 'time': 0})
        
        for session in self.sessions:
            if session.get('type') == 'pomodoro' and session.get('completed', False):
                task = session.get('task', 'General work')
                task_stats[task]['count'] += 1
                task_stats[task]['time'] += session.get('duration', 0)
        
        return dict(task_stats)
    
    def display_stats(self):
        """Display formatted statistics"""
        today_sessions = self.get_today_sessions()
        week_sessions = self.get_week_sessions()
        all_sessions = self.sessions
        
        stats_data = {
            'today_pomodoros': self.get_pomodoro_count(today_sessions),
            'today_focus_time': self.get_total_focus_time(today_sessions),
            'week_pomodoros': self.get_pomodoro_count(week_sessions),
            'week_focus_time': self.get_total_focus_time(week_sessions),
            'total_pomodoros': self.get_pomodoro_count(all_sessions),
            'total_focus_time': self.get_total_focus_time(all_sessions),
            'streak': self.get_streak(),
            'best_day': self.get_best_day()
        }
        
        Display.show_stats_summary(stats_data)
        
        # Show task breakdown
        task_stats = self.get_task_stats()
        if task_stats:
            print(f"\n📊 Top Tasks:")
            Display.show_separator()
            
            # Sort by count
            sorted_tasks = sorted(
                task_stats.items(),
                key=lambda x: x[1]['count'],
                reverse=True
            )[:5]  # Top 5
            
            for task, data in sorted_tasks:
                hours = data['time'] // 3600
                minutes = (data['time'] % 3600) // 60
                time_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
                print(f"  🍅 {task}: {data['count']} pomodoros ({time_str})")
            
            Display.show_separator()
    
    def export_stats(self, filename='stats_export.json'):
        """Export statistics to file"""
        self._ensure_data_directory()
        
        export_data = {
            'exported_at': datetime.now().isoformat(),
            'total_sessions': len(self.sessions),
            'sessions': self.sessions,
            'summary': {
                'total_pomodoros': self.get_pomodoro_count(self.sessions),
                'total_focus_time': self.get_total_focus_time(self.sessions),
                'streak': self.get_streak(),
                'best_day': self.get_best_day()
            }
        }
        
        filepath = f"data/{filename}"
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filepath
    
    def clear_all_stats(self):
        """Clear all statistics (use with caution!)"""
        self.sessions = []
        self._save_sessions()
    
    def get_weekly_chart(self):
        """Get data for weekly activity chart"""
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        
        # Initialize daily counts
        daily_data = {
            (week_start + timedelta(days=i)).strftime('%A'): 0
            for i in range(7)
        }
        
        # Count pomodoros per day
        for session in self.sessions:
            if session.get('type') == 'pomodoro' and session.get('completed', False):
                date = datetime.fromisoformat(session['timestamp']).date()
                if date >= week_start:
                    day_name = date.strftime('%A')
                    if day_name in daily_data:
                        daily_data[day_name] += 1
        
        return daily_data
    
    def display_weekly_chart(self):
        """Display ASCII chart of weekly activity"""
        data = self.get_weekly_chart()
        max_pomodoros = max(data.values()) if data.values() else 1
        
        print("\n📊 This Week's Activity:")
        Display.show_separator()
        
        for day, count in data.items():
            bar_length = int((count / max_pomodoros) * 20) if max_pomodoros > 0 else 0
            bar = '█' * bar_length
            print(f"{day[:3]}: {bar} {count}")
        
        Display.show_separator()