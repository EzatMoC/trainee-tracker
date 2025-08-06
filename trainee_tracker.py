
import streamlit as st
import pandas as pd
from datetime import datetime

if "trainees" not in st.session_state:
    st.session_state.trainees = pd.DataFrame(columns=[
        "Name", "Email", "Phone", "Enrollment Date", "Completed Lectures", "Missed Lectures"
    ])

st.title("🎓 Trainee Tracker Dashboard")

menu = st.sidebar.radio("Navigate", ["📋 View All Trainees", "➕ Enroll New Trainee", "✅ Mark Attendance"])

if menu == "📋 View All Trainees":
    st.header("All Trainees")
    if st.session_state.trainees.empty:
        st.info("No trainees enrolled yet.")
    else:
        st.dataframe(st.session_state.trainees)

elif menu == "➕ Enroll New Trainee":
    st.header("Enroll New Trainee")
    with st.form("enroll_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        submit = st.form_submit_button("Enroll")

        if submit:
            if name and email:
                new_row = {
                    "Name": name,
                    "Email": email,
                    "Phone": phone,
                    "Enrollment Date": datetime.now().strftime("%Y-%m-%d"),
                    "Completed Lectures": 0,
                    "Missed Lectures": 0
                }
                st.session_state.trainees = st.session_state.trainees.append(new_row, ignore_index=True)
                st.success(f"{name} has been enrolled!")
            else:
                st.warning("Name and Email are required.")

elif menu == "✅ Mark Attendance":
    st.header("Mark Lecture Attendance")
    if st.session_state.trainees.empty:
        st.warning("No trainees to update.")
    else:
        lecture_number = st.number_input("Lecture Number", min_value=1, value=1, step=1)
        for idx, row in st.session_state.trainees.iterrows():
            col1, col2 = st.columns([3, 2])
            with col1:
                st.write(f"**{row['Name']}**")
            with col2:
                status = st.radio(
                    f"Lecture {lecture_number}", ["Present", "Absent"], key=f"{row['Email']}_{lecture_number}"
                )
                if status == "Present":
                    st.session_state.trainees.at[idx, "Completed Lectures"] += 1
                else:
                    st.session_state.trainees.at[idx, "Missed Lectures"] += 1

        st.success("✅ Attendance updated!")
