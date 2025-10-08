# AI Study Buddy 🚀

**AI Study Buddy** is an **AI-powered learning companion** designed to help students **study smarter and stay organized**. It combines **text summarization, flashcard generation, study planning, and progress tracking** in a single, interactive platform.  

---

## 🌟 Features

- 📄 **Smart Summarizer:** Instantly summarize long texts or PDFs.  
- 🧠 **Flashcard Generator:** Convert study material into interactive Q&A flashcards.  
- 📅 **Exam Planner & Study Tracker:** Organize schedules, log study sessions, and track progress.  
- 📊 **Reports & Analytics:** Visualize performance with charts and feedback.  

---

## 💻 Tech Stack

- **Python** – Core programming language  
- **Streamlit** – Web app interface  
- **Hugging Face Transformers** – AI models for summarization  
- **PyMuPDF (fitz)** – PDF text extraction  
- **SQLite** – Database storage  
- **Matplotlib / Plotly** – Visualizations  

---

## 📂 Project Structure

ai_study_buddy/

│

├── Main.py # App entry point

├── database.py # Database operations

├── utils.py # Helper functions

├── requirements.txt # Dependencies

│

├── pages/ # Streamlit pages

│ ├── 1_Welcome.py

│ ├── 2_Summarizer.py

│ ├── 3_ExamPlanner.py

│ ├── 4_StudyTracker.py

│ ├── 5_Flashcard.py

│ ├── 6_Report.py

│ ├── 7_FAQ.py

│ ├── 8_About.py

│ └── 9_Feedback.py

│

├── stud_modules/ # Backend modules

│ ├── summarizer.py

│ ├── tracker.py

│ ├── planner.py

│ └── auth.py

│

├── assets/ # Images / GIFs / icons

└── final_clean_db.sqlite # Database



## 🔐 Security Features

- Password hashing (SHA256)  
- Parameterized SQL queries to prevent SQL injection  
- User session management and isolation  

> ⚠️ For production: use bcrypt for passwords and enable HTTPS.  

---

## 👩‍💻 Developer

**Nashrah Anam Fathima**  
Department of AI & Data Science — JNTU Hyderabad  

---

