import cv2
import time
from app.detection.detector import PassengerDetector
from app.detection.utils import resize_frame, calculate_fps
from app.analytics.density_analyzer import CrowdDensityAnalyzer
from app.tracking.tracker import PassengerTracker
import supervision as sv
from app.movement.movement_analyzer import MovementAnalyzer
from app.aggression.aggression_detector import AggressionDetector
from app.aggression.pose_estimator import PoseEstimator
import os
import time
import warnings
from app.database.event_logger import EventLogger

# Suppress unnecessary warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

warnings.filterwarnings("ignore")


def load_video(source):
    """
    Load video source safely.
    """

    cap = cv2.VideoCapture(source)

    if not cap.isOpened():

        raise Exception(
            "Unable to open video source"
        )

    return cap


def get_density_color(density_level):
    """
    Return color based on density level.
    """

    colors = {
        "LOW": (0, 255, 0),
        "MEDIUM": (0, 255, 255),
        "HIGH": (0, 165, 255),

        "OVERCROWDED": (0, 0, 255),
        "INVALID": (255, 255, 255)
    }

    return colors.get(
        density_level,
        (255, 255, 255)
    )


def main():

    # -----------------------------------
    # CONFIGURATION
    # -----------------------------------

    source = r"videos/test_video.mp4"

    confidence_threshold = 0.3

    frame_skip = 2

    # Log every 5 seconds
    log_interval = 5

    # -----------------------------------

    try:

        # Initialize detector
        detector = PassengerDetector(
            confidence_threshold=confidence_threshold
        )

        # Initialize tracker
        tracker = PassengerTracker()

        # Initialize crowd analyzer
        density_analyzer = (
            CrowdDensityAnalyzer(
                low_threshold=3,
                medium_threshold=6,
                high_threshold=10
            )
        )

        # Initialize movement analyzer
        movement_analyzer = (
            MovementAnalyzer()
        )

        # Initialize pose estimator
        pose_estimator = (
            PoseEstimator()
        )

        # Initialize aggression detector
        aggression_detector = (
            AggressionDetector()
        )

        # Initialize event logger
        event_logger = EventLogger()

        # Load video
        cap = load_video(source)

        # -----------------------------------
        # Create Resizable OpenCV Window
        # -----------------------------------

        cv2.namedWindow(
            "SmartRail AI Surveillance",
            cv2.WINDOW_NORMAL
        )

        cv2.resizeWindow(
            "SmartRail AI Surveillance",
            1000,
            600
        )


        print("SmartRail AI System Started...")
        
        previous_time = 0

        frame_count = 0

        # Logging timer
        last_log_time = time.time()

        while True:

            success, frame = cap.read()

            if not success:
                print("Video completed.")
                break

            frame_count += 1

            # -----------------------------------
            # Frame Skipping for CPU Optimization
            # -----------------------------------

            if frame_count % frame_skip != 0:
                continue

            # Resize frame
            frame = resize_frame(frame)

            # -----------------------------------
            # YOLO Detection
            # -----------------------------------

            results = detector.model(
                frame,
                imgsz=640,
                verbose=False
            )

            detections = sv.Detections.from_ultralytics(
                results[0]
            )

            # Keep only person detections
            person_detections = detections[
                detections.class_id == 0
            ]

            passenger_count = len(
                person_detections
            )

            # -----------------------------------
            # ByteTrack Tracking
            # -----------------------------------

            tracked_detections = (
                tracker.track_passengers(
                    person_detections
                )
            )

            passenger_boxes = []

            # -----------------------------------
            # Logging Timer Control
            # -----------------------------------

            current_time = time.time()

            should_log = (
                current_time - last_log_time
                >= log_interval
            )

            # -----------------------------------
            # Process Each Passenger
            # -----------------------------------

            for detection in tracked_detections:

                try:

                    # Extract tracking data
                    x1, y1, x2, y2 = map(
                        int,
                        detection[0]
                    )

                    track_id = int(
                        detection[4]
                    )

                    passenger_boxes.append(
                        (x1, y1, x2, y2)
                    )
                    
                    # -----------------------------------
                    # Movement Analytics
                    # -----------------------------------

                    movement_result = (
                        movement_analyzer.analyze_movement(
                            track_id,
                            (x1, y1, x2, y2)
                        )
                    )

                    direction = (
                        movement_result["direction"]
                    )

                    movement_status = (
                        movement_result[
                            "movement_status"
                        ]
                    )

                    speed = (
                        movement_result["speed"]
                    )

                    # -----------------------------------
                    # Log Movement Data
                    # -----------------------------------

                    if should_log:

                        event_logger.log_movement(
                            track_id,
                            direction,
                            speed,
                            movement_status
                        )

                    # -----------------------------------
                    # Draw Bounding Box
                    # -----------------------------------

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (255, 0, 0),
                        2
                    )

                    # Tracking ID
                    cv2.putText(
                        frame,
                        f"ID: {track_id}",
                        (x1, y1 - 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255, 0, 0),
                        1
                    )

                    # Direction
                    cv2.putText(
                        frame,
                        f"Dir: {direction}",
                        (x1, y1 - 25),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 255),
                        1
                    )

                    # Speed
                    cv2.putText(
                        frame,
                        f"Speed: {speed}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        1
                    )

                    # Movement Status
                    cv2.putText(
                        frame,
                        movement_status,
                        (x1, y2 + 15),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 165, 255),
                        1
                    )

                except Exception:
                    continue

            # -----------------------------------
            # Update Logging Timer
            # -----------------------------------

            if should_log:

                last_log_time = current_time

            

            # -----------------------------------
            # Pose Estimation
            # -----------------------------------

            try:

                frame, landmark_data = (
                    pose_estimator.estimate_pose(
                        frame
                    )
                )

            except Exception:

                landmark_data = {}

            # -----------------------------------
            # Aggression Detection
            # -----------------------------------

            aggression_result = (
                aggression_detector.analyze_frame(
                    frame,
                    passenger_boxes
                )
            )

            aggression_score = (
                aggression_result[
                    "aggression_score"
                ]
            )

            aggression_alert = (
                aggression_result[
                    "alert_status"
                ]
            )

            suspicious_activity = (
                aggression_result[
                    "suspicious_activity"
                ]
            )

            # -----------------------------------
            # Crowd Density Analytics
            # -----------------------------------

            density_result = (
                density_analyzer.analyze_density(
                    passenger_count
                )
            )

            density_level = (
                density_result[
                    "density_level"
                ]
            )

            alert_message = (
                density_result[
                    "alert_message"
                ]
            )

            density_color = (
                get_density_color(
                    density_level
                )
            )

            # -----------------------------------
            # Database Logging
            # -----------------------------------

            current_time = time.time()

            if (
                current_time - last_log_time
                >= log_interval
            ):

                try:

                    # Crowd analytics logging
                    event_logger.log_crowd_analytics(
                        passenger_count,
                        density_level,
                        alert_message
                    )

                    # Aggression logging
                    event_logger.log_aggression_event(
                        aggression_score,
                        suspicious_activity,
                        aggression_alert
                    )

                    # Overcrowding alerts
                    if density_level == "OVERCROWDED":

                        event_logger.log_alert(
                            "OVERCROWDING",
                            alert_message
                        )

                    # Suspicious activity alerts
                    if suspicious_activity:

                        event_logger.log_alert(
                            "AGGRESSION",
                            aggression_alert
                        )

                    # Update timer
                    last_log_time = current_time

                except Exception as database_error:

                    print(
                        f"Database Logging Error: "
                        f"{database_error}"
                    )

            # -----------------------------------
            # FPS Calculation
            # -----------------------------------

            fps, previous_time = calculate_fps(
                previous_time
            )

            # -----------------------------------
            # Display Analytics
            # -----------------------------------

            cv2.putText(
                frame,
                f"Passengers: {passenger_count}",
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                1
            )

            cv2.putText(
                frame,
                f"Density: {density_level}",
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                density_color,
                1
            )

            cv2.putText(
                frame,
                alert_message,
                (10, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                density_color,
                1
            )

            cv2.putText(
                frame,
                f"Aggression: {aggression_score}",
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                1
            )

            cv2.putText(
                frame,
                aggression_alert,
                (10, 125),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                1
            )

            cv2.putText(
                frame,
                f"FPS: {fps:.1f}",
                (10, 150),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1
            )

            # -----------------------------------
            # Suspicious Activity Alert
            # -----------------------------------

            if suspicious_activity:

                cv2.rectangle(
                    frame,
                    (0, 0),
                    (
                        frame.shape[1],
                        frame.shape[0]
                    ),
                    (0, 0, 255),
                    8
                )

                cv2.putText(
                    frame,
                    "SUSPICIOUS ACTIVITY DETECTED",
                    (50, 220),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

            # -----------------------------------
            # Show Final Output
            # -----------------------------------

            cv2.imshow(
                "SmartRail AI Surveillance",
                frame
            )

            # Safe Exit
            if cv2.waitKey(1) & 0xFF == ord('q'):

                print("Application Closed.")
                break

        # -----------------------------------
        # Cleanup
        # -----------------------------------

        cap.release()

        cv2.destroyAllWindows()

        # Close logger safely
        event_logger.close_logger()

    except Exception as error:

        print(
            f"Runtime Error: {error}"
        )


if __name__ == "__main__":
    main()