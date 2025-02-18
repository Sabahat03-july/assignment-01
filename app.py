from io import BytesIO
import streamlit as st
import os
import pandas as pd

st.set_page_config(page_title="Data Sweeper", layout="wide") 
st.title("Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization")

uploaded_files = st.file_uploader("Upload Your Files (CSV or Excel)",type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1]
        
        if file_ext == ".csv":
            df = pd.read_csv(file)
            
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else : 
            st.error(f"Invalid file type {file_ext}. Please upload a CSV or Excel file.")
            continue
        
        st.write(f"**File Name:** {file.name} ")
        st.write(f"**File Size:** {file.size/1024} KB")

        st.write("Preview the Head of The Data Frame")
        st.dataframe(df.head()) 
        
        st.subheader("Data Cleaning Options") 
        if st.checkbox(f"Clean Data for FileName: {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):      
                    df.drop_duplicates(inplace=True)
                    st.write(f"Removed Duplicates from {file.name}")
            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_columns = df.select_dtypes(include=['number']).columns
                    df[numeric_columns]= df[numeric_columns].fillna(df[numeric_columns].mean())
                    st.write("Filled Missing Values")
        
        st.subheader("Select Columns To Convert")
        columns = st.multiselect(f"Select Columns For {file.name}", df.columns)
        df = df[columns]
        
        
        st.subheader("Data Visualization")
        if st.checkbox(f"Visualize {file.name}"):
            st.bar_chart(df.select_dtypes(include=['number']).iloc[:,:2])
            
        st.subheader("Conversion Option")
        conversion_types = st.radio(f"convert {file.name} to ",["CSV","Excel"],key=f"conversion_type_{file.name}")
        
        
        if st.button(f"Convert {file.name} to {conversion_types}"):
            buffer = BytesIO()
            if conversion_types == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mine_type = "text/csv"
                
                
            elif conversion_types == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mine_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
        
        
        
            st.download_button(
                label=(f"Download {file_name} as {conversion_types}"),
                data=buffer,
                file_name=file_name,
                mine_type=mine_type
            )
        # if conversion_types == "CSV":
        #     csv_buffer = BytesIO()
        #     df.to_csv(csv_buffer, index=False)  
        #     st.download_button(f"Download {file.name} as CSV", data=csv_buffer.getvalue(), file_name=file.name, mime="text/csv")
        # elif conversion_types == "Excel":
        #     excel_buffer = BytesIO()
        #     df.to_excel(excel_buffer, index=False)
        #     st.download_button(f"Download {file.name} as Excel", data=excel_buffer.getvalue(), file_name=file.name, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.success("All files processed!")        