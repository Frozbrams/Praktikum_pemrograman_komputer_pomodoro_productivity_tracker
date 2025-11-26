"""
Display Module
Handles all CLI formatting and colored output
"""

class Colors:
    """ANSI color codes for terminal"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Display:
    """Display utility class for pretty CLI output"""
    
    @staticmethod
    def show_header():
        """Display application header"""
        header = f"""
{Colors.CYAN}{Colors.BOLD}
==========================================
     POMODORO CLI TIMER
     Stay Focused, Stay Productive
==========================================
{Colors.ENDC}"""
        print(header)
    
    @staticmethod
    def show_success(message):
        """Display success message in green"""
        print(f"{Colors.GREEN}✓ {message}{Colors.ENDC}")
    
    @staticmethod
    def show_error(message):
        """Display error message in red"""
        print(f"{Colors.RED}✗ {message}{Colors.ENDC}")
    
    @staticmethod
    def show_warning(message):
        """Display warning message in yellow"""
        print(f"{Colors.YELLOW}⚠ {message}{Colors.ENDC}")
    
    @staticmethod
    def show_info(message):
        """Display info message in blue"""
        print(f"{Colors.BLUE}ℹ {message}{Colors.ENDC}")
    
    @staticmethod
    def show_separator(length=40):
        """Display separator line"""
        print("=" * length)
    
    @staticmethod
    def show_progress_bar(current, total, length=30):
        """
        Display progress bar
        
        Args:
            current: Current progress value
            total: Total/max value
            length: Length of progress bar
        """
        filled = int(length * current / total)
        bar = '█' * filled + '░' * (length - filled)
        percentage = (current / total) * 100
        print(f"{Colors.CYAN}[{bar}] {percentage:.1f}%{Colors.ENDC}")
    
    @staticmethod
    def show_timer_display(time_str, message=""):
        """
        Display large timer
        
        Args:
            time_str: Time string in MM:SS format
            message: Optional message to display
        """
        print(f"""
{Colors.BOLD}{Colors.CYAN}
    ╔═══════════════╗
    ║   {time_str}   ║
    ╚═══════════════╝
{Colors.ENDC}""")
        if message:
            print(f"{Colors.YELLOW}{message}{Colors.ENDC}")
    
    @staticmethod
    def show_task_list(tasks):
        """
        Display formatted task list
        
        Args:
            tasks: List of task dictionaries
        """
        if not tasks:
            Display.show_info("No tasks yet. Add some tasks to get started!")
            return
        
        print(f"\n{Colors.BOLD}📝 Your Tasks:{Colors.ENDC}")
        Display.show_separator()
        
        pending = [t for t in tasks if not t.get('completed', False)]
        completed = [t for t in tasks if t.get('completed', False)]
        
        if pending:
            print(f"\n{Colors.YELLOW}⏳ Pending:{Colors.ENDC}")
            for idx, task in enumerate(pending, 1):
                print(f"  {idx}. ☐ {task['name']}")
        
        if completed:
            print(f"\n{Colors.GREEN}✓ Completed:{Colors.ENDC}")
            for idx, task in enumerate(completed, 1):
                print(f"  {idx}. ☑ {task['name']}")
        
        Display.show_separator()
        print(f"\nTotal: {len(tasks)} tasks ({len(pending)} pending, {len(completed)} completed)")
    
    @staticmethod
    def show_stats_summary(stats_data):
        """
        Display statistics summary
        
        Args:
            stats_data: Dictionary containing statistics
        """
        print(f"\n{Colors.BOLD}{Colors.CYAN}📊 PRODUCTIVITY STATISTICS{Colors.ENDC}")
        Display.show_separator()
        
        # Today's stats
        print(f"\n{Colors.BOLD}Today:{Colors.ENDC}")
        print(f"  🍅 Pomodoros completed: {Colors.GREEN}{stats_data.get('today_pomodoros', 0)}{Colors.ENDC}")
        print(f"  ⏱️  Focus time: {Colors.CYAN}{stats_data.get('today_focus_time', '0h 0m')}{Colors.ENDC}")
        
        # This week
        print(f"\n{Colors.BOLD}This Week:{Colors.ENDC}")
        print(f"  🍅 Pomodoros completed: {Colors.GREEN}{stats_data.get('week_pomodoros', 0)}{Colors.ENDC}")
        print(f"  ⏱️  Focus time: {Colors.CYAN}{stats_data.get('week_focus_time', '0h 0m')}{Colors.ENDC}")
        
        # All time
        print(f"\n{Colors.BOLD}All Time:{Colors.ENDC}")
        print(f"  🍅 Total pomodoros: {Colors.GREEN}{stats_data.get('total_pomodoros', 0)}{Colors.ENDC}")
        print(f"  ⏱️  Total focus time: {Colors.CYAN}{stats_data.get('total_focus_time', '0h 0m')}{Colors.ENDC}")
        print(f"  🔥 Current streak: {Colors.YELLOW}{stats_data.get('streak', 0)} days{Colors.ENDC}")
        
        # Most productive day
        if stats_data.get('best_day'):
            print(f"\n{Colors.BOLD}Best Day:{Colors.ENDC}")
            print(f"  📅 {stats_data['best_day']['date']}")
            print(f"  🍅 {stats_data['best_day']['pomodoros']} pomodoros")
        
        Display.show_separator()
    
    @staticmethod
    def show_ascii_tomato():
        """Display ASCII art tomato"""
        tomato = f"""{Colors.RED}
            _
           ( )
         .-'-'-.
        /       \\
       |  🍅    |
        \\       /
         '-._.-'
{Colors.ENDC}"""
        print(tomato)
    
    @staticmethod
    def clear_line():
        """Clear current line in terminal"""
        print('\r' + ' ' * 80 + '\r', end='')
    
    @staticmethod
    def show_celebration():
        """Display celebration message"""
        celebration = f"""{Colors.GREEN}{Colors.BOLD}
    ✨ ★ ✨ ★ ✨ ★ ✨ ★ ✨
         🎉 AWESOME! 🎉
    You completed a Pomodoro!
    ✨ ★ ✨ ★ ✨ ★ ✨ ★ ✨
{Colors.ENDC}"""
        print(celebration)