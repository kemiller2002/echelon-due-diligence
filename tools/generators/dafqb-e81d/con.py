from dafcommon import *

I170 = lambda loc=None, b="directly-documented", rel="derived-from": S("SRC-IRC-170", loc, rel, b)
P1771 = lambda b="directly-documented": S("SRC-IRS-PUB-1771", rel="informed-by", basis=b)
units = []

u = AU("cash-rails", "Cash contribution intake by ACH, wire and check with provisional status",
    "Contributions arrive by ACH, wire, check or securities transfer into sponsor-titled accounts or through the "
    "sponsor's existing payment provider. Each cash contribution is matched to a gift intent and fund, unmatched "
    "deposits go to an exception queue (never auto-assigned), and reversible-rail contributions remain Provisional and "
    "not grantable beyond a sponsor risk limit until the applicable return window passes. ACH authorizations are "
    "retained for their active life plus two years, and bank feeds use BAI2, ISO 20022 camt messages or bank APIs.",
    "Rails per CNV-PAY-005 and CNV-PAY-007; provisional status per TVR-CON-001; status transparency per UNB-DON-002.",
    "cash contributions would be matched to funds, held provisional on reversible rails and never auto-assigned when unmatched.",
    ["CNV-PAY-005", "CNV-PAY-007", "TVR-CON-001", "UNB-DON-002", "UNB-AST-001", "CNV-PLT-012"],
    impl="medium", rec="medium",
    oq=["No bank or payment provider has been selected; rail capabilities are unverified (UNB-PAY-008)."],
    controls=[CTL("Provisional availability for reversible-rail contributions",
        "Prevent provisional contributions from funding grants beyond the sponsor's approved exposure limit.",
        "preventive-structural", "L3-restricted-interface", ext=["UNB-CTRL-052"], fw=[S("SRC-NACHA-RULES")]),
        CTL("Exception queue for unmatched deposits",
        "Route every unmatched or ambiguous deposit to human resolution rather than automatic assignment.",
        "detective-automated", "L6-automated-analysis", ext=["UNB-CTRL-053"])],
    evrs=[EVR("Contribution intake and matching records",
        "Deposits received per rail, matching results, provisional status and exception resolution.",
        prov=["contribution id", "rail", "bank reference", "fund id", "match method", "availability state", "time"])])
u["questions"] = [
    Q("supported-rails", "Which contribution methods are supported (ACH, wire, check, online bank transfer, card), and into whose accounts do the funds settle?",
      "Sponsors need clarity on rails and fund custody.",
      "Funds settling into non-sponsor accounts.",
      [UNB(), S("SRC-NACHA-RULES")], imp="high"),
    Q("check-handling", "How are mailed checks handled (lockbox, remote deposit capture), and how are they matched to funds?",
      "Checks remain common in DAF contributions.",
      "Lost or misapplied checks.",
      [UNB()], cls="customer-preference", imp="medium"),
    Q("unidentified-deposits", "What happens to a wire or ACH deposit that cannot be matched to a donor or fund?",
      "Unmatched money must not be misapplied.",
      "Funds credited to the wrong fund.",
      [UNB()], imp="high"),
    Q("grantable-timing", "When does a cash contribution become available for grants, and how does the platform limit exposure to later reversals?",
      "Granting against reversible funds creates sponsor loss.",
      "Grants funded with contributions that are later returned.",
      [UNB(), S("SRC-NACHA-RULES")], imp="high"),
    Q("ach-authorizations", "How are donor ACH debit authorizations captured, retained and revoked?",
      "Nacha rules impose authorization and retention requirements on originators.",
      "Unauthorized debit disputes the sponsor cannot defend.",
      [S("SRC-NACHA-RULES", rel="informed-by", basis="directly-documented"), UNB()], cls="contractual-common", imp="medium", auth="Nacha (private rules)"),
]
units.append(u)

u = AU("dates", "The four contribution dates and gift completion rules",
    "Every contribution records GiftCompletionDate (tax rule by instrument and rail from a counsel-approved, versioned "
    "rule table), AcceptanceDate (accounting recognition), AvailabilityDate (sponsor risk rule, explicitly not finality) "
    "and AcknowledgmentDate. Year-end cutoffs use the gift completion date, and contributions missing evidence required by "
    "the rule table are held rather than dated by default.",
    "Date model per CNV-FIN-003, gift date rule table per UNB-RCN-FIN-012.",
    "each contribution would carry four distinct dates with the gift date derived from a counsel-approved rule table.",
    ["CNV-FIN-003", "UNB-RCN-FIN-012", "UNB-GRANT-039", "CNV-FIN-011"], impl="low", auto="full",
    challenge=CH(
        "Donors and sponsors need the correct tax year for each gift.",
        "Donor deductions claimed in the wrong year; acknowledgment errors.",
        "Many systems record a single 'received date', conflating tax completion, accounting and availability.",
        "Gift completion timing derives from tax rules for each instrument; the platform data model is not prescribed.",
        "Not usually contractual.",
        "Staff manually adjust year-end gift dates.",
        "Four separate typed dates make conflation impossible by construction.",
        "Rule table derives the gift date; missing evidence holds the contribution.",
        "Every contribution's dates and rule version are recorded.",
        "Typed date model plus rule-table derivation.",
        "Yes.", "Likely.",
        "If the rule table is wrong, every gift of that type is wrong.",
        "Low.", "Low.",
        "Systematic error from a mis-specified rule.",
        ["Removes year-end ambiguity structurally"],
        ["Requires counsel to approve and maintain the rule table"],
        "stronger", "likely"),
    controls=[CTL("Typed four-date contribution model with rule-table derivation",
        "Ensure every contribution has distinct gift completion, acceptance, availability and acknowledgment dates derived by rule.",
        "preventive-structural", "L2-type-system", ext=["UNB-CTRL-052"], policies=["SEC-LANG-002"])],
    evrs=[EVR("Contribution date derivation records",
        "Each contribution's four dates, the rule table version and the evidence used for gift completion.",
        prov=["contribution id", "instrument", "rule table version", "evidence", "four dates", "time"])])
u["questions"] = [
    Q("four-dates", "Does the platform distinguish the gift date for tax purposes from the dates funds were accepted, became available for grants and were acknowledged?",
      "Each date drives a different obligation.",
      "Wrong tax year or premature grants.",
      [I170(None, "reasonably-inferred", "informed-by"), UNB()], imp="high"),
    Q("gift-date-by-instrument", "How is the tax gift date determined for checks, ACH, wires, securities and complex assets, especially around December 31?",
      "Year-end timing rules differ by instrument.",
      "Donors claim deductions in the wrong year.",
      [I170(None, "reasonably-inferred", "informed-by"), P1771("reasonably-inferred"), UNB()], cls="legal-regulatory", imp="critical", auth="IRS"),
    Q("missing-evidence", "What happens when evidence needed to determine the gift date (for example a postmark or transfer confirmation) is missing?",
      "Defaulting dates can misstate tax years.",
      "Arbitrary gift dates.",
      [UNB()], imp="medium"),
    Q("corrections-period", "How are corrections to contribution dates handled after a period is closed?",
      "Corrections must not rewrite closed periods silently.",
      "Restated statements or acknowledgments without trace.",
      [UNB(), S("SRC-FASB-ASC-958")], imp="medium"),
]
units.append(u)

u = AU("securities", "Publicly traded securities contributions",
    "Securities gifts start from a gift intent (donor, fund, security identifier, quantity, delivering DTC participant, "
    "expected date). Custody receipts are matched deterministically; exactly one match auto-links and zero or multiple "
    "matches go to a queue, so orphan deposits are never assigned by guess. Multi-lot intents close as partial after the "
    "sponsor window, and acknowledgments cover only received lots. Settled liquidation proceeds are distinguished from "
    "unsettled proceeds, and valuations record timestamp, convention and price source.",
    "Securities intake per UNB-XIN-PAY-007, UNB-WF-002, UNB-RCN-WF-003; custody per UNB-CUST-008/015.",
    "securities gifts would be matched deterministically to donor intents with orphan deposits routed for review.",
    ["UNB-WF-002", "UNB-XIN-PAY-007", "UNB-RCN-WF-003", "UNB-CUST-008", "UNB-CUST-015", "UNB-RCN-FIN-011", "CNV-FIN-013"],
    impl="medium", rec="medium",
    oq=["No custodian has been selected; DTC participant data availability depends on custodian feeds."],
    controls=[CTL("Deterministic securities receipt matching",
        "Auto-link only unique matches on security, quantity, delivering participant and date window; queue the rest.",
        "preventive-structural", "L3-restricted-interface", ext=["UNB-CTRL-040", "UNB-CTRL-052"])],
    evrs=[EVR("Securities gift matching and valuation records",
        "Gift intents, custody receipts, match outcomes, partial closures and valuations with price source.",
        prov=["intent id", "receipt id", "CUSIP or identifier", "quantity", "delivering participant", "valuation source", "time"])])
u["questions"] = [
    Q("orphan-deposits", "How does the platform match incoming securities transfers to the correct donor and fund, and what happens to unidentified transfers?",
      "Securities often arrive without clear donor identification.",
      "Shares credited to the wrong fund.",
      [UNB()], imp="high"),
    Q("partial-lots", "How are multi-lot or partially delivered securities gifts handled and acknowledged?",
      "Partial deliveries complicate acknowledgment.",
      "Acknowledging shares that never arrived.",
      [UNB(), P1771("reasonably-inferred")], imp="medium"),
    Q("liquidation-policy", "Does the platform support immediate liquidation versus holding of contributed securities per sponsor policy, and how are proceeds tracked?",
      "Sponsors differ on liquidation; proceeds must be traceable.",
      "Proceeds misallocated or invested contrary to policy.",
      [UNB()], cls="customer-preference", imp="medium"),
    Q("securities-valuation", "How are contributed publicly traded securities valued for fund crediting and donor statements, and is the valuation method disclosed?",
      "Valuation affects donor statements and sponsor accounting.",
      "Inconsistent or undisclosed valuation.",
      [UNB(), S("SRC-FASB-ASC-958")], imp="medium"),
    Q("mutual-funds", "How are mutual fund share transfers, which do not settle through the same channels as equities, handled?",
      "Mutual fund transfers are slower and often manual.",
      "Lost or delayed mutual fund gifts.",
      [UNB()], cls="customer-preference", imp="low"),
]
units.append(u)

u = AU("noncash-substantiation", "Non-cash valuation, qualified appraisals and Forms 8283 and 8282",
    "Sponsor accounting valuations, donor-provided valuations, qualified appraisals and tax basis are kept separate. "
    "Gifts above the qualified appraisal threshold (including crypto above counsel-configured thresholds) are flagged as "
    "requiring a donor-obtained qualified appraisal. The platform tracks the sponsor's signature on Form 8283 Section B "
    "(donee acknowledgment), and monitors dispositions within three years of receipt to prepare Form 8282 data. The "
    "donee of record for intermediary-handled assets is determined by the counsel-approved agreement structure.",
    "Valuation separation per UNB-GAP-012; appraisal flags per UNB-RCN-FIN-011; donee model per UNB-RCN-WF-005 and CNV-GRT-013.",
    "non-cash gifts would carry separate valuation types, appraisal flags and Form 8283 and 8282 tracking.",
    ["UNB-GAP-012", "UNB-RCN-FIN-011", "UNB-RCN-WF-005", "CNV-GRT-013", "UNB-NAV-013"], status="proposed-target-state",
    impl="medium", rec="medium", auto="partial",
    oq=["Form 8283 and Form 8282 are not seeded sources.", "UNB-GAP-012 is a gap statement, not a normative requirement; detailed requirements are missing."],
    controls=[CTL("Form 8282 disposition window monitoring",
        "Detect sale or disposition of appraised non-cash property within three years of receipt and prepare reporting data.",
        "detective-automated", "L9-runtime-monitored", ext=["UNB-CTRL-058"], fw=[S("SRC-IRC-170", "§170(f)(11)")])],
    evrs=[EVR("Non-cash gift substantiation file",
        "Valuation types, appraisal flags, Form 8283 signature records and disposition monitoring.",
        prov=["contribution id", "asset type", "valuations by type", "appraisal flag", "8283 signer", "disposition date", "time"])])
u["questions"] = [
    Q("appraisal-flags", "How does the platform identify non-cash gifts that require a donor-obtained qualified appraisal, and does it warn donors?",
      "Donors lose deductions without required appraisals.",
      "Donor deductions disallowed; sponsor reputational harm.",
      [I170("§170(f)(11)"), UNB()], cls="legal-regulatory", imp="high", auth="IRS"),
    Q("form-8283", "How does the platform support the sponsor's acknowledgment on Form 8283 for non-cash gifts, and who signs?",
      "The donee's signature is part of the donor's substantiation.",
      "Missing or incorrect donee signatures.",
      [I170("§170(f)(11)", "reasonably-inferred", "informed-by"), UNB()], cls="legal-regulatory", imp="high", auth="IRS",
      oq=["Seed Form 8283 instructions as a source."]),
    Q("form-8282", "How does the platform track dispositions of donated property within three years so the sponsor can file Form 8282?",
      "Donee information returns are required for certain dispositions.",
      "Missed information returns and penalties.",
      [UNB(), S("SRC-IRC-170", rel="informed-by")], cls="legal-regulatory", imp="high", auth="IRS",
      oq=["Seed Form 8282 instructions as a source."]),
    Q("valuation-separation", "Does the platform keep the sponsor's accounting valuation separate from the donor's claimed deduction value and the appraisal value?",
      "These values legitimately differ.",
      "Sponsor appears to endorse a donor's deduction value.",
      [UNB(), P1771("reasonably-inferred")], imp="medium"),
    Q("no-value-on-ack", "Does the platform avoid stating a value for non-cash gifts on acknowledgments, describing the property instead?",
      "Acknowledgments for non-cash gifts describe property rather than value.",
      "Sponsor implicitly valuing property for the donor's deduction.",
      [P1771(), UNB()], cls="industry-convention", imp="medium", auth="IRS"),
]
units.append(u)

u = AU("complex-assets", "Cryptocurrency and complex asset contributions",
    "Acceptance of crypto, privately held stock, real estate, partnership interests and other complex assets is a "
    "sponsor policy decision, not presumed. Complex gifts expected to credit a DAF use a counsel-approved agent model in "
    "which the sponsor is donee of record and any intermediary is its contracted agent. Each asset class has its own "
    "acceptance diligence (source of funds and wallet screening for crypto; environmental, debt, unrelated business "
    "income and excess business holdings review for real estate and business interests), custody and disposition "
    "states, and disclosed, reasonable service charges never paid to donors, advisors or related parties.",
    "Crypto per UNB-WF-004, complex assets per UNB-GAP-011, intermediary model per CNV-GRT-013.",
    "complex assets would be accepted only under sponsor policy with asset-specific diligence and a counsel-approved intermediary model.",
    ["UNB-WF-004", "UNB-GAP-011", "CNV-GRT-013", "UNB-RCN-FIN-011", "UNB-AST-001", "CNV-FIN-010"],
    status="proposed-target-state", impl="high", rec="high", auto="low",
    oq=["UNB-GAP-011 remains a gap; detailed acceptance requirements for each complex asset class are not written.",
        "No crypto custody or liquidation provider has been selected."],
    controls=[CTL("Complex asset acceptance gate",
        "Prevent crediting a complex asset gift to a fund until sponsor-required diligence for that asset class is complete.",
        "preventive-gate", "L10-external-or-manual", ext=["UNB-CTRL-052", "UNB-CTRL-054"])],
    evrs=[EVR("Complex asset acceptance dossier",
        "Asset-class diligence checklist results, approvals, intermediary structure and disposition.",
        mech="event-driven-automated", fmt="JSON record and PDF",
        prov=["contribution id", "asset class", "diligence items", "approver", "intermediary agreement version", "time"])])
u["questions"] = [
    Q("crypto", "Does the platform support cryptocurrency contributions, and how are wallets screened, assets liquidated and gift dates and values recorded?",
      "Crypto gifts are increasingly requested and carry sanctions and valuation risk.",
      "Accepting tainted crypto or misrecording value.",
      [UNB(), S("SRC-OFAC-REGS"), S("SRC-BSA-AML")], cls="customer-preference", imp="high"),
    Q("private-business-interests", "How are gifts of privately held stock or partnership interests evaluated for excess business holdings, unrelated business income and liquidity?",
      "DAFs are subject to excess business holdings rules and UBIT.",
      "Excise taxes or illiquid assets stuck in funds.",
      [S("SRC-PPA-2006", rel="informed-by"), UNB()], cls="legal-regulatory", imp="high", auth="IRS",
      oq=["IRC 4943 is not seeded as a separate source."]),
    Q("real-estate", "How are real estate gifts diligenced (title, environmental, debt) before acceptance?",
      "Real estate carries liability risk.",
      "Sponsor inherits environmental or debt liabilities.",
      [UNB()], cls="industry-convention", imp="medium"),
    Q("intermediary-model", "When a third-party intermediary handles complex assets, who is the donee of record, and who issues acknowledgments and signs Form 8283?",
      "Structure determines tax substantiation duties.",
      "Wrong party acknowledging the gift.",
      [UNB(), I170(None, "reasonably-inferred", "informed-by")], cls="legal-regulatory", imp="high", auth="IRS"),
    Q("complex-asset-fees", "How are fees for handling complex assets disclosed and charged, and what prevents payments to donors or advisors?",
      "Service charges must be reasonable and not benefit related parties.",
      "Excess benefit or undisclosed fees.",
      [S("SRC-IRC-4958", rel="informed-by"), UNB()], imp="medium"),
]
units.append(u)

u = AU("reversals", "Contribution reversals, returns and chargebacks",
    "A returned ACH debit, dishonored check or card chargeback reverses the contribution as never completed and voids or "
    "amends the acknowledgment. If a reversed contribution already funded disbursements, the platform creates a donor "
    "receivable and sponsor exposure case and never allows a silent negative fund. Return and claim windows drive "
    "per-donor exposure limits across all unmatured reversible amounts. Card acceptance is architecturally supported but "
    "disabled in release 1.",
    "Reversal model per CNV-FIN-003, TVR-CON-001 and TVR-CON-003; ACH return handling per CNV-PAY-005; cards per CNV-PAY-008.",
    "reversals would void contributions and acknowledgments and create exposure cases rather than negative funds.",
    ["CNV-FIN-003", "TVR-CON-001", "TVR-CON-003", "CNV-PAY-005", "CNV-PAY-008", "UNB-GEX-014"], impl="medium",
    controls=[CTL("Reversal voids contribution and acknowledgment",
        "Ensure every reversal reverses the contribution and voids or amends its acknowledgment via linked entries.",
        "corrective", "L3-restricted-interface", ext=["UNB-CTRL-052", "UNB-CTRL-053"]),
        CTL("Per-donor reversible exposure limit",
        "Limit grantable capacity funded by unmatured reversible contributions per donor.",
        "preventive-structural", "L3-restricted-interface", ext=["UNB-CTRL-052"])],
    evrs=[EVR("Reversal and exposure case records",
        "Reversals with reason codes, linked accounting entries, acknowledgment amendments and exposure cases.",
        prov=["contribution id", "return reason", "linked entries", "acknowledgment action", "exposure case id", "time"])])
u["questions"] = [
    Q("returned-contributions", "What happens when a contribution is reversed (returned ACH, bounced check) after it has been credited to a fund?",
      "Reversals must be reflected accurately.",
      "Overstated fund balances.",
      [UNB(), S("SRC-NACHA-RULES")], imp="high"),
    Q("reversal-after-grant", "What happens if a reversed contribution already funded a paid grant?",
      "The sponsor bears the loss if not controlled.",
      "Sponsor loss and negative fund balances.",
      [UNB()], imp="high"),
    Q("acknowledgment-void", "Are acknowledgments voided or amended when a contribution is reversed, and is the donor notified?",
      "Donors must not claim deductions for gifts that failed.",
      "Invalid deductions supported by sponsor documents.",
      [P1771("reasonably-inferred"), UNB()], imp="high"),
    Q("card-chargebacks", "If card contributions are accepted, how are chargebacks, which can arrive months later, handled?",
      "Card chargeback windows are long.",
      "Late reversals after grants paid.",
      [UNB(), S("SRC-PCI-DSS-4.0.1")], cls="customer-preference", imp="medium"),
]
units.append(u)

u = AU("acknowledgments", "Contribution acknowledgments and substantiation",
    "Acknowledgments are issued only through a gated command that validates a counsel-approved, versioned sponsor "
    "template containing every mandatory element, including the statement that the sponsoring organization has "
    "exclusive legal control over the contributed assets and whether any goods or services were provided. Issued "
    "acknowledgments are immutable artifacts with content hashes, timely relative to the donor's filing needs, amended "
    "through linked corrections, available in annual summaries, and retained per the sponsor's schedule.",
    "Gated issuance per UNB-RCN-FIN-001, content per CNV-GRT-014, artifact registry per REQ-X-034, retention per CNV-PLT-004.",
    "acknowledgments would be issued only from counsel-approved templates that include all required statements.",
    ["UNB-RCN-FIN-001", "CNV-GRT-014", "REQ-X-034", "CNV-PLT-004", "REQ-X-036", "UNB-PLAT-003"], impl="medium",
    challenge=CH(
        "Sponsors need every acknowledgment to satisfy substantiation rules so donors keep deductions.",
        "A missing statement invalidates the donor's deduction substantiation.",
        "Manual review of letter templates and spot checks catch some errors but not template drift.",
        "Contemporaneous written acknowledgment and DAF exclusive legal control statements are required for donor deductions (§170(f)(8), §170(f)(18)).",
        "Sponsor agreements usually require accurate receipts.",
        "Staff maintain letter templates and review samples.",
        "Gated issuance makes an acknowledgment missing mandatory elements impossible to send.",
        "Template validation at issuance.",
        "Each issued acknowledgment carries template version and hash.",
        "Gated issuance from validated templates.",
        "Yes.", "Likely.",
        "If counsel's mandatory element list is incomplete, every acknowledgment shares the gap.",
        "Low.", "Low.",
        "Template errors replicate at scale.",
        ["Structural compliance with substantiation content"],
        ["Depends on counsel-maintained element list"],
        "stronger", "likely"),
    controls=[CTL("Gated acknowledgment issuance with mandatory element validation",
        "Block issuance of any acknowledgment lacking a counsel-designated mandatory element.",
        "preventive-gate", "L3-restricted-interface", ["Unbound (proposed; not built)", "Folio (exists; not operated for Unbound)"],
        ext=["UNB-CTRL-059", "UNB-CTRL-088"], fw=[S("SRC-IRC-170", "§170(f)(8)"), S("SRC-IRC-170", "§170(f)(18)")])],
    evrs=[EVR("Acknowledgment artifact registry",
        "Each issued acknowledgment with template version, validation result, content hash, delivery and amendments.",
        fmt="PDF plus JSON metadata", prov=["acknowledgment id", "contribution id", "template version", "validation result", "content hash", "issued time"])])
u["questions"] = [
    Q("ack-contents", "What does a contribution acknowledgment contain, and does it include the statement that the sponsor has exclusive legal control over the assets?",
      "DAF acknowledgments have specific required content.",
      "Donor deductions disallowed for defective acknowledgments.",
      [I170("§170(f)(18)"), P1771(), UNB()], cls="legal-regulatory", imp="critical", auth="IRS",
      alts=["Provide a sample DAF contribution receipt."]),
    Q("goods-services-statement", "Does the acknowledgment state whether any goods or services were provided in exchange?",
      "Required for contemporaneous written acknowledgments.",
      "Defective substantiation.",
      [I170("§170(f)(8)"), P1771()], cls="legal-regulatory", imp="high", auth="IRS"),
    Q("ack-timing", "How quickly are acknowledgments issued, and are annual summaries available for donors' tax filing?",
      "Donors need acknowledgments before filing.",
      "Late or missing acknowledgments.",
      [P1771("reasonably-inferred"), UNB()], cls="industry-convention", imp="medium"),
    Q("ack-amendments", "How are acknowledgments corrected or reissued, and is the history preserved?",
      "Corrections occur after reversals or errors.",
      "Conflicting acknowledgments in circulation.",
      [UNB()], imp="medium"),
    Q("ack-authenticity", "Can a donor, tax preparer or auditor verify that an acknowledgment is authentic?",
      "Forged receipts support fraudulent deductions.",
      "Fake acknowledgments attributed to the sponsor.",
      [UNB()], cls="customer-preference", imp="low"),
    Q("no-tax-advice", "Does the platform give donors individualized tax advice, and how is donor-facing tax content kept accurate?",
      "Sponsors avoid giving tax advice.",
      "Misleading tax statements create liability.",
      [UNB()], imp="medium"),
    Q("record-retention", "How long are contribution records and acknowledgments retained, and can legal holds override disposition?",
      "Substantiation and audit need long retention.",
      "Records unavailable for audit or litigation.",
      [UNB(), S("SRC-IRS-PUB-1771")], imp="medium"),
]
units.append(u)

u = AU("fees", "Donor-covered processing fees and fee disclosure",
    "For each processor-settled contribution the platform records gross amount charged (including donor-elected fee "
    "coverage), processor fee and net settled. When fee coverage is voluntary and the sponsor is merchant of record, the "
    "acknowledgment and fund credit use the gross amount and the processing fee posts as an expense; amounts paid to a "
    "non-charity (platform or mandatory convenience fees) are excluded from the acknowledgment and shown separately. "
    "Donor-facing quotes are shown for charged operations, and any amount above the donor's accepted maximum requires "
    "consent.",
    "Fee treatment per CNV-PAY-006 and UNB-XIN-PAY-006; quotes per CNV-ECO-002; fee schedules per CNV-FIN-002.",
    "donor-covered fees would be acknowledged consistently with gross and net amounts recorded separately.",
    ["CNV-PAY-006", "UNB-XIN-PAY-006", "CNV-ECO-002", "CNV-FIN-002"], impl="low",
    oq=["Card contributions are disabled in release 1 (CNV-PAY-008), so donor-covered card fees are deferred."],
    controls=[CTL("Gross, fee and net recording per settled contribution",
        "Ensure fund credit and acknowledgment amounts follow the sponsor's fee treatment rule.",
        "preventive-structural", "L3-restricted-interface", ext=["UNB-CTRL-055", "UNB-CTRL-056"])],
    evrs=[EVR("Contribution fee breakdown records",
        "Gross, fee, net, payout batch and acknowledgment amount per contribution.",
        prov=["contribution id", "gross", "fee", "net", "payout batch", "acknowledged amount", "rule version"])])
u["questions"] = [
    Q("covered-fees-ack", "When a donor covers processing fees, what amount is acknowledged and credited to the fund?",
      "Inconsistent treatment misstates deductions and fund balances.",
      "Over- or under-acknowledged gifts.",
      [UNB(), P1771("reasonably-inferred")], imp="medium"),
    Q("platform-fees", "Are any platform or convenience fees paid to a non-charity excluded from the acknowledgment and disclosed separately?",
      "Payments to non-charities are not charitable contributions.",
      "Acknowledging non-deductible amounts.",
      [I170(None, "reasonably-inferred", "informed-by"), UNB()], cls="legal-regulatory", imp="medium", auth="IRS"),
    Q("fee-disclosure", "How are contribution-related fees disclosed to donors before they give?",
      "Donors expect transparent fees.",
      "Complaints and regulatory scrutiny over hidden fees.",
      [UNB(), S("SRC-STATE-CHARITABLE-SOLICITATION")], cls="customer-preference", imp="medium"),
    Q("fee-reconciliation", "How are processor fees reconciled to settlement deposits and posted?",
      "Fee accounting must reconcile.",
      "Unreconciled differences in sponsor books.",
      [UNB(), S("SRC-AICPA-TSC", "PI1.4")], imp="low"),
]
units.append(u)

u = AU("acceptance-aml", "Contribution acceptance, payor verification and screening",
    "Contributors and third-party payors are identity-verified and screened at onboarding, delta-screened on list updates "
    "and screened on contribution. The funding account owner is matched to the donor, and third-party payments require "
    "an explicit acceptance rule. Release 1 supports only the standard DAF account type, so contributions carrying binding "
    "donor restrictions are refused or routed for sponsor decision. Embedded and public contribution endpoints enforce "
    "velocity limits and step-up challenges against card testing, and the sponsor can refuse any gift.",
    "Screening per CNV-GRT-006; funding account owner match per CNV-PLT-003; standard type per CNV-FIN-008; card testing defenses per UNB-XIN-PAY-004.",
    "contributions would be accepted only from verified, screened payors under sponsor acceptance rules.",
    ["CNV-GRT-006", "CNV-PLT-003", "CNV-FIN-008", "UNB-XIN-PAY-004", "UNB-WF-004"], impl="medium",
    oq=["Whether DAF sponsors are subject to BSA/AML program obligations is generally no for public charities; the platform's screening scope beyond OFAC needs counsel confirmation."],
    controls=[CTL("Payor identity and funding account owner match",
        "Prevent crediting contributions from unverified or mismatched funding sources without sponsor decision.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-052"]),
        CTL("Contribution endpoint velocity and challenge controls",
        "Detect and throttle card testing and automated abuse on embedded contribution endpoints.",
        "preventive-structural", "L9-runtime-monitored", fw=[S("SRC-OWASP-API-TOP10-2023", "API6:2023")])],
    evrs=[EVR("Contribution acceptance and screening records",
        "Payor verification, owner match, screening results and acceptance decisions per contribution.",
        prov=["contribution id", "payor id", "verification level", "owner match", "screening list version", "decision", "time"])])
u["questions"] = [
    Q("third-party-payors", "Can contributions be made from accounts not owned by the donor (for example a business or another person), and how is that controlled?",
      "Third-party funding obscures the true donor.",
      "Misattributed gifts or laundering.",
      [UNB(), S("SRC-FINCEN-CDD-RULE")], imp="medium"),
    Q("contributor-screening", "Are donors and payors screened against sanctions lists before contributions are accepted?",
      "Accepting property from a blocked person creates OFAC obligations.",
      "Holding property of sanctioned persons unknowingly.",
      [S("SRC-OFAC-REGS", rel="informed-by", basis="directly-documented"), UNB()], cls="legal-regulatory", imp="high", auth="OFAC (Treasury)"),
    Q("restricted-contributions", "How does the platform handle contributions that come with binding donor restrictions inconsistent with a standard DAF?",
      "Restricted gifts change the accounting and legal character of the fund.",
      "Accepting gifts the sponsor cannot honor or account for correctly.",
      [UNB(), S("SRC-FASB-ASC-958", "958-605")], imp="medium"),
    Q("gift-refusal", "Can the sponsor refuse or return a contribution, and how is that recorded?",
      "Sponsors must be able to decline problematic gifts.",
      "Forced acceptance of unwanted gifts.",
      [UNB()], cls="customer-preference", imp="low"),
    Q("card-testing", "What protections exist against card testing and automated abuse of public or embedded contribution forms?",
      "Donation forms are common card testing targets.",
      "Fraud losses and processor penalties.",
      [UNB(), S("SRC-OWASP-API-TOP10-2023", "API6:2023")], cls="industry-convention", imp="medium"),
]
units.append(u)
