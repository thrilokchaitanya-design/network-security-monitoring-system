
# Network Security Monitoring System

A real-time network security monitoring system designed to detect, visualize, and respond to network attacks using Software-Defined Networking (SDN), machine learning, and a web-based monitoring dashboard.

## Project Overview

The system combines:

- Network traffic monitoring
- Machine-learning-based attack detection
- SDN-based network control
- Real-time security alerts
- Network topology visualization
- REST APIs
- WebSocket-based real-time communication
- Role-based authentication
- Security analytics
- Alert management and mitigation actions

The project is being developed as a capstone project with separate modules for AI/Data Intelligence, Networking/SDN, Backend/Dashboard, and Hardware/Testing.

---

## Current Architecture

```text
                    Network Traffic
                          │
                          ▼
                ┌──────────────────┐
                │ Network / SDN    │
                │ Monitoring Layer │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ AI / ML Detection │
                │      Engine       │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │   FastAPI        │
                │    Backend       │
                └────────┬─────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
        PostgreSQL             WebSocket
        Database               Real-time Feed
              │                     │
              └──────────┬──────────┘
                         ▼
                ┌──────────────────┐
                │ React + Vite     │
                │ Security         │
                │ Dashboard        │
                └──────────────────┘
````

---

# Technology Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* PostgreSQL
* JWT Authentication
* WebSockets
* Pytest

## Frontend

* React
* Vite
* JavaScript / JSX
* CSS
* WebSocket client

## Networking

* Software-Defined Networking (SDN)
* Mininet
* Open vSwitch (OVS)
* Ryu Controller
* OpenFlow

## AI / Machine Learning

* CIC-IDS2017 dataset
* Exploratory Data Analysis
* Random Forest baseline
* Graph-based network representation
* GraphSAGE planned for the detection pipeline

## Hardware

* Raspberry Pi / ESP32
* GPIO
* LED
* Buzzer
* OLED display

---

# Backend Features Implemented

The FastAPI backend currently provides the following major functionality:

## Authentication

* JWT-based authentication
* Login endpoint
* Role-based access control
* Admin role
* Viewer role
* Authentication-protected endpoints

## Alerts

Implemented functionality includes:

* Create alerts
* Retrieve alerts
* Retrieve alert by ID
* Pagination
* Filter by severity
* Filter by status
* Filter by attack type
* Filter by source IP
* Filter by host
* Host validation

## Hosts

Implemented functionality includes:

* Create hosts
* Retrieve hosts
* Retrieve host by ID
* Update hosts
* Retrieve alerts associated with a host
* Retrieve host security summary
* Duplicate hostname validation
* Duplicate IP validation
* Duplicate MAC validation
* Role-based access control

## Alert Actions

Implemented functionality includes:

* Create alert actions
* Retrieve alert actions
* Validate supported actions
* Authentication requirements
* Alert existence validation

## Analytics

Implemented analytics endpoints include:

* Security summary
* Attack distribution
* Severity distribution
* Attack sources

## WebSocket

A real-time WebSocket channel is implemented at:

```text
/ws/alerts
```

The WebSocket system includes:

* Client connection handling
* Connection management
* Broadcasting of alert messages
* Disconnect handling
* Real-time alert delivery to the dashboard

---

# Frontend Features Implemented

The React dashboard currently includes:

## Dashboard

The dashboard provides the main security monitoring interface.

## Network Topology

A topology component has been created for visualizing monitored network infrastructure.

```text
NetworkTopology.jsx
NetworkTopology.css
```

## Real-Time Alerts

A real-time security alert component has been implemented.

```text
RealtimeAlerts.jsx
RealtimeAlerts.css
```

The component:

* Connects to the FastAPI WebSocket
* Displays connection status
* Receives real-time alert messages
* Displays severity
* Displays attack type
* Displays source IP
* Displays destination IP
* Displays confidence score
* Displays alert status
* Displays alert ID
* Displays alert descriptions

The dashboard currently displays:

```text
Live Security Events
```

with a real-time connection indicator.

## Alert Details

Alert detail functionality and styling have also been implemented.

---

# Testing

The backend currently has automated tests covering:

* Authentication
* Alerts
* Hosts
* Alert actions
* Analytics
* WebSocket functionality

Current test result:

```text
47 passed
18 warnings
```

WebSocket-specific tests:

```text
3 passed
```

The WebSocket tests verify:

```text
✓ WebSocket connection
✓ WebSocket broadcast
✓ WebSocket disconnect
```

---

# Frontend Build

The frontend production build has been successfully tested using:

```bash
npm run build
```

Current result:

```text
✓ built successfully
```

---

# Project Structure

```text
network-security-monitoring-system/
│
├── backend/
│   │
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── alerts.py
│   │   │   ├── hosts.py
│   │   │   ├── actions.py
│   │   │   ├── analytics.py
│   │   │   └── websocket.py
│   │   │
│   │   ├── services/
│   │   ├── database.py
│   │   └── main.py
│   │
│   └── tests/
│       ├── test_auth.py
│       ├── test_alerts.py
│       ├── test_hosts.py
│       ├── test_actions.py
│       ├── test_analytics.py
│       └── test_websocket.py
│
├── frontend/
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── NetworkTopology.jsx
│   │   │   ├── NetworkTopology.css
│   │   │   ├── RealtimeAlerts.jsx
│   │   │   └── RealtimeAlerts.css
│   │   │
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Dashboard.css
│   │   │   ├── AlertDetails.jsx
│   │   │   └── AlertDetails.css
│   │   │
│   │   └── index.css
│   │
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# Development Progress

## Completed

### Backend

* [x] FastAPI project structure
* [x] PostgreSQL integration
* [x] Database models
* [x] Authentication
* [x] JWT login
* [x] Role-based access control
* [x] Alerts API
* [x] Hosts API
* [x] Alert Actions API
* [x] Analytics API
* [x] WebSocket API
* [x] WebSocket connection manager
* [x] WebSocket tests
* [x] Backend test suite

### Frontend

* [x] React + Vite dashboard
* [x] Dashboard shell
* [x] Alert details page
* [x] Network topology component
* [x] Real-time alerts component
* [x] WebSocket connection to backend
* [x] Live connection indicator
* [x] Real-time alert rendering
* [x] Frontend production build

### Integration

* [x] Backend WebSocket endpoint
* [x] Frontend WebSocket client
* [x] Real-time alert communication
* [x] WebSocket automated tests
* [x] Full backend test suite passing

---

# Current Development Status

The W1–W9 backend and dashboard work is implemented in the repository: `/topology` and `/stats`, database-backed topology and analytics views, persisted alert ingestion with WebSocket delivery, and alert timeline/replay are available. Review 2 integration contracts and schema/API documentation are in [`docs/REVIEW2_IMPLEMENTATION.md`](docs/REVIEW2_IMPLEMENTATION.md).

The real SDN and detector processes are separate project modules. Set `SDN_CONTROLLER_URL` and connect the Member A/B detector to `POST /alerts` to demonstrate a real end-to-end attack path. Without those external processes, the UI clearly labels registered-host topology and cannot claim the live Review 2 integration is demonstrated.

### W7–W9 implementation checklist

* [x] Implement `/topology` and `/stats`
* [x] Connect dashboard topology and statistics to backend data
* [x] Replace static sample topology and test-alert broadcast with data-backed integrations
* [x] Persist and broadcast ingested detector alerts
* [x] Add chronological alert timeline and replay controls
* [ ] Run the live end-to-end attack path with Member A/B detector and SDN controller
* [ ] Verify the integrated pipeline with real attack data in the Review 2 environment

---

# Testing Commands

## Backend

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run the complete test suite:

```powershell
pytest -v
```

Run only WebSocket tests:

```powershell
pytest -v tests/test_websocket.py
```

Set the Python path if required:

```powershell
$env:PYTHONPATH = (Get-Location).Path
```

---

# Frontend

Navigate to the frontend directory:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

Build the frontend:

```powershell
npm run build
```

---

# Running the System

## Start Backend

From the `backend` directory:

```powershell
uvicorn app.main:app --reload
```

The backend runs on:

```text
http://127.0.0.1:8000
```

## Start Frontend

From the `frontend` directory:

```powershell
npm run dev
```

The frontend normally runs on:

```text
http://localhost:5173
```

## WebSocket

The real-time alert WebSocket endpoint is:

```text
ws://127.0.0.1:8000/ws/alerts
```

---

# Git Workflow

To check the current project state:

```bash
git status
```

To stage changes:

```bash
git add backend frontend
```

To commit:

```bash
git commit -m "your commit message"
```

To push:

```bash
git push origin main
```

---

# Project Roadmap

```text
Database & API Foundation
          ✓
          │
          ▼
Authentication & RBAC
          ✓
          │
          ▼
Alerts / Hosts / Actions / Analytics
          ✓
          │
          ▼
WebSocket Real-Time Communication
          ✓
          │
          ▼
React Dashboard
          ✓
          │
          ▼
Network Topology + Real-Time Alerts
          ✓
          │
          ▼
Topology & Statistics APIs
          │
          ▼
Real Pipeline Integration
          │
          ▼
End-to-End Attack Detection
          │
          ▼
Alert Timeline / Replay
          │
          ▼
Review 2
```

---

# Project Goal

The final system aims to provide a unified network security monitoring platform capable of:

1. Monitoring network traffic.
2. Detecting malicious network activity.
3. Classifying attacks using machine learning.
4. Visualizing the monitored network.
5. Generating real-time security alerts.
6. Providing security analytics.
7. Supporting alert investigation.
8. Triggering mitigation actions through the SDN infrastructure.
9. Providing a centralized web dashboard for security monitoring.

---

# Development Status

**Status:** Active Development

**Current Phase:** Dashboard + Real-Time Monitoring Integration

**Backend Tests:** 47/47 passing

**WebSocket Tests:** 3/3 passing

**Frontend Build:** Passing

**Next Major Milestone:** Connect and verify the external SDN controller and Member A/B detector for the Review 2 live attack-path demo.

```
```
