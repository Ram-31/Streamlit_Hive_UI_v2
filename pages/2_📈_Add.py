import streamlit as st
st.set_page_config(layout="wide")
import re
from Main import BASE_DIR,db


query_folder = BASE_DIR+"\\Queries"

st.title("Add Queries")

enums = db.get('filter_enums') if db.get('filter_enums') is not False else []

query_name = st.text_input('Query Name')
query = st.text_area("Paste the query",height=300,help="Enter query with filters enclosed with '{}' brackets . i.e. select {filter}")
filters= re.findall(r'\{.*?\}', query)
final_filter = list((filter_.strip("{}") for filter_ in filters))
final_filter = list(dict.fromkeys(final_filter))


chunks = [final_filter[i:i+3] for i in range(0,len(final_filter),3)]

st.caption("select filter types")
col1, col2,col3  = st.columns(3)


def get_types(chunks):
    types = []
    for val in chunks:
        for idx,value in enumerate(val):
            if idx==0:
                with col1:
                    t = st.selectbox(value,options=enums)
                    types.append({"value":value,"type":t})
            elif idx==1:
                with col2:
                    t =st.selectbox(value,options=enums)
                    types.append({"value":value,"type":t})
            else:
                with col3:
                    t = st.selectbox(value,options=enums)
                    types.append({"value":value,"type":t})

    return types


def process_query(query,query_folder,query_name):
    if query=='':
        st.error("Query cannot be null")
    elif query_name=='':
        st.error("Query name cannot be null")
    else:
        file_name = f"{query_folder}\{query_name}.sql"
        if db.get(query_name):
            st.error("Query already exists. Please use modify query tab to update the query")
            return None
        else:
            with open(file_name, 'w') as file:
                file.write(query)
                data = {
                    "query_name":query_name,
                    "query_path":file_name
                }
                return data
    return None
    
fiter_types = get_types(chunks)

if(len(final_filter)==len(fiter_types)):   
    save = st.button("Save")
    if save:
        query_data = process_query(query,query_folder,query_name)
        if query_data is None:
            st.error("Error in writing the query")
        else:
            final = {

                "query_path": query_data['query_path'],
                "query_filters" : fiter_types
            }
            db.set(query_data['query_name'],final)
            if query_data['query_name'] not in db.lgetall('Queries'):
                db.ladd('Queries',query_data['query_name'])
            db.dump()
            st.success("Saved Successfully")
        
        

else:
    st.error("filter and filter type doesn't match")
