import re
from ui.ui_components import TimerWindow, TimerWorker

def extract_timer_details(text):
    """
    Extracts the duration of a timer from a user's text input.

    This function uses regular expressions to search for time-related keywords like
    "minutes", "hours", or "seconds" and converts them into a numeric value representing
    the time in seconds.

    Args:
        text (str): The text input provided by the user, potentially containing a time duration.

    Returns:
        dict: A dictionary containing the extracted time in seconds under the key "time".
              If no time is found, returns {"time": None}.
    """
    # Search for time patterns like "5 minutes", "1 hour", "30 seconds"
    time_match = re.search(r'(\d+)\s*(minute|hour|second|minute[s]?)?', text)

    if time_match:
        # Extract the numeric value
        time_value = int(time_match.group(1))  # This is the number (e.g., 5 from "5-minute")

        # Get the unit (minute, hour, second) and convert to seconds
        unit = time_match.group(2)
        if unit in ['minute', 'minutes']:
            time_value *= 60  # Convert minutes to seconds
        elif unit in ['hour', 'hours']:
            time_value *= 3600  # Convert hours to seconds
        elif unit in ['second', 'seconds']:
            time_value *= 1  # No conversion needed for seconds

        return {"time": time_value}
    else:
        return {"time": None}  # If no time found, return None


def start_timer(time_data):
    """
    Starts a timer based on the provided time data.

    This function initializes a timer window, creates a worker to handle the timer countdown,
    and connects the necessary signals to update the window and notify the user when the timer is complete.

    Args:
        time_data (dict): A dictionary containing the key "time", which holds the duration in seconds.

    Returns:
        str: A message indicating the status of the timer. If the timer duration is valid,
             returns the duration in seconds. If no valid time is provided, returns a
             failure message indicating that the duration could not be understood.
    """
    if time_data.get("time"):
        # Create the timer window in the main thread
        timer_window = TimerWindow(time_data["time"])

        # Create the timer worker thread
        timer_worker = TimerWorker(time_data["time"])

        # Connect signals to the appropriate slots in the TimerWindow
        timer_worker.update_timer_signal.connect(timer_window.update_timer)
        timer_worker.timer_done_signal.connect(timer_window.show_timer_done_message)

        # Start the worker thread
        timer_worker.start()

        # Show the window
        timer_window.show()

        return f"Timer set for {time_data['time']} seconds!"
    else:
        return "Sorry, I couldn't understand the timer duration."
