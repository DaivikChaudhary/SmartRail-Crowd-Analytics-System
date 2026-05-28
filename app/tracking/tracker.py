"""
tracker.py
-----------
ByteTrack-based Passenger Tracking Module
Features:
1. ByteTrack integration
2. Unique tracking IDs
3. Real-time person tracking
4. CPU-optimized processing
5. Lost-track handling
6. Beginner-friendly modular code
"""

import cv2
import supervision as sv


class PassengerTracker:
    """
    Passenger Tracking Class

    Uses ByteTrack for multi-object tracking.
    """

    def __init__(
        self,
        track_activation_threshold=0.25,
        lost_track_buffer=30,
        minimum_matching_threshold=0.8,
        frame_rate=30
    ):
        """
        Initialize ByteTrack tracker.

        Args:
            track_activation_threshold:
                Minimum confidence for tracking

            lost_track_buffer:
                Number of frames before removing lost track

            minimum_matching_threshold:
                Matching threshold for tracking

            frame_rate:
                Video FPS
        """

        self.tracker = sv.ByteTrack(
            track_activation_threshold=track_activation_threshold,
            lost_track_buffer=lost_track_buffer,
            minimum_matching_threshold=minimum_matching_threshold,
            frame_rate=frame_rate
        )

    def track_passengers(self, detections):
        """
        Track detected passengers.

        Args:
            detections:
                YOLO detections converted to supervision format

        Returns:
            tracked_detections
        """

        tracked_detections = (
            self.tracker.update_with_detections(
                detections
            )
        )

        return tracked_detections

    def draw_tracks(
        self,
        frame,
        tracked_detections
    ):
        """
        Draw tracking IDs and boxes.

        Args:
            frame:
                Current video frame

            tracked_detections:
                ByteTrack output

        Returns:
            frame
        """

        for detection in tracked_detections:

            # Extract tracking information
            x1, y1, x2, y2 = map(
                int,
                detection[0]
            )

            track_id = int(detection[4])

            # Draw bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                2
            )

            # Draw tracking ID
            cv2.putText(
                frame,
                f"ID: {track_id}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0, 0),
                2
            )

        return frame