import streamlit as st
import pandas as pd
import plotly.express as px
import csv
import io
import re

# Function to process the uploaded data
def process_data(file):
    # Comprehensive mapping of countries and cities
    countries = [
        "United States", "United Kingdom", "Canada", "Australia", "Germany", "France", "Italy",
        "Spain", "China", "Japan", "India", "Russia", "Brazil", "Mexico", "South Africa",
        "Nigeria", "Kenya", "Argentina", "Chile", "Colombia", "Peru", "Venezuela", "Ecuador",
        "Turkey", "Saudi Arabia", "United Arab Emirates", "Egypt", "Israel", "Pakistan",
        "Bangladesh", "Vietnam", "Indonesia", "Malaysia", "Philippines", "Thailand",
        "South Korea", "New Zealand", "Singapore", "Sweden", "Norway", "Denmark", "Finland",
        "Netherlands", "Belgium", "Austria", "Switzerland", "Ireland", "Poland", "Portugal",
        "Czech Republic", "Hungary", "Greece", "Romania", "Bulgaria", "Slovakia", "Slovenia",
        "Croatia", "Serbia", "Ukraine", "Belarus", "Kazakhstan", "Uzbekistan", "Turkmenistan",
        "Azerbaijan", "Armenia", "Georgia", "Qatar", "Kuwait", "Bahrain", "Oman", "Jordan",
        "Lebanon", "Iraq", "Afghanistan", "Morocco", "Algeria", "Tunisia", "Libya", "Sudan",
        "Ethiopia", "Somalia", "Zimbabwe", "Zambia", "Mozambique", "Angola", "Botswana",
        "Namibia", "Malawi", "Tanzania", "Uganda", "Rwanda", "Burundi", "Ghana", "Ivory Coast",
        "Senegal", "Cameroon", "Chad", "Central African Republic", "Gabon", "Equatorial Guinea",
        "Congo", "Democratic Republic of the Congo", "Sierra Leone", "Liberia", "Guinea",
        "Mali", "Burkina Faso", "Niger", "Benin", "Togo", "Gambia", "Cape Verde", "Madagascar",
        "Maldives", "Sri Lanka", "Bhutan", "Nepal", "Myanmar", "Laos", "Cambodia", "Brunei",
        "East Timor", "Papua New Guinea", "Fiji", "Samoa", "Tonga", "Vanuatu", "Solomon Islands",
        "Micronesia", "Marshall Islands", "Palau", "Kiribati", "Nauru", "Tuvalu"
    ]

    cities = [
        "New York", "London", "Paris", "Tokyo", "Hong Kong", "Beijing", "Shanghai", "Dubai",
        "Singapore", "Los Angeles", "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide",
        "Canberra", "Hobart", "Wellington", "Auckland", "Christchurch", "Hamilton", "Dunedin",
        "Toronto", "Vancouver", "San Francisco", "Chicago", "Boston", "Madrid", "Barcelona",
        "Berlin", "Munich", "Frankfurt", "Milan", "Rome", "Naples", "Moscow", "St. Petersburg",
        "Istanbul", "Cape Town", "Johannesburg", "Buenos Aires", "Santiago", "Bogota", "Lima",
        "Mexico City", "Guadalajara", "Monterrey", "Rio de Janeiro", "Sao Paulo", "Brasilia",
        "Lisbon", "Zurich", "Geneva", "Amsterdam", "The Hague", "Stockholm", "Oslo", "Copenhagen",
        "Helsinki", "Dublin", "Warsaw", "Prague", "Vienna", "Budapest", "Athens", "Belgrade",
        "Kiev", "Riga", "Tallinn", "Vilnius", "Brussels", "Luxembourg", "Tel Aviv", "Doha",
        "Riyadh", "Abu Dhabi", "Manama", "Muscat", "Kuwait City", "Amman", "Cairo", "Casablanca",
        "Lagos", "Nairobi", "Accra", "Addis Ababa", "Dar es Salaam", "Harare", "Kigali",
        "Maputo", "Luanda", "Algiers", "Tunis", "Baghdad", "Tehran", "Kabul", "Islamabad",
        "Karachi", "Dhaka", "Colombo", "Kathmandu", "Bangkok", "Ho Chi Minh City", "Hanoi",
        "Manila", "Jakarta", "Kuala Lumpur", "Seoul", "Busan", "Taipei", "Kyoto", "Osaka",
        "Nagoya", "Fukuoka", "Sapporo", "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
        "Kolkata", "Pune", "Ahmedabad", "Surat", "Kanpur", "Jaipur", "Lucknow", "Nagpur",
        "Indore", "Patna", "Bhopal", "Vadodara", "Ludhiana", "Agra", "Thiruvananthapuram",
        "Coimbatore", "Kochi", "Mysore", "Guwahati", "Shillong", "Panaji", "Port Moresby",
        "Suva", "Apia", "Tonga", "Port Vila", "Honiara", "Nuku'alofa", "Majuro", "Funafuti"
    ]

    # Combine countries and cities into location mapping
    location_mapping = {city.lower(): country for city in cities for country in countries}

    # Map country codes to full names
    domain_to_country = {
        "au": "Australia", "uk": "United Kingdom", "nz": "New Zealand", "ca": "Canada",
        "us": "United States", "de": "Germany", "fr": "France", "in": "India",
        "jp": "Japan", "cn": "China", "br": "Brazil", "za": "South Africa", "ng": "Nigeria"
    }

    try:
        # Read the file content
        raw_data = file.getvalue().decode("utf-8")
        lines = raw_data.splitlines()
        header_found = False

        cleaned_lines = [line for line in lines if header_found or (header_found := "First Name" in line)]
        if not cleaned_lines:
            raise ValueError("The file does not contain a valid header or data rows.")

        # Convert to file-like object
        cleaned_csv = io.StringIO("\n".join(cleaned_lines))
        df = pd.read_csv(cleaned_csv)

        # Ensure required columns
        if 'Email Address' not in df.columns:
            raise ValueError("File must include 'Email Address'.")

        # Function to infer location
        def infer_location(row):
            # Check email address for domain-based location
            if pd.notnull(row.get("Email Address")):
                match = re.search(r"\.([a-z]{2})$", row["Email Address"])
                if match:
                    country_code = match.group(1).lower()
                    if country_code in domain_to_country:
                        return domain_to_country[country_code]

            return "Unknown"

        # Apply location inference
        df['Country'] = df.apply(infer_location, axis=1)
        country_counts = df['Country'].value_counts().reset_index()
        country_counts.columns = ['Country', 'Connections']
        return country_counts

    except Exception as e:
        raise ValueError(f"Error processing file: {e}")

# App title
st.title("LinkedIn Connections Geographical Heat Map")
st.write("Upload your LinkedIn connections CSV file to visualise their geographical distribution.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="file_uploader_1")

if uploaded_file:
    try:
        processed_data = process_data(uploaded_file)
        fig = px.choropleth(
            processed_data,
            locations="Country",
            locationmode="country names",
            color="Connections",
            title="Geographical Spread of LinkedIn Connections",
            color_continuous_scale="Reds"
        )
        fig.update_geos(
            showcoastlines=True,
            showcountries=True,
            countrycolor="Black",
            showocean=False,
            landcolor="White"
        )
        st.plotly_chart(fig)
    except ValueError as e:
        st.error(str(e))
else:
    st.info("Please upload a file.")
