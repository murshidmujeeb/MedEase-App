# MedEase - Pharmacy Automation System

A complete end-to-end pharmacy workflow automation system powered by Gemini AI.

## Features
- **Prescription Scanning**: Extract medicines from images using Google Gemini Vision.
- **Automated Billing**: Generates bills with GST calculations.
- **Inventory Management**: Real-time tracking and deduction.
- **Role-Based Access**: PIN-based pharmacist authentication.

## Tech Stack
- **Backend**: FastAPI, PostgreSQL, SQLAlchemy
- **Frontend**: React, TypeScript, Tailwind CSS
- **AI**: Google Gemini Pro Vision
- **Infrastructure**: Docker Compose

## Prerequisites
- Docker & Docker Compose
- Google Gemini API Key

## Setup & Run

1.  **Configure Environment**
    Create a `.env` file in the root (or set env var):
    ```bash
    GOOGLE_API_KEY=your_gemini_api_key_here
    ```

2.  **Build and Run**
    ```bash
    docker-compose up --build
    ```

3.  **Access the Application**
    - Frontend: [http://localhost:5173](http://localhost:5173)
    - Backend API: [http://localhost:8000/docs](http://localhost:8000/docs)

## Default Credentials
- **Pharmacist PIN**: `1234` (for confirming bills)

## Development
- **Backend**: `cd backend && python -m uvicorn app.main:app --reload`
- **Frontend**: `cd frontend && npm run dev`

## Database
The database is automatically seeded with ~5 demo medicines and 1 admin pharmacist on first run.
