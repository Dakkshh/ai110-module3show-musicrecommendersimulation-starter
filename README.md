# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - genre, mood, energy, tempo_bpm
- What information does your `UserProfile` store
  - favorite_genre, favorite_mood, target_energy, target_tempo
- How does your `Recommender` compute a score for each song
  - It runs each song through a weighted formula: a full match on genre adds 2.0 points, a full match on mood adds 1.5 points, and energy/tempo_bpm each add up to 1.0 point based on how close the song's value is to the user's target (not just whether it's higher or lower). These four numbers are summed into one total score per song.
- How do you choose which songs to recommend
  - After every song in the catalog has been scored, the system sorts all songs from highest score to lowest and returns the top k (e.g., top 5). This is the Ranking Rule — scoring happens per-song, ranking happens across the whole list.
  ### Algorithm Recipe

- Genre match: +2.0 points
- Mood match: +1.5 points
- Energy closeness: up to +1.0 point (based on how close the song's energy is to the user's target, not just higher/lower)
- Tempo closeness: up to +1.0 point (same closeness logic, scaled by 100 bpm)
- Total possible score: 5.5

### Expected Biases

This system may over-prioritize genre, since it carries the heaviest weight (2.0 out of 5.5 possible points). A song that matches genre but completely misses on mood could still outscore a song that nails mood, energy, and tempo but is in a different genre. This could create a "filter bubble" where users only ever see one genre recommended back to them, even if their mood or energy preferences would be better served by a different genre entirely.

You can include a simple diagram or bullet list if helpful.
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

---

## Getting Started
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

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
## Sample Recommendation Output

\`\`\`
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
\`\`\`
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



