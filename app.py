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
uploaded_file = st.file_up
