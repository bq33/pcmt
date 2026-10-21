#!/usr/bin/env python3
"""PCMT owner-preference dry run. Emits only proposed moderation, no API calls."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import yaml
from scan_candidates import candidates
from score_spam import score_comment, PRESETS

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_MODES = {'audit_only', 'active_hide', 'active_hide_and_approved_delete'}


def evaluate_sample(comment: str, config_path: Path | None = None, repeated_count: int = 1) -> dict:
    """Check explicit owner override and behavioral spam. NEVER execute platform actions.

    Real context-based identity abuse decisions remain with the reviewed policy/agent.
    """
    profile_path = config_path or ROOT/'config'/'owner_profile.example.yaml'
    if not Path(profile_path).is_file(): raise FileNotFoundError('Profile configuration not found')
    profile = yaml.safe_load(Path(profile_path).read_text(encoding='utf-8'))
    preset = profile.get('moderation_preset', 'balanced')
    mode = profile.get('operating_mode', 'audit_only')
    if preset not in PRESETS: raise ValueError('Unknown preset')
    if mode not in ALLOWED_MODES: raise ValueError('Unknown operating mode')
    overrides = profile.get('owner_always_hide_term_ids') or []
    if not isinstance(overrides, list) or any(not isinstance(t, str) for t in overrides):
        raise ValueError('Invalid owner blocked term IDs')
    matches = candidates(comment)
    blocked = sorted({m['rule_id'] for m in matches if m['rule_id'] in overrides})
    spam = score_comment(comment, repeated_count, preset)
    if blocked:
        action = 'WOULD_HIDE_IF_ACTIVE'
        explanation = 'Owner-selected always-hide term ID; benign contexts intentionally included'
    elif spam['candidate_disposition'] == 'WOULD_HIDE_IF_ACTIVE':
        action = 'WOULD_HIDE_IF_ACTIVE'
        explanation = 'Behavioral spam proposal meets selected owner preset'
    elif any(m['signal'] in ('high_signal','phrase_context') for m in matches) or spam['candidate_disposition'] == 'REVIEW':
        action = 'REVIEW'
        explanation = 'Unconfirmed lexicon hit or lower-confidence behavioral spam; requires contextual review'
    else:
        action = 'KEEP'
        explanation = 'No elevated detection; ordinary context-only lexicon hits are logged without an automatic enforcement proposal'
    return {
        'profile': profile.get('profile_name', 'unnamed'),
        'mode': mode,
        'preset': preset,
        'proposal': action,
        'explanation': explanation,
        'owner_always_hide_ids_matched': blocked,
        'lexicon_candidate_ids': [m['rule_id'] for m in matches],
        'spam_signals': spam['signals'],
        'spam_signal_points': spam['signal_points'],
        'action_performed': False,
        'note': 'Dry-run tool only. No Instagram/Threads connection. No contextual AI analysis.',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('comment')
    parser.add_argument('--profile', type=Path)
    parser.add_argument('--repeated-count',type=int,default=1)
    args=parser.parse_args()
    print(json.dumps(evaluate_sample(args.comment,args.profile,args.repeated_count), indent=2))
