# 🎵 Music Recommender Simulation — Applied AI System Extension

## Base Project

This project extends **Music Recommender Simulation**, originally built for Module 3. The original project simulated a content-based music recommender: it represented songs and a user "taste profile" as data, scored every song in a catalog against that profile using a weighted formula, and returned a ranked list of recommendations with plain-language explanations for each pick.

This extension adds a **Reliability and Testing System** on top of that original logic — the AI feature required for the Applied AI System assignment.

---

## Title and Summary

**VibeFinder: Reliability-Aware Music Recommender**

This system doesn't just recommend songs — it tells you *how much to trust* each recommendation. On top of the original weighted scoring engine, it now flags low-confidence matches, detects when a song scored well overall but missed a preference you specifically asked for (like genre or mood), logs these events for review, and is backed by an automated test suite that locks in and verifies this behavior.

This matters because a recommender that just returns its "best guess" without saying how confident it is can quietly mislead a user — the system might return a technically high-scoring song that completely ignores something the user asked for. Surfacing that gap, instead of hiding it, is the whole point of this extension.

---

## Architecture Overview

The system diagram is in [`diagrams/architecture.mmd`](diagrams/architecture.mmd).

At a high level: a user profile (genre, mood, energy, tempo) flows into `load_songs()`, which reads the song catalog. Every song is scored by `score_song()` using the weighted algorithm. That score then passes through two new reliability checks — `get_confidence_label()` (is this score actually high?) and `get_unmatched_core_preferences()` (did this song actually match what was asked, regardless of score?) — before `recommend_songs()` sorts and returns the top results. Every run is logged to `recommender.log`, and a 9-test pytest suite validates the scoring, confidence, and gap-detection logic independently.

---

## How The System Works

Real-world recommenders like Spotify or TikTok generally rely on two overlapping strategies. Collaborative filtering looks at *other users* — if people with similar listening habits to you enjoyed a song, it gets recommended to you. Content-based filtering, which is what this project implements, ignores other users entirely and instead compares a song's own attributes — genre, mood, tempo, energy — directly against a listener's stated preferences.

**Features used:**

`Song` objects use: `genre`, `mood`, `energy` (0.0–1.0), `tempo_bpm`

`user_prefs` (functional path) uses: `genre`, `mood`, `energy`, `tempo`

### Algorithm Recipe

- Genre match: +2.0 points
- Mood match: +1.5 points
- Energy closeness: up to +1.0 point (closer to target = more points, not just higher/lower)
- Tempo closeness: up to +1.0 point (same closeness logic, scaled by 100 bpm)
- Total possible score: 5.5

---

## The Reliability Feature (New)

Two checks now run on every scored song:

**1. Confidence labeling** — `get_confidence_label(score)` flags any recommendation scoring below 40% of the max possible score (5.5) as `⚠️ Low confidence match`, otherwise `✅ Confident match`.

**2. Preference-gap detection** — `get_unmatched_core_preferences()` separately checks whether the user's *specifically requested* genre and mood were actually matched, regardless of the song's overall score. This catches a case the confidence label alone misses: a song can score high (and look "confident") while still ignoring a core preference entirely.

**Example this caught:** in the adversarial test profile (genre=metal, mood=sad), the top pick "Iron Fist" scores 3.90 and shows `✅ Confident match` — but it never matched "sad" mood at all. The gap-detection flag catches this and prints `⚠️ Note: requested mood not matched by this song`, even though the confidence label alone would have made it look like a solid recommendation.

Both events are logged to `recommender.log` for later review.

---

## Design Decisions

We chose a **Reliability/Testing System** as our required AI feature instead of RAG or an agentic workflow, for three reasons:

1. **Reproducibility.** This feature requires no API keys, no network calls, and no external dependencies — it runs identically for any grader on any machine, with zero setup risk.
2. **It builds directly on work already done.** Our Phase 4 weight-shift experiment and adversarial profile testing had already surfaced real reliability issues manually; this feature formalizes those findings into permanent, automated checks instead of one-off manual observations.
3. **It's more honest about system limitations.** Rather than hiding uncertainty behind a single score, the system now actively tells the user when it's guessing vs. actually confident — this felt like a more meaningful "trustworthiness" feature than adding a generative layer on top of the same underlying scores.

**Trade-off:** we did not add a generative (RAG/LLM) explanation layer, so the explanations remain template-based ("genre match (+2.0)") rather than natural language. Given the time budget, we prioritized a feature that meaningfully changes system behavior and can be fully automated-tested over one that would add generative polish without adding measurable reliability.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):
```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
```

2. Install dependencies:
```bash
   pip install -r requirements.txt
```

3. Run the app:
```bash
   python -m src.main
```

### Running Tests

```bash
pytest -v
```

---

## Sample Interactions (Reproducible Execution Evidence)

**Command run:**
```bash
python -m src.main
```

**Sample output (High-Energy Pop and Adversarial profiles shown):**
=== High-Energy Pop ===
Sunrise City - Score: 5.43 [✅ Confident match]
Because: genre match (pop) (+2.0); mood match (happy) (+1.5); energy closeness (+0.97); tempo closeness (+0.96)

Gym Hero - Score: 3.82 [✅ Confident match]
Because: genre match (pop) (+2.0); energy closeness (+0.92); tempo closeness (+0.90)
⚠️ Note: requested mood not matched by this song

=== Adversarial (Metal genre, Sad mood) ===
Iron Fist - Score: 3.90 [✅ Confident match]
Because: genre match (metal) (+2.0); energy closeness (+0.93); tempo closeness (+0.97)
⚠️ Note: requested mood not matched by this song

Storm Runner - Score: 1.86 [⚠️ Low confidence match]
Because: energy closeness (+0.99); tempo closeness (+0.87)
⚠️ Note: requested genre, mood not matched by this song


**Log output (`recommender.log`):**

2026-08-02 22:03:03,305 - INFO - Profile 'High-Energy Pop' run. Top score: 5.43
2026-08-02 22:03:03,309 - WARNING - Low confidence recommendation for 'High-Energy Pop': Neon Pulse (score 1.84)
2026-08-02 22:03:03,315 - INFO - Profile 'Adversarial (Metal genre, Sad mood)' run. Top score: 3.90
2026-08-02 22:03:03,315 - WARNING - Low confidence recommendation for 'Adversarial (Metal genre, Sad mood)': Storm Runner (score 1.86)


**Test suite run:**
```bash
pytest -v
```

collected 9 items
tests/test_recommender.py::test_recommend_returns_songs_sorted_by_score PASSED
tests/test_recommender.py::test_explain_recommendation_returns_non_empty_string PASSED
tests/test_recommender.py::test_confidence_label_high_score PASSED
tests/test_recommender.py::test_confidence_label_low_score PASSED
tests/test_recommender.py::test_unmatched_preferences_flags_missing_mood PASSED
tests/test_recommender.py::test_unmatched_preferences_empty_when_all_matched PASSED
tests/test_recommender.py::test_adversarial_profile_top_pick_is_confident_but_flags_mood_gap PASSED
tests/test_recommender.py::test_normal_profile_top_pick_has_no_unmatched_preferences PASSED
tests/test_recommender.py::test_genre_weight_matches_documented_algorithm PASSED
9 passed in 0.06s


---

## Testing Summary

9 out of 9 tests passed. One test (`test_genre_weight_matches_documented_algorithm`) was written specifically to catch a real bug we found: the original `score_song()` function used a genre weight of +1.0 and an energy weight of up to +2.0, while the README and model card had always documented +2.0 for genre and +1.0 for energy. The code was corrected to match the documented algorithm, and this test now guards against that regression happening again.

The adversarial profile test also confirmed a more subtle finding: a song can be labeled `✅ Confident match` by score alone while still completely failing to match a user's specifically requested preference (mood, in this case). This is why we built preference-gap detection as a separate signal from the confidence score — one measures "how high did it score," the other measures "did it actually give you what you asked for."

---

## Limitations and Risks

- Only works on an 18-song catalog
- Does not understand lyrics, language, or listening history
- Confidence labeling is based on total score magnitude, not on which specific preferences were satisfied — this is why preference-gap detection was added as a separate, independent check
- No mechanism yet to refuse a recommendation entirely when nothing in the catalog is a good fit — the system always returns its best available option, even when that option isn't good

---

## Reflection

See [`model_card.md`](model_card.md) for the full responsible-AI reflection, including AI collaboration examples, biases, misuse considerations, and testing surprises.

This project taught us that reliability isn't just about tests passing — it's about designing checks that catch things a single score can hide. The adversarial profile test in particular showed that "high score" and "actually did what was asked" are two different questions, and a trustworthy system needs to answer both.