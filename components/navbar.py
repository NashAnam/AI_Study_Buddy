import streamlit as st
import textwrap

def render_navbar(active_page="Home"):
    """
    Renders the custom top navigation bar matching the Figma screenshot.
    Uses native Streamlit buttons with 'primary' type for the active page
    and 'secondary' type for inactive pages to allow for specific styling.
    """
    # Custom container styling for the navbar
    st.markdown(textwrap.dedent("""
        <style>
            .nav-container {
                background: white;
                padding: 0.5rem 1rem;
                border-radius: 12px;
                border: 1px solid #f1f5f9;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
                margin-bottom: 0.5rem;
                display: flex;
                align-items: center;
                gap: 0.3rem;
            }
            /* Target the specific container for navbar if possible, or assume it's the first block */
        </style>
    """), unsafe_allow_html=True)
    
    # We use a container to apply spacing
    with st.container():
        # Layout: Logo area (left), Nav Links (center), Profile (right)
        # Using columns to distribute space
        c_logo, c_nav, c_profile = st.columns([1.5, 5, 2])
        
        with c_logo:
             st.markdown('<div style="font-weight:700; font-size:1.2rem; color:#1e293b; display:flex; align-items:center; height:100%;"><span style="background:#2563eb; color:white; padding:4px 8px; border-radius:8px; font-size:1rem; margin-right:8px;">🧠</span> StudyBuddy</div>', unsafe_allow_html=True)
        
        with c_nav:
            # Nav items
            nav_items = [
                ("Home", "🏠", "app.py"),
                ("Summarizer", "📄", "pages/Summarizer.py"),
                ("Planner", "📅", "pages/ExamPlanner.py"),
                ("Tracker", "🎯", "pages/StudyTracker.py"),
                ("Report", "📊", "pages/Report.py"),
            ]
            
            # Create a simplified row of columns for just the nav items
            nav_cols = st.columns(len(nav_items))
            for i, (label, icon, path) in enumerate(nav_items):
                is_active = (active_page == label)
                btn_type = "primary" if is_active else "secondary"
                
                with nav_cols[i]:
                    if st.button(f"{icon} {label}", key=f"nav_{label}", type=btn_type, use_container_width=True):
                        if not is_active:
                            st.switch_page(path)

        with c_profile:
             c_status, c_logout = st.columns([1.5, 1])
             with c_status:
                st.markdown('<div style="text-align:right; color:#166534; font-size:0.85rem; font-weight:600; padding-top:6px;">● Nashrah</div>', unsafe_allow_html=True)
             with c_logout:
                if st.button("Logout", key="nav_logout", use_container_width=True):
                    st.session_state.logged_in = False
                    st.session_state.username = None
                    st.rerun()

