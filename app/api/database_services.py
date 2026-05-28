"""
database_service.py
--------------------
Database Service Layer

Project:
SmartRail Crowd Analytics and Passenger Safety System

Features:
1. Reusable database query functions
2. JSON-friendly responses
3. Safe database operations
4. Modular architecture
"""

import sqlite3


class DatabaseService:
    """
    Database Service Class
    """

    def __init__(
        self,
        database_path="/app/app/database/smartrail.db"
    ):
        """
        Initialize database service.

        Args:
            database_path:
                SQLite database path
        """

        self.database_path = database_path

    # -----------------------------------
    # DATABASE CONNECTION
    # -----------------------------------

    def get_connection(self):
        """
        Create SQLite connection.

        Returns:
            sqlite3.Connection
        """

        try:

            connection = sqlite3.connect(
                self.database_path
            )

            # Return rows as dictionaries
            connection.row_factory = (
                sqlite3.Row
            )

            return connection

        except sqlite3.Error as error:

            print(
                f"Database Connection Error: "
                f"{error}"
            )

            return None

    # -----------------------------------
    # CROWD ANALYTICS
    # -----------------------------------

    def get_crowd_analytics(
        self,
        limit=20
    ):
        """
        Fetch latest crowd analytics.

        Args:
            limit:
                Maximum rows to fetch

        Returns:
            list[dict]
        """

        query = """
        SELECT
            id,
            timestamp,
            passenger_count,
            density_level,
            alert_message
        FROM crowd_logs
        ORDER BY id DESC
        LIMIT ?
        """

        try:

            connection = self.get_connection()

            if connection is None:
                return []

            cursor = connection.cursor()

            cursor.execute(
                query,
                (limit,)
            )

            rows = cursor.fetchall()

            # Convert to JSON-friendly format
            data = [
                dict(row)
                for row in rows
            ]

            connection.close()

            return data

        except sqlite3.Error as error:

            print(
                f"Crowd Analytics Error: "
                f"{error}"
            )

            return []

    # -----------------------------------
    # ALERTS
    # -----------------------------------

    def get_alerts(
        self,
        limit=20
    ):
        """
        Fetch recent alerts.

        Args:
            limit:
                Maximum rows

        Returns:
            list[dict]
        """

        query = """
        SELECT
            id,
            timestamp,
            alert_type,
            alert_message
        FROM alerts
        ORDER BY id DESC
        LIMIT ?
        """

        try:

            connection = self.get_connection()

            if connection is None:
                return []

            cursor = connection.cursor()

            cursor.execute(
                query,
                (limit,)
            )

            rows = cursor.fetchall()

            data = [
                dict(row)
                for row in rows
            ]

            connection.close()

            return data

        except sqlite3.Error as error:

            print(
                f"Alerts Query Error: "
                f"{error}"
            )

            return []

    # -----------------------------------
    # MOVEMENT LOGS
    # -----------------------------------

    def get_movement_logs(
        self,
        limit=50
    ):
        """
        Fetch passenger movement logs.

        Args:
            limit:
                Maximum rows

        Returns:
            list[dict]
        """

        query = """
        SELECT
            id,
            timestamp,
            track_id,
            direction,
            speed,
            movement_status
        FROM movement_logs
        ORDER BY id DESC
        LIMIT ?
        """

        try:

            connection = self.get_connection()

            if connection is None:
                return []

            cursor = connection.cursor()

            cursor.execute(
                query,
                (limit,)
            )

            rows = cursor.fetchall()

            data = [
                dict(row)
                for row in rows
            ]

            connection.close()

            return data

        except sqlite3.Error as error:

            print(
                f"Movement Logs Error: "
                f"{error}"
            )

            return []

    # -----------------------------------
    # AGGRESSION EVENTS
    # -----------------------------------

    def get_aggression_events(
        self,
        limit=20
    ):
        """
        Fetch aggression events.

        Args:
            limit:
                Maximum rows

        Returns:
            list[dict]
        """

        query = """
        SELECT
            id,
            timestamp,
            aggression_score,
            suspicious_activity,
            alert_status
        FROM aggression_logs
        ORDER BY id DESC
        LIMIT ?
        """

        try:

            connection = self.get_connection()

            if connection is None:
                return []

            cursor = connection.cursor()

            cursor.execute(
                query,
                (limit,)
            )

            rows = cursor.fetchall()

            data = [
                dict(row)
                for row in rows
            ]

            connection.close()

            return data

        except sqlite3.Error as error:

            print(
                f"Aggression Events Error: "
                f"{error}"
            )

            return []