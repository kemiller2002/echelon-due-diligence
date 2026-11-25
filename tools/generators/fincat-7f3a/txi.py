from lib import *

CAT = "TXI"
OWNER = "Not assigned; proposed: Unbound platform architecture owner (role not staffed)"
DEF = dict(owner=OWNER, industries=["donor-advised-funds", "financial-services", "banking", "wealth-management"],
           juris=["US-federal"], authority="none")

U = "SRC-ECH-UNB-BASELINE"
TSC = "SRC-AICPA-TSC"
SCS = "SRC-ECH-SCS-0.1"
CWE = "SRC-MITRE-CWE"
N53 = "SRC-NIST-SP800-53-R5"
ASVS = "SRC-OWASP-ASVS"

aus = [
dict(
 title="Idempotent commands and postings keyed on stable business identifiers",
 target=("Every mutating Unbound command and every posting is idempotent on a stable business key, not a transport retry ID: "
         "for example GrantId plus installment, PaymentIntentId, or ScheduleId plus occurrence (UNB-XIN-EVA-005, UNB-RCN-GRT-004). "
         "Posting is idempotent per source event ID and accounting book, so at most one original journal exists per pair whatever "
         "the posting-rule version (RR-ACC-MDL-007-r1). Each external observation type has a registered key derived from source "
         "data (an ACH return is keyed on original trace, return reason code and return trace); a repeat with the same key and "
         "payload hash is acknowledged with no effect, while the same key with a different hash is not applied and opens a "
         "DuplicateKeyConflict case. Fee runs are idempotent per fund, schedule, period and segment set (RR-ADM-028-r1). Keys are "
         "enforced by database unique constraints in the same transaction as the effect, so a race between duplicates cannot "
         "produce two effects."),
 intended="Implement an idempotency key registry per command and observation type with unique constraints and payload hashes; contract tests replay every command.",
 prov_refs="ACC-MDL-007, RR-ACC-MDL-007-r1, UNB-XIN-EVA-005, UNB-API-004, UNB-API-STD-001, UNB-RCN-GRT-004, RR-ADM-028-r1",
 statement="Planned: Unbound's commands and postings are specified to be idempotent on stable business keys enforced by database constraints. Not implemented or tested.",
 controls=["ECTL-TXI-001"], evidence=["EVR-TXI-001"], policies=["SEC-DATA-001"],
 requirements=["ACC-MDL-007", "RR-ACC-MDL-007-r1", "UNB-XIN-EVA-005", "UNB-API-004", "UNB-API-STD-001", "UNB-RCN-GRT-004", "RR-ADM-028-r1", "UNB-GRANT-029"],
 impl_cost="medium", rec_cost="low",
 questions=[
  Q("How does the platform prevent a transaction from being processed twice if a user double-submits or a client retries after a timeout?",
    "idempotency", "Duplicate processing causes duplicate grants or payments.", "Double disbursement or double posting.",
    [D(U), S(TSC, "PI1.3"), S(CWE, "CWE-837")], "customer-preference", "critical",
    alts=["Do your APIs support idempotency keys?", "How are duplicate transactions prevented?"]),
  Q("Are idempotency keys based on business identifiers or on technical request identifiers, and why does that matter for duplicate prevention?",
    "idempotency", "Transport retry IDs do not catch business-level duplicates.", "Duplicates that arrive through different channels or sessions.",
    [D(U)], "customer-preference", "high", reqs=["UNB-XIN-EVA-005", "UNB-GRANT-029"]),
  Q("What happens when the same idempotency key is received again with different content?",
    "idempotency", "Key reuse with different payloads indicates error or attack.", "Silent overwrite or silent drop of a different transaction.",
    [D(U), S(CWE, "CWE-345")], "customer-preference", "high", reqs=["UNB-XIN-EVA-005"]),
  Q("How do you ensure that inbound files and notifications from banks or custodians are applied only once even if they are delivered repeatedly?",
    "idempotency", "Banks and custodians resend files.", "Duplicate posting of returns, receipts or positions.",
    [D(U), S(TSC, "PI1.2")], "customer-preference", "high", reqs=["UNB-XIN-EVA-005", "UNB-KNOW-027", "UNB-CUST-009"]),
  Q("Is accounting posting idempotent, so that reprocessing an event can never create a second journal for it?",
    "idempotency", "Posting duplicates misstate balances.", "Duplicate journals after recovery.",
    [D(U)], "customer-preference", "high", reqs=["ACC-MDL-007", "RR-ACC-MDL-007-r1"]),
  Q("For recurring grants and scheduled runs, how do you ensure each occurrence is executed exactly once even if the scheduler fails and restarts?",
    "idempotency", "Schedulers misfire under failure.", "Missed or duplicated recurring grants.",
    [D(U)], "customer-preference", "medium", reqs=["UNB-RCN-GRT-004", "UNB-XIN-EVA-007", "UNB-WF-005"]),
 ]),
dict(
 title="External effects: exactly-once internally, at most one live attempt externally",
 target=("Unbound does not claim exactly-once execution at external providers; no local guarantee is represented as provider "
         "exactly-once (REQ-X-019). Internally, state changes and the outbound message that will cause an external effect commit "
         "in the same transaction through a durable outbox, consumers are idempotent and ordering is per subject (UNB-EVT-002). "
         "Every external effect has a durable issuance receipt and external idempotency key so retries, recovery and replay cannot "
         "repeat payments, grants, trades, notices or filings (UNB-IMM-006, UNB-DATA-009, UNB-RES-002). Process managers issue "
         "commands with stable keys and never hold locks across external calls (UNB-XIN-EVA-007). A payment rail is eligible only "
         "if the provider contractually supports idempotent submission and status query (TVR-PAY-002); where a rail lacks an "
         "end-to-end key (noted for ACH), reconciliation and the unknown-outcome protocol close the gap. The guarantee offered is "
         "at most one live attempt per grant under any failure (TVR-PAY-001)."),
 intended="Implement the transactional outbox and effect-receipt store; select providers only with idempotent submission and status query.",
 prov_refs="REQ-X-019, UNB-EVT-002, UNB-IMM-006, UNB-DATA-009, UNB-RES-002, UNB-XIN-EVA-007, TVR-PAY-001, TVR-PAY-002",
 statement="Planned: Unbound is specified to prevent duplicate external effects through a transactional outbox, effect receipts and provider idempotency; it explicitly does not claim exactly-once execution at banks. Not implemented.",
 controls=["ECTL-TXI-002", "ECTL-TXI-001"], evidence=["EVR-TXI-002", "EVR-TXI-001"],
 requirements=["REQ-X-019", "UNB-EVT-002", "UNB-IMM-006", "UNB-DATA-009", "UNB-RES-002", "UNB-XIN-EVA-007", "TVR-PAY-001", "TVR-PAY-002", "UNB-CTL-004"],
 impl_cost="medium", rec_cost="low",
 residual=["Provider-side duplicates remain possible where the rail lacks end-to-end idempotency; detection relies on reconciliation."],
 open_questions=["Which candidate payment providers contractually support idempotent submission and status query (TVR-PAY-002 is blocked on external evidence)?"],
 challenge=dict(
  customer_intent="Never pay a grant twice or lose one.",
  adverse_outcome="Duplicate or lost disbursements.",
  conventional_control_effectiveness="Vendors often assert 'exactly-once processing', which is not achievable across independent external systems and can mislead.",
  legally_required="No.", contractually_required="Customers sometimes ask for an exactly-once guarantee in contracts.",
  historical_convention="Batch files with duplicate-file checks at the bank.",
  architectural_elimination="Within Unbound, duplicate effects from replay and recovery are eliminated because replay has no path to external adapters and effects require a receipt-backed outbox item.",
  automatic_enforcement="Unique effect keys and receipts; provider idempotency where offered.",
  continuous_evidence="Effect receipts reconciled to bank and provider statements (UNB-EVT-006).",
  stronger_alternative="An honest at-most-one-live-attempt guarantee plus mandatory reconciliation before any retry, rather than an exactly-once claim.",
  alternative_verifiable="Yes, through crash-injection tests and settlement reconciliation.",
  customer_acceptance_likelihood="Likely once explained; some procurement checklists literally ask for 'exactly-once'.",
  invalidating_conditions="Rails or providers without status query; staff originating payments outside the platform (addressed by TVR-PAY-004).",
  conventional_cost="Low to claim; high when duplicates occur.", alternative_cost="Medium engineering and operational reconciliation cost.",
  alternative_risks="Unknown outcomes need human resolution and delay some payments.",
  supporting_arguments=["Honest about distributed-system limits.", "Duplicates are prevented by construction internally and detected externally."],
  opposing_arguments=["A checklist reviewer may mark anything other than 'exactly-once: yes' as a deficiency."],
  technical_effectiveness="stronger", institutional_acceptance="likely"),
 questions=[
  Q("Do you guarantee exactly-once processing of payments and other external transactions, and how?",
    "exactly-once", "Customer wants no duplicates and no losses.", "Duplicate or lost disbursements.",
    [D(U), S(TSC, "PI1.3")], "customer-preference", "critical", alts=["Is your payment processing exactly-once?"]),
  Q("How do you ensure that a database update and the corresponding message to an external system either both happen or neither happens?",
    "outbox", "Dual-write failures create inconsistency.", "State says paid but no instruction sent, or the reverse.",
    [D(U)], "customer-preference", "high", reqs=["UNB-EVT-002", "UNB-XIN-EVA-007", "UNB-XIN-EVA-016"]),
  Q("After a crash or failover, how do you avoid resending payment instructions, emails, acknowledgments or filings that were already sent?",
    "recovery", "Recovery is when duplicates happen.", "Duplicate external effects after recovery.",
    [D(U)], "customer-preference", "critical", reqs=["UNB-IMM-006", "UNB-RES-002", "UNB-DATA-009"]),
  Q("Do you require your payment and banking providers to support idempotent submission and status queries, and what do you do when a rail cannot?",
    "provider-idempotency", "Vendor's duplicate prevention depends on its providers.", "Duplicates at the provider.",
    [D(U), S("SRC-INTERAGENCY-TPRM-2023")], "customer-preference", "high", reqs=["TVR-PAY-002", "RR-UNB-PAY-008-r1", "CNV-PLT-012"]),
  Q("How does each external effect get reconciled back to the authorized decision that caused it?",
    "effect-reconciliation", "Every money movement must trace to authority.", "Unexplained external effects.",
    [D(U), S(TSC, "PI1.4")], "customer-preference", "high", reqs=["UNB-EVT-006", "UNB-CTL-004", "UNB-PAY-010"]),
 ]),
dict(
 title="Atomic approval, reservation and journal commit",
 target=("Routine grant approval and the currency reservation against net capacity commit atomically in one transaction, so two "
         "simultaneous grants that together exceed capacity cannot both succeed and a failed grant has neither approval nor "
         "reservation (REQ-X-002, CNV-FIN-001). Every domain fact with a financial effect carries the journal batch or "
         "reservation ID committed in the same database transaction, and balances are computed only from insert-only journal "
         "and reservation tables (UNB-XIN-EVA-001). Deadline-bearing obligations are persisted in the same transaction as the "
         "state change that creates them (UNB-XIN-WFA-001). A batch such as a payment file or recurring-grant run is only a "
         "container: each item commits in its own transaction with its own key, and a batch ends PartiallyCompleted with per-item "
         "outcomes rather than all-or-nothing ambiguity (UNB-XIN-EVA-011)."),
 intended="Keep the authoritative ledger and facts in one PostgreSQL cluster per the architecture so atomicity is a local transaction property, not a distributed protocol (CNV-ARC-001).",
 prov_refs="REQ-X-002, CNV-FIN-001, UNB-XIN-EVA-001, UNB-XIN-WFA-001, UNB-XIN-EVA-011, CNV-ARC-001",
 statement="Planned: grant approval, reservation and related journal entries are specified to commit atomically in one database transaction. Not implemented or tested.",
 controls=["ECTL-TXI-003"], evidence=["EVR-TXI-003"],
 requirements=["REQ-X-002", "CNV-FIN-001", "UNB-XIN-EVA-001", "UNB-XIN-WFA-001", "UNB-XIN-EVA-011", "CNV-ARC-001", "UNB-XIN-EVA-013"],
 impl_cost="medium", rec_cost="low",
 questions=[
  Q("When a transaction updates several records (for example a grant approval, a fund reservation and a journal entry), are all updates committed atomically?",
    "atomicity", "Partial updates leave inconsistent books.", "Approved grants without reserved funds or orphan journals.",
    [D(U), S(TSC, "PI1.3")], "customer-preference", "critical", alts=["Are financial transactions ACID?"]),
  Q("If a batch of payments or grants partially fails, how do you know exactly which items succeeded and which did not?",
    "batch-integrity", "Batch failures are hard to unwind.", "Items assumed processed that were not, or vice versa.",
    [D(U)], "customer-preference", "high", reqs=["UNB-XIN-EVA-011"]),
  Q("Does your architecture rely on distributed transactions or multiple databases to keep financial records consistent?",
    "atomicity", "Distributed consistency is fragile.", "Cross-store inconsistency after partial failure.",
    [D(U)], "customer-preference", "medium", reqs=["CNV-ARC-001", "UNB-XIN-EVA-013", "UNB-XIN-EVA-016"]),
  Q("Can a fund balance shown to a user ever be derived from something other than the posted ledger and reservations?",
    "balance-derivation", "Balances must have one source of truth.", "Displayed balances diverge from books.",
    [D(U)], "customer-preference", "medium", reqs=["UNB-XIN-EVA-001", "RR-UNB-GFUND-021-r1"]),
 ]),
dict(
 title="Concurrency control, serializable reservations and dispatch fencing",
 target=("A grant reservation is created only inside one serializable transaction that computes reservable capacity from the "
         "authoritative ledger, reservation and hold records for the fund and every constrained ancestor (pool cash buffer, "
         "custody account, entity, restricted sub-balance), acquiring locks in a deterministic order; display projections are "
         "never used for this check (RR-UNB-GFUND-021-r1). Concurrent recommendations, redemptions or liquidations cannot commit "
         "the same liquidity twice (UNB-GFUND-021, UNB-NAV-028). Conflicting instructions from different advisors move both to "
         "HeldConflict unless policy resolves them deterministically (UNB-XIN-EVA-012). At the irreversible dispatch step, the "
         "release checks the current hold publication version atomically with authorization using a fencing token, and unknown "
         "hold state fails closed (CNV-ARC-003). Cancel-versus-submit races resolve by revision with exactly one winner (TVR-GR-004). "
         "Tenant migration never permits two active authoritative writers (UNB-TEN-013)."),
 intended="Test the 12 concurrency schedules and 16 invariants named in REQ-X-019 with deterministic interleavings before release.",
 prov_refs="RR-UNB-GFUND-021-r1, UNB-GFUND-021, UNB-NAV-028, UNB-XIN-EVA-012, CNV-ARC-003, TVR-GR-004, UNB-TEN-013, REQ-X-019",
 statement="Planned: Unbound specifies serializable reservations, deterministic lock ordering and fenced dispatch to prevent concurrent double-commitment. None of the specified concurrency tests has been executed.",
 controls=["ECTL-TXI-003", "ECTL-TXI-004", "ECTL-TXI-007"], evidence=["EVR-TXI-003", "EVR-TXI-004", "EVR-TXI-007"], policies=["SEC-LANG-002"],
 requirements=["RR-UNB-GFUND-021-r1", "UNB-GFUND-021", "UNB-NAV-028", "UNB-XIN-EVA-012", "CNV-ARC-003", "TVR-GR-004", "UNB-TEN-013", "REQ-X-019"],
 impl_cost="high", rec_cost="low",
 residual=["Serializable isolation can increase retries and latency at year-end surge (UNB-IMM-010 requires load tests)."],
 questions=[
  Q("How do you prevent two simultaneous transactions from spending or committing the same funds?",
    "concurrency", "Race conditions cause overcommitment.", "Grants approved beyond available assets.",
    [D(U), S(CWE, "CWE-362"), S(ASVS)], "customer-preference", "critical", alts=["How do you handle race conditions on balances?"]),
  Q("What database isolation level and locking approach protect balance checks, and how do you avoid using stale cached balances for authorization?",
    "concurrency", "Check-then-act on stale data is a classic flaw.", "Time-of-check to time-of-use errors.",
    [D(U), S(CWE, "CWE-367")], "customer-preference", "high", reqs=["RR-UNB-GFUND-021-r1", "UNB-XIN-EVA-001"]),
  Q("If a fraud or sanctions hold is placed while a payment is being released, how do you guarantee the hold takes effect before the payment is transmitted?",
    "dispatch-fencing", "Holds must win races with release.", "Payment sent after a hold was placed.",
    [D(U), S(CWE, "CWE-367")], "customer-preference", "critical", reqs=["CNV-ARC-003", "UNB-XIN-EVA-011", "CNV-GRT-006"]),
  Q("How are conflicting instructions from two authorized people on the same account resolved when they arrive at the same time?",
    "conflicting-instructions", "Multi-advisor accounts produce conflicts.", "Last-writer-wins overrides a legitimate instruction.",
    [D(U)], "customer-preference", "medium", reqs=["UNB-XIN-EVA-012", "UNB-PART-005", "TVR-GR-004"]),
  Q("How have you tested your system's behavior under concurrent access, and can you share the test approach and results?",
    "concurrency-testing", "Concurrency bugs are rarely found by ordinary tests.", "Latent race conditions in production.",
    [D(U), S("SRC-NIST-SP800-218", "PW.8"), S(SCS)], "customer-preference", "medium", reqs=["REQ-X-019", "REQ-X-081", "UNB-IMM-010"],
    oq=["No concurrency tests exist yet; REQ-X-019 lists them as not executed."]),
 ]),
dict(
 title="Completeness and accuracy of inputs from external sources",
 target=("Each external source (bank statements and return files, custodian files, processor reports, IRS exempt-organization "
         "extracts, sanctions lists) has an expected-delivery calendar and a completeness watermark; a batch is accepted only when "
         "its control totals (record count, amount sum or source trailer) match, and a source behind schedule opens a "
         "SourceFeedGapDetected case that holds automated actions depending on that source's freshness while still allowing "
         "protective actions (UNB-XIN-EVA-004). External files and webhooks carry retrieval evidence and authenticity checks, "
         "and ingestion alone never grants sponsor approval (UNB-EVT-003). Provider callbacks are authenticated and deduplicated "
         "on provider and event ID and on a semantic key (RR-REQ-X-083-r1). Raw feeds are preserved and duplicate or "
         "out-of-order observations never overwrite prior evidence (CNV-FIN-013, UNB-KNOW-027). Input validation at trust "
         "boundaries uses explicit schemas and size limits (SEC-DATA-001)."),
 intended="Build source adapters with calendar, watermark and control-total checks; preserve raw payloads with hashes.",
 prov_refs="UNB-XIN-EVA-004, UNB-EVT-003, RR-REQ-X-083-r1, CNV-FIN-013, UNB-KNOW-027, UNB-CUST-009",
 statement="Planned: external feeds are specified to be accepted only on matching control totals and authenticated origin, with missing feeds detected against a calendar. Not implemented.",
 controls=["ECTL-TXI-005", "ECTL-TXI-009"], evidence=["EVR-TXI-005", "EVR-TXI-009"], policies=["SEC-DATA-001"],
 requirements=["UNB-XIN-EVA-004", "UNB-EVT-003", "RR-REQ-X-083-r1", "CNV-FIN-013", "UNB-KNOW-027", "UNB-CUST-009"],
 impl_cost="medium", rec_cost="low",
 questions=[
  Q("How do you verify that files received from banks, custodians or processors are complete before you process them?",
    "input-completeness", "Truncated files silently omit transactions.", "Missing transactions in the books.",
    [D(U), D(TSC, "PI1.2")], "certification-criteria", "high", alts=["Do you check control totals on inbound files?"]),
  Q("How would you detect that an expected bank or custodian file never arrived?",
    "input-completeness", "Absence is harder to detect than error.", "Decisions made on stale data.",
    [D(U), S(TSC, "PI1.2")], "customer-preference", "high", reqs=["UNB-XIN-EVA-004", "SOC2-027"]),
  Q("How do you authenticate inbound webhooks, callbacks and files so that a forged message cannot change a payment or contribution status?",
    "input-authenticity", "Forged status messages can trigger reissues or false completion.", "Fraudulent state changes from spoofed inputs.",
    [D(U), S(CWE, "CWE-345"), S(N53, "SC-8")], "customer-preference", "critical", reqs=["RR-REQ-X-083-r1", "UNB-EVT-003", "UNB-API-STD-005"]),
  Q("How are inbound records validated for format, range and business rules before they affect balances?",
    "input-validation", "Malformed inputs corrupt records.", "Invalid data posted to the ledger.",
    [D(TSC, "PI1.2"), S(SCS), S(N53, "SI-10")], "certification-criteria", "medium", reqs=["UNB-XIN-EVA-004", "UNB-XIN-EVA-008"]),
 ]),
dict(
 title="Processing integrity and continuously checked financial invariants",
 target=("Unbound defines its processing integrity commitments as explicit invariants that are continuously checkable: balanced "
         "journals, valid dimensions, nonduplicated external effects, reconciled control accounts, authorized allocations, "
         "preserved restrictions and no unauthorized negative available balance (UNB-ACC-030; Secure Construction Standard, "
         "Financial and business invariants). Outputs are computed only from sealed snapshots so they are complete and "
         "reproducible (UNB-XIN-EVA-003). Releases deploy in rings and halt automatically when a ledger balance, outbox backlog, "
         "unknown-rate or error-budget check breaches its threshold (UNB-XIN-SAS-003). Every business-significant event produces "
         "attributable, tamper-evident evidence (SOC2-002), and a missing expected control heartbeat is itself an exception "
         "(SOC2-027). These map to the SOC 2 processing integrity criteria if Echelon elects that category in a future SOC 2 scope."),
 intended="Run the invariant monitor continuously in production and as a release gate; elect processing integrity in SOC 2 scope only after controls operate.",
 prov_refs="UNB-ACC-030, UNB-XIN-EVA-003, UNB-XIN-SAS-003, SOC2-002, SOC2-027",
 statement="Echelon has no SOC 2 report and has not selected processing integrity criteria. Unbound's requirements define continuously checked financial invariants as the intended basis. Not implemented.",
 kind="not-available", controls=["ECTL-TXI-006"], evidence=["EVR-TXI-006"], policies=["SOC2-002", "SOC2-021", "SOC2-027", "SOC2-036"],
 requirements=["UNB-ACC-030", "UNB-XIN-EVA-003", "UNB-XIN-SAS-003", "SOC2-002", "SOC2-027", "UNB-SCTRL-041"],
 mechanism="continuous-automated", freshness="PT1H", impl_cost="medium", rec_cost="low",
 challenge=dict(
  customer_intent="Confidence that the system processes transactions completely, accurately, timely and with authorization.",
  adverse_outcome="Silent processing errors that misstate funds or payments.",
  conventional_control_effectiveness="SOC 2 PI testing samples transactions and reviews procedures; it rarely proves invariants hold across the full population.",
  legally_required="No.", contractually_required="Some customers require SOC 2 with processing integrity in scope.",
  historical_convention="Batch control totals and periodic reconciliations.",
  architectural_elimination="Some invariant violations (unbalanced journals, edits to posted history) are eliminated by construction within the ledger scope.",
  automatic_enforcement="Database constraints and typed commands.", continuous_evidence="Invariant monitor results per hour and per release.",
  stronger_alternative="Continuously evaluated invariants with release halts, supplemented later by an independent SOC 2 including PI.",
  alternative_verifiable="Yes, if monitor logic and results are retained and independently reviewed.",
  customer_acceptance_likelihood="Uncertain as a substitute; likely as a supplement.",
  invalidating_conditions="Monitor logic shares defects with the system it monitors.",
  conventional_cost="High (audit fees, PI scope).", alternative_cost="Medium.",
  alternative_risks="First-party evidence is not independent.",
  supporting_arguments=["Full-population coverage.", "Faster detection."],
  opposing_arguments=["Customers' vendor management teams usually require an independent report.", "Monitor and system written by the same team."],
  technical_effectiveness="stronger", institutional_acceptance="uncertain"),
 questions=[
  Q("Is processing integrity included in your SOC 2 scope, and if not, how do you demonstrate that processing is complete, accurate, timely and authorized?",
    "processing-integrity", "Customers want assurance over transaction processing.", "Undetected processing errors.",
    [D(TSC, "PI1.3"), S("SRC-AICPA-SOC2-GUIDE")], "certification-criteria", "high", alts=["Which Trust Services Categories are in your SOC 2?"]),
  Q("Which financial integrity rules does your system check continuously, and what happens when one is violated?",
    "invariants", "Defined invariants make integrity testable.", "Violations go unnoticed until reconciliation.",
    [D(U), D(SCS)], "customer-preference", "high"),
  Q("How do you ensure that reports and statements delivered to us are complete and accurate representations of processed data?",
    "output-integrity", "Outputs drive donor statements and filings.", "Incomplete or inconsistent outputs.",
    [D(TSC, "PI1.4"), D(U)], "certification-criteria", "high", reqs=["UNB-XIN-EVA-003", "UNB-ACC-025"]),
  Q("Can a software release that breaks a financial integrity rule reach all customers before it is detected?",
    "release-integrity", "Defective releases can corrupt many tenants at once.", "Multi-tenant corruption from a bad deploy.",
    [D(U), S(TSC, "CC8.1")], "customer-preference", "high", reqs=["UNB-XIN-SAS-003", "CNV-PLT-010"]),
 ]),
dict(
 title="Deterministic replay and projection rebuild without side effects",
 target=("Rebuilding projections from an immutable snapshot or checkpoint plus subsequent events produces the same state as full "
         "replay; the snapshot is a cache, never authority (UNB-IMM-005). Replay is deterministic and side-effect-free: posting "
         "rules apply once at posting time and are not re-applied, replay locates existing journals by source event and book, "
         "and external effects require durable issuance receipts so replay cannot repeat them (UNB-DATA-009, RR-ACC-MDL-007-r1, "
         "UNB-XIN-EVA-001). Stored events carry schema versions; authoritative consumers that meet an unknown version stop and "
         "quarantine rather than skip (UNB-XIN-EVA-008). Replay and rebuild times are load-tested at defined scales, including "
         "a 10x grant surge, before storage technology is finalized (UNB-IMM-010, UNB-ACC-036)."),
 intended="Run replay-equivalence checks as a release gate and on a schedule against production-shaped synthetic data.",
 prov_refs="UNB-IMM-005, UNB-DATA-009, RR-ACC-MDL-007-r1, UNB-XIN-EVA-001, UNB-XIN-EVA-008, UNB-IMM-010, UNB-ACC-036",
 statement="Planned: replay and projection rebuild are specified to be deterministic and unable to trigger external effects. Not implemented or tested.",
 controls=["ECTL-TXI-002", "ECTL-TXI-007"], evidence=["EVR-TXI-007", "EVR-TXI-002"],
 requirements=["UNB-IMM-005", "UNB-DATA-009", "RR-ACC-MDL-007-r1", "UNB-XIN-EVA-001", "UNB-XIN-EVA-008", "UNB-IMM-010", "UNB-ACC-036"],
 impl_cost="medium", rec_cost="low",
 questions=[
  Q("If you need to rebuild data after a defect or restore, can you replay transactions deterministically and get exactly the same balances?",
    "deterministic-replay", "Recovery must not change results.", "Different balances after rebuild.",
    [D(U)], "customer-preference", "high", alts=["Is your event replay deterministic?"]),
  Q("When you replay or reprocess historical events, what prevents payments, emails or other external actions from being triggered again?",
    "replay-protection", "Replay is a common duplicate source.", "Duplicate external effects during recovery.",
    [D(U), S(CWE, "CWE-294")], "customer-preference", "critical", reqs=["UNB-DATA-009", "UNB-IMM-006", "UNB-RES-002"]),
  Q("How do you handle events stored in an older format when the software changes, so that historical processing remains correct?",
    "schema-evolution", "Format drift breaks replay.", "Silent misinterpretation of historical events.",
    [D(U)], "customer-preference", "medium", reqs=["UNB-XIN-EVA-008", "UNB-RCN-ARC-001"]),
  Q("How long would a full rebuild of a large sponsor's history take, and has that been measured?",
    "replay-performance", "Recovery time matters at scale.", "Unacceptable recovery time during year-end.",
    [D(U)], "customer-preference", "low", reqs=["UNB-IMM-010", "UNB-ACC-036", "UNB-ECO-007"],
    oq=["Not measured; no system exists."]),
 ]),
dict(
 title="Unknown outcome handling for timeouts and ambiguous external results",
 target=("When an external call times out or returns an ambiguous result, the item enters an explicit Unknown state; there is "
         "no retry button and no automatic retry (TVR-PAY-001, CNV-PAY-004). Each rail has an UnknownResolutionProtocol: status "
         "query by idempotency key at defined intervals, reconciliation against bank statements after the settlement window, and "
         "a defined evidence combination before NotReceived may be declared, which requires independent approval and creates a "
         "linked reissue chain (UNB-RCN-GRT-008). Before the final aging tier a bank trace or rail status request is made; only "
         "items still Unobtainable after 30 days go to two independent approvers who record duplicate-risk acceptance and a "
         "recovery plan (CNV-PAY-004). A bulk-Unknown event uses graded evidence and dual-control sampling and never bulk-declares "
         "NotReceived without per-item proof (TVR-PAY-007). Reissue after a proven NotSubmitted reuses the original idempotency key "
         "(UNB-RCN-WF-001). UIs never show success before authoritative confirmation (INT-006, AIN-014)."),
 intended="Implement the payment aggregate with an explicit ProviderKnowledge dimension and an aging queue; drill the bulk-Unknown procedure.",
 prov_refs="TVR-PAY-001, TVR-PAY-007, UNB-RCN-GRT-008, CNV-PAY-004, UNB-RCN-WF-001, AIN-019, RR-REQ-X-083-r1",
 statement="Planned: ambiguous payment outcomes are specified as an explicit Unknown state resolved only by evidence and independent approval, never by automatic retry. Not implemented.",
 controls=["ECTL-TXI-008"], evidence=["EVR-TXI-008"],
 requirements=["TVR-PAY-001", "TVR-PAY-007", "UNB-RCN-GRT-008", "CNV-PAY-004", "UNB-RCN-WF-001", "AIN-019", "RR-REQ-X-083-r1", "INT-006", "AIN-014"],
 impl_cost="medium", rec_cost="medium",
 questions=[
  Q("What does the system do when it sends a transaction to a bank or payment provider and does not receive a definitive response?",
    "unknown-outcome", "Timeouts are where duplicates and losses occur.", "Blind retry causing duplicate payment.",
    [D(U), S(TSC, "PI1.3")], "customer-preference", "critical", alts=["How are timeouts on payment submissions handled?"]),
  Q("Who can decide that an uncertain payment was never received and should be reissued, and what evidence is required?",
    "unknown-outcome", "Reissue decisions carry duplicate risk.", "Reissue of a payment that actually settled.",
    [D(U)], "customer-preference", "high", reqs=["UNB-RCN-GRT-008", "CNV-PAY-004", "TVR-PAY-007"]),
  Q("If a provider outage leaves hundreds of payments in an uncertain state, how do you resolve them without mass duplicate payments?",
    "bulk-unknown", "Mass ambiguity is a realistic outage scenario.", "Mass duplicate disbursement.",
    [D(U)], "customer-preference", "high", reqs=["TVR-PAY-007", "CNV-PLT-012"]),
  Q("Does the user interface ever show a payment or grant as completed before the bank or provider has confirmed it?",
    "status-truthfulness", "Premature success misleads donors and staff.", "Decisions based on false completion.",
    [D(U)], "customer-preference", "medium", reqs=["INT-006", "AIN-014", "UNB-PAY-009", "UNB-PAY-010"]),
 ]),
]

controls = [
 C("Business idempotency key registry with unique constraints and payload hashes", "Each command and external observation type has a registered business key; a database unique constraint in the effect transaction rejects duplicates and detects key reuse with different content.",
   "preventive-structural", "L3-restricted-interface", ["Unbound command engine (specified, not built)", "PostgreSQL"], ["EVR-TXI-001"],
   related=["UNB-CTRL-068"], cwe=["CWE-837"], refs=[S("SRC-AICPA-TSC", "PI1.3")]),
 C("Transactional outbox with effect receipts and effect-free replay", "External effects are issued only from outbox items committed with the state change; each effect records a durable receipt; replay and rebuild code paths have no access to effect adapters.",
   "preventive-structural", "L3-restricted-interface", ["Unbound command engine and outbox (specified, not built)"], ["EVR-TXI-002"],
   cwe=["CWE-837", "CWE-294"], residual=["Provider-side duplicates where rails lack idempotency"]),
 C("Serializable reservation with deterministic lock order", "Reservations are computed and inserted in one serializable transaction over authoritative records for the fund and all constrained ancestors, locking in a fixed order.",
   "preventive-structural", "L3-restricted-interface", ["Unbound grants and ledger components (specified, not built)", "PostgreSQL"], ["EVR-TXI-003"],
   related=["UNB-SCTRL-017", "UNB-CTRL-025"], cwe=["CWE-362", "CWE-367"]),
 C("Dispatch fencing on hold version and authorization", "At the irreversible dispatch step, check the current hold publication version and authorization in the same transaction that releases the instruction; fail closed on unknown hold state.",
   "preventive-structural", "L3-restricted-interface", ["Unbound payment dispatcher (specified, not built)"], ["EVR-TXI-004"],
   related=["UNB-SCTRL-029", "UNB-CTRL-049"], cwe=["CWE-367"]),
 C("Source feed completeness gate", "Accept external batches only when control totals match; detect missing deliveries against an expected calendar and hold dependent automation.",
   "preventive-gate", "L3-restricted-interface", ["Unbound integration adapters (specified, not built)"], ["EVR-TXI-005"],
   related=["UNB-SCTRL-009", "UNB-SCTRL-024"], refs=[D("SRC-AICPA-TSC", "PI1.2")]),
 C("Continuous financial invariant monitor with release halt", "Evaluate ledger and payment invariants continuously and during ring deployment; breach halts rollout and opens an incident.",
   "detective-automated", "L9-runtime-monitored", ["Unbound monitoring (specified, not built)"], ["EVR-TXI-006"],
   related=["UNB-SCTRL-041", "UNB-CTRL-075"], policies=["SOC2-027"], refs=[S("SRC-ECH-SCS-0.1")]),
 C("Concurrency, crash-injection and replay-equivalence test suite", "Deterministic interleavings, crash injection at every step of payment and posting flows, and replay-equivalence comparisons must pass before release.",
   "preventive-gate", "L8-adversarial-tested", ["Unbound test suite (specified, not built)", "Praxis CI gates (exists; not operated for Unbound)"], ["EVR-TXI-007"],
   refs=[S("SRC-NIST-SP800-218", "PW.8"), S("SRC-ECH-SCS-0.1")], notes="REQ-X-081 defines 28 first-pass simulations, none executed."),
 C("Unknown state without retry affordance and evidence-gated resolution", "The payment model has an explicit Unknown state with no automatic or manual retry; NotReceived requires the rail's evidence combination and independent approval.",
   "preventive-structural", "L3-restricted-interface", ["Unbound payment component (specified, not built)"], ["EVR-TXI-008"],
   related=["UNB-SCTRL-029"], cwe=["CWE-837"]),
 C("Authenticated and deduplicated provider callbacks", "Verify the origin of each callback or file (signature or authenticated channel), deduplicate on provider event ID and semantic key, and reject unauthenticated inputs.",
   "preventive-structural", "L3-restricted-interface", ["Unbound integration adapters (specified, not built)"], ["EVR-TXI-009"],
   policies=["SEC-DATA-001", "SEC-CRYPTO-001"], cwe=["CWE-345", "CWE-294"], refs=[S("SRC-NIST-SP800-53-R5", "SC-8")]),
]

evidence = [
 E("Idempotency outcomes and duplicate-key conflict cases", "Accepted, acknowledged-without-effect and conflicting submissions per key, with DuplicateKeyConflict cases.", NOT_ASSIGNED.format("Unbound command engine"), "event-driven-automated", "per-event"),
 E("Effect receipt ledger reconciled to providers", "Each external effect with outbox item, receipt, provider reference and reconciliation status.", NOT_ASSIGNED.format("Unbound outbox"), "event-driven-automated", "per-event"),
 E("Reservation commit records", "Reservation transactions with capacity inputs, lock scope and outcome, including rejections for insufficient capacity.", NOT_ASSIGNED.format("Unbound grants component"), "event-driven-automated", "per-event"),
 E("Dispatch fence checks", "Per item dispatch record of hold version checked, authorization state and allow or fail-closed outcome.", NOT_ASSIGNED.format("Unbound payment dispatcher"), "event-driven-automated", "per-event"),
 E("Feed watermark and gap cases", "Per source completeness watermark, control-total results and SourceFeedGapDetected cases.", NOT_ASSIGNED.format("Unbound integration adapters"), "continuous-automated", "P1D"),
 E("Invariant monitor results", "Hourly and per-release invariant evaluations, breaches and halts.", NOT_ASSIGNED.format("Unbound monitoring"), "continuous-automated", "PT1H"),
 E("Concurrency and replay test reports", "Interleaving schedules, crash points, replay-equivalence comparisons and results tied to the release commit.", NOT_ASSIGNED.format("Unbound test suite with Praxis provenance"), "event-driven-automated", "per-event", disclosure="nda"),
 E("Unknown-outcome aging and resolution records", "Unknown items by age tier, status queries, traces, evidence combinations and approvals for NotReceived.", NOT_ASSIGNED.format("Unbound payment component"), "continuous-automated", "P1D"),
 E("Callback authentication failures", "Rejected unauthenticated or replayed callbacks and files with source and reason.", NOT_ASSIGNED.format("Unbound integration adapters"), "event-driven-automated", "per-event", disclosure="internal"),
]
