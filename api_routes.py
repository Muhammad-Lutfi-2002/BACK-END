# api_routes.py
from fastapi import APIRouter, Depends
from typing import Dict

router = APIRouter()
connection_manager = ConnectionManager()

@router.get("/health", response_model=Dict, methods=["GET"])

async def check_health():
    """Check database connection health"""
    return connection_manager.get_connection_status()

@router.get("/connection-stats", response_model=Dict, methods=["GET"])

async def get_connection_stats():
    """Get detailed connection statistics"""
    status = connection_manager.db.status
    return {
        "status": status.to_dict(),
        "database_config": {
            "host": connection_manager.db.config["host"],
            "database": connection_manager.db.config["database"],
            "port": connection_manager.db.config["port"]
        }
    }
