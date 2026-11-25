from dafcommon import *

FI = ["donor-advised-funds", "nonprofit", "banking", "wealth-management"]
I4966 = lambda loc=None, b="directly-documented": S("SRC-IRC-4966", loc, "derived-from", b)

units = []

u = AU("lifecycle", "DAF account lifecycle, fund agreement versioning and point-in-time history",
    "Every DAF account is an explicit state machine (Requested, Active, Restricted, Frozen, ClosureRequested, "
    "ObligationsResolved, FinalFeesPosted, ResidualDisposed, Closed, Archived) whose transitions occur only through "
    "authorized, typed commands recorded as append-only events. The governing fund agreement and sponsor program terms "
    "are immutable versions bound to the account with effective dates, so the sponsor can reconstruct the account, its "
    "participants, balances and governing terms as of any past date. Closure cannot complete while reservations, "
    "unsettled contributions or in-flight payments remain.",
    "Model the account lifecycle as an F# discriminated-union state machine persisted append-only (Strata-managed "
    "PostgreSQL schema), with bitemporal queries and a closure state machine per UNB-RCN-ENT-006.",
    "accounts would follow a defined lifecycle with immutable, versioned fund agreements and point-in-time history.",
    ["UNB-RCN-ENT-006", "UNB-DATA-001", "UNB-DATA-003", "UNB-DATA-006", "CNV-ARC-005", "UNB-LS-015"],
    policies=["SEC-AUTH-001", "SEC-LANG-002"], fresh="per-event", impl="medium",
    residual=["Migration of legacy accounts may import incomplete historical agreements that cannot be reconstructed."],
    oq=["Which sponsor-specific lifecycle states (for example memorial or youth funds) must be supported in release 1?",
        "Strata currently has no verified runtime typed query interface; how will point-in-time queries be implemented?"],
    controls=[CTL("Typed account state machine with closure preconditions",
        "Prevent any account state change except through authorized commands and block closure while obligations remain.",
        "preventive-structural", "L2-type-system", ["Unbound (proposed; not built)", "Strata (pilot; schema only)"],
        ext=["UNB-CTRL-004"], fw=[S("SRC-AICPA-TSC", "PI1.3")], cwe=["CWE-841"])],
    evrs=[EVR("Account lifecycle event log",
        "Append-only log of every account state transition with command, actor, authority and governing agreement version, "
        "queryable as of any date. Intended producer: Unbound account module.",
        prov=["account id", "from state", "to state", "command id", "actor", "authority", "agreement version", "effective time", "recorded time"])])
u["questions"] = [
    Q("account-opening", "How is a donor-advised fund account opened, and which records establish the fund agreement, the sponsor's acceptance and the date advisory privileges begin?",
      "Sponsor needs proof of when and on what terms each fund came into existence.",
      "Disputes over account terms or the start of advisory privileges cannot be resolved from records.",
      [UNB(), S("SRC-PPA-2006")], imp="high",
      alts=["Describe your DAF account opening workflow and the records it produces.",
            "What evidence shows the sponsor accepted a new fund and on which terms?"]),
    Q("account-states", "What lifecycle states can a DAF account occupy, and can any state change occur without a recorded, authorized command?",
      "Sponsor wants account status to be trustworthy and controlled.",
      "Silent or unauthorized status changes (for example reactivating a frozen fund) enable misuse.",
      [UNB(), S("SRC-AICPA-TSC", "PI1.3")]),
    Q("account-closure", "How does the platform close an account that still has open grant reservations, unsettled contributions, pending fees or in-flight payments?",
      "Closure must not strand money or obligations.",
      "Premature closure loses track of funds in transit or leaves grants unpaid.",
      [UNB()], imp="high"),
    Q("agreement-versioning", "When fund agreement terms or program terms change, how are existing accounts versioned, and how can the sponsor tell which version governed an account on a given date?",
      "Terms evolve; historical decisions must be judged under the terms then in force.",
      "Retroactive application of new terms or inability to show the governing terms in a dispute or audit.",
      [UNB(), S("SRC-FASB-ASC-958")], cls="industry-convention"),
    Q("point-in-time-history", "Can the sponsor reconstruct an account's participants, privileges, balances and governing terms as of any past date for an audit, subpoena or donor dispute?",
      "Auditors, counsel and regulators ask what was true at a specific time.",
      "Overwritten records make historical reconstruction impossible.",
      [UNB(), S("SRC-AICPA-TSC", "PI1.5")], imp="high",
      alts=["Do you keep full history of account changes, or only current state?"]),
    Q("migration-history", "When a sponsor migrates from another DAF system, how is each fund's full history (contributions, grants, acknowledgments, participants) imported and reconciled?",
      "Sponsors switching platforms must not lose donor history.",
      "Incomplete migration breaks substantiation, reporting and donor trust.",
      [UNB(), S("SRC-ECH-DAF-LANDSCAPE")], cls="customer-preference", req=["CNV-EXP-002"]),
]
units.append(u)

u = AU("classification", "Fund type classification for section 4966(d)(2) and accounting treatment",
    "Each fund carries exactly one fund type (donor-advised, designated, agency, field-of-interest, scholarship, other "
    "excepted fund) and one accounting treatment derived from the instrument's terms, not marketing labels. The fund type "
    "selects the rule set the engine applies, so DAF rules are applied to every fund that meets the statutory definition "
    "and excepted-fund rules only where the sponsor's counsel-approved classification supports the exception.",
    "Implement an account-type register with counsel- and CPA-approved classification and AccountingTreatment per "
    "CNV-FIN-008 and UNB-XIN-ACC-001; release 1 supports only the standard DAF type.",
    "each fund would carry a counsel-approved fund type that determines which rules apply.",
    ["CNV-FIN-008", "UNB-XIN-ACC-001", "CNV-GRT-009"], impl="low",
    oq=["Release 1 supports only the standard DAF account type (CNV-FIN-008); sponsors needing designated, agency or scholarship funds would be unsupported. Confirm with target sponsors."],
    controls=[CTL("Account-type register binding rules to fund type",
        "Ensure the rule set applied to a fund follows from an approved classification rather than a free-text label.",
        "preventive-structural", "L3-restricted-interface", ext=["UNB-CTRL-043"],
        fw=[S("SRC-IRC-4966", "§4966(d)(2)")])],
    evrs=[EVR("Fund classification record",
        "Record of each fund's type and accounting treatment with the approving counsel or CPA decision and version.",
        prov=["fund id", "fund type", "accounting treatment", "approver", "decision reference", "effective time"])])
u["questions"] = [
    Q("daf-definition", "How does the platform determine whether a fund meets the statutory definition of a donor-advised fund rather than an excepted fund such as a single-organization or qualifying scholarship fund?",
      "DAF excise tax rules apply only to funds that meet the definition; misclassification is a tax exposure.",
      "Applying the wrong rule set causes taxable distributions or unnecessary restrictions.",
      [I4966("§4966(d)(2)"), UNB()], cls="legal-regulatory", imp="critical", auth="IRS"),
    Q("non-daf-funds", "Can the sponsor administer designated, agency, field-of-interest and scholarship funds alongside DAFs, each with its own rules, on the same platform?",
      "Community foundations operate many fund types and want one system.",
      "Separate systems or forced DAF treatment of non-DAF funds.",
      [UNB(), S("SRC-ECH-DAF-LANDSCAPE")], cls="customer-preference", imp="high",
      oq=["Release 1 scope excludes non-DAF fund types; confirm whether this blocks community foundation adoption."]),
    Q("advisory-expectation", "How does the system evidence the donor's reasonable expectation of advisory privileges that makes a fund a DAF?",
      "The advisory privilege element is part of the DAF definition.",
      "Sponsor cannot support its classification if challenged.",
      [I4966("§4966(d)(2)", "reasonably-inferred"), S("SRC-IRS-DAF-PROPOSED-REGS-2023")], cls="legal-regulatory", imp="medium", auth="IRS"),
    Q("accounting-treatment", "How is each fund's accounting treatment (contribution without donor restriction, with restriction, or agency liability) determined and approved?",
      "Financial statements must classify funds correctly.",
      "Misstated net assets or liabilities in audited financial statements.",
      [S("SRC-FASB-ASC-958", "958-605", "informed-by", "directly-documented"), UNB()], cls="industry-convention"),
]
units.append(u)

u = AU("privileges", "Advisory privilege grant, scope, revocation and point-in-time proof",
    "Advisory privileges (grant recommendation, investment recommendation, view-only, successor designation, "
    "participant management) are separate, explicitly scoped, effective-dated grants recorded as append-only authority "
    "facts. Every command is reauthorized server-side against current authority at execution time, so revocation takes "
    "effect at the next authorization check and no later than 60 seconds across sessions, widgets, API tokens and agent "
    "principals. No principal can grant privileges it does not hold.",
    "Central server-side authorization (SEC-AUTH-001) over typed authority facts; revocation propagation per UNB-RCN-WF-013 and AUTH-I1.",
    "advisory privileges would be explicitly scoped, revocable and reauthorized on every action.",
    ["UNB-ADV-001", "UNB-ADV-002", "UNB-PART-003", "UNB-PART-004", "UNB-XIN-EVA-014", "UNB-RCN-WF-013", "AUTH-I1", "UNB-API-003"],
    policies=["SEC-AUTH-001"], fresh="per-event", auto="full",
    residual=["Partner-side deprovisioning latency can exceed platform revocation latency (WG-2)."],
    controls=[CTL("Server-side reauthorization against effective-dated authority facts",
        "Deny any command whose actor lacks a current, in-scope privilege at execution time.",
        "preventive-structural", "L3-restricted-interface", ext=["UNB-CTRL-019", "UNB-CTRL-004"],
        fw=[S("SRC-AICPA-TSC", "CC6.1"), S("SRC-NIST-SP800-53-R5", "AC-3")], cwe=["CWE-285", "CWE-269"], policies=["SEC-AUTH-001"])],
    evrs=[EVR("Authority fact history and revocation latency measurements",
        "Append-only grants and revocations of advisory privileges plus measured time from revocation to last accepted command per channel.",
        mech="continuous-automated",
        prov=["fund id", "principal", "privilege", "scope", "grantor", "effective from", "effective to", "recorded time", "revocation latency"])])
u["questions"] = [
    Q("privilege-types", "Which advisory privileges does the platform support, and how is each granted, limited and revoked?",
      "Sponsor must control exactly what each donor or advisor can do.",
      "Overbroad privileges let advisors act beyond what the sponsor intended.",
      [UNB(), S("SRC-PPA-2006")], imp="high",
      alts=["What roles exist on a DAF account and what can each do?"]),
    Q("revocation-latency", "How quickly does revocation of an advisor's privileges take effect across web sessions, mobile apps, embedded widgets, API tokens and AI agents acting on their behalf?",
      "Revoked advisors must stop acting immediately.",
      "A removed advisor submits grants or views data after removal.",
      [UNB(), S("SRC-NIST-SP800-53-R5", "AC-2")], imp="critical"),
    Q("self-escalation", "Can an advisor grant privileges to another person or expand their own, and what prevents self-escalation?",
      "Privilege changes should be sponsor-governed.",
      "An advisor adds an associate who then benefits from grants.",
      [UNB(), S("SRC-MITRE-CWE", "CWE-269")], imp="high"),
    Q("investment-vs-grant-privileges", "How are investment advisory privileges (for example an outside investment adviser managing fund assets) separated from grant recommendation privileges?",
      "Investment managers should not gain grant authority, and the distinction matters for disqualified person analysis.",
      "Investment advisers recommend grants or are treated inconsistently for excise tax purposes.",
      [UNB(), S("SRC-IRS-DAF-PROPOSED-REGS-2023")], imp="medium", ind=FI, req=["UNB-CUST-014"]),
    Q("privilege-proof", "Can the platform prove which privileges a person held at the moment of any past action?",
      "Auditors and counsel need point-in-time authority evidence.",
      "Inability to show that an action was authorized when taken.",
      [UNB(), S("SRC-AICPA-TSC", "CC6.2")], imp="high"),
]
units.append(u)

u = AU("multiparticipant", "Multi-participant accounts, joint instructions and conflict handling",
    "A fund supports any number of participant relationships, each with its own role, scope and effective period. "
    "Instruction authority comes from the recorded fund agreement (any-one, all-must-approve, or configured quorum), "
    "never from inferred family status. Conflicting instructions from different principals with the same conflict scope "
    "are detected in the same transaction and both are held for resolution; closure, succession and authority changes "
    "require joint approval unless the agreement says otherwise. Adding a participant does not grant access to history "
    "unless the grantor's scope includes it.",
    "Relationship model per UNB-PART-001..009 with conflict scope keys (UNB-XIN-EVA-012) and CNV-GRT-016 authority rules.",
    "joint accounts would apply the fund agreement's approval rule and hold conflicting instructions for resolution.",
    ["UNB-PART-001", "UNB-PART-002", "UNB-PART-005", "UNB-PART-006", "UNB-PART-007", "UNB-PART-008", "CNV-GRT-016", "UNB-XIN-EVA-012"],
    policies=["SEC-AUTH-001"], impl="medium",
    oq=["How should the platform behave when a fund agreement is silent on joint authority and the sponsor has no default?"],
    controls=[CTL("Conflict scope detection on advisor instructions",
        "Detect and hold incompatible concurrent instructions from different principals on the same fund scope.",
        "preventive-structural", "L3-restricted-interface", ext=["UNB-CTRL-019"], cwe=["CWE-362"])],
    evrs=[EVR("Joint-instruction and conflict case records",
        "Record of each instruction requiring multiple approvals, approvals received, conflicts detected and resolution.",
        prov=["fund id", "instruction id", "conflict scope key", "principals", "approval rule version", "resolution", "recorded time"])])
u["questions"] = [
    Q("joint-authority", "How does the platform support accounts with multiple advisors who have different permissions, such as any-one-may-act versus all-must-approve?",
      "Families and couples share funds with varying authority.",
      "Grants proceed without a required co-advisor's approval.",
      [UNB()], imp="high"),
    Q("conflicting-instructions", "What happens when two advisors on the same fund submit conflicting instructions at the same time?",
      "Sponsor must not act on contradictory directions.",
      "Both instructions execute, or the wrong one wins silently.",
      [UNB()], imp="high"),
    Q("participant-onboarding", "How are additional participants invited, identity-verified and activated, and what can they see before acceptance?",
      "New participants should not see fund data before verification.",
      "Data disclosure to an unverified or mistaken invitee.",
      [UNB(), S("SRC-NIST-SP800-63-4")], imp="medium"),
    Q("history-visibility", "Does adding a participant expose prior contributions and grants, and can the existing advisors control that?",
      "Some donors want new participants (for example children) to see only future activity.",
      "Unintended disclosure of past giving to new participants.",
      [UNB()], cls="customer-preference", imp="medium"),
    Q("authority-from-agreement", "When a relationship between joint advisors changes (for example divorce or estrangement), how is authority determined and changed?",
      "Disputes between advisors are common and sensitive.",
      "Sponsor follows the wrong party, or authority is inferred from marital status.",
      [UNB()], imp="high", req=["CNV-ENT-002"]),
]
units.append(u)

u = AU("succession", "Successor advisors, charitable beneficiaries and succession activation",
    "Each fund has a versioned succession plan with zero or more ordered successors, contingent successors and "
    "charitable beneficiaries or spend-down instructions. On credible notice of death or incapacity the platform holds "
    "that person's new actions; on verification it suspends that person's rights, sessions and delegated agents in one "
    "transaction. Succession starts only when no living qualified advisor remains, may split the fund into separate "
    "successor accounts by percentage using balanced append-only entries, and handles disputes, nonresponse and "
    "contingent paths explicitly. Approved unpaid grants proceed unless sponsor policy says otherwise.",
    "Succession graph and activation per UNB-SUCC-001..014, CNV-ENT-001, UNB-RCN-ENT-004 and REQ-X-008, with preview simulation (UNB-SUCC-013).",
    "succession plans would be versioned, previewable and activated through evidence-backed sponsor workflows.",
    ["UNB-SUCC-001", "UNB-SUCC-002", "UNB-SUCC-004", "UNB-SUCC-006", "UNB-SUCC-007", "UNB-SUCC-008", "UNB-SUCC-010", "UNB-SUCC-011", "CNV-ENT-001", "UNB-RCN-ENT-004", "REQ-X-008", "UNB-GRANT-035"],
    impl="high", rec="medium", auto="partial",
    oq=["Death verification sources (death certificate, obituary, third-party death data) and their assurance are not defined.",
        "Which sponsor defaults apply when successors do not respond within the window?"],
    controls=[CTL("Atomic suspension of a deceased or incapacitated party's authority",
        "Suspend all rights, sessions and agent principals deriving from a verified deceased or incapacitated party before succession.",
        "preventive-structural", "L3-restricted-interface", ext=["UNB-CTRL-022"]),
        CTL("Succession allocation reconciliation",
        "Ensure successor account allocations are balanced, append-only and reconcile to the predecessor balance.",
        "detective-automated", "L6-automated-analysis", ext=["UNB-CTRL-023"])],
    evrs=[EVR("Succession activation dossier",
        "Evidence of the plan version, triggering evidence, verification, suspensions, notices, successor responses, allocations and approvals.",
        mech="event-driven-automated", fmt="JSON record and Folio-rendered PDF",
        prov=["fund id", "plan version", "trigger evidence", "verifier", "approver", "allocation entries", "recorded time"])])
u["questions"] = [
    Q("successor-designation", "How are successor advisors and charitable beneficiaries designated, changed and evidenced over time?",
      "Donors expect their legacy wishes to be honored and provable.",
      "Lost or overwritten designations lead to disputes.",
      [UNB(), S("SRC-PPA-2006")], imp="critical"),
    Q("death-verification", "What triggers succession, and how does the platform verify a donor's death or incapacity before changing authority?",
      "Fraudulent death reports could hijack a fund.",
      "Authority transfers on a false or unverified report.",
      [UNB()], imp="critical",
      oq=["Death verification sources and assurance level are not specified in Unbound requirements."]),
    Q("fund-splitting", "Can a fund be divided among several successors into separate accounts, and how are allocations calculated, rounded and reconciled?",
      "Multi-child families commonly split funds.",
      "Allocation errors or unbalanced entries misstate successor balances.",
      [UNB()], imp="high"),
    Q("pending-grants-at-death", "What happens to approved but unpaid grants, recurring grants and scheduled grants when the donor dies?",
      "Donor intent for committed grants should be respected while future instructions stop.",
      "Grants continue under an authority that no longer exists, or committed grants are wrongly canceled.",
      [UNB()], imp="high"),
    Q("contested-succession", "How does the platform handle contested succession, such as conflicting documents, simultaneous deaths or a challenge by family members?",
      "Sponsors need a safe hold-and-resolve path.",
      "Sponsor acts on one claimant's documents and faces liability.",
      [UNB()], imp="high", req=["CNV-ENT-002"]),
    Q("no-successor", "What happens when there is no named successor or the successor does not respond within the sponsor's window?",
      "Funds must reach a charitable default rather than sit indefinitely.",
      "Orphaned funds with no authority and no disposition.",
      [UNB()], imp="medium"),
    Q("not-inherited-disclosure", "How does the platform explain to donors that a DAF is not personal property and cannot be inherited, while still offering succession planning?",
      "Misleading succession language creates legal and reputational risk.",
      "Donors or heirs believe they own fund assets.",
      [UNB(), I4966("§4966(d)(2)", "reasonably-inferred")], imp="medium"),
]
units.append(u)

u = AU("policy-config", "Sponsor policy configuration, approval, simulation and version pinning",
    "Every sponsor-configurable policy (minimums, fees, grant limits, payout, inactivity, eligibility, approval "
    "delegation) is a declarative, versioned, effective-dated record that only authorized sponsor decision makers can "
    "approve. Material changes require affirmative sponsor adoption, can be simulated against historical data before "
    "activation, and are pinned to every decision they influence. Platform changes cannot alter sponsor policy outcomes "
    "without the sponsor's adoption, and feature flags cannot vary legal or financial semantics by tenant.",
    "Policy packs per CNV-GOV-005 and REQ-X-045, configuration register per UNB-SMP-CFG-003, replay per UNB-GEX-024.",
    "sponsor policies would be versioned, simulated before activation and pinned to each decision.",
    ["REQ-X-045", "CNV-GOV-005", "UNB-DATA-006", "UNB-SMP-CFG-001", "UNB-SMP-CFG-003", "UNB-TEN-010", "UNB-LEG-005", "UNB-GRANT-045", "UNB-XIN-SAS-002"],
    impl="medium",
    challenge=CH(
        "Sponsors want assurance that policy changes are deliberate and do not silently change outcomes.",
        "A misconfigured or vendor-changed policy approves grants or charges fees the board never authorized.",
        "Conventional change tickets and annual policy reviews document intent but do not prove which rule produced which decision.",
        "No statute requires policy simulation; sponsors' boards have fiduciary duties over policy.",
        "Commonly expected in sponsor-vendor agreements as change notification, not simulation.",
        "Vendors announce release notes; sponsors review policy documents annually.",
        "Policy as immutable data pinned to each decision removes the ambiguity of which version applied.",
        "Activation gate requires approved version; decisions record the version id automatically.",
        "Each decision record carries its policy version, enabling continuous evidence.",
        "Simulation of a proposed version against 12 months of decisions before adoption.",
        "Yes, by replaying pinned decisions under old and new versions.",
        "Likely for larger sponsors; small sponsors may find simulation results hard to interpret.",
        "If decisions depend on external facts not captured at decision time, replay is not faithful.",
        "Low direct cost but high latent risk.", "Medium engineering cost to build deterministic replay.",
        "Simulation results may be misread as legal assurance.",
        ["Makes policy authority auditable", "Prevents vendor-side silent changes"],
        ["Small sponsors may lack staff to review simulations", "Replay fidelity depends on complete input capture"],
        "stronger", "likely"),
    controls=[CTL("Policy activation gate requiring sponsor-approved version",
        "Block activation of any policy version lacking recorded approval by an authorized sponsor decision maker.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-001", "UNB-CTRL-070"])],
    evrs=[EVR("Policy version register and adoption records",
        "Each policy version with content hash, approver, adoption resolution reference, effective dates and simulation results.",
        prov=["sponsor id", "policy id", "version", "content hash", "approver", "adoption reference", "effective from", "simulation run id"])])
u["questions"] = [
    Q("configurable-policies", "Which sponsor policies are configurable (account minimums, fees, grant minimums, payout requirements, investment options, inactivity rules), and who may change them?",
      "Sponsors differ and need configuration without custom code.",
      "Unauthorized staff alter policy, or needed policies cannot be expressed.",
      [UNB()], cls="customer-preference", imp="high"),
    Q("policy-approval", "How are policy changes approved, versioned and effective-dated, and can they be simulated against existing funds before activation?",
      "Boards want to see the effect of policy changes before adopting them.",
      "Unintended consequences of policy changes discovered only after harm.",
      [UNB(), S("SRC-COSO-2013")], imp="high"),
    Q("vendor-changes", "Can a platform release or vendor configuration change alter a sponsor's policy outcomes without the sponsor's approval?",
      "Sponsor authority over policy must not be eroded by vendor releases.",
      "Vendor changes effectively make sponsor decisions.",
      [UNB(), S("SRC-INTERAGENCY-TPRM-2023")], imp="critical", ind=FI),
    Q("policy-precedence", "How are conflicts resolved between sponsor-wide, program-level and partner-level configurations?",
      "Partners and programs may configure overlapping options.",
      "A partner configuration overrides a sponsor-reserved policy.",
      [UNB()], imp="medium", req=["UNB-GRANT-010"]),
    Q("decision-version-pinning", "For any past decision, can the sponsor see exactly which policy version governed it?",
      "Audit and dispute resolution require the rule that applied.",
      "Inability to explain or defend historical decisions.",
      [UNB(), S("SRC-AICPA-TSC", "PI1.3")], imp="high", req=["UNB-GRANT-038"]),
]
units.append(u)

u = AU("exclusive-control", "Sponsor exclusive legal control, vendor authority limits and independence",
    "The architecture preserves the sponsor's exclusive legal control: charitable assets are titled to the sponsor or its "
    "custodian; external writes express requests, never approvals or money movement; reserved authority (grant "
    "approval, policy adoption, payment release) can be held only by persons appointed by sponsor board resolution, and "
    "vendor staff and AI agents are structurally excluded from it. Vendor operator access to sponsor data is denied by "
    "default and requires sponsor-approved, scoped, expiring delegation or per-case approval, all evidenced. No partner, "
    "embedding host or vendor account appears in the funds flow.",
    "AuthorityMatrix (CNV-GOV-010), A3+ authority rules (CNV-GOV-004), FundsFlow declaration (UNB-XIN-REG-001), operator access delegation (UNB-XIN-IAM-002, CNV-ARC-002).",
    "vendor staff and AI agents would be structurally unable to approve grants or move funds, and vendor access would require sponsor approval.",
    ["UNB-LEG-002", "UNB-LEG-003", "UNB-GRANT-001", "UNB-API-002", "CNV-GOV-004", "CNV-GOV-010", "UNB-XIN-REG-001", "UNB-XIN-OTH-003", "UNB-XIN-IAM-002", "CNV-ARC-002", "CNV-PAY-001", "UNB-AGT-002"],
    policies=["SEC-AUTH-001"], impl="medium", auto="high",
    challenge=CH(
        "Sponsor must show regulators, auditors and donors that it, not the vendor, controls fund assets and distributions.",
        "Vendor employees or tools effectively decide distributions, undermining exclusive legal control and creating fraud paths.",
        "Contract clauses and SOC report user-entity controls assert sponsor control but do not prevent vendor staff with admin access from acting.",
        "Exclusive legal control is part of the DAF definition (§4966(d)(2)) and acknowledgment content (§170(f)(18)); the technical design is not prescribed.",
        "Sponsor-vendor agreements typically state the vendor acts only on sponsor instruction.",
        "Vendors hold broad administrative access governed by policy and periodic access reviews.",
        "Vendor principal types have no reserved-authority capability in the type system, so they cannot approve by construction.",
        "Authority matrix enforcement at the command boundary; operator access requires sponsor-issued delegation.",
        "Every operator access and every reserved-authority action is evidenced and reportable to the sponsor.",
        "Structural exclusion of vendor and agent principals from reserved authority.",
        "Yes, through negative tests and sponsor-visible operator access logs; independent verification would need a SOC 2 or SOC 1 examination.",
        "Likely, if accompanied by independent assurance.",
        "Break-glass or database-level access outside the application could bypass the authority model.",
        "Low to implement contractually; weak in effect.", "Medium engineering cost; requires break-glass design.",
        "Over-restriction could slow incident response.",
        ["Removes the most common insider fraud path", "Aligns with sponsor's legal position"],
        ["Database administrators retain technical capability unless infrastructure access is also constrained", "No independent assurance exists yet"],
        "stronger", "likely"),
    controls=[CTL("Structural exclusion of vendor and agent principals from reserved authority",
        "Make grant approval, policy adoption and payment release unavailable to vendor staff and AI agent principal types.",
        "preventive-structural", "L2-type-system", ext=["UNB-CTRL-004", "UNB-CTRL-064"],
        fw=[S("SRC-AICPA-TSC", "CC6.3"), S("SRC-NIST-SP800-53-R5", "AC-5")], policies=["SEC-AUTH-001"], cwe=["CWE-269"],
        residual=["Infrastructure-level access (database superuser) is outside the application type system."]),
        CTL("Sponsor-approved operator access delegation",
        "Deny vendor operator access to tenant data unless covered by a current sponsor delegation or per-case approval.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-007"])],
    evrs=[EVR("Operator access and reserved-authority action log",
        "Every vendor operator access to sponsor data with delegation reference, and every reserved-authority action with appointing resolution reference.",
        mech="continuous-automated", disclosure="customer-only",
        prov=["tenant id", "principal", "principal type", "delegation or resolution reference", "action", "scope", "time"])])
u["questions"] = [
    Q("exclusive-legal-control", "How does the platform's design preserve the sponsor's exclusive legal control over contributed assets?",
      "Exclusive legal control is fundamental to the DAF structure and the donor's deduction.",
      "Vendor or donor control undermines the sponsor's legal position.",
      [I4966("§4966(d)(2)", "reasonably-inferred"), S("SRC-IRC-170", "§170(f)(18)", "informed-by", "directly-documented"), UNB()],
      cls="legal-regulatory", imp="critical", auth="IRS"),
    Q("vendor-authority", "Can any vendor employee, contractor or AI agent approve a grant, release a payment or change sponsor policy?",
      "Sponsor must retain decision authority.",
      "Insider fraud or vendor overreach.",
      [UNB(), S("SRC-AICPA-TSC", "CC6.3")], imp="critical",
      alts=["Describe segregation between vendor staff and sponsor approval authority.",
            "Can your support staff take actions in our tenant?"]),
    Q("asset-titling", "In whose name are accounts holding contributions and grant funds titled, and does the vendor ever hold, pool or route sponsor funds?",
      "Commingling with vendor funds creates custody and insolvency risk.",
      "Vendor insolvency or fraud affects charitable assets.",
      [UNB(), S("SRC-NACHA-RULES")], imp="critical", req=["CNV-PLT-012"]),
    Q("recommendations-not-binding", "How does the platform ensure donor recommendations are never treated as binding instructions?",
      "Recommendations must remain advisory.",
      "Automatic execution of recommendations erodes sponsor control.",
      [UNB(), S("SRC-PPA-2006")], imp="high"),
    Q("operator-access", "How is vendor operator access to sponsor and donor data approved, scoped, time-limited and reported to the sponsor?",
      "Sponsors need visibility into vendor access to their data.",
      "Unmonitored vendor access to donor records.",
      [UNB(), S("SRC-AICPA-TSC", "CC6.1"), S("SRC-INTERAGENCY-TPRM-2023")], cls="contractual-common", imp="high", ind=FI),
    Q("vendor-independence", "Do the vendor or its owners have board seats, fee-sharing arrangements or other financial interests with sponsors that could compromise sponsor independence?",
      "Board-vendor overlap and related-party fees are observed in the DAF market and draw scrutiny.",
      "Conflicted sponsor decisions about vendor fees and contracts.",
      [S("SRC-ECH-DAF-LANDSCAPE", rel="informed-by", basis="directly-documented"), S("SRC-IRS-FORM-990")], cls="customer-preference", imp="medium",
      oq=["Echelon has no policy on board service or fee sharing with sponsors; one is needed before sales."]),
]
units.append(u)

u = AU("inactive-minimums", "Inactive accounts, account minimums and small-balance handling",
    "Inactivity is a sponsor-configured, versioned policy: the platform detects inactivity by defined criteria, runs "
    "evidenced outreach through every verified channel, applies holds, and executes the sponsor's approved charitable "
    "default (for example a grant to the sponsor's unrestricted fund or named charities) only through an approved "
    "disposition workflow. Minimum opening balances, minimum balances, minimum grants and minimum fees are fee-schedule "
    "policy versions disclosed to donors, each tied to a cost basis, and below-minimum handling follows the sponsor's "
    "disclosed policy rather than silent fee depletion.",
    "Dormancy workflow per ADM-024 and UNB-WF-015, closure via UNB-RCN-ENT-006, minimums via UNB-SMP-ECN-001 and CNV-ECO-002.",
    "inactivity and minimum-balance rules would be sponsor-configured, disclosed and executed with evidenced notices.",
    ["ADM-024", "UNB-WF-015", "UNB-RCN-ENT-006", "UNB-SMP-ECN-001", "CNV-ECO-002", "UNB-LS-015"],
    mech="periodic-automated", fresh="P1D", auto="high", impl="low",
    challenge=CH(
        "Sponsors want inactive funds to keep producing charitable grants and to answer critics about warehoused DAF assets.",
        "Funds sit idle for years; sponsor faces reputational criticism or policy breaches.",
        "Annual manual reports of inactive funds are slow and often not acted on.",
        "No federal payout or inactivity requirement for DAFs exists as of this writing; sponsors adopt their own policies.",
        "Some sponsor policies and disclosures commit to inactivity rules.",
        "Annual staff review of a dormant-fund report with letters to donors.",
        "Not eliminable; inactivity is a donor behavior.",
        "Daily evaluation of inactivity criteria with automatic notice scheduling and hold creation.",
        "Notice delivery and disposition evidence per fund.",
        "Automated detection plus evidenced outreach and sponsor-approved default disposition.",
        "Yes, through per-fund notice and disposition records.",
        "Likely.",
        "If contact data is stale, automated notices do not reach donors; disposition must still wait for sponsor approval.",
        "Low cost, low effectiveness.", "Low to medium.",
        "Automated disposition errors are hard to reverse once grants are paid.",
        ["Turns policy into enforced practice", "Produces evidence for the board"],
        ["Donor relations risk if notices feel automated", "State unclaimed property interpretations of uncashed refunds or checks vary"],
        "stronger", "likely"),
    oq=["Whether any state treats dormant DAF balances or uncashed grant checks as unclaimed property requires counsel review."],
    controls=[CTL("Inactivity detection with evidenced outreach before disposition",
        "Ensure no inactivity disposition occurs without completed, evidenced outreach and sponsor approval.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-019"])],
    evrs=[EVR("Inactivity and minimum-balance evaluation records",
        "Daily evaluation results, notices sent and delivered, holds applied and dispositions approved per fund.",
        mech="periodic-automated", fresh="P1D",
        prov=["fund id", "policy version", "criteria met", "notice ids", "delivery status", "disposition approver", "time"])])
u["questions"] = [
    Q("inactivity-detection", "How does the platform identify inactive accounts, and what outreach, holds and default dispositions does it support?",
      "Sponsors must enforce their inactivity policies.",
      "Funds remain dormant indefinitely, contrary to sponsor policy.",
      [UNB(), S("SRC-ECH-DAF-LANDSCAPE")], cls="industry-convention", imp="high",
      alts=["Do you support a dormant fund policy?"]),
    Q("inactivity-configuration", "Can the sponsor configure inactivity thresholds and default disposition (for example a grant to its unrestricted fund or to charities the donor named), and prove that required notices were sent?",
      "Sponsor policies differ and must be evidenced.",
      "Disposition without adequate notice causes donor complaints or legal challenge.",
      [UNB()], cls="customer-preference", imp="medium"),
    Q("account-minimums", "How does the platform support minimum opening balances, minimum balances, minimum grant amounts and minimum fees, and how are these disclosed to donors?",
      "Minimums drive sponsor economics and must be disclosed.",
      "Undisclosed or inconsistently applied minimums.",
      [UNB()], cls="customer-preference", imp="medium"),
    Q("below-minimum", "What happens when an account falls below the sponsor's minimum balance, and can fees deplete a fund without notice?",
      "Small funds can be consumed by fees.",
      "Donor complaints and reputational harm from silent fee depletion.",
      [UNB()], cls="customer-preference", imp="medium", req=["CNV-FIN-002"]),
    Q("unclaimed-property", "Does the platform treat any DAF balances, refunds or uncashed items as potentially subject to state unclaimed property laws, and how is that decided?",
      "State escheat rules can apply to uncashed checks and refunds.",
      "Missed escheat filings or improper escheat of charitable assets.",
      [S("SRC-STATE-UNCLAIMED-PROPERTY"), UNB()], cls="legal-regulatory", imp="medium", jur=["US-states"], auth="state unclaimed property administrators",
      note="Applicability of unclaimed property law to DAF balances is unsettled and requires counsel review.", req=["CNV-PAY-003"]),
]
units.append(u)

u = AU("excise", "Section 4966, 4967 and 4958 compliance support",
    "Deterministic gates block, before approval and again before release, distributions that would be taxable "
    "distributions under §4966 (natural persons, non-charitable purposes without expenditure responsibility), "
    "prohibited benefits under §4967, and automatic excess benefit transactions under §4958 (grants, loans, "
    "compensation or similar payments to donors, donor-advisors, family members and 35 percent controlled entities). "
    "Disqualified-person relationships are maintained as effective-dated facts. Each policy version records its fund "
    "managers for §4966(a)(2) purposes. When a completed payment is later identified as a possible violation, an "
    "ExciseTaxIncident captures affected grants, parties and approvers and supports correction and Form 4720 data.",
    "Gates per UNB-GRANT-011, CNV-GRT-009 and TVR-GR-006; incident handling per UNB-XIN-NPG-008 and CNV-GRT-010; fund manager register per CNV-GRT-001.",
    "deterministic gates would block likely taxable distributions, prohibited benefits and excess benefit transactions, with incident records for later findings.",
    ["UNB-GRANT-011", "CNV-GRT-009", "CNV-GRT-001", "CNV-GRT-010", "TVR-GR-006", "UNB-XIN-NPG-008", "UNB-LEG-004", "UNB-LS-008", "CNV-GRT-002"],
    policies=["SEC-LANG-002"], impl="high", rec="medium",
    residual=["Benefits not visible in data (for example an undisclosed gala ticket) cannot be detected by gates and depend on donor certification."],
    oq=["Source of truth for 35 percent controlled entity relationships is undefined; donors would self-report."],
    controls=[CTL("Pre-approval and pre-release excise tax gates",
        "Block recommendations whose payee or terms indicate a taxable distribution, prohibited benefit or excess benefit transaction.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-025", "UNB-CTRL-058"],
        fw=[S("SRC-IRC-4966", "§4966(c)"), S("SRC-IRC-4967", "§4967(a)"), S("SRC-IRC-4958", "§4958(c)(2)")]),
        CTL("Excise tax incident record and remediation workflow",
        "Ensure any later-identified violation is captured with parties, approvers and remediation for sponsor and counsel review.",
        "corrective", "L10-external-or-manual", ext=["UNB-CTRL-060"])],
    evrs=[EVR("Excise gate decisions and incident records",
        "Per-recommendation gate outcomes with rule versions, plus ExciseTaxIncident records with remediation status.",
        prov=["grant id", "gate rule version", "outcome", "disqualified-person facts used", "fund managers", "incident id", "time"])])
u["questions"] = [
    Q("taxable-distributions", "How does the platform prevent taxable distributions under section 4966, such as grants to individuals or for non-charitable purposes without expenditure responsibility?",
      "Taxable distributions trigger excise taxes on the sponsor and fund managers.",
      "Sponsor and managers incur excise tax and reputational harm.",
      [I4966("§4966(c)"), UNB()], cls="legal-regulatory", imp="critical", auth="IRS"),
    Q("prohibited-benefits", "How does the platform detect and block grants that would give a donor, advisor or related person more than an incidental benefit under section 4967?",
      "Prohibited benefits trigger excise taxes on the advisor and potentially managers.",
      "Grants used to pay for benefits such as tickets, tuition or memberships.",
      [S("SRC-IRC-4967", "§4967(a)", "derived-from", "directly-documented"), UNB()], cls="legal-regulatory", imp="critical", auth="IRS"),
    Q("excess-benefit", "How are grants, loans, compensation and similar payments from a DAF to donors, advisors and their related persons prevented, given section 4958 treats them as automatic excess benefit transactions?",
      "These transactions are per se excess benefit transactions for DAFs.",
      "Payments to disqualified persons that cannot be cured by fair-value arguments.",
      [S("SRC-IRC-4958", "§4958(c)(2)", "derived-from", "directly-documented"), UNB()], cls="legal-regulatory", imp="critical", auth="IRS"),
    Q("disqualified-persons", "How does the platform identify disqualified persons for each fund (donors, advisors, family members, 35 percent controlled entities), and how is that information kept current?",
      "Gates are only as good as the relationship data behind them.",
      "Payments to related entities go undetected.",
      [S("SRC-IRC-4958", "§4958(f)(7)", "informed-by", "reasonably-inferred"), UNB()], cls="legal-regulatory", imp="high", auth="IRS",
      oq=["No authoritative data source for 35 percent controlled entities is identified."]),
    Q("fund-manager-record", "Does the platform record which fund managers approved each distribution, for purposes of manager-level excise tax exposure?",
      "Managers who knowingly approve taxable distributions face personal tax.",
      "Sponsor cannot identify or defend responsible managers.",
      [I4966("§4966(a)(2)", "reasonably-inferred"), UNB()], cls="legal-regulatory", imp="medium", auth="IRS"),
    Q("post-payment-remediation", "When a completed grant is later identified as a possible taxable distribution or prohibited benefit, what remediation and reporting support does the platform provide?",
      "Correction and reporting must be timely and evidenced.",
      "Unremediated violations and missed Form 4720 filings.",
      [I4966(None, "reasonably-inferred"), UNB()], cls="legal-regulatory", imp="high", auth="IRS",
      oq=["Form 4720 preparation support scope is undefined; no Form 4720 source is seeded."]),
    Q("form-990-schedule-d", "Can the platform produce the DAF data the sponsor reports on Form 990 Schedule D (number of funds, contributions, grants, end-of-year value)?",
      "Sponsors must report aggregate DAF activity annually.",
      "Inaccurate public reporting.",
      [S("SRC-IRS-FORM-990", rel="informed-by", basis="directly-documented"), UNB()], cls="legal-regulatory", imp="high", auth="IRS",
      req=["UNB-GRANT-040", "CNV-FIN-009"]),
]
units.append(u)

u = AU("proposed-regs", "Exposure to the 2023 IRS proposed DAF regulations and rule-change agility",
    "Legal interpretations are versioned data in a machine-checkable regulatory applicability register that distinguishes "
    "binding, proposed and disputed obligations. For the November 2023 proposed DAF regulations, the sponsor records its "
    "election (for example whether to treat personal investment advisers as donor-advisors, or to rely on the proposed "
    "definition for public-charity-only funds), the engine applies the elected rule set, and the impact of the "
    "proposed or final rule can be simulated against existing funds before activation.",
    "Regulatory register per UNB-REGMAP-001..004 with versioned legal assertions (UNB-LEG-001) and policy simulation (UNB-GEX-024).",
    "proposed and final rules would be tracked as versioned interpretations with sponsor elections and impact simulation.",
    ["UNB-LEG-001", "UNB-REGMAP-001", "UNB-REGMAP-003", "UNB-REGMAP-004", "UNB-REGMAP-005", "UNB-GEX-024", "CNV-GRT-009"],
    status="requires-external-validation",
    rationale="The legal status of the 2023 proposed regulations as of 2026-11-25 was not verified in this research, and interpretation requires counsel; the platform capability is specified only in requirements.",
    mech="event-driven-automated", auto="partial", impl="medium", rec="medium",
    oq=["Verify whether the 2023 proposed DAF regulations (REG-142338-07) have been finalized, withdrawn or remain proposed as of 2026-11-25.",
        "Baseline requirements do not mention the proposed regulations except indirectly in CNV-GRT-009; a dedicated requirement is missing."],
    controls=[CTL("Regulatory applicability register with sponsor elections",
        "Record each legal interpretation, its status (binding, proposed, disputed) and the sponsor's election, and bind rule sets to them.",
        "administrative", "L10-external-or-manual", ext=["UNB-CTRL-058"])],
    evrs=[EVR("Regulatory register entries and impact simulations",
        "Versioned interpretation records with citation, accessed date, status, counsel reviewer and simulation runs.",
        mech="event-driven-automated", prov=["reg id", "citation", "status", "accessed date", "reviewer", "sponsor election", "simulation run id"])])
u["questions"] = [
    Q("proposed-regs-readiness", "How would the platform adapt if the 2023 proposed DAF regulations are finalized, including the broader definitions of donor-advisor and taxable distribution?",
      "Sponsors want to know switching costs and readiness for regulatory change.",
      "Platform cannot implement final rules in time, forcing manual workarounds.",
      [S("SRC-IRS-DAF-PROPOSED-REGS-2023", rel="informed-by", basis="directly-documented"), UNB()], cls="customer-preference", imp="high", auth="IRS",
      note="Proposed regulations are not binding until finalized."),
    Q("investment-adviser-as-advisor", "Can the platform treat a personal investment adviser who manages fund assets as a donor-advisor, as the proposed regulations would, and can the sponsor choose whether to do so before finalization?",
      "Treating paid investment advisers as donor-advisors affects fee payments and excess benefit exposure.",
      "Payments to investment advisers become automatic excess benefit transactions after finalization.",
      [S("SRC-IRS-DAF-PROPOSED-REGS-2023", rel="informed-by", basis="directly-documented"), S("SRC-IRC-4958", rel="informed-by")], cls="customer-preference", imp="high", ind=FI, auth="IRS",
      req=["UNB-CUST-014", "UNB-XIN-REG-002"]),
    Q("interpretation-tracking", "How does the platform track the status of proposed versus final rules and record which interpretation each sponsor elected?",
      "Sponsors take different positions pending finalization.",
      "Inconsistent or undocumented positions across funds.",
      [UNB(), S("SRC-IRS-DAF-PROPOSED-REGS-2023")], cls="customer-preference", imp="medium"),
    Q("rule-impact-simulation", "Can the sponsor simulate a rule change against its existing funds and historical grants to estimate impact before activation?",
      "Boards want impact estimates before adopting new interpretations.",
      "Unexpected holds or blocked grants after activation.",
      [UNB()], cls="customer-preference", imp="medium"),
]
units.append(u)
