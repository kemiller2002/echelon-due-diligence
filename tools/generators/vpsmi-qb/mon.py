from common import *

def build():
    c = Cat("MON")
    NA = "not yet assigned"
    e1 = c.evr(1, "Security event catalog and coverage report",
               "Versioned catalog of security event types (authentication, authorization denials, privilege and role changes, data reads and exports, configuration changes, administrative and break-glass actions, database-level activity, agent actions) mapped to emitting components, with automated coverage tests proving each event is emitted with required fields.",
               NA, "event-driven-automated", "per-event", prov=["event type", "emitting component", "schema version", "test id", "release hash"])
    e2 = c.evr(2, "Log integrity verification results",
               "Periodic verification of hash chains or signed checkpoints over authoritative audit history and security logs, detecting omitted, altered, duplicated or reordered records, including after restore.",
               NA, "periodic-automated", "P1D", signing="Proposed: signed checkpoints anchored outside the production trust domain",
               notes="UNB-DATA-012 leaves the mechanism (hash chain, signed checkpoint or other) as a design decision to be benchmarked.")
    e3 = c.evr(3, "Log retention and legal hold configuration evidence",
               "Effective retention settings per log class and tenant, legal holds, and deletion or redaction events for personal data, generated from the storage configuration.",
               NA, "periodic-automated", "P30D", disclosure="nda")
    e4 = c.evr(4, "Alert and response metrics",
               "Alerts by severity with time to acknowledge and time to contain, after-hours handling, escalation records and protective actions taken.",
               NA, "continuous-automated", "P1D", disclosure="nda")
    e5 = c.evr(5, "Detection catalog and detection test results",
               "Versioned detection rules mapped to MITRE ATT&CK techniques and domain abuse cases, with seeded-event test results showing each detection fires, and false positive rates.",
               NA, "periodic-automated", "P30D", disclosure="nda")
    e6 = c.evr(6, "Tenant audit trail export",
               "Customer-accessible export or stream of tenant-scoped audit events, including Echelon personnel and break-glass actions, with integrity proofs that the customer can verify independently.",
               NA, "continuous-automated", "P1D", disclosure="customer-only")
    e7 = c.evr(7, "Missing heartbeat and evidence completeness record",
               "Expected-evidence schedule reconciled against received logs and control heartbeats; every missing or late source raises a preserved deficiency, and zero-activity periods carry independently validated zero-activity evidence.",
               NA, "continuous-automated", "PT1H",
               notes="Specified in unbound@9b38de47:architecture/CONTINUOUS-CONTROL-MONITORING-AND-EVIDENCE-ASSURANCE.md (Missing evidence algorithm); not implemented.")
    e8 = c.evr(8, "AI agent activity ledger",
               "Per agent action: agent identity, model and version, authorizing human or policy, task id, tool invoked, parameters (redacted per classification), resource, result, denial events and kill-switch events.",
               "Praxis (records agent provenance for repository work; runtime agent ledger for Unbound not built)", "continuous-automated", "per-event", disclosure="nda")
    e9 = c.evr(9, "Time synchronization status",
               "Clock offset measurements per log-producing host or service against authoritative time sources, with alerts on drift beyond tolerance.",
               NA, "continuous-automated", "P1D", disclosure="internal")
    e10 = c.evr(10, "Privileged and break-glass session records",
                "Break-glass activations with two-person approval, session records, tenant administrator notifications and post-session review outcomes; CI and deployment pipeline change records.",
                NA, "event-driven-automated", "per-event", disclosure="customer-only")

    k1 = c.ctl(1, "Mandatory structured security event emission",
               "Governed APIs, Strata persistence, agent runtimes and infrastructure emit catalog-defined security events with actor, authority, action, resource, decision, result, correlation id and policy version; missing emission fails tests.",
               "detective-automated", "L5-build-release-gate", [NA], [e1], related=["SOC2-002", "SOC2-012", "GOV-AUTH-012", "UNB-CTRL-073"],
               fw=[D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-012", "derived-from"), R("SRC-NIST-SP800-53-R5", "AU-2"), R("SRC-NIST-SP800-53-R5", "AU-3"), R("SRC-CSA-CCM-V4", "LOG-07")], cwe=["CWE-778"])
    k2 = c.ctl(2, "Append-only, independently verifiable audit history",
               "Audit and security logs are append-only below the application layer, stored in a separate trust domain, protected from Echelon administrators, and verified by hash chains or signed checkpoints.",
               "preventive-structural", "L3-restricted-interface", [NA, "Strata (candidate persistence; tamper-evidence capabilities not verified)"], [e2],
               related=["SOC2-006", "UNB-DATA-008", "UNB-DATA-012", "UNB-IMM-007", "UNB-CTRL-074"],
               fw=[R("SRC-NIST-SP800-53-R5", "AU-9"), R("SRC-NIST-SP800-53-R5", "AU-9(2)"), R("SRC-NIST-SP800-53-R5", "AU-9(3)"), R("SRC-CSA-CCM-V4", "LOG-09")])
    k3 = c.ctl(3, "Privacy-aware logging and classified retention",
               "Secrets, credentials, full account numbers and unnecessary personal data are excluded at emission by typed log schemas; retention is set per log class with legal hold and lawful deletion support.",
               "preventive-structural", "L2-type-system", [NA], [e3], related=["SOC2-003", "SOC2-023", "SOC2-032"], cwe=["CWE-532"],
               fw=[R("SRC-NIST-SP800-53-R5", "AU-11"), D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-003", "derived-from")])
    k4 = c.ctl(4, "Centralized analysis, alerting and protective response",
               "Security events flow to a central analysis platform; high-severity alerts page an on-call responder at any hour and can trigger pre-approved protective actions (account disablement, payment hold under CNV-PLT-007).",
               "detective-automated", "L9-runtime-monitored", [NA], [e4], related=["SOC2-012", "CNV-PLT-007", "UNB-CTRL-075"],
               fw=[R("SRC-NIST-SP800-53-R5", "SI-4"), R("SRC-CIS-CONTROLS-V8.1", "8.9"), R("SRC-NIST-CSF-2.0", "DE.CM-09")])
    k5 = c.ctl(5, "Tested detection engineering",
               "Detections are versioned code mapped to threats, tested with seeded events on every change and periodically, with false positive rates tracked.",
               "detective-automated", "L7-property-tested", [NA], [e5], related=["UNB-XIN-ECO-016"],
               fw=[R("SRC-MITRE-ATTACK"), R("SRC-NIST-CSF-2.0", "DE.AE-02")])
    k6 = c.ctl(6, "Tenant-scoped customer audit trail with independent verification",
               "Customers can view, export and stream their tenant's audit events, including Echelon personnel and break-glass actions, with integrity proofs verifiable outside Echelon systems.",
               "detective-automated", "L3-restricted-interface", [NA, "Folio (candidate for audit package rendering)"], [e6], related=["SOC2-009", "UNB-XIN-IAM-005"],
               fw=[D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-009", "derived-from")])
    k7 = c.ctl(7, "Missing-evidence and heartbeat detection",
               "An independent expectation engine raises a monitored deficiency for any missing or late log source or control heartbeat; monitoring failure is a degraded-assurance incident with defined fail-closed behavior for consequential actions.",
               "detective-automated", "L9-runtime-monitored", [NA], [e7], related=["SOC2-027", "SOC2-005"],
               fw=[D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-027", "derived-from"), R("SRC-NIST-SP800-53-R5", "AU-5"), R("SRC-PCI-DSS-4.0.1", "Req 10.7.2", rel="informed-by")])
    k8 = c.ctl(8, "Attributable AI agent activity logging and scope enforcement",
               "Every agent action is logged with agent identity and authorizing principal; out-of-scope tool calls are denied, logged and alerted; agents can be interrupted.",
               "detective-automated", "L9-runtime-monitored", ["Praxis (repository provenance only)", NA], [e8], related=["SOC2-017", "UNB-CTRL-066"],
               fw=[D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-017", "derived-from"), R("SRC-OWASP-AGENTIC-AI"), R("SRC-NIST-AI-600-1")])
    k9 = c.ctl(9, "Authoritative time synchronization with drift alerting",
               "All log-producing components synchronize to authoritative time sources; offsets are measured and alerted; records carry occurredAt and recordedAt in UTC.",
               "detective-automated", "L9-runtime-monitored", [NA], [e9],
               fw=[R("SRC-NIST-SP800-53-R5", "AU-8"), R("SRC-NIST-SP800-53-R5", "SC-45"), R("SRC-CSA-CCM-V4", "LOG-06"), R("SRC-CIS-CONTROLS-V8.1", "8.4")])
    k10 = c.ctl(10, "Privileged, break-glass and pipeline activity monitoring",
                "Break-glass uses sealed credentials with two-person activation, auto-expiry, paging and tenant notification; privileged sessions and CI or deployment configuration changes are recorded and reviewed.",
                "detective-automated", "L9-runtime-monitored", [NA], [e10], related=["UNB-XIN-IAM-005", "CNV-PLT-010"],
                fw=[D("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-005", "derived-from"), R("SRC-SLSA")])

    ch_tamper = challenge(
        customer_intent="Audit trails that an insider or attacker cannot quietly alter.",
        adverse_outcome="Fraud or intrusion concealed by log modification.",
        conventional_control_effectiveness="Conventional answers cite access restrictions and WORM storage; these protect storage but rarely prove completeness, and administrators of the logging platform can often still delete or omit records.",
        legally_required="Not for Echelon directly. SEC Rule 17a-4 imposes non-rewriteable or audit-trail recordkeeping on broker-dealers for required records, which can flow to a vendor that holds them.",
        contractually_required="Frequently requested as log protection.",
        historical_convention="Restricted access plus immutable storage tier.",
        architectural_elimination="Append-only history below the application API (UNB-DATA-008), with corrections as linked new records, removes the update path entirely within scope.",
        automatic_enforcement="Database permissions that deny update and delete on authoritative history to every application and administrative role.",
        continuous_evidence="Hash chain or signed checkpoint verification detecting omission, alteration, duplication and reordering (UNB-DATA-012), verifiable by the customer.",
        stronger_alternative="Structural append-only history plus customer-verifiable integrity proofs anchored outside Echelon's trust domain.",
        alternative_verifiable="Yes, by design; the customer or auditor can recompute proofs.",
        customer_acceptance_likelihood="Likely, once explained; it exceeds the conventional answer.",
        invalidating_conditions="Strata or PostgreSQL configuration permitting superuser rewrite without detection; checkpoints anchored in the same trust domain.",
        conventional_cost="low", alternative_cost="medium",
        alternative_risks="Append-only storage conflicts with lawful deletion of personal data unless redaction or crypto-shredding is designed in (SOC2-032).",
        supporting_arguments=["Unbound requirements already direct this design."],
        opposing_arguments=["Mechanism is unbenchmarked; Strata capabilities are unverified."],
        technical_effectiveness="stronger", institutional_acceptance="likely")
    ch_soc = challenge(
        customer_intent="Someone will notice and act on an attack at any hour.",
        adverse_outcome="Overnight or weekend attack proceeds undetected until business hours.",
        conventional_control_effectiveness="A staffed 24x7 SOC is effective but costly; small vendors claiming 24x7 coverage often mean an unstaffed alert email.",
        legally_required="No law reviewed requires a vendor to staff 24x7 monitoring.",
        contractually_required="Sometimes asked by banks; usually as a question rather than a contractual term.",
        historical_convention="24x7 SOC or MDR provider.",
        architectural_elimination="Fail-closed holds on consequential operations (CNV-PLT-007) and automatic protective actions limit damage when no human is awake.",
        automatic_enforcement="Pre-approved automated containment on high-confidence signals (freeze payments for a tenant, disable account, revoke agent credential).",
        continuous_evidence="Alert-to-action timing records.",
        stronger_alternative="Automated protective actions plus paging on-call with documented response time, optionally an MDR provider for infrastructure telemetry.",
        alternative_verifiable="Yes, through alert and action timing metrics and tabletop results.",
        customer_acceptance_likelihood="Uncertain: banks may still expect named 24x7 coverage.",
        invalidating_conditions="Single on-call person; automated actions with high false positive rates disrupting sponsor operations.",
        conventional_cost="high", alternative_cost="medium",
        alternative_risks="Automated holds could disrupt time-sensitive grants; must follow sponsor-adopted hold policy.",
        supporting_arguments=["Automated containment acts in seconds; humans in minutes to hours."],
        opposing_arguments=["Key-person dependency in a very small organization.", "MDR adds a subprocessor with data access."],
        technical_effectiveness="equivalent", institutional_acceptance="uncertain")
    ch_hb = challenge(
        customer_intent="Know that monitoring itself is working.",
        adverse_outcome="Silent monitoring failure interpreted as no incidents.",
        conventional_control_effectiveness="Most programs monitor for bad events, not for absence of expected events; disabled logging often goes unnoticed.",
        legally_required="No.", contractually_required="Rarely asked.",
        historical_convention="Source health dashboards reviewed manually.",
        architectural_elimination="Not applicable.", automatic_enforcement="Expectation engine raises deficiencies automatically.",
        continuous_evidence="Evidence completeness ratio with raw denominators.",
        stronger_alternative="Computed assurance from expected evidence, as specified in the Unbound continuous control monitoring architecture.",
        alternative_verifiable="Yes.", customer_acceptance_likelihood="Likely; it is additive.",
        invalidating_conditions="Expectation engine shares failure modes with the monitored pipeline.",
        conventional_cost="low", alternative_cost="medium",
        alternative_risks="Alert noise from late but harmless evidence.",
        supporting_arguments=["Treats absence of evidence as a finding rather than as health."],
        opposing_arguments=["Engineering cost before any production workload exists."],
        technical_effectiveness="stronger", institutional_acceptance="likely")

    a1 = c.au(1, "Security event logging scope and content", "proposed-target-state",
              "SOC2-012 and SOC2-002 direct monitoring scope and event content; GOV-AUTH-012 requires tamper-evident logging of authority decisions; none implemented.",
              "Unbound emits a versioned catalog of security events covering authentication, MFA changes, authorization denials, privilege and role changes, reads and exports of sensitive data, configuration and integration changes, administrative and break-glass actions, database-level activity outside the application and AI agent actions. Each record carries actor, authority used, action, resource, decision, result, occurredAt and recordedAt, correlation id and policy version. Automated tests prove every catalog event is emitted.",
              "Not established; no production system. Aegis provides fault capture with redaction for .NET applications, which is operational fault handling, not security event logging.",
              "Implement the event catalog in Unbound's governed APIs and persistence layer.", "Nothing.",
              "Unbound's security logging is designed but not implemented; we can share the designed event scope.", "planned", [k1], [e1],
              requirements=["SOC2-002", "SOC2-012", "GOV-AUTH-012"], mechanism="event-driven-automated", automation="full", impl="medium", rec="low")
    a2 = c.au(2, "Log integrity and tamper evidence", "proposed-target-state",
              "SOC2-006, UNB-DATA-008, UNB-DATA-012 and UNB-IMM-007 require append-only history, tamper-evident digests and independent verification; mechanism unbenchmarked and Strata capabilities unverified.",
              "Authoritative audit history is append-only below the application API; update and delete are denied to all application, administrator and agent roles; logs are stored in a separate trust domain; hash chains or signed checkpoints are verified daily and after any restore; customers and auditors can verify exported trails independently; access to logs is itself logged.",
              "Not established.", "Benchmark the integrity mechanism and verify Strata and PostgreSQL permission model.", "Nothing.",
              "Tamper-evident, append-only audit history is a design requirement for Unbound; it is not yet implemented or verified.",
              "planned", [k2], [e2], requirements=["SOC2-006", "UNB-DATA-008", "UNB-DATA-012", "UNB-IMM-007"], freshness="P1D",
              mechanism="periodic-automated", automation="full", impl="medium", rec="low", challenge=ch_tamper)
    a3 = c.au(3, "Log retention and privacy-aware logging", "proposed-target-state",
              "SOC2-003 prohibits secrets and unnecessary sensitive data in logs; SOC2-023 forbids inventing universal retention periods without auditor and counsel input; REQ-X-036 sets seven-year minimum retention for financial documents but not security logs.",
              "Security logs are retained at least 12 months online-searchable and longer in archive per a counsel-approved schedule by log class, with tenant-specific extension and legal hold; typed log schemas exclude secrets and restrict personal data at emission; personal data in append-only logs is handled by field-level redaction or key destruction so lawful deletion is possible.",
              "Not established.", "Set retention schedule with counsel and auditor (SOC2-023).", "Nothing.",
              "Log retention periods have not yet been set; they will be defined with counsel and auditors.", "not-available", [k3], [e3],
              requirements=["SOC2-003", "SOC2-023", "SOC2-032"], mechanism="periodic-automated", automation="high", impl="low", rec="medium",
              oq=["What retention period will apply to security logs, and does any customer regulation (for example Rule 17a-4 or Rule 204-2) require longer retention of records held in Unbound?"])
    a4 = c.au(4, "SIEM, alerting, after-hours coverage and response", "unknown",
              "No monitoring platform, on-call arrangement or MDR provider is identified. Vigila, which the Standard proposed for runtime monitoring, is a task organizer, not a monitoring system.",
              "Security events are centralized in an analysis platform with correlation across API, agent, persistence and cloud control plane sources; high-severity alerts page an on-call responder 24x7 with a 15-minute acknowledgment target; pre-approved automated protective actions (account disablement, agent credential revocation, tenant payment hold under the sponsor-adopted hold policy) execute on high-confidence signals; detection and response times are measured and reported.",
              "Unknown; no evidence located.", "Select a monitoring platform and staffing model before production.", "Nothing.",
              "Echelon has not yet selected a security monitoring platform or established after-hours coverage.", "not-available", [k4], [e4],
              requirements=["SOC2-012", "CNV-PLT-007"], mechanism="continuous-automated", automation="partial", impl="medium", rec="high", challenge=ch_soc,
              oq=["Will Echelon use an MDR provider, and would it be a subprocessor with access to customer data?", "Who provides after-hours coverage given current organization size?"])
    a5 = c.au(5, "Detection engineering", "proposed-target-state",
              "UNB-XIN-ECO-016 references detection coverage and seeded-control test pass rate as counter-metrics; TVR-SEC-008 requires matching of IdP admin actions and custody movements; no detection catalog exists.",
              "Detections are maintained as versioned code mapped to MITRE ATT&CK and to domain abuse cases (payee change followed by disbursement request, unusual grant velocity, bulk export, cross-tenant probing, account takeover indicators, agent scope violations); each detection is tested with seeded events on change and monthly; false positive rates are tracked.",
              "Not established.", "Build the detection catalog alongside the event catalog.", "Nothing.",
              "Detection engineering is planned; not yet operating.", "planned", [k5], [e5], requirements=["UNB-XIN-ECO-016", "TVR-SEC-008"],
              mechanism="periodic-automated", automation="high", impl="medium", rec="medium")
    a6 = c.au(6, "Customer administrator audit trail", "proposed-target-state",
              "SOC2-009 requires auditor-ready evidence export with chain of custody; UNB-XIN-IAM-005 requires notifying tenant administrators of break-glass within 1 hour; no customer audit UI exists.",
              "Customer administrators can view, search, export and stream (near real time, in a documented JSON schema) all audit events for their tenant, including actions by Echelon personnel, support and break-glass sessions; tenant-visible logs are retained for the contract term plus an agreed period and are exportable at termination; integrity proofs let the customer verify completeness independently; events are tenant-scoped so no tenant can see another's events.",
              "Not established.", "Implement with the event catalog and tenant isolation model.", "Nothing.",
              "A customer-visible audit trail is part of Unbound's design; it is not yet implemented.", "planned", [k6, k10], [e6, e10],
              requirements=["SOC2-009", "UNB-XIN-IAM-005"], mechanism="continuous-automated", automation="full", impl="medium", rec="low")
    a7 = c.au(7, "Missing heartbeat and log pipeline failure detection", "proposed-target-state",
              "SOC2-027 requires that a missing expected log or heartbeat create a monitored control exception, and the continuous control monitoring architecture specifies a missing-evidence algorithm and treats monitoring failure as a degraded-assurance incident; specified, not implemented.",
              "An independent expectation engine schedules expected evidence by control, source and period; missing or late sources raise preserved deficiencies within one hour; monitoring failure is a degraded-assurance incident; consequential grant and payment actions follow sponsor-approved fail-closed or manual-continuity policies while safety-critical monitoring is down; zero activity requires validated zero-activity evidence.",
              "Not established.", "Implement per the continuous control monitoring architecture.", "Nothing.",
              "Detection of missing logs and heartbeats is specified for Unbound; not implemented.", "planned", [k7], [e7],
              requirements=["SOC2-027", "SOC2-005"], freshness="PT1H", mechanism="continuous-automated", automation="full", impl="medium", rec="low", challenge=ch_hb)
    a8 = c.au(8, "AI agent activity logging and scope monitoring", "partially-implemented",
              "For repository engineering work, Praxis records agent provenance (actor kind, provider, model, runtime, reason) in execution records, as seen in this repository's AGENTS.md front matter; this is tooling evidence, not a runtime control for a production service. SOC2-017 requires runtime agents to be attributable, bounded, monitored and interruptible; not implemented for Unbound.",
              "Every AI agent action in engineering and operations is attributable to a distinct agent identity, model and version, authorizing human or policy, and task; tool invocations and results are logged with classification-based redaction of prompts and outputs; out-of-scope actions are denied, logged and alerted, and agents can be interrupted with a kill switch.",
              "Praxis records agent provenance for repository changes in Echelon repositories. No runtime agent activity logging exists for Unbound.",
              "Extend to Unbound runtime agents per SOC2-017.",
              "Praxis execution and provenance records in Echelon repositories (first-party, not independently verified).",
              "For engineering work in its repositories, Echelon records which AI agent made a change and why; runtime agent activity logging for Unbound is planned, not implemented.",
              "qualified-current-fact", [k8], [e8], independence="first-party", requirements=["SOC2-017"], mechanism="event-driven-automated", automation="full", impl="medium", rec="low",
              residual=["Prompt and output logging can capture sensitive data; redaction depends on correct classification."])
    a9 = c.au(9, "Time synchronization", "proposed-target-state",
              "The Unbound evidence envelope requires occurredAt and recordedAt; no infrastructure exists to synchronize.",
              "All components synchronize to the hosting provider's authoritative time service; offsets are monitored and alert beyond 100 ms; records use UTC with millisecond precision and carry both occurredAt and recordedAt.",
              "Not established.", "Configure with hosting selection.", "Nothing.", "Time synchronization is planned with infrastructure selection.", "planned", [k9], [e9],
              mechanism="continuous-automated", automation="full", impl="low", rec="none")
    a10 = c.au(10, "Privileged, break-glass and pipeline monitoring", "proposed-target-state",
               "UNB-XIN-IAM-005 specifies sealed break-glass credentials, two-person activation, 4-hour expiry, security owner paging and tenant notification within 1 hour; CNV-PLT-010 requires two approvers and signed builds for control-relevant modules; not implemented.",
               "Break-glass and privileged production access are recorded at session level, page the security owner, notify affected tenant administrators within 1 hour and are reviewed after each use; changes to CI workflows, deploy credentials and signing keys are alerted and reviewed.",
               "Not established.", "Implement with identity platform selection.", "Nothing.", "Break-glass and privileged access monitoring is specified for Unbound; not implemented.",
               "planned", [k10], [e10], requirements=["UNB-XIN-IAM-005", "CNV-PLT-010"], mechanism="event-driven-automated", automation="high", impl="medium", rec="low")

    I_FIN = ["financial-services", "banking", "wealth-management", "donor-advised-funds"]
    c.q(1, "event-scope", "Which security events does the service log: authentication successes and failures, MFA changes, authorization denials, privilege changes, data exports, configuration changes and administrative actions?",
        "Detectability and investigability of misuse.", "Undetected compromise and inability to investigate.",
        [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-012", "derived-from"), R("SRC-NIST-SP800-53-R5", "AU-2"), R("SRC-AICPA-TSC", "CC7.2"), R("SRC-CSA-CCM-V4", "LOG-07"), R("SRC-ISO-27002-2022", "8.15"), R("SRC-SA-SIG")],
        "industry-convention", "critical", alts=["Describe your security logging.", "What events are captured in application audit logs?"])
    c.q(1, "event-content", "Does every security log record include actor identity, role or authority used, action, resource, result, timestamp, source and a correlation identifier?",
        "Attribution and reconstruction.", "Ambiguous logs that cannot support investigation.", [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-002", "derived-from"), R("SRC-NIST-SP800-53-R5", "AU-3"), R("SRC-CSA-CCM-V4", "LOG-08")], "industry-convention", "high")
    c.q(1, "data-access", "Are reads of sensitive records, such as a staff member viewing a donor's profile or exporting a report, logged, not only changes?",
        "Insider misuse detection and privacy accountability.", "Undetected snooping or data theft.", [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-012"), R("SRC-INTERAGENCY-GLBA-SAFEGUARDS")], "customer-preference", "high", ind=I_FIN)
    c.q(1, "authorization-denials", "Are denied requests and failed authorization checks logged in enough detail to detect probing across tenants?",
        "Early warning of attacks on isolation.", "Undetected cross-tenant probing.", [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-012"), R("SRC-OWASP-API-TOP10-2023", "API1:2023")], "customer-preference", "high")
    c.q(1, "configuration", "Are changes to security configuration, roles, policies, feature flags and integrations logged with the identity of the approver?",
        "Accountability for control changes.", "Unauthorized weakening of controls.", [D("SRC-ECH-UNB-BASELINE", "GOV-AUTH-012", "derived-from"), R("SRC-AICPA-TSC", "CC8.1")], "industry-convention", "medium")
    c.q(1, "database-activity", "Do you log database activity that bypasses the application, such as direct administrator queries, migrations and privilege grants?",
        "Coverage of privileged back-end access.", "Direct data manipulation without trace.", [D("SRC-ECH-UNB-BASELINE", "UNB-DATA-008"), R("SRC-PCI-DSS-4.0.1", "Req 10.2.1", rel="informed-by")], "customer-preference", "high", ind=I_FIN)
    c.q(2, "integrity", "How are security and audit logs protected from modification or deletion, including by your own administrators?",
        "Trustworthy audit trail.", "Concealment of fraud or intrusion.", [R("SRC-NIST-SP800-53-R5", "AU-9"), R("SRC-CSA-CCM-V4", "LOG-09"), R("SRC-PCI-DSS-4.0.1", "Req 10.3.2", rel="informed-by"), D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-006")],
        "industry-convention", "critical", alts=["Are logs immutable?", "How do you ensure the integrity of audit logs?"])
    c.q(2, "tamper-evidence", "Can you detect deletion, alteration, reordering or truncation of log records, for example through hash chaining or signed checkpoints, and how often is integrity verified?",
        "Provable completeness.", "Undetected log tampering.", [D("SRC-ECH-UNB-BASELINE", "UNB-DATA-012", "derived-from"), R("SRC-NIST-SP800-53-R5", "AU-9(3)")], "customer-preference", "high")
    c.q(2, "segregation", "Are logs stored in a separate account or trust domain from the production systems that generate them?",
        "Survival of logs after compromise.", "Attacker deleting logs with production credentials.", [R("SRC-NIST-SP800-53-R5", "AU-9(2)")], "industry-convention", "medium")
    c.q(2, "log-access", "Who can access raw security logs, and is access to the logs itself logged and reviewed?",
        "Confidentiality and accountability of log data.", "Misuse of log contents.", [R("SRC-CSA-CCM-V4", "LOG-04"), R("SRC-NIST-SP800-53-R5", "AU-9(4)")], "industry-convention", "medium")
    c.q(2, "independent-verification", "Can we or our auditors verify the integrity of an exported audit trail independently of your systems?",
        "Independent verifiability.", "Dependence on vendor assertions.", [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-009"), D("SRC-ECH-UNB-BASELINE", "UNB-IMM-007")], "customer-preference", "medium", ind=I_FIN)
    c.q(3, "retention", "How long are security logs retained online and in archive, and can retention be extended for our tenant or for a legal hold?",
        "Investigation and regulatory lookback.", "Evidence lost before an incident is discovered.", [R("SRC-NIST-SP800-53-R5", "AU-11"), R("SRC-CIS-CONTROLS-V8.1", "8.10"), R("SRC-PCI-DSS-4.0.1", "Req 10.5.1", rel="informed-by"), D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-023")],
        "industry-convention", "high", alts=["What is your log retention period?"])
    c.q(3, "recordkeeping", "If we are a broker-dealer or investment adviser, can audit records relevant to our books-and-records obligations be retained in a compliant form and for the required period?",
        "Customer recordkeeping compliance.", "Regulatory recordkeeping violations.", [R("SRC-SEC-17A-4"), R("SRC-SEC-ADVISERS-BOOKS-RECORDS")], "legal-regulatory", "medium",
        ind=["financial-services", "wealth-management"], jur=["US-federal"], reg="SEC; FINRA",
        note="The obligation is the customer's; it flows to the vendor only where the vendor holds required records on the customer's behalf.")
    c.q(3, "privacy", "How do you prevent secrets, credentials, full account numbers and unnecessary personal data from being written to logs?",
        "Logs do not become a breach vector.", "Sensitive data exposure through logs.", [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-003", "derived-from"), R("SRC-MITRE-CWE", "CWE-532")], "industry-convention", "high")
    c.q(3, "privacy", "How are personal data in append-only logs handled when retention expires or a lawful deletion request applies?",
        "Privacy law compliance.", "Retention conflicts with deletion rights.", [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-032"), R("SRC-GDPR", "Art. 17"), R("SRC-CCPA-CPRA")], "legal-regulatory", "medium", jur=["EU", "US-state:CA", "US-states"],
        note="Applies where privacy law grants deletion rights to data subjects whose data appears in logs; GLBA-covered data may be exempt under some state laws.")
    c.q(4, "siem", "Are security logs centralized into a SIEM or equivalent analysis platform, and which sources feed it?",
        "Correlated detection.", "Fragmented visibility.", [R("SRC-CIS-CONTROLS-V8.1", "8.9"), R("SRC-NIST-SP800-53-R5", "SI-4"), R("SRC-CSA-CCM-V4", "LOG-05")], "industry-convention", "high")
    c.q(4, "coverage-hours", "Is security monitoring staffed 24x7, and if not, how are high-severity alerts handled outside business hours?",
        "Timely response at any hour.", "Attacks proceeding overnight or on weekends.", [R("SRC-AICPA-TSC", "CC7.3"), R("SRC-SA-SIG")], "customer-preference", "high", ind=I_FIN)
    c.q(4, "mdr", "Do you use a managed detection and response provider, what does it cover, and does it have access to customer data?",
        "Outsourced monitoring scope and fourth-party risk.", "Gaps or data exposure via the provider.", [R("SRC-INTERAGENCY-TPRM-2023"), R("SRC-ISO-27036")], "customer-preference", "medium")
    c.q(4, "metrics", "What are your mean time to detect and mean time to acknowledge for high-severity alerts, and can you share the measurements?",
        "Effectiveness evidence.", "Slow detection.", [R("SRC-CSA-CCM-V4", "SEF-05")], "customer-preference", "medium", disc="nda")
    c.q(4, "response-authority", "Are alerts routed to people or automations with authority to act, for example to freeze payments or disable accounts, and what protective actions are automatic?",
        "Containment speed for financial abuse.", "Losses while alerts wait for authority.", [D("SRC-ECH-UNB-BASELINE", "CNV-PLT-007"), R("SRC-NACHA-FRAUD-MONITORING-2026", rel="informed-by")], "customer-preference", "high", ind=["donor-advised-funds", "financial-services", "wealth-management"])
    c.q(4, "cloud-control-plane", "Do you monitor cloud control plane activity and alert on high-risk changes such as disabled logging, new access keys or public storage exposure?",
        "Infrastructure-level detection.", "Silent infrastructure compromise.", [R("SRC-CIS-BENCHMARKS"), R("SRC-NIST-CSF-2.0", "DE.CM-09")], "industry-convention", "high")
    c.q(5, "detection-engineering", "How are detection rules developed, versioned, tested and retired, and is there a catalog of detections mapped to threats?",
        "Mature, maintainable detection.", "Ad hoc rules with unknown coverage.", [R("SRC-MITRE-ATTACK"), R("SRC-NIST-CSF-2.0", "DE.AE-02")], "customer-preference", "medium", jur=["global"])
    c.q(5, "detection-testing", "Do you verify that detections actually fire, for example with simulated attacks or seeded events, and how often?",
        "Proven detection.", "Broken detections giving false comfort.", [D("SRC-ECH-UNB-BASELINE", "UNB-XIN-ECO-016"), R("SRC-MITRE-ATTACK")], "customer-preference", "medium")
    c.q(5, "domain-detection", "Do you have detections for financial-domain abuse, such as unusual grant patterns, a payee change followed by a disbursement request, or bulk exports by one user?",
        "Fraud and insider abuse detection.", "Fraudulent grants or data theft.", [D("SRC-ECH-UNB-BASELINE", "TVR-SEC-008", "informed-by"), R("SRC-NACHA-FRAUD-MONITORING-2026", rel="informed-by")], "customer-preference", "high",
        ind=["donor-advised-funds", "financial-services", "wealth-management"])
    c.q(5, "account-takeover", "How do you detect takeover of donor, advisor or customer administrator accounts?",
        "Account takeover detection.", "Fraud through hijacked accounts.", [R("SRC-FFIEC-AUTH-GUIDANCE-2021"), R("SRC-SEC-REG-S-ID", rel="informed-by")], "supervisory-guidance", "high", ind=I_FIN)
    c.q(5, "alert-quality", "How do you manage false positive rates so that alert fatigue does not hide real incidents?",
        "Signal quality.", "Missed alerts amid noise.", [R("SRC-NIST-CSF-2.0", "DE.AE-02")], "customer-preference", "low")
    c.q(6, "customer-audit-trail", "Can our administrators see a complete audit trail of actions taken by our own users in our tenant?",
        "Customer-side oversight.", "Customer unable to investigate its own users.", [R("SRC-CSA-CCM-V4", "LOG-11"), R("SRC-EDUCAUSE-HECVAT")], "contractual-common", "high",
        alts=["Is an audit log available to customer administrators?"])
    c.q(6, "vendor-access-visibility", "Will the audit trail show actions taken by your personnel and support staff in our tenant, including break-glass access?",
        "Visibility of vendor access.", "Undisclosed vendor access to customer data.", [D("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-005", "derived-from"), R("SRC-ISO-27018")], "customer-preference", "critical", ind=I_FIN)
    c.q(6, "export", "Can we export audit logs or stream them to our own SIEM in near real time, and in what format?",
        "Integration with customer monitoring.", "Siloed vendor logs.", [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-009")], "customer-preference", "medium")
    c.q(6, "retention-for-customer", "How long are tenant-visible audit logs available to us, and are they available to us after contract termination?",
        "Long-term evidence access.", "Loss of evidence at exit.", [R("SRC-NIST-SP800-53-R5", "AU-11")], "contractual-common", "medium")
    c.q(6, "tenant-scoping", "Are audit records scoped so that one tenant can never see another tenant's events, including in logs given to support staff?",
        "Isolation of audit data.", "Cross-tenant disclosure via logs.", [R("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-014"), R("SRC-ISO-27017")], "customer-preference", "high")
    c.q(7, "heartbeat", "How do you detect that a log source, agent or monitoring pipeline has stopped sending data?",
        "Monitoring reliability.", "Silent monitoring gaps.", [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-027", "derived-from"), R("SRC-NIST-SP800-53-R5", "AU-5"), R("SRC-PCI-DSS-4.0.1", "Req 10.7.2", rel="informed-by")], "industry-convention", "high")
    c.q(7, "degraded-mode", "Is a monitoring outage treated as a security incident or degraded state, and what happens to high-risk operations while monitoring is unavailable?",
        "Safe behavior under monitoring failure.", "Fraud during monitoring outages.", [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-027"), D("SRC-ECH-UNB-BASELINE", "CNV-PLT-007", "informed-by")], "customer-preference", "medium", ind=I_FIN)
    c.q(7, "absence-of-evidence", "How do you distinguish \"no events occurred\" from \"events were not collected\" for controls that report only exceptions?",
        "Valid negative evidence.", "Absence of alarms mistaken for control success.", [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-005"), D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-027")], "customer-preference", "medium")
    c.q(8, "ai-agent-attribution", "Are actions performed by AI agents in engineering and operations attributable to a specific agent identity, the human or policy that authorized it, and the task?",
        "Accountability for AI agent actions.", "Unattributable changes and actions.", [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-017", "derived-from"), R("SRC-OWASP-AGENTIC-AI"), R("SRC-NIST-AI-600-1")], "customer-preference", "high", jur=["global"])
    c.q(8, "ai-agent-logging", "Do you log AI agent tool invocations, prompts and outputs for security review, and how do you keep sensitive customer data out of those logs?",
        "Reviewability of agent behavior without new leakage.", "Undetected agent misuse or log-based data exposure.", [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-003"), R("SRC-OWASP-LLM-TOP10-2025", "LLM02:2025")], "customer-preference", "high", jur=["global"])
    c.q(8, "ai-agent-scope", "Can you detect an AI agent acting outside its authorized scope, such as accessing production data, changing permissions or disabling controls, and is it stopped automatically?",
        "Bounded agent authority.", "Excessive agency causing harm.", [R("SRC-OWASP-LLM-TOP10-2025", "LLM06:2025"), D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-017")], "customer-preference", "high", jur=["global"])
    c.q(9, "time-sync", "Are all systems that generate security logs synchronized to authoritative time sources, and how is clock drift detected?",
        "Reliable event sequencing.", "Unreconstructable timelines.", [R("SRC-NIST-SP800-53-R5", "AU-8"), R("SRC-CSA-CCM-V4", "LOG-06"), R("SRC-CIS-CONTROLS-V8.1", "8.4"), R("SRC-ISO-27002-2022", "8.17"), R("SRC-PCI-DSS-4.0.1", "Req 10.6.1", rel="informed-by")],
        "industry-convention", "medium")
    c.q(9, "timestamps", "Do log records use a consistent time zone and precision, and do they record both when an event occurred and when it was recorded?",
        "Accurate forensic timelines.", "Misordered or ambiguous events.", [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-002", "informed-by")], "customer-preference", "low")
    c.q(10, "privileged-monitoring", "How are privileged sessions and break-glass access monitored, and who reviews them afterward?",
        "Oversight of the most powerful access.", "Abuse of privileged access.", [D("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-005", "derived-from"), R("SRC-CSA-CCM-V4", "LOG-12")], "industry-convention", "high")
    c.q(10, "privileged-monitoring", "Is production access by your engineers and contractors recorded at the command or session level?",
        "Reconstructing privileged actions.", "Untraceable administrative actions.", [R("SRC-NIST-SP800-53-R5", "AU-12"), R("SRC-NYDFS-PART-500", "500.6")], "customer-preference", "medium", ind=I_FIN)
    c.q(10, "pipeline-monitoring", "Do you monitor the build and deployment pipeline for unauthorized changes, such as altered workflows, new deploy credentials or unsigned artifacts?",
        "Supply-chain attack detection.", "Malicious code deployed through a compromised pipeline.", [R("SRC-SLSA"), D("SRC-ECH-UNB-BASELINE", "CNV-PLT-010")], "customer-preference", "medium")
    return c
