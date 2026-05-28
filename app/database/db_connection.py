"""
db_connection.py
----------------
SQLite Database Connection Module

Features:
1. Automatic database creation
2. Automatic table initialization
3. Real-time optimized inserts
4. Safe exception handling
5. Modular clean architecture
"""

import sqlite3
from sqlite3 import Error
import os

import os
import sqlite3

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "..",
    "database",
    "smartrail.db"
)

DATABASE_PATH = os.path.abspath(DATABASE_PATH)

print("REAL DATABASE PATH =", DATABASE_PATH)
print("DB EXISTS =", os.path.exists(DATABASE_PATH))

connection = sqlite3.connect(
    DATABASE_PATH,
    check_same_thread=False,
    timeout=30
)

class DatabaseManager:
    """
    Database Manager Class
    """

    def __init__(
        self,
        database_path=DATABASE_PATH
    ):
        """
        Initialize database manager.

        Args:
            database_path:
                SQLite database file path
        """
        
        self.database_path = database_path

        self.connection = None

        # Initialize database
        self.initialize_database()

    def connect(self):
        """
        Create database connection.

        Returns:
            sqlite3.Connection
        """
        
        try:
            
            os.makedirs(
                os.path.dirname(self.database_path),
                exist_ok=True
            )

            self.connection = sqlite3.connect(
                self.database_path,
                check_same_thread=False,
                timeout=30
            )
            return self.connection

        except Error as error:

            print(
                f"Database Connection Error: {error}"
            )

            return None

    def execute_query(
        self,
        query,
        parameters=()
    ):
        """
        Execute INSERT/UPDATE/DELETE query.

        Args:
            query:
                SQL query

            parameters:
                Query parameters
        """

        try:

            connection = self.connect()

            if connection is None:
                return

            cursor = connection.cursor()

            cursor.execute(
                query,
                parameters
            )

            connection.commit()

        except Error as error:

            print(
                f"Database Query Error: {error}"
            )

    def fetch_query(
        self,
        query,
        parameters=()
    ):
        """
        Execute SELECT query.

        Returns:
            query results
        """

        try:

            connection = self.connect()

            if connection is None:
                return []

            cursor = connection.cursor()

            cursor.execute(
                query,
                parameters
            )

            results = cursor.fetchall()

            return results

        except Error as error:

            print(
                f"Database Fetch Error: {error}"
            )

            return []

    def create_tables(self):
        """
        Create required database tables.
        """

        # -----------------------------------
        # Crowd Logs Table
        # -----------------------------------

        crowd_logs_table = """
        CREATE TABLE IF NOT EXISTS crowd_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            passenger_count INTEGER,

            density_level TEXT,

            alert_message TEXT
        )
        """

        # -----------------------------------
        # Alerts Table
        # -----------------------------------

        alerts_table = """
        CREATE TABLE IF NOT EXISTS alerts (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            alert_type TEXT,

            alert_message TEXT
        )
        """

        # -----------------------------------
        # Movement Logs Table
        # -----------------------------------

        movement_logs_table = """
        CREATE TABLE IF NOT EXISTS movement_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            track_id INTEGER,

            direction TEXT,

            speed REAL,

            movement_status TEXT
        )
        """

        # -----------------------------------
        # Aggression Logs Table
        # -----------------------------------

        aggression_logs_table = """
        CREATE TABLE IF NOT EXISTS aggression_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            aggression_score REAL,

            suspicious_activity INTEGER,

            alert_status TEXT
        )
        """

        # Create all tables
        self.execute_query(
            crowd_logs_table
        )

        self.execute_query(
            alerts_table
        )

        self.execute_query(
            movement_logs_table
        )

        self.execute_query(
            aggression_logs_table
        )

    def initialize_database(self):
        """
        Initialize complete database system.
        """

        print(
            "Initializing SmartRail Database..."
        )

        self.connect()

        self.create_tables()

        print(
            "Database initialized successfully."
        )

    # -----------------------------------
    # CROWD LOGGING
    # -----------------------------------

    def insert_crowd_log(
        self,
        passenger_count,
        density_level,
        alert_message
    ):
        """
        Insert crowd analytics log.
        """

        query = """
        INSERT INTO crowd_logs (
            passenger_count,
            density_level,
            alert_message
        )
        VALUES (?, ?, ?)
        """

        self.execute_query(
            query,
            (
                passenger_count,
                density_level,
                alert_message
            )
        )

    # -----------------------------------
    # ALERT LOGGING
    # -----------------------------------

    def insert_alert(
        self,
        alert_type,
        alert_message
    ):
        """
        Insert alert log.
        """

        query = """
        INSERT INTO alerts (
            alert_type,
            alert_message
        )
        VALUES (?, ?)
        """

        self.execute_query(
            query,
            (
                alert_type,
                alert_message
            )
        )

    # -----------------------------------
    # MOVEMENT LOGGING
    # -----------------------------------

    def insert_movement_log(
        self,
        track_id,
        direction,
        speed,
        movement_status
    ):
        """
        Insert movement analytics log.
        """

        query = """
        INSERT INTO movement_logs (
            track_id,
            direction,
            speed,
            movement_status
        )
        VALUES (?, ?, ?, ?)
        """

        self.execute_query(
            query,
            (
                track_id,
                direction,
                speed,
                movement_status
            )
        )

    # -----------------------------------
    # AGGRESSION LOGGING
    # -----------------------------------

    def insert_aggression_log(
        self,
        aggression_score,
        suspicious_activity,
        alert_status
    ):
        """
        Insert aggression analytics log.
        """

        query = """
        INSERT INTO aggression_logs (
            aggression_score,
            suspicious_activity,
            alert_status
        )
        VALUES (?, ?, ?)
        """

        self.execute_query(
            query,
            (
                aggression_score,
                int(suspicious_activity),
                alert_status
            )
        )

    def close_connection(self):
        """
        Safely close database connection.
        """

        try:

            if self.connection:

                self.connection.close()

                print(
                    "Database connection closed."
                )

        except Error as error:

            print(
                f"Database Close Error: {error}"
            )