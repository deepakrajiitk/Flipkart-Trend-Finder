from nis import cat
from operator import sub
import streamlit as st
import time
import json
import flipkart_grid as fp
import streamlit.components.v1 as components
import os

st.title("Turing Trends")
mode=st.sidebar.selectbox('Select Page',['Home','Find Trends'],index=0)

with open("./DataSet/Categories.json","r") as f:
    product_dict=json.load(f)

if mode=='Home':    
    st.subheader("Find All Trends In Real time...")
    st.image('./Images/trends_front.jpg')
else:
    category_list=["All"]+list(product_dict.keys())
    category=st.sidebar.selectbox("Pick a Category",category_list)
    
    if category!="All":
        subcat_list=["Select"]+["All"]+list(product_dict[category][1].keys())
        subcat=st.sidebar.selectbox("Pick a Sub-Category",subcat_list)
        st.subheader(f"Trending in {category.title()}")

        if (subcat=="All"):
            if st.sidebar.button("Re-New") or (not os.path.exists(f"./DataSet/{category}_data.json")):
                with st.spinner("wait for it..."):
                   fp.getAllTrendOfCategory(category,5)

            with open(f"./DataSet/{category}_data.json","r") as f:            
                res=json.load(f)

            for i,x in enumerate(res):
                if i%3==0:
                    cols=st.columns(3)

                cols[i%3].markdown(f"**{x['Name'].capitalize()}**")
                cols[i%3].write(f"Sub-Category : {x['Subcategory']}")
                cols[i%3].markdown(f"**#{i+1}**")
                cols[i%3].image(x['Image Url'][0])
                cols[i%3].write(f"Check out here : [link]({x['Flipkart Url']})")
        elif subcat!="Select":
            if st.sidebar.button("Re-New") or (not os.path.exists(f"./DataSet/{category}_{subcat}_data.json")):
                with st.spinner("wait for it..."):
                   fp.getTrendByCatAndSub(category,subcat,5)
            
            with open(f"./DataSet/{category}_{subcat}_data.json","r") as f:            
                res=json.load(f)
                
            for i,x in enumerate(res):
                if i%3==0:
                    cols=st.columns(3)

                cols[i%3].markdown(f"**{x['Name'].capitalize()}**")
                cols[i%3].markdown(f"**#{i+1}**")
                cols[i%3].image(x['Image Url'][0])
                cols[i%3].write(f"Check out here : [link]({x['Flipkart Url']})")
    elif category=="All":
        if st.sidebar.button("Re-New") or (not os.path.exists("./DataSet/all_categories.json")):
            fp.getAllTrend(5)

        with open("./DataSet/all_categories.json") as f:
            res=json.load(f)
        cats=res.keys()
        for x in cats:
            st.subheader(f"Trending in {x.capitalize()}")
            num_col=len(res[x])
            
            for i,y in enumerate(res[x]):
                if(i%3==0):
                    cols=st.columns(3)
                
                cols[i%3].markdown(f"**{y['Name'].capitalize()}**")
                cols[i%3].write(f"Sub-Category : {y['Subcategory']}")
                cols[i%3].markdown(f"**#{i+1}**")
                cols[i%3].image(y['Image Url'][0])
                cols[i%3].write(f"Check out here : [link]({y['Flipkart Url']})")
    
