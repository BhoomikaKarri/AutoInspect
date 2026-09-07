---
title: AutoInspect
emoji: 🌉
colorFrom: blue
colorTo: purple
sdk: gradio
app_file: hf_app.py
python_version: 3.12
---

# AutoInspect

Multi-Agent AI Infrastructure Inspection System.

AutoInspect combines bridge inspection document retrieval, vision analysis, Python-based data analysis, safety checks, and human oversight into one inspection workflow.

## Components

- RAG over bridge inspection reports
- Chroma vector database
- BLIP VQA for inspection imagery
- Python condition-rating analysis
- Rule-based safety gate
- Human-in-the-loop review
- LangSmith observability

## Safety

Visual model observations are assistive only. Authoritative inspection ratings come from the inspection documentation, and uncertain or higher-risk results require human verification.