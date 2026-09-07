def evaluate_safety(condition_rating):
    if condition_rating is None:
        return {
            "risk_level": "UNKNOWN",
            "human_review_required": True,
            "message": "Condition rating could not be verified. Human review is required.",
        }

    score = condition_rating.get("score")

    if score <= 4:
        return {
            "risk_level": "HIGH",
            "human_review_required": True,
            "message": (
                "High-risk condition detected. "
                "Qualified human inspection is required before any "
                "maintenance, structural, or safety decision."
            ),
        }

    if score <= 6:
        return {
            "risk_level": "MODERATE",
            "human_review_required": True,
            "message": (
                "Moderate condition detected. "
                "Human verification is required before actionable decisions."
            ),
        }

    return {
        "risk_level": "LOW",
        "human_review_required": False,
        "message": "No high-risk condition detected by the configured rule.",
    }


if __name__ == "__main__":
    tests = [4, 5, 6, 7]

    for score in tests:
        rating = {"score": score}
        print(f"Rating {score}:")
        print(evaluate_safety(rating))
        print()