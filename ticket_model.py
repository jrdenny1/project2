"""
Data class for help desk ticket.
"""

class Ticket:
    """
    represents a single help desk ticket.
    Stores the ticket ID, user's name, priority, and description of the issue.
    """
    def __init__(self, ticket_id: str, user_name: str, priority: str, description: str) -> None:
        """
        Create a new Ticket instance.
        Whitespace is stripped away from every field.

        :param ticket_id: Ticket number as a string (numeric text like "0001").
        :param user_name: Name of the person who opened the ticket.
        :param priority: Priority label ("Low", "Medium", or "High").
        :param description: Short description of the problem.
        """
        self.ticket_id: str = ticket_id.strip()
        self.user_name: str = user_name.strip()
        self.priority: str = priority.strip()
        self.description: str = description.strip()
