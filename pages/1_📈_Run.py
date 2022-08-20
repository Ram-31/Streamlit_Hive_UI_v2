from typing import List
import streamlit as st
from Main import db
from dataclasses import dataclass
from collections import defaultdict


st.set_page_config(layout='wide')

queries  = db.get('Queries')

col1, col2  = st.columns(2)

with col1:
    selected_query= st.selectbox("Select a query to run : ",options=queries)
if selected_query is not None:
    with col2:
        data = db.get(selected_query)
        query_path = data['query_path']
        st.write(f"Selected : {selected_query}")
        check_run = st.checkbox("Load Query")


@dataclass
class Filter:
    filters_ : list

    def date_(self,name):
        return st.date_input(f'Select {name}',key=name)
    
    def text_(self,name):
        return st.text_input(f"Select {name}",key=name)

    def int_(self,name):
        return st.number_input(f"Select num {name}",key=name,value=0)

    def float_(self,name):
        return st.number_input(f"select {name}",step=1.,format="%f",key=name)




def handle_filters(filters,col4,col5,col6):
    tmp = defaultdict(list)
    for item in filters:
        tmp[item['type']].append([item['value']])
    
    parsed_list = [{'type':k, 'data':v} for k,v in tmp.items()]
    f_=Filter(filters_=filters)
    selected_filters = []
    for _ in parsed_list:
        if _['type']=='date':
            if len(_['data'])>1:
                for i in _['data']:
                    with col4:
                        s = f_.date_(i)
                        s = s.strftime("%Y-%m-%d")
                        selected_filters.append({"filter":i,"value":s})
            else:
                with col4:
                    s = s.strftime("%Y-%m-%d")
                    s = f_.date_(_['data'][0])
                    selected_filters.append({"filter": _['data'][0],"value":s })
        elif _['type']=='varchar':
            if len(_['data'])>1:
                for i in _['data']:
                    with col5:
                        s= f_.text_(i)
                        selected_filters.append({"filter":i,"value":s})
            else:
                with col5:
                    s= f_.text_(_['data'][0])
                    selected_filters.append({"filter":_['data'][0],"value":s})
        elif _['type']=='int':
            if len(_['data'])>1:
                for i in _['data']:
                    with col6:
                        s= f_.int_(i)
                        selected_filters.append({"filter":i,"value":s})
            else:
                with col6:
                    s= f_.int_(_['data'][0])
                    selected_filters.append({"filter":_['data'][0],"value":s})
        elif _['type']=='float':
            if len(_['data'])>1:
                for i in _['data']:
                    with col4:
                        s= f_.float_(i)
                        selected_filters.append({"filter":i,"value":s})
            else:
                with col4:
                    s= f_.float_(_['data'][0])
                    selected_filters.append({"filter":_['data'][0],"value":s})
        else:
            if len(_['data'])>1:
                for i in _['data']:
                    with col5:
                        s= f_.text_(i)
                        selected_filters.append({"filter":i,"value":s})
            else:
                with col5:
                    s= f_.text_(_['data'][0])
                    selected_filters.append({"filter":_['data'][0],"value": s})


    return selected_filters

def join_tuple_string(strings_tuple) -> str:
   return '='.join(strings_tuple)

def modify_query(query,filters):   
    fil_ = [i['filter'][0]  for i in filters]
    val_ = [str(i['value'])  for i in filters]
    data = { 
        "query":query,
        "filters":filters,
        "fil":fil_,
        "val":val_
        }
    st.write(data)
    #querying part to be implemented
    pass
if selected_query is not None:
    if check_run:
        with open(query_path,'r') as file:
            query = file.read()
        filters = data['query_filters']
        col4,col5,col6 = st.columns(3)
        s_filters = handle_filters(filters,col4,col5,col6)
        modify_query(query,s_filters)