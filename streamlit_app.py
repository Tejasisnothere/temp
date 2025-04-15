
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Pharma Deviation Detection")

st.title("Pharma Deviation Detection")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Data Preview:")
    st.dataframe(df)
