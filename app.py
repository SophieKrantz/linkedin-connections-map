import streamlit as st
import pandas as pd
import plotly.express as px
import csv
import io

# Function to process the uploaded data
def process_data(file):
    # Example mapping of companies to headquarters
    company_headquarters = {
        "Google": "United States",
        "Microsoft": "United States",
        "Amazon": "United States",
        "Tencent": "China",
        "Tata Consultancy Services": "India",
        "BMW": "Germany",
        "Unilever": "United Kingdom",
        "Toyota": "Japan",
        "Volkswagen": "Germany",
    }

    # List of location keywords (countries, cities, and regions)
    location_keywords = {
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

        # Cities
        "London": "United Kingdom",
        "Geneva": "Switzerland",
        "Sydney": "Australia",
        "Melbourne": "Australia",
        "Munich": "Germany",
        "Shanghai": "China",

        # Regions
        "Asia": "Asia",
        "Europe": "Europe",
        "North America": "North America",
        "Africa": "Africa",
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
            for keyword, country in location_keywords.items():
                if pd.notnull(row['Position']) and keyword.lower() in row['Position'].lower():
   
