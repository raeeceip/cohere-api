
import sys
import os
import subprocess
from pathlib import Path
import logging

class HotkeyManager:
    @staticmethod
    def setup_command_r():
        """Set up Command+R hotkey for the application"""
        if sys.platform == "darwin":
            HotkeyManager._setup_macos_hotkey()
        else:
            logging.warning("Command+R hotkey setup is currently only supported on macOS")
    
    @staticmethod
    def _setup_macos_hotkey():
        """Set up Command+R hotkey on macOS"""
        try:
            # Get the path to the application
            if getattr(sys, 'frozen', False):
                app_path = Path(sys._MEIPASS).parent.parent
            else:
                app_path = Path(os.getenv("RESOURCE_PATH")).parent
                
            # Create AppleScript to set up the hotkey
            script = f'''
            tell application "System Events"
                tell application "System Preferences"
                    activate
                end tell
                delay 1
                tell process "System Preferences"
                    click menu item "Keyboard" of menu "View" of menu bar 1
                    delay 1
                    click button "Shortcuts" of tab group 1 of window 1
                    delay 1
                    select row 1 of table 1 of scroll area 1 of splitter group 1 of tab group 1 of window 1
                    delay 1
                    click button "+" of splitter group 1 of tab group 1 of window 1
                    delay 1
                    tell sheet 1 of window 1
                        set value of text field 2 to "{app_path}"
                        set value of text field 1 to "Launch CommandR"
                        keystroke "r" using command down
                        click button "Add"
                    end tell
                end tell
            end tell
            '''
            
            subprocess.run(['osascript', '-e', script])
            logging.info("Successfully set up Command+R hotkey")
            
        except Exception as e:
            logging.error(f"Failed to set up Command+R hotkey: {e}")