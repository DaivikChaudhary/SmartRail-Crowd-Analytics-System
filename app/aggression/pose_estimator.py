"""
pose_estimator.py
-----------------
Pose Estimation Module

Features:
1. Human pose estimation
2. Body landmark extraction
3. Wrist/elbow/shoulder tracking
4. Pose skeleton visualization
5. Real-time CPU optimization
"""

import cv2
import mediapipe as mp


class PoseEstimator:
    """
    Pose Estimation Class
    """

    def __init__(
        self,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ):
        """
        Initialize MediaPipe Pose.

        Args:
            min_detection_confidence:
                Minimum confidence for detection

            min_tracking_confidence:
                Minimum confidence for tracking
        """

        # Initialize MediaPipe Pose
        self.mp_pose = mp.solutions.pose

        self.mp_drawing = (
            mp.solutions.drawing_utils
        )

        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=0,
            smooth_landmarks=True,
            min_detection_confidence=(
                min_detection_confidence
            ),
            min_tracking_confidence=(
                min_tracking_confidence
            )
        )

    def process_frame(
        self,
        frame
    ):
        """
        Process frame for pose estimation.

        Args:
            frame:
                Input video frame

        Returns:
            results:
                MediaPipe pose results
        """

        # Convert BGR → RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Process pose estimation
        results = self.pose.process(
            rgb_frame
        )

        return results

    def extract_landmarks(
        self,
        frame,
        results
    ):
        """
        Extract important body landmarks.

        Returns:
            dict:
                landmark coordinates
        """

        landmark_data = {}

        try:

            if not results.pose_landmarks:

                return landmark_data

            height, width, _ = frame.shape

            landmarks = (
                results.pose_landmarks.landmark
            )

            # -----------------------------------
            # LEFT SIDE
            # -----------------------------------

            landmark_data["left_shoulder"] = (
                int(
                    landmarks[
                        self.mp_pose.PoseLandmark.LEFT_SHOULDER
                    ].x * width
                ),
                int(
                    landmarks[
                        self.mp_pose.PoseLandmark.LEFT_SHOULDER
                    ].y * height
                )
            )

            landmark_data["left_elbow"] = (
                int(
                    landmarks[
                        self.mp_pose.PoseLandmark.LEFT_ELBOW
                    ].x * width
                ),
                int(
                    landmarks[
                        self.mp_pose.PoseLandmark.LEFT_ELBOW
                    ].y * height
                )
            )

            landmark_data["left_wrist"] = (
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

            # -----------------------------------
            # RIGHT SIDE
            # -----------------------------------

            landmark_data["right_shoulder"] = (
                int(
                    landmarks[
                        self.mp_pose.PoseLandmark.RIGHT_SHOULDER
                    ].x * width
                ),
                int(
                    landmarks[
                        self.mp_pose.PoseLandmark.RIGHT_SHOULDER
                    ].y * height
                )
            )

            landmark_data["right_elbow"] = (
                int(
                    landmarks[
                        self.mp_pose.PoseLandmark.RIGHT_ELBOW
                    ].x * width
                ),
                int(
                    landmarks[
                        self.mp_pose.PoseLandmark.RIGHT_ELBOW
                    ].y * height
                )
            )

            landmark_data["right_wrist"] = (
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

            return landmark_data

        except Exception:

            return {}

    def draw_pose(
        self,
        frame,
        results
    ):
        """
        Draw pose skeleton on frame.

        Args:
            frame:
                Current frame

            results:
                MediaPipe pose results

        Returns:
            frame
        """

        try:

            if results.pose_landmarks:

                self.mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS
                )

            return frame

        except Exception:

            return frame

    def estimate_pose(
        self,
        frame
    ):
        """
        Complete pose estimation pipeline.

        Args:
            frame:
                Current video frame

        Returns:
            frame:
                Updated frame

            landmark_data:
                Extracted landmarks
        """

        try:

            # Process frame
            results = self.process_frame(
                frame
            )

            # Draw pose skeleton
            frame = self.draw_pose(
                frame,
                results
            )

            # Extract landmarks
            landmark_data = (
                self.extract_landmarks(
                    frame,
                    results
                )
            )

            return frame, landmark_data

        except Exception:

            return frame, {}