from finlib import *

SOC1 = S("SRC-AICPA-SSAE-18", "AT-C 320")
TPRM = S("SRC-INTERAGENCY-TPRM-2023")
COSO = S("SRC-COSO-2013", "Principle 10")
IND = ["donor-advised-funds", "nonprofit", "wealth-management", "financial-services"]

units = [
AU("Custodian integration architecture, data integrity and freshness",
   target=("Unbound defines a custodian-neutral, versioned adapter contract covering account "
           "registration, positions, cash, transactions, prices, tax lots where available, "
           "corporate actions, fees, transfers and statements. Each integration declares a "
           "verified capability matrix (read-only feed, file import, manager-managed "
           "execution or API execution are separate profiles) and the system never infers "
           "trading or transfer permission from read access. Feeds arrive by polling, "
           "webhook, SFTP batch or secure statement with verifiable origin, freshness, "
           "deduplication, ordering and replay protection; every provider fact is appended "
           "with source, as-of time, received time, normalization version and hash, and "
           "corrections append superseding facts. Raw feeds are preserved. Provider "
           "credentials are scoped, rotated and stored as managed secrets. Core fund "
           "accounting and grant workflows do not require any particular custodian."),
   stmt=("Planned: a custodian-neutral adapter contract and integrity requirements are "
         "specified. No custodian integration exists today and Echelon has no custodian "
         "relationships or data licenses."),
   reqs=["UNB-CUST-001", "UNB-CUST-004", "UNB-CUST-005", "UNB-CUST-009", "UNB-CUST-012",
         "UNB-CUST-017", "UNB-CUST-018", "UNB-CUST-024", "UNB-CUST-026", "UNB-INV-032",
         "UNB-INV-033", "CNV-FIN-013"],
   oqs=["No custodian has been selected or contacted; data licensing and entitlement terms "
        "(UNB-CUST-017) are unknown.",
        "Whether target custodians sign or otherwise authenticate files is unknown."],
   impl="high", rec="medium",
   owner="Unassigned (proposed: Unbound integrations owner; sponsor Treasury for entitlements)",
   ctls=[C("Typed adapter boundary with schema validation",
           "Accept custodian data only through versioned typed adapter contracts with explicit schemas, size limits and origin verification; reject malformed or unverifiable input.",
           "preventive-structural", "L2-type-system", policies=["SEC-DATA-001", "SEC-LANG-001"],
           related=["UNB-CTRL-041"], frefs=[UB("UNB-CUST-009"), S("SRC-OWASP-ASVS", rel="informed-by")]),
       C("Provider capability matrix enforcement",
         "Permit only operations listed in the integration's verified capability profile; read-only integrations cannot emit instructions.",
         "preventive-structural", "L3-restricted-interface", policies=["SEC-AUTH-001"],
         related=["UNB-CTRL-040"], frefs=[UB("UNB-CUST-005"), UB("UNB-INV-033")]),
       C("Custodian credential management",
         "Store custodian credentials in managed secret storage with scoped service accounts and rotation.",
         "preventive-structural", "L3-restricted-interface", policies=["SEC-CRYPTO-001"],
         frefs=[UB("UNB-CUST-017")])],
   evrs=[E("Integration registry record", "Per provider: verified capability matrix, entitlements, freshness SLO, contract reference, owner and connection status.",
           "event-driven-automated", "per-event", disc="customer-only"),
         E("Feed integrity log", "Per received file or message: origin verification result, hash, sequence, duplicate or replay rejection.",
           "continuous-automated", "per-event", prov=["provider", "as_of", "received_at", "content_sha256", "normalization_version"])],
   qs=[
    Q("Supported custodians", "Which custodians and investment managers does your platform integrate with today, and by what method (API, file transfer, manual upload)?",
      "Confirm the sponsor's custodian can be supported.", "Unsupported custodian forcing manual workarounds.",
      [UB("UNB-CUST-003"), UB("UNB-INV-032")], "customer-preference", "high",
      alts=["List current custodian integrations and their production status."]),
    Q("Feed integrity", "How do you verify that custodian data is authentic, complete and not replayed or tampered with in transit?",
      "Trust in position and transaction data.", "Spoofed or altered custodian data driving balances.",
      [UB("UNB-CUST-009"), S("SRC-CSA-CCM-V4"), S("SRC-NIST-SP800-53-R5", "SI-10")], "industry-convention", "high"),
    Q("Data freshness", "How is the freshness of custodian data monitored and shown to staff and donors, and what happens when it exceeds limits?",
      "Avoid decisions on stale data.", "Grants or allocations based on outdated balances.",
      [UB("UNB-NAV-053"), UB("UNB-CUST-018")], "customer-preference", "medium"),
    Q("Custodian credentials", "How are credentials for custodian connections scoped, stored and rotated, and are they read-only where possible?",
      "Limit blast radius of credential compromise.", "Stolen credentials used to move assets.",
      [UB("UNB-CUST-017"), S("SRC-NIST-SP800-53-R5", "IA-5")], "industry-convention", "high",
      ind=["donor-advised-funds", "financial-services", "enterprise-software"]),
    Q("Custodian portability", "Is the platform tied to a particular custodian, or can we change custodians without changing fund accounting and grant workflows?",
      "Preserve the sponsor's freedom to change custodian.", "Lock-in raising cost or blocking prudent changes.",
      [UB("UNB-CUST-026"), TPRM], "customer-preference", "medium"),
    Q("Provider data corrections", "When a custodian restates or corrects previously sent data, how is the correction applied and is the original preserved?",
      "Keep an accurate and auditable history.", "Silent overwrites destroying audit trail.",
      [UB("UNB-CUST-012")], "industry-convention", "medium"),
   ]),

AU("Asset segregation, legal title and Unbound's non-custodial role",
   target=("Unbound never holds custody of donor or fund assets and never receives or holds "
           "donor or grant money; there are no operator, FBO or pooled accounts, and donor "
           "payments settle directly into sponsor-owned accounts through regulated "
           "processors. Assets are titled to the sponsoring organization at custodians the "
           "sponsor contracts. Each custody account records legal ownership, account title, "
           "restrictions and purpose; a DAF may map to segregated custody accounts, and an "
           "omnibus account supporting many DAFs must declare one attribution method "
           "(per-fund lot subaccounting or unitized) before accepting multi-fund "
           "allocations, with lot-owned positions reconciled per security to the custodian. "
           "Partner and sponsor isolation holds even when one custodian serves several "
           "partners; a provider account identifier is never a security boundary on its own. "
           "Unbound does not imply that a donor-specific account is donor-owned."),
   stmt=("Planned: Unbound's adopted convergence clause CNV-LEG-001 states that Unbound will "
         "not hold custody or donor money; assets remain in sponsor-owned accounts. This is a "
         "design commitment, not yet tested by a funds-flow conformance check."),
   reqs=["CNV-LEG-001", "UNB-CUST-002", "UNB-INV-002", "UNB-INV-011", "UNB-RCN-FIN-007",
         "UNB-CUST-019", "UNB-INV-041", "UNB-CUST-013", "UNB-CUST-028"],
   oqs=["The funds-flow conformance check in CNV-LEG-001 is specified but not built."],
   risks=["Omnibus attribution errors are internal to Unbound and only detectable through "
          "per-security reconciliation to the custodian."],
   mech="event-driven-automated", fresh="per-event",
   owner="Unassigned (proposed: Unbound product owner; sponsor legal for titling)",
   challenge={
       "customer_intent": "Donor assets cannot be lost or commingled through the technology vendor.",
       "adverse_outcome": "Vendor failure, fraud or insolvency affecting donor assets.",
       "conventional_control_effectiveness": "Conventional diligence reviews the vendor's custody controls, insurance and SOC reports when the vendor touches money.",
       "legally_required": "Custody and money-transmission rules apply if a vendor holds or transmits funds; avoiding that role avoids those regimes (interpretation; CNV-LEG-001).",
       "contractually_required": "Sponsors commonly require segregation and evidence of title.",
       "historical_convention": "Some DAF platforms operate FBO or pooled accounts through partners.",
       "architectural_elimination": "Yes within scope: Unbound has no account at which donor funds can arrive and no credentials to move them, so vendor custody risk is removed rather than controlled.",
       "automatic_enforcement": "Funds-flow conformance check blocks activation of any deployment that fails the non-custody tests.",
       "continuous_evidence": "Deployment configuration evidence that no operator-owned account or execution credential exists.",
       "stronger_alternative": "Non-custodial architecture plus per-security reconciliation to sponsor-titled accounts.",
       "alternative_verifiable": "Yes, by inspecting account titles, bank and custodian agreements and the conformance check result.",
       "customer_acceptance_likelihood": "Likely; sponsors already hold title, and fewer parties touching money is easy to explain.",
       "invalidating_conditions": "A sponsor asks Unbound to hold funds or credentials; a deployment model with operator accounts is introduced.",
       "conventional_cost": "Custody controls, crime insurance and audit scope for vendor-held funds.",
       "alternative_cost": "Lower; but sponsor must operate its own bank and custodian relationships.",
       "alternative_risks": "Instruction-relay paths could still be misused if sponsor delegation is too broad.",
       "supporting_arguments": ["Removes a whole class of vendor misappropriation risk.",
                                 "Avoids licensing regimes that apply to fund holders."],
       "opposing_arguments": ["Unbound still relays sponsor-authorized instructions, so an integrity failure in relay remains a risk.",
                              "Some sponsors want a turnkey provider that holds accounts."],
       "technical_effectiveness": "stronger", "institutional_acceptance": "likely"},
   ctls=[C("Funds-flow conformance check",
           "Before activation, verify the deployment has no operator-owned, FBO or pooled account and no Unbound credential able to execute a payment; block activation on failure.",
           "preventive-gate", "L1-eliminated-in-scope", related=["UNB-SCTRL-030"],
           frefs=[UB("CNV-LEG-001")],
           notes="L1 applies only to the scope 'Unbound-held funds'; relay of sponsor-authorized instructions is not eliminated."),
       C("Omnibus attribution declaration and per-security reconciliation",
         "Reject multi-fund allocation to any custody account without a declared attribution method; reconcile lot-owned positions per security to the custodian.",
         "preventive-structural", "L3-restricted-interface", related=["UNB-SCTRL-024"],
         frefs=[UB("UNB-RCN-FIN-007")]),
       C("Partner-scoped custody mapping",
         "Bind every custody account mapping to sponsor and partner tenant keys; never authorize by provider account identifier alone.",
         "preventive-structural", "L3-restricted-interface", policies=["SEC-AUTH-001"],
         frefs=[UB("UNB-CUST-019")])],
   evrs=[E("Funds-flow conformance result", "Per deployment: tests executed, account inventory, credential inventory and pass or fail.",
           "event-driven-automated", "per-event", disc="customer-only"),
         E("Custody account register", "Legal title, owner, purpose, restrictions and attribution method for every custody account.",
           "event-driven-automated", "per-event")],
   qs=[
    Q("Vendor custody", "Does your company ever hold, receive or control donor contributions, fund assets or grant money, including through FBO or pooled accounts?",
      "Determine whether vendor failure can affect assets.", "Vendor misappropriation or insolvency exposure.",
      [UB("CNV-LEG-001"), S("SRC-INTERAGENCY-TPRM-2023")], "industry-convention", "critical",
      alts=["Do you act as custodian or hold client funds?", "Do any client funds pass through accounts in your name?"], ind=IND),
    Q("Asset titling", "In whose name are custody accounts titled, and are DAF assets held in segregated accounts or omnibus accounts?",
      "Confirm legal ownership by the sponsor.", "Assets titled incorrectly or commingled.",
      [UB("UNB-CUST-002"), UB("UNB-INV-011")], "industry-convention", "high"),
    Q("Omnibus attribution", "For omnibus or pooled custody accounts, how do you attribute each fund's share and prove the attribution agrees with the custodian?",
      "Each fund's share is accurate.", "Misallocation between funds in an omnibus account.",
      [UB("UNB-RCN-FIN-007"), UB("UNB-INV-026")], "industry-convention", "high"),
    Q("Multi-sponsor segregation", "When the same custodian serves multiple sponsors or partners on your platform, how do you keep their custody data and instructions separate?",
      "Prevent cross-tenant exposure.", "Data leakage or misdirected instructions across sponsors.",
      [UB("UNB-CUST-019"), S("SRC-CSA-CCM-V4")], "customer-preference", "high",
      ind=["donor-advised-funds", "wealth-management", "enterprise-software"]),
    Q("Account identifier collisions", "Could a duplicated or reused custodian account number on your platform cause data or instructions to reach the wrong sponsor?",
      "Edge-case integrity of identifiers.", "Misrouted positions or instructions.",
      [UB("UNB-CUST-019")], "customer-preference", "medium"),
   ]),

AU("Custodian statements and statement of record",
   target=("Custodian statements and positions are the statement of record for assets held "
           "at the custodian; Unbound's fund statements are derived views that must reconcile "
           "to them. Contracts document the boundaries for custody, valuation reliance and "
           "statement of record. Custodian cash, positions, transactions, valuations and "
           "fees reconcile to the investment subledger, GL, bank evidence and "
           "available-to-recommend calculation. Corporate actions, income, splits and fees "
           "have deterministic posting rules and independent reconciliation. Where values "
           "come from the sponsor's external manager, a missing or stale manager price "
           "blocks the affected statement rather than being estimated. Folio renders "
           "custody reconciliation packs and fund statements with provenance references."),
   stmt=("Planned: custodian statements are intended to be the record for held assets, with "
         "Unbound statements reconciled to them. No statements exist today."),
   reqs=["UNB-CUST-010", "UNB-CUST-011", "UNB-CUST-016", "UNB-CUST-021", "UNB-CUST-025",
         "UNB-NAV-053", "CNV-FIN-005", "RR-REQ-X-032-r1"],
   oqs=["Whether donors receive custodian statements directly is a sponsor decision not "
        "captured in Unbound requirements."],
   owner="Unassigned (proposed: sponsor Controller)",
   ctls=[C("Custodian-to-subledger reconciliation",
           "Reconcile custodian positions, cash, transactions and fees to the investment subledger daily and before statement publication.",
           "detective-automated", "L9-runtime-monitored", related=["UNB-SCTRL-024", "UNB-CTRL-042"],
           frefs=[UB("UNB-CUST-010")]),
       C("Statement block on stale or missing manager price",
         "Block issuance of fund statements whose values rely on a missing or stale custodian or manager price.",
         "preventive-gate", "L3-restricted-interface", frefs=[UB("CNV-FIN-005")])],
   evrs=[E("Custody reconciliation pack", "Folio-rendered pack: custodian statement reference, subledger balances, differences and resolution.",
           "periodic-automated", "P1M", producer="not yet assigned (intended renderer: Folio, not operated for Unbound)")],
   qs=[
    Q("Statement of record", "For assets at the custodian, which record is authoritative: the custodian's statement or your platform's records?",
      "Clarity on which record governs disputes.", "Conflicting records with no agreed authority.",
      [UB("UNB-CUST-025"), S("SRC-SEC-ADVISERS-BOOKS-RECORDS")], "contractual-common", "high"),
    Q("Statement reconciliation", "How are custodian statements reconciled to the fund statements donors receive, and how often?",
      "Donor statements reflect real holdings.", "Donor statements diverging from custodian.",
      [UB("UNB-CUST-010"), COSO], "industry-convention", "high"),
    Q("Divergent statements", "If a donor sees a difference between your fund statement and a custodian or manager statement, how is it explained and resolved?",
      "Handle donor inquiries credibly.", "Loss of donor trust; undetected error.",
      [UB("UNB-CUST-011")], "customer-preference", "medium"),
    Q("Corporate actions and income", "How are dividends, interest, splits, mergers and custodian fees on custodian statements posted and reconciled?",
      "Completeness of investment accounting.", "Missed or misposted corporate actions.",
      [UB("UNB-CUST-016"), S("SRC-FASB-ASC-958")], "industry-convention", "medium"),
   ]),

AU("Custodian oversight: SOC 1 reliance and complementary user entity controls",
   target=("Unbound maintains a critical-vendor register recording each custodian's assurance "
           "type, legal entity, report period, scope, opinion, exceptions, subservice "
           "organizations and complementary user entity controls (CUECs). Every CUEC is "
           "mapped to an internal control owner (sponsor or Unbound) before the custodian is "
           "marked Assured. A bridge letter is required when the period end is more than 3 "
           "months old and assurance is marked Expired after 12 months (provisional defaults; "
           "the sponsor's auditor confirms reliance criteria); a bridge letter is never "
           "recorded as extending independent assurance. An adverse opinion or expired risk "
           "acceptance changes vendor status. AI may extract report metadata only for human "
           "confirmation. Unbound will in turn publish to each sponsor the CUECs derived "
           "from that sponsor's configuration."),
   stmt=("Planned: custodian SOC report review and CUEC mapping are specified. Echelon has "
         "no custodian relationships and has reviewed no custodian SOC reports."),
   reqs=["RR-REQ-X-073-r2", "UNB-XIN-ACC-009", "CNV-GOV-001", "SOC2-022", "UNB-RCN-PLT-013"],
   oqs=["The 3- and 12-month bridge-letter defaults are provisional monitoring values, not "
        "audit standards (RR-REQ-X-073-r2)."],
   mech="periodic-manual", autom="partial", fresh="P1Y",
   owner="Unassigned (proposed: sponsor vendor risk owner with Unbound support)",
   challenge={
       "customer_intent": "Confidence that the custodian's controls are effective and the sponsor performs its share.",
       "adverse_outcome": "Reliance on a custodian whose controls failed, or unperformed CUECs that void reliance.",
       "conventional_control_effectiveness": "Annual SOC 1 review is often a checklist exercise; CUECs are frequently acknowledged but not mapped to actual controls.",
       "legally_required": "No statute requires DAF sponsors to review custodian SOC reports; it is audit and supervisory practice.",
       "contractually_required": "Sometimes; auditors expect it for significant service organizations.",
       "historical_convention": "Annual collection of SOC reports and bridge letters.",
       "architectural_elimination": "Not eliminable; custodian controls are external.",
       "automatic_enforcement": "Vendor status changes automatically on expiry or adverse opinion; reliance flags propagate to affected reconciliations.",
       "continuous_evidence": "Independent daily reconciliation of custodian data partly substitutes for reliance on the custodian's internal controls over records.",
       "stronger_alternative": "Treat continuous independent reconciliation as primary detective evidence, with the SOC report as supporting evidence.",
       "alternative_verifiable": "Yes, via reconciliation logs.",
       "customer_acceptance_likelihood": "Uncertain: auditors still expect SOC review for custodians regardless of reconciliation.",
       "invalidating_conditions": "Reconciliation sources are themselves custodian-generated, so reconciliation cannot detect custodian-wide record falsification.",
       "conventional_cost": "Low to medium annual staff time.",
       "alternative_cost": "Reconciliation already required; incremental cost small.",
       "alternative_risks": "Overstating independence of reconciliation that depends on custodian data.",
       "supporting_arguments": ["CUEC-to-owner mapping makes reliance real rather than nominal."],
       "opposing_arguments": ["Reconciliation against custodian data is not independent of the custodian; the SOC 1 remains necessary.",
                              "Bridge letters provide management assertions, not assurance."],
       "technical_effectiveness": "equivalent", "institutional_acceptance": "uncertain"},
   ctls=[C("Critical-vendor assurance register with CUEC mapping",
           "Track custodian assurance reports, periods, opinions and exceptions; require each CUEC mapped to an owner before Assured status; expire assurance automatically.",
           "detective-automated", "L9-runtime-monitored", related=["UNB-SCTRL-044"],
           frefs=[UB("RR-REQ-X-073-r2"), SOC1]),
       C("Annual custodian SOC report review",
         "Qualified reviewer evaluates custodian SOC 1 Type 2 scope, exceptions and subservice carve-outs and records conclusions.",
         "detective-manual", "L10-external-or-manual", frefs=[SOC1, TPRM])],
   evrs=[E("Custodian assurance review record", "Report metadata, reviewer conclusions, exceptions, CUEC mapping and bridge-letter status per custodian.",
           "periodic-manual", "P1Y", disc="nda")],
   qs=[
    Q("Custodian SOC 1", "Do you obtain and review the SOC 1 Type 2 reports of the custodians your platform relies on, and how often?",
      "Oversight of critical subservice organizations.", "Undetected control failures at custodian.",
      [SOC1, TPRM, S("SRC-FFIEC-OUTSOURCING-BOOKLET")], "supervisory-guidance", "high",
      alts=["How do you oversee custodians as fourth parties?"], ind=IND),
    Q("CUEC mapping", "How are the complementary user entity controls listed in custodian SOC reports assigned to and performed by you or the sponsor?",
      "Reliance on custodian controls depends on CUECs.", "Unperformed CUECs invalidating reliance.",
      [UB("RR-REQ-X-073-r2"), SOC1], "certification-criteria", "high"),
    Q("Assurance gaps", "How do you handle gaps between a custodian's report period and our fiscal year end, qualified opinions or reported exceptions?",
      "Ensure reliance covers the relevant period.", "Reliance on outdated or qualified reports.",
      [UB("RR-REQ-X-073-r2"), S("SRC-AICPA-SOC2-GUIDE")], "certification-criteria", "medium"),
    Q("Subservice carve-outs", "Are the custodian's own subservice organizations carved out of its report, and how do you address them?",
      "Coverage of the full service chain.", "Uncovered fourth- or fifth-party risk.",
      [SOC1, S("SRC-NIST-SP800-161-R1")], "certification-criteria", "medium"),
    Q("Unbound CUECs", "Which complementary user entity controls will your platform expect our organization to perform for your controls to be effective?",
      "Know the sponsor's own obligations.", "Sponsor unaware of controls it must operate.",
      [UB("UNB-XIN-ACC-009"), UB("SOC2-022"), SOC1], "certification-criteria", "high",
      oq=["Unbound's own CUEC list is not yet drafted."]),
   ]),

AU("Trade and cash instructions to custodians",
   target=("Unbound does not execute: it never moves funds or releases an irreversible "
           "instruction using authority the sponsor has not delegated for that instruction. "
           "Where a custodian or manager contract permits, Unbound may relay sponsor-"
           "authorized instructions. Recommendations, orders, approvals, submission, "
           "acceptance, execution, partial fill, cancellation, rejection and settlement are "
           "distinct states. Cash transfers, liquidations, wires and securities transfers "
           "require independent authorization, payee or beneficiary verification, separation "
           "of duties, limits, idempotent instruction keys and provider settlement evidence. "
           "Grant payment instructions require Funded status or an approved, limit-checked "
           "liquidity advance. AI may propose but never originate or approve an instruction. "
           "In the Unbound test and simulation phase, live rail invocation is denied."),
   stmt=("Planned: instruction authority, distinct trade states and independent "
         "authorization are specified. Unbound cannot transmit any instruction today."),
   reqs=["UNB-CUST-007", "UNB-CUST-008", "UNB-INV-015", "UNB-INV-032", "CNV-LEG-001",
         "UNB-RCN-FIN-008", "UNB-RCN-WF-023", "UNB-INV-019", "UNB-INV-038"],
   oqs=["UNB-CUST-007 contemplates execution APIs with human authorization while CNV-LEG-001 "
        "forbids Unbound from routing orders for others' accounts; the boundary between "
        "permitted relay and prohibited execution needs counsel confirmation per custodian."],
   mech="event-driven-automated", fresh="per-event", impl="high",
   owner="Unassigned (proposed: sponsor Treasury)",
   ctls=[C("Typed instruction state machine with authorization gate",
           "Model each trade or cash instruction as an explicit state machine; transitions to Submitted require recorded sponsor authority, limits and independent approval.",
           "preventive-structural", "L2-type-system", policies=["SEC-LANG-002", "SEC-AUTH-001"],
           related=["UNB-SCTRL-023", "UNB-SCTRL-029", "UNB-CTRL-040"],
           frefs=[UB("UNB-CUST-007"), S("SRC-UCC-4A")]),
       C("Idempotent instruction keys",
         "Every external instruction carries a durable idempotency key; retries reuse it and duplicates are rejected.",
         "preventive-structural", "L3-restricted-interface", frefs=[UB("UNB-INV-038")]),
       C("Live rail invocation prohibition (pre-production)",
         "Deny any live custodian or payment rail call from non-production or unauthorized environments.",
         "preventive-gate", "L3-restricted-interface", related=["UNB-SCTRL-030"])],
   evrs=[E("Instruction authorization trail", "Per instruction: requester, approvers, authority reference, limits checked, idempotency key, provider acknowledgments and settlement evidence.",
           "event-driven-automated", "per-event", prov=["instruction_id", "idempotency_key", "authority_ref", "approver_ids"])],
   qs=[
    Q("Instruction capability", "Can your platform send trade or cash movement instructions to custodians, and if so under whose authority and contract?",
      "Know whether the vendor can move assets.", "Unauthorized asset movement via the vendor.",
      [UB("CNV-LEG-001"), UB("UNB-CUST-007")], "industry-convention", "critical", ind=IND),
    Q("Transfer authorization", "What authorization is required for a cash transfer, liquidation or wire out of custody (dual approval, limits, beneficiary verification)?",
      "Prevent unauthorized or fraudulent transfers.", "Fraudulent or erroneous outbound transfers.",
      [UB("UNB-CUST-008"), S("SRC-UCC-4A"), COSO], "industry-convention", "critical"),
    Q("Instruction integrity", "How do you prevent duplicate, altered or replayed instructions to a custodian?",
      "Ensure each instruction executes once as approved.", "Duplicate liquidations or tampered amounts.",
      [UB("UNB-INV-038"), S("SRC-OWASP-API-TOP10-2023")], "industry-convention", "high"),
    Q("AI-originated instructions", "Can an AI agent or automated process originate or approve a trade or transfer instruction?",
      "Human accountability for asset movements.", "Unsupervised automated movement of assets.",
      [UB("UNB-INV-019"), S("SRC-OWASP-AGENTIC-AI")], "customer-preference", "high",
      ind=["donor-advised-funds", "financial-services", "enterprise-software"]),
    Q("Liquidation for grants", "When investments must be sold to fund a grant, how do you confirm settlement before the grant payment is released?",
      "Avoid paying grants from unsettled proceeds.", "Overdraft or failed grant payment.",
      [UB("UNB-RCN-FIN-008"), UB("UNB-CUST-015")], "industry-convention", "high"),
   ]),

AU("Custodian outage, degraded modes and custodian transition",
   target=("Custodian outages, delayed feeds, revoked permissions, malformed files and account "
           "freezes trigger defined degraded modes: freshness warnings, scoped holds on "
           "affected reservations and statements, escalation, and no invented balances or "
           "unsafe transfers. The sponsor can freeze trading or allocation changes for "
           "custodian outage or valuation uncertainty. Valuations remain on hold or clearly "
           "provisional when source facts are unavailable. Custodian migrations preserve "
           "complete immutable history, account mappings, tax lots, open orders, "
           "restrictions and settlements, with overlapping read-only periods across "
           "managers. Because original feeds and append-only records are kept, fund-level "
           "holdings can be reconstructed independently of the custodian's systems."),
   stmt=("Planned: degraded modes and custodian transition requirements are specified. "
         "No outage has been experienced or tested."),
   reqs=["UNB-CUST-022", "UNB-INV-037", "UNB-INV-018", "UNB-CUST-023", "UNB-INV-009",
         "UNB-INV-008", "UNB-NAV-046", "CNV-PAY-007"],
   oqs=["No recovery drill (UNB-CUST-024) has been designed or run."],
   mech="event-driven-automated", fresh="per-event",
   owner="Unassigned (proposed: Unbound operations owner with sponsor Treasury)",
   ctls=[C("Degraded-mode state machine for custodian sources",
           "On outage or staleness, move the source to an explicit degraded state that holds dependent actions and shows freshness warnings.",
           "preventive-structural", "L2-type-system", policies=["SEC-LANG-002"],
           frefs=[UB("UNB-CUST-022")]),
       C("Custodian transition reconciliation",
         "Reconcile positions, lots and cash between outgoing and incoming custodians before activating the new mapping.",
         "preventive-gate", "L3-restricted-interface", frefs=[UB("UNB-CUST-023")])],
   evrs=[E("Degraded-mode event log", "Entry and exit of degraded states, affected funds, holds applied and escalations.",
           "event-driven-automated", "per-event"),
         E("Custodian recovery drill record", "Planned exercise of outage and transition scenarios with results.",
           "periodic-manual", "P1Y", notes="No drill designed yet.")],
   qs=[
    Q("Outage at period end", "What happens to statements, NAV and reconciliation if a custodian feed is unavailable at month or year end?",
      "Continuity of reporting.", "Incorrect or fabricated period-end values.",
      [UB("UNB-CUST-022"), S("SRC-FFIEC-BCM-BOOKLET")], "industry-convention", "high"),
    Q("Stale balance protection", "During a custodian outage, what prevents stale balances from being used to approve grants or allocations?",
      "Avoid decisions on outdated data.", "Over-commitment of fund assets.",
      [UB("UNB-NAV-046"), UB("CNV-PAY-007")], "echelon-internal", "high"),
    Q("Custodian change", "If we change custodians or investment managers, how is history, tax lot information and open activity preserved and reconciled?",
      "Smooth transitions without data loss.", "Lost cost basis or broken audit trail.",
      [UB("UNB-CUST-023"), UB("UNB-INV-009")], "customer-preference", "high"),
    Q("Account freeze or permission revocation", "How does the platform respond if a custodian freezes an account or revokes your data access?",
      "Predictable handling of provider actions.", "Silent data gaps or unsafe operations.",
      [UB("UNB-CUST-022"), UB("UNB-INV-018")], "customer-preference", "medium"),
    Q("Custodian failure reconstruction", "If a custodian failed or its records were unavailable, could the sponsor reconstruct each fund's holdings from your records?",
      "Resilience to severe custodian events.", "Inability to establish fund entitlements.",
      [UB("UNB-CUST-012"), S("SRC-FFIEC-BCM-BOOKLET")], "customer-preference", "medium"),
   ]),
]

if __name__ == "__main__":
    print("CUS", build("CUS", units, IND))
