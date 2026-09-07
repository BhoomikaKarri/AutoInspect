from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re

try:
    from langsmith import traceable
except ImportError:
    def traceable(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

try:
    from .researcher import research
    from .vision import inspect_image
    from .analyst import get_bridge_analysis
    from .safety import evaluate_safety
    from .human_review import request_human_review
except ImportError:
    from researcher import research
    from vision import inspect_image
    from analyst import get_bridge_analysis
    from safety import evaluate_safety
    from human_review import request_human_review


MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

print("Loading local Coordinator LLM...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
model.eval()


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


def build_report_data(result, rating, safety_result):
    document_findings = extract_document_findings(
        result["research"]
    )

    vision_findings = []

    if result["vision"]:
        for question, answer in result["vision"]["findings"].items():
            vision_findings.append(
                {
                    "question": question,
                    "answer": answer,
                }
            )

    return {
        "bridge": result["bridge"],
        "rating": rating,
        "document_findings": document_findings,
        "vision_findings": vision_findings,
        "analysis": result["analysis"],
        "safety": safety_result,
    }


@traceable(
    name="AutoInspect Coordinator Summary",
    run_type="chain",
)
def build_llm_summary(report_data):
    rating = report_data["rating"]

    if rating:
        rating_text = (
            f"{rating['score']} "
            f"({rating['condition']})"
        )
    else:
        rating_text = "Not available"

    document_text = "\n".join(
        f"- {item}"
        for item in report_data["document_findings"][:5]
    )

    if not document_text:
        document_text = "- No document findings extracted."

    vision_text = "\n".join(
        f"- {item['question']} -> {item['answer']}"
        for item in report_data["vision_findings"][:7]
    )

    if not vision_text:
        vision_text = "- No visual findings available."

    analysis = report_data["analysis"]

    if analysis:
        analyst_text = (
            f"Average rating: {analysis['average_rating']}\n"
            f"Lowest rating: {analysis['lowest_rating']}\n"
            f"Highest rating: {analysis['highest_rating']}\n"
            f"Rated components: {analysis['rating_count']}"
        )
    else:
        analyst_text = "No analyst data available."

    prompt = f"""
Summarize this bridge inspection in 3 sentences maximum.

Bridge:
{report_data['bridge']}

Authoritative deck rating:
{rating_text}

Document findings:
{document_text}

Visual findings:
{vision_text}

Analyst:
{analyst_text}

Safety:
{report_data['safety']['risk_level']}

Rules:
Use only the supplied facts.
Do not invent measurements.
Do not change the rating.
Do not make maintenance recommendations.
"""

    messages = [
        {
            "role": "system",
            "content": (
                "You are a cautious infrastructure inspection "
                "summarization assistant. Use only supplied evidence."
            ),
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=2200,
    )

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=70,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    generated_tokens = outputs[0][
        inputs["input_ids"].shape[-1]:
    ]

    return tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True,
    ).strip()


@traceable(
    name="AutoInspect Full Inspection",
    run_type="chain",
)
def run_inspection(
    question: str,
    bridge_name: str | None = None,
    image_path: str | None = None,
):
    print("\n==============================")
    print("COORDINATOR AGENT")
    print("==============================")

    result = {
        "question": question,
        "bridge": bridge_name,
        "research": None,
        "vision": None,
        "analysis": None,
        "safety": None,
        "human_review": None,
    }

    print("\n[1/5] Calling Researcher Agent...")

    result["research"] = research(
        question,
        bridge_name,
    )

    print("[2/5] Calling Vision Agent...")

    if image_path:
        result["vision"] = inspect_image(
            image_path
        )
    else:
        print("Vision Agent skipped.")

    print("[3/5] Calling Analyst Agent...")

    if bridge_name:
        result["analysis"] = get_bridge_analysis(
            bridge_name
        )
    else:
        print("Analyst Agent skipped.")

    print("[4/5] Calling Safety Agent...")

    rating = extract_condition_rating(
        result["research"]
    )

    result["safety"] = evaluate_safety(
        rating
    )

    print("[5/5] Checking Human Review Gate...")

    result["human_review"] = request_human_review(
        result["safety"]
    )

    return result


def print_report(
    result,
    report_data,
    summary,
):
    rating = report_data["rating"]
    analysis = report_data["analysis"]
    safety = report_data["safety"]
    human_review = result["human_review"]

    print("\n")
    print("=" * 60)
    print("AUTOINSPECT REPORT")
    print("=" * 60)

    print(f"\nBridge: {report_data['bridge']}")

    print("\nCOMPONENT ASSESSMENT")

    if rating:
        print(
            f"Deck Condition Rating: "
            f"{rating['score']} - {rating['condition']}"
        )

        print(
            f"Source Page: {rating['page']}"
        )
    else:
        print("Deck condition rating: Not found")

    print("\nDOCUMENT FINDINGS")

    for finding in report_data["document_findings"]:
        print(f"- {finding}")

    print("\nVISUAL FINDINGS")

    for item in report_data["vision_findings"]:
        print(
            f"- {item['question']} -> "
            f"{item['answer']}"
        )

    print("\nANALYST SUMMARY")

    if analysis:
        print(
            f"Average rating: "
            f"{analysis['average_rating']}"
        )

        print(
            f"Lowest rating: "
            f"{analysis['lowest_rating']}"
        )

        print(
            f"Highest rating: "
            f"{analysis['highest_rating']}"
        )

        print(
            f"Rated components: "
            f"{analysis['rating_count']}"
        )

    print("\nCOORDINATOR SUMMARY")
    print(summary)

    print("\nSAFETY GATE")

    print(
        f"Risk level: "
        f"{safety['risk_level']}"
    )

    print(
        f"Human review required: "
        f"{safety['human_review_required']}"
    )

    print(
        f"Safety message: "
        f"{safety['message']}"
    )

    print("\nHUMAN REVIEW")

    print(
        f"Status: "
        f"{human_review['status']}"
    )

    print(
        f"Approved: "
        f"{human_review['approved']}"
    )

    print(
        f"Message: "
        f"{human_review['message']}"
    )

    print("\nFINAL DECISION")

    if human_review["approved"]:
        print(
            "Inspection result approved by human reviewer."
        )
    else:
        print(
            "Inspection result has NOT been approved."
        )

    print("\nSAFETY NOTICE")

    print(
        "Automated visual observations are assistive only "
        "and must be verified by a qualified bridge inspector "
        "before maintenance, structural, or safety decisions."
    )

    print("=" * 60)


if __name__ == "__main__":

    bridge = "BridgeInspRpt-PUTNEY-00001"

    image = (
        r"data\BridgeInspRpt-PUTNEY-00001\images"
        r"\350ce9d017b7a305f4590de2dd9728b8.png"
    )

    question = (
        "What deterioration is present on the bridge deck "
        "and what evidence supports the assessment?"
    )

    result = run_inspection(
        question=question,
        bridge_name=bridge,
        image_path=image,
    )

    rating = extract_condition_rating(
        result["research"]
    )

    report_data = build_report_data(
        result,
        rating,
        result["safety"],
    )

    print("\nGenerating coordinator summary...")

    try:
        summary = build_llm_summary(
            report_data
        )
    except Exception as e:
        summary = (
            "LLM summary unavailable. "
            "Structured inspection evidence remains available."
        )

        print(
            f"\nLLM summary error: "
            f"{type(e).__name__}: {e}"
        )

    print_report(
        result,
        report_data,
        summary,
    )