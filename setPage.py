import streamlit as st
import os

def set_up_page():
    st.set_page_config(
        page_title="Hammy",
        page_icon="hammy_gifs/hammy-logo.gif",
        layout='centered',
        initial_sidebar_state='expanded',
        menu_items={
            'About': "# This is a header. This is an *extremely* cool app!"
        }
    )
    st.logo('hammy_gifs/hammy-logo.gif')
    st.html("""
  <style>
    [alt=Logo] {
      height: 6rem;
    }
  </style>
        """)
