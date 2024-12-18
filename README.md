# Voice Assistant Project

This project implements a simple voice assistant with speech-to-text capabilities, natural language processing (NLP), and integration with Spotify to play songs and a timer feature. The assistant can understand spoken commands, interpret them, and execute actions based on user intent.

## Features

- **Speech-to-Text**: Convert spoken words into text using the SpeechRecognition library.
- **Natural Language Processing (NLP)**: Process the text and extract relevant information like song names, artists, and timer durations.
- **Spotify Integration**: Play songs on Spotify based on the user's request.
- **Timer**: Set and manage timers based on the user's command.

## How It Works

### **Speech-to-Text**

Speech-to-Text (also called Speech Recognition) converts spoken words into written text. This allows users to control the system using voice commands instead of typing.

**How it works:**
1. **Sound Wave Analysis**: The system listens to the user's voice through the microphone and captures the audio.
2. **Feature Extraction**: The audio is processed to extract features that represent speech.
3. **Acoustic Modeling**: The extracted features are matched with a vocabulary of words and phonetic patterns using a trained model.
4. **Language Modeling**: The system uses a language model to interpret the words in context and generate meaningful text.
5. **Text Generation**: Finally, the recognized speech is converted into text that the system can understand.

In this project, we use the **SpeechRecognition** library to convert speech into text via Google’s Speech Recognition API. The recognized text is passed to the NLP system for further processing.

### **Natural Language Processing (NLP)**

NLP enables the system to understand and process human language by extracting meaningful information from the spoken text. In this project, we use the **spaCy** library to process the speech-to-text data.

**How it works:**
1. **Tokenization**: Splitting text into individual words or tokens.
2. **Part-of-Speech Tagging (POS)**: Identifying grammatical parts of speech (noun, verb, etc.).
3. **Named Entity Recognition (NER)**: Identifying proper nouns like people, places, and dates.
4. **Intent Recognition**: Detecting the user's intent, such as "play song" or "set timer".
5. **Contextual Understanding**: The system understands the context of words, especially those with multiple meanings.

For example, when the user says, "Play Shape of You by Ed Sheeran," NLP extracts the song name ("Shape of You") and the artist name ("Ed Sheeran").

### **Spotify Integration**

Using the **Spotipy** library, the system can search for songs on Spotify and play them on an active device.

**How it works:**
1. The user specifies a song and artist (e.g., "Play Shape of You by Ed Sheeran").
2. The NLP system extracts the song and artist names.
3. The system searches for the song on Spotify.
4. If the song is found, it is played on the active device.

### **Timer**

The system can set timers based on spoken commands. For example, saying "Set a timer for 5 minutes" will trigger the assistant to start a countdown.

**How it works:**
1. The user provides a time duration in the format "X minutes", "X hours", or "X seconds".
2. The system processes the text to extract the time.
3. A timer is started, and a countdown is shown in a window.
4. The system notifies the user when the timer is done.





Credits
- Chat
- Claude
- [https://www.youtube.com/watch?v=CMrHM8a3hqw&ab_channel=Simplilearn](https://spacy.io/usage/spacy-101#annotations-pos-deps)

