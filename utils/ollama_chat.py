"""
ollama_chat.py — V7: Dual LLM Mode
Primary  : Gemini API (free tier)
Fallback : Ollama gemma3:1b (local)
"""

import os
import re
import pandas as pd

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

GEMINI_AVAILABLE = False
gemini_model     = None

def _init_gemini():
    global GEMINI_AVAILABLE, gemini_model
    try:
        import google.generativeai as genai
        api_key = None
        try:
            import streamlit as st
            api_key = st.secrets.get("GEMINI_API_KEY", None)
        except Exception:
            pass
        if not api_key:
            api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key or api_key == "your_actual_key_here":
            print("[V7] Gemini API key nahi mili — Ollama fallback use hoga.")
            return
        genai.configure(api_key=api_key)
        gemini_model     = genai.GenerativeModel("gemini-1.5-flash")
        GEMINI_AVAILABLE = True
        print("[V7] Gemini API ready ✓")
    except ImportError:
        print("[V7] google-generativeai nahi — pip install google-generativeai")
    except Exception as e:
        print(f"[V7] Gemini init error: {e}")

_init_gemini()

OLLAMA_AVAILABLE = False

def _check_ollama():
    global OLLAMA_AVAILABLE
    try:
        import requests
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        if r.status_code == 200:
            OLLAMA_AVAILABLE = True
            print("[V7] Ollama ready ✓")
    except Exception:
        print("[V7] Ollama nahi mila — sirf Gemini use hoga.")

_check_ollama()


# ══════════════════════════════════════════════════════════════
#  SMART INTENT DETECTION
# ══════════════════════════════════════════════════════════════

def detect_intent(question: str) -> str:
    """
    Priority-based intent detection.
    "top 5 product by revenue" → sort  (NOT max)
    "region wise revenue"      → group
    "total revenue"            → sum
    """
    q = question.lower().strip()

    # ── Priority 1: group patterns — "X wise Y", "Y by X", "group by" ────────
    group_patterns = [
        r"\bwise\b", r"\bgroup by\b", r"\bper\b", r"\beach\b",
        r"\bbreakdown\b", r"\bcategory wise\b", r"\bby category\b",
        r"\bby region\b", r"\bby product\b", r"\bby city\b",
        r"\bby segment\b", r"\bby month\b",
    ]
    if any(re.search(p, q) for p in group_patterns):
        return "group"

    # "X by Y" — "product by revenue", "revenue by region"
    # Sirf agar "top N" nahi hai pehle (woh sort hai)
    if " by " in q and not re.search(r"\btop\s+\d+\b", q):
        return "group"

    # ── Priority 2: sort — "top N", "bottom N", "top 5 X by Y" ──────────────
    if re.search(r"\btop\s+\d+\b", q) or re.search(r"\bbottom\s+\d+\b", q):
        return "sort"

    # ── Priority 3: trend ─────────────────────────────────────────────────────
    if any(k in q for k in ["trend", "over time", "monthly", "weekly", "yearly"]):
        return "trend"

    # ── Priority 4: specific operations ──────────────────────────────────────
    if any(k in q for k in ["how many", "count", "total rows", "number of"]):
        return "count"

    if any(k in q for k in ["average", "mean", "avg"]):
        return "mean"

    if any(k in q for k in ["total", "sum"]):
        return "sum"

    # "top" without number = max (e.g. "top product")
    if any(k in q for k in ["maximum", "max", "highest", "largest", "best", "top"]):
        return "max"

    if any(k in q for k in ["minimum", "min", "lowest", "smallest", "worst"]):
        return "min"

    if any(k in q for k in ["sort", "rank", "order"]):
        return "sort"

    if any(k in q for k in ["where", "filter", "which", "find"]):
        return "filter"

    if any(k in q for k in ["null", "missing", "nan", "empty", "blank"]):
        return "missing"

    if any(k in q for k in ["unique", "distinct", "different values"]):
        return "unique"

    if any(k in q for k in ["correlation", "relationship", "corr", "related"]):
        return "corr"

    if any(k in q for k in ["describe", "summary", "overview", "info",
                              "shape", "dtype", "column", "columns"]):
        return "summary"

    if any(k in q for k in ["chart", "plot", "graph", "visualize",
                              "bar", "line", "pie", "histogram"]):
        return "chart"

    return "general"


def detect_cols(question: str, df: pd.DataFrame) -> list:
    q_lower = question.lower()
    found   = [c for c in df.columns if c.lower() in q_lower]
    if not found:
        for c in df.columns:
            words = c.lower().replace("_", " ").split()
            if any(w in q_lower for w in words if len(w) > 3):
                found.append(c)
    return found


# ══════════════════════════════════════════════════════════════
#  COLUMN HELPERS
# ══════════════════════════════════════════════════════════════

def _numeric_cols(df):
    return df.select_dtypes(include="number").columns.tolist()

def _cat_cols(df):
    return df.select_dtypes(include="object").columns.tolist()

def _best_num_col(df, cols):
    for c in cols:
        if c in df.columns and pd.api.types.is_numeric_dtype(df[c]):
            return c
    num = _numeric_cols(df)
    return num[0] if num else None

def _best_cat_col(df, cols):
    for c in cols:
        if c in df.columns and not pd.api.types.is_numeric_dtype(df[c]):
            return c
    cat = _cat_cols(df)
    return cat[0] if cat else None

def _all_num_cols_in(df, cols):
    return [c for c in cols if c in df.columns
            and pd.api.types.is_numeric_dtype(df[c])]


# ══════════════════════════════════════════════════════════════
#  PYTHON-FIRST COMPUTE ENGINE
# ══════════════════════════════════════════════════════════════

def compute_answer(question: str, df: pd.DataFrame, intent: str, cols: list):
    try:
        q = question.lower()

        if intent == "summary":
            desc = df.describe(include="all").to_string()
            ans  = (f"Dataset mein {df.shape[0]:,} rows aur {df.shape[1]} columns hain.\n\n"
                    f"Columns: {', '.join(df.columns.tolist())}\n\nStats:\n{desc}")
            return ans, "df.describe(include='all')"

        if intent == "missing":
            miss = df.isnull().sum()
            miss = miss[miss > 0]
            if miss.empty:
                return "Dataset mein koi missing values nahi hain. ✓", "df.isnull().sum()"
            result = "\n".join([f"  {c}: {v} missing" for c, v in miss.items()])
            return f"Missing values:\n{result}", "df.isnull().sum()"

        if intent == "count":
            return f"Dataset mein total {len(df):,} rows hain.", "len(df)"

        if intent == "unique" and cols:
            c    = cols[0]
            uniq = df[c].nunique()
            vals = df[c].dropna().unique()[:10]
            return (f"'{c}' mein {uniq} unique values hain.\nSample: {list(vals)}",
                    f"df['{c}'].unique()")

        if intent in ("mean", "sum", "max", "min"):
            nc = _best_num_col(df, cols)
            if nc:
                op_map = {"mean": df[nc].mean, "sum": df[nc].sum,
                          "max": df[nc].max,   "min": df[nc].min}
                val = op_map[intent]()
                return f"'{nc}' ka {intent} = {val:,.2f}", f"df['{nc}'].{intent}()"

        # ── sort: "top 5 product by revenue" ─────────────────────────────────
        if intent == "sort":
            nc  = _best_num_col(df, cols)
            n   = 10
            m   = re.search(r"top\s+(\d+)|bottom\s+(\d+)", q)
            if m:
                n = int(m.group(1) or m.group(2))

            ascending = "bottom" in q or "lowest" in q or "worst" in q

            if nc:
                cat_col = _best_cat_col(df, cols)
                if cat_col:
                    # "top 5 product by revenue" → groupby then sort
                    grp = (df.groupby(cat_col)[nc]
                             .sum()
                             .sort_values(ascending=ascending)
                             .head(n)
                             .reset_index())
                    grp.columns = [cat_col, f"Total {nc}"]
                    ans   = f"Top {n} {cat_col} by {nc} (table neeche ⬇️)"
                    query = (f"df.groupby('{cat_col}')['{nc}'].sum()"
                             f".sort_values(ascending={ascending}).head({n})")
                    return ans, query
                else:
                    res   = df.nlargest(n, nc)[[nc]].to_string(index=False)
                    return f"Top {n} by '{nc}':\n{res}", f"df.nlargest({n}, '{nc}')"

        if intent == "group":
            cat_col  = _best_cat_col(df, cols) or _best_cat_col(df, df.columns.tolist())
            num_cols = _all_num_cols_in(df, cols)
            if not num_cols:
                num_cols = _numeric_cols(df)[:2]
            if cat_col and num_cols:
                col_names = " vs ".join(num_cols)
                query     = (f"df.groupby('{cat_col}'){num_cols}"
                             f".sum().sort_values('{num_cols[0]}', ascending=False)")
                return (f"{cat_col} ke hisaab se {col_names} ki breakdown (table neeche ⬇️)",
                        query)

        if intent == "filter" and cols:
            nums = re.findall(r"\d+\.?\d*", q)
            if nums and cols:
                c = cols[0]
                if pd.api.types.is_numeric_dtype(df[c]):
                    val = float(nums[0])
                    res = df[df[c] > val].head(10).to_string(index=False)
                    return (f"'{c}' > {val} wale rows:\n{res}",
                            f"df[df['{c}'] > {val}]")

        if intent == "corr":
            num_df = df.select_dtypes(include="number")
            if len(num_df.columns) >= 2:
                return f"Correlation matrix:\n{num_df.corr().to_string()}", "df.corr()"

    except Exception as e:
        print(f"[compute_answer] Error: {e}")

    return None, None


# ══════════════════════════════════════════════════════════════
#  TABLE HELPER — app.py mein st.dataframe() ke liye
# ══════════════════════════════════════════════════════════════

def compute_table(question: str, df: pd.DataFrame, intent: str, cols: list):
    """Tabular result → DataFrame, warna None."""
    try:
        q = question.lower()

        if intent == "sort":
            nc  = _best_num_col(df, cols)
            n   = 10
            m   = re.search(r"top\s+(\d+)|bottom\s+(\d+)", q)
            if m:
                n = int(m.group(1) or m.group(2))
            ascending = "bottom" in q or "lowest" in q or "worst" in q

            if nc:
                cat_col = _best_cat_col(df, cols)
                if cat_col:
                    grp = (df.groupby(cat_col)[nc]
                             .sum()
                             .sort_values(ascending=ascending)
                             .head(n)
                             .reset_index())
                    grp.columns = [cat_col, f"Total {nc}"]
                    return grp
                else:
                    return df.nlargest(n, nc)[[nc]].reset_index(drop=True)

        if intent == "group":
            cat_col  = _best_cat_col(df, cols) or _best_cat_col(df, df.columns.tolist())
            num_cols = _all_num_cols_in(df, cols)
            if not num_cols:
                num_cols = _numeric_cols(df)[:2]
            if cat_col and num_cols:
                grp = (df.groupby(cat_col)[num_cols]
                         .sum()
                         .sort_values(num_cols[0], ascending=False)
                         .reset_index())
                grp.columns = [cat_col] + [f"Total {c}" for c in num_cols]
                return grp

        if intent == "corr":
            num_df = df.select_dtypes(include="number")
            if len(num_df.columns) >= 2:
                return num_df.corr().round(3)

        if intent == "summary":
            return df.describe(include="all").round(2)

    except Exception as e:
        print(f"[compute_table] Error: {e}")

    return None


# ══════════════════════════════════════════════════════════════
#  LLM CALLS
# ══════════════════════════════════════════════════════════════

def _build_prompt(question, df, context=""):
    sample   = df.head(5).to_string(index=False)
    dtypes   = df.dtypes.to_string()
    num_cols = _numeric_cols(df)
    cat_cols = _cat_cols(df)

    return f"""You are a senior data analyst. You have a pandas DataFrame called `df`.

DataFrame Info:
- Shape: {df.shape[0]} rows x {df.shape[1]} columns
- Columns & dtypes:
{dtypes}
- Numeric columns: {num_cols}
- Categorical columns: {cat_cols}

Sample data (first 5 rows):
{sample}

{f"Context from past: {context}" if context else ""}

User question: {question}

Rules:
1. Answer directly in 1-2 sentences with specific numbers from the data.
2. Provide working pandas code (one-liner preferred).
3. If question asks for ranking/top N — use groupby + sort, not just max.
4. If question asks for comparison — mention all values.
5. Be specific, not generic.

Respond in this EXACT format:
ANSWER: <your direct answer with numbers>
CODE: <pandas code>
CHART: <bar|line|pie|scatter|none>
"""

def _call_gemini(question, df, context=""):
    prompt   = _build_prompt(question, df, context)
    response = gemini_model.generate_content(prompt)
    raw      = response.text.strip()
    answer   = raw
    query    = ""
    if "ANSWER:" in raw:
        parts  = raw.split("CODE:")
        answer = parts[0].replace("ANSWER:", "").strip()
        if len(parts) > 1:
            code_part = parts[1].split("CHART:")[0].strip()
            code_part = re.sub(r"```python|```", "", code_part).strip()
            query = code_part
    return answer, query

def _call_ollama(question, df, context=""):
    import requests
    prompt = f"""Data analyst. DataFrame `df`:
{df.dtypes.to_string()}

Sample:
{df.head(3).to_string(index=False)}

Question: {question}
Give specific answer with numbers + pandas code:"""

    payload = {"model": "gemma3:1b", "prompt": prompt,
               "stream": False, "options": {"num_predict": 300, "temperature": 0.1}}
    r          = requests.post("http://localhost:11434/api/generate",
                               json=payload, timeout=60)
    r.raise_for_status()
    raw        = r.json().get("response", "").strip()
    code_match = re.search(r"```python(.*?)```", raw, re.DOTALL)
    query      = code_match.group(1).strip() if code_match else ""
    return raw, query


# ══════════════════════════════════════════════════════════════
#  MAIN FUNCTION
# ══════════════════════════════════════════════════════════════

def ask_gemma(question: str, df: pd.DataFrame, context: str = ""):
    """Returns: (answer, query, intent, cols)"""
    intent = detect_intent(question)
    cols   = detect_cols(question, df)

    answer, query = compute_answer(question, df, intent, cols)
    if answer:
        return answer, query, intent, cols

    if GEMINI_AVAILABLE:
        try:
            answer, query = _call_gemini(question, df, context)
            print("[V7] Gemini used ✓")
            return answer, query, intent, cols
        except Exception as e:
            err = str(e)
            if "quota" in err.lower() or "429" in err:
                print("[V7] Gemini quota — Ollama fallback")
            else:
                print(f"[V7] Gemini error: {e}")

    if OLLAMA_AVAILABLE:
        try:
            answer, query = _call_ollama(question, df, context)
            print("[V7] Ollama fallback used")
            return answer, query, intent, cols
        except Exception as e:
            print(f"[V7] Ollama error: {e}")

    return ("Koi LLM available nahi. Check karein:\n"
            "1. GEMINI_API_KEY .env mein set hai?\n"
            "2. Ollama chal raha hai? (ollama serve)",
            "", intent, cols)


# ══════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════

def get_llm_status():
    return {
        "gemini": GEMINI_AVAILABLE,
        "ollama": OLLAMA_AVAILABLE,
        "mode":   "Gemini (primary)" if GEMINI_AVAILABLE else
                  "Ollama fallback"   if OLLAMA_AVAILABLE else
                  "No LLM — Python only"
    }

def find_best_column(keyword: str, columns: list):
    keyword = keyword.lower()
    for c in columns:
        if keyword == c.lower(): return c
    for c in columns:
        if keyword in c.lower(): return c
    for c in columns:
        words = c.lower().replace("_", " ").replace("-", " ").split()
        if keyword in words: return c
    return None

def detect_date_column(df: pd.DataFrame):
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            return col
    date_kw = ["date", "time", "month", "year", "day", "period", "week"]
    for col in df.columns:
        if any(kw in col.lower() for kw in date_kw):
            try:
                pd.to_datetime(df[col].dropna().head(5))
                return col
            except Exception:
                continue
    return None