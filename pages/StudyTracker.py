import streamlit as st
import pandas as pd
import datetime
import time
import database
import utils
from components.navbar import render_navbar

# --- Page Setup ---
st.set_page_config(page_title="Study Tracker", page_icon="🎯", layout="wide", initial_sidebar_state="collapsed")

# Auth guard
if "username" not in st.session_state or not st.session_state.username:
    st.warning("🔒 Please log in to access this page.")
    if st.button("Go to Login"):
        st.switch_page("app.py")
    st.stop()

username = st.session_state.username

# Session Timer State
if "session_start_time" not in st.session_state:
    st.session_state.session_start_time = None
if "session_active" not in st.session_state:
    st.session_state.session_active = False
if "session_subject" not in st.session_state:
    st.session_state.session_subject = "Focused Session"


def start_session(subject):
    st.session_state.session_active = True
    st.session_state.session_start_time = datetime.datetime.now()
    st.session_state.session_subject = subject or "Focused Session"


def stop_session():
    end_time = datetime.datetime.now()
    start_time = st.session_state.session_start_time
    duration = end_time - start_time
    minutes = int(duration.total_seconds() / 60)

    if minutes > 0:
        database.add_study_log(username, st.session_state.session_subject, minutes)
        st.toast(f"✅ Logged {minutes} min for '{st.session_state.session_subject}'!")
    else:
        st.toast("Session too short to log (< 1 min).")

    st.session_state.session_active = False
    st.session_state.session_start_time = None


# --- Load CSS & Navbar ---
utils.load_css()
render_navbar(active_page="Tracker")

# --- Data Fetching ---
stats = database.get_user_stats(username)
weekly_data = database.get_weekly_activity(username)

# --- Page Header ---
c_head, c_btn = st.columns([0.75, 0.25])
with c_head:
    st.markdown("""
<div style="margin-bottom:0.5rem;">
<h2 style="margin:0; font-size:1.8rem; font-weight:700; color:#1e293b;">🎯 Study Tracker</h2>
<p style="color:#64748b; margin:0.25rem 0 0 0;">Monitor your learning progress and stay motivated</p>
</div>
""", unsafe_allow_html=True)

with c_btn:
    st.write("")
    if st.session_state.session_active:
        elapsed = datetime.datetime.now() - st.session_state.session_start_time
        total_secs = int(elapsed.total_seconds())
        hours, remainder = divmod(total_secs, 3600)
        mins, secs = divmod(remainder, 60)
        timer_display = f"{hours:02d}:{mins:02d}:{secs:02d}" if hours > 0 else f"{mins:02d}:{secs:02d}"
        if st.button(f"🟥 Stop — {timer_display}", use_container_width=True, type="primary"):
            stop_session()
            st.rerun()
    else:
        if st.button("▶️ Start Session", use_container_width=True):
            # Subject can be chosen from the manual log; default to Focused Session
            start_session(st.session_state.get("quick_subject", "Focused Session"))
            st.rerun()

# Auto-refresh timer while session is active (every 5 seconds)
if st.session_state.session_active:
    time.sleep(5)
    st.rerun()

# --- Stats Row ---
s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown(f"""
<div class="ui-card">
<div style="display:flex; justify-content:space-between; align-items:center;">
<div>
<div style="color:#64748b; font-size:0.88rem; margin-bottom:0.3rem;">Total Hours</div>
<div style="font-size:2rem; font-weight:700; color:#1e293b;">{stats['total_hours']}</div>
</div>
<div style="background:#eff6ff; width:48px; height:48px; border-radius:12px; display:flex; align-items:center; justify-content:center; color:#2563eb; font-size:1.4rem;">🕒</div>
</div>
</div>
""", unsafe_allow_html=True)

with s2:
    st.markdown(f"""
<div class="ui-card">
<div style="display:flex; justify-content:space-between; align-items:center;">
<div>
<div style="color:#64748b; font-size:0.88rem; margin-bottom:0.3rem;">This Week</div>
<div style="font-size:2rem; font-weight:700; color:#1e293b;">{stats['hours_week']}</div>
</div>
<div style="background:#f0fdf4; width:48px; height:48px; border-radius:12px; display:flex; align-items:center; justify-content:center; color:#16a34a; font-size:1.4rem;">📅</div>
</div>
</div>
""", unsafe_allow_html=True)

with s3:
    st.markdown(f"""
<div class="ui-card">
<div style="display:flex; justify-content:space-between; align-items:center;">
<div>
<div style="color:#64748b; font-size:0.88rem; margin-bottom:0.3rem;">Subjects</div>
<div style="font-size:2rem; font-weight:700; color:#1e293b;">{stats['topics_mastered']}</div>
</div>
<div style="background:#faf5ff; width:48px; height:48px; border-radius:12px; display:flex; align-items:center; justify-content:center; color:#9333ea; font-size:1.4rem;">📖</div>
</div>
</div>
""", unsafe_allow_html=True)

with s4:
    st.markdown(f"""
<div class="ui-card">
<div style="display:flex; justify-content:space-between; align-items:center;">
<div>
<div style="color:#64748b; font-size:0.88rem; margin-bottom:0.3rem;">Study Streak</div>
<div style="font-size:2rem; font-weight:700; color:#1e293b;">{stats['streak']} <span style="font-size:1rem; color:#64748b;">days</span></div>
</div>
<div style="background:#fefce8; width:48px; height:48px; border-radius:12px; display:flex; align-items:center; justify-content:center; color:#ca8a04; font-size:1.4rem;">⚡</div>
</div>
</div>
""", unsafe_allow_html=True)

# --- Main Content Grid ---
col_main, col_side = st.columns([2.2, 1])

with col_main:
    # Weekly Activity Bar Chart
    max_h = max([d['hours'] for d in weekly_data], default=0)
    if max_h == 0:
        max_h = 1

    html_bars = ""
    for d in weekly_data:
        h_pct = max((d['hours'] / max_h) * 100, 2)  # minimum 2% height for visibility
        hours_label = f"{d['hours']}h" if d['hours'] > 0 else ""
        html_bars += f"""
<div class="bar-column">
<div style="font-size:0.7rem; color:#64748b; margin-bottom:2px;">{hours_label}</div>
<div class="bar-visual" style="height:{h_pct}%; background:linear-gradient(to top, #2563eb, #60a5fa);"></div>
<div class="bar-label">{d['day']}</div>
</div>
"""

    st.markdown(f"""
<div class="ui-card">
<h3>📊 Weekly Activity</h3>
<p>Your study hours over the past 7 days</p>
<div class="bar-chart-container">
{html_bars}
</div>
</div>
""", unsafe_allow_html=True)

    # Subject Progress
    st.markdown("""
<div class="ui-card">
<h3>📚 Subject Progress</h3>
<p>Time spent studying each subject</p>
""", unsafe_allow_html=True)

    try:
        conn = database.get_db_connection()
        rows = conn.execute(
            "SELECT subject, sum(duration_minutes) as mins FROM study_logs "
            "WHERE username = ? GROUP BY subject ORDER BY mins DESC",
            (username,)
        ).fetchall()
        conn.close()

        if not rows:
            st.info("Log study sessions with different subjects to see your progress breakdown here!")
        else:
            max_mins = rows[0]['mins'] if rows else 1
            for r in rows:
                sub = r['subject'] or "General"
                m = r['mins']
                prog = min(int((m / max_mins) * 100), 100)
                hours_str = f"{round(m/60, 1)}h" if m >= 60 else f"{m}m"

                st.markdown(f"""
<div style="margin-bottom:1rem;">
<div style="display:flex; justify-content:space-between; font-size:0.88rem; margin-bottom:0.3rem;">
<span style="font-weight:500; color:#1e293b;">{sub}</span>
<span style="color:#64748b;">{hours_str}</span>
</div>
<div class="progress-track"><div class="progress-fill-blue" style="width: {prog}%;"></div></div>
</div>
""", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading subject data: {e}")

    st.markdown("</div>", unsafe_allow_html=True)


with col_side:
    # Live Timer Card
    if st.session_state.session_active:
        elapsed = datetime.datetime.now() - st.session_state.session_start_time
        total_secs = int(elapsed.total_seconds())
        hours, remainder = divmod(total_secs, 3600)
        mins, secs = divmod(remainder, 60)
        timer_str = f"{hours:02d}:{mins:02d}:{secs:02d}" if hours > 0 else f"{mins:02d}:{secs:02d}"
        st.markdown(f"""
<div class="ui-card" style="text-align:center; background:linear-gradient(135deg,#eff6ff,#eef2ff); border-color:#c7d2fe;">
<div style="font-size:0.85rem; color:#64748b; font-weight:500; margin-bottom:0.5rem;">⏱️ Session in Progress</div>
<div style="font-size:2.5rem; font-weight:800; color:#2563eb; font-variant-numeric:tabular-nums;">{timer_str}</div>
<div style="font-size:0.8rem; color:#64748b; margin-top:0.4rem;">📖 {st.session_state.session_subject}</div>
</div>
""", unsafe_allow_html=True)

    # Achievements
    st.markdown("""
<div class="ui-card">
<h3>🏅 Achievements</h3>
""", unsafe_allow_html=True)

    earned_any = False
    if stats['streak'] >= 3:
        earned_any = True
        st.markdown("""
<div class="achieve-item">
<div style="font-size:1.5rem;">⚡</div>
<div><div style="font-weight:600; font-size:0.9rem;">On Fire!</div><div style="font-size:0.8rem; color:#64748b;">3+ Day Streak</div></div>
</div>
""", unsafe_allow_html=True)

    if stats['total_hours'] >= 10:
        earned_any = True
        st.markdown("""
<div class="achieve-item">
<div style="font-size:1.5rem;">🏆</div>
<div><div style="font-weight:600; font-size:0.9rem;">Knowledge Seeker</div><div style="font-size:0.8rem; color:#64748b;">10+ Hours Studied</div></div>
</div>
""", unsafe_allow_html=True)

    if stats['topics_mastered'] >= 5:
        earned_any = True
        st.markdown("""
<div class="achieve-item">
<div style="font-size:1.5rem;">🎓</div>
<div><div style="font-weight:600; font-size:0.9rem;">Polymath</div><div style="font-size:0.8rem; color:#64748b;">5+ Subjects Studied</div></div>
</div>
""", unsafe_allow_html=True)

    if stats['hours_week'] >= 5:
        earned_any = True
        st.markdown("""
<div class="achieve-item">
<div style="font-size:1.5rem;">🚀</div>
<div><div style="font-weight:600; font-size:0.9rem;">Weekly Warrior</div><div style="font-size:0.8rem; color:#64748b;">5+ Hours This Week</div></div>
</div>
""", unsafe_allow_html=True)

    if not earned_any:
        st.markdown("<p style='font-size:0.85rem; color:#94a3b8;'>Keep studying to earn your first badge!</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Quick Manual Log
    with st.container(border=True):
        st.markdown("### 📝 Log Session")
        with st.form("manual_log", clear_on_submit=True):
            sub = st.text_input("Subject", placeholder="e.g. DSA, ML, Physics",
                                key="quick_subject")
            dur = st.number_input("Duration (minutes)", min_value=1, max_value=480, value=30)
            if st.form_submit_button("➕ Log Session", use_container_width=True, type="primary"):
                if sub:
                    database.add_study_log(username, sub, dur)
                    st.toast(f"✅ Logged {dur}m for {sub}!")
                    st.rerun()
                else:
                    st.error("Subject is required.")
