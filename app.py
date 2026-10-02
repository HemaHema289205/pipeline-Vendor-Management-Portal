import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Grama Panchayat Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 🎨 COLOR SETTINGS
# CHANGE ONLY THESE COLORS
# ============================================================

PRIMARY_COLOR = "#7C3AED"
SECONDARY_COLOR = "#EC4899"

BACKGROUND_COLOR = "#F8F7FF"
CARD_COLOR = "#FFFFFF"

TEXT_COLOR = "#111827"
MUTED_TEXT_COLOR = "#64748B"

BORDER_COLOR = "#D7D9E2"

SIDEBAR_COLOR = "#111827"
SIDEBAR_TEXT_COLOR = "#FFFFFF"

INPUT_BACKGROUND = "#FFFFFF"
INPUT_TEXT_COLOR = "#111827"

DATE_BACKGROUND = "#FFFFFF"
DATE_TEXT_COLOR = "#111827"

BUTTON_TEXT_COLOR = "#FFFFFF"

DIA_BUTTON_BACKGROUND = "#F3E8FF"
DIA_BUTTON_TEXT = "#6D28D9"


# ============================================================
# PANCHAYAT DATA
# Replace / extend this list with your actual Panchayats
# ============================================================

PANCHAYATS = [
    "Aaspurdevsara",
    "Aaurain",
    "Atrampur & Turkoli",
    "Baejalpur",
    "BANBIRPUR",
    "Behta & Bijhala",
    "Belha",
    "Bhagwanpur",
    "Chandpur",
    "Lakshmipur",
    "Rampur",
]


# ============================================================
# DIA SIZES
# ============================================================

DIA_SIZES = [
    63,
    75,
    90,
    110,
    125,
    140,
    160,
    180,
    200
]


# ============================================================
# SESSION STATE
# ============================================================

if "selected_panchayat" not in st.session_state:
    st.session_state.selected_panchayat = None

if "page" not in st.session_state:
    st.session_state.page = "home"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
    <style>

    /* -------------------------------------------------------
       GLOBAL
    ------------------------------------------------------- */

    html, body, [class*="css"] {{
        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }}

    .stApp {{
        background:
            radial-gradient(
                circle at 85% 15%,
                rgba(236, 72, 153, 0.08),
                transparent 28%
            ),
            radial-gradient(
                circle at 15% 70%,
                rgba(124, 58, 237, 0.06),
                transparent 30%
            ),
            {BACKGROUND_COLOR};
        color: {TEXT_COLOR};
    }}


    /* -------------------------------------------------------
       REMOVE STREAMLIT DEFAULT TOP SPACE
    ------------------------------------------------------- */

    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1250px !important;
    }}


    /* -------------------------------------------------------
       SIDEBAR
    ------------------------------------------------------- */

    section[data-testid="stSidebar"] {{
        background: {SIDEBAR_COLOR} !important;
        border-right: none !important;
    }}

    section[data-testid="stSidebar"] > div {{
        background: {SIDEBAR_COLOR} !important;
    }}

    section[data-testid="stSidebar"] * {{
        color: {SIDEBAR_TEXT_COLOR};
    }}

    .sidebar-title {{
        font-size: 22px;
        font-weight: 800;
        margin-top: 15px;
        margin-bottom: 8px;
        color: {SIDEBAR_TEXT_COLOR};
    }}

    .sidebar-description {{
        color: #CBD5E1 !important;
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 22px;
    }}

    div[data-testid="stSidebar"] .stDownloadButton > button {{
        width: 100%;
        min-height: 48px;
        border-radius: 12px;
        border: 1px solid #475569;
        background: transparent !important;
        color: {SIDEBAR_TEXT_COLOR} !important;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.2s ease;
    }}

    div[data-testid="stSidebar"] .stDownloadButton > button:hover {{
        background: rgba(255,255,255,0.08) !important;
        border-color: #94A3B8;
        color: #FFFFFF !important;
    }}


    /* -------------------------------------------------------
       MAIN HEADER
    ------------------------------------------------------- */

    .portal-header {{
        text-align: center;
        padding: 18px 10px 25px 10px;
    }}

    .portal-icon {{
        font-size: 48px;
        line-height: 1;
        margin-bottom: 10px;
    }}

    .portal-title {{
        font-size: clamp(32px, 4vw, 50px);
        font-weight: 800;
        color: {TEXT_COLOR};
        margin: 0;
        letter-spacing: -1.5px;
    }}

    .portal-subtitle {{
        color: {MUTED_TEXT_COLOR};
        font-size: 18px;
        margin-top: 10px;
    }}


    /* -------------------------------------------------------
       CARD
    ------------------------------------------------------- */

    .portal-card {{
        background: {CARD_COLOR};
        border: 1px solid {BORDER_COLOR};
        border-radius: 24px;
        padding: 32px;
        box-shadow:
            0 15px 40px rgba(15, 23, 42, 0.08);
        margin-top: 20px;
    }}


    /* -------------------------------------------------------
       LABELS
    ------------------------------------------------------- */

    .field-label {{
        color: {TEXT_COLOR};
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 7px;
    }}


    /* -------------------------------------------------------
       SELECTBOX
    ------------------------------------------------------- */

    div[data-baseweb="select"] > div {{
        background: {INPUT_BACKGROUND} !important;
        color: {INPUT_TEXT_COLOR} !important;
        border: 1px solid {BORDER_COLOR} !important;
        border-radius: 12px !important;
        min-height: 48px !important;
    }}

    div[data-baseweb="select"] * {{
        color: {INPUT_TEXT_COLOR} !important;
    }}

    div[data-baseweb="popover"] {{
        background: {CARD_COLOR} !important;
    }}

    div[role="option"] {{
        color: {INPUT_TEXT_COLOR} !important;
        background: {CARD_COLOR} !important;
    }}

    div[role="option"]:hover {{
        background: #F3E8FF !important;
        color: {TEXT_COLOR} !important;
    }}


    /* -------------------------------------------------------
       TEXT INPUT
    ------------------------------------------------------- */

    div[data-testid="stTextInput"] input {{
        background: {INPUT_BACKGROUND} !important;
        color: {INPUT_TEXT_COLOR} !important;
        border: 1px solid {BORDER_COLOR} !important;
        border-radius: 12px !important;
        min-height: 46px !important;
    }}

    div[data-testid="stTextInput"] input::placeholder {{
        color: #94A3B8 !important;
    }}


    /* -------------------------------------------------------
       DATE INPUT
    ------------------------------------------------------- */

    div[data-testid="stDateInput"] input {{
        background: {DATE_BACKGROUND} !important;
        color: {DATE_TEXT_COLOR} !important;
        border: 1px solid {BORDER_COLOR} !important;
        border-radius: 12px !important;
        min-height: 46px !important;
    }}

    div[data-testid="stDateInput"] button {{
        background: {DATE_BACKGROUND} !important;
        color: {DATE_TEXT_COLOR} !important;
    }}


    /* -------------------------------------------------------
       MAIN BUTTON
    ------------------------------------------------------- */

    .stButton > button {{
        width: 100%;
        min-height: 50px;
        border-radius: 13px;
        border: none !important;
        background:
            linear-gradient(
                90deg,
                {PRIMARY_COLOR},
                {SECONDARY_COLOR}
            ) !important;
        color: {BUTTON_TEXT_COLOR} !important;
        font-size: 16px;
        font-weight: 700;
        box-shadow:
            0 10px 25px rgba(124, 58, 237, 0.22);
        transition: transform 0.2s ease,
                    box-shadow 0.2s ease;
    }}

    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow:
            0 14px 30px rgba(124, 58, 237, 0.28);
    }}


    /* -------------------------------------------------------
       FORM HEADER
    ------------------------------------------------------- */

    .form-heading {{
        font-size: 30px;
        font-weight: 800;
        color: {TEXT_COLOR};
        margin-bottom: 4px;
    }}

    .form-description {{
        color: {MUTED_TEXT_COLOR};
        font-size: 15px;
        margin-bottom: 25px;
    }}


    /* -------------------------------------------------------
       DIA SECTION
    ------------------------------------------------------- */

    .dia-heading {{
        font-size: 29px;
        font-weight: 800;
        color: {TEXT_COLOR};
        margin-top: 22px;
        margin-bottom: 4px;
    }}

    .dia-description {{
        color: {MUTED_TEXT_COLOR};
        font-size: 15px;
        margin-bottom: 18px;
    }}

    .dia-label {{
        font-size: 15px;
        font-weight: 700;
        color: {TEXT_COLOR};
        margin-bottom: 6px;
    }}


    /* -------------------------------------------------------
       NUMBER INPUT
    ------------------------------------------------------- */

    div[data-testid="stNumberInput"] input {{
        background: {INPUT_BACKGROUND} !important;
        color: {INPUT_TEXT_COLOR} !important;
        border: 1px solid {BORDER_COLOR} !important;
    }}

    div[data-testid="stNumberInput"] button {{
        background: {DIA_BUTTON_BACKGROUND} !important;
        color: {DIA_BUTTON_TEXT} !important;
        border-left: 1px solid #DDD6FE !important;
    }}


    /* -------------------------------------------------------
       BACK BUTTON
    ------------------------------------------------------- */

    .back-button button {{
        background: transparent !important;
        color: {TEXT_COLOR} !important;
        border: 1px solid {BORDER_COLOR} !important;
        box-shadow: none !important;
    }}


    /* -------------------------------------------------------
       SUCCESS MESSAGE
    ------------------------------------------------------- */

    .success-box {{
        background: #ECFDF5;
        border: 1px solid #A7F3D0;
        color: #065F46;
        border-radius: 12px;
        padding: 14px 16px;
        margin-top: 15px;
        font-weight: 600;
    }}


    /* -------------------------------------------------------
       MOBILE
    ------------------------------------------------------- */

    @media (max-width: 768px) {{

        .block-container {{
            padding: 1rem !important;
        }}

        .portal-title {{
            font-size: 32px;
        }}

        .portal-subtitle {{
            font-size: 15px;
        }}

        .portal-card {{
            padding: 20px;
            border-radius: 18px;
        }}

        .dia-heading {{
            font-size: 25px;
        }}
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="font-size:40px; margin-bottom:5px;">📁</div>
        <div class="sidebar-title">Data Export</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-description">
            Download the submitted contractor records.
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Download Data
    # --------------------------------------------------------

    empty_df = pd.DataFrame(
        columns=[
            "Panchayat",
            "Contractor Name",
            "RA Bill",
            "Vendor Code",
            "Work Date",
            "Scheme ID",
            "63 DIA",
            "75 DIA",
            "90 DIA",
            "110 DIA",
            "125 DIA",
            "140 DIA",
            "160 DIA",
            "180 DIA",
            "200 DIA"
        ]
    )

    csv_data = empty_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥  Download Data Sheet",
        data=csv_data,
        file_name="panchayat_contractor_records.csv",
        mime="text/csv"
    )


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "home":

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="portal-header">

            <div class="portal-icon">🏛️</div>

            <h1 class="portal-title">
                Grama Panchayat Portal
            </h1>

            <div class="portal-subtitle">
                Select your Grama Panchayat to continue
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Selection Card
    # --------------------------------------------------------

    st.markdown(
        '<div class="portal-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="field-label">Select Panchayat</div>',
        unsafe_allow_html=True
    )

    selected = st.selectbox(
        "Panchayat",
        ["-- Select Panchayat --"] + PANCHAYATS,
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Continue  ➜", key="continue_button"):

        if selected == "-- Select Panchayat --":

            st.warning("Please select a Panchayat before continuing.")

        else:

            st.session_state.selected_panchayat = selected
            st.session_state.page = "form"
            st.rerun()

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# FORM PAGE
# ============================================================

else:

    # --------------------------------------------------------
    # Back Button
    # --------------------------------------------------------

    st.markdown('<div class="back-button">', unsafe_allow_html=True)

    if st.button("←  Back to Panchayat Selection"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


    # --------------------------------------------------------
    # Selected Panchayat
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="portal-card">

            <div style="
                font-size:14px;
                color:{MUTED_TEXT_COLOR};
                margin-bottom:6px;
            ">
                Selected Panchayat
            </div>

            <div style="
                font-size:25px;
                font-weight:800;
                color:{TEXT_COLOR};
            ">
                📍 {st.session_state.selected_panchayat}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Main Form Card
    # --------------------------------------------------------

    st.markdown(
        '<div class="portal-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="form-heading">Contractor Details</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="form-description">
            Enter the contractor and work details below.
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Contractor Details
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        contractor_name = st.text_input(
            "Contractor Name",
            placeholder="Enter contractor name"
        )

        vendor_code = st.text_input(
            "Vendor Code",
            placeholder="Enter vendor code"
        )

        scheme_id = st.text_input(
            "Scheme ID",
            placeholder="Enter scheme ID"
        )


    with col2:

        ra_bill = st.text_input(
            "RA Bill",
            placeholder="Enter RA Bill number"
        )

        work_date = st.date_input(
            "Work Date",
            value=date.today()
        )


    # --------------------------------------------------------
    # DIA SECTION
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="dia-heading">
            📏 DIA Values
        </div>

        <div class="dia-description">
            Enter the quantity for each available DIA size.
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # DIA INPUTS
    # --------------------------------------------------------

    dia_values = {}

    dia_columns = st.columns(3)

    for index, dia in enumerate(DIA_SIZES):

        with dia_columns[index % 3]:

            dia_values[dia] = st.number_input(
                f"{dia} DIA",
                min_value=0,
                value=0,
                step=1,
                key=f"dia_{dia}"
            )


    # --------------------------------------------------------
    # Submit
    # --------------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "💾  Submit Details",
        key="submit_details"
    ):

        record = {
            "Panchayat": st.session_state.selected_panchayat,
            "Contractor Name": contractor_name,
            "RA Bill": ra_bill,
            "Vendor Code": vendor_code,
            "Work Date": str(work_date),
            "Scheme ID": scheme_id
        }

        for dia in DIA_SIZES:
            record[f"{dia} DIA"] = dia_values[dia]

        st.session_state.last_record = record

        st.markdown(
            """
            <div class="success-box">
                ✅ Contractor details submitted successfully.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )
