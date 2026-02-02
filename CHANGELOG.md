# Changelog

All notable changes to AI Study Buddy will be documented in this file.

## [2.2.0] - 2026-02-02

### 🎨 Flashcard Page Redesign

#### Major UI/UX Overhaul
- **NEW**: Modern flip-card interface with gradient animations
- **NEW**: Statistics dashboard showing total cards and difficulty breakdown
- **NEW**: Tabbed interface (Study Mode, Create Cards, Manage Cards)
- **NEW**: Search and filter functionality
- **NEW**: Shuffle mode for random card order
- **NEW**: Difficulty ratings (Easy, Medium, Hard) for each card
- **NEW**: Visual difficulty badges with color coding
- **NEW**: Improved card navigation with Previous/Next buttons
- **NEW**: Better manual card creation with difficulty selection

#### Performance Improvements
- Added `@st.cache_resource` to AI model loading for faster page loads
- Model loads only once and stays cached across sessions
- Database query optimization with proper column selection

#### Code Quality
- Updated database functions to support difficulty ratings
- Better error handling and logging
- Cleaner code structure with helper functions

---

## [2.1.0] - 2026-02-02

### 🚀 Phase 2: Major Feature Enhancements

#### Database & Performance
- Added database indexes on all frequently queried columns for faster lookups
- Implemented context manager for safer database connections
- Added input validation functions (username, exam date)
- Extended flashcards table with difficulty, review_count, last_reviewed columns
- Added priority column to exams table

#### Summarizer Enhancements
- **NEW**: DOCX file support - can now summarize Word documents
- **NEW**: Keyword extraction using YAKE algorithm (extracts 5 key topics)
- **NEW**: Adjustable summary length with sliders (50-500 words)
- **NEW**: Bullet-point formatting option for summaries
- **NEW**: Progress bar during summary generation
- Enhanced file upload with better feedback messages
- Improved error handling for file processing

#### UI/UX Improvements
- Created custom CSS with modern purple/blue gradient theme
- Improved button styling with gradients and hover effects
- Enhanced file uploader visual design
- Better success/error message styling
- Improved loading states and spinners
- More professional, polished interface

#### Code Quality
- Added comprehensive docstrings to new functions
- Improved error messages and logging
- Better code organization with helper functions

### 📦 New Dependencies
- `python-docx==1.1.0` - DOCX file processing
- `yake==0.4.8` - Keyword extraction

---

## [2.0.0] - 2026-02-02

### 🔐 Security Enhancements
- **BREAKING**: Replaced SHA256 with bcrypt for password hashing
  - Existing passwords will need to be reset
  - Much more secure against brute-force attacks
- Added comprehensive error handling and logging
- Implemented input validation across all forms

### ⚡ Performance Improvements
- Fixed duplicate model loading issue
- Implemented singleton pattern for AI model
- Added GPU acceleration support (automatic detection)
- Optimized database queries with better indexing

### 🎨 Code Quality
- Created shared sidebar component (eliminated code duplication)
- Added comprehensive docstrings and type hints
- Improved error messages and user feedback
- Restructured project with components directory

### 📚 Documentation
- Complete README overhaul with GSoC focus
- Added CONTRIBUTING.md guidelines
- Created LICENSE file (MIT)
- Added demo screenshots and banner
- Improved inline code documentation

### 🐛 Bug Fixes
- Fixed inconsistent file naming (5_flashcard.py → 5_Flashcard.py)
- Improved PDF text extraction with better error handling
- Added validation for empty text summarization

### 📦 Dependencies
- Added bcrypt==4.1.2
- Added PyMuPDF==1.24.0
- Added torch==2.2.0
- Added transformers==4.36.0
- Updated requirements.txt with all dependencies

## [1.0.0] - Initial Release

### Features
- Text and PDF summarization
- Flashcard generation and management
- Study session tracking
- Exam planning
- Performance reports
- User authentication
