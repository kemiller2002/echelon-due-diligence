from lib import *

CAT = "FCT"
OWNER = "Not assigned; proposed: Unbound financial controls owner (role not staffed) with sponsor controller as user-entity owner"
DEF = dict(owner=OWNER, industries=["donor-advised-funds", "nonprofit", "financial-services", "wealth-management"],
           juris=["US-federal"], authority="none")

TSC = "SRC-AICPA-TSC"
COSO = "SRC-COSO-2013"
SOC1 = "SRC-AICPA-SSAE-18"
U = "SRC-ECH-UNB-BASELINE"
M = "SRC-ECH-UNB-CONTROL-MATRIX"
SD = "SRC-ECH-UNB-SOC2-DIRECTIVE"

aus = [
dict(
 title="Engine-enforced segregation of duties across financial processes",
 target=("Segregation of duties is enforced by the Unbound command engine, not by procedure. For posting-rule version "
         "approval, manual journals, bank and payee master changes, reconciliation sign-off, close certification and "
         "payment release, the approver must be a different principal from the preparer, and the check runs inside the "
         "command transaction (RR-UNB-ACC-022-r2, CNV-GOV-003). The rule applies to humans, service accounts and AI "
         "agents alike, so one actor cannot control request, approval and reconciliation (GOV-AUTH-004); AI can never "
         "approve its own accounting actions. Until a deterministic release gate is accepted by the sponsor's auditor and "
         "board, payment release requires three distinct people. Reconciliation sits outside the payment chain. Every "
         "conflict evaluation emits a DutyConflictEvaluated event (UNB-SCTRL-002) so an auditor can test the full "
         "population rather than a sample."),
 intended="Implement the SoD conflict matrix as a server-side policy evaluated in every consequential command; publish the matrix per sponsor; negative tests prove self-approval is denied.",
 prov_refs="UNB-ACC-022, RR-UNB-ACC-022-r2, CNV-GOV-003, GOV-AUTH-004, GOV-AUTH-005, UNB-GAP-016",
 statement=("Planned: Unbound's requirements call for segregation of duties enforced by the application engine for "
            "journals, payee changes, reconciliation, close and payment release, including for AI agents. This is not "
            "yet implemented and has not been tested or audited."),
 controls=["ECTL-FCT-001", "ECTL-FCT-009"], evidence=["EVR-FCT-001", "EVR-FCT-008"],
 policies=["SOC2-018", "SEC-AUTH-001"],
 requirements=["UNB-ACC-022", "RR-UNB-ACC-022-r2", "CNV-GOV-003", "GOV-AUTH-004", "GOV-AUTH-005", "UNB-GAP-016", "TVR-ORG-003"],
 impl_cost="medium", rec_cost="low",
 residual=["Small sponsor staffs may lack enough distinct people; compensating controls must be documented with expiry (CNV-GOV-003).",
           "Collusion between two authorized people is not prevented by SoD alone."],
 open_questions=["Who owns the SoD conflict matrix at each sponsor, and how is it versioned and approved?"],
 questions=[
  Q("How do you enforce segregation of duties between the people who prepare, approve and post financial transactions in your platform?",
    "segregation-of-duties", "Customer needs assurance that no single person can initiate and complete a financial transaction.",
    "Unauthorized or erroneous transactions posted without independent review.",
    [D(COSO, "Principle 10"), S(TSC, "CC5.1"), D(U)], "industry-convention", "critical",
    alts=["Describe the segregation of incompatible duties within the application.",
          "Can one user both create and approve a journal entry or payment?"]),
  Q("Is segregation of duties enforced by the application itself at the time of the transaction, or by after-the-fact review of access lists?",
    "segregation-of-duties", "Preventive enforcement is stronger than periodic detective review.",
    "SoD conflicts exist between reviews and are discovered only after loss.",
    [S(COSO, "Principle 10"), D(U), S("SRC-NIST-SP800-53-R5", "AC-5")], "customer-preference", "high",
    alts=["Are SoD rules hard-coded or configurable, and where are they evaluated?"]),
  Q("Do segregation of duties rules apply to service accounts, integrations and AI agents in the same way they apply to human users?",
    "segregation-of-duties", "Automated actors can become an unreviewed path around human SoD.",
    "An automated identity or agent both proposes and approves a transaction.",
    [D(U), S("SRC-NIST-AI-RMF-1.0"), S(TSC, "CC6.1")], "customer-preference", "high",
    alts=["Can an AI agent approve anything it prepared?"], reqs=["GOV-AUTH-004", "RR-UNB-ACC-022-r2", "UNB-ACC-029", "UNB-CTL-001"]),
  Q("Which specific financial functions are covered by your segregation of duties matrix (for example vendor or payee master changes, reconciliations, close sign-off, payment release)?",
    "segregation-of-duties", "Auditors test SoD by function, not by generic statement.",
    "Uncovered functions such as payee master maintenance become fraud paths.",
    [D(U), S(SOC1, "AT-C 320")], "contractual-common", "high",
    alts=["Provide your SoD conflict matrix."]),
  Q("How is reconciliation independent of the people who can initiate or release payments?",
    "segregation-of-duties", "Reconciliation by someone in the payment chain cannot detect that person's errors or fraud.",
    "Concealment of unauthorized disbursements through the reconciliation they themselves perform.",
    [D(U), S(COSO, "Principle 10")], "industry-convention", "high",
    reqs=["CNV-GOV-003", "TVR-ORG-003", "RR-UNB-ACC-022-r2"]),
  Q("How can a sponsor or its auditor obtain evidence that every approval in a period was made by someone other than the preparer?",
    "segregation-of-duties", "Population-level evidence supports auditor reliance without sampling.",
    "SoD cannot be demonstrated, forcing substantive testing or a qualified control conclusion.",
    [S(SOC1, "AT-C 320"), D(U), S(SD)], "contractual-common", "medium",
    disclosure="customer-only"),
 ]),
dict(
 title="Approval limits and delegation of authority with aggregation",
 target=("Every approval is checked against a versioned delegation-of-authority (DoA) register. Each entry declares the "
         "decision type, per-item limit, cumulative limit, aggregation window and key (approver by counterparty), the "
         "board or officer resolution that grants it and an expiry (UNB-XIN-ERP-005). An approval above the per-item limit, "
         "or one that would push the approver's cumulative approvals to the same counterparty over the window limit, is "
         "rejected and escalated, which defeats invoice or grant splitting. Entries become invalid at the next check when "
         "the holder is inactive in the workforce feed or the source resolution is superseded. Grant approvals route by role, "
         "amount, risk, relationship and exception, with dual control where policy requires (RR-UNB-GRANT-012-r1)."),
 intended="Build the DoA register and limit evaluator as a deterministic policy component; feed it from the sponsor's board resolutions and the workforce identity feed.",
 prov_refs="UNB-XIN-ERP-005, UNB-GRANT-012, RR-UNB-GRANT-012-r1, GOV-AUTH-005",
 statement="Planned: approval limits with cumulative aggregation and automatic expiry are specified in Unbound's requirements; they are not implemented or tested.",
 controls=["ECTL-FCT-002"], evidence=["EVR-FCT-002"], policies=["SOC2-018"],
 requirements=["UNB-XIN-ERP-005", "UNB-GRANT-012", "RR-UNB-GRANT-012-r1", "GOV-AUTH-005", "UNB-RULE-020"],
 impl_cost="medium", rec_cost="low",
 residual=["Limits are only as good as the sponsor's resolutions entered into the register; register changes need dual control (UNB-RULE-020)."],
 questions=[
  Q("Does the platform enforce dollar approval limits by user or role, and what happens when a transaction exceeds an approver's limit?",
    "approval-limits", "Customers rely on approval limits set by their board.", "Approvals exceed delegated authority.",
    [D(U), S(COSO, "Principle 12")], "industry-convention", "critical",
    alts=["Describe the approval hierarchy and escalation for large transactions."]),
  Q("How do you prevent an approver from splitting a large payment or grant into several smaller items that each fall under their limit?",
    "approval-limits", "Splitting is a classic way to evade limits.", "Circumvention of delegated authority through structuring.",
    [D(U), S("SRC-MITRE-CWE", "CWE-841")], "customer-preference", "high",
    reqs=["UNB-XIN-ERP-005", "EXC-10", "TVR-SEC-004"]),
  Q("How is the delegation of authority tied to the sponsor's board or officer resolutions, and how are changes to it approved?",
    "delegation-of-authority", "Authority must trace to a governing body decision.",
    "Unauthorized expansion of approval rights through configuration changes.",
    [D(U), S(COSO, "Principle 3")], "industry-convention", "high", reqs=["UNB-XIN-ERP-005", "UNB-RULE-020", "UNB-LEG-005"]),
  Q("What happens to an approver's authority when they leave the organization, change roles or their authorizing resolution expires?",
    "delegation-of-authority", "Stale authority is a common audit finding.", "Departed or reassigned staff continue to approve.",
    [D(U), S(TSC, "CC6.2")], "industry-convention", "high"),
  Q("Can approval limits differ by transaction type, counterparty risk or exception status, and how is the routing rule evidenced?",
    "approval-limits", "Risk-based routing must still be demonstrable.", "Opaque routing lets high-risk items reach low-authority approvers.",
    [D(U)], "customer-preference", "medium", reqs=["RR-UNB-GRANT-012-r1", "UNB-GRANT-012"]),
 ]),
dict(
 title="Change control over fee schedules, rates and fee computation",
 target=("Fees can only be charged under an approved, versioned fee schedule. Each version declares its basis, day count, "
         "accrual and settlement cadence, minimum and exactly one payer source; a schedule with a missing or ambiguous payer "
         "source cannot activate (CNV-FIN-002, UNB-XIN-ERP-002). Schedule publication is a high-risk policy change that requires "
         "dual control (UNB-RULE-020) and is effective-dated rather than edited in place, so fee computation segments at each "
         "version boundary (UNB-XIN-ERP-001). Fee runs are idempotent per fund, schedule, period and segment set and move through "
         "Accrued, Assessed and Posted; waivers are approved exceptions with expiry and corrections are compensating entries "
         "(RR-ADM-028-r1). Only the fee engine may emit authoritative fee events (UNB-XIN-ERP-007). Operator charges to a "
         "sponsor are billed from the operator's own system and never posted into a tenant ledger (UNB-XIN-ERP-003)."),
 intended="Implement fee schedules as immutable versions with an activation gate, independent recomputation and a monthly fee reconciliation.",
 prov_refs="CNV-FIN-002, UNB-XIN-ERP-001, UNB-XIN-ERP-002, UNB-XIN-ERP-003, UNB-XIN-ERP-007, RR-ADM-028-r1, UNB-RULE-020",
 statement="Planned: fee schedules are specified as approved, versioned, dual-controlled records with idempotent fee runs and no in-place edits. Not implemented.",
 controls=["ECTL-FCT-003", "ECTL-FCT-004"], evidence=["EVR-FCT-003", "EVR-FCT-004"],
 policies=["SOC2-018"],
 requirements=["CNV-FIN-002", "UNB-XIN-ERP-001", "UNB-XIN-ERP-002", "UNB-XIN-ERP-003", "UNB-XIN-ERP-007", "RR-ADM-028-r1", "UNB-RULE-020", "UNB-XIN-ECO-018", "UNB-REM-007"],
 impl_cost="medium", rec_cost="low",
 residual=["A correctly approved but economically wrong schedule is still charged; independent recomputation catches calculation errors, not policy errors."],
 open_questions=["Which sponsor role approves fee schedules, and is donor disclosure of schedule changes a contractual or regulatory obligation per sponsor?"],
 questions=[
  Q("How are changes to fee schedules or rates authorized, and can a single administrator change a fee rate?",
    "fee-change-control", "Unauthorized rate changes directly misstate fund balances and revenue.",
    "Overcharging or undercharging funds without authority.",
    [D(U), S(TSC, "CC8.1"), S(COSO, "Principle 10")], "customer-preference", "critical",
    alts=["Describe change control over pricing and fee configuration."]),
  Q("Are fee schedule changes effective-dated and versioned so that historical fee calculations can be reproduced exactly?",
    "fee-change-control", "Auditors and donors may challenge historical fees.", "Inability to reproduce or defend historical fee charges.",
    [D(U), S(TSC, "PI1.3")], "customer-preference", "high", reqs=["CNV-FIN-002", "UNB-XIN-ERP-001"]),
  Q("How do you independently verify that fees actually charged match the approved schedule?",
    "fee-calculation", "Calculation errors are common and can persist for years.", "Systematic fee miscalculation.",
    [D(U), D(M)], "customer-preference", "high", reqs=["RR-ADM-028-r1", "UNB-XIN-ERP-001"]),
  Q("How are fee waivers and exceptions approved, limited in time and reported?",
    "fee-exceptions", "Waivers are an override path that can conceal favoritism or revenue leakage.",
    "Unapproved or perpetual waivers.", [D(U)], "customer-preference", "medium", reqs=["RR-ADM-028-r1", "CNV-FIN-006", "UNB-XIN-ERP-005"]),
  Q("Can the vendor itself change the fees it charges the sponsor, or the fees charged to donor funds, without the sponsor's approval?",
    "vendor-fees", "Customer wants assurance that the vendor cannot unilaterally move money into its own fees.",
    "Vendor-originated fee changes posted to fund assets.", [D(U)], "contractual-common", "high",
    reqs=["UNB-XIN-ERP-003", "UNB-XIN-ERP-002"]),
 ]),
dict(
 title="SOC 1 relevance and plan for customers' financial statement audits",
 target=("Where Echelon hosts or performs fund accounting, NAV or reconciliation for a sponsor it does not control, those "
         "processes are relevant to the sponsor's internal control over financial reporting. The requirement is a SOC 1 Type 2 "
         "report covering ledger posting, NAV and unitization, reconciliation, change management and logical access, obtained "
         "before the first such sponsor's fiscal year end, with a sponsor-specific list of complementary user entity controls "
         "(UNB-XIN-ACC-009, CNV-GOV-001). Before live reliance, the sponsor's external auditor's planned approach (rely on a "
         "SOC 1, test Unbound directly or test substantively) is recorded, and the control register tags each control with the "
         "report it supports (UNB-RCN-PLT-013). Today no SOC 1 or SOC 2 report exists and none is in progress."),
 intended="Begin SOC 1 Type 2 readiness, including the first observation period, before the first staffed-administration client goes live (CNV-GOV-001); engage a CPA firm to confirm scope.",
 prov_refs="UNB-XIN-ACC-009, CNV-GOV-001, UNB-RCN-PLT-013, TVR-CMP-001",
 statement="Echelon has no SOC 1 or SOC 2 report. Unbound's requirements plan a SOC 1 Type 2 before any sponsor relies on Unbound for fund accounting at year end; until then auditors would need to test directly or substantively.",
 kind="not-available", controls=["ECTL-FCT-007"], evidence=["EVR-FCT-007", "EVR-FCT-009"],
 policies=["SOC2-021", "SOC2-022", "SOC2-036"],
 requirements=["UNB-XIN-ACC-009", "CNV-GOV-001", "UNB-RCN-PLT-013", "TVR-CMP-001", "CNV-PLT-009"],
 freshness="P1Y", mechanism="external-attestation", automation="partial", disclosure="nda",
 impl_cost="high", rec_cost="high",
 residual=["A SOC 1 covers only the scoped period and controls; sponsors still own their CUECs."],
 open_questions=["Which CPA firm, and what period start date is realistic given no production system exists?"],
 challenge=dict(
  customer_intent="The sponsor's auditor needs a basis to rely on controls at the service organization that affect the sponsor's financial statements.",
  adverse_outcome="Auditor cannot rely on Unbound controls, increasing audit fees or producing control deficiencies at the sponsor.",
  conventional_control_effectiveness="A SOC 1 Type 2 tests a sample of control operation over a period and is widely accepted, but its evidence is retrospective and sampled.",
  legally_required="Not by statute for nonprofit sponsors. For SEC-registrant customers, management's ICFR assessment under SOX 404 must address outsourced processes, which usually means a SOC 1.",
  contractually_required="Commonly required in service contracts and by user auditors; CNV-GOV-001 requires contracts to include right-to-audit and an evidence pack.",
  historical_convention="SOC 1 (formerly SAS 70) is the default reliance mechanism for outsourced accounting.",
  architectural_elimination="Not possible; reliance is an auditor judgment.",
  automatic_enforcement="Engine-enforced controls (SoD, balanced journals, period locks) reduce the number of manual controls the report must cover.",
  continuous_evidence="Full-population, generated evidence with information-produced-by-entity support could let auditors test every instance rather than a sample.",
  stronger_alternative="Continuous population-level evidence plus a SOC 1 Type 2, rather than instead of one.",
  alternative_verifiable="Only if the auditor validates the evidence-generating system (ITGCs and IPE); CNV-GOV-001 permits replacing manual procedures only after auditor confirmation.",
  customer_acceptance_likelihood="Low as a replacement, high as a supplement.",
  invalidating_conditions="Ineffective ITGCs or unvalidated report logic would make generated evidence unreliable.",
  conventional_cost="High: CPA fees and an observation period, recurring annually.",
  alternative_cost="Medium engineering cost to generate evidence; does not remove audit fees.",
  alternative_risks="Overclaiming that continuous evidence is equivalent to an attestation.",
  supporting_arguments=["Population testing is technically stronger than sampling.", "Generated evidence lowers recurring audit effort."],
  opposing_arguments=["User auditors are bound by professional standards that assume a service auditor's report or direct testing.",
                      "First-party evidence is not independent.", "A new vendor with no operating history is unlikely to be trusted without an attestation."],
  technical_effectiveness="stronger", institutional_acceptance="unlikely"),
 questions=[
  Q("Do you have a SOC 1 Type 2 report covering the services that affect our financial statements, and what period and controls does it cover?",
    "soc-1", "Sponsor's auditor needs a basis for reliance.", "Inability of the customer's auditor to rely on vendor controls.",
    [D(SOC1, "AT-C 320"), D(U)], "contractual-common", "critical",
    alts=["Provide your most recent SSAE 18 SOC 1 report and bridge letter.", "Is your SOC 1 Type 1 or Type 2?"]),
  Q("If you do not yet have a SOC 1 report, how will our external auditor obtain sufficient evidence about controls at your organization for our year-end audit?",
    "soc-1", "Gap planning before go-live.", "Audit delays, added fees or qualified findings in the first year.",
    [D(SOC1, "AT-C 320"), D(U)], "contractual-common", "critical", reqs=["CNV-GOV-001", "UNB-XIN-ACC-009"]),
  Q("Which complementary user entity controls must we operate for your controls to achieve their objectives, and are they specific to our configuration?",
    "cuec", "Sponsors must operate CUECs for the SOC conclusion to hold.", "Unperformed CUECs void reliance.",
    [D(SOC1, "AT-C 320"), D(U), S("SRC-AICPA-SOC2-GUIDE")], "contractual-common", "high", reqs=["UNB-XIN-ACC-009", "CNV-GOV-001", "SOC2-022"]),
  Q("For public-company customers, how do your controls support our management's assessment of internal control over financial reporting under SOX 404?",
    "sox", "ICFR assessments must include outsourced processes.", "Material weakness or scope limitation in management's ICFR assessment.",
    [D("SRC-SOX-404", "Section 404"), S(SOC1, "AT-C 320")], "legal-regulatory", "high",
    industries=["financial-services", "wealth-management", "banking"], authority="SEC; PCAOB (for auditor standards)",
    scope="Applies only to customers that are SEC registrants or consolidated into one; most DAF sponsors are not."),
  Q("Which subservice organizations are relevant to your controls over our financial reporting, and are they carved out or included?",
    "subservice", "Carve-outs shift testing burden to the customer.", "Unexamined subservice controls (hosting, banks, custodians).",
    [D(SOC1, "AT-C 320"), S(SD)], "contractual-common", "medium", reqs=["UNB-XIN-ACC-009", "SOC2-013", "SOC2-022"],
    oq=["Hosting provider and payment partners are not yet selected, so subservice organizations cannot be named."]),
 ]),
dict(
 title="Internal control framework, control register and control state honesty",
 target=("Unbound's financial controls are organized around a COSO-aligned control register in which every control has a "
         "unique ID, owner, objective, risk, trigger, evidence schema, source system, reviewer and failure behavior (SOC2-001, "
         "TVR-CMP-001). The register separates Proposed, Designed, Implemented, Operating, Tested, Deficient, Remediating and "
         "AuditorReviewed and never infers one state from another (SOC2-019). Today all 90 UNB-CTRL controls in the master "
         "matrix are Designed only, with no operating evidence, test execution or auditor review. Every material capability has "
         "exactly one accountable human role even when execution is automated (UNB-CTL-003)."),
 intended="Operate the register as data that generates customer answers, so a status can only advance with attached evidence.",
 provable=("The master enterprise control matrix exists as a design document (" + UNB + ":requirements/governance/MASTER-ENTERPRISE-CONTROL-MATRIX.csv) "
           "showing every control as Designed with operating evidence, test execution and auditor review all No. Nothing operational."),
 prov_refs="SOC2-001, SOC2-008, SOC2-019, TVR-CMP-001, UNB-CTL-003",
 statement="Echelon has a designed (not implemented) control matrix for Unbound mapped toward SOC 1 and SOC 2 criteria. No control is operating or tested.",
 kind="planned",
 controls=["ECTL-FCT-005"], evidence=["EVR-FCT-005"], policies=["SOC2-001", "SOC2-008", "SOC2-019", "SOC2-020"],
 requirements=["SOC2-001", "SOC2-008", "SOC2-019", "TVR-CMP-001", "UNB-CTL-003", "SOC2-034", "SOC2-035"],
 freshness="P1M", mechanism="continuous-automated", impl_cost="low", rec_cost="low",
 residual=["COSO alignment is a design claim until an independent party evaluates it."],
 questions=[
  Q("What internal control framework do you use for controls over financial processing, such as COSO 2013?",
    "control-framework", "Common language with the customer's auditors.", "Ad hoc controls with gaps in coverage.",
    [D(COSO), S(SOC1)], "industry-convention", "medium", alts=["Is your internal control program aligned to COSO?"]),
  Q("Do you maintain a control register that identifies each financial control, its owner, frequency, evidence and current operating status?",
    "control-register", "Customers need to know which controls actually operate.", "Controls described in policy but not operated.",
    [D(SD), S(COSO, "Principle 12"), D(M)], "customer-preference", "high"),
  Q("How do you distinguish controls that are designed from those that are implemented, operating and independently tested when you describe them to customers?",
    "control-status", "Prevents overstatement of control maturity.", "Customer relies on controls that do not operate.",
    [D(SD), S(COSO, "Principle 16")], "customer-preference", "high", reqs=["SOC2-019", "SOC2-020", "SOC2-008"]),
  Q("How are control deficiencies identified, communicated and remediated, and who is informed?",
    "deficiencies", "Deficiency handling is part of a functioning control system.", "Known deficiencies persist without remediation.",
    [D(COSO, "Principle 17"), S(SD)], "industry-convention", "medium", reqs=["SOC2-005", "SOC2-019", "SOC2-033"]),
 ]),
dict(
 title="Management review controls and reliability of information used in review",
 target=("Management review controls in Unbound operate on reports whose completeness and accuracy can be proven. Every "
         "financial report, statement and dashboard figure is computed from a sealed financial snapshot identified by sponsor "
         "entity, period or as-of instant and ledger commit watermark, so recomputation yields identical figures (UNB-XIN-EVA-003). "
         "Generated reports carry information-produced-by-entity support: query definition, parameters, population counts, hash "
         "and run log (CNV-GOV-001). The controller signs off reconciliation completeness monthly (CNV-FIN-004), review sign-offs "
         "and exceptions are evidence events (UNB-CTRL-045, UNB-CTRL-048), and control owners attest periodically while independent "
         "reviewers challenge completeness (SOC2-024). Manual review is replaced by generated evidence only after the auditor confirms reliance."),
 intended="Generate IPE packages automatically with each review report and record reviewer, precision threshold and follow-up in the evidence store.",
 prov_refs="UNB-XIN-EVA-003, CNV-GOV-001, CNV-FIN-004, SOC2-024",
 statement="Planned: review reports are specified to be reproducible from sealed ledger snapshots with information-produced-by-entity support. Not implemented.",
 controls=["ECTL-FCT-006"], evidence=["EVR-FCT-006", "EVR-FCT-010"], policies=["SOC2-024", "SOC2-009"],
 requirements=["UNB-XIN-EVA-003", "CNV-GOV-001", "CNV-FIN-004", "SOC2-024", "UNB-ACC-019"],
 freshness="P1M", mechanism="periodic-automated", impl_cost="medium", rec_cost="medium",
 challenge=dict(
  customer_intent="Ensure a knowledgeable person reviews financial results with enough precision to catch material errors.",
  adverse_outcome="Material misstatement passes review because the reviewer looked at incomplete or wrong data or reviewed superficially.",
  conventional_control_effectiveness="Management review controls are frequently cited by auditors as insufficiently precise or lacking evidence of what was reviewed.",
  legally_required="No.", contractually_required="Implicitly, through SOC 1 control objectives and sponsor audit expectations.",
  historical_convention="Signed review checklists and email approvals.",
  architectural_elimination="Partially: reproducible sealed snapshots eliminate the data-completeness question for review inputs.",
  automatic_enforcement="Deterministic exception rules (breaks, thresholds, aging) can flag every item that exceeds precision, leaving humans to judge exceptions.",
  continuous_evidence="IPE metadata and sign-off events per report.",
  stronger_alternative="Rule-based exception detection on the full population plus human review of exceptions and of the rules themselves.",
  alternative_verifiable="Yes, if rule versions, thresholds and outputs are retained and the auditor validates the rules.",
  customer_acceptance_likelihood="Moderate; auditors accept exception-based review when thresholds are documented and IPE is supported.",
  invalidating_conditions="Rules that are not independently approved or thresholds loosened without second approval (RR-UNB-ACC-018-r1).",
  conventional_cost="Low tooling cost, high recurring staff time.", alternative_cost="Medium build, lower recurring time.",
  alternative_risks="Reviewers may rubber-stamp clean exception reports; judgment-only risks (estimates, classifications) are not rule-detectable.",
  supporting_arguments=["Full population coverage.", "Precision becomes explicit and testable."],
  opposing_arguments=["Some reviews require judgment that rules cannot encode.", "Auditors still need evidence the reviewer understood and investigated exceptions."],
  technical_effectiveness="stronger", institutional_acceptance="uncertain"),
 questions=[
  Q("What management review controls exist over financial results produced by the platform, and how is the precision of each review defined?",
    "management-review", "Review controls are often the key ICFR control.", "Imprecise reviews miss material errors.",
    [D(COSO, "Principle 10"), S(SOC1, "AT-C 320")], "industry-convention", "high"),
  Q("How do you demonstrate the completeness and accuracy of reports and queries used in control reviews (information produced by the entity)?",
    "ipe", "Auditors test IPE before relying on review controls.", "Review based on incomplete reports.",
    [D(COSO, "Principle 13"), D(U), S(TSC, "PI1.4")], "contractual-common", "high", reqs=["CNV-GOV-001", "UNB-XIN-EVA-003"]),
  Q("If a financial report is regenerated later, will it produce exactly the same figures that were reviewed, and how is that proven?",
    "reproducibility", "Reviewed figures must remain defensible.", "Unexplained differences between reviewed and later-produced reports.",
    [D(U), S(TSC, "PI1.4")], "customer-preference", "medium", reqs=["UNB-XIN-EVA-003", "UNB-IMM-004"]),
  Q("How is evidence of review retained, including who reviewed, what they examined, exceptions found and follow-up?",
    "management-review", "Undocumented reviews cannot be relied on.", "Review cannot be evidenced at audit.",
    [S(COSO, "Principle 16"), D(SD)], "contractual-common", "medium", reqs=["SOC2-024", "CNV-FIN-004", "SOC2-005"]),
 ]),
dict(
 title="Automation, AI and deterministic rules within financial controls",
 target=("Unbound classifies every decision as deterministic (D), probabilistic recommendation or flag (P) or human-authorized "
         "(H); a probabilistic output alone can never clear a control or move money (UNB-CTL-001). AI may propose journal drafts "
         "and classifications but cannot bypass posting, approval or reconciliation controls (UNB-ACC-029); state-changing events "
         "with financial consequences come only from approved deterministic rules or authorized people (UNB-EVT-005); model-only "
         "auto-clear designs are prohibited (UNB-CTL-005). A deterministic release gate counts as an approver only when it runs a "
         "published, independently approved policy version, the human approvers cannot author or deploy it, ITGCs are effective "
         "and the auditor and board have accepted the design (CNV-GOV-003). Changes to control-relevant modules need two "
         "approvers, neither the author, and signed builds (CNV-PLT-010)."),
 intended="Encode D/P/H classification in the command catalog; agent principals can write only to an AI observation store (UNB-XIN-EVA-016).",
 prov_refs="UNB-CTL-001, UNB-CTL-005, UNB-ACC-029, UNB-EVT-005, CNV-GOV-003, CNV-PLT-010, UNB-XIN-EVA-016",
 statement="Planned: AI and automation in Unbound are specified to propose only; deterministic gates count as an approver only after auditor and board acceptance. Not implemented.",
 controls=["ECTL-FCT-001", "ECTL-FCT-010"], evidence=["EVR-FCT-001", "EVR-FCT-011"], policies=["SOC2-017", "SOC2-018"],
 requirements=["UNB-CTL-001", "UNB-CTL-005", "UNB-ACC-029", "UNB-EVT-005", "CNV-GOV-003", "CNV-PLT-010", "UNB-XIN-EVA-016"],
 impl_cost="medium", rec_cost="low",
 challenge=dict(
  customer_intent="Ensure no automated process can move money or alter books without accountable human authority.",
  adverse_outcome="Defective or manipulated automation releases funds or posts entries at scale.",
  conventional_control_effectiveness="Human dual approval is familiar but degrades with volume (approval fatigue) and is weak against well-crafted fraud.",
  legally_required="No statute requires a human approver for each payment; sponsor boards and auditors decide.",
  contractually_required="Bank agreements and sponsor policies commonly require dual control on release.",
  historical_convention="Two human approvals in a bank portal.",
  architectural_elimination="Agents have no write path to authoritative tables (UNB-XIN-EVA-016), which removes direct AI posting within that scope.",
  automatic_enforcement="An independently approved deterministic gate applies the same policy to every item without fatigue.",
  continuous_evidence="Gate version, inputs and decision for each item.",
  stronger_alternative="Deterministic gate as one approver plus human approval for exceptions and above-threshold items, with change control on the gate stronger than on any single approval.",
  alternative_verifiable="Yes, through ITGC testing of the gate and its change control, which CNV-GOV-003 makes a precondition.",
  customer_acceptance_likelihood="Uncertain; depends on each sponsor's auditor and board.",
  invalidating_conditions="Ineffective change management over the gate, or approvers able to influence gate policy.",
  conventional_cost="High recurring staff time, especially at year-end surge.", alternative_cost="Medium build plus ITGC assurance cost.",
  alternative_risks="A single defect affects every item; correlated failure.",
  supporting_arguments=["Consistency across items.", "Removes approval fatigue.", "CNV-GOV-003 keeps three-person release until acceptance."],
  opposing_arguments=["Auditors may view an automated approver as a single point of failure.", "Board members may expect a named person to approve each disbursement."],
  technical_effectiveness="equivalent", institutional_acceptance="uncertain"),
 questions=[
  Q("Can any automated process or AI model approve a journal entry, grant or payment without a human approval?",
    "automation-authority", "Customers want accountable human authority over money movement.", "Autonomous release of funds by defective automation.",
    [D(U), S("SRC-NIST-AI-RMF-1.0"), S("SRC-OWASP-AGENTIC-AI")], "customer-preference", "critical"),
  Q("If you use an automated rule as one of the approvers for payment release, what conditions must be met before that is permitted, and who accepts it?",
    "automation-authority", "Automated approval must be governed more strictly than human approval.", "Unvalidated automation replacing human control.",
    [D(U), S(COSO, "Principle 11")], "customer-preference", "high", reqs=["CNV-GOV-003", "CNV-PLT-010"]),
  Q("How are changes to the code or configuration that implements financial controls approved, and can the people who approve payments also change those rules?",
    "itgc", "ITGCs underpin all automated controls.", "Control logic altered by those it constrains.",
    [D(COSO, "Principle 11"), S(TSC, "CC8.1"), D(U)], "industry-convention", "high", reqs=["CNV-PLT-010", "CNV-GOV-003", "SOC2-011"]),
  Q("Are AI-generated suggestions (for example account classifications or reconciliation matches) clearly distinguished from approved entries in the books and audit trail?",
    "ai-in-accounting", "Auditors must distinguish proposals from authorized entries.", "AI output mistaken for authorized accounting.",
    [D(U), S("SRC-NIST-AI-600-1")], "customer-preference", "medium", reqs=["UNB-ACC-029", "UNB-XIN-EVA-016", "UNB-CTL-001"]),
 ]),
dict(
 title="Exceptions, overrides, emergency access and compensating controls",
 target=("Exceptions to financial controls are explicit records with risk acceptance authority, expiry, compensating controls "
         "and follow-up (SOC2-033). Break-glass access uses sealed credentials outside the workforce IdP, needs two-person "
         "activation, expires within four hours and cannot perform domain transitions such as grant approval, payee change, "
         "ledger posting or hold removal (UNB-XIN-IAM-005). Any platform hold executes a sponsor-adopted policy, is time-bounded "
         "and never moves funds (CNV-PLT-007). Where a sponsor lacks staff for full SoD, enforced leave applies when two trained "
         "staff exist and anomaly analytics otherwise; each alternative control is documented with expiry (CNV-GOV-003, TVR-SEC-006). "
         "Any authoritative state change without a matching command event blocks affected payments until reviewed."),
 intended="Implement the exception register and break-glass workflow, and run cross-role anomaly analytics for small-staff sponsors.",
 prov_refs="SOC2-033, UNB-XIN-IAM-005, CNV-PLT-007, CNV-GOV-003, TVR-SEC-006, UNB-ECO-003",
 statement="Planned: break-glass access is specified as two-person, time-limited and unable to approve, post or change payees. Not implemented.",
 controls=["ECTL-FCT-008", "ECTL-FCT-009"], evidence=["EVR-FCT-010", "EVR-FCT-008"], policies=["SOC2-033"],
 requirements=["SOC2-033", "UNB-XIN-IAM-005", "CNV-PLT-007", "CNV-GOV-003", "TVR-SEC-006", "UNB-ECO-003", "UNB-XIN-IAM-004"],
 impl_cost="medium", rec_cost="medium",
 questions=[
  Q("What override or emergency access exists over financial controls, who can use it, and what can it do?",
    "emergency-access", "Overrides are where controls fail.", "Emergency access used to post or release funds.",
    [D(U), S("SRC-NIST-SP800-53-R5", "AC-2"), S(COSO, "Principle 10")], "customer-preference", "critical",
    alts=["Describe break-glass procedures for production financial data."]),
  Q("How do you handle segregation of duties when a customer has too few staff to separate all incompatible duties?",
    "small-entity", "Small sponsors cannot fully staff SoD.", "SoD waived silently.",
    [D(U), S(COSO, "Principle 10")], "industry-convention", "high", reqs=["CNV-GOV-003", "TVR-SEC-006", "UNB-ECO-003"]),
  Q("How are user access rights to financial functions, including users of linked bank portals, reviewed and recertified?",
    "access-review", "Access reviews are a core ITGC.", "Excess or stale access to money movement.",
    [D(U), S(TSC, "CC6.2"), S("SRC-NIST-SP800-53-R5", "AC-2")], "industry-convention", "high", reqs=["UNB-XIN-IAM-004", "TVR-SEC-008"]),
 ]),
]

controls = [
 C("Server-side segregation of duties conflict evaluation", "Reject any consequential financial command whose approver is the preparer or holds an incompatible role for that item, for humans, service accounts and agents.",
   "preventive-structural", "L3-restricted-interface", ["Unbound authorization component (specified, not built)", "PostgreSQL"], ["EVR-FCT-001"],
   related=["UNB-SCTRL-002", "UNB-CTRL-004", "UNB-CTRL-043", "UNB-CTRL-046"], policies=["SEC-AUTH-001", "SOC2-018"], cwe=["CWE-841", "CWE-285"],
   refs=[S("SRC-COSO-2013", "Principle 10"), S("SRC-NIST-SP800-53-R5", "AC-5"), S("SRC-AICPA-TSC", "CC5.1")],
   residual=["Collusion", "Misconfigured conflict matrix"]),
 C("Delegation-of-authority limit and aggregation check", "Reject approvals beyond per-item or cumulative limits per approver and counterparty, or from expired or inactive authority, and escalate.",
   "preventive-structural", "L3-restricted-interface", ["Unbound authorization component (specified, not built)"], ["EVR-FCT-002"],
   related=["UNB-SCTRL-001", "UNB-CTRL-025"], cwe=["CWE-841"], refs=[S("SRC-COSO-2013", "Principle 3")]),
 C("Fee schedule activation gate", "Allow a fee schedule version to activate only with a single declared payer source, complete parameters and dual approval; versions are immutable and effective-dated.",
   "preventive-gate", "L3-restricted-interface", ["Unbound fee engine (specified, not built)"], ["EVR-FCT-003"],
   related=["UNB-SCTRL-032", "UNB-CTRL-055"], refs=[S("SRC-AICPA-TSC", "CC8.1")]),
 C("Independent fee recomputation and reconciliation", "Recompute posted fees from approved schedule versions and balances and raise exceptions for any difference.",
   "detective-automated", "L6-automated-analysis", ["Unbound fee engine (specified, not built)"], ["EVR-FCT-004"],
   related=["UNB-CTRL-056", "UNB-CTRL-057"], refs=[S("SRC-AICPA-TSC", "PI1.3")]),
 C("Evidence-gated control register", "Control status can advance beyond Designed only when attached operating or test evidence exists; no state is inferred from another.",
   "preventive-gate", "L6-automated-analysis", ["Unbound control register (specified, not built)", "Praxis (exists; not operated for a production Echelon service)"], ["EVR-FCT-005"],
   policies=["SOC2-019", "SOC2-008"], refs=[S("SRC-COSO-2013", "Principle 16")],
   notes="Praxis provides provenance and validation for repository records today; using it to gate a production control register is unverified."),
 C("Sealed snapshot reporting with IPE support", "Compute every review report from a sealed ledger snapshot and attach query definition, parameters, population counts, hash and run log.",
   "preventive-structural", "L3-restricted-interface", ["Unbound reporting component (specified, not built)", "Folio (exists; not operated for a production Echelon service)"], ["EVR-FCT-006"],
   related=["UNB-CTRL-045", "UNB-CTRL-088"], refs=[S("SRC-COSO-2013", "Principle 13"), S("SRC-AICPA-TSC", "PI1.4")]),
 C("SOC 1 Type 2 examination", "Obtain an independent service auditor's report on controls relevant to sponsors' ICFR before reliance at a sponsor year end.",
   "administrative", "L10-external-or-manual", ["External CPA firm (not engaged)"], ["EVR-FCT-007", "EVR-FCT-009"],
   policies=["SOC2-036"], refs=[D("SRC-AICPA-SSAE-18", "AT-C 320")], residual=["Period-limited sampled assurance"]),
 C("Two-person time-limited break-glass without domain transitions", "Emergency production access requires two-person activation, expires within four hours and is technically unable to approve, post, change payees or remove holds.",
   "preventive-structural", "L3-restricted-interface", ["Unbound identity and access component (specified, not built)"], ["EVR-FCT-010"],
   related=["UNB-SCTRL-005"], refs=[S("SRC-NIST-SP800-53-R5", "AC-2")]),
 C("Collusion-resistant analytics, enforced leave and access recertification", "Detect cross-role anomalies, enforce leave or rotation where staffing allows, and recertify financial and bank-portal access quarterly.",
   "detective-automated", "L9-runtime-monitored", ["Unbound monitoring (specified, not built)"], ["EVR-FCT-008"],
   related=["UNB-CTRL-006", "UNB-SCTRL-003", "UNB-SCTRL-004"], refs=[S("SRC-COSO-2013", "Principle 8")],
   residual=["Analytics may miss low-and-slow collusion"]),
 C("Agent principals restricted to observation writes", "AI agent identities can insert only into the AI observation store; authoritative journal, reservation and fact tables reject agent writes at the database privilege level.",
   "preventive-structural", "L3-restricted-interface", ["PostgreSQL role privileges (planned)", "Unbound command engine (specified, not built)"], ["EVR-FCT-011"],
   related=["UNB-SCTRL-035", "UNB-CTRL-064"], policies=["SOC2-017"], cwe=["CWE-269"]),
]

evidence = [
 E("Duty conflict evaluations", "One record per consequential command showing preparer, approver, roles evaluated, matrix version and allow or deny.", NOT_ASSIGNED.format("Unbound authorization component"), "event-driven-automated", "per-event"),
 E("Delegation-of-authority register and limit decisions", "Versioned DoA entries with source resolutions and each limit check outcome including cumulative totals.", NOT_ASSIGNED.format("Unbound authorization component"), "event-driven-automated", "per-event"),
 E("Fee schedule version approvals", "Each schedule version, its parameters, payer source, approvers and activation timestamp.", NOT_ASSIGNED.format("Unbound fee engine"), "event-driven-automated", "per-event"),
 E("Fee recomputation reconciliation report", "Monthly comparison of posted fees with independent recomputation, with exceptions and resolution.", NOT_ASSIGNED.format("Unbound fee engine"), "periodic-automated", "P1M", fmt="Folio-rendered report with machine-readable data"),
 E("Control register export", "Control IDs, owners, states and the evidence that justifies each state, generated from the register.", NOT_ASSIGNED.format("Unbound control register"), "continuous-automated", "P1M"),
 E("Information-produced-by-entity package", "Query definition, parameters, population counts, snapshot identifier, hash and run log for each generated review report.", NOT_ASSIGNED.format("Unbound reporting component"), "event-driven-automated", "per-event"),
 E("SOC 1 Type 2 report", "Independent service auditor's report and any bridge letter.", "External CPA firm (not engaged)", "external-attestation", "P1Y", fmt="PDF report", independence="independent-third-party", disclosure="nda", signing="Signed by the service auditor", notes="Does not exist. No engagement has started."),
 E("Access recertification and collusion analytics results", "Quarterly recertification of privileged and financial roles including bank portal users, and analytics alerts with disposition.", NOT_ASSIGNED.format("Unbound identity and monitoring components"), "periodic-automated", "P90D"),
 E("Complementary user entity control list", "Per-sponsor list of CUECs derived from that sponsor's configuration.", NOT_ASSIGNED.format("Unbound control register"), "event-driven-automated", "per-event", disclosure="customer-only"),
 E("Exception and break-glass register", "Each control exception or break-glass session with approvers, scope, expiry, actions taken and post-event review.", NOT_ASSIGNED.format("Unbound identity and access component"), "event-driven-automated", "per-event"),
 E("Agent write-denial and authority decisions", "Records of agent tool invocations and denied attempts to write authoritative data.", NOT_ASSIGNED.format("Unbound AI gateway"), "event-driven-automated", "per-event"),
]
