from rqb_common import *
c = Cat("PRF", {"industries": ["all"], "jurisdictions": ["US-federal"], "products": ["unbound"]})
OWN = "Proposed: SRE Lead (role not yet staffed)"
RAT = "No production system, load test, capacity model or performance baseline exists as of 2026-11-25."
DAFI = ["donor-advised-funds", "nonprofit", "wealth-management"]

e1 = c.E(1, "Capacity model and headroom report", "Versioned capacity model per tenant database and shared component with current utilization, forecast from volume drivers, headroom against benchmarked sustainable capacity, and actions triggered.",
         mechanism="periodic-automated", freshness="P30D", disc="nda")
e2 = c.E(2, "Per-tenant resource quota configuration and breach log", "Configured connection, compute and rate limits per tenant and per agent identity, with events when limits are reached.",
         mechanism="continuous-automated", freshness="P1D", disc="customer-only")
e3 = c.E(3, "Load and surge test report", "Reproducible load test results on the selected managed PostgreSQL modeling the largest expected sponsor at 10x normal grant volume, historical replay and projection rebuild, with p50/p95/p99 latencies, commit rate, outbox dispatch lag and pass/fail against thresholds.",
         mechanism="periodic-automated", freshness="P90D", disc="nda", prov=["test_id", "dataset_scale", "code_commit", "environment", "results_digest"])
e4 = c.E(4, "Performance SLO report", "Per-capability latency and throughput against published SLOs, from real-user monitoring segmented by device class and network quality and from server-side metrics.",
         mechanism="continuous-automated", freshness="P30D", disc="customer-only")
e5 = c.E(5, "Batch schedule and cut-off adherence log", "Schedule of batch jobs (payment file generation, statements, receipts, reconciliation) with actual start and finish times, comparison to rail and business cut-offs, and any misses.",
         mechanism="event-driven-automated", freshness="per-event", disc="customer-only")

k1 = c.C(1, "Driver-based capacity planning with headroom triggers", "Forecast capacity from documented volume drivers and act before utilization of benchmarked sustainable capacity exceeds the threshold.",
         "detective-automated", "L9-runtime-monitored", ["not yet assigned"], [e1], OWN, related=["UNB-XIN-EVA-013", "RR-UNB-ECO-001-r2"],
         fw=[R("SRC-AICPA-TSC", "A1.1"), R("SRC-ISO-27002-2022", "8.6"), R("SRC-NIST-CSF-2.0", "PR.IR-04")])
k2 = c.C(2, "Per-tenant and per-agent resource isolation", "Prevent one tenant, integration or AI agent from exhausting shared capacity through quotas, bounded fan-out and default dedicated databases.",
         "preventive-structural", "L3-restricted-interface", ["Managed PostgreSQL per-tenant database (provider not selected)", "Unbound API gateway (not built)"], [e2], OWN,
         policies=["SEC-AUTH-001"], related=["UNB-WF-005", "UNB-TEN-006"], fw=[R("SRC-OWASP-API-TOP10-2023", "API4:2023")])
k3 = c.C(3, "Surge load test as release gate", "Block release of changes to control-relevant or high-volume paths unless the surge load test passes thresholds on production-scale data.",
         "preventive-gate", "L5-build-release-gate", ["Unbound release pipeline (not built)"], [e3], OWN, related=["UNB-IMM-010", "UNB-ACC-036", "UNB-XIN-EVA-013"])
k4 = c.C(4, "Performance SLO monitoring", "Measure latency and throughput per capability from real users and servers and alert on SLO burn.",
         "detective-automated", "L9-runtime-monitored", ["not yet assigned"], [e4], OWN)
k5 = c.C(5, "Cut-off-aware batch scheduling", "Schedule batch work against rail and business cut-offs with alerts before a deadline is at risk, and isolate batch load from interactive use.",
         "preventive-gate", "L9-runtime-monitored", ["Unbound scheduler (not built)"], [e5], "Proposed: Unbound payments owner", related=["UNB-GAP-003", "CNV-PAY-007"])

a1 = c.A(1, "Capacity planning and tenant resource isolation", "proposed-target-state", RAT,
    "Capacity is planned from documented volume drivers (accounts per sponsor, activity segments, grant volume, document generation, AI-assisted case volume) and monitored against benchmarked sustainable capacity of the largest sponsor database; action is taken before peak commit rate reaches 50 percent of that capacity. Each sponsor has its own database by default, and quotas bound connections, API rates, fan-out and agent usage per tenant so no tenant can degrade another. When demand exceeds capacity, the system applies backpressure and queues deferrable work rather than failing, and never queues approvals or payments in a way that bypasses revalidation.",
    "Not established. UNB-XIN-EVA-013 sets the 50 percent threshold for introducing additional infrastructure; RR-UNB-ECO-001-r2 lists volume drivers.",
    "Build the capacity model alongside the first load test.",
    "Nothing.",
    "No capacity plan exists because no production system exists. Our design isolates each sponsor's database by default and sets explicit capacity thresholds.",
    "planned", [k1, k2], [e1, e2], OWN, freshness="P30D", mechanism="periodic-automated", automation="high", impl="medium", rec="low",
    requirements=["UNB-XIN-EVA-013", "RR-UNB-ECO-001-r2", "UNB-WF-005", "UNB-TEN-006"])
a2 = c.A(2, "Load testing and peak-event readiness", "proposed-target-state", RAT,
    "Load tests on the selected managed PostgreSQL model the year-end peak of the largest expected sponsor at ten times normal grant volume, plus historical replay and projection rebuild at production scale, and run as a release gate for high-volume paths. Year-end readiness includes a documented plan, conjunction drills (surge plus market plus provider plus regulatory change) and a staffing surge playbook. Results with thresholds and pass/fail are shared under NDA.",
    "Not established. UNB-IMM-010, UNB-ACC-036, UNB-WF-005 and TVR-OPS-003 require surge testing and year-end readiness; none has run.",
    "Run the first surge benchmark before choosing to add any second store or broker, as UNB-XIN-EVA-013 requires.",
    "Nothing.",
    "No load testing has been performed. Our requirements call for testing at ten times normal grant volume before production, including year-end peak modeling.",
    "planned", [k3], [e3], OWN, freshness="P90D", mechanism="periodic-automated", automation="high", impl="medium", rec="medium",
    requirements=["UNB-IMM-010", "UNB-ACC-036", "UNB-WF-005", "TVR-OPS-003", "UNB-ECO-005"],
    challenge={
        "customer_intent": "Be confident the platform will not slow down or fail during year-end giving.",
        "adverse_outcome": "Contributions or grants miss December 31 or rail cut-offs; donors lose deductions for the intended year.",
        "conventional_control_effectiveness": "Vendors usually cite autoscaling and a periodic load test. Autoscaling does not scale a single authoritative database writer, and generic load tests rarely model the real year-end shape or long ledger histories.",
        "legally_required": "No.",
        "contractually_required": "Sometimes as performance warranties.",
        "historical_convention": "Seasonal capacity reviews and change freezes.",
        "architectural_elimination": "Partly: per-sponsor databases bound the largest single workload to one sponsor's peak rather than the sum of all sponsors.",
        "automatic_enforcement": "Load test as a release gate on high-volume paths.",
        "continuous_evidence": "Quarterly load test reports and live headroom metrics.",
        "stronger_alternative": "Measured thresholds tied to architectural decisions (no new infrastructure until measured need), plus per-tenant partitioning of load.",
        "alternative_verifiable": "Yes, through reproducible benchmark reports.",
        "customer_acceptance_likelihood": "Likely, if benchmark evidence is shared.",
        "invalidating_conditions": "If the largest sponsor's peak exceeds what one managed PostgreSQL instance can sustain after tuning.",
        "conventional_cost": "medium", "alternative_cost": "medium",
        "alternative_risks": "Synthetic year-end shape may not match a real sponsor's peak, especially for a sponsor migrating mid-year.",
        "supporting_arguments": ["Avoids premature complexity that itself causes outages.", "Bounds blast radius of one sponsor's surge."],
        "opposing_arguments": ["A single-writer database has a hard ceiling that scale-out designs avoid.", "No real-world peak has been observed."],
        "technical_effectiveness": "equivalent", "institutional_acceptance": "likely"})
a3 = c.A(3, "Performance service levels and reporting", "proposed-target-state", RAT,
    "Echelon publishes performance SLOs per capability (for example interactive page response and command acknowledgment at the 95th percentile on mid-range phones over constrained networks, and maximum time from approval to payment file generation), measured with real-user monitoring segmented by device and network class and by server metrics, and reports them monthly per tenant. Performance SLOs are published only after a measured baseline exists.",
    "Not established.",
    "Establish baselines in a production-like environment before offering performance commitments.",
    "Nothing.",
    "We do not currently offer performance service levels. We plan to publish them once we have measured baselines.",
    "not-available", [k4], [e4], OWN, freshness="P30D", mechanism="continuous-automated", automation="full", impl="low", rec="low", requirements=["CNV-EXP-001", "UNB-PLAT-004"])
a4 = c.A(4, "Batch windows and processing deadlines", "proposed-target-state", RAT,
    "Batch work (payment file generation, reconciliation, statements, year-end acknowledgments) is scheduled against rail cut-offs and business deadlines and isolated from interactive load, so batches do not cause online slowdowns. Requests approved before a published internal cut-off are included in the next rail submission, with alerts raised before a deadline is at risk. Year-end acknowledgment and statement generation are capacity-tested for full-volume completion well before donors need them for tax filing, and Folio rendering throughput is measured before Folio is relied on for statements.",
    "Not established. UNB-GAP-003 (operational cut-offs and close) and CNV-EXP-001 (rendering throughput tests) specify the need. Folio is a print component system without production-qualified accessible PDF output (folio@56a18e1:docs/requirements/unbound-financial-report-consumer-capability-review-2026-11-23.md).",
    "Define cut-off schedules per rail with the payments component; measure document throughput in a rendering spike.",
    "Nothing.",
    "We have not yet defined batch windows or cut-off schedules. We plan to schedule processing against payment-rail cut-offs and to test year-end document volumes before production.",
    "planned", [k5], [e5], "Proposed: Unbound payments owner", freshness="per-event", mechanism="event-driven-automated", automation="high", impl="medium", rec="low",
    requirements=["UNB-GAP-003", "CNV-PAY-007", "CNV-EXP-001", "UNB-XIN-SVC-008"])

c.Q(1, "Capacity planning", "How do you plan capacity, how often do you review it, and what utilization level triggers action?",
    ["Describe your capacity management process."],
    "Capacity shortfalls cause slowdowns and outages.", "Service degrades as customer volume grows.",
    [R("SRC-AICPA-TSC", "A1.1"), R("SRC-ISO-27002-2022", "8.6"), R("SRC-NIST-SP800-53-R5", "CP-2(2)"), R("SRC-SA-SIG"), R("SRC-CSA-CAIQ-V4")], "industry-convention", "medium")
c.Q(1, "Noisy neighbor protection", "How do you prevent another customer's workload, integration or automated agent from slowing down our use of the service?",
    ["How is resource contention between tenants managed?"],
    "Shared infrastructure exposes customers to others' load.", "Another tenant's batch or attack degrades our service.",
    [R("SRC-OWASP-API-TOP10-2023", "API4:2023"), R("SRC-ISO-27017"), SCS], "customer-preference", "high")
c.Q(1, "Onboarding and migration load", "Can you absorb the load of migrating our full history and onboarding all our accounts at once without affecting performance for us or others?",
    ["What is the impact of a large data migration?"],
    "Bulk migrations are a common cause of performance incidents.", "Migration overruns or degrades production.",
    [UNB], "customer-preference", "medium", industries=DAFI)
c.Q(1, "Overload behavior", "When demand exceeds capacity, does the system queue, throttle or reject work, and how are users informed?",
    ["What happens when the system is overloaded?"],
    "Uncontrolled overload causes cascading failure.", "Requests silently lost or duplicated under load.",
    [R("SRC-NIST-SP800-53-R5", "SC-5"), UNB], "customer-preference", "medium")
c.Q(1, "Ledger growth", "How does performance hold up as our transaction history grows over many years, given that financial records are kept indefinitely or for long retention periods?",
    ["Is performance affected by data volume over time?"],
    "Append-only ledgers grow without bound.", "Reports and queries slow to unusable levels after years of history.",
    [UNB], "customer-preference", "medium", industries=["donor-advised-funds", "financial-services"])
c.Q(1, "AI throughput limits", "Do AI-assisted functions such as grant or charity vetting have throughput or rate limits that could create backlogs at peak, and how are backlogs handled?",
    ["Could AI provider rate limits delay our grants?"],
    "Third-party AI rate limits are outside the vendor's control.", "Vetting backlog delays grants at year-end.",
    [R("SRC-OWASP-LLM-TOP10-2025", "LLM10:2025"), UNB], "customer-preference", "medium", industries=DAFI)
c.Q(2, "Load testing", "Do you load test before major releases, at what multiple of expected peak, and can you share recent results?",
    ["Provide your most recent performance test report."],
    "Untested performance fails under real load.", "Release introduces regressions that appear only at scale.",
    [R("SRC-AICPA-TSC", "A1.1", rel="informed-by"), R("SRC-EDUCAUSE-HECVAT"), UNB], "customer-preference", "high")
c.Q(2, "Year-end giving peak", "How have you modeled and tested the year-end charitable giving peak, including Giving Tuesday and the final days of December, and what evidence shows the platform will keep up?",
    ["Are you prepared for December 31 volume?"],
    "DAF and nonprofit volume concentrates sharply at year-end.", "Donors miss tax-year deadlines; grants delayed.",
    [R("SRC-IRC-170", rel="informed-by"), R("SRC-ECH-DAF-LANDSCAPE", rel="informed-by", basis="reasonably-inferred"), UNB], "customer-preference", "critical", industries=DAFI)
c.Q(2, "Production-scale test data", "Do performance tests use production-scale data volumes, including long transaction histories and full rebuilds of derived views?",
    ["Are load tests run on realistic data sizes?"],
    "Small test datasets hide performance problems.", "Performance collapses on real data volumes.",
    [UNB], "customer-preference", "medium")
c.Q(3, "Performance SLAs", "Do you commit to response-time or throughput service levels, and how are they defined?",
    ["What are your performance SLAs?"],
    "Slow systems impose real operational costs.", "Persistently slow service with no recourse.",
    [R("SRC-ISO-20000-1"), R("SRC-EDUCAUSE-HECVAT")], "contractual-common", "medium")
c.Q(3, "Performance reporting", "Do you report actual performance to customers, and can we see metrics for our own tenant?",
    ["Are performance metrics shared with clients?"],
    "Customers need evidence to hold vendors to performance commitments.", "Disputes over slowness with no data.",
    [R("SRC-ISO-20000-1")], "customer-preference", "low")
c.Q(3, "Mobile and low-bandwidth performance", "How do you measure performance for users on phones and slow or unreliable networks, not only on office connections?",
    ["Is the application usable on mobile networks?"],
    "Donors and advisors increasingly act from phones.", "Mobile users time out or submit duplicates.",
    [UNB], "customer-preference", "medium", industries=DAFI)
c.Q(4, "Batch windows", "When do batch processes such as payment files, statements and reconciliations run, and do they slow down or interrupt online use?",
    ["Describe your batch processing schedule."],
    "Batch contention degrades interactive use.", "Users locked out or slowed during batch runs.",
    [R("SRC-FFIEC-ARCHITECTURE-BOOKLET")], "industry-convention", "low")
c.Q(4, "Payment cut-offs", "If we approve a grant before a stated cut-off, do you guarantee it will be submitted in time for the payment rail's processing deadline that day?",
    ["What are your daily payment cut-off times?"],
    "Missed rail cut-offs delay payments by a business day or more.", "Grants arrive late; charities miss funding.",
    [R("SRC-NACHA-RULES", rel="informed-by"), UNB], "contractual-common", "high", industries=["donor-advised-funds", "banking"])
c.Q(4, "Year-end document volume", "Can you generate and deliver all year-end contribution acknowledgments and statements in time for donors' tax filing, and has that volume been tested?",
    ["How quickly can you produce year-end tax receipts?"],
    "Donors need written acknowledgments to substantiate deductions.", "Late acknowledgments generate donor complaints and substantiation risk.",
    [R("SRC-IRS-PUB-1771", rel="informed-by"), R("SRC-IRC-170", rel="informed-by"), UNB], "industry-convention", "high", industries=DAFI)
c.write()
