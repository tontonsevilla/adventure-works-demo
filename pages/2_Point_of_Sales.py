import streamlit as st
import pandas as pd

from azure import identity
from pandas import DataFrame

# Custom
import shared.repository as repo
import shared.utilities as ut
from shared.common import setTitle, purchases, customer

def main():
    setTitle()
    st.header("Point of Sales")
    setForm()

def setForm():
    with st.container(): #st.form("frmPointOfSales", clear_on_submit=True):
        dfCustomers = repo.getCustomers()
        CUSTOMERS = dict(dfCustomers.set_index("CustomerID")["CompanyName"])
        customerId = st.selectbox("Customer", options=list(CUSTOMERS.keys()), format_func=lambda x: CUSTOMERS[x])

        dfAddress = repo.getAddress(customerId)
        ADDRESSES = dict(dfAddress.set_index("AddressID")["FullAddress"])
        addressId = st.selectbox("Customer Address", options=list(ADDRESSES.keys()), format_func=lambda x: ADDRESSES[x])

        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            dfProducts = repo.getAllProducts()
            PRODUCTS = dict(dfProducts.set_index("ProductNumber")["Name"])
            productNumber = st.selectbox("Product", options=list(PRODUCTS.keys()), format_func=lambda x: PRODUCTS[x])
            
        with col2:
            quantity = st.number_input("Quantity", step=1, min_value=1, max_value=5)

        btnCol1, btnCol2, btnCol3 = st.columns([0.7, 0.1, 0.1])

        with btnCol2:
            btnReset = st.button("Reset")

        with btnCol3:
            btnAdd = st.button("Add")

    if btnAdd:
        global customer

        if customer.id == None:
            customer.id = customerId
        elif customer.id != customerId:
            customerId = customer.id
            st.warning("Not allowed to select other customer once transaction started. Please select Reset to select new customer.")
            return

        if productNumber == "":
            st.warning("Please provide a Product Number.")
            return

        productRaw = repo.getProduct(productNumber)

        if productRaw == None:
            st.warning("Product not found.")
        else:
            product = {"ProductNumber":productNumber, "quantity": quantity, "productId": productRaw.ProductID}

            mergePurchasesAny(product)

            st.data_editor(purchases)
            st.button("Confirm Purchase", on_click=savePurchases)

    if btnReset:
        customer.reset()
        purchases.clear()

def savePurchases():
    global purchases
    global customer

    purchasesXmlStr = ut.getXmlString(purchases)
    repo.saveSalesTransaction(purchasesXmlStr, customer)

    customer.reset()
    purchases.clear()

def mergePurchasesAny(newProduct):
    global purchases
    
    appendProduct = True

    for product in purchases:
        if product["ProductNumber"] == newProduct["ProductNumber"]:
            product["Quantity"] = product["Quantity"] + newProduct["Quantity"]
            appendProduct = False
            break

    if appendProduct:
        purchases.append(newProduct)

if __name__ == "__main__":
    main()
