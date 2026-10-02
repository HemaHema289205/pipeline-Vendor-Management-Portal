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
# 🎨 CUSTOM DESIGN
# Change the CSS variables at the top of the style block
# to choose your own colors.
# ============================================================
st.markdown("""
<style>
:root {
    /* =========================================================
       🎨 CHANGE ONLY THESE COLORS TO YOUR CHOICE
       ========================================================= */
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
    --sidebar-bg: #111827;
    --sidebar-text: #ffffff;
    --success-bg: #ecfdf5;
    --success-text: #047857;
    --danger-bg: #fef2f2;
    --danger-text: #b91c1c;
}

/* ---------- App background ---------- */
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(124,58,237,.08), transparent 28%),
        radial-gradient(circle at 90% 20%, rgba(236,72,153,.07), transparent 30%),
        var(--app-bg) !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stToolbar"] {
    background: transparent !important;
}

/* ---------- Main content ---------- */
.block-container {
    max-width: 1250px !important;
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
}

/* ---------- Typography ---------- */
body, .stApp, .stApp p, .stApp label,
.stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stMarkdownContainer"] p {
    font-family: "Segoe UI", Arial, sans-serif !important;
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

/* ---------- Top title ---------- */
.portal-title {
    text-align: center;
    font-size: 2.35rem;
    font-weight: 800;
    color: var(--text);
    margin: .2rem 0 .35rem 0;
}

.portal-subtitle {
    text-align: center;
    color: var(--text-soft) !important;
    font-size: 1rem;
    margin-bottom: 1.8rem;
}

/* ---------- Selection / form cards ---------- */
[data-testid="stForm"],
.portal-card {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 22px !important;
    box-shadow: 0 14px 35px rgba(17,24,39,.07) !important;
}

[data-testid="stForm"] {
    padding: 1.5rem 1.7rem 1.7rem 1.7rem !important;
}

.portal-card {
    padding: 1.5rem;
}

/* ---------- Selected Panchayat info ---------- */
div[data-testid="stAlert"] {
    background: var(--primary-soft) !important;
    border: 1px solid rgba(124,58,237,.25) !important;
    border-radius: 14px !important;
    color: var(--text) !important;
}

div[data-testid="stAlert"] * {
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
}

/* ---------- Labels ---------- */
[data-testid="stWidgetLabel"] label,
[data-testid="stWidgetLabel"] p {
    color: var(--text) !important;
    font-weight: 600 !important;
}

/* ---------- ALL INPUTS ---------- */
div[data-baseweb="input"],
div[data-baseweb="base-input"],
div[data-baseweb="input"] > div,
div[data-baseweb="base-input"] > div,
input,
textarea {
    background: var(--surface) !important;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
}

div[data-baseweb="input"],
div[data-baseweb="base-input"] {
    border: 1.5px solid var(--border) !important;
    border-radius: 11px !important;
    box-shadow: none !important;
}

div[data-baseweb="input"]:focus-within,
div[data-baseweb="base-input"]:focus-within {
    border-color: var(--border-focus) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,.12) !important;
}

input::placeholder,
textarea::placeholder {
    color: #9ca3af !important;
    -webkit-text-fill-color: #9ca3af !important;
}

/* ---------- Selectbox CLOSED state ---------- */
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

/* ---------- Selectbox OPEN dropdown: fixes black background/text ---------- */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="popover"] > div > div,
div[data-baseweb="menu"],
div[data-baseweb="menu"] > div,
ul[role="listbox"],
ul[data-baseweb="menu"] {
    background: var(--surface) !important;
    color: var(--text) !important;
    opacity: 1 !important;
}

div[data-baseweb="popover"] *,
div[data-baseweb="menu"] *,
ul[role="listbox"] *,
ul[data-baseweb="menu"] * {
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    background-image: none !important;
}

li[role="option"],
li[data-baseweb="menu-item"],
div[role="option"] {
    background: var(--surface) !important;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    padding: 10px 14px !important;
}

li[role="option"]:hover,
li[data-baseweb="menu-item"]:hover,
div[role="option"]:hover {
    background: var(--primary-soft) !important;
    color: var(--primary-dark) !important;
    -webkit-text-fill-color: var(--primary-dark) !important;
}

li[aria-selected="true"],
div[role="option"][aria-selected="true"] {
    background: var(--primary-soft) !important;
    color: var(--primary-dark) !important;
    -webkit-text-fill-color: var(--primary-dark) !important;
    font-weight: 700 !important;
}

/* ---------- Date picker ---------- */
div[data-testid="stDateInput"] input {
    background: var(--surface) !important;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
}

/* Calendar popup */
div[data-baseweb="calendar"],
div[data-baseweb="calendar"] *,
div[role="dialog"] {
    color: var(--text) !important;
}

div[data-baseweb="calendar"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
}

/* ---------- DIA section ---------- */
.dia-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.55rem;
    font-weight: 800;
    margin: 1.25rem 0 1rem 0;
    color: var(--text);
}

.dia-caption {
    color: var(--text-soft) !important;
    font-size: .9rem;
    margin-top: -.55rem;
    margin-bottom: 1rem;
}

/* Number input */
div[data-testid="stNumberInput"] div[data-baseweb="input"] {
    border-radius: 11px 0 0 11px !important;
}

div[data-testid="stNumberInput"] input {
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
}

/* Stepper buttons */
button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"] {
    background: var(--primary-soft) !important;
    border: 1px solid var(--border) !important;
    color: var(--primary-dark) !important;
}

button[data-testid="stNumberInputStepDown"] svg,
button[data-testid="stNumberInputStepUp"] svg {
    fill: var(--primary-dark) !important;
    color: var(--primary-dark) !important;
}

/* ---------- Buttons ---------- */
.stButton > button,
[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, var(--primary), var(--accent)) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    min-height: 46px !important;
    font-weight: 750 !important;
    box-shadow: 0 8px 18px rgba(124,58,237,.20) !important;
    transition: .2s ease !important;
}

.stButton > button *,
[data-testid="stFormSubmitButton"] > button * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

.stButton > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {
    filter: brightness(.97);
    transform: translateY(-1px);
    box-shadow: 0 11px 24px rgba(124,58,237,.26) !important;
}

/* Back button */
.back-button .stButton > button {
    background: var(--surface) !important;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    border: 1px solid var(--border) !important;
    box-shadow: none !important;
}

.back-button .stButton > button * {
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: none !important;
}

section[data-testid="stSidebar"] > div {
    background: var(--sidebar-bg) !important;
}

section[data-testid="stSidebar"] * {
    color: var(--sidebar-text) !important;
    -webkit-text-fill-color: var(--sidebar-text) !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-weight: 800 !important;
}

section[data-testid="stSidebar"] .stDownloadButton > button {
    background: rgba(255,255,255,.08) !important;
    border: 1px solid rgba(255,255,255,.22) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border-radius: 11px !important;
    box-shadow: none !important;
}

section[data-testid="stSidebar"] .stDownloadButton > button:hover {
    background: rgba(255,255,255,.15) !important;
}

/* ---------- Success / Error messages ---------- */
div[data-testid="stAlert"][kind="success"] {
    background: var(--success-bg) !important;
    border-color: #a7f3d0 !important;
}

div[data-testid="stAlert"][kind="error"] {
    background: var(--danger-bg) !important;
    border-color: #fecaca !important;
}

/* ---------- Mobile ---------- */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem !important;
    }

    .portal-title {
        font-size: 1.75rem;
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

DIA_COLUMNS = [col.upper().strip() for col in [
    "63DIA", "75 DIA", "90 DIA",
    "110 DIA", "125 DIA", "140 DIA",
    "160 DIA", "180 DIA", "200 DIA"
]]

PANCHAYATS = ['Aaspurdevsara', 'Aaurain', 'Atroramipur & Turkoli', 'Baejalpur', 'BANBIRPUR', 'Behta & Bijhala', 'Barokhan', 'Bhatti khurd', 'Bhikhampur & Kopa', 'Binaeka', 'Bind', 'Dafra', 'Dahi', 'Deduaa', 'Dhansar & Banpurva', 'Dhaurahra & Dhanepurple', 'Diyawa & Keotali', 'Gahbra', 'Govindpur', 'Harikapura', 'Harraipatti & Labeda', 'Kabirpur', 'Lakhipur Kapsa & Bhushar', 'Majhagaon', 'ParvatpurSuleman', 'Pithapur', 'Puredalpatshah & Gauhani', 'Saphachhat', 'Umapur & Madramu', 'Umardiha', 'Amarpur', 'Amsauna & Dohari', 'Asalpur', 'Baseerpur', 'Chakamajhanipur & Pragaspur', 'Chaukhara & Saraygani', 'Dharampur', 'Gahari Chak', 'Gavan Patti & Ganai Diha', 'Goi', 'Gopalpur', 'Harjamau', 'Hosiyarpur', 'Jaisinghgardh', 'Kanpamandhupur', 'KaranpurKhujahi', 'Khbhor', 'Kothiyahi', 'Maruaan & Saraynakar', 'Miranpur & Rajapur Mufharid', 'Pandari Jabar', 'PipriKhalsa', 'Praanpur', 'Rakha', 'Sarkhailpur', 'Srinathpur', 'Tala', 'Aamipur', 'Aemapur Bindhan', 'Aruhari', 'Baburai Jahapur', 'Badhwait', 'Bahorikpur', 'Bakol & Arjun Ateru', 'BALLA & DHAMMOHAN', 'BASWAHI', 'Bhaesana', 'Bharatgarh & Saheb Ateru', 'BhawaniganjKota', 'Bidhasin', 'Chaurang', 'Diha Balai', 'Fatuhabad', 'GUJUWAR & SARAY CHATTA', 'Goghar', 'Govind Nagar', 'Raipur Barkhi Jalalpur Diwha', 'Jaichandrapur & Muraini', 'Jhingur & Gopalapur', 'Kajipur Kusemer', 'Kanava', 'Kodar Khurd & Rahuwar', 'Lallupatti', 'Machheha Harda Patti', 'Mahewa Malkiya', 'Maladhar Chhatta', 'Mohammadpur Sohag', 'Nariyawan', 'Patna', 'Pritampur', 'Puraeli Makhdumpur', 'Pure Jhau', 'Pure Masvan', 'Purmai Sultanpur', 'Raygardh', 'Raikashipur', 'Rajapur', 'Ramaipur', 'Ramnagar', 'Salembhadari', 'Salempur Dadeura & Kajepur Karam Husen', 'Sarai Swami', 'Saray Khandev', 'Saray gopal', 'TANDA AND PEENG', 'Wajirpur', 'Aaemna Jaatupur & Samnaspur Daamno', 'Aautaarpur', 'Bansiyara', 'Barbaspur', 'Barna', 'Bedhan Gopalpur', 'Bhawanpur', 'Bhitara & Hariharpur', 'BhitipureNain', 'Bihariya', 'Bikara', 'Burhepur', 'Chakwad', 'Chhatar', 'Chheuga', 'Devari Hardoi Patti & Narangapur', 'Devarpatti & Silawatpur', 'Dhanvaasa & Kodrajeet', 'Galgali, Tarapur Kandai', 'Garibpur', 'Gogaer', 'Jamlamau', 'Kamaarjeet Patti', 'Kamoli Veerbhanupur', 'Kanupur', 'Kashipur Dibuki', 'Khargipur & Phoolpur Rama', 'Khasar', 'Khatwara', 'Khemkaranpur', 'Kodrasal', 'Korahi', 'Kuda', 'Maharajpur', 'Malaak Tilhai', 'Mandal Bhausaw', 'Meerpur Banohi', 'Pariyawan & Lochangarh', 'Pithipur', 'Ramdaspatti', 'Ramgarh Banohi', 'Rampur', 'Raipur', 'Sarai Babuin & Dharhupur', 'Sarai Naahra', 'Saray Mahasingh', 'Saray Said Kha', 'Sheshapur Chauras', 'Siya', 'Tekki Patti', 'Tiwari Mehmadapur', 'Trilokpur & Bhav', 'Umari Bujurg', 'Umari Kotila', 'Umarpatti', 'Aandharipur', 'Antamau', 'Asthan', 'Badera', 'Badgau', 'Bariyavan & Natohi', 'Bijalipur Bangadhwa & Trilochanpur', 'Bramhauli', 'Chachamau', 'Chandapur & Dayalpur', 'Chaurahi & Bajhabit & Miragadwa', 'Chindaura & Seshomohammadpur', 'Eethu', 'Jajupur', 'Janvamau', 'Kakriha & Abdulwahidganj', 'Kandaru', 'Karamganj & Samaspur Sailwara', 'Kasipur', 'Keravdiha', 'Lathtara', 'Maddupur & Rokiyapur', 'Madhwapur', 'Manar & Ranimau', 'Mishrpur', 'Mohamidpur And Kiyawan', 'Parsai', 'Pithanapur', 'Rajwapur', 'Rewali', 'Sangrampur & Hinahu', 'Seshpur', 'Seshpurdhnpur', 'Tiwaripur', 'Adhiya', 'Ahibaranpur', 'Akthiyari Kotila', 'Bachandamau', 'Bachrauli', 'Bahadurpur', 'Banemau Uparhar', 'Bhadri & Bishiya', 'Chakadarali', 'Chakaparanpur', 'Chausa', 'Dadauli', 'Deeha', 'Dilerganj', 'Dumwamai', 'Gayaspur', 'Itaura', 'Jakhamai', 'Jasholi & Kushahil Bazar', 'Kaema', 'Kajipur Maharajganj', 'Karenati', 'Keshavpura & Rudauli', 'Khemipur', 'Kushildiha', 'Launda & Mamauli', 'Maharajpur & Kashipur Mohan', 'Mahewamohanpur & Mohaddinagar Uparhar', 'Majhilgaon', 'Malakarajakpur', 'Mauli', 'Mavai Kalan', 'Naubasta', 'Pahadpur Banohi', 'Panahnagarbarai', 'Parewanarayanpur', 'Parsipur', 'Peer Nagar', 'Pingri', 'Raiypur', 'Rehwai', 'Sahabpur & Tajunddinpur', 'Sahumai', 'Saja', 'Saraykirat', 'Sariya Praveshpur', 'Sekhpur Asik', 'Shahpur Uparhar', 'Shergarh & Sariyawa', 'Sujauli', 'Barapur Bhika', 'Gaheri', 'Sarai Makai', 'Asainapur & Dagrara', 'Asrahi', 'Basupur', 'Belha', 'Bhojpur', 'Devapur', 'Gaukhadi & Udhranpur', 'Khajuri', 'Khemsari', 'Mandipur', 'Medhawan', 'Pahadpur', 'Pandri', 'Parsupur', 'Pure Bansi', 'Pure Roop', 'Puretilakram', 'Ramgarhkhas & Hulasgarh', 'Rangardh Raela & Saray Raju', 'Rangauli', 'Rohada & Delhupur & Kalapur', 'Sarayjagat Singh', 'Saraynarayan Singh & Bhebhaura', 'Saripur', 'Tarapur', 'Bhagwanpur', 'Lilauli', 'Madhupur', 'Puraila', 'Rampur Mustarka', 'Amuwahi', 'Atarsand & Parsupur', 'Aurangabad', 'Barasarai', 'Barhupur', 'Bhaedpur', 'Bhausiya', 'Choumari', 'Darchut', 'Dehridigar', 'Dhraulimufrid & Chanduadih', 'Gehrauli', 'Hardoi', 'Hathsara', 'Itwa', 'Kansapatti', 'Koni & Salahipur Kanjas', 'Lauli Pokhatakham', 'Madura Raniganj & Sarauli', 'Malaak', 'Mandah & Bojhi', 'Mangraura', 'Nevra', 'Padumpur', 'Parsanda', 'Purebhikha & Raigarh', 'Puremanikanth', 'Sakra', 'Sarayjmuvari', 'Sheshapur Adharganj', 'Shivpur Khurd', 'Sirsidih', 'Suryagarhjagannath', 'Utras', 'Bahuta', 'Basauli', 'Beerpura Khurd & Parsad', 'Besaar', 'Bhavranpur', 'Bibipur Baradih', 'Charaeya & Asudi', 'Chintamanipur & Andevari', 'Dadupur', 'Dhuti', 'Gogalapur & Puredeojani', 'Kohraov', 'Kukuvar', 'Mahadaha', 'Marha', 'Naurangabad', 'Parsani', 'Purebasan & Aaumisaraysaifkha', 'Raichandrapatti & Arila', 'RampurBela', 'Sarastpur', 'Sardeeh', 'Srinathpur & Mariyampur', 'Sumatpur', 'Tardha', 'Thanegopapur', 'Umarpur & Bani', 'Usrauli', 'Varikhurd & Dashrathpur', 'Virauti & Ramkola', 'Alipur', 'Arjunpur & Madhukarpur', 'Batauli', 'Bharatpur', 'Budhiyapur', 'Bijumau', 'Birbhadrapur', 'Chakerhi & Nevada Kalan', 'Digaosi', 'Jamalpur', 'Kalyanpur & Purefhattesingh', 'Kanyaeyadullapur & Harnahar', 'Kedaura', 'Kherapurechemi & Purebasantray', 'Lakuri', 'Lohangpur', 'Madamai', 'Mishrainpur', 'Mohammadpur Khas', 'Mothin', 'Narayanpur', 'Pure Chhattu', 'Pure Gajai', 'Pure Jodha', 'Rampur Vavli', 'Saray Lalmati & Khandwa', 'Bandanpur & Teuanga', 'Bhilampur & Bahlolpur', 'Chakbantod', 'Chaukhandpureanti', 'Gode', 'Ishipur', 'Jagdeeshpur & Purebhaiya', 'Jahnaipur & Kushami & Saraybheliya', 'Jaitipurkathar', 'Kadipur And Bhanva', 'Katkavalli', 'Khampur & Saray Dali', 'Kisundadpur & Mahuaar', 'Madupur, Sakrauli & Ajgara', 'Naubasta & Kushfara', 'Nevada Kala & Dekahi', 'Pratapgarhgramin & Banbeerkach', 'Pure Madhav Singh & Gadichakdeiya', 'Pure Mustafa', 'Rajapur Kalan', 'Ramnagar', 'Saraybeerbhadra', 'Setapur', 'Variya Samudra', 'Arjunpura', 'Ashapur & Chaubeypur', 'Bajhan', 'Bansi', 'Barendra & Singhni', 'Barista & Basupur', 'Bhadausi & Rampur Praan', 'Bhawanipur', 'Dandupur Daulat', 'Gauhani & Pachkhara', 'Gaura Dand', 'Gobari', 'Jalapur', 'Kalayanpur Mauraha', 'Kalyanpur Dadiwach', 'Khaira Gaurbari & Adhaarpur', 'Lakhraon', 'Makaipur', 'Mehmadapur', 'Nari', 'Para Hamidpur', 'Pure Bharat', 'Pure Pandey Kamora & Tejgarh', 'Pure Parmeshwar', 'Rajapur Raeniya & Nevada Gauradand', 'Sandwa Chandika And Katka Manpur', 'Sangrampur', 'Shivrajpur', 'Sukulpur & Chauraha', 'Tiwaripur', 'Trilokpur Visai', 'Upadhyaypur', 'Usari', 'Aasanva', 'Alavalpur', 'Amawa & Semra', 'Atheha', 'Badshapur', 'Bewali', 'Bhagatpur', 'Bhawanigarh', 'Deuma Poorab', 'Gadiyaan & Shukulpur', 'Indilpur', 'Jogapur', 'Katehti', 'Khanipur', 'Kumbhidiha', 'Muraeni', 'Narval', 'Pattikachera & Ahabidihad', 'Pedariya', 'Pinjari', 'Pranipur & Mustafabad', 'Pure Bhagvat & Pure Loka', 'Pure Narayandas', 'Saruaava', 'Singhgarh', 'Uchapur & Rampur Kasiha', 'Usmanpur', 'Bijemau & Visanpur', 'Jariyari', 'Rajapur & Naseerpur', 'Rasoeya & PremdarPatti']

# ============================================================
# INITIALIZE EXCEL FILE
# ============================================================
if not os.path.exists(EXCEL_FILE):
    df_init = pd.DataFrame(columns=[
        "DATE",
        "RA BILL",
        "VENDOR CODE",
        "NAME OF THE CONTRACTOR",
        "SCHEME ID",
        "PANCHAYAT",
        "TYPE"
    ] + DIA_COLUMNS)

    df_init.to_excel(EXCEL_FILE, index=False)

# ============================================================
# SESSION STATE
# ============================================================
if "page" not in st.session_state:
    st.session_state.page = "index"

if "selected_panchayat" not in st.session_state:
    st.session_state.selected_panchayat = ""

# ============================================================
# PAGE 1: PANCHAYAT SELECTION
# ============================================================
if st.session_state.page == "index":

    st.markdown("""
<div class="portal-title">🏛️ Grama Panchayat Portal</div>
<div class="portal-subtitle">Select your Grama Panchayat to continue</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="portal-card">', unsafe_allow_html=True)

    selected_panchayat = st.selectbox(
        "Select Panchayat",
        ["-- Select Panchayat --"] + PANCHAYATS,
        index=0
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    if st.button("Continue ➡️", use_container_width=True):
        if selected_panchayat != "-- Select Panchayat --":
            st.session_state.selected_panchayat = selected_panchayat
            st.session_state.page = "details"
            st.rerun()
        else:
            st.error("Please select a valid Panchayat.")

# ============================================================
# PAGE 2: CONTRACTOR DETAILS
# ============================================================
elif st.session_state.page == "details":

    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    if st.button("⬅️ Back"):
        st.session_state.page = "index"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
<div class="portal-title">📋 Contractor Details</div>
<div class="portal-subtitle">Enter the work and DIA information for the selected Panchayat</div>
""", unsafe_allow_html=True)

    st.info(
        f"📍  Selected Panchayat: **{st.session_state.selected_panchayat}**"
    )

    st.write("")

    with st.form("contractor_form"):

        col1, col2 = st.columns(2, gap="large")

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
                value=datetime.today()
            )

        st.markdown(
            '<div class="dia-title">📏 DIA Values</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="dia-caption">Enter the quantity for each available DIA size.</div>',
            unsafe_allow_html=True
        )

        dia_cols = st.columns(3, gap="medium")
        dia_values = {}

        for i, dia_label in enumerate(DIA_COLUMNS):
            with dia_cols[i % 3]:
                dia_values[dia_label] = st.number_input(
                    dia_label,
                    min_value=0,
                    value=0,
                    step=1,
                    format="%d"
                )

        st.write("")

        submitted = st.form_submit_button(
            "💾  Submit Details",
            use_container_width=True
        )

        if submitted:

            if not contractor_name.strip() or not vendor_code.strip() or not scheme_id.strip() or not ra_bill.strip():
                st.error("Please fill in all required fields!")
            else:

                formatted_date = work_date.strftime("%d-%m-%Y")

                if os.path.exists(EXCEL_FILE):
                    df = pd.read_excel(EXCEL_FILE)
                    df.columns = df.columns.str.strip().str.upper()
                else:
                    df = pd.DataFrame(columns=[
                        "DATE",
                        "RA BILL",
                        "VENDOR CODE",
                        "NAME OF THE CONTRACTOR",
                        "SCHEME ID",
                        "PANCHAYAT",
                        "TYPE"
                    ] + DIA_COLUMNS)

                new_row = {
                    "DATE": formatted_date,
                    "RA BILL": ra_bill.strip(),
                    "VENDOR CODE": vendor_code.strip(),
                    "NAME OF THE CONTRACTOR": contractor_name.strip(),
                    "SCHEME ID": scheme_id.strip(),
                    "PANCHAYAT": st.session_state.selected_panchayat,
                    "TYPE": "this_bill"
                }

                for dia_label in DIA_COLUMNS:
                    new_row[dia_label] = dia_values[dia_label]

                df = pd.concat(
                    [df, pd.DataFrame([new_row])],
                    ignore_index=True
                )

                df.to_excel(EXCEL_FILE, index=False)

                st.success("Details submitted and saved successfully!")
                st.balloons()

# ============================================================
# SIDEBAR: DATA EXPORT
# ============================================================
with st.sidebar:

    st.markdown("## 📂 Data Export")
    st.caption("Download the submitted contractor records.")

    if os.path.exists(EXCEL_FILE):

        with open(EXCEL_FILE, "rb") as file:

            st.download_button(
                label="📥 Download Data Sheet",
                data=file,
                file_name="contractor_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    else:
        st.warning("No data file available yet.")
