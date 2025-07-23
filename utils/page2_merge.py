import pandas as pd

def merge_spreadsheets(stack_file, cae_file, ns2_file):
    # Read from row 2 (index 1) for Software Stack
    stack_df = pd.read_excel(stack_file, header=1)

    # Read from row 20 (index 19) for CAE
    cae_df = pd.read_excel(cae_file, header=19)

    # NS2 starts from the top (row 1), so no change needed
    ns2_df = pd.read_excel(ns2_file)

    # Select and rename the columns to align with the merge keys
    cae_selected = cae_df[["SKU", "Package Type", "Deployment Type", "Notes", "On The Current PL"]]
    stack_selected = stack_df[["Product ID", "SW Stack"]]

    # Merge NS2 with CAE (SKU in CAE vs Product ID in NS2)
    merged = ns2_df.merge(cae_selected, left_on="Product ID", right_on="SKU", how="left")

    # Merge the result with Software Stack (Product ID matches)
    merged = merged.merge(stack_selected, on="Product ID", how="left")

    # Drop the now-redundant SKU column from CAE
    merged = merged.drop(columns=["SKU"])

    return merged
