# 🛡️ AI Contract Guardian

**AI Contract Guardian** is a high-end legal-tech forensic tool designed to protect businesses and individuals from "Gotcha" clauses in contracts. Using Google's **LangExtract** and **Gemini LLMs**, it extracts high-risk terms, critical deadlines, and provides an objective fairness assessment of any legal agreement.

## 🚀 Features
- **Forensic Clause Extraction**: Identifies predatory terms like hidden limitation of liability, automatic renewals, and one-sided termination rights.
- **Source Grounding**: Prevents AI hallucinations by forcing the model to cite the exact original text from the provided PDF.
- **Fairness Scoring**: A proprietary scoring system (1-100) that evaluates how balanced a contract is for the signing party.
- **Deadline Calendar**: Automatically identifies and lists key notification and renewal dates.
- **Structured Data**: Exports all legal risks into machine-readable JSON formats powered by Pydantic.

## 🛠️ Technology Stack
- **Core Library**: [LangExtract](https://github.com/google/langextract) (Google)
- **AI Model**: Gemini 1.5/2.0
- **Web Interface**: Streamlit
- **Document Ingestion**: PyMuPDF

## 📦 Installation & Setup

1. **Clone and Enter**:
   ```bash
   git clone [your-repo-url]
   cd ai-contract-guardian
   ```

2. **Initialize Environment**:
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set API Key**:
   Create a `.env` file or provide your key directly in the app.
   ```bash
   export LANGEXTRACT_API_KEY="your-gemini-key"
   ```

4. **Launch Application**:
   ```bash
   streamlit run app.py
   ```

## 🏗️ Project Structure
```text
ai-contract-guardian/
├── app.py              # Main Streamlit UI
├── engine/             # Core AI & Extraction Logic
│   ├── contract_rules.py # Pydantic Legal Schema
│   ├── ingestion.py      # PDF text extraction
│   └── processor.py      # LangExtract integration
├── data/               # Sample documents
└── outputs/            # Extracted logs and reports
```

## 👨‍💻 Developed by
**Divine Heart** – *Empowering users through automated forensic intelligence.*
