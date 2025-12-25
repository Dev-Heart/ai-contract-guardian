import os
import langextract as lx
from .contract_rules import ContractAnalysis
from dotenv import load_dotenv

load_dotenv()

def process_contract(text: str, api_key: str = None):
    """
    Uses LangExtract to analyze a contract against the defined Legal Risk Schema.
    """
    key = api_key or os.getenv("LANGEXTRACT_API_KEY") or os.getenv("GOOGLE_API_KEY")
    
    if not key:
        raise ValueError("Missing API Key. Please provide one or set it in .env")

    # Define the extraction prompt
    description = (
        "Extract high-risk clauses, key dates, and fairness assessments from the provided legal contract. "
        "Pay special attention to automatic renewals, limitation of liability, termination rights, and confidentiality terms. "
        "Ensure all extracted original_text matches the source document exactly."
    )

    # Use LangExtract to perform the structured extraction
    try:
        result = lx.extract(
            text_or_documents=text,
            prompt_description=description,
            output_schema=ContractAnalysis,
            api_key=key,
            model_id="gemini-1.5-flash", 
            fence_output=True 
        )
        return result
    except Exception as e:
        # Capture and log detailed error for debugging
        error_msg = f"LangExtract Error Type: {type(e).__name__} | Error Details: {str(e)}"
        print(error_msg)
        # We can also store this in st.session_state if we want to show it in UI
        return {"error": error_msg}
