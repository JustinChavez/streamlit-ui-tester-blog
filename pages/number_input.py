import streamlit as st

first_number = st.number_input("First Number", value=0)
second_number = st.number_input("Second Number", value=0)

if st.button("Add"):
    st.write(str(first_number + second_number))