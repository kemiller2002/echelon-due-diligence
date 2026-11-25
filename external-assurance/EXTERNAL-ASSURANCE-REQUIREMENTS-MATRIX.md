---
id: DD-EXT-001
title: External assurance requirements matrix
status: draft
version: 0.2.0
created: 2026-11-25
updated: 2026-11-25
tags: [due-diligence, external-assurance, penetration-testing, soc2, iso27001, pci, cost]
related_documents:
  - external-assurance/external-assurance-matrix.csv
  - scanner-validation/SCANNER-VALIDATION-RESEARCH-REPORT.md
  - cost-avoidance/PENETRATION-TESTING-COST-REDUCTION-STRATEGY.md
  - cost-avoidance/COMPLIANCE-COST-AVOIDANCE-REPORT.md
  - sources/assurance-testing.jsonl
---

# External assurance requirements matrix

## Purpose and status

This matrix records, for each external assurance or advisory activity Echelon Foundry
might buy, why it is bought, whether anything actually requires it, whether it must be
independent, what qualification or accreditation applies, whether internal work can
satisfy it, and what it costs according to credible public sources. The machine-readable
form is `external-assurance/external-assurance-matrix.csv` (one row per activity, same
fields). Source records are in `sources/assurance-testing.jsonl`.

Current state (from `architecture/ECHELON-CURRENT-STATE-BRIEF.md`): Echelon has no
production Unbound deployment, no SOC 2 report, no ISO certificate and no external
penetration test. Nothing in this matrix describes an implemented Echelon capability.

## How to read the cost column

Credible, non-marketing public price data for assurance engagements is scarce. This
matrix uses three kinds of figures and labels each:

1. **Government rate data.** GSA CALC+ ceiling hourly rates for federal Multiple Award
   Schedule labor categories, queried 2026-11-25 (`SRC-GSA-CALC`). These are maximum
   hourly prices in federal contracts, not commercial quotes, and they price labor
   hours, not engagements. Percentiles were computed over labor categories whose names
   contain the stated keyword.
2. **Vendor marketing.** Figures published by sellers of compliance automation or
   testing services (`SRC-VENDOR-*`). They are labeled VENDOR MARKETING, have no
   disclosed methodology, and are shown only because nothing better was found.
3. **Unknown.** Where no credible public figure was found, the cell says so.

For internal labor, the BLS median annual wage for information security analysts was
$129,180 in May 2025 (`SRC-BLS-INFOSEC`); dividing by 2,080 hours gives about $62 per
hour before benefits and overhead (arithmetic, not a BLS figure). GAO found FedRAMP
authorization cost estimates "ranged anywhere from tens of thousands to millions of
dollars" (`SRC-GAO-24-106591`), which illustrates how widely mandated third-party
assessment costs vary.

## Summary

| ID | Activity | Required by law or contract? | Independence required? | Internal work can satisfy? | Cost evidence |
|---|---|---|---|---|---|
| EXT-01 | Independent penetration test | Only via PCI (if in scope), FedRAMP (if pursued), DORA TLPT (EU financial entities), or contract | PCI: organizational independence, internal allowed; FedRAMP: 3PAO; customers: usually third party | Partly; first-party only | GSA hourly; vendor marketing |
| EXT-02 | Vulnerability scanning (internal, non-ASV) | PCI 11.3.1 if in scope | Reasonable independence of internal staff (PCI) | Yes | GSA hourly |
| EXT-03 | PCI ASV external scan | PCI 11.3.2 if in scope | Must be an ASV | No | Unknown |
| EXT-04 | SOC 2 readiness | No | No | Yes | Vendor marketing |
| EXT-05 | SOC 2 Type I | Contract and market | Independent CPA | No | Vendor marketing |
| EXT-06 | SOC 2 Type II | Contract and market | Independent CPA | No | Vendor marketing |
| EXT-07 | ISO/IEC 27001 certification | Contract and market | Accredited certification body | No | Vendor marketing |
| EXT-08 | Privacy consulting | No purchase mandate | No | Yes, except legal opinions | GSA hourly |
| EXT-09 | Regulatory consulting | No purchase mandate | No | Research yes, legal conclusions no | Unknown |
| EXT-10 | Policy development | No | No | Yes | GSA hourly |
| EXT-11 | Vendor risk assessments | Contractual at most | No | Yes | GSA hourly |
| EXT-12 | Business continuity assessment | Not established | No | Yes | GSA hourly |
| EXT-13 | Accessibility audit | Legal applicability not established | Not required by sources reviewed | Yes, with limits | GSA hourly |
| EXT-14 | AI governance assessment | Not established | Only for certification | Yes for self-assessment | GSA hourly |
| EXT-15 | Compliance monitoring platform | No | No | Yes in principle | Unknown |
| EXT-16 | Evidence collection | No | No | Yes | Unknown |
| EXT-17 | Questionnaire completion | No | No | Yes | Unknown |
| EXT-18 | SOC 1 Type 1 | Contract and user-auditor reliance; no statute | Independent CPA (AT-C 320) | No | Unknown |
| EXT-19 | SOC 1 Type 2 | Contract and user-auditor reliance; no statute | Independent CPA (AT-C 320) | No | Unknown |

## Key findings

1. **Only three items on the list are ones that internal work can never replace:**
   SOC 2 examinations (independent CPA under AICPA attestation standards), ISO/IEC 27001
   certification (accredited certification body under ISO/IEC 17021-1 and 27006-1), and
   PCI ASV scans when PCI applies (PCI DSS 11.3.2; `SRC-PCI-ASV-PROGRAM`). FedRAMP
   penetration tests (3PAO, `SRC-FEDRAMP-PENTEST-GUIDANCE` section 8.0) and DORA TLPT for
   identified EU financial entities (Regulation (EU) 2022/2554 Articles 26 and 27) add
   similar requirements, but only for those markets.
2. **Penetration testing independence is defined more narrowly than many buyers
   assume.** PCI DSS v4.0 requirements 11.4.2, 11.4.3 and 11.4.5 allow "a qualified
   internal resource or qualified external third party" provided organizational
   independence exists, and say the tester does not need to be a QSA or ASV
   (`SRC-PCI-DSS-V4-SAQ-D`). The PCI guidance defines independence as organizational
   separation from management of the target systems (`SRC-PCI-PENTEST-GUIDANCE`). For a
   very small organization, where the same people build and operate Unbound, that
   separation is hard to demonstrate. Customers, insurers and SOC 2 auditors commonly
   expect a third-party test. That expectation is market practice, not a rule, and it has
   not been measured for Echelon's buyers.
3. **No certification is mandated for penetration testers under PCI.** The PCI guidance
   lists OSCP, CEH, GPEN, GWAPT, GXPN, CREST and CHECK as examples, says PCI SSC "does not
   validate or endorse these certifications", and says experience cannot be shown by
   certifications alone. FedRAMP requires the team lead to hold an industry-recognized
   penetration testing credential. CREST company accreditation and individual
   certification (CPSA, CRT, CCT) are separate things (search excerpts of CREST pages
   only; `SRC-CREST` is not fully verified).
4. **SOC 2 does not mandate penetration testing.** A CPA author writing for CSA states
   there are no explicit requirements for penetration testing in SOC 2, while CC4.1
   (monitoring activities) and CC7.1 (detection of vulnerabilities) are commonly
   supported by it (`SRC-CSA-SOC2-PENTEST`; the article is sponsored by a testing firm).
   The AICPA points-of-focus text itself could not be retrieved in this session.
5. **Independent review of internally generated evidence suffices** where the assurance
   provider tests the evidence (SOC 2 and ISO audits do this by design), where the
   requirement permits qualified internal resources with organizational independence
   (PCI internal scans and pen tests), and where a customer agrees in writing. **It does
   not suffice** where a named qualified body must perform the work itself: ASV scans,
   FedRAMP 3PAO testing, DORA TLPT external tester rotation, accredited ISO certification,
   CPA attestation.
6. **Cost data is weak.** No credible independent public price source was found for SOC 2
   or ISO/IEC 27001 audits, ASV scans or compliance platforms. All savings claims built on
   these numbers must be treated as hypotheses (see DD-COST-002).

## When internal penetration testing is permissible

| Context | Internal permissible? | Condition | Source |
|---|---|---|---|
| PCI DSS v4.0 11.4.2, 11.4.3, 11.4.5 | Yes | Qualified, organizationally independent of the tested systems' management; not required to be QSA or ASV | `SRC-PCI-DSS-V4-SAQ-D`, `SRC-PCI-PENTEST-GUIDANCE` |
| PCI DSS 11.3.2 external scans | No | ASV only | `SRC-PCI-ASV-PROGRAM` |
| FedRAMP | No (for JAB P-ATO) | Recognized 3PAO; agency ATO may use AO-designated assessor | `SRC-FEDRAMP-PENTEST-GUIDANCE` |
| DORA TLPT | Restricted | Competent authority approval, conflict controls, external threat intelligence provider, external testers every three tests; significant credit institutions external only | `SRC-TIBER-EU` |
| UK public sector and CNI | Scheme based | CHECK companies developed for this purpose; mandate not confirmed | `SRC-NCSC-CHECK` |
| SOC 2 | No rule either way | Auditor judgment; customers often expect third party | `SRC-CSA-SOC2-PENTEST` |
| Customer contract or insurer | Per contract | Read the clause; obtain written acceptance for any internal substitute | Secure Construction Standard, External assurance section |

## Individual and firm qualifications

| Credential | Type | Verified facts | Source |
|---|---|---|---|
| OSCP / OSCP+ | Individual | 24-hour proctored practical exam; OSCP does not expire; OSCP+ expires after three years | `SRC-OFFSEC-CERTS` |
| GPEN | Individual | Proctored, 82 questions, three hours, 73% pass; renewal via CPE | `SRC-GIAC-CERTS` |
| GWAPT | Individual | Listed in PCI guidance as example; page not analyzed | `SRC-GIAC-CERTS` |
| CREST CPSA, CRT, CCT INF/APP | Individual | CRT requires CPSA (search excerpt, not verified) | `SRC-CREST` |
| CREST accredited member company | Firm | Company accreditation separate from staff certification (search excerpt, not verified) | `SRC-CREST` |
| CHECK company | Firm (UK) | NCSC-assured companies for public sector and CNI testing | `SRC-NCSC-CHECK` |
| FedRAMP 3PAO | Firm | Recognized 3PAO; team lead credential | `SRC-FEDRAMP-PENTEST-GUIDANCE` |
| PCI ASV | Firm plus employees | Qualified by PCI SSC; employees re-certify every 12 months | `SRC-PCI-ASV-PROGRAM` |
| CPA firm (SOC) | Firm | Licensed CPA; AICPA peer review for accounting and auditing practices | `SRC-AICPA-SOC2`, `SRC-AICPA-PEER-REVIEW` |
| ISO/IEC 27001 certification body | Firm | Accredited to ISO/IEC 17021-1 with 27006-1 | `SRC-ISO-17021-1`, `SRC-ISO-27006` |
| CISSP, CSSLP, CISA, CISM | Individual | Management, secure development and audit credentials, not pen test qualifications | `SRC-ISC2-CERTS`, `SRC-ISACA-CERTS` |

## Detailed matrix

### EXT-01 Independent penetration testing (application, API, external network)

- **Why purchased:** Customer due diligence and contracts; SOC 2 auditors commonly look for it as evidence under CC4.1 and CC7.1 though SOC 2 does not mandate it; insurer applications; PCI DSS 11.4 if in scope; the Secure Construction Standard plans an external test for Unbound.
- **Legally required:** Not required by any statute located for a US DAF administration SaaS. Required by PCI DSS 11.4.2/11.4.3 if Echelon is in PCI scope (not established); by FedRAMP if pursued; DORA Art. 26 TLPT binds only identified EU financial entities and their in-scope ICT providers.
- **Independence required:** PCI: organizational independence of the tester, internal resource allowed, QSA or ASV not required. FedRAMP: recognized 3PAO for JAB P-ATO; agency AO designee otherwise. DORA TLPT: internal testers only with competent authority approval, external threat intelligence and external testers every three tests. Customers: independence expectation is market practice, not verified quantitatively.
- **Qualifications or accreditation:** PCI: 'qualified' with no mandated certification; PCI guidance lists OSCP, CEH, GPEN, GWAPT, GXPN, CREST and CHECK as non-required examples and says certifications alone are insufficient. FedRAMP: team lead must hold an industry-recognized pen test credential. UK schemes: CHECK (NCSC) and CREST (CBEST). DORA Art. 27: certified by an accreditation body or adherence to codes of conduct, professional indemnity insurance.
- **Internal work can satisfy:** Partly. Internal testing is permissible under PCI only with organizational independence from management of the target, which a very small organization may be unable to demonstrate. Internal testing is first-party evidence and cannot be labeled independent. It cannot satisfy FedRAMP or customer contracts that name third-party testing.
- **Open source substitutes:** ZAP, Nuclei, Schemathesis, garak, PyRIT support testing but do not substitute for a human-led test of authorization and financial business logic.
- **Scope reduction:** Small attack surface by construction (Limen boundary, single data access path, no user HTML), threat models, test accounts, architecture and data flow documentation, prior automated scan results and fixed known issues let testers spend hours on authorization, tenant isolation and money movement. See DD-COST-001.
- **Evidence sharing across products:** Shared platform components can be tested once per version and referenced by later product tests if the build and configuration are identical and the report scope says so; product-specific surfaces still need testing.
- **Continuous performance:** Post-launch: internal continuous DAST and API fuzzing, plus a vulnerability disclosure policy or bug bounty; retest after significant change (PCI language) or major releases.
- **Typical cost range:** Hourly labor reference only: labor categories containing 'penetration' n=445, p25 $125.86, median $157.03, p75 $196.59 per hour (GSA CALC+ federal MAS ceiling hourly rates, snapshot 2026-11-25 (SRC-GSA-CALC); ceiling rates, not commercial engagement quotes). Vendor marketing (Software Secured): $5,000 to $100,000 or more per test; human-led authenticated web plus external network $15,000 to $50,000.
- **Cost source type:** government rate data; vendor marketing
- **Cost sources:** SRC-GSA-CALC; SRC-VENDOR-SOFTWARESECURED-PENTEST-COST
- **Substitution risks:** Replacing with internal or automated testing would misstate assurance, miss business logic and authorization flaws, and likely fail customer and insurer requirements.
- **Likely customer acceptance:** Independent third-party report or attestation letter: high (expected). Internal report: low for financial-sector buyers (assumption; to be measured).
- **Total cost of ownership:** External fee plus internal preparation (environment, accounts, documentation), coordination during test, remediation engineering, retest fee, and report handling under NDA. Repeats at least annually and after significant change.

### EXT-02 Vulnerability scanning (internal and non-ASV external)

- **Why purchased:** Continuous hygiene; SOC 2 CC7.1 evidence; customer questionnaires; PCI DSS 11.3.1 internal scans if in scope.
- **Legally required:** No statute located. PCI DSS 11.3.1 if in scope.
- **Independence required:** PCI: internal scans may be performed by qualified internal staff reasonably independent of the system scanned; QSA or ASV not required.
- **Qualifications or accreditation:** None mandated beyond 'qualified'.
- **Internal work can satisfy:** Yes, for non-PCI purposes and for PCI internal scans with reasonable independence.
- **Open source substitutes:** Trivy, Grype, OSV-Scanner, Nuclei, ZAP baseline, Checkov; OpenSSF Scorecard for repository hygiene.
- **Scope reduction:** Immutable images, minimal base images, locked dependencies and few exposed services reduce findings volume.
- **Evidence sharing across products:** High: one pipeline and SARIF normalization serve every Echelon repository.
- **Continuous performance:** Yes: per commit, per image build and scheduled rescans for new advisories.
- **Typical cost range:** Hourly labor reference only: labor categories containing 'vulnerab' n=176, p25 $101.35, median $133.3, p75 $182.43 per hour (GSA CALC+ federal MAS ceiling hourly rates, snapshot 2026-11-25 (SRC-GSA-CALC); ceiling rates, not commercial engagement quotes). Commercial scanner license prices: unknown (not public in sources reviewed).
- **Cost source type:** government rate data; license prices unknown
- **Cost sources:** SRC-GSA-CALC
- **Substitution risks:** Open-source data feeds and rules may lag; false negatives on F# code paths are not addressed by these tools; triage burden.
- **Likely customer acceptance:** High for internal scanning as an operating control when evidence is current and reviewed (assumption).
- **Total cost of ownership:** No license fee for open-source tools; engineering time to integrate, tune, triage and maintain; CI compute.

### EXT-03 PCI ASV external vulnerability scan

- **Why purchased:** PCI DSS 11.3.2 for in-scope internet-facing systems.
- **Legally required:** Contractually required under PCI DSS when in scope; Echelon PCI scope not established.
- **Independence required:** Must be performed by a PCI SSC Approved Scanning Vendor using its approved scan solution.
- **Qualifications or accreditation:** ASV company qualified by PCI SSC; ASV employees re-certify every 12 months.
- **Internal work can satisfy:** No. Internal or open-source scans cannot replace ASV scans.
- **Open source substitutes:** None acceptable for 11.3.2; internal scans can pre-check before the ASV run.
- **Scope reduction:** Keep cardholder data out of Echelon systems (for example hosted payment pages by a processor) to shrink or remove PCI scope; applicability must be decided with the acquirer or QSA.
- **Evidence sharing across products:** Possible across products sharing the same in-scope external IPs.
- **Continuous performance:** At least once every three months and after significant change, with rescans.
- **Typical cost range:** Unknown: no ASV price found in credible public sources.
- **Cost source type:** unknown
- **Cost sources:** SRC-PCI-ASV-PROGRAM; SRC-PCI-DSS-V4-SAQ-D
- **Substitution risks:** Non-compliance with PCI DSS if substituted.
- **Likely customer acceptance:** Required where applicable; irrelevant otherwise.
- **Total cost of ownership:** Vendor fee plus remediation and dispute handling each quarter.

### EXT-04 SOC 2 readiness assessment

- **Why purchased:** Identify control gaps before an examination; often bundled by auditors or compliance platforms.
- **Legally required:** No.
- **Independence required:** No for the readiness work itself. Whether a CPA firm that performs readiness can later perform the examination depends on AICPA independence rules (not reviewed in this session: unknown).
- **Qualifications or accreditation:** None required.
- **Internal work can satisfy:** Yes. Unbound's 89-control matrix and SOC2-001..032 directive are already a readiness design, though all controls are status Designed.
- **Open source substitutes:** This repository's controls, evidence requirements and answer units; Praxis and Tutela evidence.
- **Scope reduction:** Narrow system description and boundaries; inherit controls from cloud providers via their SOC reports (complementary subservice organization controls).
- **Evidence sharing across products:** High if Echelon runs one shared control environment for all products.
- **Continuous performance:** Yes, as continuous control monitoring.
- **Typical cost range:** Vendor marketing (Vanta): readiness 'starts around $10,000'.
- **Cost source type:** vendor marketing
- **Cost sources:** SRC-VENDOR-VANTA-SOC2-COST
- **Substitution risks:** Self-assessment blind spots; misreading criteria.
- **Likely customer acceptance:** Customers do not accept readiness as assurance.
- **Total cost of ownership:** Mostly internal time; optional external fee.

### EXT-05 SOC 2 Type I examination

- **Why purchased:** Customer and partner requirement for service organization assurance on control design at a point in time.
- **Legally required:** No statute; contractual and market driven.
- **Independence required:** Yes. Attestation examination by an independent CPA under AICPA attestation standards (AT-C 205).
- **Qualifications or accreditation:** Licensed CPA firm; AICPA peer review applies to firms performing accounting and auditing work.
- **Internal work can satisfy:** No. Internal evidence can only feed the examination.
- **Open source substitutes:** None.
- **Scope reduction:** System boundary design, carve-out of subservice organizations, fewer in-scope systems, automated evidence.
- **Evidence sharing across products:** One report can cover several products if described in one system description (auditor decision).
- **Continuous performance:** Point in time; usually a step toward Type II.
- **Typical cost range:** Vendor marketing (Vanta): SOC 2 audit fee 'usually runs between $10,000 and $50,000' (not split by type). No credible independent public source found.
- **Cost source type:** vendor marketing
- **Cost sources:** SRC-VENDOR-VANTA-SOC2-COST; SRC-AICPA-SOC2
- **Substitution risks:** Any internal 'SOC 2-aligned' report risks being read as attestation; must be labeled first-party.
- **Likely customer acceptance:** Accepted as interim; many financial buyers ask for Type II (assumption).
- **Total cost of ownership:** Auditor fee, internal preparation, management assertion and representation letter, remediation.

### EXT-06 SOC 2 Type II examination

- **Why purchased:** Customer requirement for assurance that controls operated effectively over a period.
- **Legally required:** No statute; contractual and market driven.
- **Independence required:** Yes, independent CPA.
- **Qualifications or accreditation:** Licensed CPA firm; peer review.
- **Internal work can satisfy:** No.
- **Open source substitutes:** None.
- **Scope reduction:** As Type I; continuous automated evidence reduces sample pulls and auditor time (hypothesis).
- **Evidence sharing across products:** High with shared control environment.
- **Continuous performance:** Annual recurring period.
- **Typical cost range:** Vendor marketing (Vanta) only, as for Type I; page states Type 2 costs more than Type 1 without figures.
- **Cost source type:** vendor marketing
- **Cost sources:** SRC-VENDOR-VANTA-SOC2-COST
- **Substitution risks:** None acceptable.
- **Likely customer acceptance:** High; the common expectation for SaaS vendors handling financial data (assumption).
- **Total cost of ownership:** Recurring auditor fee, evidence operations all year, remediation, bridge letters.

### EXT-07 ISO/IEC 27001 certification

- **Why purchased:** International and enterprise customer requirement; alternative or complement to SOC 2.
- **Legally required:** No.
- **Independence required:** Yes, certification body impartiality under ISO/IEC 17021-1 and 27006-1.
- **Qualifications or accreditation:** Accredited certification body (accreditation by a national accreditation body to ISO/IEC 17021-1 with 27006-1).
- **Internal work can satisfy:** No for certification; the standard itself requires internal audits and management review that internal staff can perform.
- **Open source substitutes:** None for certification.
- **Scope reduction:** ISMS scope definition; audit time under ISO/IEC 27006-1 depends on scope and personnel (tables not read).
- **Evidence sharing across products:** High with one ISMS; SOC 2 evidence largely reusable.
- **Continuous performance:** Three-year cycle with surveillance audits.
- **Typical cost range:** Vendor marketing (Secureframe): audit costs about $10,000 to $50,000; about $10,000 per year surveillance. No credible independent source found.
- **Cost source type:** vendor marketing
- **Cost sources:** SRC-VENDOR-SECUREFRAME-ISO-COST; SRC-ISO-27006
- **Substitution risks:** Non-accredited certificates have low credibility.
- **Likely customer acceptance:** Accepted by many international buyers; US financial buyers often prefer SOC 2 (assumption).
- **Total cost of ownership:** Certification and surveillance fees, ISMS operation, internal audit.

### EXT-08 Privacy consulting

- **Why purchased:** Interpret privacy obligations for donor data; privacy notices; data protection assessments.
- **Legally required:** Purchase not required. Specific assessments may be required by law where a law applies (not established for Unbound).
- **Independence required:** No.
- **Qualifications or accreditation:** None mandated; legal advice requires licensed counsel.
- **Internal work can satisfy:** Yes for operational privacy engineering; no for legal opinions.
- **Open source substitutes:** None for legal judgment.
- **Scope reduction:** Data minimization by design reduces analysis scope.
- **Evidence sharing across products:** Moderate.
- **Continuous performance:** On regulatory change.
- **Typical cost range:** Hourly labor reference only: labor categories containing 'privacy' n=89, p25 $118.51, median $144.69, p75 $174.96 per hour (GSA CALC+ federal MAS ceiling hourly rates, snapshot 2026-11-25 (SRC-GSA-CALC); ceiling rates, not commercial engagement quotes). Attorney rates: unknown.
- **Cost source type:** government rate data
- **Cost sources:** SRC-GSA-CALC
- **Substitution risks:** Misinterpretation of law.
- **Likely customer acceptance:** Customers seldom ask for the consultant; they ask for outcomes.
- **Total cost of ownership:** Fees plus internal implementation.

### EXT-09 Regulatory consulting (DAF, payments, tax-exempt rules)

- **Why purchased:** Interpret sponsor and platform obligations; payment role (CNV-PAY-001).
- **Legally required:** No requirement to purchase located.
- **Independence required:** No.
- **Qualifications or accreditation:** Legal opinions require licensed attorneys; otherwise none.
- **Internal work can satisfy:** Research yes; legal conclusions no.
- **Open source substitutes:** Primary-source research in this repository.
- **Scope reduction:** Clear role allocation (sponsor originates payments) narrows questions.
- **Evidence sharing across products:** Low to moderate.
- **Continuous performance:** On regulatory change.
- **Typical cost range:** Unknown: no credible public source.
- **Cost source type:** unknown
- **Cost sources:** none
- **Substitution risks:** Unlicensed legal conclusions; misclassification of regulated activity.
- **Likely customer acceptance:** Sponsors may ask for counsel opinions (assumption).
- **Total cost of ownership:** Counsel fees plus internal research.

### EXT-10 Security and compliance policy development

- **Why purchased:** Speed; auditor familiarity with template structure.
- **Legally required:** No.
- **Independence required:** No.
- **Qualifications or accreditation:** None.
- **Internal work can satisfy:** Yes; policies must reflect actual operation, which only Echelon knows.
- **Open source substitutes:** Public frameworks (NIST, CSA CCM) as structure; Echelon Secure Construction Standard.
- **Scope reduction:** Policy as code tied to enforced rules reduces drift.
- **Evidence sharing across products:** High.
- **Continuous performance:** Annual review and on change.
- **Typical cost range:** Hourly labor reference only: labor categories containing 'polic' n=706, p25 $104.2, median $138.31, p75 $187.97 per hour (GSA CALC+ federal MAS ceiling hourly rates, snapshot 2026-11-25 (SRC-GSA-CALC); ceiling rates, not commercial engagement quotes).
- **Cost source type:** government rate data
- **Cost sources:** SRC-GSA-CALC
- **Substitution risks:** Generic policies that do not match practice create audit exceptions.
- **Likely customer acceptance:** Customers review content, not authorship.
- **Total cost of ownership:** Mostly internal time and approval workflow.

### EXT-11 Vendor risk assessments

- **Why purchased:** Assess Echelon's own suppliers (cloud, payment, AI providers); SOC 2 vendor management criteria; customer questionnaires about subprocessors.
- **Legally required:** No general statute located; may be contractual.
- **Independence required:** No.
- **Qualifications or accreditation:** None.
- **Internal work can satisfy:** Yes, using supplier SOC reports and certificates.
- **Open source substitutes:** CSA CAIQ for structured supplier answers; OpenSSF Scorecard for open-source dependencies.
- **Scope reduction:** Few, well-assured suppliers.
- **Evidence sharing across products:** High.
- **Continuous performance:** Annual and on change.
- **Typical cost range:** Hourly labor reference only: labor categories containing 'risk' n=62, p25 $140.38, median $173.95, p75 $212.07 per hour (GSA CALC+ federal MAS ceiling hourly rates, snapshot 2026-11-25 (SRC-GSA-CALC); ceiling rates, not commercial engagement quotes).
- **Cost source type:** government rate data
- **Cost sources:** SRC-GSA-CALC
- **Substitution risks:** Shallow reviews miss concentration risk.
- **Likely customer acceptance:** High if documented.
- **Total cost of ownership:** Internal time.

### EXT-12 Business continuity assessment

- **Why purchased:** Customer and sponsor resilience questions; SOC 2 availability criteria if selected.
- **Legally required:** Not established for Echelon.
- **Independence required:** No, unless a customer contract specifies.
- **Qualifications or accreditation:** None mandated.
- **Internal work can satisfy:** Yes, with exercised recovery tests as evidence.
- **Open source substitutes:** Infrastructure as code rebuild tests; restore drills.
- **Scope reduction:** Managed services and reproducible infrastructure.
- **Evidence sharing across products:** High with shared infrastructure.
- **Continuous performance:** Scheduled restore and failover exercises.
- **Typical cost range:** Hourly labor reference only: labor categories containing 'continuity' n=32, p25 $92.29, median $130.06, p75 $154.27 per hour (GSA CALC+ federal MAS ceiling hourly rates, snapshot 2026-11-25 (SRC-GSA-CALC); ceiling rates, not commercial engagement quotes).
- **Cost source type:** government rate data
- **Cost sources:** SRC-GSA-CALC
- **Substitution risks:** Untested plans.
- **Likely customer acceptance:** Moderate to high with test evidence (assumption).
- **Total cost of ownership:** Exercise time and infrastructure cost.

### EXT-13 Accessibility audit

- **Why purchased:** Donor-facing usability; procurement (VPAT/ACR requests); legal risk.
- **Legally required:** Applicability of ADA, Section 508 or other accessibility law to Unbound not established.
- **Independence required:** Not required by any source reviewed; buyers may prefer third-party.
- **Qualifications or accreditation:** None mandated in sources reviewed.
- **Internal work can satisfy:** Yes for testing against WCAG with automated and manual checks; independent audit improves credibility.
- **Open source substitutes:** Automated accessibility checkers and Forma accessibility contracts; automated tools cover only part of WCAG.
- **Scope reduction:** Forma components with accessibility contracts reduce per-screen defects (hypothesis).
- **Evidence sharing across products:** High if products share Forma.
- **Continuous performance:** Automated checks in CI plus periodic manual review.
- **Typical cost range:** Hourly labor reference only: labor categories containing 'accessib' n=114, p25 $102.05, median $134.23, p75 $159.09 per hour (GSA CALC+ federal MAS ceiling hourly rates, snapshot 2026-11-25 (SRC-GSA-CALC); ceiling rates, not commercial engagement quotes). Section 508 categories: n=69, median $100.36.
- **Cost source type:** government rate data
- **Cost sources:** SRC-GSA-CALC; SRC-W3C-WCAG
- **Substitution risks:** Automated tools miss many issues.
- **Likely customer acceptance:** Moderate.
- **Total cost of ownership:** Audit fee plus remediation and regression checks.

### EXT-14 AI governance assessment

- **Why purchased:** Customer questions about AI agents handling grants; bounded agent authority required by the Standard.
- **Legally required:** Not established for Unbound; jurisdiction dependent.
- **Independence required:** Voluntary frameworks do not require it; ISO/IEC 42001 certification would require a certification body (not verified in session).
- **Qualifications or accreditation:** None for NIST AI RMF; certification body for ISO/IEC 42001 (not verified).
- **Internal work can satisfy:** Yes for self-assessment against NIST AI RMF; no for certification.
- **Open source substitutes:** garak, PyRIT for technical testing; NIST AI RMF as framework.
- **Scope reduction:** Narrow agent authority, deterministic approval gates, no autonomous money movement.
- **Evidence sharing across products:** High if agent runtime is shared.
- **Continuous performance:** Per model or prompt change.
- **Typical cost range:** Hourly labor reference only: labor categories containing 'artificial' n=185, p25 $142.12, median $193.66, p75 $257.95 per hour (GSA CALC+ federal MAS ceiling hourly rates, snapshot 2026-11-25 (SRC-GSA-CALC); ceiling rates, not commercial engagement quotes). These are mostly engineering categories, not governance assessors.
- **Cost source type:** government rate data
- **Cost sources:** SRC-GSA-CALC; SRC-NIST-AI-RMF
- **Substitution risks:** Immature market; claims of AI assurance are easy to overstate.
- **Likely customer acceptance:** Unknown.
- **Total cost of ownership:** Internal testing and documentation; optional certification.

### EXT-15 Compliance monitoring platform

- **Why purchased:** Automated evidence collection, policy templates, auditor network, questionnaire tooling.
- **Legally required:** No.
- **Independence required:** No; the platform is a tool, not assurance.
- **Qualifications or accreditation:** None.
- **Internal work can satisfy:** Yes in principle: Praxis provenance and Tutela evidence could provide monitoring; build cost unmeasured.
- **Open source substitutes:** Echelon-native evidence pipeline; no specific open-source platform evaluated.
- **Scope reduction:** Fewer systems and uniform infrastructure reduce integrations needed.
- **Evidence sharing across products:** High.
- **Continuous performance:** Continuous by design.
- **Typical cost range:** Unknown: list prices not public in sources reviewed.
- **Cost source type:** unknown
- **Cost sources:** none
- **Substitution risks:** Auditors must assess reliability of entity-produced evidence regardless of tool; a home-built system may need more auditor testing (hypothesis).
- **Likely customer acceptance:** Customers do not see the platform; auditors' acceptance of a custom pipeline is unknown and must be confirmed in writing.
- **Total cost of ownership:** Subscription versus build and maintain; integration upkeep; auditor familiarity.

### EXT-16 Evidence collection for audits

- **Why purchased:** Reduce auditor hours and internal disruption.
- **Legally required:** No.
- **Independence required:** No; evidence is first-party and auditors evaluate it.
- **Qualifications or accreditation:** None.
- **Internal work can satisfy:** Yes.
- **Open source substitutes:** Praxis provenance, Tutela verification results, signed CI artifacts.
- **Scope reduction:** Machine-readable evidence keyed to control IDs.
- **Evidence sharing across products:** High.
- **Continuous performance:** Yes.
- **Typical cost range:** Unknown.
- **Cost source type:** unknown
- **Cost sources:** none
- **Substitution risks:** Evidence integrity and completeness must be demonstrable to auditors.
- **Likely customer acceptance:** Indirect (through auditor).
- **Total cost of ownership:** Internal build and maintenance.

### EXT-17 Security questionnaire completion

- **Why purchased:** Sales throughput.
- **Legally required:** No.
- **Independence required:** No; answers are first-party representations.
- **Qualifications or accreditation:** None.
- **Internal work can satisfy:** Yes; this repository's answer units are designed for it.
- **Open source substitutes:** This knowledge base; CSA CAIQ as a shareable standard response.
- **Scope reduction:** One answer per control concern; trust center publication.
- **Evidence sharing across products:** High.
- **Continuous performance:** Maintained answer library.
- **Typical cost range:** Unknown.
- **Cost source type:** unknown
- **Cost sources:** none
- **Substitution risks:** Overstated answers create contractual and misrepresentation risk.
- **Likely customer acceptance:** High when consistent with reports and evidence.
- **Total cost of ownership:** Internal time; library maintenance.

### EXT-18 SOC 1 Type 1 examination

- **Why purchased:** Sponsors' financial statement auditors rely on it when Unbound records ledgers, fund balances, NAV and unitization, fees and grant payments that flow into sponsors' financial statements (ANS-AUD-002, ANS-FCT-004, ANS-RCN-005). Added 2026-11-25 fix pass (OBJ-SOC2AUD-002).
- **Legally required:** No statute requires Echelon to obtain one. User auditors may otherwise need to test Unbound directly or perform substantive procedures; contracts with sponsors may require it.
- **Independence required:** Yes: independent CPA firm under AICPA attestation standards (SSAE 18, AT-C 320). The same firm should not also perform readiness or design work that would impair independence (AICPA independence rules not reviewed at primary source).
- **Qualifications or accreditation:** Licensed CPA firm with current AICPA peer review.
- **Internal work can satisfy:** No. Internal control testing is first-party and cannot substitute.
- **Open source substitutes:** None.
- **Scope reduction:** Report as of the production go-live date covering ledger posting, NAV and unitization, fee computation, grant authorization, payment file preparation, reconciliation, change and logical access (ANS-AUD-001 roadmap).
- **Evidence sharing across products:** Shares control environment, change and access testing with SOC 2, but has separate control objectives, system description and report; restricted use limits sharing to user entities and their auditors.
- **Continuous performance:** One-time point-in-time report, followed by Type 2.
- **Typical cost range:** Unknown. No credible public cost source located; a separate examination from SOC 2, so additive to SOC 2 fees.
- **Cost source type:** unknown
- **Cost sources:** none (SRC-AICPA-SOC1-GUIDE and SRC-AICPA-SSAE-18 describe the engagement, not its cost)
- **Substitution risks:** A SOC 2 report does not address control objectives relevant to user entities' financial reporting; presenting it as a SOC 1 substitute misleads user auditors.
- **Likely customer acceptance:** Expected by sponsors' auditors when Unbound is a financial reporting system (assumption, not measured).
- **Total cost of ownership:** Auditor fee, system description and control objectives drafting, management assertion, internal preparation; restricted-use distribution handling.

### EXT-19 SOC 1 Type 2 examination

- **Why purchased:** Sponsors' financial statement auditors rely on it when Unbound records ledgers, fund balances, NAV and unitization, fees and grant payments that flow into sponsors' financial statements (ANS-AUD-002, ANS-FCT-004, ANS-RCN-005). Added 2026-11-25 fix pass (OBJ-SOC2AUD-002).
- **Legally required:** No statute requires Echelon to obtain one. User auditors may otherwise need to test Unbound directly or perform substantive procedures; contracts with sponsors may require it.
- **Independence required:** Yes: independent CPA firm under AICPA attestation standards (SSAE 18, AT-C 320). The same firm should not also perform readiness or design work that would impair independence (AICPA independence rules not reviewed at primary source).
- **Qualifications or accreditation:** Licensed CPA firm with current AICPA peer review.
- **Internal work can satisfy:** No. Internal control testing is first-party and cannot substitute.
- **Open source substitutes:** None.
- **Scope reduction:** Period of at least three months sized to cover as much of the first hosted sponsor's fiscal year as possible; where go-live is less than roughly six to nine months before that fiscal year end, no Type 2 can exist in time and the fallback is direct or substantive testing by the sponsor's auditor (ANS-AUD-001).
- **Evidence sharing across products:** Shares control environment, change and access testing with SOC 2, but has separate control objectives, system description and report; restricted use limits sharing to user entities and their auditors.
- **Continuous performance:** Annual recurring period aligned to sponsors' fiscal years; bridge letters for gaps.
- **Typical cost range:** Unknown. No credible public cost source located; a separate examination from SOC 2, so additive to SOC 2 fees.
- **Cost source type:** unknown
- **Cost sources:** none (SRC-AICPA-SOC1-GUIDE and SRC-AICPA-SSAE-18 describe the engagement, not its cost)
- **Substitution risks:** A SOC 2 report does not address control objectives relevant to user entities' financial reporting; presenting it as a SOC 1 substitute misleads user auditors.
- **Likely customer acceptance:** Expected by sponsors' auditors when Unbound is a financial reporting system (assumption, not measured).
- **Total cost of ownership:** Recurring auditor fee, evidence operations all year, complementary user entity control documentation per sponsor, bridge letters, remediation. Likely the largest recurring assurance cost for a fund administration platform (judgment, not sourced).

SOC 1 use restriction: a SOC 1 report is intended for the service organization, its user entities and their auditors. It is distributed only to existing customers and their auditors, never to prospects (trust-center/TRUST-CENTER-REQUIREMENTS.md).

## Limitations and open questions

- PCI DSS v4.0.1 standard text was license-gated (HTTP 403); requirement text was read
  from the PCI DSS v4.0 SAQ D. Confirm against v4.0.1 before relying on numbering.
- Whether any PCI scope applies to Echelon or Unbound is not established (payments are
  originated by the sponsor under `CNV-PAY-001`; card acceptance is unknown).
- AICPA Trust Services Criteria points of focus and AICPA independence rules for
  readiness plus examination by the same firm were not reviewed at primary source.
- CREST, ISO and ISO/IEC 42001 pages blocked automated access; related records are
  marked `verified: false`.
- Customer, insurer and auditor acceptance of internal evidence has not been measured;
  every acceptance statement above is an assumption until Echelon obtains written
  positions.
