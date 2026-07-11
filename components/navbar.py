import streamlit as st


def render_navbar(active_page="Home"):
    """
    Renders a clean horizontal navigation bar using an HTML-based layout
    for the logo + username, and Streamlit buttons for navigation.
    """
    current_user = st.session_state.get("username", "User")

    # Inject navbar-specific CSS overrides
    st.markdown("""
<style>
/* Tighter button padding inside the navbar so text never wraps */
div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"]:first-child .stButton > button {
    padding: 0.4rem 0.6rem !important;
    font-size: 0.82rem !important;
    white-space: nowrap !important;
    min-height: 0 !important;
}
</style>
""", unsafe_allow_html=True)

    with st.container():
        # Layout: Logo (narrow) | Nav links (wide) | User + Logout (narrow)
        c_logo, c_nav, c_user, c_logout = st.columns([1.2, 6, 1.2, 0.8])

        with c_logo:
            st.markdown(
                '<div style="font-weight:700; font-size:1.1rem; color:#1e293b; '
                'display:flex; align-items:center; height:100%; white-space:nowrap;">'
                '<span style="background:linear-gradient(135deg,#2563eb,#4f46e5); color:white; '
                'padding:5px 9px; border-radius:10px; font-size:0.95rem; margin-right:8px;">🧠</span>'
                'StudyBuddy</div>',
                unsafe_allow_html=True,
            )

        with c_nav:
            nav_items = [
                ("Home",       "🏠", "app.py"),
                ("Summarizer", "📄", "pages/Summarizer.py"),
                ("Planner",    "📅", "pages/ExamPlanner.py"),
                ("Tracker",    "🎯", "pages/StudyTracker.py"),
                ("Report",     "📊", "pages/Report.py"),
            ]
            nav_cols = st.columns(len(nav_items))
            for i, (label, icon, path) in enumerate(nav_items):
                is_active = active_page == label
                btn_type = "primary" if is_active else "secondary"
                with nav_cols[i]:
                    if st.button(
                        f"{icon} {label}",
                        key=f"nav_{label}",
                        type=btn_type,
                        use_container_width=True,
                    ):
                        if not is_active:
                            st.switch_page(path)

        with c_user:
            st.markdown(
                f'<div style="text-align:right; color:#166534; font-size:0.82rem; '
                f'font-weight:600; padding-top:9px; white-space:nowrap;">'
                f'<span style="display:inline-block; width:7px; height:7px; '
                f'background:#22c55e; border-radius:50%; margin-right:5px; '
                f'vertical-align:middle;"></span>{current_user}</div>',
                unsafe_allow_html=True,
            )

        with c_logout:
            if st.button("↩ Exit", key="nav_logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.rerun()
