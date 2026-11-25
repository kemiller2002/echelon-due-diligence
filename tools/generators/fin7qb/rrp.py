from finlib import *

F990 = S("SRC-IRS-FORM-990", "Schedule D Part I", "maps-to", "directly-documented")
P1771 = S("SRC-IRS-PUB-1771")
OFAC603 = S("SRC-OFAC-REGS", "31 CFR 501.603", "maps-to", "directly-documented")
OFAC604 = S("SRC-OFAC-REGS", "31 CFR 501.604", "maps-to", "directly-documented")
UP = S("SRC-STATE-UNCLAIMED-PROPERTY")
SOL = S("SRC-STATE-CHARITABLE-SOLICITATION")
SOC1 = S("SRC-AICPA-SSAE-18", "AT-C 320")
ASC = S("SRC-FASB-ASC-958")
IND = ["donor-advised-funds", "nonprofit"]

units = [
AU("Form 990 Schedule D and annual DAF reporting data package",
   target=("For each legal sponsor and tax year, Unbound produces a reproducible DAF annual "
           "reporting data package from the locked ledger: count of donor-advised funds at "
           "year end, aggregate contributions, grants and year-end value (each defined in a "
           "CPA-approved, form-year-versioned data dictionary mapped to current form lines), "
           "the transfer-out subset, and evidence for the donor written-disclosure "
           "questions. Which account types count as DAFs comes from a counsel-approved "
           "classification register. A DAF bridge reconciles Schedule D Part I line 4 to the "
           "sum of year-end fund statements and the DAF component of audited net assets, and "
           "lines 2 and 3 to the statement of activities, using only typed reconciling items; "
           "any unexplained residual blocks sign-off. Grants carry Schedule I and F attributes "
           "at approval and recipient aggregates reconcile to total grants with zero "
           "unexplained difference. Estimated UBIT accrues with Form 990-T installment "
           "support. Preparation, review, signature, filing and acceptance are distinct "
           "states; amended packages repeat them; AI has no signing or filing authority."),
   stmt=("Planned: a reproducible Schedule D data package and reconciliation to audited "
         "statements are specified. Unbound does not file returns; the sponsor and its "
         "preparer remain responsible for filing. Nothing has been produced yet."),
   reqs=["CNV-FIN-009", "RR-REQ-X-060-r1", "UNB-RCN-ENT-011", "UNB-RCN-ENT-012",
         "UNB-XIN-ACC-006", "UNB-XIN-NPG-004", "CNV-FIN-010", "UNB-ACC-021", "UNB-GAP-024",
         "UNB-RCN-WF-006", "UNB-RCN-WF-007"],
   oqs=["No CPA-approved data dictionary exists yet; Schedule I and F instructions and Form "
        "990-T sources are not seeded."],
   mech="periodic-automated", fresh="P1Y", impl="medium",
   owner="Unassigned (proposed: sponsor Tax Lead with CPA preparer)",
   challenge={
       "customer_intent": "Schedule D and related schedules are accurate and agree with audited financial statements.",
       "adverse_outcome": "Inaccurate public filings, IRS inquiries, reputational harm.",
       "conventional_control_effectiveness": "Year-end spreadsheet compilation by staff and preparer review; reconciliation to audit often informal.",
       "legally_required": "The sponsor must file Form 990 with Schedule D Part I; the vendor has no filing duty.",
       "contractually_required": "Sponsors expect vendors to supply the data.",
       "historical_convention": "Manual extracts and preparer workpapers.",
       "architectural_elimination": "Mechanical compilation error is largely removed by producing figures from the locked ledger with a versioned dictionary.",
       "automatic_enforcement": "Unexplained residual in the DAF bridge blocks sign-off.",
       "continuous_evidence": "Package carries as-of and known-at snapshot and reproducible query definitions.",
       "stronger_alternative": "Ledger-derived package with typed reconciling items to audited statements.",
       "alternative_verifiable": "Yes; preparer and auditor can re-run.",
       "customer_acceptance_likelihood": "Likely.",
       "invalidating_conditions": "DAF classification register wrong; dictionary not updated for form-year changes.",
       "conventional_cost": "Staff and preparer time each year.",
       "alternative_cost": "Build cost; annual dictionary maintenance by CPA.",
       "alternative_risks": "Misclassification propagates consistently.",
       "supporting_arguments": ["Ties public reporting to the same books the auditor tests."],
       "opposing_arguments": ["Form line definitions are judgment-laden; automation does not remove the need for CPA review."],
       "technical_effectiveness": "stronger", "institutional_acceptance": "likely"},
   ctls=[C("DAF bridge reconciliation gate",
           "Reconcile Schedule D figures to fund statements and audited net assets with typed reconciling items; block sign-off on unexplained residual.",
           "preventive-gate", "L3-restricted-interface", related=["UNB-SCTRL-033", "UNB-CTRL-060"],
           frefs=[UB("UNB-XIN-ACC-006"), F990]),
       C("Distinct prepare, review, sign and file states",
         "Require different principals for preparation, review and signature; deny AI signing or filing authority.",
         "preventive-structural", "L2-type-system", related=["UNB-CTRL-058"], policies=["SEC-AUTH-001"],
         frefs=[UB("RR-REQ-X-060-r1")])],
   evrs=[E("DAF annual reporting data package", "Package with data dictionary version, as-of and known-at snapshot, figures, bridge, reconciling items and state history.",
           "periodic-automated", "P1Y", prov=["tax_year", "dictionary_version", "snapshot_id", "query_hash"], disc="customer-only")],
   qs=[
    Q("Schedule D data", "Can your platform produce the Form 990 Schedule D Part I figures for donor-advised funds (count, contributions, grants, year-end value)?",
      "Accurate annual information return.", "Incorrect public filing.",
      [F990, UB("CNV-FIN-009")], "legal-regulatory", "critical", auth="IRS",
      alts=["What year-end reports do you provide for Form 990 preparation?"], ind=IND),
    Q("Reconciliation to audit", "How do Schedule D figures reconcile to our audited financial statements and to the sum of donor fund statements?",
      "Consistency of filings and audit.", "Contradictory public figures.",
      [UB("UNB-XIN-ACC-006"), ASC], "industry-convention", "high"),
    Q("DAF classification", "How does the platform determine which accounts count as donor-advised funds for reporting, and who approves that classification?",
      "Correct reporting population.", "Misreporting of designated or agency funds as DAFs or vice versa.",
      [UB("UNB-RCN-ENT-011"), S("SRC-PPA-2006"), S("SRC-IRS-DAF-PROPOSED-REGS-2023")], "legal-regulatory", "high", auth="IRS"),
    Q("Amended returns", "If figures change after filing, can you produce an amended package with the same review controls and a record of what changed?",
      "Controlled amendments.", "Uncontrolled or undocumented amendments.",
      [UB("UNB-RCN-WF-007")], "industry-convention", "medium"),
    Q("Grant schedules", "Can you produce grant data needed for Form 990 Schedules I and F, including foreign grant regions and disbursement methods?",
      "Complete grant reporting.", "Missing or wrong grant schedule data.",
      [UB("UNB-XIN-NPG-004"), S("SRC-IRS-FORM-990")], "legal-regulatory", "high", auth="IRS",
      oq=["Schedules I and F instructions not seeded."]),
    Q("UBIT support", "Does the platform track unrelated business taxable income from contributed or held assets and support Form 990-T estimates?",
      "Correct UBIT reporting and allocation.", "Unreported UBIT and penalties.",
      [UB("CNV-FIN-010"), UB("UNB-XIN-ACC-008")], "legal-regulatory", "medium", auth="IRS",
      oq=["Form 990-T source not seeded."]),
   ]),

AU("Contribution acknowledgments and IRS substantiation",
   target=("Acknowledgments are issued only through a gated command that validates a "
           "counsel-approved, versioned sponsor template containing every mandatory element: "
           "the statement that the sponsoring organization has exclusive legal control over "
           "the contributed assets, the goods-or-services statement, cash amount or noncash "
           "description (without a sponsor valuation of noncash property), donor and sponsor "
           "identity, and contribution date; issuance is blocked if any element is missing. "
           "Each contribution records gift completion, acceptance, availability and "
           "acknowledgment dates separately. Acknowledgment timing for reversible rails is "
           "sponsor-configured (default after finality); a returned ACH or chargeback voids or "
           "amends the acknowledgment through a recorded correction. The contributor of "
           "record is determined by a CPA- and counsel-approved rule and never defaults to "
           "the advisory-privilege holder. Statements are never presented as acknowledgments, "
           "and tax disclosures never imply nonitemizer deductibility. Legally significant "
           "wording cannot be altered by sponsor branding. Issued documents are immutable and "
           "accessible."),
   stmt=("Planned: template-validated acknowledgments with all mandatory elements are "
         "specified. No acknowledgment has been issued."),
   reqs=["UNB-RCN-FIN-001", "CNV-FIN-003", "UNB-RCN-WF-004", "UNB-RCN-ENT-009",
         "RR-UNB-ACC-006-r1", "UNB-DOC-002", "UNB-RCN-FIN-015", "UNB-RCN-PLT-007",
         "UNB-RCN-PLT-010", "RR-REQ-X-032-r1", "UNB-RCN-FIN-012", "UNB-RCN-GRT-015"],
   oqs=["Counsel-approved acknowledgment templates do not exist yet."],
   mech="event-driven-automated", fresh="per-event",
   owner="Unassigned (proposed: sponsor compliance with counsel)",
   ctls=[C("Gated acknowledgment issuance with mandatory element validation",
           "Issue acknowledgments only via a command that validates every counsel-designated element against a versioned template.",
           "preventive-gate", "L2-type-system", policies=["SEC-LANG-002"],
           related=["UNB-CTRL-053", "UNB-SCTRL-031"],
           frefs=[UB("UNB-RCN-FIN-001"), S("SRC-IRC-170", "170(f)(18)", "maps-to", "directly-documented")]),
       C("Protected legal terminology",
         "Reject sponsor branding or terminology overrides that alter legally meaningful acknowledgment wording.",
         "preventive-gate", "L3-restricted-interface", frefs=[UB("UNB-RCN-PLT-007")]),
       C("Acknowledgment correction on reversal",
         "On returned or charged-back contributions, void or amend the acknowledgment through a linked correction and notify the donor.",
         "corrective", "L3-restricted-interface", frefs=[UB("CNV-FIN-003")])],
   evrs=[E("Acknowledgment issuance record", "Template version, element validation result, document hash, delivery receipts and corrections.",
           "event-driven-automated", "per-event", prov=["template_version", "document_sha256", "contribution_id"],
           producer="not yet assigned (intended renderer: Folio)")],
   qs=[
    Q("Acknowledgment content", "Do contribution acknowledgments include every element the IRS requires for DAF contributions, including the sponsor's exclusive legal control statement?",
      "Donor deductions are substantiated.", "Donor deductions disallowed for defective acknowledgments.",
      [S("SRC-IRC-170", "170(f)(18)", "maps-to", "directly-documented"), S("SRC-IRC-170", "170(f)(8)"), P1771],
      "legal-regulatory", "critical", auth="IRS", ind=IND,
      alts=["Provide a sample DAF contribution acknowledgment."]),
    Q("Acknowledgment timing", "When are acknowledgments issued for reversible payment methods such as ACH debit or card, and what happens if the payment is reversed?",
      "Avoid acknowledging contributions that fail.", "Acknowledgments for contributions never received.",
      [UB("UNB-RCN-WF-004"), UB("CNV-FIN-003"), S("SRC-NACHA-RULES")], "industry-convention", "high"),
    Q("Contributor of record", "For joint accounts, third-party payers or entity payers, how do you decide whose name appears on the acknowledgment?",
      "Correct substantiation recipient.", "Acknowledgment issued to the wrong taxpayer.",
      [UB("UNB-RCN-ENT-009"), P1771], "legal-regulatory", "medium", auth="IRS"),
    Q("Corrections", "How are acknowledgment errors corrected, and is the original preserved alongside the corrected version?",
      "Auditable corrections.", "Silent changes to tax documents.",
      [UB("UNB-DOC-002")], "industry-convention", "medium"),
    Q("Statements versus receipts", "How do you ensure fund statements and annual summaries are not mistaken for tax receipts or imply deductibility the donor may not have?",
      "Avoid misleading tax statements.", "Donor misreporting deductions.",
      [UB("UNB-RCN-FIN-015"), UB("RR-REQ-X-032-r1")], "legal-regulatory", "medium", auth="IRS"),
    Q("Gift completion date", "How is the date of a completed gift determined for securities, checks, wires and crypto, and is it stated on the acknowledgment?",
      "Correct tax year for deductions.", "Gifts acknowledged in the wrong tax year.",
      [UB("UNB-RCN-FIN-012"), P1771], "legal-regulatory", "high", auth="IRS"),
   ]),

AU("Noncash gift reporting: Forms 8283 and 8282",
   target=("When the sponsor signs a donor's Form 8283 Section B, Unbound records the "
           "signature event, property description, lot identifiers and date of receipt, and "
           "records that the signature acknowledges receipt, not value. Any sale or other "
           "disposition of such a lot within the counsel-configured reporting window creates "
           "a Form 8282 obligation with due date, owner and donor-copy task, tracked to "
           "filing evidence with escalation. Multi-lot securities intents close as partial "
           "after the sponsor window and acknowledgments and Form 8283 cover only received "
           "lots. For complex-asset gifts through intermediaries, the counsel-approved "
           "structure (agent model by default) determines the donee of record for "
           "acknowledgment, Form 8283 and 8282 duties."),
   stmt=("Planned: Form 8283 signature recording and Form 8282 obligation tracking are "
         "specified. Not implemented."),
   reqs=["UNB-RCN-FIN-002", "UNB-RCN-FIN-003", "UNB-GAP-012", "RR-UNB-INV-012-r1",
         "UNB-RCN-WF-003", "UNB-RCN-WF-005", "CNV-GRT-013", "RR-UNB-ACC-031-r1"],
   oqs=["Forms 8283 and 8282 instructions are not in the seeded source list."],
   mech="event-driven-automated", fresh="per-event",
   owner="Unassigned (proposed: sponsor Tax Lead)",
   ctls=[C("Form 8282 obligation generator",
           "Create a tracked obligation whenever a lot linked to a signed Form 8283 is disposed of within the reporting window.",
           "detective-automated", "L9-runtime-monitored", related=["UNB-CTRL-059"],
           frefs=[UB("UNB-RCN-FIN-003")])],
   evrs=[E("Form 8283/8282 tracking record", "Signature events, lots, dispositions, obligations, filings and donor copies.",
           "event-driven-automated", "per-event")],
   qs=[
    Q("Form 8283 signature", "When the sponsor signs a donor's Form 8283, what does the platform record, and does it make clear the sponsor does not attest to value?",
      "Proper donee acknowledgment of noncash gifts.", "Sponsor appearing to vouch for valuation.",
      [UB("UNB-RCN-FIN-002"), S("SRC-IRC-170", "170(f)(11)"), P1771], "legal-regulatory", "high", auth="IRS", ind=IND),
    Q("Form 8282 tracking", "How do you track dispositions of donated property that require Form 8282 filing and ensure it is filed on time?",
      "Timely donee information returns.", "Penalties for missed Form 8282 filings.",
      [UB("UNB-RCN-FIN-003"), P1771], "legal-regulatory", "high", auth="IRS"),
    Q("Partial securities gifts", "If only some of the securities a donor intended to give arrive, what is acknowledged and reported?",
      "Accurate noncash reporting.", "Acknowledging property never received.",
      [UB("UNB-RCN-WF-003")], "legal-regulatory", "medium", auth="IRS"),
    Q("Intermediary gifts", "For complex assets received through an intermediary, who is the donee of record for acknowledgment and noncash reporting?",
      "Clear reporting responsibility.", "Duplicate or missing donee reporting.",
      [UB("CNV-GRT-013"), UB("UNB-RCN-WF-005")], "legal-regulatory", "medium", auth="IRS"),
   ]),

AU("Information returns (Forms 1099) and payee tax identity",
   status="unknown",
   rationale=("No Unbound requirement specifies Form 1099 determination, TIN collection or "
              "information-return data; sponsor operating accounts payable is explicitly out "
              "of initial scope (RR-UNB-ACC-012-r1). Applicability has not been analyzed."),
   target=("Recommended target (not yet a requirement): Unbound classifies every payee by tax "
           "status at onboarding and flags payments that may require information returns "
           "under a CPA-approved rule table, for example payments to non-exempt persons such "
           "as referral or service fees paid from sponsor operating funds. Grants to "
           "tax-exempt charities are not expected to require Form 1099 reporting, and DAFs "
           "do not make grants to individuals. Where a flag applies, Unbound collects and "
           "validates payee TIN data through the sponsor's process and exports summarized, "
           "reconciled data to the sponsor's accounts payable or 1099 system of record; it "
           "does not file. Processor-issued Forms 1099-K to the sponsor are reconciled to "
           "recorded contributions by processor and period."),
   stmt=("Not available: Unbound does not currently specify Form 1099 support. Sponsor "
         "operating payables, where most information returns arise, are out of Unbound's "
         "initial scope."),
   stmt_kind="not-available",
   reqs=["RR-UNB-ACC-012-r1", "UNB-XIN-CRM-006", "UNB-ACC-021", "UNB-GRANT-040"],
   oqs=["Gap for the Unbound gap analysis: no requirement for information-return "
        "applicability rules, payee TIN collection and validation, or 1099-K reconciliation.",
        "Sources needed but not seeded: IRS General Instructions for Certain Information "
        "Returns and Forms 1099-MISC, 1099-NEC and 1099-K instructions."],
   mech="not-defined", autom="partial", impl="low", rec="low", fresh="P1Y",
   owner="Unassigned (proposed: sponsor Tax Lead)",
   ctls=[C("Payee tax status classification and information-return flag",
           "Classify payees by tax status and flag payments that may require information returns under a CPA-approved rule table.",
           "detective-automated", "L9-runtime-monitored", frefs=[UB("UNB-ACC-021")],
           notes="Recommended only; no Unbound requirement exists.")],
   evrs=[E("Information-return applicability report", "Annual list of payments flagged as possibly reportable, with payee status and TIN validation result.",
           "not-defined", "P1Y", notes="Recommended; not specified in Unbound.")],
   qs=[
    Q("1099 production", "Does the platform identify payments that require Form 1099 reporting and produce or export the data, and which payments does it consider in scope?",
      "Meet information reporting duties.", "Missed information returns and penalties.",
      [UB("UNB-ACC-021"), UB("RR-UNB-ACC-012-r1")], "legal-regulatory", "medium", auth="IRS", ind=IND,
      oq=["1099 instructions not seeded."]),
    Q("Payee TIN collection", "For payees that may require information returns, how are taxpayer identification numbers collected and validated?",
      "Valid TINs for reporting.", "Backup withholding failures and penalties.",
      [UB("UNB-ACC-021")], "legal-regulatory", "low", auth="IRS",
      oq=["No Unbound requirement on TIN collection."]),
    Q("Grants and 1099s", "How do you determine that grant payments to charities do not require information returns, and how are any non-charity payments flagged?",
      "Correct scoping of reporting.", "Over- or under-reporting.",
      [UB("UNB-GRANT-040"), S("SRC-IRS-TEOS")], "legal-regulatory", "low", auth="IRS"),
    Q("1099-K reconciliation", "How are Forms 1099-K issued by payment processors to the sponsor reconciled to contributions recorded on the platform?",
      "Consistency between processor reporting and books.", "Unexplained differences raising IRS inquiries.",
      [UB("UNB-ACC-018")], "industry-convention", "low",
      oq=["1099-K instructions not seeded; card contributions deferred (CNV-PAY-008)."]),
   ]),

AU("OFAC blocked property and rejected transaction reporting",
   target=("Only an authorized human confirms a sanctions true match. On confirmation "
           "involving property in the sponsor's possession, the system records the property "
           "as blocked, prevents any movement (BlockedProperty ledger classification), stops "
           "retry, reissue and capacity restoration, opens a sanctions case, generates "
           "blocked-property report data due to OFAC within 10 business days, tracks the "
           "annual report of blocked property and retains related records for at least 10 "
           "years. A confirmed match without property in possession refuses the transaction "
           "and produces rejected-transaction report data within 10 business days. "
           "Intermediary or provider blocking notices also move a payment to Blocked. "
           "Reliance on OFAC general licenses is versioned and re-verified. Unbound prepares "
           "report data; the sponsor files."),
   stmt=("Planned: OFAC blocking, rejection and report-data generation are specified. "
         "Not implemented; no screening or reporting has occurred."),
   reqs=["UNB-RCN-REG-003", "UNB-RCN-WF-024", "TVR-CMP-004", "UNB-RCN-GRT-006",
         "UNB-RCN-GRT-007", "CNV-GRT-007", "RR-REQ-X-083-r1"],
   oqs=["TVR-CMP-004-Q (blocking versus rejecting) remains open and needs counsel plus drill."],
   mech="event-driven-automated", fresh="per-event",
   owner="Unassigned (proposed: sponsor OFAC compliance officer)",
   ctls=[C("Blocked property state and movement prohibition",
           "On confirmed true match with property in possession, classify as BlockedProperty and reject any movement, retry or reissue.",
           "preventive-structural", "L2-type-system", related=["UNB-SCTRL-014"],
           policies=["SEC-LANG-002"], frefs=[UB("UNB-RCN-REG-003"), OFAC603]),
       C("OFAC report deadline tracker",
         "Track 10-business-day blocked and rejected report deadlines and annual blocked property report; escalate before due.",
         "detective-automated", "L9-runtime-monitored", frefs=[UB("UNB-RCN-WF-024"), OFAC604])],
   evrs=[E("OFAC report data package", "Report data, deadline, filing evidence and retained case records per blocked or rejected transaction.",
           "event-driven-automated", "per-event", retention="At least 10 years (UNB-RCN-REG-003)", disc="internal")],
   qs=[
    Q("Blocked property reports", "If a grant or contribution involves a sanctioned party, can the platform block the property and produce the data for the OFAC report within the required 10 business days?",
      "Sanctions reporting compliance.", "OFAC penalties.",
      [OFAC603, S("SRC-OFAC-COMPLIANCE-FRAMEWORK")], "legal-regulatory", "critical", auth="OFAC", ind=IND,
      alts=["Describe your OFAC blocking and reporting workflow."]),
    Q("Rejected transactions", "How are rejected transactions involving sanctioned parties recorded and reported?",
      "Complete sanctions reporting.", "Unreported rejected transactions.",
      [OFAC604], "legal-regulatory", "high", auth="OFAC"),
    Q("Annual report and retention", "Do you support the annual report of blocked property and retain sanctions records for the required period?",
      "Ongoing sanctions obligations.", "Missing annual reports or records.",
      [OFAC603, UB("UNB-RCN-REG-003")], "legal-regulatory", "medium", auth="OFAC"),
    Q("Match confirmation", "Who confirms a potential sanctions match as a true match, and can automated or AI processes make that determination?",
      "Accountable sanctions decisions.", "Wrongful blocking or missed true matches.",
      [S("SRC-OFAC-COMPLIANCE-FRAMEWORK"), UB("UNB-RCN-GRT-007"), S("SRC-TREASURY-CHARITY-GUIDELINES")], "supervisory-guidance", "high", auth="OFAC"),
   ]),

AU("State charitable registration support and Unbound platform registration",
   target=("Unbound registers as a charitable fundraising platform with the California "
           "Attorney General's Registry and the Hawaii Department of the Attorney General "
           "before activating white-label, embedded, direct-to-consumer or charity-side "
           "donation features for users in those states, and meets associated disclosure and "
           "recordkeeping duties; release 1 ships sponsor-branded deployments only, and those "
           "features stay disabled until registrations are recorded. Unbound does not author "
           "solicitation appeals for sponsors unless fundraising-counsel registration "
           "requirements are determined. For sponsors, Unbound tracks state registration "
           "applicability, deadlines, changes, reminders and authorized submission (WF-21). "
           "California registry status of grantees is ingested and shown, with sponsor "
           "policy choosing hold or warn; the 50-state build is deferred. A regulatory-change "
           "watch list includes state solicitation changes."),
   stmt=("Planned: Unbound's requirements call for platform registration in California and "
         "Hawaii before certain features launch. Echelon has made no registrations; release 1 "
         "is scoped to sponsor-branded deployments."),
   reqs=["CNV-LEG-002", "UNB-WF-021", "CNV-GRT-015", "UNB-EXT-002", "UNB-RCN-REG-001"],
   oqs=["CNV-LEG-002 marks the sponsor-direct California interpretation as moderate "
        "confidence; counsel confirmation is pending.",
        "The state jurisdiction table (evidence backlog) has not been verified."],
   mech="periodic-manual", autom="partial", fresh="P1Y",
   owner="Unassigned (proposed: Echelon counsel for platform registration; sponsor compliance for its own)",
   ctls=[C("Feature activation gate on registration status",
           "Disable white-label, embedded, direct-to-consumer and charity-side donation features in a jurisdiction until the required registration is recorded.",
           "preventive-gate", "L3-restricted-interface", frefs=[UB("CNV-LEG-002"), SOL]),
       C("Sponsor registration deadline tracker",
         "Track sponsor state registration applicability, renewals and changes with reminders and authorized submission records.",
         "detective-automated", "L9-runtime-monitored", frefs=[UB("UNB-WF-021")])],
   evrs=[E("Platform registration record", "Registrations held by Echelon/Unbound per state with renewal dates and evidence.",
           "periodic-manual", "P1Y", producer="not yet assigned", disc="public"),
         E("Sponsor registration calendar", "Per sponsor and state: applicability, due dates, submissions and confirmations.",
           "periodic-automated", "P1M")],
   qs=[
    Q("Platform registration", "Is your company registered as a charitable fundraising platform, commercial co-venturer or fundraising counsel in states that require it?",
      "Vendor complies with state solicitation law.", "Enforcement action affecting the program.",
      [UB("CNV-LEG-002"), SOL], "legal-regulatory", "high", jur=["US-states", "US-state:CA", "US-state:HI"],
      auth="State attorneys general", ind=IND, prod=["unbound", "echelon-organization"]),
    Q("Sponsor registration support", "Does the platform help us track and meet our own state charitable registration and renewal deadlines?",
      "Sponsor stays registered where it solicits.", "Lapsed registrations and penalties.",
      [UB("UNB-WF-021"), SOL], "legal-regulatory", "medium", jur=["US-states"], auth="State attorneys general"),
    Q("Grantee registration status", "Does the platform check grantees' state charity registration status (for example the California Registry) before grants are paid?",
      "Avoid grants to delinquent charities where policy forbids.", "Grants to charities not in good standing.",
      [UB("CNV-GRT-015"), UB("UNB-EXT-002")], "customer-preference", "medium", jur=["US-states", "US-state:CA"]),
    Q("Regulatory change monitoring", "How do you monitor changes in state charitable solicitation and DAF-related rules that affect the platform?",
      "Timely response to rule changes.", "Operating under outdated rules.",
      [UB("UNB-RCN-REG-001"), S("SRC-IRS-DAF-PROPOSED-REGS-2023")], "industry-convention", "medium", jur=["US-federal", "US-states"]),
   ]),

AU("Unclaimed property reporting for uncashed grants and dormant accounts",
   target=("Uncashed grant checks follow explicit states (Issued, Outstanding, AgedOutreach, "
           "StaleDated, VoidRequested, VoidConfirmed, Cleared, UnclaimedPropertyReportable). "
           "Outstanding uncashed grant checks are presumed reportable property owed to the "
           "payee charity. The reporting state is the payee's last known address state, else "
           "the sponsor's state of incorporation (fixed rule XID-BNK-003). A counsel-approved, "
           "statute-derived UnclaimedPropertyRule table per state gives dormancy period, "
           "exemptions, due-diligence notice window and content, and report and remittance "
           "dates. Two outreach attempts, including an offer to reissue by ACH, precede "
           "dormancy. Void and re-credit to the fund is permitted only if the grant was "
           "cancelled before cashing with notice to the charity and the state rule allows; an "
           "item with no rule row stays in review and is never re-credited. Unknown inputs "
           "default to hold and report at dormancy. Dormant DAF accounts follow a sponsor "
           "dormancy policy with charitable default disposition; escheat processing is "
           "limited to payment instruments unless counsel records otherwise."),
   stmt=("Planned: unclaimed property handling for uncashed grant checks is specified in "
         "detail. No state rule table has been populated or verified."),
   reqs=["UNB-XIN-BNK-007", "UNB-XIN-NPG-011", "CNV-PAY-003", "UNB-RCN-GRT-005",
         "UNB-RCN-ENT-005", "RR-UNB-WF-015-r1", "RR-UNB-PAY-006-r1", "UNB-PAY-006", "ADM-024"],
   oqs=["State UnclaimedPropertyRule rows must be populated from statute text; none exist yet."],
   mech="event-driven-automated", fresh="per-event",
   owner="Unassigned (proposed: sponsor Treasury with counsel)",
   ctls=[C("Unclaimed property rule engine with no-rule hold",
           "Determine reporting state, dormancy and outreach deadlines from the rule table; hold items without a rule row and forbid re-credit to funds.",
           "preventive-structural", "L3-restricted-interface", frefs=[UB("UNB-XIN-BNK-007"), UP]),
       C("Due-diligence outreach scheduler",
         "Schedule and record the required outreach attempts before items become reportable.",
         "detective-automated", "L9-runtime-monitored", frefs=[UB("UNB-XIN-NPG-011")])],
   evrs=[E("Unclaimed property report data", "Per state and period: items, outreach evidence, report and remittance evidence or exemption citation.",
           "periodic-automated", "P1Y", disc="customer-only")],
   qs=[
    Q("Uncashed grant checks", "How does the platform handle grant checks that are never cashed, including escheatment to the states?",
      "Comply with unclaimed property law.", "Penalties and audits by state unclaimed property administrators.",
      [UB("UNB-RCN-GRT-005"), UP], "legal-regulatory", "high", jur=["US-states"], auth="State unclaimed property administrators", ind=IND),
    Q("Due diligence letters", "Are required due-diligence notices sent before property is reported, and is evidence retained?",
      "Meet pre-reporting notice duties.", "Noncompliant reporting.",
      [UB("UNB-XIN-NPG-011"), UP], "legal-regulatory", "medium", jur=["US-states"]),
    Q("Re-crediting voided grants", "Under what conditions can a voided, uncashed grant be returned to the donor's fund instead of reported as unclaimed property?",
      "Avoid improper retention of owed property.", "Escheat violations from re-crediting.",
      [UB("CNV-PAY-003"), UP], "legal-regulatory", "high", jur=["US-states"]),
    Q("Reporting state", "How do you determine which state an unclaimed grant must be reported to?",
      "Correct jurisdiction.", "Reporting to the wrong state.",
      [UB("UNB-XIN-NPG-011"), UP], "legal-regulatory", "medium", jur=["US-states"]),
    Q("Dormant accounts", "How are dormant donor-advised fund accounts handled, and are any fund balances treated as unclaimed property?",
      "Correct treatment of inactive funds.", "Improper escheat of charitable assets or donor complaints.",
      [UB("UNB-RCN-ENT-005"), UB("RR-UNB-WF-015-r1"), UP], "legal-regulatory", "medium", jur=["US-states"],
      oq=["Counsel position on DAF balance escheat not recorded."]),
   ]),

AU("Audit-ready reporting packages and regulatory reporting accuracy evidence",
   target=("Unbound generates auditor-ready, time-bounded, reproducible packages: audit "
           "schedules, roll-forwards, supporting workpapers, transaction drill-down and "
           "independently verifiable as-of snapshots, exported through Folio with chain of "
           "custody and access redaction. External auditors receive time-limited, "
           "least-privilege, read-only workspaces with activity history. Every regulatory or "
           "tax report reconciles to the locked ledger with typed reconciling items and zero "
           "unexplained difference, and carries information-produced-by-entity support "
           "(query definition, parameters, population counts, hash, run log). Reports are "
           "reproducible exactly as filed. Audit adjustments post only in a period 13 linked "
           "to audit findings. Preparation, review and sign-off are separate principals and "
           "AI cannot sign or file. Package integrity is verified before release. None of "
           "this replaces the sponsor's external audit or an independent SOC report, which "
           "do not yet exist for Unbound."),
   stmt=("Planned: generated, reproducible audit packages and auditor read-only access are "
         "specified. Echelon has no audit or SOC report and no package has been produced."),
   reqs=["UNB-ACC-020", "SOC2-009", "MON-016", "CNV-GOV-001", "RR-UNB-ACC-017-r1",
         "CNV-FIN-011", "UNB-NAV-050", "REQ-X-039", "UNB-ACC-025", "UNB-GRANT-040",
         "UNB-XIN-NPG-004", "SOC2-020"],
   oqs=["No auditor has reviewed the package design; acceptance of generated evidence is "
        "conditional on a user auditor's planned approach (CNV-GOV-001)."],
   mech="periodic-automated", fresh="P1Y", impl="medium", rec="low",
   owner="Unassigned (proposed: sponsor Controller; Unbound compliance lead)",
   challenge={
       "customer_intent": "Year-end audit and regulatory reports are fast, complete and defensible.",
       "adverse_outcome": "Audit delays, qualified opinions, inaccurate filings.",
       "conventional_control_effectiveness": "Prepared-by-client lists fulfilled manually; accuracy depends on staff extracts that auditors must test separately.",
       "legally_required": "Audits are required for many charities by state law or funders; the package format is not.",
       "contractually_required": "Sponsors expect vendor support for audits.",
       "historical_convention": "Manual PBC fulfillment and spreadsheet roll-forwards.",
       "architectural_elimination": "Manual extraction error removed when packages are pure queries over a certified close snapshot.",
       "automatic_enforcement": "Integrity verification and zero-residual reconciliation gate package release.",
       "continuous_evidence": "IPE metadata and hashes generated with every report.",
       "stronger_alternative": "Generated, reproducible packages with auditor re-performance access.",
       "alternative_verifiable": "Yes, through read-only auditor workspace and re-runnable queries.",
       "customer_acceptance_likelihood": "Likely for efficiency; reliance level is the auditor's decision.",
       "invalidating_conditions": "Auditor tests IPE and finds query definitions or populations unreliable.",
       "conventional_cost": "Staff weeks at year end.",
       "alternative_cost": "Build cost; low recurring.",
       "alternative_risks": "Errors in shared query logic affect every package consistently.",
       "supporting_arguments": ["Reproducibility allows auditors to test once and rely on logic."],
       "opposing_arguments": ["Auditors must still test IPE each period; savings may be smaller than expected.",
                              "A new vendor without SOC reports gets limited reliance."],
       "technical_effectiveness": "stronger", "institutional_acceptance": "uncertain"},
   ctls=[C("Audit package integrity verification",
           "Verify completeness, hashes and redaction of every audit package before release and record chain of custody.",
           "preventive-gate", "L3-restricted-interface", related=["UNB-SCTRL-046", "UNB-CTRL-089", "SOC2-009"],
           frefs=[UB("SOC2-009"), S("SRC-AICPA-TSC", "CC7.2")]),
       C("Report-to-ledger reconciliation with IPE metadata",
         "Reconcile every regulatory report to the locked ledger and attach IPE metadata; block release on unexplained difference.",
         "preventive-gate", "L3-restricted-interface", related=["UNB-SCTRL-033", "UNB-CTRL-060"],
         frefs=[UB("CNV-GOV-001"), SOC1]),
       C("Auditor read-only workspace",
         "Provide time-limited, least-privilege, read-only auditor access with activity logging.",
         "preventive-structural", "L3-restricted-interface", policies=["SEC-AUTH-001"],
         frefs=[UB("MON-016")])],
   evrs=[E("Audit package", "Roll-forwards, schedules, workpapers, snapshots, IPE metadata and chain of custody.",
           "periodic-automated", "P1Y", producer="not yet assigned (intended renderer: Folio)", disc="auditor-only",
           prov=["snapshot_id", "query_hash", "population_count", "package_sha256"]),
         E("Auditor access log", "Auditor workspace grants, expiry and activity history.", "continuous-automated", "per-event", disc="auditor-only")],
   qs=[
    Q("Year-end package", "What audit-ready reports and schedules does the platform provide for our annual financial statement audit (roll-forwards, fund schedules, reconciliations)?",
      "Efficient, complete audits.", "Audit delays and adjustments.",
      [UB("UNB-ACC-020"), ASC], "contractual-common", "high", ind=IND,
      alts=["Can the system fulfill our auditor's prepared-by-client list?"]),
    Q("Auditor access", "Can our external auditors access the platform directly with read-only, time-limited access?",
      "Independent auditor testing.", "Reliance solely on vendor-supplied extracts.",
      [UB("MON-016"), S("SRC-AICPA-TSC", "CC6.1")], "contractual-common", "medium"),
    Q("Reporting accuracy evidence", "How do you demonstrate that regulatory and tax reports produced by the platform are complete and accurate?",
      "Trustworthy regulatory filings.", "Inaccurate filings based on unreliable reports.",
      [UB("CNV-GOV-001"), SOC1, F990], "certification-criteria", "high"),
    Q("Sign-off separation", "Who prepares, reviews and signs off regulatory reports, and can automated or AI processes sign or file them?",
      "Accountability for filings.", "Unreviewed or AI-signed filings.",
      [UB("RR-REQ-X-060-r1"), S("SRC-COSO-2013", "Principle 10")], "industry-convention", "high"),
    Q("Audit adjustments", "How are auditor-proposed adjustments recorded after year end without altering closed periods?",
      "Clean audit trail of adjustments.", "Closed periods rewritten.",
      [UB("CNV-FIN-011")], "industry-convention", "medium"),
    Q("Reproducibility as filed", "Can you reproduce any report exactly as it was originally filed or delivered, even after later corrections?",
      "Defend filed reports.", "Inability to show what was filed.",
      [UB("REQ-X-039"), UB("UNB-NAV-010")], "industry-convention", "medium"),
   ]),
]

if __name__ == "__main__":
    print("RRP", build("RRP", units, IND))
