import streamlit as st
from utils.page1_compare import compare_products
from utils.page2_merge import merge_spreadsheets

st.set_page_config(page_title="NS2 Pricing Tool", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Page 1: Compare Pricing Files", "Page 2: Merge Data"])

if page == "Page 1: Compare Pricing Files":
    st.title("SAP vs NS2 Product Comparison")

    sap_file = st.file_uploader("Upload SAP Pricing Plan", type=["xlsx"])
    ns2_file = st.file_uploader("Upload NS2 Cloud Material Code", type=["xlsx"])

    if sap_file and ns2_file:
        result_df = compare_products(sap_file, ns2_file)
        st.success("Comparison complete!")
        st.dataframe(result_df)

        st.download_button("Download Result",
                           result_df.to_csv(index=False),
                           file_name="product_comparison.csv")

elif page == "Page 2: Merge Data":
    st.title("Combine Software Stack, CAE, and NS2 Material Code")

    stack_file = st.file_uploader("Upload Software Stack File", type=["xlsx"])
    cae_file = st.file_uploader("Upload CAE File", type=["xlsx"])
    ns2_cloud_file = st.file_uploader("Upload NS2 Cloud Material Code", type=["xlsx"])

    if stack_file and cae_file and ns2_cloud_file:
        merged_df = merge_spreadsheets(stack_file, cae_file, ns2_cloud_file)
        st.success("Merge complete!")
        st.dataframe(merged_df)

        st.download_button("Download Merged File",
                           merged_df.to_csv(index=False),
                           file_name="merged_data.csv")
