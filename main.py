# fixed_main.py
from fastapi import FastAPI, HTTPException, Depends, Query, Body

from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime
from config import Config
import mysql.connector
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="House Rental API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    """Get a new database connection."""
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        return conn
    except mysql.connector.Error as e:
        logger.error(f"Database connection error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database connection failed")

# Example Property Model
class PropertyBase:
    def __init__(self, property_name, address, city, property_type, monthly_rent):
        self.property_name = property_name
        self.address = address
        self.city = city
        self.property_type = property_type
        self.monthly_rent = monthly_rent

@app.post("/api/v1/properties/")
async def create_property(property_data: PropertyBase = Body(...)):

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        INSERT INTO properties (property_name, address, city, property_type, monthly_rent)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            property_data.property_name,
            property_data.address,
            property_data.city,
            property_data.property_type,
            property_data.monthly_rent
        )
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Property created successfully", "property_id": cursor.lastrowid}
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fixed_main:app", host="0.0.0.0", port=8000, reload=True)
