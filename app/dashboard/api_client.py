"""
api_client.py
---------------
FastAPI Client Module

Project:
SmartRail Crowd Analytics and Passenger Safety System

Features:
1. Connect to FastAPI backend
2. Fetch analytics data
3. Fetch alerts
4. Fetch movement logs
5. Fetch aggression events
6. Safe API handling
"""

import requests


class SmartRailAPIClient:
    """
    SmartRail FastAPI Client
    """

    def __init__(
        self,
        base_url="http://127.0.0.1:8000"
    ):
        """
        Initialize API client.

        Args:
            base_url:
                FastAPI backend URL
        """

        self.base_url = base_url

    # -----------------------------------
    # GENERIC GET REQUEST
    # -----------------------------------

    def send_get_request(
        self,
        endpoint
    ):
        """
        Send GET request safely.

        Args:
            endpoint:
                API endpoint

        Returns:
            JSON response
        """

        try:

            url = (
                f"{self.base_url}"
                f"{endpoint}"
            )

            response = requests.get(
                url,
                timeout=10
            )

            # Raise HTTP errors
            response.raise_for_status()

            return response.json()

        except requests.exceptions.ConnectionError:

            print(
                "API Connection Error:"
                " Backend server offline."
            )

            return []

        except requests.exceptions.Timeout:

            print(
                "API Timeout Error"
            )

            return []

        except requests.exceptions.HTTPError as error:

            print(
                f"HTTP Error: {error}"
            )

            return []

        except Exception as error:

            print(
                f"Unexpected API Error: "
                f"{error}"
            )

            return []

    # -----------------------------------
    # CROWD ANALYTICS
    # -----------------------------------

    def get_analytics(self):
        """
        Fetch crowd analytics.

        Returns:
            list[dict]
        """

        return self.send_get_request(
            "/analytics"
        )

    # -----------------------------------
    # ALERTS
    # -----------------------------------

    def get_alerts(self):
        """
        Fetch alerts.

        Returns:
            list[dict]
        """

        return self.send_get_request(
            "/alerts"
        )

    # -----------------------------------
    # MOVEMENT LOGS
    # -----------------------------------

    def get_movement_logs(self):
        """
        Fetch movement analytics.

        Returns:
            list[dict]
        """

        return self.send_get_request(
            "/movement"
        )

    # -----------------------------------
    # AGGRESSION EVENTS
    # -----------------------------------

    def get_aggression_events(self):
        """
        Fetch aggression analytics.

        Returns:
            list[dict]
        """

        return self.send_get_request(
            "/aggression-events"
        )

    # -----------------------------------
    # HEALTH CHECK
    # -----------------------------------

    def check_health(self):
        """
        Verify API server health.

        Returns:
            dict
        """

        return self.send_get_request(
            "/health"
        )


# -----------------------------------
# TEST CLIENT
# -----------------------------------

if __name__ == "__main__":

    # Create client
    client = SmartRailAPIClient()

    print("\nAPI Health:\n")

    print(
        client.check_health()
    )

    print("\nCrowd Analytics:\n")

    print(
        client.get_analytics()
    )

    print("\nAlerts:\n")

    print(
        client.get_alerts()
    )

    print("\nMovement Logs:\n")

    print(
        client.get_movement_logs()
    )

    print("\nAggression Events:\n")

    print(
        client.get_aggression_events()
    )