# 🧠 AI Study Buddy
### Your Intelligent Learning Companion — Powered by AI
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.37.0-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![HuggingFace](https://img.shields.io/badge/🤗_Transformers-4.36.0-FFD21E.svg?style=for-the-badge)](https://huggingface.co/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-22c55e.svg?style=for-the-badge)](LICENSE)
**[🚀 Quick Start](#-installation) · [✨ Features](#-features) · [📂 Project Structure](#-project-structure) · [🐛 Report Bug](https://github.com/NashAnam/AI_Study_Buddy/issues)**
</div>
---
## 🎯 What is AI Study Buddy?
**AI Study Buddy** is a full-stack, AI-powered web application that acts as your personal learning assistant. It combines real-time NLP summarization, interactive study tracking with a live timer, smart exam planning, and a comprehensive analytics dashboard — all in a single, beautiful app.
Built with **Streamlit + SQLite + HuggingFace Transformers**, it runs entirely locally with no external API costs.
---
## ✨ Features
### 📄 AI-Powered Summarizer
- Paste text or upload **PDF, DOCX, or TXT** files for instant summarization
- Powered by **DistilBART-CNN** (HuggingFace Transformers) with intelligent poly-chunking for long documents
- **Configurable summary length** (10–100%) wired directly to the model's `max_length`
- **Keyword extraction** via the YAKE algorithm
- **Summary history** with formatted timestamps, one-click copy, and delete options
- Quick-load sample templates (Scientific Article, Historical Text, Biology Notes)
### 📅 Smart Exam Planner
- Add tasks with **title, subject, due date, time, and priority** (Low / Medium / High)
- Color-coded priority strips on task cards (red / blue / green)
- One-click **mark as done** or **delete** directly from each card
- **Completed tasks** in a collapsible expander section with delete support
- Real-time stats: Total Tasks · Completed · Upcoming · This Week
- **Live calendar widget** showing today's date and pending count
- Proper form error handling via session-state flags (no silent drops)
### 🎯 Study Tracker
- **Live session timer** — start a focused session and watch it count up in real time (`HH:MM:SS`), auto-refreshing every 5 seconds
- Sessions are logged automatically on stop with subject and duration
- **Manual session logging** form (subject + duration in minutes)
- Weekly activity **bar chart** with per-day hour labels
- Subject-wise **progress bars** ranked by total minutes
- **Achievements system**: On Fire! (3+ day streak) · Knowledge Seeker (10+ hrs) · Polymath (5+ subjects) · Weekly Warrior (5+ hrs this week)
- Live timer card visible in sidebar while session is active
### 📊 Study Report
- Overview stat cards: Daily Goal % · Total Hours · Subjects · Streak
- **Weekly activity bar chart** (last 7 days)
- **Subject breakdown table** with session counts and progress bars
- **Personalized insights**: Great Consistency · Productive Week · Diverse Learner · Goal Achieved
- **Weekly goal card** (10h target) with progress bar
- **Download report** as a `.txt` file including the full weekly breakdown
### 🏠 Dashboard (Home)
- Personalized welcome hero with **live daily goal progress bar** (60 min target)
- Real-time stats: Study Streak · Hours This Week · Subjects Studied
- Quick-action cards linking to every page
- **Today's Schedule** panel showing tasks due today with pending count
### 🔐 Authentication
- **Secure registration & login** with bcrypt password hashing (12 rounds)
- Parameterized SQL queries (injection-safe)
- Input validation with clear error messages
- Session-state based routing — all pages protected behind auth guards
---
## 💻 Tech Stack
|
 Layer 
|
 Technology 
|
|
-------
|
-----------
|
|
**
Web Framework
**
|
 Streamlit 1.37.0 
|
|
**
Language
**
|
 Python 3.8+ 
|
|
**
AI / NLP
**
|
 HuggingFace Transformers — DistilBART-CNN-12-6 
|
|
**
Keyword Extraction
**
|
 YAKE 
|
|
**
Document Parsing
**
|
 PyMuPDF (PDF) · python-docx (DOCX) 
|
|
**
Database
**
|
 SQLite (with automated schema migrations) 
|
|
**
Auth
**
|
 bcrypt (12 rounds) 
|
|
**
Styling
**
|
 Vanilla CSS (Inter font, glassmorphism, animations) 
|
|
**
Data
**
|
 pandas · numpy 
|
---
## 📂 Project Structure
```
ai_study_buddy/
│
├── app.py                  # Entry point — Auth + Dashboard
├── database.py             # SQLite schema, migrations & all DB queries
├── utils.py                # AI pipeline, CSS loader, file parser, keyword extractor
├── requirements.txt        # All dependencies (pinned versions)
│
├── components/
│   └── navbar.py           # Custom sticky navigation bar (dynamic username)
│
├── pages/
│   ├── Summarizer.py       # AI text & file summarization page
│   ├── ExamPlanner.py      # Task management & exam scheduling page
│   ├── StudyTracker.py     # Live timer, logging & achievement page
│   └── Report.py           # Analytics & insights dashboard page
│
├── static/
│   └── custom.css          # Full design system (cards, nav, charts, animations)
│
├── .streamlit/
│   └── config.toml         # Theme config (blue primary, sidebar hidden)
│
└── study_buddy.sqlite      # Auto-created local database
```
---
## 🚀 Installation
### Prerequisites
- Python 3.8 or higher
- pip
- Git
### Quick Start
**1. Clone the repository**
```bash
git clone https://github.com/NashAnam/AI_Study_Buddy.git
cd AI_Study_Buddy
```
**2. Create and activate a virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```
**3. Install dependencies**
```bash
pip install -r requirements.txt
```
> ⚠️ `torch` and `transformers` are large packages (~1–2 GB). The first install and first summarization will take a few minutes to download the model weights.
**4. Run the application**
```bash
streamlit run app.py
```
**5. Open in your browser**
```
http://localhost:8501
```
### Default Login
|
 Field 
|
 Value 
|
|
-------
|
-------
|
|
 Username 
|
`admin`
|
|
 Password 
|
`admin123`
|
> You can also register a new account from the landing page.
---
## 📖 Usage Guide
### Getting Started
1. Open the app and **log in** (or register a new account)
2. The **Dashboard** shows your daily goal, streak, and weekly hours at a glance
3. Use the **top navbar** to navigate between pages — no sidebar needed
### Summarizer
1. Go to **📄 Summarizer**
2. Paste text in the text box **or** upload a PDF/DOCX/TXT file
3. Adjust the **Summary Length** slider (10–100%)
4. Click **✨ Generate Summary**
5. Your summary is saved to history automatically — delete or copy anytime
### Study Tracker
1. Go to **🎯 Tracker**
2. Click **▶️ Start Session** — the timer starts counting live
3. Click **🟥 Stop** when done — the session is logged automatically
4. Or use the **📝 Manual Log** form to add past sessions
5. Track progress in the **Weekly Activity** chart and **Subject Progress** bars
### Exam Planner
1. Go to **📅 Planner**
2. Fill in the **Add Task** form on the right: title, subject, date, time, priority
3. Click **Add Task** — it appears in the Upcoming Tasks list immediately
4. Click **✅ Done** to complete or **🗑️** to delete any task
### Report
1. Go to **📊 Report**
2. View overall stats, weekly chart, and subject breakdown
3. Read personalized **Insights & Tips** based on your activity
4. Click **📥 Download Report** to save a `.txt` summary
---
## 🔧 Key Technical Decisions
|
 Decision 
|
 Rationale 
|
|
----------
|
-----------
|
|
**
DistilBART
**
 over BART-large 
|
 6× smaller, runs on CPU, same quality for student notes 
|
|
**
Poly-chunking
**
 strategy 
|
 Handles documents longer than the model's 1024-token limit 
|
|
**
SQLite
**
 over PostgreSQL 
|
 Zero config, file-based, perfect for local/single-user apps 
|
|
**
Absolute CSS path
**
 (
`os.path.abspath`
) 
|
 Fixes CSS loading when Streamlit's CWD differs from project root 
|
|
**
Session-state flags
**
 for form errors 
|
 Avoids Streamlit's "cannot call st.error() in a callback" limitation 
|
|
**
`time.sleep(5)`
 + 
`st.rerun()`
**
 for timer 
|
 Lightweight real-time update without WebSocket complexity 
|
|
**
bcrypt rounds=12
**
|
 Balances security with acceptable login latency 
|
---
## 🐛 Known Limitations
- The AI summarizer requires an internet connection on **first run** to download model weights (~500 MB). After that it works fully offline.
- The live study timer uses polling (`sleep + rerun`), so it refreshes every ~5 seconds — not millisecond-precise.
- SQLite is single-user by design. For multi-user deployments, switch to PostgreSQL.
---
## 👩‍💻 About the Developer
**Nashrah Anam Fathima**
Department of AI & Data Science · JNTU Hyderabad
Passionate about building AI-powered tools that solve real student problems.
| | |
|--|--|
| 📧 Email | [nashrahanam36@gmail.com](mailto:nashrahanam36@gmail.com) |
| 💼 LinkedIn | [Nashrah Anam](https://www.linkedin.com/in/nashrah-anam-351a322a0/) |
| 🐙 GitHub | [@NashAnam](https://github.com/NashAnam) |
| 🌐 Portfolio | [nashanam.github.io/portfolio](https://nashanam.github.io/portfolio/) |
---
## 📄 License
This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
---
<div align="center">
**Made with ❤️ for students worldwide**
[![Star this repo](https://img.shields.io/github/stars/NashAnam/AI_Study_Buddy?style=social)](https://github.com/NashAnam/AI_Study_Buddy)
*If this project helped you, please give it a ⭐ — it means a lot!*
</div>
