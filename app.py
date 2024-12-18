"""
Main Entry Point for AI Assistant Application

This script initializes and runs the AI Assistant application using PyQt5. 
It creates an instance of the `AssistantWindow` class and starts the application's event loop.

Modules:
    - sys: Provides access to system-specific parameters and functions, such as command-line arguments.
    - PyQt5.QtWidgets: Used for creating the application and managing the main event loop.
    - ui.main_window: Contains the `AssistantWindow` class that defines the main GUI for the assistant.

Usage:
    Run this script directly to start the AI Assistant application.
    Example: `python app.py`
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import AssistantWindow

# Check if the script is being executed directly
if __name__ == "__main__":
    # Create a QApplication instance
    # QApplication manages application-wide settings and the event loop
    app = QApplication(sys.argv)

    # Create an instance of the AssistantWindow
    # This is the main GUI for the AI assistant
    window = AssistantWindow()

    # Show the main window
    # This makes the window visible on the screen
    window.show()

    # Start the application's event loop
    # This keeps the application running and responsive to user input
    sys.exit(app.exec_())
