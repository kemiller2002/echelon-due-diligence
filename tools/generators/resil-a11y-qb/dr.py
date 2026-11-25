from rqb_common import *
c = Cat("DR", {"industries": ["all"], "jurisdictions": ["US-federal"], "products": ["unbound"]})
OWN = "Proposed: SRE Lead (role not yet staffed)"
RAT = "No production deployment, hosting provider, DR topology or restore test exists as of 2026-11-25; RTO/RPO values in RR-UNB-RES-003-r2 are labeled candidates pending approval."
FIN = ["banking", "financial-services", "wealth-management", "donor-advised-funds"]

e1 = c.E(1, "Approved recovery objectives table", "Versioned table of RPO and RTO per data class (C0 to C4 in RR-UNB-RES-003-r2) and per customer-facing capability, with fault assumptions, approver and the contract clause that references it.",
         mechanism="periodic-manual", freshness="P1Y", disc="customer-only", prov=["version", "approver", "approval_date"])
e2 = c.E(2, "Failover topology and fencing test results", "Description of replica placement, quorum configuration and fencing mechanism, plus results of automated tests that a stale replica cannot authorize financial writes and that failover never produces two writers.",
         mechanism="periodic-automated", freshness="P90D", disc="nda", prov=["environment", "test_suite_version", "run_id", "result"])
e3 = c.E(3, "DR exercise report with measured recovery times", "Dated report of each failover or restore exercise stating scenario, data class, start and end timestamps, achieved RTO and RPO versus objectives, data-integrity verification results and remediation items. Production and synthetic evidence are labeled distinctly.",
         mechanism="periodic-manual", freshness="P1Y", disc="nda", prov=["exercise_id", "environment", "start", "end", "achieved_rto", "achieved_rpo", "integrity_check_digest"],
         notes="SOC2-031 requires production evidence to be kept distinct from test or synthetic evidence.")
e4 = c.E(4, "Recovery dependency map", "Machine-readable graph of what each capability needs to recover (DNS, identity provider, key management, secrets, CI/CD, database, object storage, payment connectivity) with recovery order and the alternate for each.",
         mechanism="periodic-automated", freshness="P90D", disc="nda", fmt="JSON graph generated from infrastructure definitions")
e5 = c.E(5, "Environment rebuild-from-source test", "Result of rebuilding a complete environment in a clean account from source, infrastructure definitions and Strata schema, then restoring data and passing integrity checks.",
         mechanism="periodic-automated", freshness="P180D", disc="nda", prov=["source_commit", "schema_digest", "duration", "result"])
e6 = c.E(6, "Tenant-selective restore test result", "Evidence that one tenant's data was restored to a chosen point in time without altering other tenants, with negative isolation checks on the restored data.",
         mechanism="periodic-automated", freshness="P1Y", disc="customer-only", prov=["tenant_profile", "target_time", "rows_restored", "isolation_check_result"])
e7 = c.E(7, "Post-restore payment safety verification", "Record that after a restore, payment release stayed blocked until C0 consistency checks and provider reconciliation passed, including the list of payments in Unknown status and how each was resolved.",
         mechanism="event-driven-automated", freshness="per-event", disc="customer-only", prov=["restore_id", "consistency_result", "reconciled_at", "unknown_count"])
e8 = c.E(8, "Disaster declaration and customer notification log", "Time-stamped log of disaster declaration, decision maker, customer notifications sent and acknowledgments, and the post-event report.",
         mechanism="event-driven-automated", freshness="per-event", disc="customer-only")

k1 = c.C(1, "Contractual per-data-class recovery objectives", "Commit recovery objectives per data class and capability, derived from the BIA, and reference them in every tenant contract.",
         "administrative", "L10-external-or-manual", ["not yet assigned"], [e1], OWN, related=["RR-UNB-RES-003-r2", "UNB-RES-003"],
         fw=[R("SRC-NIST-SP800-53-R5", "CP-2"), R("SRC-ISO-27002-2022", "5.30")])
k2 = c.C(2, "Fenced single authoritative writer with quorum durability", "Acknowledge authoritative financial commits only after quorum-durable replication and allow exactly one fenced writer, so failover cannot lose acknowledged commits or create split brain.",
         "preventive-structural", "L3-restricted-interface", ["Managed PostgreSQL (provider not selected)", "Unbound ledger component (not built)"], [e2], OWN,
         related=["REQ-X-006", "CNV-ARC-001"], fw=[R("SRC-NIST-SP800-53-R5", "CP-10"), R("SRC-ISO-27002-2022", "8.14")],
         residual=["RPO zero holds only under the stated fault assumptions; a correlated loss of a quorum can still lose acknowledged commits."])
k3 = c.C(3, "Scheduled recovery exercises with measured objectives", "Exercise failover and restore for every data class at least annually per isolation profile and compare measured results to objectives.",
         "detective-manual", "L8-adversarial-tested", ["not yet assigned"], [e3], OWN, related=["SOC2-015", "UNB-CTRL-080"],
         fw=[R("SRC-NIST-SP800-53-R5", "CP-4"), R("SRC-AICPA-TSC", "A1.3")])
k4 = c.C(4, "Fault-injection suite at transactional boundaries", "Inject crashes, stale replicas, provider timeouts and webhook replays at each transactional boundary in a production-like environment and assert no lost or duplicated financial effects.",
         "detective-automated", "L8-adversarial-tested", ["Unbound test harness (not built)"], [e2, e3], OWN, related=["REQ-X-081", "UNB-TEC-STRATA-004"])
k5 = c.C(5, "Generated recovery dependency map", "Generate the recovery dependency graph from infrastructure definitions so it cannot drift from the deployed system.",
         "detective-automated", "L6-automated-analysis", ["not yet assigned"], [e4], OWN)
k6 = c.C(6, "Rebuild from source into a clean account", "Ensure the full environment can be recreated from version-controlled source, infrastructure definitions and Strata schema in a new, uncompromised account.",
         "corrective", "L7-property-tested", ["Strata (schema compile and deploy)", "Praxis (provenance)", "infrastructure-as-code tool (not selected)"], [e5], OWN,
         fw=[R("SRC-NIST-SP800-53-R5", "CP-10"), R("SRC-NIST-CSF-2.0", "RC.RP-05")],
         notes="Strata is pilot status and supports PostgreSQL 16 only (ECHELON-CURRENT-STATE-BRIEF.md).")
k7 = c.C(7, "Tenant-scoped restore tooling", "Restore one tenant to a point in time through tooling bound to a single verified tenant context, with negative isolation tests on the result.",
         "preventive-structural", "L3-restricted-interface", ["Unbound tenancy component (not built)"], [e6], OWN, policies=["SEC-AUTH-001"],
         related=["UNB-TEN-014", "UNB-TEN-006"])
k8 = c.C(8, "Payment release lock after restore", "Keep payment release disabled after any restore until C0 consistency and external provider reconciliation pass and independent authorization lifts the lock; replay protective holds and cancellations first.",
         "preventive-gate", "L2-type-system", ["Unbound payments component (not built)"], [e7], "Proposed: Unbound payments owner",
         related=["REQ-X-006", "RR-UNB-RES-003-r2", "RR-REQ-X-004-r1"])
k9 = c.C(9, "Disaster declaration authority and notification procedure", "Define who may declare a disaster, notification timelines and channels, and complementary customer actions.",
         "administrative", "L10-external-or-manual", ["not yet assigned"], [e8], OWN, fw=[R("SRC-NIST-CSF-2.0", "RC.CO-03")])

a1 = c.A(1, "Recovery time and recovery point objectives", "proposed-target-state", RAT,
    "Recovery objectives are defined per data class and per capability in one versioned table referenced by each contract: acknowledged authoritative financial and security commits (ledger, reservations, approvals, holds, payee versions, authority, payment intents) have RPO zero and RTO of four hours or less; issued documents RPO zero and RTO 24 hours; operational records RPO 15 minutes and RTO 24 hours; rebuildable projections are rebuilt rather than restored. The fault assumptions under which RPO zero holds are stated explicitly, and a tenant may buy stricter RTO with a matching isolation profile.",
    "Candidate values exist in RR-UNB-RES-003-r2; they are not approved and no infrastructure exists to meet them.",
    "Approve objectives before architecture acceptance and verify by restore test before production use.",
    "Requirement text only.",
    "Our design targets zero data loss for acknowledged financial transactions and recovery within four hours for the financial core. These are candidate design targets; no production system exists and they have not been tested.",
    "planned", [k1], [e1], OWN, freshness="P1Y", mechanism="periodic-manual", automation="partial", impl="low", rec="low",
    requirements=["RR-UNB-RES-003-r2", "UNB-RES-003", "UNB-GAP-034"],
    oq=["Which managed PostgreSQL provider and replication configuration will be used, and can it deliver quorum-durable commits across zones?"])
a2 = c.A(2, "Failover, regional resilience and split-brain prevention", "proposed-target-state", RAT,
    "Unbound runs one component monolith on managed PostgreSQL with quorum-durable synchronous replication across availability zones and a fenced single writer. Authoritative financial writes are suspended, not redirected, when safe quorum is lost, so availability is traded for correctness. Regional loss is handled by restore or promotion in a secondary region that honors the tenant's residency, with an RTO stated separately for regional events. Failback requires replica catch-up and reconciliation. Cloud-provider exit is addressed by portability of data and infrastructure definitions, not by active multi-cloud.",
    "Not established. REQ-X-006 and the resilience research note define the intended design.",
    "Select provider and topology; implement fencing and quorum tests before payment features launch.",
    "Nothing.",
    "No production hosting has been selected. Our design suspends financial writes rather than risk inconsistent data during failover. Regional recovery objectives are not yet defined.",
    "planned", [k2, k4], [e2], OWN, freshness="P90D", mechanism="periodic-automated", automation="high", impl="high", rec="medium",
    requirements=["REQ-X-006", "REQ-X-047", "CNV-ARC-001"],
    challenge={
        "customer_intent": "Keep the service running through a data center or region failure.",
        "adverse_outcome": "Extended outage, or worse, inconsistent financial state after failover.",
        "conventional_control_effectiveness": "Active-active multi-region designs maximize availability but introduce conflict resolution and split-brain risk for financial ledgers; vendors often report failover success without proving no transactions were lost or duplicated.",
        "legally_required": "No statute sets vendor topology. FFIEC guidance expects banks to understand vendor resilience; EU DORA requires EU financial entities to have ICT continuity arrangements and to contract for them.",
        "contractually_required": "Bank contracts often ask for geographically separated recovery sites.",
        "historical_convention": "Hot site or secondary data center expectations from core banking.",
        "architectural_elimination": "Split brain is eliminated in scope by a fenced single writer that refuses writes without quorum.",
        "automatic_enforcement": "Fencing tokens and quorum checks enforced by the database and ledger component.",
        "continuous_evidence": "Fault-injection test results on each release.",
        "stronger_alternative": "Fail closed for money movement, fail open for read-only access, and prove it with fault injection.",
        "alternative_verifiable": "Yes, by test results and exercise reports.",
        "customer_acceptance_likelihood": "Uncertain: customers may read 'suspends writes' as lower availability.",
        "invalidating_conditions": "If the managed database cannot provide quorum-durable synchronous commit across zones.",
        "conventional_cost": "very-high", "alternative_cost": "medium",
        "alternative_risks": "Regional RTO may be longer than a multi-region active design.",
        "supporting_arguments": ["Correctness of money is the customer's primary concern.", "A single-writer design is simpler to test exhaustively."],
        "opposing_arguments": ["Longer regional recovery time.", "Customers comparing headline uptime may prefer active-active vendors."],
        "technical_effectiveness": "stronger", "institutional_acceptance": "uncertain"})
a3 = c.A(3, "DR testing and evidence", "proposed-target-state", RAT,
    "Every data class is restored at least annually per isolation profile, and failover is exercised at least annually, with measured RTO and RPO compared to objectives. A fault-injection suite runs on each release in a production-like environment. Evidence is generated automatically, time-stamped and digest-protected, and test evidence is labeled distinct from production evidence. Customers receive exercise summaries under NDA.",
    "Not established. SOC2-015 and RR-UNB-RES-003-r2 require dated recovery test evidence.",
    "Run first restore and failover exercises in a pre-production environment before production launch.",
    "Nothing.",
    "No disaster recovery test has been performed because no production environment exists. We plan annual exercises with measured results shared under NDA.",
    "planned", [k3, k4], [e3], OWN, freshness="P1Y", mechanism="periodic-automated", automation="high", impl="medium", rec="medium",
    requirements=["SOC2-015", "SOC2-031", "REQ-X-081"])
a4 = c.A(4, "Recovery dependency mapping and clean rebuild", "proposed-target-state", RAT,
    "A generated dependency map shows what each capability needs to recover and in which order, including DNS, identity provider, key management, secrets, CI/CD and payment connectivity. The whole environment can be rebuilt from source, infrastructure definitions and Strata-managed schema into a clean account, which is the recovery path for destructive cyber events such as ransomware or cloud-account compromise. Encryption keys have documented recovery procedures so that key loss cannot make backups unreadable.",
    "Not established. Strata exists as a declarative schema tool in pilot status (PostgreSQL 16 only) but is not operated for any production Echelon service.",
    "Adopt infrastructure as code from the first environment; test clean rebuild twice a year.",
    "Strata can compile and diff schemas today; no environment rebuild has been performed.",
    "We intend to be able to rebuild the full environment from source into a clean account. This is a design intent and has not been tested.",
    "planned", [k5, k6], [e4, e5], OWN, freshness="P180D", mechanism="periodic-automated", automation="high", impl="medium", rec="low",
    requirements=["UNB-GAP-030", "UNB-GAP-034"])
a5 = c.A(5, "Tenant-level restoration", "proposed-target-state", RAT,
    "A single tenant can be restored to a chosen point in time without affecting other tenants, using tooling bound to one verified tenant context and verified by negative isolation tests. The capability depends on isolation profile: dedicated databases restore independently; shared physical backups do not by themselves guarantee independent tenant recovery, and Echelon discloses that limit. Tenants on dedicated profiles may have separately configured and tested objectives.",
    "Not established. UNB-TEN-014 explicitly warns that shared physical backups do not guarantee tenant-selective recovery.",
    "Default to dedicated database per tenant (Profile B) and test tenant-selective restore annually.",
    "Nothing.",
    "Our design isolates each sponsor in its own database by default so it can be restored independently. This has not been built or tested.",
    "planned", [k7], [e6], OWN, freshness="P1Y", mechanism="periodic-automated", automation="high", impl="medium", rec="low",
    requirements=["UNB-TEN-014", "UNB-TEN-006", "UNB-TEN-008"], policies=["SEC-AUTH-001"],
    challenge={
        "customer_intent": "Recover our data after our own error or a corruption without waiting for, or harming, other customers.",
        "adverse_outcome": "Restore of a shared database rolls back other tenants or exposes their data.",
        "conventional_control_effectiveness": "Most multi-tenant vendors restore whole databases and extract one tenant manually, which is slow and error-prone.",
        "legally_required": "No.",
        "contractually_required": "Occasionally in enterprise contracts.",
        "historical_convention": "Single-tenant hosting made this trivial; SaaS made it rare.",
        "architectural_elimination": "Per-tenant databases eliminate cross-tenant rollback in scope.",
        "automatic_enforcement": "Restore tooling accepts exactly one tenant context.",
        "continuous_evidence": "Annual restore test per profile.",
        "stronger_alternative": "Per-tenant database plus append-only history allows both restore and deterministic replay to a point.",
        "alternative_verifiable": "Yes.",
        "customer_acceptance_likelihood": "Likely.",
        "invalidating_conditions": "If cost pressure forces shared-schema Profile A for small tenants.",
        "conventional_cost": "medium", "alternative_cost": "medium",
        "alternative_risks": "More databases increase operational overhead and upgrade coordination.",
        "supporting_arguments": ["Clear blast-radius boundaries."],
        "opposing_arguments": ["Per-tenant databases cost more at small scale."],
        "technical_effectiveness": "stronger", "institutional_acceptance": "likely"})
a6 = c.A(6, "Financial integrity and payment safety after recovery", "proposed-target-state", RAT,
    "After any restore or failover, payment release stays blocked until consistency checks across all C0 stores pass and external bank and custodian outcomes are reconciled; payments with Unknown outcomes cannot be re-sent until resolved through the rail's protocol. Protective holds and cancellations are replayed before anything else, and independent authorization is required to lift the lock. If a recovery would lose an acknowledged financial fact, an approved procedure defines compensating records and customer notice.",
    "Not established. REQ-X-006, RR-REQ-X-004-r1 and RR-UNB-RES-003-r2 specify this behavior; the acceptance scenario in REQ-X-006 is marked not executed.",
    "Implement the release lock and reconciliation gate as part of the payments component; include in every restore exercise.",
    "Nothing.",
    "Our design keeps payments blocked after any recovery until balances and payment outcomes are reconciled, to prevent duplicate or lost payments. This has not been built or tested.",
    "planned", [k8], [e7], "Proposed: Unbound payments owner", freshness="per-event", mechanism="event-driven-automated", automation="full", impl="medium", rec="low",
    requirements=["REQ-X-006", "RR-REQ-X-004-r1", "RR-UNB-RES-003-r2"],
    challenge={
        "customer_intent": "Ensure recovery does not create financial errors.",
        "adverse_outcome": "Payments resent after restore, holds lost, canceled grants paid.",
        "conventional_control_effectiveness": "Conventional DR questions measure time to restore and ignore whether restored state is safe to act on; a fast restore that replays stale instructions is worse than a slow one.",
        "legally_required": "No specific rule for Echelon; Nacha and UCC 4A allocate loss for erroneous payments to the originator and its bank, which is the customer.",
        "contractually_required": "Rarely stated explicitly.",
        "historical_convention": "Core processors reconcile after recovery by manual procedure.",
        "architectural_elimination": "Duplicate dispatch is eliminated in scope by an idempotent payment chain that blocks re-dispatch while an outcome is Unknown.",
        "automatic_enforcement": "Release lock is a typed state the dispatch path cannot bypass.",
        "continuous_evidence": "Per-restore verification record.",
        "stronger_alternative": "Treat RTO for money movement as time to safe, reconciled state, and report it that way.",
        "alternative_verifiable": "Yes, in restore exercises.",
        "customer_acceptance_likelihood": "Likely for finance teams; uncertain for buyers who compare headline RTO.",
        "invalidating_conditions": "If provider reconciliation data is unavailable for long periods.",
        "conventional_cost": "low", "alternative_cost": "medium",
        "alternative_risks": "Payments may stay blocked longer than the customer tolerates.",
        "supporting_arguments": ["Prevents the most damaging recovery error."],
        "opposing_arguments": ["Longer effective RTO for payments."],
        "technical_effectiveness": "stronger", "institutional_acceptance": "likely"})
a7 = c.A(7, "Disaster declaration, communication and customer responsibilities", "proposed-target-state", RAT,
    "Named roles may declare a disaster; customers are notified through pre-registered alternate channels within one hour of declaration, receive status at defined intervals, and receive a post-event report within ten business days stating achieved RTO and RPO against commitments. Complementary customer responsibilities (verifying balances, resubmitting rejected requests, confirming out-of-band payments) are documented in advance.",
    "Not established.",
    "Define declaration authority and notification procedure with the continuity plan.",
    "Nothing.",
    "We have not yet defined disaster declaration authority or notification timelines. We plan to document them, including customer responsibilities, before production.",
    "planned", [k9], [e8], OWN, mechanism="event-driven-automated", automation="partial", impl="low", rec="low", requirements=["SOC2-022", "SOC2-026"])

c.Q(1, "Recovery objectives", "What are your recovery time and recovery point objectives for each service we would use?",
    ["Provide RTO and RPO for the production environment.", "How much data could we lose, and for how long could we be down, in a disaster?"],
    "Customer must align its own continuity plan with vendor recovery capability.", "Customer assumes faster recovery or less data loss than the vendor can deliver.",
    [R("SRC-NIST-SP800-34-R1"), R("SRC-ISO-27002-2022", "5.30"), R("SRC-FFIEC-BCM-BOOKLET"), R("SRC-SA-SIG"), R("SRC-CSA-CAIQ-V4"), R("SRC-EDUCAUSE-HECVAT"), UNB],
    "supervisory-guidance", "critical", authority="FFIEC member agencies (for bank customers)")
c.Q(1, "Recovery objectives by data class", "Do your recovery objectives differ by type of data, for example ledger transactions versus documents versus search indexes, and what are the values for each?",
    ["Is RPO zero for financial transactions?"],
    "A single RPO hides that financial records need stronger protection than derived data.", "Financial transactions lost under an RPO set for less critical data.",
    [R("SRC-NIST-SP800-34-R1"), UNB], "customer-preference", "high", industries=FIN)
c.Q(1, "Contractual objectives", "Are your recovery objectives committed in the contract, with remedies if missed, and can we purchase stricter objectives?",
    ["Are RTO/RPO contractual or targets only?"],
    "Non-contractual targets provide no recourse.", "Vendor misses targets without consequence.",
    [R("SRC-EU-DORA", "Article 30"), R("SRC-INTERAGENCY-TPRM-2023")], "contractual-common", "high", juris=["US-federal", "EU"])
c.Q(1, "Fault assumptions", "Under what failure conditions does your stated RPO hold, and which correlated failures could cause loss of transactions you had already confirmed to us?",
    ["What assumptions underlie your zero data loss claim?"],
    "RPO claims are meaningless without the failure model behind them.", "Customer relies on an RPO zero claim that fails under realistic correlated failures.",
    [R("SRC-NIST-SP800-34-R1"), UNB], "customer-preference", "high", industries=FIN)
c.Q(2, "Failover", "Is production deployed across multiple availability zones or data centers, is failover automatic or manual, and how long does it take?",
    ["Describe your high availability architecture."],
    "Single-site deployment is a single point of failure.", "Prolonged outage from a single facility failure.",
    [R("SRC-ISO-27002-2022", "8.14"), R("SRC-NIST-SP800-53-R5", "CP-7"), R("SRC-AICPA-TSC", "A1.2"), R("SRC-CSA-CCM-V4")], "industry-convention", "high")
c.Q(2, "Split-brain prevention", "During failover, how do you prevent two database nodes from accepting writes at the same time, or a stale replica from authorizing a payment?",
    ["How do you ensure consistency of financial data during failover?"],
    "Failover can produce inconsistent financial state.", "Duplicate or conflicting financial transactions after failover.",
    [R("SRC-NIST-SP800-53-R5", "CP-10"), UNB], "customer-preference", "high", industries=FIN)
c.Q(2, "Regional resilience", "Can you continue or restore service if an entire cloud region is lost, where is the recovery region, and does it keep our data in our required jurisdiction?",
    ["Do you have geographically diverse recovery capability?"],
    "Regional events affect all zones in a region.", "Extended outage or residency violation during regional recovery.",
    [R("SRC-NIST-SP800-53-R5", "CP-6"), R("SRC-NIST-SP800-53-R5", "CP-7"), R("SRC-GDPR", rel="informed-by"), R("SRC-FFIEC-ARCHITECTURE-BOOKLET")], "supervisory-guidance", "high",
    juris=["US-federal", "EU"], authority="FFIEC member agencies")
c.Q(2, "Cloud concentration", "Do you depend on a single cloud provider, and what is your plan if that provider becomes unavailable to you for an extended period or terminates your account?",
    ["Do you have a cloud exit strategy?"],
    "Concentration on one hyperscaler is a systemic risk regulators track.", "Account suspension or provider failure halts service indefinitely.",
    [R("SRC-EU-DORA", "Article 28"), R("SRC-FFIEC-ARCHITECTURE-BOOKLET"), R("SRC-INTERAGENCY-TPRM-2023")], "supervisory-guidance", "medium",
    industries=FIN, juris=["US-federal", "EU"], authority="EU competent authorities; FFIEC member agencies")
c.Q(2, "Failback", "After failing over, how do you return to the primary site, and how do you verify that no data was lost or duplicated in the process?",
    ["Describe your failback procedure."],
    "Failback is a second risky transition that is rarely tested.", "Data divergence introduced during return to primary.",
    [R("SRC-NIST-SP800-34-R1"), UNB], "industry-convention", "medium")
c.Q(3, "DR testing", "How often do you test disaster recovery, does testing include an actual failover or full restore, and can you share the most recent results including the recovery times achieved?",
    ["Provide your last DR test report.", "When did you last perform a full DR test?"],
    "Untested DR plans routinely fail.", "Recovery objectives are unachievable in practice.",
    [R("SRC-NIST-SP800-53-R5", "CP-4"), R("SRC-AICPA-TSC", "A1.3"), R("SRC-FFIEC-BCM-BOOKLET"), R("SRC-NYDFS-PART-500", "500.16"), R("SRC-EU-DORA", "Article 11")],
    "supervisory-guidance", "critical", juris=["US-federal", "EU"], authority="FFIEC member agencies; NYDFS; EU competent authorities")
c.Q(3, "Test realism", "Do recovery tests use production-scale data volumes, and did measured recovery meet your stated objectives?",
    ["Were RTO and RPO met in your last test?"],
    "Small-scale tests understate recovery time.", "Restore of a full-size ledger takes far longer than tested.",
    [R("SRC-NIST-SP800-34-R1"), UNB], "customer-preference", "high")
c.Q(3, "Test evidence integrity", "How is DR test evidence produced and protected, and how do you distinguish it from production evidence?",
    ["Is DR test evidence system-generated?"],
    "Hand-assembled test reports can overstate success.", "Customer relies on embellished or fabricated test results.",
    [R("SRC-AICPA-TSC", "A1.3"), SOC2D], "customer-preference", "medium", disc="nda")
c.Q(3, "Fault injection", "Do you deliberately inject failures, such as process crashes mid-transaction or delayed provider responses, to prove recovery correctness?",
    ["Do you perform chaos engineering?"],
    "Recovery paths that are never exercised harbor defects.", "Crash during a payment leaves inconsistent state.",
    [R("SRC-NIST-SP800-53-R5", "CP-4"), UNB], "customer-preference", "medium", industries=FIN)
c.Q(4, "Dependency mapping", "Do you maintain a map of what each service needs to recover, such as DNS, identity provider, key management, secrets and payment connectivity, and the order of recovery?",
    ["Have you documented recovery dependencies?"],
    "Recovery stalls on an overlooked dependency.", "Systems restored but unusable because a dependency was not recovered.",
    [R("SRC-NIST-SP800-34-R1"), R("SRC-ISO-27031"), R("SRC-NIST-CSF-2.0", "RC.RP-01")], "industry-convention", "medium")
c.Q(4, "Key management recovery", "If your key management service or encryption keys were lost or unavailable, could you still recover our data, and how is that tested?",
    ["What is your plan for loss of encryption keys?"],
    "Encrypted backups are useless without keys.", "Permanent data loss through key loss.",
    [R("SRC-NIST-SP800-53-R5", "SC-12"), SCS], "industry-convention", "high", disc="nda")
c.Q(4, "Destructive cyber event recovery", "If your production cloud account were compromised or encrypted by ransomware, can you rebuild the environment from source in a clean account, and how long would that take?",
    ["Describe your ransomware recovery plan."],
    "Destructive attacks defeat replication-based DR.", "Replicated corruption or attacker persistence after recovery.",
    [R("SRC-NIST-CSF-2.0", "RC.RP-05"), R("SRC-FFIEC-BCM-BOOKLET"), R("SRC-NYDFS-PART-500", "500.16")], "supervisory-guidance", "critical",
    industries=FIN, authority="FFIEC member agencies; NYDFS")
c.Q(5, "Tenant-selective restore", "Can you restore only our data to a specific point in time without affecting other customers?",
    ["If we corrupt our own data, can you restore just our tenant?"],
    "Customer errors require tenant-level recovery.", "Customer cannot recover from its own error without a platform-wide restore.",
    [R("SRC-CSA-CCM-V4"), UNB], "customer-preference", "high")
c.Q(5, "Isolation during restore", "During a restore, how do you prevent our data from being mixed with, or exposed to, another customer's data?",
    ["How is tenant isolation preserved during recovery operations?"],
    "Restore tooling often runs with elevated, cross-tenant privileges.", "Cross-tenant data exposure during recovery.",
    [R("SRC-ISO-27017"), SCS, UNB], "customer-preference", "high")
c.Q(5, "Dedicated profile objectives", "If we choose a dedicated database or deployment, are our recovery objectives configured and tested independently of shared tenants?",
    ["Do dedicated environments have their own DR testing?"],
    "Dedicated isolation should come with matching recovery evidence.", "Dedicated tenant assumes independent DR that was never tested.",
    [UNB], "customer-preference", "medium", industries=["banking", "donor-advised-funds"])
c.Q(6, "Duplicate payment prevention after restore", "After restoring from a backup, how do you ensure payments sent after the backup point are not sent again?",
    ["How do you avoid replaying financial instructions after recovery?"],
    "Restores roll the system back to before payments were sent.", "Duplicate payments to grantees.",
    [R("SRC-NACHA-RULES", rel="informed-by"), R("SRC-UCC-4A", rel="informed-by"), UNB], "customer-preference", "critical", industries=["donor-advised-funds", "banking", "financial-services"])
c.Q(6, "External reconciliation before resume", "Before resuming money movement after a recovery, how do you reconcile restored balances and payment states with bank and custodian records?",
    ["Do you reconcile with external records after DR?"],
    "Restored internal state may disagree with external reality.", "Payments made against incorrect available balances.",
    [R("SRC-FFIEC-BCM-BOOKLET"), UNB], "customer-preference", "critical", industries=["donor-advised-funds", "banking", "financial-services"])
c.Q(6, "Recovery ordering for protective actions", "Does your recovery sequence restore protective controls, such as holds, freezes and access revocations, before any function that can move money?",
    ["What is restored first after an outage?"],
    "A hold placed just before an outage can be lost if payments recover first.", "Payment released that a hold should have stopped.",
    [UNB], "customer-preference", "high", industries=["donor-advised-funds", "banking"])
c.Q(7, "Disaster declaration", "Who has authority to declare a disaster, and how quickly and by what channels will we be notified after declaration?",
    ["What is your notification timeline in a DR event?"],
    "Customers need prompt notice to invoke their own plans.", "Customer learns of a disaster late and cannot act.",
    [R("SRC-NIST-CSF-2.0", "RC.CO-03"), R("SRC-CIRN-RULE-2021", "12 CFR 53.4"), R("SRC-NIST-SP800-34-R1")], "contractual-common", "high", authority="OCC, FDIC, Federal Reserve (bank service providers)",
    note="The CIRN bank service provider notice duty applies only if Echelon is a bank service provider to a banking organization; it is otherwise a contractual expectation.")
c.Q(7, "Customer responsibilities", "What must we do during and after a disaster, for example resubmitting transactions or confirming balances, and is this documented in advance?",
    ["What are the complementary user entity controls for recovery?"],
    "Shared responsibilities are often discovered during the event.", "Gaps between vendor and customer recovery steps.",
    [R("SRC-AICPA-SOC2-GUIDE"), SOC2D], "industry-convention", "medium")
c.Q(7, "Post-event reporting", "After an actual disaster or major recovery, will you give us a written report comparing achieved recovery time and data loss with your commitments?",
    ["Do you provide post-incident DR reports?"],
    "Customers and their examiners need evidence of how recovery went.", "Missed objectives go unreported.",
    [R("SRC-EU-DORA", "Article 11"), R("SRC-INTERAGENCY-TPRM-2023")], "contractual-common", "medium", juris=["US-federal", "EU"])
c.write()
