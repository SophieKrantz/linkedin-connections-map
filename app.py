import streamlit as st
import pandas as pd
import plotly.express as px

# Function to process the uploaded data
def process_data(file):
    try:
        df = pd.read_csv(file)
        if 'Location' not in df.columns:
            raise ValueError("The uploaded file does not have a 'Location' column.")
        location_counts = df['Location'].value_counts().reset_index()
        location_counts.columns = ['Country', 'Connections']
        return location_counts
    except pd.errors.EmptyDataError:
        raise ValueError("The uploaded file is empty or improperly formatted.")
    except Exception as e:
        raise ValueError(f"Unexpected error while processing the file: {e}")

# App title
st.title("LinkedIn Connections Diversity Tool")
st.write("Upload your LinkedIn connections CSV file to analyse geographical diversity.")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="file_uploader_1")

if uploaded_file is not None:
    st.write("Uploaded File Preview:")
    try:
        # Display raw file content for debugging
        raw_data = uploaded_file.getvalue()
        st.text("Raw File Content:")
        st.text(raw_data.decode("utf-8"))  # Display raw file content as text

        # Parse the file as CSV
        data = pd.read_csv(uploaded_file)
        st.write("Parsed File Content:")
        st.write(data)  # Display parsed data for debugging

        # Process the data
        processed_data = process_data(uploaded_file)
        st.write("Geographical Distribution:")
        st.write(processed_data)

        # Create the map visualization
        fig = px.choropleth(
            processed_data,
            locations="Country",
            locationmode="country names",
            color="Connections",
            title="Geographical Spread of LinkedIn Connections",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig)
    except ValueError as ve:
        st.error(f"Error: {ve}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
else:
    st.info("Please upload a file to proceed.")
