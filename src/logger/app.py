import streamlit as st
from data_handling import save_sneaker_data
from sneaker_inventory_log import Sneaker

st.title("Sneaker Logger")

with st.form("log_form"):
    purchase_date = st.text_input("Purchase Date")
    retailer = st.text_input("Retailer")
    release_date = st.text_input("Release Date")
    size = st.text_input("Size")
    brand = st.text_input("Brand")
    model = st.text_input("Model")
    colorway = st.text_input("Colorway")
    sku = st.text_input("SKU")
    retail_price = st.number_input("Retail Price")
    resale_price = st.number_input("Resale Price")
    quantity = st.number_input("Quantity", min_value=1, step=1)

    if st.form_submit_button("Log Sneaker"):
        sneaker = Sneaker(
            purchase_date, retailer, release_date, size, brand,
            model, colorway, sku, retail_price, resale_price, quantity
        )
        save_sneaker_data(sneaker)
        st.success("Logged successfully!")
