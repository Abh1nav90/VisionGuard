# app.py
import streamlit as st
import cv2
import numpy as np
import time
import pandas as pd
from datetime import datetime
from io import BytesIO
from detector.yolo_detector import detect_objects
from utils.alerts import should_alert, play_alert_sound
from utils.summary import init_summary, reset_summary

st.set_page_config(page_title="VisionGuard AI", layout="wide", page_icon="👁️")

# ─────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: #1e1e2e;
        border-radius: 12px;
        padding: 16px 20px;
        text-align: center;
        border: 1px solid #2e2e4e;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #a78bfa; }
    .metric-label { font-size: 0.8rem; color: #888; margin-top: 4px; }
    .alert-high   { background:#ff4b4b22; border-left: 4px solid #ff4b4b; padding: 8px 14px; border-radius: 4px; }
    .alert-medium { background:#ffa50022; border-left: 4px solid #ffa500; padding: 8px 14px; border-radius: 4px; }
    .risk-high   { color: #ff4b4b; font-weight: 600; }
    .risk-medium { color: #ffa500; font-weight: 600; }
    .risk-low    { color: #21c55d; font-weight: 600; }
    div[data-testid="stSidebar"] { background: #111827; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# SIDEBAR — SETTINGS (Tier 1: Confidence + Proximity threshold)
# ─────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/eye.png", width=60)
    st.title("VisionGuard AI")
    st.caption("Real-Time Detection System")
    st.divider()

    st.subheader("⚙️ Detection Settings")

    confidence_threshold = st.slider(
        "Confidence threshold",
        min_value=0.1, max_value=0.9,
        value=0.4, step=0.05,
        help="Filter out detections below this confidence score"
    )

    proximity_threshold = st.slider(
        "Alert distance (meters)",
        min_value=1.0, max_value=20.0,
        value=7.0, step=0.5,
        help="Trigger alert when pedestrian is closer than this distance"
    )

    sound_enabled = st.toggle("🔊 Alert sound", value=True)

    st.divider()
    st.subheader("🎨 Risk color legend")
    st.markdown('<span class="risk-high">● HIGH</span> &nbsp; < 4m', unsafe_allow_html=True)
    st.markdown('<span class="risk-medium">● MEDIUM</span> &nbsp; 4–7m', unsafe_allow_html=True)
    st.markdown('<span class="risk-low">● LOW</span> &nbsp; > 7m', unsafe_allow_html=True)

    st.divider()
    st.caption("VisionGuard AI v2.0")

# ─────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────
if "summary" not in st.session_state:
    st.session_state.summary = init_summary()
if "fps_list" not in st.session_state:
    st.session_state.fps_list = []
if "last_frame_time" not in st.session_state:
    st.session_state.last_frame_time = time.time()

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.title("👁️ VisionGuard AI")
st.subheader("Real-Time Pedestrian & Vehicle Detection System")
st.divider()

# ─────────────────────────────────────────
# LIVE METRICS ROW (Tier 1: Live stats dashboard)
# ─────────────────────────────────────────
m1, m2, m3, m4, m5 = st.columns(5)
pedestrian_metric = m1.empty()
vehicle_metric    = m2.empty()
alert_metric      = m3.empty()
fps_metric        = m4.empty()
total_metric      = m5.empty()

def update_metrics(summary, fps=0.0):
    pedestrian_metric.metric("🚶 Pedestrians", summary["pedestrians"])
    vehicle_metric.metric("🚗 Vehicles",    summary["vehicles"])
    alert_metric.metric("🚨 Alerts",       summary["alerts"])
    fps_metric.metric("⚡ FPS",            f"{fps:.1f}")
    total_metric.metric("📦 Total",         summary["total"])

update_metrics(st.session_state.summary)

st.divider()

# ─────────────────────────────────────────
# INPUT TYPE
# ─────────────────────────────────────────
input_type = st.radio(
    "Select input type",
    ["Upload Image", "Upload Video", "Live Camera"],
    horizontal=True
)

frame_placeholder = st.empty()
alert_box         = st.empty()

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
def compute_fps():
    now = time.time()
    elapsed = now - st.session_state.last_frame_time
    st.session_state.last_frame_time = now
    fps = 1.0 / elapsed if elapsed > 0 else 0.0
    st.session_state.fps_list.append(fps)
    if len(st.session_state.fps_list) > 30:
        st.session_state.fps_list.pop(0)
    return round(sum(st.session_state.fps_list) / len(st.session_state.fps_list), 1)


def trigger_alert(summary):
    alert_box.markdown('<div class="alert-high">🚨 <b>Pedestrian too close! Immediate danger.</b></div>',
                       unsafe_allow_html=True)
    if sound_enabled:
        play_alert_sound()


def export_csv(summary):
    """Convert detection log to CSV bytes."""
    if not summary["detection_log"]:
        return None
    df = pd.DataFrame(summary["detection_log"])
    return df.to_csv(index=False).encode("utf-8")


def export_pdf_txt(summary):
    """Generate a simple plain-text report (PDF-ready)."""
    lines = [
        "=" * 50,
        "       VISIONGUARD AI — DETECTION REPORT",
        "=" * 50,
        f"Session start : {summary['start_time']}",
        f"Report time   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "SUMMARY",
        "-" * 30,
        f"  Pedestrians detected : {summary['pedestrians']}",
        f"  Vehicles detected    : {summary['vehicles']}",
        f"  Total detections     : {summary['total']}",
        f"  Alerts triggered     : {summary['alerts']}",
        "",
        "DETECTION LOG",
        "-" * 30,
    ]
    for entry in summary["detection_log"]:
        lines.append(
            f"  [{entry['time']}]  {entry['type']:12s}  "
            f"dist={entry['distance_m']}m  risk={entry['risk'].upper()}"
        )
    lines += ["", "=" * 50, "  Generated by VisionGuard AI v2.0", "=" * 50]
    return "\n".join(lines).encode("utf-8")


# ─────────────────────────────────────────
# IMAGE MODE
# ─────────────────────────────────────────
if input_type == "Upload Image":
    if st.button("🔄 Reset session"):
        st.session_state.summary = init_summary()
        st.rerun()

    image_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if image_file:
        image = np.frombuffer(image_file.read(), np.uint8)
        frame = cv2.imdecode(image, cv2.IMREAD_COLOR)
        summary = st.session_state.summary

        t0 = time.time()
        frame, alert = detect_objects(frame, summary, confidence_threshold, proximity_threshold)
        fps = round(1.0 / max(time.time() - t0, 0.001), 1)

        frame_placeholder.image(frame, channels="BGR", width="stretch")
        update_metrics(summary, fps)

        if alert and should_alert():
            trigger_alert(summary)

        # ── Tier 1: Detection history log ──
        st.divider()
        st.subheader("📋 Detection history log")
        if summary["detection_log"]:
            df = pd.DataFrame(summary["detection_log"])
            df.columns = ["Time", "Type", "Distance (m)", "Risk"]

            def color_risk(val):
                colors = {"high": "color: #ff4b4b", "medium": "color: #ffa500", "low": "color: #21c55d"}
                return colors.get(val.lower(), "")

            st.dataframe(
                df.style.map(color_risk, subset=["Risk"]),
                width="stretch", hide_index=True
            )
        else:
            st.info("No detections yet.")

        # ── Tier 1: CSV / PDF export ──
        st.divider()
        st.subheader("📥 Export report")
        col1, col2 = st.columns(2)
        with col1:
            csv_data = export_csv(summary)
            if csv_data:
                st.download_button(
                    "⬇️ Download CSV",
                    data=csv_data,
                    file_name=f"visionguard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    width="stretch"
                )
            else:
                st.button("⬇️ Download CSV", disabled=True, width="stretch")
        with col2:
            txt_data = export_pdf_txt(summary)
            st.download_button(
                "⬇️ Download Report (.txt)",
                data=txt_data,
                file_name=f"visionguard_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                width="stretch"
            )


# ─────────────────────────────────────────
# VIDEO MODE
# ─────────────────────────────────────────
elif input_type == "Upload Video":
    if st.button("🔄 Reset session"):
        st.session_state.summary = init_summary()
        st.rerun()

    video_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])

    if video_file:
        with open("temp_video.mp4", "wb") as f:
            f.write(video_file.read())

        summary = st.session_state.summary
        cap = cv2.VideoCapture("temp_video.mp4")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            t0 = time.time()
            frame, alert = detect_objects(frame, summary, confidence_threshold, proximity_threshold)
            fps = compute_fps()

            frame_placeholder.image(frame, channels="BGR", width="stretch")
            update_metrics(summary, fps)

            if alert and should_alert():
                trigger_alert(summary)

            time.sleep(0.03)

        cap.release()

        # ── Detection log + export after video ends ──
        st.divider()
        st.subheader("📋 Detection history log")
        if summary["detection_log"]:
            df = pd.DataFrame(summary["detection_log"])
            df.columns = ["Time", "Type", "Distance (m)", "Risk"]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No detections logged.")

        st.divider()
        st.subheader("📥 Export report")
        col1, col2 = st.columns(2)
        with col1:
            csv_data = export_csv(summary)
            if csv_data:
                st.download_button(
                    "⬇️ Download CSV",
                    data=csv_data,
                    file_name=f"visionguard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    width="stretch"
                )
        with col2:
            txt_data = export_pdf_txt(summary)
            st.download_button(
                "⬇️ Download Report (.txt)",
                data=txt_data,
                file_name=f"visionguard_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                width="stretch"
            )


# ─────────────────────────────────────────
# LIVE CAMERA MODE
# ─────────────────────────────────────────
elif input_type == "Live Camera":
    st.info("Click **Start Camera** to begin live detection")

    col1, col2 = st.columns(2)
    with col1:
        start_cam = st.checkbox("▶️ Start Camera")
    with col2:
        if st.button("🔄 Reset session"):
            st.session_state.summary = init_summary()
            st.rerun()

    if start_cam:
        cap = cv2.VideoCapture(0)
        summary = st.session_state.summary

        if not cap.isOpened():
            st.error("❌ Camera not accessible. Check your device.")
        else:
            while start_cam:
                ret, frame = cap.read()
                if not ret:
                    break

                t0 = time.time()
                frame, alert = detect_objects(frame, summary, confidence_threshold, proximity_threshold)
                fps = compute_fps()

                frame_placeholder.image(frame, channels="BGR", width="stretch")
                update_metrics(summary, fps)

                if alert and should_alert():
                    trigger_alert(summary)

                time.sleep(0.03)

            cap.release()

        # Export available after camera stops
        if summary["detection_log"]:
            st.divider()
            st.subheader("📋 Detection history log")
            df = pd.DataFrame(summary["detection_log"])
            df.columns = ["Time", "Type", "Distance (m)", "Risk"]
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.divider()
            st.subheader("📥 Export report")
            col1, col2 = st.columns(2)
            with col1:
                csv_data = export_csv(summary)
                if csv_data:
                    st.download_button(
                        "⬇️ Download CSV",
                        data=csv_data,
                        file_name=f"visionguard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        width="stretch"
                    )
            with col2:
                txt_data = export_pdf_txt(summary)
                st.download_button(
                    "⬇️ Download Report (.txt)",
                    data=txt_data,
                    file_name=f"visionguard_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    width="stretch"
                )