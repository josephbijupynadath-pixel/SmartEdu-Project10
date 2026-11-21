from modules.recommendation import recommend_resources
from modules.prediction import predict_marks, load_training_data, evaluate_model
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="SmartEdu",
    page_icon="🎓",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
.block-container {
    padding-top: 2rem;
}
h1 {
    color: #183153;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🎓 SmartEdu")
st.sidebar.caption("Smart Education System")
st.sidebar.divider()

page = st.sidebar.radio(
    "MAIN MENU",
    [
        "Home",
        "Student Dashboard",
        "AI Prediction",
        "Learning Resources",
        "Blockchain Security",
        "Research Results"
    ]
)

st.sidebar.divider()
st.sidebar.info("AI-Based Personalized Learning & Secure Academic Records")

# HOME PAGE
if page == "Home":

    st.title("🎓 Welcome to SmartEdu")

    st.subheader(
        "AI-Based Personalized Learning and "
        "Blockchain-Secured Academic Records"
    )

    st.write(
        "SmartEdu is an intelligent educational platform "
        "designed to support personalized learning, "
        "student performance prediction and secure "
        "academic record verification."
    )

    st.divider()

    st.subheader("Application Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📊 Student Dashboard")
        st.write("Monitor student learning and academic performance.")

    with col2:
        st.info("🤖 AI Prediction")
        st.write("Predict student performance using Machine Learning.")

    with col3:
        st.info("📚 Personalized Learning")
        st.write("Provide suitable learning resources.")

    col4, col5 = st.columns(2)

    with col4:
        st.info("🔐 Blockchain Security")
        st.write("Verify the integrity of academic records.")

    with col5:
        st.info("📈 Research Results")
        st.write("Evaluate model performance and research findings.")

    st.divider()

    st.success("Welcome! Select a page from the sidebar to continue.")

# STUDENT DASHBOARD
elif page == "Student Dashboard":

    import pandas as pd

    st.title("📊 Student Dashboard")
    st.write("Student academic performance overview.")

    # Load student dataset
    df = pd.read_csv("data/students.csv")

    # Display student statistics
    st.subheader("Student Statistics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Students", len(df))
    col2.metric("Average Marks", round(df["Marks"].mean(), 2))
    col3.metric("Average Attendance", round(df["Attendance"].mean(), 2))
    col4.metric("Departments", df["Department"].nunique())

    # Display student records
    st.subheader("Student Academic Records")
    st.dataframe(df, use_container_width=True)

    # Marks visualization
    st.subheader("Student Marks Analysis")
    st.bar_chart(df.set_index("Student_Name")["Marks"])

    # Attendance visualization
    st.subheader("Student Attendance Analysis")
    st.bar_chart(df.set_index("Student_Name")["Attendance"])


# AI PREDICTION
elif page == "AI Prediction":

    st.title("🤖 AI-Based Student Performance Prediction")

    st.write("Predict student academic performance using Machine Learning.")

    try:
        df = load_training_data()

        st.subheader("Enter Student Details")

        col1, col2 = st.columns(2)

        with col1:
            department = st.selectbox(
                "Select Department",
                sorted(df["Department"].unique())
            )

            semester = st.selectbox(
                "Select Semester",
                sorted(df["Semester"].unique())
            )

        with col2:
            subject = st.selectbox(
                "Select Subject",
                sorted(df["Subject"].unique())
            )

            attendance = st.slider(
                "Attendance Percentage",
                0, 100, 80
            )

        if st.button("Predict Student Performance"):

            marks = predict_marks(
                department,
                semester,
                subject,
                attendance
            )

            st.subheader("Prediction Results")

            st.metric("Predicted Marks", f"{marks}/100")

            if marks >= 85:
                category = "Excellent"
                st.success("Excellent Performance!")

            elif marks >= 70:
                category = "Good"
                st.success("Good Performance!")

            elif marks >= 50:
                category = "Average"
                st.warning("Average Performance")

            else:
                category = "At Risk"
                st.error("Student Needs Academic Support")

            st.write("Performance Category:", category)

            st.progress(int(marks))

            st.info(
                "Recommendation: Continue regular learning "
                "and maintain good attendance."
            )

        st.caption(
            f"Model trained using {len(df)} student records."
        )

    except Exception as e:
        st.error(f"Prediction error: {e}")

# LEARNING RESOURCES
elif page == "Learning Resources":

    st.title("📚 Personalized Learning Resources")

    st.write("Learning materials based on student academic needs.")

    subject = st.selectbox(
        "Select Subject",
        ["Database", "Python", "Mathematics", "Computer Networks"]
    )

    marks = st.slider("Enter Student Marks", 0, 100, 60)

    attendance = st.slider(
        "Attendance Percentage", 0, 100, 80
    )

    if st.button("Get Learning Recommendations"):

        recommendations = recommend_resources(
            subject, marks, attendance
        )

        st.subheader("Recommended Learning Resources")

        for item in recommendations:
            st.write("📌", item)
            
# BLOCKCHAIN SECURITY

elif page == "Blockchain Security":

    from modules.blockchain import (
        create_blockchain,
        verify_blockchain
    )

    st.title("🔒 Blockchain Academic Record Security")

    st.write("Secure academic records and verify their integrity.")

    st.subheader("Create Secure Academic Record")

    student_id = st.text_input("Student ID")
    student_name = st.text_input("Student Name")
    grade = st.text_input("Academic Grade")

    if st.button("Generate Blockchain Record"):

        if student_id and student_name and grade:

            record = {
                "student_id": student_id,
                "name": student_name,
                "grade": grade
            }

            blockchain = create_blockchain([record])

            st.session_state["blockchain"] = blockchain

            st.success("Academic record secured successfully!")

            st.write("Generated SHA-256 Hash:")

            st.code(blockchain[0]["hash"])

        else:
            st.warning("Please fill in all fields.")

    st.divider()

    st.subheader("Verify Academic Record")

    if "blockchain" in st.session_state:

        if st.button("Verify Blockchain"):

            if verify_blockchain(st.session_state["blockchain"]):
                st.success("Blockchain is valid. Record integrity verified!")
            else:
                st.error("Blockchain verification failed!")

    else:
        st.info("Generate an academic record first.")

# RESEARCH RESULTS
elif page == "Research Results":
    st.title("📊 Research Results")
    st.write("Machine Learning Model Evaluation and Research Analysis.")

    try:
        results = evaluate_model()

        m1, m2, m3 = st.columns(3)
        m1.metric("MAE", results["MAE"])
        m2.metric("RMSE", results["RMSE"])
        m3.metric("R² Score", results["R2 Score"])

        c1, c2 = st.columns(2)
        c1.metric("Training Records", results["Training Records"])
        c2.metric("Testing Records", results["Testing Records"])

        st.subheader("Actual vs. Predicted Marks")
        comparison_df = results["Comparison"]
        st.dataframe(comparison_df, width="stretch")
        st.bar_chart(comparison_df, width="stretch")

    except Exception as e:
        st.error(f"Error displaying research results: {e}")
