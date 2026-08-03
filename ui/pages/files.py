import requests
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="PDF list",
    page_icon="📋",
)
uploaded_pdf_response=requests.get(
    "http://127.0.0.1:8000/uploadpdf/uploaded_pdf_list/"
)
df = pd.DataFrame(uploaded_pdf_response.json())

event=st.dataframe(df,
             on_select="rerun",
            selection_mode="single-row",
            )
selected_row = event.selection.rows

category = st.selectbox(
        "Select extracted data category",
        ["Customer Details",
        "Transactions",
        "Account Details",
        "Reward Points",
        "Other Information"]
         )

if st.button("Open"):
    filtered_df = df.iloc[selected_row[0]]
    st.session_state.file_id=filtered_df["file_id"]  #API follows a key(field) based navigation

    if category == "Transactions":
        st.switch_page("pages/transactions.py")

    elif category == "Customer Details":
            st.switch_page("pages/customer.py")

    elif category == "Account Details":
        st.switch_page("pages/account.py")

    elif category == "Reward Points":
        st.switch_page("pages/points.py")

    elif category == "Other Information":
        st.switch_page("pages/other.py")

    