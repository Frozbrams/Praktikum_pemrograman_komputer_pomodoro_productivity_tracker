# 🍅 Pomodoro CLI Timer

A powerful command-line Pomodoro timer with task management and productivity tracking. Stay focused, track your progress, and boost your productivity!

## ✨ Features

### Core Features
- ⏱️ **Pomodoro Timer** - Classic 25-minute work sessions with breaks
- 📝 **Task Management** - Built-in todo list with priority levels
- 📊 **Statistics Tracking** - Track your productivity over time
- 🔔 **System Notifications** - Get notified when sessions start/end
- ⚙️ **Customizable Settings** - Adjust timer durations to your preference

### Advanced Features
- 🎯 Work on specific tasks during pomodoro sessions
- 📈 View daily, weekly, and all-time statistics
- 🔥 Track your productivity streak
- 🏆 See your most productive day
- 📋 Priority system for tasks (high, medium, low)
- 💾 Auto-save all data (tasks and sessions)
- 🎨 Colorful CLI interface

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- No external dependencies required!

### Installation

1. **Clone or download this repository**
```bash
git clone <repository-url>
cd pomodoro-cli
```

2. **Run the application**
```bash
python main.py
```

That's it! No installation of external libraries needed.

### Optional Dependencies

For enhanced features (notifications on Windows):
```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```
pomodoro-cli/
│
├── main.py                     # Main application entry point
├── requirements.txt            # Python dependencies (optional)
├── README.md                   # This file
│
├── src/                        # Source code
│   ├── __init__.py            # Package initialization
│   ├── timer.py               # Pomodoro timer logic
│   ├── task_manager.py        # Task management
│   ├── stats.py               # Statistics tracking
│   ├── display.py             # CLI display & formatting
│   └── notifier.py            # System notifications
│
├── data/                       # Data storage (auto-created)
│   ├── tasks.json             # Tasks database
│   └── sessions.json          # Pomodoro sessions history
│
└── assets/                     # Media files (optional)
    └── sounds/                # Custom notification sounds
```

## 🎮 Usage

### Main Menu Options

When you run the application, you'll see:

```
╔═══════════════════════════════════════╗
║     🍅 POMODORO CLI TIMER 🍅         ║
║      Stay Focused, Stay Productive    ║
╚═══════════════════════════════════════╝

📋 MAIN MENU
========================================
1. Start Pomodoro Timer
2. Manage Tasks
3. View Statistics
4. Settings
5. Exit
========================================
```

### 1. Start Pomodoro Timer

- Select a task to work on (or work without a specific task)
- Timer starts for 25 minutes (default)
- Get notified when time's up
- Automatic break scheduling (5-min short breaks, 15-min long breaks)
- Press `Ctrl+C` to pause/stop anytime

### 2. Manage Tasks

**Add tasks:**
- Enter task name and it's added to your list

**View tasks:**
- See all pending and completed tasks
- Tasks show with priority indicators (🔴 High, 🟡 Medium, 🟢 Low)

**Complete tasks:**
- Mark tasks as done when finished

**Delete tasks:**
- Remove tasks you no longer need

### 3. View Statistics

See your productivity metrics:
- **Today's stats** - Pomodoros completed and focus time
- **This week** - Weekly productivity overview
- **All time** - Total statistics since you started
- **Streak** - Consecutive days with at least one pomodoro
- **Best day** - Your most productive day ever
- **Top tasks** - Which tasks you've worked on most

### 4. Settings

Customize timer durations:
- **Pomodoro duration** (default: 25 minutes)
- **Short break** (default: 5 minutes)
- **Long break** (default: 15 minutes)
- **Reset to defaults** anytime

## 🎯 Pomodoro Technique

The Pomodoro Technique is a time management method that uses a timer to break work into intervals:

1. **Work for 25 minutes** (1 Pomodoro)
2. **Take a 5-minute break**
3. **Repeat 4 times**
4. **Take a longer 15-30 minute break**

### Benefits:
- ✅ Improved focus and concentration
- ✅ Reduced mental fatigue
- ✅ Better time management
- ✅ Increased productivity
- ✅ Reduced procrastination

## 📊 Data Storage

All your data is stored locally in JSON files:

- `data/tasks.json` - Your task list
- `data/sessions.json` - Pomodoro session history

These files are created automatically when you first use the app.

### Backup Your Data

Simply copy the `data/` folder to backup your tasks and statistics!

## ⌨️ Keyboard Shortcuts

- `Ctrl+C` - Pause/stop timer
- `Enter` - Confirm selections
- Number keys - Select menu options

## 🎨 Features in Detail

### Task Priority System

Organize tasks by importance:
- 🔴 **High priority** - Urgent and important tasks
- 🟡 **Medium priority** - Regular tasks
- 🟢 **Low priority** - Nice-to-have tasks

### Statistics Dashboard

Track your productivity with:
- Daily pomodoro count
- Weekly trends
- Total focus time
- Productivity streaks
- Most productive day
- Task completion rates

### Cross-Platform Notifications

Works on:
- ✅ Windows (native notifications)
- ✅ macOS (notification center)
- ✅ Linux (notify-send)

### Colored CLI Output

Beautiful terminal colors:
- 🟢 Green - Success messages
- 🔴 Red - Errors
- 🟡 Yellow - Warnings
- 🔵 Blue - Information
- 🟣 Cyan - Headers and timers

## 🛠️ Troubleshooting

### Colors not showing on Windows?
Install colorama:
```bash
pip install colorama
```

### Notifications not working on Windows?
Install plyer:
```bash
pip install plyer
```

### Can't create data folder?
Make sure you have write permissions in the project directory.

## 📝 Tips for Maximum Productivity

1. **Plan your tasks** - Add all tasks before starting
2. **Set priorities** - Focus on high-priority tasks first
3. **No multitasking** - One task per pomodoro
4. **Take breaks seriously** - Don't skip them!
5. **Track consistently** - Use it every day to build habits
6. **Review your stats** - Learn from your productivity patterns

## 🤝 Contributing

This is a college project, but suggestions and improvements are welcome!

## 📄 License

This project is created for educational purposes.

## 👨‍💻 Author

Created as a college project for learning Python programming.

## 🙏 Acknowledgments

- Francesco Cirillo - Creator of the Pomodoro Technique
- Python community for excellent documentation
- All productivity enthusiasts!

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section
2. Make sure you're using Python 3.6+
3. Verify file permissions for the `data/` directory

---

**Stay focused, stay productive! 🍅✨**

*"The Pomodoro Technique is a powerful tool for managing time and achieving goals."*