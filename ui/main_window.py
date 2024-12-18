from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication
from PyQt5.QtCore import Qt, QThreadPool
from ui.ui_components import SiriButton, TimerWindow, SpeechToTextWorker, TimerWorker, TimerThread
from utils.utils import speak_out_loud
from utils.match_intent import match_intent
from commands.timer import extract_timer_details
from commands.calendar import add_task_to_google_calendar, extract_event_datetime_google_format
from commands.song_player import play_song_on_spotify, extract_song_and_artist

class AssistantWindow(QMainWindow):
    """
    Main Window for the AI Assistant application.
    Provides GUI components and integrates various features such as setting timers,
    adding events to Google Calendar, playing music on Spotify, and responding to voice commands.
    """

    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()

        self.setWindowTitle("AI Assistant")
        self.setGeometry(100, 100, 100, 100)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # Make window stay on top
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.move_to_bottom_right()

        self.layout = QVBoxLayout()
        self.listen_button = SiriButton(self)
        self.listen_button.clicked.connect(self.start_listening)
        self.layout.addWidget(self.listen_button, alignment=Qt.AlignCenter)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        QApplication.instance().aboutToQuit.connect(self.cleanup_timers)

    def move_to_bottom_right(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = screen_geometry.right() - self.width() - 50
        y = screen_geometry.bottom() - self.height() - 50
        self.move(x, y)

    def start_timer(self, time_in_seconds):
        self.cleanup_timers()
        self.timer_worker = TimerWorker(time_in_seconds)
        self.timer_thread = TimerThread(self.timer_worker)

        self.timer_worker.open_timer_window_signal.connect(self.open_timer_window)
        self.timer_worker.update_timer_signal.connect(self.update_timer_display)
        self.timer_worker.timer_done_signal.connect(self.on_timer_complete)

        self.timer_thread.start()

    def open_timer_window(self, time_in_seconds):
        self.timer_window = TimerWindow(time_in_seconds)
        self.timer_window.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.timer_window.show()

    def update_timer_display(self, remaining_time):
        if hasattr(self, 'timer_window'):
            self.timer_window.update_timer_label(remaining_time)

    def on_timer_complete(self, message):
        if hasattr(self, 'timer_window'):
            self.timer_window.close()

    def start_listening(self):
        print("Starting listening...")  # Debug
        self.listen_button.start_pulsing()
        QApplication.processEvents()
        worker = SpeechToTextWorker(self.on_listening_complete)
        self.threadpool.start(worker)

    def on_listening_complete(self, text):
        print(f"Listening complete: {text}")  # Debug
        self.listen_button.stop_pulsing()
        self.process_command(text)
        self.start_listening()  # Continue listening

    def start_speaking(self, text):
        self.listen_button.start_pulsing()
        QApplication.processEvents()
        speak_out_loud(text)
        self.listen_button.stop_pulsing()

    def cleanup_timers(self):
        print("Cleaning up timers...")  # Debug
        if hasattr(self, 'timer_thread') and self.timer_thread.isRunning():
            if hasattr(self, 'timer_worker'):
                self.timer_worker.stop_timer()
            self.timer_thread.quit()
            self.timer_thread.wait()

        if hasattr(self, 'timer_window'):
            self.timer_window.close()

    def closeEvent(self, event):
        print("Window close event triggered")  # Debug
        self.cleanup_timers()
        event.accept()

    def process_command(self, text):
        if text and "can you" in text:
            text = text.replace("can you", "")
        if text:
            print(f"Processing command: {text}")  # Debug
            intent = match_intent(text)
            if intent == "play_song":
                song_data = extract_song_and_artist(text)
                response = play_song_on_spotify(song_data)
                self.start_speaking(response)
            elif intent == "set_timer":
                time_data = extract_timer_details(text)
                time = time_data["time"]
                if time:
                    self.start_timer(time)
            elif intent == "stop_timer":
                self.cleanup_timers()
                self.start_speaking("Timers stopped.")
            elif intent == "add_calendar":
                calendar_data = extract_event_datetime_google_format(text)
                response = add_task_to_google_calendar(calendar_data)
                print(response)
                self.start_speaking(response)
            else:
                self.start_speaking("Sorry, I didn't understand that command.")
