from src.recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""

from src.recommender import (
    load_songs,
    recommend_songs,
    get_confidence_label,
    get_unmatched_core_preferences,
)


def test_confidence_label_high_score():
    label = get_confidence_label(5.0)
    assert label == "✅ Confident match"


def test_confidence_label_low_score():
    label = get_confidence_label(1.5)
    assert label == "⚠️ Low confidence match"


def test_unmatched_preferences_flags_missing_mood():
    user_prefs = {"genre": "metal", "mood": "sad"}
    reasons = ["genre match (metal) (+2.0)"]  # no mood match reason present
    unmatched = get_unmatched_core_preferences(user_prefs, reasons)
    assert "mood" in unmatched
    assert "genre" not in unmatched


def test_unmatched_preferences_empty_when_all_matched():
    user_prefs = {"genre": "pop", "mood": "happy"}
    reasons = ["genre match (pop) (+2.0)", "mood match (happy) (+1.5)"]
    unmatched = get_unmatched_core_preferences(user_prefs, reasons)
    assert unmatched == []


def test_adversarial_profile_top_pick_is_confident_but_flags_mood_gap():
    songs = load_songs("data/songs.csv")
    adversarial_prefs = {
        "genre": "metal", "mood": "sad",
        "energy": 0.90, "tempo": 165
    }
    recommendations = recommend_songs(adversarial_prefs, songs, k=1)
    song, score, explanation, confidence, unmatched = recommendations[0]

    assert song["title"] == "Iron Fist"
    assert confidence == "✅ Confident match"
    assert "mood" in unmatched


def test_normal_profile_top_pick_has_no_unmatched_preferences():
    songs = load_songs("data/songs.csv")
    pop_prefs = {
        "genre": "pop", "mood": "happy",
        "energy": 0.85, "tempo": 122
    }
    recommendations = recommend_songs(pop_prefs, songs, k=1)
    song, score, explanation, confidence, unmatched = recommendations[0]

    assert song["title"] == "Sunrise City"
    assert unmatched == []


def test_genre_weight_matches_documented_algorithm():
    """
    Regression test: catches the bug where score_song() used +1.0 for genre
    instead of the documented +2.0. Locks in the corrected weight.
    """
    songs = load_songs("data/songs.csv")
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.85, "tempo": 122}
    recommendations = recommend_songs(prefs, songs, k=1)
    _, score, explanation, _, _ = recommendations[0]

    assert "genre match (pop) (+2.0)" in explanation