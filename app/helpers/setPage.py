import streamlit as st
import os


def set_up_page():
    og_dir = os.getcwd()
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))  # Get the absolute path of the parent directory
    logo_path = os.path.join(parent_dir, 'assets', 'hammy_gifs', 'hammy-logo.gif')  # Construct the full path to the image
    icon_path = os.path.join(parent_dir, 'assets', 'hammy_gifs', 'hammy-still.png')  # Construct the full path to the image
    st.set_page_config(
        page_title="HammyFit",
        page_icon= icon_path,
        layout='centered',
        initial_sidebar_state='expanded',
        menu_items={
            'About': "# This is a header. This is an *extremely* cool app!"
        }
    )
    st.logo(logo_path)
    st.html("""
  <style>
    [alt=Logo] {
      height: 6rem;
    }
  </style>
        """)
    
