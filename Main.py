import streamlit as st
from PIL import Image
import os
from db import Database


BASE_DIR = os.path.join(os.path.dirname(__file__))

try:
    db = Database().connection
except:
    st.error("Error connecting to DB")


if __name__=="__main__":
    st.markdown("<h1 style='text-align: center; color: black;'>Hive Query Dashboard</h1>", unsafe_allow_html=True)
