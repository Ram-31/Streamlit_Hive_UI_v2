import streamlit as st
st.title("Delete Queries")
from Main import db
import os

legacy = db.lgetall('Queries') if db.lgetall('Queries') is not False else []


with st.form("delete_form"):
    selected = st.selectbox("Select a query to delete",legacy,index=0)
    submitted = st.form_submit_button("Delete")

if submitted:
    data = db.get(selected)
    if data is not None:
        query_path = data['query_path']
    if os.path.isfile(query_path):
        os.remove(query_path)
    else:
        st.warning("Error in file removal")
    try:
        db.rem(selected)
        d_pos= legacy.index(selected)
        db.lpop('Queries',d_pos)
        db.dump()
        st.info("Deleted")
    except:
        st.error("Error in delete method")