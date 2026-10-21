# PCMT repository security checklist

**Recommended sequence:** prototype privately, audit the files for credential leaks, publish a reviewed public release, and only then accept public submissions. Publishing public code is not granting anyone permission to operate an Instagram/Threads account.

- [ ] Create a **private GitHub repository first**. Confirm no account secrets, personal comment archives, screenshots, or private owner configurations have been committed.
- [ ] Public repo contains **code, generic policy and reviewed lexicon only**. No OAuth secrets, Instagram/Threads access, session cookies, credentials, or social-media scraping artifacts.
- [ ] Protect `main` with required reviews, CODEOWNERS for `.github/`, `tools/`, `policy/`, and `lexicon/`, and passing checks. Enable secret scanning, Dependabot, and CodeQL where available.
- [ ] Set GitHub Actions token permissions to read-only unless a specific trusted workflow needs more. Never add secrets to public pull-request workflows.
- [ ] Do **not** run `pull_request_target` or untrusted PR code with privileged credentials. No automatic merging of proposals.
- [ ] Rejected proposals and unapproved text never appear in an exported moderation policy. A successful CI run is not semantic moderation approval.
- [ ] New arbitrary regex requires separate maintainer review, bounded complexity testing, and explicit allowlisting before being added to the build.
- [ ] Pin release versions; agent never loads arbitrary latest GitHub URLs or issue comments as its operating instructions.
- [ ] Record a SHA-256 file digest for released moderation policies, and allow rollback to prior versions.
- [ ] Keep the Lovable submissions database separate, protected by RLS and server-side rate limits; anonymous users may submit, not list/revise/approve proposals.
- [ ] Render all submission text as inert text. Do not follow commenter-submitted links or execute embedded code or instructions.
- [ ] Test prompt injection attempts in comments, contribution notes, and uploaded files. Explicitly distinguish policy/instruction sources from untrusted examples.
- [ ] Never infer sex work, identity, gender, or intent from a profile image. Solicitation moderation is behavior-based.

Public lexicons can also educate evaders about exact matches. That's an acceptable openness trade-off only if detection is layered, contextual, and monitored for evasion. You may choose to keep local, high-sensitivity rules private while contributing broad patterns to the public project.
