"""
movement_analyzer.py
--------------------
Passenger Movement Analytics Module
Features:
1. Track centroid history
2. Calculate movement direction
3. Detect stationary passengers
4. Estimate movement speed
5. Maintain trajectory history
6. CPU-optimized real-time analytics
"""

import math
from collections import defaultdict, deque


class MovementAnalyzer:
    """
    Movement Analysis Class

    Tracks passenger movement patterns
    using centroid trajectory history.
    """

    def __init__(
        self,
        max_history=20,
        stationary_threshold=5
    ):
        """
        Initialize analyzer.

        Args:
            max_history:
                Maximum trajectory points stored

            stationary_threshold:
                Minimum movement distance
                required to consider passenger moving
        """

        # Store centroid history for each ID
        self.trajectory_history = defaultdict(
            lambda: deque(maxlen=max_history)
        )

        self.stationary_threshold = (
            stationary_threshold
        )

    def calculate_centroid(
        self,
        x1,
        y1,
        x2,
        y2
    ):
        """
        Calculate bounding box centroid.

        Returns:
            tuple: (cx, cy)
        """

        cx = int((x1 + x2) / 2)

        cy = int((y1 + y2) / 2)

        return cx, cy

    def update_trajectory(
        self,
        track_id,
        centroid
    ):
        """
        Update passenger trajectory history.
        """

        self.trajectory_history[
            track_id
        ].append(centroid)

    def calculate_speed(
        self,
        previous_point,
        current_point
    ):
        """
        Estimate movement speed using
        Euclidean distance.
        """

        x1, y1 = previous_point
        x2, y2 = current_point

        speed = math.sqrt(
            (x2 - x1) ** 2 +
            (y2 - y1) ** 2
        )

        return round(speed, 2)

    def calculate_direction(
        self,
        previous_point,
        current_point
    ):
        """
        Estimate movement direction.
        """

        x1, y1 = previous_point
        x2, y2 = current_point

        dx = x2 - x1
        dy = y2 - y1

        # Horizontal movement
        if abs(dx) > abs(dy):

            if dx > 0:
                return "RIGHT"

            return "LEFT"

        # Vertical movement
        else:

            if dy > 0:
                return "DOWN"

            return "UP"

    def analyze_movement(
        self,
        track_id,
        bbox
    ):
        """
        Analyze passenger movement.

        Args:
            track_id:
                Unique passenger ID

            bbox:
                Bounding box coordinates

        Returns:
            dict:
                {
                    "direction": str,
                    "movement_status": str,
                    "speed": float,
                    "trajectory": list
                }
        """

        try:

            # Extract coordinates
            x1, y1, x2, y2 = bbox

            # Calculate centroid
            centroid = self.calculate_centroid(
                x1,
                y1,
                x2,
                y2
            )

            # Update trajectory
            self.update_trajectory(
                track_id,
                centroid
            )

            trajectory = (
                self.trajectory_history[
                    track_id
                ]
            )

            # Not enough points yet
            if len(trajectory) < 2:

                return {
                    "direction": "UNKNOWN",
                    "movement_status": "INITIALIZING",
                    "speed": 0.0,
                    "trajectory": list(trajectory)
                }

            # Get previous and current points
            previous_point = trajectory[-2]

            current_point = trajectory[-1]

            # Calculate speed
            speed = self.calculate_speed(
                previous_point,
                current_point
            )

            # Calculate direction
            direction = self.calculate_direction(
                previous_point,
                current_point
            )

            # Detect stationary passengers
            if speed < self.stationary_threshold:

                movement_status = "STATIONARY"

            else:

                movement_status = "MOVING"

            return {
                "direction": direction,
                "movement_status": movement_status,
                "speed": speed,
                "trajectory": list(trajectory)
            }

        except Exception as error:

            return {
                "direction": "ERROR",
                "movement_status": str(error),
                "speed": 0.0,
                "trajectory": []
            }