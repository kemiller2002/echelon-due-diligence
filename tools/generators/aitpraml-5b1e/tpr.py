from qbc_aitpraml import Cat, challenge

C = Cat("TPR",
        industries=["all"],
        jurisdictions=["US-federal", "global"],
        products=["all-echelon-products"])

BANK = ["banking", "financial-services", "wealth-management", "donor-advised-funds"]
IAG = "SRC-INTERAGENCY-TPRM-2023"
PLAN = "Business plan section 12.02 (vendor governance) is a draft whose body is a generic template shared across sections and contains no vendor-specific rules."

C.au(1, title="Third-party inventory and criticality tiering",
     status="proposed-target-state",
     rationale="SOC2-013 requires inventory of critical services and subservice organizations; RR-REQ-X-073-r2 requires a critical-vendor register; UNB-XIN-SAS-011 requires the subprocessor register be generated from the vendor inventory. No Echelon vendor inventory was located. " + PLAN,
     target="Echelon keeps one vendor inventory that is the source for the subprocessor register, the SBOM-linked open-source inventory and the AI provider list. Each entry records service, data classes accessed, integration points, contract, owner, inherent risk tier and criticality to each customer-facing service. Tiering criteria are documented (data sensitivity, operational criticality, substitutability, regulatory relevance) and applied consistently. The inventory is reconciled quarterly against spend, contracts, identity provider integrations, network egress destinations and code dependencies, so unrecorded vendors surface automatically.",
     current="Not established.",
     intended="Create the inventory before any production deployment and generate the subprocessor register from it.",
     provable="Nothing.",
     statement="Echelon has not yet established its vendor inventory or tiering. It plans a single inventory that drives its subprocessor list, with documented tiering criteria and automated reconciliation.",
     kind="planned",
     controls=[1, 2], evrs=[1, 2],
     requirements=["SOC2-013", "RR-REQ-X-073-r2", "UNB-XIN-SAS-011"],
     freshness="P90D", mechanism="periodic-automated", automation="high",
     impl_cost="low", rec_cost="low",
     owner="Not assigned (proposed: Echelon vendor risk owner)",
     residual=["Free-tier or individually purchased tools may escape spend-based reconciliation."])

C.au(2, title="Pre-engagement vendor due diligence proportional to risk",
     status="proposed-target-state",
     rationale="SOC2-013 and SOC2-030 require due diligence and design review before new external APIs; RR-REQ-X-073-r2 requires assurance type and report period recording. No due diligence procedure or record exists.",
     target="Before a vendor is engaged or integrated, Echelon performs due diligence scaled to tier: for critical vendors, security assurance (SOC 2 Type 2 or equivalent with CUEC mapping), financial condition, ownership and sanctions screening, legal and regulatory standing, business continuity, subcontractor reliance and data location; for low-risk vendors, a short record. Integration with a new vendor is technically blocked until the inventory entry and approval exist: new egress destinations, OAuth applications and dependencies need an approved vendor record. Neither engineers nor AI agents can add a data-processing vendor on their own.",
     current="Not established.",
     intended="Implement a tiered due diligence checklist and tie it to the SOC2-030 design review gate.",
     provable="Nothing.",
     statement="Echelon plans tiered vendor due diligence before engagement, with technical blocks on unapproved integrations. No due diligence procedure is yet in place.",
     kind="planned",
     controls=[3, 4], evrs=[3, 4],
     requirements=["SOC2-013", "SOC2-030", "RR-REQ-X-073-r2"],
     freshness="per-event", mechanism="event-driven-automated", automation="partial",
     impl_cost="low", rec_cost="low",
     owner="Not assigned (proposed: Echelon vendor risk owner)")

C.au(3, title="Vendor contract requirements, including flow-through of customer and regulator rights",
     status="unknown",
     rationale="No vendor contract standards or executed vendor contracts were reviewed. Unbound requirements expect sponsor regulatory and audit needs to be supported but do not define Echelon's own vendor contract terms.",
     target="Contracts with vendors that touch customer data or critical services include: security obligations and right to assess; breach notification fast enough for Echelon to meet its own commitments (for example the bank service provider notice under the 2021 computer-security incident rule and 72-hour service provider notice under amended Regulation S-P); audit and regulator examination access that flows to Echelon's regulated customers; data use limits including no AI training; subcontractor approval; data location; business continuity and SLAs; and termination assistance with data return and deletion certification. A contract template and a gap register record where a vendor's standard terms fall short and who accepted the gap.",
     current="Unknown.",
     intended="Draft a vendor contract standard and gap register before first critical vendor engagement for a production service.",
     provable="Nothing.",
     statement="Echelon has not yet established vendor contract standards. It plans to require notification, audit, data-use, subcontracting and exit terms that allow it to meet obligations to regulated customers.",
     kind="not-available",
     controls=[5], evrs=[5],
     requirements=["SOC2-013"],
     freshness="per-event", mechanism="periodic-manual", automation="low",
     impl_cost="low", rec_cost="low",
     owner="Not assigned (proposed: Echelon counsel)",
     residual=["Large cloud and AI providers rarely accept negotiated terms; gaps must be risk-accepted and compensated."],
     open=["Which current vendors (cloud, source hosting, AI providers) are under standard click-through terms only?"])

C.au(4, title="Ongoing monitoring of vendors, assurance report review and CUEC operation",
     status="proposed-target-state",
     rationale="CNV-GOV-002 specifies SOC report gap computation, bridge letters treated as management assertions, stale-report alerts at 12 months, and tracking of exceptions and unmapped CUECs, with release 1 performing this as an annual review task. RR-REQ-X-073-r2 requires every CUEC mapped to an internal control owner before a vendor is marked Assured and allows AI only to extract report metadata for human confirmation. None is operating.",
     target="Critical vendors are monitored continuously for signals (status pages, breach disclosures, security advisories, ownership changes, financial distress) and reviewed formally at least annually. SOC reports are reviewed for scope, period, opinion, exceptions and CUECs; every CUEC is mapped to an Echelon control with an owner and evidence; bridge letters are recorded as management assertions that do not extend assurance; stale or qualified reports trigger compensating procedures or time-limited risk acceptance. Event triggers (breach, outage, ownership change, scope change) force out-of-cycle review. Issues are tracked to closure.",
     current="Not established.",
     intended="Run the CNV-GOV-002 annual review task from first vendor engagement; automate gap tracking later.",
     provable="Nothing.",
     statement="Echelon plans annual and event-triggered review of critical vendors, including SOC report and CUEC analysis, with continuous signal monitoring. Not yet operating.",
     kind="planned",
     controls=[6, 7], evrs=[6, 7],
     requirements=["CNV-GOV-002", "RR-REQ-X-073-r2", "SOC2-013", "SOC2-022"],
     freshness="P1Y", mechanism="periodic-manual", automation="partial",
     impl_cost="low", rec_cost="medium",
     owner="Not assigned (proposed: Echelon vendor risk owner)",
     challenge=challenge(
         intent="Customers want assurance that their vendor's vendors remain secure and reliable over time, not just at onboarding.",
         adverse="A critical vendor's controls degrade or it is breached and Echelon does not react.",
         conv_eff="Annual questionnaires sent to vendors are widely regarded as low-signal: answers are self-reported and dated, and large providers decline custom questionnaires.",
         legal="Not law for Echelon. Interagency Guidance expects banks to monitor third parties; banks expect their service providers to oversee subcontractors.",
         contract="Bank and broker-dealer customers commonly require subcontractor oversight.",
         history="Questionnaire-driven TPRM programs.",
         elim="Exposure to some vendors can be reduced structurally: minimize data shared, encrypt with Echelon-held keys where feasible, and design for vendor substitution.",
         auto="Signal feeds and assurance report expiry tracking.",
         cont="Continuous signal log and CUEC control evidence.",
         alt="Assurance-report analysis with mapped CUECs plus continuous external signals and data minimization, instead of custom annual questionnaires to large providers.",
         verif="Review records, CUEC mappings and signal logs are inspectable.",
         accept="Likely; regulators and auditors recognize SOC report review as stronger than questionnaires.",
         invalid="Vendors without assurance reports still need direct assessment.",
         conv_cost="medium (questionnaire administration)",
         alt_cost="low to medium",
         alt_risk="External rating services can be noisy and opaque.",
         pro=["Independent reports beat self-attestation.", "CUEC mapping closes the most common reliance gap."],
         con=["Small vendors lack reports; questionnaires remain necessary for them.", "Signal feeds cost money and produce false positives."],
         tech="stronger", inst="likely"))

C.au(5, title="Concentration risk and fourth-party visibility",
     status="unknown",
     rationale="UNB-CTL-006 requires modelling vendor data restrictions and correlated AI failures; SOC2-022 requires subservice organization controls where relevant; CNV-GOV-002 tracks coverage gaps. No concentration or fourth-party analysis exists.",
     target="Echelon maps which customer-facing services depend on each critical vendor and on that vendor's own critical providers (fourth parties), including carve-out subservice organizations named in vendor SOC reports. It measures concentration on single cloud regions, single AI providers and single identity or source-hosting providers, records the impact of each failing, and sets tolerances. Where a single provider is accepted, the exit plan and degraded-mode design (for example deterministic paths continuing without AI) are the mitigation.",
     current="Unknown.",
     intended="Produce a dependency map from the vendor inventory and vendor SOC report subservice sections.",
     provable="Nothing.",
     statement="Echelon has not yet analyzed vendor concentration or fourth-party dependencies. It plans to map them and to design critical paths to keep working when an AI provider is unavailable.",
     kind="not-available",
     controls=[8], evrs=[8],
     requirements=["UNB-CTL-006", "SOC2-022", "CNV-GOV-002", "CNV-AIO-001"],
     freshness="P1Y", mechanism="periodic-manual", automation="partial",
     impl_cost="low", rec_cost="low",
     owner="Not assigned (proposed: Echelon vendor risk owner)")

C.au(6, title="Exit and termination plans for critical vendors",
     status="proposed-target-state",
     rationale="CNV-GOV-009 requires commercial licences plus escrow or fork rights for release-1 production dependencies; business plan section 12.04 (continuity and exit) is a generic template draft. UNB-OPS-001 requires support for vendor failure. No exit plan exists.",
     target="Each critical vendor has a written exit plan: trigger conditions, alternate provider or in-house fallback, data export format, migration steps, time to exit, cost estimate and owner. Architecture favors substitutability: standard PostgreSQL managed by Strata rather than proprietary databases, provider-neutral AI interfaces with deterministic fallbacks, infrastructure as code. Exit plans for the most critical vendors are rehearsed (data export and restore on an alternate provider) on a defined cadence. Termination includes credential revocation, data return and deletion confirmation.",
     current="Not established.",
     intended="Write exit plans for cloud hosting and AI providers before production.",
     provable="Nothing. Strata exists as a declarative PostgreSQL schema tool in pilot status, supporting PostgreSQL 16 only.",
     statement="Echelon plans documented and rehearsed exit plans for critical vendors and an architecture that favors substitutable providers. No exit plans exist yet.",
     kind="planned",
     controls=[9], evrs=[9],
     requirements=["CNV-GOV-009", "UNB-OPS-001"],
     freshness="P1Y", mechanism="periodic-manual", automation="partial",
     impl_cost="medium", rec_cost="low",
     owner="Not assigned (proposed: Echelon engineering owner)",
     challenge=challenge(
         intent="Customers and regulators want assurance that failure or termination of a vendor will not strand the service.",
         adverse="A critical provider fails, changes terms or exits, and the service cannot continue or migrate in time.",
         conv_eff="Written exit plans are often never tested and decay; their value lies in rehearsal and in architecture that makes exit feasible.",
         legal="Not law for Echelon in the US. For EU financial entity customers, DORA requires exit strategies for ICT services supporting critical functions, which those customers will flow down.",
         contract="Often required by bank and EU financial customers.",
         history="Document-centric continuity planning.",
         elim="Substitutable architecture reduces lock-in: open-standard database, infrastructure as code, provider-neutral AI interfaces.",
         auto="Automated export and restore to an alternate environment as a scheduled job.",
         cont="Rehearsal results with time-to-restore.",
         alt="Rehearsed automated migration paths for the top dependencies instead of document-only exit plans for every vendor.",
         verif="Rehearsal records show actual time and completeness.",
         accept="Likely; tested exits are stronger than documents.",
         invalid="Some managed services have no practical alternative at equal capability.",
         conv_cost="low (documents)",
         alt_cost="medium (rehearsal infrastructure and time)",
         alt_risk="Maintaining portability limits use of provider-specific features.",
         pro=["Evidence of actual exit capability.", "Architecture benefits beyond exit."],
         con=["Rehearsal costs time for a small team.", "Customers may still require a document for every critical vendor."],
         tech="stronger", inst="likely"))

C.au(7, title="Third-party risk program governance aligned to the Interagency Guidance lifecycle",
     status="proposed-target-state",
     rationale="Unbound control matrix has vendor risk controls UNB-CTRL-082 to 084 (status Designed; no operating evidence). SOC2-013 covers inventory, due diligence, contracts and monitoring. " + PLAN + " No adopted TPRM policy exists.",
     target="An approved third-party risk policy defines the lifecycle used by Echelon (planning, due diligence and selection, contract negotiation, ongoing monitoring, termination) with governance across it (oversight, accountability, documentation, independent review), mirroring the stages of the 2023 Interagency Guidance so bank customers can map Echelon's practice to their own. It names the accountable owner and risk acceptance authority, sets reporting to leadership, and is independently reviewed. Echelon provides customers the information they need for their own oversight of Echelon as a third party, including its subcontractor oversight.",
     current="Not established.",
     intended="Adopt a TPRM policy based on the Interagency Guidance lifecycle when Echelon prepares for its first regulated customer.",
     provable="Nothing.",
     statement="Echelon has not yet adopted a third-party risk management policy. It plans a program aligned to the Interagency Guidance lifecycle and will provide customers the information needed to oversee Echelon as their third party.",
     kind="planned",
     controls=[10], evrs=[10],
     requirements=["SOC2-013"],
     freshness="P1Y", mechanism="periodic-manual", automation="low",
     impl_cost="low", rec_cost="low",
     owner="Not assigned (proposed: Echelon managing member)",
     residual=["Independent review of the TPRM program is difficult for a very small organization without external help."])

# ---------------- Controls ----------------
C.ctl(1, title="Single vendor inventory with documented tiering",
      objective="All third parties are recorded with service, data, integrations, owner and a tier derived from documented criteria.",
      type="administrative", level="L10-external-or-manual",
      systems=["not yet assigned"],
      related=["SOC2-013", "RR-REQ-X-073-r2", "UNB-CTRL-082"],
      refs=["SRC-NIST-CSF-2.0|GV.SC-04|d", f"{IAG}||r", "SRC-ISO-27001-2022|A.5.19|d"],
      evrs=[1], owner="Not assigned (proposed: Echelon vendor risk owner)")
C.ctl(2, title="Automated inventory reconciliation",
      objective="Quarterly automated comparison of the inventory with spend, contracts, identity provider applications, egress destinations and code dependencies flags unrecorded vendors.",
      type="detective-automated", level="L6-automated-analysis",
      systems=["not yet assigned"],
      refs=["SRC-CIS-CONTROLS-V8.1||r", "SRC-NIST-SP800-161-R1||r"],
      evrs=[2], owner="Not assigned (proposed: Echelon vendor risk owner)")
C.ctl(3, title="Tiered due diligence before engagement",
      objective="Due diligence depth follows tier; critical vendors require assurance report review, financial review, sanctions screening, BCP and subcontractor review before approval.",
      type="preventive-procedural", level="L10-external-or-manual",
      systems=["not yet assigned"],
      related=["SOC2-013", "UNB-CTRL-082"],
      refs=[f"{IAG}|Due Diligence and Third-Party Selection|d", "SRC-NIST-CSF-2.0|GV.SC-06|d", "SRC-NIST-SP800-53-R5|SR-6|r"],
      evrs=[3], owner="Not assigned (proposed: Echelon vendor risk owner)")
C.ctl(4, title="Technical block on unapproved vendor integrations",
      objective="New egress destinations, OAuth applications and data-processing dependencies require an approved vendor record before they can be enabled; engineers and agents cannot add them alone.",
      type="preventive-gate", level="L5-build-release-gate",
      systems=["not yet assigned"],
      policies=["SEC-SUPPLY-001"], related=["SOC2-030"],
      refs=["SRC-NIST-SP800-53-R5|SA-9|r", "SRC-ISO-27001-2022|A.5.19|r"],
      evrs=[4], owner="Not assigned (proposed: Echelon engineering owner)")
C.ctl(5, title="Vendor contract standard and gap register",
      objective="Contracts include security, notification, audit and regulator access, data use, subcontracting, location, continuity and exit terms; gaps are risk-accepted by a named authority.",
      type="administrative", level="L10-external-or-manual",
      systems=["not yet assigned"],
      refs=[f"{IAG}|Contract Negotiation|d", "SRC-NIST-CSF-2.0|GV.SC-05|d", "SRC-ISO-27001-2022|A.5.20|d", "SRC-EU-DORA|Art. 30|r"],
      evrs=[5], owner="Not assigned (proposed: Echelon counsel)")
C.ctl(6, title="Assurance report review with CUEC mapping and bridge-letter tracking",
      objective="Vendor SOC reports are reviewed for scope, period, opinion and exceptions; every CUEC is mapped to an owned Echelon control; bridge letters are recorded as assertions; stale reports trigger compensating procedures.",
      type="detective-manual", level="L10-external-or-manual",
      systems=["not yet assigned"],
      related=["CNV-GOV-002", "RR-REQ-X-073-r2", "UNB-CTRL-083"],
      refs=["SRC-AICPA-SOC2-GUIDE||r", "SRC-AICPA-TSC|CC9.2|d", f"{IAG}|Ongoing Monitoring|d"],
      evrs=[6], owner="Not assigned (proposed: Echelon vendor risk owner)")
C.ctl(7, title="Continuous vendor signal monitoring and event-triggered review",
      objective="Critical vendors are monitored for breach, outage, advisory, ownership and financial signals; triggers open out-of-cycle reviews; issues are tracked to closure.",
      type="detective-automated", level="L9-runtime-monitored",
      systems=["not yet assigned"],
      related=["UNB-CTRL-084"],
      refs=["SRC-NIST-CSF-2.0|GV.SC-07|d", "SRC-ISO-27001-2022|A.5.22|d"],
      evrs=[7], owner="Not assigned (proposed: Echelon vendor risk owner)")
C.ctl(8, title="Dependency and concentration map including fourth parties",
      objective="Customer-facing services are mapped to critical vendors and their critical providers; concentration tolerances are set and breaches escalated.",
      type="detective-manual", level="L10-external-or-manual",
      systems=["not yet assigned"],
      related=["UNB-CTL-006", "SOC2-022"],
      refs=[f"{IAG}||r", "SRC-EU-DORA|Art. 28|r", "SRC-NIST-SP800-161-R1||r"],
      evrs=[8], owner="Not assigned (proposed: Echelon vendor risk owner)")
C.ctl(9, title="Rehearsed exit plans for critical vendors",
      objective="Each critical vendor has an exit plan; the most critical are rehearsed by export and restore on an alternate provider; termination revokes access and confirms data deletion.",
      type="corrective", level="L8-adversarial-tested",
      systems=["Strata (pilot) for schema portability", "not yet assigned"],
      related=["CNV-GOV-009"],
      refs=[f"{IAG}|Termination|d", "SRC-NIST-CSF-2.0|GV.SC-10|d", "SRC-EU-DORA|Art. 28|r"],
      evrs=[9], owner="Not assigned (proposed: Echelon engineering owner)")
C.ctl(10, title="Approved TPRM policy with independent review",
       objective="A policy defines lifecycle, roles, risk acceptance authority and reporting; the program is independently reviewed periodically.",
       type="administrative", level="L10-external-or-manual",
       systems=["not yet assigned"],
       related=["UNB-CTRL-082", "UNB-CTRL-084"],
       refs=[f"{IAG}|Oversight and Accountability|d", "SRC-NIST-CSF-2.0|GV.SC-01|d", "SRC-ISO-27036||r"],
       evrs=[10], owner="Not assigned (proposed: Echelon managing member)")

# ---------------- Evidence ----------------
C.evr(1, title="Vendor inventory export", description="Current vendor inventory with tier, criticality per service, data classes and owner.",
      mechanism="periodic-automated", freshness="P90D", format="CSV/JSON", disclosure="nda")
C.evr(2, title="Inventory reconciliation report", description="Quarterly reconciliation results listing unrecorded vendors found and their disposition.",
      mechanism="periodic-automated", freshness="P90D", format="Report", disclosure="internal")
C.evr(3, title="Vendor due diligence file", description="Per vendor and tier: completed checks, findings, approver and date.",
      mechanism="event-driven-automated", freshness="per-event", format="Register entry with attachments")
C.evr(4, title="Integration approval gate records", description="Records of blocked and approved new egress destinations, OAuth apps and data-processing dependencies with linked vendor approvals.",
      mechanism="event-driven-automated", freshness="per-event", format="Gate log", disclosure="internal")
C.evr(5, title="Contract term checklist and gap acceptances", description="Per critical vendor: required terms present or absent, with risk acceptance records for gaps.",
      mechanism="periodic-manual", freshness="P1Y", format="Register entry", disclosure="internal")
C.evr(6, title="SOC report review records and CUEC mapping", description="Per vendor report: scope, period, opinion, exceptions, CUEC-to-control mapping, bridge letter status and compensating procedures.",
      mechanism="periodic-manual", freshness="P1Y", format="Review record", disclosure="nda")
C.evr(7, title="Vendor signal log and review triggers", description="Logged signals for critical vendors and resulting out-of-cycle reviews and issues.",
      mechanism="continuous-automated", freshness="P30D", format="Event log", disclosure="internal")
C.evr(8, title="Dependency and concentration map", description="Map of services to vendors and fourth parties with concentration measures and tolerances.",
      mechanism="periodic-manual", freshness="P1Y", format="Diagram and table", disclosure="nda")
C.evr(9, title="Exit plans and rehearsal results", description="Exit plan per critical vendor and dated rehearsal results with time to restore and gaps found.",
      mechanism="periodic-manual", freshness="P1Y", format="Plan and test record", disclosure="nda")
C.evr(10, title="TPRM policy and independent review report", description="Approved policy version and independent review findings with remediation.",
       mechanism="periodic-manual", freshness="P1Y", format="Policy and report", disclosure="nda")

# ---------------- Questions ----------------
C.q(1, "Vendor inventory", "Do you maintain an inventory of the third parties that support the services you provide to us, including what each provides and what data it can access?",
    "The customer's risk extends to its vendor's vendors.",
    "Unknown third parties hold customer data or support critical services.",
    ["SRC-ECH-UNB-SOC2-DIRECTIVE|SOC2-013", "SRC-NIST-CSF-2.0|GV.SC-04|r", "SRC-SA-SIG||r", "SRC-CSA-CAIQ-V4||r"],
    "industry-convention", "high",
    ["Provide a list of your critical third-party service providers.", "Do you maintain a vendor register?"])
C.q(1, "Tiering", "How do you tier vendors by inherent risk and criticality, and what criteria do you use?",
    "Oversight effort should match risk.",
    "High-risk vendors receive the same light review as low-risk ones.",
    [f"{IAG}|Planning|r", "SRC-NIST-CSF-2.0|GV.SC-04|d"],
    "supervisory-guidance", "medium", industries=BANK, authority="OCC; FDIC; Federal Reserve (expectation on banks, flowed to their service providers)")
C.q(1, "Critical vendors", "Which of your vendors are critical to the service you provide to us, and what would happen to our service if each failed?",
    "The customer needs to understand its fourth-party dependencies for its own continuity planning.",
    "Hidden single points of failure.",
    [f"{IAG}||r", "SRC-FFIEC-BCM-BOOKLET||r", "SRC-EU-DORA|Art. 28|r"],
    "supervisory-guidance", "high", industries=BANK, authority="OCC; FDIC; Federal Reserve")
C.q(1, "AI and open source in inventory", "Are AI model providers and material open-source components included in your third-party inventory and risk tiering?",
    "AI providers and open-source projects are dependencies that often escape vendor programs.",
    "Unassessed reliance on AI providers or unmaintained open-source components.",
    ["SRC-NIST-AI-RMF-1.0|GOVERN 6.1|r", "SRC-OPENSSF-S2C2F||r"],
    "customer-preference", "medium")
C.q(1, "Inventory completeness", "How do you verify your vendor inventory is complete, for example by reconciling against spend, contracts and technical integrations?",
    "Inventories drift without reconciliation.",
    "Shadow vendors outside oversight.",
    ["SRC-CIS-CONTROLS-V8.1||r", "SRC-NIST-SP800-161-R1||r"],
    "customer-preference", "low")

C.q(2, "Due diligence", "What due diligence do you perform before engaging a new vendor that will access customer data or support a critical service?",
    "Vendor selection is where most risk can be avoided cheaply.",
    "Onboarding vendors with weak controls.",
    [f"{IAG}|Due Diligence and Third-Party Selection|d", "SRC-NIST-SP800-53-R5|SR-6|r", "SRC-AICPA-TSC|CC9.2|d", "SRC-SA-SIG||r"],
    "industry-convention", "high")
C.q(2, "Proportional diligence", "How does the depth of your due diligence differ between critical and low-risk vendors?",
    "Proportionality shows the program is risk-based.",
    "Resources misallocated to low-risk vendors while critical ones are under-reviewed.",
    [f"{IAG}||d", "SRC-TPRM-COMMUNITY-BANK-GUIDE-2024||r"],
    "supervisory-guidance", "medium", industries=BANK, authority="OCC; FDIC; Federal Reserve")
C.q(2, "Vendor financial condition", "Do you evaluate the financial condition and viability of critical vendors before and during the relationship?",
    "A vendor failure can be financial, not only technical.",
    "Abrupt loss of a critical vendor through insolvency.",
    [f"{IAG}|Due Diligence and Third-Party Selection|r"],
    "supervisory-guidance", "medium", industries=BANK, authority="OCC; FDIC; Federal Reserve")
C.q(2, "Vendor screening", "Do you screen prospective vendors and their owners against sanctions lists and for adverse media before engagement?",
    "Paying a sanctioned vendor is a violation and a reputational event.",
    "Dealing with a blocked person through the vendor chain.",
    ["SRC-OFAC-REGS||r", "SRC-OFAC-COMPLIANCE-FRAMEWORK|Risk Assessment|r"],
    "legal-regulatory", "medium", jurisdictions=["US-federal"], authority="OFAC",
    scope="OFAC prohibitions apply to Echelon as a US person; screening is the conventional means of compliance, not itself mandated.")
C.q(2, "Integration approval", "Can an engineer or an AI agent connect a new third-party service that receives customer data without vendor risk approval? How is that prevented?",
    "Integrations added during development bypass procurement.",
    "Customer data flows to an unassessed service.",
    ["SRC-ECH-UNB-SOC2-DIRECTIVE|SOC2-030", "SRC-NIST-SP800-53-R5|SA-9|r"],
    "customer-preference", "high")

C.q(3, "Contract terms", "What security, confidentiality, incident notification, audit and data return terms do you require in contracts with vendors that handle customer data?",
    "Contract terms are the enforceable part of vendor oversight.",
    "No recourse or information when a vendor fails.",
    [f"{IAG}|Contract Negotiation|d", "SRC-ISO-27001-2022|A.5.20|d", "SRC-NIST-CSF-2.0|GV.SC-05|d", "SRC-FTC-SAFEGUARDS-RULE|314.4(f)|r"],
    "industry-convention", "high")
C.q(3, "Regulator access", "Do your contracts with subcontractors preserve audit and examination access for you, for us and for our regulators?",
    "Regulated customers must be able to examine outsourced functions end to end.",
    "Examination obstructed at the subcontractor level.",
    [f"{IAG}|Contract Negotiation|d", "SRC-BSCA|12 U.S.C. 1867(c)|r", "SRC-EU-DORA|Art. 30|d", "SRC-FINRA-RN-21-29||r"],
    "supervisory-guidance", "high", industries=BANK, jurisdictions=["US-federal", "EU"], authority="OCC; FDIC; Federal Reserve; FINRA; EU competent authorities")
C.q(3, "Notification timing", "Do your vendor contracts require incident notification quickly enough for you to meet your notification obligations to us?",
    "Notification chains fail when subcontractor deadlines are longer than customer deadlines.",
    "Late notice to the customer and its regulators.",
    ["SRC-CIRN-RULE-2021||r", "SRC-SEC-REG-SP-2024||r", "SRC-NYDFS-PART-500|500.11|r"],
    "contractual-common", "high", industries=BANK)
C.q(3, "Vendor data use", "Do your vendor contracts limit what vendors may do with metadata, telemetry and derived data generated from our use of your service, not only with our content itself?",
    "Usage metadata and derived data are often excluded from confidentiality terms and reused for analytics or AI training.",
    "Customer activity patterns or derived data used beyond the contracted purpose.",
    ["SRC-GDPR|Art. 28|r", "SRC-GLBA||r", "SRC-ISO-27001-2022|A.5.20|r"],
    "contractual-common", "high")
C.q(3, "Continuity terms", "Do contracts with critical vendors include service levels, business continuity obligations and termination assistance?",
    "Continuity of the customer's service depends on vendor commitments.",
    "No obligation on the vendor to support recovery or transition.",
    [f"{IAG}|Contract Negotiation|d", "SRC-EU-DORA|Art. 30|r", "SRC-FFIEC-BCM-BOOKLET||r"],
    "industry-convention", "medium")

C.q(4, "Ongoing monitoring", "How do you monitor the security and performance of your critical vendors after onboarding?",
    "Risk changes during the relationship.",
    "Degraded vendor controls go unnoticed.",
    [f"{IAG}|Ongoing Monitoring|d", "SRC-NIST-CSF-2.0|GV.SC-07|d", "SRC-ISO-27001-2022|A.5.22|d", "SRC-CSA-CCM-V4|STA|r"],
    "industry-convention", "high")
C.q(4, "SOC report review", "Do you obtain and review your critical vendors' SOC reports at least annually, and how do you handle exceptions, qualified opinions and gaps between the report period and today?",
    "SOC reports are only useful if read and acted on.",
    "Reliance on stale or qualified assurance.",
    ["SRC-ECH-UNB-BASELINE|CNV-GOV-002", "SRC-AICPA-SOC2-GUIDE||r", "SRC-AICPA-TSC|CC9.2|r"],
    "industry-convention", "high")
C.q(4, "CUECs", "How do you identify and operate the complementary user entity controls listed in your vendors' SOC reports?",
    "Vendor assurance depends on user controls being in place.",
    "Assumed vendor protections that require Echelon action never operate.",
    ["SRC-ECH-UNB-BASELINE|RR-REQ-X-073-r2", "SRC-AICPA-SOC2-GUIDE||r"],
    "industry-convention", "medium")
C.q(4, "Reassessment triggers", "What events cause an out-of-cycle reassessment of a vendor, such as a breach, outage, ownership change or new service?",
    "Material events change risk immediately.",
    "Delayed response to a vendor incident.",
    [f"{IAG}|Ongoing Monitoring|r", "SRC-NIST-CSF-2.0|GV.SC-07|r"],
    "supervisory-guidance", "medium", industries=BANK, authority="OCC; FDIC; Federal Reserve")
C.q(4, "Continuous signals", "Do you use continuous external signals, such as breach disclosures, security advisories or rating services, to monitor vendors between reviews?",
    "Point-in-time reviews miss developing problems.",
    "Late awareness of vendor compromise.",
    ["SRC-NIST-CSF-2.0|GV.SC-07|r"],
    "customer-preference", "low")
C.q(4, "Issue tracking", "How are vendor-related issues and findings tracked, escalated and closed?",
    "Findings without follow-through do not reduce risk.",
    "Known vendor weaknesses persist.",
    [f"{IAG}|Ongoing Monitoring|r", "SRC-ISO-27036||r"],
    "industry-convention", "low")

C.q(5, "Concentration risk", "Do you assess concentration risk, such as several critical functions depending on one cloud provider, one region or one AI provider?",
    "Concentration turns one vendor failure into a total outage.",
    "Correlated failure across services.",
    [f"{IAG}||r", "SRC-EU-DORA|Art. 28|r", "SRC-FFIEC-ARCHITECTURE-BOOKLET||r"],
    "supervisory-guidance", "medium", industries=BANK, jurisdictions=["US-federal", "EU"], authority="OCC; FDIC; Federal Reserve; EU competent authorities")
C.q(5, "Fourth parties", "Do you identify the critical subcontractors of your critical vendors, and how do you gain assurance over them?",
    "Fourth-party failures propagate to the customer.",
    "Unknown fourth-party dependency causes an outage or breach.",
    [f"{IAG}||r", "SRC-NIST-SP800-161-R1||r", "SRC-SA-SIG||r"],
    "industry-convention", "medium")
C.q(5, "Provider failure impact", "If your primary cloud provider or AI provider became unavailable for an extended period, what would happen to our service?",
    "The customer needs to plan for its vendor's dependencies.",
    "Prolonged service loss.",
    ["SRC-ECH-UNB-BASELINE|CNV-AIO-001", "SRC-NIST-AI-RMF-1.0|GOVERN 6.2|r", "SRC-FFIEC-BCM-BOOKLET||r"],
    "customer-preference", "high")
C.q(5, "Jurisdictional concentration", "Are any critical vendors or their operations concentrated in a single country or jurisdiction that creates legal or geopolitical risk?",
    "Jurisdiction affects data access by authorities and continuity.",
    "Service disruption or forced data access through foreign law.",
    ["SRC-EU-DORA|Art. 28|r", "SRC-NIST-SP800-161-R1||r"],
    "customer-preference", "low")
C.q(5, "Carve-out subservice organizations", "When a vendor's SOC report carves out its subservice organizations, how do you obtain assurance over those carved-out providers?",
    "Carve-outs leave gaps that the user must fill.",
    "Unassured subservice organization in the critical path.",
    ["SRC-AICPA-SOC2-GUIDE||r", "SRC-ECH-UNB-SOC2-DIRECTIVE|SOC2-022"],
    "industry-convention", "low")

C.q(6, "Exit plans", "Do you have documented exit plans for your critical vendors, including alternate providers and the time needed to transition?",
    "Exit readiness determines resilience to vendor failure or termination.",
    "Inability to replace a failing vendor in time.",
    [f"{IAG}|Termination|d", "SRC-EU-DORA|Art. 28|d", "SRC-NIST-CSF-2.0|GV.SC-10|r"],
    "supervisory-guidance", "medium", industries=BANK, jurisdictions=["US-federal", "EU"], authority="OCC; FDIC; Federal Reserve; EU competent authorities")
C.q(6, "Exit testing", "Have you tested or rehearsed any of your vendor exit plans? What were the results?",
    "Untested exit plans are assumptions.",
    "Exit plan fails when invoked.",
    ["SRC-EU-DORA|Art. 28|r", "SRC-FFIEC-BCM-BOOKLET||r"],
    "customer-preference", "low")
C.q(6, "Vendor offboarding", "When a vendor relationship ends, how do you ensure return or deletion of data and revocation of the vendor's access?",
    "Offboarding failures leave data and access behind.",
    "Former vendor retains customer data or access.",
    [f"{IAG}|Termination|d", "SRC-NIST-CSF-2.0|GV.SC-10|d", "SRC-NIST-SP800-88||r"],
    "industry-convention", "medium")
C.q(6, "Lock-in", "How do you avoid lock-in to proprietary components such as databases or AI providers that would make exit impractical?",
    "Lock-in turns vendor risk into permanent dependency.",
    "Exit is technically or economically infeasible.",
    ["SRC-ECH-UNB-BASELINE|CNV-GOV-009", "SRC-EU-DORA|Art. 28|r"],
    "customer-preference", "low")

C.q(7, "TPRM policy", "Do you have a third-party risk management policy approved by senior management? When was it last reviewed?",
    "A policy establishes accountability and minimum standards.",
    "Ad hoc vendor decisions.",
    [f"{IAG}|Oversight and Accountability|d", "SRC-NIST-CSF-2.0|GV.SC-01|d", "SRC-ISO-27001-2022|A.5.19|d", "SRC-CSA-CAIQ-V4||r"],
    "industry-convention", "high")
C.q(7, "Lifecycle alignment", "Does your third-party risk program follow a lifecycle comparable to the 2023 Interagency Guidance: planning, due diligence, contract negotiation, ongoing monitoring and termination, with oversight throughout?",
    "Banks map their service providers' practices to the guidance they are examined against.",
    "Gaps in a stage of the lifecycle the bank must cover.",
    [f"{IAG}||d", "SRC-OCC-BULLETIN-2023-17||d", "SRC-FDIC-FIL-29-2023||d", "SRC-FRB-SR-23-4||d"],
    "supervisory-guidance", "high", industries=BANK, jurisdictions=["US-federal"], authority="OCC; FDIC; Federal Reserve")
C.q(7, "Program review", "Is your third-party risk program subject to independent review or internal audit?",
    "Independent review tests whether the program operates as designed.",
    "Program exists on paper only.",
    [f"{IAG}|Oversight and Accountability|r"],
    "supervisory-guidance", "medium", industries=BANK, authority="OCC; FDIC; Federal Reserve")
C.q(7, "Risk reporting", "How is third-party risk reported to your leadership, and what do you share with customers about it?",
    "Leadership must see vendor risk to act on it.",
    "Material vendor risk unknown to decision makers.",
    [f"{IAG}|Oversight and Accountability|r", "SRC-NIST-CSF-2.0|GV.SC-03|r"],
    "industry-convention", "low")
C.q(7, "Risk acceptance", "Who has authority to accept residual vendor risk, and how are those acceptances recorded and time-limited?",
    "Risk acceptance must be accountable and revisited.",
    "Indefinite undocumented acceptance of vendor gaps.",
    ["SRC-ECH-UNB-SOC2-DIRECTIVE|SOC2-033", "SRC-ECH-UNB-BASELINE|CNV-GOV-002"],
    "industry-convention", "medium")
C.q(7, "Support for customer oversight", "As our third party, what information and access will you provide so we can perform our own due diligence and ongoing monitoring of you?",
    "The bank's obligations to oversee Echelon depend on Echelon's cooperation.",
    "Customer cannot satisfy examiner expectations about its oversight of Echelon.",
    [f"{IAG}||d", "SRC-TPRM-COMMUNITY-BANK-GUIDE-2024||r", "SRC-FINRA-RN-21-29||r"],
    "supervisory-guidance", "high", industries=BANK, authority="OCC; FDIC; Federal Reserve; FINRA")
