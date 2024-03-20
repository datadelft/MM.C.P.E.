import mysql.connector
from filefunctions import read_database_config
import streamlit as st


def query_db(query):
    # Establish a connection to the database
    try:
        # Accessing database information
        config = read_database_config('database.yaml')
        connection = mysql.connector.connect(
            host=config['database']['host'],
            user=config['database']['user'],
            password=config['database']['password'],
            database=config['database']['database']
        )

        print("Connected to the database")
        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        if connection.is_connected() and query != "":

            # Execute the query
            cursor.execute(query)

            # Fetch all rows
            rows = cursor.fetchall()

            # Close the connection
            if connection is not None and connection.is_connected():
                cursor.close()
                connection.close()
                print("Connection closed")

            return rows

    except mysql.connector.Error as e:
        st.write("Error connecting to the database:", e)

    finally:
        print("Done")
