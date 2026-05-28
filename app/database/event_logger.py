"""
event_logger.py
----------------
SmartRail Event Logging System

Features:
1. Crowd analytics logging
2. Alert logging
3. Movement analytics logging
4. Aggression event logging
5. Safe database operations
6. Reusable logging functions
"""

from app.database.db_connection import DatabaseManager

class EventLogger:
    """
    Event Logger Class
    """

    def __init__(self):
        """
        Initialize logger system.
        """

        try:

            # Initialize database manager
            self.db_manager = (
                DatabaseManager()
            )

            print(
                "Event Logger Initialized."
            )

        except Exception as error:

            print(
                f"Logger Initialization Error: {error}"
            )

    # -----------------------------------
    # CROWD ANALYTICS LOGGING
    # -----------------------------------

    def log_crowd_analytics(
        self,
        passenger_count,
        density_level,
        alert_message
    ):
        """
        Save crowd analytics.

        Args:
            passenger_count:
                Total detected passengers

            density_level:
                LOW/MEDIUM/HIGH

            alert_message:
                Crowd alert message
        """

        try:

            self.db_manager.insert_crowd_log(
                passenger_count,
                density_level,
                alert_message
            )

        except Exception as error:

            print(
                f"Crowd Logging Error: {error}"
            )

    # -----------------------------------
    # ALERT LOGGING
    # -----------------------------------

    def log_alert(
        self,
        alert_type,
        alert_message
    ):
        """
        Save system alerts.

        Args:
            alert_type:
                Alert category

            alert_message:
                Alert description
        """

        try:

            self.db_manager.insert_alert(
                alert_type,
                alert_message
            )

        except Exception as error:

            print(
                f"Alert Logging Error: {error}"
            )

    # -----------------------------------
    # MOVEMENT ANALYTICS LOGGING
    # -----------------------------------

    def log_movement(
        self,
        track_id,
        direction,
        speed,
        movement_status
    ):
        """
        Save movement analytics.

        Args:
            track_id:
                Passenger tracking ID

            direction:
                LEFT/RIGHT/UP/DOWN

            speed:
                Estimated movement speed

            movement_status:
                MOVING/STATIONARY
        """

        try:

            self.db_manager.insert_movement_log(
                track_id,
                direction,
                speed,
                movement_status
            )

        except Exception as error:

            print(
                f"Movement Logging Error: {error}"
            )

    # -----------------------------------
    # AGGRESSION EVENT LOGGING
    # -----------------------------------

    def log_aggression_event(
        self,
        aggression_score,
        suspicious_activity,
        alert_status
    ):
        """
        Save aggression analytics.

        Args:
            aggression_score:
                Suspicion score

            suspicious_activity:
                Boolean flag

            alert_status:
                Alert type
        """

        try:

            self.db_manager.insert_aggression_log(
                aggression_score,
                suspicious_activity,
                alert_status
            )

        except Exception as error:

            print(
                f"Aggression Logging Error: {error}"
            )

    # -----------------------------------
    # SYSTEM SHUTDOWN
    # -----------------------------------

    def close_logger(self):
        """
        Safely close database connection.
        """

        try:

            self.db_manager.close_connection()

            print(
                "Event Logger Closed."
            )

        except Exception as error:

            print(
                f"Logger Close Error: {error}"
            )