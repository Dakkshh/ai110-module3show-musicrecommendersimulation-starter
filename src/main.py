"""
Command line runner for the Music Recommender Simulation.
"""

import logging
from src.recommender import load_songs, recommend_songs

logging.basicConfig(
    filename="recommender.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def print_recommendations(label: str, user_prefs: dict, songs: list) -> None:
    print(f"\n=== {label} ===")
    recommendations = recommend_songs(user_prefs, songs, k=5)

    top_score = recommendations[0][1] if recommendations else 0.0
    logging.info(f"Profile '{label}' run. Top score: {top_score:.2f}")

    for rec in recommendations:
        song, score, explanation, confidence, unmatched = rec
        print(f"{song['title']} - Score: {score:.2f} [{confidence}]")
        print(f"Because: {explanation}")

        if unmatched:
            unmatched_str = ", ".join(unmatched)
            print(f"⚠️ Note: requested {unmatched_str} not matched by this song")
            logging.warning(
                f"Preference gap for '{label}': {song['title']} did not match requested {unmatched_str}"
            )

        print()

        if confidence.startswith("⚠️"):
            logging.warning(f"Low confidence recommendation for '{label}': {song['title']} (score {score:.2f})")

def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = {
        "High-Energy Pop": {
            "genre": "pop", "mood": "happy",
            "energy": 0.85, "tempo": 122
        },
        "Chill Lofi": {
            "genre": "lofi", "mood": "chill",
            "energy": 0.38, "tempo": 76
        },
        "Deep Intense Rock": {
            "genre": "rock", "mood": "intense",
            "energy": 0.92, "tempo": 155
        },
        "Adversarial (Metal genre, Sad mood)": {
            "genre": "metal", "mood": "sad",
            "energy": 0.90, "tempo": 165
        },
    }

    for label, user_prefs in profiles.items():
        print_recommendations(label, user_prefs, songs)


if __name__ == "__main__":
    main()