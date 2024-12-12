import streamlit as st
import pandas as pd
import plotly.express as px

# Function to process the uploaded data
def process_data(file):
    df = pd.read_csv(file)
    location_counts = df['Location'].value_counts().reset_index()
    location_counts.columns = ['Country', 'Connections']
    return location_counts

st.title("LinkedIn Connections Diversity Tool")
st.write("Upload your LinkedIn connections CSV file to analyse geographical diversity.")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="file_uploader_1")

if uploaded_file is not None:
    st.write("Uploaded File Preview:")
    try:
        # Read and display raw file content
        raw_data = uploaded_file.getvalue()
        st.text("Raw File Content:")
        st.text(raw_data.decode("utf-8"))  # Display raw file content

        # Try to parse the file as CSV
        data = pd.read_csv(uploaded_file)
        st.write("Parsed File Content:")
        st.write(data)  # Display parsed data for debugging

        # Check if 'Location' column exists
        if 'Location' not in data.columns:
            raise ValueError("The uploaded file does not have a 'Location' column.")

        # Process the data
        data = process_data(uploaded_file)
        st.write("Geographical Distribution:")
        st.write(data)

        # Create the map visualization
        fig = px.choropleth(
            data,
            locations="Country",
            locationmode="country names",
            color="Connections",
            title="Geographical Spread of LinkedIn Connections",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig)
    except Exception as e:
        # Display detailed error messages
        st.error(f"Error reading file or processing data: {e}")
else:
    st.info("Please upload a file to proceed.")
