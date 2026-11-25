from finlib import *

UP3 = S("SRC-UPMIFA", "Section 3")
UP5 = S("SRC-UPMIFA", "Section 5")
IA = S("SRC-SEC-ADVISERS-COMPLIANCE-RULE")
ASC = S("SRC-FASB-ASC-958")
COSO = S("SRC-COSO-2013", "Principle 10")
IND = ["donor-advised-funds", "nonprofit", "wealth-management", "financial-services"]
POOL_NOTE = ("CNV-LEG-001 (adopted) states that no sponsor-maintained investment pools will be "
             "offered and that values come from the sponsor's external manager or custodian; "
             "UNB-NAV-* and UNB-INV-003 nonetheless specify a full pool NAV and unitization "
             "engine. The answer follows CNV-LEG-001; the NAV engine applies only if a new "
             "owner decision reverses it.")

units = [
AU("Investment authority, regulatory boundary and adviser involvement",
   target=("Unbound is not an investment adviser and does not provide investment advice. It "
           "does not author fund- or donor-specific securities or allocation recommendations, "
           "construct models, select managers, route orders for others' accounts, take "
           "compensation varying with assets, trades or liquidations, or hold custody. Each "
           "sponsor delegates investment management to an external registered investment "
           "manager or custodian platform under a written agreement, and the sponsor board "
           "keeps the duties to select the manager, set its scope and investment policy and "
           "monitor performance and cost. Unbound records explicit investment authority "
           "(sponsor policy, investment committee, authorized manager, mandate, limits) and "
           "supports advisor-managed accounts and RIA relationships as delegated, scoped, "
           "time-bound and revocable permissions on named legal accounts. Donor and advisor "
           "preferences are recommendations or policy-permitted elections among options the "
           "sponsor's manager makes available, never trade authority. AI explanations of "
           "options are generated only from approved option metadata. Sponsor-maintained "
           "pools are not offered."),
   stmt=("Planned: Unbound's adopted design (CNV-LEG-001) keeps Echelon outside investment "
         "advice and custody; investment discretion stays with the sponsor and its external "
         "manager. Echelon has not obtained a legal opinion confirming this position."),
   reqs=["CNV-LEG-001", "UNB-CUST-006", "UNB-INV-006", "UNB-INV-013", "UNB-INV-016",
         "UNB-INV-019", "GOV-AUTH-007", "UNB-CUST-014", "UNB-ADV-001"],
   oqs=["CNV-LEG-001 labels its adviser and UPMIFA analysis 'interpretation'; no counsel "
        "opinion on Investment Advisers Act status is recorded.",
        POOL_NOTE],
   mech="event-driven-automated", fresh="per-event",
   owner="Unassigned (proposed: Echelon counsel for regulatory boundary; sponsor investment committee for authority)",
   ctls=[C("Investment authority register",
           "Record sponsor policy, investment committee delegation, manager mandate, account scope, limits, expiry and revocation for every investment authority; deny actions outside it.",
           "preventive-structural", "L3-restricted-interface", policies=["SEC-AUTH-001"],
           related=["UNB-CTRL-034", "UNB-SCTRL-023"], frefs=[UB("UNB-CUST-006")]),
       C("No-recommendation boundary for AI and product features",
         "Restrict AI and product content about investment options to approved option metadata; block generation of fund- or donor-specific securities or allocation recommendations.",
         "preventive-structural", "L3-restricted-interface", frefs=[UB("CNV-LEG-001")],
         residual=["Prompt or content drift could produce advice-like output; requires adversarial testing not yet designed."])],
   evrs=[E("Investment authority change log", "Creation, change, expiry and revocation of every delegation and mandate with approvers.",
           "event-driven-automated", "per-event"),
         E("Regulatory boundary legal opinion", "Counsel opinion on Investment Advisers Act and state adviser status of Unbound's relay and reporting functions.",
           "external-attestation", "P1Y", producer="not yet assigned (no counsel engaged)", indep="second-party", disc="nda")],
   qs=[
    Q("Adviser status", "Is your company, or any affiliate, a registered investment adviser, and does your platform provide investment advice to sponsors or donors?",
      "Understand regulatory status of the vendor.", "Unregistered advisory activity or conflicts.",
      [S("SRC-SEC-ADVISERS-COMPLIANCE-RULE"), UB("CNV-LEG-001")], "legal-regulatory", "high",
      auth="SEC; state securities regulators", jur=["US-federal", "US-states"],
      alts=["Does the platform make investment recommendations?"], ind=IND),
    Q("Investment discretion", "Who holds investment discretion over DAF assets on your platform, and how is that authority documented and limited?",
      "Clear accountability for investment decisions.", "Unauthorized investment actions.",
      [UB("UNB-CUST-006"), UP5], "industry-convention", "high"),
    Q("Donor recommendations versus authority", "How does the platform distinguish a donor's or advisor's investment recommendation from authority to trade?",
      "Preserve sponsor's exclusive legal control.", "Donor control undermining DAF status.",
      [UB("UNB-INV-013"), S("SRC-IRC-4966"), S("SRC-PPA-2006")], "legal-regulatory", "high",
      auth="IRS"),
    Q("Advisor-managed accounts", "How do you support advisor-managed or RIA-managed DAF accounts, including scope of delegation, expiry and revocation?",
      "Control of third-party advisors over fund assets.", "Advisor acting beyond authority after relationship ends.",
      [UB("UNB-INV-006"), UB("UNB-INV-016"), IA], "industry-convention", "high"),
    Q("AI investment output", "Can any AI feature generate security-level or allocation recommendations for a specific donor or fund?",
      "Avoid unregistered advice and unsuitable recommendations.", "AI output constituting advice.",
      [UB("CNV-LEG-001"), S("SRC-NIST-AI-RMF-1.0")], "customer-preference", "medium",
      ind=["donor-advised-funds", "wealth-management", "enterprise-software"]),
    Q("Sponsor investment pools", "Does your platform operate or administer sponsor-maintained commingled investment pools, and if so how are they structured legally?",
      "Understand securities law exposure of pooled vehicles.", "Pool structure triggering registration or disclosure duties.",
      [UB("CNV-LEG-001"), UB("UNB-INV-003")], "legal-regulatory", "medium", auth="SEC",
      oq=[POOL_NOTE, "Investment Company Act section 3(c)(10) source not seeded."]),
   ]),

AU("Allocation elections and rebalancing",
   target=("Donor allocation elections among sponsor-approved options are captured as "
           "versioned, effective-dated recommendations with minimums, eligibility, "
           "restrictions and target percentages, then relayed to the sponsor's manager under "
           "the sponsor's delegation. Each portfolio change distinguishes request, policy "
           "evaluation, sponsor decision, approved instruction, execution, settlement and "
           "reconciliation. Model portfolios are versioned targets separate from holdings "
           "and trade instructions. Rebalancing follows sponsor policy: drift detection, "
           "tolerance bands, restricted lists, pre-trade and post-trade compliance. "
           "Conflicting preferences among joint advisors follow a documented fund governance "
           "rule with no last-write-wins. Cutoffs are explicit and backdating is rejected. "
           "During a dispute freeze, standing policy and scheduled rebalancing continue but "
           "advisor-directed allocation changes are held."),
   stmt=("Planned: allocation and rebalancing workflows are specified; execution of "
         "rebalancing is the external manager's responsibility. Not implemented."),
   reqs=["UNB-INV-005", "UNB-INV-007", "UNB-INV-015", "UNB-INV-017", "UNB-INV-023",
         "UNB-INV-031", "UNB-INV-035", "CNV-ENT-002"],
   mech="event-driven-automated", fresh="per-event",
   owner="Unassigned (proposed: sponsor investment operations)",
   ctls=[C("Allocation election validation",
           "Validate each election against current menu, minimums, restrictions and effective date; reject backdated or ineligible elections.",
           "preventive-gate", "L3-restricted-interface", related=["UNB-CTRL-034"],
           frefs=[UB("UNB-INV-005"), UB("UNB-INV-023")]),
       C("Drift and post-trade compliance monitor",
         "Compare holdings reported by the manager to target allocations and policy limits; open exceptions for drift beyond tolerance.",
         "detective-automated", "L9-runtime-monitored", related=["UNB-CTRL-036"],
         frefs=[UB("UNB-INV-031")])],
   evrs=[E("Allocation election record", "Election, policy evaluation, sponsor decision, relayed instruction and manager confirmation per change.",
           "event-driven-automated", "per-event"),
         E("Drift exception report", "Funds or pools outside tolerance with age and resolution.", "continuous-automated", "P1D")],
   qs=[
    Q("Allocation elections", "How are donor allocation elections among investment options captured, approved and communicated to the investment manager?",
      "Accurate execution of permitted elections.", "Elections lost, misapplied or executed without approval.",
      [UB("UNB-INV-005"), UB("UNB-INV-015")], "industry-convention", "high", ind=IND),
    Q("Rebalancing", "Who initiates rebalancing, what drift tolerances apply, and what evidence shows rebalancing occurred as policy requires?",
      "Portfolios kept within policy.", "Unmanaged drift and policy breach.",
      [UB("UNB-INV-031"), UP3], "industry-convention", "medium"),
    Q("Conflicting instructions", "How are conflicting allocation instructions from joint advisors on one fund resolved?",
      "Fair and predictable governance.", "Last-write-wins overriding a co-advisor.",
      [UB("UNB-INV-017")], "customer-preference", "medium"),
    Q("Cutoffs and backdating", "What cutoff times govern allocation changes, and how do you prevent backdated effective dates?",
      "Prevent timing abuse.", "Selection of favorable historical prices.",
      [UB("UNB-INV-023"), UB("UNB-NAV-021")], "industry-convention", "high"),
    Q("Allocation during disputes", "What happens to scheduled rebalancing and allocation changes when a fund is frozen for a dispute, death or incapacity?",
      "Protect assets during contested periods.", "Unauthorized changes during disputes.",
      [UB("CNV-ENT-002"), UB("UNB-INV-018")], "customer-preference", "medium"),
   ]),

AU("Unitization, valuation inputs and NAV publication",
   target=("Under the adopted operating model, unit values and positions come from the "
           "sponsor's external manager or custodian and are reconciled to the custodian; "
           "Unbound derives fund-level valuations from those inputs and a missing or stale "
           "manager price blocks the affected statement rather than being estimated. "
           "In-tolerance fund-level valuations publish by deterministic policy only under a "
           "recorded investment-committee delegation that approves tolerances and pricing "
           "sources, reviewed at least annually; out-of-tolerance, stale, missing or "
           "overridden prices route to a human approver before publication, and a risk-based "
           "independent sample is reviewed the next business day. Without a delegation every "
           "valuation requires a human checker. Valuation states (Draft, InputsValidated, "
           "Calculated, ExceptionHold, IndependentlyReviewed, Approved, Published, "
           "Superseded, Rejected) make publication a controlled act. Authoritative monetary "
           "and unit arithmetic uses fixed-precision decimal with specified rounding and "
           "residual allocation, never binary floating point; F# decimal types make this the "
           "default. Subscriptions and redemptions use forward pricing with explicit trade, "
           "valuation and settlement dates so no participant or agent can select a known "
           "historical price."),
   stmt=("Planned: valuation inputs from the sponsor's external manager, controlled "
         "publication and fixed-precision arithmetic are specified. No valuation has been "
         "calculated or published."),
   reqs=["CNV-FIN-005", "CNV-LEG-001", "UNB-NAV-003", "UNB-NAV-004", "UNB-NAV-005",
         "UNB-NAV-006", "UNB-NAV-007", "UNB-NAV-008", "UNB-NAV-011", "UNB-NAV-021",
         "UNB-NAV-022", "UNB-NAV-025", "UNB-INV-022", "UNB-INV-023"],
   oqs=[POOL_NOTE],
   owner="Unassigned (proposed: sponsor Fund Controller under investment committee delegation)",
   challenge={
       "customer_intent": "Unit values and fund values are correct before donors see them.",
       "adverse_outcome": "Wrong values drive wrong grants, fees and statements.",
       "conventional_control_effectiveness": "Daily human maker-checker sign-off on every NAV is common but becomes rubber-stamping when values are routinely in tolerance.",
       "legally_required": "No statute prescribes NAV review for DAF sponsor-level valuations; registered fund rules do not apply to this model.",
       "contractually_required": "Auditors and sponsors expect documented review of valuations.",
       "historical_convention": "Human checker signs every NAV strike.",
       "architectural_elimination": "Partly: manual arithmetic error is removed by deterministic calculation with decimal types; price-input error is not.",
       "automatic_enforcement": "Publication is a gated state transition; out-of-tolerance and stale inputs cannot publish without human approval.",
       "continuous_evidence": "Each valuation records inputs, high-water marks, rule version and reviewer.",
       "stronger_alternative": "Delegated deterministic publication for in-tolerance values plus next-day independent sample and mandatory human review of exceptions.",
       "alternative_verifiable": "Yes, from valuation records and the delegation record.",
       "customer_acceptance_likelihood": "Uncertain; depends on the investment committee recording a delegation and the auditor accepting it.",
       "invalidating_conditions": "Tolerances too wide; pricing source compromised; delegation lapses unnoticed.",
       "conventional_cost": "Daily staff review time per pool or option.",
       "alternative_cost": "Lower recurring review; build cost for tolerance engine.",
       "alternative_risks": "Correlated input error across all values that stays within tolerance.",
       "supporting_arguments": ["Human attention is focused on exceptions where error is likely.",
                                 "Arithmetic error is removed structurally."],
       "opposing_arguments": ["Without operating history, tolerance calibration is guesswork.",
                              "Some sponsors and auditors will insist on daily human sign-off."],
       "technical_effectiveness": "equivalent", "institutional_acceptance": "uncertain"},
   ctls=[C("Controlled valuation publication state machine",
           "Publish a valuation only via a gated transition requiring validated inputs, tolerance check and either a recorded delegation or human approval.",
           "preventive-gate", "L2-type-system", policies=["SEC-LANG-002"],
           related=["UNB-SCTRL-021", "UNB-CTRL-037", "UNB-CTRL-039"],
           frefs=[UB("UNB-NAV-005"), UB("CNV-FIN-005")]),
       C("Fixed-precision decimal money and unit types",
         "Represent all authoritative monetary and unit values with fixed-precision decimal types and explicit rounding; prohibit binary floating point in these paths.",
         "preventive-structural", "L2-type-system", systems=["Unbound (specified, not built); F# decimal type"],
         policies=["SEC-LANG-001", "SEC-LANG-002"], frefs=[UB("UNB-NAV-022")]),
       C("Valuation determinism property tests",
         "Property-test that valuations, unit issuance and redemption are reproducible from the same inputs and conserve totals within residual policy.",
         "detective-automated", "L7-property-tested", frefs=[UB("UNB-NAV-044")])],
   evrs=[E("Valuation record", "Inputs, sources, high-water marks, rule and code version, tolerance result, reviewer or delegation reference, publication event.",
           "event-driven-automated", "per-event",
           prov=["valuation_id", "as_of", "price_source_versions", "rule_version", "reviewer_or_delegation"]),
         E("Investment committee delegation record", "Approved tolerances, pricing sources, scope and review date.",
           "periodic-manual", "P1Y", producer="Sponsor investment committee (not yet assigned)", indep="first-party", disc="customer-only")],
   qs=[
    Q("Unit value source", "How are unit values or NAVs for each investment option determined, and who calculates them?",
      "Understand valuation responsibility.", "Unclear accountability for valuation errors.",
      [UB("CNV-FIN-005"), UB("UNB-NAV-003"), ASC], "industry-convention", "high", ind=IND,
      alts=["Describe your NAV calculation process."]),
    Q("NAV approval", "What review and approval occurs before a NAV or unit value is published to donors?",
      "Prevent publication of erroneous values.", "Wrong values reaching donors and grants.",
      [UB("UNB-NAV-008"), COSO], "industry-convention", "high"),
    Q("Arithmetic precision", "What numeric precision and rounding rules apply to unit and monetary calculations, and how are rounding residuals handled?",
      "Avoid systematic rounding drift.", "Accumulated rounding errors and unbalanced totals.",
      [UB("UNB-NAV-022"), UB("UNB-INV-029")], "customer-preference", "medium",
      ind=["donor-advised-funds", "financial-services", "enterprise-software"]),
    Q("Forward pricing", "How do you prevent a donor, advisor or automated agent from transacting at a known, favorable historical unit price?",
      "Fairness among participants.", "Dilution of other funds through stale-price arbitrage.",
      [UB("UNB-NAV-021"), UB("UNB-INV-023")], "industry-convention", "high"),
    Q("Pending transactions", "How are pending subscriptions and redemptions treated before their strike point so they do not distort unit counts?",
      "Accurate unit counts.", "Circular or premature unit recognition.",
      [UB("UNB-NAV-025")], "industry-convention", "medium"),
    Q("Missing prices", "What value is shown and used when a price is missing or stale on a valuation date?",
      "No fabricated or zero values.", "Silent forward-filled or zero prices.",
      [UB("UNB-NAV-046"), UB("UNB-NAV-015")], "industry-convention", "high"),
   ]),

AU("Valuation errors, corrections and remediation",
   target=("Corrected valuations are new approved publications linked to the original, "
           "recording cause class (source price error, missed position, late trade, "
           "corporate action, FX, fee accrual, cutoff, unit allocation, fraud or "
           "unauthorized override), affected period, funds, materiality, reviewer and "
           "remediation plan. Counterfactual unit and money impacts are calculated for every "
           "affected fund, transaction, grant, fee and statement; a sponsor-approved "
           "materiality and remediation policy decides compensation, restatement, unit "
           "adjustment, corrected statements and escalation to auditor. Settled transfers "
           "and historical unit issuance are never overwritten; corrective events are "
           "appended. Closed-period corrections require separate restatement authority and "
           "the originally issued reports remain reproducible. Propagation is idempotent, "
           "bounded and approval-gated."),
   stmt=("Planned: correction lineage, impact analysis and remediation policy are "
         "specified. No correction policy has been approved by any sponsor."),
   reqs=["UNB-NAV-010", "UNB-NAV-018", "UNB-NAV-038", "UNB-NAV-039", "UNB-NAV-040",
         "UNB-NAV-041", "UNB-NAV-042", "UNB-NAV-043", "UNB-NAV-045", "RR-UNB-DATA-005-r1"],
   oqs=["Materiality thresholds for compensating funds are sponsor policy and are not set."],
   mech="event-driven-automated", fresh="per-event", impl="high",
   owner="Unassigned (proposed: sponsor Fund Controller)",
   ctls=[C("Correction impact registry and bounded propagation",
           "Map each correctable fact to derived records; compute impacts and require approval before propagating corrections.",
           "corrective", "L3-restricted-interface", related=["UNB-SCTRL-022", "UNB-CTRL-038"],
           frefs=[UB("RR-UNB-DATA-005-r1"), UB("UNB-NAV-045")])],
   evrs=[E("Valuation correction case", "Original and corrected values, cause class, impact analysis, materiality decision, remediation and approvals.",
           "event-driven-automated", "per-event", disc="customer-only")],
   qs=[
    Q("Error policy", "What is your policy when a NAV or unit value error is discovered, including materiality thresholds and compensation to affected funds?",
      "Fair remediation of errors.", "Donors or funds bearing losses from vendor or manager errors.",
      [UB("UNB-NAV-041")], "industry-convention", "high", ind=IND),
    Q("Original reports preserved", "After a valuation correction, can the originally published statements and values still be reproduced exactly as issued?",
      "Auditability of what donors were told.", "Rewritten history.",
      [UB("UNB-NAV-010"), UB("UNB-NAV-043")], "industry-convention", "medium"),
    Q("Downstream impact", "How do pricing corrections flow through to fees, grant amounts, statements and performance figures?",
      "Complete remediation.", "Partial corrections leaving related figures wrong.",
      [UB("UNB-NAV-018"), UB("UNB-NAV-040")], "customer-preference", "medium"),
    Q("Closed-period corrections", "Who may approve a valuation correction affecting a closed accounting period, and how is it recorded?",
      "Control over restatements.", "Unauthorized restatement of audited periods.",
      [UB("UNB-NAV-043"), UB("CNV-FIN-011")], "industry-convention", "medium"),
   ]),

AU("Investment policy compliance, liquidity and concentration",
   target=("Sponsor investment policies and exceptions are versioned, effective-dated and "
           "linked to decisions and reporting evidence. Policy defines menus, prohibited "
           "investments, concentration limits, liquidity thresholds, rebalancing tolerance, "
           "manager eligibility and escalation. Pre-trade and post-trade compliance checks "
           "run against holdings reported by the manager. Each fund's external investments "
           "are backed by a sponsor-approved liquidity buffer at the custodian derived from "
           "a documented stress model (net outflow over the settlement horizon including the "
           "December peak); a fixed percentage is allowed only as a labeled placeholder "
           "until twelve months of outflow data exist. No display implies unsettled or "
           "illiquid assets are spendable. Business-enterprise holdings are computed with "
           "related persons before accepting a business interest and on later transactions "
           "to track excess business holdings disposal periods. The sponsor can freeze "
           "trading for compliance holds, valuation uncertainty or liquidity stress."),
   stmt=("Planned: policy versioning, liquidity buffer modeling and holdings tests are "
         "specified. No policy has been loaded or monitored."),
   reqs=["UNB-INV-014", "UNB-INV-020", "UNB-INV-030", "UNB-INV-031", "UNB-INV-018",
         "CNV-FIN-001", "UNB-NAV-036", "UNB-RCN-FIN-004", "UNB-INV-024", "UNB-INV-035"],
   oqs=["IRC section 4943 (excess business holdings) is relevant but not in the seeded source list."],
   owner="Unassigned (proposed: sponsor investment committee with compliance owner)",
   ctls=[C("Policy limit monitor",
           "Evaluate reported holdings against versioned policy limits (prohibited assets, concentration, liquidity) and open exceptions.",
           "detective-automated", "L9-runtime-monitored", related=["UNB-CTRL-036"],
           frefs=[UB("UNB-INV-014"), UP3]),
       C("Liquidity buffer gate",
         "Prevent grant funding plans that would breach the approved liquidity buffer without approval.",
         "preventive-gate", "L3-restricted-interface", frefs=[UB("CNV-FIN-001")]),
       C("Excess business holdings computation",
         "Compute combined holdings with related persons at acceptance and on related transactions; track disposal deadlines.",
         "detective-automated", "L9-runtime-monitored", frefs=[UB("UNB-RCN-FIN-004"), S("SRC-PPA-2006")])],
   evrs=[E("Investment policy compliance report", "Limits evaluated, breaches, exceptions approved and their expiry.", "continuous-automated", "P1D", disc="customer-only"),
         E("Liquidity stress model record", "Model version, assumptions, outflow data and approved buffer.", "periodic-manual", "P1Y")],
   qs=[
    Q("IPS compliance", "How do you monitor compliance with the sponsor's investment policy statement, and how are breaches reported?",
      "Board oversight of investment policy.", "Undetected policy breaches.",
      [UB("UNB-INV-014"), UP3], "industry-convention", "high", ind=IND),
    Q("Liquidity for grants", "How do you ensure enough liquidity exists to pay approved grants on time, including at year-end peaks?",
      "Grants paid when promised.", "Delayed grants or forced sales.",
      [UB("CNV-FIN-001"), UB("UNB-INV-030")], "industry-convention", "high"),
    Q("Concentration and business holdings", "How are concentrated positions and contributed business interests monitored for excess business holdings rules?",
      "Avoid excise taxes on the sponsor.", "Excess business holdings penalties.",
      [UB("UNB-RCN-FIN-004"), S("SRC-PPA-2006")], "legal-regulatory", "high", auth="IRS",
      oq=["IRC 4943 source not seeded."]),
    Q("Policy exceptions", "How are investment policy exceptions requested, approved, time-limited and recorded?",
      "Controlled deviations.", "Permanent informal exceptions.",
      [UB("UNB-INV-020")], "industry-convention", "medium"),
    Q("Policy versioning", "When the investment policy changes, how is the effective date applied and the prior version retained?",
      "Clear history of governing policy.", "Ambiguity over which policy applied.",
      [UB("UNB-INV-020"), COSO], "industry-convention", "low"),
   ]),

AU("Prudent investment governance support (UPMIFA) and performance and cost reporting",
   status="proposed-target-state",
   target=("Unbound supports, but does not perform, the sponsor board's prudence duties. "
           "Under CNV-LEG-001 the board selects the external manager, sets scope and "
           "investment policy and monitors performance and cost; Unbound provides "
           "decision records (delegations, policy versions, manager reviews, exceptions) and "
           "reports with explicit methodology: time-weighted versus money-weighted returns, "
           "benchmarks, gross and net of fees, cash-flow timing and as-of dates, and never "
           "presents accounting gains as performance. Manager fees, pool fees and fund "
           "charges are shown without double counting so the board can assess cost "
           "reasonableness. Whether UPMIFA applies to a sponsor's DAF assets, and whether any "
           "fund is an endowment fund subject to its spending provisions, is a counsel "
           "determination per state; Unbound requirements contain no explicit UPMIFA "
           "requirement."),
   stmt=("Planned: performance and cost reporting with explicit methodology is specified. "
         "Unbound has no UPMIFA-specific requirement; applicability to DAF assets has not "
         "been analyzed by counsel."),
   reqs=["CNV-LEG-001", "UNB-CUST-027", "UNB-INV-028", "UNB-NAV-037", "UNB-INV-036",
         "UNB-INV-040", "UNB-INV-020"],
   oqs=["Gap: no Unbound requirement addresses UPMIFA directly (only a parenthetical "
        "'interpretation' in CNV-LEG-001). Needed: counsel analysis of UPMIFA section 3 "
        "prudence and section 5 delegation applicability per state, and whether any "
        "account type (for example designated or endowment-type funds) needs spending-policy "
        "support.",
        "GIPS or other performance standard alignment is not specified; source not seeded."],
   mech="periodic-automated", fresh="P3M",
   owner="Unassigned (proposed: sponsor investment committee; Unbound reporting owner)",
   challenge={
       "customer_intent": "The board can show it invested prudently and monitored manager performance and cost.",
       "adverse_outcome": "Board unable to evidence prudence; unreasonable costs go unnoticed.",
       "conventional_control_effectiveness": "Quarterly manager reports reviewed by investment committee; quality depends on consultant.",
       "legally_required": "For charities subject to UPMIFA, the prudence standard is law; its application to DAF assets is not established here.",
       "contractually_required": "Not typically.",
       "historical_convention": "Investment consultant reports and committee minutes.",
       "architectural_elimination": "Not eliminable; prudence is a judgment.",
       "automatic_enforcement": "Policy reviews and manager reviews can be scheduled with overdue escalation.",
       "continuous_evidence": "Decision records linking delegation, policy versions and reviews.",
       "stronger_alternative": "Machine-linked decision record of selection, scope, monitoring and cost review.",
       "alternative_verifiable": "Yes, through retained decision records.",
       "customer_acceptance_likelihood": "Likely as support; the board remains responsible.",
       "invalidating_conditions": "Counsel concludes UPMIFA requires processes not captured.",
       "conventional_cost": "Consultant fees and committee time.",
       "alternative_cost": "Reporting build cost.",
       "alternative_risks": "Tool output mistaken for the board's own judgment.",
       "supporting_arguments": ["Structured records make prudence evidence durable."],
       "opposing_arguments": ["A platform cannot make a board prudent; the value is documentation only.",
                              "Applicability uncertainty means requirements may be over or under built."],
       "technical_effectiveness": "unknown", "institutional_acceptance": "likely"},
   ctls=[C("Performance methodology declaration",
           "Every performance report declares return method, benchmark, fee basis, cash-flow treatment and as-of date; reports lacking any element are rejected.",
           "preventive-gate", "L3-restricted-interface", frefs=[UB("UNB-INV-028"), UB("UNB-NAV-037")]),
       C("Investment governance review schedule",
         "Schedule and track manager reviews, policy reviews and delegation renewals with overdue escalation.",
         "detective-automated", "L9-runtime-monitored", frefs=[UP5])],
   evrs=[E("Manager performance and cost report", "Folio report with declared methodology, gross and net returns, benchmarks and all fee layers.",
           "periodic-automated", "P3M", producer="not yet assigned (intended renderer: Folio)"),
         E("Investment governance decision record", "Manager selection, scope, policy approvals and review minutes references.",
           "event-driven-automated", "per-event", producer="Sponsor board (not yet assigned)")],
   qs=[
    Q("UPMIFA support", "How does your platform help our board document prudent investment decision-making and delegation as required by applicable state law?",
      "Evidence of board prudence.", "Board unable to show compliance with prudence standard.",
      [UP3, UP5], "legal-regulatory", "medium", jur=["US-states"],
      auth="State attorneys general", oq=["No Unbound UPMIFA requirement."], ind=["donor-advised-funds", "nonprofit"]),
    Q("Performance reporting", "How are investment performance figures calculated (time-weighted, money-weighted, gross or net of fees), and is the methodology disclosed?",
      "Comparable, honest performance reports.", "Misleading performance claims.",
      [UB("UNB-INV-028"), UB("UNB-NAV-037")], "industry-convention", "medium", ind=IND),
    Q("Endowment-type funds", "Do you support funds that require a spending policy or endowment treatment alongside DAFs, and how are they distinguished?",
      "Correct treatment by fund type.", "Applying DAF rules to endowments or vice versa.",
      [S("SRC-UPMIFA", "Section 4"), UB("UNB-RCN-ENT-011")], "legal-regulatory", "low", jur=["US-states"],
      oq=["No Unbound spending-policy requirement located."]),
    Q("Investment cost transparency", "Can the board see total investment cost per option, including manager fees, fund expense ratios and sponsor charges, without double counting?",
      "Assess cost reasonableness.", "Hidden or duplicated costs.",
      [UB("UNB-INV-036"), UP3], "industry-convention", "medium"),
   ]),

AU("Valuation of illiquid and non-cash assets",
   target=("Valuation methodology is defined per asset class and structure. A pricing "
           "hierarchy (independent market feed, custodian mark, approved valuation service, "
           "documented manual appraisal, or explicit hold) has policy-controlled precedence "
           "and freshness limits. Illiquid valuations require appraisal methodology, "
           "approval, uncertainty range where meaningful, age limits and valuation-event "
           "triggers, marked provisional where policy permits. Stale, conflicting, missing or "
           "outlier prices create exceptions with severity and reviewer decision; prices are "
           "never silently forward-filled, and provider observations are evidence, not "
           "automatically approved marks. Continuously traded assets record exact UTC "
           "timestamp, valuation convention and source; contributed crypto above "
           "counsel-set thresholds is flagged for donor qualified appraisal. The donor's tax "
           "appraisal, the sponsor's book value and proceeds are separate typed values. "
           "In-kind workflows record asset classification, completed-gift rule, acceptance "
           "decision, holdings test and liquidation policy before acceptance."),
   stmt=("Planned: illiquid and non-cash valuation rules are specified. Unbound has never "
         "valued an asset."),
   reqs=["UNB-NAV-013", "UNB-NAV-015", "UNB-NAV-017", "UNB-NAV-019", "UNB-INV-021",
         "UNB-INV-012", "RR-UNB-INV-012-r1", "UNB-RCN-FIN-011", "UNB-GAP-012",
         "RR-UNB-ACC-006-r1", "UNB-NAV-016"],
   oqs=["FASB ASC 820 (fair value) is relevant but not seeded."],
   mech="event-driven-automated", fresh="per-event",
   owner="Unassigned (proposed: sponsor Controller with valuation committee)",
   ctls=[C("Pricing hierarchy and exception engine",
           "Select prices by approved hierarchy and freshness limits; raise exceptions for stale, conflicting, missing or outlier prices; prohibit silent forward-fill.",
           "detective-automated", "L9-runtime-monitored", related=["UNB-SCTRL-021"],
           frefs=[UB("UNB-NAV-013"), UB("UNB-NAV-015")]),
       C("Illiquid valuation approval",
         "Require documented methodology, approver and age limit for each illiquid valuation; expire and re-trigger on age or event.",
         "preventive-gate", "L10-external-or-manual", frefs=[UB("UNB-NAV-017")])],
   evrs=[E("Illiquid valuation file", "Methodology, appraiser or source, uncertainty range, approver and expiry per asset.",
           "event-driven-automated", "per-event", disc="customer-only")],
   qs=[
    Q("Illiquid valuation", "How are illiquid assets such as private company stock, real estate or limited partnership interests valued, and how often?",
      "Reasonable values for hard-to-value assets.", "Overstated fund values or misleading statements.",
      [UB("UNB-NAV-017"), ASC], "industry-convention", "high", ind=IND),
    Q("Pricing hierarchy", "What pricing sources do you use, in what order of precedence, and what freshness limits apply?",
      "Consistent valuation inputs.", "Arbitrary or stale pricing.",
      [UB("UNB-NAV-013")], "industry-convention", "medium"),
    Q("Tax versus book value", "How do you keep the donor's appraised value for tax purposes separate from the sponsor's book value and sale proceeds?",
      "Avoid implying the sponsor endorses donor valuations.", "Sponsor appearing to vouch for deduction amounts.",
      [UB("UNB-GAP-012"), S("SRC-IRC-170", "170(f)(11)"), S("SRC-IRS-PUB-1771")], "legal-regulatory", "high", auth="IRS"),
    Q("Digital asset valuation", "How are contributed digital assets valued (timestamp, price source, convention), and when is a qualified appraisal flagged?",
      "Accurate crypto gift valuation.", "Mis-valued crypto gifts and deduction disputes.",
      [UB("UNB-RCN-FIN-011"), S("SRC-IRC-170")], "legal-regulatory", "medium", auth="IRS"),
    Q("Price exceptions", "What happens when prices for a holding are stale, conflicting or outliers?",
      "Detect bad prices.", "Silent use of wrong prices.",
      [UB("UNB-NAV-015"), UB("UNB-NAV-019")], "industry-convention", "medium"),
   ]),
]

if __name__ == "__main__":
    print("INV", build("INV", units, IND))
