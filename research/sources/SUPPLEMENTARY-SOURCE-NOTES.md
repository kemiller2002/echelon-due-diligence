---
id: DD-SRC-SUP-001
title: Supplementary Source Notes and Applicability Ratings
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [due-diligence, sources, supplementary, regulatory-applicability]
---

# Supplementary Source Notes and Applicability Ratings

Companion to `sources/supplementary.jsonl` (81 records). Each fact was checked on
2026-11-25 against the issuer's own site where it could be reached, or against an
authoritative mirror (Federal Register API, govinfo, eCFR API, LII for U.S. Code text,
RFC Editor and IETF Datatracker APIs). Where the issuer blocked scripted access and no
mirror confirmed the facts, the record has `verification.verified: false`, `unknown`
values and an explanation in `notes`. This note does not restate requirement text and is
not legal advice.

## 1. Rating scale

- **Binds Echelon directly**: the source applies to Echelon Foundry by its own terms, or
  is a vendor statement about Echelon's own platform that has the same practical effect
  (for example an end-of-support date). Voluntary standards that Echelon would adopt as
  its own practice are also listed here, marked "(voluntary)".
- **Flows down from customers**: binds DAF sponsors (or their auditors) and reaches
  Unbound as product, reporting or contract requirements.
- **Only for certain customer types**: becomes relevant only if Unbound serves a
  particular sponsor type (bank-affiliated, insurer-affiliated, public-entity,
  public-company parent, platform-style fundraising, federal award recipient).
- **Not applicable**: does not reach Echelon or Unbound on current facts; kept because
  questionnaires cite it or as background.

Confidence: **High** means verified at the issuer or an official mirror;
**Medium** means partially verified or the applicability reasoning depends on
unsettled facts; **Low** means not verified at the issuer.

## 2. Register

### 2.1 Vulnerability disclosure, patching, logging, incident response

| ID | Rating | Confidence |
|---|---|---|
| SRC-RFC-9116 | Binds Echelon directly (voluntary) | High |
| SRC-NIST-SP800-40-R4 | Binds Echelon directly (voluntary) | High |
| SRC-NIST-SP800-92 | Binds Echelon directly (voluntary) | High |
| SRC-NIST-SP800-86 | Binds Echelon directly (voluntary) | High |
| SRC-NIST-SP800-216 | Binds Echelon directly (voluntary) | High |
| SRC-CISA-BOD-20-01 | Not applicable (federal agencies only; model VDP) | High |
| SRC-CISA-SSVC | Binds Echelon directly (voluntary) | High |
| SRC-CISA-STOPRANSOMWARE-GUIDE | Binds Echelon directly (voluntary) | High |
| SRC-OFAC-RANSOMWARE-ADVISORY-2021 | Binds Echelon directly (OFAC applies to all U.S. persons) | High |
| SRC-OMB-M-21-31 | Not applicable (federal; rescinded) | High |
| SRC-CIRCIA | Only for certain customer types (future covered entities) | Medium |
| SRC-NAIC-DATA-SECURITY-MODEL-LAW | Not applicable unless an insurer-affiliated sponsor | High |
| SRC-GLBA-RESPONSE-PROGRAM-GUIDANCE | Only for certain customer types (bank or bank trust sponsors) | High |

### 2.2 Software supply chain and web/API security

| ID | Rating | Confidence |
|---|---|---|
| SRC-SIGSTORE | Binds Echelon directly (voluntary) | High |
| SRC-IN-TOTO | Binds Echelon directly (voluntary) | High (dates unknown) |
| SRC-GITHUB-ARTIFACT-ATTESTATIONS | Binds Echelon directly (voluntary) | High |
| SRC-NUGET-PACKAGE-SIGNING | Binds Echelon directly (voluntary) | Medium (page last updated 2021) |
| SRC-NPM-PROVENANCE | Binds Echelon directly (voluntary) | High |
| SRC-W3C-CSP | Binds Echelon directly (voluntary) | High |
| SRC-WHATWG-POSTMESSAGE | Binds Echelon directly (voluntary) | High |
| SRC-RFC-9700 | Binds Echelon directly (voluntary) | High |
| SRC-RFC-9421 | Binds Echelon directly (voluntary) | High |
| SRC-IETF-IDEMPOTENCY-KEY-DRAFT | Binds Echelon directly (voluntary; draft only) | High |
| SRC-STANDARD-WEBHOOKS | Binds Echelon directly (voluntary) | High |
| SRC-OPENCHAIN-ISO-5230 | Binds Echelon directly (voluntary) | Medium (ISO page blocked) |
| SRC-SPDX-LICENSE-LIST | Binds Echelon directly (voluntary) | High |
| SRC-CISA-MEMORY-SAFETY-ROADMAP | Binds Echelon directly (voluntary) | High |
| SRC-MS-BINARYFORMATTER-GUIDANCE | Binds Echelon directly (platform vendor statement) | High |
| SRC-DOTNET-SUPPORT-POLICY | Binds Echelon directly | High |
| SRC-POSTGRESQL-VERSIONING-POLICY | Binds Echelon directly (if PostgreSQL is used) | High |

### 2.3 Cryptography

| ID | Rating | Confidence |
|---|---|---|
| SRC-FIPS-140-3-CMVP | Only for certain customer types (federal or FIPS-requiring sponsors) | High |
| SRC-NIST-SP800-57 | Binds Echelon directly (voluntary) | High |
| SRC-NIST-SP800-52 | Binds Echelon directly (voluntary) | High |
| SRC-NIST-SP800-131A | Binds Echelon directly (voluntary) | High |
| SRC-NIST-FIPS-203-204-205 | Binds Echelon directly (voluntary planning input) | High |
| SRC-NIST-IR-8547 | Binds Echelon directly (voluntary planning input) | High |
| SRC-NSA-CNSA-2.0 | Not applicable (national security systems) | Low (issuer blocked) |

### 2.4 Accessibility, privacy, children, bankruptcy, data transfer

| ID | Rating | Confidence |
|---|---|---|
| SRC-ISO-14289-PDFUA | Flows down from customers (if Unbound produces PDFs) | Low (issuer blocked) |
| SRC-MATTERHORN-PROTOCOL | Flows down from customers | Low (issuer blocked) |
| SRC-DOJ-ADA-TITLE-II-RULE-2024 | Only for certain customer types (public entities) | High |
| SRC-COPPA | Binds Echelon directly only if minors use Unbound | High |
| SRC-USC-11-365N | Binds Echelon directly (bankruptcy of licensor) | High |
| SRC-DOJ-28CFR202-BULK-DATA | Binds Echelon directly | High |
| SRC-CO-PRIVACY-ACT | Flows down from customers | Medium (AG page blocked; nonprofit coverage unverified) |
| SRC-OR-CPA | Flows down from customers | High |

### 2.5 Tax, charitable substantiation and exempt organization reporting

| ID | Rating | Confidence |
|---|---|---|
| SRC-IRC-6001 | Binds Echelon directly and flows down from customers | High |
| SRC-IRC-6104 | Flows down from customers | High |
| SRC-IRS-1099-INSTRUCTIONS | Flows down from customers (and binds Echelon for its own vendors) | High |
| SRC-IRS-FORM-8283-8282 | Flows down from customers | High |
| SRC-TREAS-REG-1.170A-13 | Flows down from customers | High |
| SRC-IRS-PUB-561 | Flows down from customers | High |
| SRC-IRS-DIGITAL-ASSET-GUIDANCE | Flows down from customers | High |
| SRC-IRS-NOTICE-2017-73 | Flows down from customers | High |
| SRC-IRC-4943 | Flows down from customers | High |
| SRC-IRC-6115 | Flows down from customers | High |
| SRC-TREAS-REG-53.4945-5 | Flows down from customers | High |
| SRC-IRS-FORM-4720 | Flows down from customers | High |
| SRC-IRS-FORM-990-SCHEDULES | Flows down from customers | High |
| SRC-IRS-FORM-990-T | Flows down from customers (complex-asset sponsors) | High |

### 2.6 Investment, accounting, audit and performance

| ID | Rating | Confidence |
|---|---|---|
| SRC-FASB-ASC-820 | Flows down from customers | Low (issuer blocked) |
| SRC-ICA-3C10 | Flows down from customers (sponsors with charitable pools) | High |
| SRC-SEC-CUSTODY-RULE | Only for certain customer types (adviser affiliates) | High |
| SRC-CFA-GIPS | Only for certain customer types (GIPS-claiming managers) | High |
| SRC-AICPA-SOC1-GUIDE | Flows down from customers | High |
| SRC-PCAOB-AS-2201 | Only for certain customer types (public-company parents) | Low (issuer blocked) |
| SRC-AICPA-NFP-AAG | Flows down from customers | High |
| SRC-2CFR200-303 | Only for certain customer types (federal award recipients) | High |

### 2.7 Communications and charitable solicitation

| ID | Rating | Confidence |
|---|---|---|
| SRC-CAN-SPAM | Binds Echelon directly | High |
| SRC-TCPA | Binds Echelon directly (if Unbound sends SMS or automated calls) | High |
| SRC-CA-GOV-CODE-12599.9 | Only for certain customer types (platform-style sponsors; possibly Unbound) | Medium (statute text blocked) |
| SRC-HI-HRS-467B | Only for certain customer types (platform-style sponsors) | High |

### 2.8 Payments and bank reporting

| ID | Rating | Confidence |
|---|---|---|
| SRC-REG-E | Not applicable (in most flows) | High |
| SRC-UCC-3-4 | Flows down from customers (check-paying sponsors) | High |
| SRC-REG-CC | Not applicable (bank-facing background) | High |
| SRC-REG-J-FEDWIRE-OC6 | Not applicable (bank-facing; informs wire data design) | High |
| SRC-NACHA-TPSP-AUDIT-GUIDANCE | Binds Echelon directly once Unbound performs ACH functions (scope open) | Medium |
| SRC-FINCEN-CHECK-FRAUD-ALERT-2023 | Flows down from customers | High |
| SRC-FBI-IC3-REPORT | Binds Echelon directly (threat context only) | High |
| SRC-ISO-20022 | Flows down from customers | Low (issuer unreachable) |
| SRC-BAI2-BTRS | Flows down from customers | High |
| SRC-X9-POSITIVE-PAY | Flows down from customers (no X9 standard found) | Low (recorded as unknown) |

## 3. Status surprises

1. **.NET 8 and .NET 9 reached end of support on November 10, 2026**, fifteen days
   before this check (last patches 8.0.34 and 9.0.23). Any Echelon system still on either
   runtime is unsupported. .NET 10 (LTS) and .NET 11 (STS, released November 10, 2026)
   both end support on November 14, 2028.
2. **PostgreSQL 14 reached end of life on November 12, 2026**, and PostgreSQL 19 was
   released November 19, 2026.
3. **OMB M-21-31 was rescinded** by OMB M-26-14 on May 22, 2026. Questionnaires citing
   EL0 to EL3 logging tiers cite a withdrawn federal baseline.
4. **NIST IR 8547 was finalized in October 2026.** Quantum-vulnerable public-key
   algorithms are deprecated after 2030 and disallowed under NIST standards after 2035.
   The final cites OMB M-26-15, including federal TLS 1.3 support by January 2, 2030.
5. **FIPS 140-2 sunset passed.** CMVP allowed FIPS 140-2 modules for new systems only
   until September 21, 2026; those certificates move to the Historical List.
6. **Pending NIST revisions remain drafts:** SP 800-92 Rev. 1 (draft since October
   2023), SP 800-131A Rev. 3 (draft since October 2024) and SP 800-57 Part 1 Rev. 6
   (draft since December 2025). Cite the finals.
7. **CIRCIA final rule still not published.** CISA cites funding lapses and held extra
   town halls in June 2026. No reporting duty is in force.
8. **DOJ ADA Title II compliance dates extended by one year** (interim final rule,
   April 20, 2026): April 26, 2027 for large public entities and April 26, 2028 for small
   ones and special districts.
9. **SEC custody rule is being rewritten.** The 2023 Safeguarding proposal was withdrawn
   in 2025, and a new proposal (Adviser and Regulated Fund Custody Rules; Crypto Custody
   Rules) was published October 6, 2026 with comments due December 7, 2026.
10. **FCC TCPA consent-revocation changes take effect November 25, 2026** (today),
    including an exclusive revocation method and a revised financial institution
    fraud-alert exemption.
11. **Hawaii added charitable fundraising platform and platform charity rules effective
    July 1, 2026** (L 2025, c 108). The definition excludes vendors that solely provide
    technical services, which is the position Unbound should document. California's
    AB 488 regime (Gov. Code 12599.9) has applied since January 1, 2023, with regulations
    effective March 26, 2024.
12. **CSP Level 3 is still a W3C Working Draft** (latest October 27, 2026); CSP Level 2
    (2016) remains the latest Recommendation.
13. **The IETF Idempotency-Key header is still an Internet-Draft** after five years
    (revision 09, November 21, 2026). Do not cite it as a standard.
14. **Standard Webhooks** remains version 1.0.0 but now deprecates the `v1a` asymmetric
    signature in favor of `v2a`.
15. **Treas. Reg. 1.170A-13 is not where current appraisal rules live.** Qualified
    appraisal and noncash substantiation rules for contributions after July 30, 2018 are
    in 1.170A-16 and 1.170A-17; the record covers all three.
16. **Nacha TPSP audit scope is narrower than often assumed.** Nacha describes the TPSP
    annual Rules Compliance Audit as covering functions performed on behalf of a
    participating DFI or Third-Party Sender. Whether Unbound, acting for the sponsor as
    Originator, is in scope by rule or only by ODFI contract is an open question.
17. **No public ASC X9 positive pay issue file standard was found.** Banks define their
    own layouts; Unbound needs configurable exports.
18. **Outside this file:** CISA's directives index shows BOD 26-04 revoked BOD 19-02
    and BOD 22-01. This affects `SRC-CISA-BOD-22-01` in another register file.

## 4. Verification gaps

Eight records are unverified (`verified: false`) because issuer sites blocked scripted
access or no source exists: SRC-NSA-CNSA-2.0, SRC-ISO-14289-PDFUA,
SRC-MATTERHORN-PROTOCOL, SRC-CO-PRIVACY-ACT (partially verified), SRC-FASB-ASC-820,
SRC-PCAOB-AS-2201, SRC-ISO-20022 and SRC-X9-POSITIVE-PAY. A human with a browser should
confirm editions and URLs for these before they are cited to a customer.

Several verified records carry individual facts from general knowledge or search
results; each such fact is labeled in the record's `limitations` or `notes` (for
example the TCPA 1991 enactment, the Form 990 Schedule I $5,000 threshold, the Form 8282
three-year rule, CIRCIA's U.S. Code citation and the FIPS 140-3 effective date, which
was left out of the record).

eCFR human-readable pages redirected scripted requests to a bot check, so eCFR-based
records use the verified eCFR API URL as `url`, matching existing register practice.

## 5. ID mapping

All 81 requested IDs were used unchanged. Two records cover more than their ID suggests:
`SRC-TREAS-REG-1.170A-13` also covers 1.170A-16 and 1.170A-17, and `SRC-ICA-3C10` covers
Investment Company Act sections 3(c)(10) and 7(e). The Form 990 request was split into
`SRC-IRS-FORM-990-SCHEDULES` (Schedules I, F and L) and `SRC-IRS-FORM-990-T`.
