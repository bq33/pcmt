"""Offline functional checks. Contextual moderation is NOT delegated to these tests."""
import csv, importlib.util, pathlib, re, unittest, yaml

ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('pcmt_build',ROOT/'tools'/'build_policy.py')
build=importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)
scan_spec=importlib.util.spec_from_file_location('pcmt_scanner',ROOT/'tools'/'scan_candidates.py')
scanner=importlib.util.module_from_spec(scan_spec)
scan_spec.loader.exec_module(scanner)

class PolicyTests(unittest.TestCase):
    def test_every_lexicon_valid_and_unique(self):
        docs=build.load_categories()
        self.assertGreaterEqual(sum(len(d['entries']) for d in docs),100)
        self.assertEqual(len(docs),12)

    def test_regex_variants_for_mudshark(self):
        for text in ['mudshark','mud shark','mud-shark','mud_shark','M.U.D.S.H.A.R.K','mudsharks','mudsharking','mud sharking']:
            with self.subTest(text=text):
                self.assertIn('PCMT-AB-027',{h['rule_id'] for h in scanner.candidates(text)})

    def test_no_mudshark_substring_collision(self):
        for text in ['smudsharky','mudsharkable','mudsharkedish','unmudshark']:
            with self.subTest(text=text):
                self.assertNotIn('PCMT-AB-027',{h['rule_id'] for h in scanner.candidates(text)})

    def test_benign_mentions_are_candidates_but_not_verdicts(self):
        # Even a benign fish or business name is a candidate; semantics stay with the policy/agent.
        for text in ['Mudshark Ceramics makes pottery','We caught a mud shark while fishing','The phrase mudshark is racist']:
            with self.subTest(text=text):
                self.assertIn('PCMT-AB-027',{h['rule_id'] for h in scanner.candidates(text)})
                self.assertNotIn('WOULD_HIDE_IF_ACTIVE',repr(scanner.candidates(text)))

    def test_contextual_cases_include_benign_and_harmful(self):
        with open(ROOT/'tests'/'Moderation_Test_Cases.csv',newline='',encoding='utf-8') as f:
            data=list(csv.DictReader(f))
        self.assertGreaterEqual(len(data),75)
        self.assertTrue(any('mudshark' in r['example_comment'].lower() and r['expected_disposition_in_audit']=='KEEP' for r in data))
        self.assertTrue(any('mudshark' in r['example_comment'].lower() and r['expected_disposition_in_audit']=='WOULD_HIDE_IF_ACTIVE' for r in data))

    def test_compiled_policy_has_terms_safety_and_two_platforms(self):
        policy=build.compile_policy().read_text(encoding='utf-8')
        self.assertIn('operating_mode: audit_only',policy)
        self.assertIn('platforms: [instagram, threads]',policy)
        self.assertIn('mudshark',policy)
        self.assertIn('R-013',policy)
        self.assertIn('R-014',policy)
        self.assertIn("don't click on my bio",policy)
        self.assertIn('moderation_preset: aggressive',policy)
        self.assertIn('Appendix A',policy)
        self.assertIn('do not take action', policy)

if __name__=='__main__': unittest.main()
