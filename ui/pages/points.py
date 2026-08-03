import requests
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="RewardPoints",
    page_icon="⭐",
)
st.header("Reward Points")
file_id = st.session_state.file_id

points_response=requests.get(
    f"http://127.0.0.1:8000/uploadpdf/uploaded_pdf_list/{file_id}/PointsDetails/"
)

df = pd.DataFrame(points_response.json())
st.dataframe(df)