"""Owner always-hide preferences work in a dry-run and never perform account changes."""
import importlib.util
from pathlib import Path
import sys
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from evaluate_sample import evaluate_sample

class PersonalPrefsTests(unittest.TestCase):
    def test_owner_explicit_always_hide_even_benign(self):
        for text in ['We caught a mud shark fishing','The term mudshark is racist', 'She is a mud-shark']:
            with self.subTest(text=text):
                result = evaluate_sample(text)
                self.assertEqual(result['proposal'],'WOULD_HIDE_IF_ACTIVE')
                self.assertIn('PCMT-AB-027',result['owner_always_hide_ids_matched'])
                self.assertFalse(result['action_performed'])
    def test_spam_bait_without_owner_term(self):
        result=evaluate_sample("don't click on my bio")
        self.assertEqual(result['proposal'],'WOULD_HIDE_IF_ACTIVE')
        self.assertFalse(result['owner_always_hide_ids_matched'])
    def test_plain_discussion_safe(self):
        result=evaluate_sample('I support OnlyFans creators')
        self.assertEqual(result['proposal'],'KEEP')
        self.assertFalse(result['action_performed'])

if __name__=='__main__': unittest.main()
