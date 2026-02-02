import streamlit as st
import os
import database
import utils
from components.navbar import render_navbar

# --- Page Config ---
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize DB on start
database.init_all_tables()

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

def load_css():
    css_file = os.path.join("static", "custom.css")
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    load_css()
    
    if st.session_state.logged_in:
        show_dashboard()
    else:
        show_landing_page()

def show_landing_page():
    # Reduced Spacer
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_content, col_spacer, col_login = st.columns([1.2, 0.2, 0.8])
    
    with col_content:
        st.markdown("""
<div style="margin-bottom: 1.5rem;">
<span style="background:#2563eb; color:white; padding: 8px 12px; border-radius:12px; font-weight:700; font-size:1.2rem;">🧠</span>
<span style="font-weight:700; font-size:1.5rem; color:#1f2937; margin-left:0.5rem;">AI Study Buddy</span>
</div>
<h1 style="font-size: 3.5rem; line-height: 1.1; margin-bottom: 1.5rem; font-weight: 800;">
<span style="color:#2563eb;">Master Your Studies</span><br>
<span class="gradient-text">with AI Power</span>
</h1>
<p style="font-size: 1.25rem; color: #6b7280; line-height: 1.6; margin-bottom: 2.5rem; max_width: 90%;">
Your intelligent learning companion. Generate summaries, track your study habits, and organize your exam prep—all in one place.
</p>
""", unsafe_allow_html=True)
        
        st.markdown("""
<div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 2.5rem;">
<div class="feature-pill" style="background:#eff6ff; color:#2563eb; border-color:#bfdbfe;">⚡ AI Summarizer</div>
<div class="feature-pill" style="background:#fff7ed; color:#ea580c; border-color:#fed7aa;">📊 Study Analytics</div>
<div class="feature-pill" style="background:#f0fdf4; color:#16a34a; border-color:#bbf7d0;">📅 Smart Planning</div>
</div>
""", unsafe_allow_html=True)
        
        st.markdown("""
<div class="bullet-item"><div class="bullet-dot"></div>AI-powered text summarization</div>
<div class="bullet-item"><div class="bullet-dot"></div>Comprehensive study tracking and analytics</div>
<div class="bullet-item"><div class="bullet-dot"></div>Personalized learning insights</div>
""", unsafe_allow_html=True)

    with col_login:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align:center; margin-bottom:1.5rem;">Welcome Back</h2>', unsafe_allow_html=True)
        tab_login, tab_rego = st.tabs(["Login", "Register"])
        with tab_login:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form("login_form"):
                u = st.text_input("Username", placeholder="e.g. nashrah")
                p = st.text_input("Password", type="password")
                c1, c2 = st.columns([1,1])
                with c1: st.checkbox("Remember me", value=False)
                with c2: st.markdown("<div style='text-align:right; color:#2563eb; font-size:0.9rem; cursor:pointer;'>Forgot password?</div>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                if st.form_submit_button("Sign In →", type="primary", use_container_width=True):
                    user = database.get_user(u)
                    if user and utils.verify_password(p, user[1]):
                        st.session_state.logged_in = True
                        st.session_state.username = u
                        st.rerun()
                    else: st.error("Invalid credentials")
        with tab_rego:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form("register_form"):
                nu = st.text_input("Choose Username")
                np = st.text_input("Choose Password", type="password")
                ncp = st.text_input("Confirm Password", type="password")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.form_submit_button("Create Account", type="primary", use_container_width=True):
                    if np != ncp: st.error("Passwords do not match")
                    elif not nu or not np: st.error("Fields cannot be empty")
                    else:
                        if database.add_user(nu, utils.hash_password(np)): st.success("Account created! Please login.")
                        else: st.error("Username already taken")
        st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard():
    render_navbar(active_page="Home")
    
    username = st.session_state.username
    stats = database.get_user_stats(username)
    
    # --- 1. Welcome Hero Section ---
    st.markdown(f"""
<div class="hero-card">
<div style="background:rgba(255,255,255,0.2); width:fit-content; padding:4px 12px; border-radius:8px; font-size:0.8rem; margin-bottom:1rem;">
✨ Welcome back!
</div>
<h1>Hello, {username}! 👋</h1>
<p style="opacity:0.9; font-size:1.1rem; margin-bottom:2rem;">
You're on track and ready to explore your personal AI study assistant
</p>
<div style="background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2); padding:1rem; border-radius:12px; max-width:600px;">
<div style="font-size:0.9rem; opacity:0.9; margin-bottom:0.5rem;">Daily Learning Goal (60m)</div>
<div class="progress-bg"><div class="progress-fill" style="width: {stats['daily_goal_pct']}%;"></div></div>
<div style="font-size:0.8rem; opacity:0.8; margin-top:0.5rem;">{stats['daily_goal_pct']}% complete</div>
</div>
</div>
""", unsafe_allow_html=True)
    
    # --- 2. Stats Grid ---
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(f"""
<div class="stat-card">
<div style="color:#64748b; font-size:0.9rem; margin-bottom:0.5rem;">Study Streak</div>
<div style="display:flex; justify-content:space-between; align-items:center;">
<div style="font-size:1.8rem; font-weight:700;">{stats['streak']} <span style="font-size:1rem; font-weight:400; color:#64748b;">days</span></div>
<div style="background:#fef9c3; color:#ca8a04; width:40px; height:40px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1.2rem;">⚡</div>
</div>
</div>
""", unsafe_allow_html=True)
    with s2:
        st.markdown(f"""
<div class="stat-card">
<div style="color:#64748b; font-size:0.9rem; margin-bottom:0.5rem;">Hours This Week</div>
<div style="display:flex; justify-content:space-between; align-items:center;">
<div style="font-size:1.8rem; font-weight:700;">{stats['hours_week']} <span style="font-size:1rem; font-weight:400; color:#64748b;">hrs</span></div>
<div style="background:#dbeafe; color:#2563eb; width:40px; height:40px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1.2rem;">🕒</div>
</div>
</div>
""", unsafe_allow_html=True)
    with s3:
        st.markdown(f"""
<div class="stat-card">
<div style="color:#64748b; font-size:0.9rem; margin-bottom:0.5rem;">Topics Mastered</div>
<div style="display:flex; justify-content:space-between; align-items:center;">
<div style="font-size:1.8rem; font-weight:700;">{stats['topics_mastered']} <span style="font-size:1rem; font-weight:400; color:#64748b;">topics</span></div>
<div style="background:#dcfce7; color:#16a34a; width:40px; height:40px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1.2rem;">📈</div>
</div>
</div>
""", unsafe_allow_html=True)
        
    
    # --- 3. Main Content (Actions & Schedule) ---
    c_main, c_sched = st.columns([2, 1])
    
    with c_main:
        st.markdown("### Quick Actions")
        st.markdown("<div style='color:#64748b; margin-bottom:1.5rem;'>Choose an action to get started with your study session</div>", unsafe_allow_html=True)
        
        ac1, ac2 = st.columns(2)
        with ac1:
            st.markdown("""
<div class="action-card" style="margin-bottom:0.5rem;">
<div class="icon-box" style="background:linear-gradient(135deg, #3b82f6, #06b6d4); width:40px; height:40px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:white; margin-bottom:1rem; font-size:1.2rem;">📄</div>
<h3 style="margin:0; font-size:1.1rem; color:#1e293b;">Summarize Notes</h3>
<p style="color:#64748b; font-size:0.9rem; margin-top:0.5rem;">AI-powered text summarization</p>
</div>
""", unsafe_allow_html=True)
            if st.button("Open Summarizer", key="btn_sum", use_container_width=True, type="primary"):
                 st.switch_page("pages/Summarizer.py")
            
            
            st.markdown("""
<div class="action-card" style="margin-bottom:0.5rem;">
<div class="icon-box" style="background:linear-gradient(135deg, #f97316, #ef4444); width:40px; height:40px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:white; margin-bottom:1rem; font-size:1.2rem;">🎯</div>
<h3 style="margin:0; font-size:1.1rem; color:#1e293b;">Track Progress</h3>
<p style="color:#64748b; font-size:0.9rem; margin-top:0.5rem;">Monitor your learning journey</p>
</div>
""", unsafe_allow_html=True)
            if st.button("Open Tracker", key="btn_track", use_container_width=True, type="primary"):
                 st.switch_page("pages/StudyTracker.py")
            
        with ac2:
            st.markdown("""
<div class="action-card" style="margin-bottom:0.5rem;">
<div class="icon-box" style="background:linear-gradient(135deg, #10b981, #10b981); width:40px; height:40px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:white; margin-bottom:1rem; font-size:1.2rem;">📅</div>
<h3 style="margin:0; font-size:1.1rem; color:#1e293b;">Plan Exam Prep</h3>
<p style="color:#64748b; font-size:0.9rem; margin-top:0.5rem;">Smart study scheduling</p>
</div>
""", unsafe_allow_html=True)
            if st.button("Open Planner", key="btn_plan", use_container_width=True, type="primary"):
                 st.switch_page("pages/ExamPlanner.py")
 
            
            st.markdown("""
<div class="action-card" style="margin-bottom:0.5rem;">
<div class="icon-box" style="background:linear-gradient(135deg, #8b5cf6, #d946ef); width:40px; height:40px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:white; margin-bottom:1rem; font-size:1.2rem;">📊</div>
<h3 style="margin:0; font-size:1.1rem; color:#1e293b;">View Insights</h3>
<p style="color:#64748b; font-size:0.9rem; margin-top:0.5rem;">Deep dive into your performance</p>
</div>
""", unsafe_allow_html=True)
            if st.button("Open Report", key="btn_report", use_container_width=True, type="primary"):
                 st.switch_page("pages/Report.py")

    with c_sched:
        today_tasks = database.get_todays_tasks(username)
        count_pending = len(today_tasks)
        
        st.markdown(f"""
<div style="background:white; border:1px solid #e2e8f0; border-radius:16px; padding:1.5rem; height:100%;">
<h3 style="margin-top:0; font-size:1.2rem;">Today's Schedule</h3>
<p style="color:#64748b; font-size:0.9rem; margin-bottom:1.5rem;"> You have {count_pending} tasks today</p>
""", unsafe_allow_html=True)

        if not today_tasks:
             st.markdown('<div style="color:#94a3b8; font-style:italic; font-size:0.9rem;">No tasks due today. Enjoy your free time!</div>', unsafe_allow_html=True)
        else:
             for t in today_tasks[:4]: # Limit to 4
                completed_class = "completed" if t['completed'] else ""
                check_icon = "✓" if t['completed'] else ""
                time_display = f"• {t['time_str']}" if t['time_str'] else ""
                
                # Render simple item
                # Note: 'task-item' and 'completed' classes handle styles. 
                # If completed, check needs styling. 
                # If NOT completed, we show a circle?
                icon_html = f'<div style="color:#16a34a;">{check_icon}</div>' if t['completed'] else '<div style="width:20px; height:20px; border:2px solid #cbd5e1; border-radius:50%;"></div>'
                
                st.markdown(f"""
<div class="task-item {completed_class}">
{icon_html}
<div>
<div style="font-weight:500; font-size:0.95rem; {('text-decoration:line-through; color:#64748b;' if t['completed'] else '')}">{t['title']}</div>
<div style="color:#64748b; font-size:0.8rem;">{t['subject'] or 'General'} {time_display}</div>
</div>
</div>
""", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True) # End card
        
        st.write("")
        if st.button("View All Tasks", use_container_width=True):
            st.switch_page("pages/ExamPlanner.py")

if __name__ == "__main__":
    main()
