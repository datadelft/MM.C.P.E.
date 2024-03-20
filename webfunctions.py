import streamlit as st
from database import query_db
from datetime import datetime
from filefunctions import export_to_csv
from filefunctions import string_to_filename


def channel_name_dropdown():

    # Fetch rows into lists
    channel_names_from_database = []
    channel_ids_from_database = []

    query = "select Id, DisplayName from Channels"

    for row in query_db(query):
        channel_id, channel_name = row  # row returned is tuple ("id", "name"), we split it here
        if channel_name != "":
            channel_ids_from_database.append(channel_id)  # list with indexes matching those of the names
            channel_names_from_database.append(channel_name)  # list with indexes matching those of the id's

    # Create a dropdown selection box
    selected_option = st.selectbox(
        'Select a channel to export',
        channel_names_from_database
    )

    # return the channel_id directly instead of the channel_name
    index = channel_names_from_database.index(
        selected_option)  # check the index in the list for the chosen channel name
    return channel_ids_from_database[index], \
        channel_names_from_database[index]  # return the channel ID and name


def export_data(chan_id, chan_name):

    query = "SELECT UserName, Message FROM Posts INNER JOIN Users " \
            "ON Posts.UserId = Users.Id WHERE ChannelId = '" + chan_id + "' ORDER BY Posts.CreateAt"

    # Fetch rows into lists
    posts = []
    for row in query_db(query):
        posts.append(row)

    # Create a download button for the CSV file
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    export_to_csv(posts, current_datetime + "_" + string_to_filename(chan_name) + ".csv")

    # display results
    st.table(posts)
