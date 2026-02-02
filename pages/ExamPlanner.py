import streamlit as st
import datetime
import database
import pandas as pd
from components.navbar import render_navbar

# --- Setup ---
st.set_page_config(page_title="Study Planner", page_icon="📅", layout="wide")

# Ensure user is logged in
if "username" not in st.session_state or not st.session_state.username:
    st.warning("Please log in to view your planner.")
    st.stop()
    
username = st.session_state.username

BACKGROUND_COLORS = {
    "high": "linear-gradient(to bottom, #ef4444, #f43f5e)",
    "medium": "linear-gradient(to bottom, #3b82f6, #06b6d4)",
    "low": "linear-gradient(to bottom, #22c55e, #10b981)",
}

def load_css():
    with open("static/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def complete_task(task_id):
    database.update_task_status(task_id, True)

def delete_task_action(task_id):
    database.delete_task(task_id)

def add_new_task():
    # Fetch values from session state
    subject = st.session_state.get("task_subject_input", "")
    date_val = st.session_state.get("task_date_input", datetime.date.today())
    time_val = st.session_state.get("task_time_input", "09:00 AM")
    priority = st.session_state.get("task_priority_input", "Low")
    
    if not subject:
        st.error("Subject / Topic is required!")
        return

    try:
        # subject acts as both title and subject for simplification
        if database.add_task(username, subject, subject, date_val, time_val, priority):
            st.toast(f"✅ Saved: {subject}", icon="🚀")
            # We don't manually clear keys that are bound to widgets to avoid the 
            # "cannot be modified after instantiation" error. 
            # Instead, we just rerun to refresh the list, or we could use a form.
            # But the user wants it simple, so just rerun.
            st.rerun() 
        else:
            st.error("Failed to add task. Check log.")
    except Exception as e:
        st.error(f"Error: {e}")

def main():
    database.init_all_tables() # Trigger migration
    load_css()
    render_navbar(active_page="Planner")
    
    # --- Header ---
    c_head, c_btn = st.columns([0.8, 0.2])
    with c_head:
        st.markdown("""
<div style="margin-bottom:0.5rem;">
<h2 style="margin:0; font-size:1.8rem; font-weight:700;">Study Planner</h2>
<p style="color:#64748b; margin:0;">Organize and schedule your study sessions</p>
</div>
""", unsafe_allow_html=True)
    with c_btn:
        st.write("") # Spacer
        # This button is just visual here, the form is below
        # st.markdown('<div style="text-align:right;"><button style="background:linear-gradient(to right, #2563eb, #4f46e5); color:white; border:none; padding:8px 16px; border-radius:8px; font-weight:600;">+ Add Task</button></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Fetch Data ---
    tasks = database.get_tasks(username)
    # Tasks are Row objects.
    # We can convert to dicts or access by key
    
    # Filter
    completed_tasks = [t for t in tasks if t['completed']]
    upcoming_tasks = [t for t in tasks if not t['completed']]
    weekly_count = database.get_tasks_this_week(username)

    # --- Stats Row ---
    s1, s2, s3, s4 = st.columns(4)
    
    def stat_box(label, value, icon, bg_color, icon_color):
        st.markdown(f"""
<div class="ui-card" style="padding:1.2rem; display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
<div>
<div style="font-size:0.85rem; color:#64748b; margin-bottom:0.2rem;">{label}</div>
<div style="font-size:1.5rem; font-weight:700;">{value}</div>
</div>
<div style="background:{bg_color}; width:40px; height:40px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:{icon_color}; font-size:1.2rem;">
{icon}
</div>
</div>
""", unsafe_allow_html=True)

    with s1: stat_box("Total Tasks", len(tasks), "📖", "#eff6ff", "#2563eb")
    with s2: stat_box("Completed", len(completed_tasks), "✅", "#f0fdf4", "#16a34a")
    with s3: stat_box("Upcoming", len(upcoming_tasks), "🕒", "#fff7ed", "#ea580c")
    with s4: stat_box("This Week", str(weekly_count), "📅", "#faf5ff", "#9333ea")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Main Content ---
    c_list, c_sidebar = st.columns([2, 1])

    with c_list:
        # Upcoming Tasks
        st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
<div>
<h3 style="margin:0; font-size:1.1rem; font-weight:600;">Upcoming Tasks</h3>
<p style="margin:0; color:#64748b; font-size:0.9rem;">Your scheduled study sessions</p>
</div>
</div>
""", unsafe_allow_html=True)

        if not upcoming_tasks:
             st.info("No upcoming tasks! Add one to get started.")

        for t in upcoming_tasks:
            priority = t['priority'].lower() if t['priority'] else 'medium'
            prio_badge = f"<span class='badge-{priority}'>{priority}</span>"
            date_str = pd.to_datetime(t['due_date']).strftime("%b %d") if t['due_date'] else "No Date"
            
            with st.container():
                # Render the card HTML
                color_grad = BACKGROUND_COLORS.get(priority, BACKGROUND_COLORS['medium'])
                
                st.markdown(f"""
<div class="task-card" style="margin-bottom:0.5rem;">
<div class="task-color-strip" style="background:{color_grad};"></div>
<div style="display:flex; justify-content:space-between; align-items:start;">
<div style="display:flex; gap:1rem; align-items:start;">
<div style="background:white; border:2px solid #cbd5e1; width:20px; height:20px; border-radius:50%; margin-top:2px;"></div>
<div>
<div style="font-weight:600; font-size:1rem; color:#1e293b; margin-bottom:0.25rem;">{t['title']}</div>
<div style="font-size:0.85rem; color:#64748b; display:flex; gap:1rem; align-items:center;">
<span>📖 {t['subject'] or 'General'}</span>
<span>📅 {date_str}</span>
<span>⏰ {t['time_str'] or ''}</span>
{prio_badge}
</div>
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)
                
                c_done, c_del, c_spacer = st.columns([0.2, 0.2, 0.6])
                with c_done:
                    st.button("✅ Done", key=f"comp_{t['id']}", use_container_width=True,
                              on_click=complete_task, args=(t['id'],))
                with c_del:
                    st.button("🗑️", key=f"del_{t['id']}", help="Delete task", use_container_width=True,
                              on_click=delete_task_action, args=(t['id'],))

        # Completed Logic
        if completed_tasks:
            st.markdown("<br><h3>Completed Tasks</h3>", unsafe_allow_html=True)
            for t in completed_tasks:
                date_str = pd.to_datetime(t['due_date']).strftime("%b %d") if t['due_date'] else ""
                st.markdown(f"""
<div class="task-item completed">
<div style="color:#16a34a; font-size:1.2rem;">✓</div>
<div>
<div style="text-decoration:line-through; color:#64748b; font-weight:500;">{t['title']}</div>
<div style="font-size:0.8rem; color:#64748b;">{t['subject']} • {date_str}</div>
</div>
</div>
""", unsafe_allow_html=True)

    with c_sidebar:
        # Calendar Widget
        today = datetime.date.today()
        st.markdown(f"""
<div class="calendar-widget">
<h3 style="margin:0; text-align:left;">Calendar</h3>
<hr style="margin:1rem 0; border-top:1px solid #e2e8f0;">
<div class="cal-month">{today.strftime("%B %Y")}</div>
<div class="cal-day-big">{today.day}</div>
<div class="cal-weekday">{today.strftime("%A")}</div>
<div style="display:flex; justify-content:space-between; font-size:0.9rem; margin-top:1rem;">
<span style="color:#64748b;">Today's Tasks</span>
<span style="background:#eff6ff; color:#2563eb; padding:2px 8px; border-radius:99px; font-size:0.75rem; border:1px solid #bfdbfe;">{len(upcoming_tasks)} tasks</span>
</div>
</div>
""", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        # Quick Add Task Form
        with st.container(border=True):
            st.markdown("### Quick Add Task")
            st.text_input("Subject / Topic", key="task_subject_input", placeholder="e.g. DSA, ML, Physics Review")
            
            c1, c2 = st.columns(2)
            with c1:
                st.date_input("Date", key="task_date_input")
            with c2:
                # Use simple text input for time as requested
                st.text_input("Time", key="task_time_input", value="09:00 AM", placeholder="e.g. 10:30 PM")
            
            st.selectbox("Priority", ["Low", "Medium", "High"], key="task_priority_input")
            
            if st.button("Add Task", type="primary", use_container_width=True):
                add_new_task()

        # Study Tip
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
<div style="background:#fffbeb; border:1px solid #fde68a; border-radius:12px; padding:1rem; display:flex; gap:0.75rem;">
<div style="font-size:1.2rem;">📅</div>
<div style="font-size:0.9rem; color:#92400e;">
<strong>Planning Tip:</strong> Break larger tasks into smaller chunks for better focus.
</div>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
