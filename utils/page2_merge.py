import pandas as pd

def merge_spreadsheets(stack_file, cae_file, ns2_file, stack_sheet_name):
    # Read Software Stack sheet from specified sheet name
    stack_df = pd.read_excel(stack_file, header=1, sheet_name=stack_sheet_name)
    stack_df.columns = stack_df.columns.str.strip()

    # Fill down the SW Stack descriptions
    stack_df["SW Stack"] = stack_df["SW Stack"].ffill()
    stack_df = stack_df.rename(columns={"SKU#": "Product ID"})

    # Normalize Product ID
    stack_df["Product ID"] = (
        stack_df["Product ID"]
        .astype(str).str.strip()
        .str.replace(r"\.0$", "", regex=True)
        .str.upper()
    )

    # Load CAE file
    cae_df = pd.read_excel(cae_file, header=19, sheet_name="CAE Unofficial PAM")
    cae_df.columns = cae_df.columns.str.strip()
    cae_df["SKU"] = (
        cae_df["SKU"]
        .astype(str).str.strip()
        .str.replace(r"\.0$", "", regex=True)
        .str.upper()
    )
    cae_selected = cae_df[["SKU", "Package Type", "Deployment Type", "Notes", "On The Current PL"]]

    # Load NS2 file
    ns2_df = pd.read_excel(ns2_file, sheet_name="Availability Matrix Excel")
    ns2_df.columns = ns2_df.columns.str.strip()
    ns2_df["Product ID"] = (
        ns2_df["Product ID"]
        .astype(str).str.strip()
        .str.replace(r"\.0$", "", regex=True)
        .str.upper()
    )

    # Merge files
    merged = ns2_df.merge(cae_selected, left_on="Product ID", right_on="SKU", how="left")
    merged = merged.merge(stack_df, on="Product ID", how="left")
    merged = merged.drop(columns=["SKU"])

    return merged
