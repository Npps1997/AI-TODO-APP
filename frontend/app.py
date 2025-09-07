import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="AI-Powered To-Do", page_icon="✅", layout="centered")

if "token" not in st.session_state:
    st.session_state.token = None

def login(username, password):
    response = requests.post(f"{BACKEND_URL}/token", data={"username": username, "password": password})
    if response.status_code == 200:
        st.session_state.token = response.json()["access_token"]
        st.success("Logged in successfully")
    else:
        st.error("Login failed: check credentials")

def register(username, password):
    response = requests.post(f"{BACKEND_URL}/register", json={"username": username, "password": password})
    if response.status_code == 200:
        st.success("Registration successful! Please log in.")
    else:
        st.error(f"Registration failed: {response.text}")

if not st.session_state.token:
    st.title("Login or Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            login(username, password)
    with col2:
        if st.button("Register"):
            register(username, password)
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.token}"}

st.title("✅ AI-Powered To-Do Manager (Streamlit + FastAPI + SQLite + Gemini)")

# Helpers using headers

def fetch_tasks():
    r = requests.get(f"{BACKEND_URL}/tasks", headers=headers)
    r.raise_for_status()
    return r.json()

def add_task(description: str):
    r = requests.post(f"{BACKEND_URL}/tasks", json={"description": description}, headers=headers)
    r.raise_for_status()
    return r.json()

def update_task(task_id: int, description=None, status=None):
    payload = {}
    if description is not None and description.strip():
        payload["description"] = description
    if status is not None:
        payload["status"] = status
    r = requests.put(f"{BACKEND_URL}/tasks/{task_id}", json=payload, headers=headers)
    r.raise_for_status()
    return r.json()

def delete_task(task_id: int):
    r = requests.delete(f"{BACKEND_URL}/tasks/{task_id}", headers=headers)
    r.raise_for_status()
    return r.json()

def ai_generate(topic: str):
    r = requests.post(f"{BACKEND_URL}/ai/generate-tasks", json={"topic": topic}, headers=headers)
    r.raise_for_status()
    return r.json()["suggestions"]

def ai_summarize(text: str):
    r = requests.post(f"{BACKEND_URL}/ai/summarize-feedback", json={"text": text}, headers=headers)
    r.raise_for_status()
    return r.json()["summary"]

# Tabs UI

tab1, tab2, tab3 = st.tabs(["Tasks", "AI Suggestions", "Summarize Feedback"])

with tab1:
    st.subheader("Tasks (CRUD)")
    with st.form("add_form", clear_on_submit=True):
        desc = st.text_input("New task description", placeholder="e.g., Clean data and create EDA notebook")
        submitted = st.form_submit_button("Add Task")
        if submitted and desc.strip():
            add_task(desc.strip())
            st.success("Task added")

    st.markdown("---")

    tasks = fetch_tasks()
    if tasks:
        df = pd.DataFrame(tasks)
        st.dataframe(df, hide_index=True, use_container_width=True)

        st.markdown("### Update a Task")
        col1, col2 = st.columns(2)
        with col1:
            uid = st.number_input("Task ID", min_value=1, step=1)
        with col2:
            new_status = st.selectbox("Status", ["pending", "in-progress", "done"])
            new_desc = st.text_input("New description (optional)")
            if st.button("Update"):
                try:
                    update_task(int(uid), description=new_desc if new_desc else None, status=new_status)
                    st.success("Task updated")
                    tasks = fetch_tasks()
                    df = pd.DataFrame(tasks)
                    st.dataframe(df, hide_index=True, use_container_width=True)
                except Exception as e:
                    st.error(f"Update failed: {e}")

        st.markdown("### Delete a Task")
        del_id = st.number_input("Task ID to delete", min_value=1, step=1, key="del")
        if st.button("Delete"):
            try:
                delete_task(int(del_id))
                st.success("Task deleted")
                tasks = fetch_tasks()
                df = pd.DataFrame(tasks)
            except Exception as e:
                st.error(f"Delete failed: {e}")
    else:
        st.info("No tasks yet. Add your first task above!")

with tab2:
    st.subheader("AI: Auto-generate tasks with Gemini")
    topic = st.text_input("Topic / Goal", placeholder="e.g., Build a churn prediction model")
    if st.button("Generate Suggestions"):
        if topic.strip():
            try:
                ideas = ai_generate(topic.strip())
                st.markdown("#### Suggestions")
                st.write(ideas)
            except Exception as e:
                st.error(f"Generation failed: {e}")
        else:
            st.warning("Please enter a topic.")

with tab3:
    st.subheader("AI: Summarize Feedback")
    fb = st.text_area("Paste student or user feedback")
    if st.button("Summarize"):
        if fb.strip():
            try:
                summary = ai_summarize(fb.strip())
                st.markdown("#### Summary")
                st.write(summary)
            except Exception as e:
                st.error(f"Summarization failed: {e}")
        else:
            st.warning("Please paste some feedback to summarize.")
