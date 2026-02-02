Real-Time Vehicle and Pedestrian Detection System
Overview
This project aims to develop a real-time vehicle and pedestrian detection system to enhance driving safety. By utilizing the YOLOv9 object detection model, the system accurately identifies vehicles and pedestrians, estimates their distance from the vehicle, and triggers alerts when necessary. The system is designed to operate in real-time, providing critical information to drivers to prevent potential collisions.

Features
Real-Time Object Detection: Utilizes the YOLOv9 model to detect vehicles and pedestrians in video frames.
Distance Estimation: Implements depth estimation algorithms to calculate the distance between the vehicle and detected objects.
Alert System: Triggers visual and auditory alerts when pedestrians are detected within a critical distance threshold.
Responsive Frontend: User interface developed using HTML, CSS, and JavaScript, allowing users to upload videos, view live camera feeds, and monitor real-time detection statistics.
Backend Integration: Built with Flask, the backend handles video processing, object detection, and alert generation.
System Architecture
Camera Integration: Captures real-time video footage from a vehicle-mounted camera.
Object Detection: YOLOv9 processes each frame to identify vehicles and pedestrians, providing bounding boxes and class labels.
Distance Estimation: Estimates the distance of detected objects based on bounding box sizes and known dimensions.
Alert Mechanism: Configurable thresholds trigger alerts when objects are within a predefined proximity to the vehicle.
UML Diagrams
The system’s structure and interactions are represented using UML diagrams, including:

Use Case Diagrams
Class Diagrams
Sequence Diagrams
Activity Diagrams
