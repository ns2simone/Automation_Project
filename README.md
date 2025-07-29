# NS2 Pricing Tool 🧾💻

This Streamlit-based web application streamlines the process of comparing the SAP Pricing List with the NS2 Availability Matrix and merging CAE Unofficial PAM, NS2 Availability Matrix, and Software Stack data. It's designed to assist NS2 pricing teams in identifying product additions, removals, and updates as well as consolidating disparate datasets into one unified view.

---

## 🚀 Features

### 📄 Page 1: Compare Pricing Files
- **Inputs:** SAP Pricing Plan (`.xlsx`) and NS2 Cloud Material Code (`.xlsx`)
- **Output:** CSV file highlighting:
  - Products to **ADD** (exist in SAP Pricing List but not in NS2 Availability Matrix)
  - Products to **REMOVE** (exist in NS2 Availability Matrix but not SAP Pricing List)
  - Products to **UPDATE** (exist in both, but have differing descriptions)
- **Case-insensitive matching** and **".0" suffix cleanup** for Product IDs.
- Automatically filters rows to only include those containing `"priv"` (case-insensitive) in the description fields.
- Ensures all Product IDs are treated as strings/text.

---

### 🔀 Page 2: Merge Data
- **Inputs:**
  - Software Stack file (`.xlsx`) – user is prompted for the changing sheet name
  - CAE Unofficial PAM file (`.xlsx` or `.xlsm`)
  - NS2 Cloud Material Code file (`.xlsx`)
- **Output:** Unified dataset including:
  - Product metadata from NS2
  - Matching entries from CAE (by SKU). Only includes columns: Package Type, Deployment Type, Notes, On The Current PL
  - Software Stack info with descriptions based on `SKU#`
- Automatically **normalizes product IDs**, trims whitespace, and propagates merged results for consistency.

---

## 🧰 How to Use

### 1. Launch the App
Run from terminal:

```bash
streamlit run app.py
