"""
Main file for project 2
This launches the PyQt GUI and shows the main window.
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