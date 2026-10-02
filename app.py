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
    initial_sidebar_state="expanded",
)

# ============================================================
# COLORS — matched to the reference image
# ============================================================
PRIMARY_COLOR = "#7C3AED"
SECONDARY_COLOR = "#EC4899"
BACKGROUND_COLOR = "#FFF9FC"
CARD_COLOR = "#FFFFFF"
TEXT_COLOR = "#111B44"
MUTED_TEXT_COLOR = "#59627D"
BORDER_COLOR = "#E3E4EE"
SIDEBAR_COLOR = "#FFFFFF"
SIDEBAR_TEXT_COLOR = "#17204A"
INPUT_BACKGROUND = "#FFFFFF"
INPUT_TEXT_COLOR = "#17204A"
DIA_BUTTON_BACKGROUND = "#FFF0FA"
DIA_BUTTON_TEXT = "#C21882"

# ============================================================
# DATA
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

DIA_SIZES = [63, 75, 90, 110, 125, 140, 160, 180, 200]

# ============================================================
# SESSION STATE
# ============================================================
if "selected_panchayat" not in st.session_state:
    st.session_state.selected_panchayat = None

if "page" not in st.session_state:
    st.session_state.page = "home"

if "records" not in st.session_state:
    st.session_state.records = []

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown(
    f"""
    <style>
    /* ========================= GLOBAL ========================= */
    html, body, [class*="css"] {{
        font-family: Inter, -apple-system, BlinkMacSystemFont,
        "Segoe UI", sans-serif;
    }}

    .stApp {{
        background:
            radial-gradient(circle at 92% 13%,
                rgba(236,72,153,.10), transparent 28%),
            radial-gradient(circle at 12% 78%,
                rgba(124,58,237,.045), transparent 30%),
            {BACKGROUND_COLOR};
        color: {TEXT_COLOR};
    }}

    .block-container {{
        padding-top: 0.9rem !important;
        padding-bottom: 2rem !important;
        max-width: 1180px !important;
    }}

    /* Remove Streamlit header/footer clutter */
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}

    footer {{
        visibility: hidden;
    }}

    /* ========================= SIDEBAR ========================= */
    section[data-testid="stSidebar"] {{
        background: {SIDEBAR_COLOR} !important;
        border-right: 1px solid #F0DDEA !important;
        min-width: 303px !important;
        width: 303px !important;
    }}

    section[data-testid="stSidebar"] > div {{
        background: {SIDEBAR_COLOR} !important;
        padding: 0 !important;
    }}

    section[data-testid="stSidebar"] * {{
        color: {SIDEBAR_TEXT_COLOR};
    }}

    /* Hide sidebar collapse button */
    button[data-testid="stSidebarCollapseButton"] {{
        display: none !important;
    }}

    .side-brand {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 23px 24px 18px 28px;
    }}

    .side-brand-icon {{
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
    }}

    .side-brand-title {{
        font-size: 16px;
        font-weight: 800;
        letter-spacing: -.35px;
        white-space: nowrap;
    }}

    .side-nav {{
        margin: 0 12px;
    }}

    .side-nav-item {{
        height: 40px;
        border-radius: 9px;
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 0 22px;
        margin-bottom: 8px;
        color: #C21882 !important;
        font-size: 14px;
        font-weight: 650;
    }}

    .side-nav-item.active {{
        background: linear-gradient(90deg, #FBE3F3, #F9D9ED);
    }}

    .side-nav-icon {{
        width: 20px;
        text-align: center;
        font-size: 19px;
    }}

    .side-tagline {{
        position: fixed;
        left: 28px;
        bottom: 62px;
        width: 245px;
        text-align: center;
        color: #DF5C9D !important;
        font-family: "Segoe Script", "Brush Script MT", cursive;
        font-size: 15px;
        line-height: 1.35;
        font-weight: 600;
    }}

    .side-tagline .heart {{
        display: block;
        margin: 2px auto 4px;
        font-family: Arial, sans-serif;
        font-size: 17px;
    }}

    .side-village {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 302px;
        height: 82px;
        overflow: hidden;
        pointer-events: none;
    }}

    .side-village .ground {{
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 15px;
        background: #F6C7DF;
        opacity: .65;
    }}

    .tree {{
        position: absolute;
        bottom: 12px;
        width: 18px;
        height: 43px;
        border-radius: 50% 50% 38% 38%;
        background: #F2A7CC;
        opacity: .70;
    }}

    .tree::after {{
        content: "";
        position: absolute;
        width: 3px;
        height: 30px;
        left: 8px;
        top: 34px;
        background: #D99ABF;
    }}

    .tree.t1 {{ left: 30px; transform: scale(.9); }}
    .tree.t2 {{ left: 58px; transform: scale(.65); bottom: 8px; }}
    .tree.t3 {{ left: 205px; transform: scale(.72); }}
    .tree.t4 {{ left: 248px; transform: scale(.95); }}
    .tree.t5 {{ left: 275px; transform: scale(.58); bottom: 9px; }}

    .house {{
        position: absolute;
        bottom: 12px;
        width: 35px;
        height: 24px;
        background: #F9D9EA;
        border-radius: 3px;
    }}

    .house::before {{
        content: "";
        position: absolute;
        left: -5px;
        top: -15px;
        width: 0;
        height: 0;
        border-left: 22px solid transparent;
        border-right: 22px solid transparent;
        border-bottom: 18px solid #EFA8C8;
    }}

    .house::after {{
        content: "";
        position: absolute;
        width: 7px;
        height: 13px;
        left: 14px;
        bottom: 0;
        background: #D88AB5;
    }}

    .house.h1 {{ left: 93px; }}
    .house.h2 {{ left: 139px; transform: scale(.78); bottom: 10px; }}
    .house.h3 {{ left: 177px; transform: scale(.6); bottom: 9px; }}

    /* Sidebar download button */
    div[data-testid="stSidebar"] .stDownloadButton {{
        margin: 3px 12px 0 12px;
    }}

    div[data-testid="stSidebar"] .stDownloadButton > button {{
        width: 100%;
        height: 40px;
        justify-content: flex-start !important;
        padding-left: 22px !important;
        border: 0 !important;
        background: transparent !important;
        color: #C21882 !important;
        border-radius: 9px !important;
        font-size: 14px !important;
        font-weight: 650 !important;
        box-shadow: none !important;
    }}

    div[data-testid="stSidebar"] .stDownloadButton > button:hover {{
        background: #FBE3F3 !important;
    }}

    /* ========================= TOP ACTIONS ========================= */
    .top-actions {{
        height: 38px;
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 19px;
        color: #17204A;
        font-size: 13px;
        margin-bottom: 3px;
    }}

    .top-action-icon {{
        font-size: 18px;
        color: #6E7590;
    }}

    .top-sun {{
        color: #E63D91;
        font-size: 18px;
    }}

    /* ========================= PORTAL HEADER ========================= */
    .portal-header {{
        display: flex;
        align-items: center;
        gap: 17px;
        padding: 5px 0 18px 5px;
    }}

    .portal-icon {{
        font-size: 42px;
        line-height: 1;
        filter: saturate(.85);
    }}

    .portal-title {{
        font-size: 31px;
        font-weight: 850;
        color: {TEXT_COLOR};
        margin: 0;
        letter-spacing: -.9px;
        line-height: 1.15;
    }}

    .portal-subtitle {{
        color: #17204A;
        font-size: 16px;
        margin-top: 7px;
    }}

    /* ========================= CARDS ========================= */
    .portal-card {{
        background: {CARD_COLOR};
        border: 1px solid #F1DCEB;
        border-radius: 17px;
        padding: 25px 27px 28px 27px;
        box-shadow: 0 12px 30px rgba(63, 35, 80, .055);
        margin: 6px 0 0 0;
    }}

    .home-card {{
        margin-left: 67px;
        margin-right: 67px;
        padding-top: 29px;
    }}

    .field-label {{
        color: {TEXT_COLOR};
        font-size: 14px;
        font-weight: 750;
        margin-bottom: 7px;
    }}

    /* ========================= SELECT ========================= */
    div[data-baseweb="select"] > div {{
        background: {INPUT_BACKGROUND} !important;
        color: {INPUT_TEXT_COLOR} !important;
        border: 1px solid #E7A9DF !important;
        border-radius: 10px !important;
        min-height: 45px !important;
        box-shadow: none !important;
    }}

    div[data-baseweb="select"] * {{
        color: {INPUT_TEXT_COLOR} !important;
    }}

    div[data-baseweb="popover"] {{
        background: #FFFFFF !important;
    }}

    div[role="option"] {{
        color: {INPUT_TEXT_COLOR} !important;
        background: #FFFFFF !important;
    }}

    div[role="option"]:hover {{
        background: #FCE9F6 !important;
    }}

    /* ========================= INPUTS ========================= */
    div[data-testid="stTextInput"] {{
        margin-bottom: 5px;
    }}

    div[data-testid="stTextInput"] label,
    div[data-testid="stDateInput"] label,
    div[data-testid="stNumberInput"] label {{
        color: {TEXT_COLOR} !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        margin-bottom: 5px !important;
    }}

    div[data-testid="stTextInput"] input {{
        background: #FFFFFF !important;
        color: {INPUT_TEXT_COLOR} !important;
        border: 1px solid #D9DCE8 !important;
        border-radius: 9px !important;
        min-height: 38px !important;
        font-size: 13px !important;
    }}

    div[data-testid="stTextInput"] input::placeholder {{
        color: #8990A8 !important;
    }}

    div[data-testid="stDateInput"] input {{
        background: #FFFFFF !important;
        color: {INPUT_TEXT_COLOR} !important;
        border: 1px solid #D9DCE8 !important;
        border-radius: 9px !important;
        min-height: 38px !important;
        font-size: 13px !important;
    }}

    div[data-testid="stDateInput"] button {{
        background: #FFFFFF !important;
        color: {TEXT_COLOR} !important;
    }}

    /* ========================= FORM ========================= */
    .form-card {{
        margin: 0 10px;
        padding: 19px 21px 20px 21px;
    }}

    .form-heading {{
        font-size: 14px;
        font-weight: 800;
        color: {TEXT_COLOR};
        margin-bottom: 7px;
    }}

    .form-description {{
        color: {MUTED_TEXT_COLOR};
        font-size: 12px;
        margin-bottom: 18px;
    }}

    .back-link {{
        display: inline-block;
        color: #C21882;
        font-size: 14px;
        font-weight: 650;
        margin: 2px 0 12px 12px;
    }}

    /* ========================= DIA ========================= */
    .dia-section {{
        margin-top: 5px;
    }}

    .dia-title-row {{
        display: flex;
        align-items: center;
        gap: 11px;
        border-bottom: 1px solid #EFC6DF;
        padding-bottom: 6px;
        margin-bottom: 10px;
    }}

    .dia-icon {{
        font-size: 23px;
    }}

    .dia-heading {{
        font-size: 21px;
        font-weight: 820;
        color: {TEXT_COLOR};
        margin: 0;
    }}

    .dia-description {{
        color: {MUTED_TEXT_COLOR};
        font-size: 12px;
        margin-bottom: 5px;
    }}

    div[data-testid="stNumberInput"] {{
        margin-bottom: 4px;
    }}

    div[data-testid="stNumberInput"] input {{
        background: #FFFFFF !important;
        color: {INPUT_TEXT_COLOR} !important;
        border: 1px solid #D9DCE8 !important;
        border-radius: 8px 0 0 8px !important;
        min-height: 34px !important;
        font-size: 12px !important;
    }}

    div[data-testid="stNumberInput"] button {{
        background: {DIA_BUTTON_BACKGROUND} !important;
        color: {DIA_BUTTON_TEXT} !important;
        border-left: 1px solid #F3C8E3 !important;
        min-height: 34px !important;
    }}

    /* ========================= BUTTONS ========================= */
    .stButton > button {{
        width: 100%;
        min-height: 47px;
        border-radius: 11px;
        border: none !important;
        background: linear-gradient(
            90deg, {PRIMARY_COLOR}, {SECONDARY_COLOR}
        ) !important;
        color: #FFFFFF !important;
        font-size: 15px;
        font-weight: 750;
        box-shadow: 0 8px 20px rgba(124,58,237,.18);
        transition: all .2s ease;
    }}

    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 11px 24px rgba(124,58,237,.23);
    }}

    .back-button > button {{
        width: auto !important;
        min-height: 30px !important;
        padding: 0 !important;
        border: 0 !important;
        background: transparent !important;
        color: #C21882 !important;
        box-shadow: none !important;
        font-size: 14px !important;
        font-weight: 650 !important;
    }}

    .back-button > button:hover {{
        transform: none !important;
        box-shadow: none !important;
    }}

    /* ========================= SUCCESS ========================= */
    .success-box {{
        background: #ECFDF5;
        border: 1px solid #A7F3D0;
        color: #065F46;
        border-radius: 10px;
        padding: 11px 14px;
        margin-top: 12px;
        font-size: 13px;
        font-weight: 650;
    }}

    /* ========================= MOBILE ========================= */
    @media (max-width: 900px) {{
        .block-container {{
            padding: 0.7rem !important;
        }}

        .home-card,
        .form-card {{
            margin-left: 0;
            margin-right: 0;
        }}

        .portal-title {{
            font-size: 26px;
        }}

        .portal-subtitle {{
            font-size: 14px;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(
        """
        <div class="side-brand">
            <div class="side-brand-icon">🏛️</div>
            <div class="side-brand-title">Grama Panchayat Portal</div>
        </div>

        <div class="side-nav">
            <div class="side-nav-item active">
                <span class="side-nav-icon">⌂</span>
                <span>Home</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
            "200 DIA",
        ]
    )

    if st.session_state.records:
        export_df = pd.DataFrame(st.session_state.records)
    else:
        export_df = empty_df

    csv_data = export_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⇩  Download Data Sheet",
        data=csv_data,
        file_name="panchayat_contractor_records.csv",
        mime="text/csv",
        key="download_data",
    )

    st.markdown(
        """
        <div class="side-tagline">
            Stronger Panchayats<br>
            Brighter Future
            <span class="heart">— ♥ —</span>
        </div>

        <div class="side-village">
            <div class="ground"></div>
            <div class="tree t1"></div>
            <div class="tree t2"></div>
            <div class="tree t3"></div>
            <div class="tree t4"></div>
            <div class="tree t5"></div>
            <div class="house h1"></div>
            <div class="house h2"></div>
            <div class="house h3"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# TOP RIGHT ACTIONS
# ============================================================
st.markdown(
    """
    <div class="top-actions">
        <span>Share</span>
        <span class="top-action-icon">♣</span>
        <span class="top-sun">☼</span>
        <span class="top-action-icon">⋮</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HOME PAGE
# ============================================================
if st.session_state.page == "home":

    st.markdown(
        """
        <div class="portal-header">
            <div class="portal-icon">🏛️</div>
            <div>
                <h1 class="portal-title">Grama Panchayat Portal</h1>
                <div class="portal-subtitle">
                    Select your Grama Panchayat to continue
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="portal-card home-card">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="field-label">Select Panchayat</div>',
        unsafe_allow_html=True,
    )

    selected = st.selectbox(
        "Panchayat",
        ["-- Select Panchayat --"] + PANCHAYATS,
        label_visibility="collapsed",
        key="panchayat_select",
    )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    if st.button("Continue  →", key="continue_button"):
        if selected == "-- Select Panchayat --":
            st.warning("Please select a Panchayat before continuing.")
        else:
            st.session_state.selected_panchayat = selected
            st.session_state.page = "form"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# FORM PAGE
# ============================================================
else:

    st.markdown('<div class="back-button">', unsafe_allow_html=True)

    if st.button("←  Back", key="back_button"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="portal-card form-card">',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="1.3rem")

    with col1:
        contractor_name = st.text_input(
            "Contractor Name",
            placeholder="Enter contractor name",
        )

        vendor_code = st.text_input(
            "Vendor Code",
            placeholder="Enter vendor code",
        )

        scheme_id = st.text_input(
            "Scheme ID",
            placeholder="Enter scheme ID",
        )

    with col2:
        ra_bill = st.text_input(
            "RA Bill",
            placeholder="Enter RA Bill number",
        )

        work_date = st.date_input(
            "Work Date",
            value=date.today(),
        )

    st.markdown(
        """
        <div class="dia-section">
            <div class="dia-title-row">
                <span class="dia-icon">📏</span>
                <h2 class="dia-heading">DIA Values</h2>
            </div>
            <div class="dia-description">
                Enter the quantity for each available DIA size.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    dia_values = {}
    dia_columns = st.columns(3, gap="1.6rem")

    for index, dia in enumerate(DIA_SIZES):
        with dia_columns[index % 3]:
            dia_values[dia] = st.number_input(
                f"{dia} DIA",
                min_value=0,
                value=0,
                step=1,
                key=f"dia_{dia}",
            )

    st.markdown("<div style='height:7px'></div>", unsafe_allow_html=True)

    if st.button("▣  Submit Details", key="submit_details"):
        record = {
            "Panchayat": st.session_state.selected_panchayat,
            "Contractor Name": contractor_name,
            "RA Bill": ra_bill,
            "Vendor Code": vendor_code,
            "Work Date": str(work_date),
            "Scheme ID": scheme_id,
        }

        for dia in DIA_SIZES:
            record[f"{dia} DIA"] = dia_values[dia]

        st.session_state.records.append(record)

        st.markdown(
            """
            <div class="success-box">
                ✓ Contractor details submitted successfully.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
