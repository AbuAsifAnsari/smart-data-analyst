import pandas as pd

def load_file(uploaded_file):
    filename = uploaded_file.name
    if filename.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif filename.endswith((".xlsx", ".xls")):
        df = pd.read_excel(uploaded_file)
    else:
        return None, "❌ Sirf CSV ya Excel file upload karein."
    return df, None

def get_data_summary(df):
    basic = f"""
DATASET OVERVIEW:
- Total Rows: {df.shape[0]}
- Total Columns: {df.shape[1]}
- Columns: {list(df.columns)}
"""
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    numeric_summary = "\nNUMERIC COLUMNS FULL STATS:\n"
    if numeric_cols:
        numeric_summary += df[numeric_cols].describe().to_string()
        numeric_summary += "\n\nCOLUMN TOTALS:\n"
        for col in numeric_cols:
            numeric_summary += f"- {col}: Total = {df[col].sum():.2f}, Avg = {df[col].mean():.2f}\n"

    cat_cols = df.select_dtypes(include='object').columns.tolist()
    cat_summary = "\nCATEGORICAL COLUMNS (value counts):\n"
    for col in cat_cols:
        cat_summary += f"\n{col} unique values ({df[col].nunique()} total):\n"
        cat_summary += df[col].value_counts().to_string() + "\n"

    group_summary = "\nGROUP-WISE AGGREGATIONS (actual computed):\n"
    for cat in cat_cols:
        for num in numeric_cols:
            grouped = df.groupby(cat)[num].sum().sort_values(ascending=False)
            group_summary += f"\n{num} by {cat}:\n{grouped.to_string()}\n"

    return basic + numeric_summary + cat_summary + group_summary