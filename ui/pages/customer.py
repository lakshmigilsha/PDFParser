import requests
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CustomerDetails",
    page_icon="👤",
)
st.header("Customer Details")
file_id = st.session_state.file_id

customer_response=requests.get(
    f"http://127.0.0.1:8000/uploadpdf/uploaded_pdf_list/{file_id}/CustomerDetails/"
)

df = pd.DataFrame(customer_response.json())
st.dataframe(df)