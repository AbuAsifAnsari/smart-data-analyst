# utils/dashboard.py
import pandas as pd

def auto_detect_kpi_columns(df: pd.DataFrame) -> dict:
    """
    Auto-detect important columns for KPI cards.
    Returns dict: { "revenue": col, "quantity": col, "category": col, "date": col }
    """
    from utils.ollama_chat import find_best_column, detect_date_column

    all_cols = list(df.columns)
    return {
        "revenue":  find_best_column("revenue",  all_cols),
        "quantity": find_best_column("quantity", all_cols),
        "category": find_best_column("category", all_cols),
        "product":  find_best_column("product",  all_cols),
        "date":     detect_date_column(df),
    }


def compute_kpis(df: pd.DataFrame, kpi_cols: dict) -> dict:
    """Compute KPI values from auto-detected columns."""
    kpis = {}

    rev_col = kpi_cols.get("revenue")
    if rev_col and pd.api.types.is_numeric_dtype(df[rev_col]):
        kpis["Total Revenue"] = f"₹{df[rev_col].sum():,.0f}"
        kpis["Avg Order Value"] = f"₹{df[rev_col].mean():,.0f}"

    qty_col = kpi_cols.get("quantity")
    if qty_col and pd.api.types.is_numeric_dtype(df[qty_col]):
        kpis["Total Orders"] = f"{df[qty_col].sum():,.0f}"

    prod_col = kpi_cols.get("product") or kpi_cols.get("category")
    if prod_col and rev_col:
        try:
            top = df.groupby(prod_col)[rev_col].sum().idxmax()
            kpis["Top Product"] = str(top)
        except:
            pass

    kpis["Total Rows"] = f"{len(df):,}"
    return kpis