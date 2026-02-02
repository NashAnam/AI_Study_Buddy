import streamlit as st
import database
from components.navbar import render_navbar
from datetime import datetime

# --- Setup ---
st.set_page_config(page_title="Study Report", page_icon="📊", layout="wide")

if "username" not in st.session_state or not st.session_state.username:
    st.warning("Please log in.")
    st.stop()
    
username = st.session_state.username

def load_css():
    with open("static/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    load_css()
    render_navbar(active_page="Report")
    
    # --- Fetch Data ---
    stats = database.get_user_stats(username)
    weekly = database.get_weekly_activity(username)
    
    # --- Header ---
    c_head, c_btn = st.columns([0.8, 0.2])
    with c_head:
        st.markdown("""
<div style="margin-bottom:0.5rem;">
<h2 style="margin:0; font-size:1.8rem; font-weight:700;">Study Report</h2>
<p style="color:#64748b; margin:0;">Comprehensive analysis of your learning progress</p>
</div>
""", unsafe_allow_html=True)
    with c_btn:
        st.write("") 
        
        # Simple CSV export logic
        report_data = f"Study Report for {username}\n"
        report_data += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report_data += f"Streak: {stats['streak']} days\n"
        report_data += f"Total Hours: {stats['total_hours']}h\n"
        report_data += f"Topics Mastered: {stats['topics_mastered']}\n"
        report_data += f"Daily Goal Completion: {stats['daily_goal_pct']}%\n"
        
        st.download_button(
            label="📥 Download Report",
            data=report_data,
            file_name=f"study_report_{username}.txt",
            mime="text/plain",
            use_container_width=True
        )


    # --- Stats Row ---
    s1, s2, s3, s4 = st.columns(4)
    
    def stat_card(title, value, badge_text, badge_color, icon, bg_gradient):
        st.markdown(f"""
<div class="ui-card" style="background:{bg_gradient}; border:1px solid rgba(0,0,0,0.05);">
<div style="display:flex; justify-content:space-between; margin-bottom:1rem;">
<div style="background:white; width:48px; height:48px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:1.4rem; box-shadow:0 1px 2px rgba(0,0,0,0.05);">
{icon}
</div>
<div style="background:white; border:1px solid {badge_color}; color:#1e293b; padding:2px 8px; border-radius:99px; font-size:0.75rem; font-weight:600; height:fit-content; display:flex; align-items:center;">
{badge_text}
</div>
</div>
<div style="font-size:0.9rem; color:#64748b; margin-bottom:0.2rem;">{title}</div>
<div style="font-size:2rem; font-weight:700; color:#1e293b;">{value}</div>
</div>
""", unsafe_allow_html=True)

    with s1: 
        stat_card("Daily Goal", f"{stats['daily_goal_pct']}%", "Today", "#bfdbfe", "🎯", "linear-gradient(to bottom right, #eff6ff, #ecfeff)")
    with s2: 
        stat_card("Total Hours", f"{stats['total_hours']}h", "All Time", "#bbf7d0", "🕒", "linear-gradient(to bottom right, #f0fdf4, #ecfdf5)")
    with s3: 
        stat_card("Topics", str(stats['topics_mastered']), "Active", "#e9d5ff", "📖", "linear-gradient(to bottom right, #faf5ff, #fdf4ff)")
    with s4: 
        stat_card("Streak", str(stats['streak']), "Days", "#fed7aa", "🏆", "linear-gradient(to bottom right, #fff7ed, #fef2f2)")

    # --- Main Content Grid ---
    col_main, col_side = st.columns([2.2, 1])

    with col_main:
        with st.container():
            # Chart rendering logic
            max_h = max([d['hours'] for d in weekly]) if weekly else 1
            if max_h == 0: max_h = 1
            
            html_bars = ""
            for m in weekly:
                h_pct = (m['hours'] / max_h) * 100
                html_bars += f"""
<div class="bar-column">
<div class="bar-visual" style="height:{h_pct}%; background:linear-gradient(to top, #2563eb, #6366f1);"></div>
<div class="bar-label">{m['day']}</div>
</div>
"""
            
            st.markdown(f"""
<div class="ui-card">
<h3>Activity Analysis</h3>
<p>Study distribution over the last 7 days</p>
<div class="bar-chart-container" style="height:150px; width:100%;">
{html_bars}
</div>
</div>
""", unsafe_allow_html=True)

    with col_side:
        # Insights
        st.markdown("""
<div class="ui-card">
<h3>Insights & Tips</h3>
<p>Based on your activity</p>
""", unsafe_allow_html=True)
        
        if stats['streak'] > 2:
            st.markdown("""
<div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:12px; padding:0.8rem; display:flex; gap:0.75rem; margin-bottom:0.75rem;">
<div style="font-size:0.9rem;">🔥</div>
<div><div style="font-weight:600; font-size:0.9rem;">Great Consistency</div><div style="font-size:0.8rem;">You're building a strong habit!</div></div>
</div>
""", unsafe_allow_html=True)
        elif stats['total_hours'] < 1:
             st.markdown("""
<div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:12px; padding:0.8rem; display:flex; gap:0.75rem; margin-bottom:0.75rem;">
<div style="font-size:0.9rem;">💡</div>
<div><div style="font-weight:600; font-size:0.9rem;">Getting Started</div><div style="font-size:0.8rem;">Try a 25-minute study session today.</div></div>
</div>
""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
