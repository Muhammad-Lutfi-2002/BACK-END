# connection_manager.py
from contextlib import contextmanager

class ConnectionManager:
    def __init__(self):
        self.db = DatabaseConnection()
        
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        connection = None
        try:
            connection = self.db.connect()
            yield connection
        finally:
            if connection and connection.is_connected():
                connection.close()
                logger.info("Database connection closed")

    def get_connection_status(self):
        """Get current connection status"""
        return self.db.check_connection()