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
st.sidebar.info("This tool uses Google's LangExtract to analyze legal documents for risk.")

# Separate the info from the input to prevent overlap
api_key = st.sidebar.text_input(
    "Gemini API Key", 
    type="password", 
    help="Get your key at https://aistudio.google.com/app/apikey",
    placeholder="Paste your key here and press enter"
)

# Main Header
st.title("🛡️ AI Contract Guardian")
st.markdown("### Protect your business from 'Gotcha' clauses and risky legal terms.")
st.divider()

# State Management for AI Analysis
if "ai_analysis_triggered" not in st.session_state:
    st.session_state.ai_analysis_triggered = False

# Reset state if a new file is uploaded
def reset_ai_state():
    st.session_state.ai_analysis_triggered = False

# File Upload
uploaded_file = st.file_uploader("Upload your contract (PDF)", type="pdf", on_change=reset_ai_state)

if uploaded_file:
    if not api_key:
        st.warning("👈 Please enter your Gemini API Key in the sidebar to begin.")
    else:
        # Step 1: Manual Trigger
        if not st.session_state.ai_analysis_triggered:
            st.success(f"✅ Document ready: **{uploaded_file.name}**")
            st.info("💡 **Ready?** Click the button below to start the AI Forensic Scan.")
            if st.button("🚀 Analyse Contract", use_container_width=True, type="primary"):
                st.session_state.ai_analysis_triggered = True
                st.rerun()
            st.stop()

        # Step 2: Processing
        with st.status("Analyzing your contract... (This may take a minute)", expanded=True) as status:
            st.write("📖 Extracting text from PDF...")
            # Save temp file
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            try:
                contract_text = extract_text_from_pdf(temp_path)
                st.write(f"📝 Text extracted ({len(contract_text)} characters)")
                
                st.write("🧬 Running LangExtract Forensic Engine...")
                analysis = process_contract(contract_text, api_key=api_key)
                
                # Check for errors in analysis object
                if isinstance(analysis, dict) and "error" in analysis:
                    status.update(label="Analysis Failed", state="error")
                    st.error(f"🚨 **Processing Error**: {analysis['error']}")
                    st.info("Common fixes: Check if your API key is correct and has access to the Gemini 1.5 Flash model.")
                    st.stop()
                elif analysis:
                    status.update(label="Analysis Complete!", state="complete", expanded=False)
                else:
                    status.update(label="Analysis Failed", state="error")
                    st.error("There was an unknown error processing your contract.")
                    st.stop()
            finally:
                # Always cleanup
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        # 3. Display Results
        if analysis and not isinstance(analysis, dict):
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

else:
    st.info("👋 **Welcome to AI Contract Guardian**\n\n1. Enter your API key in the sidebar.\n2. Upload a PDF contract to start.")

st.divider()
st.caption("Developed by Divine Heart • Powered by LangExtract")

st.divider()
st.caption("Developed by Divine Heart • Powered by LangExtract")
