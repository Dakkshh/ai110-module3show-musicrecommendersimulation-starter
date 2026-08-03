from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv


@dataclass
class Song:
    """Represents a song and its attributes. Required by tests/test_recommender.py"""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences. Required by tests/test_recommender.py"""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _score_song_oop(user: UserProfile, song: Song) -> Tuple[float, List[str]]:
    """Shared scoring logic for the OOP Recommender."""
    score = 0.0
    reasons = []

    if song.genre == user.favorite_genre:
        score += 2.0
        reasons.append(f"genre match ({user.favorite_genre}) (+2.0)")

    if song.mood == user.favorite_mood:
        score += 1.5
        reasons.append(f"mood match ({user.favorite_mood}) (+1.5)")

    energy_closeness = 1 - abs(song.energy - user.target_energy)
    energy_points = max(0.0, energy_closeness) * 1.0
    score += energy_points
    reasons.append(f"energy closeness (+{energy_points:.2f})")

    is_acoustic = song.acousticness > 0.5
    if is_acoustic == user.likes_acoustic:
        score += 0.5
        reasons.append("acoustic preference match (+0.5)")

    return score, reasons


class Recommender:
    """OOP implementation of the recommendation logic. Required by tests/test_recommender.py"""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [(_score_song_oop(user, song)[0], song) for song in self.songs]
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = _score_song_oop(user, song)
        if not reasons:
            return "No matching preferences found for this song."
        return "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file. Required by src/main.py"""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    Expects user_prefs keys: "genre", "mood", "energy", and optionally "tempo".
    """
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append(f"genre match ({user_prefs['genre']}) (+2.0)")

    if song["mood"] == user_prefs.get("mood"):
        score += 1.5
        reasons.append(f"mood match ({user_prefs['mood']}) (+1.5)")

    if "energy" in user_prefs:
        energy_closeness = max(0.0, 1 - abs(song["energy"] - user_prefs["energy"])) * 1.0
        score += energy_closeness
        reasons.append(f"energy closeness (+{energy_closeness:.2f})")

    if "tempo" in user_prefs:
        tempo_closeness = max(0.0, 1 - abs(song["tempo_bpm"] - user_prefs["tempo"]) / 100)
        score += tempo_closeness
        reasons.append(f"tempo closeness (+{tempo_closeness:.2f})")

    return score, reasons

MAX_POSSIBLE_SCORE = 5.5
LOW_CONFIDENCE_THRESHOLD = 0.4  # 40% of max possible score


def get_confidence_label(score: float) -> str:
    """
    Returns a human-readable confidence label based on how close
    the score is to the maximum possible score.
    """
    ratio = score / MAX_POSSIBLE_SCORE
    if ratio < LOW_CONFIDENCE_THRESHOLD:
        return "⚠️ Low confidence match"
    return "✅ Confident match"

def get_unmatched_core_preferences(user_prefs: Dict, reasons: List[str]) -> List[str]:
    """
    Checks whether the user's core stated preferences (genre, mood) were
    actually satisfied by this song, regardless of overall score.
    Returns a list of preference names that were requested but not matched.
    """
    unmatched = []

    if "genre" in user_prefs:
        genre_matched = any(reason.startswith("genre match") for reason in reasons)
        if not genre_matched:
            unmatched.append("genre")

    if "mood" in user_prefs:
        mood_matched = any(reason.startswith("mood match") for reason in reasons)
        if not mood_matched:
            unmatched.append("mood")

    return unmatched


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str, str, List[str]]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    Returns tuples of (song, score, explanation, confidence_label, unmatched_preferences).
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "No matching preferences found."
        confidence = get_confidence_label(score)
        unmatched = get_unmatched_core_preferences(user_prefs, reasons)
        scored.append((song, score, explanation, confidence, unmatched))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]