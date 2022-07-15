import streamlit as st

subpage = st.selectbox("Subpage Navigator", ["First Page", "Second Page"])

st.write(f"Hello this is the {subpage}")

