# utils/summary.py
from datetime import datetime


def init_summary():
    return {
        "pedestrians": 0,
        "vehicles": 0,
        "total": 0,
        "alerts": 0,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "detection_log": []
    }


def reset_summary():
    return init_summary()


def log_detection(summary, detection_type, distance=None, risk=None):
    """Log each detection event with timestamp."""
    summary["detection_log"].append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "type": detection_type,
        "distance_m": str(round(distance, 2)) if distance is not None else "N/A",  # always string
        "risk": risk or "low"
    })