import csv
from io import StringIO
import yaml
import streamlit as st


def read_database_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def export_to_csv(data, file_name):
    # Create a CSV string from the data
    csv_data = StringIO()
    writer = csv.writer(csv_data, delimiter=';')
    writer.writerows(data)

    # Create a download link for the CSV file
    csv_data_str = csv_data.getvalue().encode('utf-8').strip()
    st.download_button(
        label="Download CSV",
        data=csv_data_str,
        file_name=file_name,
        mime="text/csv"
    )


def string_to_filename(s):
    # Replace invalid characters with underscores
    valid_chars = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    filename = ''.join(c if c in valid_chars else '_' for c in s)
    # Remove leading/trailing spaces and double underscores
    filename = filename.strip().replace('__', '_')
    return filename
