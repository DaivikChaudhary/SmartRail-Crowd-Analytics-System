"""
routes.py
----------
FastAPI Routes Module

Project:
SmartRail Crowd Analytics and Passenger Safety System

Features:
1. Crowd analytics API
2. Alert history API
3. Movement analytics API
4. Aggression event API
5. Health check API
"""

from fastapi import APIRouter
from fastapi import HTTPException

from app.api.database_services import DatabaseService

from app.api.schemas import (
    AnalyticsResponse,
    AlertResponse,
    MovementResponse,
    AggressionResponse,
    HealthResponse
)

# Create API router
router = APIRouter()

# Initialize database service
database_service = DatabaseService()


# -----------------------------------
# HEALTH CHECK ROUTE
# -----------------------------------

@router.get(
    "/health",
    response_model=HealthResponse
)
def health_check():
    """
    Health check endpoint.

    Used to verify:
    - API status
    - server availability
    """

    return {
        "status": "OK",
        "message": "SmartRail API Running"
    }


# -----------------------------------
# CROWD ANALYTICS ROUTE
# -----------------------------------

@router.get(
    "/analytics",
    response_model=list[AnalyticsResponse]
)
def get_analytics():
    """
    Fetch crowd analytics data.
    """

    try:

        analytics_data = (
            database_service
            .get_crowd_analytics()
        )

        return analytics_data

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Analytics API Error: "
                f"{error}"
            )
        )


# -----------------------------------
# ALERTS ROUTE
# -----------------------------------

@router.get(
    "/alerts",
    response_model=list[AlertResponse]
)
def get_alerts():
    """
    Fetch system alerts.
    """

    try:

        alerts = (
            database_service
            .get_alerts()
        )

        return alerts

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Alerts API Error: "
                f"{error}"
            )
        )


# -----------------------------------
# MOVEMENT ANALYTICS ROUTE
# -----------------------------------

@router.get(
    "/movement",
    response_model=list[MovementResponse]
)
def get_movement_logs():
    """
    Fetch movement analytics.
    """

    try:

        movement_logs = (
            database_service
            .get_movement_logs()
        )

        return movement_logs

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Movement API Error: "
                f"{error}"
            )
        )


# -----------------------------------
# AGGRESSION EVENTS ROUTE
# -----------------------------------

@router.get(
    "/aggression-events",
    response_model=list[AggressionResponse]
)
def get_aggression_events():
    """
    Fetch aggression analytics.
    """

    try:

        aggression_events = (
            database_service
            .get_aggression_events()
        )

        return aggression_events

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Aggression API Error: "
                f"{error}"
            )
        )