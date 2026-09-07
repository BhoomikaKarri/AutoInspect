from pathlib import Path
import json


DATA_DIR = Path("data")


def load_bridge_qa(bridge_folder: Path):
    qa_path = bridge_folder / "qa_pairs.json"

    if not qa_path.exists():
        return []

    with open(qa_path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_ratings(qa_pairs):
    ratings = []

    for item in qa_pairs:
        rating = item.get("condition_rating")

        if not isinstance(rating, dict):
            continue

        score = rating.get("score")

        if score is not None:
            ratings.append(
                {
                    "score": score,
                    "question": item.get("question", ""),
                }
            )

    return ratings


def analyze_bridges():
    bridge_results = []

    for bridge_folder in sorted(DATA_DIR.iterdir()):
        if not bridge_folder.is_dir():
            continue

        qa_pairs = load_bridge_qa(bridge_folder)
        ratings = extract_ratings(qa_pairs)

        scores = [item["score"] for item in ratings]

        if not scores:
            continue

        bridge_results.append(
            {
                "bridge": bridge_folder.name,
                "ratings": scores,
                "average_rating": round(sum(scores) / len(scores), 2),
                "lowest_rating": min(scores),
                "highest_rating": max(scores),
                "rating_count": len(scores),
            }
        )

    return bridge_results


def get_bridge_analysis(bridge_name=None):
    results = analyze_bridges()

    if bridge_name is None:
        return results

    for result in results:
        if result["bridge"] == bridge_name:
            return result

    return None


if __name__ == "__main__":
    results = analyze_bridges()

    print("\n==============================")
    print("ANALYST AGENT")
    print("==============================")

    for result in results:
        print(f"\nBridge: {result['bridge']}")
        print(f"Ratings: {result['ratings']}")
        print(f"Average rating: {result['average_rating']}")
        print(f"Lowest rating: {result['lowest_rating']}")
        print(f"Highest rating: {result['highest_rating']}")
        print(f"Number of rated components: {result['rating_count']}")