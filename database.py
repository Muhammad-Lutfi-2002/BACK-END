# database.py
import mysql.connector
from mysql.connector import Error
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.connection = None
        self._connect()

    def _connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME
            )
            if self.connection.is_connected():
                logger.info("✅ Successfully connected to database")
        except Error as e:
            logger.error(f"❌ Error connecting to database: {e}")
            raise

    def get_connection(self):
        try:
            if self.connection is None or not self.connection.is_connected():
                logger.info("Reconnecting to database...")
                self._connect()
            return self.connection
        except Error as e:
            logger.error(f"Failed to get database connection: {e}")
            raise

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("🔌 Database connection closed")

    def __enter__(self):
        return self.get_connection()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()