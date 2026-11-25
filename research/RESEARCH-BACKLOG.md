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
| BL-008 | Unbound due diligence profile and requirements gap analysis | done | DD-PRD-UNB-001, DD-GAP-UNB-001, 104 proposed requirements |
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
| BL-021 | Fix pass from DD-VAL-ADV-001: plan independent evidence for payment, reconciliation, grant, fee and sanctions answers; give requires-external-validation answers non-first-party evidence (TEN-005, AML-006, DAF-010, AIG-007, WLB-002); mark all challenge acceptance ratings as unvalidated agent judgment; name second-person roles or state compensating controls for two-person controls; reconcile ANS-HR-006 versus ANS-ISP-007, LEG-003 versus IR-004 notification triggers, PAY-008 versus RCN-004; resolve SOC 2 versus SOC 1 timeline and add SOC 1 to external assurance matrix and cost report; remove "auditor acceptance" preconditions (FCT-007, PAY-008); fix evidence verification V-11 independence definition; restrict SOC 1 to customer tier in trust center; add CEO/CIO fallback to bank incident notice | open | after refinement pass |
| BL-022 | Missing questions from DD-VAL-ADV-001: operating history and references; incumbent conversion and parallel run; pricing; excise tax liability allocation for platform defects (4966/4967/4958); implementation plan; threat intelligence sharing; AI processing of customers' confidential questionnaires; OCC 12 CFR Part 9 for bank-trusteed funds; continuity in bank resolution; UDAP in donor-facing pages; Pub. L. 119-21 non-itemizer deduction exclusion | open | |
| BL-023 | Counsel reverification before customer use: 2026 interagency TPRM proposal (91 FR 58536), NYDFS October 2025 TPSP letter, Nacha 2026 rule details | open | counsel |
| BL-024 | Citation hygiene from DD-GAP-UNB-001: 457 questions cite 59 superseded Unbound records without the governing CNV clause (worst: UNB-TEN-008 without CNV-TEN-001, 40 times); 256 cite Deferred-scope requirements without saying so; 16 cite UNB-CTRL/UNB-SCTRL control IDs as requirements | open | after fix pass |
| BL-025 | Add questions on scheduled contributions (no bank question and no Unbound requirement) | open | |
