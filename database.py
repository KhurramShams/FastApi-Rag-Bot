
import sqlite3
import datetime
import logging
import uuid

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """Initialize SQLite database and create tickets table if it doesn't exist."""
    try:
        conn = sqlite3.connect("support_tickets.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id TEXT PRIMARY KEY,
                user_id TEXT,
                description TEXT,
                timestamp TEXT,
                status TEXT,
                pdf_file_name TEXT
            )
        """)
        conn.commit()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise
    finally:
        conn.close()

def save_ticket(user_id, description, pdf_file_name):
    """Save a support ticket to the database."""
    try:
        ticket_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().isoformat()
        status = "Open"
        conn = sqlite3.connect("support_tickets.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO tickets (ticket_id, user_id, description, timestamp, status, pdf_file_name)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (ticket_id, user_id, description, timestamp, status, pdf_file_name)
        )
        conn.commit()
        logger.info(f"Saved ticket {ticket_id} for user {user_id}")
        return ticket_id
    except Exception as e:
        logger.error(f"Error saving ticket: {str(e)}")
        raise
    finally:
        conn.close()

def get_tickets(status=None):
    """Retrieve all tickets, optionally filtered by status."""
    try:
        conn = sqlite3.connect("support_tickets.db")
        cursor = conn.cursor()
        if status:
            cursor.execute("SELECT * FROM tickets WHERE status = ?", (status,))
        else:
            cursor.execute("SELECT * FROM tickets")
        tickets = cursor.fetchall()
        columns = ["ticket_id", "user_id", "description", "timestamp", "status", "pdf_file_name"]
        return [dict(zip(columns, ticket)) for ticket in tickets]
    except Exception as e:
        logger.error(f"Error retrieving tickets: {str(e)}")
        raise
    finally:
        conn.close()

def update_ticket_status(ticket_id, status):
    """Update the status of a ticket."""
    try:
        conn = sqlite3.connect("support_tickets.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE tickets SET status = ? WHERE ticket_id = ?", (status, ticket_id))
        conn.commit()
        logger.info(f"Updated ticket {ticket_id} to status {status}")
    except Exception as e:
        logger.error(f"Error updating ticket status: {str(e)}")
        raise
    finally:
        conn.close()