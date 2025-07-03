<p align="center">
  <img src="https://raw.githubusercontent.com/Iceycoast/Iceycoast/main/banner.png" alt="Medicoast banner" />
</p>

<h1 align="center">Medicoast – Modular Health Tracker System</h1>
<h4 align="center">🚀 Rebuilding the 40-Step Health App from Scratch – Now with SQL, Modular Design & Flet UI</h4>

---

## 🧠 Project Overview

This repository is the **official reboot** of the original 40-step health tracker challenge — now redesigned as a fully modular, scalable, and professional-grade app called **Medicoast**.

- 🧱 **From JSON to SQL** – All trackers now use a central SQLite DB
- 🎯 **Modular Architecture** – Clean folders, reusable logic, screen separation
- 🌐 **Web App with Flet** – Accessible on both desktop and mobile
- 👤 **Multi-User Support** – Each entry tied to a unique `username`
- 🧠 **AI Integration** – GPT-based health summaries, advice, trends
- 🔐 **Local-first, cloud-ready**

---

## 🔁 Why This Repo Exists

> I'm restarting the 40-question mega project with a better approach:  
> Clean SQL-powered storage, Flet-based modern GUI, and full separation of backend + frontend.

This project will grow in phases and serve as my flagship health tech app, designed to scale into something production-worthy.

---

## ⚙️ Tech Stack

- **Python 3.11+**
- **SQLite** – Local relational DB
- **Flet** – GUI framework for desktop + web apps
- **OpenAI API** – AI-powered summaries, trend detection
- **dotenv** – For secret management
- **Modular Design** – Separate logic for each tracker

---

## 🧩 Trackers Being Rebuilt

| Tracker         | Status       |
| --------------- | ------------ |
| 💧 Water Intake | ⏳ Rewriting |
| 🍽️ Meals        | ⏳ Upcoming  |
| ⚖️ BMI Tracker  | ⏳ Upcoming  |
| 😴 Sleep        | ⏳ Upcoming  |
| 💊 Medication   | ⏳ Upcoming  |
| 😄 Mood         | ⏳ Upcoming  |
| 📓 Journal      | ⏳ Upcoming  |
| 🧘 Habits       | ⏳ Upcoming  |

➡️ Each tracker will have:

- Its own **SQL schema**
- A **modular logic file** (`logic.py`)
- A **Flet UI screen** for interaction

---

## 📁 Project Structure

```bash
medicoast/
├── run.py              # Web app launcher
├── db/                 # SQLite .db file
├── app/                # Logic modules
├── ui/                 # Flet screens/components
├── assets/             # Icons, banners
├── .env                # API keys
└── README.md           # You're here
```

---

## 🔜 Upcoming Milestones

- [ ] ✅ Scaffold `db_utils.py` + SQLite setup
- [ ] ✅ Create login system using unique usernames
- [ ] ⏳ Build Q1: Water Tracker (SQL + GUI)
- [ ] ⏳ Launch app in browser via Flet
- [ ] ⏳ Add AI summaries using OpenAI

---

## ✍️ Author

> **Iceycoast**  
> From story-driven games to code-driven apps — I build clean, AI-enhanced health tools with Python.  
> ⚒️ Currently mastering SQL, backend architecture, and clean UI workflows.

---

## 🧠 Project Context

This is part of a personal challenge to rebuild my entire original 40-step health tracker using:

- Real DBs
- Real architecture
- Real-world app standards

Follow this repo as it evolves into a production-grade health assistant.
