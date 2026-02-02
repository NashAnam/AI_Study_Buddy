# Performance Optimization Tips

## 🚀 Speed Up Your AI Study Buddy

### Current Optimizations Applied:
✅ **Model Caching**: AI model loads only once using `@st.cache_resource`
✅ **Database Indexes**: Faster queries with indexed columns
✅ **Pagination**: Shows only last 10 summaries instead of all
✅ **Context Manager**: Efficient database connections

### Why First Load is Slow:
1. **Model Download** (~1.6GB): BART model downloads on first run
2. **Model Loading**: Transformer initialization takes time
3. **CPU Processing**: Without GPU, processing is slower

### How to Speed It Up:

#### 1. **Model Already Downloaded?**
After the first load, the model is cached. Subsequent visits should be **much faster**.

#### 2. **Use GPU (Optional)**
If you have an NVIDIA GPU:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
This can make summarization **10x faster**!

#### 3. **Reduce Model Size (Alternative)**
For faster loading, you can use a smaller model. Edit `stud_modules/summarizer.py`:
```python
# Change from:
model="facebook/bart-large-cnn"
# To:
model="sshleifer/distilbart-cnn-12-6"  # Smaller, faster
```

#### 4. **Clear Cache if Needed**
If the app feels slow, clear Streamlit cache:
- Press `C` in the running app
- Or restart: `Ctrl+C` then `streamlit run app.py`

### Expected Load Times:
- **First Time**: 30-60 seconds (downloading model)
- **Subsequent Loads**: 5-10 seconds (model cached)
- **With GPU**: 2-3 seconds
- **Other Pages**: Instant (no model loading)

### Pages That Load Instantly:
- ✅ Home
- ✅ Flashcards
- ✅ Study Tracker
- ✅ Exam Planner
- ✅ Reports
- ⏳ Summarizer (only slow on first load)

The slow loading is **normal for AI models** and only happens once! 🚀
