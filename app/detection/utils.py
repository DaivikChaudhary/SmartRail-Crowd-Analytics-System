"""
utils.py
---------
Utility functions
"""

import cv2
import time


def resize_frame(frame, width=960, height=540):
    """
    Resize frame for better CPU performance
    and proper display window size.
    """

    return cv2.resize(frame, (width, height))


def calculate_fps(previous_time):
    """
    Calculate FPS
    """

    current_time = time.time()

    fps = 1 / (current_time - previous_time)

    return round(fps, 2), current_time