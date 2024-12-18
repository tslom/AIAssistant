from fuzzywuzzy import fuzz

commands = {
    "add_calendar": ["add a meeting", "add to my calendar", "schedule a meeting", "add a task", "remind me to", "remind me to", ],
    "set_timer": ["set timer", "start a timer for", "make a timer", "timer for"],
    "stop_timer": ["stop timer", "stop", "stop the clock", "stop timing"],
    "play_song": ["play", "play [song] by [artist]", "can you play [song] by [artist]", "can you play [song]"],
}


def match_intent(user_text):
    """
    Matches a user's text input to a predefined intent using fuzzy string matching.

    Args:
        user_text (str): The text input provided by the user.

    Returns:
        str: The intent that best matches the user's input, or "unknown" if no match is found.
    """
    for intent, phrases in commands.items():
        for phrase in phrases:
            if fuzz.partial_ratio(user_text.lower(), phrase.lower()) > 60:
                return intent
    return "unknown"
