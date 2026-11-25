from qbc_aitpraml import Cat, challenge

C = Cat("REG",
        industries=["financial-services", "banking", "wealth-management", "donor-advised-funds"],
        jurisdictions=["US-federal", "US-states"],
        products=["all-echelon-products"])

C.au(1, title="Regulatory inventory, applicability determinations and Echelon's own regulatory status",
     status="proposed-target-state",
     rationale="Unbound requires a machine-checkable applicability register with citation, jurisdiction, affected entity, classification and accountable reviewer (UNB-REGMAP-001), explicit recording of inapplicable, disputed, guidance-only and proposed obligations (UNB-REGMAP-003), re-evaluation triggers (UNB-REGMAP-004), and an OperatorStatusRegister mapping features to licensing questions such as investment adviser or money transmitter status (UNB-XIN-REG-002). Design choices intended to keep Unbound outside licensed roles are recorded (CNV-LEG-001: no holding of funds, no payment execution, no individualized investment advice; CNV-PAY-001: Unbound as Nacha third-party service provider, sponsor as originator). Agents cannot publish legal interpretations as binding policy (AIN-035, GOV-AUTH-011). Nothing is implemented and no counsel review is recorded.",
     target="Echelon maintains one regulatory applicability register covering law that binds Echelon itself (for example OFAC, FTC Safeguards Rule if applicable, state privacy and breach laws, California charitable fundraising platform registration per CNV-LEG-002), law that binds customers and flows to Echelon by contract or supervisory expectation (GLBA, Interagency TPRM guidance, BSCA, Nacha, IRC DAF provisions, SEC and FINRA recordkeeping), and guidance or proposals (marked as such). Each row has primary citation, classification, affected entity, facts relied on, counsel reviewer and date, and mapped controls. Echelon's own status (not a money transmitter, not an investment adviser, Nacha TPSP) is a recorded counsel determination tied to funds-flow conformance checks that block deployments that would change it. AI may draft analyses but only counsel-approved interpretations become binding.",
     current="Not established; requirements only.",
     intended="Build the register per UNB-REGMAP-001 to 006 and obtain counsel review of operator status before any customer deployment.",
     provable="Nothing.",
     statement="Echelon has designed a regulatory applicability register and a product architecture intended to avoid holding funds, executing payments or giving investment advice. The register is not built and Echelon's regulatory status has not yet been confirmed by counsel.",
     kind="planned",
     controls=[1, 2], evrs=[1, 2],
     requirements=["UNB-REGMAP-001", "UNB-REGMAP-003", "UNB-REGMAP-004", "UNB-REGMAP-005", "UNB-REGMAP-006", "UNB-XIN-REG-001", "UNB-XIN-REG-002", "CNV-LEG-001", "CNV-LEG-002", "CNV-PAY-001", "AIN-035", "GOV-AUTH-011"],
     freshness="P180D", mechanism="periodic-manual", automation="partial",
     impl_cost="medium", rec_cost="low",
     owner="Not assigned (proposed: Echelon counsel)",
     open=["Has counsel reviewed whether any planned Unbound feature would require money transmitter, investment adviser or broker registration?"])

C.au(2, title="Compliance monitoring and testing against mapped obligations",
     status="proposed-target-state",
     rationale="UNB-REGMAP-002 requires a reviewer-approved many-to-many mapping from obligation to control to test to evidence and blocks the compliance gate for binding obligations without an independently verified control. SOC2-019 distinguishes control states and SOC2-024 requires owner attestation and independent challenge. Not implemented; the master control matrix shows all controls Designed with no operating evidence, test execution or auditor review.",
     target="Every binding obligation in the register maps to controls, tests and evidence. Compliance status is computed from evidence, not declared: a control without current evidence shows as failing. Compliance issues are tracked with owner, severity, due date and escalation, and an independent compliance review tests the program annually. The deployment gate refuses activation for a customer when an applicable binding obligation lacks a verified control.",
     current="Not established.",
     intended="Implement per UNB-REGMAP-002 and the continuous control monitoring architecture.",
     provable="Nothing.",
     statement="Echelon plans compliance monitoring in which each applicable obligation is mapped to controls, tests and evidence, with status computed from evidence. Not yet implemented.",
     kind="planned",
     controls=[3], evrs=[3],
     requirements=["UNB-REGMAP-002", "SOC2-019", "SOC2-024", "SOC2-034"],
     freshness="P30D", mechanism="continuous-automated", automation="high",
     impl_cost="medium", rec_cost="medium",
     owner="Not assigned (proposed: Echelon compliance owner)")

C.au(3, title="Regulator examination access (Bank Service Company Act) and cooperation with customer examinations",
     status="proposed-target-state",
     rationale="No contract terms or procedures exist. Unbound provides for auditor-ready Folio evidence packages (SOC2-009), replayable decisions (GOV-AUTH-022) and partner isolation of audit evidence (GOV-AUTH-016), which would support examinations but are not built. Echelon has never been examined.",
     target="Echelon contractually acknowledges that, when it performs services for an insured depository institution, those services are subject to examination by the institution's federal banking regulator to the same extent as if performed by the institution (12 U.S.C. 1867(c)), and supports the institution's notice of the service relationship to its regulator. Echelon commits to cooperate with examinations of its customers by any regulator with jurisdiction (federal banking agencies, SEC, FINRA, state regulators, IRS), to provide evidence packages within agreed timeframes, and to notify customers of regulator inquiries concerning their services where legally permitted. For EU financial entity customers, Echelon accepts the access, audit and inspection rights DORA requires in ICT contracts. Evidence packages are generated per tenant so one customer's examination never exposes another's data.",
     current="Not established; Echelon has not been examined by any regulator.",
     intended="Include examination and cooperation clauses in the customer agreement template; build tenant-scoped evidence export.",
     provable="Nothing.",
     statement="Echelon has not been examined by any regulator. It will contractually acknowledge regulator examination authority over services it performs for banks under the Bank Service Company Act and commit to cooperate with customers' regulatory examinations.",
     kind="planned",
     controls=[4], evrs=[4],
     requirements=["SOC2-009", "GOV-AUTH-016", "GOV-AUTH-022"],
     freshness="per-event", mechanism="event-driven-automated", automation="high",
     impl_cost="low", rec_cost="low",
     owner="Not assigned (proposed: Echelon counsel)",
     challenge=challenge(
         intent="Regulated customers must show examiners that outsourcing has not reduced the regulator's visibility.",
         adverse="An examiner cannot obtain information about an outsourced function, resulting in findings against the customer.",
         conv_eff="Examination clauses establish rights but examiners rarely visit small vendors; in practice the customer requests documents on short deadlines, and vendors without ready evidence fail those requests.",
         legal="For services to insured depository institutions, 12 U.S.C. 1867(c) subjects the services to examination by statute regardless of contract. Most DAF sponsors are charities, not banks, so BSCA applies only when a bank or bank-affiliated customer is served.",
         contract="Standard in bank vendor contracts; DORA mandates access rights for EU financial entities.",
         history="Clause-based acknowledgment.",
         elim="Not eliminable; it is a legal right. The burden of response can be reduced.",
         auto="Tenant-scoped evidence export on demand.",
         cont="Evidence produced continuously so examination requests are answered from existing records.",
         alt="Standing, tenant-scoped evidence packages that customers can hand to examiners, plus the contractual acknowledgment.",
         verif="Customers can request a sample package at any time.",
         accept="Likely; examiners value timely, complete records.",
         invalid="Examiners may still require on-site or direct access.",
         conv_cost="low (clause)",
         alt_cost="medium (evidence export)",
         alt_risk="Pre-packaged evidence may be seen as curated; it must be reproducible from source records.",
         pro=["Faster examination responses.", "Same evidence serves SOC and examination purposes."],
         con=["Cannot substitute for statutory access.", "Small vendor capacity during simultaneous exams."],
         tech="stronger", inst="likely"))

C.au(4, title="Sanctions exposure of Echelon itself",
     status="unknown",
     rationale="No record of screening Echelon's owners, personnel, contractors, vendors or customers against sanctions lists was located, and ownership details of Echelon Foundry, LLC are not established in the records reviewed. OFAC prohibitions apply to Echelon as a US person independent of any customer obligation.",
     target="Echelon screens its owners, managers, personnel, contractors, vendors and customers against OFAC lists (including the 50 percent rule for ownership) at onboarding and on list changes, records results, and does not operate in or support customers in comprehensively sanctioned jurisdictions without a license. Echelon provides customers an annual written attestation of its sanctions status and discloses any OFAC enforcement action or voluntary self-disclosure.",
     current="Unknown; no record located.",
     intended="Perform and record initial screening of owners, personnel and vendors; adopt a short sanctions compliance procedure based on the OFAC framework.",
     provable="Nothing.",
     statement="Echelon has not yet documented sanctions screening of its owners, personnel, vendors and customers. It plans to complete and record that screening and provide an attestation on request.",
     kind="not-available",
     controls=[5], evrs=[5],
     freshness="P1Y", mechanism="periodic-manual", automation="partial",
     impl_cost="low", rec_cost="low",
     owner="Not assigned (proposed: Echelon managing member)",
     open=["Ownership and control structure of Echelon Foundry, LLC for 50 percent rule analysis."])

C.au(5, title="Complaints handling and reporting to customers",
     status="proposed-target-state",
     rationale="UNB-XIN-SVC-005 requires classifying any expression of dissatisfaction as a complaint case with acknowledgment (default 2 business days), response targets (default 15 business days), taxonomy and escalation; UNB-GAP-026 and UNB-CHAR-027 address complaint escalation and charity complaints. CNV-PLT-005 includes correction alerts. Not implemented.",
     target="Complaints from customers and from their donors, advisors and grantees are captured from every channel as complaint cases with acknowledgment and response deadlines, a taxonomy that flags potential regulatory issues (privacy, discrimination, misrepresentation, sanctions holds), root cause analysis and routing to the sponsor where the sponsor owns the decision. Customers receive complaint data and trend reports for their own complaint management and examinations. Echelon's own complaints about its service are tracked the same way.",
     current="Not established.",
     intended="Implement the complaint case profile per UNB-XIN-SVC-005.",
     provable="Nothing.",
     statement="Echelon's design includes complaint capture from all channels with acknowledgment and response deadlines, root cause analysis and reporting to customers. Not yet implemented.",
     kind="planned",
     controls=[6], evrs=[6],
     requirements=["UNB-XIN-SVC-005", "UNB-GAP-026", "UNB-CHAR-027"],
     freshness="P30D", mechanism="continuous-automated", automation="high",
     impl_cost="medium", rec_cost="low",
     owner="Not assigned (proposed: Unbound product owner)",
     products=None)

C.au(6, title="Regulatory change management",
     status="proposed-target-state",
     rationale="UNB-RCN-REG-001 requires a regulatory-change watch list (including proposed section 4966 regulations, OFAC rule changes and state charitable solicitation changes) linked to affected requirements, with a status change opening an impact review within 10 business days. CNV-GRT-008 requires proposed regulations to be tracked as proposed, not effective. CNV-GOV-005 requires versioned, effective-dated policy packs with sponsor adoption. Not implemented.",
     target="Echelon monitors primary sources for changes to laws and guidance in its register, records each item with status (proposed, final, effective) and the requirements and controls it affects, opens an impact review within a set period, and delivers changes as versioned, effective-dated policy packs that sponsors adopt affirmatively. Proposed rules are never applied as binding. Interpretations embedded in product rules require counsel approval; AI may summarize changes but not decide their effect.",
     current="Not established.",
     intended="Implement per UNB-RCN-REG-001 and CNV-GOV-005.",
     provable="Nothing.",
     statement="Echelon plans a regulatory change watch list linked to affected requirements, with counsel-approved interpretations delivered as effective-dated policy updates. Not yet operating.",
     kind="planned",
     controls=[7], evrs=[7],
     requirements=["UNB-RCN-REG-001", "CNV-GRT-008", "CNV-GOV-005", "UNB-REGMAP-005", "AIN-035"],
     freshness="P30D", mechanism="periodic-manual", automation="partial",
     impl_cost="low", rec_cost="medium",
     owner="Not assigned (proposed: Echelon compliance owner)")

C.au(7, title="Support for customers' regulatory notification, reporting and recordkeeping obligations",
     status="proposed-target-state",
     rationale="Incident response requirements (SOC2-026) and OFAC report data generation (CNV-GRT-006, UNB-RCN-REG-003), Schedule D data (CNV-FIN-009) and retention rules (CNV-PLT-004, CNV-PLT-009) are specified. No incident notification commitments to customers exist and no production system exists.",
     target="Echelon commits to notify each bank customer's designated contact as soon as possible when a computer-security incident has materially disrupted or degraded, or is reasonably likely to materially disrupt or degrade, covered services for four or more hours, consistent with the 2021 bank service provider rule; to notify covered broker-dealer and adviser customers of breaches of their customer information as soon as possible and within 72 hours, consistent with amended Regulation S-P service provider requirements; and to meet any shorter contractual deadlines. The platform produces data for customers' regulatory reports (OFAC blocked and rejected transaction reports, Form 990 Schedule D) and retains records in forms that meet customers' recordkeeping rules where those apply.",
     current="Not established.",
     intended="Add notification commitments to the customer agreement and incident runbooks; implement report data generation per the cited requirements.",
     provable="Nothing.",
     statement="Echelon plans to commit to regulatory-grade incident notification for bank and securities customers and to produce data for their regulatory reports. Not yet in place.",
     kind="planned",
     controls=[8, 9], evrs=[8, 9],
     requirements=["SOC2-026", "CNV-GRT-006", "UNB-RCN-REG-003", "CNV-FIN-009", "CNV-PLT-004", "CNV-PLT-009"],
     freshness="per-event", mechanism="event-driven-automated", automation="high",
     impl_cost="medium", rec_cost="low",
     owner="Not assigned (proposed: Echelon incident response owner)",
     residual=["Records retained for securities recordkeeping rules may need specific storage attributes that must be confirmed with each customer's compliance function."])

# fix: products None default handled below
for a in C.aus:
    a.pop("products", None)

# ---------------- Controls ----------------
C.ctl(1, title="Regulatory applicability register with counsel review",
      objective="Each law, rule and guidance item has a register row with citation, classification, affected entity, facts, counsel reviewer and date, mapped controls and re-evaluation triggers.",
      type="administrative", level="L10-external-or-manual",
      systems=["Unbound regulatory applicability register (designed, not built)"],
      related=["UNB-REGMAP-001", "UNB-REGMAP-003", "UNB-REGMAP-004", "UNB-CTRL-058"],
      refs=["SRC-ISO-37301||r", "SRC-ISO-27001-2022|A.5.31|d", "SRC-NIST-CSF-2.0|GV.OC-03|d"],
      evrs=[1], owner="Not assigned (proposed: Echelon counsel)")
C.ctl(2, title="Funds-flow and operator-status conformance gate",
      objective="Each deployment is checked against the recorded funds-flow and operator-status determinations; a deployment that would hold funds, execute payments or provide advice is blocked.",
      type="preventive-gate", level="L5-build-release-gate",
      systems=["not yet assigned"],
      related=["CNV-LEG-001", "UNB-XIN-REG-001", "UNB-XIN-REG-002"],
      refs=["SRC-NACHA-RULES||r"],
      evrs=[2], owner="Not assigned (proposed: Unbound product owner)")
C.ctl(3, title="Evidence-computed compliance status and compliance gate",
      objective="Compliance status per obligation is computed from current control evidence; missing evidence shows as failing; customer activation is refused when an applicable binding obligation lacks a verified control.",
      type="preventive-gate", level="L5-build-release-gate",
      systems=["not yet assigned"],
      related=["UNB-REGMAP-002", "SOC2-019", "SOC2-034", "UNB-CTRL-059"],
      refs=["SRC-ISO-37301||r", "SRC-ISO-27001-2022|A.5.36|r", "SRC-COSO-2013||r"],
      evrs=[3], owner="Not assigned (proposed: Echelon compliance owner)")
C.ctl(4, title="Examination access terms and tenant-scoped examination packages",
      objective="Customer agreements acknowledge regulator examination authority and cooperation duties; tenant-scoped evidence packages are produced on request within agreed timeframes.",
      type="administrative", level="L6-automated-analysis",
      systems=["Folio (exists; not operated for this purpose)", "not yet assigned"],
      related=["SOC2-009", "GOV-AUTH-016"],
      refs=["SRC-BSCA|12 U.S.C. 1867(c)|d", "SRC-EU-DORA|Art. 30|r", "SRC-FFIEC-OUTSOURCING-BOOKLET||r"],
      evrs=[4], owner="Not assigned (proposed: Echelon counsel)")
C.ctl(5, title="Sanctions screening of Echelon's owners, personnel, vendors and customers",
      objective="Owners, personnel, contractors, vendors and customers are screened at onboarding and on list changes, with recorded results and annual attestation.",
      type="detective-automated", level="L6-automated-analysis",
      systems=["not yet assigned"],
      refs=["SRC-OFAC-COMPLIANCE-FRAMEWORK|Internal Controls|d", "SRC-OFAC-REGS||r"],
      evrs=[5], owner="Not assigned (proposed: Echelon managing member)")
C.ctl(6, title="Complaint case capture, deadlines and reporting",
      objective="Every expression of dissatisfaction becomes a complaint case with acknowledgment and response deadlines, taxonomy, root cause and customer reporting.",
      type="detective-automated", level="L9-runtime-monitored",
      systems=["not yet assigned"],
      related=["UNB-XIN-SVC-005"],
      refs=["SRC-ISO-37301||r"],
      evrs=[6], owner="Not assigned (proposed: Unbound product owner)")
C.ctl(7, title="Regulatory watch list with impact review deadlines",
      objective="Regulatory changes are tracked by status and linked to affected requirements; status changes open impact reviews within a set period; proposed rules are not applied as binding.",
      type="detective-manual", level="L10-external-or-manual",
      systems=["not yet assigned"],
      related=["UNB-RCN-REG-001", "CNV-GRT-008", "CNV-GOV-005"],
      refs=["SRC-ISO-37301||r", "SRC-IRS-DAF-PROPOSED-REGS-2023||r"],
      evrs=[7], owner="Not assigned (proposed: Echelon compliance owner)")
C.ctl(8, title="Regulatory incident notification commitments and runbook",
      objective="Incident runbooks include customer notification clocks meeting the bank service provider rule, Regulation S-P service provider notice and contractual deadlines, with notification records.",
      type="corrective", level="L10-external-or-manual",
      systems=["not yet assigned"],
      related=["SOC2-026", "UNB-CTRL-076"],
      refs=["SRC-CIRN-RULE-2021||d", "SRC-SEC-REG-SP-2024||r", "SRC-NIST-SP800-61-R3||r"],
      evrs=[8], owner="Not assigned (proposed: Echelon incident response owner)")
C.ctl(9, title="Regulatory report data generation and conforming retention",
      objective="The platform generates data for customers' regulatory reports and retains records per the schedules in CNV-PLT-004 and CNV-PLT-009.",
      type="preventive-structural", level="L3-restricted-interface",
      systems=["not yet assigned"],
      related=["CNV-GRT-006", "UNB-RCN-REG-003", "CNV-FIN-009", "CNV-PLT-004", "UNB-CTRL-058"],
      refs=["SRC-OFAC-REGS|31 CFR 501.603|d", "SRC-IRS-FORM-990||r", "SRC-SEC-17A-4||r", "SRC-SEC-ADVISERS-BOOKS-RECORDS||r"],
      evrs=[9], owner="Not assigned (proposed: Unbound product owner)")

# ---------------- Evidence ----------------
C.evr(1, title="Regulatory applicability register export", description="Register rows with citation, classification, affected entity, counsel reviewer and date, and mapped controls.",
      mechanism="periodic-manual", freshness="P180D", format="CSV/JSON", disclosure="nda")
C.evr(2, title="Funds-flow and operator-status conformance results", description="Per deployment: funds-flow declaration, conformance test results and blocked activations.",
      mechanism="event-driven-automated", freshness="per-event", format="Gate report", disclosure="customer-only")
C.evr(3, title="Obligation-to-evidence compliance dashboard snapshot", description="Computed status per obligation with linked control evidence, failing items and issues.",
      mechanism="continuous-automated", freshness="P30D", format="Report", disclosure="customer-only")
C.evr(4, title="Examination cooperation terms and package log", description="Executed contract clause references and log of examination evidence packages produced, with turnaround.",
      mechanism="event-driven-automated", freshness="per-event", format="Contract register and package log", disclosure="customer-only")
C.evr(5, title="Echelon sanctions screening records and attestation", description="Screening results for owners, personnel, vendors and customers with list versions, and the signed annual attestation.",
      mechanism="periodic-automated", freshness="P1Y", format="Screening log and attestation", disclosure="nda")
C.evr(6, title="Complaint register and trend report", description="Complaint cases with timestamps, taxonomy, outcomes and periodic trend reports provided to customers.",
      mechanism="continuous-automated", freshness="P30D", format="Case export and report", disclosure="customer-only")
C.evr(7, title="Regulatory watch list and impact reviews", description="Watch list entries with status history, linked requirements and impact review records with due and completion dates.",
      mechanism="periodic-manual", freshness="P30D", format="Register", disclosure="nda")
C.evr(8, title="Incident notification records", description="Per incident: detection time, customer notification times, recipients and content.",
      mechanism="event-driven-automated", freshness="per-event", format="Incident record", disclosure="customer-only")
C.evr(9, title="Regulatory report data and retention configuration", description="Generated report data sets and retention schedule configuration with legal hold status.",
      mechanism="event-driven-automated", freshness="per-event", format="Data export and configuration", disclosure="customer-only")

# ---------------- Questions ----------------
C.q(1, "Regulatory inventory", "Do you maintain an inventory of the laws and regulations that apply to you and to the services you provide to us, with your reasoning for each?",
    "The customer needs assurance the vendor understands its regulatory environment.",
    "Vendor unaware of obligations that affect the customer.",
    ["SRC-ECH-UNB-BASELINE|UNB-REGMAP-001", "SRC-ISO-27001-2022|A.5.31|d", "SRC-NIST-CSF-2.0|GV.OC-03|d", "SRC-SA-SIG||r"],
    "industry-convention", "high", industries=["all"],
    alts=["How do you identify legal and regulatory requirements applicable to your services?"])
C.q(1, "Direct obligations", "Which laws and regulations do you consider binding on Echelon itself, as distinct from obligations that bind us and flow to you by contract?",
    "Confusing direct and flowed obligations leads to gaps.",
    "Neither party owns an obligation.",
    ["SRC-ECH-UNB-BASELINE|UNB-REGMAP-003", "SRC-INTERAGENCY-TPRM-2023||r"],
    "customer-preference", "medium", industries=["all"])
C.q(1, "Binding versus guidance", "How does your compliance program distinguish binding law from supervisory guidance, industry practice and customer preferences?",
    "Treating guidance as law, or law as optional, both cause errors.",
    "Misallocated compliance effort or missed legal duties.",
    ["SRC-ECH-UNB-BASELINE|UNB-REGMAP-003"],
    "customer-preference", "low")
C.q(1, "Legal interpretation", "Who interprets laws for your product rules, and can AI-generated legal analysis ever become a binding rule without counsel review?",
    "Product rules encode legal interpretations that bind customers' operations.",
    "Incorrect AI-drafted interpretation embedded in compliance logic.",
    ["SRC-ECH-UNB-BASELINE|AIN-035", "SRC-ECH-UNB-BASELINE|GOV-AUTH-011", "SRC-ECH-UNB-BASELINE|UNB-REGMAP-006"],
    "customer-preference", "high")
C.q(1, "Regulatory status", "Are you, or do you need to be, licensed or registered as a money transmitter, investment adviser, broker-dealer or other regulated entity for the services you provide? What is your role under the Nacha Operating Rules?",
    "Unlicensed activity by a vendor exposes the customer and can halt the service.",
    "Service interruption or enforcement due to vendor licensing gaps.",
    ["SRC-ECH-UNB-BASELINE|CNV-LEG-001", "SRC-ECH-UNB-BASELINE|UNB-XIN-REG-002", "SRC-ECH-UNB-BASELINE|CNV-PAY-001", "SRC-NACHA-RULES||r"],
    "legal-regulatory", "critical", products=["unbound"],
    authority="State money transmission regulators; SEC; state securities regulators; Nacha (rules)",
    scope="Licensing duties apply only if Echelon performs the regulated activity; the Unbound design intends that it does not, pending counsel confirmation.")

C.q(2, "Compliance monitoring", "How do you monitor and test your ongoing compliance with applicable legal and regulatory requirements?",
    "Compliance is a continuing state, not a one-time review.",
    "Compliance drift between reviews.",
    ["SRC-ECH-UNB-BASELINE|UNB-REGMAP-002", "SRC-ISO-37301||r", "SRC-ISO-27001-2022|A.5.36|r"],
    "industry-convention", "high", industries=["all"])
C.q(2, "Obligation mapping", "Is each applicable obligation mapped to specific controls, tests and evidence?",
    "Mapping exposes obligations with no control.",
    "Uncontrolled legal obligations.",
    ["SRC-ECH-UNB-BASELINE|UNB-REGMAP-002", "SRC-ECH-UNB-SOC2-DIRECTIVE|SOC2-035"],
    "customer-preference", "medium")
C.q(2, "Independent compliance testing", "Has an independent party, such as internal audit or an outside firm, tested your compliance program? Can you share results?",
    "Independent testing shows the program works.",
    "Self-assessed compliance overstated.",
    ["SRC-ECH-UNB-SOC2-DIRECTIVE|SOC2-024", "SRC-OFAC-COMPLIANCE-FRAMEWORK|Testing and Auditing|r"],
    "customer-preference", "medium")
C.q(2, "Compliance issues", "How are compliance issues recorded, escalated to management and remediated, and are material issues disclosed to customers?",
    "Customers need to learn of issues that affect them.",
    "Undisclosed compliance failures affecting the customer.",
    ["SRC-ECH-UNB-SOC2-DIRECTIVE|SOC2-033", "SRC-ISO-37301||r"],
    "contractual-common", "medium")

C.q(3, "Bank Service Company Act", "Do you acknowledge that services you perform for us as an insured depository institution are subject to examination by our federal banking regulator under the Bank Service Company Act?",
    "Banks must preserve regulatory visibility over outsourced services.",
    "Examination findings against the bank for outsourcing without regulator access.",
    ["SRC-BSCA|12 U.S.C. 1867(c)|d", "SRC-INTERAGENCY-TPRM-2023||r", "SRC-FFIEC-OUTSOURCING-BOOKLET||r"],
    "legal-regulatory", "high", industries=["banking"], jurisdictions=["US-federal"],
    authority="OCC; FDIC; Federal Reserve",
    scope="Applies to services performed for insured depository institutions; most DAF sponsors are charities, not banks.")
C.q(3, "Customer examinations", "Will you cooperate with our regulators, including the SEC, FINRA, state regulators and the IRS, and provide information and access during examinations of us?",
    "Customers remain accountable to regulators for outsourced functions.",
    "Customer unable to answer examiners about outsourced activity.",
    ["SRC-FINRA-RN-21-29||d", "SRC-INTERAGENCY-TPRM-2023||r", "SRC-SEC-ADVISER-OUTSOURCING-PROPOSAL||r"],
    "supervisory-guidance", "high", industries=["financial-services", "wealth-management", "donor-advised-funds", "banking"],
    authority="SEC; FINRA; state regulators; IRS")
C.q(3, "Examination history", "Have you ever been examined by a federal or state regulator? Were there findings, and how were they resolved?",
    "Prior examination history indicates regulatory maturity.",
    "Unresolved regulatory findings at the vendor.",
    ["SRC-FFIEC-IT-HANDBOOK||r", "SRC-SA-SIG||r"],
    "customer-preference", "medium")
C.q(3, "Examination response time", "How quickly can you produce records and evidence for our examiners, and in what form?",
    "Examination requests have short deadlines.",
    "Missed examination deadlines.",
    ["SRC-ECH-UNB-SOC2-DIRECTIVE|SOC2-009", "SRC-ECH-UNB-BASELINE|GOV-AUTH-022"],
    "customer-preference", "medium")
C.q(3, "Regulator inquiry notice", "Will you notify us of regulator inquiries, subpoenas or examinations that concern our services or data, where legally permitted?",
    "Customers need to know when their data or services are under regulatory scrutiny.",
    "Customer surprised by regulatory action involving its vendor.",
    ["SRC-INTERAGENCY-TPRM-2023|Contract Negotiation|r"],
    "contractual-common", "medium")
C.q(3, "EU access rights", "For our EU-regulated entities, will your contract include the access, inspection and audit rights required for ICT services under DORA?",
    "EU financial entities must include specific rights in ICT contracts.",
    "Non-compliant ICT contract for the EU entity.",
    ["SRC-EU-DORA|Art. 30|d", "SRC-EBA-OUTSOURCING-GL||r"],
    "legal-regulatory", "low", jurisdictions=["EU"], authority="EU competent authorities",
    scope="Applies to EU financial entity customers only.")

C.q(4, "Sanctions status", "Are Echelon, its owners, officers or personnel listed on any sanctions list, or owned 50 percent or more by sanctioned persons?",
    "Dealing with a sanctioned vendor is prohibited for US persons.",
    "Customer transacts with a blocked person by contracting with the vendor.",
    ["SRC-OFAC-REGS||d", "SRC-OFAC-COMPLIANCE-FRAMEWORK||r"],
    "legal-regulatory", "critical", industries=["all"], jurisdictions=["US-federal"], authority="OFAC")
C.q(4, "Sanctioned jurisdictions", "Do you have operations, personnel, contractors or subprocessors in comprehensively sanctioned countries or regions?",
    "Activity in embargoed jurisdictions can create violations for customers.",
    "Indirect sanctions violation through vendor operations.",
    ["SRC-OFAC-REGS||d"],
    "legal-regulatory", "high", industries=["all"], jurisdictions=["US-federal"], authority="OFAC")
C.q(4, "Echelon screening program", "Do you screen your own customers, vendors and personnel against sanctions lists, and how often?",
    "A vendor without its own sanctions controls may expose customers.",
    "Vendor relationships with sanctioned parties.",
    ["SRC-OFAC-COMPLIANCE-FRAMEWORK|Internal Controls|d"],
    "industry-convention", "medium", industries=["all"], jurisdictions=["US-federal"], authority="OFAC")
C.q(4, "Enforcement history", "Has Echelon ever been subject to an OFAC enforcement action, penalty or voluntary self-disclosure?",
    "Enforcement history indicates control failures.",
    "Undisclosed sanctions compliance failures.",
    ["SRC-OFAC-COMPLIANCE-FRAMEWORK||r"],
    "customer-preference", "medium", industries=["all"], jurisdictions=["US-federal"], authority="OFAC")

C.q(5, "Complaints handling", "Do you have a documented process for handling complaints from us and from our donors, advisors or grantees, with response timeframes?",
    "Complaints signal service failures and potential regulatory issues.",
    "Unaddressed complaints escalate to regulators or the public.",
    ["SRC-ECH-UNB-BASELINE|UNB-XIN-SVC-005", "SRC-ISO-37301||r"],
    "industry-convention", "medium", products=["unbound"], industries=["donor-advised-funds", "nonprofit", "financial-services"])
C.q(5, "Complaint routing", "When a donor or grantee complains to you about a decision we made, how is the complaint recorded and routed to us?",
    "The sponsor owns grant and fund decisions and must answer complaints about them.",
    "Complaints lost between vendor and sponsor.",
    ["SRC-ECH-UNB-BASELINE|UNB-XIN-SVC-005", "SRC-ECH-UNB-BASELINE|UNB-GAP-026"],
    "customer-preference", "medium", products=["unbound"], industries=["donor-advised-funds", "nonprofit"])
C.q(5, "Complaint analysis", "Do you analyze complaints for root causes and potential regulatory issues, such as discrimination, privacy or misleading communications, and share trends with us?",
    "Patterns in complaints reveal systemic problems.",
    "Systemic issue undetected until regulatory action.",
    ["SRC-ECH-UNB-BASELINE|UNB-XIN-SVC-005"],
    "customer-preference", "low")
C.q(5, "Complaint records", "Can you provide complaint records about our services for our own regulatory reporting and examinations?",
    "Regulators review complaint handling at regulated firms.",
    "Incomplete complaint records in examination.",
    ["SRC-FINRA-RULE-3110||r", "SRC-ECH-UNB-BASELINE|UNB-XIN-SVC-005"],
    "customer-preference", "low", industries=["financial-services", "wealth-management", "banking"])

C.q(6, "Regulatory change", "How do you identify regulatory changes that affect your service, such as new DAF regulations, OFAC rule changes or new AI laws, and assess their impact?",
    "The service must remain compliant as rules change.",
    "Customer operations fall out of compliance after a rule change.",
    ["SRC-ECH-UNB-BASELINE|UNB-RCN-REG-001", "SRC-ISO-37301||r", "SRC-IRS-DAF-PROPOSED-REGS-2023||r"],
    "industry-convention", "high")
C.q(6, "Change implementation", "How quickly do you implement required regulatory changes, and how are customers informed and asked to adopt them?",
    "Customers need lead time and control over policy changes.",
    "Unannounced policy changes or late compliance.",
    ["SRC-ECH-UNB-BASELINE|CNV-GOV-005", "SRC-ECH-UNB-BASELINE|UNB-RCN-REG-001"],
    "customer-preference", "medium", products=["unbound"])
C.q(6, "Proposed versus final rules", "How does your product distinguish proposed rules from final and effective rules, for example the proposed DAF regulations under section 4966?",
    "Applying proposed rules as binding can restrict legitimate activity; ignoring them can leave sponsors unprepared.",
    "Incorrect grant restrictions or missed effective dates.",
    ["SRC-ECH-UNB-BASELINE|CNV-GRT-008", "SRC-IRS-DAF-PROPOSED-REGS-2023||d", "SRC-IRC-4966||r"],
    "customer-preference", "medium", products=["unbound"], industries=["donor-advised-funds"])
C.q(6, "Interpretation approval", "Who approves the legal interpretations built into your product rules when regulations change?",
    "Product rules apply interpretations at scale.",
    "Unapproved interpretation affects many customers at once.",
    ["SRC-ECH-UNB-BASELINE|UNB-REGMAP-006", "SRC-ECH-UNB-BASELINE|UNB-REGMAP-005"],
    "customer-preference", "medium")

C.q(7, "Service relationship notice", "Will you give us the information we need to notify our federal banking regulator of our service relationship with you, as the Bank Service Company Act requires, and tell us promptly of changes that affect that notice?",
    "Insured depository institutions must notify their regulator of service relationships covered by the BSCA.",
    "Bank fails to file or update a required service relationship notice.",
    ["SRC-BSCA|12 U.S.C. 1867(c)(2)|r", "SRC-INTERAGENCY-TPRM-2023||r"],
    "legal-regulatory", "medium", industries=["banking"], jurisdictions=["US-federal"],
    authority="OCC; FDIC; Federal Reserve",
    scope="The notice duty is the bank's; Echelon supplies information. Incident notification to banks is covered under the incident response category.")
C.q(7, "Regulation S-P notice", "If a breach involves our customers' information, will you notify us as soon as possible and within 72 hours, as amended Regulation S-P requires us to ensure of our service providers?",
    "Covered institutions must oversee service providers' breach notice.",
    "Broker-dealer or adviser misses its customer notification obligations.",
    ["SRC-SEC-REG-SP-2024||d"],
    "legal-regulatory", "high", industries=["financial-services", "wealth-management"], jurisdictions=["US-federal"],
    authority="SEC",
    scope="Applies where the customer is a covered institution under Regulation S-P; the 72-hour service provider notice is implemented through the customer's written policies and contract.")
C.q(7, "Regulatory reporting data", "Can your platform produce the data we need for our regulatory reports, such as OFAC blocked and rejected transaction reports and Form 990 Schedule D?",
    "Reports built manually from vendor data are error-prone.",
    "Late or inaccurate regulatory filings.",
    ["SRC-OFAC-REGS|31 CFR 501.603|d", "SRC-OFAC-REGS|31 CFR 501.604|d", "SRC-IRS-FORM-990||d", "SRC-ECH-UNB-BASELINE|CNV-FIN-009"],
    "customer-preference", "high", products=["unbound"], industries=["donor-advised-funds", "nonprofit"])
C.q(7, "Recordkeeping compatibility", "Do you retain records in a form that meets our recordkeeping obligations, for example SEC rules for broker-dealers or investment advisers?",
    "Regulated firms remain responsible for records held by vendors.",
    "Records unavailable or non-compliant at examination.",
    ["SRC-SEC-17A-4||d", "SRC-SEC-ADVISERS-BOOKS-RECORDS||d", "SRC-ECH-UNB-BASELINE|CNV-PLT-004"],
    "legal-regulatory", "medium", industries=["financial-services", "wealth-management"], jurisdictions=["US-federal"],
    authority="SEC; FINRA",
    scope="Applies to records the customer must keep under its own regulatory regime; whether Unbound holds such records depends on the customer's operating model.")
