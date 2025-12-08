"""
Entry point for the Help Desk Ticket Tracker application.
"""
from PyQt6 import QtWidgets
from logic import TicketWindow

def main() -> None:
    """
    Create the application object and show the main window.
    """
    app = QtWidgets.QApplication([])
    window = TicketWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()