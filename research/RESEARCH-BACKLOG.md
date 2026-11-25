---
id: DD-BACKLOG-001
title: Due diligence research backlog
status: canonical
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
---

# Research backlog

States: open, in-progress, done, blocked. Update in place; history is in git.

| ID | Item | State | Notes |
|---|---|---|---|
| BL-001 | Source register for all mission frameworks with verified versions and licensing | in-progress | sources/*.jsonl |
| BL-002 | Canonical question bank, 2,000+ materially distinct questions | in-progress | questions/*.jsonl |
| BL-003 | Real-world questionnaires and named-organization expectations | in-progress | questionnaires/, industry-profiles/ |
| BL-004 | Trust center research and requirements | in-progress | trust-center/ |
| BL-005 | Scanner validation, F# coverage, pen test and external assurance economics | in-progress | scanner-validation/, external-assurance/, cost-avoidance/ |
| BL-006 | Echelon system capability verification and evidence architecture | in-progress | architecture/, gap-analysis/ |
| BL-007 | Security by construction model and CWE matrix | in-progress | security-by-construction/ |
| BL-008 | Unbound due diligence profile and requirements gap analysis | open | depends on BL-002 |
| BL-009 | Organizational policy gap analysis | open | depends on BL-002, BL-006 |
| BL-010 | Adversarial reviews from ten perspectives | open | depends on BL-002 to BL-008 |
| BL-011 | Roadmap, commercial opportunity, executive findings | open | last |
| BL-012 | Labeled benchmark of public questionnaire items for AQR matching | open | OQ-DD-AQR-001 |
| BL-013 | Second-pass diminishing-returns test: sample new public questionnaires and measure new-question yield | open | completion criterion |
| BL-014 | Healthcare industry profile (HIPAA BAA expectations) | open | lower priority; directory reserved |
| BL-015 | Fix pass from DD-VAL-ADV-002: CWE matrix rows CWE-457 (L1 contradicts own bypasses), CWE-396/252/636 (L4 rests on FS0025, which does not apply), CWE-1321 (copied bypass text), CWE-639 (intra-sponsor object access not covered by tenant isolation), CWE-89 L1 conditional on nonexistent Strata interface; scope every claim to server-side F# (exclude WebAssembly in browser); relabel "beyond scanning" as hypothesized | open | after refinement pass |
| BL-016 | Fix pass on answers: ANS-AIA-007 (cites build check as customer safeguard), ANS-TEN-004 ("eliminates" owner RLS bypass; superusers, BYPASSRLS and deploy identity remain), single-person-infeasible commitments (24x7 Sev 1 in 30 minutes, 12-month transition, funded wind-down), "no training" versus bank model validation contradiction, Folio HTML-to-PDF SSRF and file read, repository instruction files as prompt-injection path, trust center publishing planned controls as attacker signal | open | after refinement pass |
| BL-017 | AQR spec: define claim-diff mechanism; handle negated questions and picklists in the status-to-wording rule; mitigate wrong-match-to-true-answer | open | |
| BL-018 | Penetration test cost claim: ANS-PEN-002 scope likely raises first-test cost; restate DD-COST-001 savings as later-cycle hypotheses | open | |
| BL-019 | Privacy: DPA template, privacy notice, ROPA, applicable-law register incl. Indiana privacy law; government demand handling; fund-name anonymity leak; retention conflict precedence rule | open | |
| BL-020 | Owner fact verification (research/OWNER-FACT-VERIFICATION-CHECKLIST.md) | open | owner |
