from io import BytesIO
import streamlit as st
import os
import pandas as pd
import random

# Initialize XP System State
if 'xp' not in st.session_state:
    st.session_state.xp = 0

def earn_xp(points):
    st.session_state.xp += points
    st.success(f"🎉 You earned {points} XP! Keep going!")

# Growth Mindset Encouraging Messages
def growth_message():
    messages = [
        "Great job! Every small step adds up. 🚀",
        "Mistakes are proof that you are trying! Keep learning. 💡",
        "Data cleaning is an art, and you are mastering it! 🎨",
        "Challenge yourself! Try exploring new insights. 📊",
        "Keep pushing! Growth happens outside the comfort zone. 🔥"
    ]
    return random.choice(messages)

st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("Data Sweeper: Growth Edition 🚀")
st.write("Transform your files while developing a growth mindset. Earn XP for every action!")
st.write(f"🌟 Your XP: {st.session_state.xp}")

uploaded_files = st.file_uploader("Upload Your Files (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1]
        
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"Invalid file type {file_ext}. Please upload a CSV or Excel file.")
                continue
        except Exception as e:
            st.error(f"Error loading file {file.name}: {str(e)}")
            continue
        
        st.write(f"*File Name:* {file.name} ")
        st.write(f"*File Size:* {file.size/1024:.2f} KB")
        
        st.write("Preview The Head of The Data Frame")
        st.dataframe(df.head())
        
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write(f"✅ Removed Duplicates from {file.name}")
                    earn_xp(10)
            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_columns = df.select_dtypes(include=['number']).columns
                    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
                    st.write("✅ Filled Missing Values")
                    earn_xp(10)
        
        st.subheader("AI Smart Insights")
        if st.button(f"Get AI Insights for {file.name}"):
            insight = random.choice([
                "Consider normalizing numerical columns for better analysis.",
                "Removing outliers can improve your dataset quality.",
                "Try encoding categorical variables for machine learning models.",
                "Check if there are correlated features for better feature selection.",
                "Exploring different visualization methods can unlock hidden patterns."
            ])
            st.info(f"🤖 AI Suggestion: {insight}")
            earn_xp(5)
        
        st.subheader("Select Columns To Convert")
        columns = st.multiselect(f"Select Columns For {file.name}", df.columns)
        if columns:
            df = df[columns]
        
        st.subheader("Data Visualization")
        if st.checkbox(f"Visualize {file.name}"):
            st.bar_chart(df.select_dtypes(include=['number']).iloc[:, :2])
            earn_xp(15)
            st.write(growth_message())
        
        st.subheader("Conversion Option")
        conversion_types = st.radio(f"Convert {file.name} to", ["CSV", "Excel"], key=f"conversion_type_{file.name}")
        
        if st.button(f"Convert {file.name} to {conversion_types}"):
            buffer = BytesIO()
            try:
                if conversion_types == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conversion_types == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)
                
                st.download_button(
                    label=f"Download {file_name} as {conversion_types}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )
                earn_xp(20)
                st.write(growth_message())
            except Exception as e:
                st.error(f"Error converting file: {str(e)}")
    
    st.success("All files processed! Keep growing your skills! 🚀")
    st.progress(min(st.session_state.xp / 100, 1.0))
    
    st.subheader("Join the Growth Mindset Community")
    st.write("Want to learn and grow with others? Join our community!")
    if st.button("Join Now 💡"):
        st.balloons()
        st.success("Welcome to the Growth Mindset Community! Keep learning and innovating! 🌍")