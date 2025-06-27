import streamlit as st
import pandas as pd
import altair as alt
from datetime import date, timedelta
import os

# -- Setup --
st.set_page_config(page_title="Habit Tracker", layout="wide")
st.title("🧠 Personal Habit Tracker")

# -- Sidebar Login --
with st.sidebar:
    st.header("👤 User Login")
    username = st.text_input("Enter your name")
    dark_mode = st.toggle("🌙 Dark Mode", value=True)

if not username:
    st.warning("Enter your name to continue.")
    st.stop()

# -- File Handling --
user_file = f"habits_{username}.csv"
if os.path.exists(user_file):
    df = pd.read_csv(user_file, parse_dates=["Date"])
else:
    df = pd.DataFrame(columns=["Date", "Habit", "Status"])
    df.to_csv(user_file, index=False)

# -- Add New Habit Entry --
with st.form("habit_form"):
    st.subheader("➕ Add New Habit")
    col1, col2 = st.columns(2)
    with col1:
        habit = st.text_input("Habit")
    with col2:
        status = st.radio("Status", ["Done", "Not Done"], horizontal=True)
    submitted = st.form_submit_button("Log Entry")

    if submitted and habit:
        new_entry = {"Date": date.today(), "Habit": habit.strip().title(), "Status": status}
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(user_file, index=False)
        st.success(f"✅ Logged: {habit} - {status}")
        st.balloons()

# -- Filters --
st.sidebar.header("🔍 Filters")
habit_filter = st.sidebar.selectbox("Filter by Habit", ["All"] + sorted(df["Habit"].unique()))
filtered_df = df if habit_filter == "All" else df[df["Habit"] == habit_filter]

# -- Tabbed Interface --
tab1, tab2, tab3 = st.tabs(["📅 Habit Log", "📈 Insights", "⏳ Streaks"])

# -- 📅 Tab 1: Log Display --
with tab1:
    st.subheader("📋 Habit History")
    st.dataframe(filtered_df.sort_values(by="Date", ascending=False), use_container_width=True)
    if not filtered_df.empty:
        st.metric("Total Entries", len(filtered_df))
        st.metric("Unique Habits", filtered_df['Habit'].nunique())
    else:
        st.info("No entries yet. Start logging habits!")

# -- 📈 Tab 2: Visual Insights --
with tab2:
    if not filtered_df.empty:
        chart = alt.Chart(filtered_df).mark_bar().encode(
            x="Habit:N",
            y="count():Q",
            color="Status:N"
        ).properties(height=400)
        st.altair_chart(chart, use_container_width=True)

        # Pie chart
        pie_data = filtered_df['Status'].value_counts().reset_index()
        pie_data.columns = ['Status', 'Count']
        pie_chart = alt.Chart(pie_data).mark_arc().encode(
            theta="Count:Q",
            color="Status:N",
            tooltip=["Status", "Count"]
        )
        st.altair_chart(pie_chart, use_container_width=True)
# -- ⏳ Tab 3: Streaks --
with tab3:
    st.subheader("🔥 Weekly Habit Streaks")
    if not filtered_df.empty:
        streak_df = filtered_df.copy()
        streak_df["Date"] = pd.to_datetime(streak_df["Date"], errors='coerce')
        streak_df["Week"] = streak_df["Date"].dt.to_period("W").apply(lambda r: r.start_time)
        streak_count = streak_df.groupby(["Week", "Habit", "Status"]).size().unstack(fill_value=0).reset_index()
        st.dataframe(streak_count, use_container_width=True)
    else:
        st.info("Streak data will show once you log more entries.")

        st.info("Streak data will show once you log more entries.")

# -- Footer --
st.caption("🛠️ Made with ❤️ in Streamlit")
