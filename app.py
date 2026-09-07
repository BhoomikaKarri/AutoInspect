import re
from pathlib import Path

import streamlit as st
from pypdf import PdfReader

from agents.coordinator import (
    run_inspection,
    build_report_data,
    build_llm_summary,
)
from agents.safety import evaluate_safety


st.set_page_config(
    page_title="AutoInspect",
    page_icon="🔍",
    layout="wide",
)


DATA_DIR = Path(__file__).parent / "data"


def get_bridges():
    return sorted(
        [
            path.name
            for path in DATA_DIR.iterdir()
            if path.is_dir() and (path / "images").exists()
        ]
    )


def get_images(bridge_name):
    image_dir = DATA_DIR / bridge_name / "images"

    if not image_dir.exists():
        return []

    return sorted(image_dir.glob("*.png"))


def get_authoritative_deck_rating(bridge_name):
    pdf_path = (
        DATA_DIR
        / bridge_name
        / f"{bridge_name}.pdf"
    )

    if not pdf_path.exists():
        return None

    try:
        reader = PdfReader(str(pdf_path))

        for page_number, page in enumerate(
            reader.pages,
            start=1,
        ):
            text = page.extract_text() or ""

            normalized = re.sub(
                r"\s+",
                " ",
                text,
            ).strip()

            patterns = [
                (
                    r"B\.C\.01\s+Deck\s+Condition\s+Rating"
                    r".*?"
                    r"\(\s*(\d+)\s*-\s*"
                    r"([A-Z][A-Z ]*?)"
                    r"(?:\s*-\s*|\))"
                ),
                (
                    r"58\s*-\s*Deck\s*"
                    r"\(\s*(\d+)\s*-\s*"
                    r"([A-Z][A-Z ]*?)"
                    r"(?:\s*-\s*|\))"
                ),
            ]

            for pattern in patterns:
                match = re.search(
                    pattern,
                    normalized,
                    re.IGNORECASE,
                )

                if match:
                    return {
                        "score": int(match.group(1)),
                        "condition": match.group(2).strip(),
                        "page": page_number,
                        "source": str(pdf_path),
                    }

    except Exception as e:
        st.error(
            f"Could not read inspection PDF: {e}"
        )

    return None


def get_image_path(
    bridge_name,
    image_name,
):
    return (
        DATA_DIR
        / bridge_name
        / "images"
        / image_name
    )


def build_static_summary(
    bridge_name,
    rating,
    document_findings,
    vision_findings,
):
    if rating:
        rating_text = (
            f"Deck condition is rated "
            f"{rating['score']} - {rating['condition']} "
            f"on page {rating['page']} of the inspection report."
        )
    else:
        rating_text = (
            "The authoritative deck condition rating "
            "could not be verified."
        )

    document_summary = ""

    if document_findings:
        document_summary = (
            f"The report documents findings including "
            f"{document_findings[0].lower()}."
        )

    visual_answers = []

    for item in vision_findings:
        answer = str(item["answer"]).strip()

        if answer:
            visual_answers.append(answer)

    visual_summary = ""

    if visual_answers:
        visual_summary = (
            "The vision model observed: "
            + ", ".join(visual_answers[:5])
            + "."
        )

    return " ".join(
        part
        for part in [
            rating_text,
            document_summary,
            visual_summary,
        ]
        if part
    )


st.title("AutoInspect")

st.subheader(
    "Multi-Agent AI Infrastructure Inspection System"
)

st.write(
    "Document-grounded bridge inspection using RAG, "
    "Vision AI, data analysis, safety checks, and human review."
)


bridges = get_bridges()

if not bridges:
    st.error(
        "No bridge inspection data found."
    )
    st.stop()


st.sidebar.header(
    "Inspection Setup"
)


bridge_name = st.sidebar.selectbox(
    "Bridge",
    bridges,
)


images = get_images(
    bridge_name
)

if not images:
    st.error(
        "No inspection images found for this bridge."
    )
    st.stop()


image_names = [
    image.name
    for image in images
]


selected_image_name = st.sidebar.selectbox(
    "Inspection Image",
    image_names,
)


question = st.sidebar.text_area(
    "Inspection Question",
    value=(
        "What deterioration is present on the bridge deck "
        "and what evidence supports the assessment?"
    ),
)


run_button = st.sidebar.button(
    "Run Inspection",
    type="primary",
)


selected_image = get_image_path(
    bridge_name,
    selected_image_name,
)


st.header("Inspection Image")

st.image(
    str(selected_image),
    use_container_width=True,
)


if run_button:

    with st.spinner(
        "Running Researcher, Vision, Analyst, and Safety agents..."
    ):

        result = run_inspection(
            question=question,
            bridge_name=bridge_name,
            image_path=str(selected_image),
        )

    authoritative_rating = (
        get_authoritative_deck_rating(
            bridge_name
        )
    )

    if authoritative_rating:
        result["safety"] = evaluate_safety(
            authoritative_rating
        )
    else:
        result["safety"] = evaluate_safety(
            None
        )

    report_data = build_report_data(
        result,
        authoritative_rating,
        result["safety"],
    )

    static_summary = build_static_summary(
        bridge_name,
        authoritative_rating,
        report_data["document_findings"],
        report_data["vision_findings"],
    )

    st.session_state["result"] = result
    st.session_state["report_data"] = report_data
    st.session_state["rating"] = authoritative_rating
    st.session_state["static_summary"] = static_summary
    st.session_state["ai_summary"] = None
    st.session_state["review_decision"] = "Select decision"


if "result" in st.session_state:

    result = st.session_state["result"]
    report_data = st.session_state["report_data"]
    rating = st.session_state["rating"]


    st.divider()

    st.header(
        "Inspection Assessment"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        if rating:

            st.metric(
                "Deck Rating",
                f"{rating['score']} - {rating['condition']}",
            )

            st.caption(
                f"Authoritative PDF page: {rating['page']}"
            )

        else:

            st.metric(
                "Deck Rating",
                "Not Found",
            )


    with col2:

        if result["analysis"]:

            st.metric(
                "Average Rating",
                result["analysis"]["average_rating"],
            )

        else:

            st.metric(
                "Average Rating",
                "N/A",
            )


    with col3:

        st.metric(
            "Risk Level",
            result["safety"]["risk_level"],
        )


    st.header(
        "Document Findings"
    )


    if report_data["document_findings"]:

        for finding in report_data[
            "document_findings"
        ]:

            st.write(
                f"• {finding}"
            )

    else:

        st.write(
            "No document findings extracted."
        )


    st.header(
        "Visual Findings"
    )


    if report_data["vision_findings"]:

        for item in report_data[
            "vision_findings"
        ]:

            st.write(
                f"**{item['question']}** → "
                f"{item['answer']}"
            )

    else:

        st.write(
            "No visual findings available."
        )


    st.header(
        "Analyst Summary"
    )


    if result["analysis"]:

        analysis = result["analysis"]

        st.write(
            f"Average rating: "
            f"{analysis['average_rating']}"
        )

        st.write(
            f"Lowest rating: "
            f"{analysis['lowest_rating']}"
        )

        st.write(
            f"Highest rating: "
            f"{analysis['highest_rating']}"
        )

        st.write(
            f"Rated components: "
            f"{analysis['rating_count']}"
        )

    else:

        st.write(
            "No analyst data available."
        )


    st.header(
        "Coordinator Summary"
    )


    st.write(
        st.session_state["static_summary"]
    )


    if st.button(
        "Generate AI Coordinator Summary"
    ):

        with st.spinner(
            "Running local Qwen coordinator..."
        ):

            try:

                st.session_state["ai_summary"] = (
                    build_llm_summary(
                        report_data
                    )
                )

            except Exception as e:

                st.session_state["ai_summary"] = (
                    "Local AI summary could not be generated."
                )

                st.error(
                    f"{type(e).__name__}: {e}"
                )


    if st.session_state["ai_summary"]:

        st.subheader(
            "AI Coordinator Summary"
        )

        st.write(
            st.session_state["ai_summary"]
        )


    st.divider()

    st.header(
        "Human-in-the-Loop Safety Gate"
    )


    safety = result["safety"]


    if safety["risk_level"] == "HIGH":

        st.error(
            "HIGH RISK — Human review required"
        )

    elif safety["risk_level"] == "MODERATE":

        st.warning(
            "MODERATE RISK — Human verification required"
        )

    elif safety["risk_level"] == "UNKNOWN":

        st.warning(
            "⚠️ RISK UNKNOWN — Condition rating could not "
            "be verified. Human review required."
        )

    elif safety["risk_level"] == "LOW":

        st.success(
            "LOW RISK"
        )

    else:

        st.error(
            "UNRECOGNIZED RISK STATE — Human review required."
        )


    st.write(
        safety["message"]
    )


    if safety["human_review_required"]:

        st.subheader(
            "Human Review"
        )


        decision_options = [
            "Select decision",
            "Approve",
            "Reject",
        ]


        current_decision = st.session_state.get(
            "review_decision",
            "Select decision",
        )


        decision = st.radio(
            "Inspection decision",
            decision_options,
            index=decision_options.index(
                current_decision
            ),
            horizontal=True,
        )


        st.session_state[
            "review_decision"
        ] = decision


        if decision == "Approve":

            st.success(
                "Inspection result approved by human reviewer."
            )

        elif decision == "Reject":

            st.error(
                "Inspection result rejected by human reviewer."
            )

        else:

            st.info(
                "Human decision required before this "
                "result can be considered approved."
            )


    else:

        st.success(
            "Human review was not required."
        )


    st.divider()


    st.caption(
        "Automated visual observations are assistive only "
        "and must be verified by a qualified bridge inspector "
        "before maintenance, structural, or safety decisions."
    )