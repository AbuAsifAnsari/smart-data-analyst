# ─── Theme Color Tokens ───────────────────────────────────────────────────────

DARK = {
    "bg_page":       "#07071A",
    "bg_sidebar":    "linear-gradient(180deg, #0D0D2B 0%, #0A0A1F 100%)",
    "bg_card":       "rgba(255,255,255,0.03)",
    "bg_card_hover": "rgba(255,255,255,0.05)",
    "border":        "rgba(255,255,255,0.06)",
    "border_hover":  "rgba(124,58,237,0.35)",
    "text_primary":  "#F1F5F9",
    "text_secondary":"#94A3B8",
    "text_muted":    "#4B5563",
    "accent":        "#7C3AED",
    "accent_light":  "#A78BFA",
    "accent2":       "#06B6D4",
    "accent2_light": "#67E8F9",
    "success":       "#10B981",
    "warning":       "#F59E0B",
    "danger":        "#EF4444",
}

LIGHT = {
    "bg_page":       "#F8FAFC",
    "bg_sidebar":    "#FFFFFF",
    "bg_card":       "#FFFFFF",
    "bg_card_hover": "#FAFAFA",
    "border":        "#E5E7EB",
    "border_hover":  "#DDD6FE",
    "text_primary":  "#111827",
    "text_secondary":"#6B7280",
    "text_muted":    "#9CA3AF",
    "accent":        "#7C3AED",
    "accent_light":  "#6D28D9",
    "accent2":       "#0891B2",
    "accent2_light": "#0E7490",
    "success":       "#059669",
    "warning":       "#D97706",
    "danger":        "#DC2626",
}


# ─── CSS Generator ────────────────────────────────────────────────────────────

def get_css(dark_mode: bool = True) -> str:
    t = DARK if dark_mode else LIGHT

    # Ambient orbs only in dark mode
    orb_css = """
    .main-orb-1 {
        position: fixed;
        width: 500px; height: 500px;
        background: radial-gradient(circle, rgba(124,58,237,0.10) 0%, transparent 70%);
        top: -150px; right: -100px;
        pointer-events: none; z-index: 0;
        animation: orbFloat1 12s ease-in-out infinite;
    }
    .main-orb-2 {
        position: fixed;
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(6,182,212,0.07) 0%, transparent 70%);
        bottom: -100px; left: -80px;
        pointer-events: none; z-index: 0;
        animation: orbFloat2 16s ease-in-out infinite;
    }
    @keyframes orbFloat1 {
        0%, 100% { transform: translate(0,0); }
        50%       { transform: translate(-30px, 30px); }
    }
    @keyframes orbFloat2 {
        0%, 100% { transform: translate(0,0); }
        50%       { transform: translate(20px, -20px); }
    }
    """ if dark_mode else ""

    # KPI card top-bar gradient — cycles through 4 colors
    kpi_colors = [
        "linear-gradient(90deg, #7C3AED, #A78BFA)",
        "linear-gradient(90deg, #06B6D4, #67E8F9)" if dark_mode else "linear-gradient(90deg, #0891B2, #06B6D4)",
        "linear-gradient(90deg, #10B981, #6EE7B7)" if dark_mode else "linear-gradient(90deg, #059669, #10B981)",
        "linear-gradient(90deg, #F59E0B, #FCD34D)" if dark_mode else "linear-gradient(90deg, #D97706, #F59E0B)",
    ]

    card_bg     = t["bg_card"]
    card_border = t["border"]
    blur_val    = "blur(12px)" if dark_mode else "none"

    return f"""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global Reset ── */
html, body, [class*="css"], [class*="st-"], .stApp {{
    font-family: 'Inter', sans-serif !important;
}}

/* ── Hide Streamlit Branding ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {{
    display: none !important;
    visibility: hidden !important;
}}

/* ── Ambient Orbs (dark only) ── */
{orb_css}

/* ════════════════════════════════════
   APP BACKGROUND
════════════════════════════════════ */
.stApp {{
    background: {t["bg_page"]} !important;
}}

section[data-testid="stMain"] {{
    background: {t["bg_page"]} !important;
}}

.main .block-container {{
    background: {t["bg_page"]} !important;
    padding: 2rem 2.5rem 3rem !important;
    max-width: 100% !important;
    position: relative; z-index: 1;
}}

/* ════════════════════════════════════
   SIDEBAR
════════════════════════════════════ */
[data-testid="stSidebar"] {{
    background: {t["bg_sidebar"]} !important;
    border-right: 1px solid {t["border"]} !important;
    box-shadow: {"4px 0 32px rgba(0,0,0,0.5)" if dark_mode else "4px 0 16px rgba(0,0,0,0.06)"} !important;
}}

[data-testid="stSidebar"] > div {{
    padding: 1.5rem 1rem !important;
}}

[data-testid="stSidebar"] * {{
    color: {t["text_secondary"]} !important;
}}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] .stTitle {{
    color: {t["text_primary"]} !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px !important;
}}

[data-testid="stSidebar"] [data-testid="stFileUploader"] {{
    background: {"rgba(255,255,255,0.03)" if dark_mode else "#F9FAFB"} !important;
    border: 2px dashed {t["border"]} !important;
    border-radius: 12px !important;
    padding: 8px !important;
    transition: border-color 0.2s !important;
}}

[data-testid="stSidebar"] [data-testid="stFileUploader"]:hover {{
    border-color: {t["accent"]} !important;
}}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * {{
    color: {t["text_muted"]} !important;
    font-size: 13px !important;
}}

[data-testid="stSidebar"] [data-testid="stFileUploader"] button {{
    background: {"#1E293B" if dark_mode else "#F3F4F6"} !important;
    border: 1px solid {t["border"]} !important;
    color: {t["text_secondary"]} !important;
    border-radius: 6px !important;
    font-size: 13px !important;
    padding: 4px 12px !important;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] > label {{
    color: {t["text_muted"]} !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {{
    gap: 4px !important;
    display: flex !important;
    flex-direction: column !important;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] {{
    background: transparent !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    transition: all 0.15s !important;
    cursor: pointer !important;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:hover {{
    background: {"rgba(124,58,237,0.12)" if dark_mode else "#F3F0FF"} !important;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] p {{
    color: {t["text_secondary"]} !important;
    font-size: 15px !important;
    font-weight: 500 !important;
}}

[data-testid="stSidebar"] hr {{
    border-color: {t["border"]} !important;
    margin: 12px 0 !important;
}}

/* Gemini connected badge */
[data-testid="stSidebar"] [data-testid="stAlert"] {{
    background: {"rgba(16,185,129,0.08)" if dark_mode else "#ECFDF5"} !important;
    border: 1px solid {"rgba(16,185,129,0.2)" if dark_mode else "#A7F3D0"} !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
}}

[data-testid="stSidebar"] [data-testid="stAlert"] * {{
    color: {t["success"]} !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}}

[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] small {{
    color: {t["text_muted"]} !important;
    font-size: 12px !important;
}}

/* Session history buttons */
[data-testid="stSidebar"] .stButton > button {{
    background: {"rgba(255,255,255,0.03)" if dark_mode else "#F9FAFB"} !important;
    border: 1px solid {t["border"]} !important;
    color: {t["text_muted"]} !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    text-align: left !important;
    padding: 6px 10px !important;
    width: 100% !important;
    transition: all 0.15s !important;
}}

[data-testid="stSidebar"] .stButton > button:hover {{
    background: {"rgba(124,58,237,0.12)" if dark_mode else "#F3F0FF"} !important;
    border-color: {t["accent"]} !important;
    color: {t["accent_light"]} !important;
}}

[data-testid="stSidebar"] .stButton:last-child > button {{
    background: {"rgba(239,68,68,0.06)" if dark_mode else "#FEF2F2"} !important;
    border-color: {"rgba(239,68,68,0.15)" if dark_mode else "#FECACA"} !important;
    color: {t["danger"]} !important;
}}

[data-testid="stSidebar"] .stButton:last-child > button:hover {{
    background: {"rgba(239,68,68,0.12)" if dark_mode else "#FEE2E2"} !important;
}}

/* ════════════════════════════════════
   PAGE HEADERS
════════════════════════════════════ */
h1 {{
    color: {t["text_primary"]} !important;
    font-size: 28px !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
    margin-bottom: 1.5rem !important;
}}

h2, h3 {{
    color: {t["text_primary"]} !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px !important;
}}

h2 {{ font-size: 20px !important; }}
h3 {{ font-size: 17px !important; }}

p, span, label, div {{
    color: {"#CBD5E1" if dark_mode else "#374151"} !important;
    font-size: 15px !important;
}}

/* ════════════════════════════════════
   KPI METRIC CARDS
════════════════════════════════════ */
[data-testid="stMetric"] {{
    background: {card_bg} !important;
    border: 1px solid {card_border} !important;
    border-radius: 16px !important;
    padding: 20px 24px !important;
    backdrop-filter: {blur_val} !important;
    -webkit-backdrop-filter: {blur_val} !important;
    box-shadow: {"0 0 0 1px rgba(124,58,237,0.08), 0 4px 24px rgba(0,0,0,0.3)" if dark_mode else "0 1px 4px rgba(0,0,0,0.06)"} !important;
    position: relative !important;
    overflow: hidden !important;
    transition: all 0.2s ease !important;
}}

[data-testid="stMetric"]:hover {{
    border-color: {t["border_hover"]} !important;
    box-shadow: {"0 0 0 1px rgba(124,58,237,0.3), 0 4px 32px rgba(124,58,237,0.15)" if dark_mode else "0 4px 16px rgba(124,58,237,0.12)"} !important;
    transform: translateY(-2px) !important;
}}

[data-testid="stMetric"]::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important; left: 0 !important; right: 0 !important;
    height: 2px !important;
    background: linear-gradient(90deg, {t["accent"]}, #A78BFA, {t["accent2"]}) !important;
    border-radius: 16px 16px 0 0 !important;
}}

[data-testid="stMetricLabel"] > div {{
    color: {t["text_muted"]} !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}}

[data-testid="stMetricValue"] > div {{
    color: {t["text_primary"]} !important;
    font-size: 30px !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
    line-height: 1.2 !important;
}}

[data-testid="stMetricDelta"] > div {{
    font-size: 13px !important;
    font-weight: 600 !important;
}}

/* ════════════════════════════════════
   PLOTLY CHARTS
════════════════════════════════════ */
[data-testid="stPlotlyChart"] {{
    background: {card_bg} !important;
    border: 1px solid {card_border} !important;
    border-radius: 16px !important;
    padding: 16px !important;
    backdrop-filter: {blur_val} !important;
    -webkit-backdrop-filter: {blur_val} !important;
    box-shadow: {"0 4px 24px rgba(0,0,0,0.3)" if dark_mode else "0 1px 4px rgba(0,0,0,0.06)"} !important;
}}

/* ════════════════════════════════════
   DATAFRAME
════════════════════════════════════ */
[data-testid="stDataFrame"] {{
    background: {card_bg} !important;
    border: 1px solid {card_border} !important;
    border-radius: 16px !important;
    overflow: hidden !important;
    backdrop-filter: {blur_val} !important;
    box-shadow: {"0 4px 24px rgba(0,0,0,0.3)" if dark_mode else "0 1px 4px rgba(0,0,0,0.06)"} !important;
}}

[data-testid="stDataFrame"] * {{
    color: {"#CBD5E1" if dark_mode else "#374151"} !important;
    font-size: 14px !important;
}}

/* ════════════════════════════════════
   EXPANDER
════════════════════════════════════ */
[data-testid="stExpander"] {{
    background: {card_bg} !important;
    border: 1px solid {card_border} !important;
    border-radius: 16px !important;
    backdrop-filter: {blur_val} !important;
    overflow: hidden !important;
}}

details[data-testid="stExpander"] summary {{
    color: {t["text_primary"]} !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 14px 20px !important;
    background: {card_bg} !important;
}}

details[data-testid="stExpander"][open] summary {{
    border-bottom: 1px solid {card_border} !important;
}}

/* ════════════════════════════════════
   ALERTS
════════════════════════════════════ */
[data-testid="stAlert"] {{
    border-radius: 12px !important;
    border-left-width: 4px !important;
    font-size: 15px !important;
    background: {"rgba(124,58,237,0.08)" if dark_mode else "#F3F0FF"} !important;
    border-color: {t["accent"]} !important;
}}

/* ════════════════════════════════════
   CHAT MESSAGES
════════════════════════════════════ */
[data-testid="stChatMessage"] {{
    background: {card_bg} !important;
    border: 1px solid {card_border} !important;
    border-radius: 16px !important;
    padding: 16px 20px !important;
    margin-bottom: 10px !important;
    backdrop-filter: {blur_val} !important;
}}

[data-testid="stChatMessage"][data-testid*="user"] {{
    background: {"rgba(124,58,237,0.08)" if dark_mode else "#F3F0FF"} !important;
    border-color: {"rgba(124,58,237,0.2)" if dark_mode else "#DDD6FE"} !important;
}}

/* ════════════════════════════════════
   CHAT INPUT
════════════════════════════════════ */
[data-testid="stChatInput"] {{
    background: {card_bg} !important;
    border: 2px solid {card_border} !important;
    border-radius: 16px !important;
    padding: 4px 8px !important;
    transition: all 0.2s !important;
    backdrop-filter: {blur_val} !important;
}}

[data-testid="stChatInput"]:focus-within {{
    border-color: {t["accent"]} !important;
    box-shadow: 0 0 0 4px {"rgba(124,58,237,0.12)" if dark_mode else "rgba(124,58,237,0.08)"} !important;
}}

[data-testid="stChatInput"] textarea {{
    color: {t["text_primary"]} !important;
    font-size: 15px !important;
    background: transparent !important;
}}

/* ════════════════════════════════════
   BUTTONS
════════════════════════════════════ */
.stButton > button {{
    background: {card_bg} !important;
    border: 1px solid {card_border} !important;
    color: {t["accent_light"]} !important;
    border-radius: 10px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 9px 16px !important;
    transition: all 0.15s !important;
    backdrop-filter: {blur_val} !important;
}}

.stButton > button:hover {{
    background: {"rgba(124,58,237,0.12)" if dark_mode else "#F3F0FF"} !important;
    border-color: {t["accent"]} !important;
    color: {t["accent_light"]} !important;
    box-shadow: 0 2px 12px {"rgba(124,58,237,0.2)" if dark_mode else "rgba(124,58,237,0.15)"} !important;
    transform: translateY(-1px) !important;
}}

/* Download button */
.stDownloadButton > button {{
    background: linear-gradient(135deg, {t["accent"]}, #4F46E5) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 10px 20px !important;
    box-shadow: 0 2px 12px rgba(124,58,237,0.35) !important;
    transition: all 0.2s !important;
}}

.stDownloadButton > button:hover {{
    box-shadow: 0 4px 20px rgba(124,58,237,0.5) !important;
    transform: translateY(-1px) !important;
}}

/* ════════════════════════════════════
   MISC
════════════════════════════════════ */
hr {{
    border: none !important;
    border-top: 1px solid {card_border} !important;
    margin: 1.5rem 0 !important;
}}

.stCode, code {{
    background: {"#0A0F1E" if dark_mode else "#F3F4F6"} !important;
    border: 1px solid {card_border} !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    color: {t["accent_light"]} !important;
}}

.stSpinner > div {{
    border-top-color: {t["accent"]} !important;
}}

.stCaption, [data-testid="stCaptionContainer"] {{
    color: {t["text_muted"]} !important;
    font-size: 13px !important;
}}

.stSubheader {{
    color: {t["text_primary"]} !important;
    font-weight: 700 !important;
    font-size: 17px !important;
}}

/* Scrollbar */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: {"#07071A" if dark_mode else "#F1F5F9"}; }}
::-webkit-scrollbar-thumb {{ background: {"#1E293B" if dark_mode else "#D1D5DB"}; border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: {"#334155" if dark_mode else "#9CA3AF"}; }}

</style>

<!-- Ambient orbs injected into DOM (dark mode only) -->
{"<div class='main-orb-1'></div><div class='main-orb-2'></div>" if dark_mode else ""}
"""


# ─── Legacy alias — keeps old code working ────────────────────────────────────
CUSTOM_CSS = get_css(dark_mode=True)