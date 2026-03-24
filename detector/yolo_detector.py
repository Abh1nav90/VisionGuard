# detector/yolo_detector.py
import cv2
from ultralytics import YOLO
from detector.distance import estimate_distance
from utils.summary import log_detection

# Load stable YOLO model
model = YOLO("yolov8n.pt")

PEDESTRIAN_CLASS_ID = 0
VEHICLE_CLASS_IDS = [2, 3, 5, 7]  # car, bike, bus, truck


def get_risk(distance):
    """Return risk level string based on distance."""
    if distance is None:
        return "low"
    if distance < 4.0:
        return "high"
    elif distance < 7.0:
        return "medium"
    return "low"


def get_bbox_color(risk):
    """Return BGR color based on risk level."""
    return {
        "high":   (0, 0, 255),    # Red
        "medium": (0, 165, 255),  # Orange
        "low":    (0, 255, 0),    # Green
    }.get(risk, (0, 255, 0))


def detect_objects(frame, summary, confidence_threshold=0.4, proximity_threshold=7.0):
    results = model(frame, verbose=False, conf=confidence_threshold)[0]
    alert_triggered = False

    for box in results.boxes:
        cls_id = int(box.cls[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        height = y2 - y1
        label = None

        # Pedestrian
        if cls_id == PEDESTRIAN_CLASS_ID:
            distance = estimate_distance(height)
            risk = get_risk(distance)
            color = get_bbox_color(risk)
            dist_str = f"{distance}m" if distance else "?"
            label = f"Pedestrian {dist_str} [{risk.upper()}]"
            summary["pedestrians"] += 1
            summary["total"] += 1
            log_detection(summary, "Pedestrian", distance, risk)

            if distance is not None and distance < proximity_threshold:
                alert_triggered = True
                summary["alerts"] += 1

        # Vehicle
        elif cls_id in VEHICLE_CLASS_IDS:
            color = (255, 200, 0)  # Blue-yellow for vehicles
            label = "Vehicle"
            summary["vehicles"] += 1
            summary["total"] += 1
            log_detection(summary, "Vehicle")

        if label:
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            # Background for label text
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
            cv2.rectangle(frame, (x1, y1 - th - 8), (x1 + tw + 4, y1), color, -1)
            cv2.putText(
                frame, label,
                (x1 + 2, y1 - 4),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55, (255, 255, 255), 2,
            )

    return frame, alert_triggered