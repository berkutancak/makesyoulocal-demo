import streamlit as st
import pandas as pd
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="Ops & Automation Toolbox", layout="wide", page_icon="🛠️")

# Pulling Secrets from Streamlit Dashboard
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
except Exception as e:
    st.error("API Key missing or invalid. Please check Streamlit Secrets.")

# --- SIDEBAR ACCESS CONTROL ---
st.sidebar.title("🔐 Access Control")
access_password = st.sidebar.text_input("Enter Access Key:", type="password")
st.sidebar.info("This prototype is protected to manage API limits. Key: makesyoulocal-2026")

st.title("🛠️ Automation Operations Toolbox")
st.write("Supporting MakesYouLocal's mission through AI-driven operational clarity.")

# Password Protection Logic
if access_password == st.secrets["APP_PASSWORD"]:

    tab1, tab2 = st.tabs(["📝 Friction-to-SOP", "📊 Ticket Insight Triage"])

    # --- TAB 1: SOP GENERATOR ---
    with tab1:
        st.header("Friction-to-SOP Generator")
        st.info("Convert messy process brain-dumps into professional documentation.")
        
        messy_input = st.text_area("Describe the process:", 
                                   placeholder="e.g., When a customer asks for a refund in Dixa, I check Shopify...",
                                   height=200,
                                   max_chars=3000)

        if st.button("Generate SOP"):
            if messy_input:
                with st.spinner("Gemini is structuring your documentation..."):
                    prompt = (
                        f"Convert the following messy process description into a professional SOP. "
                        f"Use Markdown headings: Objective, Prerequisites, Step-by-Step Instructions, and Troubleshooting. "
                        f"Process: {messy_input}"
                    )
                    response = model.generate_content(prompt)
                    st.markdown("---")
                    st.markdown(response.text)
            else:
                st.warning("Please enter a process description.")

    # --- TAB 2: TICKET TRIAGE ---
    with tab2:
        st.header("Ticket-to-Insight Triage")
        st.info("Upload a CSV of support tickets to identify automation opportunities.")
        
        uploaded_file = st.file_uploader("Upload Ticket Export (CSV)", type="csv")
        
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.write("Data Preview:", df.head())
            
            if st.button("Analyze for Automation"):
                with st.spinner("Analyzing patterns..."):
                    ticket_data = df.to_string(index=False)[:5000]
                    prompt = (
                        f"Analyze these e-commerce support tickets. "
                        f"1. Identify top 3 recurring themes. "
                        f"2. Suggest one specific automation for each (e.g., via Make.com or Dixa). "
                        f"Focus on the 'Market' column to see if issues are specific to a country. Data: {ticket_data}"
                    )
                    response = model.generate_content(prompt)
                    st.subheader("🤖 AI Insights")
                    st.write(response.text)

else:
    if access_password == "":
        st.warning("Please enter the Access Key in the sidebar to unlock.")
    else:
        st.error("Incorrect Access Key.")
