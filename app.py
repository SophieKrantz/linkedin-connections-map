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
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    st.write("Uploaded File Preview:")
    try:
        # Display the file content for debugging
        data = pd.read_csv(uploaded_file)
        st.write(data)
        
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
        # Display the error message if something goes wrong
        st.error(f"Error reading file or processing data: {e}")
else:
    st.info("Please upload a file to proceed.")
