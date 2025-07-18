# MediCoast

**MediCoast** is a modular health and wellness tracking application built with FastAPI. It provides endpoints for tracking water intake, meals, BMI, sleep, mood, medication, and generates daily AI-powered summaries and weekly PDF health reports.

---

## Features

- **User Management**: Register, login, and manage users with JWT-based authentication.
- **Trackers**:
  - **Water Intake**: Log and view daily water consumption.
  - **Meals**: Track meals and calories.
  - **BMI**: Log BMI entries and receive AI-generated advice.
  - **Sleep**: Record sleep sessions and durations.
  - **Mood**: Track daily moods, with AI utilities for insights.
  - **Medication**: Log medications taken.
- **Summaries**:
  - **Daily Summary**: AI-generated, friendly daily health summaries using OpenAI.
  - **Weekly Summary**: Aggregated stats and downloadable PDF reports with graphs.
- **Modular Design**: Each tracker and summary feature is organized in its own module for maintainability.
- **Logging**: All actions are logged to `logs/medicoast.log` for monitoring and debugging.

---

## Project Structure

```
Medicoast/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── logger.py
│   ├── startup.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── medicoast.db
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   └── jwt.py
│   │
│   ├── users/
│   │   ├── __init__.py
│   │   ├── controller.py
│   │   ├── db.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── schema.sql
│   │   └── utils.py
│   │
│   ├── summary/
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   │
│   │   ├── daily_summary/
│   │   │   ├── __init__.py
│   │   │   ├── ai_summary.py
│   │   │   ├── controller.py
│   │   │   ├── db.py
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   ├── schema.sql
│   │   │   └── utils.py
│   │   │
│   │   └── weekly_summary/
│   │       ├── __init__.py
│   │       ├── controller.py
│   │       ├── db.py
│   │       ├── models.py
│   │       ├── routes.py
│   │       │
│   │       └── pdf_generator/
│   │           ├── __init__.py
│   │           ├── graphs_generator.py
│   │           ├── pdf_generator.py
│   │           └── utils.py
│   │
│   ├── trackers/
│   │   ├── bmi_tracker/
│   │   │   ├── __init__.py
│   │   │   ├── ai_advice.py
│   │   │   ├── controller.py
│   │   │   ├── db.py
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   ├── schema.sql
│   │   │   └── utils.py
│   │   │
│   │   ├── meals_tracker/
│   │   │   ├── __init__.py
│   │   │   ├── controller.py
│   │   │   ├── db.py
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   └── schema.sql
│   │   │
│   │   ├── medication_tracker/
│   │   │   ├── __init__.py
│   │   │   ├── controller.py
│   │   │   ├── db.py
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   └── schema.sql
│   │   │
│   │   ├── mood_tracker/
│   │   │   ├── __init__.py
│   │   │   ├── ai_utils.py
│   │   │   ├── controller.py
│   │   │   ├── db.py
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   └── schema.sql
│   │   │
│   │   ├── sleep_tracker/
│   │   │   ├── __init__.py
│   │   │   ├── controller.py
│   │   │   ├── db.py
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   ├── schema.sql
│   │   │   └── utils.py
│   │   │
│   │   └── water_tracker/
│   │       ├── __init__.py
│   │       ├── controller.py
│   │       ├── db.py
│   │       ├── models.py
│   │       ├── routes.py
│   │       ├── schema.sql
│   │       └── utils.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── validators.py
│
├── logs/
│   └── medicoast.log
│
├── requirements.txt
└── README.md
```

---

## Setup & Installation

1. **Clone the repository**:

   ```bash
   git clone <repo-url>
   cd Medicoast
   ```

2. **Create a virtual environment and install dependencies**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Environment Variables**:

   - Create a `.env` file in the root or `app/` directory with:
     ```
     JWT_SECRET_KEY=your_secret_key
     OPENAI_API_KEY=your_openai_key
     DB_PATH=app/db/medicoast.db
     AI_MODEL=gpt-3.5-turbo
     ```
   - The app will auto-create the database folder if it doesn't exist.

4. **Run the Application**:

   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000`.

---

## API Overview

- **User Endpoints** (`/users`):

  - `POST /register` — Register a new user
  - `POST /login` — Login and receive JWT
  - `GET /check-username/{username}` — Check username availability

- **Trackers**:

  - `/water` — Log, view, and delete water intake
  - `/meals` — Log, view, and delete meals
  - `/bmi` — Log, view, delete BMI, and get AI advice
  - `/sleep` — Log, view, and delete sleep sessions
  - `/mood` — Log, view, and delete moods
  - `/medication` — Log, view, and delete medications

- **Summaries**:
  - `GET /summary/daily?date=YYYY-MM-DD` — Get daily AI summary
  - `GET /summary/weekly/pdf` — View weekly PDF report
  - `GET /summary/weekly/pdf/download` — Download weekly PDF report

> **Note:** All tracker and summary endpoints require authentication via JWT.

---

## Technology Stack

- **Backend**: Python (FastAPI)
- **Database**: SQLite (auto-initialized with schema files)
- **AI Integration**: OpenAI API for summaries and advice
- **PDF Generation**: FPDF
- **Data Analysis & Graphs**: pandas, matplotlib
- **Authentication**: JWT
- **Logging**: Python logging module

---

## Development Notes

- **Schema Initialization**: On startup, all `schema.sql` files are executed to ensure the database is up-to-date.
- **Logging**: All logs are written to `logs/medicoast.log`.
- **Modularity**: Each tracker and summary feature is self-contained for easy extension.

---

## Contributing

1. Fork the repo and create your branch.
2. Commit your changes.
3. Push to your branch and open a Pull Request.

---

## Future Features

- Fully working front end using:
  - HTML
  - CSS
  - Tailwind CSS
  - React JS

**Author:** Amit Bal (Iceycoast)
