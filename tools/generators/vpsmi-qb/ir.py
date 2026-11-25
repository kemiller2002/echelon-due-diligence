from common import *

def build():
    c = Cat("IR")
    NA = "not yet assigned"
    e1 = c.evr(1, "Approved incident response plan and playbooks",
               "Versioned, approved incident response plan with severity model, roles, playbooks (unauthorized grant or payment instruction, tenant data exposure, compromised AI agent, compromised build pipeline, ransomware, credential compromise), regulatory notification matrix and annual review record.",
               NA, "periodic-manual", "P1Y", disclosure="nda")
    e2 = c.evr(2, "Incident roles, on-call roster and external retainer record",
               "Named incident commander and deputies, on-call schedule, escalation tree, customer contact registry with verification dates, and retained outside counsel and forensic firm (or the absence of each).",
               NA, "periodic-manual", "P90D", disclosure="customer-only")
    e3 = c.evr(3, "Exercise record",
               "Tabletop and technical exercise records: date, scenario, participants, timings for key actions (log retrieval, account disablement, payment hold, key rotation), gaps found and corrective action status.",
               NA, "periodic-manual", "P1Y", disclosure="nda", notes="SOC2-015 requires dated evidence of incident response tabletop exercises.")
    e4 = c.evr(4, "Incident timeline and notification log",
               "Per incident: detection, determination, containment, eradication and recovery timestamps; each notification sent (recipient, legal basis or contract clause, deadline, time sent, content hash, channel, acknowledgment).",
               NA, "event-driven-automated", "per-event", prov=["incident id", "actor", "timestamp", "obligation id", "content hash"],
               signing="Proposed: append-only, signed timeline", disclosure="customer-only")
    e5 = c.evr(5, "Regulatory notification obligation matrix",
               "Machine-readable matrix of notification obligations by customer type and jurisdiction (CIRN rule bank service provider notice, Regulation S-P service provider notice, state breach laws, NYDFS 500.17 support, GDPR Article 33 processor notice, contractual terms), with deadlines, triggers, recipients and contact sources, reviewed by counsel.",
               NA, "periodic-manual", "P1Y", disclosure="nda")
    e6 = c.evr(6, "Forensic evidence preservation and chain of custody record",
               "Preserved artifacts (logs, snapshots, images, agent ledgers) with hashes, custody transfers, storage location, access log and retention or legal hold status.",
               NA, "event-driven-automated", "per-event", disclosure="auditor-only")
    e7 = c.evr(7, "Post-incident report and corrective action tracker",
               "Root cause analysis, contributing factors, customer-facing summary, corrective actions with owners and due dates, and verification that threats, invariants, tests and detections were updated.",
               NA, "event-driven-automated", "per-event", disclosure="customer-only")
    e8 = c.evr(8, "Ransomware readiness evidence",
               "Immutable or logically isolated backup configuration, restore test results with timing, and the approved ransom payment decision policy including sanctions screening steps.",
               NA, "periodic-automated", "P90D", disclosure="nda")
    e9 = c.evr(9, "Containment action record",
               "Each containment action (credential revocation, tenant isolation, platform hold, agent kill switch) with authority, scope, timing, sponsor notification and release.",
               NA, "event-driven-automated", "per-event", disclosure="customer-only")

    k1 = c.ctl(1, "Approved, scenario-specific incident response plan",
               "An approved plan with severity model and playbooks covering Unbound-specific scenarios is reviewed annually and after significant incidents.",
               "administrative", "L10-external-or-manual", [NA], [e1], related=["SOC2-026", "UNB-CTRL-076", "UNB-OPS-001"],
               fw=[R("SRC-NIST-SP800-61-R3"), R("SRC-NIST-SP800-53-R5", "IR-8"), R("SRC-CSA-CCM-V4", "SEF-03"), R("SRC-ISO-27002-2022", "5.24")])
    k2 = c.ctl(2, "Defined incident roles, on-call and external support",
               "Incident commander, deputies and on-call coverage are defined with no single-person dependency; outside counsel and forensic support are pre-arranged; customer contacts are verified at least quarterly.",
               "administrative", "L10-external-or-manual", [NA], [e2], fw=[R("SRC-CSA-CCM-V4", "SEF-08"), R("SRC-NIST-SP800-53-R5", "IR-7")])
    k3 = c.ctl(3, "Annual tabletop and technical response exercises",
               "At least annual tabletop exercises and semiannual technical drills with timing measurement and tracked corrective actions.",
               "detective-manual", "L10-external-or-manual", [NA], [e3], related=["SOC2-015"],
               fw=[R("SRC-NIST-SP800-53-R5", "IR-3"), R("SRC-CSA-CCM-V4", "SEF-04"), D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-015", "derived-from")])
    k4 = c.ctl(4, "Obligation-driven notification workflow with deadline tracking",
               "Each incident is evaluated against the notification obligation matrix; deadlines start automatically at the defined trigger; notifications are sent over authenticated channels and logged with acknowledgment.",
               "preventive-procedural", "L9-runtime-monitored", [NA], [e4, e5], related=["SOC2-026", "REQ-X-016"],
               fw=[R("SRC-CSA-CCM-V4", "SEF-07"), R("SRC-NIST-CSF-2.0", "RS.CO-02"), R("SRC-NIST-CSF-2.0", "RS.CO-03"), R("SRC-CIRN-RULE-2021", "12 CFR 53.4"), R("SRC-SEC-REG-SP-2024", "17 CFR 248.30")])
    k5 = c.ctl(5, "Forensic preservation and chain of custody",
               "On incident declaration, relevant logs, snapshots and agent ledgers are preserved with hashes and custody records under legal hold.",
               "corrective", "L10-external-or-manual", [NA], [e6], related=["REQ-X-016", "UNB-CTRL-077"],
               fw=[R("SRC-ISO-27002-2022", "5.28"), R("SRC-NIST-CSF-2.0", "RS.AN-07")])
    k6 = c.ctl(6, "Post-incident review feeding threats, tests and detections",
               "Every significant incident produces a root cause analysis, a customer summary and tracked corrective actions, and updates threat models, invariants, regression tests and detections.",
               "corrective", "L10-external-or-manual", [NA, "Tutela (requires incidents to feed threats, invariants and regression evidence; not operated)"], [e7],
               related=["SOC2-026", "UNB-CTRL-078"], fw=[R("SRC-ISO-27002-2022", "5.27"), R("SRC-NIST-CSF-2.0", "ID.IM-03")])
    k7 = c.ctl(7, "Ransomware resilience and ransom decision policy",
               "Backups are immutable or isolated from production credentials and restore-tested; any ransom decision follows an approved policy with counsel, insurer and sanctions screening.",
               "corrective", "L10-external-or-manual", [NA], [e8], related=["UNB-GAP-034"],
               fw=[R("SRC-OFAC-REGS"), R("SRC-FFIEC-BCM-BOOKLET")])
    k8 = c.ctl(8, "Rapid containment including platform holds and agent kill switch",
               "Pre-authorized containment actions (credential revocation, tenant isolation, sponsor-policy holds that never move funds, AI agent kill switch) execute within minutes and notify the sponsor's designated officer immediately.",
               "corrective", "L9-runtime-monitored", [NA], [e9], related=["CNV-PLT-007", "UNB-XIN-IAM-005", "SOC2-017"],
               fw=[D("SRC-ECH-UNB-BASELINE", "CNV-PLT-007", "derived-from"), R("SRC-NIST-SP800-53-R5", "IR-4")])

    ch_ttx = challenge(
        customer_intent="Confidence that the vendor can actually execute its plan under pressure.",
        adverse_outcome="Slow, confused response and missed notification deadlines.",
        conventional_control_effectiveness="Annual discussion-based tabletops test coordination but not technical capability; findings are often not tracked to closure.",
        legally_required="Not for Echelon directly; NYDFS 500.16 and PCI DSS 12.10.2 require testing for covered entities.",
        contractually_required="Commonly asked; sometimes required annually.",
        historical_convention="Annual tabletop with sign-in sheet.",
        architectural_elimination="Not applicable.",
        automatic_enforcement="Scheduled technical drills (restore, revoke, hold, kill switch) run automatically in a non-production cell with timing captured.",
        continuous_evidence="Drill timing records and corrective action aging.",
        stronger_alternative="Annual tabletop for decisions and communications plus frequent automated technical drills measuring time to contain.",
        alternative_verifiable="Yes, from drill records.",
        customer_acceptance_likelihood="Likely; it is additive.",
        invalidating_conditions="Drills only in environments that differ from production.",
        conventional_cost="low", alternative_cost="medium",
        alternative_risks="Automated drills can create a false sense of readiness for human decisions such as regulatory determinations.",
        supporting_arguments=["Measured technical response time is more informative than attendance at a tabletop."],
        opposing_arguments=["Auditors look for the tabletop artifact specifically."],
        technical_effectiveness="stronger", institutional_acceptance="likely")
    ch_notify = challenge(
        customer_intent="Learn about incidents fast enough to meet the customer's own legal deadlines and protect its clients.",
        adverse_outcome="Customer misses regulatory deadlines or learns of an incident from the press.",
        conventional_control_effectiveness="Fixed-hour contractual clauses (for example 24, 48 or 72 hours) vary by customer and are measured from ambiguous triggers; vendors often delay notice until confirmation.",
        legally_required="Yes in part: the CIRN rule requires bank service providers to notify affected banking organizations as soon as possible for qualifying disruptions; amended Regulation S-P requires covered institutions to ensure service providers notify within 72 hours of becoming aware of a breach; state laws require service providers to notify data owners.",
        contractually_required="Nearly always negotiated.",
        historical_convention="Notice within 24 to 72 hours of discovery or confirmation.",
        architectural_elimination="Not applicable.",
        automatic_enforcement="Obligation matrix computes the earliest applicable deadline per customer at incident declaration.",
        continuous_evidence="Notification log with deadline and sent timestamps.",
        stronger_alternative="Single uniform early-notice commitment (initial notice within 24 hours of reasonable suspicion affecting customer data or covered services, with updates every 24 hours), satisfying the strictest common obligation, plus structured follow-up data packages.",
        alternative_verifiable="Yes, via the notification log.",
        customer_acceptance_likelihood="Likely; uniform early notice is generally welcomed.",
        invalidating_conditions="Very small team cannot staff 24-hour notice; law enforcement delay requests.",
        conventional_cost="low", alternative_cost="low",
        alternative_risks="Early notices on suspicion may later prove false alarms and cause customer burden.",
        supporting_arguments=["Customers' own deadlines (36 hours for banks under CIRN, 72 hours under NYDFS) require earlier vendor notice."],
        opposing_arguments=["Counsel may prefer flexible 'without undue delay' language to limit liability."],
        technical_effectiveness="stronger", institutional_acceptance="likely")
    ch_roles = challenge(
        customer_intent="Someone competent and empowered will run the response at any hour.",
        adverse_outcome="Key-person unavailability stalls response.",
        conventional_control_effectiveness="Named roles on paper do not ensure availability; small vendors often list one person in several roles.",
        legally_required="No.", contractually_required="Customers ask for named contacts and 24x7 escalation.",
        historical_convention="Incident response team roster.",
        architectural_elimination="Automated containment reduces the human actions needed in the first hour.",
        automatic_enforcement="Pre-authorized automated containment; paging with escalation.",
        continuous_evidence="On-call schedule coverage report; drill timings.",
        stronger_alternative="Automated first-hour containment plus a retained incident response firm on contract for surge capacity and independence.",
        alternative_verifiable="Partially: retainer contract and drill timing records.",
        customer_acceptance_likelihood="Uncertain while Echelon has very few personnel.",
        invalidating_conditions="Founder-only organization with no retainer.",
        conventional_cost="medium", alternative_cost="medium",
        alternative_risks="Retained firm lacks system familiarity unless onboarded.",
        supporting_arguments=["A retainer converts key-person risk into a contractual capability."],
        opposing_arguments=["Retainers cost money before revenue."],
        technical_effectiveness="equivalent", institutional_acceptance="uncertain")

    a1 = c.au(1, "Incident response plan and severity model", "proposed-target-state",
              "SOC2-026 requires documented detection, triage, containment, remediation, communication and lessons learned; UNB-GAP-034 and UNB-OPS-001 call for cyber incident response; no plan exists. The business plan section on incident learning is a draft governance position, not a plan.",
              "An approved incident response plan aligned with NIST SP 800-61 Rev. 3 and CSF 2.0 covers detection, triage, containment, eradication, recovery and post-incident review; defines security incident, privacy breach and outage and how one event can trigger several obligations; uses a severity model that drives escalation and notification; includes playbooks for unauthorized grant or payment instructions, tenant data exposure, compromised AI agent, compromised build pipeline, credential compromise and ransomware; is reviewed annually; and a summary is shared with customers.",
              "No incident response plan exists. Not established.",
              "Write and approve the plan before any customer production data is loaded.", "Nothing.",
              "Echelon does not yet have an adopted incident response plan; one will be established before Unbound handles customer production data.",
              "not-available", [k1], [e1], requirements=["SOC2-026", "UNB-GAP-034", "UNB-OPS-001"], freshness="P1Y", mechanism="periodic-manual", automation="low",
              impl="low", rec="low", oq=["Who will approve the incident response plan for Echelon Foundry, LLC?"])
    a2 = c.au(2, "Incident response roles, on-call coverage and external support", "unknown",
              "Headcount, named security officer and retainers are not established (current-state brief). No cyber insurance is established.",
              "A named incident commander and at least one trained deputy, 24x7 paging with escalation, a retained incident response and forensics firm, outside breach counsel, and a verified customer contact registry; AI agents may gather evidence and draft communications but may not send regulatory or customer notices, release holds or destroy evidence without human approval.",
              "Unknown; no evidence located. No named security officer, retainer or insurance located.",
              "Assign roles and contract a retainer before production.", "Nothing.",
              "Incident response roles and external support have not yet been established.", "not-available", [k2], [e2], requirements=["SOC2-017"],
              mechanism="periodic-manual", automation="low", impl="medium", rec="medium", challenge=ch_roles,
              oq=["Will Echelon retain an incident response firm and breach counsel, and when?", "Will Echelon obtain cyber insurance (see INS)?"])
    a3 = c.au(3, "Incident response testing and exercises", "proposed-target-state",
              "SOC2-015 requires dated evidence of incident response tabletop exercises; none has been held.",
              "Annual tabletop exercises covering ransomware, insider misuse, compromised AI agent, cross-tenant exposure and an incident during year-end giving peaks, with customer participation offered; semiannual automated technical drills measuring time to retrieve logs, disable accounts, place a sponsor-policy hold, revoke agent credentials and rotate keys; corrective actions tracked to closure and summaries shared.",
              "No exercise has occurred.", "Hold the first tabletop when the plan is approved.", "Nothing.",
              "No incident response exercise has yet been conducted; exercises are planned once the plan is adopted.", "not-available", [k3], [e3],
              requirements=["SOC2-015"], freshness="P1Y", mechanism="periodic-manual", automation="partial", impl="low", rec="low", challenge=ch_ttx)
    a4 = c.au(4, "Customer incident notification commitments", "proposed-target-state",
              "REQ-X-016 requires incident records to define earliest credible compromise and independent channels; UNB-XIN-IAM-005 requires tenant notification of break-glass within 1 hour; CNV-PLT-007 requires immediate notice of platform holds. No general customer breach notice commitment exists.",
              "Initial notice to affected customers within 24 hours of reasonable suspicion that customer data or covered services are affected, with updates at least every 24 hours until containment and a final report; the clock starts at reasonable suspicion, not confirmation; notices include what is known, affected data and tenants, actions taken, recommended customer actions and contact; notices are sent to registered contacts and confirmed over a second authenticated channel; subprocessor incidents and incidents affecting shared infrastructure or the same release are included.",
              "Not established.", "Adopt in the security addendum after counsel review.", "Nothing.",
              "Customer incident notification terms have not yet been adopted; Echelon will propose specific timelines in its security addendum.", "not-available", [k4], [e4, e5],
              requirements=["REQ-X-016", "UNB-XIN-IAM-005", "CNV-PLT-007"], mechanism="event-driven-automated", automation="partial", disclosure="nda", impl="low", rec="low",
              challenge=ch_notify)
    a5 = c.au(5, "Bank service provider notification under the 2021 Computer-Security Incident Notification rule", "unknown",
              "Whether Unbound's customers will include banking organizations, and whether Echelon will perform covered services subject to the Bank Service Company Act, is not established. No Echelon source addresses the rule.",
              "Where Echelon provides services to a banking organization subject to the Bank Service Company Act, it notifies each affected bank customer's designated contacts as soon as possible after determining that a computer-security incident has materially disrupted or degraded, or is reasonably likely to materially disrupt or degrade, covered services for four or more hours, and supports the bank's own 36-hour determination and notification to its primary federal regulator with rapid, structured facts. Scheduled maintenance previously communicated is excluded as the rule provides. Designated contacts are collected at onboarding and verified.",
              "Unknown; no evidence located.", "Determine applicability with counsel and build into the obligation matrix.", "Nothing.",
              "Echelon has not yet established a process for bank service provider incident notification; applicability depends on the customer and services, and will be determined with counsel.",
              "not-available", [k4], [e4, e5], mechanism="event-driven-automated", automation="partial", impl="low", rec="low",
              oq=["Will any Unbound customer be a banking organization (for example a bank or trust company acting as or for a DAF sponsor)?", "Does Unbound constitute covered services under the Bank Service Company Act?"])
    a6 = c.au(6, "Service provider notice under amended SEC Regulation S-P (2024)", "unknown",
              "Applicability depends on whether customers are covered institutions (broker-dealers, registered investment advisers, investment companies, transfer agents). Wealth managers serving DAF donors may be. No Echelon source addresses Regulation S-P.",
              "For covered-institution customers, Echelon contractually agrees to take appropriate measures to protect against unauthorized access to customer information and to notify the covered institution as soon as possible and no later than 72 hours after becoming aware of a breach resulting in unauthorized access to a customer information system Echelon maintains; provides structured facts on sensitive customer information affected so the customer can meet its 30-day individual notification deadline; and supports the customer's service provider due diligence and monitoring.",
              "Unknown; no evidence located.", "Determine customer types and adopt contract terms with counsel.", "Nothing.",
              "Echelon has not yet adopted Regulation S-P service provider terms; it intends to meet the 72-hour service provider notice expectation for covered-institution customers.",
              "planned", [k4], [e4, e5], mechanism="event-driven-automated", automation="partial", impl="low", rec="low",
              oq=["Will Unbound serve SEC-registered advisers or broker-dealers, or DAF sponsors affiliated with them?"])
    a7 = c.au(7, "Support for state breach laws and other regulatory notification obligations", "unknown",
              "No Echelon source maps breach notification obligations. Customer-held obligations (state breach laws, NYDFS 500.17, GDPR Article 33, Form 8-K Item 1.05, FTC Safeguards Rule notice) depend on customer type and data.",
              "An obligation matrix reviewed by counsel maps each customer type and jurisdiction to its deadlines; Echelon notifies data owners as state laws require of service providers, and provides structured incident data (affected individuals by state of residence, data elements, timeline, containment) quickly enough for customers to meet NYDFS 72-hour, GDPR 72-hour, FTC 30-day and SEC four-business-day materiality-based deadlines.",
              "Unknown; no evidence located.", "Build the matrix with counsel before production.", "Nothing.",
              "Echelon has not yet mapped regulatory notification obligations; this will be completed with counsel before production.", "not-available", [k4], [e4, e5],
              mechanism="periodic-manual", automation="partial", impl="medium", rec="low")
    a8 = c.au(8, "Forensics, evidence preservation and regulator cooperation", "proposed-target-state",
              "REQ-X-016 requires incident records to define earliest credible compromise, lookback and evidence provenance; SOC2-006 directs protected evidence storage and legal hold; no forensic capability exists.",
              "On declaration, logs, snapshots, images and agent ledgers in scope are preserved with hashes and chain of custody under legal hold for at least the longer of seven years or the applicable hold; customers' forensic firms may participate under coordination; Echelon cooperates with customers' regulators, auditors and law enforcement and provides records within agreed timeframes; forensic summaries are shared with affected customers.",
              "Not established.", "Define preservation procedures with the logging architecture.", "Nothing.",
              "Forensic preservation and regulator cooperation procedures are planned; not established.", "planned", [k5], [e6],
              requirements=["REQ-X-016", "SOC2-006"], mechanism="event-driven-automated", automation="partial", impl="low", rec="low",
              oq=["Is seven years appropriate for incident evidence, aligned with REQ-X-036, or should counsel set a different period?"])
    a9 = c.au(9, "Post-incident review and lessons learned", "proposed-target-state",
              "SOC2-026 requires lessons learned; Tutela requires incidents to feed threats, invariants and regression evidence (tutela@476dc682:requirements/TUTELA-REQUIREMENTS.md TUT-1303); the business plan describes incident learning as a draft governance position.",
              "Every significant incident yields a blameless root cause analysis within 10 business days, a customer-facing post-incident report within 15 business days, corrective actions tracked to verified completion, and updates to threat models, invariants, regression tests and detections.",
              "Not established.", "Apply Tutela incident ingestion once Unbound operates.", "Nothing.",
              "Post-incident review practices are planned; no incidents have been handled for a production Echelon service.", "planned", [k6], [e7],
              requirements=["SOC2-026"], mechanism="event-driven-automated", automation="partial", impl="low", rec="low")
    a10 = c.au(10, "Ransomware preparedness and ransom payment policy", "proposed-target-state",
               "UNB-GAP-034 calls for cyber incident response, immutable backup and restoration tests; no backup or ransom policy exists.",
               "Backups are immutable or logically isolated from production and administrative credentials and are restore-tested quarterly; the plan assumes no ransom payment, and any extortion decision requires counsel, insurer (if any) and sanctions screening against OFAC lists, with law enforcement engagement; customers are informed promptly of any data theft or extortion threat involving their data.",
               "Not established.", "Implement with backup architecture (see BKP).", "Nothing.",
               "Ransomware preparedness is planned; Unbound has no production data to protect yet.", "planned", [k7], [e8], requirements=["UNB-GAP-034"],
               mechanism="periodic-automated", automation="high", impl="medium", rec="low")
    a11 = c.au(11, "Containment: credential revocation, tenant isolation, platform holds and AI agent kill switch", "proposed-target-state",
               "CNV-PLT-007 defines sponsor-adopted, time-bounded platform holds that never move funds and notify the sponsor immediately; UNB-XIN-IAM-005 defines break-glass limits; SOC2-017 requires agents to be interruptible; none implemented.",
               "Pre-authorized containment actions execute within minutes: revoke workforce, service and agent credentials; isolate a tenant; place platform holds under the sponsor's adopted hold policy that never move, reverse or redirect funds and leave the sponsor able to pay through its own bank; stop all or specific AI agents and review every action they took in the affected window from the agent ledger.",
               "Not established.", "Implement with identity, hold policy and agent runtime.", "Nothing.",
               "Containment capabilities, including sponsor-policy holds and AI agent stop controls, are specified for Unbound; not implemented.", "planned", [k8], [e9],
               requirements=["CNV-PLT-007", "UNB-XIN-IAM-005", "SOC2-017"], mechanism="event-driven-automated", automation="high", impl="medium", rec="low")
    a12 = c.au(12, "Incident history disclosure", "unknown",
               "Echelon has no production service and no customers; the current-state brief prohibits claiming any incident history. No incident records were located, which is not proof that none occurred in corporate systems.",
               "Echelon discloses, under NDA, all security incidents in the last three years that required notification to customers or regulators, with summaries of root cause and corrective actions, and any related litigation or regulatory action.",
               "Unknown; no incident records located.", "Maintain an incident register from formation onward.", "Nothing.",
               "Echelon has no production service and therefore no service incident history to report; corporate incident records have not been formally maintained.",
               "not-available", [k6], [e7], disclosure="nda", impl="none", rec="none",
               oq=["Has Echelon Foundry experienced any security incident in corporate systems (email, source hosting, identity) since formation?"])

    I_FIN = ["financial-services", "banking", "wealth-management", "donor-advised-funds"]
    BANKREG = "OCC, FDIC, Federal Reserve"
    c.q(1, "plan", "Do you have a documented, approved incident response plan, reviewed at least annually, covering detection, triage, containment, eradication, recovery and post-incident review?",
        "Prepared, structured response.", "Chaotic response causing greater harm.",
        [R("SRC-NIST-SP800-61-R3"), R("SRC-NIST-SP800-53-R5", "IR-8"), R("SRC-CSA-CCM-V4", "SEF-03"), R("SRC-ISO-27002-2022", "5.24"), R("SRC-AICPA-TSC", "CC7.4"), D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-026"), R("SRC-SA-SIG")],
        "contractual-common", "critical", alts=["Provide a copy of your incident response plan.", "Is there a formal, tested incident management program?"])
    c.q(1, "severity", "How do you classify incident severity, and how does severity drive escalation and customer notification?",
        "Proportionate, consistent response.", "Under-escalation of serious incidents.", [R("SRC-ISO-27002-2022", "5.25"), R("SRC-CSA-CCM-V4", "SEF-06")], "industry-convention", "high")
    c.q(1, "definitions", "Does your plan distinguish security incidents, privacy breaches and operational outages, and address how one event can trigger several notification obligations?",
        "Complete handling of overlapping obligations.", "Missed legal obligations.", [R("SRC-NIST-SP800-61-R3"), R("SRC-STATE-BREACH-LAWS"), R("SRC-CIRN-RULE-2021")], "customer-preference", "medium", ind=I_FIN)
    c.q(1, "playbooks", "Does the plan include playbooks for service-specific scenarios such as an unauthorized grant or payment instruction, tenant data exposure, a compromised AI agent or a compromised build pipeline?",
        "Preparedness for the vendor's real risks.", "Generic plans failing in domain-specific incidents.", [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-026"), R("SRC-OWASP-AGENTIC-AI")], "customer-preference", "high", ind=["donor-advised-funds", "financial-services", "wealth-management"])
    c.q(1, "plan-sharing", "Will you share your incident response plan, or a summary of it, with us?",
        "Customer ability to align its own plan.", "Misaligned response between vendor and customer.", [R("SRC-INTERAGENCY-TPRM-2023")], "customer-preference", "medium", disc="nda")
    c.q(2, "roles", "Who is the designated incident lead, who backs them up, and how are they reached at any hour?",
        "Accountable leadership in an incident.", "Delayed response from unclear ownership.", [R("SRC-CSA-CCM-V4", "SEF-08"), R("SRC-NYDFS-PART-500", "500.16")], "contractual-common", "high")
    c.q(2, "external-support", "Which external parties are pre-arranged for incidents, such as outside counsel, a forensic firm, an insurer's breach panel or crisis communications?",
        "Surge capacity and expertise.", "Delays while engaging help mid-incident.", [R("SRC-NIST-SP800-61-R3")], "customer-preference", "medium")
    c.q(2, "key-person", "How does a small organization avoid dependence on one person for incident response?",
        "Resilience of the response capability.", "Response stalls when one person is unavailable.", [R("SRC-FFIEC-BCM-BOOKLET"), R("SRC-INTERAGENCY-TPRM-2023")], "customer-preference", "high", ind=I_FIN)
    c.q(2, "ai-agents", "What is the role of AI agents in incident response, and which actions may they take without human approval?",
        "Controlled use of automation in a crisis.", "Agents destroying evidence or sending erroneous notices.", [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-017"), R("SRC-NIST-AI-RMF-1.0")], "customer-preference", "medium", jur=["global"])
    c.q(2, "contacts", "Do you maintain and verify a list of each customer's designated security and compliance contacts, and how do we update ours?",
        "Notices reach the right people.", "Notices sent to departed staff.", [D("SRC-CSA-CCM-V4", "SEF-08")], "industry-convention", "medium")
    c.q(3, "testing", "How often do you test the incident response plan through tabletop exercises or simulations, and when was the last one held?",
        "Proven readiness.", "Untested plans failing in practice.", [R("SRC-NIST-SP800-53-R5", "IR-3"), R("SRC-CSA-CCM-V4", "SEF-04"), D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-015"), R("SRC-PCI-DSS-4.0.1", "Req 12.10.2", rel="informed-by")],
        "contractual-common", "high", alts=["Do you conduct annual incident response tabletop exercises?"])
    c.q(3, "scenarios", "Do exercises include realistic scenarios such as ransomware, insider misuse, a compromised AI agent, or an incident during year-end giving peaks?",
        "Relevance of testing.", "Exercises that miss likely failure modes.", [R("SRC-NIST-SP800-61-R3")], "customer-preference", "medium", ind=["donor-advised-funds", "nonprofit"])
    c.q(3, "joint-exercises", "Will you invite customers to joint exercises or share exercise results and improvement actions?",
        "Coordinated response readiness.", "Untested vendor-customer handoffs.", [R("SRC-FFIEC-BCM-BOOKLET")], "customer-preference", "low", ind=["banking", "financial-services"])
    c.q(3, "technical-drills", "Do you test technical response capabilities, such as log retrieval, account disablement, payment holds and key rotation, and measure how long each takes?",
        "Measured technical readiness.", "Slow containment.", [D("SRC-ECH-UNB-BASELINE", "CNV-PLT-007", "informed-by")], "customer-preference", "medium")
    c.q(4, "notification-timing", "Within what time will you notify us after discovering or reasonably suspecting a security incident affecting our data or the service?",
        "Timely awareness to meet the customer's own obligations.", "Missed customer deadlines and unmitigated harm.",
        [R("SRC-CSA-CCM-V4", "SEF-07"), R("SRC-INTERAGENCY-TPRM-2023"), R("SRC-SA-SIG"), R("SRC-EDUCAUSE-HECVAT")], "contractual-common", "critical",
        alts=["What is your breach notification SLA?", "How quickly will you inform us of a security breach involving our data?"])
    c.q(4, "notification-trigger", "What starts the notification clock: discovery, reasonable suspicion, confirmation or determination of impact?",
        "Unambiguous commitments.", "Delays through narrow trigger definitions.", [R("SRC-STATE-BREACH-LAWS"), R("SRC-CIRN-RULE-2021")], "contractual-common", "high")
    c.q(4, "notification-content", "What will the initial notice and later updates contain, and how often will you update us?",
        "Actionable information.", "Notices too vague to act on.", [R("SRC-NIST-CSF-2.0", "RS.CO-02"), R("SRC-NIST-CSF-2.0", "RS.CO-03")], "contractual-common", "high")
    c.q(4, "notification-channel", "Through which channel will you notify us, and how can we verify that a notice really came from you and not an attacker?",
        "Authentic communication during incidents.", "Spoofed notices used for fraud.", [D("SRC-ECH-UNB-BASELINE", "REQ-X-016", "derived-from")], "customer-preference", "medium")
    c.q(4, "subprocessor-incidents", "Will you notify us of incidents at your subprocessors that affect our data, and within what time?",
        "Fourth-party incident visibility.", "Hidden subprocessor breaches.", [R("SRC-ISO-27036"), R("SRC-INTERAGENCY-TPRM-2023"), R("SRC-GDPR", "Art. 28")], "contractual-common", "high")
    c.q(4, "indirect-incidents", "Will you notify us of a security incident that did not involve our data but affected shared infrastructure or the software release we use?",
        "Awareness of related risk.", "Customer unaware of shared exposure.", [R("SRC-ISO-27017")], "customer-preference", "medium")
    c.q(5, "cirn-bank-service-provider", "As a bank service provider, will you notify our designated contacts as soon as possible when an incident has materially disrupted or degraded, or is reasonably likely to materially disrupt or degrade, the services you provide us for four or more hours?",
        "Bank's ability to meet its 36-hour regulator notice.", "Bank misses its regulatory notification.", [D("SRC-CIRN-RULE-2021", "12 CFR 53.4"), R("SRC-BSCA")], "legal-regulatory", "critical",
        ind=["banking"], jur=["US-federal"], reg=BANKREG,
        note="Applies where the vendor is a bank service provider performing covered services subject to the Bank Service Company Act; OCC, Federal Reserve and FDIC adopted parallel provisions.")
    c.q(5, "cirn-contacts", "Who at your organization sends bank service provider incident notices, and to which designated contacts at our bank will they go?",
        "Notice reaches bank-designated contacts.", "Notice misrouted.", [D("SRC-CIRN-RULE-2021")], "legal-regulatory", "high", ind=["banking"], jur=["US-federal"], reg=BANKREG)
    c.q(5, "cirn-determination-support", "Can you give us facts quickly enough for us to decide whether your incident is a notification incident we must report to our primary federal regulator within 36 hours?",
        "Bank's own compliance.", "Late or inaccurate regulator notice.", [R("SRC-CIRN-RULE-2021", "12 CFR 53.3")], "legal-regulatory", "high", ind=["banking"], jur=["US-federal"], reg=BANKREG,
        note="The 36-hour obligation is the bank's; vendor support is contractual but directly enables it.")
    c.q(5, "bsca", "Is your service subject to the Bank Service Company Act such that our regulators may examine you, and will you cooperate with such an examination?",
        "Regulatory examination of the vendor.", "Customer unable to satisfy examiner access.", [D("SRC-BSCA"), R("SRC-FFIEC-OUTSOURCING-BOOKLET")], "legal-regulatory", "medium", ind=["banking"], jur=["US-federal"], reg=BANKREG)
    c.q(6, "reg-sp-72-hour", "If we are a covered institution under Regulation S-P, will you notify us as soon as possible and no later than 72 hours after becoming aware of a breach resulting in unauthorized access to a customer information system you maintain?",
        "Covered institution meets amended Regulation S-P service provider oversight.", "Customer cannot meet its 30-day notice obligation or oversight requirement.",
        [D("SRC-SEC-REG-SP-2024", "17 CFR 248.30")], "legal-regulatory", "critical", ind=["financial-services", "wealth-management"], jur=["US-federal"], reg="SEC",
        note="The rule binds the covered institution, which must require this of its service providers through policies and procedures; it flows to the vendor via contract.")
    c.q(6, "reg-sp-individual-notice", "Will you provide the facts we need to determine which individuals' sensitive customer information was affected, so we can meet our 30-day individual notification deadline?",
        "Timely individual notice.", "Regulatory violation and harm to individuals.", [D("SRC-SEC-REG-SP-2024")], "legal-regulatory", "high", ind=["financial-services", "wealth-management"], jur=["US-federal"], reg="SEC")
    c.q(6, "reg-sp-oversight", "Will you agree to the service provider terms and support the due diligence and monitoring we must perform under amended Regulation S-P?",
        "Customer oversight program.", "Customer deficiency in service provider oversight.", [D("SRC-SEC-REG-SP-2024"), R("SRC-SEC-ADVISER-OUTSOURCING-PROPOSAL", rel="informed-by")], "legal-regulatory", "high", ind=["financial-services", "wealth-management"], jur=["US-federal"], reg="SEC")
    c.q(6, "daf-affiliated", "For DAF sponsors affiliated with a broker-dealer or investment adviser, which of your incident obligations arise from the affiliate's regulation rather than the sponsor's?",
        "Clarity of obligations in affiliated sponsor structures.", "Gaps from misunderstood regulatory reach.", [R("SRC-SEC-REG-SP-2024"), R("SRC-ECH-DAF-LANDSCAPE", rel="informed-by")], "unknown", "medium",
        ind=["donor-advised-funds", "wealth-management"], jur=["US-federal"], reg="unknown",
        oq=["Under what conditions does a commercial DAF sponsor's data fall within an affiliated covered institution's customer information?"])
    c.q(7, "state-breach-laws", "How will you support our obligations under state data breach laws, including identifying affected individuals by state of residence and the data elements involved?",
        "Multi-state breach compliance.", "Missed or inaccurate notices.", [R("SRC-STATE-BREACH-LAWS")], "legal-regulatory", "high", jur=["US-states"], reg="State attorneys general",
        note="Most state laws require a service provider that maintains data for an owner to notify the owner; the owner notifies individuals and regulators.")
    c.q(7, "nydfs", "If we are regulated by NYDFS, can you support our 72-hour notice to the superintendent and provide the information we need for it?",
        "NYDFS compliance.", "Late notice to NYDFS.", [D("SRC-NYDFS-PART-500", "500.17"), R("SRC-NYDFS-PART-500", "500.11")], "legal-regulatory", "high",
        ind=["financial-services", "banking", "insurance"], jur=["US-state:NY"], reg="NYDFS",
        note="500.11 requires covered entities' third-party policies to address notice from service providers.")
    c.q(7, "gdpr", "If we process EU or UK personal data through your service, will you notify us without undue delay as our processor so we can meet the 72-hour supervisory authority deadline?",
        "GDPR breach compliance.", "Late notification to authorities.", [D("SRC-GDPR", "Art. 33"), R("SRC-GDPR", "Art. 28"), R("SRC-UK-GDPR")], "legal-regulatory", "medium", jur=["EU", "UK"], reg="EU and UK data protection authorities")
    c.q(7, "sec-8k", "If we are a public company, will you provide timely facts so we can assess materiality for a Form 8-K Item 1.05 disclosure?",
        "Public company disclosure compliance.", "Late or inaccurate securities disclosure.", [D("SRC-SEC-CYBER-DISCLOSURE-2023", "Item 1.05")], "legal-regulatory", "medium", ind=["enterprise-software", "financial-services"], jur=["US-federal"], reg="SEC",
        note="Obligation is the registrant's; third-party incidents are within scope of its assessment.")
    c.q(7, "ftc-safeguards", "If we are subject to the FTC Safeguards Rule, will you provide what we need to notify the FTC of an event involving information of 500 or more consumers?",
        "FTC compliance.", "Missed FTC notice.", [R("SRC-FTC-SAFEGUARDS-RULE", "314.4(j)")], "legal-regulatory", "medium", ind=["financial-services"], jur=["US-federal"], reg="FTC")
    c.q(8, "forensics", "How do you preserve forensic evidence, such as logs, snapshots, images and memory, during an incident, and how long is it retained?",
        "Investigability.", "Lost evidence preventing root cause and scope determination.", [R("SRC-ISO-27002-2022", "5.28"), R("SRC-NIST-CSF-2.0", "RS.AN-07"), D("SRC-ECH-UNB-BASELINE", "REQ-X-016")], "industry-convention", "high")
    c.q(8, "chain-of-custody", "Do you maintain chain of custody for incident evidence so it can be used in litigation, insurance claims or regulatory proceedings?",
        "Evidence admissibility.", "Inadmissible or disputed evidence.", [R("SRC-ISO-27002-2022", "5.28")], "customer-preference", "medium")
    c.q(8, "regulator-cooperation", "Will you cooperate with our regulators, auditors and law enforcement during an investigation, including providing access to relevant records?",
        "Customer regulatory obligations.", "Obstruction of examination or investigation.", [R("SRC-INTERAGENCY-TPRM-2023"), R("SRC-BSCA"), R("SRC-EU-DORA", "Article 30")], "supervisory-guidance", "high", ind=I_FIN, reg="Customer's regulators")
    c.q(8, "forensic-sharing", "Will you share the forensic report or a summary with us, and may our own forensic firm participate?",
        "Customer's independent understanding.", "Reliance on vendor narrative.", [R("SRC-INTERAGENCY-TPRM-2023")], "contractual-common", "medium", disc="nda")
    c.q(9, "root-cause", "After an incident, do you perform a documented root cause analysis and track corrective actions to verified completion?",
        "Learning and recurrence prevention.", "Repeat incidents.", [R("SRC-ISO-27002-2022", "5.27"), R("SRC-NIST-CSF-2.0", "RS.AN-03"), D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-026")], "industry-convention", "high")
    c.q(9, "post-incident-report", "Will you provide affected customers with a written post-incident report, and within what time?",
        "Customer closure and own reporting.", "Customer unable to report to its board or regulator.", [R("SRC-CSA-CCM-V4", "SEF-07")], "contractual-common", "high", disc="nda")
    c.q(9, "feedback", "How do incident findings change your threat models, controls, tests and detections so the same failure cannot recur silently?",
        "Systemic improvement.", "Recurrence through unchanged controls.", [R("SRC-NIST-CSF-2.0", "ID.IM-03"), D("SRC-ECH-SCS-0.1", "Enforcement model", "informed-by")], "customer-preference", "medium")
    c.q(10, "ransomware", "What specifically prepares you to recover from ransomware without paying, including immutable backups and tested restoration?",
        "Recovery without extortion.", "Prolonged outage or data loss.", [D("SRC-ECH-UNB-BASELINE", "UNB-GAP-034"), R("SRC-FFIEC-BCM-BOOKLET"), R("SRC-NIST-CSF-2.0", "RC.RP-03")], "industry-convention", "high")
    c.q(10, "ransom-policy", "What is your policy on paying a ransom or extortion demand, and how do you address OFAC sanctions risk in that decision?",
        "Legal and ethical handling of extortion.", "Sanctions violations or funding criminals.", [R("SRC-OFAC-REGS"), R("SRC-OFAC-COMPLIANCE-FRAMEWORK")], "legal-regulatory", "medium", jur=["US-federal"], reg="OFAC",
        note="OFAC prohibitions apply to US persons making payments to sanctioned persons, including ransom payments.")
    c.q(10, "extortion", "If our data is stolen and an attacker threatens to publish it, how and when will we be informed?",
        "Awareness of data theft and extortion.", "Customer surprised by publication.", [R("SRC-STATE-BREACH-LAWS")], "customer-preference", "high")
    c.q(11, "containment", "What containment actions can you take quickly, such as revoking credentials, isolating a tenant, holding outbound payment instructions or stopping AI agents, and who authorizes them?",
        "Speed of damage limitation.", "Ongoing loss during deliberation.", [R("SRC-NIST-SP800-53-R5", "IR-4"), D("SRC-ECH-UNB-BASELINE", "CNV-PLT-007")], "customer-preference", "high")
    c.q(11, "holds", "If an incident requires holding grants or payments, how will you notify us and keep our ability to pay through our own bank channel?",
        "Sponsor control of funds during incidents.", "Vendor action blocking legitimate sponsor payments.", [D("SRC-ECH-UNB-BASELINE", "CNV-PLT-007", "derived-from")], "customer-preference", "high", ind=["donor-advised-funds", "nonprofit"])
    c.q(11, "ai-agent-containment", "How do you contain an incident involving a compromised or misbehaving AI agent, including revoking its credentials and reviewing everything it did?",
        "Containment of agent-driven incidents.", "Persistent damage from an agent acting with valid credentials.", [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-017"), R("SRC-OWASP-AGENTIC-AI")], "customer-preference", "high", jur=["global"])
    c.q(12, "history", "How many security incidents have you had in the last three years, and did any require notification to customers or regulators?",
        "Track record.", "Undisclosed history of breaches.", [R("SRC-SA-SIG"), R("SRC-VSA-FULL")], "customer-preference", "high", disc="nda",
        alts=["Have you experienced a data breach in the past 36 months?"])
    c.q(12, "history", "Has any security incident resulted in litigation, regulatory action or contractual claims against you?",
        "Legal exposure and maturity.", "Inherited legal risk.", [R("SRC-SA-SIG")], "customer-preference", "medium", disc="nda")
    return c
