import pyttsx3
import spacy

nlp = spacy.load("en_core_web_sm")

engine = pyttsx3.init()


def speak_out_loud(command):
    """
    Converts a given text command into spoken words using a text-to-speech engine.

    Args:
        command (str): The text to be spoken.

    Returns:
        None
    """
    engine.say(command)
    engine.runAndWait()