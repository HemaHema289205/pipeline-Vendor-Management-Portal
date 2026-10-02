import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Grama Panchayat Portal",
    page_icon="🏛️",
    layout="centered" 
)

# Custom Styling: Modern, Clean White & Soft Pink UI (Zero Black Boxes)
st.markdown("""
<style>
    /* Global App Background */
    .stApp, header[data-testid="stHeader"] {
        background-color: #fff0f3 !important;
        background-image: linear-gradient(135deg, #ffffff 0%, #fff0f5 50%, #ffe4ec 100%) !important;
    }
    
    header[data-testid="stHeader"], [data-testid="stToolbar"] {
        background: transparent !important;
    }

    /* Solid Black Crisp Text Everywhere */
    *, p, span, label, h1, h2, h3, h4, h5, h6, [data-testid="stMarkdownContainer"] p {
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Container / Card Styling */
    [data-testid="stForm"], div[data-testid="stVerticalBlock"] > div:has(div.stSelectbox) {
        background-color: #ffffff !important;
        border-radius: 16px !important;
        padding: 32px !important;
        border: 1.5px solid #fbcfe8 !important;
        box-shadow: 0 10px 25px -5px rgba(244, 114, 182, 0.12), 0 8px 10px -6px rgba(244, 114, 182, 0.08) !important;
    }

    /* Pure White Input Fields */
    div[data-baseweb="input"],
    div[data-baseweb="input"] > div,
    div[data-baseweb="base-input"],
    div[data-baseweb="select"],
    div[data-baseweb="select"] *,
    input {
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
        border-color: #f9a8d4 !important;
        border-radius: 10px !important;
    }

    /* Dropdown Arrow & Menu */
    div[data-baseweb="select"] svg {
        fill: #111827 !important;
        color: #111827 !important;
    }

    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[data-baseweb="menu"],
    li[data-baseweb="menu-item"] {
        background-color: #ffffff !important;
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
    }

    li[data-baseweb="menu-item"]:hover,
    li[aria-selected="true"] {
        background-color: #fdf2f8 !important;
        color: #be185d !important;
        -webkit-text-fill-color: #be185d !important;
    }

    /* Stepper Buttons for DIA Numbers */
    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"] {
        background-color: #fce7f3 !important;
        color: #be185d !important;
        border: 1px solid #f472b6 !important;
        border-radius: 6px !important;
    }
    button[data-testid="stNumberInputStepDown"]:hover,
    button[data-testid="stNumberInputStepUp"]:hover {
        background-color: #fbcfe8 !important;
    }

    /* Interactive Gradient Action Buttons */
    .stButton > button, 
    [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #ec4899 0%, #db2777 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.65rem 1.6rem !important;
        box-shadow: 0 4px 14px rgba(219, 39, 119, 0.35) !important;
        transition: all 0.2s ease-in-out !important;
    }

    .stButton > button *, 
    [data-testid="stFormSubmitButton"] > button * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
    }

    .stButton > button:hover, 
    [data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(219, 39, 119, 0.45) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"], 
    section[data-testid="stSidebar"] > div {
        background-color: #fff5f7 !important;
        border-right: 1.5px solid #fbcfe8 !important;
    }
</style>
""", unsafe_allow_html=True)

EXCEL_FILE = "contractor_data.xlsx"

# Define DIA columns
DIA_COLUMNS = [col.upper().strip() for col in [
    "63DIA", "75 DIA", "90 DIA", "110 DIA", "125 DIA", "140 DIA", "160 DIA", "180 DIA", "200 DIA"
]]

# Complete list of panchayats
PANCHAYATS = [
    "Aaspurdevsara", "Aaurain", "Atroramipur & Turkoli", "Baejalpur", "BANBIRPUR",
    "Behta & Bijhala", "Barokhan", "Bhatti khurd", "Bhikhampur & Kopa", "Binaeka",
    "Bind", "Dafra", "Dahi", "Deduaa", "Dhansar & Banpurva", "Dhaurahra & Dhanepurple",
    "Diyawa & Keotali", "Gahbra", "Govindpur", "Harikapura", "Harraipatti & Labeda",
    "Kabirpur", "Lakhipur Kapsa & Bhushar", "Majhagaon", "ParvatpurSuleman", "Pithapur",
    "Puredalpatshah & Gauhani", "Saphachhat", "Umapur & Madramu", "Umardiha", "Amarpur",
    "Amsauna & Dohari", "Asalpur", "Baseerpur", "Chakamajhanipur & Pragaspur",
    "Chaukhara & Saraygani", "Dharampur", "Gahari Chak", "Gavan Patti & Ganai Diha",
    "Goi", "Gopalpur", "Harjamau", "Hosiyarpur", "Jaisinghgardh", "Kanpamandhupur",
    "KaranpurKhujahi", "Khbhor", "Kothiyahi", "Maruaan & Saraynakar", "Miranpur & Rajapur Mufharid",
    "Pandari Jabar", "PipriKhalsa", "Praanpur", "Rakha", "Sarkhailpur", "Srinathpur", "Tala",
    "Aamipur", "Aemapur Bindhan", "Aruhari", "Baburai Jahapur", "Badhwait", "Bahorikpur",
    "Bakol & Arjun Ateru", "BALLA & DHAMMOHAN", "BASWAHI", "Bhaesana", "Bharatgarh & Saheb Ateru",
    "BhawaniganjKota", "Bidhasin", "Chaurang", "Diha Balai", "Fatuhabad", "GUJUWAR & SARAY CHATTA",
    "Goghar", "Govind Nagar", "Raipur Barkhi Jalalpur Diwha", "Jaichandrapur & Muraini",
    "Jhingur & Gopalapur", "Kajipur Kusemer", "Kanava", "Kodar Khurd & Rahuwar", "Lallupatti",
    "Machheha Harda Patti", "Mahewa Malkiya", "Maladhar Chhatta", "Mohammadpur Sohag", "Nariyawan",
    "Patna", "Pritampur", "Puraeli Makhdumpur", "Pure Jhau", "Pure Masvan", "Purmai Sultanpur",
    "Raygardh", "Raikashipur", "Rajapur", "Ramaipur", "Ramnagar", "Salembhadari",
    "Salempur Dadeura & Kajepur Karam Husen", "Sarai Swami", "Saray Khandev", "Saray gopal",
    "TANDA AND PEENG", "Wajirpur", "Aaemna Jaatupur & Samnaspur Daamno", "Aautaarpur", "Bansiyara",
    "Barbaspur", "Barna", "Bedhan Gopalpur", "Bhawanpur", "Bhitara & Hariharpur", "BhitipureNain",
    "Bihariya", "Bikara", "Burhepur", "Chakwad", "Chhatar", "Chheuga", "Devari Hardoi Patti & Narangapur",
    "Devarpatti & Silawatpur", "Dhanvaasa & Kodrajeet", "Galgali, Tarapur Kandai", "Garibpur", "Gogaer",
    "Jamlamau", "Kamaarjeet Patti", "Kamoli Veerbhanupur", "Kanupur", "Kashipur Dibuki",
    "Khargipur & Phoolpur Rama", "Khasar", "Khatwara", "Khemkaranpur", "Kodrasal", "Korahi", "Kuda",
    "Maharajpur", "Malaak Tilhai", "Mandal Bhausaw", "Meerpur Banohi", "Pariyawan & Lochangarh",
    "Pithipur", "Ramdaspatti", "Ramgarh Banohi", "Rampur", "Raipur", "Sarai Babuin & Dharhupur",
    "Sarai Naahra", "Saray Mahasingh", "Saray Said Kha", "Sheshapur Chauras", "Siya", "Tekki Patti",
    "Tiwari Mehmadapur", "Trilokpur & Bhav", "Umari Bujurg", "Umari Kotila", "Umarpatti", "Aandharipur",
    "Antamau", "Asthan", "Badera", "Badgau", "Bariyavan & Natohi", "Bijalipur Bangadhwa & Trilochanpur",
    "Bramhauli", "Chachamau", "Chandapur & Dayalpur", "Chaurahi & Bajhabit & Miragadwa",
    "Chindaura & Seshomohammadpur", "Eethu", "Jajupur", "Janvamau", "Kakriha & Abdulwahidganj",
    "Kandaru", "Karamganj & Samaspur Sailwara", "Kasipur", "Keravdiha", "Lathtara", "Maddupur & Rokiyapur",
    "Madhwapur", "Manar & Ranimau", "Mishrpur", "Mohamidpur And Kiyawan", "Parsai", "Pithanapur",
    "Rajwapur", "Rewali", "Sangrampur & Hinahu", "Seshpur", "Seshpurdhnpur", "Tiwaripur", "Adhiya",
    "Ahibaranpur", "Akthiyari Kotila", "Bachandamau", "Bachrauli", "Bahadurpur", "Banemau Uparhar",
    "Bhadri & Bishiya", "Chakadarali", "Chakaparanpur", "Chausa", "Dadauli", "Deeha", "Dilerganj",
    "Dumwamai", "Gayaspur", "Itaura", "Jakhamai", "Jasholi & Kushahil Bazar", "Kaema",
    "Kajipur Maharajganj", "Karenati", "Keshavpura & Rudauli", "Khemipur", "Kushildiha", "Launda & Mamauli",
    "Maharajpur & Kashipur Mohan", "Mahewamohanpur & Mohaddinagar Uparhar", "Majhilgaon", "Malakarajakpur",
    "Mauli", "Mavai Kalan", "Naubasta", "Pahadpur Banohi", "Panahnagarbarai", "Parewanarayanpur",
    "Parsipur", "Peer Nagar", "Pingri", "Raiypur", "Rehwai", "Sahabpur & Tajunddinpur", "Sahumai",
    "Saja", "Saraykirat", "Sariya Praveshpur", "Sekhpur Asik", "Shahpur Uparhar", "Shergarh & Sariyawa",
    "Sujauli", "Barapur Bhika", "Gaheri", "Sarai Makai", "Asainapur & Dagrara", "Asrahi", "Basupur",
    "Belha", "Bhojpur", "Devapur", "Gaukhadi & Udhranpur", "Khajuri", "Khemsari", "Mandipur", "Medhawan",
    "Pahadpur", "Pandri", "Parsupur", "Pure Bansi", "Pure Roop", "Puretilakram", "Ramgarhkhas & Hulasgarh",
    "Rangardh Raela & Saray Raju", "Rangauli", "Rohada & Delhupur & Kalapur", "Sarayjagat Singh",
    "Saraynarayan Singh & Bhebhaura", "Saripur", "Tarapur", "Bhagwanpur", "Lilauli", "Madhupur", "Puraila",
    "Rampur Mustarka", "Amuwahi", "Atarsand & Parsupur", "Aurangabad", "Barasarai", "Barhupur", "Bhaedpur",
    "Bhausiya", "Choumari", "Darchut", "Dehridigar", "Dhraulimufrid & Chanduadih", "Gehrauli", "Hardoi",
    "Hathsara", "Itwa", "Kansapatti", "Koni & Salahipur Kanjas", "Lauli Pokhatakham", "Madura Raniganj & Sarauli",
    "Malaak", "Mandah & Bojhi", "Mangraura", "Nevra", "Padumpur", "Parsanda", "Purebhikha & Raigarh",
    "Puremanikanth", "Sakra", "Sarayjmuvari", "Sheshapur Adharganj", "Shivpur Khurd", "Sirsidih",
    "Suryagarhjagannath", "Utras", "Bahuta", "Basauli", "Beerpura Khurd & Parsad", "Besaar", "Bhavranpur",
    "Bibipur Baradih", "Charaeya & Asudi", "Chintamanipur & Andevari", "Dadupur", "Dhuti",
    "Gogalapur & Puredeojani", "Kohraov", "Kukuvar", "Mahadaha", "Marha", "Naurangabad", "Parsani",
    "Purebasan & Aaumisaraysaifkha", "Raichandrapatti & Arila", "RampurBela", "Sarastpur", "Sardeeh",
    "Srinathpur & Mariyampur", "Sumatpur", "Tardha", "Thanegopapur", "Umarpur & Bani", "Usrauli",
    "Varikhurd & Dashrathpur", "Virauti & Ramkola", "Alipur", "Arjunpur & Madhukarpur", "Batauli", "Bharatpur",
    "Budhiyapur", "Bijumau", "Birbhadrapur", "Chakerhi & Nevada Kalan", "Digaosi", "Jamalpur",
    "Kalyanpur & Purefhattesingh", "Kanyaeyadullapur & Harnahar", "Kedaura", "Kherapurechemi & Purebasantray",
    "Lakuri", "Lohangpur", "Madamai", "Mishrainpur", "Mohammadpur Khas", "Mothin", "Narayanpur", "Pure Chhattu",
    "Pure Gajai", "Pure Jodha", "Rampur Vavli", "Saray Lalmati & Khandwa", "Bandanpur & Teuanga",
    "Bhilampur & Bahlolpur", "Chakbantod", "Chaukhandpureanti", "Gode", "Ishipur", "Jagdeeshpur & Purebhaiya",
    "Jahnaipur & Kushami & Saraybheliya", "Jaitipurkathar", "Kadipur And Bhanva", "Katkavalli",
    "Khampur & Saray Dali", "Kisundadpur & Mahuaar", "Madupur, Sakrauli & Ajgara", "Naubasta & Kushfara",
    "Nevada Kala & Dekahi", "Pratapgarhgramin & Banbeerkach", "Pure Madhav Singh & Gadichakdeiya",
    "Pure Mustafa", "Rajapur Kalan", "Ramnagar", "Saraybeerbhadra", "Setapur", "Variya Samudra", "Arjunpura",
    "Ashapur & Chaubeypur", "Bajhan", "Bansi", "Barendra & Singhni", "Barista & Basupur", "Bhadausi & Rampur Praan",
    "Bhawanipur", "Dandupur Daulat", "Gauhani & Pachkhara", "Gaura Dand", "Gobari", "Jalapur", "Kalayanpur Mauraha",
    "Kalyanpur Dadiwach", "Khaira Gaurbari & Adhaarpur", "Lakhraon", "Makaipur", "Mehmadapur", "Nari",
    "Para Hamidpur", "Pure Bharat", "Pure Pandey Kamora & Tejgarh", "Pure Parmeshwar", "Rajapur Raeniya & Nevada Gauradand",
    "Sandwa Chandika And Katka Manpur", "Sangrampur", "Shivrajpur", "Sukulpur & Chauraha", "Tiwaripur",
    "Trilokpur Visai", "Upadhyaypur", "Usari", "Aasanva", "Alavalpur", "Amawa & Semra", "Atheha", "Badshapur",
    "Bewali", "Bhagatpur", "Bhawanigarh", "Deuma Poorab", "Gadiyaan & Shukulpur", "Indilpur", "Jogapur", "Katehti",
    "Khanipur", "Kumbhidiha", "Muraeni", "Narval", "Pattikachera & Ahabidihad", "Pedariya", "Pinjari",
    "Pranipur & Mustafabad", "Pure Bhagvat & Pure Loka", "Pure Narayandas", "Saruaava", "Singhgarh",
    "Uchapur & Rampur Kasiha", "Usmanpur", "Bijemau & Visanpur", "Jariyari", "Rajapur & Naseerpur",
    "Rasoeya & PremdarPatti"
]

# Initialize Excel file
if not os.path.exists(EXCEL_FILE):
    df_init = pd.DataFrame(columns=[
        "DATE", "RA BILL", "VENDOR CODE", "NAME OF THE CONTRACTOR", "SCHEME ID", "PANCHAYAT", "TYPE"
    ] + DIA_COLUMNS)
    df_init.to_excel(EXCEL_FILE, index=False)

# Session state initialization for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'index'
if 'selected_panchayat' not in st.session_state:
    st.session_state.selected_panchayat = ''

# Page 1: Index View
if st.session_state.page == 'index':
    st.markdown("<h1 style='text-align: center;'>🏛️ GRAMA PANCHAYAT PORTAL</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #4b5563; font-weight: 500;'>Select your Grama Panchayat to continue</p>", unsafe_allow_html=True)
    
    st.write("")
    selected_panchayat = st.selectbox("Select Panchayat", ["-- Select Panchayat --"] + PANCHAYATS)
    
    st.write("")
    if st.button("Continue ➡️", use_container_width=True):
        if selected_panchayat != "-- Select Panchayat --":
            st.session_state.selected_panchayat = selected_panchayat
            st.session_state.page = 'details'
            st.rerun()
        else:
            st.error("Please select a valid Panchayat.")

# Page 2: Details View
elif st.session_state.page == 'details':
    if st.button("⬅️ Back"):
        st.session_state.page = 'index'
        st.rerun()
        
    st.markdown("<h1 style='text-align: center;'>CONTRACTOR DETAILS</h1>", unsafe_allow_html=True)
    st.info(f"📍 **Selected Panchayat:** {st.session_state.selected_panchayat}")
    
    with st.form("contractor_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            contractor_name = st.text_input("Contractor Name")
            vendor_code = st.text_input("Vendor Code")
            scheme_id = st.text_input("Scheme ID")
            
        with col2:
            ra_bill = st.text_input("RA Bill")
            work_date = st.date_input("Work Date", value=datetime.today())
            
        st.markdown("<h3 style='margin-top: 15px;'>📏 DIA Values</h3>", unsafe_allow_html=True)
        dia_cols = st.columns(3)
        dia_values = {}
        
        for i, dia_label in enumerate(DIA_COLUMNS):
            with dia_cols[i % 3]:
                dia_values[dia_label] = st.number_input(f"{dia_label}", min_value=0, value=0, step=1)
                
        st.write("")
        submitted = st.form_submit_button("💾 Submit Details", use_container_width=True)
        
        if submitted:
            if not contractor_name or not vendor_code or not scheme_id or not ra_bill:
                st.error("Please fill in all required fields!")
            else:
                formatted_date = work_date.strftime("%d-%m-%Y")
                
                # Load Excel
                if os.path.exists(EXCEL_FILE):
                    df = pd.read_excel(EXCEL_FILE)
                    df.columns = df.columns.str.strip().str.upper()
                else:
                    df = pd.DataFrame(columns=[
                        "DATE", "RA BILL", "VENDOR CODE", "NAME OF THE CONTRACTOR", "SCHEME ID", "PANCHAYAT", "TYPE"
                    ] + DIA_COLUMNS)
                
                # Prepare new row data
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
                    
                # Append and save
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_excel(EXCEL_FILE, index=False)
                
                st.success("Details submitted and saved successfully!")
                st.balloons()

    # Sidebar: Data export
    with st.sidebar:
        st.header("📂 Data Export")
        if os.path.exists(EXCEL_FILE):
            with open(EXCEL_FILE, "rb") as file:
                st.download_button(
                    label="📥 Download Data Sheet",
                    data=file,
                    file_name="contractor_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
