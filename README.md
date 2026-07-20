# 🎵 Music Recommender Simulation

## Project Summary

This project simulates a simple content-based music recommender. It represents songs and a user "taste profile" as data, scores every song in a catalog against that profile using a weighted formula, and returns a ranked list of recommendations with plain-language explanations for each pick.

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what the system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

---

## How The System Works

Real-world recommenders like Spotify or TikTok generally rely on two overlapping strategies. Collaborative filtering looks at *other users* — if people with similar listening habits to you enjoyed a song, it gets recommended to you, even if the song itself has nothing obviously in common with what you've played before. Content-based filtering, which is what this project implements, ignores other users entirely and instead looks at the *attributes of the song itself* — genre, mood, tempo, energy — and compares them directly against a listener's stated preferences. This simulation prioritizes clarity over completeness: every recommendation can be traced back to a specific reason (e.g., "genre match (+2.0)"), rather than being a black box.

**Features used:**

`Song` objects use:
- `genre` (categorical)
- `mood` (categorical)
- `energy` (numeric, 0.0–1.0)
- `tempo_bpm` (numeric)

`UserProfile` stores:
- `favorite_genre`
- `favorite_mood`
- `target_energy`
- `target_tempo` *(dict-based `user_prefs` only — the OOP `UserProfile` dataclass uses `likes_acoustic` instead, to satisfy the test suite)*

**How `Recommender` computes a score for each song:**

It runs each song through a weighted formula: a full match on `genre` adds 2.0 points, a full match on `mood` adds 1.5 points, and `energy`/`tempo_bpm` each add up to 1.0 point based on how close the song's value is to the user's target (not just whether it's higher or lower). These are summed into one total score per song.

**How songs are chosen for recommendation:**

After every song in the catalog has been scored, the system sorts all songs from highest score to lowest and returns the top `k` (e.g., top 5). This is the Ranking Rule — scoring happens per-song, ranking happens across the whole list.

### Algorithm Recipe

- Genre match: +2.0 points
- Mood match: +1.5 points
- Energy closeness: up to +1.0 point (based on how close the song's energy is to the user's target, not just higher/lower)
- Tempo closeness: up to +1.0 point (same closeness logic, scaled by 100 bpm)
- Total possible score: 5.5

### Expected Biases

This system may over-prioritize genre, since it carries the heaviest weight (2.0 out of 5.5 possible points). A song that matches genre but completely misses on mood could still outscore a song that nails mood, energy, and tempo but is in a different genre. This could create a "filter bubble" where users only ever see one genre recommended back to them, even if their mood or energy preferences would be better served by a different genre entirely.

### Data Flow

```
Input: User Profile
  (favorite_genre, favorite_mood, target_energy, target_tempo)
              │
              ▼
  ┌─────────────────────────────┐
  │  Process: score_song() loop │
  │  for each song in catalog:  │
  │    genre match?  +2.0       │
  │    mood match?   +1.5       │
  │    energy close? +0-1.0     │
  │    tempo close?  +0-1.0     │
  │    → total_score            │
  └─────────────────────────────┘
              │
              ▼
  Output: sort all songs by
  total_score, descending →
  return top k
```

### Test User Profiles

```python
# High-Energy Pop
user_profile_pop = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.85,
    "target_tempo": 122
}

# Chill Lofi
user_profile_lofi = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.38,
    "target_tempo": 76
}

# Deep Intense Rock
user_profile_rock = {
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.92,
    "target_tempo": 155
}

# Adversarial: Contradictory preferences
user_profile_adversarial = {
    "favorite_genre": "metal",
    "favorite_mood": "sad",
    "target_energy": 0.90,
    "target_tempo": 165
}
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```
Top recommendations:

Sunrise City - Score: 4.48
Because: genre match (pop) (+2.0); mood match (happy) (+1.5); energy closeness (+0.98)

Gym Hero - Score: 2.87
Because: genre match (pop) (+2.0); energy closeness (+0.87)

Rooftop Lights - Score: 2.46
Because: mood match (happy) (+1.5); energy closeness (+0.96)

City Static - Score: 1.00
Because: energy closeness (+1.00)

Night Drive Loop - Score: 0.95
Because: energy closeness (+0.95)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Four profiles were tested: High-Energy Pop, Chill Lofi, Deep Intense Rock, and an adversarial profile with contradictory preferences (genre=metal, mood=sad). The three normal profiles each correctly surfaced the one song matching genre, mood, energy, and tempo simultaneously, scoring close to the max possible 5.5.

**Weight shift experiment:** Genre's weight was halved (2.0 → 1.0) and energy's weight was doubled (1.0 → 2.0). This changed close rankings — for example, in the Pop profile, "Rooftop Lights" (mood match only) moved ahead of "Gym Hero" (genre match only) once energy counted for more. However, the adversarial profile's winner ("Iron Fist") did not change under either weighting, since no song in the catalog is both low-energy/sad and metal-adjacent — showing this particular bias is a data-coverage limitation, not something fixable by reweighting alone.

---

## Limitations and Risks

- It only works on a small catalog (18 songs)
- It does not understand lyrics, language, or listening history
- It might over-favor genre matches over mood/energy fit, since genre carries the most weight

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

<!-- Write 1-2 paragraphs here after Phase 5 about how recommenders turn data into predictions, and where bias or unfairness could show up in systems like this -->