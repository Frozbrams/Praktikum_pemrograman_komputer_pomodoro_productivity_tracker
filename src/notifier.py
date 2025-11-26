"""
Notifier Module
Handles system notifications and alert sounds
"""

import platform
import subprocess
import os

class Notifier:
    """Handle system notifications across different platforms"""
    
    def __init__(self):
        """Initialize notifier and detect platform"""
        self.system = platform.system()
        self.sound_enabled = True
    
    def notify(self, title, message):
        """
        Send system notification
        
        Args:
            title: Notification title
            message: Notification message
        """
        try:
            if self.system == "Darwin":  # macOS
                self._notify_macos(title, message)
            elif self.system == "Linux":
                self._notify_linux(title, message)
            elif self.system == "Windows":
                self._notify_windows(title, message)
            else:
                # Fallback: print to console
                print(f"\n🔔 {title}: {message}")
        except Exception as e:
            # If notification fails, just print
            print(f"\n🔔 {title}: {message}")
    
    def _notify_macos(self, title, message):
        """Send notification on macOS"""
        script = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", script], check=False)
        if self.sound_enabled:
            os.system("afplay /System/Library/Sounds/Glass.aiff &")
    
    def _notify_linux(self, title, message):
        """Send notification on Linux"""
        try:
            subprocess.run(
                ["notify-send", title, message],
                check=False
            )
            if self.sound_enabled:
                os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga &")
        except FileNotFoundError:
            # notify-send not available
            print(f"\n🔔 {title}: {message}")
    
    def _notify_windows(self, title, message):
        """Send notification on Windows"""
        try:
            from plyer import notification
            notification.notify(
                title=title,
                message=message,
                app_name="Pomodoro CLI",
                timeout=5
            )
        except ImportError:
            # If plyer not installed, use powershell
            try:
                ps_script = f"""
                [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
                $Template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
                $RawXml = [xml] $Template.GetXml()
                ($RawXml.toast.visual.binding.text|where {{$_.id -eq "1"}}).AppendChild($RawXml.CreateTextNode("{title}")) > $null
                ($RawXml.toast.visual.binding.text|where {{$_.id -eq "2"}}).AppendChild($RawXml.CreateTextNode("{message}")) > $null
                $SerializedXml = New-Object Windows.Data.Xml.Dom.XmlDocument
                $SerializedXml.LoadXml($RawXml.OuterXml)
                $Toast = [Windows.UI.Notifications.ToastNotification]::new($SerializedXml)
                $Toast.Tag = "Pomodoro"
                $Toast.Group = "Pomodoro"
                $Notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Pomodoro CLI")
                $Notifier.Show($Toast);
                """
                subprocess.run(
                    ["powershell", "-Command", ps_script],
                    check=False,
                    capture_output=True
                )
            except:
                # Ultimate fallback
                print(f"\n🔔 {title}: {message}")
        
        if self.sound_enabled:
            try:
                import winsound
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            except:
                pass
    
    def play_sound(self, sound_type="complete"):
        """
        Play notification sound
        
        Args:
            sound_type: Type of sound ('start', 'complete', 'break')
        """
        if not self.sound_enabled:
            return
        
        try:
            if self.system == "Darwin":  # macOS
                sounds = {
                    'start': '/System/Library/Sounds/Tink.aiff',
                    'complete': '/System/Library/Sounds/Glass.aiff',
                    'break': '/System/Library/Sounds/Bottle.aiff'
                }
                sound_file = sounds.get(sound_type, sounds['complete'])
                os.system(f"afplay {sound_file} &")
                
            elif self.system == "Linux":
                sounds = {
                    'start': '/usr/share/sounds/freedesktop/stereo/service-login.oga',
                    'complete': '/usr/share/sounds/freedesktop/stereo/complete.oga',
                    'break': '/usr/share/sounds/freedesktop/stereo/bell.oga'
                }
                sound_file = sounds.get(sound_type, sounds['complete'])
                if os.path.exists(sound_file):
                    os.system(f"paplay {sound_file} &")
                    
            elif self.system == "Windows":
                import winsound
                frequency = 1000 if sound_type == 'complete' else 800
                duration = 200
                winsound.Beep(frequency, duration)
        except:
            # If sound fails, just continue silently
            pass
    
    def bell(self):
        """Play terminal bell sound"""
        print('\a', end='', flush=True)
    
    def enable_sound(self):
        """Enable notification sounds"""
        self.sound_enabled = True
    
    def disable_sound(self):
        """Disable notification sounds"""
        self.sound_enabled = False
    
    def toggle_sound(self):
        """Toggle sound on/off"""
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled