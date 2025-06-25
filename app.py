import streamlit as st
import pandas as pd
from datetime import date
import os
import altair as alt

# Configure page
st.set_page_config(page_title="Habit Tracker", layout="wide")
st.title("🧠 Personal Habit Tracker")

# --- User Login ---
st.sidebar.header("👤 User Login")
username = st.sidebar.text_input("Enter your name")

if not username:
    st.warning("Please enter your name to access your habit tracker.")
    st.stop()

# Define user-specific CSV file
user_file = f"habits_{username}.csv"

# Load or initialize data
if os.path.exists(user_file):
    df = pd.read_csv(user_file)
else:
    df = pd.DataFrame(columns=["Date", "Habit", "Status"])

# --- Sidebar Filter ---
st.sidebar.header("🔍 Filter")
habit_filter = st.sidebar.selectbox(
    "Select Habit", ["All"] + sorted(df["Habit"].unique()), index=0
)

# --- Form Input ---
with st.form("habit_form"):
    st.subheader("➕ Add New Habit")
    habit = st.text_input("Habit Name")
    status = st.radio("Status", ["Done", "Not Done"])
    submitted = st.form_submit_button("Add Entry")
    if submitted and habit:
        new_entry = {"Date": date.today(), "Habit": habit, "Status": status}
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(user_file, index=False)
        st.success(f"🎉 Logged: {habit} - {status}")
        st.balloons()

# --- Filtered View ---
filtered_df = df.copy()
if habit_filter != "All":
    filtered_df = filtered_df[filtered_df["Habit"] == habit_filter]

# --- Display Data ---
st.subheader("📅 Habit Log")
if not filtered_df.empty:
    st.dataframe(filtered_df, use_container_width=True)
    st.metric("📈 Total Habits Logged", len(filtered_df))
else:
    st.info("No entries to show for this selection yet.")

# --- Chart ---
if not filtered_df.empty:
    st.subheader("📊 Habit Completion Chart")
    chart = alt.Chart(filtered_df).mark_bar().encode(
        x="Habit:N",
        y="count():Q",
        color="Status:N"
    ).properties(width=600)
    st.altair_chart(chart, use_container_width=True)