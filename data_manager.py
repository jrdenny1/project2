"""
Handles reading and writing ticket data to a CSV file
for the Help Desk Ticket Tracker Program
"""
import csv
import os
from typing import List

from ticket_model import Ticket

TICKETS_FILE = "tickets.csv"

def append_ticket(ticket: Ticket) -> None:
    """
    Append a ticket to the CSV file.
    If the file doesnt exist, the function will create it and write a header row.

    :param ticket: Ticket to append to persistent storage.
    :raises RuntimeError: If the file cannot be opened or written.
    """
    file_exists = os.path.exists(TICKETS_FILE)

    try:
        with open(TICKETS_FILE, mode="a", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)

            if not file_exists:
                writer.writerow(["ticket_id", "user_name", "priority", "description"])
            
            writer.writerow(
                [
                    ticket.ticket_id,
                    ticket.user_name,
                    ticket.priority,
                    ticket.description,
                ]
            )
    except OSError as error:
        raise RuntimeError(f"Could not write to {TICKETS_FILE}: {error}") from error
    
def load_tickets() -> List[Ticket]:
    """
    Load all tickets from CSV file.
    :return: A list of Ticket objects. Returns an Empty list if the file does not exist yet.
    :rtype: list[Ticket]
    :raises RuntimeError: If the file exists but cannot be read
    """
    tickets: List[Ticket] = []

    if not os.path.exists(TICKETS_FILE):
        return tickets
    
    try:
        with open(TICKETS_FILE, mode="r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                ticket_id = (row.get("ticket_id") or "").strip()
                user_name = (row.get("user_name") or "").strip()
                priority = (row.get("priority") or "").strip()
                description = (row.get("description") or "").strip()

                if ticket_id and user_name and priority and description:
                    tickets.append(
                        Ticket(
                            ticket_id=ticket_id,
                            user_name=user_name,
                            priority=priority,
                            description=description,
                        )
                    )
    except OSError as error:
        raise RuntimeError(f"Could not read {TICKETS_FILE}: {error}") from error
    return tickets