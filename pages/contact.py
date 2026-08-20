import streamlit as st

st.set_page_config(
    page_title="تواصل معنا — الطالب الصامد",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from contact_page import render_contact_page

render_contact_page()
