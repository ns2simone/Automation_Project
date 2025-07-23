import pandas as pd

def compare_products(sap_file, ns2_file):
    # --- Load both SAP sheets ---
    sap_classic = pd.read_excel(sap_file, header=1, sheet_name="Classic SAP Solutions")
    sap_cloud = pd.read_excel(sap_file, header=1, sheet_name="S4 & Native HANA Solutions")

    # Combine both SAP sheets
    sap = pd.concat([sap_classic, sap_cloud], ignore_index=True)
    sap.columns = sap.columns.str.strip()

    # Load NS2 sheet
    ns2 = pd.read_excel(ns2_file, sheet_name="Availability Matrix Excel")
    ns2.columns = ns2.columns.str.strip()

    # --- Filter for "private" and drop duplicates ---
    sap = sap[sap['Price List Item'].str.contains("priv", case=False, na=False)]
    sap = sap.drop_duplicates(subset="Material")

    ns2 = ns2[ns2['SKU Description'].str.contains("priv", case=False, na=False)]
    ns2 = ns2.drop_duplicates(subset="Product ID")

    # --- Normalize IDs as strings and remove ".0" ---
    sap["Material"] = sap["Material"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True)
    ns2["Product ID"] = ns2["Product ID"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True)

    sap["Material"] = sap["Material"].str.upper()
    ns2["Product ID"] = ns2["Product ID"].str.upper()

    # --- Add/remove logic ---
    to_add = sap[~sap["Material"].isin(ns2["Product ID"])].copy()
    to_add["Product ID"] = to_add["Material"]
    to_add["SKU Description"] = to_add["Price List Item"]
    to_add["Status"] = "ADD"

    to_remove = ns2[~ns2["Product ID"].isin(sap["Material"])].copy()
    to_remove["Status"] = "REMOVE"

    to_add = to_add[["Product ID", "SKU Description", "Status"]]
    to_remove = to_remove[["Product ID", "SKU Description", "Status"]]

    # --- Combine and return ---
    result = pd.concat([to_add, to_remove], ignore_index=True)
    return result
