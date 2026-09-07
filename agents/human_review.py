def request_human_review(safety_result):
    if not safety_result["human_review_required"]:
        return {
            "approved": True,
            "status": "AUTO_APPROVED",
            "message": "Human review was not required."
        }

    print("\n==============================")
    print("HUMAN REVIEW REQUIRED")
    print("==============================")

    print(f"Risk level: {safety_result['risk_level']}")
    print(f"Message: {safety_result['message']}")

    while True:
        choice = input(
            "\nApprove this inspection result? "
            "[y = approve / n = reject]: "
        ).strip().lower()

        if choice == "y":
            return {
                "approved": True,
                "status": "HUMAN_APPROVED",
                "message": "Inspection result approved by human reviewer."
            }

        if choice == "n":
            return {
                "approved": False,
                "status": "HUMAN_REJECTED",
                "message": "Inspection result rejected by human reviewer."
            }

        print("Please enter y or n.")


if __name__ == "__main__":
    safety = {
        "risk_level": "HIGH",
        "human_review_required": True,
        "message": "High-risk condition detected."
    }

    result = request_human_review(safety)

    print("\nReview Result:")
    print(result)