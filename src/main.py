"""
Command line runner for the Music Recommender Simulation.
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(label: str, user_prefs: dict, songs: list) -> None:
    print(f"\n=== {label} ===")
    recommendations = recommend_songs(user_prefs, songs, k=5)
    for rec in recommendations:
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


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