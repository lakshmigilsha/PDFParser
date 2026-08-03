import requests
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AdditionalInfo",
    page_icon="🔎",
)
st.header("Other Information")
file_id = st.session_state.file_id

other_response=requests.get(
    f"http://127.0.0.1:8000/uploadpdf/uploaded_pdf_list/{file_id}/OtherDetails/"
)

df = pd.DataFrame(other_response.json())
st.dataframe(df)