import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

st.title("🎓 Student Performance Analysis Dashboard")


uploaded_file = st.file_uploader("Upload Student CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    
    df["Average"] = df[["Math", "Science", "English"]].mean(axis=1)

    def grade(avg):
        if avg >= 85:
            return 'A'
        elif avg >= 70:
            return 'B'
        elif avg >= 50:
            return 'C'
        else:
            return 'D'

    df["Grade"] = df["Average"].apply(grade)

    
    st.subheader("📄 Student Table")
    st.dataframe(df)

   
    st.sidebar.header("🔍 Filters")
    grade_filter = st.sidebar.multiselect(
        "Filter by Grade",
        options=df["Grade"].unique(),
        default=df["Grade"].unique()
    )
    attendance_threshold = st.sidebar.slider("Minimum Attendance (%)", 0, 100, 75)

    
    if "Attendance" in df.columns:
        filtered_df = df[(df["Grade"].isin(grade_filter)) & (df["Attendance"] >= attendance_threshold)]
    else:
        filtered_df = df[df["Grade"].isin(grade_filter)]

    st.subheader("✅ Filtered Students")
    st.dataframe(filtered_df)

    
    st.subheader("🏆 Top 3 Students by Average")
    st.dataframe(df.sort_values("Average", ascending=False).head(3))

   
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Average Marks")
        plt.figure(figsize=(10, 5))
        sns.barplot(x="Name", y="Average", data=df, palette="viridis")
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())
        plt.clf()

    with col2:
        if "Attendance" in df.columns:
            st.subheader("📈 Attendance")
            plt.figure(figsize=(10, 5))
            sns.barplot(x="Name", y="Attendance", data=df, palette="coolwarm")
            plt.xticks(rotation=45)
            st.pyplot(plt.gcf())
            plt.clf()
        else:
            st.info("Attendance data not available to plot.")


    st.subheader("🎓 Grade Distribution")
    grade_counts = df["Grade"].value_counts()
    plt.figure(figsize=(5, 5))
    plt.pie(
        grade_counts,
        labels=grade_counts.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=['#4CAF50', '#2196F3', '#FFC107', '#F44336']
    )
    st.pyplot(plt.gcf())
    plt.clf()

else:
    st.info("📥 Please upload a student data CSV file to begin.")
