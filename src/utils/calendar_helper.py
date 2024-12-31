
import json
import logging
import subprocess
from datetime import datetime
from typing import Dict

def create_calendar_event(event_details: Dict) -> bool:
    try:
        script = f'''
        tell application "Calendar"
            tell calendar "Calendar"
                make new event at end with properties {{
                    summary: "{event_details['title']}",
                    start date: date "{event_details['date']} {event_details['time']}",
                    duration: {event_details.get('duration', 30)} * minutes
                }}
            end tell
        end tell
        '''
        
        subprocess.run(['osascript', '-e', script])
        return True
    except Exception as e:
        logging.error(f"Error creating calendar event: {str(e)}")
        return False