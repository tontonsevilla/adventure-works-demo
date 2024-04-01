import streamlit as st
import pandas as pd

from pandas import DataFrame

# Custom
from shared.common import setTitle  
import shared.repository as repo

source_df = DataFrame
editor_df = DataFrame

def main():
    setTitle()
    st.header("Product List")

    source_df = repo.getAllProducts()
    editor_df = st.data_editor(source_df, key = "product_edit", num_rows="dynamic", use_container_width=True, on_change=data_editor_on_change)

def data_editor_on_change():
    editor_key=st.session_state["product_edit"]

    target = pd.DataFrame(editor_key.get("edited_rows")).transpose().reset_index()
    modified_columns = [i for i in target.notna().columns if i != "index"]
    
    st.write(modified_columns)

if __name__ == "__main__":
    main()