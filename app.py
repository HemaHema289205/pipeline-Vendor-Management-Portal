

from flask import Flask, render_template_string, request, redirect, jsonify
import pandas as pd
import os
from datetime import datetime
import random
import string

app = Flask(__name__)
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

# Initialize Excel file with correct structure
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=[
        "DATE", "RA BILL", "VENDOR CODE", "NAME OF THE CONTRACTOR", "SCHEME ID", "PANCHAYAT", "TYPE"
    ] + DIA_COLUMNS)
    df.to_excel(EXCEL_FILE, index=False)

# Generate a random ID for form elements
def generate_random_id(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# HTML template for index page
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grama Panchayat Portal</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Orbitron', sans-serif;
            background: #0a0a1a;
            color: #e0e0ff;
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }
        
        /* Animated background */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, #0a0a1a, #1a0a2a, #2a0a3a);
            z-index: -2;
        }
        
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
        }
        
        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(100, 200, 255, 0.5);
            border-radius: 50%;
            animation: float 15s infinite linear;
        }
        
        @keyframes float {
            0% {
                transform: translateY(100vh) translateX(0);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100vh) translateX(100px);
                opacity: 0;
            }
        }
        
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
            position: relative;
            z-index: 1;
        }
        
        .logo {
            margin-bottom: 30px;
            text-align: center;
            animation: pulse 2s infinite alternate;
        }
        
        @keyframes pulse {
            0% {
                transform: scale(1);
            }
            100% {
                transform: scale(1.05);
            }
        }
        
        .logo i {
            font-size: 4rem;
            background: linear-gradient(45deg, #00c6ff, #0072ff);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 0 30px rgba(0, 114, 255, 0.5);
        }
        
        .title {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #00c6ff, #0072ff, #7b2ff7);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-align: center;
            letter-spacing: 2px;
        }
        
        .subtitle {
            font-size: 1rem;
            color: #a0a0ff;
            margin-bottom: 40px;
            text-align: center;
            letter-spacing: 1px;
        }
        
        .card {
            width: 100%;
            max-width: 500px;
            background: rgba(20, 20, 40, 0.7);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(100, 100, 255, 0.2);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5), 
                        0 0 0 1px rgba(100, 100, 255, 0.1) inset;
            padding: 30px;
            transform: translateY(0);
            transition: all 0.3s ease;
            animation: slideUp 0.8s ease-out;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), 
                        0 0 0 1px rgba(100, 100, 255, 0.2) inset;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        .form-label {
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            color: #a0c0ff;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .search-container {
            position: relative;
            margin-bottom: 15px;
        }
        
        .search-input {
            width: 100%;
            padding: 15px 20px 15px 50px;
            background: rgba(30, 30, 60, 0.5);
            border: 1px solid rgba(100, 100, 255, 0.3);
            border-radius: 50px;
            color: #e0e0ff;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        .search-input:focus {
            outline: none;
            border-color: #0072ff;
            box-shadow: 0 0 15px rgba(0, 114, 255, 0.3);
            background: rgba(40, 40, 80, 0.7);
        }
        
        .search-icon {
            position: absolute;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            color: #7090ff;
        }
        
        .select-container {
            position: relative;
        }
        
        .select-input {
            width: 100%;
            padding: 15px 20px;
            background: rgba(30, 30, 60, 0.5);
            border: 1px solid rgba(100, 100, 255, 0.3);
            border-radius: 15px;
            color: #e0e0ff;
            font-size: 1rem;
            appearance: none;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .select-input:focus {
            outline: none;
            border-color: #0072ff;
            box-shadow: 0 0 15px rgba(0, 114, 255, 0.3);
            background: rgba(40, 40, 80, 0.7);
        }
        
        .select-arrow {
            position: absolute;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            color: #7090ff;
            pointer-events: none;
        }
        
        .btn {
            display: block;
            width: 100%;
            padding: 15px;
            background: linear-gradient(45deg, #0072ff, #7b2ff7);
            border: none;
            border-radius: 50px;
            color: white;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 10px;
            position: relative;
            overflow: hidden;
            z-index: 1;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, #7b2ff7, #0072ff);
            z-index: -1;
            transition: all 0.3s ease;
            opacity: 0;
        }
        
        .btn:hover::before {
            opacity: 1;
        }
        
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0, 114, 255, 0.3);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .suggestions {
            position: absolute;
            top: 100%;
            left: 0;
            width: 100%;
            max-height: 200px;
            overflow-y: auto;
            background: rgba(30, 30, 60, 0.9);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(100, 100, 255, 0.3);
            z-index: 10;
            display: none;
        }
        
        .suggestion-item {
            padding: 12px 20px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .suggestion-item:hover {
            background: rgba(100, 100, 255, 0.2);
        }
        
        .footer {
            margin-top: 40px;
            text-align: center;
            color: #606080;
            font-size: 0.8rem;
        }
        
        @media (max-width: 768px) {
            .title {
                font-size: 2rem;
            }
            
            .card {
                max-width: 90%;
            }
        }
    </style>
</head>
<body>
    <div class="particles" id="particles"></div>
    
    <div class="container">
        <div class="logo">
            <i class="fas fa-landmark"></i>
        </div>
        
        <h1 class="title">GRAMA PANCHAYAT PORTAL</h1>
        <p class="subtitle">Select your Grama Panchayat to continue</p>
        
        <div class="card">
            <form id="panchayatForm">
                <div class="form-group">
                    <label class="form-label" for="search">Search Panchayat</label>
                    <div class="search-container">
                        <i class="fas fa-search search-icon"></i>
                        <input type="text" id="search" class="search-input" placeholder="Type to search...">
                        <div class="suggestions" id="suggestions"></div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label class="form-label" for="panchayat">Select Panchayat</label>
                    <div class="select-container">
                        <select id="panchayat" class="select-input" required>
                            <option value="">-- Select Panchayat --</option>
                            {% for panchayat in panchayats %}
                            <option value="{{ panchayat }}">{{ panchayat }}</option>
                            {% endfor %}
                        </select>
                        <i class="fas fa-chevron-down select-arrow"></i>
                    </div>
                </div>
                
                <button type="submit" class="btn">
                    <i class="fas fa-arrow-right"></i> Continue
                </button>
            </form>
        </div>
        
        <div class="footer">
            <p>&copy; 2023 Grama Panchayat Management System | All rights reserved</p>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Create floating particles
            const particlesContainer = document.getElementById('particles');
            for (let i = 0; i < 50; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 15 + 's';
                particle.style.animationDuration = (15 + Math.random() * 15) + 's';
                particlesContainer.appendChild(particle);
            }
            
            // Search functionality
            const searchInput = document.getElementById('search');
            const panchayatSelect = document.getElementById('panchayat');
            const suggestions = document.getElementById('suggestions');
            const form = document.getElementById('panchayatForm');
            
            // Filter panchayats based on search input
            searchInput.addEventListener('input', function() {
                const searchTerm = this.value.toLowerCase();
                const options = panchayatSelect.options;
                suggestions.innerHTML = '';
                
                if (searchTerm.length > 0) {
                    let matchFound = false;
                    
                    for (let i = 1; i < options.length; i++) {
                        const optionText = options[i].text.toLowerCase();
                        if (optionText.includes(searchTerm)) {
                            matchFound = true;
                            options[i].style.display = '';
                            
                            // Add to suggestions
                            const suggestionItem = document.createElement('div');
                            suggestionItem.className = 'suggestion-item';
                            suggestionItem.textContent = options[i].text;
                            suggestionItem.addEventListener('click', function() {
                                panchayatSelect.value = options[i].value;
                                searchInput.value = options[i].text;
                                suggestions.style.display = 'none';
                            });
                            suggestions.appendChild(suggestionItem);
                        } else {
                            options[i].style.display = 'none';
                        }
                    }
                    
                    suggestions.style.display = matchFound ? 'block' : 'none';
                } else {
                    for (let i = 1; i < options.length; i++) {
                        options[i].style.display = '';
                    }
                    suggestions.style.display = 'none';
                }
            });
            
            // Hide suggestions when clicking outside
            document.addEventListener('click', function(e) {
                if (!searchInput.contains(e.target) && !suggestions.contains(e.target)) {
                    suggestions.style.display = 'none';
                }
            });
            
            // Handle form submission
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                const selected = panchayatSelect.value;
                if (selected) {
                    // Add loading effect
                    const btn = form.querySelector('.btn');
                    const originalText = btn.innerHTML;
                    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                    btn.disabled = true;
                    
                    // Simulate processing delay
                    setTimeout(() => {
                        window.location.href = `/details?panchayat=${encodeURIComponent(selected)}`;
                    }, 800);
                } else {
                    // Show error effect
                    panchayatSelect.style.borderColor = '#ff4757';
                    setTimeout(() => {
                        panchayatSelect.style.borderColor = '';
                    }, 2000);
                }
            });
        });
    </script>
</body>
</html>
"""

# HTML template for details page
DETAILS_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contractor Details</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Orbitron', sans-serif;
            background: #0a0a1a;
            color: #e0e0ff;
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }
        
        /* Animated background */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, #0a0a1a, #1a0a2a, #2a0a3a);
            z-index: -2;
        }
        
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
        }
        
        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(100, 200, 255, 0.5);
            border-radius: 50%;
            animation: float 15s infinite linear;
        }
        
        @keyframes float {
            0% {
                transform: translateY(100vh) translateX(0);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100vh) translateX(100px);
                opacity: 0;
            }
        }
        
        .container {
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }
        
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            animation: slideDown 0.8s ease-out;
        }
        
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .back-btn {
            display: flex;
            align-items: center;
            background: rgba(30, 30, 60, 0.5);
            border: 1px solid rgba(100, 100, 255, 0.3);
            border-radius: 50px;
            padding: 10px 20px;
            color: #a0c0ff;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .back-btn:hover {
            background: rgba(40, 40, 80, 0.7);
            border-color: #0072ff;
            transform: translateY(-3px);
        }
        
        .back-btn i {
            margin-right: 8px;
        }
        
        .title {
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(45deg, #00c6ff, #0072ff, #7b2ff7);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-align: center;
            letter-spacing: 2px;
        }
        
        .panchayat-info {
            background: rgba(30, 30, 60, 0.5);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(100, 100, 255, 0.2);
            padding: 15px 20px;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            animation: fadeIn 1s ease-out;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        
        .panchayat-info i {
            font-size: 1.5rem;
            margin-right: 15px;
            color: #0072ff;
        }
        
        .panchayat-info span {
            font-weight: 600;
            font-size: 1.1rem;
            color: #e0e0ff;
        }
        
        .form-container {
            background: rgba(20, 20, 40, 0.7);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(100, 100, 255, 0.2);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5), 
                        0 0 0 1px rgba(100, 100, 255, 0.1) inset;
            padding: 30px;
            animation: slideUp 0.8s ease-out;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .progress-bar {
            height: 6px;
            background: rgba(30, 30, 60, 0.5);
            border-radius: 3px;
            margin-bottom: 30px;
            overflow: hidden;
        }
        
        .progress {
            height: 100%;
            background: linear-gradient(90deg, #0072ff, #7b2ff7);
            border-radius: 3px;
            width: 0%;
            transition: width 0.3s ease;
        }
        
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .form-group {
            position: relative;
        }
        
        .form-label {
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            color: #a0c0ff;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .form-input {
            width: 100%;
            padding: 15px 20px;
            background: rgba(30, 30, 60, 0.5);
            border: 1px solid rgba(100, 100, 255, 0.3);
            border-radius: 15px;
            color: #e0e0ff;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        .form-input:focus {
            outline: none;
            border-color: #0072ff;
            box-shadow: 0 0 15px rgba(0, 114, 255, 0.3);
            background: rgba(40, 40, 80, 0.7);
        }
        
        .form-icon {
            position: absolute;
            right: 15px;
            top: 42px;
            color: #7090ff;
        }
        
        .dia-section {
            background: rgba(30, 30, 60, 0.5);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
        }
        
        .dia-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .dia-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: #e0e0ff;
            display: flex;
            align-items: center;
        }
        
        .dia-title i {
            margin-right: 10px;
            color: #0072ff;
        }
        
        .dia-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 15px;
        }
        
        .dia-item {
            background: rgba(40, 40, 80, 0.7);
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            transition: all 0.3s ease;
            border: 1px solid rgba(100, 100, 255, 0.2);
        }
        
        .dia-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 114, 255, 0.2);
            border-color: #0072ff;
        }
        
        .dia-label {
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            color: #a0c0ff;
            font-size: 0.9rem;
        }
        
        .dia-input {
            width: 100%;
            padding: 10px;
            background: rgba(20, 20, 40, 0.7);
            border: 1px solid rgba(100, 100, 255, 0.3);
            border-radius: 10px;
            color: #e0e0ff;
            text-align: center;
            font-size: 1rem;
            font-weight: 600;
        }
        
        .dia-input:focus {
            outline: none;
            border-color: #0072ff;
            box-shadow: 0 0 10px rgba(0, 114, 255, 0.3);
        }
        
        .btn-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        
        .btn {
            padding: 15px 40px;
            background: linear-gradient(45deg, #0072ff, #7b2ff7);
            border: none;
            border-radius: 50px;
            color: white;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
            z-index: 1;
            display: flex;
            align-items: center;
        }
        
        .btn i {
            margin-right: 10px;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, #7b2ff7, #0072ff);
            z-index: -1;
            transition: all 0.3s ease;
            opacity: 0;
        }
        
        .btn:hover::before {
            opacity: 1;
        }
        
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0, 114, 255, 0.3);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .footer {
            margin-top: 40px;
            text-align: center;
            color: #606080;
            font-size: 0.8rem;
        }
        
        @media (max-width: 768px) {
            .header {
                flex-direction: column;
                gap: 20px;
            }
            
            .title {
                font-size: 1.5rem;
            }
            
            .form-grid {
                grid-template-columns: 1fr;
            }
            
            .dia-grid {
                grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
            }
        }
    </style>
</head>
<body>
    <div class="particles" id="particles"></div>
    
    <div class="container">
        <div class="header">
            <a href="/" class="back-btn">
                <i class="fas fa-arrow-left"></i> Back
            </a>
            <h1 class="title">CONTRACTOR DETAILS</h1>
            <div></div> <!-- Spacer for flex alignment -->
        </div>
        
        <div class="panchayat-info">
            <i class="fas fa-map-marker-alt"></i>
            <span>{{ panchayat }}</span>
        </div>
        
        <div class="form-container">
            <div class="progress-bar">
                <div class="progress" id="progress"></div>
            </div>
            
            <form id="contractorForm" action="/submit" method="post">
                <input type="hidden" name="panchayat" value="{{ panchayat }}">
                
                <div class="form-grid">
                    <div class="form-group">
                        <label class="form-label" for="contractorName">Contractor Name</label>
                        <input type="text" id="contractorName" name="contractorName" class="form-input" required>
                        <i class="fas fa-user form-icon"></i>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label" for="vendorCode">Vendor Code</label>
                        <input type="text" id="vendorCode" name="vendorCode" class="form-input" required>
                        <i class="fas fa-id-card form-icon"></i>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label" for="SchemeID">Scheme ID</label>
                        <input type="text" id="SchemeID" name="SchemeID" class="form-input" required>
                        <i class="fas fa-project-diagram form-icon"></i>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label" for="raBill">RA Bill</label>
                        <input type="text" id="raBill" name="raBill" class="form-input" required>
                        <i class="fas fa-receipt form-icon"></i>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label" for="workDate">Work Date</label>
                        <input type="date" id="workDate" name="workDate" class="form-input" required>
                        <i class="fas fa-calendar-alt form-icon"></i>
                    </div>
                </div>
                
                <div class="dia-section">
                    <div class="dia-header">
                        <h3 class="dia-title">
                            <i class="fas fa-ruler-combined"></i> DIA Values
                        </h3>
                    </div>
                    
                    <div class="dia-grid">
                        <div class="dia-item">
                            <label class="dia-label" for="bill_63">63 DIA</label>
                            <input type="number" id="bill_63" name="bill_63" class="dia-input" min="0" value="0">
                        </div>
                        <div class="dia-item">
                            <label class="dia-label" for="bill_75">75 DIA</label>
                            <input type="number" id="bill_75" name="bill_75" class="dia-input" min="0" value="0">
                        </div>
                        <div class="dia-item">
                            <label class="dia-label" for="bill_90">90 DIA</label>
                            <input type="number" id="bill_90" name="bill_90" class="dia-input" min="0" value="0">
                        </div>
                        <div class="dia-item">
                            <label class="dia-label" for="bill_110">110 DIA</label>
                            <input type="number" id="bill_110" name="bill_110" class="dia-input" min="0" value="0">
                        </div>
                        <div class="dia-item">
                            <label class="dia-label" for="bill_125">125 DIA</label>
                            <input type="number" id="bill_125" name="bill_125" class="dia-input" min="0" value="0">
                        </div>
                        <div class="dia-item">
                            <label class="dia-label" for="bill_140">140 DIA</label>
                            <input type="number" id="bill_140" name="bill_140" class="dia-input" min="0" value="0">
                        </div>
                        <div class="dia-item">
                            <label class="dia-label" for="bill_160">160 DIA</label>
                            <input type="number" id="bill_160" name="bill_160" class="dia-input" min="0" value="0">
                        </div>
                        <div class="dia-item">
                            <label class="dia-label" for="bill_180">180 DIA</label>
                            <input type="number" id="bill_180" name="bill_180" class="dia-input" min="0" value="0">
                        </div>
                        <div class="dia-item">
                            <label class="dia-label" for="bill_200">200 DIA</label>
                            <input type="number" id="bill_200" name="bill_200" class="dia-input" min="0" value="0">
                        </div>
                    </div>
                </div>
                
                <div class="btn-container">
                    <button type="submit" class="btn" id="submitBtn">
                        <i class="fas fa-save"></i> Submit Details
                    </button>
                </div>
            </form>
        </div>
        
        <div class="footer">
            <p>&copy; 2023 Grama Panchayat Management System | All rights reserved</p>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Create floating particles
            const particlesContainer = document.getElementById('particles');
            for (let i = 0; i < 50; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 15 + 's';
                particle.style.animationDuration = (15 + Math.random() * 15) + 's';
                particlesContainer.appendChild(particle);
            }
            
            // Form progress tracking
            const form = document.getElementById('contractorForm');
            const inputs = form.querySelectorAll('input[required]');
            const progressBar = document.getElementById('progress');
            
            function updateProgress() {
                let filledInputs = 0;
                inputs.forEach(input => {
                    if (input.value.trim() !== '') {
                        filledInputs++;
                    }
                });
                
                const progress = (filledInputs / inputs.length) * 100;
                progressBar.style.width = progress + '%';
            }
            
            inputs.forEach(input => {
                input.addEventListener('input', updateProgress);
            });
            
            // Form submission
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                
                const submitBtn = document.getElementById('submitBtn');
                const originalText = submitBtn.innerHTML;
                
                // Show loading state
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                submitBtn.disabled = true;
                
                // Simulate processing delay
                setTimeout(() => {
                    form.submit();
                }, 1500);
            });
        });
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(INDEX_HTML, panchayats=PANCHAYATS)

@app.route("/details")
def details():
    panchayat = request.args.get("panchayat", "")
    return render_template_string(DETAILS_HTML, panchayat=panchayat)

@app.route("/submit", methods=["POST"])
def submit():
    contractor = request.form.get("contractorName", '').strip()
    vendor_code = request.form.get("vendorCode", '').strip()
    scheme_id = request.form.get("SchemeID", '').strip()
    panchayat = request.form.get("panchayat", '').strip()
    ra_bill = request.form.get("raBill", '').strip()
    date = request.form.get("workDate", '').strip()

    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
    except ValueError:
        formatted_date = ""

    # Load existing Excel data
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        df.columns = df.columns.str.strip().str.upper()
    else:
        df = pd.DataFrame(columns=[
            "DATE", "RA BILL", "VENDOR CODE", "NAME OF THE CONTRACTOR", "SCHEME ID", "PANCHAYAT", "TYPE"
        ] + DIA_COLUMNS)

    # Prepare the new row
    bill_row = {
        "DATE": formatted_date,
        "RA BILL": ra_bill,
        "VENDOR CODE": vendor_code,
        "NAME OF THE CONTRACTOR": contractor,
        "SCHEME ID": scheme_id,
        "PANCHAYAT": panchayat,
        "TYPE": "this_bill"
    }

    # Fill DIA values
    for dia_label in DIA_COLUMNS:
        dia_value = dia_label.split()[0]
        bill_input = request.form.get(f"bill_{dia_value}", "0").strip()

        try:
            bill = int(bill_input) if bill_input else 0
        except ValueError:
            bill = 0

        bill_row[dia_label] = bill

    # Append and save
    df = pd.concat([df, pd.DataFrame([bill_row])], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

    return redirect("/")

if __name__ == "__main__":
    app.run(host='192.168.29.220', port=5000, debug=True)

    
    


