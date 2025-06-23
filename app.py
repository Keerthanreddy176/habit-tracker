import streamlit as st
import pandas as pd
from datetime import date
import os
import altair as alt

st.set_page_config(page_title="Habit Tracker", layout="wide")
st.title("🧠 Personal Habit Tracker")

# Load or initialize data
csv_file = "habits.csv"
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=["Date", "Habit", "Status"])

# Sidebar filter
st.sidebar.header("🔍 Filter")
habit_filter = st.sidebar.selectbox("Select Habit", ["All"] + sorted(df["Habit"].unique()), index=0)

# Form input
with st.form("habit_form"):
    st.subheader("➕ Add New Habit")
    habit = st.text_input("Habit Name")
    status = st.radio("Status", ["Done", "Not Done"])
    submitted = st.form_submit_button("Add Entry")
    if submitted and habit:
        new_entry = {"Date": date.today(), "Habit": habit, "Status": status}
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(csv_file, index=False)
        st.success(f"Logged: {habit} - {status}")

# Filtered view
if habit_filter != "All":
    df = df[df["Habit"] == habit_filter]

# Display data
st.subheader("📅 Habit Log")
st.dataframe(df, use_container_width=True)

# Chart
if not df.empty:
    st.subheader("📊 Habit Completion Chart")
    chart = alt.Chart(df).mark_bar().encode(
        x="Habit:N",
        y="count():Q",
        color="Status:N"
    ).properties(width=600)
    st.altair_chart(chart, use_container_width=True)