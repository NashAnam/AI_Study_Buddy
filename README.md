# 🧠 AI Study Buddy

### Your Intelligent Learning Companion — Powered by AI

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB.svg?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.37.0-FF4B4B.svg?style=for-the-badge\&logo=streamlit\&logoColor=white)](https://streamlit.io/)
[![HuggingFace](https://img.shields.io/badge/🤗_Transformers-4.36.0-FFD21E.svg?style=for-the-badge)](https://huggingface.co/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57.svg?style=for-the-badge\&logo=sqlite\&logoColor=white)](https://sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-22c55e.svg?style=for-the-badge)](LICENSE)

**🚀 Quick Start • ✨ Features • 📂 Project Structure • 🐛 Report Bug**

---

# 🎯 What is AI Study Buddy?

**AI Study Buddy** is a full-stack AI-powered web application that acts as your personal learning assistant. It combines real-time NLP summarization, interactive study tracking with a live timer, smart exam planning, and a comprehensive analytics dashboard—all in one beautiful application.

Built with **Streamlit + SQLite + HuggingFace Transformers**, it runs entirely locally with no external API costs.

---

# ✨ Features

## 📄 AI-Powered Summarizer

* Paste text or upload **PDF, DOCX, or TXT** files
* Powered by **DistilBART-CNN** (HuggingFace Transformers)
* Intelligent poly-chunking for long documents
* Configurable summary length (10–100%)
* Keyword extraction using **YAKE**
* Summary history with timestamps
* Copy or delete previous summaries
* Built-in sample templates

---

## 📅 Smart Exam Planner

* Add tasks with title, subject, due date, time, and priority
* Color-coded priority cards
* Mark tasks as completed
* Delete tasks instantly
* Completed tasks section
* Live statistics
* Calendar widget
* Proper validation and error handling

---

## 🎯 Study Tracker

* Live study session timer
* Automatic session logging
* Manual study log
* Weekly activity chart
* Subject-wise progress bars
* Achievement system
* Sidebar live timer

---

## 📊 Study Report

* Daily goal tracking
* Weekly study statistics
* Subject breakdown
* Personalized insights
* Weekly goal progress
* Download study report (.txt)

---

## 🏠 Dashboard

* Personalized welcome page
* Daily goal progress
* Study streak
* Weekly hours
* Quick navigation cards
* Today's schedule

---

## 🔐 Authentication

* Secure registration & login
* bcrypt password hashing
* SQL injection protection
* Session-based authentication
* Protected pages

---

# 💻 Tech Stack

| Layer              | Technology                                     |
| ------------------ | ---------------------------------------------- |
| Web Framework      | Streamlit 1.37                                 |
| Language           | Python 3.8+                                    |
| AI / NLP           | HuggingFace Transformers (DistilBART-CNN-12-6) |
| Keyword Extraction | YAKE                                           |
| Document Parsing   | PyMuPDF, python-docx                           |
| Database           | SQLite                                         |
| Authentication     | bcrypt                                         |
| Styling            | Vanilla CSS                                    |
| Data Processing    | pandas, numpy                                  |

---

# 📂 Project Structure

```text
ai_study_buddy/

├── app.py
├── database.py
├── utils.py
├── requirements.txt

├── components/
│   └── navbar.py

├── pages/
│   ├── Summarizer.py
│   ├── ExamPlanner.py
│   ├── StudyTracker.py
│   └── Report.py

├── static/
│   └── custom.css

├── .streamlit/
│   └── config.toml

└── study_buddy.sqlite
```

---

# 🚀 Installation

## Prerequisites

* Python 3.8+
* Git
* pip

## 1. Clone Repository

```bash
git clone https://github.com/NashAnam/AI_Study_Buddy.git

cd AI_Study_Buddy
```

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `torch` and `transformers` will download model weights during the first installation.

## 4. Run Application

```bash
streamlit run app.py
```

## 5. Open Browser

```
http://localhost:8501
```

---

# 🔑 Default Login

| Field    | Value    |
| -------- | -------- |
| Username | admin    |
| Password | admin123 |

You can also register a new account.

---

# 📖 Usage Guide

## Dashboard

* View today's progress
* Check study streak
* Track weekly hours
* Navigate using the top navbar

## Summarizer

1. Open **Summarizer**
2. Paste text or upload a document
3. Adjust summary length
4. Click **Generate Summary**

## Study Tracker

1. Start study session
2. Timer runs automatically
3. Stop session to save it
4. View charts and achievements

## Exam Planner

1. Add a task
2. Choose priority
3. Set due date
4. Mark complete or delete

## Report

* Weekly charts
* Subject analytics
* Download report
* Personalized insights

---

# 🔧 Key Technical Decisions

| Decision           | Reason                             |
| ------------------ | ---------------------------------- |
| DistilBART         | Smaller and faster than BART-large |
| Poly-chunking      | Supports long documents            |
| SQLite             | Lightweight and zero configuration |
| Absolute CSS Path  | Reliable CSS loading               |
| Session State      | Better Streamlit form handling     |
| sleep() + rerun()  | Simple live timer                  |
| bcrypt (12 rounds) | Secure password hashing            |

---

# 🐛 Known Limitations

* First summarization downloads model weights.
* Timer refreshes every 5 seconds.
* SQLite is intended for local single-user usage.

---

#  About the Developer

## Nashrah Anam Fathima

**Department of AI & Data Science**


Passionate about building AI-powered applications that solve real student problems.

| Platform     | Link                                                      |
| ------------ | --------------------------------------------------------- |
| 📧 Email     | [nashrahanam36@gmail.com](mailto:nashrahanam36@gmail.com) |
| 💼 LinkedIn  | https://www.linkedin.com/in/nashrah-anam-351a322a0/       |
| 🐙 GitHub    | https://github.com/NashAnam                               |
| 🌐 Portfolio | https://nashanam.github.io/portfolio/                     |

---



---

# ⭐ Support

If you found this project helpful, consider giving it a **Star ⭐** on GitHub.



