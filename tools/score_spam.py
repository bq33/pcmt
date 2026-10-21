#!/usr/bin/env python3
"""Offline signals for unsolicited commercial and adult-content promotion.

This is a deterministic candidate classifier, NOT a bot detector, identity classifier,
AI agent, or social-platform connector. Never executes untrusted text or follows URLs.

Returned actions are proposals; current policy operating_mode still governs.
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata

PRESETS = {
    'balanced': {'review': 4, 'hide': 7},
    'aggressive': {'review': 2, 'hide': 4},
    'maximum': {'review': 2, 'hide': 3},
}

# Patterns describe observed solicitation behavior, not demographics or appearance.
# They operate on a single social comment, not on a person's identity or their profile.
REVERSE_BIO = re.compile(
    r"\b(?:don['’]?t|do\s+not|never)\s+"
    r"(?:click|check|look\s+at|visit|open|tap|peek\s+at)\s+"
    r"(?:(?:on|at|in)\s+)?(?:my|the)\s+"
    r"(?:bio|profile|page|link)\b", re.I)
PROFILE_CTA = re.compile(
    r"\b(?:check(?:\s+out)?|click|visit|tap|see|go\s+to|follow)\s+"
    r"(?:(?:on|at|in)\s+)?(?:my|our|the)\s+"
    r"(?:bio|profile|page|link|account)\b|\b(?:link\s+in\s+(?:(?:my|the)\s+)?bio)\b", re.I)
ADULT_SERVICE = re.compile(r"\b(?:only\s*fans|onlyfans|fansly|premium\s+snap|private\s+snap)\b", re.I)
SOLICITATION = re.compile(r"\b(?:subscribe|sign\s+up|join|unlock|paid|exclusive|premium|free|dm\s+me|link\s+in\s+(?:(?:my|the)\s+)?bio|in\s+bio|check\s+my\s+bio|see\s+my\s+bio)\b", re.I)
ADULT_TEASER = re.compile(r"\b(?:spicy\s+(?:pics?|content)|uncensored\s+(?:pics?|content)|nudes?|private\s+content)\b", re.I)
PROMO_ACCOUNT = re.compile(r"\b(?:promote\s+it\s+on|send\s+(?:it|pic|photo|post)\s+to)\s+@?[\w.]{2,}\b", re.I)
GENERIC_PRAISE = re.compile(r"\b(?:nice\s+(?:post|pic|photo|content)|great\s+post|amazing\s+(?:post|pic|photo)|love\s+your\s+(?:post|page|content))\b", re.I)
DM_CTA = re.compile(r"\b(?:dm|message|inbox)\s+me\s+(?:for|to|get)\b", re.I)
META_DISCUSSION = re.compile(r"\b(?:the\s+phrase|people\s+say|this\s+is\s+spam|that\s+is\s+spam|comment\s+bots?|spam\s+(?:comment|tactic|pattern)|example\s+of\s+spam)\b", re.I)

def _normalize(comment: str) -> str:
    """Normalize a bounded copy for scoring, never overwrite original content."""
    text = unicodedata.normalize('NFKC', comment[:4000]).casefold()
    text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cf')
    return text.replace('’', "'")


def score_comment(comment: str, repeated_count: int = 1, preset: str = 'aggressive') -> dict:
    """Returns explainable candidate scoring, not a decision to actually moderate."""
    if preset not in PRESETS:
        raise ValueError('Unknown moderation preset')
    if not isinstance(comment, str):
        raise TypeError('Comment must be text')
    if not 1 <= repeated_count <= 100000:
        raise ValueError('repeated_count must be between 1 and 100000')
    text = _normalize(comment)
    hits = []
    score = 0

    def add(name: str, weight: int):
        nonlocal score
        hits.append(name)
        score += weight

    if REVERSE_BIO.search(text):
        add('reverse_psychology_profile_bait', 4)
    elif PROFILE_CTA.search(text):
        add('profile_link_cta', 3)

    if ADULT_SERVICE.search(text) and SOLICITATION.search(text):
        add('adult_subscription_solicitation', 5)
    elif ADULT_TEASER.search(text) and (SOLICITATION.search(text) or PROFILE_CTA.search(text)):
        add('adult_content_solicitation', 4)
    if PROMO_ACCOUNT.search(text):
        add('promote_on_another_account', 4)
    if DM_CTA.search(text):
        add('unsolicited_dm_cta', 2)
    if GENERIC_PRAISE.search(text) and (PROFILE_CTA.search(text) or REVERSE_BIO.search(text)):
        add('generic_praise_plus_cta', 2)
    if repeated_count >= 3:
        add('same_text_repeated_across_owned_posts', 3)
    # Explicit discussion of spam patterns is not treated as unsolicited promotion.
    if META_DISCUSSION.search(text) and score > 0:
        hits.append('educational_or_counterspeech_context')
        score = max(0, score - 4)

    thresholds = PRESETS[preset]
    proposal = ('WOULD_HIDE_IF_ACTIVE' if score >= thresholds['hide'] else
                'REVIEW' if score >= thresholds['review'] else 'KEEP')
    return {
        'category': 'unsolicited_promotion_or_spam',
        'preset': preset,
        'signals': hits,
        'signal_points': score,
        'candidate_disposition': proposal,
        'operating_mode': 'audit_only',
        'action_performed': False,
        'warning': 'Not proof of bot identity; no platform actions performed',
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('comment', help='Sample comment text; evaluated offline only')
    parser.add_argument('--preset', choices=list(PRESETS), default='aggressive')
    parser.add_argument('--repeated-count', type=int, default=1)
    args = parser.parse_args()
    print(json.dumps(score_comment(args.comment,args.repeated_count,args.preset),indent=2))
