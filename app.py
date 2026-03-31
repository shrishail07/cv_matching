import streamlit as st
from admin_dashboard import admin_dashboard
from hireing_dashboard import hiring_dashboard

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="PragyanAI Hiring Platform",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------
# SESSION STATE INIT
# -------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_type" not in st.session_state:
    st.session_state.user_type = None

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# -------------------------
# PASSWORDS
# Admin password:  admin@123
# Manager password: manager@123
# -------------------------
ADMIN_PASSWORD   = "admin@123"
MANAGER_PASSWORD = "manager@123"

# Admin dashboard state
if "admin_jd_list" not in st.session_state:
    st.session_state.admin_jd_list = []

if "resumes_to_analyze" not in st.session_state:
    st.session_state.resumes_to_analyze = []

if "admin_match_results" not in st.session_state:
    st.session_state.admin_match_results = []

if "resume_statuses" not in st.session_state:
    st.session_state.resume_statuses = {}

if "vendors" not in st.session_state:
    st.session_state.vendors = []

if "vendor_statuses" not in st.session_state:
    st.session_state.vendor_statuses = {}

# -------------------------
# PAGE NAVIGATION HELPER
# -------------------------
def go_to(page_name):
    st.session_state.page = page_name

# -------------------------
# LOGIN PAGE
# -------------------------
def login_page():
    st.title("🧠 PragyanAI Hiring Platform")
    st.subheader("Please log in to continue")
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name = st.text_input("Your Name", placeholder="Enter your name", key="login_name")

        role = st.selectbox(
            "Login as",
            ["Select Role", "Admin", "Hiring Manager"],
            key="login_role_select"
        )

        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", use_container_width=True):
            if not name.strip():
                st.error("Please enter your name.")
            elif role == "Select Role":
                st.error("Please select a role.")
            elif not password:
                st.error("Please enter your password.")
            elif role == "Admin" and password == ADMIN_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.user_type = "admin"
                st.session_state.user_name = name.strip()
                go_to("admin_dashboard")
                st.rerun()
            elif role == "Hiring Manager" and password == MANAGER_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.user_type = "hiring_manager"
                st.session_state.user_name = name.strip()
                go_to("hiring_dashboard")
                st.rerun()
            else:
                st.error("Incorrect password for the selected role.")

# -------------------------
# ROUTER
# -------------------------
current_page = st.session_state.page

if current_page == "login" or not st.session_state.logged_in:
    login_page()

elif current_page == "admin_dashboard":
    if st.session_state.user_type == "admin":
        admin_dashboard(go_to)
    else:
        st.error("Access denied. Admins only.")
        go_to("login")
        st.rerun()

elif current_page == "hiring_dashboard":
    if st.session_state.user_type == "hiring_manager":
        hiring_dashboard(go_to)
    else:
        st.error("Access denied.")
        go_to("login")
        st.rerun()

else:
    st.warning("Unknown page. Redirecting to login.")
    go_to("login")
    st.rerun()
