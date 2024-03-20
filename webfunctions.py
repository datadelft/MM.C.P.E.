import streamlit as st
from database import query_db
from datetime import datetime
from filefunctions import export_to_csv
from filefunctions import string_to_filename
from filefunctions import get_base64
from database import fetch_first_from_db

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


def export_data(chan_id, chan_name, from_datetime, to_datetime):

    print(from_datetime, to_datetime)

    query = "SELECT UserName, Message " \
            "FROM Posts INNER JOIN Users " \
            "ON Posts.UserId = Users.Id WHERE (ChannelId = '" + chan_id + "' and " \
            "Posts.CreateAt >= " + str(from_datetime) + " and " \
            "Posts.CreateAt <= " + str(to_datetime) + " ) ORDER BY Posts.CreateAt"

    print(query)

    # Fetch rows into lists
    posts = []
    for row in query_db(query):
        posts.append(row)

    # Create a download button for the CSV file
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    export_to_csv(posts, current_datetime + "_" + string_to_filename(chan_name) + ".csv")

    # display results
    st.table(posts)


def show_background():
    # decode the binary
    bin_str = get_base64("img/background.jpg")
    # set the style element
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    # render the background
    st.markdown(page_bg_img, unsafe_allow_html=True)


def get_user_timeframe(chan_id):

    # find first post timestamp in selected channel
    # mattermost uses unix timestamps for the CreateAt field of a post.
    query = "SELECT MIN(CreateAt) FROM Posts WHERE ChannelId = '" + chan_id + "'"
    first_post_timedate_in_ms = fetch_first_from_db(query)

    print("Received timestamp in milliseconds" + str(first_post_timedate_in_ms))
    # determine the first post date available in the database
    original_from_unix = first_post_timedate_in_ms / 1000  # from timestamp can only process seconds not ms
    original_from = datetime.fromtimestamp(original_from_unix)

    # Extract date and time components
    preset_date = original_from.date()
    preset_time = original_from.time()

    # Create a layout with two columns
    col1, col2 = st.columns(2)

    # Get 'from' date and time input from the user
    with col1:
        from_date = st.date_input("From Date", preset_date)
    with col2:
        from_time = st.time_input("From Time", preset_time)

    # Get 'to' date and time input from the user
    with col1:
        to_date = st.date_input("To Date")
    with col2:
        to_time = st.time_input("To Time")

    # Combine date and time inputs into datetime objects
    from_datetime = datetime.combine(from_date, from_time)
    to_datetime = datetime.combine(to_date, to_time)

    unix_from = int(from_datetime.timestamp())
    unix_to = int(to_datetime.timestamp())

    return unix_from, unix_to
