<div align="center">

![AI Study Buddy Banner](assets/banner.png)

# 📚 AI Study Buddy

### Your Intelligent Learning Companion Powered by AI

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.37.0-FF4B4B.svg)](https://streamlit.io/)
[![Transformers](https://img.shields.io/badge/🤗%20Transformers-4.36.0-yellow.svg)](https://huggingface.co/transformers/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Beginner Friendly](https://img.shields.io/badge/Beginner-Friendly-success.svg)](https://github.com/NashAnam/AI_Study_Buddy)
[![GSoC 2026](https://img.shields.io/badge/GSoC-2026%20Ready-orange.svg)](https://summerofcode.withgoogle.com/)

> **Built by a GSoC 2026 Aspirant** | Demonstrating AI/ML skills, clean code architecture, and real-world problem solving

**[View Demo](#) • [Documentation](#installation) • [Report Bug](https://github.com/NashAnam/AI_Study_Buddy/issues) • [Request Feature](https://github.com/NashAnam/AI_Study_Buddy/issues)**

</div>

---

## 🎯 Why This Project?

As a **GSoC 2026 aspirant**, I built this project to demonstrate:
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
✅ Generate interactive flashcards automatically from study material  
✅ Track study sessions and visualize progress with analytics  
✅ Plan exams with intelligent scheduling and reminders  
✅ Get personalized insights and performance reports  

---

## ✨ Features

### 🤖 **AI-Powered Summarization**
- Instantly summarize long texts, PDFs, and documents using **BART** (Facebook's state-of-the-art transformer model)
- Supports chunked processing for documents exceeding 1024 tokens
- GPU acceleration for faster processing
- Download summaries as text files
- View history of all past summaries

![Summarizer Demo](assets/demo_summarizer.png)

### 🧠 **Smart Flashcard Generator**
- Convert study material into interactive Q&A flashcards
- Create, edit, and delete flashcards
- Review mode with flip animations
- Persistent storage for all your flashcards
- Bulk operations support

![Flashcard Demo](assets/demo_flashcard.png)

### 📅 **Exam Planner & Scheduler**
- Add upcoming exams with dates and difficulty levels
- Organize study schedules by subject
- Set priorities and add notes
- Visual calendar view
- Countdown timers for exams

### 📊 **Study Tracker & Analytics**
- Log study sessions with subject and duration
- Track daily, weekly, and monthly study patterns
- Visualize progress with interactive charts (Plotly)
- Subject-wise breakdown and statistics
- Identify peak productivity hours

### 📈 **Performance Reports**
- Generate comprehensive study reports
- Data-driven insights and recommendations
- Export reports as PDFs
- Track improvement over time
- Subject-wise performance analysis

### 🔐 **Secure User Management**
- Bcrypt password hashing (industry-standard security)
- User authentication and session management
- Isolated user data with SQL parameterized queries
- Secure login/registration system

---

## 💻 Tech Stack

### **Core Technologies**
- **Python 3.8+** - Primary programming language
- **Streamlit** - Modern web framework for data apps
- **SQLite** - Lightweight database for data persistence

### **AI/ML Libraries**
- **🤗 Transformers** - Hugging Face library for NLP models
- **PyTorch** - Deep learning framework with GPU support
- **BART (facebook/bart-large-cnn)** - Pre-trained summarization model

### **Data Processing & Visualization**
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Plotly** - Interactive visualizations
- **Matplotlib** - Statistical plotting

### **Document Processing**
- **PyMuPDF (fitz)** - PDF text extraction
- **ReportLab** - PDF report generation

### **Security**
- **bcrypt** - Password hashing and verification
- **hashlib** - Additional cryptographic functions

---

## 📂 Project Structure

```
ai_study_buddy/
│
├── app.py                      # Main application entry point
├── database.py                 # Database operations & schema
├── utils.py                    # Utility functions (password hashing, etc.)
├── requirements.txt            # Python dependencies
├── .env.example               # Environment configuration template
│
├── components/                 # Reusable UI components
│   ├── __init__.py
│   └── sidebar.py             # Shared navigation sidebar
│
├── pages/                      # Streamlit multi-page app
│   ├── 1_Welcome.py           # Landing page
│   ├── 2_Summarizer.py        # Text/PDF summarization
│   ├── 3_ExamPlanner.py       # Exam scheduling
│   ├── 4_StudyTracker.py      # Study session logging
│   ├── 5_Flashcard.py         # Flashcard management
│   ├── 6_Report.py            # Analytics & reports
│   ├── 7_FAQ.py               # Frequently asked questions
│   ├── 8_About.py             # About the project
│   └── 9_Feedback.py          # User feedback form
│
├── stud_modules/               # Backend modules
│   ├── summarizer.py          # AI summarization logic
│   ├── tracker.py             # Study tracking functions
│   ├── planner.py             # Exam planning utilities
│   └── auth.py                # Authentication helpers
│
├── assets/                     # Static files
│   ├── banner.png             # Application banner
│   └── demo_*.png             # Demo screenshots
│
└── final_clean_db.sqlite      # SQLite database
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
- 🧠 Create flashcards with clear, concise questions
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
- � **Logging**: Structured logging for debugging

### **Full-Stack Development**
- 🌐 **Web Framework**: Streamlit for interactive UI
- 🗄️ **Database**: SQLite with proper schema design
- 📊 **Data Visualization**: Plotly and Matplotlib charts
- 🎨 **UI/UX**: Clean, intuitive interface design

---

## 🛠️ Future Enhancements

### **Planned Features**
- [ ] Spaced repetition algorithm for flashcards (Leitner system)
- [ ] Multi-language support for summarization
- [ ] Voice input for notes and flashcards
- [ ] Mobile app (React Native/Flutter)
- [ ] Collaborative study groups
- [ ] Integration with Google Calendar
- [ ] OCR support for handwritten notes
- [ ] AI chatbot for Q&A assistance
- [ ] Dark mode theme
- [ ] Export data to Anki format

### **Technical Improvements**
- [ ] Migrate to PostgreSQL for production
- [ ] Add comprehensive unit tests
- [ ] Implement CI/CD pipeline
- [ ] Docker containerization
- [ ] REST API for mobile apps
- [ ] Redis caching for performance
- [ ] WebSocket for real-time updates

---

## 🤝 Contributing

Contributions are **welcome and encouraged**! This project is ideal for:
- 🎓 Students learning AI/ML and web development
- 💻 GSoC participants looking for meaningful projects
- 🌟 Open source enthusiasts wanting to help students worldwide

### **How to Contribute**

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### **Contribution Ideas**
- 🐛 Fix bugs or improve error handling
- ✨ Add new features from the roadmap
- 📝 Improve documentation
- 🎨 Enhance UI/UX design
- 🧪 Write tests
- 🌍 Add translations

---

## 🔐 Security Features

- ✅ **Bcrypt password hashing** with salt (12 rounds)
- ✅ **Parameterized SQL queries** to prevent SQL injection
- ✅ **User session management** with Streamlit
- ✅ **Input validation** and sanitization
- ⚠️ **Production Recommendations**:
  - Use HTTPS for deployment
  - Implement rate limiting for login attempts
  - Add CSRF protection
  - Use environment variables for secrets

---

## 📊 Performance

- **Model Loading**: Singleton pattern ensures model loads only once
- **GPU Acceleration**: Automatic detection and usage of CUDA-enabled GPUs
- **Chunked Processing**: Handles documents of any length efficiently
- **Database Indexing**: Optimized queries for fast data retrieval
- **Caching**: Streamlit's built-in caching for improved performance

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 About Me - GSoC 2026 Aspirant

**Nashrah Anam Fathima**  
Department of AI & Data Science  
JNTU Hyderabad

🎯 **GSoC 2026 Aspirant** passionate about AI/ML and open source  
💻 Building real-world projects to solve student challenges  
� Eager to contribute to impactful open source organizations  

### **Connect With Me**
- �📧 Email: [your-email@example.com](mailto:your-email@example.com)
- 💼 LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- 🐙 GitHub: [@NashAnam](https://github.com/NashAnam)
- 📝 Portfolio: [Your Portfolio](https://yourportfolio.com)

### **Why I'm a Great GSoC Candidate**
✅ Strong foundation in AI/ML and software engineering  
✅ Proven ability to build complete, production-ready applications  
✅ Excellent documentation and communication skills  
✅ Passionate about learning and contributing to open source  
✅ Self-motivated and able to work independently  

---

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) for the Transformers library
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Facebook AI](https://ai.facebook.com/) for the BART model
- All contributors and users of this project

---

## 📞 Support

If you encounter any issues or have questions:
- 🐛 [Open an issue](https://github.com/NashAnam/AI_Study_Buddy/issues)
- 💬 [Start a discussion](https://github.com/NashAnam/AI_Study_Buddy/discussions)
- 📧 Email the developer

---

## ⭐ Star History

If you find this project helpful, please consider giving it a ⭐ on GitHub!

---

<div align="center">

**Made with ❤️ for students worldwide**

### 🌟 GSoC 2026 Portfolio Project 🌟

**Demonstrating AI/ML expertise • Clean code architecture • Real-world impact**

*If you're a GSoC organization looking for passionate contributors, let's connect!*

[![Star this repo](https://img.shields.io/github/stars/NashAnam/AI_Study_Buddy?style=social)](https://github.com/NashAnam/AI_Study_Buddy)

</div>
