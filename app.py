/* ============================================================
   SIDEBAR — PROFESSIONAL PANCHAYAT BRANDING
   ============================================================ */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #fff8fc 0%,
        #fff0f7 55%,
        #ffe8f2 100%
    ) !important;

    border-right: 1px solid #f3c4d9 !important;
}

section[data-testid="stSidebar"] > div {
    background: transparent !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #172554 !important;
    -webkit-text-fill-color: #172554 !important;
}

/* Panchayat logo/title */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 4px 28px 4px;
}

.sidebar-logo {
    width: 42px;
    height: 42px;
    border-radius: 12px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: linear-gradient(
        135deg,
        #8b5cf6,
        #ec4899
    );

    color: white !important;
    font-size: 23px;
    box-shadow: 0 7px 18px rgba(139, 92, 246, .22);
}

.sidebar-title {
    font-size: 17px;
    font-weight: 800;
    color: #172554 !important;
    line-height: 1.2;
}

.sidebar-subtitle {
    font-size: 11px;
    color: #8b5cf6 !important;
    font-weight: 600;
    margin-top: 3px;
}

/* Sidebar section */
.sidebar-section-title {
    font-size: 11px;
    font-weight: 800;

    letter-spacing: 1.3px;

    color: #9d174d !important;

    margin-bottom: 8px;
}

/* Download button — NO BLACK BOX */
section[data-testid="stSidebar"]
.stDownloadButton > button {

    background: transparent !important;
    background-color: transparent !important;

    border: none !important;

    box-shadow: none !important;

    color: #be185d !important;
    -webkit-text-fill-color: #be185d !important;

    font-size: 14px !important;
    font-weight: 700 !important;

    padding: 7px 0 !important;

    justify-content: flex-start !important;

    transition: all .2s ease;
}

section[data-testid="stSidebar"]
.stDownloadButton > button * {

    color: #be185d !important;
    -webkit-text-fill-color: #be185d !important;

    background: transparent !important;
}

section[data-testid="stSidebar"]
.stDownloadButton > button:hover {

    background: transparent !important;

    transform: translateX(4px);

    box-shadow: none !important;
}


/* ============================================================
   STRONGER PANCHAYATS QUOTE
   ============================================================ */

.sidebar-quote {

    position: absolute;

    bottom: 55px;

    left: 25px;
    right: 25px;

    text-align: center;

    padding: 18px 10px;
}


/* decorative top line */
.sidebar-quote::before {

    content: "✦  ✦  ✦";

    display: block;

    color: #f9a8d4 !important;

    font-size: 13px;

    margin-bottom: 9px;
}


/* Main quotation */
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

    -webkit-text-fill-color: #db2777 !important;
}


/* second line */
.sidebar-quote-main span {

    color: #7c3aed !important;

    -webkit-text-fill-color: #7c3aed !important;
}


/* heart */
.sidebar-heart {

    margin: 9px 0;

    color: #ec4899 !important;

    font-size: 14px;
}


/* supporting text */
.sidebar-quote-small {

    font-size: 11px;

    line-height: 1.5;

    color: #9d174d !important;

    -webkit-text-fill-color: #9d174d !important;

    opacity: .75;
}


/* small decorative village */
.sidebar-village {

    margin-top: 13px;

    font-size: 28px;

    letter-spacing: 5px;

    opacity: .75;
}
