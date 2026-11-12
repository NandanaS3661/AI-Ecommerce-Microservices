import streamlit as st, requests
API="http://api-gateway:8000"
st.set_page_config(page_title="AI Shop",page_icon="🛍️",layout="wide")
st.title("AI-Powered E-Commerce")
st.caption("FastAPI microservices • MySQL • MongoDB • Machine Learning")
products,orders,assistant,docs=st.tabs(["Products","Orders & recommendations","AI assistant","Knowledge documents"])
with products:
    query=st.text_input("Search catalogue")
    if st.button("Search products"): st.dataframe(requests.get(API+"/products",params={"q":query}).json(),use_container_width=True)
    with st.form("add-product"):
        name=st.text_input("Product name"); category=st.text_input("Category")
        description=st.text_area("Description"); price=st.number_input("Price",min_value=1.0)
        stock=st.number_input("Stock",min_value=0,step=1); submit=st.form_submit_button("Add product")
        if submit: st.json(requests.post(API+"/products",json={"name":name,"category":category,"description":description,"price":price,"stock":stock}).json())
with orders:
    with st.form("new-order"):
        uid=st.number_input("User ID",min_value=1,step=1); pid=st.number_input("Product ID",min_value=1,step=1)
        qty=st.number_input("Quantity",min_value=1,step=1); submit=st.form_submit_button("Place order")
        if submit: st.json(requests.post(API+"/orders",json={"user_id":uid,"product_id":pid,"quantity":qty}).json())
    rid=st.number_input("Product ID for recommendations",min_value=1,step=1)
    if st.button("Get recommendations"): st.json(requests.post(API+"/recommendations/recommend",json={"product_id":rid}).json())
with assistant:
    user=st.text_input("User ID",value="guest"); question=st.text_input("Ask the assistant")
    if st.button("Ask"): st.json(requests.post(API+"/ai/chat",json={"user_id":user,"message":question}).json())
with docs:
    title=st.text_input("Document title"); content=st.text_area("Document text")
    if st.button("Upload document"): st.json(requests.post(API+"/ai/documents",json={"title":title,"content":content}).json())
