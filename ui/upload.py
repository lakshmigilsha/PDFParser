import requests
import streamlit as st
st.set_page_config(
    page_title="Hello!Upload PDF",
    page_icon="👋",
)
st.markdown("""
    :rainbow[Bank Statement Extractor]""")

uploaded_file = st.file_uploader(label="Upload PDF",type="pdf")

if uploaded_file is not None:
    upload_response = requests.post(
        "http://127.0.0.1:8000/uploadpdf/",
        files={
            "file": (
                uploaded_file.name,
                uploaded_file,
                "application/pdf"
            )
        }
    )
    st.write(upload_response.json()["message"])

    st.switch_page("pages/files.py")