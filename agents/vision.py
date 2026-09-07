from pathlib import Path

from PIL import Image
from transformers import BlipProcessor, BlipForQuestionAnswering


MODEL_NAME = "Salesforce/blip-vqa-base"

processor = BlipProcessor.from_pretrained(MODEL_NAME)
model = BlipForQuestionAnswering.from_pretrained(MODEL_NAME)


QUESTIONS = [
    "What type of bridge component is shown?",
    "Is there visible cracking?",
    "Is there visible rust or corrosion?",
    "Is there visible spalling or concrete loss?",
    "Is there visible water staining or leakage?",
    "Is there exposed steel or rebar?",
    "What is the most significant visible defect?",
]


def ask_vlm(image, question: str) -> str:
    inputs = processor(
        images=image,
        text=question,
        return_tensors="pt",
    )

    output = model.generate(
        **inputs,
        max_new_tokens=30,
    )

    return processor.decode(
        output[0],
        skip_special_tokens=True,
    )


def inspect_image(image_path: str) -> dict:
    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = Image.open(image_path).convert("RGB")

    findings = {}

    for question in QUESTIONS:
        findings[question] = ask_vlm(image, question)

    return {
        "image": str(image_path),
        "findings": findings,
    }


if __name__ == "__main__":
    image_path = (
        r"data\BridgeInspRpt-PUTNEY-00001\images"
        r"\350ce9d017b7a305f4590de2dd9728b8.png"
    )

    result = inspect_image(image_path)

    print("\n==============================")
    print("VISION INSPECTION AGENT")
    print("==============================")

    print(f"\nImage: {result['image']}")

    for question, answer in result["findings"].items():
        print(f"\nQ: {question}")
        print(f"A: {answer}")