import streamlit as st
import pandas as pd
import datetime
import time
import database
from components.navbar import render_navbar

# --- Setup ---
st.set_page_config(page_title="Study Tracker", page_icon="🎯", layout="wide")

if "username" not in st.session_state or not st.session_state.username:
    st.warning("Please log in.")
    st.stop()
    
username = st.session_state.username

# Session Timer State
if "session_start_time" not in st.session_state:
    st.session_state.session_start_time = None
if "session_active" not in st.session_state:
    st.session_state.session_active = False

def load_css():
    with open("static/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def toggle_session():
    if not st.session_state.session_active:
        # Start
        st.session_state.session_active = True
        st.session_state.session_start_time = datetime.datetime.now()
        st.rerun()
    else:
        # Stop & Save
        end_time = datetime.datetime.now()
        start_time = st.session_state.session_start_time
        duration = end_time - start_time
        minutes = int(duration.total_seconds() / 60)
        
        # Log to DB (default subject 'General' for quick session, or ask user? 
        # For simplicity, we'll log as 'General Study' or allow subject selection before start?)
        # Let's save as 'Focused Session'.
        if minutes > 0:
            database.add_study_log(username, "Focused Session", minutes)
            st.toast(f"Logged {minutes} minutes of study!")
        else:
            st.toast("Session too short to log.")
            
        st.session_state.session_active = False
        st.session_state.session_start_time = None
        # st.rerun() is redundant in a callback

def main():
    load_css()
    render_navbar(active_page="Tracker")
    
    # --- Data Fetching ---
    stats = database.get_user_stats(username)
    weekly_data = database.get_weekly_activity(username)
    
    # --- Header ---
    c_head, c_btn = st.columns([0.8, 0.2])
    with c_head:
        st.markdown("""
<div style="margin-bottom:0.5rem;">
<h2 style="margin:0; font-size:1.8rem; font-weight:700;">Study Tracker</h2>
<p style="color:#64748b; margin:0;">Monitor your learning progress and stay motivated</p>
</div>
""", unsafe_allow_html=True)
    with c_btn:
        st.write("") 
        
        # Interactive Session Button
        if st.session_state.session_active:
            # Active State
            elapsed = datetime.datetime.now() - st.session_state.session_start_time
            elapsed_mins = int(elapsed.total_seconds() / 60)
            st.button(f"🟥 Stop ({elapsed_mins}m)", on_click=toggle_session, use_container_width=True, type="primary")
        else:
            # Inactive State
            st.button("⏰ Start Session", on_click=toggle_session, use_container_width=True)


    # --- Stats Row (Real Data) ---
    s1, s2, s3, s4 = st.columns(4)
    
    with s1:
        st.markdown(f"""
<div class="ui-card">
<div style="display:flex; justify-content:space-between;">
<div><div style="color:#64748b; font-size:0.9rem;">Total Hours</div><div style="font-size:2rem; font-weight:700;">{stats['total_hours']}</div></div>
<div style="background:#eff6ff; width:48px; height:48px; border-radius:12px; display:flex; align-items:center; justify-content:center; color:#2563eb; font-size:1.2rem;">🕒</div>
</div>
</div>
""", unsafe_allow_html=True)
    
    with s2:
        st.markdown(f"""
<div class="ui-card">
<div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
<div><div style="color:#64748b; font-size:0.9rem;">This Week</div><div style="font-size:2rem; font-weight:700;">{stats['hours_week']}</div></div>
<div style="background:#f0fdf4; width:48px; height:48px; border-radius:12px; display:flex; align-items:center; justify-content:center; color:#16a34a; font-size:1.2rem;">📅</div>
</div>
</div>
""", unsafe_allow_html=True)
        
    with s3:
        st.markdown(f"""
<div class="ui-card">
<div style="display:flex; justify-content:space-between;">
<div><div style="color:#64748b; font-size:0.9rem;">Subjects</div><div style="font-size:2rem; font-weight:700;">{stats['topics_mastered']}</div></div>
<div style="background:#faf5ff; width:48px; height:48px; border-radius:12px; display:flex; align-items:center; justify-content:center; color:#9333ea; font-size:1.2rem;">📖</div>
</div>
</div>
""", unsafe_allow_html=True)
        
    with s4:
        st.markdown(f"""
<div class="ui-card">
<div style="display:flex; justify-content:space-between;">
<div><div style="color:#64748b; font-size:0.9rem;">Study Streak</div><div style="font-size:2rem; font-weight:700;">{stats['streak']}</div></div>
<div style="background:#fefce8; width:48px; height:48px; border-radius:12px; display:flex; align-items:center; justify-content:center; color:#ca8a04; font-size:1.2rem;">⚡</div>
</div>
</div>
""", unsafe_allow_html=True)

    # --- Main Content Grid ---
    col_main, col_side = st.columns([2.2, 1])

    with col_main:
        # Weekly Activity Bar Chart (Real Data)
        with st.container():
            # Find max hours for scaling
            max_h = max([d['hours'] for d in weekly_data]) if weekly_data else 1
            if max_h == 0: max_h = 1
            
            html_bars = ""
            for d in weekly_data:
                h_pct = (d['hours'] / max_h) * 100
                html_bars += f"""
<div class="bar-column">
<div class="bar-visual" style="height:{h_pct}%; background:linear-gradient(to top, #2563eb, #60a5fa);"></div>
<div class="bar-label">{d['day']}</div>
</div>
"""
            
            st.markdown(f"""
<div class="ui-card">
<h3>Weekly Activity</h3>
<p>Your study hours over the past 7 days</p>
<div class="bar-chart-container">
{html_bars}
</div>
</div>
""", unsafe_allow_html=True)

        # Subject Progress Wrapper
        with st.container():
            st.markdown("""
<div class="ui-card">
<h3>Subject Progress</h3>
<p>Track your study time by subject</p>
""", unsafe_allow_html=True)
            
            # Fetch real logs for subjects
            try:
                conn = database.get_db_connection()
                rows = conn.execute("SELECT subject, sum(duration_minutes) as mins FROM study_logs WHERE username = ? GROUP BY subject ORDER BY mins DESC", (username,)).fetchall()
                conn.close()
                
                if not rows:
                    st.info("Log more study sessions with different subjects to see detailed progress here!")
                else:
                    max_mins = rows[0]['mins'] if rows else 1
                    for r in rows:
                        sub = r['subject'] or "General"
                        m = r['mins']
                        prog = min(int((m / max_mins) * 100), 100)
                        
                        st.markdown(f"""
<div style="margin-bottom:1rem;">
<div style="display:flex; justify-content:space-between; font-size:0.9rem; margin-bottom:0.25rem;">
<span>{sub}</span>
<span>{m} mins</span>
</div>
<div class="progress-track"><div class="progress-fill-blue" style="width: {prog}%;"></div></div>
</div>
""", unsafe_allow_html=True)
            except:
                st.error("Error loading subject progress")
            
            st.markdown("</div>", unsafe_allow_html=True) 

    with col_side:
        # Achievements (Dynamic based on logic)
        st.markdown("""
<div class="ui-card">
<h3>Achievements</h3>
""", unsafe_allow_html=True)
        
        # 1. Streak Badge
        if stats['streak'] >= 3:
            st.markdown("""
<div class="achieve-item">
<div style="color:#ca8a04;">⚡</div>
<div><div style="font-weight:600; font-size:0.9rem;">On Fire!</div><div style="font-size:0.8rem; color:#64748b;">3+ Day Streak</div></div>
</div>
""", unsafe_allow_html=True)
        
        # 2. Total Hours Badge
        if stats['total_hours'] >= 10:
             st.markdown("""
<div class="achieve-item">
<div style="color:#2563eb;">🏆</div>
<div><div style="font-weight:600; font-size:0.9rem;">Knowledge Seeker</div><div style="font-size:0.8rem; color:#64748b;">10+ Total Hours</div></div>
</div>
""", unsafe_allow_html=True)

        # 3. Topic Mastery Badge
        if stats['topics_mastered'] >= 5:
             st.markdown("""
<div class="achieve-item">
<div style="color:#16a34a;">🎓</div>
<div><div style="font-weight:600; font-size:0.9rem;">Polymath</div><div style="font-size:0.8rem; color:#64748b;">5+ Subjects Studied</div></div>
</div>
""", unsafe_allow_html=True)
             
        if stats['streak'] < 3 and stats['total_hours'] < 10 and stats['topics_mastered'] < 5:
             st.markdown("<p style='font-size:0.8rem; color:#94a3b8;'>Start a streak or study more subjects to earn badges!</p>", unsafe_allow_html=True)
             
        st.markdown("</div>", unsafe_allow_html=True)

        # Quick Manual Log
        with st.container(border=True):
             st.markdown("### 📝 Manual Log")
             with st.form("manual_log", clear_on_submit=True):
                 sub = st.text_input("Subject", placeholder="e.g. DSA, ML, Physics")
                 dur = st.number_input("Duration (minutes)", min_value=1, value=30)
                 if st.form_submit_button("Log Session", use_container_width=True):
                     if sub:
                        database.add_study_log(username, sub, dur)
                        st.toast(f"Logged {dur}m for {sub}!")
                        st.rerun()
                     else:
                        st.error("Subject required")

if __name__ == "__main__":
    main()
