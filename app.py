
import streamlit as st
import pandas as pd
from datetime import date
from html import escape

# ============================================================
# GRAMA PANCHAYAT PORTAL
# Streamlit single-file application
# ============================================================

st.set_page_config(
    page_title="Grama Panchayat Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# App configuration
# -----------------------------
PANCHAYATS = [
    "Eluru",
    "Pedavegi",
    "Denduluru",
    "Nuzvid",
    "Bhimadole",
    "Unguturu",
    "Chatrai",
    "Agiripalli",
]

DIA_SIZES = [63, 75, 90, 110, 125, 140, 160, 180, 200]

DATA_COLUMNS = [
    "Panchayat",
    "Contractor Name",
    "Vendor Code",
    "RA Bill",
    "Work Date",
    "Scheme ID",
    *[f"{size} DIA" for size in DIA_SIZES],
    "Submitted On",
]

# -----------------------------
# Session state
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_panchayat" not in st.session_state:
    st.session_state.selected_panchayat = ""

if "submissions" not in st.session_state:
    st.session_state.submissions = []

for size in DIA_SIZES:
    key = f"dia_{size}"
    if key not in st.session_state:
        st.session_state[key] = 0

# -----------------------------
# CSS
# -----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,500;0,600;1,500&display=swap');

    :root {
        --navy: #101c46;
        --navy2: #172653;
        --purple: #7336f1;
        --pink: #f2388b;
        --pink-soft: #ffe6f2;
        --border: #e5ddea;
        --muted: #69718c;
        --bg: #fff8fc;
    }

    * {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 92% 15%, rgba(246, 176, 211, 0.22), transparent 28%),
            radial-gradient(circle at 72% 75%, rgba(150, 105, 247, 0.10), transparent 25%),
            linear-gradient(135deg, #fffafd 0%, #fff7fb 48%, #fff9fd 100%);
        color: var(--navy);
    }

    /* Streamlit chrome */
    #MainMenu, footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    div[data-testid="stToolbar"] {
        visibility: hidden;
        height: 0;
    }

    section[data-testid="stSidebar"] {
        width: 302px !important;
        min-width: 302px !important;
        border-right: 1px solid #f0ddeb;
        background: rgba(255,255,255,0.88);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 18px;
    }

    /* Main page width */
    .block-container {
        max-width: 1120px;
        padding-top: 28px;
        padding-bottom: 40px;
    }

    /* Sidebar */
    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 2px 18px 22px 18px;
    }

    .brand-icon {
        font-size: 30px;
        line-height: 1;
        filter: saturate(0.9);
    }

    .brand-text {
        font-size: 17px;
        font-weight: 700;
        color: var(--navy);
        letter-spacing: -0.3px;
    }

    .side-note {
        text-align: center;
        margin-top: 185px;
        color: #e36aa5;
        font-family: 'Playfair Display', serif;
        font-style: italic;
        font-size: 17px;
        line-height: 1.35;
    }

    .side-note .heart {
        font-family: sans-serif;
        font-size: 15px;
    }

    .village {
        margin-top: 12px;
        text-align: center;
        opacity: 0.78;
        font-size: 42px;
        letter-spacing: 2px;
    }

    /* Sidebar Streamlit buttons */
    section[data-testid="stSidebar"] .stButton > button,
    section[data-testid="stSidebar"] .stDownloadButton > button {
        border: none !important;
        background: transparent !important;
        color: #c60b72 !important;
        box-shadow: none !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 10px 16px !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        min-height: 42px !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover,
    section[data-testid="stSidebar"] .stDownloadButton > button:hover {
        background: #ffe8f4 !important;
    }

    .side-active {
        background: #ffe0f0;
        color: #c30a70;
        border-radius: 9px;
        padding: 11px 16px;
        margin: 0 8px 8px 8px;
        font-weight: 700;
    }

    .side-item {
        color: #c30a70;
        padding: 9px 16px;
        margin: 0 8px;
        font-weight: 600;
    }

    /* Top actions */
    .top-actions {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 18px;
        color: #1d274d;
        font-size: 14px;
        margin-bottom: 4px;
    }

    .top-actions span {
        color: #5f6882;
    }

    /* Page title */
    .page-title {
        display: flex;
        align-items: center;
        gap: 16px;
        margin: 2px 0 20px 0;
    }

    .title-icon {
        font-size: 42px;
        line-height: 1;
    }

    .page-title h1 {
        margin: 0;
        font-size: 32px;
        line-height: 1.15;
        font-weight: 800;
        letter-spacing: -1px;
        color: var(--navy);
    }

    .page-title p {
        margin: 7px 0 0 0;
        font-size: 16px;
        color: #172653;
    }

    /* Main cards */
    .card {
        background: rgba(255,255,255,0.94);
        border: 1px solid #f0dce9;
        border-radius: 18px;
        box-shadow: 0 12px 35px rgba(184, 66, 139, 0.09);
        padding: 26px 28px 28px 28px;
    }

    .card-label {
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 8px;
        color: var(--navy);
    }

    .back-link {
        color: #c40b72;
        font-weight: 700;
        font-size: 14px;
        margin: 0 0 12px 4px;
    }

    /* Streamlit widgets */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        border: 1px solid #dcd7e8 !important;
        border-radius: 10px !important;
        background: white !important;
        min-height: 46px !important;
        box-shadow: none !important;
    }

    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="input"] > div:focus-within {
        border-color: #df58aa !important;
        box-shadow: 0 0 0 2px rgba(224, 61, 146, 0.08) !important;
    }

    .stTextInput label,
    .stDateInput label,
    .stSelectbox label,
    .stNumberInput label {
        color: var(--navy) !important;
        font-weight: 600 !important;
    }

    .stTextInput input,
    .stDateInput input,
    .stNumberInput input {
        color: #18234b !important;
    }

    /* Main gradient buttons */
    .stButton > button {
        min-height: 47px;
        border: none !important;
        border-radius: 11px !important;
        background: linear-gradient(90deg, #7332ef, #ef3b8b) !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 18px rgba(187, 53, 143, 0.18);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 22px rgba(187, 53, 143, 0.24);
    }

    /* DIA section */
    .dia-heading {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 10px;
        margin-bottom: 2px;
    }

    .dia-heading h2 {
        margin: 0;
        font-size: 22px;
        color: var(--navy);
    }

    .dia-rule {
        height: 1px;
        background: #f1b9d8;
        flex: 1;
        margin-left: 8px;
    }

    .dia-help {
        color: #263153;
        font-size: 13px;
        margin: 6px 0 12px 0;
    }

    .dia-name {
        font-size: 13px;
        font-weight: 600;
        color: var(--navy);
        margin-bottom: 3px;
    }

    /* Counter row */
    .counter-label {
        font-size: 13px;
        font-weight: 600;
        color: var(--navy);
        margin-bottom: 4px;
    }

    .counter-box {
        display: flex;
        align-items: center;
    }

    /* Messages */
    .success-box {
        background: #effcf4;
        border: 1px solid #bfe8cf;
        color: #176b38;
        padding: 11px 14px;
        border-radius: 10px;
        margin-top: 14px;
        font-weight: 600;
    }

    .error-box {
        background: #fff1f3;
        border: 1px solid #f1c0ca;
        color: #9b2440;
        padding: 11px 14px;
        border-radius: 10px;
        margin-top: 14px;
        font-weight: 600;
    }

    /* Responsive */
    @media (max-width: 900px) {
        section[data-testid="stSidebar"] {
            width: 260px !important;
            min-width: 260px !important;
        }

        .page-title h1 {
            font-size: 27px;
        }

        .block-container {
            padding-left: 20px;
            padding-right: 20px;
        }
    }

    @media (max-width: 650px) {
        .block-container {
            padding-top: 15px;
            padding-left: 12px;
            padding-right: 12px;
        }

        .page-title {
            gap: 9px;
        }

        .title-icon {
            font-size: 32px;
        }

        .page-title h1 {
            font-size: 23px;
        }

        .page-title p {
            font-size: 13px;
        }

        .card {
            padding: 18px 15px 20px 15px;
            border-radius: 14px;
        }

        .side-note {
            margin-top: 90px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Helpers
# -----------------------------
def village_art():
    return """
    <div class="village">
        🌳 🏠 🌳 🏡 🌳
    </div>
    """

def reset_dia_values():
    for size in DIA_SIZES:
        st.session_state[f"dia_{size}"] = 0

def go_home():
    st.session_state.page = "home"

def go_form():
    st.session_state.page = "form"

def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div class="brand">
                <div class="brand-icon">🏛️</div>
                <div class="brand-text">Grama Panchayat Portal</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.page == "home":
            st.markdown('<div class="side-active">⌂ &nbsp; Home</div>', unsafe_allow_html=True)
        else:
            if st.button("⌂   Home", key="side_home"):
                go_home()
                st.rerun()

        # Download section
        data = pd.DataFrame(st.session_state.submissions, columns=DATA_COLUMNS)
        csv_data = data.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⇩   Download Data Sheet",
            data=csv_data,
            file_name="grama_panchayat_data.csv",
            mime="text/csv",
            key="download_csv",
            use_container_width=True,
        )

        st.markdown(
            """
            <div class="side-note">
                Stronger Panchayats<br>
                Brighter Future<br>
                <span class="heart">──── ♥ ────</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(village_art(), unsafe_allow_html=True)

render_sidebar()

# -----------------------------
# Top action bar
# -----------------------------
st.markdown(
    """
    <div class="top-actions">
        <span>Share</span>
        <span>⌯</span>
        <span>☼</span>
        <span>⋮</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# HOME PAGE
# -----------------------------
if st.session_state.page == "home":

    st.markdown(
        """
        <div class="page-title">
            <div class="title-icon">🏛️</div>
            <div>
                <h1>Grama Panchayat Portal</h1>
                <p>Select your Grama Panchayat to continue</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-label">Select Panchayat</div>', unsafe_allow_html=True)

    selected = st.selectbox(
        "Panchayat",
        options=["-- Select Panchayat --"] + PANCHAYATS,
        index=0 if not st.session_state.selected_panchayat else
              PANCHAYATS.index(st.session_state.selected_panchayat) + 1,
        label_visibility="collapsed",
        key="panchayat_select",
    )

    st.session_state.selected_panchayat = (
        "" if selected == "-- Select Panchayat --" else selected
    )

    st.write("")

    if st.button("Continue   →", use_container_width=True, key="continue_btn"):
        if not st.session_state.selected_panchayat:
            st.warning("Please select a Grama Panchayat first.")
        else:
            reset_dia_values()
            st.session_state.page = "form"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# FORM PAGE
# -----------------------------
else:

    if st.button("←   Back", key="back_btn"):
        go_home()
        st.rerun()

    st.markdown(
        f"""
        <div style="margin: 2px 0 14px 4px; color:#5d6680; font-size:14px;">
            Selected Panchayat:
            <strong style="color:#b90b6e;">{escape(st.session_state.selected_panchayat)}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)

    # First two-column section
    left, right = st.columns(2, gap="large")

    with left:
        contractor = st.text_input(
            "Contractor Name",
            placeholder="Enter contractor name",
            key="contractor",
        )

        vendor_code = st.text_input(
            "Vendor Code",
            placeholder="Enter vendor code",
            key="vendor_code",
        )

        scheme_id = st.text_input(
            "Scheme ID",
            placeholder="Enter scheme ID",
            key="scheme_id",
        )

    with right:
        ra_bill = st.text_input(
            "RA Bill",
            placeholder="Enter RA Bill number",
            key="ra_bill",
        )

        work_date = st.date_input(
            "Work Date",
            value=date.today(),
            key="work_date",
            format="YYYY/MM/DD",
        )

    # DIA heading
    st.markdown(
        """
        <div class="dia-heading">
            <div style="font-size:24px;">📏</div>
            <h2>DIA Values</h2>
            <div class="dia-rule"></div>
        </div>
        <div class="dia-help">
            Enter the quantity for each available DIA size.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 3 columns x 3 rows
    dia_cols = st.columns(3, gap="large")

    for index, size in enumerate(DIA_SIZES):
        col = dia_cols[index % 3]
        with col:
            key = f"dia_{size}"
            st.markdown(
                f'<div class="counter-label">{size} DIA</div>',
                unsafe_allow_html=True,
            )

            c1, c2, c3 = st.columns([6.8, 1.1, 1.1], gap="small")

            with c1:
                st.number_input(
                    f"{size} DIA value",
                    min_value=0,
                    step=1,
                    key=key,
                    label_visibility="collapsed",
                )

            with c2:
                if st.button("−", key=f"minus_{size}", use_container_width=True):
                    st.session_state[key] = max(0, st.session_state[key] - 1)
                    st.rerun()

            with c3:
                if st.button("+", key=f"plus_{size}", use_container_width=True):
                    st.session_state[key] += 1
                    st.rerun()

    st.write("")

    if st.button("▣   Submit Details", use_container_width=True, key="submit_btn"):
        errors = []

        if not st.session_state.selected_panchayat:
            errors.append("Panchayat is required.")
        if not contractor.strip():
            errors.append("Contractor Name is required.")
        if not vendor_code.strip():
            errors.append("Vendor Code is required.")
        if not ra_bill.strip():
            errors.append("RA Bill is required.")
        if not scheme_id.strip():
            errors.append("Scheme ID is required.")

        if errors:
            st.markdown(
                '<div class="error-box">⚠ ' + "<br>⚠ ".join(errors) + "</div>",
                unsafe_allow_html=True,
            )
        else:
            record = {
                "Panchayat": st.session_state.selected_panchayat,
                "Contractor Name": contractor.strip(),
                "Vendor Code": vendor_code.strip(),
                "RA Bill": ra_bill.strip(),
                "Work Date": work_date.strftime("%Y-%m-%d"),
                "Scheme ID": scheme_id.strip(),
            }

            for size in DIA_SIZES:
                record[f"{size} DIA"] = st.session_state[f"dia_{size}"]

            record["Submitted On"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

            st.session_state.submissions.append(record)

            st.markdown(
                '<div class="success-box">✓ Details submitted successfully.</div>',
                unsafe_allow_html=True,
            )

            # Reset only form-specific values after successful submission
            for key in ["contractor", "vendor_code", "ra_bill", "scheme_id"]:
                st.session_state[key] = ""

            reset_dia_values()

    st.markdown("</div>", unsafe_allow_html=True)

    # Small session summary
    if st.session_state.submissions:
        st.write("")
        st.caption(
            f"Records submitted in this session: {len(st.session_state.submissions)}. "
            "Use “Download Data Sheet” from the left sidebar to export them as CSV."
        )
