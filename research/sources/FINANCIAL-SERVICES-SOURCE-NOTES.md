---
id: DD-SRC-FIN-001
title: Financial Services Source Notes and Regulatory Applicability Matrix
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [due-diligence, sources, financial-services, regulatory-applicability]
---

# Financial Services Source Notes and Regulatory Applicability Matrix

Companion to `sources/financial-services.jsonl` (66 records: the 57 pre-allocated
`financial-services` IDs from `sources/SEED-IDS.json` plus 9 sources discovered in this
pass). All facts were checked on 2026-11-25 against issuer sites or authoritative mirrors
(Federal Register API and govinfo, eCFR API, member-agency transmittals for FFIEC
material). Where a fact could not be confirmed, the JSONL record says so and uses
`unknown`. This note does not restate requirement text and is not legal advice.

## 1. Echelon's position in the payment and supervision chain

- Unbound is DAF administration software and a third-party service provider to DAF
  sponsors. Sponsors are 501(c)(3) public charities: national charities, community
  foundations and financial-institution-affiliated sponsors.
- Under Unbound clause `CNV-PAY-001` the sponsor is the ACH Originator and Unbound is a
  Nacha Third-Party Service Provider (TPSP). Echelon does not hold or transmit funds.
- Echelon has no production deployment, no SOC report and no bank or broker-dealer
  customer today (see `architecture/ECHELON-CURRENT-STATE-BRIEF.md`).

The consequence is that almost no financial regulation binds Echelon by its own terms.
Most of the regulatory weight reaches Echelon second hand, through sponsors' contracts,
their banks, and the affiliates of financial-institution-affiliated sponsors.

## 2. Landscape summary

### 2.1 Rules that bind Echelon directly (3)

1. **OFAC sanctions (SRC-OFAC-REGS).** Applies to every U.S. person, strict liability.
   Echelon must not deal with blocked persons or facilitate prohibited transactions, and
   grant routing makes sanctions screening support a core diligence topic.
2. **Nacha fraud monitoring (SRC-NACHA-FRAUD-MONITORING-2026)** and **the Nacha Operating
   Rules generally (SRC-NACHA-RULES).** As a TPSP performing ACH functions for an
   Originator, Unbound must have risk-based fraud monitoring processes reviewed at least
   annually. Phase 2 removed the volume threshold, so this now applies regardless of
   Unbound's volume. Enforcement is contractual (sponsor and ODFI agreements) and through
   Nacha's rules enforcement process rather than by statute.

### 2.2 Rules that bind sponsors and flow down to Unbound (19)

DAF tax law is the heart of the product: IRC 4966 (taxable distributions), 4967
(prohibited benefits), 4958 (automatic excess benefit for donors and advisors), 170
(deduction and the DAF written acknowledgment rule) and the Pension Protection Act of
2006 that created them. Form 990 Schedule D, Publication 1771, IRS exempt organization
data, FASB ASC 958, UCC Article 4A, OFAC's compliance framework, Treasury's charity
guidelines, COSO, UPMIFA and state unclaimed property and charitable solicitation laws
also bind or guide sponsors and become Unbound product or contract requirements.
Echelon is not the taxpayer or filer, but defects in Unbound grant controls become
sponsor tax exposure and therefore Echelon contract liability.

### 2.3 Rules that apply only if a particular customer type is served (33)

- **Bank and credit union customers or ODFI review:** interagency TPRM guidance and its
  agency transmittals, FFIEC IT Handbook booklets, FFIEC authentication guidance, the
  Interagency Information Security Standards, the Bank Service Company Act and the
  computer-security incident notification rule. These become live if a bank trust
  department or bank-affiliated entity uses Unbound, or if a sponsor's ODFI or bank
  examines the sponsor's payment vendors. The BSCA would also allow federal banking
  agencies to examine Echelon directly in that case.
- **Broker-dealer or adviser affiliates of financial-institution-affiliated sponsors:**
  Regulation S-P (72-hour service provider breach notice), Regulation S-ID, Advisers Act
  rules 206(4)-7 and 204-2, Exchange Act rule 17a-4, FINRA rules 3110 and 4370 and
  Regulatory Notice 21-29, the FinCEN investment adviser AML rule (effective 2028). The
  sponsor charity itself is not a covered firm; these apply only if an affiliate shares
  customer information with Unbound or relies on it for a regulated function.
- **New York DFS covered entities:** 23 NYCRR 500.11 third-party service provider policy.
- **Public company parents:** SOX 404 and the SEC cybersecurity disclosure rule, which
  would show up as SOC 1 requests or third-party risk questionnaires.
- **GLBA and the FTC Safeguards Rule** are rated customer-type dependent or flow-down
  because whether a charity sponsor, or Echelon itself, is a GLBA "financial
  institution" is unresolved. This is the largest open legal question in this register.

### 2.4 Not applicable (11)

EU DORA, its RTS on ICT contractual policy, EBA outsourcing and non-ICT third-party
guidelines (no EU financial entity customers); the sunset FFIEC Cybersecurity Assessment
Tool; the withdrawn SEC adviser outsourcing proposal and its withdrawal notice; FinCEN's
2026 AML/CFT program and CDD proposals (Echelon and sponsors are not BSA financial
institutions; the existing CDD rule is rated customer-type dependent only because a
sponsor's bank applies it to the sponsor); the 2026 core service provider statement; and the OCC/FDIC reputation risk
rule, which binds agencies only.

## 3. Status changes verified in this pass

| Item | Finding | Evidence |
|---|---|---|
| FFIEC Cybersecurity Assessment Tool | Sunset. FFIEC statement August 29, 2024; removed from FFIEC website August 31, 2025; no successor designated. Recorded `withdrawn`. | Fed SR 24-7 (2024-11-22), OCC Bulletin 2024-25 |
| FFIEC Outsourcing Technology Services booklet | No retirement notice found. 2004 release confirmed (OCC Bulletin 2004-32, July 15, 2004). A non-authoritative vendor blog reports a February 2026 FFIEC edit removing reputation language. FFIEC site blocked by CAPTCHA, so recorded `unknown`. | OCC Bulletin 2004-32; search results |
| SEC Outsourcing by Investment Advisers proposal (S7-25-22) | Withdrawn June 17, 2025; the SEC said it does not intend to finalize. | 90 FR 25531 (FR Doc. 2025-11110) |
| IRS proposed DAF regulations (REG-142338-07) | Still proposed. No final rule or withdrawal found in the Federal Register through 2026-11-25. Last FR action April 19, 2024 hearing notice. Secondary sources say final 4966 regulations remain on the 2025-2026 Priority Guidance Plan (not verified at IRS). | Federal Register API search |
| Nacha 2026 fraud monitoring | Phase 1 effective March 20, 2026 (ODFIs and parties with 2023 volume of 6 million or more). Phase 2 effective June 19, 2026, a federal holiday, so practical date June 22, 2026 for all other non-consumer Originators, TPSPs and TPSs. Both in effect. | Nacha Phase 1 and Phase 2 rule pages |
| SEC Regulation S-P amendments | Effective August 2, 2024. Compliance 18 months after publication for larger entities (December 3, 2025) and 24 months for smaller entities (June 3, 2026). Both passed. Dates computed from the release text. | 89 FR 47688 |
| NYDFS Part 500 Second Amendment | Effective November 1, 2023, with phases at 180 days, one year, 18 months and two years. Final phase (MFA for all access, asset inventory) November 1, 2025. All phases passed. | DFS-hosted official amendment text |
| DORA | Applies from January 17, 2025 (Article 64). | EUR-Lex |
| Interagency TPRM guidance (2023) | Still current, but on September 15, 2026 the OCC, Fed, FDIC and NCUA proposed replacement guidance that would replace the 2023 guidance and the community bank guide; comments extended to December 16, 2026. | 91 FR 58536; 91 FR 74279 |
| EBA Outsourcing Guidelines (2019) | Final Guidelines on non-ICT third-party risk published September 18, 2026; not yet applicable; will repeal the 2019 guidelines once applicable. | EBA page |
| IRC 170 | Amended by Pub. L. 119-21 (July 4, 2025): 0.5 percent floor and a non-itemizer cash deduction that excludes DAF contributions. | LII mirror of 26 U.S.C. 170 |
| Interagency Information Security Standards | Supplement A amended by the OCC/FDIC reputation risk final rule, effective June 9, 2026. | 91 FR 18279; eCFR API |
| FinCEN investment adviser AML rule | Effective date delayed from January 1, 2026 to January 1, 2028. | 91 FR 36 |
| FinCEN CDD and AML/CFT program rules | New proposals April 10, 2026 (program reform) and November 19, 2026 (CDD). | 91 FR 18704; 91 FR 74514 |

## 4. Contradictions and uncertainties

- **Nacha Phase 2 date.** Nacha pages say both June 19 and June 22, 2026. Resolved: June 19
  is the nominal effective date and a federal holiday, so June 22 is the practical date.
- **EBA outsourcing guidelines status.** The EBA page navigation labels the 2019
  outsourcing guidelines "repealed" while the same page says the replacement is "not yet
  applicable" and will repeal them "once applicable". Recorded as `current` pending an
  application date. Unresolved.
- **Community bank guide title.** The OCC bulletin says "Third-Party Relationships: A Guide
  for Community Banks"; the 2026 Federal Register proposal says "Third-Party Risk
  Management: A Guide for Community Banks". Same issuance.
- **FFIEC material.** All FFIEC pages returned CAPTCHA blocks. Booklet dates rest on
  Federal Reserve and OCC transmittals, which are authoritative mirrors, but current
  booklet text (including reported 2026 reputation edits) is unconfirmed.
- **Treasury charity guidelines.** The only Treasury-hosted copy sits under an
  "archive-documents" path with 2003 file metadata, while the Federal Register shows a
  2006 update. Whether Treasury treats the guidelines as current is unknown.
- **GLBA coverage.** Whether DAF sponsors or Echelon are GLBA financial institutions, and
  whether the FTC has jurisdiction over nonprofit sponsors, is not resolved here.
- **Nacha TPSP obligations.** The rule pages confirm fraud monitoring and data security
  obligations for TPSPs. Whether the annual Rules compliance audit and other duties
  attach to a TPSP that does not transmit files to the ODFI needs confirmation from the
  paid rule text.
- **Unverified records (12).** SRC-FFIEC-IT-HANDBOOK, SRC-FFIEC-BCM-BOOKLET,
  SRC-FFIEC-OUTSOURCING-BOOKLET, SRC-INTERAGENCY-GLBA-SAFEGUARDS, SRC-SEC-17A-4,
  SRC-TREASURY-CHARITY-GUIDELINES, SRC-IRS-TEOS, SRC-FASB-ASC-958, SRC-UPMIFA,
  SRC-UCC-4A, SRC-STATE-UNCLAIMED-PROPERTY and SRC-STATE-CHARITABLE-SOLICITATION are kept
  with `verified: false` and explain what is missing.
- **Mirrors and URLs.** Statutes were checked on the Cornell LII mirror, not the official
  U.S. Code site. Several eCFR records use the eCFR API endpoint as `url` because the
  human-readable eCFR pages block scripted access; replace with page URLs when confirmed.

## 5. Notable applicability conclusions

1. Echelon is not a bank service provider today. Bank TPRM and FFIEC material is the
   vocabulary of vendor questionnaires, but it becomes binding on Echelon only if a bank
   is a customer (BSCA examination exposure, 12 CFR 53.4 notice). Do not overstate it to
   charity sponsors, and do not ignore it for bank-affiliated prospects.
2. Nacha is Echelon's most direct financial-services obligation. Fraud monitoring is in
   force for Unbound as a TPSP now; account-number encryption at rest is legally required
   only above 2 million entries but will be expected by every sponsor and ODFI.
3. For financial-institution-affiliated sponsors, the flow-down risk comes from the
   affiliate, not the charity: Regulation S-P's 72-hour breach notice to the covered
   institution is the most concrete term to plan for if brokerage data is shared.
4. DAF tax rules are where Unbound's product correctness is legally consequential. The
   2023 proposed regulations remain proposed and must be treated as design-for-target,
   not current law. The 2025 change excluding DAF gifts from the non-itemizer deduction
   needs to be reflected in donor-facing content.
5. EU regimes are not applicable and should be answered as such.

## 6. Regulatory applicability matrix

Applicability ratings: **Direct** = binds Echelon directly; **Flow-down** = binds
Echelon's customer and flows down by contract or supervisory expectation;
**Customer-type dependent** = applies only if a particular customer type is served;
**Not applicable**. Confidence reflects verification and legal clarity.

| Source ID | Who it binds | How it reaches Echelon/Unbound | Applicability | Confidence | Open questions |
|---|---|---|---|---|---|
| SRC-INTERAGENCY-TPRM-2023 | Fed, FDIC, OCC supervised banks | Bank or bank-affiliated customer, or ODFI vendor review; questionnaires and contract terms | Customer-type dependent | High | Replacement pending (2026 proposal) |
| SRC-OCC-BULLETIN-2023-17 | OCC-supervised banks | As above | Customer-type dependent | High | None |
| SRC-FDIC-FIL-29-2023 | FDIC-supervised banks | As above; community banks serving community foundations | Customer-type dependent | High | None |
| SRC-FRB-SR-23-4 | Fed-supervised banking organizations | As above | Customer-type dependent | High | None |
| SRC-TPRM-COMMUNITY-BANK-GUIDE-2024 | No one (resource) | Shapes community bank questionnaires | Customer-type dependent | High | Replacement pending |
| SRC-FFIEC-IT-HANDBOOK | Banks, credit unions; examined TSPs | Bank customers; BSCA examination | Customer-type dependent | Medium (unverified) | FFIEC site unreadable; 2026 edits unconfirmed |
| SRC-FFIEC-IS-BOOKLET | Banks, credit unions; examined TSPs | Bank customers; questionnaire vocabulary | Customer-type dependent | Medium | Possible 2026 text edits |
| SRC-FFIEC-BCM-BOOKLET | Banks, credit unions; examined TSPs | Bank customers | Customer-type dependent | Medium (unverified) | Exact release day |
| SRC-FFIEC-DAM-BOOKLET | Banks, credit unions; examined TSPs | Bank customers; SDLC evidence | Customer-type dependent | High | None |
| SRC-FFIEC-ARCHITECTURE-BOOKLET | Banks, credit unions; examined TSPs | Bank customers | Customer-type dependent | High | None |
| SRC-FFIEC-OUTSOURCING-BOOKLET | Banks, credit unions | Bank customers | Customer-type dependent | Low (unverified) | Current status and revision date |
| SRC-FFIEC-AUTH-GUIDANCE-2021 | Banks, credit unions | Bank customers; MFA design reference | Customer-type dependent | High | None |
| SRC-FFIEC-CAT | No one (sunset) | Legacy questionnaires only | Not applicable | High | None |
| SRC-BSCA | Insured depository institutions and their service providers | Only if Echelon serves a bank | Customer-type dependent | High | Would any planned customer be a bank trust department? |
| SRC-CIRN-RULE-2021 | Banking organizations; bank service providers | Only if Echelon is a BSCA bank service provider | Customer-type dependent | High | Confirm 4-hour trigger wording in 12 CFR 53.4 |
| SRC-GLBA | Financial institutions | Contract safeguards; redisclosure limits | Flow-down | Low | Are sponsors or Echelon GLBA financial institutions? |
| SRC-INTERAGENCY-GLBA-SAFEGUARDS | Banks | Bank customers' service provider oversight | Customer-type dependent | Medium (unverified) | Trace 2026-04-10 eCFR change |
| SRC-FTC-SAFEGUARDS-RULE | Non-bank financial institutions under FTC | Benchmark; direct only if Echelon is a financial institution | Customer-type dependent | Low | FTC jurisdiction over sponsors and Echelon |
| SRC-SEC-REG-SP-2024 | Broker-dealers, advisers, funds, transfer agents | Affiliate of FI-affiliated sponsor sharing customer data; 72-hour notice | Customer-type dependent | High | Will any affiliate share customer information? |
| SRC-SEC-REG-S-ID | SEC-regulated firms with covered accounts | Only via BD or RIA affiliate | Customer-type dependent | Medium | None |
| SRC-SEC-CYBER-DISCLOSURE-2023 | Public issuers | Public parent's TPRM process | Customer-type dependent | Medium | None |
| SRC-SEC-ADVISERS-COMPLIANCE-RULE | Registered advisers | Adviser affiliate reliance | Customer-type dependent | Medium | None |
| SRC-SEC-ADVISERS-BOOKS-RECORDS | Registered advisers | Only if adviser records stored on Unbound | Customer-type dependent | Medium | None |
| SRC-SEC-17A-4 | Broker-dealers | Only if BD records stored on Unbound | Customer-type dependent | Medium (unverified) | Confirm 2022 amendment citation |
| SRC-SEC-ADVISER-OUTSOURCING-PROPOSAL | No one (withdrawn) | Legacy questionnaires only | Not applicable | High | None |
| SRC-FINRA-RULE-3110 | FINRA members | BD affiliate outsourcing supervision | Customer-type dependent | High | Latest amendment |
| SRC-FINRA-RN-21-29 | FINRA members (guidance) | BD affiliate vendor diligence | Customer-type dependent | High | None |
| SRC-FINRA-RULE-4370 | FINRA members | BD affiliate BCP | Customer-type dependent | High | None |
| SRC-FINRA-CYBER-GUIDANCE | FINRA members (guidance) | BD affiliate questionnaires (third-party risk, GenAI) | Customer-type dependent | Medium | 2027 report expected |
| SRC-NYDFS-PART-500 | DFS covered entities | Affiliate or NY trust company customer; 500.11 TPSP policy | Customer-type dependent | High | Any DFS-licensed affiliate in scope? |
| SRC-NACHA-RULES | DFIs by agreement; Originators and TPSPs via agreements | Unbound is a TPSP under CNV-PAY-001 | Direct | Medium | Which TPSP duties (Rules compliance audit) apply |
| SRC-NACHA-DATA-SECURITY | Non-FI Originators, TPSPs, TPSs above 2M entries | Only above volume threshold | Customer-type dependent | High | Projected Unbound ACH volume |
| SRC-NACHA-FRAUD-MONITORING-2026 | All non-consumer Originators, TPSPs, TPSs; ODFIs | Unbound as TPSP, in effect since June 2026 | Direct | High | How sponsor and Unbound split monitoring duties |
| SRC-BSA-AML | BSA financial institutions | Indirect via sponsors' banks and custodians | Customer-type dependent | Medium | Re-check money transmitter status if flows change |
| SRC-FINCEN-CDD-RULE | Covered financial institutions | Not applicable directly | Customer-type dependent | High | None |
| SRC-OFAC-REGS | All U.S. persons | Binds Echelon and every sponsor; screening support | Direct | High | Screening responsibility split in contracts |
| SRC-OFAC-COMPLIANCE-FRAMEWORK | No one (guidance) | Sponsor programs; Echelon's own program | Flow-down | High | None |
| SRC-TREASURY-CHARITY-GUIDELINES | No one (voluntary) | Sponsor grantee due diligence features | Flow-down | Low (unverified) | Is it still current at Treasury? |
| SRC-IRC-4966 | Sponsors, fund managers | Grant eligibility controls | Flow-down | High | None |
| SRC-IRC-4967 | Donors, advisors, managers | Benefit attestations | Flow-down | High | None |
| SRC-IRC-4958 | Disqualified persons, managers | Payee relationship screening | Flow-down | High | Could Echelon personnel be disqualified persons? |
| SRC-IRC-170 | Donors; sponsors for acknowledgments | Receipts; donor messaging after Pub. L. 119-21 | Flow-down | High | Effective dates of 2025 changes |
| SRC-PPA-2006 | Sponsors, donors (via codified sections) | See IRC records | Flow-down | High | None |
| SRC-IRS-DAF-PROPOSED-REGS-2023 | Would bind sponsors | Design-for-target configuration | Flow-down | High | Finalization timing and content |
| SRC-IRS-PUB-1771 | No one (explains binding rules) | Acknowledgment templates | Flow-down | High | Newer revision after 2025 law |
| SRC-IRS-TEOS | No one (dataset) | Grantee eligibility data | Flow-down | Medium (unverified) | Bulk data terms; TEOS URL |
| SRC-IRS-FORM-990 | Sponsors (filers) | Schedule D DAF reporting exports | Flow-down | High | None |
| SRC-FASB-ASC-958 | Sponsors (GAAP) | Accounting data; SOC 1 demand | Flow-down | Low (unverified) | Not verified |
| SRC-UPMIFA | Charitable institutions where enacted | Investment and spending reporting | Flow-down | Low (unverified) | Are DAF assets institutional funds? |
| SRC-UCC-4A | Originators and banks in funds transfers | Security procedure and fraud liability in contracts | Flow-down | Low (unverified) | 2022 amendments; not verified |
| SRC-SOX-404 | Public issuers | SOC 1 request from public parent | Customer-type dependent | Medium | None |
| SRC-COSO-2013 | No one (voluntary) | SOC report criteria; auditor expectations | Flow-down | High | None |
| SRC-COSO-ERM-2017 | No one (voluntary) | Larger sponsors' risk functions | Flow-down | Medium | None |
| SRC-EU-DORA | EU financial entities; critical ICT TPPs | None today | Not applicable | High | None |
| SRC-EBA-OUTSOURCING-GL | EU banks and similar | None today | Not applicable | Medium | Repeal timing (page conflicts) |
| SRC-STATE-UNCLAIMED-PROPERTY | Holders (sponsors; Echelon for own property) | Uncashed grant tracking and reporting | Flow-down | Low (unverified) | Not verified; state variation |
| SRC-STATE-CHARITABLE-SOLICITATION | Soliciting charities; some intermediaries | Possible platform or fundraiser status | Flow-down | Low (unverified) | Not verified; counsel review |
| SRC-INTERAGENCY-TPRM-PROPOSAL-2026 | Would bind banks and credit unions (guidance) | Future bank or credit union customers | Customer-type dependent | High | Final content and timing |
| SRC-INTERAGENCY-CORE-PROVIDER-STATEMENT-2026 | Agencies; core providers | Not a core provider | Not applicable | High | None |
| SRC-SEC-PROPOSAL-WITHDRAWAL-2025 | No one | Evidence of withdrawal | Not applicable | High | None |
| SRC-FINCEN-AMLCFT-PROGRAM-PROPOSAL-2026 | Would bind BSA financial institutions | Not applicable | Not applicable | High | Final rule timing |
| SRC-FINCEN-CDD-PROPOSAL-2026 | Would bind covered FIs | Not applicable; sponsors' banks may ask more | Not applicable | High | Final rule content |
| SRC-FINCEN-IA-AML-RULE-2024 | Advisers from 2028-01-01 | Adviser affiliates only | Customer-type dependent | High | Further delay or change |
| SRC-OCC-FDIC-REPUTATION-RISK-RULE-2026 | OCC and FDIC | Indirect: changes bank guidance text | Not applicable | High | None |
| SRC-EU-DORA-RTS-2024-1773 | EU financial entities | None today | Not applicable | High | None |
| SRC-EBA-NON-ICT-TPRM-GL-2026 | EU banks and similar (once applicable) | None today | Not applicable | Medium | Application date |

