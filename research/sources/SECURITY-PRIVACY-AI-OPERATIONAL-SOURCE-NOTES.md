---
id: DD-SRC-SEC-001
title: Security, privacy, AI governance and operational source notes for vendor due diligence
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [due-diligence, sources, security, privacy, ai-governance, operational, licensing]
---

# Security, privacy, AI governance and operational source notes

Companion to the source registers `sources/security-frameworks.jsonl` (67 records),
`sources/privacy.jsonl` (14), `sources/ai-governance.jsonl` (23) and
`sources/operational.jsonl` (20). Every fact below was checked on 2026-11-25 against the
issuer's own site unless the record says otherwise. Records with
`verification.verified: false` hold at least one fact that could not be confirmed on an
issuer page; treat those facts as provisional.

Subjects:

- **Echelon**: Echelon Foundry, a small US software company (Indiana LLC). As of
  2026-11-25 it has no production system, no SOC report, no ISO certificate and no
  external penetration test (`architecture/ECHELON-CURRENT-STATE-BRIEF.md`).
- **Unbound**: a donor-advised fund (DAF) administration platform, requirements stage
  only. Its intended customers are DAF sponsors, including sponsors affiliated with
  financial institutions. Per `CNV-PAY-001` the sponsor originates payments and Unbound
  acts as a third-party service provider.

Authority classes used throughout: **binding law or regulation** (statutes,
regulations, federal directives), **supervisory expectation** (bank regulator
guidance), **certification criteria** (criteria an assessor or auditor tests against),
**voluntary framework or standard** and **customer convention** (questionnaires and
contract asks that are market practice, not law).

## 1. Material changes found versus the seed list

These corrections change answers, not just citations.

| Seed item | Finding on 2026-11-25 | Record |
|---|---|---|
| SR 11-7 / OCC 2011-12 | Superseded on 2026-04-17 by SR 26-2, interagency Revised Guidance on Model Risk Management (Fed, OCC, FDIC); SR 21-8 also superseded | `SRC-SR-11-7`, `SRC-SR-26-2` |
| EU AI Act staged dates | Amended by Regulation (EU) 2026/1744 (Digital Omnibus on AI), in force 2026-07-27. Annex III high-risk obligations moved to 2027-12-02, Annex I high-risk to 2028-08-02; new prohibitions and legacy Article 50(2) compliance from 2026-12-02 | `SRC-EU-AI-ACT`, `SRC-EU-AI-OMNIBUS-2026` |
| Colorado AI Act (SB 24-205 as amended) | SB 25B-004 had delayed it to 2026-06-30; SB 26-189 (signed 2026-05-14) then repealed and reenacted it as an automated decision-making technology (ADMT) law. Developer documentation starts 2027-01-01 | `SRC-COLORADO-AI-ACT`, `SRC-COLORADO-SB26-189` |
| OMB M-22-18 and M-23-16 | Rescinded by OMB M-26-05 (2026-01-23). The CISA attestation form is now optional for agencies | `SRC-OMB-M-22-18`, `SRC-OMB-M-26-05`, `SRC-CISA-SSDF-ATTESTATION` |
| CISA SBOM minimum elements (2025) | The 2025 draft was followed by the 2026 Minimum Elements (2026-07-29), which CISA says replace the NTIA 2021 elements | `SRC-CISA-SBOM-MIN`, `SRC-NTIA-SBOM-MIN` |
| CISA BOD 22-01 | Revoked; superseded by BOD 26-04 (2026-06-10) | `SRC-CISA-BOD-22-01`, `SRC-CISA-BOD-26-04` |
| ADA Title II web rule (2024) | DOJ interim final rule (effective 2026-04-20) extended compliance dates to 2027-04-26 (50,000 or more population) and 2028-04-26 (smaller entities) | `SRC-ADA` |
| CSA CAIQ / CCM v4 | Current is v4.1 (released 2026-01-27) | `SRC-CSA-CAIQ-V4`, `SRC-CSA-CCM-V4` |
| CSA AICM | Current is v1.1 (2026-06-22) | `SRC-CSA-AICM` |
| ISO/IEC 27017 | 2026 edition published 2026-07-27; 2015 edition withdrawn | `SRC-ISO-27017` |
| ISO/IEC 27018, 27701, 27031 | 2025 editions are current | `SRC-ISO-27018`, `SRC-ISO-27701`, `SRC-ISO-27031` |
| NIST SP 800-88 | Rev. 2 (2025-09-26) is current | `SRC-NIST-SP800-88` |
| NIST SP 800-53 | Release 5.2.0 (2025-08-27) adds SA-15(13), SA-24, SI-02(07) | `SRC-NIST-SP800-53-R5` |
| NIST SSDF | 1.1 remains final; SSDF 1.2 (SP 800-218 Rev. 1) is an initial public draft (2025-12-17) | `SRC-NIST-SP800-218`, `SRC-NIST-SP800-218-R1-IPD` |
| CWE | CWE 5.0 released 2026-10-28; 2025 Top 25 (2025-12-11) is the latest list | `SRC-MITRE-CWE`, `SRC-MITRE-CWE-TOP25` |
| OWASP Top 10 | 2025 edition is current | `SRC-OWASP-TOP10` |
| OWASP LLM Top 10 | A 2026 edition supersedes 2025 | `SRC-OWASP-LLM-TOP10-2025`, `SRC-OWASP-LLM-TOP10-2026` |
| SLSA | v1.2 (2025-11-24) is current | `SRC-SLSA` |
| EN 301 549 | V4.1.1 (2026-09) is current and references WCAG 2.2 | `SRC-EN-301-549` |
| AICPA TSC | Exposure drafts of proposed 2027 SOC 2 TSC and Description Criteria issued 2026-11-16 | `SRC-AICPA-TSC-2027-ED` |
| VSA | Current editions are labeled VSA CORE 2027 and VSA FULL 2027 | `SRC-VSA-CORE`, `SRC-VSA-FULL` |
| FAR | FAC 2026-01 (effective 2026-03-13); Revolutionary FAR Overhaul in progress | `SRC-FAR` |
| StateRAMP | Operates as GovRAMP | `SRC-STATERAMP` |

Confirmed unchanged: OWASP ASVS 5.0.0 (2025-05-30), CIS Controls v8.1, NIST CSF 2.0,
NIST Privacy Framework 1.0 (1.1 still a draft), NIST AI RMF 1.0, PCI DSS v4.0.1 (an RFC
on it ran 2026-06-03 to 2026-07-20), ISO/IEC 27001:2022 with Amd 1:2024, ISO/IEC
42001:2023 (no amendment listed).

Could not confirm: the current SIG release year (2026 confirmed on the issuer page, a
2027 release reported but not confirmed because the issuer site forces an SSO
redirect), HECVAT build (4.1.6 reported by search) and license, PCI SSF version numbers,
CMMC Phase 2 status, and the NAIC adoption count.

## 2. Role of each source in vendor due diligence

Role codes: **Q** questionnaire a customer sends; **A** assurance or certification
evidence a customer accepts; **C** control catalog or requirement source Echelon designs
to; **T** taxonomy or vocabulary for classifying findings; **L** law or regulation that
sets obligations; **S** supervisory expectation that shapes customer TPRM; **G** general
guidance.

| Source | Role | Authority | Use in Echelon due diligence |
|---|---|---|---|
| Shared Assessments SIG | Q | Customer convention | Likeliest questionnaire from bank-affiliated sponsors; map by ID only |
| Shared Assessments SCA | Q, A | Customer convention | Procedures a customer may use to test SIG answers |
| CSA CAIQ v4.1 | Q, A | Customer convention | Publishable self-assessment; STAR Level 1 |
| CSA CCM v4.1 | C, T | Voluntary | Mapping hub (ships mappings to 800-171, ATT&CK, DORA) |
| CSA STAR | A | Certification scheme | Level 1 self (first-party); Level 2 third-party |
| CSA AICM v1.1 / AI-CAIQ | C, Q | Voluntary | AI questionnaire if Unbound adds AI features |
| VSA CORE and FULL 2027 | Q | Customer convention | Technology-buyer questionnaire with AI and privacy modules |
| Google VSAQ | Q (historical) | Customer convention | Apache-licensed templates for drafting original questions |
| EDUCAUSE HECVAT 4 | Q | Customer convention | Only if higher-ed foundations are customers |
| NIST CSF 2.0 | C, T | Voluntary | Top-level outcome taxonomy for the answer library |
| NIST SP 800-53 Rev. 5 (5.2.0), 800-53B | C | Voluntary (binding on federal systems) | Control IDs as cross-reference anchors |
| NIST SP 800-171 Rev. 3 | C | Contractual (CUI only) | Not applicable without CUI |
| NIST SSDF 1.1 (and 1.2 draft), SP 800-218A | C | Voluntary | Secure development program basis |
| NIST SP 800-61 Rev. 3 | C | Voluntary | Incident response program |
| NIST SP 800-63-4 | C | Voluntary | Donor and staff authentication design |
| NIST SP 800-161 Rev. 1, ISO/IEC 27036 | C | Voluntary | Supplier risk management |
| NIST SP 800-88 Rev. 2 | C | Voluntary | Data disposal answers |
| NIST SP 800-207, IR 8397 | G, C | Voluntary | Architecture vocabulary; minimum verification techniques |
| CIS Controls v8.1, CIS Benchmarks | C | Voluntary | Corporate IT baseline (IG1); hardening |
| AICPA TSC 2017 (2022 PoF), 2027 draft, SOC 2 Guide, SSAE 18 | A | Certification criteria | SOC 2 readiness; the dominant assurance ask from US financial customers |
| AICPA SOC for Supply Chain | A | Certification criteria | Not suited to a SaaS service organization |
| ISO/IEC 27001, 27002, 27017, 27018 | A, C | Certification criteria (27001) and voluntary | Alternative or complement to SOC 2 |
| OWASP ASVS 5.0.0 | C | Voluntary | Application requirement catalog (Level 2 target) |
| OWASP Top 10:2025, API Top 10 2023, WSTG 4.2, Cheat Sheets | T, G | Voluntary | Test scope vocabulary; developer guidance |
| OWASP SAMM v2, BSIMM16 | C, G | Voluntary | Honest maturity statements |
| MITRE CWE 5.0, CWE Top 25 (2025), CAPEC 3.9, ATT&CK v20.1, ATLAS | T | Voluntary | Classifying findings and threats |
| PCI DSS v4.0.1, PCI SSF | A, C | Contractual (card brands) | Only if card data is in scope (not established) |
| SLSA 1.2, OpenSSF Scorecard, S2C2F, OSPS Baseline | C | Voluntary | Build provenance and dependency hygiene |
| SPDX 3.0.1 (ISO/IEC 5962 = 2.2.1), CycloneDX 1.7 (ECMA-424 2nd ed.), OpenVEX 0.2.0 | T | Voluntary | SBOM and VEX formats |
| CISA 2026 SBOM Minimum Elements | C | Voluntary | SBOM content baseline buyers will cite |
| OMB M-26-05 (M-22-18 rescinded), CISA attestation form | L (federal agencies) | Binding on agencies only | Federal context; SBOM on request norm |
| CISA Secure by Design pledge | G | Voluntary | Optional public commitment |
| CVSS 4.0, EPSS, CISA KEV, BOD 26-04 (BOD 22-01 revoked) | T, L (agencies) | Voluntary for Echelon | Vulnerability prioritization and SLAs |
| ISO/IEC 29147, 30111 | C | Voluntary | Vulnerability disclosure policy |
| FedRAMP, GovRAMP, TX-RAMP, CMMC, FAR, 2 CFR 200 | A, L | Binding in government procurement only | Not applicable to the DAF sponsor market |
| ISO 22301, 22313, ISO/IEC 27031, NIST SP 800-34, BCI GPG 7.0, DRII PP | C | Voluntary | Continuity and recovery program |
| WCAG 2.2 and 2.1, ITI VPAT 2.5Rev, Section 508, EN 301 549, ADA, EAA | C, A, L | Mixed (see matrix) | Accessibility conformance report for donor UI |
| ISO/IEC 20000-1, ISO 37301 | C | Voluntary (certifiable) | Low demand; structural reference |
| Software escrow practice | Contract ask | Customer convention | Plausible ask from bank-affiliated customers |
| GDPR, UK GDPR (with DUAA 2025), SCCs, DPF, EDPB 07/2020 | L, G | Binding where applicable | Conditional on EU or UK data flows |
| CCPA/CPRA and CPPA 2025 regulations | L | Binding on covered businesses | Conditional (see matrix) |
| US state privacy and breach laws | L | Binding | Breach laws likely; privacy laws conditional |
| Regulation P (GLBA) | L | Binding on financial institutions | Indirect via affiliated financial institutions |
| NIST Privacy Framework, ISO/IEC 27701:2025, AICPA privacy criteria | C, A | Voluntary or certification | Privacy program structure |
| PIPEDA | L | Binding in Canada | Unlikely |
| NIST AI RMF 1.0, AI 600-1, AI 100-2 E2025 | C, T | Voluntary | AI governance and AI threat vocabulary |
| ISO/IEC 42001, 23894, 42005, 42006 | A, C | Certification criteria and voluntary | Future AI management system; impact assessment template |
| OWASP LLM Top 10 2026, Agentic Top 10 2026, AI Exchange | T, G | Voluntary | AI feature and internal agent security |
| EU AI Act (as amended), Colorado SB 26-189, CPPA ADMT rules, EO 14365 | L | Binding where applicable | Conditional (see matrix) |
| SR 26-2 (SR 11-7 superseded) | S | Supervisory expectation | Bank-affiliated customers may treat Unbound logic as a vendor model |
| Treasury AI report (2024), NAIC AI bulletin | G, S | Informational; insurer guidance | Context only; NAIC not applicable |

## 3. Which questionnaires derive from which frameworks

Derivations below are stated by the questionnaire issuer unless marked otherwise.
Echelon should maintain one canonical answer per control concern and map outward.

| Questionnaire | Derived from or mapped to (per issuer) | Notes |
|---|---|---|
| SIG (Shared Assessments) | Issuer SIG page lists direct mappings including Shared Assessments SCA 2026, ISO/IEC 27001:2022, 27002:2022, 27701, 42001, NIST AI 100-1, NIST SP 800-161r1, 800-53 (5.1.1), 800-171r3, NIST CSF 1.1 and 2.0, NIST Privacy Framework, CMMC 2.0, CIS Controls v8, PCI DSS 4.0, DORA, EBA outsourcing guidelines, GDPR, NIS 2, Interagency TPRM Guidance 2023, FedRAMP, FFIEC CAT and IT Handbook booklets, HIPAA | 21 risk domains including Artificial Intelligence; the SCA is the companion test procedure set |
| CAIQ v4.1 | Built on CCM v4.1; CCM v4.1 ships mappings including NIST SP 800-171 rev.2, MITRE ATT&CK v17.1 and a DORA reverse mapping | CAIQ is the yes/no question form of CCM controls; STAR Level 1 submission requires the STAR version |
| AI-CAIQ | Built on AICM v1.1, which maps to ISO/IEC 42001, ISO/IEC 27001, BSI AIC4, EU AI Act, NIST AI RMF and AI 600-1, and AIUC-1 | Role-based guidance (model provider, orchestrated service provider, application provider, AI customer, cloud provider) |
| VSA CORE and FULL 2027 | Issuer states CORE is a strict subset of FULL; no framework mapping stated on the fetched page | Adds AI and regional privacy modules in 2027 |
| HECVAT 4 | Not verified; search results describe AI, privacy and accessibility additions | Issuer site blocked |
| VPAT 2.5Rev (ACR) | Revised Section 508, EN 301 549, WCAG 2.0, 2.1 and 2.2 (issuer page) | EU edition (April 2025) predates EN 301 549 V4.1.1 |
| CISA Secure Software Development Attestation Form | NIST SSDF (SP 800-218) practices, per M-22-18 lineage | Now optional for agencies under M-26-05 |
| Bank and sponsor custom questionnaires | Commonly organized around NIST CSF, FFIEC booklets and the 2023 Interagency TPRM Guidance (not verified per customer) | See financial-services register |

## 4. Licensing constraints that limit Echelon's reuse

Operating contract rule 5 applies: write original questions and answers, cite source and
locator only. The table records what each issuer's terms add.

| Source family | Terms observed | Practical constraint for Echelon |
|---|---|---|
| Shared Assessments SIG and SCA | Paid license (issuer page shows USD 7,000 per year corporate license or membership); proprietary | Never copy question text; answer customer-supplied SIG files only; cite domain or question IDs |
| CSA CCM, CAIQ, AICM | Free download. Website terms: publications may be used, copied and printed, not modified or translated without consent; notices retained. CCM page: a license is needed to customize or use commercially (products, consulting), not for internal use | Completing and publishing a CAIQ about Unbound is fine; embedding CCM or CAIQ content in an Echelon product or paid service needs a CSA license |
| VSA | Limited license only to evaluate one's own processes and direct vendors or to give feedback; use in security consulting or hosted vendor-management services prohibited | Answer only; do not host or redistribute VSA content in any Echelon tool |
| HECVAT | Not confirmed; copyright and trademark reported | Treat as restricted |
| ISO and ISO/IEC standards | Copyrighted, sold per copy (IEC Webstore prices CHF 67 to 227; ISO/IEC 5962 and amendments CHF 0) | Cite clause and control numbers; paraphrase; purchase before relying on exact text |
| PCI SSC | Click-through license; internal study copies only; no derivatives (per search excerpts of the agreement) | Do not reproduce requirements; cite requirement numbers |
| AICPA TSC, guides, SSAEs | Copyright; free account download for TSC; guides sold; standards for own professional use | Cite criteria IDs (for example CC6.1); no reproduction of points of focus |
| CIS Controls | CC BY-NC-ND 4.0 | No derivatives and no commercial redistribution; cite safeguard IDs |
| CIS Benchmarks (PDF) | CC BY-NC-SA 4.0; tooling via paid membership | Non-commercial use; share-alike if adapted |
| NIST publications | Not subject to US copyright; foreign rights reserved with a broad license | Reusable with citation |
| US federal and CISA documents, OMB memos, CFR | US government works | Reusable with citation |
| EU legal acts (EUR-Lex) | Reusable with acknowledgment; OJ is authentic | Reusable |
| OWASP projects (ASVS, SAMM, API Top 10, WSTG, Cheat Sheets, GenAI project) | CC BY-SA 4.0 where confirmed | Reusable with attribution; adapted text must be shared alike, which affects any Echelon-published derivative |
| MITRE CWE, CAPEC, ATT&CK | Royalty-free license for research, development and commercial use; reproduce MITRE copyright and license | Reusable with notice |
| MITRE ATLAS data, Google VSAQ, OpenSSF Scorecard, OSPS Baseline, CycloneDX spec | Apache License 2.0 | Reusable with notice |
| SLSA, SPDX 3.0.1, S2C2F | Community Specification License 1.0 (SPDX pre-existing parts CC BY 3.0) | Reusable under those terms |
| OpenVEX | CC0 1.0 | Unrestricted |
| FIRST CVSS | Use with attribution; publishers must provide score and vector | Always publish vector strings |
| W3C WCAG | W3C Document License: copy and distribute unmodified with notice | Quote success criteria with notice; do not modify |
| ETSI EN 301 549 | No reproduction without authorization except extracts strictly necessary for implementation | Cite clause numbers |
| BCI GPG, DRII, BSIMM, IAPP tracker, NCSL | Proprietary or member content | Cite only |

## 5. Privacy and AI regulatory applicability matrix

Ratings: **Applies** (binding on Echelon or Unbound now), **Likely** (binding once
Unbound operates with customers), **Conditional** (depends on a fact not yet
established), **Indirect** (reaches Echelon only through a customer's obligations and
contract), **Unlikely**, **Not applicable**. Confidence: High, Medium, Low.

| Source | Who it binds | How it reaches Echelon or Unbound | Rating | Confidence | Open questions |
|---|---|---|---|---|---|
| State data breach notification laws (`SRC-STATE-BREACH-LAWS`) | Entities that own or maintain personal information of state residents | Unbound will maintain donor personal information on behalf of sponsors; most statutes require a maintaining third party to notify the data owner | Likely | High in principle; details per state | Which data elements Unbound stores (SSN, account numbers, credentials) changes which statutes trigger |
| State comprehensive privacy laws (`SRC-US-STATE-PRIVACY-LAWS`) | Controllers and processors meeting state thresholds; several states do not exempt nonprofits (to be confirmed) | Sponsors may be controllers; Unbound would be a processor with statutory contract terms | Conditional | Low | Which enacted states cover nonprofit DAF sponsors; entity-level versus data-level GLBA exemptions; sponsor donor counts per state |
| CCPA/CPRA (`SRC-CCPA-CPRA`) | For-profit businesses meeting thresholds | Only via customers that are CCPA businesses, or if Echelon crosses thresholds | Conditional (low) | Medium | Are any customers for-profit businesses (for example a sponsor's commercial affiliate)? |
| CPPA 2025 regulations (`SRC-CPPA-REGS-2025`) | CCPA businesses: risk assessments, cybersecurity audits, ADMT rights | Customers subject to audits may push audit evidence requests to Unbound | Conditional (low) | Medium | Phased compliance dates not captured |
| Regulation P, GLBA (`SRC-GLBA-REG-P`) | Financial institutions under CFPB jurisdiction | Affiliated bank or broker-dealer sharing NPI with Unbound triggers reuse and redisclosure limits and service-provider contract terms | Indirect | Medium-low | Is any target sponsor itself a GLBA financial institution, or only its affiliate? Does Unbound receive NPI from the affiliate (account linkage, transfers in kind)? |
| GDPR (`SRC-GDPR`) | Controllers and processors in the EU, and non-EU ones targeting or monitoring people in the EU | Only if Unbound serves EU-resident donors or a GDPR-subject customer engages it | Unlikely | Medium | Will any sponsor knowingly serve EU-resident donors? |
| UK GDPR, DPA 2018, DUAA 2025 (`SRC-UK-GDPR`) | Same pattern for the UK | Same | Unlikely | Medium | Same, for UK residents |
| EU SCCs and EU-U.S. DPF (`SRC-EU-SCC-2021`, `SRC-EU-US-DPF`) | Parties to EU transfers; DPF self-certified US organizations | Only with an EU data flow | Unlikely | Medium | DPF appeal outcome at the Court of Justice |
| PIPEDA (`SRC-CAN-PIPEDA`) | Organizations in commercial activity in Canada | Only with Canadian donors or customers | Unlikely | Medium | None now |
| EU AI Act as amended (`SRC-EU-AI-ACT`, `SRC-EU-AI-OMNIBUS-2026`) | Providers and deployers with EU market or EU output use | No EU market established; DAF administration is not an Annex III category on its face | Not applicable now (conditional) | Medium | Any EU-facing AI feature; general-purpose AI model use is via third-party providers |
| Colorado SB 26-189 ADMT (`SRC-COLORADO-SB26-189`) | Developers and deployers of covered ADMT used for consequential decisions (includes financial or lending services) about Colorado individuals | Unbound would be a developer only if sponsors use Unbound ADMT to materially influence consequential decisions about individuals | Conditional (low) | Low | Is donor account approval, fraud hold or grant denial a consequential decision under the Act? Exemption text for federally regulated or GLBA entities; deployer and consumer-rights start dates |
| Other state AI laws (`SRC-US-STATE-AI-LAWS`) | Varies | Mostly employment, chatbot disclosure or sector-specific; little DAF overlap verified | Conditional (low) | Low | Inventory not completed; federal preemption efforts (EO 14365) |
| EO 14365 (`SRC-EO-14365`) | Federal executive branch | Signal only; does not bind Echelon | Not applicable | Medium | Text not read |
| SR 26-2 model risk guidance (`SRC-SR-26-2`) | Banking organizations (most relevant above USD 30 billion in assets) | Bank-affiliated customers may inventory Unbound scoring, screening or AI components as vendor models and request documentation, validation support and change notice | Indirect | Medium | Will any Unbound logic (for example grant eligibility screening or fraud scoring) be classed as a model by a customer? Guidance attachment not read |
| NIST AI RMF and AI 600-1 | No one (voluntary) | Customer convention; likely AI questionnaire basis | Indirect (customer convention) | High | Does Unbound plan any AI feature in its first release? |
| ISO/IEC 42001 | No one (voluntary certification) | Occasional enterprise ask | Unlikely near term | Medium | Timing relative to SOC 2 |
| NAIC AI bulletin | Insurers in adopting states | None | Not applicable | High | None |
| Treasury AI report | No one | Context for bank customer expectations | Not applicable (informational) | High | None |

## 6. Notable conclusions

1. The near-certain asks from financial-institution-affiliated sponsors are customer
   conventions, not law: a SIG (Lite or Core) or a bank-built questionnaire, and a SOC 2
   Type 2 report. The AICPA has exposed proposed 2027 TSC, so Unbound's first SOC 2 may
   be tested against revised criteria; readiness work should track the draft.
2. The only privacy obligations that are likely to bind Unbound directly once it
   operates are state breach notification duties of a data maintainer. Everything else
   is conditional on facts not yet established (nonprofit coverage under specific state
   privacy laws, GLBA status of sponsors, EU or UK data flows).
3. AI regulation is currently a low and conditional risk for Unbound. The two largest
   regimes moved: the EU AI Act high-risk dates slipped to 2027-12-02 and 2028-08-02,
   and Colorado replaced its AI Act with an ADMT law whose developer duties start
   2027-01-01. Bank-affiliated customers' model risk programs (now SR 26-2) are the more
   probable channel for AI-related diligence.
4. Several federal software-supply-chain mandates that questionnaires still cite are
   gone or replaced (M-22-18, M-23-16, BOD 22-01, NTIA 2021 SBOM elements). Answers
   should cite current sources and note the change rather than claim compliance with a
   rescinded mandate.
5. Licensing limits reuse more than expected: VSA prohibits use in consulting or hosted
   vendor-management services, CCM and CAIQ need a CSA license for commercial embedding,
   and CIS Controls are no-derivatives. Echelon's answer library must stay original and
   reference these by identifier only.

## 7. Open questions

These belong in `research/open-questions.jsonl`; they are listed here because this task
was limited to the source files and this note.

1. Confirm whether Shared Assessments SIG 2027 has been released and its change log
   (issuer site requires sign-in for automated clients).
2. Confirm HECVAT current build and terms of use (EDUCAUSE site returned HTTP 403).
3. Confirm PCI Secure Software and Secure SLC Standard version numbers.
4. Determine whether Unbound will ever store, process or transmit card data.
5. Identify which enacted state comprehensive privacy laws cover nonprofit DAF sponsors
   and their processors, and how each treats GLBA.
6. Determine whether any target sponsor is itself a GLBA financial institution, and
   whether Unbound will receive NPI from an affiliated institution.
7. Read the full text of Colorado SB 26-189 for exemptions and start dates, and assess
   whether any Unbound decision is a consequential decision.
8. Read the SR 26-2 attachment to see whether it addresses vendor models and AI
   explicitly.
9. Capture CPPA 2025 regulation phase-in dates for cybersecurity audits and ADMT.
10. Confirm CMMC Phase 2 status and the BOD 26-04 remediation timelines (both blocked
    for automated access).
11. Record the comment deadline and planned effective date of the proposed 2027 SOC 2
    TSC.
