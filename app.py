import streamlit as st
import os
from engine.ingestion import extract_text_from_pdf
from engine.processor import process_contract

# Set professional page config
st.set_page_config(
    page_title="AI Contract Guardian",
    page_icon="🛡️",
    layout="wide"
)

# Sidebar: Configuration
st.sidebar.title("⚙️ Setup")
api_key = st.sidebar.text_input("Gemini API Key", type="password", help="Get your key at https://aistudio.google.com/app/apikey")
st.sidebar.info("This tool uses Google's LangExtract to analyze legal documents for risk.")

# Main Header
st.title("🛡️ AI Contract Guardian")
st.markdown("### Protect your business from 'Gotcha' clauses and risky legal terms.")
st.divider()

# File Upload
uploaded_file = st.file_uploader("Upload your contract (PDF)", type="pdf")

if uploaded_file and api_key:
    # 1. Show processing status
    with st.status("Analyzing your contract... (This may take a minute)", expanded=True) as status:
        st.write("📖 Extracting text from PDF...")
        # Save temp file
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        contract_text = extract_text_from_pdf(temp_path)
        st.write(f"📝 Text extracted ({len(contract_text)} characters)")
        
        st.write("🧬 Running LangExtract Forensic Engine...")
        analysis = process_contract(contract_text, api_key=api_key)
        
        if analysis:
            status.update(label="Analysis Complete!", state="complete", expanded=False)
        else:
            status.update(label="Analysis Failed", state="error")
            st.error("There was an error processing your contract. Please check your API key.")
            st.stop()
        
        # Cleanup
        os.remove(temp_path)

    # 2. Display Results
    if analysis:
        # Header Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Contract Type", analysis.contract_type)
        with col2:
            st.metric("Fairness Score", f"{analysis.fairness_score}/100")
        with col3:
            st.metric("High-Risk Terms", len(analysis.high_risk_clauses))

        # Overview
        st.subheader("📋 Executive Summary")
        st.info(analysis.overall_summary)

        # Risk Details
        st.subheader("🚩 Identified Risks")
        if analysis.high_risk_clauses:
            for clause in analysis.high_risk_clauses:
                with st.expander(f"{clause.clause_name} - Level: {clause.risk_level}"):
                    st.warning(clause.summary)
                    st.markdown("**Evidence from text:**")
                    st.caption(f"\"{clause.original_text}\"")
        else:
            st.success("No high-risk clauses were found.")

        # Key Dates
        st.subheader("📅 Key Dates & Deadlines")
        if analysis.key_dates:
            for date in analysis.key_dates:
                st.write(f"- **{date.event}**: {date.date_description}")
                if date.risk_summary:
                    st.caption(f"💡 {date.risk_summary}")
        else:
            st.info("No specific deadlines were identified.")

elif not api_key:
    st.warning("Please enter your Gemini API Key in the sidebar to begin.")

st.divider()
st.caption("Developed by Divine Heart • Powered by LangExtract")
