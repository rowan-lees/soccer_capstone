import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="⚽",
)

st.write("# Welcome to my Streamlit App! 👋")
st.sidebar.success("Select a option")

st.markdown(
    """
    This app does blah blah blah
    """
)