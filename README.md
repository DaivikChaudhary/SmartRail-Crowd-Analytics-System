# 🚆 SmartRail Crowd Analytics and Passenger Safety System

## 📌 Project Overview

SmartRail Crowd Analytics and Passenger Safety System is an AI-powered real-time railway surveillance and crowd monitoring platform designed for unreserved railway coaches and crowded public transportation environments.

The system uses Computer Vision, Real-Time Analytics, Passenger Tracking, Movement Analysis, and Aggression Detection to improve passenger safety and crowd management.

This project simulates an industrial AI surveillance architecture capable of analyzing live CCTV/IP camera streams and generating real-time safety analytics.

---

# 🎯 Key Features

## ✅ Real-Time Passenger Detection

* Detects passengers using YOLOv8 object detection.
* Works on CCTV/IP camera streams and recorded videos.

## ✅ Passenger Counting

* Counts passengers inside railway coaches in real-time.

## ✅ Crowd Density Analytics

* Classifies crowd density levels:

  * LOW
  * MEDIUM
  * HIGH
  * OVERCROWDED

## ✅ Passenger Tracking

* Tracks passengers using ByteTrack.
* Assigns unique IDs to passengers.

## ✅ Movement Analytics

* Detects:

  * movement direction
  * speed estimation
  * stationary passengers
  * crowd flow patterns

## ✅ Aggression & Suspicious Activity Detection

* Uses MediaPipe Pose Estimation.
* Detects abnormal body movement and suspicious interactions.

## ✅ Alert Generation System

* Generates:

  * overcrowding alerts
  * suspicious activity alerts
  * aggression alerts

## ✅ Database Logging

* Stores analytics and alerts in SQLite/MySQL database.

## ✅ FastAPI Backend APIs

* Provides APIs for:

  * analytics
  * alerts
  * movement logs
  * aggression events

## ✅ Streamlit Dashboard

* Real-time monitoring dashboard with:

  * analytics cards
  * alert panels
  * charts
  * historical analytics

## ✅ Dockerized Architecture

* Fully containerized using Docker and Docker Compose.

---

# 🏗️ System Architecture

```text
CCTV/IP Camera
        ↓
OpenCV Video Processing
        ↓
YOLOv8 Passenger Detection
        ↓
Passenger Tracking (ByteTrack)
        ↓
Movement Analytics
        ↓
MediaPipe Pose Estimation
        ↓
Aggression Detection
        ↓
Database Logging
        ↓
FastAPI Backend
        ↓
Streamlit Dashboard
```

---

# 🛠️ Tech Stack

## AI & Computer Vision

* Python
* OpenCV
* YOLOv8
* MediaPipe
* NumPy

## Backend

* FastAPI
* Uvicorn

## Dashboard

* Streamlit
* Plotly
* Pandas

## Database

* SQLite
* MySQL (optional)

## Deployment

* Docker
* Docker Compose

---

# 📂 Project Structure

```text
SmartRail/
│
├── app/
│   ├── detection/
│   ├── tracking/
│   ├── analytics/
│   ├── movement/
│   ├── aggression/
│   ├── database/
│   ├── api/
│   └── dashboard/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone <your-repository-url>
cd SmartRail
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run AI Surveillance System

```bash
python app/detection/main.py
```

---

# 🚀 Run FastAPI Backend

```bash
uvicorn run_api:app --reload
```

API Docs:

```text
http://127.0.0.1:8000/docs
```

---

# 📊 Run Streamlit Dashboard

```bash
streamlit run app/dashboard/dashboard.py
```

Dashboard URL:

```text
http://localhost:8501
```

---

# 🐳 Docker Setup

## Build Containers

```bash
docker compose build
```

## Start Services

```bash
docker compose up
```

---

# 📡 API Endpoints

| Endpoint               | Description            |
| ---------------------- | ---------------------- |
| GET /analytics         | Get crowd analytics    |
| GET /alerts            | Get system alerts      |
| GET /movement          | Get movement analytics |
| GET /aggression-events | Get aggression logs    |
| GET /health            | System health check    |

---

# 💡 Industrial Applications

* Smart Railway Surveillance
* Metro Crowd Monitoring
* Public Transport Safety
* Smart City Surveillance
* Station Crowd Analytics
* Passenger Behavior Monitoring

---

# 👨‍💻 Author

Daivik Chaudhary

AI/ML & Data Analytics Enthusiast

---

# ⭐ Project Highlights

✅ Real-Time AI Surveillance
✅ Crowd Analytics Platform
✅ Passenger Safety Monitoring
✅ Industrial AI Architecture
✅ REST APIs & Dashboard
✅ Dockerized Deployment
