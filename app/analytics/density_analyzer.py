"""
density_analyzer.py
-------------------
Crowd Density Analysis Module
Features:
1. Analyze passenger crowd density
2. Generate overcrowding alerts
3. Configurable thresholds
4. Real-time optimized processing
5. Beginner-friendly clean OOP design
"""


class CrowdDensityAnalyzer:
    """
    Crowd Density Analyzer Class

    This class analyzes passenger count
    and classifies crowd density levels.
    """

    def __init__(
        self,
        low_threshold=10,
        medium_threshold=25,
        high_threshold=40
    ):
        """
        Initialize density thresholds.

        Args:
            low_threshold (int):
                Maximum passengers for LOW density

            medium_threshold (int):
                Maximum passengers for MEDIUM density

            high_threshold (int):
                Maximum passengers for HIGH density
        """

        self.low_threshold = low_threshold
        self.medium_threshold = medium_threshold
        self.high_threshold = high_threshold

    def analyze_density(self, passenger_count):
        """
        Analyze crowd density level.

        Args:
            passenger_count (int):
                Number of detected passengers

        Returns:
            dict:
                {
                    "density_level": str,
                    "alert_message": str
                }
        """

        # -------------------------------
        # Input Validation
        # -------------------------------

        if not isinstance(passenger_count, int):
            return {
                "density_level": "INVALID",
                "alert_message": "Passenger count must be integer"
            }

        if passenger_count < 0:
            return {
                "density_level": "INVALID",
                "alert_message": "Passenger count cannot be negative"
            }

        # -------------------------------
        # Density Classification
        # -------------------------------

        if passenger_count <= self.low_threshold:

            density_level = "LOW"

            alert_message = (
                "Crowd density is normal."
            )

        elif passenger_count <= self.medium_threshold:

            density_level = "MEDIUM"

            alert_message = (
                "Moderate crowd detected."
            )

        elif passenger_count <= self.high_threshold:

            density_level = "HIGH"

            alert_message = (
                "High crowd density detected."
            )

        else:

            density_level = "OVERCROWDED"

            alert_message = (
                "ALERT: Overcrowding detected!"
            )

        # -------------------------------
        # Return Analysis Result
        # -------------------------------

        return {
            "density_level": density_level,
            "alert_message": alert_message
        }