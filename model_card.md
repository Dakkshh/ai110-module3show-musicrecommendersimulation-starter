# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Find your taste in my jam  

---

## 2. Intended Use  

This recommender is a classroom exploration tool, not a production system. It's designed to take a single stated "taste profile" (favorite genre, favorite mood, target energy, target tempo) and return a small ranked list of songs from a fixed catalog that best match those preferences, along with a plain-language explanation for each pick. It assumes the user can articulate their preferences directly (rather than the system inferring taste from listening history), and it assumes those preferences are internally consistent — it has no way to detect or handle contradictory requests. It's meant to demonstrate, at a small and transparent scale, how a content-based recommender turns attribute data into ranked suggestions — not to serve real listeners or scale beyond its 18-song catalog.

---

## 3. How the Model Works  

Each song has a genre, a mood, an energy level (0 to 1), and a tempo in beats per minute. A user's taste profile states a favorite genre, a favorite mood, a target energy, and a target tempo. The model checks every song in the catalog against that profile and gives it points: matching the genre exactly is worth the most points, matching the mood is worth a bit less, and having an energy or tempo close to the user's target is worth up to a point each — the closer the value, the more points, rather than just rewarding "higher energy" or "faster tempo" outright. All the points get added up into one score per song, and the songs are then sorted from highest score to lowest, with the top few returned as recommendations. Each recommendation also comes with a short explanation listing exactly which parts of the profile it matched, so the reasoning is visible instead of hidden.

One change from the starter logic: during Phase 4 testing, the weights on genre and energy were experimentally adjusted (genre's weight was lowered and energy's weight was raised) to see how sensitive the rankings were to those choices — see the Evaluation and Limitations sections below for what that revealed.

---

## 4. Data  

The catalog contains 18 songs. The original starter file had 10 songs covering pop, lofi, rock, ambient, jazz, synthwave, and indie pop, with moods like happy, chill, intense, relaxed, moody, and focused. 8 more songs were added to broaden coverage: hip-hop, classical, folk, EDM, R&B, metal, country, and reggae, with moods like energetic, nostalgic, romantic, angry, and dreamy. Even with the expanded set, 18 songs is still a very small catalog — many genre/mood/energy/tempo combinations that a real user might want simply aren't represented, which is part of why the adversarial testing (see Limitations) exposed such a clear gap.

---

## 5. Strengths  

The system performs reliably when a user's stated preferences are internally consistent — that is, when genre, mood, energy, and tempo targets naturally belong together. In testing, profiles like "High-Energy Pop," "Chill Lofi," and "Deep Intense Rock" all correctly surfaced the one song in the catalog that matched genre, mood, energy, and tempo simultaneously (Sunrise City, Midnight Coding, and Storm Runner respectively), each scoring close to the maximum possible 5.5 points. The explanation strings (e.g., "genre match (+2.0); mood match (+1.5)...") also make it easy to see exactly why a song was recommended, which is a strength over black-box systems — a user could look at the output and immediately understand the reasoning.

---

## 6. Limitations and Bias 

Two separate biases showed up during testing:

**Weight-sensitive bias:** With the original weights (genre 2.0, mood 1.5, energy 1.0, tempo 1.0), a song that matched genre alone could outrank a song that matched mood and had closer energy/tempo, simply because genre carried the most points. After halving genre's weight and doubling energy's weight in an experiment, several rankings flipped — for example, in the "High-Energy Pop" profile, "Rooftop Lights" (mood match, no genre match) moved ahead of "Gym Hero" (genre match, no mood match) once energy counted for more. This shows the system's rankings are sensitive to weight choices, not just to how well a song objectively fits.

**Data-coverage bias:** An adversarial profile with contradictory preferences (favorite_genre="metal", favorite_mood="sad") was tested to see how the system handles conflicting signals. In both the original and reweighted versions, "Iron Fist" (metal/angry) won by a wide margin, and the "sad" mood target was never satisfied by anything in the catalog. Changing the weights did not fix this — no combination of weights can produce a good match when the catalog simply contains no low-energy, sad, metal-adjacent songs. This reveals a limitation that isn't about the scoring formula at all, but about the dataset itself: with only 18 songs, some legitimate (or even contradictory) preference combinations have no good match available, and the system has no way to say "I couldn't find anything that fits" — it just returns its best (still weak) option as if it were a strong recommendation.

---

## 7. Evaluation  

Four user profiles were tested against the 18-song catalog: "High-Energy Pop" (genre=pop, mood=happy, energy=0.85, tempo=122), "Chill Lofi" (genre=lofi, mood=chill, energy=0.38, tempo=76), "Deep Intense Rock" (genre=rock, mood=intense, energy=0.92, tempo=155), and an adversarial profile with contradictory preferences (genre=metal, mood=sad, energy=0.90, tempo=165).

For the three "normal" profiles, the top recommendation matched intuition exactly each time — the song sharing genre, mood, energy, and tempo with the profile scored highest, close to the maximum possible score. The adversarial profile was the most revealing test: it exposed that the system cannot detect when a user's own preferences are internally contradictory, and will confidently return a high-scoring recommendation even when a core preference (mood) was never actually satisfied.

A weight-shift experiment (halving genre's weight, doubling energy's weight) was also run to test sensitivity. It changed rankings for near-tied songs in the normal profiles (e.g., a strong mood/energy match could now beat a genre-only match), but did not change the outcome of the adversarial profile at all — confirming that the adversarial issue is a data-coverage problem, not a tunable weighting problem.

---

## 8. Future Work  

A few improvements worth trying next:

- **Add more features**, like valence or danceability, so the system can distinguish songs that currently look similar on genre/mood/energy/tempo alone but feel different (e.g., a genre match with mismatched valence still gets treated as a good fit right now).
- **Detect contradictory preferences** — if a user's mood and genre targets are historically never seen together, the system could flag that instead of silently returning its best (weak) guess as if it were confident.
- **Improve diversity in the top results** — right now, if one song is a near-perfect match, it's common for the next few results to be thematically very similar (e.g., all lofi/chill in the Lofi profile). A real system might intentionally include one or two more different songs so the user doesn't get a "genre bubble" of nearly-identical suggestions.

---

## 9. Personal Reflection  

My biggest learning moment was realizing my UserProfile design didn't match what the tests actually needed — a good reminder to check the real spec instead of assuming.
AI helped a lot with the scoring math and generating test cases I wouldn't have thought of, like a contradictory "metal + sad" profile. But I still had to double-check its code against my real files, since it can't see my repo and sometimes assumed fields that didn't exist yet.
What surprised me most: even a simple 4-feature system felt like real recommendations for normal cases — but the adversarial test showed it doesn't actually "know" when it fails. It just confidently returns its best guess, even when a preference was never matched.