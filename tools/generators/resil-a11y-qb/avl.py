from rqb_common import *
c = Cat("AVL", {"industries": ["all"], "jurisdictions": ["US-federal"], "products": ["unbound"]})
OWN = "Proposed: SRE Lead (role not yet staffed)"
RAT = "No production service, uptime history, SLA, status page or service-credit terms exist as of 2026-11-25."
FIN = ["banking", "financial-services", "wealth-management", "donor-advised-funds"]

e1 = c.E(1, "Published service level definition", "Versioned SLA and SLO document defining availability per capability (read access, submission, approval, payment dispatch), measurement window, exclusions, and how fail-closed refusals are counted.",
         mechanism="periodic-manual", freshness="P1Y", disc="public")
e2 = c.E(2, "Availability measurement stream", "Synthetic probes from at least two external vantage points per capability and server-side success ratios per tenant, retained raw so customers can recompute reported figures.",
         mechanism="continuous-automated", freshness="P1D", disc="customer-only", prov=["probe_id", "vantage", "capability", "tenant_scope", "timestamp", "result"],
         notes="CNV-EXP-001 requires published service levels to be measured with a stated methodology before publication.")
e3 = c.E(3, "Monthly availability report per tenant", "Computed availability per capability and tenant against SLO, with incident references, exclusions applied and credits owed.",
         mechanism="periodic-automated", freshness="P30D", disc="customer-only")
e4 = c.E(4, "Status page and notification log", "Component-level status history hosted independently of production, with time of first customer notice per incident and subscriber delivery records.",
         mechanism="event-driven-automated", freshness="per-event", disc="public")
e5 = c.E(5, "Incident post-mortem reports", "Customer-facing root-cause report per qualifying incident with timeline, impact by tenant and capability, and corrective actions.",
         mechanism="event-driven-automated", freshness="per-event", disc="customer-only")
e6 = c.E(6, "Change calendar and maintenance notices", "Record of scheduled maintenance notices, actual downtime per change, and change-freeze periods, linked to Praxis change provenance.",
         producer="Praxis (change provenance) plus not yet assigned notice system", mechanism="event-driven-automated", freshness="per-event", disc="customer-only")
e7 = c.E(7, "Service credit ledger", "Per-tenant record of SLA misses, credits calculated, claims and payments.", mechanism="periodic-automated", freshness="P30D", disc="customer-only")
e8 = c.E(8, "Subprocessor dependency and status register", "Mapping of each capability to the subprocessors it depends on, their published SLAs, live status feed and historical incidents affecting the service.",
         mechanism="continuous-automated", freshness="P1D", disc="customer-only")
e9 = c.E(9, "Degraded-mode behavior test results", "Automated tests showing, for each dependency failure, which functions continue, which fail closed, and what the user interface displays, including payment status Unknown.",
         mechanism="periodic-automated", freshness="P30D", disc="nda", prov=["scenario", "dependency", "functions_continued", "functions_refused", "ui_state"])

k1 = c.C(1, "Capability-level SLO definition", "Define availability separately for read access, submission, approval and payment dispatch so a headline figure cannot mask a money-movement outage.",
         "administrative", "L10-external-or-manual", ["not yet assigned"], [e1], "Proposed: Unbound product owner", related=["CNV-EXP-001"],
         fw=[R("SRC-AICPA-TSC", "A1.1"), R("SRC-ISO-20000-1")])
k2 = c.C(2, "Independent multi-vantage availability measurement", "Measure availability from outside the production environment and per tenant, and retain raw results for customer verification.",
         "detective-automated", "L9-runtime-monitored", ["not yet assigned"], [e2, e3], OWN, related=["MON-018"])
k3 = c.C(3, "Independent status page with timed notification", "Publish component status from infrastructure separate from production and notify subscribers within a defined time of detection.",
         "detective-automated", "L9-runtime-monitored", ["not yet assigned"], [e4, e5], OWN, fw=[R("SRC-CIRN-RULE-2021", "12 CFR 53.4")])
k4 = c.C(4, "Zero-downtime deployment and change freeze", "Deploy without planned downtime by default, run schema changes online, and freeze non-emergency changes during declared customer peak periods.",
         "preventive-gate", "L5-build-release-gate", ["Praxis (change provenance)", "Strata (schema diff)", "Unbound release pipeline (not built)"], [e6], OWN,
         related=["SOC2-011", "CNV-PLT-010"])
k5 = c.C(5, "Automated service credit calculation", "Compute credits from the measurement stream without requiring the customer to claim and prove the outage.",
         "corrective", "L9-runtime-monitored", ["not yet assigned"], [e7], "Proposed: Finance Lead (role not yet staffed)")
k6 = c.C(6, "Subprocessor dependency register with live status", "Map capabilities to subprocessors, flow down availability expectations, and surface provider status to customers.",
         "detective-automated", "L9-runtime-monitored", ["not yet assigned"], [e8], "Proposed: Vendor Risk Lead (role not yet staffed)",
         related=["RR-REQ-X-073-r2", "UNB-API-STD-005"], fw=[R("SRC-AICPA-TSC", "CC9.2")])
k7 = c.C(7, "Typed degraded modes with fail-closed money movement", "Represent each dependency outage as an explicit degraded state in which non-financial functions continue, money movement and authority changes fail closed, and the UI shows uncertain states distinctly.",
         "preventive-structural", "L2-type-system", ["Unbound (not built)", "Forma (state presentation components)"], [e9], "Proposed: Unbound architecture owner",
         related=["CNV-PLT-007", "UNB-CUST-022", "UNB-INV-037", "UNB-EXT-036", "UNB-UX-003"],
         notes="Forma components exist; the Unbound state machine that drives them does not.")

a1 = c.A(1, "Availability commitment and definition", "proposed-target-state", RAT,
    "Echelon publishes capability-level service levels rather than a single uptime figure: separate monthly targets for read access to records and statements, for submission of requests, and for approval and payment dispatch, measured with a stated methodology. A deliberate fail-closed refusal of a financial action because safety cannot be confirmed is reported transparently as unavailability of that capability, not excluded. Exclusions are limited and enumerated; scheduled maintenance counts against the target unless within a pre-announced window under a defined monthly cap.",
    "Not established. CNV-EXP-001 requires service levels to be measured with a stated methodology before publication.",
    "Publish SLOs only after measurement exists in a production-like environment.",
    "Nothing.",
    "Echelon does not currently offer an availability SLA because no production service exists. We intend to publish capability-level service levels once we can measure them.",
    "not-available", [k1], [e1], "Proposed: Unbound product owner", mechanism="periodic-manual", automation="partial", impl="low", rec="low", disc="public",
    requirements=["CNV-EXP-001", "UNB-GAP-028"],
    challenge={
        "customer_intent": "Know how reliably the service will be there when needed.",
        "adverse_outcome": "Service unavailable at critical moments without recourse.",
        "conventional_control_effectiveness": "A single 99.9 percent uptime number, usually measured by the vendor with broad exclusions, says little about whether money movement worked and can hide partial outages.",
        "legally_required": "No.",
        "contractually_required": "Yes, almost universally expected in enterprise SaaS contracts.",
        "historical_convention": "Hosting-era uptime SLAs measured at the network edge.",
        "architectural_elimination": "Not applicable; availability is a measured outcome.",
        "automatic_enforcement": "Measurement and credit calculation can be automated.",
        "continuous_evidence": "Raw probe data per capability and tenant.",
        "stronger_alternative": "Capability-level SLOs with customer-recomputable raw data, counting fail-closed refusals honestly.",
        "alternative_verifiable": "Yes, if raw data is shared.",
        "customer_acceptance_likelihood": "Uncertain: procurement templates expect one percentage; a lower figure for payment dispatch may look worse than competitors.",
        "invalidating_conditions": "If capability-level SLOs are too complex for customers to use in their own risk assessments.",
        "conventional_cost": "low", "alternative_cost": "medium",
        "alternative_risks": "Honest fail-closed accounting lowers reported availability relative to competitors who exclude it.",
        "supporting_arguments": ["Aligns the metric with the customer's real concern.", "Removes incentive to fail open to protect an uptime number."],
        "opposing_arguments": ["Harder to compare across vendors.", "Customers may still require a single headline figure."],
        "technical_effectiveness": "stronger", "institutional_acceptance": "uncertain"})
a2 = c.A(2, "Availability measurement and reporting", "proposed-target-state", RAT,
    "Availability is measured by synthetic probes from at least two external vantage points per capability and by server-side success ratios per tenant, so partial outages affecting some tenants or features are counted. Monthly per-tenant reports are generated automatically, and customers can obtain the raw measurement data to recompute them or compare with their own monitoring. Historical availability is published once a production record exists.",
    "Not established. MON-018 specifies monitoring of operational resilience signals.",
    "Implement measurement before any SLA is offered.",
    "Nothing. There is no uptime history because there is no production service.",
    "We have no uptime history because no production service exists. We plan per-tenant, externally measured availability reporting with raw data available to customers.",
    "not-available", [k2], [e2, e3], OWN, freshness="P30D", mechanism="continuous-automated", automation="full", impl="low", rec="low", requirements=["MON-018", "CNV-EXP-001"])
a3 = c.A(3, "Status page, outage notification and post-incident reports", "proposed-target-state", RAT,
    "A component-level status page hosted independently of production shows current status and history; customers can subscribe by email and webhook. Customers are notified of a material outage within 30 minutes of detection, which is designed to satisfy the bank service provider obligation to notify affected banking organizations as soon as possible when covered services are materially disrupted for four or more hours. A root-cause report follows within ten business days of a qualifying incident.",
    "Not established.",
    "Stand up an independent status page before the first customer.",
    "Nothing.",
    "No status page exists yet. We plan an independently hosted status page and defined notification times before production.",
    "planned", [k3], [e4, e5], OWN, freshness="per-event", mechanism="event-driven-automated", automation="high", impl="low", rec="low", disc="public",
    requirements=["SOC2-026"])
a4 = c.A(4, "Maintenance windows and change-related downtime", "proposed-target-state", RAT,
    "Deployments are zero-downtime by default and schema changes are applied online through Strata-managed migrations with expand-and-contract patterns. Any planned downtime is announced at least five business days ahead, scheduled outside customer business hours, capped monthly, and prohibited during declared freeze periods such as the last two weeks of December. Emergency maintenance is announced as soon as it is decided, with reason.",
    "Not established. Strata can compute schema diffs in pilot status; no deployment pipeline for Unbound exists.",
    "Design the release pipeline for zero downtime from the start.",
    "Nothing.",
    "We have not set maintenance windows because no production service exists. We intend zero-downtime deployments and change freezes at year-end.",
    "planned", [k4], [e6], OWN, freshness="per-event", mechanism="event-driven-automated", automation="high", impl="medium", rec="low",
    requirements=["SOC2-011", "CNV-PLT-010"])
a5 = c.A(5, "Service credits and remedies", "proposed-target-state", RAT,
    "Service credits are calculated automatically from the measurement stream and applied without a claim process; repeated misses (for example three months in any six) give the customer a termination right without penalty and transition assistance. Credits are not the exclusive remedy for failures caused by breach of security or data-integrity obligations.",
    "Not established; no contract templates located.",
    "Draft SLA schedule with counsel when SLOs are measurable.",
    "Nothing.",
    "We do not currently offer service credits. Remedies will be defined when a service level agreement is offered.",
    "not-available", [k5], [e7], "Proposed: Finance Lead (role not yet staffed)", mechanism="periodic-automated", automation="full", impl="low", rec="low",
    oq=["Will Echelon's commercial counsel accept credits that are not the exclusive remedy?"])
a6 = c.A(6, "Subprocessor dependency and its effect on availability", "proposed-target-state", RAT,
    "Each capability is mapped to the subprocessors it depends on (cloud hosting, managed PostgreSQL, identity, email delivery, payment connectivity, custodian feeds, charity registries, AI providers). Echelon's SLA does not exclude outages of its own chosen subprocessors; it does distinguish outages of parties the customer chose, such as the sponsor's bank or custodian. Provider status is shown on the status page and in the product.",
    "Not established. RR-REQ-X-073-r2 specifies a critical-vendor register; UNB-API-STD-005 requires documented provider outage behavior per integration.",
    "Build the register at provider selection.",
    "Nothing.",
    "No production subprocessors have been selected. We plan to publish which providers each function depends on.",
    "planned", [k6], [e8], "Proposed: Vendor Risk Lead (role not yet staffed)", freshness="P1D", mechanism="continuous-automated", automation="high", impl="low", rec="low",
    requirements=["RR-REQ-X-073-r2", "UNB-API-STD-005", "SOC2-013"])
a7 = c.A(7, "Degraded modes and fail-closed financial actions", "proposed-target-state", RAT,
    "Every dependency outage maps to an explicit degraded state. Read access, drafting and non-financial work continue; money movement, payee changes and authority changes fail closed when the system cannot confirm safety (for example the hold registry is stale beyond its freshness bound or database quorum is lost), and the user sees a distinct, honest status such as 'Outcome being confirmed' rather than a false success or a generic error. Platform-originated holds are time-bounded, notify the sponsor's designated officer, never move funds, and leave the sponsor able to pay through its own bank.",
    "Not established. CNV-PLT-007, UNB-CUST-022, UNB-INV-037, UNB-EXT-036 and UNB-UX-003 specify the behavior.",
    "Implement degraded states as typed domain states with automated tests per dependency.",
    "Nothing beyond requirement text and Forma presentation components, which exist in a separate design-system repository.",
    "Our design stops money movement when safety cannot be confirmed while keeping other functions available, and tells users plainly what state a payment is in. This has not been built or tested.",
    "planned", [k7], [e9], "Proposed: Unbound architecture owner", freshness="P30D", mechanism="periodic-automated", automation="full", impl="medium", rec="low",
    requirements=["CNV-PLT-007", "UNB-CUST-022", "UNB-INV-037", "UNB-EXT-036", "UNB-UX-003", "TVR-UX-002"],
    challenge={
        "customer_intent": "Keep working during partial outages without risking incorrect payments.",
        "adverse_outcome": "Either total outage from a minor dependency failure, or unsafe payments made on stale data.",
        "conventional_control_effectiveness": "Conventional availability engineering treats any refusal as failure, which pressures systems to fail open; questionnaires rarely ask what the system does when it cannot confirm safety.",
        "legally_required": "No. Sanctions and payment rules make the originator (the sponsor) liable for unsafe payments, which is why fail-closed protects the customer.",
        "contractually_required": "Not commonly specified.",
        "historical_convention": "Batch systems queued everything and reconciled later.",
        "architectural_elimination": "Unsafe dispatch on stale hold data is eliminated in scope by an atomic fencing check at dispatch.",
        "automatic_enforcement": "Typed degraded states; dispatch requires a fresh safety proof.",
        "continuous_evidence": "Monthly automated degraded-mode test results.",
        "stronger_alternative": "Fail closed for money, fail open for reading, and report both honestly.",
        "alternative_verifiable": "Yes, by test results and by status history.",
        "customer_acceptance_likelihood": "Likely among compliance officers; uncertain among users who want payments to go out.",
        "invalidating_conditions": "If fail-closed periods are long and frequent enough that sponsors route around the platform.",
        "conventional_cost": "low", "alternative_cost": "medium",
        "alternative_risks": "Over-conservative freshness bounds could block payments unnecessarily at peak.",
        "supporting_arguments": ["Protects the sponsor from liability for unsafe payments.", "Users are never told a payment succeeded when it did not."],
        "opposing_arguments": ["Lower apparent availability.", "Users may perceive the system as unreliable."],
        "technical_effectiveness": "stronger", "institutional_acceptance": "likely"})

c.Q(1, "Uptime commitment", "What availability do you commit to contractually, and over what measurement period?",
    ["What is your uptime SLA?", "Do you guarantee 99.9 percent availability?"],
    "Customer needs a reliability commitment it can rely on and enforce.", "Unreliable service with no recourse.",
    [R("SRC-AICPA-TSC", "A1.1", rel="informed-by"), R("SRC-ISO-20000-1"), R("SRC-SA-SIG"), R("SRC-EDUCAUSE-HECVAT"), R("SRC-EU-DORA", "Article 30")],
    "contractual-common", "critical", juris=["US-federal", "EU"])
c.Q(1, "Definition of available", "What counts as available: being able to log in, view records, submit a grant recommendation, approve it, or dispatch a payment, and is each measured separately?",
    ["How do you define downtime?"],
    "A headline figure can hide outages in the functions that matter most.", "Payment dispatch down while the vendor reports full availability.",
    [R("SRC-ISO-20000-1"), UNB], "customer-preference", "high", industries=FIN)
c.Q(1, "SLA exclusions", "What is excluded from the availability calculation, for example scheduled maintenance, third-party outages, or force majeure?",
    ["List all SLA exclusions."],
    "Broad exclusions make an SLA meaningless.", "Most real outages fall under exclusions.",
    [R("SRC-INTERAGENCY-TPRM-2023")], "contractual-common", "high")
c.Q(1, "SLA by tier", "Does the availability commitment differ by service tier or by isolation option, such as a dedicated database?",
    ["Are higher SLAs available for premium tiers?"],
    "Customers with stricter needs may need a stronger commitment.", "Customer pays for isolation without matching availability.",
    [UNB], "customer-preference", "low")
c.Q(2, "Measurement method", "How is availability measured: from where, by whom, using synthetic checks or server-side metrics, and is the method documented?",
    ["Is availability measured by an independent third party?"],
    "Vendor-controlled measurement can be self-serving.", "Reported availability overstates real experience.",
    [R("SRC-AICPA-TSC", "A1.1", rel="informed-by"), UNB], "customer-preference", "high")
c.Q(2, "Historical availability", "What was your actual availability for each of the last twelve months, and how many incidents caused customer-visible outages?",
    ["Provide uptime history for the past year."],
    "Past performance is the best evidence of reliability.", "Customer selects a vendor with a poor reliability record.",
    [R("SRC-SA-SIG"), R("SRC-VSA-FULL")], "customer-preference", "high", note="No production history exists; answer is not available.")
c.Q(2, "Partial outages", "Are outages that affect only some customers, regions or features counted in reported availability, and how?",
    ["Does your uptime figure include partial degradations?"],
    "Aggregate metrics dilute tenant-specific outages.", "Customer suffers outages that do not appear in reports.",
    [R("SRC-ISO-27017", rel="informed-by"), UNB], "customer-preference", "medium")
c.Q(2, "Customer verification", "Can we obtain the raw availability measurements for our tenant so that we can verify reported figures and service credits?",
    ["Will you share monitoring data with us?"],
    "Independent verification prevents disputes.", "Disputed credits with no shared evidence.",
    [R("SRC-INTERAGENCY-TPRM-2023")], "customer-preference", "medium", industries=FIN)
c.Q(3, "Status page", "Do you publish a status page with component-level status and incident history, and can we subscribe to updates?",
    ["Provide your status page URL."],
    "Customers need timely, self-service outage information.", "Customer learns of outages from its own users.",
    [R("SRC-AICPA-TSC", "CC2.3"), R("SRC-NIST-CSF-2.0", "RC.CO-03")], "industry-convention", "medium")
c.Q(3, "Outage notification timing", "How quickly will you notify us of an outage or significant degradation, and does your process meet the notification duty for bank service providers when covered services are disrupted for four hours or more?",
    ["Within what time will you notify us of service disruptions?"],
    "Banking organizations must learn promptly of service provider disruptions.", "Bank customer misses its own notification obligations.",
    [D("SRC-CIRN-RULE-2021", "12 CFR 53.4"), R("SRC-BSCA", rel="informed-by"), R("SRC-NYDFS-PART-500", "500.17", rel="informed-by")], "legal-regulatory", "high",
    industries=["banking", "financial-services"], authority="OCC, FDIC, Federal Reserve",
    note="The 2021 rule binds bank service providers that provide covered services to banking organizations. Whether Echelon qualifies depends on its customers; for non-bank sponsors this is a contractual expectation.")
c.Q(3, "Post-incident reports", "Will you provide a written root-cause analysis after significant incidents, and within what time?",
    ["Do you share RCAs with customers?"],
    "Root-cause reports show whether problems are being fixed.", "Recurring incidents with no visible correction.",
    [R("SRC-ISO-20000-1"), R("SRC-NIST-SP800-61-R3")], "contractual-common", "medium")
c.Q(3, "Status page independence", "Is your status page hosted on infrastructure independent of your production environment, so it remains available during a full outage?",
    ["Where is your status page hosted?"],
    "A status page on the failed infrastructure fails with it.", "No information available during the worst outages.",
    [R("SRC-NIST-SP800-53-R5", "CP-8", rel="informed-by")], "customer-preference", "low")
c.Q(4, "Maintenance windows", "When are scheduled maintenance windows, how much notice do you give, how long do they last, and in which time zone?",
    ["Describe your planned maintenance policy."],
    "Maintenance during business hours disrupts operations.", "Unexpected downtime during critical work.",
    [R("SRC-ISO-20000-1"), R("SRC-EDUCAUSE-HECVAT")], "contractual-common", "medium")
c.Q(4, "Zero-downtime changes", "Do routine releases and database schema changes require downtime, or are they deployed without interrupting service?",
    ["Are deployments zero-downtime?"],
    "Frequent releases with downtime erode availability.", "Release cadence forces regular outages.",
    [R("SRC-NIST-SP800-53-R5", "CM-3", rel="informed-by"), SOC2D], "customer-preference", "medium")
c.Q(4, "Change freeze at peak", "Do you freeze non-emergency changes during our critical periods, such as the last two weeks of December for charitable giving?",
    ["Do you have blackout periods for changes?"],
    "Changes during peak periods have the highest consequence.", "A release defect during year-end giving blocks contributions or grants.",
    [UNB], "customer-preference", "high", industries=["donor-advised-funds", "nonprofit", "wealth-management"])
c.Q(4, "Emergency maintenance", "How are emergency maintenance events communicated, and how often have they occurred?",
    ["What notice is given for unplanned maintenance?"],
    "Emergency changes bypass normal notice.", "Frequent unannounced downtime.",
    [R("SRC-ISO-20000-1"), SOC2D], "contractual-common", "low")
c.Q(5, "Service credits", "What service credits apply when you miss the availability commitment, how are they calculated, and do we have to claim them?",
    ["Describe SLA remedies."],
    "Credits provide financial accountability.", "No consequence for poor availability.",
    [R("SRC-INTERAGENCY-TPRM-2023")], "contractual-common", "medium")
c.Q(5, "Chronic failure termination", "Do we have a right to terminate without penalty if you repeatedly miss service levels?",
    ["Is there a chronic SLA failure termination clause?"],
    "Credits alone do not fix a persistently unreliable vendor.", "Customer locked into an unreliable service.",
    [R("SRC-EU-DORA", "Article 28"), R("SRC-INTERAGENCY-TPRM-2023")], "contractual-common", "medium", juris=["US-federal", "EU"])
c.Q(5, "Exclusive remedy", "Are service credits our sole remedy for availability failures, including failures that cause financial loss or data integrity problems?",
    ["Are credits the exclusive remedy?"],
    "Exclusive-remedy clauses can cap recovery far below actual loss.", "Customer bears losses from vendor failure.",
    [R("SRC-INTERAGENCY-TPRM-2023")], "contractual-common", "medium", note="Overlaps with LEG category liability terms.")
c.Q(6, "Subprocessor dependency", "Which subprocessors, if they fail, would make your service unavailable, and do their outages count against your SLA?",
    ["Are third-party outages excluded from your SLA?"],
    "Vendors often exclude outages of their own chosen suppliers.", "Customer bears risk of the vendor's supplier choices.",
    [R("SRC-AICPA-TSC", "CC9.2"), R("SRC-EU-DORA", "Article 28"), R("SRC-FFIEC-BCM-BOOKLET", "Appendix J")], "supervisory-guidance", "high",
    juris=["US-federal", "EU"], authority="FFIEC member agencies; EU competent authorities")
c.Q(6, "Dependency visibility", "Do you monitor your critical providers and show us their status, for example payment connectivity or custodian feeds, inside the product or on your status page?",
    ["Can we see when an upstream provider is degraded?"],
    "Customers need to distinguish vendor failure from provider failure.", "Misdiagnosed outages and wrong escalation.",
    [UNB], "customer-preference", "medium", industries=FIN)
c.Q(7, "Degraded operation", "When a dependency such as a bank feed, custodian, or charity registry is unavailable, which functions keep working and which stop?",
    ["Describe degraded-mode behavior."],
    "Partial failure should not mean total failure.", "Minor dependency outage halts all work.",
    [R("SRC-NIST-CSF-2.0", "PR.IR-03"), UNB], "customer-preference", "high", industries=FIN)
c.Q(7, "Fail-closed financial actions", "If your system cannot confirm that a payment is safe, for example because a sanctions or hold check is stale, does it refuse the payment rather than proceed?",
    ["Do financial controls fail open or fail closed?"],
    "Systems under pressure to stay available may skip safety checks.", "Payment to a sanctioned or held recipient during degraded operation.",
    [R("SRC-OFAC-COMPLIANCE-FRAMEWORK", rel="informed-by"), R("SRC-NIST-SP800-53-R5", "SC-24", rel="informed-by"), UNB], "customer-preference", "critical",
    industries=["donor-advised-funds", "banking", "financial-services"])
c.Q(7, "Uncertain status display", "During an outage or delay, how does the interface show the status of a payment or grant whose outcome is not yet known?",
    ["Will users ever see a payment marked complete when it is not?"],
    "False success messages cause duplicate actions and donor complaints.", "Users resubmit or rely on a payment that never happened.",
    [UNB], "customer-preference", "high", industries=["donor-advised-funds", "nonprofit"])
c.Q(7, "Fail-closed reporting", "When the system refuses financial actions for safety reasons, is that counted and reported as unavailability, or excluded from your SLA?",
    ["Do safety-related refusals count as downtime?"],
    "Excluding safety refusals hides real disruptions and rewards failing open.", "Customer cannot see how often payments were blocked.",
    [UNB], "customer-preference", "medium", industries=FIN)
c.Q(6, "Flow-down of provider service levels", "Do your contracts with critical providers carry service levels and notification duties strong enough to support the commitments you make to us?",
    ["Are your upstream SLAs aligned with the SLA you offer us?"],
    "A vendor cannot reliably promise more than its suppliers commit to.", "Vendor SLA unsupported by any upstream commitment.",
    [R("SRC-FFIEC-OUTSOURCING-BOOKLET"), R("SRC-EU-DORA", "Article 30"), R("SRC-ISO-27036")], "supervisory-guidance", "medium",
    industries=FIN, juris=["US-federal", "EU"], authority="FFIEC member agencies; EU competent authorities")
c.write()
