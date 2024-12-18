from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QMainWindow, QWidget
from PyQt5.QtCore import QTimer, Qt, QRunnable, pyqtSlot, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QPainter, QColor, QBrush, QPainterPath, QFont

from utils.speech_to_text import record_text


class SiriButton(QPushButton):
    """
    Custom QPushButton styled as a Siri-like button with a pulsing animation.
    """

    def __init__(self, parent=None):
        """
        Initializes the SiriButton.

        Args:
            parent (QWidget): The parent widget, if any.
        """
        super().__init__(parent)
        self.setFixedSize(100, 100)
        self.setStyleSheet("border-radius: 50px; background-color: #0096FF;")
        self.pulsing = False
        self.ripple_radius = 0
        self.ripple_opacity = 255
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ripple)

    def start_pulsing(self):
        """
        Starts the pulsing animation for the button.
        """
        if not self.pulsing:
            self.pulsing = True
            self.ripple_radius = 0
            self.ripple_opacity = 255
            self.timer.start(30)

    def stop_pulsing(self):
        """
        Stops the pulsing animation for the button.
        """
        if self.pulsing:
            self.pulsing = False
            self.timer.stop()
            self.ripple_radius = 0
            self.update()

    def update_ripple(self):
        """
        Updates the ripple effect during the pulsing animation.
        """
        if self.pulsing:
            self.ripple_radius += 2
            self.ripple_opacity -= 5
            if self.ripple_opacity <= 0:
                self.ripple_radius = 0
                self.ripple_opacity = 255
            self.update()

    def paintEvent(self, event):
        """
        Custom paint event to draw the pulsing ripple effect.

        Args:
            event (QPaintEvent): The paint event instance.
        """
        super().paintEvent(event)

        if self.pulsing:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            path = QPainterPath()
            center = self.rect().center()
            radius = self.width() // 2
            path.addEllipse(center, radius, radius)
            painter.setClipPath(path)

            color = QColor("#ADD8E6")
            color.setAlpha(self.ripple_opacity)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)

            painter.drawEllipse(center, self.ripple_radius, self.ripple_radius)


class TimerWindow(QMainWindow):
    """
    A window that displays a countdown timer.
    """
    timer_closed = pyqtSignal()  # Signal emitted when the window is closed

    def __init__(self, time_in_seconds):
        """
        Initializes the TimerWindow.

        Args:
            time_in_seconds (int): The duration of the timer in seconds.
        """
        super().__init__()
        self.setWindowTitle("Timer")
        self.setGeometry(100, 100, 200, 100)  # Position the window at the bottom-left of the screen
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.timer_label = QLabel(self)
        self.timer_label.setAlignment(Qt.AlignCenter)

        font = QFont()
        font.setPointSize(48)
        font.setBold(True)
        self.timer_label.setFont(font)

        layout = QVBoxLayout()
        layout.addWidget(self.timer_label)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_timer_label(self, remaining_time):
        """
        Updates the timer display with the remaining time.

        Args:
            remaining_time (int): The remaining time in seconds.
        """
        minutes, seconds = divmod(int(remaining_time), 60)
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")

    def closeEvent(self, event):
        """
        Handles the window close event.

        Emits the `timer_closed` signal when the window is closed.

        Args:
            event (QCloseEvent): The close event instance.
        """
        self.timer_closed.emit()
        event.accept()


class TimerWorker(QObject):
    """
    Handles the logic for a countdown timer in a background thread.
    """
    update_timer_signal = pyqtSignal(int)  # Signal to update the timer
    timer_done_signal = pyqtSignal(str)   # Signal emitted when the timer completes
    open_timer_window_signal = pyqtSignal(int)  # Signal to open the timer window

    def __init__(self, time_in_seconds):
        """
        Initializes the TimerWorker.

        Args:
            time_in_seconds (int): The duration of the timer in seconds.
        """
        super().__init__()
        self.time_in_seconds = time_in_seconds
        self.is_running = True

    @pyqtSlot()
    def start_timer(self):
        """
        Starts the countdown timer and emits signals during the countdown.
        """
        self.open_timer_window_signal.emit(self.time_in_seconds)

        while self.time_in_seconds > 0 and self.is_running:
            QThread.msleep(1000)
            self.time_in_seconds -= 1
            self.update_timer_signal.emit(self.time_in_seconds)

        if self.is_running:
            self.timer_done_signal.emit("Timer Complete!")
            self.is_running = False

    @pyqtSlot()
    def stop_timer(self):
        """
        Stops the countdown timer.
        """
        self.is_running = False


class TimerThread(QThread):
    """
    Thread class to run the TimerWorker in a separate thread.
    """

    def __init__(self, timer_worker):
        """
        Initializes the TimerThread.

        Args:
            timer_worker (TimerWorker): The TimerWorker instance to run in the thread.
        """
        super().__init__()
        self.timer_worker = timer_worker

    def run(self):
        """
        Runs the TimerWorker's timer logic.
        """
        self.timer_worker.start_timer()


class SpeechToTextWorker(QRunnable):
    """
    Runnable class to handle speech-to-text functionality in a background thread.
    """

    def __init__(self, callback):
        """
        Initializes the SpeechToTextWorker.

        Args:
            callback (function): The callback function to execute with the transcribed text.
        """
        super().__init__()
        self.callback = callback

    @pyqtSlot()
    def run(self):
        """
        Executes the speech-to-text process and invokes the callback with the result.
        """
        text = record_text()  # Run speech-to-text
        self.callback(text)
