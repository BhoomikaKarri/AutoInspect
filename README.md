(
echo # 🌉 AutoInspect
echo.
echo ### Multi-Agent AI Infrastructure Inspection System
echo.
echo AutoInspect is a **multi-agent AI system for intelligent bridge infrastructure inspection** that combines document-grounded reasoning, vision-language analysis, autonomous data analysis, observability, and human-in-the-loop safety.
echo.
echo The system retrieves evidence from bridge inspection reports using **Retrieval-Augmented Generation ^(RAG^)**, analyzes inspection imagery using a **Vision-Language Model**, performs structured inspection-data analysis, evaluates risk, and produces an evidence-grounded inspection result.
echo.
echo ---
echo.
echo ## 🚀 Project Overview
echo.
echo Infrastructure inspection involves multiple forms of evidence:
echo.
echo ```text
echo Inspection Reports
echo         +
echo Visual Inspection Images
echo         +
echo Structured Condition Ratings
echo         +
echo AI-Based Analysis
echo         +
echo Safety Controls
echo         ↓
echo Evidence-Grounded Inspection Support
echo ```
echo.
echo AutoInspect brings these capabilities together through a modular multi-agent architecture.
echo.
echo ---
echo.
echo ## 🧠 System Architecture
echo.
echo ```text
echo                          ┌──────────────────────┐
echo                          │        USER          │
echo                          │ Bridge + Question    │
echo                          │ + Inspection Image   │
echo                          └──────────┬───────────┘
echo                                     │
echo                                     ▼
echo                          ┌──────────────────────┐
echo                          │    COORDINATOR       │
echo                          │ Agent Orchestration  │
echo                          └──────────┬───────────┘
echo                                     │
echo                   ┌─────────────────┼─────────────────┐
echo                   │                 │                 │
echo                   ▼                 ▼                 ▼
echo         ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
echo         │ Research Agent │ │  Vision Agent  │ │ Analyst Agent  │
echo         │                │ │                │ │                │
echo         │ RAG Retrieval  │ │ BLIP VQA       │ │ QA + Statistics│
echo         └───────┬────────┘ └───────┬────────┘ └───────┬────────┘
echo                 │                  │                  │
echo                 ▼                  ▼                  ▼
echo         ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
echo         │ Inspection    │  │ Image Evidence│  │ Condition     │
echo         │ Report        │  │               │  │ Analysis      │
echo         └───────┬───────┘  └───────┬───────┘  └───────┬───────┘
echo                 │                  │                  │
echo                 └──────────────────┼──────────────────┘
echo                                    ▼
echo                          ┌──────────────────────┐
echo                          │    SAFETY LAYER      │
echo                          │ Risk Evaluation      │
echo                          └──────────┬───────────┘
echo                                     │
echo                                     ▼
echo                          ┌──────────────────────┐
echo                          │   HUMAN REVIEW       │
echo                          │ Approval / Rejection │
echo                          └──────────┬───────────┘
echo                                     │
echo                                     ▼
echo                          ┌──────────────────────┐
echo                          │ INSPECTION RESULT    │
echo                          │ Evidence + Findings  │
echo                          │ + Risk Status        │
echo                          └──────────────────────┘
echo ```
echo.
echo ---
echo.
echo ## ✨ Key Features
echo.
echo ### 🤖 Multi-Agent Workflow
echo.
echo ^| Component ^| Responsibility ^|
echo ^|---^|---^|
echo ^| Coordinator ^| Orchestrates the inspection workflow ^|
echo ^| Research Agent ^| Retrieves evidence from inspection reports ^|
echo ^| Vision Agent ^| Analyzes inspection imagery ^|
echo ^| Analyst Agent ^| Performs structured condition-rating analysis ^|
echo ^| Safety Agent ^| Evaluates inspection risk ^|
echo ^| Human Review ^| Handles high-risk or uncertain results ^|
echo.
echo ---
echo.
echo ## 📚 Retrieval-Augmented Generation
echo.
echo The Research Agent uses a document-grounded retrieval pipeline:
echo.
echo ```text
echo Bridge Inspection PDFs
echo           │
echo           ▼
echo     PDF Extraction
echo           │
echo           ▼
echo      Text Chunking
echo           │
echo           ▼
echo    Sentence Embeddings
echo           │
echo           ▼
echo        ChromaDB
echo           │
echo           ▼
echo    Semantic Retrieval
echo           │
echo           ▼
echo  Bridge-Specific Evidence
echo ```
echo.
echo The retrieval workflow is **bridge-aware**, helping prevent evidence from unrelated inspection reports from being mixed together.
echo.
echo ---
echo.
echo ## 👁️ Vision-Language Analysis
echo.
echo The Vision Agent uses:
echo.
echo **Salesforce BLIP VQA**
echo.
echo ```text
echo Salesforce/blip-vqa-base
echo ```
echo.
echo The model supports visual inspection observations such as:
echo.
echo - Concrete cracking
echo - Rust / corrosion
echo - Spalling
echo - Water staining
echo - Exposed metal / rebar
echo - Concrete deterioration
echo - Visible defects
echo.
echo Visual model output is treated as **supporting evidence**, rather than the sole source of authoritative condition ratings.
echo.
echo ---
echo.
echo ## 📊 Autonomous Data Analysis
echo.
echo The Analyst Agent processes structured inspection QA data and calculates condition-rating statistics.
echo.
echo Example:
echo.
echo ```text
echo Bridge: PUTNEY-00001
echo.
echo Condition Ratings:
echo [4, 4, 5, 4, 4, 4, 7]
echo.
echo Average Rating: 4.57
echo Minimum Rating: 4
echo Maximum Rating: 7
echo Observations: 7
echo ```
echo.
echo ---
echo.
echo ## 🛡️ Safety Layer
echo.
echo AutoInspect contains a rule-based safety gate that determines whether human verification is required.
echo.
echo ^| Condition Rating ^| Risk Level ^| Human Review ^|
echo ^|---^|---^|---^|
echo ^| ≤ 4 ^| HIGH ^| Required ^|
echo ^| 5–6 ^| MODERATE ^| Required ^|
echo ^| ≥ 7 ^| LOW ^| Not required by default ^|
echo ^| Unknown ^| UNKNOWN ^| Required ^|
echo.
echo ---
echo.
echo ## 👤 Human-in-the-Loop
echo.
echo Higher-risk or uncertain results are explicitly routed through a human approval gate.
echo.
echo Possible outcomes:
echo.
echo ```text
echo AUTO_APPROVED
echo HUMAN_APPROVED
echo HUMAN_REJECTED
echo ```
echo.
echo ---
echo.
echo ## 🔍 LangSmith Observability
echo.
echo AutoInspect integrates **LangSmith** for workflow observability.
echo.
echo The workflow can expose:
echo.
echo - Bridge input
echo - User question
echo - Retrieval operations
echo - Vision analysis
echo - Agent outputs
echo - Safety evaluation
echo - Human-review result
echo - Final inspection output
echo.
echo ---
echo.
echo ## 🧩 Technology Stack
echo.
echo ### AI / Machine Learning
echo.
echo - Python
echo - Hugging Face Transformers
echo - BLIP VQA
echo - Sentence Transformers
echo - Qwen2.5-1.5B-Instruct
echo.
echo ### Agent and Workflow
echo.
echo - LangGraph
echo - LangChain
echo.
echo ### Retrieval
echo.
echo - ChromaDB
echo - Sentence embeddings
echo - PDF text extraction
echo - RAG
echo.
echo ### Application
echo.
echo - Streamlit
echo.
echo ### Observability
echo.
echo - LangSmith
echo.
echo ### Dataset
echo.
echo - BridgeEQA
echo.
echo ---
echo.
echo ## 📁 Project Structure
echo.
echo ```text
echo AutoInspect/
echo │
echo ├── agents/
echo │   ├── analyst.py
echo │   ├── coordinator.py
echo │   ├── human_review.py
echo │   ├── local_llm.py
echo │   ├── researcher.py
echo │   ├── safety.py
echo │   └── vision.py
echo │
echo ├── data/
echo │   ├── BridgeInspRpt-DOVER-00028/
echo │   ├── BridgeInspRpt-GROTON-00036/
echo │   ├── BridgeInspRpt-MIDDLEBURY-0011A/
echo │   ├── BridgeInspRpt-PUTNEY-00001/
echo │   └── BridgeInspRpt-RICHFORD-00003/
echo │
echo ├── rag/
echo │   ├── build_rag.py
echo │   ├── create_vector_db.py
echo │   ├── test_pdf.py
echo │   └── test_retrieval.py
echo │
echo ├── tools/
echo │
echo ├── app.py
echo ├── requirements.txt
echo ├── README.md
echo └── .gitignore
echo ```
echo.
echo ---
echo.
echo ## ⚙️ Local Setup
echo.
echo ### 1. Clone the repository
echo.
echo ```bash
echo git clone https://github.com/BhoomikaKarri/AutoInspect.git
echo cd AutoInspect
echo ```
echo.
echo ### 2. Create a virtual environment
echo.
echo Windows:
echo.
echo ```bash
echo python -m venv .venv
echo .venv\Scripts\activate
echo ```
echo.
echo ### 3. Install dependencies
echo.
echo ```bash
echo pip install -r requirements.txt
echo ```
echo.
echo ---
echo.
echo ## 🗄️ Build the Vector Database
echo.
echo ```bash
echo python rag/create_vector_db.py
echo ```
echo.
echo ---
echo.
echo ## ▶️ Run the Application
echo.
echo ```bash
echo streamlit run app.py
echo ```
echo.
echo ---
echo.
echo ## 🔎 Example Inspection Workflow
echo.
echo ### Input
echo.
echo ```text
echo Bridge:
echo BridgeInspRpt-PUTNEY-00001
echo.
echo Question:
echo What is the condition of the bridge deck?
echo.
echo Image:
echo Selected inspection image
echo ```
echo.
echo ### Processing
echo.
echo ```text
echo 1. Identify selected bridge
echo 2. Retrieve relevant inspection evidence
echo 3. Analyze inspection image
echo 4. Analyze structured inspection data
echo 5. Evaluate safety risk
echo 6. Request human review when required
echo 7. Produce final inspection result
echo ```
echo.
echo ---
echo.
echo ## 🏗️ Design Principles
echo.
echo ### Evidence First
echo Inspection conclusions should be grounded in available inspection evidence.
echo.
echo ### Specialized Agents
echo Each major capability has a dedicated responsibility.
echo.
echo ### Bridge-Aware Retrieval
echo Retrieved evidence is filtered to the selected bridge.
echo.
echo ### Human Oversight
echo Higher-risk or uncertain conclusions require explicit human verification.
echo.
echo ### Observable Execution
echo LangSmith provides visibility into the multi-agent workflow.
echo.
echo ---
echo.
echo ## 📦 Dataset
echo.
echo AutoInspect was developed using a selective subset of the **BridgeEQA** dataset.
echo.
echo Official dataset:
echo.
echo https://huggingface.co/datasets/hoskerelab/bridge-eqa
echo.
echo ---
echo.
echo ## 🎯 Why This Project?
echo.
echo AutoInspect demonstrates how **agentic AI can combine retrieval, vision, structured analysis, observability, and safety controls** for a real-world infrastructure inspection scenario.
echo.
echo The architecture is designed around modular AI components rather than relying on a single general-purpose model.
echo.
echo ---
echo.
echo ## ⚠️ Safety Disclaimer
echo.
echo AutoInspect is a **research and portfolio prototype**.
echo.
echo It is not a replacement for:
echo.
echo - Certified structural inspections
echo - Professional engineering judgment
echo - Regulatory inspection procedures
echo - Real-world safety certification
echo.
echo AI-generated observations are intended as **decision-support evidence** and should be verified by qualified professionals before real-world maintenance, structural, or safety decisions.
echo.
echo ---
echo.
echo ## 🚀 Future Improvements
echo.
echo - Persistent inspection memory
echo - Historical bridge-condition comparison
echo - External infrastructure APIs
echo - Advanced vision models
echo - Automated inspection report generation
echo - Real-time drone inspection pipelines
echo - Larger evaluation benchmarks
echo - Cloud-native multi-agent deployment
echo.
echo ---
echo.
echo ## 👩‍💻 Author
echo.
echo **Bhoomika Karri**
echo.
echo GitHub:
echo.
echo https://github.com/BhoomikaKarri
echo.
echo ---
echo.
echo ## 📄 License
echo.
echo This project is intended for educational, research, and portfolio purposes.
echo.
echo The BridgeEQA dataset is governed by its own license and terms. Refer to the official dataset repository for applicable dataset licensing information.
) > README.md