import streamlit as st
import hashlib
import json
import os

USERS_FILE = "data/users.json"

import streamlit as st

def is_logged_in():
    return st.session_state.get("logged_in", False)

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = {"password": hash_password(password)}
    save_users(users)
    return True

def login_user(username, password):
    users = load_users()
    hashed = hash_password(password)
    if username in users and users[username]["password"] == hashed:
        return True
    return False

def auth_page():
    st.title("🔐 Login or Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")
        user = st.text_input("Username", key="login_user")
        passwd = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if login_user(user, passwd):
                st.success("Login successful")
                st.session_state["user"] = user
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")

    with tab2:
        st.subheader("Register")
        new_user = st.text_input("New Username", key="reg_user")
        new_pass = st.text_input("New Password", type="password", key="reg_pass")
        if st.button("Register"):
            if register_user(new_user, new_pass):
                st.success("Registration successful! Please login.")
            else:
                st.warning("Username already exists.")
