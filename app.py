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

        # Split lines and find the header
        lines = raw_data.splitlines()
        cleaned_lines = []
        header_found = False

        for line in lines:
            if not header_found and "First Name" in line and "Location" in line:
                header_found = True  # Header row identified
            if header_found:
                cleaned_lines.append(line)  # Keep rows after the header

        # Convert cleaned lines into a file-like object
        cleaned_csv = io.StringIO("\n".join(cleaned_lines))

        # Detect the delimiter
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(cleaned_lines[0]).delimiter

        # Read the cleaned CSV
        df = pd.read_csv(cleaned_csv, delimiter=delimiter)

        # Ensure the 'Location' column exists
        if 'Location' not in df.columns:
            raise ValueError("The uploaded file does not have a 'Location' column.")

        # Count connections by location
        location_counts = df['Location'].value_counts().reset_index()
        location_counts.columns = ['Country', 'Connections']
        return location_counts

    except pd.errors.ParserError as e:
        raise ValueError(f"Error parsing the cleaned CSV file: {e}")
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
