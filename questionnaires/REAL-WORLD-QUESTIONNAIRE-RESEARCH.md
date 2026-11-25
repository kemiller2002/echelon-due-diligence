---
id: DD-QNR-001
title: Real-world questionnaire and customer expectation research
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [due-diligence, questionnaires, customer-expectations, research]
---

# Real-world questionnaire and customer expectation research

## Purpose and method

This document records what publicly available customer questionnaires, supplier
requirement documents, insurance applications and procurement templates actually ask of
technology vendors, and compares that to what abstract frameworks (SIG, CAIQ, NIST CSF,
SOC 2 Trust Services Criteria) emphasize. It feeds the canonical question bank
(`questions/`) with topics that the frameworks underweight.

Method: web search, then direct retrieval of each document with `curl` (text extracted
with `pdftotext` or from `.docx` XML) or, where the issuer blocked `curl`, with a page
fetch tool. Every document relied on has a source record in
`sources/questionnaires-and-customer-expectations.jsonl` (63 records, 61 verified by
retrieval, 2 recorded as unverified because the issuer returned HTTP 403 or redirected).
Only publicly accessible material was used. No login-gated, NDA or confidential material
was accessed. No questionnaire text is reproduced; topics are paraphrased and cited.

Pre-allocated seed identifiers (for example `SRC-SA-SIG`, `SRC-EDUCAUSE-HECVAT`,
`SRC-INTERAGENCY-TPRM-2023`) are referenced where relevant but were not verified in this
task; their records belong to other source files.

Related outputs:

- `industry-profiles/financial-services/FINANCIAL-SERVICES-VENDOR-ASSESSMENT-PROFILE.md` (DD-IND-FS-001)
- `industry-profiles/donor-advised-funds/DAF-SPONSOR-TECHNOLOGY-PROCUREMENT-PROFILE.md` (DD-IND-DAF-001)
- `trust-center/TRUST-CENTER-RESEARCH.md` (DD-TC-001)
- `industry-profiles/enterprise-software/INSURANCE-UNDERWRITING-PROFILE.md` (DD-IND-INS-001)

## Corpus overview

| Document family | Examples retrieved (source IDs) | Count |
|---|---|---|
| Bank and broker-dealer supplier requirements | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-MS-SECURITY-STANDARDS-IT-CYBER, SRC-Q-MS-THIRD-PARTY-REG-REQS, SRC-Q-TRUIST-TPISS, SRC-Q-GS-VENDOR-TECH-RISK-EXPECTATIONS, SRC-Q-FIDELITY-SUPPLIER-POLICIES, SRC-Q-BOA-SUPPLIER-EXPECTATIONS, SRC-Q-WF-SUPPLIER-EXPECTATIONS, SRC-Q-JPMC-SUPPLIER-CODE, SRC-Q-GS-VENDOR-CODE, SRC-Q-MS-SUPPLIER-CODE, SRC-Q-EDWARD-JONES-CODE | 12 |
| Published data processing agreement | SRC-Q-MS-DATA-PROCESSING-TERMS | 1 |
| Supervisory and regulatory items fetched here | SRC-Q-NYDFS-IL-20251021-TPSP, SRC-Q-SEC-REG-SP-2024-FACT-SHEET, SRC-Q-DECHERT-SEC-WITHDRAWALS-2025 | 3 |
| AI vendor assessments | SRC-Q-FSISAC-GENAI-VENDOR-GUIDE, SRC-Q-PURDUE-AI-VENDOR-Q, SRC-Q-ACLU-GENAI-VENDOR-Q, SRC-Q-MEMPHIS-VENDOR-SEC-PRIV-TEMPLATE, SRC-Q-AU-AI-PROCUREMENT | 5 |
| Public-sector and university security and privacy | SRC-Q-MD-STD-317-SA-01, SRC-Q-WI-DOA-10816, SRC-Q-UTS-MIN-SECURITY-REQS, SRC-Q-ARIZONA-3P-SEC-PRIV-Q, SRC-Q-UCI-PIA, SRC-Q-USU-VENDOR-MGMT-PLAN | 6 |
| Accessibility (VPAT/ACR requests and contract language) | SRC-Q-YALE-ACCESSIBLE-PURCHASING, SRC-Q-MTU-ICT-ACCESSIBILITY-PROCUREMENT, plus accessibility sections of SRC-Q-FIDELITY-SUPPLIER-POLICIES and SRC-Q-MS-THIRD-PARTY-REG-REQS | 2 (+2) |
| Business continuity questionnaires | SRC-Q-OHIO-U-VENDOR-BCP-Q, SRC-Q-SIFMA-COB-ASSESSMENT | 2 |
| Cyber insurance applications | SRC-Q-ATBAY-CYBER-APP-2026, SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022, SRC-Q-CORVUS-RANSOMWARE-SUPP-2022, SRC-Q-AXIS-RANSOMWARE-SUPP, SRC-Q-TMHCC-NETGUARD-APP-2026, SRC-Q-INDIANA-CYBER-INSURANCE-TOOLKIT | 6 |
| DAF sponsor and administrator public documents | 13 records, see DD-IND-DAF-001 | 13 |
| Trust center practice | 13 records, see DD-TC-001 | 13 |

Gaps: no public bank vendor due diligence questionnaire in fill-in form was located (banks
publish requirement documents; the questionnaires themselves are delivered through TPRM
platforms after onboarding). No community foundation or DAF sponsor published a vendor
questionnaire. The HECVAT download page and EDUCAUSE articles returned HTTP 403 and are
covered only by the seed ID `SRC-EDUCAUSE-HECVAT`. A public SIG or VSA copy was not used;
both are covered by seed IDs and their content is licensed.

## What real questionnaires ask that abstract frameworks underweight

Frameworks state outcomes ("access is restricted", "incidents are reported"). Real
customer documents state numbers, deadlines, locations, named technologies and contract
consequences. The recurring differences:

1. **Hard deadlines instead of "timely".** Customer breach notice not later than 24
   hours (SRC-Q-MS-DATA-PROCESSING-TERMS); 72 hours from service provider to covered
   institution under Regulation S-P (SRC-Q-SEC-REG-SP-2024-FACT-SHEET); alerting
   stakeholders within 24 hours (SRC-Q-TRUIST-TPISS); remediate customer-identified
   material findings within 5 days or agree a plan (SRC-Q-TRUIST-TPISS); privileged access
   removed within 24 hours (SRC-Q-TRUIST-TPISS); 90 days notice of material subcontracting
   changes (SRC-Q-MS-THIRD-PARTY-REG-REQS); 48 hours notice for on-site audits
   (SRC-Q-MS-THIRD-PARTY-REG-REQS); critical patch target bands from under 24 hours to
   over 7 days (SRC-Q-AXIS-RANSOMWARE-SUPP).
2. **Location as a control.** Country where hosted software is developed and maintained
   and where support is performed, stated on invoices (SRC-Q-FIDELITY-SUPPLIER-POLICIES);
   supplier personnel remote access restricted to the United States unless approved
   (SRC-Q-TRUIST-TPISS); infrastructure outside the contiguous United States for vendor
   and subcontractors (SRC-Q-WI-DOA-10816); data assumed to stay in the customer's country
   unless disclosed, with advance notice of location changes (SRC-Q-MS-THIRD-PARTY-REG-REQS);
   limits on where data is stored, processed or accessed (SRC-Q-NYDFS-IL-20251021-TPSP).
3. **Integration into the customer's identity plane.** SaaS must federate to the bank's
   enterprise IdP (SRC-Q-TRUIST-TPISS); federated login or SSO expected
   (SRC-Q-GS-VENDOR-TECH-RISK-EXPECTATIONS); customer involvement in approving and reviewing
   its own employees' entitlements in vendor systems (SRC-Q-MS-MIN-SECURITY-STANDARDS).
4. **Per-customer cryptography.** Dedicated keys for the customer's services in public
   cloud (SRC-Q-MS-MIN-SECURITY-STANDARDS); customer-unique encryption keys and a 24-month
   maximum rotation (SRC-Q-TRUIST-TPISS); named approved algorithms and protocols
   (SRC-Q-MS-SECURITY-STANDARDS-IT-CYBER).
5. **Customer-run testing and monitoring of the vendor.** Customer right to perform or
   commission pen tests of supplier services (SRC-Q-MS-SECURITY-STANDARDS-IT-CYBER);
   annual non-intrusive customer audit and OSINT or threat hunting against higher-risk
   suppliers (SRC-Q-TRUIST-TPISS); university scanning of a production-mirror environment
   as an alternative to a third-party test (SRC-Q-UTS-MIN-SECURITY-REQS); participation in
   regulator-driven threat-led penetration testing (SRC-Q-MS-THIRD-PARTY-REG-REQS).
6. **Assurance acceptance rules.** A SOC 2 Type 2 is accepted only with an unqualified
   opinion covering CC3, CC6 and CC7 (SRC-Q-MD-STD-317-SA-01); a SOC 2 Type II or FedRAMP
   document exempts the vendor from 80 security questions (SRC-Q-WI-DOA-10816); annual
   SOC 1 or SOC 2 Type II covering the most recent 12 months, or ISO 27001 with Statement
   of Applicability (SRC-Q-MS-THIRD-PARTY-REG-REQS); consortium assessments such as KYP3
   do not replace bank-specific requirements (SRC-Q-TRUIST-TPISS); self-assessed VPATs are
   not accepted (SRC-Q-FIDELITY-SUPPLIER-POLICIES).
7. **AI disclosure and data-use limits written into vendor terms**, not only into AI
   governance frameworks (see section "New question topics").
8. **Exit and resolution.** Exit assistance at the fees in effect before termination;
   services must continue if the customer enters a resolution event; divestee use
   (SRC-Q-MS-THIRD-PARTY-REG-REQS); certified deletion including backups and cached copies
   (SRC-Q-NYDFS-IL-20251021-TPSP); certificates of destruction on request
   (SRC-Q-MS-MIN-SECURITY-STANDARDS).
9. **People screening depth.** Seven-year county criminal searches, credit reports, SSN
   verification, education and employment verification, fingerprinting for unescorted
   premises access, and vendor reimbursement of the customer's own checks
   (SRC-Q-FIDELITY-SUPPLIER-POLICIES). Frameworks only say "screening proportional to risk".
10. **Fraud controls around payments.** Dual authorization above a dollar threshold
    (SRC-Q-ATBAY-CYBER-APP-2026) and call-back verification of new or changed payee bank
    details (SRC-Q-TMHCC-NETGUARD-APP-2026, SRC-Q-INDIANA-CYBER-INSURANCE-TOOLKIT). For a
    grant disbursement platform these become product questions, not only corporate ones.

## Recurring themes across document families

| Theme | Where it recurs | Notes |
|---|---|---|
| MFA everywhere, with named scope (email, remote, privileged, backups, vendor access) | Every insurance application; SRC-Q-MS-MIN-SECURITY-STANDARDS; SRC-Q-TRUIST-TPISS; SRC-Q-UTS-MIN-SECURITY-REQS; SRC-Q-NYDFS-IL-20251021-TPSP | Insurers ask about factor type (SMS vs authenticator vs security key) in SRC-Q-AXIS-RANSOMWARE-SUPP |
| Independent penetration testing, annual, covering apps and networks | SRC-Q-MS-MIN-SECURITY-STANDARDS; SRC-Q-UTS-MIN-SECURITY-REQS; SRC-Q-GS-VENDOR-TECH-RISK-EXPECTATIONS; SRC-Q-WI-DOA-10816 (off-cycle triggers) | Executive summaries are the usual shareable artifact (SRC-Q-GITLAB-CUSTOMER-ASSURANCE) |
| Subcontractor (fourth party) oversight and flow-down | SRC-Q-MS-MIN-SECURITY-STANDARDS; SRC-Q-TRUIST-TPISS; SRC-Q-GS-VENDOR-TECH-RISK-EXPECTATIONS; SRC-Q-NYDFS-IL-20251021-TPSP; SRC-Q-BOA-SUPPLIER-EXPECTATIONS; SRC-Q-SIFMA-COB-ASSESSMENT | Includes consent, notice periods and NDAs with subcontractors |
| BC/DR plan delivered to the customer and tested with real recovery | SRC-Q-MS-MIN-SECURITY-STANDARDS; SRC-Q-OHIO-U-VENDOR-BCP-Q; SRC-Q-SIFMA-COB-ASSESSMENT; SRC-Q-ATBAY-CYBER-APP-2026 | RPO aligned to the customer's requirement, not the vendor's |
| Change notification to the customer | SRC-Q-MS-MIN-SECURITY-STANDARDS; SRC-Q-MS-THIRD-PARTY-REG-REQS (material adverse impact) | Proactive notice of any change that may impact the customer |
| Accessibility with evidence | SRC-Q-FIDELITY-SUPPLIER-POLICIES; SRC-Q-MS-THIRD-PARTY-REG-REQS; SRC-Q-YALE-ACCESSIBLE-PURCHASING; SRC-Q-MTU-ICT-ACCESSIBILITY-PROCUREMENT | WCAG 2.2 AA in finance documents, WCAG 2.1 AA in universities |
| Data minimization in non-production and logs | SRC-Q-MS-MIN-SECURITY-STANDARDS | Production data in lower environments and logging of PII prohibited |
| Ransomware resilience | All insurance forms | Immutable, offline, encrypted backups with offline key copies and restore tests |
| ESG and human rights supplier screening | SRC-Q-GS-VENDOR-CODE; SRC-Q-MS-SUPPLIER-CODE; SRC-Q-BOA-SUPPLIER-EXPECTATIONS | Low security weight but appears in onboarding |

## Unusual or high-friction questions

These are the items most likely to stall a deal for a small, pre-revenue vendor such as
Echelon. Each should have a prepared, honest answer.

| Item | Source | Why it is high friction for Echelon |
|---|---|---|
| Third-party (not self-assessed) accessibility conformance report | SRC-Q-FIDELITY-SUPPLIER-POLICIES | Requires paying an external auditor; Forma accessibility contracts are not a substitute |
| Background checks including credit report and customer reimbursement of its own checks | SRC-Q-FIDELITY-SUPPLIER-POLICIES | No personnel screening program is established (DD-ARC-001) |
| Customer-specific encryption keys in public cloud | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-TRUIST-TPISS | Architectural decision for multi-tenant Unbound; costly to retrofit |
| Prior written consent for every sub-processor | SRC-Q-MS-DATA-PROCESSING-TERMS | Conflicts with the general-authorization model most SaaS DPAs use |
| 24-hour personal information incident notice | SRC-Q-MS-DATA-PROCESSING-TERMS | Stricter than 72-hour norms; needs an on-call capability |
| US-only remote access by supplier personnel | SRC-Q-TRUIST-TPISS | Constrains offshore contractors and AI agent hosting regions |
| Remediate assessment findings in 5 days or agree a plan | SRC-Q-TRUIST-TPISS | Requires capacity to respond to customer-run assessments |
| SOC 2 accepted only with unqualified opinion on CC3, CC6, CC7 | SRC-Q-MD-STD-317-SA-01 | A first SOC 2 with exceptions may not qualify |
| Annual SOC report covering the most recent 12 months | SRC-Q-MS-THIRD-PARTY-REG-REQS | Type 1 or short-window Type 2 will not satisfy |
| Redacted and unredacted copies of security documents for public records | SRC-Q-WI-DOA-10816 | Public-sector buyers may be compelled to disclose submissions |
| Explain the basis of any model or GenAI used | SRC-Q-MS-MIN-SECURITY-STANDARDS | Requires model documentation for AI-assisted features |
| Continue service during the customer's resolution event at existing fees | SRC-Q-MS-THIRD-PARTY-REG-REQS | Financial commitment that a small vendor must price |
| Insurance representation that MFA remains continuously enforced | SRC-Q-TMHCC-NETGUARD-APP-2026 | A lapse can affect coverage; turns a control into a warranty |
| Donors must never share sponsor credentials with third-party tools | SRC-Q-FC-SECURITY-PAGE | Rules out screen-scraping or credential-based aggregation as an integration model |
| Disclosure of whether the product uses an accessibility overlay | SRC-Q-YALE-ACCESSIBLE-PURCHASING | Overlays are viewed negatively; the answer should be a clear no |

## Evidence demanded

| Evidence | Demanded by | Notes for Echelon |
|---|---|---|
| SOC 2 Type II (most recent 12 months), SOC 1 Type II, ISO 27001 certificate with SoA, FedRAMP or GovRAMP | SRC-Q-MS-THIRD-PARTY-REG-REQS, SRC-Q-MD-STD-317-SA-01, SRC-Q-WI-DOA-10816, SRC-Q-NYDFS-IL-20251021-TPSP | None exist; answer status `unknown` or `proposed-target-state` |
| Penetration test results or summary, with remediation tracking | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-UTS-MIN-SECURITY-REQS, SRC-Q-WI-DOA-10816, SRC-Q-NYDFS-IL-20251021-TPSP | No external test exists |
| BC/DR plans and test results | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-SIFMA-COB-ASSESSMENT, SRC-Q-OHIO-U-VENDOR-BCP-Q | Plans are design-stage in Unbound requirements |
| Certificates of destruction | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-NYDFS-IL-20251021-TPSP | Needs a deletion attestation process including backups |
| Architecture and data flow diagrams | SRC-Q-UTS-MIN-SECURITY-REQS, SRC-Q-CSA-BUILDING-TRUST-CENTER-2024 | Can be produced from Unbound requirements, marked as design |
| ACR or VPAT from an approved third-party auditor, dated within 18 months | SRC-Q-FIDELITY-SUPPLIER-POLICIES, SRC-Q-YALE-ACCESSIBLE-PURCHASING | None exists |
| Written policies (infosec, data handling, BC/DR, incident response) | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-BOA-SUPPLIER-EXPECTATIONS, SRC-Q-ARIZONA-3P-SEC-PRIV-Q | Only the proposed Secure Construction Standard v0.1 exists |
| Cyber insurance certificate | SRC-Q-PLAID-SECURITY-PORTAL-2023 (published as trust artifact); see DD-IND-INS-001 | No policy established |
| Training records and metrics, including safe AI use | SRC-Q-MS-MIN-SECURITY-STANDARDS | None established |
| AI model documentation: basis, limitations, training data provenance, bias testing | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-PURDUE-AI-VENDOR-Q, SRC-Q-ACLU-GENAI-VENDOR-Q, SRC-Q-FSISAC-GENAI-VENDOR-GUIDE | Applies only if Unbound ships AI features |

## New question topics for the canonical question bank

Topics below are materially distinct from generic framework items (different concern,
control, evidence or population, per DD-GOV-001). Suggested category codes come from
`questions/TAXONOMY.json`. Priority reflects frequency across the corpus and impact on
financial-services and DAF buyers.

| # | Topic | Why it matters | Category | Source IDs | Priority |
|---|---|---|---|---|---|
| 1 | Proactive disclosure that a service uses a model or GenAI, with an explanation of the model and its basis | Large FS buyers now require this as a supplier security standard, not an optional AI questionnaire | AIG | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-FSISAC-GENAI-VENDOR-GUIDE | High |
| 2 | Whether customer data may be used to train or improve AI models, and contractual commitments | Named contract topic in supervisory guidance and AI questionnaires | AIG, PRV | SRC-Q-NYDFS-IL-20251021-TPSP, SRC-Q-ACLU-GENAI-VENDOR-Q, SRC-Q-FSISAC-GENAI-VENDOR-GUIDE | High |
| 3 | Prohibition on entering customer data into third-party or open-source GenAI tools by vendor staff | Explicit bank requirement; covers workforce use of AI, not product AI | AIS, HR | SRC-Q-TRUIST-TPISS, SRC-Q-MS-MIN-SECURITY-STANDARDS | High |
| 4 | Logged, restricted access to model data and training datasets | Distinct control from general data access | AIS | SRC-Q-MS-MIN-SECURITY-STANDARDS | Medium |
| 5 | Named human oversight role and evidence for AI outputs (no generic "human in the loop") | Reviewers reject unsupported oversight claims | AIA | SRC-Q-PURDUE-AI-VENDOR-Q, SRC-Q-MEMPHIS-VENDOR-SEC-PRIV-TEMPLATE | Medium |
| 6 | Training data copyright, IP indemnity and environmental footprint of AI features | Nonprofit and university buyers ask; mission-driven DAF sponsors are similar | AIG, IPR | SRC-Q-ACLU-GENAI-VENDOR-Q, SRC-Q-AU-AI-PROCUREMENT | Low |
| 7 | Security, resilience and safe-AI training for personnel assigned to the customer, with metrics reported | Training content and reporting are specified, not just "awareness training" | HR | SRC-Q-MS-MIN-SECURITY-STANDARDS | Medium |
| 8 | Depth of background investigation (credit, county criminal, identity, education, employment, fingerprinting) and who pays | Fidelity-family requirement likely to reach Fidelity Charitable vendors (inferred) | HR | SRC-Q-FIDELITY-SUPPLIER-POLICIES | High |
| 9 | Countries where software is developed, maintained and supported, and where personnel access data remotely | Location is treated as a control and a tax or invoicing disclosure | GOV, REG | SRC-Q-FIDELITY-SUPPLIER-POLICIES, SRC-Q-TRUIST-TPISS, SRC-Q-WI-DOA-10816, SRC-Q-MS-THIRD-PARTY-REG-REQS | High |
| 10 | Mandatory SSO federation to the customer's IdP and customer participation in entitlement reviews for its users | Customer identity plane integration | AUN, IAM | SRC-Q-TRUIST-TPISS, SRC-Q-GS-VENDOR-TECH-RISK-EXPECTATIONS, SRC-Q-MS-MIN-SECURITY-STANDARDS | High |
| 11 | Privileged access review cadence (quarterly), deprovisioning within 24 hours, just-in-time privileged access | Numeric thresholds | IAM | SRC-Q-TRUIST-TPISS, SRC-Q-MS-MIN-SECURITY-STANDARDS | Medium |
| 12 | Prohibition of PII and SSNs in logs | Distinct from log retention and protection | MON, DCL | SRC-Q-MS-MIN-SECURITY-STANDARDS | Medium |
| 13 | Prohibition of production data in non-production environments | Common FS requirement, often missed | DCL, SDL | SRC-Q-MS-MIN-SECURITY-STANDARDS | Medium |
| 14 | Customer-dedicated encryption keys, HSM use for high-value keys, single-purpose keys, key inventory, maximum rotation period | Per-tenant cryptography is architectural | ENC, TEN | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-TRUIST-TPISS | High |
| 15 | Timeline to remediate findings from customer-run assessments, and acceptance of customer OSINT or attack-surface monitoring | Customer is an active tester | VUL, RSK | SRC-Q-TRUIST-TPISS | Medium |
| 16 | Customer and regulator right to pen test, audit on site (with notice period) and take copies of records | Rights clauses frequently negotiated | AUD, LEG | SRC-Q-MS-SECURITY-STANDARDS-IT-CYBER, SRC-Q-MS-THIRD-PARTY-REG-REQS, SRC-Q-TRUIST-TPISS | High |
| 17 | Per-sub-processor prior written consent, objection rights and notice period (for example 90 days) | Stricter than general authorization | SUB | SRC-Q-MS-DATA-PROCESSING-TERMS, SRC-Q-MS-THIRD-PARTY-REG-REQS, SRC-Q-NYDFS-IL-20251021-TPSP | High |
| 18 | Notification of government or law enforcement access requests for customer data within a fixed time | Separate obligation from breach notice | PRV, LEG | SRC-Q-MS-DATA-PROCESSING-TERMS | Medium |
| 19 | Breach notice to customer within 24 hours, and support for the customer's 30-day individual notice under Regulation S-P | Concrete deadlines for FS customers | IR | SRC-Q-MS-DATA-PROCESSING-TERMS, SRC-Q-SEC-REG-SP-2024-FACT-SHEET | High |
| 20 | Certified deletion at exit including backups and cached copies, and revocation of API and federated access | Offboarding is now examined explicitly | RET, TRM | SRC-Q-NYDFS-IL-20251021-TPSP, SRC-Q-MS-MIN-SECURITY-STANDARDS | High |
| 21 | Exit assistance at existing fees and continuity during the customer's recovery or resolution event | Bank resolution planning flows to vendors | TRM | SRC-Q-MS-THIRD-PARTY-REG-REQS | Low for DAF sponsors, Medium for bank-sponsored DAFs |
| 22 | SOC report acceptability: opinion type, criteria covered, period length and recency | Buyers reject qualified or short-period reports | AUD | SRC-Q-MD-STD-317-SA-01, SRC-Q-MS-THIRD-PARTY-REG-REQS | High |
| 23 | Availability of assurance reports before contract signature | Buyers want reports pre-signature | AUD | SRC-Q-ARIZONA-3P-SEC-PRIV-Q | Medium |
| 24 | Handling of security documents under public records laws (redacted copies) | Public-sector disclosure risk for trust artifacts | AUD, LEG | SRC-Q-WI-DOA-10816 | Low |
| 25 | End-of-life and unsupported component detection, risk treatment and disclosure to the customer | Insurance and bank requirement | ASM, VUL | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022 | Medium |
| 26 | Cloud configuration drift prevention and a CSP shared-responsibility matrix covering resilience | Explicit cloud requirement | CLD | SRC-Q-MS-MIN-SECURITY-STANDARDS | Medium |
| 27 | DNS security controls (encrypted DNS, protective DNS, DNS logging) | Frequently absent from SaaS questionnaires | NET | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022 | Low |
| 28 | Session security specifics (concurrent login prevention, session ID rotation, cookie flags, configurable timeouts) | Testable application controls | APP | SRC-Q-MS-MIN-SECURITY-STANDARDS | Medium |
| 29 | Independent third-party accessibility audit, overlay disclosure, ACR recency, WCAG version adoption roadmap and remediation schedule | Accessibility now carries termination remedies | A11Y | SRC-Q-FIDELITY-SUPPLIER-POLICIES, SRC-Q-YALE-ACCESSIBLE-PURCHASING, SRC-Q-MTU-ICT-ACCESSIBILITY-PROCUREMENT, SRC-Q-MS-THIRD-PARTY-REG-REQS | High |
| 30 | Integration model that never requires donor or advisor credentials for sponsor accounts | DAF sponsor explicitly warns donors against credential-sharing tools | API, DON, WLB | SRC-Q-FC-SECURITY-PAGE | High |
| 31 | Consent-based, logged vendor support access to donor accounts | Sponsor privacy notices describe consent for vendor login | DON, IAM, SUP | SRC-Q-GKCCF-PRIVACY-POLICY, SRC-Q-VANGUARD-CHARITABLE-PRIVACY | High |
| 32 | Payee bank detail change verification (call-back to number on file) and dual authorization for disbursements | Insurers ask it of the vendor; DAF buyers will ask it of the product | FRD, PAY | SRC-Q-TMHCC-NETGUARD-APP-2026, SRC-Q-INDIANA-CYBER-INSURANCE-TOOLKIT, SRC-Q-ATBAY-CYBER-APP-2026 | High |
| 33 | Ransomware-specific backup assurance: immutability, offline encrypted copies, offline key copies, measured restore time | Underwriting-driven, increasingly echoed in BC questionnaires | BKP | SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022, SRC-Q-ATBAY-CYBER-APP-2026, SRC-Q-AXIS-RANSOMWARE-SUPP | Medium |
| 34 | Recovery exercise in the last 12 months that included actual recovery of all systems needed for the service, and turnover of key recovery staff | More specific than "BCP tested annually" | BCP, DR | SRC-Q-OHIO-U-VENDOR-BCP-Q, SRC-Q-SIFMA-COB-ASSESSMENT | Medium |
| 35 | Recovery objectives set per service to match the customer's requirement, and DR capacity parity with production | Customer-driven RPO and RTO | DR, AVL | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-SIFMA-COB-ASSESSMENT | Medium |
| 36 | Proactive notice of changes that may affect the customer, and of developments that may materially impair service | Change notification as a duty | CHG, GOV | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-MS-THIRD-PARTY-REG-REQS | Medium |
| 37 | Sustainability, human rights and modern slavery supplier due diligence responses | Appears in large-bank onboarding even for software vendors | GOV | SRC-Q-GS-VENDOR-CODE, SRC-Q-MS-SUPPLIER-CODE, SRC-Q-BOA-SUPPLIER-EXPECTATIONS | Low |
| 38 | Small-business accommodation and remediation plans when expectations cannot yet be met | Some buyers document a path for small suppliers; useful for a pre-revenue vendor | GOV, TPR | SRC-Q-BOA-SUPPLIER-EXPECTATIONS | Medium |

## Objections and contrary evidence (preserved)

- Several sources are old (Beazley and Corvus 2022, Goldman Sachs technology expectations
  2021, SIFMA COB assessment uploaded 2017). They may overstate or understate current
  practice. They are retained because recent equivalents were not public.
- Bank supplier documents state that contract terms prevail. A public baseline is not
  proof that a specific requirement will be in an Unbound contract.
- Large-bank requirements (Morgan Stanley, Truist) are the strictest public examples. A
  community foundation or independent DAF sponsor is likely to ask less. Using them as a
  baseline risks over-engineering for early customers; not using them risks redesign when
  a bank-affiliated sponsor is pursued. Product decisions should weigh both.
- Insurance applications ask about the applicant's own enterprise environment. Their
  relevance to customer questionnaires is indirect (see DD-IND-INS-001).

## Open questions

- Which of the named DAF sponsors route technology vendors through a parent company TPRM
  program (Fidelity, Schwab, Vanguard, Morgan Stanley, Goldman Sachs, Bank of America,
  Edward Jones)? Not publicly documented; requires direct inquiry.
- Does Bank of America's non-public Service Provider Security Requirements Document apply
  to vendors of the Charitable Gift Fund? Unknown.
- Current HECVAT 4 AI section content could not be retrieved (HTTP 403); verify via a
  permitted channel.
