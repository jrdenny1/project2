"""
Data class for help desk ticket.
"""

class Ticket:
    """
    represents a single help desk ticket. 
    """
    def __init__(self, ticket_id: str, user_name: str, priority: str, description: str) -> None:
        self.ticket_id: str = ticket_id.strip()
        self.user_name: str = user_name.strip()
        self.priority: str = priority.strip()
        self.description: str = description.strip()
