CUSTOM_CSS = """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global Reset ── */
html, body, [class*="css"], [class*="st-"], .stApp {
    font-family: 'Inter', sans-serif !important;
}

/* ── Hide Streamlit Branding ── */
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] {
    display: none !important;
    visibility: hidden !important;
}

/* ════════════════════════════════════
   SIDEBAR
════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important;
    border-right: 1px solid #334155 !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.15) !important;
}

[data-testid="stSidebar"] > div {
    padding: 1.5rem 1rem !important;
}

/* Sidebar all text */
[data-testid="stSidebar"] * {
    color: #94A3B8 !important;
}

/* Sidebar Title */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] .stTitle {
    color: #F1F5F9 !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px !important;
}

/* Sidebar File Uploader */
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.04) !important;
    border: 2px dashed #334155 !important;
    border-radius: 12px !important;
    padding: 8px !important;
    transition: border-color 0.2s !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploader"]:hover {
    border-color: #3B82F6 !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * {
    color: #64748B !important;
    font-size: 12px !important;
}

/* Sidebar Browse Button */
[data-testid="stSidebar"] [data-testid="stFileUploader"] button {
    background: #1E293B !important;
    border: 1px solid #334155 !important;
    color: #94A3B8 !important;
    border-radius: 6px !important;
    font-size: 12px !important;
    padding: 4px 12px !important;
}

/* Sidebar Radio — Navigation */
[data-testid="stSidebar"] [data-testid="stRadio"] > label {
    color: #64748B !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    margin-bottom: 4px !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {
    gap: 4px !important;
    display: flex !important;
    flex-direction: column !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] {
    background: transparent !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    transition: all 0.15s !important;
    cursor: pointer !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:hover {
    background: rgba(59,130,246,0.08) !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] p {
    color: #94A3B8 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}

/* Sidebar Divider */
[data-testid="stSidebar"] hr {
    border-color: #1E293B !important;
    margin: 12px 0 !important;
}

/* Sidebar Success Badge */
[data-testid="stSidebar"] [data-testid="stAlert"] {
    background: rgba(16,185,129,0.1) !important;
    border: 1px solid rgba(16,185,129,0.25) !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
}

[data-testid="stSidebar"] [data-testid="stAlert"] * {
    color: #10B981 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}

/* Sidebar Warning Badge */
[data-testid="stSidebar"] [data-testid="stNotification"] {
    background: rgba(245,158,11,0.1) !important;
    border-color: rgba(245,158,11,0.25) !important;
}

/* Sidebar Caption */
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] small {
    color: #475569 !important;
    font-size: 11px !important;
}

/* Sidebar Session Buttons */
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid #1E293B !important;
    color: #64748B !important;
    border-radius: 8px !important;
    font-size: 12px !important;
    text-align: left !important;
    padding: 6px 10px !important;
    width: 100% !important;
    transition: all 0.15s !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(59,130,246,0.08) !important;
    border-color: #3B82F6 !important;
    color: #E2E8F0 !important;
}

/* Clear Chat Button */
[data-testid="stSidebar"] .stButton:last-child > button {
    background: rgba(239,68,68,0.08) !important;
    border-color: rgba(239,68,68,0.2) !important;
    color: #F87171 !important;
}

[data-testid="stSidebar"] .stButton:last-child > button:hover {
    background: rgba(239,68,68,0.15) !important;
}

/* ════════════════════════════════════
   MAIN CONTENT
════════════════════════════════════ */
.stApp {
    background: #F1F5F9 !important;
}

section[data-testid="stMain"] {
    background: #F1F5F9 !important;
}

.main .block-container {
    background: #F1F5F9 !important;
    padding: 2rem 2.5rem 3rem !important;
    max-width: 100% !important;
}

/* ── Page Headers ── */
h1 {
    color: #0F172A !important;
    font-size: 26px !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
    margin-bottom: 1.5rem !important;
}

h2, h3 {
    color: #1E293B !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px !important;
}

h2 { font-size: 18px !important; }
h3 { font-size: 16px !important; }

/* ── KPI Metric Cards ── */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px !important;
    padding: 20px 24px !important;
    box-shadow: 0 1px 3px rgba(15,23,42,0.06),
                0 4px 16px rgba(15,23,42,0.04) !important;
    position: relative !important;
    overflow: hidden !important;
    transition: all 0.2s ease !important;
}

[data-testid="stMetric"]:hover {
    box-shadow: 0 4px 24px rgba(59,130,246,0.12),
                0 1px 3px rgba(15,23,42,0.08) !important;
    border-color: #BFDBFE !important;
    transform: translateY(-1px) !important;
}

[data-testid="stMetric"]::before {
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 3px !important;
    background: linear-gradient(90deg, #3B82F6, #8B5CF6) !important;
    border-radius: 16px 16px 0 0 !important;
}

[data-testid="stMetricLabel"] > div {
    color: #64748B !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}

[data-testid="stMetricValue"] > div {
    color: #0F172A !important;
    font-size: 28px !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
    line-height: 1.2 !important;
}

[data-testid="stMetricDelta"] > div {
    font-size: 12px !important;
    font-weight: 600 !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid #E2E8F0 !important;
    margin: 1.5rem 0 !important;
}

/* ── Subheaders ── */
.stSubheader {
    color: #1E293B !important;
    font-weight: 700 !important;
}

/* ── Plotly Charts ── */
[data-testid="stPlotlyChart"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px !important;
    padding: 16px !important;
    box-shadow: 0 1px 3px rgba(15,23,42,0.06) !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px !important;
    overflow: hidden !important;
    box-shadow: 0 1px 3px rgba(15,23,42,0.06) !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px !important;
    box-shadow: 0 1px 3px rgba(15,23,42,0.06) !important;
    overflow: hidden !important;
}

details[data-testid="stExpander"] summary {
    color: #1E293B !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 14px 20px !important;
    background: #FFFFFF !important;
    border-radius: 16px !important;
}

details[data-testid="stExpander"][open] summary {
    border-bottom: 1px solid #F1F5F9 !important;
    border-radius: 16px 16px 0 0 !important;
}

/* ── Info Alerts ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-left-width: 4px !important;
    font-size: 14px !important;
}

/* ── Caption ── */
.stCaption, [data-testid="stCaptionContainer"] {
    color: #94A3B8 !important;
    font-size: 12px !important;
}

/* ── Chat Messages ── */
[data-testid="stChatMessage"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px !important;
    padding: 16px 20px !important;
    margin-bottom: 10px !important;
    box-shadow: 0 1px 3px rgba(15,23,42,0.06) !important;
}

[data-testid="stChatMessage"][data-testid*="user"] {
    background: #EFF6FF !important;
    border-color: #BFDBFE !important;
}

/* ── Chat Input ── */
[data-testid="stChatInput"] {
    background: #FFFFFF !important;
    border: 2px solid #E2E8F0 !important;
    border-radius: 16px !important;
    padding: 4px 8px !important;
    box-shadow: 0 1px 3px rgba(15,23,42,0.06) !important;
    transition: all 0.2s !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 4px rgba(59,130,246,0.08) !important;
}

[data-testid="stChatInput"] textarea {
    color: #0F172A !important;
    font-size: 14px !important;
}

/* ── Suggestion Buttons ── */
.stButton > button {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    color: #3B82F6 !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 8px 16px !important;
    transition: all 0.15s !important;
    box-shadow: 0 1px 2px rgba(15,23,42,0.05) !important;
}

.stButton > button:hover {
    background: #EFF6FF !important;
    border-color: #3B82F6 !important;
    color: #2563EB !important;
    box-shadow: 0 2px 8px rgba(59,130,246,0.15) !important;
    transform: translateY(-1px) !important;
}

/* ── Download Buttons ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #3B82F6, #2563EB) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 20px !important;
    box-shadow: 0 2px 8px rgba(59,130,246,0.3) !important;
    transition: all 0.2s !important;
}

.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
    box-shadow: 0 4px 16px rgba(59,130,246,0.4) !important;
    transform: translateY(-1px) !important;
}

/* ── Code blocks ── */
.stCode, code {
    background: #F8FAFC !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    font-size: 12px !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #3B82F6 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #F1F5F9; }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #94A3B8; }

</style>
"""