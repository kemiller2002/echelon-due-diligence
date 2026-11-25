---
id: DD-PRD-UNB-001
title: Unbound due diligence profile
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [due-diligence, unbound, product-profile, donor-advised-funds]
related_documents:
  - gap-analysis/UNBOUND-REQUIREMENTS-GAP-ANALYSIS.md
  - product-profiles/unbound/proposed-requirements.jsonl
  - industry-profiles/donor-advised-funds/DAF-SPONSOR-TECHNOLOGY-PROCUREMENT-PROFILE.md
  - architecture/ECHELON-CURRENT-STATE-BRIEF.md
---

# Unbound due diligence profile

## 1. Position in one paragraph

Unbound is a DAF administration platform that exists only as requirements
(`unbound@9b38de47`): 1,653 baseline records, 82 convergence clauses and a 90-control
matrix whose controls are all status Designed with no operating evidence. There is no
production system, customer, SOC report, penetration test, certification or insurance
policy (DD-ARC-001). The honest answer to almost every diligence question is therefore
"designed, not built". What distinguishes Unbound is the quality of its business-control
design (sponsor authority, sanctions, payment roles, reconciliation, tenant isolation,
AI authority limits). What blocks a sale is the absence of the security program,
infrastructure decisions, contract package and organizational facts that third-party
risk teams check before they read any product control. The gap analysis
(DD-GAP-UNB-001) gives method and evidence; 104 proposed requirements are in
`proposed-requirements.jsonl`.

## 2. Who will assess Unbound

Classifications follow DD-IND-DAF-001: documented, inferred or unknown. Instruments are
the assessor's likely tools; none of them has been received.

| Assessor | Basis | Likely instruments | What decides the outcome |
|---|---|---|---|
| Parent-institution TPRM for bank- and broker-affiliated sponsors (Bank of America Charitable Gift Fund, Morgan Stanley GIFT, Goldman Sachs Philanthropy Fund, possibly DAFgiving360) | Inferred, Medium to High: sponsor administration runs through the parent or an outsourced administrator; parent supplier standards are documented | Parent supplier security standard and addenda, SIG-based questionnaire, interagency TPRM due diligence, onsite or remote assessment, contract security schedule | SOC 2 Type II, penetration test, US-only access, 24-hour breach notice, subprocessor consent, background checks, insurance certificates, financial statements, exit and escrow |
| Fidelity Charitable through FMR supplier process | Inferred, Medium (administration contracted to FMR); more likely competitor or integration counterparty than buyer | Fidelity supplier policies: background investigations, third-party accessibility conformance report, location disclosure | Independent ACR, personnel screening, credential-free integration |
| Independent national sponsors (American Endowment Foundation, Vanguard Charitable, National Philanthropic Trust) | Documented privacy flow-down and confidentiality terms; vendor questionnaires unknown | Vendor questionnaire, SOC 2 request, privacy and DPA review | SOC 2, privacy notice ownership for branded services, confidentiality and processor terms |
| Community foundations | Unknown; inferred to accept vendor-standard assurance | Short security questionnaire or HECVAT-like form, SOC 2 request, references | SOC 2 or credible substitute, references, price, migration support, accessibility |
| Financial institutions buying private-label DAF programs (the NPT GivingPoint market) | Inferred, Medium | Bank TPRM program, FFIEC-aligned questionnaire, regulator access clause | Bank service provider notification, examiner access, resilience, isolation between partners |
| RIAs and broker-dealers distributing a sponsor program | Documented regulatory driver (Regulation S-P) | Regulation S-P service provider oversight review | 72-hour breach notice, data use limits, partner data isolation |
| Sponsor external auditors (user auditors) | Documented in Unbound (`CNV-GOV-001`) | SOC 1 Type II request, CUEC list, direct testing or substantive procedures | SOC 1 scope and timing, CUEC list, IPE evidence, reconciliation controls |
| Sponsor ODFI banks | Documented in Unbound (`CNV-PAY-001`, Nacha) | Nacha TPSP onboarding review, origination agreement terms, fraud monitoring evidence | TPSP versus Third-Party Sender determination, data security, fraud monitoring program |
| Cyber insurers (for Echelon and for sponsors) | Documented application questions | Carrier applications and ransomware supplements | MFA, EDR, immutable backups, payment dual control; answers act as representations |
| Acquirers or investors | Inferred | Technical and legal diligence lists | IP title, license posture, key-person risk, controls evidence |

## 3. The 40 questions that will decide a sale

"Honest current answer" reflects `unbound@9b38de47` and DD-ARC-001. "What changes it"
names proposed requirements; the governing existing requirements are in the gap
analysis.

| # | Question | Concern | Honest current answer | What would change it |
|---|---|---|---|---|
| 1 | DDQ-AUD-0001 | SOC 2 Type II report | None. No auditor engaged. SOC2-036 forbids claiming one | DD-UNB-AUD-001, DD-UNB-GOV-003 |
| 2 | DDQ-PEN-0001 | Independent penetration test | None, and no requirement schedules one | DD-UNB-SEC-008 |
| 3 | DDQ-REG-0005 | Licensing as money transmitter, adviser or broker-dealer | Designed to stay outside these regimes (CNV-LEG-001: no custody, no unilateral payment control, no advice); no counsel opinion | DD-UNB-LEG-001 |
| 4 | DDQ-PAY-0002 | Does the vendor hold or pool funds | No by design (CNV-LEG-001, CNV-PAY-001); the funds-flow conformance check is specified, not built | DD-UNB-LEG-001 |
| 5 | DDQ-PAY-0003 | Can the vendor originate, alter or stop payments | Design: no; only sponsor-adopted, time-bounded protective holds (CNV-PLT-007) | DD-UNB-PAY-001, DD-UNB-LEG-008 |
| 6 | DDQ-TEN-0001 | Multi-tenant architecture | Designed: schema and role per sponsor with row-level security (CNV-ARC-001), but the baseline also states a dedicated-database default | DD-UNB-TEN-001, DD-UNB-TEN-002 |
| 7 | DDQ-ENC-0001 | Encryption at rest | Not specified in requirements | DD-UNB-SEC-001 |
| 8 | DDQ-ENC-0013 | Key management | Unresolved (ADR-006) | DD-UNB-SEC-003 |
| 9 | DDQ-CLD-0001 | Hosting provider | Not chosen | DD-UNB-SEC-021 |
| 10 | DDQ-ISP-0001 | Written security program | None adopted; only the proposed Secure Construction Standard v0.1 | DD-UNB-SEC-020 |
| 11 | DDQ-IR-0015 | Incident notification time | No commitment | DD-UNB-LEG-006, DD-UNB-SEC-016 |
| 12 | DDQ-INS-0001 | Cyber insurance | Unknown; none established | DD-UNB-LEG-003 |
| 13 | DDQ-BCP-0018 | Founder unavailable tomorrow | No succession arrangement or credential custody documented | DD-UNB-BCP-001, DD-UNB-SEC-024 |
| 14 | DDQ-FST-0012 | Continuity if Echelon fails | Sponsor is records custodian with reconciled export (CNV-ENT-002); no escrow, wind-down plan or reserve | DD-UNB-EXIT-004, DD-UNB-EXIT-005 |
| 15 | DDQ-IPR-0006 | PolyForm Noncommercial components | Commercial license is a launch gate (CNV-GOV-009); none executed | DD-UNB-VEND-003 |
| 16 | DDQ-AIG-0027 | Is customer data used to train models | Unknown; no commitment or provider terms inventory | DD-UNB-AIA-001, DD-UNB-AIA-002 |
| 17 | DDQ-AIA-0037 | Can AI coding agents merge or deploy without human approval | Unknown; branch protection and review are not evidenced | DD-UNB-SEC-010, DD-UNB-AIA-003 |
| 18 | DDQ-AIA-0014 | Can AI approve grants or release payments | No by design (CNV-AIO-001; release 1 agents limited to reversible actions at A2 or below) | Build and test; DD-UNB-AIA-004 |
| 19 | DDQ-DAF-0034 | Can vendor staff approve grants or change policy | No by design (CNV-GRT-001, CNV-ARC-002, CNV-GOV-006) | DD-UNB-OPS-003 |
| 20 | DDQ-INV-0006 | Does the platform run sponsor investment pools | No (CNV-LEG-001), but 53 unamended UNB-NAV records describe a pool NAV engine | DD-UNB-FIN-007 |
| 21 | DDQ-AML-0002 | Sanctions screening timing | Strong design: onboarding, list change, before release, fenced at dispatch (CNV-GRT-006); reference matcher unfit and no provider | DD-UNB-AML-001 |
| 22 | DDQ-FRD-0032 | Nacha 2026 fraud monitoring | Accepted by contract (CNV-PAY-001); no program defined | DD-UNB-PAY-003 |
| 23 | DDQ-FRD-0006 | Payee bank change verification | Strong design (REQ-X-005, CNV-PLT-011, CNV-PAY-002) | Build and test |
| 24 | DDQ-TXI-0007 | Exactly-once payment processing | Strong design (CNV-ARC-003, CNV-PAY-004); ACH has no end-to-end key (TVR-PAY-002-Q) | DD-UNB-PAY-006 |
| 25 | DDQ-RCN-0004 | Fund balances reconcile to the GL | Strong design (CNV-FIN-004, CNV-FIN-012); sampling method and break reporting unspecified | DD-UNB-FIN-002 |
| 26 | DDQ-FCT-0017 | SOC 1 Type 2 | None; planned by reliance (CNV-GOV-001); CUEC list deferred | DD-UNB-FIN-006 |
| 27 | DDQ-ACT-0006 | Can posted entries be edited | No by design (ACC-MDL-002, UNB-DATA-001); integrity mechanism undecided | DD-UNB-FIN-005 |
| 28 | DDQ-DCL-0010 | Field-level protection of account numbers and TINs | Not specified | DD-UNB-SEC-004, DD-UNB-PAY-002 |
| 29 | DDQ-PRV-0014 | Safeguards commitment for bank customers | No position; GLBA applicability open | DD-UNB-PRV-003 |
| 30 | DDQ-PRV-0018 | Standard DPA | None | DD-UNB-PRV-002, DD-UNB-LEG-002 |
| 31 | DDQ-SUB-0001 | Published subprocessor list | Specified but Deferred (UNB-XIN-SAS-011) | DD-UNB-VEND-001 |
| 32 | DDQ-PRT-0005 | Export of full fund history | Full reconciled export required (CNV-ENT-002); no published schema | DD-UNB-EXIT-002 |
| 33 | DDQ-PRT-0015 | Import from current administrator | Required with reconciliation report (CNV-EXP-002); no migration specification | DD-UNB-EXIT-001 |
| 34 | DDQ-TRM-0004 | In-flight items at termination | Partly designed (CNV-ENT-002) | DD-UNB-EXIT-003 |
| 35 | DDQ-WLB-0015 | Does embedded content trust host identity | Intended no (INT-015, AIN-029, both one-line Proposed rows); embedding mechanism undecided | DD-UNB-WLB-002 |
| 36 | DDQ-API-0008 | Partner API authentication | Not specified | DD-UNB-API-001 |
| 37 | DDQ-A11Y-0006 | VPAT or ACR | None; WCAG 2.2 AA is a design requirement (CNV-EXP-001) | DD-UNB-A11Y-001, DD-UNB-A11Y-002 |
| 38 | DDQ-DR-0001 | RTO and RPO | Candidate values only; stated per capability in one record and per data class in the governing clause | DD-UNB-BCP-003 |
| 39 | DDQ-VUL-0013 | Vulnerability remediation targets | None | DD-UNB-SEC-006 |
| 40 | DDQ-SDL-0012 | Can a developer merge their own change | Two non-author approvers required for control-relevant modules (CNV-PLT-010); staffing to meet it not established | DD-UNB-SEC-024, DD-UNB-SEC-010 |

## 4. Coverage by scope area

Coverage describes the Unbound requirements, not implementation. Readiness is the
ability to give an assessor a credible, evidenced answer today; nothing is implemented,
so readiness is at most "design reviewable".

Coverage scale: **Strong** (governing clause with acceptance criteria), **Partial**
(clauses exist with material open items), **Thin** (list items, hypotheses or deferred
records only), **None**.

Readiness scale: **Design reviewable** (an assessor can review a coherent design),
**Design with conflicts** (contradictory text must be resolved first), **Not
answerable** (key decision or artifact missing).

| Area | Coverage | Readiness | Key existing requirements | Key question IDs | Key gaps (proposed) |
|---|---|---|---|---|---|
| Donor identity | Strong | Design reviewable | CNV-PLT-003, CNV-PLT-011, AUTH-I7 | DDQ-DON-0001, DDQ-DON-0006, DDQ-AUN-0033 | Proofing vendor (VEND-002), accessible authentication (A11Y-004), death verification (DON-001) |
| Donor privacy | Partial | Not answerable | UNB-DATA-007, UNB-XIN-EVA-014, CNV-TEN-001, CNV-ARC-001 | DDQ-PRV-0007, DDQ-PRV-0025, DDQ-PRV-0044, DDQ-DCL-0014 | PRV-001 to PRV-008, SEC-004 |
| Contributions | Strong for cash; Partial for non-cash | Design reviewable | CNV-FIN-003, CNV-GRT-013, CNV-PAY-005, UNB-RCN-FIN-001 | DDQ-CON-0007, DDQ-CON-0016, DDQ-CON-0029 | FIN-010 |
| Contribution reconciliation | Strong | Design reviewable | CNV-FIN-004, CNV-FIN-013, CNV-FIN-003 | DDQ-RCN-0004, DDQ-RCN-0009, DDQ-CON-0003 | FIN-002 |
| Grant recommendations | Strong | Design reviewable | UNB-GRANT-001, UNB-GRANT-002, UNB-GRANT-029, UNB-RCN-GRT-010, CNV-GRT-016 | DDQ-GRT-0001, DDQ-GRT-0004 | None material |
| Grant approval | Strong | Design reviewable | CNV-GRT-001, CNV-GRT-011, CNV-GOV-003, CNV-FIN-001 | DDQ-GRT-0007, DDQ-GRT-0008, DDQ-AIA-0014 | Staffing for separation of duties (SEC-024) |
| Charity eligibility | Strong | Design reviewable | CNV-GRT-002, CNV-GRT-003, CNV-GRT-015 | DDQ-CHV-0001, DDQ-CHV-0002, DDQ-CHV-0018 | GRT-001, CHV-001 |
| Charity reverification | Strong | Design reviewable | CNV-GRT-003, CNV-GRT-004 | DDQ-CHV-0007, DDQ-CHV-0012 | None material |
| Sanctions screening | Strong | Not answerable | CNV-GRT-006, CNV-PLT-004 | DDQ-AML-0001, DDQ-AML-0002, DDQ-AML-0011 | AML-001 (no fit matcher), LEG-007 |
| Fraud prevention | Partial | Design reviewable | REQ-X-005, CNV-PLT-011, TVR-SEC-004, TVR-SEC-010, UNB-GRANT-044 | DDQ-FRD-0001, DDQ-FRD-0006, DDQ-FRD-0032 | PAY-003 (Nacha program), SEC-018 |
| Grant restrictions | Strong | Design reviewable | UNB-GRANT-010, UNB-GRANT-024, UNB-GRANT-048, CNV-GRT-009, CNV-GRT-014 | DDQ-GRT-0013, DDQ-GRT-0014, DDQ-GRT-0024 | None material |
| Recurring grants | Strong | Design reviewable | UNB-GRANT-003, UNB-GRANT-027, TVR-GR-005, CNV-GRT-010, REQ-X-008 | DDQ-GRT-0018, DDQ-GRT-0021 | None material |
| Scheduled contributions | None | Not answerable | CNV-FIN-003 (no donor ACH debit in release 1) | DDQ-CON-0005 (nearest; no dedicated question) | FIN-001 |
| Financial transaction integrity | Strong | Design reviewable | CNV-ARC-003, CNV-PAY-004, UNB-XIN-EVA-011, CNV-FIN-001 | DDQ-TXI-0001, DDQ-TXI-0007, DDQ-TXI-0018 | PAY-006 |
| Investment allocations | Partial | Design with conflicts | CNV-LEG-001, CNV-FIN-005, CNV-FIN-001 | DDQ-INV-0002, DDQ-INV-0006, DDQ-CUS-0007 | FIN-007, FIN-008, LEG-001 |
| Custodial integrations | Partial | Not answerable | CNV-FIN-013, UNB-CUST-009, UNB-CUST-017 | DDQ-CUS-0002, DDQ-CUS-0021, DDQ-CUS-0022 | FIN-009, FIN-008, VEND-002 |
| Fee calculations | Strong | Design reviewable | CNV-FIN-002, CNV-FIN-006, CNV-ECO-002, CNV-GRT-013 | DDQ-FCT-0012, DDQ-FEE-0008, DDQ-FEE-0013 | FIN-003, FIN-011 |
| Account balances | Strong | Design reviewable | CNV-FIN-001, CNV-FIN-003, CNV-FIN-012, CNV-EXP-003 | DDQ-ACT-0018, DDQ-ACT-0029, DDQ-RCN-0004 | FIN-005 |
| General ledger integrity | Strong | Design reviewable | ACC-MDL-001, ACC-MDL-002, CNV-FIN-011, CNV-FIN-012, UNB-DATA-012 | DDQ-ACT-0001, DDQ-ACT-0006, DDQ-ACT-0009 | FIN-005, GOV-002 |
| Separation of duties | Strong | Not answerable | CNV-GOV-003, GOV-AUTH-004, UNB-ACC-022, CNV-PLT-010 | DDQ-AUZ-0018, DDQ-FCT-0001, DDQ-RCN-0020 | SEC-024 |
| Audit trails | Partial | Design reviewable | UNB-DATA-001, SOC2-025, CNV-PLT-009, CNV-PLT-010 | DDQ-MON-0007, DDQ-MON-0012, DDQ-MON-0028 | SEC-014, FIN-005 |
| Financial reporting | Partial | Design reviewable | CNV-FIN-009, UNB-XIN-NPG-004, UNB-ACC-021, CNV-FIN-012 | DDQ-RRP-0001, DDQ-RRP-0007, DDQ-FCT-0017 | FIN-004, FIN-006 |
| Multi-tenant isolation | Strong | Design with conflicts | CNV-ARC-001, CNV-ARC-002, CNV-TEN-001, ACC-MDL-005 | DDQ-TEN-0001, DDQ-TEN-0006, DDQ-ARC-0024 | TEN-001, TEN-002 |
| White labeling | Partial | Design reviewable | REQ-X-030, REQ-X-045, UNB-RCN-WF-009, CNV-LEG-002 | DDQ-WLB-0001, DDQ-WLB-0006, DDQ-WLB-0009 | PRV-001, WLB-001, WLB-003 |
| Embedded components | Thin | Not answerable | INT-015, AIN-029, MON-022, AUTH-I1, TVR-WID-002 | DDQ-WLB-0011, DDQ-WLB-0014, DDQ-WLB-0015 | WLB-002 |
| External APIs | Partial | Design reviewable | UNB-API-STD-005, UNB-API-006, CNV-EXP-001, CNV-AIO-001 | DDQ-API-0001, DDQ-API-0008, DDQ-API-0030 | API-001 to API-003 |
| AI-assisted workflows | Strong (product boundary); Thin (providers and engineering agents) | Design reviewable | CNV-AIO-001, CNV-AIO-002, UNB-AIO-003, CNV-GRT-001 | DDQ-AIA-0014, DDQ-AIS-0002, DDQ-AIG-0027 | AIA-001 to AIA-006 |
| Manual intervention | Partial | Design reviewable | CNV-GOV-006, CNV-PLT-007, CNV-ARC-002, UNB-XIN-IAM-005, TVR-PAY-004 | DDQ-FCT-0034, DDQ-IAM-0023, DDQ-BCP-0026 | OPS-003, OPS-002, PAY-004 |
| Business continuity | Thin | Not answerable | UNB-OPS-001, SOC2-015, CNV-ARC-001, CNV-PLT-012 | DDQ-BCP-0001, DDQ-BCP-0017, DDQ-DR-0001 | BCP-001 to BCP-004, PAY-004 |
| Accessibility | Strong (design); Thin (evidence) | Design with conflicts | CNV-EXP-001, UNB-UX-002, UNB-UX-006, CNV-PLT-011 | DDQ-A11Y-0006, DDQ-A11Y-0019, DDQ-A11Y-0033 | A11Y-001 to A11Y-004 |
| Customer data migration | Thin | Not answerable | CNV-EXP-002, UNB-RCN-WF-009 | DDQ-PRT-0015, DDQ-PRT-0016, DDQ-RCN-0035 | EXIT-001 |
| Customer termination | Partial | Design reviewable | CNV-ENT-002, CNV-PLT-009 | DDQ-TRM-0001, DDQ-TRM-0004, DDQ-TRM-0011 | EXIT-003, EXIT-004, EXIT-006 |
| Data export | Partial | Design reviewable | CNV-ENT-002, REQ-X-039 | DDQ-PRT-0005, DDQ-PRT-0006, DDQ-PRT-0007 | EXIT-002, EXIT-005, LEG-005 |
| Insurance | None | Not answerable | none | DDQ-INS-0001, DDQ-INS-0008, DDQ-INS-0009 | LEG-003 |
| Secure SDLC | Thin | Not answerable | CNV-PLT-010, REQ-X-006, UNB-GAP-029 (hypothesis) | DDQ-SDL-0001, DDQ-SDL-0012, DDQ-AIS-0037 | SEC-010, SEC-012, AIA-003 |
| Vulnerability management | Thin | Not answerable | SOC2-016 | DDQ-VUL-0001, DDQ-VUL-0009, DDQ-VUL-0013 | SEC-006, SEC-007 |
| Scanning | Thin | Not answerable | SOC2-016, CNV-GOV-009 | DDQ-SCN-0001, DDQ-SCN-0002, DDQ-SCS-0011 | SEC-009, SEC-005, SEC-011 |
| Cloud hosting | Thin | Not answerable | CNV-ARC-001, UNB-TEN-008 | DDQ-CLD-0001, DDQ-CLD-0018, DDQ-CLD-0023 | SEC-021, SEC-022, SEC-023 |
| Escrow | Thin (dependency escrow only) | Not answerable | CNV-GOV-009 | DDQ-FST-0013, DDQ-ESC-0001, DDQ-ESC-0007 | EXIT-004, VEND-003 |
| Subprocessors | Thin (deferred) | Not answerable | UNB-XIN-SAS-011, SOC2-013, SOC2-022 | DDQ-SUB-0001, DDQ-SUB-0005, DDQ-PRV-0019 | VEND-001, VEND-002 |
| Application security | Thin | Not answerable | CNV-PLT-010, UNB-EVT-003 | DDQ-APP-0007, DDQ-APP-0011, DDQ-APP-0036 | SEC-013, SEC-012 |
| Encryption | Thin | Not answerable | SOC2-014, UNB-TEN-006, UNB-TEN-008 | DDQ-ENC-0001, DDQ-ENC-0005, DDQ-ENC-0013 | SEC-001 to SEC-005, PAY-002 |
| AI security | Partial | Design reviewable | CNV-AIO-002, UNB-AIO-003, AIN-012 (proposed), UNB-GAP-033 (hypothesis) | DDQ-AIS-0002, DDQ-AIS-0008, DDQ-AIS-0012 | AIA-003, AIA-004 |
| Penetration testing | None | Not answerable | SOC2-016 (mention) | DDQ-PEN-0001, DDQ-PEN-0006, DDQ-TEN-0021 | SEC-008, TEN-002 |

Proposed IDs in the table omit the `DD-UNB-` prefix.

## 5. Mapping to the sponsor audit controls (C01 to C24)

Source: `SRC-ECH-DAF-TECH-AUDIT` (daf-landscape technology audit control matrix). The
matrix is written from the sponsor's perspective; the "Unbound basis" column names the
requirements an auditor would test, and "Assessable today" states what evidence could be
shown now.

| Control | Dimension | Unbound basis | Assessable today | Gap and proposed |
|---|---|---|---|---|
| C01 | Legal owner and custody | CNV-LEG-001, CNV-PAY-001, UNB-XIN-REG-001 | Design only | Counsel opinion and executed role tables (LEG-001) |
| C02 | Bank and charity funds segregation | CNV-LEG-001 (no operator or FBO accounts) | Design only | Funds-flow conformance check build (LEG-001) |
| C03 | Double-entry fund accounting | ACC-MDL-001, ACC-MDL-002, CNV-FIN-011, CNV-FIN-004 | Design only | Integrity mechanism (FIN-005), sampling method (FIN-002) |
| C04 | Sponsor decision authority | CNV-GRT-001, CNV-GOV-003, CNV-AIO-001, CNV-GOV-010 | Design only | Manual intervention register (OPS-003), staffing (SEC-024) |
| C05 | Payment settlement and returns | CNV-FIN-003, CNV-PAY-004, CNV-PAY-005, CNV-PAY-007 | Design only | Bank selection (VEND-002), ACH idempotency (PAY-006) |
| C06 | API versioning and idempotency | CNV-EXP-001, UNB-XIN-EVA-011, CNV-ARC-003 | Design only | Sandbox and changelog (API-002), ACH binding (PAY-006) |
| C07 | Audit provenance and lineage | UNB-DATA-001, UNB-DATA-012, CNV-PLT-010, SOC2-025 | Design only | Anchoring and verifier (FIN-005), log retention (SEC-014) |
| C08 | Donor consent and tenant isolation | CNV-ARC-001, CNV-ARC-002, CNV-TEN-001, CNV-GRT-006 (neutral catalog) | Design with conflicts | Isolation default (TEN-001), independent tests (TEN-002), embedded security (WLB-002) |
| C09 | Security assurance actual scope | CNV-GOV-001, SOC2-036, MON-024 | Nothing to show: no SOC report or pen test | AUD-001, SEC-008, SEC-003 |
| C10 | Incident response and disclosure | SOC2-015, UNB-GAP-034 | Nothing to show | SEC-016, LEG-006, OPS-001 |
| C11 | Business continuity and vendor failure | CNV-ENT-002, CNV-PLT-007, CNV-ARC-001 | Design only | Escrow and reserve (EXIT-004), drill (EXIT-006), emergency payments (PAY-004) |
| C12 | Data portability and exit | CNV-ENT-002, CNV-EXP-002 | Design only | Export schema and reconstruction (EXIT-002), data definition (LEG-005) |
| C13 | Custody data freshness | CNV-FIN-005, CNV-FIN-013, UNB-CUST-009 | Design only | Custodian activation gate (FIN-009) |
| C14 | Gift acceptance and tax provenance | CNV-FIN-003, CNV-GRT-013, UNB-RCN-FIN-001 | Design only | Non-cash substantiation (FIN-010) |
| C15 | Integration dependency risks | CNV-PLT-012, CNV-ECO-005, UNB-API-STD-005 | Design only | Provider selection (VEND-002), custodian gate (FIN-009) |
| C16 | Availability and degradation | CNV-ARC-001, CNV-ARC-003 (fail closed) | Design only; no SLOs measured | Support and status page (OPS-001), recovery tests (BCP-003) |
| C17 | Program and contract migration | CNV-EXP-002, CNV-ENT-002 | Design only | Migration specification (EXIT-001), change-of-control terms (EXIT-003) |
| C18 | Product and vendor lifecycle finances | none (organizational) | Nothing to show | Wind-down reserve (EXIT-004), key-person continuity (BCP-001), entity (LEG-004) |
| C19 | AI decision quality | CNV-AIO-001, CNV-AIO-002, CNV-GRT-011 | Design only | Adversarial suite (AIA-004), model change control (AIA-005) |
| C20 | Accessibility and mobile reliability | CNV-EXP-001, UNB-UX-006, CNV-PLT-011 | Design only | ACR (A11Y-001), accessible PDF (A11Y-002) |
| C21 | Fee and ledger integrity | CNV-FIN-002, CNV-FIN-006, CNV-GRT-013 | Design only | Recomputation (FIN-011), fee notice (FIN-003) |
| C22 | Public technical evidence | MON-024, SOC2-036, CNV-ECO-003 (claims gated on evidence) | Nothing public | Developer documentation (API-002), disclosure policy (SEC-007) |
| C23 | Hosting and dependency truth | CNV-ARC-001 | Not answerable: no provider chosen | Hosting decision (SEC-021), SBOM (SEC-011) |
| C24 | Independent customer reference | none | Not answerable: no customers | Pilot sponsor; no requirement can substitute |

## 6. Critical path to being assessable

"Assessable" means a sponsor's third-party risk team can complete its review with
evidence rather than intentions. Steps are ordered by dependency; each names the proposed
requirements it closes. Durations are not estimated because staffing is unknown.

1. **Organizational facts.** Form and register the contracting entity, assign IP, name a
   succession designee and second credential custodian, and decide minimum staffing for
   two-person controls (LEG-004, BCP-001, SEC-024). Nothing else can be contracted,
   insured or audited until these exist.
2. **Baseline hygiene.** Flag contradicted text and resolve the isolation default, the
   pool and trade-execution text, and the Strata assumptions (GOV-001, TEN-001, FIN-007,
   FIN-008, GOV-002). This is cheap and removes the answers most likely to be judged
   misleading.
3. **Perimeter and counterparties.** Obtain the regulatory perimeter opinion and select
   hosting, bank or rail, sanctions provider, custodian feeds, identity proofing and AI
   providers with due diligence files (LEG-001, SEC-021, VEND-002, AML-001, AIA-001).
4. **Security program foundation.** Adopt the program charter and policy set, the secure
   development standard with enforced review, the incident response plan, personnel and
   endpoint controls, and decide encryption, key management, secrets and network design
   (SEC-020, SEC-010, SEC-016, SEC-017 to SEC-019, SEC-001 to SEC-005, SEC-022,
   SEC-023, AIA-003).
5. **Contract and commercial package.** Publish the MSA, security addendum, DPA,
   incident notification terms, exit schedule and subprocessor register; bind insurance;
   execute component commercial licenses; arrange escrow (LEG-002, LEG-006, PRV-002,
   VEND-001, LEG-003, VEND-003, EXIT-004).
6. **Build with gates.** Implement scanning, SBOM and signed provenance, threat models,
   ASVS verification and the tenant isolation suite in the pipeline from the first
   commit (SEC-009, SEC-011, SEC-012, SEC-013, TEN-002).
7. **Money movement obligations.** Implement payment file security, Nacha account number
   protection and the TPSP fraud monitoring program before any rail goes live (PAY-001,
   PAY-002, PAY-003).
8. **Independent validation.** Penetration test before real donor data; SOC 2 readiness
   and Type II observation period beginning at first production data; independent ACR
   (SEC-008, AUD-001, A11Y-001).
9. **Operate and evidence.** Run restore, rebuild, exit and incident exercises; publish
   the CUEC list; begin the reference pilot (BCP-003, BCP-004, EXIT-006, SEC-016,
   FIN-006). Control C24 (independent customer reference) can be satisfied only by a
   real pilot sponsor.

Until steps 1 to 5 are complete, the most useful sales artifact is an honest design
dossier that labels every answer as planned, consistent with DD-GOV-001 rules 3 and 4.

## 7. Source and method notes

- Coverage judgments rest on reading the governing clauses in `unbound@9b38de47`; the
  automated mining in DD-GAP-UNB-001 section 2 only screens citations.
- Assessor classifications rest on DD-IND-DAF-001; no confidential or login-gated
  material was used.
- Cost figures in proposed requirements are labeled order-of-magnitude judgment and are
  not sourced.
