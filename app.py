import streamlit as st
import pandas as pd
import os
from datetime import date

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
# COLORS
# Change ONLY these values if you want another color theme
# ============================================================

PRIMARY = "#7C3AED"
PRIMARY_DARK = "#5B21B6"

PINK = "#EC4899"
PINK_DARK = "#DB2777"

LIGHT_PINK = "#FCE7F3"
VERY_LIGHT_PINK = "#FFF7FB"

LIGHT_PURPLE = "#F3E8FF"

TEXT = "#172554"
TEXT_SECONDARY = "#64748B"

WHITE = "#FFFFFF"

BORDER = "#E5D9EA"

INPUT_BORDER = "#D8DCE8"

SHADOW = "rgba(124, 58, 237, 0.08)"


# ============================================================
# PANCHAYAT DATA
# Replace this list with your complete original list
# ============================================================

PANCHAYATS = [
    "Aspurdevasda",
    "Aaurain",
    "Atrampur & Turkoli",
    "Baejalpur",
    "BANBIRPUR",
    "Behla & Bijhala",
    "Bhaiswal",
    "Bhamrauli",
    "Bhitaura",
    "Chandpur",
    "Chhata",
    "Dariyapur",
    "Dharampur",
    "Dibiyapur",
    "Durgapur",
    "Fatehpur",
    "Gopalpur",
    "Haripur",
    "Jalalpur",
    "Kalyanpur",
    "Lakshmipur",
    "Mahadevpur",
    "Nandpur",
    "Rampur",
    "Shahpur",
    "Sultanpur"
]


# ============================================================
# DIA VALUES
# ============================================================

DIA_COLUMNS = [
    "63DIA",
    "75 DIA",
    "90 DIA",
    "110 DIA",
    "125 DIA",
    "140 DIA",
    "160 DIA",
    "180 DIA",
    "200 DIA"
]


# ============================================================
# EXCEL FILE
# ============================================================

EXCEL_FILE = "contractor_data.xlsx"

if not os.path.exists(EXCEL_FILE):

    columns = [
        "DATE",
        "RA BILL",
        "VENDOR CODE",
        "NAME OF THE CONTRACTOR",
        "SCHEME ID",
        "PANCHAYAT",
        "TYPE"
    ] + DIA_COLUMNS

    pd.DataFrame(columns=columns).to_excel(
        EXCEL_FILE,
        index=False
    )


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_panchayat" not in st.session_state:
    st.session_state.selected_panchayat = ""


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
<style>

/* =========================================================
   GLOBAL
   ========================================================= */

html, body, [class*="css"] {{
    font-family: "Segoe UI", Arial, sans-serif !important;
}}

.stApp {{
    background:
        radial-gradient(
            circle at 80% 15%,
            rgba(236,72,153,0.10),
            transparent 30%
        ),
        radial-gradient(
            circle at 20% 85%,
            rgba(124,58,237,0.06),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #FFFFFF 0%,
            #FFF9FC 45%,
            #FFF1F8 100%
        ) !important;

    color: {TEXT} !important;
}}


/* Remove Streamlit top spacing */

header[data-testid="stHeader"] {{
    background: transparent !important;
}}


/* Main container */

.block-container {{
    max-width: 1100px !important;

    padding-top: 25px !important;
    padding-bottom: 60px !important;
}}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {{
    background: {WHITE} !important;

    border-right:
        1px solid #F0DCE8 !important;
}}


section[data-testid="stSidebar"] > div {{
    background: {WHITE} !important;
}}


/* Sidebar title */

.sidebar-brand {{
    display: flex;

    align-items: center;

    gap: 12px;

    margin-top: 8px;

    margin-bottom: 28px;
}}


.sidebar-building {{
    font-size: 31px;

    line-height: 1;

    background:
        linear-gradient(
            135deg,
            {PINK},
            {PRIMARY}
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}}


.sidebar-brand-text {{
    font-size: 17px;

    font-weight: 800;

    color: {TEXT};
}}


/* Sidebar menu */

.sidebar-home {{
    display: flex;

    align-items: center;

    gap: 13px;

    padding: 11px 14px;

    border-radius: 9px;

    background:
        linear-gradient(
            90deg,
            #FCE7F3,
            #FCEAF5
        );

    color: {PINK_DARK};

    font-size: 14px;

    font-weight: 700;

    margin-bottom: 8px;
}}


.sidebar-download {{
    display: flex;

    align-items: center;

    gap: 13px;

    padding: 11px 14px;

    color: {PINK_DARK};

    font-size: 14px;

    font-weight: 600;
}}


/* Actual Streamlit download button */

section[data-testid="stSidebar"]
div[data-testid="stDownloadButton"] button {{

    background: transparent !important;

    border: none !important;

    box-shadow: none !important;

    color: {PINK_DARK} !important;

    -webkit-text-fill-color: {PINK_DARK} !important;

    font-size: 14px !important;

    font-weight: 600 !important;

    padding: 8px 14px !important;

    text-align: left !important;

    justify-content: flex-start !important;
}}


section[data-testid="stSidebar"]
div[data-testid="stDownloadButton"] button:hover {{

    background: {LIGHT_PINK} !important;

    border-radius: 8px !important;

    color: {PINK_DARK} !important;
}}


section[data-testid="stSidebar"]
div[data-testid="stDownloadButton"] button span {{

    color: {PINK_DARK} !important;

    -webkit-text-fill-color: {PINK_DARK} !important;
}}


/* =========================================================
   SIDEBAR BOTTOM ILLUSTRATION
   ========================================================= */

.sidebar-bottom-art {{

    position: fixed;

    bottom: 0;

    left: 0;

    width: 300px;

    text-align: center;

    pointer-events: none;

}}


.sidebar-tagline {{

    font-family: Georgia, serif;

    font-style: italic;

    font-size: 15px;

    line-height: 1.4;

    color: {PINK};

    margin-bottom: 8px;
}}


.village-art {{

    font-size: 52px;

    letter-spacing: -8px;

    opacity: 0.85;
}}


/* =========================================================
   MAIN HEADER
   ========================================================= */

.main-header {{

    display: flex;

    align-items: center;

    gap: 18px;

    margin-top: 5px;

    margin-bottom: 28px;
}}


.main-building {{

    width: 62px;

    height: 62px;

    border-radius: 16px;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 39px;

    background:
        linear-gradient(
            135deg,
            #F3E8FF,
            #FCE7F3
        );

    box-shadow:
        0 8px 20px
        rgba(124,58,237,0.10);
}}


.main-title {{

    font-size: 36px;

    line-height: 1.1;

    font-weight: 850;

    letter-spacing: -0.8px;

    color: {TEXT};
}}


.main-subtitle {{

    margin-top: 6px;

    font-size: 16px;

    color: {TEXT_SECONDARY};
}}


/* =========================================================
   MAIN CARD
   ========================================================= */

.portal-card {{

    background:
        rgba(255,255,255,0.96);

    border:
        1px solid {BORDER};

    border-radius:
        20px;

    padding:
        30px;

    box-shadow:
        0 15px 45px
        {SHADOW};
}}


/* =========================================================
   LABELS
   ========================================================= */

[data-testid="stWidgetLabel"] label {{

    color: {TEXT} !important;

    font-size: 14px !important;

    font-weight: 700 !important;
}}


/* =========================================================
   SELECT BOX
   ========================================================= */

div[data-baseweb="select"] > div {{

    background:
        {WHITE} !important;

    border:
        1.5px solid
        #E9A8D2 !important;

    border-radius:
        10px !important;

    min-height:
        44px !important;
}}


div[data-baseweb="select"] span {{

    color:
        {TEXT} !important;

    -webkit-text-fill-color:
        {TEXT} !important;
}}


div[data-baseweb="select"] svg {{

    fill:
        {TEXT} !important;
}}


/* Dropdown popup */

div[data-baseweb="popover"] > div {{
    background: {WHITE} !important;
}}


div[data-baseweb="menu"] {{
    background: {WHITE} !important;
}}


ul[role="listbox"] {{
    background: {WHITE} !important;
}}


li[role="option"] {{
    background: {WHITE} !important;

    color: {TEXT} !important;

    -webkit-text-fill-color: {TEXT} !important;

    font-size: 14px !important;

    padding: 10px 14px !important;
}}


li[role="option"]:hover {{
    background: {LIGHT_PINK} !important;

    color: {PINK_DARK} !important;
}}


/* =========================================================
   TEXT INPUT
   ========================================================= */

div[data-baseweb="input"] {{

    background:
        {WHITE} !important;

    border:
        1.5px solid
        {INPUT_BORDER} !important;

    border-radius:
        9px !important;
}}


div[data-baseweb="input"]:focus-within {{

    border-color:
        #C084FC !important;

    box-shadow:
        0 0 0 3px
        rgba(192,132,252,0.10)
        !important;
}}


input {{

    color:
        {TEXT} !important;

    -webkit-text-fill-color:
        {TEXT} !important;

    background:
        {WHITE} !important;
}}


input::placeholder {{

    color:
        #94A3B8 !important;

    -webkit-text-fill-color:
        #94A3B8 !important;
}}


/* =========================================================
   DATE INPUT
   ========================================================= */

div[data-testid="stDateInput"]
div[data-baseweb="input"] {{

    background:
        {WHITE} !important;

    border:
        1.5px solid
        {INPUT_BORDER} !important;

    border-radius:
        9px !important;
}}


div[data-testid="stDateInput"] input {{

    background:
        {WHITE} !important;

    color:
        {TEXT} !important;

    -webkit-text-fill-color:
        {TEXT} !important;
}}


div[data-testid="stDateInput"] button {{

    background:
        {WHITE} !important;

    border:
        none !important;
}}


div[data-testid="stDateInput"] svg {{

    fill:
        {TEXT} !important;
}}


/* =========================================================
   DIA HEADER
   ========================================================= */

.dia-header {{

    display: flex;

    align-items: center;

    gap: 10px;

    margin-top: 25px;

    margin-bottom: 5px;
}}


.dia-icon {{

    font-size: 27px;

    color: {PINK};
}}


.dia-title {{

    font-size: 25px;

    font-weight: 850;

    color: {TEXT};
}}


.dia-line {{

    flex: 1;

    height: 1px;

    background:
        linear-gradient(
            90deg,
            #F5B7D9,
            #F9DCEA
        );

    margin-left: 10px;
}}


.dia-description {{

    font-size: 13px;

    color: {TEXT_SECONDARY};

    margin-bottom: 14px;
}}


/* =========================================================
   NUMBER INPUT
   ========================================================= */

div[data-testid="stNumberInput"] div[data-baseweb="input"] {{

    border-radius:
        8px !important;
}}


button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"] {{

    background:
        #FDF0F8 !important;

    border:
        1px solid
        #F4D3E5 !important;

    color:
        {PINK_DARK} !important;
}}


button[data-testid="stNumberInputStepDown"] svg,
button[data-testid="stNumberInputStepUp"] svg {{

    fill:
        {PINK_DARK} !important;
}}


/* =========================================================
   PRIMARY BUTTON
   ========================================================= */

.stButton > button,
[data-testid="stFormSubmitButton"] button {{

    background:
        linear-gradient(
            90deg,
            {PRIMARY},
            {PINK}
        ) !important;

    border:
        none !important;

    color:
        white !important;

    -webkit-text-fill-color:
        white !important;

    min-height:
        48px !important;

    border-radius:
        10px !important;

    font-weight:
        800 !important;

    font-size:
        15px !important;

    box-shadow:
        0 10px 24px
        rgba(219,39,119,0.18) !important;
}}


.stButton > button:hover,
[data-testid="stFormSubmitButton"] button:hover {{

    filter:
        brightness(0.97);

    transform:
        translateY(-1px);
}}


/* =========================================================
   BACK BUTTON
   ========================================================= */

.back-button button {{

    background:
        transparent !important;

    color:
        {PINK_DARK} !important;

    -webkit-text-fill-color:
        {PINK_DARK} !important;

    border:
        none !important;

    box-shadow:
        none !important;

    padding:
        0 !important;

    min-height:
        30px !important;

    font-size:
        14px !important;
}}


/* =========================================================
   INFO MESSAGE
   ========================================================= */

div[data-testid="stAlert"] {{

    border-radius:
        10px !important;

    border:
        1px solid #E9D5FF !important;

    background:
        #FAF5FF !important;

    color:
        {TEXT} !important;
}}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media(max-width: 900px) {{

    .main-title {{
        font-size: 28px;
    }}

    .main-building {{
        width: 52px;
        height: 52px;
        font-size: 31px;
    }}

    .portal-card {{
        padding: 20px;
    }}

    .sidebar-bottom-art {{
        display: none;
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

    # Brand
    st.markdown(
        """
        <div class="sidebar-brand">

            <div class="sidebar-building">
                🏛️
            </div>

            <div class="sidebar-brand-text">
                Grama Panchayat Portal
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # Home
    st.markdown(
        """
        <div class="sidebar-home">
            🏠
            <span>Home</span>
        </div>
        """,
        unsafe_allow_html=True
    )


    # Download
    if os.path.exists(EXCEL_FILE):

        with open(EXCEL_FILE, "rb") as f:

            st.download_button(
                label="⬇  Download Data Sheet",
                data=f,
                file_name="contractor_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


    # Bottom illustration
    st.markdown(
        """
        <div class="sidebar-bottom-art">

            <div class="sidebar-tagline">
                Stronger Panchayats<br>
                Brighter Future
                <br>
                ── ♥ ──
            </div>

            <div class="village-art">
                🌳 🏠 🌳 🏡 🌳
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PAGE 1 — PANCHAYAT SELECTION
# ============================================================

if st.session_state.page == "home":

    # Header
    st.markdown(
        """
        <div class="main-header">

            <div class="main-building">
                🏛️
            </div>

            <div>

                <div class="main-title">
                    Grama Panchayat Portal
                </div>

                <div class="main-subtitle">
                    Select your Grama Panchayat to continue
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # Card start
    st.markdown(
        '<div class="portal-card">',
        unsafe_allow_html=True
    )


    # Label
    st.markdown(
        """
        <div style="
            font-size:15px;
            font-weight:800;
            color:#172554;
            margin-bottom:8px;
        ">
            Select Panchayat
        </div>
        """,
        unsafe_allow_html=True
    )


    selected = st.selectbox(
        "Select Panchayat",
        ["-- Select Panchayat --"] + PANCHAYATS,
        label_visibility="collapsed"
    )


    st.markdown(
        "<div style='height:18px'></div>",
        unsafe_allow_html=True
    )


    if st.button(
        "Continue  →",
        use_container_width=True
    ):

        if selected == "-- Select Panchayat --":

            st.warning(
                "Please select a Panchayat before continuing."
            )

        else:

            st.session_state.selected_panchayat = selected

            st.session_state.page = "details"

            st.rerun()


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# PAGE 2 — CONTRACTOR DETAILS
# ============================================================

else:

    # Back
    st.markdown(
        '<div class="back-button">',
        unsafe_allow_html=True
    )

    if st.button("←  Back"):

        st.session_state.page = "home"

        st.rerun()

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # Selected Panchayat
    st.markdown(
        f"""
        <div style="
            margin-bottom:15px;
            font-size:14px;
            color:#64748B;
        ">
            Selected Panchayat:
            <strong style="color:#172554;">
                {st.session_state.selected_panchayat}
            </strong>
        </div>
        """,
        unsafe_allow_html=True
    )


    # Main form card
    st.markdown(
        '<div class="portal-card">',
        unsafe_allow_html=True
    )


    with st.form("contractor_form"):

        # ====================================================
        # TOP FIELDS
        # ====================================================

        col1, col2 = st.columns(
            2,
            gap="large"
        )


        with col1:

            contractor_name = st.text_input(
                "Contractor Name",
                placeholder="Enter contractor name"
            )


        with col2:

            ra_bill = st.text_input(
                "RA Bill",
                placeholder="Enter RA Bill number"
            )


        col3, col4 = st.columns(
            2,
            gap="large"
        )


        with col3:

            vendor_code = st.text_input(
                "Vendor Code",
                placeholder="Enter vendor code"
            )


        with col4:

            work_date = st.date_input(
                "Work Date",
                value=date.today()
            )


        col5, col6 = st.columns(
            2,
            gap="large"
        )


        with col5:

            scheme_id = st.text_input(
                "Scheme ID",
                placeholder="Enter scheme ID"
            )


        # ====================================================
        # DIA SECTION
        # ====================================================

        st.markdown(
            """
            <div class="dia-header">

                <div class="dia-icon">
                    📏
                </div>

                <div class="dia-title">
                    DIA Values
                </div>

                <div class="dia-line"></div>

            </div>

            <div class="dia-description">
                Enter the quantity for each available DIA size.
            </div>
            """,
            unsafe_allow_html=True
        )


        # ====================================================
        # DIA GRID
        # ====================================================

        dia_values = {}

        row1 = st.columns(3, gap="large")

        for i in range(3):

            with row1[i]:

                dia = DIA_COLUMNS[i]

                dia_values[dia] = st.number_input(
                    dia,
                    min_value=0,
                    value=0,
                    step=1,
                    key=f"dia_{i}"
                )


        row2 = st.columns(3, gap="large")

        for i in range(3):

            with row2[i]:

                dia = DIA_COLUMNS[i + 3]

                dia_values[dia] = st.number_input(
                    dia,
                    min_value=0,
                    value=0,
                    step=1,
                    key=f"dia_{i+3}"
                )


        row3 = st.columns(3, gap="large")

        for i in range(3):

            with row3[i]:

                dia = DIA_COLUMNS[i + 6]

                dia_values[dia] = st.number_input(
                    dia,
                    min_value=0,
                    value=0,
                    step=1,
                    key=f"dia_{i+6}"
                )


        st.markdown(
            "<div style='height:10px'></div>",
            unsafe_allow_html=True
        )


        # ====================================================
        # SUBMIT
        # ====================================================

        submitted = st.form_submit_button(
            "💾  Submit Details",
            use_container_width=True
        )


        # ====================================================
        # SAVE DATA
        # ====================================================

        if submitted:

            if not contractor_name.strip():

                st.error(
                    "Please enter Contractor Name."
                )

            elif not ra_bill.strip():

                st.error(
                    "Please enter RA Bill."
                )

            elif not vendor_code.strip():

                st.error(
                    "Please enter Vendor Code."
                )

            elif not scheme_id.strip():

                st.error(
                    "Please enter Scheme ID."
                )

            else:

                df = pd.read_excel(
                    EXCEL_FILE
                )


                new_row = {

                    "DATE":
                        work_date.strftime(
                            "%d-%m-%Y"
                        ),

                    "RA BILL":
                        ra_bill.strip(),

                    "VENDOR CODE":
                        vendor_code.strip(),

                    "NAME OF THE CONTRACTOR":
                        contractor_name.strip(),

                    "SCHEME ID":
                        scheme_id.strip(),

                    "PANCHAYAT":
                        st.session_state.selected_panchayat,

                    "TYPE":
                        "this_bill"
                }


                for dia in DIA_COLUMNS:

                    new_row[dia] = dia_values[dia]


                new_data = pd.DataFrame(
                    [new_row]
                )


                df = pd.concat(
                    [
                        df,
                        new_data
                    ],
                    ignore_index=True
                )


                df.to_excel(
                    EXCEL_FILE,
                    index=False
                )


                st.success(
                    "Details submitted successfully!"
                )

                st.balloons()


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )
