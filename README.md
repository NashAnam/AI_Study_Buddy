# 📚 AI Study Buddy

### Your Intelligent Learning Companion Powered by AI

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.37.0-FF4B4B.svg)](https://streamlit.io/)
[![Transformers](https://img.shields.io/badge/🤗%20Transformers-4.36.0-yellow.svg)](https://huggingface.co/transformers/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Beginner Friendly](https://img.shields.io/badge/Beginner-Friendly-success.svg)](https://github.com/NashAnam/AI_Study_Buddy)

> **An Intelligent Learning Companion** | Demonstrating AI/ML skills, clean code architecture, and real-world problem solving

**[View Demo](#) • [Documentation](#installation) • [Report Bug](https://github.com/NashAnam/AI_Study_Buddy/issues) • [Request Feature](https://github.com/NashAnam/AI_Study_Buddy/issues)**

</div>

---

## 🎯 Why This Project?

I built this project to demonstrate:
- 🤖 **AI/ML Expertise**: Implementing transformer models (BART) for real-world NLP tasks
- 🏗️ **Software Architecture**: Clean, modular code with separation of concerns
- 🔐 **Security Best Practices**: Industry-standard bcrypt hashing, SQL injection prevention
- 📊 **Full-Stack Development**: Backend logic, database design, and interactive UI
- 📚 **Technical Documentation**: Comprehensive README, contributing guidelines, and code docs

---

## 💡 Problem Statement

Students face several challenges in their learning journey:
- **Information Overload**: Difficulty processing and retaining large volumes of study material
- **Time Management**: Struggling to organize study schedules and track progress effectively
- **Active Recall**: Lack of efficient tools for creating and reviewing flashcards
- **Progress Tracking**: No centralized system to monitor study habits and performance
- **Exam Preparation**: Difficulty planning and prioritizing multiple exams

**AI Study Buddy** solves these problems by providing an all-in-one AI-powered platform that helps students:
✅ Summarize lengthy documents instantly using state-of-the-art NLP models  
✅ Track study sessions and visualize progress with analytics  
✅ Plan exams with intelligent scheduling and reminders  
✅ Get personalized insights and performance reports  

---

## ✨ Features

### 📄 **AI-Powered Summarizer**
- Instantly summarize any length of text, from single sentences to massive PDFs.
- **Intelligent Chunking**: Seamlessly processes documents exceeding model limits using a poly-chunking strategy.
- **Visual Feedback**: Real-time progress tracking with AI status indicators.
- **Keywords Extraction**: Automatically identifies key topics using the YAKE algorithm.
- **Built-in Copy**: Integrated code blocks for one-click summary copying.


### 📅 **Smart Exam Planner**
- **Unified Interface**: Subject and topic merged for faster task entry.
- **Flexible Scheduling**: Accepts any time format (e.g., "9 AM", "Morning", "23:00").
- **Integrated Actions**: One-click completion and deletion directly from the card.
- **Dynamic Tracking**: Real-time "Tasks Due This Week" counter.

### 🎯 **Advanced Study Tracker**
- **Interactive Timer**: Start/Stop focused sessions that log directly to your history.
- **Automated Progress**: Real-time subject-wise breakdown chart.
- **Gamified Achievements**: Earn badges like "On Fire!" and "Knowledge Seeker" as you study.

---

## 💻 Tech Stack

### **Core Technologies**
- **Python 3.13+** - Primary programming language
- **Streamlit 1.50.1** - High-performance web framework
- **SQLite** - Robust data persistence with automated migrations

### **AI/ML Infrastructure**
- **🤗 Transformers & PyTorch** - Powering the BART-large-cnn summarization engine
- **YAKE** - Statistical keyword extraction
- **PyMuPDF & python-docx** - High-fidelity document parsing

---

## 📂 Project Structure

```
ai_study_buddy/
│
├── app.py                      # Dashboard & Authentication
├── database.py                 # DB Schema & Automated Migrations
├── utils.py                    # AI Pipelines & Core Logic
├── requirements.txt            # Project Dependencies
│
├── components/                 
│   └── navbar.py              # Fluid Navigation Overhaul
│
├── pages/                      
│   ├── Summarizer.py          # AI Text & File Analysis
│   ├── ExamPlanner.py         # Smart Task Management
│   ├── StudyTracker.py        # Progress Logging & Timer
│   └── Report.py              # Visual Analytics Hub
│
├── static/                     
│   └── custom.css             # Premium Responsive Styling
│
└── study_buddy.sqlite          # Local Data Store
```

---

## 🚀 Installation

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package manager)
- Git

### **Quick Start**

1. **Clone the repository**
   ```bash
   git clone https://github.com/NashAnam/AI_Study_Buddy.git
   cd AI_Study_Buddy
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional)
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the app**
   - Open your browser and navigate to `http://localhost:8501`
   - Default login credentials:
     - **Username**: `admin`
     - **Password**: `admin123`

---

## 📖 Usage Guide

### **First Time Setup**
1. Register a new account or use the default admin credentials
2. Navigate through the sidebar to explore features
3. Start by uploading a document to the Summarizer
4. Create flashcards from your study material
5. Log your study sessions in the Study Tracker
6. Add upcoming exams in the Exam Planner
7. View your progress in the Reports section

### **Tips for Best Results**
- 📄 For best summarization results, use well-formatted text or PDFs
- ⏱️ Log study sessions immediately after completing them
- 📅 Update exam dates regularly for accurate planning
- 📊 Review reports weekly to track improvement

---

## 🎓 Technical Skills Demonstrated

This project showcases my proficiency in:

### **AI/ML & NLP**
- 🤖 **Transformer Models**: Implemented Facebook's BART for text summarization
- ⚡ **Performance Optimization**: GPU acceleration with automatic device detection
- 🧠 **Model Management**: Singleton pattern for efficient resource usage
- 📄 **Document Processing**: PDF text extraction with PyMuPDF

### **Software Engineering**
- 🏗️ **Clean Architecture**: Modular design with separation of concerns
- 🔄 **DRY Principle**: Reusable components (shared sidebar, utilities)
- 📝 **Documentation**: Comprehensive docstrings, type hints, and README
- 🐛 **Error Handling**: Robust exception handling and logging

### **Security & Best Practices**
- 🔐 **Authentication**: Bcrypt password hashing (12 rounds)
- 🛡️ **SQL Injection Prevention**: Parameterized queries
- ✅ **Input Validation**: Comprehensive data validation
-  **Logging**: Structured logging for debugging

### **Full-Stack Development**
- 🌐 **Web Framework**: Streamlit for interactive UI
- 🗄️ **Database**: SQLite with proper schema design
- 📊 **Data Visualization**: Plotly and Matplotlib charts
- 🎨 **UI/UX**: Clean, intuitive interface design




## 👩‍💻 About Me

**Nashrah Anam Fathima**  
Department of AI & Data Science  
JNTU Hyderabad

🎯 **Aspirant** passionate about AI/ML and open source  
💻 Building real-world projects to solve student challenges  
 Eager to contribute to impactful open source organizations  

### **Connect With Me**
- 📧 Email: [nashrahanam36@gmail.com](mailto:nashrahanam36@gmail.com)
- 💼 LinkedIn: [Nashrah Anam](https://www.linkedin.com/in/nashrah-anam-351a322a0/)
- 🐙 GitHub: [@NashAnam](https://github.com/NashAnam)
- 📝 Portfolio: [My Portfolio](https://nashanam.github.io/portfolio/)

---

## ⭐ Star History

If you find this project helpful, please consider giving it a ⭐ on GitHub!

---

**Made with ❤️ for students worldwide**

### 🌟 Portfolio Project 🌟


[![Star this repo](https://img.shields.io/github/stars/NashAnam/AI_Study_Buddy?style=social)](https://github.com/NashAnam/AI_Study_Buddy)
