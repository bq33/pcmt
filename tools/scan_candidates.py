#!/usr/bin/env python3
"""Local candidate term detection ONLY: returns possible hits, never moderation decisions.

Do not feed comment text to a shell without standard quoting. No network calls or account actions.
"""
import argparse
from pathlib import Path
import re, sys
import unicodedata
import yaml

ROOT=Path(__file__).resolve().parents[1]

def candidates(text: str):
    text=unicodedata.normalize('NFKC',text)
    found=[]
    for file in sorted((ROOT/'lexicon').glob('*.yaml')):
        doc=yaml.safe_load(file.read_text(encoding='utf-8'))
        for entry in doc['entries']:
            if 'pattern' in entry:
                match=re.search(entry['pattern'],text)
            else:
                forms=[entry['term']]+entry.get('variants',[])
                match=next((m for form in forms if (m:=re.search(r'(?<!\w)'+re.escape(form)+r'(?!\w)',text,re.I))),None)
            if match:
                found.append({'rule_id':entry['id'], 'category':doc['category'], 'signal':entry['signal'], 'matched':match.group(0)})
    return found

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('comment',help='Comment text to scan locally (not stored or posted)')
    args=ap.parse_args()
    for hit in candidates(args.comment):
        print(f"CANDIDATE ONLY: {hit['rule_id']} / {hit['signal']} / {hit['matched']!r}")
    if not candidates(args.comment): print('No lexicon candidate. This does NOT mean the comment is safe.')
    print('No automatic moderation decisions or social account actions are performed.')
