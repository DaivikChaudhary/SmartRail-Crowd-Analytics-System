"""
schemas.py
------------
Pydantic Response Schemas

Project:
SmartRail Crowd Analytics and Passenger Safety System

Features:
1. Crowd analytics schemas
2. Alert schemas
3. Movement analytics schemas
4. Aggression event schemas
5. API response validation
"""

from typing import Optional

from pydantic import BaseModel


# -----------------------------------
# HEALTH RESPONSE
# -----------------------------------

class HealthResponse(BaseModel):
    """
    Health check response schema.
    """

    status: str

    message: str


# -----------------------------------
# CROWD ANALYTICS RESPONSE
# -----------------------------------

class AnalyticsResponse(BaseModel):
    """
    Crowd analytics response schema.
    """

    id: int

    timestamp: str

    passenger_count: int

    density_level: str

    alert_message: str


# -----------------------------------
# ALERT RESPONSE
# -----------------------------------

class AlertResponse(BaseModel):
    """
    System alert response schema.
    """

    id: int

    timestamp: str

    alert_type: str

    alert_message: str


# -----------------------------------
# MOVEMENT ANALYTICS RESPONSE
# -----------------------------------

class MovementResponse(BaseModel):
    """
    Passenger movement analytics schema.
    """

    id: int

    timestamp: str

    track_id: int

    direction: str

    speed: float

    movement_status: str


# -----------------------------------
# AGGRESSION EVENT RESPONSE
# -----------------------------------

class AggressionResponse(BaseModel):
    """
    Aggression event response schema.
    """

    id: int

    timestamp: str

    aggression_score: float

    suspicious_activity: int

    alert_status: str