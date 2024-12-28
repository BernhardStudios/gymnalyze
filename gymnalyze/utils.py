def load_video(video_path):
    import cv2
    video = cv2.VideoCapture(video_path)
    return video

import cv2
import numpy as np
import math

def get_point_on_ellipse(center, axes, rotation_angle, angle):
    """
    Calculate the coordinates of a point on the ellipse.

    :param center: Tuple (x, y) representing the center of the ellipse.
    :param axes: Tuple (major_axis, minor_axis) representing the ellipse axes.
    :param rotation_angle: Rotation angle of the ellipse (degrees).
    :param angle: Angle (in degrees) of the point on the ellipse measured clockwise.
    :return: Tuple (x, y) representing the point on the ellipse.
    """
    # Convert angles from degrees to radians
    rotation_rad = math.radians(rotation_angle)
    angle_rad = math.radians(angle)

    # Compute point on the ellipse without rotation
    x = axes[0] * math.cos(angle_rad)
    y = axes[1] * math.sin(angle_rad)

    # Apply rotation to the point
    x_rotated = x * math.cos(rotation_rad) - y * math.sin(rotation_rad)
    y_rotated = x * math.sin(rotation_rad) + y * math.cos(rotation_rad)

    # Translate point to the ellipse's center
    return (int(center[0] + x_rotated), int(center[1] + y_rotated))

class Color:
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    BLUE = (255, 0, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    ORANGE = (0, 165, 255)
    YELLOW = (0, 255, 255)
    PURPLE = (255, 0, 255)
    PINK = (255, 192, 203)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (211, 211, 211)
    DARK_GRAY = (169, 169, 169)
    BROWN = (165, 42, 42)
    CYAN = (255, 255, 0)
    TEAL = (128, 128, 0)
    LIME = (51, 204, 51)