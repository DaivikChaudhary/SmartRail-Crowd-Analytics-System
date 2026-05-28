"""
detector.py
------------
Handles YOLOv8 passenger detection
"""

from ultralytics import YOLO
import cv2


class PassengerDetector:
    """
    Passenger Detection Class
    """

    def __init__(
        self,
        model_path="yolov8n.pt",
        confidence_threshold=0.5
    ):
        """
        Initialize YOLO model
        """

        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold

    def detect_passengers(self, frame):
        """
        Detect only persons in frame

        Args:
            frame: Video frame

        Returns:
            frame
            passenger_count
        """

        passenger_count = 0

        # Run YOLO prediction
        results = self.model(frame, verbose=False)

        # Loop through detections
        for result in results:

            boxes = result.boxes

            for box in boxes:

                # Class ID
                class_id = int(box.cls[0])

                # COCO class 0 = person
                if class_id == 0:

                    confidence = float(box.conf[0])

                    # Confidence filtering
                    if confidence >= self.confidence_threshold:

                        passenger_count += 1

                        # Bounding box coordinates
                        x1, y1, x2, y2 = map(
                            int,
                            box.xyxy[0]
                        )

                        # Draw rectangle
                        cv2.rectangle(
                            frame,
                            (x1, y1),
                            (x2, y2),
                            (0, 255, 0),
                            2
                        )

                        # Confidence label
                        label = f"Passenger {confidence:.2f}"

                        cv2.putText(
                            frame,
                            label,
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 255, 0),
                            2
                        )

        return frame, passenger_count