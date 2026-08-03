import requests
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Transactions",
    page_icon="💳",
)
st.header("Transactions")
file_id = st.session_state.file_id

transaction_response=requests.get(
    f"http://127.0.0.1:8000/uploadpdf/uploaded_pdf_list/{file_id}/transactions/"
)

df = pd.DataFrame(transaction_response.json())
st.dataframe(df)
st.subheader("📈 Balance Analysis")

st.line_chart(
    df,
    x="date",
    y="balance"
)