import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Grama Panchayat Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM DESIGN
# ============================================================
st.markdown("""
<style>

:root {

    /* ========================================================
       🎨 CHANGE COLORS HERE
       ======================================================== */

    --app-bg: #f7f8fc;
    --surface: #ffffff;
    --surface-soft: #f8fafc;

    --primary: #7c3aed;
    --primary-dark: #5b21b6;
    --primary-soft: #ede9fe;

    --accent: #ec4899;
    --accent-soft: #fce7f3;

    --text: #111827;
    --text-soft: #4b5563;

    --border: #d9dce5;
    --border-focus: #8b5cf6;

    --success-bg: #ecfdf5;
    --danger-bg: #fef2f2;
}


/* ============================================================
   APP BACKGROUND
   ============================================================ */

.stApp {

    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(124,58,237,.08),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(236,72,153,.07),
            transparent 30%
        ),
        var(--app-bg) !important;
}


header[data-testid="stHeader"] {
    background: transparent !important;
}


[data-testid="stToolbar"] {
    background: transparent !important;
}


/* ============================================================
   MAIN CONTENT
   ============================================================ */

.block-container {

    max-width: 1250px !important;

    padding-top: 2rem !important;

    padding-bottom: 3rem !important;
}


/* ============================================================
   TYPOGRAPHY
   ============================================================ */

body,
.stApp,
.stApp p,
.stApp label,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stMarkdownContainer"] p {

    font-family:
        "Segoe UI",
        Arial,
        sans-serif !important;

    color: var(--text) !important;
}


.stApp [data-testid="stMarkdownContainer"] p,
.stApp label {

    color: var(--text) !important;
}


h1 {

    font-weight: 800 !important;

    letter-spacing: -.5px !important;
}


/* ============================================================
   MAIN HEADER
   ============================================================ */

.main-header {

    display: flex;

    align-items: center;

    justify-content: center;

    gap: 16px;

    margin: .2rem 0 1.7rem 0;
}


.main-header-icon {

    width: 58px;

    height: 58px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 17px;

    background:
        linear-gradient(
            135deg,
            #ede9fe,
            #fce7f3
        );

    font-size: 34px;

    box-shadow:
        0 8px 20px
        rgba(139,92,246,.12);
}


.main-title {

    font-size: 40px;

    font-weight: 850;

    color: #172554 !important;

    -webkit-text-fill-color: #172554 !important;

    line-height: 1.05;
}


.main-subtitle {

    margin-top: 7px;

    font-size: 16px;

    color: #64748b !important;

    -webkit-text-fill-color: #64748b !important;
}


/* ============================================================
   PANCHAYAT SELECT BOX
   ============================================================ */

[data-testid="stSelectbox"] {

    margin-top: .2rem !important;

    margin-bottom: .7rem !important;
}


div[data-baseweb="select"] > div {

    background: var(--surface) !important;

    color: var(--text) !important;

    -webkit-text-fill-color: var(--text) !important;

    border: 1.5px solid var(--border) !important;

    border-radius: 11px !important;

    box-shadow: none !important;
}


div[data-baseweb="select"] span,
div[data-baseweb="select"] input {

    color: var(--text) !important;

    -webkit-text-fill-color: var(--text) !important;
}


div[data-baseweb="select"] svg {

    fill: var(--text) !important;

    color: var(--text) !important;
}


/* ============================================================
   OPEN PANCHAYAT DROPDOWN
   ============================================================ */

div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="popover"] > div > div,
div[data-baseweb="menu"],
div[data-baseweb="menu"] > div,
ul[role="listbox"],
ul[data-baseweb="menu"] {

    background: #ffffff !important;

    color: #111827 !important;

    opacity: 1 !important;
}


div[data-baseweb="popover"] *,
div[data-baseweb="menu"] *,
ul[role="listbox"] *,
ul[data-baseweb="menu"] * {

    color: #111827 !important;

    -webkit-text-fill-color: #111827 !important;

    background-image: none !important;
}


li[role="option"],
li[data-baseweb="menu-item"],
div[role="option"] {

    background: #ffffff !important;

    color: #111827 !important;

    -webkit-text-fill-color: #111827 !important;

    padding: 10px 14px !important;
}


li[role="option"]:hover,
li[data-baseweb="menu-item"]:hover,
div[role="option"]:hover {

    background: #ede9fe !important;

    color: #5b21b6 !important;

    -webkit-text-fill-color: #5b21b6 !important;
}


li[aria-selected="true"],
div[role="option"][aria-selected="true"] {

    background: #ede9fe !important;

    color: #5b21b6 !important;

    -webkit-text-fill-color: #5b21b6 !important;

    font-weight: 700 !important;
}


/* ============================================================
   FORM
   ============================================================ */

[data-testid="stForm"] {

    background: var(--surface) !important;

    border: 1px solid var(--border) !important;

    border-radius: 22px !important;

    box-shadow:
        0 14px 35px
        rgba(17,24,39,.07) !important;

    padding:
        1.5rem 1.7rem 1.7rem 1.7rem !important;
}


/* ============================================================
   LABELS
   ============================================================ */

[data-testid="stWidgetLabel"] label,
[data-testid="stWidgetLabel"] p {

    color: var(--text) !important;

    font-weight: 600 !important;
}


/* ============================================================
   TEXT INPUTS
   ============================================================ */

div[data-baseweb="input"],
div[data-baseweb="base-input"],
div[data-baseweb="input"] > div,
div[data-baseweb="base-input"] > div,
input,
textarea {

    background: #ffffff !important;

    color: #111827 !important;

    -webkit-text-fill-color: #111827 !important;
}


div[data-baseweb="input"],
div[data-baseweb="base-input"] {

    border:
        1.5px solid
        var(--border) !important;

    border-radius: 11px !important;

    box-shadow: none !important;
}


div[data-baseweb="input"]:focus-within,
div[data-baseweb="base-input"]:focus-within {

    border-color:
        var(--border-focus) !important;

    box-shadow:
        0 0 0 3px
        rgba(139,92,246,.12) !important;
}


input::placeholder,
textarea::placeholder {

    color: #9ca3af !important;

    -webkit-text-fill-color:
        #9ca3af !important;
}


/* ============================================================
   WORK DATE
   ============================================================ */

div[data-testid="stDateInput"] input,
div[data-testid="stDateInput"] div[data-baseweb="input"],
div[data-testid="stDateInput"] div[data-baseweb="base-input"],
div[data-testid="stDateInput"] div[data-baseweb="input"] > div {

    background: #ffffff !important;

    color: #111827 !important;

    -webkit-text-fill-color: #111827 !important;

    border-color: var(--border) !important;

    box-shadow: none !important;
}


div[data-testid="stDateInput"] input {

    color: #111827 !important;

    -webkit-text-fill-color:
        #111827 !important;
}


div[data-testid="stDateInput"] button {

    background: #ffffff !important;

    color: #111827 !important;

    border: none !important;
}


div[data-testid="stDateInput"] svg {

    fill: #111827 !important;

    color: #111827 !important;
}


/* ============================================================
   CALENDAR
   ============================================================ */

div[data-baseweb="calendar"],
div[data-baseweb="calendar"] *,
div[role="dialog"] {

    color: #111827 !important;
}


div[data-baseweb="calendar"] {

    background: #ffffff !important;

    border:
        1px solid
        var(--border) !important;
}


/* ============================================================
   SELECTED PANCHAYAT MESSAGE
   ============================================================ */

div[data-testid="stAlert"] {

    background:
        var(--primary-soft) !important;

    border:
        1px solid
        rgba(124,58,237,.25) !important;

    border-radius: 14px !important;

    color: var(--text) !important;
}


div[data-testid="stAlert"] * {

    color: var(--text) !important;

    -webkit-text-fill-color:
        var(--text) !important;
}


/* ============================================================
   DIA SECTION
   ============================================================ */

.dia-title {

    display: flex;

    align-items: center;

    gap: 10px;

    font-size: 1.55rem;

    font-weight: 800;

    margin:
        1.25rem 0 1rem 0;

    color: var(--text);
}


.dia-caption {

    color:
        var(--text-soft) !important;

    font-size: .9rem;

    margin-top: -.55rem;

    margin-bottom: 1rem;
}


/* ============================================================
   DIA NUMBER INPUT
   ============================================================ */

div[data-testid="stNumberInput"]
div[data-baseweb="input"] {

    border-radius:
        11px 0 0 11px !important;
}


div[data-testid="stNumberInput"] input {

    color: #111827 !important;

    -webkit-text-fill-color:
        #111827 !important;
}


/* ============================================================
   DIA + / - BUTTONS
   ============================================================ */

button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"] {

    background:
        var(--primary-soft) !important;

    border:
        1px solid
        var(--border) !important;

    color:
        var(--primary-dark) !important;
}


button[data-testid="stNumberInputStepDown"] svg,
button[data-testid="stNumberInputStepUp"] svg {

    fill:
        var(--primary-dark) !important;

    color:
        var(--primary-dark) !important;
}


/* ============================================================
   MAIN BUTTONS
   ============================================================ */

.stButton > button,
[data-testid="stFormSubmitButton"] > button {

    background:
        linear-gradient(
            135deg,
            var(--primary),
            var(--accent)
        ) !important;

    color: #ffffff !important;

    -webkit-text-fill-color:
        #ffffff !important;

    border: none !important;

    border-radius: 12px !important;

    min-height: 46px !important;

    font-weight: 750 !important;

    box-shadow:
        0 8px 18px
        rgba(124,58,237,.20) !important;

    transition: .2s ease !important;
}


.stButton > button *,
[data-testid="stFormSubmitButton"] > button * {

    color: #ffffff !important;

    -webkit-text-fill-color:
        #ffffff !important;
}


.stButton > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {

    filter: brightness(.97);

    transform: translateY(-1px);

    box-shadow:
        0 11px 24px
        rgba(124,58,237,.26) !important;
}


/* ============================================================
   BACK BUTTON
   ============================================================ */

.back-button .stButton > button {

    background:
        #ffffff !important;

    color:
        #111827 !important;

    -webkit-text-fill-color:
        #111827 !important;

    border:
        1px solid
        var(--border) !important;

    box-shadow: none !important;
}


.back-button .stButton > button * {

    color:
        #111827 !important;

    -webkit-text-fill-color:
        #111827 !important;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #fff8fc 0%,
            #fff0f7 55%,
            #ffe8f2 100%
        ) !important;

    border-right:
        1px solid
        #f3c4d9 !important;
}


section[data-testid="stSidebar"] > div {

    background: transparent !important;

    position: relative !important;

    min-height: 100vh !important;
}


section[data-testid="stSidebar"] * {

    color: #172554 !important;

    -webkit-text-fill-color:
        #172554 !important;
}


/* ============================================================
   SIDEBAR BRAND
   ============================================================ */

.sidebar-brand {

    display: flex;

    align-items: center;

    gap: 12px;

    padding:
        8px 4px 26px 4px;
}


.sidebar-logo {

    width: 44px;

    height: 44px;

    border-radius: 13px;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        linear-gradient(
            135deg,
            #8b5cf6,
            #ec4899
        );

    color: #ffffff !important;

    -webkit-text-fill-color:
        #ffffff !important;

    font-size: 23px;

    box-shadow:
        0 7px 18px
        rgba(139,92,246,.20);
}


.sidebar-title {

    font-size: 17px;

    font-weight: 800;

    color: #172554 !important;

    -webkit-text-fill-color:
        #172554 !important;

    line-height: 1.15;
}


.sidebar-subtitle {

    font-size: 11px;

    color: #8b5cf6 !important;

    -webkit-text-fill-color:
        #8b5cf6 !important;

    font-weight: 700;

    margin-top: 4px;
}


/* ============================================================
   SIDEBAR DATA MANAGEMENT
   ============================================================ */

.sidebar-section-title {

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 1.4px;

    color: #9d174d !important;

    -webkit-text-fill-color:
        #9d174d !important;

    margin:
        4px 0 8px 0;
}


/* ============================================================
   DOWNLOAD - NO BLACK BOX
   ============================================================ */

section[data-testid="stSidebar"]
.stDownloadButton > button {

    background: transparent !important;

    background-color:
        transparent !important;

    border: none !important;

    box-shadow: none !important;

    color: #be185d !important;

    -webkit-text-fill-color:
        #be185d !important;

    font-size: 14px !important;

    font-weight: 700 !important;

    padding: 7px 0 !important;

    justify-content:
        flex-start !important;

    text-align: left !important;
}


section[data-testid="stSidebar"]
.stDownloadButton > button * {

    color: #be185d !important;

    -webkit-text-fill-color:
        #be185d !important;

    background:
        transparent !important;
}


section[data-testid="stSidebar"]
.stDownloadButton > button:hover {

    background:
        transparent !important;

    box-shadow:
        none !important;

    transform:
        translateX(4px);
}


/* ============================================================
   STRONGER PANCHAYATS
   ============================================================ */

.sidebar-quote {

    position: absolute;

    bottom: 48px;

    left: 20px;

    right: 20px;

    text-align: center;

    padding: 16px 8px;
}


.sidebar-quote-main {

    font-family:
        Georgia,
        "Times New Roman",
        serif !important;

    font-size: 18px;

    line-height: 1.35;

    font-weight: 700;

    font-style: italic;

    color: #db2777 !important;

    -webkit-text-fill-color:
        #db2777 !important;
}


.sidebar-quote-main span {

    color: #7c3aed !important;

    -webkit-text-fill-color:
        #7c3aed !important;
}


.sidebar-heart {

    margin: 9px 0;

    color: #ec4899 !important;

    -webkit-text-fill-color:
        #ec4899 !important;

    font-size: 13px;
}


.sidebar-quote-small {

    font-size: 11px;

    line-height: 1.5;

    color: #9d174d !important;

    -webkit-text-fill-color:
        #9d174d !important;

    opacity: .78;
}


.sidebar-village {

    margin-top: 12px;

    font-size: 25px;

    letter-spacing: 3px;

    opacity: .75;
}


/* ============================================================
   SUCCESS / ERROR
   ============================================================ */

div[data-testid="stAlert"][kind="success"] {

    background:
        var(--success-bg) !important;

    border-color:
        #a7f3d0 !important;
}


div[data-testid="stAlert"][kind="error"] {

    background:
        var(--danger-bg) !important;

    border-color:
        #fecaca !important;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 768px) {

    .block-container {

        padding: 1rem !important;
    }

    .main-title {

        font-size: 28px;
    }

    .main-header {

        gap: 10px;
    }

    .main-header-icon {

        width: 48px;

        height: 48px;

        font-size: 28px;
    }

    [data-testid="stForm"] {

        padding: 1rem !important;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FILE / DATA CONFIGURATION
# ============================================================

EXCEL_FILE = "contractor_data.xlsx"


DIA_COLUMNS = [
    col.upper().strip()
    for col in [
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
]


# ============================================================
# PANCHAYAT LIST
# ============================================================

PANCHAYATS = [
    'Aaspurdevsara',
    'Aaurain',
    'Atroramipur & Turkoli',
    'Baejalpur',
    'BANBIRPUR',
    'Behta & Bijhala',
    'Barokhan',
    'Bhatti khurd',
    'Bhikhampur & Kopa',
    'Binaeka',
    'Bind',
    'Dafra',
    'Dahi',
    'Deduaa',
    'Dhansar & Banpurva',
    'Dhaurahra & Dhanepurple',
    'Diyawa & Keotali',
    'Gahbra',
    'Govindpur',
    'Harikapura',
    'Harraipatti & Labeda',
    'Kabirpur',
    'Lakhipur Kapsa & Bhushar',
    'Majhagaon',
    'ParvatpurSuleman',
    'Pithapur',
    'Puredalpatshah & Gauhani',
    'Saphachhat',
    'Umapur & Madramu',
    'Umardiha',

    'Amarpur',
    'Amsauna & Dohari',
    'Asalpur',
    'Baseerpur',
    'Chakamajhanipur & Pragaspur',
    'Chaukhara & Saraygani',
    'Dharampur',
    'Gahari Chak',
    'Gavan Patti & Ganai Diha',
    'Goi',
    'Gopalpur',
    'Harjamau',
    'Hosiyarpur',
    'Jaisinghgardh',
    'Kanpamandhupur',
    'KaranpurKhujahi',
    'Khbhor',
    'Kothiyahi',
    'Maruaan & Saraynakar',
    'Miranpur & Rajapur Mufharid',
    'Pandari Jabar',
    'PipriKhalsa',
    'Praanpur',
    'Rakha',
    'Sarkhailpur',
    'Srinathpur',
    'Tala',

    'Aamipur',
    'Aemapur Bindhan',
    'Aruhari',
    'Baburai Jahapur',
    'Badhwait',
    'Bahorikpur',
    'Bakol & Arjun Ateru',
    'BALLA & DHAMMOHAN',
    'BASWAHI',
    'Bhaesana',
    'Bharatgarh & Saheb Ateru',
    'BhawaniganjKota',
    'Bidhasin',
    'Chaurang',
    'Diha Balai',
    'Fatuhabad',
    'GUJUWAR & SARAY CHATTA',
    'Goghar',
    'Govind Nagar',
    'Raipur Barkhi Jalalpur Diwha',
    'Jaichandrapur & Muraini',
    'Jhingur & Gopalapur',
    'Kajipur Kusemer',
    'Kanava',
    'Kodar Khurd & Rahuwar',
    'Lallupatti',
    'Machheha Harda Patti',
    'Mahewa Malkiya',
    'Maladhar Chhatta',
    'Mohammadpur Sohag',
    'Nariyawan',
    'Patna',
    'Pritampur',
    'Puraeli Makhdumpur',
    'Pure Jhau',
    'Pure Masvan',
    'Purmai Sultanpur',
    'Raygardh',
    'Raikashipur',
    'Rajapur',
    'Ramaipur',
    'Ramnagar',
    'Salembhadari',
    'Salempur Dadeura & Kajepur Karam Husen',
    'Sarai Swami',
    'Saray Khandev',
    'Saray gopal',
    'TANDA AND PEENG',
    'Wajirpur',

    'Aaemna Jaatupur & Samnaspur Daamno',
    'Aautaarpur',
    'Bansiyara',
    'Barbaspur',
    'Barna',
    'Bedhan Gopalpur',
    'Bhawanpur',
    'Bhitara & Hariharpur',
    'BhitipureNain',
    'Bihariya',
    'Bikara',
    'Burhepur',
    'Chakwad',
    'Chhatar',
    'Chheuga',
    'Devari Hardoi Patti & Narangapur',
    'Devarpatti & Silawatpur',
    'Dhanvaasa & Kodrajeet',
    'Galgali, Tarapur Kandai',
    'Garibpur',
    'Gogaer',
    'Jamlamau',
    'Kamaarjeet Patti',
    'Kamoli Veerbhanupur',
    'Kanupur',
    'Kashipur Dibuki',
    'Khargipur & Phoolpur Rama',
    'Khasar',
    'Khatwara',
    'Khemkaranpur',
    'Kodrasal',
    'Korahi',
    'Kuda',
    'Maharajpur',
    'Malaak Tilhai',
    'Mandal Bhausaw',
    'Meerpur Banohi',
    'Pariyawan & Lochangarh',
    'Pithipur',
    'Ramdaspatti',
    'Ramgarh Banohi',
    'Rampur',
    'Raipur',
    'Sarai Babuin & Dharhupur',
    'Sarai Naahra',
    'Saray Mahasingh',
    'Saray Said Kha',
    'Sheshapur Chauras',
    'Siya',
    'Tekki Patti',
    'Tiwari Mehmadapur',
    'Trilokpur & Bhav',
    'Umari Bujurg',
    'Umari Kotila',
    'Umarpatti',

    'Aandharipur',
    'Antamau',
    'Asthan',
    'Badera',
    'Badgau',
    'Bariyavan & Natohi',
    'Bijalipur Bangadhwa & Trilochanpur',
    'Bramhauli',
    'Chachamau',
    'Chandapur & Dayalpur',
    'Chaurahi & Bajhabit & Miragadwa',
    'Chindaura & Seshomohammadpur',
    'Eethu',
    'Jajupur',
    'Janvamau',
    'Kakriha & Abdulwahidganj',
    'Kandaru',
    'Karamganj & Samaspur Sailwara',
    'Kasipur',
    'Keravdiha',
    'Lathtara',
    'Maddupur & Rokiyapur',
    'Madhwapur',
    'Manar & Ranimau',
    'Mishrpur',
    'Mohamidpur And Kiyawan',
    'Parsai',
    'Pithanapur',
    'Rajwapur',
    'Rewali',
    'Sangrampur & Hinahu',
    'Seshpur',
    'Seshpurdhnpur',
    'Tiwaripur',

    'Adhiya',
    'Ahibaranpur',
    'Akthiyari Kotila',
    'Bachandamau',
    'Bachrauli',
    'Bahadurpur',
    'Banemau Uparhar',
    'Bhadri & Bishiya',
    'Chakadarali',
    'Chakaparanpur',
    'Chausa',
    'Dadauli',
    'Deeha',
    'Dilerganj',
    'Dumwamai',
    'Gayaspur',
    'Itaura',
    'Jakhamai',
    'Jasholi & Kushahil Bazar',
    'Kaema',
    'Kajipur Maharajganj',
    'Karenati',
    'Keshavpura & Rudauli',
    'Khemipur',
    'Kushildiha',
    'Launda & Mamauli',
    'Maharajpur & Kashipur Mohan',
    'Mahewamohanpur & Mohaddinagar Uparhar',
    'Majhilgaon',
    'Malakarajakpur',
    'Mauli',
    'Mavai Kalan',
    'Naubasta',
    'Pahadpur Banohi',
    'Panahnagarbarai',
    'Parewanarayanpur',
    'Parsipur',
    'Peer Nagar',
    'Pingri',
    'Raiypur',
    'Rehwai',
    'Sahabpur & Tajunddinpur',
    'Sahumai',
    'Saja',
    'Saraykirat',
    'Sariya Praveshpur',
    'Sekhpur Asik',
    'Shahpur Uparhar',
    'Shergarh & Sariyawa',
    'Sujauli',

    'Barapur Bhika',
    'Gaheri',
    'Sarai Makai',
    'Asainapur & Dagrara',
    'Asrahi',
    'Basupur',
    'Belha',
    'Bhojpur',
    'Devapur',
    'Gaukhadi & Udhranpur',
    'Khajuri',
    'Khemsari',
    'Mandipur',
    'Medhawan',
    'Pahadpur',
    'Pandri',
    'Parsupur',
    'Pure Bansi',
    'Pure Roop',
    'Puretilakram',
    'Ramgarhkhas & Hulasgarh',
    'Rangardh Raela & Saray Raju',
    'Rangauli',
    'Rohada & Delhupur & Kalapur',
    'Sarayjagat Singh',
    'Saraynarayan Singh & Bhebhaura',
    'Saripur',
    'Tarapur',

    'Bhagwanpur',
    'Lilauli',
    'Madhupur',
    'Puraila',
    'Rampur Mustarka',

    'Amuwahi',
    'Atarsand & Parsupur',
    'Aurangabad',
    'Barasarai',
    'Barhupur',
    'Bhaedpur',
    'Bhausiya',
    'Choumari',
    'Darchut',
    'Dehridigar',
    'Dhraulimufrid & Chanduadih',
    'Gehrauli',
    'Hardoi',
    'Hathsara',
    'Itwa',
    'Kansapatti',
    'Koni & Salahipur Kanjas',
    'Lauli Pokhatakham',
    'Madura Raniganj & Sarauli',
    'Malaak',
    'Mandah & Bojhi',
    'Mangraura',
    'Nevra',
    'Padumpur',
    'Parsanda',
    'Purebhikha & Raigarh',
    'Puremanikanth',
    'Sakra',
    'Sarayjmuvari',
    'Sheshapur Adharganj',
    'Shivpur Khurd',
    'Sirsidih',
    'Suryagarhjagannath',
    'Utras',

    'Bahuta',
    'Basauli',
    'Beerpura Khurd & Parsad',
    'Besaar',
    'Bhavranpur',
    'Bibipur Baradih',
    'Charaeya & Asudi',
    'Chintamanipur & Andevari',
    'Dadupur',
    'Dhuti',
    'Gogalapur & Puredeojani',
    'Kohraov',
    'Kukuvar',
    'Mahadaha',
    'Marha',
    'Naurangabad',
    'Parsani',
    'Purebasan & Aaumisaraysaifkha',
    'Raichandrapatti & Arila',
    'RampurBela',
    'Sarastpur',
    'Sardeeh',
    'Srinathpur & Mariyampur',
    'Sumatpur',
    'Tardha',
    'Thanegopapur',
    'Umarpur & Bani',
    'Usrauli',
    'Varikhurd & Dashrathpur',
    'Virauti & Ramkola',

    'Alipur',
    'Arjunpur & Madhukarpur',
    'Batauli',
    'Bharatpur',
    'Budhiyapur',
    'Bijumau',
    'Birbhadrapur',
    'Chakerhi & Nevada Kalan',
    'Digaosi',
    'Jamalpur',
    'Kalyanpur & Purefhattesingh',
    'Kanyaeyadullapur & Harnahar',
    'Kedaura',
    'Kherapurechemi & Purebasantray',
    'Lakuri',
    'Lohangpur',
    'Madamai',
    'Mishrainpur',
    'Mohammadpur Khas',
    'Mothin',
    'Narayanpur',
    'Pure Chhattu',
    'Pure Gajai',
    'Pure Jodha',
    'Rampur Vavli',
    'Saray Lalmati & Khandwa',

    'Bandanpur & Teuanga',
    'Bhilampur & Bahlolpur',
    'Chakbantod',
    'Chaukhandpureanti',
    'Gode',
    'Ishipur',
    'Jagdeeshpur & Purebhaiya',
    'Jahnaipur & Kushami & Saraybheliya',
    'Jaitipurkathar',
    'Kadipur And Bhanva',
    'Katkavalli',
    'Khampur & Saray Dali',
    'Kisundadpur & Mahuaar',
    'Madupur, Sakrauli & Ajgara',
    'Naubasta & Kushfara',
    'Nevada Kala & Dekahi',
    'Pratapgarhgramin & Banbeerkach',
    'Pure Madhav Singh & Gadichakdeiya',
    'Pure Mustafa',
    'Rajapur Kalan',
    'Ramnagar',
    'Saraybeerbhadra',
    'Setapur',
    'Variya Samudra',

    'Arjunpura',
    'Ashapur & Chaubeypur',
    'Bajhan',
    'Bansi',
    'Barendra & Singhni',
    'Barista & Basupur',
    'Bhadausi & Rampur Praan',
    'Bhawanipur',
    'Dandupur Daulat',
    'Gauhani & Pachkhara',
    'Gaura Dand',
    'Gobari',
    'Jalapur',
    'Kalayanpur Mauraha',
    'Kalyanpur Dadiwach',
    'Khaira Gaurbari & Adhaarpur',
    'Lakhraon',
    'Makaipur',
    'Mehmadapur',
    'Nari',
    'Para Hamidpur',
    'Pure Bharat',
    'Pure Pandey Kamora & Tejgarh',
    'Pure Parmeshwar',
    'Rajapur Raeniya & Nevada Gauradand',
    'Sandwa Chandika And Katka Manpur',
    'Sangrampur',
    'Shivrajpur',
    'Sukulpur & Chauraha',
    'Tiwaripur',
    'Trilokpur Visai',
    'Upadhyaypur',
    'Usari',

    'Aasanva',
    'Alavalpur',
    'Amawa & Semra',
    'Atheha',
    'Badshapur',
    'Bewali',
    'Bhagatpur',
    'Bhawanigarh',
    'Deuma Poorab',
    'Gadiyaan & Shukulpur',
    'Indilpur',
    'Jogapur',
    'Katehti',
    'Khanipur',
    'Kumbhidiha',
    'Muraeni',
    'Narval',
    'Pattikachera & Ahabidihad',
    'Pedariya',
    'Pinjari',
    'Pranipur & Mustafabad',
    'Pure Bhagvat & Pure Loka',
    'Pure Narayandas',
    'Saruaava',
    'Singhgarh',
    'Uchapur & Rampur Kasiha',
    'Usmanpur',

    'Bijemau & Visanpur',
    'Jariyari',
    'Rajapur & Naseerpur',
    'Rasoeya & PremdarPatti'
]


# ============================================================
# INITIALIZE EXCEL FILE
# ============================================================

if not os.path.exists(EXCEL_FILE):

    df_init = pd.DataFrame(
        columns=[
            "DATE",
            "RA BILL",
            "VENDOR CODE",
            "NAME OF THE CONTRACTOR",
            "SCHEME ID",
            "PANCHAYAT",
            "TYPE"
        ] + DIA_COLUMNS
    )

    df_init.to_excel(
        EXCEL_FILE,
        index=False
    )


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:

    st.session_state.page = "index"


if "selected_panchayat" not in st.session_state:

    st.session_state.selected_panchayat = ""


# ============================================================
# PAGE 1 - PANCHAYAT SELECTION
# ============================================================

if st.session_state.page == "index":

    st.markdown(
        """
        <div class="main-header">

            <div class="main-header-icon">
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


    selected_panchayat = st.selectbox(

        "Select Panchayat",

        [
            "-- Select Panchayat --"
        ] + PANCHAYATS,

        index=0
    )


    st.write("")


    if st.button(
        "Continue ➡️",
        use_container_width=True
    ):

        if selected_panchayat != "-- Select Panchayat --":

            st.session_state.selected_panchayat = (
                selected_panchayat
            )

            st.session_state.page = "details"

            st.rerun()

        else:

            st.error(
                "Please select a valid Panchayat."
            )


# ============================================================
# PAGE 2 - CONTRACTOR DETAILS
# ============================================================

elif st.session_state.page == "details":

    st.markdown(
        '<div class="back-button">',
        unsafe_allow_html=True
    )


    if st.button("⬅️ Back"):

        st.session_state.page = "index"

        st.rerun()


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="main-header">

            <div class="main-header-icon">
                📋
            </div>

            <div>

                <div class="main-title">
                    Contractor Details
                </div>

                <div class="main-subtitle">
                    Enter the work and DIA information
                    for the selected Panchayat
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.info(
        f"📍 Selected Panchayat: "
        f"**{st.session_state.selected_panchayat}**"
    )


    st.write("")


    with st.form("contractor_form"):

        col1, col2 = st.columns(
            2,
            gap="large"
        )


        # ====================================================
        # LEFT COLUMN
        # ====================================================

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


        # ====================================================
        # RIGHT COLUMN
        # ====================================================

        with col2:

            ra_bill = st.text_input(
                "RA Bill",
                placeholder="Enter RA Bill number"
            )


            work_date = st.date_input(
                "Work Date",
                value=datetime.today()
            )


        # ====================================================
        # DIA TITLE
        # ====================================================

        st.markdown(
            """
            <div class="dia-title">
                📏 DIA Values
            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            """
            <div class="dia-caption">
                Enter the quantity for each available DIA size.
            </div>
            """,
            unsafe_allow_html=True
        )


        # ====================================================
        # DIA INPUTS
        # ====================================================

        dia_cols = st.columns(
            3,
            gap="medium"
        )


        dia_values = {}


        for i, dia_label in enumerate(
            DIA_COLUMNS
        ):

            with dia_cols[i % 3]:

                dia_values[dia_label] = (
                    st.number_input(
                        dia_label,

                        min_value=0,

                        value=0,

                        step=1,

                        format="%d"
                    )
                )


        st.write("")


        # ====================================================
        # SUBMIT
        # ====================================================

        submitted = st.form_submit_button(

            "💾  Submit Details",

            use_container_width=True
        )


        if submitted:

            if (
                not contractor_name.strip()
                or not vendor_code.strip()
                or not scheme_id.strip()
                or not ra_bill.strip()
            ):

                st.error(
                    "Please fill in all required fields!"
                )

            else:

                formatted_date = (
                    work_date.strftime(
                        "%d-%m-%Y"
                    )
                )


                if os.path.exists(
                    EXCEL_FILE
                ):

                    df = pd.read_excel(
                        EXCEL_FILE
                    )

                    df.columns = (
                        df.columns
                        .str.strip()
                        .str.upper()
                    )

                else:

                    df = pd.DataFrame(
                        columns=[
                            "DATE",
                            "RA BILL",
                            "VENDOR CODE",
                            "NAME OF THE CONTRACTOR",
                            "SCHEME ID",
                            "PANCHAYAT",
                            "TYPE"
                        ] + DIA_COLUMNS
                    )


                # ============================================
                # NEW ROW
                # ============================================

                new_row = {

                    "DATE":
                        formatted_date,

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


                # ============================================
                # ADD DIA VALUES
                # ============================================

                for dia_label in DIA_COLUMNS:

                    new_row[dia_label] = (
                        dia_values[dia_label]
                    )


                # ============================================
                # SAVE
                # ============================================

                df = pd.concat(
                    [
                        df,
                        pd.DataFrame([new_row])
                    ],
                    ignore_index=True
                )


                df.to_excel(
                    EXCEL_FILE,
                    index=False
                )


                st.success(
                    "Details submitted and saved successfully!"
                )


                st.balloons()


# ============================================================
# SIDEBAR - BRANDING + DATA EXPORT
# ============================================================

with st.sidebar:

    # ========================================================
    # BRANDING
    # ========================================================

    st.markdown(
        """
        <div class="sidebar-brand">

            <div class="sidebar-logo">
                🏛️
            </div>

            <div>

                <div class="sidebar-title">
                    Grama Panchayat
                </div>

                <div class="sidebar-subtitle">
                    Digital Governance Portal
                </div>

            </div>

        </div>

        <div class="sidebar-section-title">
            DATA MANAGEMENT
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # DOWNLOAD
    # ========================================================

    if os.path.exists(
        EXCEL_FILE
    ):

        with open(
            EXCEL_FILE,
            "rb"
        ) as file:

            st.download_button(

                label="📥  Download Data Sheet",

                data=file,

                file_name=
                    "contractor_data.xlsx",

                mime=
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                use_container_width=False
            )

    else:

        st.caption(
            "No data file available yet."
        )


    # ========================================================
    # STRONGER PANCHAYATS
    # ========================================================

    st.markdown(
        """
        <div class="sidebar-quote">

            <div class="sidebar-quote-main">

                Stronger Panchayats

                <br>

                <span>
                    Brighter Future
                </span>

            </div>


            <div class="sidebar-heart">
                ───── ♥ ─────
            </div>


            <div class="sidebar-quote-small">

                Digital governance for

                <br>

                better rural development

            </div>


            <div class="sidebar-village">

                🌳 🏠 🌳

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )
