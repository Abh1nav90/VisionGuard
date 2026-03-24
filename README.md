<div align="center">

# 👁️ VisionGuard AI
### Real-Time Pedestrian & Vehicle Detection System

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-FF4B4B?style=for-the-badge)](https://visionguard-dwiz4twnypak6dkqkr96zz.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF?style=for-the-badge)](https://ultralytics.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-Academic-green?style=for-the-badge)](LICENSE)

**A production-grade computer vision system that detects pedestrians and vehicles in real time, estimates proximity, and triggers smart cooldown-controlled alerts.**

[🌐 Live App](https://visionguard-dwiz4twnypak6dkqkr96zz.streamlit.app) · [📖 Documentation](#how-to-run) · [🐛 Report Bug](https://github.com/Vinay-Partap/VisionGuard/issues)

</div>

---

## 📌 Overview

VisionGuard AI is a **DeepTech / System-Based AI project** built for real-world pedestrian safety monitoring. Using the YOLOv8 deep learning model, the system processes images and video streams to:

- Detect pedestrians and classify them by proximity risk (**HIGH / MEDIUM / LOW**)
- Trigger audio + visual alerts only when safety thresholds are breached
- Prevent alert flooding using a cooldown engine
- Export session data as **CSV reports** for further analysis

> 💡 **Problem it solves:** Traditional driver-assistance systems fail to provide timely warnings due to poor visibility, blind spots, or delayed human response. VisionGuard automates proximity-aware detection in real time.

---

## 🚀 Live Demo

👉 **[Try VisionGuard AI Live](https://visionguard-dwiz4twnypak6dkqkr96zz.streamlit.app)**

Upload any image or video containing pedestrians/vehicles and see real-time detection with risk-level bounding boxes and proximity alerts.

---

## ✨ Features

| Feature                        | Description                                                 |
| ------------------------------ | ----------------------------------------------------------- |
| 🎯 **YOLOv8 Detection**         | Real-time object detection using Ultralytics YOLOv8n        |
| 🚦 **Risk-Level Color Coding**  | RED = HIGH (<4m), ORANGE = MEDIUM (4–7m), GREEN = LOW (>7m) |
| 🔊 **Smart Alert System**       | Audio + visual alerts with cooldown to prevent flooding     |
| 📊 **Live Analytics Dashboard** | Real-time metrics: Pedestrians, Vehicles, Alerts, FPS       |
| 📋 **Detection History Log**    | Timestamped log of every detection with distance & risk     |
| 📥 **Export Reports**           | Download session data as CSV or formatted text report       |
| ⚙️ **Configurable Thresholds**  | Adjustable confidence & proximity sliders from sidebar      |
| 🎥 **Multi-Input Support**      | Image upload, Video upload, and Live Camera (local)         |

---

## 🏗️ System Architecture

```
User Input (Image / Video / Camera)
            ↓
   YOLOv8 Object Detection
   (confidence threshold filter)
            ↓
  Pedestrian Distance Estimation
  (bounding box height → meters)
            ↓
  Risk Classification Engine
  HIGH(<4m) | MEDIUM(4-7m) | LOW(>7m)
            ↓
  Alert Decision Engine
  (cooldown logic → no flooding)
            ↓
  Streamlit UI + Live Dashboard
  + Detection Log + Export
```

---

## 🛠️ Tech Stack

| Layer                | Technology           |
| -------------------- | -------------------- |
| Language             | Python 3.11+         |
| Deep Learning        | YOLOv8 (Ultralytics) |
| Computer Vision      | OpenCV, Pillow       |
| Web Interface        | Streamlit            |
| Numerical Processing | NumPy, Pandas        |
| Model Backend        | PyTorch              |
| Deployment           | Streamlit Cloud      |

---

## 📁 Project Structure

```
VisionGuard/
├── app.py                    # Main Streamlit application
├── detector/
│   ├── yolo_detector.py      # YOLOv8 detection + risk classification
│   ├── distance.py           # Bounding box → distance estimation
│   └── tracker.py            # Object tracking (optional)
├── utils/
│   ├── alerts.py             # Alert engine + cooldown logic
│   └── summary.py            # Detection log + session analytics
├── assets/
│   └── alert.wav             # Alert sound file
├── .streamlit/
│   └── config.toml           # UI theme configuration
├── requirements.txt
└── README.md
```

---

## ⚡ How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/Vinay-Partap/VisionGuard.git
cd VisionGuard
```

### 2. Create & Activate Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

---

## 📊 Alert Logic

```
distance < 4.0m  →  🔴 HIGH RISK   →  Alert triggered
distance < 7.0m  →  🟠 MEDIUM RISK →  Alert triggered  
distance ≥ 7.0m  →  🟢 LOW RISK    →  No alert
```

- Cooldown of **3 seconds** between alerts prevents flooding
- All thresholds configurable via sidebar sliders

---

## 🔮 Future Scope

- [ ] Vehicle speed estimation via tracking
- [ ] Heatmap overlay showing pedestrian density zones
- [ ] Custom danger zone (ROI) drawing on frame
- [ ] Edge device deployment (Raspberry Pi / Jetson Nano)
- [ ] Integration with smart traffic management systems
- [ ] REST API endpoint via FastAPI

---

## 👨‍💻 Author

**Vinay Partap**
[![GitHub](https://img.shields.io/badge/GitHub-Vinay--Partap-181717?style=flat&logo=github)](https://github.com/Vinay-Partap)

---

## 📄 License

This project is developed for academic and research purposes.

---

<div align="center">
  <strong>⭐ If you found this project useful, please consider giving it a star!</strong>
</div>