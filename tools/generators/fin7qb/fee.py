from finlib import *

LAND = S("SRC-ECH-DAF-LANDSCAPE", rel="informed-by", basis="directly-documented")
COSO = S("SRC-COSO-2013", "Principle 10")
TSC_PI = S("SRC-AICPA-TSC", "PI1.3")
IND = ["donor-advised-funds", "nonprofit", "wealth-management", "financial-services"]

units = [
AU("Fee schedule definition, versioning and cost basis",
   target=("Every fee schedule is an approved, effective-dated version that declares its "
           "FeeBase contract: measurement basis (end-of-day market value by default; "
           "average daily, period-end or quarter-average options), inclusions and "
           "exclusions, valuation version, tier method, day count, accrual and settlement "
           "cadence, minimums, waivers, payer source, recipient type, service identity and "
           "treatment of reserved-but-uncommunicated grants. Accrued unpaid fees and fees "
           "already embedded in pool or manager NAV are excluded from any base. A schedule "
           "that sets a minimum annual fee or minimum balance must reference a current cost "
           "basis record (no older than 13 months) and either stay within a configured "
           "ratio to fully allocated cost or record a disclosed non-cost rationale. "
           "Schedules are scoped per sponsor, partner and program and never leak across "
           "partners."),
   stmt=("Planned: versioned fee schedules with declared fee bases are specified. No fee "
         "schedule has been configured or charged."),
   reqs=["CNV-FIN-002", "UNB-RCN-FIN-005", "UNB-NAV-032", "ADM-027", "UNB-SMP-ECN-001",
         "UNB-ACC-010", "RR-ADM-027-r1"],
   mech="event-driven-automated", fresh="per-event",
   owner="Unassigned (proposed: sponsor Controller; Unbound fee engine owner)",
   ctls=[C("FeeBase contract validation at schedule approval",
           "Reject publication of a fee schedule version missing any required FeeBase element or a current cost basis where minimums apply.",
           "preventive-gate", "L2-type-system", policies=["SEC-LANG-002"],
           related=["UNB-CTRL-055"], frefs=[UB("UNB-RCN-FIN-005"), UB("UNB-SMP-ECN-001")])],
   evrs=[E("Fee schedule version register", "All schedule versions with FeeBase contract, effective dates, approvers and cost basis reference.",
           "event-driven-automated", "per-event", disc="customer-only")],
   qs=[
    Q("Schedule versioning", "How are fee schedules defined, approved and versioned, and can you show which version applied to a fund on any date?",
      "Know exactly which fees applied when.", "Disputed or undocumented fee charges.",
      [UB("CNV-FIN-002"), COSO], "industry-convention", "high", ind=IND),
    Q("Fee base", "What balance is the asset-based fee calculated on (end-of-day value, average daily balance, period end), and is the basis documented per schedule?",
      "Transparent and consistent fee basis.", "Fees computed on inconsistent or inflated bases.",
      [UB("UNB-RCN-FIN-005"), LAND], "customer-preference", "high"),
    Q("Minimum fees", "How are minimum annual fees or minimum balances justified, and are they disclosed to donors?",
      "Fairness to small funds.", "Minimum fees eroding small funds without justification.",
      [UB("UNB-SMP-ECN-001"), UB("CNV-ECO-002")], "customer-preference", "medium"),
    Q("Tier method", "For tiered fee schedules, is the rate applied blended across tiers or to the whole balance at the tier reached, and is that stated?",
      "Avoid cliff effects and misunderstanding.", "Unexpected fee jumps at tier boundaries.",
      [UB("UNB-RCN-FIN-005")], "customer-preference", "low"),
    Q("Partner-specific schedules", "When different partners or programs have different fee schedules on the same platform, how do you ensure the correct schedule applies to each fund?",
      "Correct fees per program.", "Wrong schedule applied across partners.",
      [UB("ADM-027"), UB("UNB-INV-041")], "customer-preference", "medium",
      ind=["donor-advised-funds", "wealth-management", "enterprise-software"]),
   ]),

AU("Fee calculation accuracy, transparency and reconciliation",
   target=("Fee administration runs as an idempotent run per (fund, schedule, period, segment "
           "set) through Accrued, Assessed, Posted and optionally Waived or Reversed; replaying "
           "a run posts nothing new, and corrections are compensating entries. Every accrual "
           "stores its computed base and inputs and is deterministically recomputable, so any "
           "donor or auditor can see base, rate, days and result. Only the fee engine emits "
           "authoritative fee events; informational events cannot change fee state. Fees are "
           "never charged twice at pool and fund level. Advisor or manager fee debits visible "
           "in custodian feeds are recorded as distinct transactions and reconciled; where "
           "feeds do not expose them they are raised as reconciliation exceptions. Fees "
           "embedded in manager NAV are disclosed as such."),
   stmt=("Planned: idempotent, recomputable fee runs and fee reconciliation are specified. "
         "No fee has been calculated."),
   reqs=["RR-ADM-028-r1", "UNB-RCN-FIN-005", "UNB-NAV-033", "UNB-INV-036", "UNB-XIN-ERP-007",
         "CNV-FIN-013", "UNB-NAV-022", "UNB-FIN-002"],
   impl="medium", rec="low",
   owner="Unassigned (proposed: sponsor Controller)",
   challenge={
       "customer_intent": "Fees charged are exactly what the schedule says.",
       "adverse_outcome": "Systematic overcharging, donor complaints, refunds and reputational harm.",
       "conventional_control_effectiveness": "Periodic sample recalculation of a few accounts by staff or auditors detects only gross errors.",
       "legally_required": "No statute prescribes fee recalculation for DAF sponsors.",
       "contractually_required": "Sponsors and auditors expect fee accuracy testing.",
       "historical_convention": "Quarterly spot checks and annual audit sampling.",
       "architectural_elimination": "Arithmetic and double-posting errors largely eliminated by deterministic, idempotent runs with decimal types; schedule configuration errors are not.",
       "automatic_enforcement": "Every accrual is recomputed independently and compared before posting.",
       "continuous_evidence": "Stored base and inputs for every accrual enable 100 percent recomputation.",
       "stronger_alternative": "Full-population recomputation each run instead of sampling.",
       "alternative_verifiable": "Yes; an auditor can re-run the recomputation.",
       "customer_acceptance_likelihood": "Likely.",
       "invalidating_conditions": "The recomputation shares the same flawed schedule configuration, so it confirms consistent but wrong fees.",
       "conventional_cost": "Staff time for sampling.",
       "alternative_cost": "Compute cost negligible; build cost moderate.",
       "alternative_risks": "False confidence when configuration itself is wrong.",
       "supporting_arguments": ["Whole-population check rather than sample."],
       "opposing_arguments": ["Independent recomputation by the same system is not independent of configuration errors; configuration review is still needed."],
       "technical_effectiveness": "stronger", "institutional_acceptance": "likely"},
   ctls=[C("Idempotent fee run with full recomputation",
           "Execute fee runs keyed by (fund, schedule, period, segment set); recompute each accrual from stored inputs and block posting on mismatch.",
           "preventive-structural", "L7-property-tested", related=["UNB-SCTRL-032", "UNB-CTRL-056"],
           frefs=[UB("RR-ADM-028-r1"), TSC_PI]),
       C("Single authoritative fee event emitter",
         "Allow only the fee engine to emit authoritative fee events; reject inbound integration messages claiming fee effects.",
         "preventive-structural", "L3-restricted-interface", policies=["SEC-AUTH-001"],
         frefs=[UB("UNB-XIN-ERP-007")]),
       C("Custodian fee debit reconciliation",
         "Reconcile manager and advisor fee debits in custodian feeds to expected fees; raise exceptions for unexplained debits.",
         "detective-automated", "L9-runtime-monitored", related=["UNB-SCTRL-024"],
         frefs=[UB("CNV-FIN-013")])],
   evrs=[E("Fee run record", "Per run: inputs, computed bases, rates, results, recomputation comparison and postings.",
           "event-driven-automated", "per-event", prov=["run_key", "schedule_version", "valuation_version", "base", "result"]),
         E("Fee calculation explanation for donors", "Donor-facing breakdown of each fee charged (base, rate, days, schedule version).",
           "event-driven-automated", "per-event", disc="customer-only")],
   qs=[
    Q("Fee explanation", "Can you show a donor exactly how each fee charged to their fund was calculated?",
      "Transparency and dispute resolution.", "Unexplainable charges eroding trust.",
      [UB("UNB-RCN-FIN-005"), LAND], "customer-preference", "high", ind=IND,
      alts=["Do fund statements itemize fees with their calculation basis?"]),
    Q("Double charging", "How do you prevent the same service being charged twice, for example at both the pool or manager level and the fund level?",
      "Avoid duplicate fees.", "Systematic overcharging through layered fees.",
      [UB("UNB-NAV-033"), UB("UNB-INV-036")], "customer-preference", "high"),
    Q("Accuracy testing", "How is fee calculation accuracy tested, and is every fee recalculated or only a sample?",
      "Assurance of fee accuracy.", "Undetected systematic fee errors.",
      [UB("RR-ADM-028-r1"), TSC_PI], "industry-convention", "high"),
    Q("Rerun safety", "If a fee run is interrupted or rerun, what prevents fees being posted twice?",
      "Operational safety of batch processes.", "Duplicate fee postings.",
      [UB("RR-ADM-028-r1")], "industry-convention", "medium"),
    Q("Embedded manager fees", "Are investment manager fees embedded in unit values or charged explicitly, and how is this disclosed to donors?",
      "Full cost visibility.", "Hidden investment costs.",
      [UB("UNB-NAV-033"), LAND], "customer-preference", "medium"),
    Q("Custodian fee debits", "How are advisor or manager fees debited directly at the custodian reconciled to what was agreed?",
      "Detect unauthorized fee debits.", "Unapproved fees taken from fund assets.",
      [UB("CNV-FIN-013")], "industry-convention", "medium"),
   ]),

AU("Fee change control, waivers and donor notice",
   target=("Fee schedules change only by approving a new effective-dated version through the "
           "sponsor's configuration governance, which detects conflicts with platform hard "
           "controls, encoded law and pack baselines before approval; changes are by "
           "supersession, never in-place edits, and never retroactive. Waivers are approved "
           "schedule exceptions with reason and expiry. AI may draft a proposed change but "
           "cannot approve it. Donor-facing quotes are shown for charged operations and any "
           "amount above the donor's accepted maximum requires consent or is absorbed by the "
           "sponsor. A minimum advance-notice period for fee increases is a sponsor policy "
           "that Unbound should enforce as a release gate; no such requirement exists yet."),
   stmt=("Planned: versioned fee change approval and waiver control are specified. Advance "
         "donor notice of fee changes is not yet specified in Unbound requirements."),
   reqs=["RR-ADM-048-r1", "UNB-REM-007", "ADM-028", "RR-ADM-028-r1", "CNV-ECO-002",
         "UNB-XIN-ERP-007", "UNB-RCN-WF-021"],
   oqs=["Gap: no Unbound requirement mandates advance notice to donors or sponsors before a "
        "fee increase takes effect, or a notice record linked to the schedule version."],
   mech="event-driven-automated", fresh="per-event",
   owner="Unassigned (proposed: sponsor governance with Controller)",
   ctls=[C("Fee schedule change approval with conflict detection",
           "Require independent approval of new fee schedule versions after automated conflict detection; prohibit retroactive effective dates; deny AI approval.",
           "preventive-gate", "L3-restricted-interface", related=["UNB-CTRL-055", "UNB-SCTRL-002"],
           policies=["SEC-AUTH-001"], frefs=[UB("RR-ADM-048-r1")]),
       C("Waiver expiry enforcement",
         "Expire fee waivers automatically at their end date and report waivers by approver.",
         "detective-automated", "L9-runtime-monitored", related=["UNB-CTRL-057"],
         frefs=[UB("RR-ADM-028-r1")])],
   evrs=[E("Fee change approval record", "Proposed and approved schedule diffs, conflict check results, approvers and notice evidence.",
           "event-driven-automated", "per-event", disc="customer-only")],
   qs=[
    Q("Change authority", "Who can change fee schedules on the platform, and what approvals and evidence are required?",
      "Prevent unauthorized fee changes.", "Unauthorized fee increases.",
      [UB("RR-ADM-048-r1"), COSO], "industry-convention", "high", ind=IND),
    Q("Donor notice", "How much advance notice do donors receive before a fee change takes effect, and how is notice recorded?",
      "Fair treatment of donors.", "Surprise fee increases and complaints.",
      [LAND, UB("CNV-ECO-002")], "customer-preference", "medium",
      oq=["No Unbound requirement for advance fee-change notice."]),
    Q("Retroactive changes", "Can a fee change be applied retroactively to past periods?",
      "Stability of past charges.", "Retroactive charges without consent.",
      [UB("RR-ADM-048-r1")], "customer-preference", "medium"),
    Q("Waivers", "How are fee waivers approved, time-limited and reported?",
      "Controlled discounts.", "Favoritism or unrecorded waivers.",
      [UB("RR-ADM-028-r1")], "industry-convention", "medium"),
    Q("Service charge quotes", "Are donors shown the fee before requesting a charged service (for example an expedited or international grant)?",
      "Informed consent for charges.", "Unexpected service charges.",
      [UB("CNV-ECO-002")], "customer-preference", "medium"),
   ]),

AU("Grant priority over fees and fee shortfall handling",
   target=("Recognized grants payable and, by default, reserved grants rank ahead of fees. A "
           "fee shortfall becomes a fund-level memo claim against future capacity, not an "
           "entity-level asset; it may be waived by an authorized approver with a reason and "
           "is written off on fund closure. Fee schedules declare their treatment of "
           "reserved-but-uncommunicated grants. Fund closure posts final fees as a defined "
           "state before residual disposition, with no closing-period minimum or proration "
           "unless the schedule version states it. During a dispute freeze, fees accrue and "
           "are collected while grants are held; waiver is a separate decision."),
   stmt=("Planned: grants rank ahead of fees and fee shortfalls never create negative funds, "
         "per Unbound convergence clause CNV-FIN-006. Not implemented."),
   reqs=["CNV-FIN-006", "CNV-FIN-002", "UNB-RCN-ENT-006", "CNV-ENT-002", "UNB-RCN-FIN-009"],
   mech="event-driven-automated", fresh="per-event",
   owner="Unassigned (proposed: sponsor Controller)",
   ctls=[C("Capacity waterfall with grants ahead of fees",
           "Compute fund capacity so that recognized and reserved grants are satisfied before fee assessment; record any shortfall as a memo claim.",
           "preventive-structural", "L3-restricted-interface", frefs=[UB("CNV-FIN-006")])],
   evrs=[E("Fee shortfall memo claim register", "Open fee shortfalls per fund with waiver or write-off decisions.",
           "event-driven-automated", "per-event")],
   qs=[
    Q("Priority", "If a fund cannot cover both an approved grant and accrued fees, which is paid first?",
      "Protect charitable distributions.", "Fees consuming money committed to charities.",
      [UB("CNV-FIN-006")], "customer-preference", "high", ind=IND),
    Q("Commitments below fees", "Can fees reduce a fund's balance below the amount needed for grants already approved or reserved?",
      "Ensure committed grants can be paid.", "Grant default due to fee deductions.",
      [UB("CNV-FIN-006"), UB("UNB-RCN-FIN-009")], "customer-preference", "high"),
    Q("Closure fees", "How are fees handled when a fund is closed, including final and minimum fees?",
      "Fair closure accounting.", "Unexpected closure charges.",
      [UB("UNB-RCN-ENT-006"), UB("CNV-FIN-002")], "customer-preference", "medium"),
    Q("Fees during freezes", "Do fees continue to accrue while a fund is frozen for a dispute or succession, and can they be waived?",
      "Predictable treatment in contested situations.", "Disputes over fees charged during freezes.",
      [UB("CNV-ENT-002")], "customer-preference", "low"),
   ]),

AU("Donor-covered, pass-through and processing fees",
   target=("When fee coverage is voluntary and the sponsor is merchant of record, the "
           "acknowledgment amount is the gross amount charged, the fund is credited gross, "
           "and the processing fee posts as an expense (to the fund only if the schedule "
           "discloses pass-through). Amounts paid to a non-charity (platform or mandatory "
           "convenience fees) are excluded from the acknowledgment and shown separately. "
           "Donor-paid service fees are receipted as service fees with no deductibility "
           "statement. Bank return and intermediary fees are borne by the sponsor by default, "
           "domestic wires are sent without deductions and international wires default to "
           "OUR; any pass-through is disclosed. Required accessibility accommodations carry "
           "no fee. Card contributions, and therefore donor-covered card fees, are deferred "
           "beyond release 1."),
   stmt=("Planned and deferred: donor-covered card fee rules are specified but scheduled "
         "after release 1 (CNV-PAY-006, CNV-PAY-008). No fee of any kind is processed today."),
   reqs=["CNV-PAY-006", "CNV-PAY-007", "CNV-ECO-002", "UNB-XIN-ECO-018", "RR-REQ-X-032-r1"],
   oqs=["Counsel has not confirmed the acknowledgment treatment of voluntary donor-covered fees."],
   mech="event-driven-automated", fresh="per-event",
   owner="Unassigned (proposed: sponsor Controller with counsel)",
   ctls=[C("Acknowledgment amount derivation rule for covered fees",
           "Derive acknowledgment amounts from typed contribution components (gross charge, non-charity fees, service fees) under a counsel-approved rule.",
           "preventive-structural", "L2-type-system", frefs=[UB("CNV-PAY-006"), S("SRC-IRS-PUB-1771")]),
       C("Pass-through fee disclosure gate",
         "Block charging any pass-through rail fee to a fund or grantee unless the schedule discloses it.",
         "preventive-gate", "L3-restricted-interface", frefs=[UB("CNV-PAY-007")])],
   evrs=[E("Contribution component breakdown", "Per contribution: gross, covered fee, non-charity amounts, credited amount and acknowledgment amount.",
           "event-driven-automated", "per-event")],
   qs=[
    Q("Donor-covered fees", "When a donor elects to cover processing fees, what amount appears on their acknowledgment and what is credited to the fund?",
      "Accurate tax acknowledgments.", "Overstated deduction or misleading receipt.",
      [UB("CNV-PAY-006"), S("SRC-IRS-PUB-1771"), S("SRC-IRC-170")], "legal-regulatory", "high",
      auth="IRS", ind=["donor-advised-funds", "nonprofit"]),
    Q("Rail fees", "Are wire, return or intermediary bank fees ever deducted from grants or charged to funds, and is that disclosed?",
      "Grantees receive full amounts.", "Grantees short-paid by hidden fees.",
      [UB("CNV-PAY-007")], "customer-preference", "medium"),
    Q("Platform fees on receipts", "Are platform or convenience fees paid to non-charities excluded from acknowledged amounts?",
      "Correct deductible amounts.", "Donor claims deduction for non-charitable payment.",
      [UB("CNV-PAY-006"), S("SRC-IRS-PUB-1771")], "legal-regulatory", "medium", auth="IRS"),
    Q("Service charge recovery", "How do you show that service charges recover actual cost rather than generating undisclosed margin?",
      "Justify charges.", "Excessive charges against charitable assets.",
      [UB("UNB-XIN-ECO-018"), LAND], "customer-preference", "low"),
   ]),

AU("Revenue sharing, advisor compensation and conflict disclosure",
   status="proposed-target-state",
   target=("Referral attribution is recorded as an immutable informational fact; Unbound "
           "computes, accrues or exports no referral compensation unless a counsel-approved "
           "rule for that arrangement and jurisdiction exists. Decided rule: referral "
           "compensation is never paid from fund assets; flat fair-market-value fees from "
           "sponsor operating funds are permitted only under written agreement, to persons "
           "who are not advisors or related parties of the referred fund, in states where "
           "paid-solicitor rules are satisfied, and never per grant or per dollar granted. "
           "No compensation or other payment is made from a fund to a donor, donor-advisor "
           "(including an advisor the donor designated with investment privileges), family "
           "member or 35 percent controlled entity; advisor or manager compensation from DAF "
           "assets is held until the advisor relationship is classified by counsel. "
           "Sponsor-engaged managers may be paid only under sponsor contracts with uniform "
           "program-wide fees. Echelon itself takes no compensation varying with assets, "
           "trades or liquidations. Disclosure of Echelon's own relationships with sponsors "
           "(including any board overlap) is an organizational matter not yet established."),
   stmt=("Planned: Unbound requirements block fees or referral payments from fund assets to "
         "donors, donor-advisors and their advisors pending counsel rules. Echelon's own "
         "revenue model and any related-party relationships with sponsors are not yet "
         "established or disclosed."),
   reqs=["UNB-XIN-CRM-006", "CNV-GRT-009", "UNB-RCN-ENT-015", "UNB-RCN-FIN-010",
         "CNV-LEG-001", "CNV-LEG-002", "REQ-X-067", "CNV-FIN-013", "UNB-ENT-003"],
   oqs=["Echelon's pricing and any revenue-sharing model with distribution partners is not "
        "established in reviewed records (business plan is a plan, not evidence).",
        "No Unbound requirement covers disclosure to the sponsor board of vendor-sponsor "
        "related-party relationships (the daf-landscape governance research flags board "
        "overlap at other vendors as a diligence question). Form 990 Schedule L source not seeded.",
        "The 2023 proposed DAF regulations on investment advisors (REG-142338-07) are not final; "
        "re-review is required on finalization (UNB-RCN-ENT-015)."],
   mech="event-driven-automated", fresh="per-event", autom="partial",
   owner="Unassigned (proposed: Echelon counsel and sponsor compliance owner)",
   challenge={
       "customer_intent": "Fees and incentives do not compromise donor interests or create excess benefit.",
       "adverse_outcome": "Excise taxes under sections 4958 or 4967, reputational damage, conflicted advice.",
       "conventional_control_effectiveness": "Disclosure documents and annual conflict certifications; weak at preventing payments.",
       "legally_required": "Section 4958 treats compensation from a DAF to a donor or donor-advisor as an excess benefit; paid-solicitor registration applies in many states.",
       "contractually_required": "Sponsors increasingly require conflict disclosure from vendors.",
       "historical_convention": "Disclosure of revenue sharing in program descriptions; advisor fees often paid from DAF assets.",
       "architectural_elimination": "Partly: payments to related parties from fund assets are blocked by a nonwaivable related-party hold; referral compensation cannot be computed from fund data without an approved rule.",
       "automatic_enforcement": "Accrual hold when advisor classification is missing.",
       "continuous_evidence": "Related-party registry checks logged per payment.",
       "stronger_alternative": "Structural prohibition plus disclosure, rather than disclosure alone.",
       "alternative_verifiable": "Yes, via payment check logs.",
       "customer_acceptance_likelihood": "Likely among sponsors; possibly unwelcome to advisor channels whose economics depend on asset-based fees.",
       "invalidating_conditions": "Related-party registry incomplete; advisor relationships not disclosed by donors.",
       "conventional_cost": "Low.",
       "alternative_cost": "Moderate build; may reduce channel revenue.",
       "alternative_risks": "Commercial disadvantage versus platforms that pay advisors from DAF assets.",
       "supporting_arguments": ["Prevents the highest-severity tax outcome rather than disclosing it.",
                                 "Removes per-dollar incentives that create conflicts."],
       "opposing_arguments": ["Advisor-managed DAF programs commonly pay asset-based advisory fees from fund assets; a strict hold may make Unbound unattractive to that channel.",
                              "Registry completeness depends on donor self-disclosure."],
       "technical_effectiveness": "stronger", "institutional_acceptance": "uncertain"},
   ctls=[C("Related-party payment hold",
           "Block any payment or fee accrual from fund assets whose payee matches a donor, advisor, related person or their advisor until a counsel-approved rule permits it.",
           "preventive-gate", "L3-restricted-interface", related=["UNB-CTRL-055"],
           frefs=[UB("CNV-GRT-009"), S("SRC-IRC-4958", "4958(c)(2)")]),
       C("Referral compensation computation block",
         "Prevent computing or exporting referral compensation from contribution, balance or grant data without an approved compensation rule.",
         "preventive-structural", "L3-restricted-interface", frefs=[UB("UNB-XIN-CRM-006")]),
       C("Vendor conflict disclosure to sponsor",
         "Echelon discloses to each sponsor any ownership, board, compensation or referral relationship with the sponsor, its directors or its distribution partners.",
         "administrative", "L10-external-or-manual", systems=["Echelon Foundry governance (not established)"],
         residual=["No Echelon conflict policy exists."])],
   evrs=[E("Related-party check log", "Per payment or accrual: payee match result against related-party registry and rule reference.",
           "event-driven-automated", "per-event"),
         E("Echelon related-party and compensation disclosure", "Statement of Echelon relationships and compensation arrangements with the sponsor and partners.",
           "periodic-manual", "P1Y", producer="not yet assigned", disc="nda")],
   qs=[
    Q("Revenue sharing", "Does your company share revenue with or pay compensation to financial advisors, platforms, referrers or sponsors, and how is it disclosed?",
      "Identify conflicts of interest.", "Undisclosed incentives distorting recommendations.",
      [UB("UNB-XIN-CRM-006"), LAND, S("SRC-STATE-CHARITABLE-SOLICITATION")], "customer-preference", "high",
      ind=IND, alts=["Describe all revenue-sharing arrangements tied to the DAF program."]),
    Q("Advisor fees from DAF assets", "Can investment advisor fees be paid from DAF assets, and how do you check whether the advisor is a donor, donor-advisor or related person?",
      "Avoid excess benefit transactions.", "Automatic excess benefit and excise taxes.",
      [UB("UNB-RCN-FIN-010"), S("SRC-IRC-4958", "4958(c)(2)"), S("SRC-IRS-DAF-PROPOSED-REGS-2023")],
      "legal-regulatory", "critical", auth="IRS", ind=IND),
    Q("Asset-based vendor compensation", "Does your compensation vary with the fund's assets, trading activity or liquidations?",
      "Vendor incentives aligned with donors.", "Vendor incentive to grow AUM or trading.",
      [UB("CNV-LEG-001")], "customer-preference", "medium",
      oq=["Echelon pricing model not established."]),
    Q("Vendor-sponsor relationships", "Do any of your owners, officers or employees serve on our board or have financial relationships with our organization or its directors?",
      "Board independence in vendor oversight.", "Conflicted vendor selection or renewal.",
      [LAND, S("SRC-IRS-FORM-990")], "customer-preference", "high", ind=["donor-advised-funds", "nonprofit"],
      oq=["Form 990 Schedule L instructions not seeded."], prod=["echelon-organization"]),
    Q("Prohibited payments", "How does the platform prevent any payment from a fund to a donor, advisor, family member or entity they control?",
      "Compliance with DAF prohibited benefit rules.", "Excise taxes on donor, advisor and manager.",
      [UB("CNV-GRT-009"), S("SRC-IRC-4967"), S("SRC-IRC-4958")], "legal-regulatory", "critical", auth="IRS"),
    Q("Paid solicitor registration", "If referral partners are compensated, are they registered as paid solicitors or fundraisers where state law requires?",
      "State solicitation compliance.", "Enforcement by state attorneys general.",
      [UB("CNV-LEG-002"), S("SRC-STATE-CHARITABLE-SOLICITATION")], "legal-regulatory", "medium",
      jur=["US-states"], auth="State attorneys general"),
   ]),
]

if __name__ == "__main__":
    print("FEE", build("FEE", units, IND))
