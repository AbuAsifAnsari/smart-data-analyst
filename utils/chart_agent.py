import logging
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

logger = logging.getLogger(__name__)

# ─── Dark theme color palette ─────────────────────────────────────────────────
DARK_BG    = "#07071A"
GRID_COLOR = "rgba(124,58,237,0.08)"
TEXT_COLOR = "#94A3B8"
TITLE_COLOR = "#E2E8F0"

PALETTE = [
    "#A78BFA",  # violet
    "#67E8F9",  # cyan
    "#6EE7B7",  # emerald
    "#FCD34D",  # amber
    "#60A5FA",  # blue
    "#F472B6",  # pink
    "#2DD4BF",  # teal
    "#FB923C",  # orange
]

CONTINUOUS_SCALE = [
    [0.0,  "#1E1B4B"],
    [0.25, "#4C1D95"],
    [0.5,  "#7C3AED"],
    [0.75, "#A78BFA"],
    [1.0,  "#DDD6FE"],
]

PIE_COLORS = ["#A78BFA", "#67E8F9", "#6EE7B7", "#FCD34D", "#60A5FA", "#F472B6", "#2DD4BF", "#FB923C"]


# ─── Safe import of detect_date_column ───────────────────────────────────────
try:
    from utils.ollama_chat import detect_date_column as _detect_date_col
except ImportError:
    logger.warning("utils.ollama_chat not found — date detection disabled")
    _detect_date_col = None


def detect_date_column(df: pd.DataFrame):
    if _detect_date_col is not None:
        return _detect_date_col(df)
    # Fallback: find first datetime-like column
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            return col
        if df[col].dtype == object:
            sample = df[col].dropna().head(5)
            try:
                pd.to_datetime(sample)
                return col
            except Exception:
                continue
    return None


# ─── cols helper ─────────────────────────────────────────────────────────────
def _get(cols, key, fallback=None):
    if isinstance(cols, dict):
        return cols.get(key, fallback)
    if isinstance(cols, list):
        if key == "primary":
            return cols[0] if len(cols) > 0 else fallback
        if key == "secondary":
            return cols[1] if len(cols) > 1 else fallback
    return fallback


# ─── Chart type auto-selector ────────────────────────────────────────────────
def auto_select_chart(intent: str, df: pd.DataFrame, cols) -> str:
    primary   = _get(cols, "primary")
    secondary = _get(cols, "secondary")

    if intent == "trend":
        return "line"
    if intent == "correlation":
        if primary and secondary:
            p_num = pd.api.types.is_numeric_dtype(df[primary]) if primary in df.columns else False
            s_num = pd.api.types.is_numeric_dtype(df[secondary]) if secondary in df.columns else False
            if p_num and s_num:
                return "scatter"
    if intent in ("ranking", "comparison"):
        return "bar"
    if intent == "filter":
        return "histogram" if df.select_dtypes(include="number").shape[1] > 0 else "bar"
    if intent == "aggregation":
        if primary and not secondary and df.select_dtypes(include="object").shape[1] > 0:
            return "pie"
        return "bar"
    return "bar"


# ─── Column keyword maps ─────────────────────────────────────────────────────
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


def _match_cols(q: str, col_list: list, keyword_map: list) -> list:
    matched = []
    for col in col_list:
        if col.lower() in q:
            matched.append(col)
    for col in col_list:
        if col in matched:
            continue
        for _key, words in keyword_map:
            if any(w in col.lower() for w in words) and any(w in q for w in words):
                matched.append(col)
                break
    return matched


def _is_id_col(col: str) -> bool:
    return any(kw in col.lower() for kw in _ID_KEYWORDS)


# ─── Main chart generator ────────────────────────────────────────────────────
def generate_chart(question: str, df: pd.DataFrame, intent: str, cols):
    if df is None or df.empty:
        return None

    primary      = _get(cols, "primary")
    secondary    = _get(cols, "secondary")
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols     = df.select_dtypes(include="object").columns.tolist()
    q            = question.lower()

    try:
        explicit_nums = [col for col in numeric_cols if col.lower() in q]
        explicit_cats = [col for col in cat_cols if col.lower() in q and not _is_id_col(col)]

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
            for i, num_col in enumerate(nums):
                fig.add_trace(go.Bar(
                    name         = num_col,
                    x            = grouped[cat],
                    y            = grouped[num_col],
                    marker_color = PALETTE[i % len(PALETTE)],
                    marker_line  = dict(width=0),
                    text         = grouped[num_col].apply(lambda v: f"{v:,.0f}"),
                    textposition = "outside",
                    textfont     = dict(color=TEXT_COLOR, size=12),
                    opacity      = 0.9,
                ))
            fig.update_layout(barmode="group", title=f"{cat} — {' vs '.join(nums)}")
            return _style(fig)

        # ── Pattern B: 2 cat + 1 numeric → grouped bar ───────────────────────
        strict_cats = [col for col in cat_cols if col.lower() in q and not _is_id_col(col)]
        if len(strict_cats) >= 2 and len(explicit_nums) >= 1:
            cat1    = strict_cats[0]
            cat2    = strict_cats[1]
            num     = explicit_nums[0]
            grouped = df.groupby([cat1, cat2])[num].sum().reset_index()
            fig     = px.bar(
                grouped, x=cat1, y=num, color=cat2,
                barmode="group",
                title=f"{num} by {cat1} × {cat2}",
                color_discrete_sequence=PALETTE
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
                    color_continuous_scale=CONTINUOUS_SCALE,
                    text_auto=".2s"
                )
                fig.update_traces(
                    textposition="outside",
                    textfont=dict(color=TEXT_COLOR, size=12),
                    marker_line_width=0,
                    opacity=0.9
                )
                return _style(fig)

            if n_unique <= 5:
                fig = px.pie(
                    grouped, names=cat, values=num,
                    title=f"{num} by {cat}",
                    color_discrete_sequence=PIE_COLORS,
                    hole=0.4,
                )
                fig.update_traces(
                    textfont=dict(size=13, color="#F1F5F9"),
                    marker=dict(line=dict(color=DARK_BG, width=2))
                )
            else:
                grouped = grouped.head(15)
                fig = px.bar(
                    grouped, x=cat, y=num,
                    title=f"{num} by {cat}",
                    color=num,
                    color_continuous_scale=CONTINUOUS_SCALE,
                    text_auto=".2s"
                )
                fig.update_traces(
                    textposition="outside",
                    textfont=dict(color=TEXT_COLOR, size=12),
                    marker_line_width=0,
                    opacity=0.9
                )
            return _style(fig)

    except Exception as e:
        logger.warning("Chart pattern matching failed: %s", e)

    # ── Intent-based fallback ─────────────────────────────────────────────────
    chart_type = auto_select_chart(intent, df, cols)

    try:
        # ── Line chart (trend) ────────────────────────────────────────────────
        if chart_type == "line":
            date_col = detect_date_column(df)
            num_col  = (
                primary if primary and primary in numeric_cols
                else (numeric_cols[0] if numeric_cols else None)
            )
            if date_col and num_col:
                plot_df            = df.copy()
                plot_df[date_col]  = pd.to_datetime(plot_df[date_col], errors="coerce")
                plot_df            = plot_df.dropna(subset=[date_col])
                plot_df["_period"] = plot_df[date_col].dt.to_period("M").astype(str)
                grouped            = plot_df.groupby("_period")[num_col].sum().reset_index()
                grouped.columns    = ["Period", num_col]
                fig = px.line(
                    grouped, x="Period", y=num_col,
                    title=f"{num_col} over time",
                    markers=True,
                    color_discrete_sequence=["#A78BFA"]
                )
                fig.update_traces(
                    line=dict(width=2.5),
                    marker=dict(size=7, color="#A78BFA", line=dict(color=DARK_BG, width=2))
                )
                fig.add_traces(go.Scatter(
                    x=grouped["Period"], y=grouped[num_col],
                    fill="tozeroy",
                    fillcolor="rgba(167,139,250,0.08)",
                    line=dict(width=0),
                    showlegend=False,
                    hoverinfo="skip"
                ))
                return _style(fig)

        # ── Scatter chart ─────────────────────────────────────────────────────
        if chart_type == "scatter":
            if (primary and secondary
                    and primary in numeric_cols
                    and secondary in numeric_cols):
                color_col = cat_cols[0] if cat_cols else None
                fig = px.scatter(
                    df, x=primary, y=secondary,
                    color=color_col,
                    title=f"{primary} vs {secondary}",
                    trendline="ols",
                    color_discrete_sequence=PALETTE
                )
                fig.update_traces(marker=dict(size=8, opacity=0.75, line=dict(width=0)))
                return _style(fig)

        # ── Histogram ─────────────────────────────────────────────────────────
        if chart_type == "histogram":
            num_col = (
                primary if primary and primary in numeric_cols
                else (numeric_cols[0] if numeric_cols else None)
            )
            if num_col:
                fig = px.histogram(
                    df, x=num_col,
                    title=f"Distribution of {num_col}",
                    color_discrete_sequence=["#67E8F9"],
                    nbins=30
                )
                fig.update_traces(marker_line_width=0, opacity=0.85)
                return _style(fig)

        # ── Pie chart ─────────────────────────────────────────────────────────
        if chart_type == "pie":
            cat_col = (
                primary if primary and primary in cat_cols
                else (cat_cols[0] if cat_cols else None)
            )
            num_col = (
                secondary if secondary and secondary in numeric_cols
                else (numeric_cols[0] if numeric_cols else None)
            )
            if cat_col and num_col:
                grouped = df.groupby(cat_col)[num_col].sum().reset_index()
                grouped = grouped.nlargest(8, num_col)
                fig = px.pie(
                    grouped, names=cat_col, values=num_col,
                    title=f"{num_col} by {cat_col}",
                    color_discrete_sequence=PIE_COLORS,
                    hole=0.4
                )
                fig.update_traces(
                    textfont=dict(size=13, color="#F1F5F9"),
                    marker=dict(line=dict(color=DARK_BG, width=2))
                )
                return _style(fig)

        # ── Bar chart (default) ───────────────────────────────────────────────
        cat_col = (
            primary if primary and primary in cat_cols
            else (cat_cols[0] if cat_cols else None)
        )
        num_col = (
            secondary if secondary and secondary in numeric_cols
            else primary   if primary   and primary   in numeric_cols
            else (numeric_cols[0] if numeric_cols else None)
        )

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
                color_continuous_scale=CONTINUOUS_SCALE,
                text_auto=".2s"
            )
            fig.update_traces(
                textposition="outside",
                textfont=dict(color=TEXT_COLOR, size=12),
                marker_line_width=0,
                opacity=0.9
            )
            return _style(fig)

    except Exception as e:
        logger.warning("Intent-based chart fallback failed: %s", e)

    return None


# ─── Dark Plotly theme ────────────────────────────────────────────────────────
def _style(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        paper_bgcolor = DARK_BG,
        plot_bgcolor  = DARK_BG,
        font          = dict(family="Inter, sans-serif", size=13, color=TEXT_COLOR),
        title_font    = dict(size=16, color=TITLE_COLOR, family="Inter, sans-serif"),
        margin        = dict(l=48, r=24, t=56, b=48),
        showlegend    = True,
        legend        = dict(
            font        = dict(color=TEXT_COLOR, size=12),
            bgcolor     = "rgba(7,7,26,0.8)",
            bordercolor = "rgba(124,58,237,0.2)",
            borderwidth = 1,
        ),
        xaxis = dict(
            showgrid   = False,
            zeroline   = False,
            tickfont   = dict(color=TEXT_COLOR, size=12),
            title_font = dict(color=TEXT_COLOR),
            linecolor  = "rgba(124,58,237,0.15)",
            showline   = True,
        ),
        yaxis = dict(
            showgrid   = True,
            gridcolor  = GRID_COLOR,
            zeroline   = False,
            tickfont   = dict(color=TEXT_COLOR, size=12),
            title_font = dict(color=TEXT_COLOR),
            linecolor  = "rgba(124,58,237,0.15)",
            showline   = False,
        ),
        coloraxis_showscale = False,
        hoverlabel = dict(
            bgcolor     = "#1E1B4B",
            font_size   = 13,
            font_color  = "#F1F5F9",
            bordercolor = "rgba(124,58,237,0.4)",
        ),
    )
    return fig