import streamlit as st
import webfunctions as web


if __name__ == '__main__':

    web.show_background()

    st.title("MM.C.P.E.")
    st.write("The streamlit MatterMost Channel Post Exporter ;-)")

    channel_id, channel_name = web.channel_name_dropdown()  # create the dropdown selection with channel names

    from_datetime, to_datetime = web.get_user_timeframe(channel_id)

    # Create a clickable button
    if st.button('Export'):
        st.write('Button clicked, channel choice was ' + channel_name + " with id " + channel_id)

        web.export_data(channel_id, channel_name, from_datetime * 1000 , to_datetime * 1000)  # *1000 to get back to ms
