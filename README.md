# Chemical Equipment Parameter Visualizer

## 1. High-Level System Architecture
This is a hybrid application comprising three main components:

1.  **Backend (Django REST Framework)**: The core source of truth.
    -   Handles parsing of CSV files using Pandas.
    -   Stores metadata in SQLite.
    -   Provides REST APIs for uploading, analyzing, and retrieving history.
    -   Generates PDF reports using ReportLab.
2.  **Web Frontend (React.js)**: A modern web interface for users to upload data and view interactive dashboards.
    -   Uses Chart.js for visualization.
    -   Communicates with the backend via Axios.
3.  **Desktop Frontend (PyQt5)**: A native desktop application for offline-like capabilities (though it connects to the same local server).
    -   Uses Matplotlib for embedding charts.
    -   Provides a native GUI experience using standard Qt widgets.

## 2. Folder Structure
```text
chemical_app/
├── backend/                  # Django Project
│   ├── chemical_project/     # Project Settings
│   ├── core/                 # App Logic (Views, Models, Serializers)
│   ├── db.sqlite3            # Database (created after migration)
│   ├── manage.py             # Management Script
│   └── requirements.txt      # Backend Dependencies
├── web-frontend/             # React Project
│   ├── src/                  # Source Code
│   │   ├── components/       # React Components (Dashboard, Upload, etc.)
│   │   ├── services/         # API Integration
│   │   ├── App.jsx           # Main App Component
│   │   └── main.jsx          # Entry Point
│   ├── public/               # Static Files
│   ├── index.html            # HTML Entry Point
│   ├── package.json          # Node Dependencies
│   └── vite.config.js        # Vite Config
├── desktop-frontend/         # PyQt5 Project
│   ├── ui/                   # UI Modules
│   ├── utils/                # API Logic
│   ├── main.py               # Application Entry Point
│   └── requirements.txt      # Desktop Dependencies
└── README.md                 # This file
```

## 3. Setup & Running Instructions

### Prerequisites
-   Python 3.8+
-   Node.js & npm (for Web Frontend)

### A. Backend Setup
1.  Navigate to `backend/`:
    ```bash
    cd backend
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Apply Migrations:
    ```bash
    python manage.py makemigrations core
    python manage.py migrate
    ```
4.  Run Server:
    ```bash
    python manage.py runserver
    ```
    *Server runs at http://127.0.0.1:8000/*

### B. Web Frontend Setup
1.  Navigate to `web-frontend/`:
    ```bash
    cd web-frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run Development Server:
    ```bash
    npm run dev
    ```
    *App runs at http://localhost:3000/*

### C. Desktop Frontend Setup
1.  Navigate to `desktop-frontend/`:
    ```bash
    cd desktop-frontend
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run Application:
    ```bash
    python main.py
    ```

## 4. Features & API usage
-   **CSV Upload**: Upload `dataset.csv`. The backend parses it and stores the equipment data. Only the last 5 uploads are kept.
    -   API: `POST /api/upload/`
-   **Dashboard**: View aggregate statistics (Avg Flow, Pressure, Temp) and Charts.
    -   API: `GET /api/analysis/<id>/`
-   **History**: View past uploads.
    -   API: `GET /api/history/`
-   **PDF Report**: Download a summary report.
    -   API: `GET /api/report/<id>/`

## 5. Common Mistakes & Fixes
-   **CORS Error**: If the web app cannot connect to the backend, ensure `django-cors-headers` is installed and `CORS_ALLOW_ALL_ORIGINS = True` is in `settings.py`.
-   **Missing Columns**: The CSV must strictly follow the format: `Equipment Name, Type, Flowrate, Pressure, Temperature`.
-   **Database Locked**: If running the desktop app and backend efficiently, ensure SQLite isn't being locked by a hung process. Restart the server.
-   **PyQt Plugin Error**: If `qt.qpa.plugin: Could not find the Qt platform plugin "windows"`, ensure PyQt5 is installed correctly (`pip install pyqt5 --upgrade`).

## 6. Tech Stack
-   **Backend**: Python, Django, DRF, Pandas, ReportLab
-   **Frontend (Web)**: React, Vite, Chart.js, Axios
-   **Frontend (Desktop)**: Python, PyQt5, Matplotlib, Requests
