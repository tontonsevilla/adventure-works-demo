import streamlit as st
from shared.customer import Person

purchases = []
customer = Person(None,None)

def setTitle():
    st.title("Adventure Works App")
