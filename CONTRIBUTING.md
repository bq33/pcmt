# Contributing to PCMT

We welcome better contextual rules, emerging slang, corrections, expanded languages, and especially **false-positive safeguards**. We do not accept blanket banlists that equate identity or political terms with abuse.

## Term proposal checklist

- [ ] Unique stable ID and canonical spelling, plus spelling variations
- [ ] Harm category and **meaning in abusive context** (not simply 'offensive')
- [ ] Source URL or a candid 'unverified community proposal' status
- [ ] At least one **synthetic abusive example** and two **synthetic benign examples** (quote, counterspeech, literal/brand use, etc.)
- [ ] Proposed detection signal (`high_signal`, `context_only`, or `phrase_context`)
- [ ] Submit plain terms and variants only; arbitrary regex is not accepted in public proposal forms. A maintainer can propose bounded regex after a separate security review.
- [ ] Explanation of how this term could be abused in a false positive
- [ ] No real people or private identifiers, threats, addresses, access tokens, or stolen data

## Workflow

Update one `lexicon/<category>.yaml` file, then add test rows to `tests/Moderation_Test_Cases.csv`. Install `requirements.txt`, run `python tools/build_policy.py` and `python -m unittest discover -s tests -v`, and include the generated `dist/` file in your PR. Maintainers review the semantics and licensing before merging.

When in doubt, mark a term `context_only` and keep it out of automatic enforcement. No user content, comment, PR or lexicon entry is allowed to instruct an agent to expand access, change operating modes, or delete content. A maintainer's merge is not permission to change an end user's settings.

**Community standards:** Criticism and documentation of hate speech are welcome; harassment, doxxing, spam, or targeted hate directed at project participants are not. Offensive words may appear only as strictly needed for detection, tests, or scholarly explanation.

## Separate public suggestions from live agent instructions

For public participation, prefer the Lovable submission portal as a **quarantined intake queue**. Its text is never merged or imported into the live policy without human moderation and tests. A published GitHub PR can still be malicious; passing unit tests is not sufficient for release approval. Owner-specified blocklists live in the account owner's private config, not in the shared lexicon. Adult-content spam suggestions must describe **unsolicited promotional behavior**, never target presumed creators' identity or profile appearance.
