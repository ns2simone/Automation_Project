import pandas as pd

def compare_products(sap_file, ns2_file):
    # --- Sheet name checks ---
    expected_sheets_sap = ["Classic SAP Solutions", "S4 & Native HANA Solutions"]
    expected_sheet_ns2 = "Availability Matrix Excel"
    
    sap_sheets = pd.ExcelFile(sap_file).sheet_names
    ns2_sheets = pd.ExcelFile(ns2_file).sheet_names

    for sheet in expected_sheets_sap:
        assert sheet in sap_sheets, f"Incorrect sheet name or missing sheet '{sheet}' in SAP file. Available sheets: {sap_sheets}"

    assert expected_sheet_ns2 in ns2_sheets, f"Incorrect sheet name or missing sheet '{expected_sheet_ns2}' in NS2 file. Available sheets: {ns2_sheets}"

    # --- Load both SAP sheets (header on row 2, which is index 1) ---
    try:
        sap_classic = pd.read_excel(sap_file, header=1, sheet_name="Classic SAP Solutions")
        sap_cloud = pd.read_excel(sap_file, header=1, sheet_name="S4 & Native HANA Solutions")
    except Exception as e:
        raise ValueError(f"Failed to read SAP sheets. Make sure the header starts on row 2.\nDetails: {e}")
    
    # Combine SAP sheets
    sap = pd.concat([sap_classic, sap_cloud], ignore_index=True)
    sap.columns = sap.columns.str.strip()

    # --- Load NS2 sheet ---
    try:
        ns2 = pd.read_excel(ns2_file, sheet_name="Availability Matrix Excel")
    except Exception as e:
        raise ValueError(f"Failed to read NS2 sheet. Ensure the sheet name and format are correct.\nDetails: {e}")

    ns2.columns = ns2.columns.str.strip()

    # --- Required column checks ---
    required_sap_cols = {"Material", "Price List Item"}
    required_ns2_cols = {"Product ID", "SKU Description"}

    assert required_sap_cols.issubset(sap.columns), \
        f"SAP sheet is missing required columns: {required_sap_cols - set(sap.columns)}"

    assert required_ns2_cols.issubset(ns2.columns), \
        f"NS2 sheet is missing required columns: {required_ns2_cols - set(ns2.columns)}"

    # --- Filter for 'priv' in description ---
    sap = sap[sap['Price List Item'].str.contains("priv", case=False, na=False)]
    ns2 = ns2[ns2['SKU Description'].str.contains("priv", case=False, na=False)]

    # --- Drop duplicates ---
    sap = sap.drop_duplicates(subset="Material")
    ns2 = ns2.drop_duplicates(subset="Product ID")

    # --- Normalize IDs and descriptions ---
    sap["Material"] = sap["Material"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True).str.upper()
    ns2["Product ID"] = ns2["Product ID"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True).str.upper()

    sap["Price List Item"] = sap["Price List Item"].astype(str).str.strip()
    ns2["SKU Description"] = ns2["SKU Description"].astype(str).str.strip()

    # --- ADD logic ---
    to_add = sap[~sap["Material"].isin(ns2["Product ID"])].copy()
    to_add["Product ID"] = to_add["Material"]
    to_add["SKU Description"] = to_add["Price List Item"]
    to_add["Status"] = "ADD"

    # --- REMOVE logic ---
    to_remove = ns2[~ns2["Product ID"].isin(sap["Material"])].copy()
    to_remove["Status"] = "REMOVE"

    # --- UPDATE logic ---
    sap_common = sap[sap["Material"].isin(ns2["Product ID"])]
    ns2_common = ns2[ns2["Product ID"].isin(sap["Material"])]

    merged = pd.merge(
        sap_common[["Material", "Price List Item"]],
        ns2_common[["Product ID", "SKU Description"]],
        left_on="Material", right_on="Product ID",
        how="inner"
    )

    merged = merged.drop(columns=["Product ID"])

    updates = merged[
        merged["Price List Item"].str.lower() != merged["SKU Description"].str.lower()
    ].copy()

    updates["Product ID"] = updates["Material"]
    updates["SAP Description"] = updates["Price List Item"]
    updates["NS2 Description"] = updates["SKU Description"]
    updates["Status"] = "UPDATE"
    updates = updates[["Product ID", "SAP Description", "NS2 Description", "Status"]]

    # --- Format ADD and REMOVE to match UPDATE structure ---
    to_add["SAP Description"] = ""
    to_add["NS2 Description"] = to_add["SKU Description"]
    to_add = to_add[["Product ID", "SAP Description", "NS2 Description", "Status"]]

    to_remove["SAP Description"] = ""
    to_remove["NS2 Description"] = to_remove["SKU Description"]
    to_remove = to_remove[["Product ID", "SAP Description", "NS2 Description", "Status"]]

    # --- Combine and return ---
    result = pd.concat([to_add, to_remove, updates], ignore_index=True)
    return result
