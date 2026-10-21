# Changelog

## 1.2.0 — 2026-10-16

- Added owner-configurable moderation presets, with `aggressive` recommended for personal-account preference and `audit_only` still the default operation.
- Added a separate owner override example for always-hiding `mudshark` variants regardless of benign interpretation (explicit opt-in required).
- Added 16 community lexicon candidates for reverse-psychology bio bait, commercial solicitation, premium-content funneling, and unrelated profile promotion.
- Added an offline, deterministic spam-signals scorer, per-owner override dry-run evaluator, and regression cases. Signals classify **promotional behavior**, not whether a commenter is really a bot, sex worker, or adult model.
- Added a dedicated Lovable submission-portal brief and repo security checklist to isolate untrusted suggestions from live moderation instructions.
- Improved prompt-injection and GitHub CI hardening guidance; no secrets, platform connections, or automatic actions are included.


## 1.1.0 — 2026-10-16

- Renamed concept to **Personal Content Moderation Tool (PCMT)**.
- Added **Threads** as a first-class target alongside Instagram with per-platform capability checks.
- Converted initial term lists into community-maintainable category YAML dictionaries.
- Added `mudshark`/`mud shark` and spelling variants, `R-013` detector, documented false-positive contexts, and benchmark examples.
- Added a standalone compiled Markdown policy for Muse; default remains **audit_only**.
- Added contributor workflow, issue/PR templates, validation tests and continuous integration configuration.
- No direct account integration or automatic enforcement added.

## 1.0.0 — 2026-10-16

- Instagram-only starter moderation policy and initial contextual test cases.
