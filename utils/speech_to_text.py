# Python program to translate
# speech to text and text to speech
# https://www.geeksforgeeks.org/python-convert-speech-to-text-and-text-to-speech/#

import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
r = sr.Recognizer()


def record_text():
    """
    Captures and converts user speech input into text.

    Uses a microphone as the source and Google's speech recognition API for transcription.

    Returns:
        str: The transcribed text if speech is successfully recognized.
        None: If an error occurs or no speech is detected.
    """
    while True:
        try:
            # Use the microphone as source for input.
            with sr.Microphone() as source2:
                # Adjust for ambient noise.
                r.adjust_for_ambient_noise(source2, duration=0.5)
                print("Say something!")

                # Listen for the user's input.
                audio2 = r.listen(source2, phrase_time_limit=30, timeout=4)

                # Convert audio to text using Google API.
                MyText = r.recognize_google(audio2)
                return MyText.lower()

        except sr.WaitTimeoutError:
            # Triggered when no audio is detected within the timeout period.
            print("No audio detected within the timeout period.")
            return None
        except sr.RequestError as e:
            # API request failed.
            print("Could not request results; {0}".format(e))
            return None
        except sr.UnknownValueError:
            # Speech was unintelligible.
            print("Unknown error occurred.")
            return None
        except Exception as e:
            # Handle unexpected exceptions.
            print(e)
            return None


def output_text(text):
    """
    Outputs text to the console and appends it to a file.

    Args:
        text (str): The text to be written and displayed.

    Returns:
        None
    """
    print(text)
    with open("../output.txt", "a") as f:
        f.write(text + "\n")