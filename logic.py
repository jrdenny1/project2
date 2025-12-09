"""
Main window logic for the Help Desk Tracker GUI.
"""
from PyQt6 import QtWidgets, QtGui
from ticket_window import Ui_MainWindow
from ticket_model import Ticket
import data_manager

class TicketWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Main window class for the ticket tracker. 
    Inherits from QMainWindow and Ui_MainWindow so we can access all the widgets.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self._configure_status_label()
        self._configure_table()
        self._connect_signals()
        self._load_tickets_into_table()

    def _configure_status_label(self) -> None:
        """
        Configure the status label appearance.
        Default is empty and shows messages in red so errors are easy to spot.
        """
        palette = self.statusLabel.palette()
        palette.setColor(self.statusLabel.foregroundRole(), QtGui.QColor("red"))
        self.statusLabel.setPalette(palette)
        self.statusLabel.setText("")
    
    def _configure_table(self) -> None:
        """
        Set up the ticket table headers and default behavior.
        """
        headers = ["Ticket ID", "User Name", "Priority", "Description"]
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.setRowCount(0)

        header = self.tableWidget.horizontalHeader()
        header.setStretchLastSection(True)
    
    def _connect_signals(self) -> None:
        """
        Connect buttons to their slots.
        """
        self.addButton.clicked.connect(self.handle_add_ticket_clicked)
        self.exitButton.clicked.connect(self.close)

    def handle_add_ticket_clicked(self) -> None:
        """
        Handle the Add Ticket button click.

        Validates the input fields.
        Appends the ticket to the CSV file if everything is valid.
        Refreshes the table.
        Shows either an error message or a success message.
        """
        self.statusLabel.setText("")

        ticket_id = self.ticketIdInput.text().strip()
        user_name = self.userNameInput.text().strip()
        priority = self._get_selected_priority()
        description = self.descriptionInput.toPlainText().strip()

        error_message = self._validate_input(ticket_id, user_name, priority, description)
        if error_message is not None:
            self.statusLabel.setText(error_message)
            return
        
        ticket = Ticket(
            ticket_id=ticket_id,
            user_name=user_name,
            priority=priority, 
            description=description,
        )

        try:
            data_manager.append_ticket(ticket)
            self._load_tickets_into_table()
            self._clear_form()
            self.statusLabel.setText("Ticket added successfully.")
        except RuntimeError as error:
            self.statusLabel.setText(str(error))
    
    def _get_selected_priority(self) -> str | None:
        """
        Returns the selected priority as a string, or None if nothing is selected.

        :return: "Low", "Medium", "High", or none if no radio button is selected.
        """
        if self.priorityLowRadio.isChecked():
            return "Low"
        if self.priorityMedRadio.isChecked():
            return "Medium"
        if self.priorityHighRadio.isChecked():
            return "High"
        return None
    
    def _validate_input(
        self,
        ticket_id: str,
        user_name: str,
        priority: str | None,
        description: str,
    ) -> str | None:
        """
        Validate the ticket fields and return an error message if anything is wrong.
        Returns None if all fields are valid.

        :param ticket_id: Ticket number from the text box.
        :param user_name: Name of the user opening the ticket.
        :param priority: Priority string, or None if nothing was selected.
        :param description: Problem description from the text area.
        :return: Error message string, or None if all fields are valid.
        """
        if not ticket_id:
            return "Please enter a ticket ID."
        
        if not ticket_id.isdigit():
            return "Ticket ID must be numeric (e.g. 0001)."

        if not user_name:
            return "Please enter a user name."
        
        if priority is None:
            return "Please select a priority."

        if not description:
            return "Please enter a description."

        return None
    
    def _clear_form(self) -> None:
        """
        Clear the input fields after a successful ticket save.
        """
        self.ticketIdInput.clear()
        self.userNameInput.clear()
        self.descriptionInput.clear()

        self.priorityLowRadio.setAutoExclusive(False)
        self.priorityMedRadio.setAutoExclusive(False)
        self.priorityHighRadio.setAutoExclusive(False)

        self.priorityLowRadio.setChecked(False)
        self.priorityMedRadio.setChecked(False)
        self.priorityHighRadio.setChecked(False)

        self.priorityLowRadio.setAutoExclusive(True)
        self.priorityMedRadio.setAutoExclusive(True)
        self.priorityHighRadio.setAutoExclusive(True)
    
    def _load_tickets_into_table(self) -> None:
        """
        Load all tickets from the CSV file and display them in the table widget.
        Errors from data layer are shown in status label.
        """
        try:
            tickets = data_manager.load_tickets()
        except RuntimeError as error:
            self.statusLabel.setText(str(error))
            return

        self.tableWidget.setRowCount(len(tickets))

        for row, ticket in enumerate(tickets):
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(ticket.ticket_id))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(ticket.user_name))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(ticket.priority))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(ticket.description))