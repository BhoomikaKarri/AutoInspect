# 🌉 AutoInspect

### Multi-Agent AI Infrastructure Inspection System

AutoInspect is a multi-agent AI system for intelligent bridge infrastructure inspection that combines **document-grounded reasoning, vision-language analysis, autonomous data analysis, observability, and human-in-the-loop safety**.

## 🚀 Features

- 🤖 Multi-agent inspection workflow
- 📚 Retrieval-Augmented Generation (RAG)
- 🗄️ ChromaDB vector search
- 👁️ BLIP Vision-Language analysis
- 📊 Structured condition-rating analysis
- 🛡️ Rule-based safety gate
- 👤 Human-in-the-loop approval
- 🔍 LangSmith observability
- 🖥️ Streamlit interface

## 🧠 Architecture

```text
                    USER
                     │
          Bridge + Question + Image
                     │
                     ▼
             ┌──────────────┐
             │  Coordinator │
             └──────┬───────┘
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
   Research       Vision      Analyst
     Agent        Agent        Agent
       │            │            │
       ▼            ▼            ▼
      RAG          BLIP       Statistics
       │            │            │
       └────────────┼────────────┘
                    ▼
              Safety Layer
                    │
                    ▼
              Human Review
                    │
                    ▼
          Inspection Result

📚 RAG Pipeline

Inspection PDFs
      ↓
PDF Text Extraction
      ↓
Text Chunking
      ↓
Sentence Embeddings
      ↓
ChromaDB
      ↓
Semantic Retrieval
      ↓
Bridge-Specific Evidence
The Research Agent uses bridge-aware retrieval so evidence remains associated with the selected inspection report.

👁️ Vision Analysis

The Vision Agent uses:

Salesforce/blip-vqa-base

It provides supporting observations such as:

Concrete cracking
Rust / corrosion
Spalling
Water staining
Exposed metal / rebar
Concrete deterioration
Visible defects

Visual observations are assistive evidence and are not treated as the sole authority for inspection ratings.

📊 Data Analysis

The Analyst Agent processes structured inspection QA data.

Example:
Bridge: PUTNEY-00001

Condition Ratings:
[4, 4, 5, 4, 4, 4, 7]

Average: 4.57
Minimum: 4
Maximum: 7

🛡️ Safety & Human Review
| Condition Rating | Risk Level | Human Review            |
| ---------------- | ---------- | ----------------------- |
| ≤ 4              | HIGH       | Required                |
| 5–6              | MODERATE   | Required                |
| ≥ 7              | LOW        | Not required by default |
| Unknown          | UNKNOWN    | Required                |

Higher-risk or unverifiable results are routed through an explicit human approval/rejection gate.

Possible outcomes:

AUTO_APPROVED
HUMAN_APPROVED
HUMAN_REJECTED

🔍 LangSmith

LangSmith provides observability for the inspection workflow, including:

User inputs
Retrieval activity
Vision analysis
Agent outputs
Safety evaluation
Human-review decisions
Final inspection results

🧩 Tech Stack

Python
LangGraph
LangChain
ChromaDB
Sentence Transformers
Hugging Face Transformers
BLIP VQA
Qwen2.5-1.5B-Instruct
Streamlit
LangSmith

📁 Project Structure

AutoInspect/
├── agents/
│   ├── analyst.py
│   ├── coordinator.py
│   ├── human_review.py
│   ├── local_llm.py
│   ├── researcher.py
│   ├── safety.py
│   └── vision.py
│
├── data/
│   ├── BridgeInspRpt-DOVER-00028/
│   ├── BridgeInspRpt-GROTON-00036/
│   ├── BridgeInspRpt-MIDDLEBURY-0011A/
│   ├── BridgeInspRpt-PUTNEY-00001/
│   └── BridgeInspRpt-RICHFORD-00003/
│
├── rag/
├── tools/
├── app.py
├── hf_app.py
├── requirements.txt
├── README.md
└── .gitignore

⚙️ Run Locally

git clone https://github.com/BhoomikaKarri/AutoInspect.git
cd AutoInspect
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python rag/create_vector_db.py
streamlit run app.py

📦 Dataset

This project uses a selective subset of the BridgeEQA dataset.

Official dataset:
https://huggingface.co/datasets/hoskerelab/bridge-eqa

⚠️ Safety Disclaimer

AutoInspect is a research and portfolio prototype.

It is not a replacement for certified structural inspection, professional engineering judgment, regulatory procedures, or real-world safety certification.

AI-generated observations should be verified by qualified professionals before real-world maintenance, structural, or safety decisions.

🎯 Project Goal

AutoInspect demonstrates how agentic AI can combine retrieval, vision, autonomous analysis, observability, and human oversight in a practical infrastructure-inspection workflow.

👩‍💻 Author

Bhoomika Karri

GitHub:
https://github.com/BhoomikaKarri
