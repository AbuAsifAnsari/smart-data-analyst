# utils/chart_agent.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ─── cols helper — list bhi aaye ya dict, dono handle karo ───────────────────
def _get(cols, key, fallback=None):
    """
    cols list ho sakti hai (ask_gemma se) ya dict (dashboard se).
    key = "primary" | "secondary"
    """
    if isinstance(cols, dict):
        return cols.get(key, fallback)
    elif isinstance(cols, list):
        if key == "primary":
            return cols[0] if len(cols) > 0 else fallback
        elif key == "secondary":
            return cols[1] if len(cols) > 1 else fallback
    return fallback


# ─── Chart type auto-selector ─────────────────────────────────────────────────
def auto_select_chart(intent: str, df: pd.DataFrame, cols) -> str:
    primary   = _get(cols, "primary")
    secondary = _get(cols, "secondary")

    if intent == "trend":
        return "line"
    if intent == "correlation":
        if primary and secondary:
            if pd.api.types.is_numeric_dtype(df.get(primary, pd.Series())) and \
               pd.api.types.is_numeric_dtype(df.get(secondary, pd.Series())):
                return "scatter"
    if intent == "ranking":
        return "bar"
    if intent == "comparison":
        return "bar"
    if intent == "filter":
        num_cols = df.select_dtypes(include="number").columns.tolist()
        return "histogram" if num_cols else "bar"
    if intent == "aggregation":
        if primary and not secondary:
            cat_cols = df.select_dtypes(include="object").columns.tolist()
            if cat_cols:
                return "pie"
        return "bar"
    return "bar"


# ─── Column keyword maps ──────────────────────────────────────────────────────
_NUM_KW = [
    ("revenue",  ["revenue", "sales", "income", "amount", "value", "earning"]),
    ("quantity", ["quantity", "qty", "units", "volume"]),
    ("profit",   ["profit", "margin", "gain", "net"]),
    ("discount", ["discount"]),
    ("price",    ["price", "cost", "rate"]),
]
_CAT_KW = [
    ("product",  ["product", "item", "goods"]),
    ("category", ["category", "type", "segment"]),
    ("region",   ["region", "area", "zone", "location", "state"]),
    ("customer", ["customer", "client", "buyer"]),
    ("city",     ["city", "town"]),
]

_ID_KEYWORDS = ["id", "_id", "code", "no.", "number", "num",
                "invoice", "serial", "index", "key"]


def _match_cols(q, col_list, keyword_map):
    matched = []
    for col in col_list:
        if col.lower() in q:
            matched.append(col)
    for col in col_list:
        if col in matched:
            continue
        for key, words in keyword_map:
            if any(w in col.lower() for w in words) and \
               any(w in q for w in words):
                matched.append(col)
                break
    return matched


def _is_id_col(col: str) -> bool:
    return any(kw in col.lower() for kw in _ID_KEYWORDS)


# ─── Main chart generator ─────────────────────────────────────────────────────
def generate_chart(question: str, df: pd.DataFrame, intent: str, cols):
    if df is None or df.empty:
        return None

    # ── cols se primary/secondary nikalo (list ya dict dono support) ──────────
    primary      = _get(cols, "primary")
    secondary    = _get(cols, "secondary")
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols     = df.select_dtypes(include="object").columns.tolist()
    q            = question.lower()

    try:
        # ── Explicit column matches ───────────────────────────────────────────
        explicit_nums = [col for col in numeric_cols if col.lower() in q]
        explicit_cats = [col for col in cat_cols
                         if col.lower() in q and not _is_id_col(col)]

        if len(explicit_nums) < 2:
            for col in _match_cols(q, numeric_cols, _NUM_KW):
                if col not in explicit_nums:
                    explicit_nums.append(col)

        if len(explicit_cats) < 1:
            for col in _match_cols(q, cat_cols, _CAT_KW):
                if col not in explicit_cats and not _is_id_col(col):
                    explicit_cats.append(col)

        # ── Pattern A: 1 cat + 2 numeric → grouped bar ───────────────────────
        if len(explicit_cats) >= 1 and len(explicit_nums) >= 2:
            cat     = explicit_cats[0]
            nums    = explicit_nums[:3]
            grouped = df.groupby(cat)[nums].sum().reset_index()
            grouped = grouped.sort_values(nums[0], ascending=False).head(15)
            fig     = go.Figure()
            colors  = ["#7F77DD", "#1D9E75", "#EF9F27", "#D85A30"]
            for i, num_col in enumerate(nums):
                fig.add_trace(go.Bar(
                    name         = num_col,
                    x            = grouped[cat],
                    y            = grouped[num_col],
                    marker_color = colors[i % len(colors)],
                    text         = grouped[num_col].apply(lambda v: f"{v:,.0f}"),
                    textposition = "outside"
                ))
            fig.update_layout(barmode="group", title=f"{cat} — {' vs '.join(nums)}")
            return _style(fig)

        # ── Pattern B: 2 cat + 1 numeric → grouped bar ───────────────────────
        strict_cats = [col for col in cat_cols
                       if col.lower() in q and not _is_id_col(col)]
        if len(strict_cats) >= 2 and len(explicit_nums) >= 1:
            cat1    = strict_cats[0]
            cat2    = strict_cats[1]
            num     = explicit_nums[0]
            grouped = df.groupby([cat1, cat2])[num].sum().reset_index()
            fig     = px.bar(
                grouped, x=cat1, y=num, color=cat2,
                barmode="group",
                title=f"{num} by {cat1} × {cat2}",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            return _style(fig)

        # ── Pattern C: 1 cat + 1 numeric → pie / bar ─────────────────────────
        if len(explicit_cats) >= 1 and len(explicit_nums) >= 1:
            cat      = explicit_cats[0]
            num      = explicit_nums[0]
            n_unique = df[cat].nunique()
            grouped  = df.groupby(cat)[num].sum().reset_index()

            n         = next((int(w) for w in q.split() if w.isdigit()), None)
            ascending = any(w in q for w in ["bottom", "lowest", "worst", "least"])
            grouped   = grouped.sort_values(num, ascending=ascending)

            if n:
                grouped = grouped.head(n)
                fig = px.bar(
                    grouped, x=cat, y=num,
                    title=f"Top {n} {cat} by {num}",
                    color=num,
                    color_continuous_scale="Teal",
                    text_auto=".2s"
                )
                fig.update_traces(textposition="outside")
                return _style(fig)

            if n_unique <= 5:
                fig = px.pie(
                    grouped, names=cat, values=num,
                    title=f"{num} by {cat}",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
            else:
                grouped = grouped.head(15)
                fig = px.bar(
                    grouped, x=cat, y=num,
                    title=f"{num} by {cat}",
                    color=num,
                    color_continuous_scale="Teal",
                    text_auto=".2s"
                )
                fig.update_traces(textposition="outside")
            return _style(fig)

    except Exception:
        pass

    # ── Intent-based fallback (primary/secondary cols se) ─────────────────────
    chart_type = auto_select_chart(intent, df, cols)

    try:
        # ── Line chart (trend) ────────────────────────────────────────────────
        if chart_type == "line":
            from utils.ollama_chat import detect_date_column
            date_col = detect_date_column(df)
            num_col  = primary if primary and primary in numeric_cols else \
                       (numeric_cols[0] if numeric_cols else None)
            if date_col and num_col:
                plot_df              = df.copy()
                plot_df[date_col]    = pd.to_datetime(plot_df[date_col], errors="coerce")
                plot_df              = plot_df.dropna(subset=[date_col])
                plot_df["_period"]   = plot_df[date_col].dt.to_period("M").astype(str)
                grouped              = plot_df.groupby("_period")[num_col].sum().reset_index()
                grouped.columns      = ["Period", num_col]
                fig = px.line(
                    grouped, x="Period", y=num_col,
                    title=f"{num_col} over time",
                    markers=True,
                    color_discrete_sequence=["#7F77DD"]
                )
                return _style(fig)

        # ── Scatter chart (correlation) ───────────────────────────────────────
        if chart_type == "scatter":
            if primary and secondary and \
               primary in numeric_cols and secondary in numeric_cols:
                color_col = cat_cols[0] if cat_cols else None
                fig = px.scatter(
                    df, x=primary, y=secondary,
                    color=color_col,
                    title=f"{primary} vs {secondary}",
                    trendline="ols",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                return _style(fig)

        # ── Histogram ─────────────────────────────────────────────────────────
        if chart_type == "histogram":
            num_col = primary if primary and primary in numeric_cols else \
                      (numeric_cols[0] if numeric_cols else None)
            if num_col:
                fig = px.histogram(
                    df, x=num_col,
                    title=f"Distribution of {num_col}",
                    color_discrete_sequence=["#1D9E75"]
                )
                return _style(fig)

        # ── Pie chart ─────────────────────────────────────────────────────────
        if chart_type == "pie":
            cat_col = primary if primary and primary in cat_cols else \
                      (cat_cols[0] if cat_cols else None)
            num_col = secondary if secondary and secondary in numeric_cols else \
                      (numeric_cols[0] if numeric_cols else None)
            if cat_col and num_col:
                grouped = df.groupby(cat_col)[num_col].sum().reset_index()
                grouped = grouped.nlargest(8, num_col)
                fig = px.pie(
                    grouped, names=cat_col, values=num_col,
                    title=f"{num_col} by {cat_col}",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                return _style(fig)

        # ── Bar chart (default) ───────────────────────────────────────────────
        cat_col = primary if primary and primary in cat_cols else \
                  (cat_cols[0] if cat_cols else None)
        num_col = secondary if secondary and secondary in numeric_cols else \
                  primary   if primary   and primary   in numeric_cols else \
                  (numeric_cols[0] if numeric_cols else None)

        if cat_col and num_col and cat_col != num_col:
            ascending = any(w in q for w in ["bottom", "lowest", "worst", "least"])
            n         = next((int(w) for w in q.split() if w.isdigit()), None)
            grouped   = df.groupby(cat_col)[num_col].sum().reset_index()
            grouped   = grouped.sort_values(num_col, ascending=ascending)
            grouped   = grouped.head(n if n else 15)
            fig = px.bar(
                grouped, x=cat_col, y=num_col,
                title=f"{num_col} by {cat_col}",
                color=num_col,
                color_continuous_scale="Teal",
                text_auto=".2s"
            )
            fig.update_traces(textposition="outside")
            return _style(fig)

    except Exception:
        pass

    return None


# ─── Plotly theme helper ──────────────────────────────────────────────────────
def _style(fig):
    fig.update_layout(
        paper_bgcolor       = "rgba(0,0,0,0)",
        plot_bgcolor        = "rgba(0,0,0,0)",
        font                = dict(family="sans-serif", size=13),
        margin              = dict(l=40, r=20, t=50, b=40),
        title_font          = dict(size=15),
        showlegend          = True,
        xaxis               = dict(showgrid=False, zeroline=False),
        yaxis               = dict(
            showgrid  = True,
            gridcolor = "rgba(128,128,128,0.15)",
            zeroline  = False
        ),
        coloraxis_showscale = False,
    )
    return fig