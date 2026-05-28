"""
aggression_detector.py
-----------------------
Aggression Detection Module

Features:
1. Body landmark movement analysis
2. Rapid arm movement detection
3. Motion intensity estimation
4. Close interaction analysis
5. Heuristic aggression scoring
6. Real-time CPU optimization
"""

import cv2
import math
import numpy as np
import mediapipe as mp


class AggressionDetector:
    """
    Aggression Detection Class
    """

    def __init__(
        self,
        motion_threshold=40,
        arm_speed_threshold=35,
        proximity_threshold=120,
        aggression_threshold=70
    ):
        """
        Initialize aggression detector.

        Args:
            motion_threshold:
                Threshold for abnormal movement

            arm_speed_threshold:
                Threshold for rapid arm movement

            proximity_threshold:
                Distance threshold between passengers

            aggression_threshold:
                Final aggression score threshold
        """

        # MediaPipe Pose
        self.mp_pose = mp.solutions.pose

        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # Thresholds
        self.motion_threshold = motion_threshold

        self.arm_speed_threshold = arm_speed_threshold

        self.proximity_threshold = proximity_threshold

        self.aggression_threshold = aggression_threshold

        # Store previous landmarks
        self.previous_landmarks = {}

    def calculate_distance(
        self,
        point1,
        point2
    ):
        """
        Calculate Euclidean distance.
        """

        return math.sqrt(
            (point2[0] - point1[0]) ** 2 +
            (point2[1] - point1[1]) ** 2
        )

    def extract_arm_landmarks(
        self,
        landmarks,
        width,
        height
    ):
        """
        Extract arm keypoints.

        Returns:
            dict
        """

        try:

            left_wrist = (
                int(
                    landmarks[
                        self.mp_pose.PoseLandmark.LEFT_WRIST
                    ].x * width
                ),
                int(
                    landmarks[
                        self.mp_pose.PoseLandmark.LEFT_WRIST
                    ].y * height
                )
            )

            right_wrist = (
                int(
                    landmarks[
                        self.mp_pose.PoseLandmark.RIGHT_WRIST
                    ].x * width
                ),
                int(
                    landmarks[
                        self.mp_pose.PoseLandmark.RIGHT_WRIST
                    ].y * height
                )
            )

            return {
                "left_wrist": left_wrist,
                "right_wrist": right_wrist
            }

        except Exception:

            return None

    def calculate_arm_speed(
        self,
        current_points,
        previous_points
    ):
        """
        Estimate arm movement speed.
        """

        if previous_points is None:
            return 0

        left_speed = self.calculate_distance(
            current_points["left_wrist"],
            previous_points["left_wrist"]
        )

        right_speed = self.calculate_distance(
            current_points["right_wrist"],
            previous_points["right_wrist"]
        )

        return max(left_speed, right_speed)

    def analyze_frame(
        self,
        frame,
        passenger_boxes
    ):
        """
        Analyze aggression activity.

        Args:
            frame:
                Current video frame

            passenger_boxes:
                List of tracked passenger boxes

        Returns:
            dict
        """

        aggression_score = 0

        suspicious_activity = False

        alert_status = "NORMAL"

        try:

            frame_rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            results = self.pose.process(
                frame_rgb
            )

            # No pose detected
            if not results.pose_landmarks:

                return {
                    "aggression_score": 0,
                    "alert_status": "NO_POSE",
                    "suspicious_activity": False
                }

            height, width, _ = frame.shape

            landmarks = (
                results.pose_landmarks.landmark
            )

            # Extract arm keypoints
            arm_points = self.extract_arm_landmarks(
                landmarks,
                width,
                height
            )

            if arm_points is None:

                return {
                    "aggression_score": 0,
                    "alert_status": "INVALID_POSE",
                    "suspicious_activity": False
                }

            # -----------------------------------
            # Rapid Arm Movement Detection
            # -----------------------------------

            arm_speed = self.calculate_arm_speed(
                arm_points,
                self.previous_landmarks.get(
                    "arms"
                )
            )

            if arm_speed > self.arm_speed_threshold:

                aggression_score += 40

            # Store current landmarks
            self.previous_landmarks[
                "arms"
            ] = arm_points

            # -----------------------------------
            # Close Passenger Interaction
            # -----------------------------------

            for i in range(len(passenger_boxes)):

                for j in range(i + 1, len(passenger_boxes)):

                    box1 = passenger_boxes[i]
                    box2 = passenger_boxes[j]

                    cx1 = int(
                        (box1[0] + box1[2]) / 2
                    )

                    cy1 = int(
                        (box1[1] + box1[3]) / 2
                    )

                    cx2 = int(
                        (box2[0] + box2[2]) / 2
                    )

                    cy2 = int(
                        (box2[1] + box2[3]) / 2
                    )

                    distance = self.calculate_distance(
                        (cx1, cy1),
                        (cx2, cy2)
                    )

                    if distance < self.proximity_threshold:

                        aggression_score += 15

            # -----------------------------------
            # Abnormal Motion Intensity
            # -----------------------------------

            if arm_speed > self.motion_threshold:

                aggression_score += 30

            # -----------------------------------
            # Final Decision
            # -----------------------------------

            if aggression_score >= self.aggression_threshold:

                suspicious_activity = True

                alert_status = "AGGRESSION_ALERT"

            return {
                "aggression_score": aggression_score,
                "alert_status": alert_status,
                "suspicious_activity": suspicious_activity
            }

        except Exception:

            return {
                "aggression_score": 0,
                "alert_status": "ERROR",
                "suspicious_activity": False
            }