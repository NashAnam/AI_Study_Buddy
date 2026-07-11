import streamlit as st
import database
import utils
from components.navbar import render_navbar
from datetime import datetime

# --- Page Setup ---
st.set_page_config(page_title="Study Report", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

# Auth guard
if "username" not in st.session_state or not st.session_state.username:
    st.warning("🔒 Please log in to view your report.")
    if st.button("Go to Login"):
        st.switch_page("app.py")
    st.stop()

username = st.session_state.username

# --- Load CSS & Navbar ---
utils.load_css()
render_navbar(active_page="Report")

# --- Fetch Data ---
stats = database.get_user_stats(username)
weekly = database.get_weekly_activity(username)

# --- Page Header ---
c_head, c_btn = st.columns([0.75, 0.25])
with c_head:
    st.markdown("""
<div style="margin-bottom:0.5rem;">
<h2 style="margin:0; font-size:1.8rem; font-weight:700; color:#1e293b;">📊 Study Report</h2>
<p style="color:#64748b; margin:0.25rem 0 0 0;">Comprehensive analysis of your learning progress</p>
</div>
""", unsafe_allow_html=True)

with c_btn:
    st.write("")
    # Build a richer report
    report_lines = [
        f"AI Study Buddy — Report for @{username}",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "=== Performance Summary ===",
        f"Daily Goal Completion : {stats['daily_goal_pct']}%",
        f"Total Hours Studied   : {stats['total_hours']}h",
        f"Hours This Week       : {stats['hours_week']}h",
        f"Subjects Covered      : {stats['topics_mastered']}",
        f"Current Streak        : {stats['streak']} days",
        "",
        "=== Weekly Breakdown ===",
    ]
    for d in weekly:
        report_lines.append(f"  {d['day']}: {d['hours']}h")

    report_data = "\n".join(report_lines)

    st.download_button(
        label="📥 Download Report",
        data=report_data,
        file_name=f"study_report_{username}_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
        use_container_width=True,
        type="primary"
    )

# --- Stats Row ---
s1, s2, s3, s4 = st.columns(4)

def stat_card(col, title, value, badge_text, badge_color, icon, bg_gradient):
    with col:
        st.markdown(f"""
<div class="ui-card" style="background:{bg_gradient}; border:1px solid rgba(0,0,0,0.04);">
<div style="display:flex; justify-content:space-between; margin-bottom:1rem;">
<div style="background:white; width:48px; height:48px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:1.4rem; box-shadow:0 1px 3px rgba(0,0,0,0.07);">
{icon}
</div>
<div style="background:white; border:1px solid {badge_color}; color:#374151; padding:2px 10px; border-radius:99px; font-size:0.75rem; font-weight:600; height:fit-content; display:flex; align-items:center;">
{badge_text}
</div>
</div>
<div style="font-size:0.88rem; color:#64748b; margin-bottom:0.2rem;">{title}</div>
<div style="font-size:2rem; font-weight:700; color:#1e293b;">{value}</div>
</div>
""", unsafe_allow_html=True)

stat_card(s1, "Daily Goal",    f"{stats['daily_goal_pct']}%", "Today",    "#bfdbfe", "🎯", "linear-gradient(135deg, #eff6ff, #ecfeff)")
stat_card(s2, "Total Hours",   f"{stats['total_hours']}h",   "All Time", "#bbf7d0", "🕒", "linear-gradient(135deg, #f0fdf4, #ecfdf5)")
stat_card(s3, "Subjects",      str(stats['topics_mastered']), "Active",  "#e9d5ff", "📖", "linear-gradient(135deg, #faf5ff, #fdf4ff)")
stat_card(s4, "Streak",        f"{stats['streak']}d",        "Days",     "#fed7aa", "🏆", "linear-gradient(135deg, #fff7ed, #fef2f2)")

st.markdown("<br>", unsafe_allow_html=True)

# --- Main Content Grid ---
col_main, col_side = st.columns([2.2, 1])

with col_main:
    # Weekly Activity Chart
    max_h = max([d['hours'] for d in weekly], default=0)
    if max_h == 0:
        max_h = 1

    html_bars = ""
    for m in weekly:
        h_pct = max((m['hours'] / max_h) * 100, 2)
        label = f"{m['hours']}h" if m['hours'] > 0 else ""
        html_bars += f"""
<div class="bar-column">
<div style="font-size:0.7rem; color:#64748b; margin-bottom:2px;">{label}</div>
<div class="bar-visual" style="height:{h_pct}%; background:linear-gradient(to top, #2563eb, #6366f1);"></div>
<div class="bar-label">{m['day']}</div>
</div>
"""

    st.markdown(f"""
<div class="ui-card">
<h3>📈 Activity Analysis</h3>
<p>Study distribution over the last 7 days</p>
<div class="bar-chart-container" style="height:180px; width:100%;">
{html_bars}
</div>
</div>
""", unsafe_allow_html=True)

    # Subject breakdown table
    try:
        conn = database.get_db_connection()
        rows = conn.execute(
            "SELECT subject, sum(duration_minutes) as mins, count(*) as sessions "
            "FROM study_logs WHERE username = ? GROUP BY subject ORDER BY mins DESC",
            (username,)
        ).fetchall()
        conn.close()

        if rows:
            st.markdown("""
<div class="ui-card">
<h3>📚 Subject Breakdown</h3>
<p>Detailed time distribution per subject</p>
""", unsafe_allow_html=True)

            max_mins = rows[0]['mins'] if rows else 1
            for r in rows:
                sub = r['subject'] or "General"
                m = r['mins']
                sessions = r['sessions']
                prog = min(int((m / max_mins) * 100), 100)
                hours_str = f"{round(m/60, 1)}h" if m >= 60 else f"{m}m"

                st.markdown(f"""
<div style="margin-bottom:1.1rem;">
<div style="display:flex; justify-content:space-between; align-items:center; font-size:0.9rem; margin-bottom:0.3rem;">
<span style="font-weight:600; color:#1e293b;">{sub}</span>
<span style="color:#64748b;">{hours_str} · {sessions} session{'s' if sessions != 1 else ''}</span>
</div>
<div class="progress-track"><div class="progress-fill-blue" style="width:{prog}%;"></div></div>
</div>
""", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading subject data: {e}")


with col_side:
    # Insights & Tips
    st.markdown("""
<div class="ui-card">
<h3>💡 Insights & Tips</h3>
<p>Based on your activity</p>
""", unsafe_allow_html=True)

    insights_shown = 0

    if stats['streak'] > 2:
        st.markdown("""
<div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:12px; padding:0.8rem; display:flex; gap:0.6rem; margin-bottom:0.75rem; align-items:flex-start;">
<div>🔥</div>
<div><div style="font-weight:600; font-size:0.88rem;">Great Consistency!</div><div style="font-size:0.8rem; color:#64748b;">You're building a strong study habit.</div></div>
</div>
""", unsafe_allow_html=True)
        insights_shown += 1

    if stats['hours_week'] >= 5:
        st.markdown("""
<div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:12px; padding:0.8rem; display:flex; gap:0.6rem; margin-bottom:0.75rem; align-items:flex-start;">
<div>🚀</div>
<div><div style="font-weight:600; font-size:0.88rem;">Productive Week!</div><div style="font-size:0.8rem; color:#64748b;">You've hit 5+ hours this week. Keep it up!</div></div>
</div>
""", unsafe_allow_html=True)
        insights_shown += 1

    if stats['topics_mastered'] >= 3:
        st.markdown("""
<div style="background:#faf5ff; border:1px solid #e9d5ff; border-radius:12px; padding:0.8rem; display:flex; gap:0.6rem; margin-bottom:0.75rem; align-items:flex-start;">
<div>🎓</div>
<div><div style="font-weight:600; font-size:0.88rem;">Diverse Learner!</div><div style="font-size:0.8rem; color:#64748b;">Studying multiple subjects improves retention.</div></div>
</div>
""", unsafe_allow_html=True)
        insights_shown += 1

    if stats['daily_goal_pct'] >= 100:
        st.markdown("""
<div style="background:#fefce8; border:1px solid #fde047; border-radius:12px; padding:0.8rem; display:flex; gap:0.6rem; margin-bottom:0.75rem; align-items:flex-start;">
<div>⭐</div>
<div><div style="font-weight:600; font-size:0.88rem;">Goal Achieved!</div><div style="font-size:0.8rem; color:#64748b;">You hit your daily 60-min goal today!</div></div>
</div>
""", unsafe_allow_html=True)
        insights_shown += 1

    if insights_shown == 0:
        if stats['total_hours'] < 1:
            st.markdown("""
<div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:12px; padding:0.8rem; display:flex; gap:0.6rem; margin-bottom:0.75rem; align-items:flex-start;">
<div>💡</div>
<div><div style="font-weight:600; font-size:0.88rem;">Just Getting Started</div><div style="font-size:0.8rem; color:#64748b;">Try a 25-minute session today to kick off your streak!</div></div>
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown("""
<div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:0.8rem; font-size:0.85rem; color:#64748b; margin-bottom:0.75rem;">
Log more sessions to unlock personalized insights!
</div>
""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Progress toward weekly goal
    weekly_goal_hrs = 10
    weekly_pct = min(int((stats['hours_week'] / weekly_goal_hrs) * 100), 100)
    st.markdown(f"""
<div class="ui-card">
<h3>🎯 Weekly Goal</h3>
<p>Target: {weekly_goal_hrs}h per week</p>
<div style="font-size:1.5rem; font-weight:700; color:#2563eb; margin-bottom:0.5rem;">{stats['hours_week']}h <span style="font-size:0.9rem; color:#64748b;">/ {weekly_goal_hrs}h</span></div>
<div class="progress-track"><div class="progress-fill-blue" style="width:{weekly_pct}%;"></div></div>
<div style="font-size:0.8rem; color:#64748b; margin-top:0.4rem;">{weekly_pct}% complete</div>
</div>
""", unsafe_allow_html=True)
