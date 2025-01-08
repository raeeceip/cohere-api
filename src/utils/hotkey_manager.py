
import sys
import os
import subprocess
from pathlib import Path
import logging

class HotkeyManager:
    @staticmethod
    def setup_command_r():
        """Set up Command+R hotkey for the application"""
        logging.basicConfig(level=logging.INFO)
        if sys.platform == "darwin":
            HotkeyManager._setup_macos_hotkey()
        else:
            logging.error("Hotkey setup is only supported on macOS at this time")
            

    @staticmethod
    def _setup_macos_hotkey():
        """Set up Command+R hotkey on macOS"""
        try:
            # Get the path to the application
            if getattr(sys, 'frozen', False):
                app_path = Path(sys._MEIPASS).parent.parent
            else:
                app_path = Path(os.getenv("RESOURCE_PATH", ".")).parent
            
            logging.info(f"Setting up hotkey for application at: {app_path}")

            # Modified AppleScript to be more reliable
            script = f'''
            tell application "System Events"
                try
                    tell application "System Settings"
                        activate
                    end tell
                    delay 1
                    tell process "System Settings"
                        click menu item "Keyboard" of menu 1 of menu bar item "View" of menu bar 1
                        delay 1
                        click button "Keyboard Shortcuts..." of group 1 of window 1
                        delay 1
                        select row 8 of outline 1 of scroll area 1 of splitter group 1 of window 1
                        delay 1
                        click button "+" of splitter group 1 of window 1
                        delay 1
                        
                        tell sheet 1 of window 1
                            set value of text field 1 to "Launch CommandR"
                            set value of text field 2 to "{str(app_path)}"
                            keystroke "r" using {{"command down"}}
                            click button "Add"
                        end tell
                        
                        return "Hotkey setup completed successfully"
                    end tell
                on error errMsg
                    return "Error: " & errMsg
                end try
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                 capture_output=True, 
                                 text=True)
            
            if result.returncode != 0:
                logging.error(f"AppleScript failed: {result.stderr}")
                return False
                
            if "Error:" in result.stdout:
                logging.error(f"AppleScript error: {result.stdout}")
                return False
                
            logging.info("Successfully set up Command+R hotkey")
            return True
            
        except Exception as e:
            logging.error(f"Failed to set up Command+R hotkey: {str(e)}")
            return False