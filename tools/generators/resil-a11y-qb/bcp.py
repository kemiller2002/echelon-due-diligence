from rqb_common import *
c = Cat("BCP", {"industries": ["all"], "jurisdictions": ["US-federal"], "products": ["all-echelon-products"]})
OWN = "Proposed: Business Continuity Owner (role not yet staffed)"
BIZ_NOTE = "Echelon has no production service and no adopted BCM policy as of 2026-11-25; answers describe target state."

# ---------- Evidence requirements ----------
e1 = c.E(1, "Approved business continuity policy and program charter",
         "Versioned policy naming scope (all customer-facing services and supporting functions), accountable executive, review cadence, approval record and change history.",
         mechanism="periodic-manual", freshness="P1Y", disc="nda", fmt="Markdown policy in a governed repository with approval record",
         prov=["version", "approver", "approval_date", "commit"], retention="P7Y")
e2 = c.E(2, "Business impact analysis register",
         "Per-function record of consequence over time, maximum tolerable period of disruption, minimum service level, dependencies (people, systems, providers, AI models) and derived recovery objectives, reviewed at least annually and on material change.",
         mechanism="periodic-manual", freshness="P1Y", disc="nda", fmt="JSON Lines register with schema",
         prov=["function_id", "reviewer", "review_date", "dependency_versions"])
e3 = c.E(3, "Continuity plan set and out-of-band copy attestation",
         "Plans and runbooks per disruption scenario (loss of people, technology, facility, provider) with evidence that a current copy is reachable when the primary cloud account and identity provider are unavailable.",
         mechanism="periodic-automated", freshness="P90D", disc="nda",
         prov=["plan_version", "copy_location_class", "checked_at", "digest"],
         notes="The out-of-band reachability check could be automated by comparing digests of the governed copy and the offline copy.")
e4 = c.E(4, "Exercise and test reports with remediation tracking",
         "Dated report for each tabletop, functional or full exercise: scenario, participants (including customer or provider participants), objectives, observed timings, findings and linked remediation items with closure evidence.",
         mechanism="periodic-manual", freshness="P1Y", disc="nda", prov=["exercise_id", "date", "participants", "findings", "remediation_ids"])
e5 = c.E(5, "Key-person dependency register and portability test result",
         "Register of capabilities, credentials and decisions that depend on one individual, with named alternates and the result of an exercise in which an alternate or qualified third party performed the capability from documentation alone.",
         mechanism="periodic-manual", freshness="P180D", disc="nda", prov=["capability_id", "primary", "alternate", "last_portability_test"])
e6 = c.E(6, "Emergency credential custody record",
         "Inventory of root, registrar, signing, cloud-organization and break-glass credentials showing custody arrangement (sealed, split or dual control), holders and last verification that the arrangement still works.",
         mechanism="periodic-manual", freshness="P180D", disc="auditor-only", prov=["credential_class", "custody_method", "holders", "verified_at"])
e7 = c.E(7, "AI provider dependency and fallback test record",
         "Inventory of engineering, operational and runtime functions that call external AI models, with the provider, model version, the defined non-AI or alternate-model fallback and the dated result of operating with the provider disabled.",
         mechanism="periodic-automated", freshness="P90D", disc="customer-only", prov=["function", "provider", "model_version", "fallback", "test_date", "result"])
e8 = c.E(8, "Alternate grant and payment processing drill record",
         "Evidence that a sponsor completed an urgent grant through its own bank channel while the platform was unavailable, that the OutOfBandPaymentRecorded reconciliation canceled the queued instruction, and that no duplicate payment occurred.",
         mechanism="periodic-manual", freshness="P1Y", disc="customer-only", prov=["drill_id", "sponsor", "grant_ref", "bank_txn_ref", "reconciliation_result"])
e9 = c.E(9, "Critical subprocessor continuity assessments",
         "Per critical subprocessor: assurance report type and period, bridge letter where needed, reviewed continuity commitments, concentration and substitution analysis, and exit plan.",
         mechanism="periodic-manual", freshness="P1Y", disc="nda", prov=["vendor", "report_type", "period_end", "reviewer", "review_date"])
e10 = c.E(10, "Customer exit package verification",
          "Signed exit manifest with SHA-256 digests, record counts and trial balances that the customer can independently verify, generated in a rehearsal at least annually.",
          mechanism="periodic-automated", freshness="P1Y", disc="customer-only", prov=["tenant", "export_watermark", "manifest_digest", "trial_balance_digest"], signing="Detached signature over manifest (mechanism not yet chosen)")
e11 = c.E(11, "Workforce disruption readiness check",
          "Record that every operational role can be performed remotely with managed devices, that no function depends on a single physical site, and that the minimum staffing table per function is current.",
          mechanism="periodic-manual", freshness="P1Y", disc="nda")

# ---------- Controls ----------
k1 = c.C(1, "Board-approved continuity policy with annual review", "Ensure continuity obligations are owned, scoped to all customer-facing services and reviewed at least annually and on material change.",
         "administrative", "L10-external-or-manual", ["Praxis (governed document and approval record)"], [e1], OWN,
         related=["UNB-CTRL-079", "UNB-CTRL-081", "SOC2-015"], fw=[R("SRC-ISO-22301-2019", "5.2"), R("SRC-NIST-SP800-53-R5", "CP-1")])
k2 = c.C(2, "BIA-derived recovery objectives gate", "Prevent a capability from being activated for a customer unless the BIA register contains its consequence profile, dependencies and approved recovery objectives.",
         "preventive-gate", "L5-build-release-gate", ["Unbound release gate (not built)", "Praxis"], [e2], OWN,
         related=["UNB-CTRL-079"], fw=[R("SRC-ISO-22301-2019", "8.2.2"), R("SRC-NIST-SP800-53-R5", "RA-9")],
         notes="UNB-RES-003 and RR-UNB-RES-003-r2 require objectives before architecture acceptance and production use.")
k3 = c.C(3, "Out-of-band continuity plan availability", "Keep current plans, contact trees and emergency procedures reachable when the production cloud account, email domain and identity provider are unavailable.",
         "preventive-procedural", "L10-external-or-manual", ["not yet assigned"], [e3], OWN, fw=[R("SRC-NIST-SP800-53-R5", "CP-2")])
k4 = c.C(4, "Scenario-based continuity exercise program", "Exercise plans at least annually against named scenarios, including correlated year-end surge with provider outage, and track findings to closure.",
         "detective-manual", "L8-adversarial-tested", ["not yet assigned"], [e4], OWN, related=["SOC2-015", "UNB-CTRL-080"],
         fw=[R("SRC-ISO-22301-2019", "8.5"), R("SRC-NIST-SP800-53-R5", "CP-4"), R("SRC-AICPA-TSC", "A1.3")])
k5 = c.C(5, "Key-person dependency elimination and portability testing", "Ensure no capability, credential or decision depends on one person by maintaining alternates and proving portability through exercises in which the primary does not participate.",
         "preventive-procedural", "L8-adversarial-tested", ["Praxis (repository operating system and provenance)"], [e5], OWN,
         related=["UNB-CTRL-081"], residual=["A small organization may not be able to staff qualified alternates for every capability; documentation portability is weaker than a trained alternate."])
k6 = c.C(6, "Dual-control custody of emergency credentials", "Ensure loss or incapacity of any single person cannot make root, registrar, signing or cloud-organization credentials unrecoverable, and no single person can use them alone.",
         "preventive-structural", "L3-restricted-interface", ["Identity provider and cloud organization (provider not selected)"], [e6], "Proposed: Security Lead (role not yet staffed)",
         policies=["SEC-CRYPTO-001"], related=["UNB-XIN-IAM-005"])
k7 = c.C(7, "Rules-first operation without AI providers", "Guarantee that money movement, authority, holds and records remain operable and correct when every external AI model is unavailable, by routing decisions through deterministic policy first and treating AI as advisory.",
         "preventive-structural", "L1-eliminated-in-scope", ["Unbound decision routing (not built)"], [e7], "Proposed: Unbound architecture owner",
         related=["REQ-X-017", "UNB-RES-001"], fw=[R("SRC-NIST-AI-RMF-1.0", rel="informed-by")],
         notes="Scope of elimination: authoritative financial and authority state changes. AI-assisted vetting throughput and engineering velocity are still degraded by a provider outage.")
k8 = c.C(8, "Sponsor-retained payment authority and out-of-band payment reconciliation", "Ensure a sponsor can always pay through its own bank channel and that out-of-band payments cancel matching queued instructions so no duplicate is sent after recovery.",
         "preventive-structural", "L2-type-system", ["Unbound payments component (not built)"], [e8], "Proposed: Unbound payments owner",
         related=["CNV-PLT-007", "CNV-PAY-001", "REQ-X-006"], fw=[R("SRC-NACHA-RULES", rel="informed-by")])
k9 = c.C(9, "Critical subprocessor continuity oversight", "Inventory critical subprocessors, review their assurance and continuity commitments annually, and maintain a tested substitution or exit path for each.",
         "administrative", "L10-external-or-manual", ["not yet assigned"], [e9], "Proposed: Vendor Risk Lead (role not yet staffed)",
         related=["UNB-CTRL-082", "UNB-CTRL-084", "SOC2-013", "RR-REQ-X-073-r2"], fw=[R("SRC-AICPA-TSC", "CC9.2"), R("SRC-FFIEC-BCM-BOOKLET", "Appendix J")])
k10 = c.C(10, "Verifiable customer exit package", "Allow each customer to take a complete, independently verifiable copy of its authoritative history at any time and on exit, reducing dependence on Echelon's continued existence.",
          "preventive-structural", "L7-property-tested", ["Unbound export component (not built)"], [e10], "Proposed: Unbound product owner",
          related=["RR-UNB-TEN-016-r1"])
k11 = c.C(11, "Location-independent workforce operation", "Ensure every operational role can be performed from any location on managed devices so that site loss or public-health restrictions do not stop operations.",
          "preventive-procedural", "L10-external-or-manual", ["not yet assigned"], [e11], OWN, fw=[R("SRC-FFIEC-BCM-BOOKLET", rel="informed-by")])

# ---------- Answer units ----------
STATUS_RAT = "No production service, no adopted continuity policy and no exercise records exist as of 2026-11-25 (architecture/ECHELON-CURRENT-STATE-BRIEF.md)."
a1 = c.A(1, "Business continuity management program and policy", "proposed-target-state", STATUS_RAT,
    "Echelon operates a business continuity management program aligned with ISO 22301 concepts. A board-approved policy covers every customer-facing service and the functions that support it, names an accountable executive, is reviewed at least annually and on material change, and its summary and change log are available to customers under NDA. Continuity evidence (BIA, plans, exercises, remediation) is generated in a governed repository with provenance so that customers can verify freshness rather than rely on an annual attestation.",
    "Not established. The business plan (13.06) states an intent to test recovery and record evidence; no continuity policy, owner or review record was located.",
    "Adopt a continuity policy before the first customer contract; record approvals in Praxis-governed repositories; publish a customer-facing summary.",
    "Nothing. Only planning text in the business plan and Unbound requirements UNB-GAP-028, UNB-OPS-001 and SOC2-015.",
    "Echelon has not yet adopted a business continuity policy. We plan to adopt one, aligned with ISO 22301 concepts, before any production customer goes live, and to share a summary under NDA.",
    "planned", [k1], [e1], OWN, freshness="P1Y", mechanism="periodic-manual", automation="partial", impl="low", rec="low",
    requirements=["UNB-GAP-028", "UNB-OPS-001", "SOC2-015"], oq=["Who is the accountable executive for continuity, and does a board or equivalent body exist to approve the policy?"])
a2 = c.A(2, "Business impact analysis and criticality", "proposed-target-state", STATUS_RAT,
    "Every capability has a BIA entry stating customer consequence over time (for example missed grant deadlines, unreceipted year-end contributions, blocked payroll-like disbursements to charities), maximum tolerable disruption, minimum acceptable service, and dependencies including cloud, identity, payment rails, custodians, charity data sources and AI model providers. Recovery objectives are derived from the BIA, and Echelon provides each financial customer with the information needed to classify Unbound in its own BIA and critical-vendor inventory.",
    "Not established. Unbound requirements call for per-capability failure modes (UNB-RES-001) and per-data-class recovery objectives (RR-UNB-RES-003-r2) but no BIA has been performed.",
    "Perform a BIA as part of architecture acceptance; gate capability activation on a reviewed BIA entry.",
    "Nothing beyond requirement text.",
    "A business impact analysis has not yet been performed. Our design requirements call for one per capability, and we plan to provide its results to customers for use in their own impact analyses.",
    "planned", [k2], [e2], OWN, freshness="P1Y", mechanism="periodic-manual", automation="partial", impl="low", rec="low",
    requirements=["UNB-RES-001", "UNB-RES-003", "RR-UNB-RES-003-r2"])
a3 = c.A(3, "Continuity plans, alternate communications and crisis notification", "proposed-target-state", STATUS_RAT,
    "Scenario plans exist for loss of people, technology, facilities and providers. Each plan names decision authority, customer and regulator-facing communication steps and alternate channels that do not depend on the production platform, its email domain or its identity provider. Current copies are held out of band and checked automatically for drift. Customers receive a designated contact list and the channels Echelon will use if its primary domain is compromised.",
    "Not established.",
    "Draft plans with the BIA; store a signed out-of-band copy; register alternate channels with each customer at onboarding.",
    "Nothing.",
    "Continuity plans have not yet been written. We plan scenario-based plans with alternate communication channels that work when our primary systems are unavailable.",
    "planned", [k3], [e3], OWN, freshness="P90D", mechanism="periodic-automated", automation="high", impl="low", rec="low",
    requirements=["ADM-040", "UNB-GAP-028"])
a4 = c.A(4, "Continuity exercises and testing", "proposed-target-state", STATUS_RAT,
    "Plans are exercised at least annually with scenario variety, including correlated conjunctions (year-end surge plus payment-provider outage plus custodian delay), and customers may observe or participate in a joint exercise annually. Each exercise produces a dated report with measured timings, findings and remediation closure evidence; summaries are shared under NDA.",
    "Not established. TVR-OPS-003 specifies a year-end readiness plan with conjunction drills; no drill has run.",
    "Run a first tabletop before production; add functional exercises once a production-like environment exists.",
    "Nothing.",
    "No continuity exercises have been conducted because no production service exists. We plan annual exercises, including joint exercises with customers who request them.",
    "planned", [k4], [e4], OWN, freshness="P1Y", mechanism="periodic-manual", automation="low", impl="low", rec="medium",
    requirements=["TVR-OPS-003", "SOC2-015", "UNB-ECO-005"])
a5 = c.A(5, "Key-person and founder dependence", "unknown",
    "Headcount, ownership and succession arrangements are not established in records reviewed. The business plan (11.09) treats founder dependence as a concentration risk to be decomposed, which indicates the dependence exists.",
    "No capability, credential or decision depends on a single individual. A key-person register lists each capability with a named alternate; emergency credentials are held under dual control or split custody; the codebase, requirements, decisions and operating procedures are in governed repositories with provenance so a qualified successor can operate and change the system; and portability is proven by exercises in which the primary does not participate. Contracts give customers a verifiable exit package and transition assistance if Echelon cannot continue.",
    "Unknown. The business plan identifies founder dependence as a risk and proposes capability decomposition and portability tests (11.09); no register, alternate or portability test was located.",
    "Build the key-person register at formation; place emergency credentials under dual control; run a portability test before the first production customer.",
    "Repositories under Praxis governance exist with provenance records, which supports knowledge portability, but no portability test has been run.",
    "Echelon is an early-stage organization and acknowledges key-person dependence as a material risk. We plan to document alternates, place critical credentials under dual control and test that others can operate the service before going live.",
    "planned", [k5, k6], [e5, e6], "Proposed: Chief Executive (role holder not established)", freshness="P180D", mechanism="periodic-manual",
    automation="partial", impl="medium", rec="medium",
    oq=["How many people can currently deploy, restore, and rotate credentials for Echelon systems?", "Is there a written succession arrangement for ownership and signing authority of Echelon Foundry, LLC?"],
    residual=["A very small team cannot fully eliminate key-person risk; customers may require escrow or contractual step-in rights as compensation."],
    challenge={
        "customer_intent": "Avoid losing a critical service because one person, typically the founder, becomes unavailable.",
        "adverse_outcome": "Service cannot be operated, repaired or recovered; credentials are lost; customer data or payment authority is stranded.",
        "conventional_control_effectiveness": "Conventional answers (key-person insurance, an org chart showing a deputy) provide money or names but not working capability; they rarely prove a successor can actually operate the system.",
        "legally_required": "No. Supervisory guidance (FFIEC, interagency TPRM) expects financial institutions to assess vendor concentration and viability; it does not impose staffing levels on the vendor.",
        "contractually_required": "Sometimes, as step-in rights, escrow, or transition assistance clauses in bank and enterprise contracts.",
        "historical_convention": "Buyers ask for headcount and backup staff because larger vendors could show them.",
        "architectural_elimination": "Partial. Governed repositories, reproducible builds, infrastructure as code and AI-agent-executable runbooks can make operational knowledge portable, and a customer-held exit package removes data-stranding risk.",
        "automatic_enforcement": "Dual-control credential custody can be enforced by the identity provider and cloud organization policy.",
        "continuous_evidence": "Praxis provenance shows who changed what; a periodic portability exercise produces dated evidence that an alternate succeeded.",
        "stronger_alternative": "Prove portability by exercise and give customers a verifiable exit package, instead of asserting headcount.",
        "alternative_verifiable": "Yes, through exercise reports and exit-package rehearsals the customer can verify.",
        "customer_acceptance_likelihood": "Uncertain. Bank procurement scores small vendors on headcount and financial viability regardless of portability evidence.",
        "invalidating_conditions": "If portability depends on AI agents that themselves depend on one person's accounts or one provider, or if documentation drifts from the running system.",
        "conventional_cost": "medium",
        "alternative_cost": "medium",
        "alternative_risks": "Documentation and agent runbooks may give false confidence if exercises are not realistic.",
        "supporting_arguments": ["Working capability is what the customer needs, not headcount.", "Exit packages address the worst outcome directly."],
        "opposing_arguments": ["A successor without tacit knowledge may still fail under incident pressure.", "Regulators and procurement officers may treat a single-founder vendor as unacceptable for critical services regardless of evidence."],
        "technical_effectiveness": "stronger", "institutional_acceptance": "uncertain"})
a6 = c.A(6, "Workforce disruption and pandemic readiness", "proposed-target-state", STATUS_RAT,
    "All operational roles can be performed remotely on managed devices with no dependency on a single office or data center under Echelon's control. The plan defines minimum staffing per function, absenteeism triggers and which non-essential work is suspended, and identifies the share of operational work performed by AI agents under human supervision, including what happens if supervising staff are unavailable.",
    "Not established. Echelon appears to have no physical facility dependency, but this is not documented.",
    "Document remote-operation and staffing thresholds with the continuity plan.",
    "Nothing.",
    "We have not yet documented a pandemic or workforce-disruption plan. We intend to operate without dependence on any single office.",
    "planned", [k11], [e11], OWN, mechanism="periodic-manual", automation="low", impl="low", rec="low")
a7 = c.A(7, "Dependence on AI providers for engineering, operations and runtime", "proposed-target-state",
    "Echelon intends AI agents to perform engineering and operations work and Unbound requirements route some decisions to AI (REQ-X-017); no dependency inventory or fallback test exists.",
    "AI is never in the authoritative path for money movement, authority, holds or records: deterministic policy evaluates first and AI is advisory, so a model-provider outage degrades throughput and convenience but not correctness. Each AI-dependent function has a named fallback (alternate model, human queue, or deferral) tested quarterly with the provider disabled. Engineering can continue at reduced velocity without AI agents because the codebase is conventional F#/.NET under human review. Model versions are pinned and provider deprecations are tracked as change events.",
    "Not established. Requirements REQ-X-017 (rules first, AI second, human third), UNB-RES-001 (model outage failure modes) and UNB-CTL-006 (correlated AI failures) describe the intended design.",
    "Inventory AI dependencies; implement rules-first routing; test with providers disabled.",
    "Nothing beyond requirement text.",
    "Our design keeps AI out of the authoritative path for payments and approvals so that an AI provider outage cannot cause incorrect financial actions. This is a design intent; it has not been built or tested.",
    "planned", [k7], [e7], "Proposed: Unbound architecture owner", freshness="P90D", mechanism="periodic-automated", automation="high", impl="medium", rec="low",
    requirements=["REQ-X-017", "UNB-RES-001", "UNB-CTL-006"],
    challenge={
        "customer_intent": "Ensure the vendor does not stop or behave wrongly when an AI provider fails, changes models, or changes terms.",
        "adverse_outcome": "Stalled grant vetting at year-end, unreviewable decisions, or engineering unable to ship a security fix.",
        "conventional_control_effectiveness": "Conventional vendor continuity reviews look at the AI provider's SOC report and uptime, which does not address model behavior change or deprecation.",
        "legally_required": "No statute requires it for Echelon. EU DORA requires EU financial entities to manage ICT concentration risk, which includes AI services they rely on indirectly.",
        "contractually_required": "Increasingly requested in AI addenda; not yet standard.",
        "historical_convention": "New concern; no settled convention.",
        "architectural_elimination": "Yes within scope: if authoritative state changes cannot depend on AI output, provider failure cannot corrupt financial state.",
        "automatic_enforcement": "Type-level separation of advisory AI outputs from authoritative commands can be enforced in F# domain types and tested.",
        "continuous_evidence": "Scheduled provider-disabled test runs produce dated results.",
        "stronger_alternative": "Architectural exclusion of AI from authority, plus tested fallbacks, rather than reliance on provider assurances.",
        "alternative_verifiable": "Partly: test results and code review can show it; customers cannot easily inspect the type boundary themselves.",
        "customer_acceptance_likelihood": "Likely, if evidence is offered.",
        "invalidating_conditions": "If AI-generated code changes reach production without human review, or if runtime vetting has no human capacity at peak.",
        "conventional_cost": "low", "alternative_cost": "medium",
        "alternative_risks": "Human fallback capacity for AI-assisted vetting may be insufficient at year-end volume.",
        "supporting_arguments": ["Correctness does not depend on a third party.", "Model churn becomes a throughput issue, not an integrity issue."],
        "opposing_arguments": ["Engineering velocity and incident response may in practice depend heavily on AI agents.", "Fallback capacity is unproven."],
        "technical_effectiveness": "stronger", "institutional_acceptance": "likely"})
a8 = c.A(8, "Alternate processing for grants and payments during platform outage", "proposed-target-state", STATUS_RAT,
    "The sponsor, not Unbound, originates payments, so the sponsor can always pay an urgent grant through its own bank channel. Unbound provides a documented alternate procedure, an offline read-only archive of fund balances and pending grants, and an OutOfBandPaymentRecorded command that, after recovery, cancels the matching queued instruction and registers the expected bank debit, so no duplicate payment is sent. Manual processing preserves the sponsor's dual approval and sanctions screening through a checklist, and replay of queued requests occurs only after reconciliation and revalidation.",
    "Not established. Requirements CNV-PAY-001, CNV-PLT-007 and REQ-X-006 specify the design.",
    "Implement the OutOfBandPaymentRecorded command and offline archive before payment features launch; drill annually with each sponsor.",
    "Nothing beyond requirement text.",
    "Unbound is designed so the sponsor keeps payment authority and can pay through its own bank during an outage, with recorded reconciliation afterwards. This has not been built or tested.",
    "planned", [k8], [e8], "Proposed: Unbound payments owner", freshness="P1Y", mechanism="periodic-manual", automation="partial", impl="medium", rec="low",
    requirements=["CNV-PAY-001", "CNV-PLT-007", "REQ-X-006", "ADM-040"],
    challenge={
        "customer_intent": "Keep urgent grants and disbursements flowing if the platform is down.",
        "adverse_outcome": "Charities miss funding; donors miss deadlines; duplicate payments occur after recovery.",
        "conventional_control_effectiveness": "Vendors usually promise faster recovery. Fast recovery does not help a sponsor during the outage and does not address duplicates after recovery.",
        "legally_required": "No for Echelon. FINRA Rule 4370 requires member firms to plan for customers' prompt access to funds; that applies to the customer if it is a member firm.",
        "contractually_required": "Common in bank contracts as alternate processing provisions.",
        "historical_convention": "Banks expect alternate processing sites for core processors.",
        "architectural_elimination": "Partly: because the sponsor originates payments (CNV-PAY-001), the platform is never the only path to pay.",
        "automatic_enforcement": "Duplicate prevention via idempotency keys and the out-of-band cancellation command.",
        "continuous_evidence": "Drill records and reconciliation results.",
        "stronger_alternative": "Sponsor-retained authority plus deterministic reconciliation instead of an alternate processing site.",
        "alternative_verifiable": "Yes, by drill.",
        "customer_acceptance_likelihood": "Uncertain; some sponsors lack staff to execute manual payments.",
        "invalidating_conditions": "If a sponsor has outsourced its bank operations entirely to the platform or lacks bank channel access.",
        "conventional_cost": "high", "alternative_cost": "low",
        "alternative_risks": "Manual processing may skip sanctions screening or dual approval unless checklists are followed.",
        "supporting_arguments": ["Removes the platform as a single point of failure for payments."],
        "opposing_arguments": ["Shifts operational burden to the customer during a crisis.", "Manual processes are where fraud tends to occur."],
        "technical_effectiveness": "stronger", "institutional_acceptance": "uncertain"})
a9 = c.A(9, "Subprocessor continuity and Echelon viability", "proposed-target-state", STATUS_RAT,
    "Critical subprocessors (cloud, managed PostgreSQL, payment connectivity, identity, AI providers) are inventoried with assurance reports, bridge letters and reviewed continuity commitments. If Echelon cannot continue, customers can take a verifiable exit package at any time, contracts provide transition assistance and notice, and source code escrow is available where a customer requires it.",
    "Not established. RR-REQ-X-073-r2 specifies a critical-vendor register and RR-UNB-TEN-016-r1 specifies the exit package; neither is implemented.",
    "Build the vendor register at provider selection; implement exit package before production; evaluate escrow providers.",
    "Nothing.",
    "No subprocessors have been selected for production. We plan to maintain a critical-vendor register and to provide customers with a verifiable exit package.",
    "planned", [k9, k10], [e9, e10], "Proposed: Vendor Risk Lead (role not yet staffed)", freshness="P1Y", mechanism="periodic-manual",
    automation="partial", impl="medium", rec="low", requirements=["RR-REQ-X-073-r2", "RR-UNB-TEN-016-r1", "SOC2-013"],
    challenge={
        "customer_intent": "Survive the vendor's failure or a subprocessor's failure without losing data or operations.",
        "adverse_outcome": "Customer cannot access records, statements or payment history after vendor insolvency.",
        "conventional_control_effectiveness": "Source code escrow is the conventional answer; release conditions are often litigated and the customer rarely has the skills to run released code.",
        "legally_required": "No. Supervisory guidance expects banks to plan for vendor failure.",
        "contractually_required": "Escrow is common in bank and public-sector contracts for critical software.",
        "historical_convention": "Escrow dates from on-premises licensed software.",
        "architectural_elimination": "Partly: a customer-held, independently verifiable data package removes data loss risk; it does not provide a running system.",
        "automatic_enforcement": "Scheduled exit-package generation.",
        "continuous_evidence": "Manifest digests and rehearsal results.",
        "stronger_alternative": "Continuous verifiable data portability plus documented successor-operator procedures.",
        "alternative_verifiable": "Yes.",
        "customer_acceptance_likelihood": "Uncertain; procurement checklists may still require escrow.",
        "invalidating_conditions": "If the export schema is not usable by any alternative platform within the customer's tolerance.",
        "conventional_cost": "medium", "alternative_cost": "medium",
        "alternative_risks": "Data without software may still leave the customer unable to operate for months.",
        "supporting_arguments": ["Customer controls its own records continuously."],
        "opposing_arguments": ["Escrow plus data provides more than data alone.", "Regulators may expect a named alternate provider."],
        "technical_effectiveness": "equivalent", "institutional_acceptance": "uncertain"})

FIN = ["banking", "financial-services", "wealth-management", "donor-advised-funds"]
# ---------- Questions ----------
c.Q(1, "BCM program governance", "Do you maintain a documented business continuity management program covering every service you provide to us, with a named accountable executive?",
    ["Is there a formal business continuity policy approved by senior management?", "Describe your BCM program, its scope and ownership."],
    "Customer needs assurance the vendor will keep critical services running through disruptions.", "Unplanned prolonged outage of a critical service with no coordinated response.",
    [R("SRC-ISO-22301-2019", "5.2"), R("SRC-NIST-SP800-53-R5", "CP-2"), R("SRC-FFIEC-BCM-BOOKLET"), R("SRC-SA-SIG"), R("SRC-CSA-CAIQ-V4"), UNB],
    "supervisory-guidance", "critical", industries=["all"], authority="FFIEC member agencies (for bank customers)", note=BIZ_NOTE)
c.Q(1, "BCM program governance", "How often is the continuity plan reviewed and re-approved, by whom, and when was it last approved?",
    ["Provide the date of the last BCP review and the approving body."],
    "Stale plans do not reflect current systems or staff.", "Plan fails in an event because it describes retired systems or departed people.",
    [R("SRC-FINRA-RULE-4370", "4370(b)", rel="informed-by"), R("SRC-ISO-22301-2019", "9.3"), R("SRC-NYDFS-PART-500", "500.16")],
    "contractual-common", "high", industries=FIN, authority="FINRA (binds member firms, not Echelon)",
    note="FINRA Rule 4370 requires member firms to review their own plans annually; firms commonly ask critical vendors for equivalent cadence.")
c.Q(1, "BCM certification", "Is your continuity program certified to ISO 22301, or assessed within a SOC 2 availability scope?",
    ["Do you hold an ISO 22301 certificate?", "Is availability included in your SOC 2 report?"],
    "Independent assurance reduces the customer's own testing burden.", "Customer relies on self-assertion for a critical dependency.",
    [R("SRC-ISO-22301-2019"), R("SRC-AICPA-TSC", "A1.2"), R("SRC-AICPA-SOC2-GUIDE")], "customer-preference", "medium",
    note="No certification or SOC report exists; see AUD category for assurance roadmap.")
c.Q(1, "BCM transparency", "Will you share your continuity plan, or a summary, and notify us of material changes to it during the contract term?",
    ["Can we review your BCP under NDA?"],
    "Customer must incorporate the vendor's plan in its own continuity planning.", "Customer plan relies on vendor capabilities that silently changed.",
    [R("SRC-INTERAGENCY-TPRM-2023"), R("SRC-EU-DORA", "Article 30"), R("SRC-FFIEC-BCM-BOOKLET", "Appendix J")],
    "contractual-common", "high", industries=FIN, juris=["US-federal", "EU"], authority="OCC, FDIC, Federal Reserve; EU competent authorities under DORA")
c.Q(2, "Business impact analysis", "Have you performed a business impact analysis that identifies critical functions, the maximum tolerable period of disruption for each, and the resources each depends on?",
    ["Describe your BIA methodology and when it was last performed."],
    "Recovery priorities must reflect real consequences.", "Recovery effort spent on low-value services while critical ones stay down.",
    [R("SRC-ISO-22301-2019", "8.2.2"), R("SRC-NIST-SP800-34-R1"), R("SRC-FFIEC-BCM-BOOKLET"), R("SRC-BCI-GPG"), UNB], "supervisory-guidance", "high",
    authority="FFIEC member agencies (for bank customers)")
c.Q(2, "Business impact analysis", "Does your impact analysis reflect our time-critical obligations, such as grant disbursement deadlines, year-end contribution acknowledgments, and statement delivery dates, rather than only your own revenue impact?",
    ["How do customer deadlines influence your recovery priorities?"],
    "Vendor BIAs often rank by vendor revenue rather than customer harm.", "Recovery ordering ignores a customer's regulatory or donor deadline.",
    [R("SRC-ISO-22301-2019", "8.2.2"), R("SRC-IRS-PUB-1771", rel="informed-by"), UNB], "customer-preference", "high",
    industries=["donor-advised-funds", "nonprofit"], products=["unbound"])
c.Q(2, "Dependency identification", "Does your impact analysis identify upstream dependencies, including cloud hosting, identity provider, payment connectivity, custodians, charity data sources and AI model providers, and the effect of each failing?",
    ["List the third parties whose failure would stop your service."],
    "Hidden dependencies cause surprise outages.", "Concentration on an unidentified fourth party.",
    [R("SRC-NIST-SP800-53-R5", "RA-9"), R("SRC-EU-DORA", "Article 28"), R("SRC-CSA-CCM-V4"), UNB], "supervisory-guidance", "high",
    juris=["US-federal", "EU"], products=["unbound"])
c.Q(2, "Customer BIA support", "Can you give us what we need to classify your service in our own impact analysis and critical-vendor inventory, including which of our functions would stop if you were unavailable?",
    ["Is your service a critical business constituent for our firm?", "Would you be considered a critical or significant third party?"],
    "Broker-dealers, banks and EU financial entities must assess critical vendors in their own plans.", "Customer misclassifies a critical dependency and is criticized in examination.",
    [D("SRC-FINRA-RULE-4370", "4370(c)(7)", rel="informed-by"), R("SRC-FFIEC-BCM-BOOKLET", "Appendix J"), R("SRC-EU-DORA", "Article 28"), R("SRC-INTERAGENCY-TPRM-2023")],
    "legal-regulatory", "high", industries=FIN, juris=["US-federal", "EU"], authority="FINRA; OCC, FDIC, Federal Reserve; EU competent authorities",
    note="The obligation binds the customer (member firm, bank, EU financial entity). It reaches Echelon only as an information request and contract terms; Echelon is not itself subject to Rule 4370.")
c.Q(3, "Continuity plans", "Do your continuity plans cover loss of key staff, loss of technology, loss of a work location and loss of a critical supplier, with named decision authority for each?",
    ["What disruption scenarios does your BCP address?"],
    "Plans that cover only technology fail in people or supplier events.", "No authority to make decisions during an event.",
    [R("SRC-ISO-22301-2019", "8.4"), R("SRC-NIST-SP800-34-R1"), R("SRC-DRII-PP"), R("SRC-SA-SIG")], "industry-convention", "high")
c.Q(3, "Alternate communications", "During a disruption, how will you communicate with us and with our staff if your primary platform, email domain or phone system is unavailable?",
    ["Describe alternate communication methods between your firm and customers during an emergency."],
    "Customers need status and instructions even when the vendor's main channels are down.", "Customer cannot learn of an outage or receive instructions.",
    [D("SRC-FINRA-RULE-4370", "4370(c)(4)", rel="informed-by"), R("SRC-NIST-SP800-53-R5", "CP-8"), R("SRC-NIST-SP800-53-R5", "CP-11")],
    "contractual-common", "high", industries=FIN, authority="FINRA (binds member firms)",
    note="Rule 4370 requires a member firm to plan alternate communications with its customers; firms ask vendors for matching channels.")
c.Q(3, "Crisis communications", "If your domain or email system is compromised during an incident, how will we verify that communications claiming to be from you are authentic?",
    ["How do customers authenticate emergency notices from you?"],
    "Attackers impersonate vendors during incidents to redirect payments.", "Fraudulent instructions accepted as vendor emergency notices.",
    [R("SRC-NIST-SP800-61-R3"), R("SRC-NACHA-RULES", rel="informed-by"), UNB], "customer-preference", "high", industries=FIN, products=["unbound"])
c.Q(3, "Plan availability", "Can your staff access the continuity plan, contact lists and runbooks if your cloud account, identity provider and document systems are all unavailable?",
    ["Where are offline copies of the BCP kept?"],
    "Plans stored only in the failed system are useless.", "Response delayed because plans are inaccessible.",
    [R("SRC-NIST-SP800-53-R5", "CP-2"), R("SRC-ISO-27031")], "industry-convention", "medium")
c.Q(4, "Continuity testing", "How often do you test your continuity plans, what kinds of tests do you run (tabletop, functional, full interruption), and when was the last test?",
    ["Provide the BCP test schedule and most recent test date."],
    "Untested plans fail.", "Plan assumptions invalid at the moment of need.",
    [R("SRC-ISO-22301-2019", "8.5"), R("SRC-NIST-SP800-53-R5", "CP-4"), R("SRC-AICPA-TSC", "A1.3"), R("SRC-FFIEC-BCM-BOOKLET"), R("SRC-NYDFS-PART-500", "500.16")],
    "supervisory-guidance", "critical", industries=FIN, authority="FFIEC member agencies; NYDFS (for covered entities)")
c.Q(4, "Joint exercises", "Will you participate in our continuity exercises, or allow us to observe yours, at least annually?",
    ["Do you conduct joint BCP testing with clients?"],
    "Banks are expected to test with critical service providers.", "Integration between customer and vendor plans never validated.",
    [R("SRC-FFIEC-BCM-BOOKLET"), R("SRC-EU-DORA", "Article 30"), R("SRC-INTERAGENCY-TPRM-2023")], "supervisory-guidance", "high",
    industries=FIN, juris=["US-federal", "EU"], authority="FFIEC member agencies; EU competent authorities under DORA")
c.Q(4, "Test results", "What did your last continuity test find, how were the findings remediated, and can you share the results?",
    ["Provide a summary of BCP test results and corrective actions."],
    "Test results show whether the plan works and whether the vendor fixes gaps.", "Recurring failures hidden behind a claim that testing occurred.",
    [R("SRC-AICPA-TSC", "A1.3"), R("SRC-ISO-22301-2019", "10.1")], "contractual-common", "high", disc="nda")
c.Q(4, "Correlated scenarios", "Do your exercises include correlated scenarios, for example a year-end giving surge coinciding with a payment-provider or custodian outage, rather than single isolated failures?",
    ["Have you exercised simultaneous failures during your peak period?"],
    "Real disruptions cluster at peak periods.", "Plan works for single failures but collapses under concurrent stress.",
    [R("SRC-BCI-GPG"), UNB], "customer-preference", "medium", industries=["donor-advised-funds", "nonprofit", "wealth-management"], products=["unbound"])
c.Q(5, "Key-person dependence", "Which of your functions, decisions or systems depend on a single individual, including the founder, and what is the alternate for each?",
    ["Identify any key-person dependencies.", "What is your bus factor for production operations?"],
    "Small vendors can fail when one person is unavailable.", "Service stops or cannot be repaired after loss of one person.",
    [R("SRC-FFIEC-BCM-BOOKLET"), R("SRC-INTERAGENCY-TPRM-2023"), BP], "supervisory-guidance", "critical", products=["echelon-organization", "unbound"])
c.Q(5, "Founder succession", "If your founder were permanently unavailable tomorrow, who would hold legal authority, system access and technical knowledge to operate and change the service, and is this documented?",
    ["Describe your succession plan for executive leadership."],
    "Founder-led vendors carry concentrated authority and knowledge.", "No one can legally or technically act for the vendor.",
    [R("SRC-INTERAGENCY-TPRM-2023"), R("SRC-TPRM-COMMUNITY-BANK-GUIDE-2024"), BP], "supervisory-guidance", "critical",
    products=["echelon-organization"], oq=["Does the operating agreement of Echelon Foundry, LLC provide for successor management?"])
c.Q(5, "Emergency credential custody", "How are root cloud credentials, domain registrar access, code-signing keys and similar emergency credentials protected against both loss of the single holder and misuse by a single holder?",
    ["Are break-glass credentials escrowed or held under dual control?"],
    "Lost credentials can make recovery impossible; single-holder credentials enable insider abuse.", "Permanent lockout or unilateral destructive action.",
    [R("SRC-NIST-SP800-53-R5", "AC-2"), R("SRC-CIS-CONTROLS-V8.1"), SCS], "industry-convention", "high", disc="nda")
c.Q(5, "Knowledge portability", "Could a qualified third party operate, maintain and recover your service using only your documentation, repositories and runbooks, and have you tested that?",
    ["Is operational knowledge documented sufficiently for a successor to operate the system?"],
    "Tacit knowledge in one person's head is a continuity risk.", "Documented procedures that do not actually work for a newcomer.",
    [R("SRC-ISO-22301-2019", "7.5"), BP], "customer-preference", "medium", products=["echelon-organization", "unbound"])
c.Q(6, "Pandemic and workforce disruption", "Does your plan address extended workforce absence, such as a pandemic, including absenteeism thresholds, minimum staffing per function and which work you would suspend?",
    ["Describe your pandemic preparedness plan."],
    "Workforce loss is a distinct scenario from technology loss.", "Critical functions unstaffed during a public-health event.",
    [R("SRC-FFIEC-BCM-BOOKLET"), R("SRC-ISO-22301-2019", "8.4")], "supervisory-guidance", "medium", industries=FIN)
c.Q(6, "Remote operation", "Can every operational and support role be performed remotely and securely, and does any function depend on a specific office or on-premises equipment?",
    ["Are there any single-site dependencies in your operations?"],
    "Site loss should not stop service.", "Office closure halts operations.",
    [R("SRC-FINRA-RULE-4370", "4370(c)(6)", rel="informed-by"), R("SRC-NIST-SP800-53-R5", "CP-7")], "industry-convention", "medium")
c.Q(7, "AI-performed operations", "Where AI agents perform engineering or operations tasks for you, how would you continue those functions if the agent tooling were unavailable, and do your staff retain the skills to do the work themselves?",
    ["What happens to your operations if your AI coding or operations tools stop working?"],
    "Vendors increasingly depend on AI agents for core work.", "Inability to patch, deploy or respond to incidents without AI tools.",
    [R("SRC-NIST-AI-RMF-1.0", rel="informed-by"), R("SRC-NIST-AI-600-1", rel="informed-by"), R("SRC-NIST-SP800-218A", rel="informed-by")], "customer-preference", "high",
    products=["all-echelon-products"])
c.Q(7, "AI provider outage", "What happens to the service if your primary AI model provider has an extended outage, retires the model you use, or changes its terms so you can no longer use it?",
    ["Describe your contingency for loss of your AI vendor.", "Is there a fallback model or provider?"],
    "AI provider concentration is a new third-party risk.", "Features stop or behave differently without notice.",
    [R("SRC-EU-DORA", "Article 28"), R("SRC-NIST-AI-RMF-1.0", rel="informed-by"), R("SRC-CSA-AICM", rel="informed-by"), UNB], "customer-preference", "high",
    juris=["US-federal", "EU"], products=["unbound"])
c.Q(7, "Runtime AI fallback", "Which customer-facing functions, such as grant vetting, support responses or document drafting, call a third-party AI service at runtime, and what is the non-AI fallback for each?",
    ["Can the service operate with AI features turned off?"],
    "Customer needs to know which functions degrade during an AI outage.", "Grant processing halts at peak because vetting depends on an unavailable model.",
    [R("SRC-OWASP-LLM-TOP10-2025", rel="informed-by"), R("SRC-NIST-AI-600-1", rel="informed-by"), UNB], "customer-preference", "high",
    industries=["donor-advised-funds", "nonprofit", "financial-services"], products=["unbound"])
c.Q(8, "Alternate grant processing", "If your platform is unavailable, how can we continue to approve and disburse urgent grants, and what records or tools will we have to do so?",
    ["What manual workaround exists if the system is down?", "Describe alternate processing arrangements."],
    "Charities and donors depend on timely grants.", "Disbursements stop during an outage.",
    [R("SRC-FFIEC-BCM-BOOKLET"), R("SRC-NIST-SP800-53-R5", "CP-7"), UNB], "supervisory-guidance", "critical",
    industries=["donor-advised-funds", "nonprofit", "banking"], products=["unbound"])
c.Q(8, "Post-outage reconciliation", "After an outage, how are payments we made manually reconciled back into the platform so that queued instructions are not also sent, producing duplicate payments?",
    ["How do you prevent duplicate disbursements after recovery?"],
    "Manual workarounds create double-payment risk at recovery.", "Duplicate payments to charities, possibly unrecoverable.",
    [R("SRC-NACHA-RULES", rel="informed-by"), R("SRC-UCC-4A", rel="informed-by"), UNB], "customer-preference", "critical",
    industries=["donor-advised-funds", "banking"], products=["unbound"])
c.Q(8, "Controls during manual processing", "When grants are processed outside the platform during an outage, how are sanctions screening, dual approval and charity eligibility checks still performed and evidenced?",
    ["Are compliance controls maintained during contingency operations?"],
    "Controls are most often bypassed during emergencies.", "Payment to a sanctioned party or ineligible organization during contingency processing.",
    [R("SRC-OFAC-COMPLIANCE-FRAMEWORK", rel="informed-by"), R("SRC-IRC-4966", rel="informed-by"), R("SRC-NIST-SP800-53-R5", "CP-13")], "legal-regulatory", "critical",
    industries=["donor-advised-funds"], products=["unbound"], authority="OFAC; IRS",
    note="Sanctions and taxable-distribution rules bind the sponsor, not Echelon; Unbound's role is to supply the checklist and evidence capture.")
c.Q(9, "Subprocessor continuity", "Which of your subprocessors are critical to delivering the service, and how do you assess and monitor their continuity and recovery capabilities?",
    ["Do you review the BCP or SOC reports of your critical vendors?"],
    "A vendor is only as resilient as its critical suppliers.", "Fourth-party failure causes customer outage.",
    [R("SRC-AICPA-TSC", "CC9.2"), R("SRC-FFIEC-BCM-BOOKLET", "Appendix J"), R("SRC-INTERAGENCY-TPRM-2023"), R("SRC-ISO-27036")], "supervisory-guidance", "high",
    industries=FIN, authority="FFIEC member agencies")
c.Q(9, "Vendor viability", "If your company ceases operations, is acquired or becomes insolvent, what ensures we can continue, for example source code escrow, a data exit package or transition assistance?",
    ["Do you offer software escrow?", "What happens to our data if you go out of business?"],
    "Early-stage vendors carry elevated failure risk.", "Customer loses access to records and cannot operate.",
    [R("SRC-SOFTWARE-ESCROW-PRACTICE"), R("SRC-EU-DORA", "Article 28"), R("SRC-INTERAGENCY-TPRM-2023"), UNB], "contractual-common", "critical",
    juris=["US-federal", "EU"], products=["echelon-organization", "unbound"])
c.Q(9, "Subprocessor change notice", "Will you notify us in advance when you replace or add a critical subprocessor in a way that changes your continuity or recovery capability?",
    ["Do you provide notice of changes to critical suppliers?"],
    "Customer's assessment depends on the vendor's supply chain.", "Silent substitution of a weaker provider.",
    [R("SRC-EU-DORA", "Article 30"), R("SRC-GDPR", "Art. 28", rel="informed-by")], "contractual-common", "medium", juris=["US-federal", "EU"])
c.Q(6, "Supervision of AI agents during staff absence", "If the people who supervise your AI agents are unavailable, for example during a pandemic, do the agents stop, continue under reduced authority, or continue unchanged?",
    ["Are autonomous agents permitted to operate without human oversight during staffing shortages?"],
    "Agents may be relied on as substitute capacity exactly when oversight is weakest.", "Unsupervised agents take consequential actions during a workforce disruption.",
    [R("SRC-NIST-AI-RMF-1.0", rel="informed-by"), R("SRC-OWASP-AGENTIC-AI", rel="informed-by"), SOC2D], "customer-preference", "medium", products=["all-echelon-products"])
c.write()
