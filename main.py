import streamlit as st
import webfunctions as web


if __name__ == '__main__':

    web.show_background()

    st.title("MM.C.P.E.")
    st.write("The streamlit MatterMost Channel Post Exporter ;-)")

    channel_id, channel_name = web.channel_name_dropdown()  # create the dropdown selection with channel names

    # Create a clickable button
    if st.button('Export'):
        st.write('Button clicked, channel choice was ' + channel_name + " with id " + channel_id)

        web.export_data(channel_id, channel_name)
