from lib import *

CAT = "ACT"
OWNER = "Not assigned; proposed: Unbound ledger product owner (role not staffed) with each sponsor's controller as accounting-policy owner"
DEF = dict(owner=OWNER, industries=["donor-advised-funds", "nonprofit", "financial-services"],
           juris=["US-federal"], authority="none")

ASC = "SRC-FASB-ASC-958"
U = "SRC-ECH-UNB-BASELINE"
TSC = "SRC-AICPA-TSC"
COSO = "SRC-COSO-2013"
SOC1 = "SRC-AICPA-SSAE-18"
N53 = "SRC-NIST-SP800-53-R5"

aus = [
dict(
 title="Balanced double-entry journals by entity, currency and balancing segment",
 target=("Every Unbound posting is double-entry and must balance, in exact decimal, separately for each combination of "
         "accounting entity, transaction currency and every balancing segment declared in the posting policy; for DAF books "
         "fund and restriction are mandatory balancing segments (RR-UNB-ACC-002-r1, UNB-RCN-FIN-006). A journal that fails any "
         "check is rejected, not posted. Multicurrency postings balance in both transaction and functional currency under an "
         "approved FX method and unlike currencies are never summed (ACC-MDL-003, UNB-ACC-016). Every posted line carries valid "
         "required dimensions (ACC-MDL-001). Internal fund transfers use clearing lines that net to zero sponsor-wide per currency. "
         "The balance rule is enforced both in the typed posting command and by database constraints on the journal tables, "
         "and property-based tests generate random journals to prove unbalanced entries cannot persist."),
 intended="Implement a single posting command with a private-constructor F# journal type and database CHECK or deferred constraints; publish the balancing-segment policy per book.",
 prov_refs="UNB-ACC-002, RR-UNB-ACC-002-r1, ACC-MDL-001, ACC-MDL-003, UNB-RCN-FIN-006, UNB-ACC-016",
 statement="Planned: Unbound's ledger is specified to reject any journal that does not balance per entity, currency, fund and restriction. Not implemented or tested.",
 controls=["ECTL-ACT-001", "ECTL-ACT-011"], evidence=["EVR-ACT-001", "EVR-ACT-011"], policies=["SOC2-018"],
 requirements=["UNB-ACC-002", "RR-UNB-ACC-002-r1", "ACC-MDL-001", "ACC-MDL-003", "UNB-RCN-FIN-006", "UNB-ACC-016", "UNB-SCTRL-025", "UNB-ACC-030"],
 impl_cost="medium", rec_cost="low",
 questions=[
  Q("Does the system enforce double-entry accounting so that every journal entry balances before it can be posted?",
    "journal-integrity", "Unbalanced entries corrupt every downstream report.", "Misstated balances and unreconcilable ledgers.",
    [D(U), S(TSC, "PI1.3"), S(COSO, "Principle 10")], "industry-convention", "critical",
    alts=["Can an out-of-balance entry ever be saved?"]),
  Q("Do journals balance within each individual fund and restriction class, not only in total for the organization?",
    "fund-accounting", "Fund-level balance is the essence of fund accounting.", "Assets of one fund silently funding another.",
    [D(U), S(ASC, "958-205")], "industry-convention", "critical", reqs=["RR-UNB-ACC-002-r1", "UNB-RCN-FIN-006"]),
  Q("How are multicurrency transactions recorded and balanced, and can currency conversion change the source transaction amount?",
    "multicurrency", "International grants and gifts need correct FX accounting.", "Hidden FX gains or losses and misstated source amounts.",
    [D(U)], "customer-preference", "medium", reqs=["ACC-MDL-003", "UNB-ACC-016"],
    scope="Applies only to sponsors that enable non-USD activity."),
  Q("Is balance enforced in the database itself, so that a defect or direct database access cannot persist an unbalanced journal?",
    "journal-integrity", "Application-only checks can be bypassed.", "Unbalanced data written outside the application path.",
    [D(U), S(N53, "SI-7"), S("SRC-ECH-SCS-0.1")], "customer-preference", "high", reqs=["RR-UNB-ACC-002-r1", "RR-UNB-ACC-026-r1", "CNV-PLT-010"]),
  Q("What dimensions must every journal line carry (for example entity, fund, program, restriction, currency), and how are invalid combinations rejected?",
    "dimensions", "Reporting by fund and program depends on valid dimensions.", "Unattributable postings.",
    [D(U)], "customer-preference", "medium", reqs=["ACC-MDL-001", "UNB-ACC-001"]),
 ]),
dict(
 title="Append-only journals, linked corrections and tamper evidence",
 target=("Posted journals are never updated or deleted. Corrections are new reversal, reclassification or adjustment entries "
         "with explicit linkage to the original, reason, evidence, authorization and both effective and recorded dates "
         "(ACC-MDL-002, UNB-ACC-003, UNB-IMM-002, UNB-IMM-003). Normal operational database roles cannot UPDATE, DELETE or "
         "TRUNCATE authoritative rows, and schema deployment refuses destructive changes to ledger tables, including removal "
         "of append-only triggers or privilege revocations (UNB-IMM-001, RR-UNB-ACC-026-r1). Queries answer both what was true "
         "on an effective date and what was known on a recorded date, so backdated corrections never rewrite an earlier "
         "as-known view (UNB-IMM-004). Missing, reordered, duplicated or altered records are detectable through integrity "
         "checkpoints, with ledger digests anchored externally at least daily (UNB-IMM-007, CNV-PLT-010)."),
 intended="Use PostgreSQL privileges and triggers for append-only enforcement; use Strata only for declarative schema management with destructive-change refusal; anchor digests outside the database.",
 prov_refs="ACC-MDL-002, UNB-ACC-003, UNB-IMM-001..UNB-IMM-004, UNB-IMM-007, RR-UNB-ACC-026-r1, CNV-PLT-010",
 statement="Planned: Unbound's journals are specified as append-only with linked corrections, bitemporal history and externally anchored digests. Not implemented. Strata, Echelon's schema tool, exists in pilot form but does not itself provide these guarantees.",
 controls=["ECTL-ACT-002", "ECTL-ACT-003"], evidence=["EVR-ACT-002", "EVR-ACT-003"], policies=["SOC2-006", "SEC-DB-001"],
 requirements=["ACC-MDL-002", "UNB-ACC-003", "UNB-IMM-001", "UNB-IMM-002", "UNB-IMM-003", "UNB-IMM-004", "UNB-IMM-007", "RR-UNB-ACC-026-r1", "CNV-PLT-010"],
 impl_cost="medium", rec_cost="low",
 residual=["A database superuser can still alter data; detection relies on external digest anchoring and break-glass controls.",
           "Append-only storage conflicts with privacy erasure; UNB-IMM-008 and SOC2-032 require a reviewed approach."],
 challenge=dict(
  customer_intent="Know that historical books cannot be secretly changed.",
  adverse_outcome="Fraud concealed by editing or deleting posted entries; restated history without trace.",
  conventional_control_effectiveness="Application audit logs plus restricted access are common but can be bypassed by privileged users and logs can be altered.",
  legally_required="No statute mandates an append-only ledger for DAF sponsors; record integrity expectations come from auditors and IRS recordkeeping.",
  contractually_required="Sometimes, as an immutability or audit trail clause.",
  historical_convention="Change logs and period locks in ERP systems.",
  architectural_elimination="Within the application and operational roles, in-place edits are eliminated because no such operation or privilege exists.",
  automatic_enforcement="Database privileges and triggers; deployment refuses destructive schema changes.",
  continuous_evidence="Integrity checkpoints and externally anchored daily digests.",
  stronger_alternative="Append-only PostgreSQL with external digest anchoring instead of a separate ledger database or blockchain product.",
  alternative_verifiable="Yes, by independent recomputation of the digest chain against the anchor.",
  customer_acceptance_likelihood="Likely; some customers may ask specifically for a named immutable ledger product.",
  invalidating_conditions="Superuser access without break-glass control; anchors stored where the same administrator can alter them.",
  conventional_cost="Low.", alternative_cost="Low to medium; storage growth and replay cost (UNB-ECO-007).",
  alternative_risks="Privacy erasure obligations; operational cost of correcting through new entries only.",
  supporting_arguments=["Removes the edit path rather than logging it.", "Bitemporal queries preserve originally issued statements."],
  opposing_arguments=["A determined database owner can still rewrite and re-anchor if anchoring is not independent.",
                      "Customers may equate immutability with distributed ledgers despite weaker practical guarantees for this use."],
  technical_effectiveness="stronger", institutional_acceptance="likely"),
 questions=[
  Q("Can posted journal entries be edited or deleted by any user, administrator or vendor employee?",
    "immutability", "Edits to posted history defeat audit.", "Concealment of fraud or error by altering posted entries.",
    [D(U), S(N53, "AU-9"), S(TSC, "PI1.5")], "customer-preference", "critical",
    alts=["Is the general ledger immutable?", "How do you protect the audit trail of financial transactions from modification?"]),
  Q("How are accounting errors corrected, and is the original entry preserved with a link to its correction and the reason and approval for it?",
    "corrections", "Auditors need to see the original and the correction.", "Untraceable corrections.",
    [D(U), S(COSO, "Principle 10")], "industry-convention", "high", reqs=["ACC-MDL-002", "UNB-ACC-003", "UNB-IMM-002", "UNB-IMM-003"]),
  Q("Can you produce the ledger as it was known on a past date, separately from the ledger as later corrected for that date?",
    "bitemporal", "Needed to reproduce previously issued statements and investigate restatements.", "Inability to explain differences from issued reports.",
    [D(U)], "customer-preference", "medium", reqs=["UNB-IMM-004", "ACC-MDL-010"]),
  Q("How would you detect that ledger records were deleted, reordered, duplicated or altered outside the application, for example by a database administrator?",
    "tamper-evidence", "Privileged insiders can bypass application controls.", "Undetected tampering.",
    [D(U), S(N53, "AU-9"), S(N53, "SI-7")], "customer-preference", "high", reqs=["UNB-IMM-007", "CNV-PLT-010", "UNB-SCTRL-040"]),
  Q("How do schema migrations and database deployments protect ledger tables and their append-only protections from being dropped or weakened?",
    "tamper-evidence", "Deployments are a path to silently remove protections.", "Protections removed during a release.",
    [D(U), S("SRC-ECH-SCS-0.1")], "customer-preference", "medium", reqs=["RR-UNB-ACC-026-r1", "ACC-MDL-011"]),
 ]),
dict(
 title="Fund accounting under FASB ASC 958 and DAF account classification",
 target=("Unbound separates financial statement classification from fund advisory designation. Each account type carries one "
         "CPA-approved accounting treatment determined from its transfer-instrument terms, not marketing labels: contribution "
         "without donor restrictions (variance power granted, advisory privileges only), contribution with donor restrictions, "
         "agency or pass-through liability, or equity transaction (CNV-FIN-008, UNB-XIN-ACC-001). Receipts into liability-treated "
         "accounts never increase contribution revenue or Schedule D DAF aggregates. A DAF subfund designation does not by itself "
         "imply donor-restricted net assets (ACC-MDL-008, UNB-ACC-033). Cash and assets held, fund net asset balances, grant "
         "commitments, restricted net assets and available-to-recommend amounts are distinct; available-to-recommend is a "
         "controlled projection, not a GL account (ACC-MDL-004). Pledges, conditional gifts and contingent commitments are "
         "modeled separately from settled assets (UNB-ACC-032). An account type without an approved treatment cannot accept receipts."),
 intended="Ship an account-type register whose treatment field is approved by the sponsor's CPA before activation; the posting policy derives revenue versus liability from it.",
 prov_refs="CNV-FIN-008, UNB-XIN-ACC-001, ACC-MDL-004, ACC-MDL-008, UNB-ACC-005, UNB-ACC-033, UNB-ACC-032",
 statement="Planned: Unbound's accounting model is specified around ASC 958 classifications with CPA-approved treatment per account type. Accounting policy decisions remain the sponsor's and its auditor's. Not implemented.",
 controls=["ECTL-ACT-006"], evidence=["EVR-ACT-006"], policies=["SOC2-018"],
 requirements=["CNV-FIN-008", "UNB-XIN-ACC-001", "ACC-MDL-004", "ACC-MDL-008", "UNB-ACC-005", "UNB-ACC-033", "UNB-ACC-032", "UNB-ACC-006"],
 impl_cost="medium", rec_cost="low",
 residual=["Classification correctness depends on the sponsor's CPA judgment; the platform enforces only that a judgment is recorded."],
 open_questions=["Has any CPA reviewed the default treatments proposed in CNV-FIN-008?"],
 questions=[
  Q("Does the system support nonprofit fund accounting under FASB ASC 958, including net assets with and without donor restrictions?",
    "asc-958", "Sponsors report under US GAAP for nonprofits.", "Misclassified net assets and audit adjustments.",
    [D(ASC), D(U)], "industry-convention", "critical",
    alts=["How does the platform support GAAP reporting for not-for-profit entities?"]),
  Q("How do you determine whether amounts received into a donor-advised fund are contribution revenue or a liability (agency or pass-through)?",
    "asc-958", "Agency transactions are not contributions.", "Overstated revenue and misreported DAF aggregates.",
    [D(ASC, "958-605"), D(U)], "industry-convention", "high", reqs=["CNV-FIN-008", "UNB-XIN-ACC-001"]),
  Q("Does the platform treat donor-advised fund balances as donor-restricted net assets by default, and who decides the classification?",
    "asc-958", "A common misconception that affects statements.", "Systematic misclassification.",
    [D(ASC, "958-205"), D(U)], "industry-convention", "high", reqs=["ACC-MDL-008", "UNB-ACC-033", "CNV-FIN-008"]),
  Q("How are pledges, conditional contributions and grant commitments distinguished from cash and settled assets in the books and in amounts available for grants?",
    "asc-958", "Conditional items should not inflate available balances.", "Grants made against unrealized assets.",
    [D(ASC, "958-605"), D(U)], "industry-convention", "high", reqs=["UNB-ACC-032", "ACC-MDL-004", "UNB-RCN-GRT-009"]),
  Q("How is the amount a donor sees as available to recommend derived, and can it differ from the fund's general ledger balance?",
    "available-balance", "Donor-facing balances must be explainable.", "Donor confusion or grants exceeding true capacity.",
    [D(U)], "customer-preference", "medium", reqs=["ACC-MDL-004", "CNV-FIN-012", "RR-UNB-GFUND-021-r1"]),
 ]),
dict(
 title="Grant expense recognition and period-end cutoff",
 target=("Each sponsor book declares an effective-dated grant recognition point: approval communicated to the grantee (default), "
         "sponsor approval (only under a documented sponsor policy that approval creates the obligation with no free rescission "
         "right) or payment released (only where payment is the first communication) (CNV-FIN-007, which supersedes the narrower "
         "rule in UNB-XIN-ACC-002). Approval, communication, condition and rescission evidence is always captured; a recommendation "
         "alone never creates a payable (UNB-SCTRL-026). Conditional grants carry no expense until a recorded barrier-met or "
         "waiver event. At each period end a cutoff register lists approved-but-uncommunicated, communicated-but-unpaid and "
         "conditional grants with their recognition status."),
 intended="Generate the cutoff register automatically from grant lifecycle facts; recognition rule versions are CPA-approved.",
 prov_refs="CNV-FIN-007, UNB-XIN-ACC-002, UNB-ACC-007",
 statement="Planned: grant expense recognition is specified as a sponsor-declared, CPA-approved policy with an automatic period-end cutoff register. Not implemented.",
 controls=["ECTL-ACT-006", "ECTL-ACT-004"], evidence=["EVR-ACT-012"],
 requirements=["CNV-FIN-007", "UNB-XIN-ACC-002", "UNB-ACC-007", "UNB-SCTRL-026"],
 impl_cost="low", rec_cost="low",
 questions=[
  Q("When does the system recognize grant expense and grants payable, and can each sponsor configure that recognition point?",
    "grant-recognition", "Recognition timing affects expense and liabilities.", "Misstated grants payable at period end.",
    [D(ASC), D(U)], "industry-convention", "high"),
  Q("How do you produce a period-end cutoff listing of grants approved, communicated, unpaid and conditional?",
    "cutoff", "Auditors test cutoff of grants payable.", "Cutoff errors.", [D(U), S(TSC, "PI1.4")], "industry-convention", "high"),
  Q("Can a donor's grant recommendation ever create a liability or payment without sponsor approval?",
    "grant-recognition", "Sponsor holds legal control of DAF assets.", "Liabilities recorded from donor wishes.",
    [D(U), D("SRC-IRC-4966")], "legal-regulatory", "critical", reqs=["UNB-ACC-007", "UNB-SCTRL-026", "UNB-PAY-003"],
    authority="IRS (sponsor's legal control over DAF assets)"),
 ]),
dict(
 title="Period close, period locks and late-arriving events",
 target=("Accounting periods have soft and hard close states, close checklists and reopen approvals (UNB-ACC-017). Every posting "
         "reads the period row with a shared lock (or runs serializable) and a hard close takes an exclusive lock, so a posting "
         "cannot slip into a period while it closes; a posting dated in a hard-closed period is rejected with PERIOD_CLOSED and "
         "recorded instead as a prior-period adjustment in the first open period carrying the original relates-to period and "
         "effective date, with controller approval above a sponsor threshold (UNB-XIN-EVA-002). A hard-closed period may be "
         "reopened only before its statements are issued and only with controller and CFO approval. Closed periods remain "
         "immutable and originally issued statements are preserved (ACC-MDL-010). Unbalanced or unexplained control-account "
         "breaks block unsupported close certification (ACC-MDL-009), and the preparer cannot certify their own close (UNB-SCTRL-027)."),
 intended="Implement period state as a locked row with transactional checks; close certification is a separate command subject to SoD.",
 prov_refs="UNB-ACC-017, UNB-XIN-EVA-002, ACC-MDL-009, ACC-MDL-010, CNV-FIN-011",
 statement="Planned: period locks are specified to be enforced inside each posting transaction, with late items routed to approved prior-period adjustments. Not implemented.",
 controls=["ECTL-ACT-004", "ECTL-FCT-001"], evidence=["EVR-ACT-004", "EVR-FCT-001"], policies=["SOC2-018"],
 requirements=["UNB-ACC-017", "UNB-XIN-EVA-002", "ACC-MDL-009", "ACC-MDL-010", "CNV-FIN-011", "UNB-SCTRL-027", "UNB-SCTRL-028", "UNB-ACC-034"],
 impl_cost="medium", rec_cost="medium",
 questions=[
  Q("How do you prevent transactions from being posted into a closed accounting period?",
    "period-close", "Closed periods must stay closed.", "Changes to reported results after close.",
    [D(U), S(COSO, "Principle 10"), S(TSC, "PI1.3")], "industry-convention", "critical",
    alts=["Describe period locking controls."]),
  Q("Who can reopen a closed period, under what conditions, and how is the reopening evidenced?",
    "period-close", "Reopening is an override that auditors scrutinize.", "Unauthorized restatement of closed results.",
    [D(U), S(COSO, "Principle 10")], "industry-convention", "high"),
  Q("How are transactions that arrive after a period closes but relate to it (for example a late custodian statement) recorded?",
    "late-items", "Late items are inevitable with external feeds.", "Late items lost, misdated or forced into closed periods.",
    [D(U)], "customer-preference", "high", reqs=["UNB-XIN-EVA-002", "CNV-FIN-011", "UNB-ACC-017"]),
  Q("What must be reconciled and resolved before a period can be certified as closed, and can unresolved breaks be overridden?",
    "close-certification", "Close should not hide unreconciled differences.", "Certification of books with unexplained breaks.",
    [D(U), S(COSO, "Principle 10")], "industry-convention", "high", reqs=["ACC-MDL-009", "UNB-SCTRL-028", "RR-UNB-ACC-018-r1"]),
  Q("Is there a race condition between period close and in-flight postings, and how is it prevented?",
    "period-close", "Concurrency at close is a subtle source of error.", "Entries posted into a period after its close was certified.",
    [D(U), S("SRC-MITRE-CWE", "CWE-362")], "customer-preference", "medium", reqs=["UNB-XIN-EVA-002"]),
 ]),
dict(
 title="Audit adjustments, prior-period adjustments and accounting changes",
 target=("Each fiscal year has an AuditAdjustment period after period 12 that accepts only journals linked to an auditor finding "
         "(auditor reference, proposer, controller decision); every proposed adjustment is recorded as Booked or Passed with amount "
         "and rationale, and Passed items feed a summary of unadjusted differences (UNB-XIN-ACC-005, CNV-FIN-011). Audited "
         "statements are generated from period 12 plus audit-adjustment journals. Every posting-rule change and every correction "
         "of a posted error carries an AccountingChangeRecord classified by an authorized controller as change in principle, "
         "change in estimate or error correction, with materiality assessment and CPA approval reference; changes in principle "
         "recast comparatives as separately versioned as-adjusted reports while preserving as-originally-issued reports "
         "(UNB-XIN-ACC-004). After issuance, late items post as immaterial current-period corrections with disclosure or as "
         "material restatements, judged against the sponsor's materiality setting agreed with its auditor (UNB-XIN-EVA-002)."),
 intended="Model audit findings and accounting changes as first-class records that gate the journals they authorize.",
 prov_refs="UNB-XIN-ACC-004, UNB-XIN-ACC-005, UNB-XIN-EVA-002, CNV-FIN-011",
 statement="Planned: audit adjustments are specified to post only into a dedicated audit-adjustment period linked to auditor findings, with a summary of unadjusted differences. Not implemented.",
 controls=["ECTL-ACT-005", "ECTL-ACT-007"], evidence=["EVR-ACT-005", "EVR-ACT-007"],
 requirements=["UNB-XIN-ACC-004", "UNB-XIN-ACC-005", "UNB-XIN-EVA-002", "CNV-FIN-011", "UNB-XIN-ACC-003"],
 impl_cost="medium", rec_cost="low",
 questions=[
  Q("How are year-end audit adjustments proposed by our external auditor recorded, and are passed adjustments tracked?",
    "audit-adjustments", "Auditor needs a clean record of booked and passed adjustments.", "Untracked or misapplied audit adjustments.",
    [D(U), S(SOC1)], "industry-convention", "high", alts=["Do you support a 13th period for audit adjustments?"]),
  Q("When a posting rule or accounting policy changes, how is the effect on prior periods handled and documented?",
    "accounting-changes", "Policy changes can silently rewrite history.", "Unapproved retrospective changes.",
    [D(U)], "industry-convention", "high", reqs=["UNB-XIN-ACC-004", "RR-ACC-MDL-007-r1"]),
  Q("How are material errors in previously issued statements corrected while preserving the statements as originally issued?",
    "restatement", "Restatements must be transparent.", "Loss of the originally issued record.",
    [D(U)], "industry-convention", "medium", reqs=["UNB-XIN-ACC-004", "UNB-XIN-EVA-002", "ACC-MDL-010"]),
  Q("How do you verify that posted journals still match what the approved posting rules would have produced from the source events?",
    "rule-integrity", "Detects posting logic defects or tampering.", "Systematic posting errors persist undetected.",
    [D(U), S(TSC, "PI1.3")], "customer-preference", "medium", reqs=["UNB-XIN-ACC-003"]),
 ]),
dict(
 title="Multi-entity and multi-sponsor ledgers, isolation and book of record",
 target=("Unbound runs one double-entry journal component serving distinct entity books with separate permissions (CNV-FIN-012). "
         "Each sponsor tenant has its own schema and database role with row-level security on every tenant table and negative "
         "isolation tests, and can move to a dedicated database when risk or contract requires (CNV-ARC-001, UNB-ACC-027). "
         "Cross-tenant authorization is enforced for append, projection, replay, export and correction (UNB-IMM-009). Multiple "
         "legal entities, intercompany and interfund transactions and eliminations are supported where authorized (UNB-ACC-015). "
         "For each entity and function the sponsor designates Unbound as Authoritative, Shadow or NotUsed; in Shadow mode Unbound "
         "never posts to that function and reconciles daily to the external book, and changing designation requires a cutover "
         "record with opening-balance tie-out (UNB-XIN-ACC-010). Transfers between sponsors post as independent entries in each "
         "sponsor's books (UNB-XIN-EVA-009)."),
 intended="Implement per-tenant schema and role isolation with a negative test suite run on every release.",
 prov_refs="CNV-FIN-012, CNV-ARC-001, UNB-ACC-015, UNB-ACC-027, UNB-IMM-009, UNB-XIN-ACC-010, UNB-XIN-EVA-009",
 statement="Planned: each sponsor's ledger is specified to be isolated by schema, database role and row-level security, with optional dedicated databases. Not implemented or tested.",
 controls=["ECTL-ACT-008"], evidence=["EVR-ACT-008"], policies=["SEC-AUTH-001", "SOC2-014"],
 requirements=["CNV-FIN-012", "CNV-ARC-001", "UNB-ACC-015", "UNB-ACC-027", "UNB-IMM-009", "UNB-XIN-ACC-010", "UNB-XIN-EVA-009", "ACC-MDL-005"],
 impl_cost="high", rec_cost="medium",
 questions=[
  Q("Does the ledger support multiple legal entities with intercompany or interfund transactions and eliminations for consolidated reporting?",
    "multi-entity", "Sponsors often have affiliated entities.", "Double counting in consolidated statements.",
    [D(U)], "customer-preference", "medium", reqs=["UNB-ACC-015", "UNB-RCN-FIN-006"]),
  Q("How are different sponsors' ledgers segregated so that one customer's postings, balances or reports can never include another customer's data?",
    "multi-sponsor", "Multi-tenant ledgers risk commingling.", "Cross-customer data exposure or misposting.",
    [D(U), S("SRC-ECH-SCS-0.1"), S("SRC-CSA-CCM-V4")], "customer-preference", "critical", reqs=["CNV-ARC-001", "UNB-ACC-027", "UNB-IMM-009", "ACC-MDL-005"]),
  Q("If our existing ERP remains our general ledger of record, how does your platform avoid creating a competing authoritative book?",
    "book-of-record", "Two authoritative books create reconciliation and audit problems.", "Conflicting balances and unclear system of record.",
    [D(U)], "customer-preference", "high", reqs=["UNB-XIN-ACC-010", "CNV-FIN-012"]),
  Q("When funds transfer between sponsors, such as a fund moving to another sponsoring organization, how is each side's ledger kept complete and independent?",
    "multi-sponsor", "Sponsor-to-sponsor transfers must be auditable on both sides.", "Lost history or unbalanced transfer accounting.",
    [D(U)], "customer-preference", "medium", reqs=["UNB-XIN-EVA-009", "UNB-RCN-FIN-013"]),
 ]),
dict(
 title="Audit support, reproducible statements and DAF regulatory bridges",
 target=("Unbound supports audit schedules, roll-forwards, workpapers, transaction drill-down from statement line to source "
         "event and evidence, external auditor access and independently verifiable as-of snapshots (UNB-ACC-020). Every report "
         "figure is computed from a sealed snapshot identified by entity, period and ledger commit watermark, so the same report "
         "recomputed later is identical (UNB-XIN-EVA-003). For each sponsor and tax year a DAF bridge reconciles Form 990 "
         "Schedule D Part I values, the sum of fund statements and the DAF component of audited net assets using only typed "
         "reconciling items; any unexplained residual blocks sign-off (UNB-XIN-ACC-006, CNV-FIN-009). Folio renders versioned "
         "statements and audit packages with source, policy and template provenance (UNB-ACC-025)."),
 intended="Provide an auditor portal and generated audit package per period built from sealed snapshots.",
 prov_refs="UNB-ACC-020, UNB-ACC-025, UNB-XIN-EVA-003, UNB-XIN-ACC-006, CNV-FIN-009",
 statement="Planned: audit support is specified around drill-down to source evidence, reproducible sealed snapshots and a Schedule D bridge. Not implemented. Folio, Echelon's report rendering system, exists but is not operated for Unbound.",
 controls=["ECTL-ACT-010", "ECTL-FCT-006"], evidence=["EVR-ACT-010", "EVR-FCT-006"], policies=["SOC2-009"],
 requirements=["UNB-ACC-020", "UNB-ACC-025", "UNB-XIN-EVA-003", "UNB-XIN-ACC-006", "CNV-FIN-009", "UNB-XIN-NPG-004"],
 freshness="P1Y", mechanism="periodic-automated", impl_cost="medium", rec_cost="low",
 questions=[
  Q("What support do you provide to our external auditors, such as read-only access, standard audit schedules and transaction drill-down?",
    "audit-support", "Audit efficiency and cost.", "Prolonged audits and higher fees.",
    [D(U), S(SOC1)], "customer-preference", "high", alts=["Can auditors access the system directly?"]),
  Q("Can you trace any figure on a fund statement or financial statement back to the individual source transactions and supporting evidence?",
    "traceability", "Auditors vouch figures to source.", "Unsupported balances.", [D(U), S(TSC, "PI1.4")], "industry-convention", "high",
    reqs=["UNB-ACC-020", "UNB-XIN-EVA-006"]),
  Q("How do you reconcile Form 990 Schedule D donor-advised fund figures to the audited financial statements and individual fund statements?",
    "regulatory-bridge", "IRS reporting must agree with audited figures.", "Inconsistent regulatory reporting.",
    [D("SRC-IRS-FORM-990"), D(U)], "legal-regulatory", "high", reqs=["UNB-XIN-ACC-006", "CNV-FIN-009"], authority="IRS"),
  Q("If a report is reissued months later, how do you prove it is identical to the version previously delivered to donors or auditors?",
    "reproducibility", "Issued statements must be defensible.", "Unexplained differences between versions.",
    [D(U)], "customer-preference", "medium", reqs=["UNB-XIN-EVA-003", "UNB-ACC-025", "UNB-IMM-004"]),
 ]),
dict(
 title="Chart of accounts mapping and general ledger export to sponsor ERP",
 target=("Unbound provides a configurable, versioned chart of accounts with entity, sponsor, program, fund, restriction, currency "
         "and other approved dimensions and enforces dimension validity (UNB-ACC-001). By default the sponsor's ERP remains the "
         "book of record for entity financial statements, accounts payable, payroll and fixed assets; Unbound exports balanced, "
         "summarized, dimension-complete journals for DAF program activity to that ERP and reconciles the receiving control "
         "accounts (RR-UNB-ACC-012-r1, CNV-FIN-012). Exports carry control totals, the source snapshot identifier and the mapping "
         "version; imports from ERP, bank and custodian feeds are reconciliation sources and never silently replace Unbound's "
         "authoritative books (UNB-ACC-028)."),
 intended="Publish a versioned account mapping per sponsor and an export manifest with control totals; reconcile ERP control accounts daily or per sponsor frequency.",
 prov_refs="UNB-ACC-001, RR-UNB-ACC-012-r1, CNV-FIN-012, UNB-ACC-028, ACC-MDL-001",
 statement="Planned: Unbound is specified to export balanced, dimension-complete journals to the sponsor's ERP under a versioned account mapping and to reconcile the receiving accounts. Not implemented; no ERP connector exists.",
 controls=["ECTL-ACT-009"], evidence=["EVR-ACT-009"],
 requirements=["UNB-ACC-001", "RR-UNB-ACC-012-r1", "CNV-FIN-012", "UNB-ACC-028", "ACC-MDL-001", "UNB-XIN-ERP-003"],
 impl_cost="medium", rec_cost="low",
 challenge=dict(
  customer_intent="Get complete, accurate DAF activity into the sponsor's general ledger without rekeying.",
  adverse_outcome="Incomplete or mismapped exports misstate the sponsor's statements.",
  conventional_control_effectiveness="Spreadsheet exports with manual journal upload are error-prone and weakly evidenced.",
  legally_required="No.", contractually_required="Often expected in procurement as 'GL integration'.",
  historical_convention="Vendors either replace the GL entirely or export flat files.",
  architectural_elimination="Not building a second full ERP removes a whole class of duplicate-book reconciliation problems (CNV-FIN-012).",
  automatic_enforcement="Exports are balanced by construction and carry control totals and mapping versions.",
  continuous_evidence="Export manifests and receiving control-account reconciliation.",
  stronger_alternative="Integration-first design with summarized balanced exports and reconciliation, instead of a full native ERP.",
  alternative_verifiable="Yes, by control totals and reconciliation evidence.",
  customer_acceptance_likelihood="Likely for sponsors with an ERP; less likely for small sponsors wanting one system.",
  invalidating_conditions="Sponsors without an ERP or without staff to reconcile.",
  conventional_cost="Very high to build and maintain native AP, payroll and fixed asset modules.", alternative_cost="Medium.",
  alternative_risks="Dependence on each ERP's import capability; mapping drift.",
  supporting_arguments=["Avoids duplicate authoritative books.", "Keeps scope on DAF-specific accounting."],
  opposing_arguments=["Some customers will score a 'full accounting suite' higher in procurement.", "Small sponsors may lack an ERP."],
  technical_effectiveness="stronger", institutional_acceptance="likely"),
 questions=[
  Q("Can the platform map its accounts to our chart of accounts and export journal entries to our general ledger system?",
    "gl-export", "Avoid rekeying and errors.", "Mismapped or incomplete GL entries.", [D(U)], "customer-preference", "high",
    alts=["Which ERP or accounting systems do you integrate with?"],
    oq=["No ERP connector or export format has been selected or built."]),
  Q("How do you ensure that a GL export is complete and that every exported entry is received and posted in our system?",
    "gl-export", "Interfaces are a common source of completeness errors.", "Dropped or duplicated interface entries.",
    [D(U), S(TSC, "PI1.4")], "industry-convention", "high", reqs=["RR-UNB-ACC-012-r1", "UNB-ACC-028"]),
  Q("How are changes to the account mapping controlled and versioned, and can historical exports be reproduced under the mapping in effect at the time?",
    "coa-mapping", "Mapping changes alter reported figures.", "Silent reclassification through mapping edits.",
    [D(U), S(TSC, "CC8.1")], "customer-preference", "medium", reqs=["UNB-ACC-001", "UNB-LEG-005"]),
  Q("Does your platform replace our general ledger, or is it designed to feed it, and which accounting functions are out of scope?",
    "scope", "Scope clarity prevents gaps between systems.", "Functions nobody owns.", [D(U)], "customer-preference", "medium",
    reqs=["CNV-FIN-012", "RR-UNB-ACC-012-r1", "RR-UNB-ACC-022-r2"]),
 ]),
]

controls = [
 C("Balanced journal enforcement at posting boundary", "Reject any journal not balanced per entity, currency and declared balancing segment, both in the typed posting command and by database constraint.",
   "preventive-structural", "L3-restricted-interface", ["Unbound ledger component (specified, not built)", "PostgreSQL constraints (planned)"], ["EVR-ACT-001"],
   related=["UNB-SCTRL-025", "UNB-CTRL-043"], cwe=["CWE-840"], refs=[S("SRC-AICPA-TSC", "PI1.3")]),
 C("Append-only ledger privileges and destructive-change refusal", "Operational roles hold INSERT-only rights on authoritative tables; triggers reject UPDATE, DELETE and TRUNCATE; deployment refuses destructive ledger schema changes.",
   "preventive-structural", "L3-restricted-interface", ["PostgreSQL role privileges and triggers (planned)", "Strata (exists in pilot; destructive-change refusal for ledger tables not verified)"], ["EVR-ACT-002"],
   related=["UNB-SCTRL-022", "UNB-CTRL-044"], policies=["SEC-DB-001", "SOC2-006"], refs=[S("SRC-NIST-SP800-53-R5", "AU-9")],
   residual=["Superuser or break-glass misuse"], notes="RR-UNB-ACC-026-r1 forbids claiming these guarantees come from Strata."),
 C("Ledger integrity checkpoints with external digest anchoring", "Compute hash-chained checkpoints over the journal and anchor digests outside the database at least daily; verify independently and on restore.",
   "detective-automated", "L9-runtime-monitored", ["Unbound ledger component (specified, not built)"], ["EVR-ACT-003"],
   related=["UNB-SCTRL-040", "UNB-CTRL-074"], refs=[S("SRC-NIST-SP800-53-R5", "SI-7")]),
 C("Transactional period lock", "Postings take a shared lock on the period row; hard close takes an exclusive lock; postings into hard-closed periods are rejected and routed to prior-period adjustment.",
   "preventive-structural", "L3-restricted-interface", ["Unbound ledger component (specified, not built)", "PostgreSQL"], ["EVR-ACT-004"],
   related=["UNB-CTRL-046"], cwe=["CWE-362"]),
 C("Audit-adjustment period gate", "The AuditAdjustment period accepts only journals linked to an AuditFinding with controller decision; booked and passed items are recorded.",
   "preventive-gate", "L3-restricted-interface", ["Unbound ledger component (specified, not built)"], ["EVR-ACT-005"], related=["UNB-CTRL-045"]),
 C("CPA-approved account treatment and recognition policy register", "Account types and grant recognition points cannot accept receipts or recognize expense without an approved, effective-dated accounting treatment.",
   "preventive-gate", "L3-restricted-interface", ["Unbound ledger component (specified, not built)"], ["EVR-ACT-006", "EVR-ACT-012"],
   related=["UNB-SCTRL-026", "UNB-CTRL-043"], refs=[S("SRC-FASB-ASC-958")], residual=["Wrong CPA judgment is not detected by the platform"]),
 C("Posting re-derivation comparison", "Recompute expected journals from source events under each journal's recorded rule version and raise exceptions for differences without modifying the ledger.",
   "detective-automated", "L6-automated-analysis", ["Unbound ledger component (specified, not built)"], ["EVR-ACT-007"], refs=[S("SRC-AICPA-TSC", "PI1.3")]),
 C("Per-sponsor schema, role and row-level security isolation", "Each sponsor's ledger lives in its own schema with its own database role and row-level security; negative cross-tenant tests run on each release.",
   "preventive-structural", "L3-restricted-interface", ["PostgreSQL (planned)", "Unbound tenant connection broker (specified, not built)"], ["EVR-ACT-008"],
   related=["UNB-SCTRL-006", "UNB-CTRL-007", "UNB-CTRL-008"], policies=["SEC-AUTH-001"], cwe=["CWE-639"]),
 C("GL export manifest and receiving-account reconciliation", "Every export carries control totals, snapshot identifier and mapping version; the receiving ERP control accounts are reconciled to the export.",
   "detective-automated", "L6-automated-analysis", ["Unbound integration component (specified, not built)"], ["EVR-ACT-009"], refs=[S("SRC-AICPA-TSC", "PI1.4")]),
 C("DAF regulatory bridge with typed reconciling items", "Block sign-off of the annual package when Schedule D, fund statements and audited net assets do not reconcile through typed items.",
   "preventive-gate", "L6-automated-analysis", ["Unbound reporting component (specified, not built)"], ["EVR-ACT-010"],
   related=["UNB-SCTRL-033", "UNB-CTRL-058"], refs=[S("SRC-IRS-FORM-990")]),
 C("Ledger invariant property-based test suite", "Generated journals, corrections, replays and concurrent postings must preserve balance, uniqueness and immutability invariants before release.",
   "preventive-gate", "L7-property-tested", ["Unbound test suite (specified, not built)", "Praxis CI gates (exists; not operated for Unbound)"], ["EVR-ACT-011"],
   policies=["SEC-LANG-002"], refs=[S("SRC-ECH-SCS-0.1")]),
]

evidence = [
 E("Journal posting validation outcomes", "Accepted and rejected posting attempts with balancing results per segment.", NOT_ASSIGNED.format("Unbound ledger component"), "event-driven-automated", "per-event"),
 E("Append-only privilege and trigger configuration attestation", "Generated listing of database privileges and triggers on authoritative tables compared to the approved baseline, plus deployment refusal logs.", NOT_ASSIGNED.format("Unbound ledger component and deployment pipeline"), "periodic-automated", "P1D"),
 E("Integrity checkpoint verification results", "Digest chain verification results and external anchor receipts.", NOT_ASSIGNED.format("Unbound ledger component"), "periodic-automated", "P1D"),
 E("Period state and close certification records", "Period transitions, lock holders, reopen approvals, PERIOD_CLOSED rejections and close certifications with preparer and approver.", NOT_ASSIGNED.format("Unbound ledger component"), "event-driven-automated", "per-event"),
 E("Audit adjustment register and summary of unadjusted differences", "AuditFinding-linked journals with booked or passed status and rationale.", NOT_ASSIGNED.format("Unbound ledger component"), "event-driven-automated", "per-event", disclosure="auditor-only"),
 E("Account treatment approvals", "Account-type register versions with CPA approval references and effective dates.", NOT_ASSIGNED.format("Unbound ledger component"), "event-driven-automated", "per-event"),
 E("Re-derivation exception report", "Differences between posted journals and recomputed expected journals.", NOT_ASSIGNED.format("Unbound ledger component"), "periodic-automated", "P1M"),
 E("Tenant isolation negative test results", "Results of cross-tenant append, query, replay, export and correction attempts per release.", NOT_ASSIGNED.format("Unbound test suite"), "event-driven-automated", "per-event"),
 E("GL export manifests and ERP reconciliation", "Export manifests with control totals and the reconciliation of receiving control accounts.", NOT_ASSIGNED.format("Unbound integration component"), "event-driven-automated", "per-event"),
 E("Annual DAF bridge package", "Schedule D Part I, fund statement totals and audited net asset reconciliation with typed reconciling items.", NOT_ASSIGNED.format("Unbound reporting component"), "periodic-automated", "P1Y", fmt="Folio-rendered report with machine-readable data"),
 E("Ledger property-based test reports", "Test runs with seeds, generators, invariants checked and failures, tied to release commit.", NOT_ASSIGNED.format("Unbound test suite with Praxis provenance"), "event-driven-automated", "per-event", disclosure="nda"),
 E("Grant cutoff register", "Per period list of approved-uncommunicated, communicated-unpaid and conditional grants with recognition status.", NOT_ASSIGNED.format("Unbound grants and ledger components"), "periodic-automated", "P1M"),
]
