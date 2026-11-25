---
id: DD-TC-002
title: Echelon Trust Center requirements
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [trust-center, requirements, disclosure, evidence]
---

# Echelon Trust Center requirements

Research-phase specification. Builds on `trust-center/TRUST-CENTER-RESEARCH.md`
(DD-TC-001, tiering and market practice), `architecture/EVIDENCE-ARCHITECTURE-SPECIFICATION.md`
(DD-ARC-003, evidence records) and `architecture/AUTOMATED-QUESTIONNAIRE-RESPONSE-REQUIREMENTS.md`
(DD-ARC-004). Nothing is implemented.

## 1. Purpose

Let a prospect, customer, auditor or regulator obtain current, accurate, evidence-backed
assurance information without a manual request, at the tier they are entitled to, while
never exposing exploitable security detail, other customers' information, or a claim
Echelon cannot prove.

The defining design choice: **the trust center is a projection of the canonical
knowledge base and the evidence store, not a separately authored website.** A page or
document appears only because an approved answer unit or evidence record with a
matching disclosure classification exists. This makes the trust center as honest as the
knowledge base and removes a second copy that can drift.

## 2. Information model

| Trust center object | Derived from | Rule |
|---|---|---|
| Topic page (for example "Encryption") | Answer units in the category (`answers/*.jsonl`) | Renders `customer_statement` only; statement kind shown as a visible label (Operating, Partially implemented, Planned, Not available) |
| Artifact (SOC report, pen test letter, policy, ACR) | Evidence records (`schemas/dd/evidence-record.schema.json`) of artifact type | Shown only if signature valid, not expired, not revoked, not superseded, and its disclosure class is at or below the viewer's tier |
| Assurance badge (for example "SOC 2 Type II") | Evidence record with `independence = independent-third-party` and current period | Never shown for first-party assessments; first-party reports carry "First-party assessment" label (Secure Construction Standard, assurance deliverables) |
| Subprocessor list | Vendor register (REC-ORGPOL-004) | Generated; change history retained; notification to subscribed customers on change |
| Status and incident history | Availability evidence and incident records | Public summary only; customer-specific RCAs to affected customers |
| Questionnaire library (CAIQ, SIG Lite style, HECVAT style) | AQR output over the canonical bank | Regenerated on answer change; version and date shown; original wording mapping never copies licensed text |
| Planned items | Answer units with `customer_statement_kind = planned` | Shown with target date only if the date is an approved decision; else "not yet available" |

## 3. Requirements

| ID | Requirement | Priority | Verification |
|---|---|---|---|
| TC-INF-001 | Every published statement traces to an answer unit ID and version, and every artifact to an evidence record ID and content hash. | P0 | Page source contains trace IDs; trace check in CI |
| TC-INF-002 | Publication is generated from the knowledge base and evidence store; no hand-authored claims on assurance topics. | P0 | Build reproduces the site from repository state |
| TC-HON-001 | A capability claim renders as current only when the answer unit status is `verified-operational` or `implemented-not-independently-verified` (the latter labeled "not independently verified"). | P0 | Property test over statuses (same rule as `tools/build.fsx` ASPIRATIONAL-AS-CURRENT) |
| TC-HON-002 | Independence is always labeled: first-party, independent third party, or regulatory examination. A SOC 2 attestation is never called a certification. | P0 | Content lint |
| TC-HON-003 | Empty tiers display "not yet available" rather than being hidden, so absence is visible and not inferred. | P1 | Snapshot tests |
| TC-TIER-001 | Six access tiers as in DD-TC-001: public, authenticated prospect, NDA, existing customer, auditor only, internal. Internal is never rendered. | P0 | Access control tests per tier |
| TC-TIER-002 | Gated grants are logged with identity, organization, basis (NDA ID, contract ID, audit right), scope and expiry; grants expire automatically. | P0 | Grant log inspection; expiry test |
| TC-TIER-003 | NDA tier supports clickwrap NDA acceptance with recorded version; approval may be automatic only for allowlisted domains and only for artifacts marked auto-approvable. | P1 | Workflow tests |
| TC-TIER-004 | Downloads of NDA and customer artifacts are watermarked with recipient identity and date. | P1 | Watermark presence test |
| TC-TIER-005 | Public-sector requesters receive redaction-ready versions by default (public records exposure). | P2 | Artifact variant exists |
| TC-RED-001 | Publication pipeline blocks content containing: finding-level vulnerability detail, internal hostnames, IP ranges, credentials or tokens, customer names or identifiers, personal data, and exploit steps. | P0 | Canary and pattern tests; secret scanner over generated output |
| TC-RED-002 | Pen test material is published only as an executive summary or attestation letter at NDA tier; full reports only to an existing-customer access group. | P0 | Tier assignment test |
| TC-EVD-001 | Artifacts disappear or display "expired" automatically when evidence expires, is revoked or is superseded; historical versions remain available to entitled viewers with their period clearly labeled. | P0 | Expiry and revocation fixtures |
| TC-EVD-002 | Evidence signature verification uses open standards (DSSE, ECDSA P-256 per DD-ARC-003) so viewers and auditors can verify without Echelon tooling. | P1 | Independent verification script |
| TC-SUB-001 | Subprocessor list shows name, purpose, data categories, location, and date added; customers can subscribe to change notices with the contractual notice period. | P0 before first customer | Notification test |
| TC-INC-001 | Security incident disclosures follow the incident policy: public summaries for broad-impact incidents; affected-customer RCAs only to affected customers; timelines match contractual and legal notice duties. | P1 | Tabletop exercise output |
| TC-AI-001 | Public AI use disclosure lists product features using AI, model providers (as subprocessors), data use and training commitments, and human oversight points. | P0 | Generated from AIG/AIA answer units |
| TC-A11Y-001 | The trust center itself conforms to WCAG 2.2 AA; ACRs are published for products. | P1 | Accessibility test evidence |
| TC-OPS-001 | Request intake for items not available self-service routes to AQR (DD-ARC-004) and records turnaround time. | P2 | Ledger metrics |
| TC-OPS-002 | Every page shows last-reviewed date and the date of the underlying evidence. | P1 | Snapshot test |

## 4. Build versus buy

| Option | Advantages | Disadvantages | Fit |
|---|---|---|---|
| Commercial trust center platform (SafeBase/Drata, Vanta, Conveyor, Whistic) | Mature NDA and access workflows; buyers recognize them | Recurring license; content authored inside the platform drifts from the knowledge base unless integrated; vendor sees NDA documents | Good for NDA workflow only if fed from the knowledge base by API |
| Static generated site plus small access service | Low recurring cost; single source of truth; honest by construction | Engineering and maintenance cost; NDA and access workflow must be built; less buyer familiarity | Good fit with Echelon's generated-evidence strategy once artifacts exist |
| Hybrid: generated public site; platform or simple portal for gated tiers | Balances cost and familiarity | Two systems | Recommended starting point |

Cost figures are not asserted here; see `cost-avoidance/COMPLIANCE-COST-AVOIDANCE-REPORT.md`
for sourced data and hypotheses. Recommendation: do not buy a platform before at least
one independent artifact (pen test letter or SOC report) exists; start with the public
tier generated from this repository (security overview with honest statuses,
vulnerability disclosure policy, AI use disclosure, subprocessor list).

## 5. Phasing

1. **Now (no artifacts):** public honest-status overview, VDP, AI disclosure; all
   generated. Value: deflects baseline questions; demonstrates candor.
2. **After first independent pen test and policies adopted:** NDA tier with pen test
   letter and policy set.
3. **After SOC 2 Type I or II:** SOC 2 under NDA, SOC 3 public, bridge letters.
4. **With customers:** customer tier, subprocessor notifications, incident RCAs, auditor
   tier backed by the evidence store.

## 6. Open questions

- OQ-DD-TC-001: Platform choice and whether its vendor may hold NDA artifacts.
- OQ-DD-TC-002: Does a trust center with mostly "planned" items help or hurt a
  pre-revenue vendor with DAF sponsors? (Test with two sponsor conversations; preserved
  objection from DD-TC-001.)
- OQ-DD-TC-003: Watermarking and download controls versus auditor expectations for
  unaltered reports.
