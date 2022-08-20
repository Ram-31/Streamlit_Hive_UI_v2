from email.policy import default
import streamlit as st
import re
import os
st.set_page_config(layout="wide")
from Main import db


if db is None:
    st.error("Error with DB connection")

st.title("Modify Queries")

legacy = db.lgetall('Queries') if db.lgetall('Queries') is not False else []
enums = db.get('filter_enums') if db.get('filter_enums') is not False else []


selected = st.selectbox("Select a query to modify",legacy,index=0)
run = st.checkbox('load')





def generate_filters(chunks,enums,filters):
    st.caption("Modify filter types")
    types = []
    col1, col2,col3  = st.columns(3)
    for val in chunks:
        for idx,value in enumerate(val):
            def_= list(filter(lambda x: value in x['value'], filters))
            def_ = [i['type'] for i in def_]
            try:
                in_ = enums.index(def_[0])
            except:
                in_ = enums.index('varchar')
            if idx==0:
                with col1:
                    t = st.selectbox(value,options=enums,index=in_)
                    types.append({"value":value,"type":t})
            elif idx==1:
                with col2:
                    t = st.selectbox(value,options=enums,index=in_)
                    types.append({"value":value,"type":t})
            else:
                with col3:
                    t = st.selectbox(value,options=enums,index=in_)
                    types.append({"value":value,"type":t})

    return types


def handle_filter(new,enums,filters):
    chunks = [new[i:i+3] for i in range(0,len(new),3)]
    types = generate_filters(chunks,enums,filters)
    return types


if run:
    data = db.get(selected)
    if data is not None:
        query_path = data['query_path']
        with open(query_path,'r') as query:
            query = query.read()
            modified_query = st.text_area(" ",query,height=300)
        filters = data['query_filters']
        new_filter= re.findall(r'\{.*?\}', modified_query)
        new_filter = list((filter_.strip("{}") for filter_ in new_filter))
        new_filter = list(dict.fromkeys(new_filter))
        final_filters = handle_filter(new_filter,enums,filters)
        save = st.button("Save")
        if save:
            try:
                data = {
                    "query_path" : query_path,
                    "query_filters" : final_filters
                }
                with open(query_path, 'w') as file:
                    file.write(modified_query)
                db.set(selected,data)
                db.dump()
                st.success("Modified Successfully")
            except:
                st.error("Failed to modify")
        
        
