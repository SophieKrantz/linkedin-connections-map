import streamlit as st
import pandas as pd
import plotly.express as px
import csv
import io

# Function to process the uploaded data
def process_data(file):
    try:
        # Read the raw file content
        raw_data = file.getvalue().decode("utf-8")

        # Split lines to skip metadata notes
        lines = raw_data.splitlines()
        cleaned_lines = []
        header_found = False

        for line in lines:
            # Look for the header row starting with "First Name"
            if not header_found and "First Name" in line:
                header_found = True  # Header row identified
            if header_found:
                cleaned_lines.append(line)  # Keep rows after the header

        if not cleaned_lines:
            raise ValueError("The file does not contain a valid header or data rows.")

        # Convert cleaned lines into a file-like object
        cleaned_csv = io.StringIO("\n".join(cleaned_lines))

        # Read the cleaned CSV
        df = pd.read_csv(cleaned_csv)

        # Attempt to find a column that could represent location
        possible_columns = ['Location', 'Country', 'City', 'Region']
        location_column = None
        for col in possible_columns:
            if col in df.columns:
                location_column = col
                break

        if not location_column:
            raise ValueError("The uploaded file does not have a column for geographic data (e.g., 'Location', 'Country').")

        # Count connections by the detected location column
        location_counts = df[location_column].value_counts().reset_index()
        location_counts.columns = ['Country', 'Connections']
        return location_counts

    except pd.errors.ParserError as e:
        raise ValueError(f"Error parsing the cleaned CSV file: {e}")
    except Exception as e:
        raise ValueError(f"Unexpected error while processing the file: {e}")

# App title
st.title("LinkedIn Connections Geographical Heat Map")
st.write("Upload your LinkedIn connections CSV file to visualise their geographical distribution.")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="file_uploader_1")

if uploaded_file is not None:
    try:
        # Process the data
        processed_data = process_data(uploaded_file)

        # Create the heat map
        st.write("Geographical Distribution of LinkedIn Connections:")
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
