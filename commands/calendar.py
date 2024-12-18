from datetime import timedelta, datetime

import dateparser
import pytz
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from utils.utils import nlp


def add_task_to_google_calendar(data, duration_minutes=60, timezone="America/Los_Angeles"):
    """
    Extracts event details from a string and adds the task to Google Calendar.

    Args:
        data (dict): Input string containing event details.
        duration_minutes (int): Duration of the event in minutes. Default is 60.
        timezone (str): Timezone for the event. Default is America/Los_Angeles.

    Returns:
        str: Success or error message.
    """
    try:
        SCOPES = ["https://www.googleapis.com/auth/calendar"]

        # Use flow.run_local_server() only if you haven't already authorized
        flow = InstalledAppFlow.from_client_secrets_file(
            '/Users/26slomianyjt/Desktop/MyCode/SpeechRecognition/credentials.json',
            SCOPES
        )

        # Load or create credentials
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        except FileNotFoundError:
            creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('calendar', 'v3', credentials=creds)

        # Extract event details using NLP function
        extracted_details = data

        if not extracted_details['date_time']:
            return "Error: Could not parse a valid datetime from the input text."

        # Define start and end times
        start_datetime = datetime.fromisoformat(extracted_details['date_time'])

        # Localize the datetime if not already timezone-aware
        if start_datetime.tzinfo is None:
            localized_start = pytz.timezone(timezone).localize(start_datetime)
        else:
            localized_start = start_datetime

        end_datetime = (localized_start + timedelta(minutes=duration_minutes)).isoformat()

        # Define the event for Google Calendar
        event = {
            'summary': extracted_details['event_name'] or "Untitled Event",
            'start': {
                'dateTime': localized_start.isoformat(),
                'timeZone': timezone
            },
            'end': {
                'dateTime': end_datetime,
                'timeZone': timezone
            },
        }

        # Add the event to Google Calendar
        service.events().insert(calendarId='primary', body=event).execute()
        return "Task added successfully!"
    except Exception as e:
        return f"Error adding task: {e}"


def extract_event_datetime_google_format(text, timezone="UTC"):
    """
    Extracts the event name and datetime from a given string and formats the date for Google Calendar.

    Args:
        text (str): Input string containing an event and datetime.
        timezone (str): Timezone to format the datetime, default is UTC.

    Returns:
        dict: A dictionary containing the event_name and date_time in Google Calendar format.
    """
    # Process text with spaCy
    doc = nlp(text)

    # Placeholder for extracted entities
    date_time_str = None
    event_name_parts = []

    # Identify named entities for dates and times
    for ent in doc.ents:
        if ent.label_ in ["DATE", "TIME"]:
            date_time_str = ent.text
        elif ent.label_ in ["EVENT", "ORG", "WORK_OF_ART", "PERSON"]:
            event_name_parts.append(ent.text)

    # Fallback if date was not identified by spaCy
    if date_time_str is None:
        date_time_str = dateparser.parse(text)

    # Parse date and time using dateparser
    parsed_date = dateparser.parse(date_time_str) if date_time_str else None

    # Convert to Google Calendar RFC3339 format
    if parsed_date:
        if parsed_date.tzinfo is None:
            local_timezone = pytz.timezone(timezone)
            localized_date = local_timezone.localize(parsed_date)
        else:
            localized_date = parsed_date  # Already timezone-aware

        google_calendar_date = localized_date.isoformat()  # Converts to RFC3339
    else:
        google_calendar_date = None

    # Create the result dictionary
    result = {
        "event_name": " ".join(event_name_parts).strip() or None,
        "date_time": google_calendar_date
    }

    print(result)

    return result
