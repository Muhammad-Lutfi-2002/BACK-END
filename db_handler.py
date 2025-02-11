# db_handler.py
from mysql.connector import connect, Error
from fastapi import HTTPException, status
from config import get_db_config
import logging
from typing import Optional
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    filename='connection.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ConnectionStatus:
    def __init__(self):
        self.last_connection: Optional[datetime] = None
        self.connection_attempts: int = 0
        self.is_connected: bool = False
        self.last_error: Optional[str] = None
        
    def to_dict(self):
        return {
            "last_connection": self.last_connection.isoformat() if self.last_connection else None,
            "connection_attempts": self.connection_attempts,
            "is_connected": self.is_connected,
            "last_error": self.last_error
        }

class DatabaseConnection:
    def __init__(self):
        self.config = get_db_config()
        self.status = ConnectionStatus()
        
    def connect(self):
        """Establish database connection with status tracking"""
        self.status.connection_attempts += 1
        try:
            connection = connect(**self.config)
            if connection.is_connected():
                self.status.is_connected = True
                self.status.last_connection = datetime.now()
                self.status.last_error = None
                logger.info("Database connection established successfully")
                return connection
        except Error as e:
            self.status.is_connected = False
            self.status.last_error = str(e)
            logger.error(f"Database connection failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection failed"
            )

    def check_connection(self):
        """Check current connection status"""
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                return {
                    "status": "connected",
                    "message": "Database connection successful",
                    "connection_info": self.status.to_dict(),
                    "server_time": datetime.now().isoformat()
                }
        except Error as e:
            return {
                "status": "error",
                "message": str(e),
                "connection_info": self.status.to_dict(),
                "server_time": datetime.now().isoformat()
            }
