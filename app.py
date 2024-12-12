import streamlit as st
import pandas as pd
import plotly.express as px
import csv
import io

# Function to process the uploaded data
def process_data(file):
    # Comprehensive mapping of countries, major cities, states, and regions
    location_mapping = {
        # Countries
        "Australia": "Australia",
        "India": "India",
        "Germany": "Germany",
        "China": "China",
        "Japan": "Japan",
        "United States": "United States",
        "UK": "United Kingdom",
        "New Zealand": "New Zealand",
        "Canada": "Canada",
        "Brazil": "Brazil",
        "South Africa": "South Africa",
        "Russia": "Russia",
        "France": "France",
        "Italy": "Italy",
        "Spain": "Spain",
        "Mexico": "Mexico",
        "Indonesia": "Indonesia",
        "Nigeria": "Nigeria",

        # Major Cities
        "London": "United Kingdom",
        "Geneva": "Switzerland",
        "Sydney": "Australia",
        "Melbourne": "Australia",
        "Munich": "Germany",
        "Berlin": "Germany",
        "Shanghai": "China",
        "Beijing": "China",
        "New York": "United States",
        "Los Angeles": "United States",
        "Paris": "France",
        "Rome": "Italy",
        "Moscow": "Russia",
        "Tokyo": "Japan",
        "Rio de Janeiro": "Brazil",

        # States and Regions
        "California": "United States",
        "Texas": "United States",
        "Victoria": "Australia",
        "Queensland": "Australia",
        "Bavaria": "Germany",
        "Ontario": "Canada",
        "Quebec": "Canada",
        "Africa": "Africa",
        "Europe": "Europe",
        "Asia": "Asia",
        "North America": "North America",
        "Latin America": "Latin America",
        "Middle East": "Middle East",
    }

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

        # Ensure the required columns exist
        if 'Company' not in df.columns or 'Position' not in df.columns:
            raise ValueError("The uploaded file does not have the required columns: 'Company' or 'Position'.")

        # Infer locations from Company and Position
        def infer_location(row):
            # Check Position for location keywords
            for keyword, country in location_mapping.items():
                if pd.notnull(row['Position']) and keyword.lower() in row['Position'].lower():
                    return country

            # Check Company for location keywords
            for keyword, country in location_mapping.items():
                if pd.notnull(row['Company']) and keyword.lower() in row['Company'].lower():
                    return country

            # Fallback to Unknown
            return "Unknown"

        # Apply the inference logic
        df['Country'] = df.apply(infer_location, axis=1)

        # Count connections by inferred country
        country_counts = df['Country'].value_counts().reset_index()
        country_counts.columns = ['Country', 'Connections']
        return country_counts

    except pd.errors.ParserError as e:
        raise ValueError(f"Error parsing the cleaned CSV file: {e}")
    except Exception as e:
        raise ValueError(f"Unexpected error while processing the file: {e}")

# App title
st.title("LinkedIn Connections Geographical Heat Map")
st.write("Upload your LinkedIn connections CSV file to visualise their geographical distribution (inferred from company and position data).")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="file_uploader_1")

if uploaded_file is not None:
    try:
        # Process the data
        processed_data = process_data(uploaded_file)

        # Create the choropleth heat map
        st.write("Geographical Distribution of LinkedIn Connections:")
        fig = px.choropleth(
            processed_data,
            locations="Country",
            locationmode="country names",
            color="Connections",
            title="Geographical Spread of LinkedIn Connections (Inferred)",
            color_continuous_scale="Reds",  # Use a warm color scale
            range_color=[1, processed_data['Connections'].max()],  # Start from 1 to ensure all countries are shown
        )
        fig.update_geos(
            showcoastlines=True,
            showland=True,
            landcolor="LightGray",  # Background for non-connection areas
            showcountries=True,
            countrycolor="Black",  # Outline all countries
            showocean=False,  # Remove ocean for a clean look
        )
        st.plotly_chart(fig)
    except ValueError as ve:
        st.error(f"Error: {ve}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
else:
    st.info("Please upload a file to proceed.")
