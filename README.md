#Grama Panchayat Portal - Streamlit

Run locally

pip install -r requirements.txt
streamlit run app.py

Deploy on Streamlit Community Cloud

Create a GitHub repository.

Upload app.py and requirements.txt.

Open Streamlit Community Cloud.

Select the repository and app.py.

Deploy.

Important

The included app stores submitted records in Streamlit session memory and lets you download them as CSV.

For permanent multi-user storage after deployment, connect the submit function to:

Google Sheets

Supabase

Firebase

PostgreSQL / MySQL

Replace the sample PANCHAYATS list with your actual Panchayat names.
