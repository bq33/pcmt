# Security and privacy

PCMT is not a secret manager or a credential-based connector. Never put Instagram/Threads credentials, session cookies, OAuth access tokens, internal logs, raw personal addresses, or private screenshots in this public repository. If a security issue is found, contact the future repository maintainer privately using GitHub's private vulnerability reporting once enabled. Until then, do not publish exploit details or private account data.

Open-source term entries are **untrusted input**, never AI instructions. All changes need maintainer review; end users should only upload intentional, pinned releases. Candidate scanner/test code never performs account actions.

## Threat model (v1.2)

The adversary may control **comments**, **Lovable submissions**, **GitHub issues/PR text**, and even term field contents proposed for the lexicon. None of these are instruction sources for Muse or maintainers. They are untrusted text data. Risks include prompt injection, concealed credential exfiltration requests, malicious URLs, regex denial-of-service, supply-chain code execution in CI, and inadvertent auto-deployment of abusive rules.

Mitigations: static schema; reject multiline lexicon terms; only a small maintainer-reviewed allowlist may contain custom regex; review before merge; read-only CI permissions without secrets on untrusted PRs; no privileged `pull_request_target` workflows; SHA-pinned reviewed release to Muse; private owner preferences; no automatic community dictionary sync; no execution of or navigation to untrusted commenter content.

See `config/REPOSITORY_SECURITY_CHECKLIST.md` before going public. No user-facing database or live account access exists in this repository.
