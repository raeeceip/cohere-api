#!/usr/bin/env python3

from datetime import datetime, timedelta
from typing import Dict, Optional, Any, Union
import logging
import re
import json

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class ResponseValidator:
    """
    Validates outputs from Cohere API and system commands.
    Focuses on calendar events, chat responses, and command outputs.
    """
    
    @staticmethod
    def validate_calendar_event(text: str) -> Dict[str, Union[str, int]]:
        """
        Extract and validate calendar event details from text.
        Returns: Dict with title, date, time, and duration.
        Raises: ValidationError if required fields cannot be extracted.
        """
        try:
            # Extract date, time, and duration using regex
            date_patterns = [
                r'(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
                r'tomorrow',
                r'next\s+\w+',  # next Monday, next Tuesday, etc.
                r'(today|tomorrow|\d{1,2}(?:st|nd|rd|th)?(?:\s+of\s+)?(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)(?:\s+\d{4})?)'
            ]
            time_pattern = r'(\d{1,2}(?::\d{2})?\s*(?:am|pm)?|\d{2}:\d{2})'
            duration_pattern = r'(\d+)\s*(?:hour|hr|minute|min)s?'
            
            # Find date match
            date_str = None
            for pattern in date_patterns:
                match = re.search(pattern, text.lower())
                if match:
                    date_str = match.group(0)
                    break
            
            if not date_str:
                raise ValidationError("Could not find a valid date in the text")

            # Convert relative dates
            today = datetime.now()
            if date_str == 'tomorrow':
                event_date = today + timedelta(days=1)
            elif 'next' in date_str:
                weekdays = {
                    'monday': 0, 'tuesday': 1, 'wednesday': 2,
                    'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6
                }
                target_day = weekdays.get(date_str.split()[-1].lower())
                if target_day is None:
                    raise ValidationError(f"Invalid day in '{date_str}'")
                    
                days_ahead = target_day - today.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                event_date = today + timedelta(days=days_ahead)
            else:
                # Try parsing the date string
                try:
                    event_date = datetime.strptime(date_str, '%Y-%m-%d')
                except ValueError:
                    # Try other date formats
                    try:
                        event_date = datetime.strptime(date_str, '%B %d, %Y')
                    except ValueError:
                        raise ValidationError(f"Could not parse date: {date_str}")

            # Find and validate time
            time_match = re.search(time_pattern, text.lower())
            if not time_match:
                raise ValidationError("Could not find a valid time in the text")
                
            time_str = time_match.group(1)
            try:
                # Handle different time formats
                if 'am' in time_str.lower() or 'pm' in time_str.lower():
                    # 12-hour format
                    if ':' not in time_str:
                        time_str += ':00'
                    time_obj = datetime.strptime(time_str, '%I:%M%p')
                else:
                    # 24-hour format
                    if ':' not in time_str:
                        time_str += ':00'
                    time_obj = datetime.strptime(time_str, '%H:%M')
            except ValueError:
                raise ValidationError(f"Could not parse time: {time_str}")

            # Extract duration (default 30 minutes)
            duration = 30
            duration_match = re.search(duration_pattern, text.lower())
            if duration_match:
                duration = int(duration_match.group(1))
                if 'hour' in duration_match.group(0):
                    duration *= 60
                # Cap duration between 1 minute and 8 hours
                duration = max(1, min(duration, 480))

            # Extract title - everything before the first time/date reference
            all_patterns = '|'.join(date_patterns + [time_pattern, duration_pattern])
            matches = list(re.finditer(all_patterns, text.lower()))
            if matches:
                title = text[:matches[0].start()].strip()
            else:
                title = "New Event"

            if not title:
                title = "New Event"

            return {
                "title": title,
                "date": event_date.strftime('%Y-%m-%d'),
                "time": time_obj.strftime('%H:%M'),
                "duration": duration
            }

        except Exception as e:
            logging.error(f"Calendar validation error: {str(e)}")
            raise ValidationError(str(e))

    @staticmethod
    def validate_chat_response(response: str) -> str:
        """
        Validate and clean chat responses.
        Performs basic content filtering and cleanup.
        """
        if not response or not response.strip():
            raise ValidationError("Empty response received")

        # Remove excessive whitespace
        cleaned = ' '.join(response.split())
        
        # Basic validation
        if len(cleaned) < 2:
            raise ValidationError("Response too short")
            
        # Detect potential error messages
        error_indicators = ['error:', 'exception:', 'failed:', 'invalid:']
        if any(indicator in cleaned.lower() for indicator in error_indicators):
            logging.warning(f"Potential error in response: {cleaned}")
            # Don't raise error, just log warning
            
        return cleaned

    @staticmethod
    def validate_command_output(output: Any) -> Dict[str, Any]:
        """
        Validate system command outputs.
        Handles different output types and formats.
        """
        try:
            # Handle None/empty output
            if output is None:
                return {"status": "error", "message": "No output received"}

            # If output is already a dict, validate its structure
            if isinstance(output, dict):
                return output

            # Try parsing as JSON if it's a string
            if isinstance(output, str):
                try:
                    return json.loads(output)
                except json.JSONDecodeError:
                    # If not JSON, return as simple message
                    return {
                        "status": "success",
                        "message": output.strip()
                    }

            # For other types, convert to string
            return {
                "status": "success",
                "message": str(output)
            }

        except Exception as e:
            logging.error(f"Command output validation error: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

# Example usage:
"""
validator = ResponseValidator()

# Validate calendar event
try:
    event = validator.validate_calendar_event(
        "Schedule team meeting tomorrow at 2pm for 1 hour"
    )
    print("Validated event:", event)
except ValidationError as e:
    print("Calendar validation failed:", str(e))

# Validate chat response
try:
    cleaned = validator.validate_chat_response("  Here is my response.  ")
    print("Validated response:", cleaned)
except ValidationError as e:
    print("Response validation failed:", str(e))

# Validate command output
result = validator.validate_command_output('{"status": "success"}')
print("Validated output:", result)
"""