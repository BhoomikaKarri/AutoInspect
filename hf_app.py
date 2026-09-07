import re
from pathlib import Path

import gradio as gr
import spaces
from pypdf import PdfReader

from agents.researcher import research
from agents.vision import inspect_image
from agents.analyst import get_bridge_analysis
from agents.safety import evaluate_safety


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def get_bridges():
    return sorted(
        path.name
        for path in DATA_DIR.iterdir()
        if path.is_dir()
    )


def get_images(bridge_name):
    if not bridge_name:
        return []

    image_dir = DATA_DIR / bridge_name / "images"

    if not image_dir.exists():
        return []

    return sorted(
        str(path)
        for path in image_dir.iterdir()
        if path.suffix.lower() in {
            ".png",
            ".jpg",
            ".jpeg",
        }
    )


def extract_condition_rating(research_results):
    if not research_results:
        return None

    for item in research_results:
        text = item.get("content", "")

        match = re.search(
            r"B\.C\.01 Deck Condition Rating\s*"
            r"\(\s*(\d+)\s*-\s*([A-Z ]+)",
            text,
            re.IGNORECASE,
        )

        if match:
            return {
                "score": int(match.group(1)),
                "condition": match.group(2).strip(),
                "page": item.get("page"),
                "bridge": item.get("bridge"),
            }

    return None


def find_rating(research_results):
    rating = extract_condition_rating(research_results)

    if rating:
        return rating

    if not research_results:
        return None

    bridge_name = research_results[0].get("bridge")

    if not bridge_name:
        return None

    pdf_path = (
        DATA_DIR
        / bridge_name
        / f"{bridge_name}.pdf"
    )

    if not pdf_path.exists():
        return None

    try:
        reader = PdfReader(str(pdf_path))

        pattern = (
            r"58\s*-\s*Deck\s*"
            r"\(\s*(\d+)\s*-\s*([A-Z ]+)"
        )

        for page_number, page in enumerate(
            reader.pages,
            start=1,
        ):
            text = page.extract_text() or ""

            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:
                return {
                    "score": int(match.group(1)),
                    "condition": match.group(2).strip(),
                    "page": page_number,
                    "bridge": bridge_name,
                }

    except Exception:
        return None

    return None


def extract_document_findings(research_results):
    if not research_results:
        return []

    findings = []

    patterns = [
        r"widespread[^.]*",
        r"isolated[^.]*",
        r"moderate[^.]*",
        r"minor[^.]*",
        r"spalling[^.]*",
        r"cracking[^.]*",
        r"rust staining[^.]*",
        r"efflorescence[^.]*",
        r"exposed rebar[^.]*",
        r"delamination[^.]*",
        r"settlement[^.]*",
    ]

    for item in research_results:
        text = item.get("content", "")

        for pattern in patterns:
            matches = re.findall(
                pattern,
                text,
                re.IGNORECASE,
            )

            for match in matches:
                cleaned = match.strip()

                if cleaned and cleaned not in findings:
                    findings.append(cleaned)

    return findings[:8]


@spaces.GPU(duration=120)
def run_autoinspect(
    bridge_name,
    image_path,
    question,
):
    if not bridge_name:
        return (
            "Please select a bridge.",
            "",
            "",
            "",
            "",
        )

    if not question:
        question = (
            "What deterioration is present on "
            "the bridge deck and what evidence "
            "supports the assessment?"
        )

    research_results = research(
        question,
        bridge_name,
    )

    vision_result = None

    if image_path:
        vision_result = inspect_image(
            image_path
        )

    analysis = get_bridge_analysis(
        bridge_name
    )

    rating = find_rating(
        research_results
    )

    safety = evaluate_safety(
        rating
    )

    document_findings = extract_document_findings(
        research_results
    )

    if vision_result:
        vision_findings = vision_result.get(
            "findings",
            {},
        )
    else:
        vision_findings = {}

    if rating:
        assessment = (
            f"Deck Rating: "
            f"{rating['score']} - "
            f"{rating['condition']}\n"
            f"Authoritative PDF Page: "
            f"{rating['page']}\n"
            f"Average Rating: "
            f"{analysis['average_rating']}\n"
            f"Risk Level: "
            f"{safety['risk_level']}\n\n"
            f"{safety['message']}"
        )
    else:
        assessment = (
            "Deck Rating: Not verified\n"
            f"Average Rating: "
            f"{analysis['average_rating']}\n"
            f"Risk Level: "
            f"{safety['risk_level']}\n\n"
            f"{safety['message']}"
        )

    document_text = "\n".join(
        f"- {item}"
        for item in document_findings
    )

    if not document_text:
        document_text = "No document findings extracted."

    visual_text = "\n".join(
        f"- {question}: {answer}"
        for question, answer in vision_findings.items()
    )

    if not visual_text:
        visual_text = "No visual findings available."

    analyst_text = (
        f"Average rating: "
        f"{analysis['average_rating']}\n"
        f"Lowest rating: "
        f"{analysis['lowest_rating']}\n"
        f"Highest rating: "
        f"{analysis['highest_rating']}\n"
        f"Rated components: "
        f"{analysis['rating_count']}"
    )

    safety_text = (
        f"Risk: {safety['risk_level']}\n"
        f"Human review required: "
        f"{safety['human_review_required']}\n"
        f"{safety['message']}"
    )

    return (
        assessment,
        document_text,
        visual_text,
        analyst_text,
        safety_text,
    )


def update_images(bridge_name):
    images = get_images(bridge_name)

    return gr.Dropdown(
        choices=images,
        value=images[0] if images else None,
    )


bridges = get_bridges()

with gr.Blocks(
    title="AutoInspect"
) as demo:

    gr.Markdown(
        """
# AutoInspect

### Multi-Agent AI Infrastructure Inspection System

Document-grounded bridge inspection using RAG,
Vision AI, data analysis, safety checks,
and human oversight.
"""
    )

    with gr.Row():

        with gr.Column():

            bridge = gr.Dropdown(
                choices=bridges,
                label="Bridge",
                value=bridges[0]
                if bridges
                else None,
            )

            image = gr.Dropdown(
                choices=get_images(
                    bridges[0]
                )
                if bridges
                else [],
                label="Inspection Image",
            )

            question = gr.Textbox(
                label="Inspection Question",
                value=(
                    "What deterioration is present "
                    "on the bridge deck and what evidence "
                    "supports the assessment?"
                ),
                lines=3,
            )

            run_button = gr.Button(
                "Run Inspection",
                variant="primary",
            )

        with gr.Column():

            assessment = gr.Textbox(
                label="Inspection Assessment",
                lines=8,
            )

            document = gr.Textbox(
                label="Document Findings",
                lines=10,
            )

            visual = gr.Textbox(
                label="Visual Findings",
                lines=10,
            )

            analyst = gr.Textbox(
                label="Analyst Summary",
                lines=6,
            )

            safety = gr.Textbox(
                label="Safety Gate",
                lines=6,
            )

    bridge.change(
        fn=update_images,
        inputs=bridge,
        outputs=image,
    )

    run_button.click(
        fn=run_autoinspect,
        inputs=[
            bridge,
            image,
            question,
        ],
        outputs=[
            assessment,
            document,
            visual,
            analyst,
            safety,
        ],
    )


demo.launch()