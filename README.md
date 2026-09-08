# 🌉 AutoInspect

### Multi-Agent AI Infrastructure Inspection System

AutoInspect is a **multi-agent AI system for intelligent bridge infrastructure inspection** that combines document-grounded reasoning, vision-language analysis, autonomous data analysis, observability, and human-in-the-loop safety.

The system retrieves evidence from bridge inspection reports using **Retrieval-Augmented Generation (RAG)**, analyzes inspection imagery using a **Vision-Language Model**, performs structured inspection-data analysis, evaluates risk, and produces an evidence-grounded inspection result.

---

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

---

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
```

## 📚 RAG Pipeline

```text
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
```
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

Visual observations are treated as assistive evidence and are not used as the sole authority for inspection ratings.

📊 Data Analysis
The Analyst Agent processes structured inspection QA data and calculates condition-rating statistics.

Example:
```text
Bridge: PUTNEY-00001

Condition Ratings:
[4, 4, 5, 4, 4, 4, 7]

Average: 4.57
Minimum: 4
Maximum: 7
```

🛡️ Safety & Human Review
AutoInspect includes a rule-based safety gate.
```text
| Condition Rating | Risk Level | Human Review            |
| ---------------- | ---------- | ----------------------- |
| ≤ 4              | HIGH       | Required                |
| 5–6              | MODERATE   | Required                |
| ≥ 7              | LOW        | Not required by default |
| Unknown          | UNKNOWN    | Required                |
```
Higher-risk or unverifiable results are routed through an explicit human approval/rejection gate.

Possible outcomes:
```text
AUTO_APPROVED
HUMAN_APPROVED
HUMAN_REJECTED
```
🔍 LangSmith Observability
LangSmith provides observability for the inspection workflow, including:
User inputs
Retrieval activity
Vision analysis
Agent outputs
Safety evaluation
Human review decisions
Final inspection results

This makes the multi agent workflow easier to inspect, debug, and evaluate.

🧩 Tech Stack
```text
AI / Machine Learning
Python
Hugging Face Transformers
BLIP VQA
Sentence Transformers
Qwen2.5-1.5B-Instruct
Agent & Workflow
LangGraph
LangChain
Retrieval
ChromaDB
Sentence Embeddings
PDF Text Extraction
RAG
Application
Streamlit
Observability
LangSmith
Dataset
BridgeEQA
```

📁 Project Structure
```text
AutoInspect/
│
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
│   ├── build_rag.py
│   ├── create_vector_db.py
│   ├── test_pdf.py
│   └── test_retrieval.py
│
├── tools/
│
├── app.py
├── hf_app.py
├── requirements.txt
├── README.md
└── .gitignore
```

⚙️ Run Locally
```text
git clone https://github.com/BhoomikaKarri/AutoInspect.git
cd AutoInspect

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
python rag/create_vector_db.py
streamlit run app.py
```
🔎 Example Inspection Workflow
Input
Bridge:
BridgeInspRpt-PUTNEY-00001

Question:
What is the condition of the bridge deck?

Image:
Selected inspection image

Processing
1. Identify selected bridge
2. Retrieve relevant inspection evidence
3. Analyze inspection image
4. Analyze structured inspection data
5. Evaluate safety risk
6. Request human review when required
7. Produce final inspection result

🏗️ Design Principles

Evidence First
Inspection conclusions should be grounded in available inspection evidence.

Specialized Agents
Each major capability has a dedicated responsibility.

Bridge-Aware Retrieval
Retrieved evidence is filtered to the selected bridge.

Human Oversight
Higher risk or uncertain conclusions require explicit human verification.

Observable Execution
LangSmith provides visibility into the multi-agent workflow.

📦 Dataset
This project uses a selective subset of the BridgeEQA dataset.

Official dataset:
https://huggingface.co/datasets/hoskerelab/bridge-eqa

🎯 Project Goal
AutoInspect demonstrates how agentic AI can combine retrieval, vision, autonomous analysis, observability, and human oversight in a practical infrastructure-inspection workflow.

⚠️ Safety Disclaimer
AutoInspect is a research and portfolio prototype.
It is not a replacement for:
Certified structural inspection
Professional engineering judgment
Regulatory procedures
Real world safety certification
AI generated observations should be verified by qualified professionals before real-world maintenance, structural, or safety decisions.

👩‍💻 Author
Bhoomika Karri
GitHub:
https://github.com/BhoomikaKarri
