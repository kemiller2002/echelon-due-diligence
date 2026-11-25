from finlib import *

COSO = S("SRC-COSO-2013", "Principle 10")
SOC1 = S("SRC-AICPA-SSAE-18", "AT-C 320")
TSC_PI = S("SRC-AICPA-TSC", "PI1.3")
ASC958 = S("SRC-FASB-ASC-958")
LAND = S("SRC-ECH-DAF-LANDSCAPE")
FIN_IND = ["donor-advised-funds", "nonprofit", "financial-services", "wealth-management"]

units = [
AU("Reconciliation scope, sources and cadence (bank, custodian, payment rail, subledger, GL)",
   target=("Unbound is designed to reconcile continuously, not only at month end. Every "
           "authoritative balance has an independent external counterpart: sponsor-owned "
           "bank accounts (BAI2/BTRS and ISO 20022 camt.052/053/054 feeds, prior-day "
           "mandatory) to the cash subledger; custodian positions, cash and transactions to "
           "the investment subledger per security and per custody account; payment-rail "
           "settlement and returns to grants payable; and the sum of fund-level balances to "
           "the sponsor GL control accounts by entity, fund, restriction and currency. Where "
           "the sponsor's GL is kept in an external book of record, Unbound reconciles to it "
           "and is never a second authoritative book. Exact matches auto-pass, residual "
           "items route to an exception queue, and spendable capacity is derived from "
           "internal reservations against the last verified balance, never from a feed "
           "balance alone; releases fail closed when feeds are stale beyond the approved "
           "window. Because Unbound holds no donor money (CNV-LEG-001), all cash reconciled "
           "is in sponsor-owned accounts."),
   stmt=("Planned: Unbound's requirements specify continuous reconciliation of bank, "
         "custodian, payment-rail and fund subledger data to the sponsor general ledger. "
         "No reconciliation is operating today because Unbound is not yet built or deployed."),
   reqs=["CNV-FIN-004", "UNB-GAP-001", "UNB-ACC-018", "UNB-WF-019", "ACC-MDL-009",
         "CNV-PAY-007", "UNB-CUST-010", "UNB-INV-026", "RR-UNB-ACC-008-r2",
         "UNB-HYP-005", "CNV-LEG-001"],
   oqs=["UNB-HYP-005 records continuous three-way reconciliation as a hypothesis; no "
        "measured break-rate or cost evidence exists (daf-landscape reconciliation "
        "economics model is explicitly illustrative).",
        "Which sponsor bank and custodian feed formats are actually available for the "
        "first sponsor has not been established."],
   risks=["Continuous matching can only be as complete as the external feeds; a bank or "
          "custodian that provides only monthly statements reduces the design to periodic "
          "reconciliation for that source."],
   owner="Unassigned (proposed: sponsor Controller with Unbound reconciliation component owner)",
   challenge={
       "customer_intent": "Assurance that recorded fund balances agree with money and securities that actually exist, and that differences are found quickly.",
       "adverse_outcome": "Misstated fund balances, grants funded from money that is not there, undetected theft or posting errors.",
       "conventional_control_effectiveness": "Monthly manual bank and custodian reconciliations detect differences up to roughly 30 to 60 days late and depend on preparer diligence; sampling of reviewer sign-off is common audit evidence.",
       "legally_required": "No statute requires a DAF sponsor to reconcile at a given frequency; reconciliation supports GAAP financial statements and the sponsor's audit.",
       "contractually_required": "Commonly required by sponsor contracts and by auditors relying on a service organization's controls.",
       "historical_convention": "Month-end reconciliation with preparer and reviewer signatures.",
       "architectural_elimination": "Not eliminable: external balances are outside Unbound's control. Internal subledger-to-GL differences can be largely eliminated by deriving GL control balances from the same balanced append-only journal.",
       "automatic_enforcement": "Statements, NAV publication and new reservations for an affected scope are blocked while a material break is open (RR-UNB-ACC-018-r1).",
       "continuous_evidence": "Each match decision, feed receipt and break is an append-only event with source hash.",
       "stronger_alternative": "Continuous matching with exception-only human review and an independently attested sample of auto-passed items.",
       "alternative_verifiable": "Yes, if the match log, source hashes and sample attestations are retained and re-performable by an auditor.",
       "customer_acceptance_likelihood": "Likely for detection speed; uncertain for replacing reviewer sign-off until an auditor confirms reliance (CNV-GOV-001).",
       "invalidating_conditions": "Feeds unavailable or not machine-readable; tolerances set too loosely; auto-match rules changed without independent approval.",
       "conventional_cost": "Recurring staff time per account per month; scales with account count.",
       "alternative_cost": "Higher build cost for adapters and match engine; lower marginal cost per account once built.",
       "alternative_risks": "Over-trust in automation; systematic matching error affecting many items at once.",
       "supporting_arguments": ["Detection latency drops from weeks to a day or less.",
                                 "Exception-only review concentrates human attention where differences exist."],
       "opposing_arguments": ["Auditors and sponsor controllers are accustomed to signed monthly reconciliations and may still require them.",
                              "No DAF-specific evidence yet shows that continuous reconciliation reduces cost (UNB-HYP-005 is a hypothesis)."],
       "technical_effectiveness": "stronger", "institutional_acceptance": "uncertain"},
   ctls=[C("Continuous multi-source reconciliation engine",
           "Match every external bank, custodian and payment-rail observation to internal ledger entries, and fund-level totals to GL control accounts, with exact matches auto-passed and all others queued.",
           "detective-automated", "L9-runtime-monitored",
           related=["UNB-CTRL-046", "UNB-CTRL-047", "UNB-SCTRL-024"],
           policies=["SEC-DATA-001"],
           frefs=[UB("CNV-FIN-004"), S("SRC-COSO-2013", "Principle 10", "maps-to")]),
       C("Stale-feed fail-closed release gate",
         "Prevent payment release or new reservations from relying on a bank or custodian balance older than the approved freshness window.",
         "preventive-gate", "L3-restricted-interface", related=["UNB-SCTRL-029"],
         frefs=[UB("CNV-PAY-007")])],
   evrs=[E("Reconciliation run and match log",
           "Per source and scope: feed receipt (source, as-of, received time, hash), match decisions with rule version, unmatched items and resulting breaks.",
           "continuous-automated", "P1D", fmt="JSON Lines event stream",
           prov=["source_id", "as_of", "received_at", "content_sha256", "rule_version", "run_id"],
           retention="Per sponsor record-retention policy (not yet set; SOC2-023)"),
         E("Feed freshness status",
           "Per external source, last verified balance time versus approved window, and any release blocked for staleness.",
           "continuous-automated", "PT1H")],
   qs=[
    Q("Reconciliation scope", "Which external sources (bank, custodian, payment processor, external GL) does your platform reconcile to the fund ledger, and which internal balances does each source prove?",
      "Know whether every recorded balance is checked against an independent source.",
      "Unreconciled balance types allowing undetected misstatement or loss.",
      [UB("UNB-GAP-001"), COSO, ASC958], "industry-convention", "critical",
      alts=["Describe your reconciliation coverage across cash, securities, grants payable and fund balances.",
            "List each reconciliation performed, its counterparty source and the ledger account it supports."], ind=FIN_IND),
    Q("Reconciliation cadence", "How often is each reconciliation performed (continuously, daily, monthly), and what is the maximum time an unexplained difference can exist before detection?",
      "Bound detection latency for errors and misappropriation.",
      "Late detection of breaks, allowing losses or misstatements to compound.",
      [UB("CNV-FIN-004"), COSO], "industry-convention", "high",
      alts=["Are reconciliations performed in real time or at period end?"]),
    Q("Three-way reconciliation", "Do you reconcile bank, custodian and fund-ledger records against each other (three-way), or only each pair to the GL?",
      "Ensure cash moving between custodian and bank is traced on both sides.",
      "Cash in transit between custodian and bank lost or double counted.",
      [UB("UNB-WF-019"), UB("UNB-HYP-005")], "customer-preference", "medium"),
    Q("Fund-to-control reconciliation", "Does the sum of all individual DAF fund balances reconcile to the sponsor's general ledger control and net asset accounts by entity, restriction and currency?",
      "Ensure donor statements in aggregate agree with audited financial statements.",
      "Fund statements that do not tie to the sponsor's books, undermining audit and Schedule D.",
      [UB("ACC-MDL-009"), UB("CNV-FIN-006"), ASC958], "industry-convention", "critical",
      alts=["How do you prove subledger-to-GL integrity for donor fund balances?"]),
    Q("External book of record", "When the sponsor keeps its general ledger in its own accounting system, how does your platform reconcile to it, and which system is authoritative?",
      "Avoid two competing books and unresolved differences between them.",
      "Divergent books leading to audit findings or wrong fund balances.",
      [UB("RR-UNB-ACC-008-r2"), COSO], "industry-convention", "high"),
    Q("Bank feed ingestion", "What bank statement formats and delivery methods do you ingest (for example BAI2, ISO 20022 camt.053, bank APIs), and what happens when a feed is late or missing?",
      "Ensure bank data is complete and its absence is noticed.",
      "Reconciliation silently skipped because data never arrived.",
      [UB("CNV-PAY-007"), S("SRC-FFIEC-ARCHITECTURE-BOOKLET")], "industry-convention", "high",
      ind=["donor-advised-funds", "banking", "financial-services"]),
    Q("Capacity from feeds", "Is any spendable or grantable balance ever derived directly from an external feed balance, or only from internal reservations checked against the last verified balance?",
      "Prevent grants being authorized against stale or unverified balances.",
      "Over-disbursement when a feed shows funds that are not available.",
      [UB("CNV-PAY-007"), UB("UNB-RCN-FIN-009")], "echelon-internal", "high"),
   ]),

AU("Matching rules, tolerances and auto-clear governance",
   target=("Match rules and tolerances are versioned policy objects. Tolerances are absolute "
           "and relative per source, currency and asset class, calibrated from observed "
           "feeds. A new source starts in ProvisionalCalibration: exact match only, every "
           "non-exact item to human review and 100 percent review for at least one full "
           "close cycle of parallel run, after which the controller approves tolerances. "
           "Differences are classified against RoundingTolerance (auto-clear with evidence), "
           "Materiality and AgingLimit thresholds; loosening any threshold requires a second "
           "approver. There are no balancing plugs or silent write-offs. External "
           "observations carry registered business idempotency keys so duplicates cannot "
           "match twice. AI may propose a match or explanation but cannot apply a manual "
           "match, change a tolerance or approve its own proposal."),
   stmt=("Planned: tolerance and match-rule governance is specified in Unbound's "
         "requirements, including second-approver control on loosening thresholds. Not "
         "implemented."),
   reqs=["CNV-FIN-004", "RR-UNB-ACC-018-r1", "UNB-GAP-002", "UNB-XIN-EVA-005",
         "UNB-NAV-012", "UNB-ACC-029", "GOV-AUTH-004"],
   oqs=["Default numeric tolerances are deliberately not set (CNV-FIN-004 labels any "
        "starting value illustrative); a sponsor will ask for them."],
   risks=["Calibration from observed data can normalize a persistent systematic error "
          "present during the parallel run."],
   owner="Unassigned (proposed: sponsor Controller)",
   ctls=[C("Versioned tolerance policy with dual approval to loosen",
           "Store every match rule and tolerance as an effective-dated policy version; any loosening requires a second, independent approver; an AI principal cannot approve.",
           "preventive-gate", "L3-restricted-interface", related=["UNB-CTRL-046", "UNB-SCTRL-002"],
           policies=["SEC-AUTH-001"], frefs=[UB("RR-UNB-ACC-018-r1")]),
       C("No-plug invariant",
         "Reject any journal that clears a reconciliation difference without a typed reason, linked evidence and authorized approver.",
         "preventive-structural", "L3-restricted-interface", related=["UNB-SCTRL-025"],
         frefs=[UB("UNB-NAV-012"), UB("CNV-FIN-004")])],
   evrs=[E("Tolerance and match-rule version history",
           "Every policy version with author, approvers, effective date and diff from prior version; calibration evidence for new sources.",
           "event-driven-automated", "per-event", prov=["policy_id", "version", "approved_by", "approved_at"])],
   qs=[
    Q("Match rule governance", "How are automated matching rules created, tested, versioned and approved, and who is permitted to change them?",
      "Ensure auto-matching cannot be altered to hide differences.",
      "Unauthorized rule changes that auto-clear real breaks.",
      [UB("UNB-GAP-002"), COSO], "industry-convention", "high"),
    Q("Tolerances", "What tolerances allow a difference to auto-clear, how were they calibrated, and what approval is needed to widen them?",
      "Understand how much difference is accepted without human review.",
      "Material errors absorbed within loose tolerances.",
      [UB("RR-UNB-ACC-018-r1"), UB("CNV-FIN-004")], "industry-convention", "high",
      alts=["What thresholds do you use for auto-clearing reconciliation differences?"]),
    Q("New source onboarding", "When a new bank account, custodian or payment processor is connected, how is reconciliation validated before automation is trusted (for example a parallel run)?",
      "Avoid trusting an unproven feed.",
      "Systematic mismatches or mapping errors on a new source going undetected.",
      [UB("CNV-FIN-004")], "customer-preference", "medium"),
    Q("Plugs and write-offs", "Can a reconciliation difference ever be closed by a balancing entry or write-off, and if so with what approval and evidence?",
      "Detect concealment of losses.",
      "Fraud or error concealed by unexplained plug entries.",
      [UB("UNB-NAV-012"), COSO], "industry-convention", "critical"),
    Q("Duplicate observations", "How do you prevent a duplicated bank or custodian record (for example a resent file) from matching or posting twice?",
      "Ensure each external event is counted once.",
      "Duplicate postings inflating or deflating balances.",
      [UB("UNB-XIN-EVA-005"), TSC_PI], "industry-convention", "medium"),
    Q("AI in matching", "Can an AI agent propose, apply or approve a reconciliation match, explanation or tolerance change?",
      "Understand whether automated agents can alter financial control outcomes.",
      "Agent-created matches or tolerance changes hiding real differences.",
      [UB("UNB-ACC-029"), S("SRC-NIST-AI-RMF-1.0")], "customer-preference", "high",
      ind=["donor-advised-funds", "financial-services", "enterprise-software"]),
   ]),

AU("Break management: ownership, aging, escalation and fund impact",
   target=("Every unmatched item becomes a break case with owner, fund attribution, "
           "amount, age and evidence. Breaks above Materiality block close certification, "
           "NAV publication and new reservations for the affected scope only; immaterial "
           "unexplained differences escalate when the AgingLimit expires regardless of "
           "amount. A break is attributed to funds through its unmatched items; an "
           "unattributable break opens a controller decision due within a sponsor-set "
           "number of business days to either publish affected statements marked "
           "provisional (reconciliation pending) or withhold them. Breaks found after close "
           "open a post-close adjustment case that preserves the original close package. "
           "Break counts, aging and materiality are reported to the sponsor."),
   stmt=("Planned: break ownership, aging, materiality-based blocking and escalation are "
         "specified in Unbound requirements. No break history exists because the system "
         "is not operating."),
   reqs=["RR-UNB-ACC-018-r1", "UNB-GAP-002", "CNV-FIN-004", "EXC-18", "UNB-ACC-035",
         "RR-UNB-ACC-017-r1", "UNB-ECO-001"],
   oqs=["Sponsor-facing break reporting format and frequency are not specified."],
   owner="Unassigned (proposed: sponsor Controller)",
   ctls=[C("Break case lifecycle with aging escalation",
           "Open, own, age and escalate every break; materiality and aging thresholds drive automatic escalation and scoped blocking.",
           "detective-automated", "L9-runtime-monitored",
           related=["UNB-SCTRL-028", "UNB-CTRL-048"], frefs=[UB("RR-UNB-ACC-018-r1")]),
       C("Scoped publication block on material break",
         "Block statements, NAV publication and new reservations for funds affected by a material open break, without halting unaffected funds.",
         "preventive-gate", "L3-restricted-interface", related=["UNB-CTRL-046"],
         frefs=[UB("CNV-FIN-004")])],
   evrs=[E("Break register and aging report",
           "All breaks with owner, fund attribution, amount, age, status, resolution evidence and approver.",
           "continuous-automated", "P1D", disc="customer-only"),
         E("Post-close adjustment case file",
           "For breaks found after close: original close package reference, adjustment journals, approvals and affected statements.",
           "event-driven-automated", "per-event")],
   qs=[
    Q("Break ownership", "How are reconciliation breaks recorded, assigned to an owner and tracked to resolution?",
      "Ensure no difference is left unowned.", "Breaks aging indefinitely without action.",
      [UB("UNB-GAP-002"), COSO], "industry-convention", "high",
      alts=["Describe your exception management workflow for reconciliation items."]),
    Q("Aging and escalation", "What aging thresholds trigger escalation of unresolved breaks, to whom, and does escalation depend on amount?",
      "Prevent small differences accumulating unnoticed.", "Aged small breaks masking larger patterns.",
      [UB("RR-UNB-ACC-018-r1")], "industry-convention", "high"),
    Q("Fund impact", "When a cash or position break is open, what happens to affected donors' statements, displayed balances and ability to recommend grants?",
      "Protect donors and grantees from decisions based on wrong balances.",
      "Grants approved or statements issued from unreconciled balances.",
      [UB("CNV-FIN-004"), UB("RR-UNB-ACC-018-r1")], "customer-preference", "high"),
    Q("Unattributable breaks", "If a cash difference cannot be attributed to particular funds, how is it handled and who decides whether statements are issued?",
      "Understand handling of sponsor-level unexplained differences.",
      "Silent absorption of losses across all funds.",
      [UB("CNV-FIN-004")], "customer-preference", "medium"),
    Q("Post-close breaks", "How do you handle a reconciliation break discovered after a period has been closed and statements issued?",
      "Ensure corrections are controlled and prior outputs preserved.",
      "Retroactive changes that rewrite issued statements.",
      [UB("EXC-18"), UB("CNV-FIN-011")], "industry-convention", "medium"),
    Q("Break metrics", "Do you report reconciliation break volumes, aging and resolution times to the sponsor, and at what frequency?",
      "Give the sponsor oversight of operational quality.", "Sponsor unaware of deteriorating reconciliation quality.",
      [UB("UNB-ECO-001"), S("SRC-INTERAGENCY-TPRM-2023")], "customer-preference", "medium"),
   ]),

AU("Segregation of duties and independence of reconciliation from payment initiation",
   target=("No principal, whether human, service account or AI agent, can control "
           "request, approval and reconciliation of the same transaction. The component "
           "that initiates a payment or instruction cannot attest to its independent "
           "settlement; reconciliation accountability sits with a role outside the payment "
           "chain. Duty conflicts are evaluated per material action and self-approval is "
           "blocked. For small sponsors where full separation is impractical, compensating "
           "detective controls apply: cross-role anomaly analytics and independent periodic "
           "review, with the residual risk accepted in writing by the sponsor."),
   stmt=("Planned: Unbound requirements prohibit one actor (including an agent) from "
         "controlling request, approval and reconciliation. Not implemented."),
   reqs=["GOV-AUTH-004", "GOV-AUTH-014", "TVR-ORG-003", "UNB-ACC-022", "MON-008",
         "TVR-SEC-006", "UNB-NAV-008"],
   oqs=["TVR-ORG-003-Q (small-scale compensation for reconciliation segregation) is open in "
        "Unbound; the answer for a sponsor with one or two finance staff is unresolved."],
   risks=["Collusion between two principals defeats segregation; detective analytics are "
          "specified (TVR-SEC-006) but untested."],
   mech="event-driven-automated", fresh="per-event",
   owner="Unassigned (proposed: Unbound governance and sponsor Controller)",
   ctls=[C("Duty conflict evaluation per material action",
           "Evaluate request, approval and reconciliation roles for the same transaction and deny self-attestation, including for AI agent principals.",
           "preventive-structural", "L3-restricted-interface",
           related=["UNB-SCTRL-002", "UNB-CTRL-046"], policies=["SEC-AUTH-001"],
           frefs=[UB("GOV-AUTH-004"), S("SRC-COSO-2013", "Principle 10", "maps-to")])],
   evrs=[E("Duty conflict decision log",
           "Per material action: actors in each role, conflict evaluation result and denial events.",
           "event-driven-automated", "per-event", prov=["action_id", "actor_ids", "role", "decision"])],
   qs=[
    Q("Reconciler independence", "Is the person or system that reconciles accounts independent of those who initiate, approve or release payments?",
      "Prevent one person hiding their own unauthorized payment.",
      "Misappropriation concealed by the person who also reconciles.",
      [UB("TVR-ORG-003"), COSO, S("SRC-AICPA-TSC", "CC5.1")], "industry-convention", "critical",
      alts=["Describe segregation of duties between payment processing and reconciliation."]),
    Q("Automation self-attestation", "Can the same automated process or AI agent that initiated a transaction also confirm it settled correctly?",
      "Avoid automation grading its own work.", "Systematic errors confirmed by the component that caused them.",
      [UB("GOV-AUTH-014"), S("SRC-OWASP-AGENTIC-AI")], "customer-preference", "high",
      ind=["donor-advised-funds", "financial-services", "enterprise-software"]),
    Q("Small-team compensation", "If a sponsor has too few finance staff for full segregation, what compensating controls does the platform provide?",
      "Make segregation workable for small sponsors.", "Segregation waived without compensating detection.",
      [UB("TVR-ORG-003"), COSO], "industry-convention", "medium",
      oq=["TVR-ORG-003-Q unresolved in Unbound."]),
    Q("Collusion detection", "What detective controls address collusion between payment and reconciliation roles (for example rotation, anomaly analytics)?",
      "Address risk not covered by segregation alone.", "Coordinated fraud by two insiders.",
      [UB("TVR-SEC-006")], "customer-preference", "medium"),
   ]),

AU("Independent attestation of reconciliation and auditor reliance",
   target=("The controller signs off reconciliation completeness monthly from a generated "
           "certification package. A risk-stratified sample of auto-passed items is "
           "independently attested each period, with sample size set by the controller "
           "from an error-bound method. Close certification is granted only when continuous "
           "invariants pass, material breaks are resolved and the sample is attested; "
           "manual close checklists are not required. Because a sponsor's auditor may rely "
           "on Unbound, the requirements call for SOC 1 Type 2 readiness from inception, a "
           "SOC 1 Type 2 covering ledger posting, NAV, reconciliation, change and access "
           "before the first hosted sponsor's fiscal year end, and generated reports carrying "
           "information-produced-by-entity support. Today there is no SOC 1 report, no "
           "auditor engagement and no attestation."),
   stmt=("Not available: Echelon has no SOC 1 or SOC 2 report and no independent attestation "
         "of reconciliation. Planned: SOC 1 Type 2 readiness and sample attestation are "
         "specified in Unbound requirements."),
   stmt_kind="not-available",
   reqs=["CNV-FIN-004", "RR-UNB-ACC-017-r1", "CNV-GOV-001", "UNB-XIN-ACC-009",
         "UNB-RCN-PLT-013", "SOC2-019", "SOC2-020"],
   oqs=["No CPA firm is engaged; the SOC 1 versus SOC 2 scope agreement required by "
        "UNB-RCN-PLT-013 has not been made.",
        "The error-bound sampling method for auto-passed items is not specified."],
   mech="periodic-automated", fresh="P1M", impl="high", rec="high",
   owner="Unassigned (proposed: Unbound CFO for SOC 1 readiness; sponsor Controller for sign-off)",
   challenge={
       "customer_intent": "An independent party confirms reconciliations are complete and accurate.",
       "adverse_outcome": "Auditor cannot rely on the platform; sponsor bears extra audit cost or receives a qualified opinion.",
       "conventional_control_effectiveness": "Reviewer initials on a monthly reconciliation provide weak evidence that review occurred; quality varies.",
       "legally_required": "No; auditor reliance follows AICPA standards for user auditors, not statute.",
       "contractually_required": "Often; sponsors and their auditors commonly require a SOC 1 Type 2 from fund accounting service providers.",
       "historical_convention": "Manual sign-off plus a SOC 1 Type 2 covering the service provider.",
       "architectural_elimination": "Not eliminable; independence must come from outside the system.",
       "automatic_enforcement": "Close certification gated on invariants, resolved material breaks and attested sample.",
       "continuous_evidence": "Generated certification package with population counts, query definitions, hashes and run logs.",
       "stronger_alternative": "Continuous evidence plus statistically sized independent sampling, with SOC 1 Type 2 as the external wrapper.",
       "alternative_verifiable": "Yes, if the auditor can re-perform population queries and the sample selection.",
       "customer_acceptance_likelihood": "Uncertain until a user auditor documents a planned approach that relies on it (CNV-GOV-001).",
       "invalidating_conditions": "Auditor declines to rely on system-generated evidence; IPE support not accepted.",
       "conventional_cost": "SOC 1 Type 2 engagement plus staff time for manual sign-offs.",
       "alternative_cost": "SOC 1 Type 2 is still required; savings are in reduced manual review effort.",
       "alternative_risks": "Sampling method challenged; reliance on generated reports without adequate IPE testing.",
       "supporting_arguments": ["Generated, reproducible evidence is easier to test than signatures.",
                                 "Sampling of auto-passed items addresses the risk that automation is wrong."],
       "opposing_arguments": ["A SOC 1 Type 2 is still the price of entry; continuous evidence does not replace it.",
                              "Early-stage vendor without any report will face reliance refusal regardless of design."],
       "technical_effectiveness": "stronger", "institutional_acceptance": "uncertain"},
   ctls=[C("Generated close certification package",
           "Produce per-period evidence that invariants pass, material breaks are resolved and the attested sample is complete, as the sole basis for close certification.",
           "preventive-gate", "L3-restricted-interface",
           related=["UNB-SCTRL-027", "UNB-CTRL-048", "SOC2-009"], frefs=[UB("RR-UNB-ACC-017-r1")]),
       C("Independent attestation of auto-passed sample",
         "A principal independent of the reconciliation configuration attests a risk-stratified sample of auto-passed matches each period.",
         "detective-manual", "L10-external-or-manual", related=["UNB-SCTRL-027"],
         frefs=[UB("CNV-FIN-004")]),
       C("SOC 1 Type 2 examination covering reconciliation",
         "Obtain an independent service auditor's SOC 1 Type 2 report covering reconciliation, ledger posting, NAV, change management and logical access.",
         "administrative", "L10-external-or-manual", systems=["External CPA firm (not engaged)"],
         frefs=[SOC1, UB("UNB-XIN-ACC-009")],
         residual=["No report exists; reliance unavailable until at least one full observation period completes."])],
   evrs=[E("Monthly reconciliation completeness certification",
           "Controller-signed certification with population counts, invariant results, open breaks and sample attestation reference.",
           "periodic-automated", "P1M", signing="Approver identity bound to certification event",
           disc="customer-only"),
         E("SOC 1 Type 2 report",
           "Independent service auditor report covering reconciliation and related ICFR controls.",
           "external-attestation", "P1Y", producer="not yet assigned (no CPA firm engaged)",
           indep="independent-third-party", disc="nda")],
   qs=[
    Q("Period sign-off", "Who signs off that reconciliations are complete and accurate each period, and what evidence supports the sign-off?",
      "Accountability for reconciliation completeness.", "Reconciliations marked complete without review.",
      [UB("CNV-FIN-004"), COSO], "industry-convention", "high"),
    Q("SOC 1 coverage", "Is reconciliation within the scope of a SOC 1 Type 2 report our auditor can rely on, and for what period?",
      "Allow the sponsor's auditor to rely on vendor controls.", "Additional substantive audit work or qualified opinion.",
      [SOC1, UB("UNB-XIN-ACC-009")], "certification-criteria", "critical",
      alts=["Provide your most recent SOC 1 report covering fund accounting and reconciliation.",
            "Is your reconciliation process tested by an independent service auditor?"]),
    Q("Sampling of automation", "How do you verify that automatically matched items were correctly matched, and how is the sample size determined?",
      "Detect systematic auto-match errors.", "Automation silently wrong across many items.",
      [UB("CNV-FIN-004"), S("SRC-AICPA-SOC2-GUIDE")], "customer-preference", "medium"),
    Q("Auditor re-performance", "Can our external auditor independently re-perform a reconciliation from the same source data, and with what access?",
      "Enable audit testing without reliance on the vendor's word.", "Unverifiable reconciliation claims.",
      [UB("MON-016"), UB("UNB-ACC-020")], "contractual-common", "high"),
   ]),

AU("Reconciliation evidence, reproducibility and retention",
   target=("For every reconciliation, Unbound retains the raw external feed exactly as "
           "received, normalized records with normalization version, source hashes, match "
           "decisions with rule version and the resulting breaks, all append-only. Any "
           "past reconciliation can be re-run as of its original known-at time and produce "
           "the same result, and projections rebuild deterministically from append-only "
           "evidence with checksum comparison. System-generated reconciliation reports "
           "carry information-produced-by-entity support (query definition, parameters, "
           "population counts, hash and run log). Folio renders reconciliation packs with "
           "immutable source references. Retention periods are set with counsel and the "
           "auditor; Unbound does not invent universal retention periods."),
   stmt=("Planned: raw-feed preservation, append-only reconciliation evidence and "
         "reproducible reports are specified. Strata (schema management) and Folio "
         "(document rendering) exist as Echelon tools but are not operated for any "
         "production Unbound service."),
   reqs=["UNB-CUST-012", "CNV-FIN-013", "UNB-NAV-044", "UNB-ACC-020", "SOC2-009",
         "SOC2-023", "CNV-GOV-001", "UNB-CUST-021", "UNB-NAV-051"],
   oqs=["UNB-NAV-051 requires Strata's append-only and ordering guarantees to be verified; "
        "the current-state brief records no verified Strata runtime query interface."],
   mech="continuous-automated", fresh="per-event",
   owner="Unassigned (proposed: Unbound evidence platform owner)",
   ctls=[C("Raw feed preservation and append-only evidence store",
           "Persist every external file or message exactly as received with hash, and append normalized and decision records without update or delete.",
           "preventive-structural", "L3-restricted-interface",
           systems=["Unbound (specified, not built)", "Strata (pilot; capability unverified)"],
           related=["UNB-SCTRL-040", "UNB-CTRL-047"], policies=["SEC-DB-001", "SEC-DATA-001"],
           frefs=[UB("UNB-CUST-012")]),
       C("Deterministic replay check",
         "Periodically rebuild reconciliation projections from append-only evidence and compare checksums with issued results.",
         "detective-automated", "L7-property-tested", related=["UNB-SCTRL-041"],
         frefs=[UB("UNB-NAV-044")])],
   evrs=[E("Reconciliation evidence bundle",
           "Raw source files, normalized records, match decisions, rule versions and IPE metadata for a reconciliation run.",
           "event-driven-automated", "per-event",
           prov=["content_sha256", "normalization_version", "rule_version", "query_definition", "population_count"],
           signing="Hash chain or signature (mechanism not yet chosen)", disc="auditor-only"),
         E("Replay comparison report", "Checksum comparison of rebuilt versus issued reconciliation results.",
           "periodic-automated", "P1M", disc="auditor-only")],
   qs=[
    Q("Evidence retained", "What evidence do you retain for each reconciliation (source files, match decisions, approvals), and can it be provided to auditors?",
      "Support audit and dispute resolution.", "Inability to prove how a balance was reconciled.",
      [UB("UNB-ACC-020"), S("SRC-AICPA-TSC", "CC7.2")], "industry-convention", "high"),
    Q("Reproducibility", "Can you reproduce a reconciliation as it existed on a past date, using the data known at that time, and obtain the same result?",
      "Allow later verification of past conclusions.", "Historical reconciliations that cannot be verified.",
      [UB("UNB-NAV-044"), UB("UNB-CUST-012")], "customer-preference", "medium"),
    Q("System report reliability", "How do you demonstrate the completeness and accuracy of system-generated reconciliation reports used as audit evidence?",
      "Meet auditor requirements for information produced by the entity.", "Audit evidence rejected as unreliable.",
      [UB("CNV-GOV-001"), SOC1], "certification-criteria", "high"),
    Q("Raw feed and retention", "Do you keep the original bank and custodian files as received, and for how long?",
      "Preserve primary evidence.", "Loss of original evidence after normalization.",
      [UB("CNV-FIN-013"), UB("SOC2-023"), S("SRC-SEC-ADVISERS-BOOKS-RECORDS")], "industry-convention", "medium",
      oq=["Retention period not set; SOC2-023 defers to auditor and counsel."]),
   ]),

AU("Reconciliation of uncertain outcomes, returns, reversals and migrations",
   target=("Each payment and collection rail has an Unknown-resolution protocol: status "
           "query by idempotency key at defined intervals, reconciliation against bank "
           "statements after the settlement window, and a defined evidence combination "
           "before declaring NotReceived; re-initiation reuses the original idempotency "
           "key. If NotReceived evidence cannot be obtained within the final aging tier, "
           "two independent treasury approvers may resolve by recorded decision with "
           "duplicate-risk acceptance. Returned or voided grant funds re-credit the "
           "originating fund via a linked compensating entry and capacity is restored only "
           "after reconciliation. A reversed contribution that already funded grants "
           "creates a donor receivable and sponsor exposure case, never a silent negative "
           "fund. Migrations from predecessor platforms reconcile staged balances before "
           "cutover."),
   stmt=("Planned: unknown-outcome, return and reversal reconciliation protocols are "
         "specified in Unbound requirements. Not implemented or tested."),
   reqs=["UNB-RCN-GRT-008", "UNB-RCN-WF-001", "UNB-RCN-WF-022", "UNB-RCN-GRT-015",
         "TVR-CON-003", "UNB-PAY-010", "UNB-EVT-006", "RR-REQ-X-061-r1", "UNB-TEN-013",
         "CNV-EXP-002"],
   mech="event-driven-automated", fresh="per-event", impl="high",
   owner="Unassigned (proposed: sponsor Treasury with Controller review)",
   ctls=[C("Unknown-outcome resolution protocol per rail",
           "Hold any payment with unknown outcome in an explicit state until evidence resolves it; forbid re-initiation except under the original idempotency key after proven NotSubmitted.",
           "preventive-structural", "L2-type-system", policies=["SEC-LANG-002"],
           related=["UNB-SCTRL-029"], frefs=[UB("UNB-RCN-GRT-008")]),
       C("Migration reconciliation gate",
         "Block cutover until staged balances, units and open items reconcile to the predecessor platform and parallel validation passes.",
         "preventive-gate", "L3-restricted-interface", frefs=[UB("RR-REQ-X-061-r1")])],
   evrs=[E("Unknown-outcome case record", "Status queries, bank evidence, resolution decision and approvers for each unknown payment or collection.",
           "event-driven-automated", "per-event"),
         E("Migration reconciliation report", "Source versus destination balances, units, lots and open items with differences and sign-off.",
           "event-driven-automated", "per-event", disc="customer-only")],
   qs=[
    Q("Unknown payment outcomes", "How do you reconcile a payment whose outcome is unknown (for example a timeout with the bank or processor) without risking a duplicate payment?",
      "Prevent duplicate or lost grant payments.", "Double payment or unpaid grantee.",
      [UB("UNB-RCN-GRT-008"), S("SRC-NACHA-RULES")], "industry-convention", "high",
      ind=["donor-advised-funds", "nonprofit", "banking"]),
    Q("Returns and voids", "How are returned ACH payments, rejected wires and voided checks reconciled back to the grant and the donor's fund?",
      "Correct fund balances after failed payments.", "Funds lost in suspense or double counted.",
      [UB("UNB-RCN-GRT-015"), S("SRC-NACHA-RULES")], "industry-convention", "high"),
    Q("Reversed contributions", "If a contribution is reversed after it has already funded a grant, how is the shortfall reconciled and who bears it?",
      "Understand exposure from reversible rails.", "Negative fund balances or unrecorded sponsor loss.",
      [UB("TVR-CON-003"), S("SRC-NACHA-RULES")], "customer-preference", "medium"),
    Q("Migration reconciliation", "When migrating funds from our current platform, how do you reconcile balances, units and history before cutover?",
      "Avoid losing or misstating funds during migration.", "Migration errors that corrupt opening balances.",
      [UB("RR-REQ-X-061-r1"), UB("UNB-TEN-013")], "contractual-common", "critical",
      alts=["What reconciliation evidence do you provide at conversion?"]),
   ]),
]

if __name__ == "__main__":
    print("RCN", build("RCN", units))
