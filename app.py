import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Grama Panchayat Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 🎨 COLOR SETTINGS
# =========================================================
# Future lo colors change cheyyali ante ikkada maatrame change cheyyi

APP_BG = "#FFF9FC"
WHITE = "#FFFFFF"

PRIMARY = "#7C3AED"
SECONDARY = "#EC4899"

PRIMARY_LIGHT = "#F3E8FF"
PINK_LIGHT = "#FCE7F3"

TEXT = "#14213D"
TEXT_LIGHT = "#667085"

BORDER = "#E7DFF0"
BORDER_FOCUS = "#C084FC"

SIDEBAR_BG = "#FFFFFF"

SUCCESS_BG = "#ECFDF3"
SUCCESS_TEXT = "#027A48"

ERROR_BG = "#FEF3F2"
ERROR_TEXT = "#B42318"


# =========================================================
# EXCEL FILE
# =========================================================

EXCEL_FILE = "contractor_data.xlsx"


# =========================================================
# DIA COLUMNS
# =========================================================

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


# =========================================================
# PANCHAYAT LIST
# =========================================================

PANCHAYATS = [
    "Aspurdevasda",
    "Aaurain",
    "Atrampur & Turkoli",
    "Baejalpur",
    "BANBIRPUR",
    "Behla & Bijhala",
    "Bhaiswal",
    "Bhamrauli",
    "Bhawanipur",
    "Bhitaura",
    "Chak",
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


# =========================================================
# CREATE EXCEL IF NOT EXISTS
# =========================================================

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

    empty_df = pd.DataFrame(columns=columns)

    empty_df.to_excel(
        EXCEL_FILE,
        index=False
    )


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_panchayat" not in st.session_state:
    st.session_state.selected_panchayat = ""


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    f"""
<style>

/* =====================================================
   GLOBAL
   ===================================================== */

.stApp {{
    background:
        radial-gradient(
            circle at 85% 15%,
            rgba(236, 72, 153, 0.08),
            transparent 25%
        ),
        radial-gradient(
            circle at 15% 80%,
            rgba(124, 58, 237, 0.06),
            transparent 25%
        ),
        {APP_BG};

    color: {TEXT};
}}


header[data-testid="stHeader"] {{
    background: transparent !important;
}}


.block-container {{
    max-width: 1180px !important;

    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
}}


/* =====================================================
   FONT
   ===================================================== */

* {{
    font-family:
        "Segoe UI",
        Arial,
        sans-serif !important;
}}


/* =====================================================
   SIDEBAR
   ===================================================== */

section[data-testid="stSidebar"] {{
    background: {SIDEBAR_BG} !important;

    border-right:
        1px solid {BORDER} !important;
}}


section[data-testid="stSidebar"] > div {{
    background: {SIDEBAR_BG} !important;
}}


/* Sidebar Logo */

.sidebar-logo {{
    width: 48px;
    height: 48px;

    border-radius: 14px;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        linear-gradient(
            135deg,
            {PRIMARY},
            {SECONDARY}
        );

    color: white !important;

    font-size: 24px;

    box-shadow:
        0 8px 20px
        rgba(124,58,237,0.18);
}}


.sidebar-title {{
    font-size: 18px;

    font-weight: 800;

    color: {TEXT} !important;
}}


.sidebar-description {{
    margin-top: 8px;

    font-size: 13px;

    line-height: 1.6;

    color: {TEXT_LIGHT} !important;
}}


/* =====================================================
   DOWNLOAD BUTTON
   ONLY TEXT — NO BLACK BOX
   ===================================================== */

section[data-testid="stSidebar"]
.stDownloadButton
> button {{

    background: transparent !important;

    border: none !important;

    box-shadow: none !important;

    color: {SECONDARY} !important;

    -webkit-text-fill-color:
        {SECONDARY} !important;

    font-weight: 700 !important;

    padding:
        8px 0 !important;

    justify-content:
        flex-start !important;
}}


section[data-testid="stSidebar"]
.stDownloadButton
> button:hover {{

    background:
        {PINK_LIGHT} !important;

    border-radius: 8px !important;

    box-shadow: none !important;
}}


section[data-testid="stSidebar"]
.stDownloadButton
> button * {{

    color:
        {SECONDARY} !important;

    -webkit-text-fill-color:
        {SECONDARY} !important;
}}


/* =====================================================
   MAIN HEADER
   ===================================================== */

.portal-header {{

    display: flex;

    align-items: center;

    gap: 18px;

    margin-top: 25px;

    margin-bottom: 8px;
}}


.portal-icon {{

    width: 65px;

    height: 65px;

    border-radius: 18px;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        linear-gradient(
            135deg,
            {PRIMARY_LIGHT},
            {PINK_LIGHT}
        );

    font-size: 35px;

    box-shadow:
        0 10px 25px
        rgba(124,58,237,0.08);
}}


.portal-title {{

    font-size: 42px;

    line-height: 1.1;

    font-weight: 850;

    letter-spacing: -1px;

    color: {TEXT} !important;
}}


.portal-subtitle {{

    margin-top: 7px;

    font-size: 17px;

    color: {TEXT_LIGHT} !important;
}}


/* =====================================================
   MAIN CARD
   ===================================================== */

.portal-card {{

    margin-top: 30px;

    background: {WHITE};

    border:
        1px solid {BORDER};

    border-radius: 22px;

    padding: 30px;

    box-shadow:
        0 18px 45px
        rgba(38,24,57,0.07);
}}


/* =====================================================
   LABELS
   ===================================================== */

[data-testid="stWidgetLabel"] label {{

    color: {TEXT} !important;

    font-weight: 700 !important;
}}


/* =====================================================
   TEXT INPUT
   ===================================================== */

div[data-baseweb="input"] {{

    background:
        {WHITE} !important;

    border:
        1.5px solid
        {BORDER} !important;

    border-radius:
        10px !important;

    box-shadow:
        none !important;
}}


div[data-baseweb="input"]:focus-within {{

    border-color:
        {BORDER_FOCUS} !important;

    box-shadow:
        0 0 0 3px
        rgba(192,132,252,0.13)
        !important;
}}


input {{

    background:
        {WHITE} !important;

    color:
        {TEXT} !important;

    -webkit-text-fill-color:
        {TEXT} !important;
}}


input::placeholder {{

    color:
        #98A2B3 !important;

    -webkit-text-fill-color:
        #98A2B3 !important;
}}


/* =====================================================
   SELECTBOX
   ===================================================== */

div[data-baseweb="select"]
> div {{

    background:
        {WHITE} !important;

    border:
        1.5px solid
        #E8B9D4 !important;

    border-radius:
        10px !important;
}}


div[data-baseweb="select"] * {{

    color:
        {TEXT} !important;

    -webkit-text-fill-color:
        {TEXT} !important;
}}


div[data-baseweb="select"] svg {{

    fill:
        {TEXT} !important;
}}


/* =====================================================
   DROPDOWN POPUP
   IMPORTANT FIX FOR YOUR SCREENSHOT
   ===================================================== */

div[data-baseweb="popover"] {{

    background:
        {WHITE} !important;

    opacity:
        1 !important;
}}


div[data-baseweb="popover"] > div {{

    background:
        {WHITE} !important;
}}


div[data-baseweb="menu"] {{

    background:
        {WHITE} !important;
}}


ul[role="listbox"] {{

    background:
        {WHITE} !important;
}}


li[role="option"] {{

    background:
        {WHITE} !important;

    color:
        {TEXT} !important;

    -webkit-text-fill-color:
        {TEXT} !important;

    padding:
        10px 14px !important;
}}


li[role="option"]:hover {{

    background:
        {PINK_LIGHT} !important;

    color:
        #BE185D !important;
}}


li[aria-selected="true"] {{

    background:
        {PRIMARY_LIGHT} !important;

    color:
        {PRIMARY} !important;
}}


/* =====================================================
   DATE INPUT
   WHITE BACKGROUND + BLACK TEXT
   ===================================================== */

div[data-testid="stDateInput"]
div[data-baseweb="input"] {{

    background:
        {WHITE} !important;

    border:
        1.5px solid
        {BORDER} !important;

    box-shadow:
        none !important;
}}


div[data-testid="stDateInput"]
input {{

    background:
        {WHITE} !important;

    color:
        {TEXT} !important;

    -webkit-text-fill-color:
        {TEXT} !important;
}}


div[data-testid="stDateInput"]
button {{

    background:
        {WHITE} !important;

    border:
        none !important;
}}


div[data-testid="stDateInput"]
svg {{

    fill:
        {TEXT} !important;
}}


/* =====================================================
   DIA SECTION
   ===================================================== */

.dia-section {{

    margin-top: 30px;

    padding-top: 25px;

    border-top:
        1px solid #F1E7EF;
}}


.dia-heading {{

    display: flex;

    align-items: center;

    gap: 12px;
}}


.dia-icon {{

    font-size: 28px;
}}


.dia-title {{

    font-size: 27px;

    font-weight: 850;

    color:
        {TEXT} !important;
}}


.dia-description {{

    margin-top: 5px;

    margin-bottom: 20px;

    font-size: 14px;

    color:
        {TEXT_LIGHT} !important;
}}


/* =====================================================
   NUMBER INPUT
   ===================================================== */

div[data-testid="stNumberInput"]
div[data-baseweb="input"] {{

    border-radius:
        10px 0 0 10px !important;
}}


button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"] {{

    background:
        #FFF0F8 !important;

    border:
        1px solid
        #F1C7DF !important;

    color:
        #C0268D !important;
}}


button[data-testid="stNumberInputStepDown"] svg,
button[data-testid="stNumberInputStepUp"] svg {{

    fill:
        #C0268D !important;
}}


/* =====================================================
   PRIMARY BUTTON
   ===================================================== */

.stButton > button,
[data-testid="stFormSubmitButton"] > button {{

    background:
        linear-gradient(
            90deg,
            {PRIMARY},
            {SECONDARY}
        ) !important;

    color:
        #FFFFFF !important;

    -webkit-text-fill-color:
        #FFFFFF !important;

    border:
        none !important;

    border-radius:
        11px !important;

    min-height:
        48px !important;

    font-weight:
        800 !important;

    box-shadow:
        0 10px 25px
        rgba(217,70,239,0.20) !important;
}}


.stButton > button:hover,
[data-testid="stFormSubmitButton"]
> button:hover {{

    transform:
        translateY(-1px);

    filter:
        brightness(0.98);
}}


/* =====================================================
   INFO / SUCCESS
   ===================================================== */

div[data-testid="stAlert"] {{

    border-radius:
        12px !important;
}}


/* =====================================================
   RESPONSIVE
   ===================================================== */

@media(max-width: 900px) {{

    .portal-title {{
        font-size: 30px;
    }}

    .portal-icon {{
        width: 52px;
        height: 52px;
        font-size: 28px;
    }}

    .portal-card {{
        padding: 20px;
    }}

}}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            display:flex;
            align-items:center;
            gap:12px;
            margin-bottom:8px;
        ">

            <div class="sidebar-logo">
                🏛️
            </div>

            <div class="sidebar-title">
                Data Export
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-description">

            Download the submitted contractor
            records from the portal.

        </div>
        """,
        unsafe_allow_html=True
    )

    if os.path.exists(EXCEL_FILE):

        with open(EXCEL_FILE, "rb") as file:

            st.download_button(
                "📥  Download Data Sheet",
                data=file,
                file_name="contractor_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


# =========================================================
# PAGE 1
# PANCHAYAT SELECTION
# =========================================================

if st.session_state.page == "home":

    st.markdown(
        """
        <div class="portal-header">

            <div class="portal-icon">
                🏛️
            </div>

            <div>

                <div class="portal-title">
                    Grama Panchayat Portal
                </div>

                <div class="portal-subtitle">
                    Select your Grama Panchayat to continue
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="portal-card">',
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div style="
            font-size:16px;
            font-weight:700;
            margin-bottom:10px;
        ">
            Select Panchayat
        </div>
        """,
        unsafe_allow_html=True
    )


    selected = st.selectbox(
        "Panchayat",
        ["-- Select Panchayat --"] + PANCHAYATS,
        label_visibility="collapsed"
    )


    st.write("")


    if st.button(
        "Continue  ➜",
        use_container_width=True
    ):

        if selected == "-- Select Panchayat --":

            st.error(
                "Please select a Panchayat before continuing."
            )

        else:

            st.session_state.selected_panchayat = selected

            st.session_state.page = "details"

            st.rerun()


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# PAGE 2
# CONTRACTOR DETAILS
# =========================================================

else:

    # -----------------------------------------------------
    # BACK
    # -----------------------------------------------------

    if st.button("← Back"):

        st.session_state.page = "home"

        st.rerun()


    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="portal-header"
             style="margin-top:8px;">

            <div class="portal-icon">
                📋
            </div>

            <div>

                <div class="portal-title">
                    Contractor Details
                </div>

                <div class="portal-subtitle">
                    Enter contractor and DIA information
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # SELECTED PANCHAYAT
    # -----------------------------------------------------

    st.info(
        f"📍  Selected Panchayat: "
        f"**{st.session_state.selected_panchayat}**"
    )


    # -----------------------------------------------------
    # FORM
    # -----------------------------------------------------

    with st.form("contractor_form"):

        col1, col2 = st.columns(
            2,
            gap="large"
        )


        # =================================================
        # LEFT
        # =================================================

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


        # =================================================
        # RIGHT
        # =================================================

        with col2:

            ra_bill = st.text_input(
                "RA Bill",
                placeholder="Enter RA Bill number"
            )


            work_date = st.date_input(
                "Work Date",
                value=datetime.today()
            )


        # =================================================
        # DIA HEADER
        # =================================================

        st.markdown(
            """
            <div class="dia-section">

                <div class="dia-heading">

                    <div class="dia-icon">
                        📏
                    </div>

                    <div class="dia-title">
                        DIA Values
                    </div>

                </div>

                <div class="dia-description">
                    Enter the quantity for each available DIA size.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # =================================================
        # DIA VALUES
        # =================================================

        dia_cols = st.columns(
            3,
            gap="large"
        )

        dia_values = {}


        for index, dia in enumerate(DIA_COLUMNS):

            with dia_cols[index % 3]:

                dia_values[dia] = st.number_input(
                    dia,
                    min_value=0,
                    value=0,
                    step=1
                )


        st.write("")


        # =================================================
        # SUBMIT
        # =================================================

        submitted = st.form_submit_button(
            "💾  Submit Details",
            use_container_width=True
        )


        # =================================================
        # SAVE
        # =================================================

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

                    new_row[dia] = (
                        dia_values[dia]
                    )


                new_df = pd.DataFrame(
                    [new_row]
                )


                df = pd.concat(
                    [
                        df,
                        new_df
                    ],
                    ignore_index=True
                )


                df.to_excel(
                    EXCEL_FILE,
                    index=False
                )


                st.success(
                    "✅ Details submitted successfully!"
                )

                st.balloons()
