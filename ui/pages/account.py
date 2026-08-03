import requests
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AccountDetails",
    page_icon="🏦",
)
st.header("Account Details")
file_id = st.session_state.file_id

account_response=requests.get(
    f"http://127.0.0.1:8000/uploadpdf/uploaded_pdf_list/{file_id}/AccountDetails/"
)

df = pd.DataFrame(account_response.json())
st.dataframe(df)