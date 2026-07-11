import streamlit as st
import datetime
import database
import utils
import pandas as pd
from components.navbar import render_navbar

# --- Page Setup ---
st.set_page_config(page_title="Study Planner", page_icon="📅", layout="wide", initial_sidebar_state="collapsed")

# Auth guard
if "username" not in st.session_state or not st.session_state.username:
    st.warning("🔒 Please log in to view your planner.")
    if st.button("Go to Login"):
        st.switch_page("app.py")
    st.stop()

username = st.session_state.username

# Priority color strip gradients
PRIORITY_COLORS = {
    "high":   "linear-gradient(to bottom, #ef4444, #f43f5e)",
    "medium": "linear-gradient(to bottom, #3b82f6, #06b6d4)",
    "low":    "linear-gradient(to bottom, #22c55e, #10b981)",
}

# Session state for error/success messages from the form
if "task_msg" not in st.session_state:
    st.session_state.task_msg = None
if "task_msg_type" not in st.session_state:
    st.session_state.task_msg_type = "success"


def complete_task(task_id):
    database.update_task_status(task_id, True)


def delete_task_action(task_id):
    database.delete_task(task_id)


# --- Load CSS & Navbar ---
database.init_all_tables()
utils.load_css()
render_navbar(active_page="Planner")

# --- Page Header ---
st.markdown("""
<div style="margin-bottom:0.5rem;">
<h2 style="margin:0; font-size:1.8rem; font-weight:700; color:#1e293b;">📅 Study Planner</h2>
<p style="color:#64748b; margin:0.25rem 0 0 0;">Organize and schedule your study sessions</p>
</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Fetch Data ---
tasks = database.get_tasks(username)
completed_tasks = [t for t in tasks if t['completed']]
upcoming_tasks  = [t for t in tasks if not t['completed']]
weekly_count    = database.get_tasks_this_week(username)

# --- Stats Row ---
s1, s2, s3, s4 = st.columns(4)

def stat_box(col, label, value, icon, bg_color, icon_color):
    with col:
        st.markdown(f"""
<div class="ui-card" style="display:flex; justify-content:space-between; align-items:center;">
<div>
<div style="font-size:0.85rem; color:#64748b; margin-bottom:0.3rem;">{label}</div>
<div style="font-size:1.6rem; font-weight:700; color:#1e293b;">{value}</div>
</div>
<div style="background:{bg_color}; width:42px; height:42px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1.2rem;">
{icon}
</div>
</div>
""", unsafe_allow_html=True)

stat_box(s1, "Total Tasks",  len(tasks),           "📖", "#eff6ff", "#2563eb")
stat_box(s2, "Completed",    len(completed_tasks),  "✅", "#f0fdf4", "#16a34a")
stat_box(s3, "Upcoming",     len(upcoming_tasks),   "🕒", "#fff7ed", "#ea580c")
stat_box(s4, "This Week",    weekly_count,          "📅", "#faf5ff", "#9333ea")

st.markdown("<br>", unsafe_allow_html=True)

# --- Main Content ---
c_list, c_sidebar = st.columns([2, 1])

with c_list:
    # Upcoming Tasks
    st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
<div>
<h3 style="margin:0; font-size:1.15rem; font-weight:600;">📌 Upcoming Tasks</h3>
<p style="margin:0; color:#64748b; font-size:0.88rem;">Your scheduled study sessions</p>
</div>
</div>
""", unsafe_allow_html=True)

    if not upcoming_tasks:
        st.info("🎉 No upcoming tasks! Add one in the panel on the right.")
    else:
        for t in upcoming_tasks:
            priority = (t['priority'] or 'medium').lower()
            prio_badge = f"<span class='badge-{priority}'>{priority}</span>"
            try:
                date_str = pd.to_datetime(str(t['due_date'])).strftime("%b %d, %Y")
            except Exception:
                date_str = str(t['due_date']) if t['due_date'] else "No Date"

            color_grad = PRIORITY_COLORS.get(priority, PRIORITY_COLORS['medium'])

            st.markdown(f"""
<div class="task-card">
<div class="task-color-strip" style="background:{color_grad};"></div>
<div style="display:flex; justify-content:space-between; align-items:flex-start;">
<div style="display:flex; gap:1rem; align-items:flex-start;">
<div style="background:white; border:2px solid #cbd5e1; width:20px; height:20px; border-radius:50%; margin-top:3px; flex-shrink:0;"></div>
<div>
<div style="font-weight:600; font-size:1rem; color:#1e293b; margin-bottom:0.3rem;">{t['title']}</div>
<div style="font-size:0.85rem; color:#64748b; display:flex; gap:0.75rem; align-items:center; flex-wrap:wrap;">
<span>📖 {t['subject'] or 'General'}</span>
<span>📅 {date_str}</span>
{'<span>⏰ ' + (t['time_str'] or '') + '</span>' if t['time_str'] else ''}
{prio_badge}
</div>
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

            c_done, c_del, c_spacer = st.columns([0.2, 0.15, 0.65])
            with c_done:
                st.button("✅ Done", key=f"comp_{t['id']}", use_container_width=True,
                          on_click=complete_task, args=(t['id'],))
            with c_del:
                st.button("🗑️", key=f"del_{t['id']}", help="Delete task", use_container_width=True,
                          on_click=delete_task_action, args=(t['id'],))

    # Completed Tasks
    if completed_tasks:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander(f"✅ Completed Tasks ({len(completed_tasks)})", expanded=False):
            for t in completed_tasks:
                try:
                    date_str = pd.to_datetime(str(t['due_date'])).strftime("%b %d")
                except Exception:
                    date_str = ""

                subject = t['subject'] or 'General'
                st.markdown(f"""
<div class="task-item completed" style="margin-bottom:0.5rem;">
<div style="color:#16a34a; font-size:1.2rem;">✓</div>
<div>
<div style="text-decoration:line-through; color:#94a3b8; font-weight:500;">{t['title']}</div>
<div style="font-size:0.8rem; color:#94a3b8;">{subject} • {date_str}</div>
</div>
</div>
""", unsafe_allow_html=True)

                c_del2, c_sp = st.columns([0.15, 0.85])
                with c_del2:
                    st.button("🗑️", key=f"cdel_{t['id']}", help="Delete",
                              use_container_width=True,
                              on_click=delete_task_action, args=(t['id'],))


with c_sidebar:
    # Calendar Widget
    today = datetime.date.today()
    st.markdown(f"""
<div class="calendar-widget">
<div class="cal-month">{today.strftime("%B %Y")}</div>
<div class="cal-day-big">{today.day}</div>
<div class="cal-weekday">{today.strftime("%A")}</div>
<hr style="border:none; border-top:1px solid #e2e8f0; margin:0.75rem 0;">
<div style="display:flex; justify-content:space-between; font-size:0.88rem;">
<span style="color:#64748b;">Upcoming</span>
<span style="background:#eff6ff; color:#2563eb; padding:2px 10px; border-radius:99px; font-size:0.75rem; font-weight:600; border:1px solid #bfdbfe;">{len(upcoming_tasks)} tasks</span>
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Add Task Form
    with st.container(border=True):
        st.markdown("### ➕ Add Task")

        # Show any pending messages from the form submission
        if st.session_state.task_msg:
            if st.session_state.task_msg_type == "success":
                st.success(st.session_state.task_msg)
            else:
                st.error(st.session_state.task_msg)
            st.session_state.task_msg = None

        with st.form("add_task_form", clear_on_submit=True):
            task_title = st.text_input("Task Title", placeholder="e.g. Revise Chapter 3")
            task_subject = st.text_input("Subject", placeholder="e.g. DSA, ML, Physics")
            c1, c2 = st.columns(2)
            with c1:
                task_date = st.date_input("Due Date", value=datetime.date.today())
            with c2:
                task_time = st.text_input("Time", value="09:00 AM", placeholder="e.g. 10:30 AM")
            task_priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=1)

            submitted = st.form_submit_button("Add Task", type="primary", use_container_width=True)

        if submitted:
            # Validation and DB write happen AFTER the form (outside the form block)
            # to avoid the "cannot modify widget" error
            if not task_title:
                st.session_state.task_msg = "Task title is required!"
                st.session_state.task_msg_type = "error"
                st.rerun()
            else:
                success = database.add_task(
                    username, task_title,
                    task_subject or "General",
                    task_date, task_time, task_priority
                )
                if success:
                    st.session_state.task_msg = f"✅ Task '{task_title}' added!"
                    st.session_state.task_msg_type = "success"
                    st.rerun()
                else:
                    st.session_state.task_msg = "Failed to add task. Please try again."
                    st.session_state.task_msg_type = "error"
                    st.rerun()

    # Study Tip
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
<div style="background:#fffbeb; border:1px solid #fde68a; border-radius:12px; padding:1rem; display:flex; gap:0.75rem; align-items:flex-start;">
<div style="font-size:1.3rem;">💡</div>
<div style="font-size:0.88rem; color:#92400e;">
<strong>Planning Tip:</strong> Break larger tasks into smaller 25-minute Pomodoro chunks for better focus and retention.
</div>
</div>
""", unsafe_allow_html=True)
