from lib import *

CAT = "PAY"
OWNER = "Not assigned; proposed: Unbound payments product owner (role not staffed); the sponsor remains Originator and payment authority"
DEF = dict(owner=OWNER, industries=["donor-advised-funds", "nonprofit", "banking", "financial-services"],
           juris=["US-federal"], authority="none")

U = "SRC-ECH-UNB-BASELINE"
NACHA = "SRC-NACHA-RULES"
NDS = "SRC-NACHA-DATA-SECURITY"
NFM = "SRC-NACHA-FRAUD-MONITORING-2026"
UCC = "SRC-UCC-4A"
UP = "SRC-STATE-UNCLAIMED-PROPERTY"
OFAC = "SRC-OFAC-REGS"
TPRM = "SRC-INTERAGENCY-TPRM-2023"
N53 = "SRC-NIST-SP800-53-R5"
COSO = "SRC-COSO-2013"

aus = [
dict(
 title="Nacha roles: sponsor as Originator, Unbound as Third-Party Service Provider holding no funds",
 target=("Each program records a role table naming the Originator (the sponsor), the ODFI, Third-Party Service Providers "
         "(Unbound), any Third-Party Sender or grant-rail partner, and the authorization holder (CNV-PAY-001). By default the "
         "sponsor is Originator of record on sponsor-titled accounts under its own ODFI agreement; the platform operator is a "
         "Third-Party Service Provider, never a Third-Party Sender, and holds no funds (UNB-XIN-BNK-001). Unbound does not sign "
         "an origination agreement, hold or pool donor or grant money, or execute or block a payment on its own authority; any "
         "configuration that would do so is rejected, and a funds-flow conformance check blocks activation of any deployment "
         "that fails (CNV-PAY-001, CNV-LEG-001, UNB-XIN-REG-001). Unbound accepts TPSP obligations by contract, including Nacha "
         "risk-based fraud monitoring, data security and audit cooperation. A versioned RailObligation register maps every "
         "binding obligation for each rail and role to a control, and production enablement of any rail must pass a RailGoLive "
         "gate (RR-UNB-PAY-008-r1). Outbound payments are deliberately deferred: no rail, bank or provider is selected and no "
         "live payment is authorized (PAY-DEF-001 in DEFERRED-PAYMENTS-AND-REMAINING-GAPS.md)."),
 intended="Complete funds-flow legal review and ODFI engagement per sponsor before any rail is enabled; publish the role table to each sponsor's ODFI.",
 prov_refs="CNV-PAY-001, UNB-XIN-BNK-001, CNV-LEG-001, UNB-XIN-REG-001, RR-UNB-PAY-008-r1, UNB-PAY-008",
 statement="Unbound does not process live payments. Its requirements define the sponsor as Originator and Unbound as a Third-Party Service Provider that never holds funds or originates on its own authority. No rail or bank relationship exists yet.",
 kind="planned", controls=["ECTL-PAY-001", "ECTL-PAY-002"], evidence=["EVR-PAY-001", "EVR-PAY-002"],
 requirements=["CNV-PAY-001", "UNB-XIN-BNK-001", "CNV-LEG-001", "UNB-XIN-REG-001", "RR-UNB-PAY-008-r1", "UNB-PAY-008", "UNB-XIN-REG-002"],
 impl_cost="medium", rec_cost="low",
 residual=["Role classification depends on facts each ODFI and counsel will assess; if Unbound transmits files to the ODFI on the sponsor's behalf, some banks may analyze it as closer to a Third-Party Sender arrangement."],
 open_questions=["CNV-LEG-001 says Unbound SHALL NOT be able to execute a payment, while UNB-XIN-REG-001 gives the operator instruction-only authority and the dispatcher transmits instructions (UNB-XIN-EVA-011, CNV-ARC-003). Clarify with counsel whether transmitting sponsor-authorized files is consistent with the TPSP characterization and with 'cannot execute'."],
 challenge=dict(
  customer_intent="ODFI and sponsor want clarity on who bears Nacha warranties and liabilities and whether the vendor is a Third-Party Sender requiring its own agreement and audit.",
  adverse_outcome="Misclassified role leads to missing agreements, unmet audit obligations or unexpected vendor liability.",
  conventional_control_effectiveness="Many payment vendors act as Third-Party Senders with pooled accounts, which concentrates risk and requires stronger oversight.",
  legally_required="Nacha Operating Rules (contractual) define the roles; money transmission law may apply if a vendor holds funds.",
  contractually_required="ODFI origination agreements and TPSP contracts.",
  historical_convention="Vendor-held FBO or pooled accounts as Third-Party Sender.",
  architectural_elimination="Within conforming deployments, vendor custody of funds is eliminated: no operator-titled accounts exist (CNV-LEG-001).",
  automatic_enforcement="Funds-flow conformance check blocks activation.", continuous_evidence="Role table and FundsFlow declaration versions.",
  stronger_alternative="TPSP-only model with sponsor-titled accounts and sponsor-held ODFI relationships.",
  alternative_verifiable="Yes, through account titling evidence and ODFI agreements.",
  customer_acceptance_likelihood="Likely for sponsors with existing bank relationships; harder for small sponsors without ACH origination capability.",
  invalidating_conditions="A sponsor without an ODFI agreement, or a rail partner that pools funds.",
  conventional_cost="Licensing and compliance cost if the vendor holds funds.", alternative_cost="Sponsor must maintain ODFI relationships.",
  alternative_risks="Operational dependence on each sponsor's bank capabilities.",
  supporting_arguments=["Avoids money transmission exposure.", "Keeps legal control of DAF assets with the sponsor."],
  opposing_arguments=["Some ODFIs may still treat a file-transmitting vendor as a Third-Party Sender.", "Small sponsors may prefer a vendor-originated model."],
  technical_effectiveness="stronger", institutional_acceptance="uncertain"),
 questions=[
  Q("In ACH payments made through your platform, who is the Originator, who is the ODFI, and what is your role under the Nacha Operating Rules?",
    "nacha-roles", "Role determines obligations and liability.", "Unclear warranties and liability allocation.",
    [D(NACHA), D(U)], "contractual-common", "critical", alts=["Are you a Third-Party Sender or a Third-Party Service Provider?"]),
  Q("Do you ever hold, pool or take title to our funds or donor funds, for example in a for-benefit-of account?",
    "funds-custody", "Vendor custody creates credit and money transmission risk.", "Loss of funds on vendor failure; licensing issues.",
    [D(U), S("SRC-FFIEC-IT-HANDBOOK")], "legal-regulatory", "critical", reqs=["CNV-LEG-001", "UNB-XIN-REG-001"],
    authority="State money transmission regulators (if funds are held)", juris=["US-federal", "US-states"]),
  Q("Can your company originate, alter, stop or block a payment without our authorization?",
    "payment-authority", "Sponsor must retain payment authority.", "Vendor-initiated or vendor-blocked payments.",
    [D(U)], "customer-preference", "critical", reqs=["CNV-PAY-001", "CNV-LEG-001", "CNV-PLT-007"]),
  Q("Which Nacha obligations do you accept by contract as our service provider, such as data security, fraud monitoring and audit cooperation?",
    "tpsp-obligations", "ODFIs require evidence that service providers meet the Rules.", "Unmet Rules obligations attributed to the Originator.",
    [D(NACHA), D(NFM), D(NDS), D(U)], "contractual-common", "high", reqs=["CNV-PAY-001", "UNB-XIN-BNK-001"]),
  Q("Will you support our ODFI's due diligence and audit of your role, including any required Nacha Rules compliance audit?",
    "tpsp-obligations", "ODFIs oversee third parties in the ACH chain.", "ODFI cannot complete oversight.",
    [D(NACHA), D(TPRM)], "contractual-common", "high", industries=["banking", "donor-advised-funds"], reqs=["CNV-PAY-001", "CNV-GOV-001", "CNV-PLT-009"],
    authority="Nacha; federal banking agencies (third-party risk guidance)"),
  Q("What must be in place before a payment rail is enabled for a customer in production?",
    "rail-activation", "Premature go-live is a common failure.", "Live payments without tested controls or agreements.",
    [D(U)], "customer-preference", "high", reqs=["RR-UNB-PAY-008-r1", "UNB-XIN-BNK-001", "UNB-PAY-008"]),
 ]),
dict(
 title="ACH debit authorizations, retention, account validation and return-rate monitoring",
 target=("Release 1 does not originate ACH debits from donors; contributions arrive by ACH credit, wire, check, securities "
         "transfer or the sponsor's existing processor (CNV-PAY-005). When donor debit origination is enabled, the system captures "
         "a signed or similarly authenticated authorization stating amount or range, frequency, start date, debiting entity and "
         "revocation method, delivers a copy, gives at least 10 days' notice of out-of-range amounts and honors revocation for "
         "entries not yet sent (UNB-XIN-PAY-001). Authorizations are retained for their active life plus two years after "
         "termination or revocation and are not deleted while warranty claims may arise (CNV-PAY-005). The first WEB debit to an "
         "account, and the first after any change, requires account validation by prenote, micro-entry or a third-party service "
         "(UNB-XIN-PAY-002). Rolling 60-day unauthorized, administrative and overall return rates are computed per Originator with "
         "alerts at configurable fractions of the Nacha thresholds and automatic suspension above a sponsor hard limit; "
         "reinitiation is allowed only for R01 and R09 (and R02 to R04 after correction), at most twice within 180 days, with "
         "'RETRY PYMT' and identical company name, ID and amount (UNB-XIN-PAY-005)."),
 intended="Keep donor debit origination disabled until the RailGoLive gate passes for a sponsor; implement authorization records under a retention class that cannot expire during warranty windows.",
 prov_refs="CNV-PAY-005, UNB-XIN-PAY-001, UNB-XIN-PAY-002, UNB-XIN-PAY-005",
 statement="Unbound will not originate donor ACH debits in its first release. When enabled, authorization capture, retention for two years after revocation, account validation and return-rate monitoring are specified. Not implemented.",
 controls=["ECTL-PAY-003", "ECTL-PAY-005", "ECTL-PAY-006"], evidence=["EVR-PAY-003", "EVR-PAY-005"],
 requirements=["CNV-PAY-005", "UNB-XIN-PAY-001", "UNB-XIN-PAY-002", "UNB-XIN-PAY-005", "RR-REQ-X-036-r1"],
 impl_cost="medium", rec_cost="low",
 open_questions=["Regulation E (12 CFR 1005.10) governs preauthorized transfers from consumer accounts; it is not yet in the seeded source list."],
 questions=[
  Q("How are ACH debit authorizations from donors obtained, what do they contain, and how is a copy provided to the donor?",
    "ach-authorization", "Invalid authorizations create unauthorized returns and liability.", "Unauthorized-return disputes and Rules violations.",
    [D(NACHA), D(U)], "contractual-common", "high", scope="Donor ACH debit origination is out of scope for release 1 (CNV-PAY-005)."),
  Q("How long do you retain ACH authorizations and revocations, and can they be deleted under a privacy or retention request while a claim is still possible?",
    "authorization-retention", "Authorizations must survive the warranty period.", "Inability to defend a claim.",
    [D(NACHA), D(U)], "contractual-common", "high", reqs=["CNV-PAY-005", "UNB-XIN-PAY-001", "RR-REQ-X-036-r1", "UNB-IMM-008"]),
  Q("Do you validate a consumer's account before the first WEB debit and after the account number changes?",
    "account-validation", "Nacha requires fraud screening for WEB debits including account validation.", "Debits to invalid or fraudulent accounts.",
    [D(NACHA), D(U)], "contractual-common", "high", reqs=["UNB-XIN-PAY-002"]),
  Q("How do you monitor return rates for debit entries against Nacha thresholds and act when they rise?",
    "return-rates", "Excess returns trigger Nacha inquiries and possible suspension.", "Originator placed under review or suspended.",
    [D(NACHA), D(U)], "contractual-common", "medium", reqs=["UNB-XIN-PAY-005"]),
  Q("Under what conditions will your system reinitiate a returned ACH entry, and how do you prevent improper reinitiation?",
    "reinitiation", "Improper reinitiation violates the Rules.", "Rules violations and donor complaints.",
    [D(NACHA), D(U)], "contractual-common", "medium", reqs=["CNV-PAY-005", "UNB-XIN-PAY-005"]),
 ]),
dict(
 title="ACH returns and notifications of change",
 target=("Returns match on original entry trace number, return reason code and return trace; NOCs match on original trace, change "
         "code and COR trace. When addenda are missing a fallback match (amount, effective date, company ID, account last four, "
         "individual ID) routes to a queue and never auto-posts (CNV-PAY-005). These keys are the registered business idempotency "
         "keys, so redelivered files have no second effect (UNB-XIN-EVA-005). NOC corrections apply within six banking days or "
         "before the next entry, whichever is later, under change control; a matched bank-originated NOC counts as destination "
         "evidence without cooling-off but notifies the charity's verified channels, while any charity-requested change triggered by "
         "an NOC follows the full destination-change rule (CNV-PAY-002). Returns are accepted even after a grant is Disbursed or "
         "Final where the rail permits (TVR-GR-002); returned grant funds re-credit the originating fund by linked compensating "
         "entry, generate no acknowledgment, and restore capacity only after reconciliation (UNB-RCN-GRT-015). Return and NOC "
         "matching apply to grant payments from release 1."),
 intended="Build return and NOC ingestion with deterministic matching, an exception queue and an NOC application timer.",
 prov_refs="CNV-PAY-005, CNV-PAY-002, UNB-XIN-EVA-005, TVR-GR-002, UNB-RCN-GRT-015, RR-UNB-PAY-006-r1",
 statement="Planned: returns and NOCs are specified to match deterministically on trace keys, with unmatched items queued for people and NOC corrections applied within Nacha timeframes under change control. Not implemented.",
 controls=["ECTL-PAY-004", "ECTL-TXI-001"], evidence=["EVR-PAY-004", "EVR-TXI-001"],
 requirements=["CNV-PAY-005", "CNV-PAY-002", "UNB-XIN-EVA-005", "TVR-GR-002", "UNB-RCN-GRT-015", "RR-UNB-PAY-006-r1", "UNB-PAY-006"],
 impl_cost="medium", rec_cost="medium",
 questions=[
  Q("How are returned ACH payments matched to the original grant payment and reflected in the fund and the books?",
    "returns", "Returns must restore funds correctly.", "Lost or misapplied returned funds.",
    [D(NACHA), D(U)], "contractual-common", "high", alts=["Describe your ACH returns processing."]),
  Q("How do you process Notifications of Change, and within what timeframe are corrections applied to future payments?",
    "noc", "Nacha sets deadlines for applying NOCs.", "Repeated entries with stale account data; Rules violations.",
    [D(NACHA), D(U)], "contractual-common", "high", reqs=["CNV-PAY-002", "CNV-PAY-005"]),
  Q("What happens when a return arrives without enough information to match it automatically?",
    "returns", "Fuzzy auto-matching misapplies funds.", "Returned funds posted to the wrong fund.",
    [D(U)], "customer-preference", "medium", reqs=["CNV-PAY-005"]),
  Q("Can an NOC be used by a fraudster to redirect future payments, and how do you guard against that?",
    "noc", "Account updates are a fraud vector.", "Payment redirection through forged change data.",
    [D(U), S(NFM)], "customer-preference", "high", reqs=["CNV-PAY-002", "UNB-XIN-EVA-005"]),
  Q("If a grant payment is returned after the grant was marked complete, how are the grant status, donor communication and acknowledgments corrected?",
    "returns", "Status truthfulness after late returns.", "Donor and charity told a grant was paid when it was not.",
    [D(U)], "customer-preference", "medium", reqs=["TVR-GR-002", "UNB-RCN-GRT-015", "UNB-XIN-EVA-015"]),
 ]),
dict(
 title="Wire transfers, UCC Article 4A security procedures and irrevocable rails",
 target=("Rails are governed by a versioned RailEligibility matrix keyed by payment class, rail and direction, with per-payment "
         "and daily limits and an irreversibility class; Irrevocable and RequestOnly rails such as wires require independent "
         "destination confirmation for each payment above a threshold, and instant rails default to not allowed for grants until "
         "a sponsor enables them (UNB-XIN-BNK-004). Domestic wires are sent with no-deduction instructions and international "
         "wires default to OUR charges, with any pass-through disclosed (CNV-PAY-007). Wire outcomes are confirmed by Fedwire "
         "IMAD/OMAD and beneficiary-bank confirmation before final aging (CNV-PAY-004). An adverse sanctions or status event on "
         "a dispatched but unsettled payment automatically triggers a recall request recorded as externally uncertain (UNB-RCN-GRT-016). "
         "Because the sponsor is the bank's customer under Article 4A, the commercially reasonable security procedure is agreed "
         "between the sponsor and its bank; Unbound's role is to deliver only independently approved instructions through an "
         "authenticated channel the sponsor's bank recognizes."),
 intended="Document, per sponsor, how Unbound-delivered wire instructions interact with the sponsor's Article 4A security procedure, and keep account-number and beneficiary-name consistency checks before release.",
 prov_refs="UNB-XIN-BNK-004, CNV-PAY-007, CNV-PAY-004, UNB-RCN-GRT-016, UNB-CUST-008",
 statement="Planned: wires are specified as irrevocable-class payments with independent destination confirmation, limits and confirmation tracking. No wire capability exists, and Unbound's requirements do not yet address Article 4A security procedure agreements explicitly.",
 controls=["ECTL-PAY-007", "ECTL-FRD-003"], evidence=["EVR-PAY-006", "EVR-FRD-003"],
 requirements=["UNB-XIN-BNK-004", "CNV-PAY-007", "CNV-PAY-004", "UNB-RCN-GRT-016", "UNB-CUST-008", "REQ-X-005"],
 impl_cost="medium", rec_cost="low",
 open_questions=["No Unbound requirement addresses the Article 4A security procedure between sponsor and bank, or loss allocation when a verified instruction comes through Unbound. Recommend a requirement."],
 questions=[
  Q("What security procedure is used to verify wire instructions sent from your platform to our bank, and how does it fit our agreement with the bank under UCC Article 4A?",
    "ucc-4a", "Article 4A allocates loss based on agreed security procedures.", "Customer bears loss for a verified but fraudulent order.",
    [D(UCC, "4A-202"), S(UCC, "4A-201")], "legal-regulatory", "critical", juris=["US-states", "US-federal"],
    authority="State law (UCC Article 4A as enacted); Federal Reserve Regulation J for Fedwire",
    oq=["Not addressed in Unbound requirements."]),
  Q("How do you handle a wire where the beneficiary name and account number do not match?",
    "ucc-4a", "Banks may pay on account number alone.", "Funds credited to the wrong beneficiary.",
    [D(UCC, "4A-207"), D(U)], "legal-regulatory", "high", juris=["US-states"], authority="State law (UCC Article 4A as enacted)",
    reqs=["UNB-XIN-BNK-004", "REQ-X-005", "CNV-PAY-002"]),
  Q("What limits and additional approvals apply to wires compared with ACH, given that wires are generally irrevocable?",
    "wire-controls", "Irrevocable rails need stronger pre-release controls.", "Unrecoverable erroneous or fraudulent wire.",
    [D(U), S(COSO, "Principle 10")], "customer-preference", "critical", reqs=["UNB-XIN-BNK-004", "UNB-CUST-008"]),
  Q("How do you confirm a wire's final status and handle a recall if a problem is discovered after it is sent?",
    "wire-status", "Recall success depends on speed.", "Lost funds due to slow recall.",
    [D(U)], "customer-preference", "high", reqs=["CNV-PAY-004", "UNB-RCN-GRT-016"]),
  Q("For international grants paid by wire, how are intermediary bank fees, sanctions screening of banks in the chain and foreign beneficiary details handled?",
    "international-wires", "Cross-border wires carry fee and sanctions risk.", "Short-paid grants or sanctions violations.",
    [D(U), D(OFAC)], "legal-regulatory", "high", authority="OFAC (sanctions)", juris=["US-federal", "global"],
    reqs=["CNV-PAY-007", "UNB-RCN-GRT-007", "UNB-XIN-EVA-005"], scope="International grants are subject to sponsor scope decisions (UNB-REM-014)."),
 ]),
dict(
 title="Check issuance, void handling, stale dating and reissue",
 target=("The check rail models Issued, Outstanding, AgedOutreach, StaleDated, VoidRequested, VoidConfirmed, Cleared and "
         "UnclaimedPropertyReportable, each with a defined grant, reservation and ledger effect (UNB-RCN-GRT-005). Positive pay with "
         "daily issue files including voids is mandatory, and a check is mailed only after the bank acknowledges its issue record "
         "(CNV-PAY-002, UNB-XIN-BNK-006). Checks void by default at 90 days, configurable but never later than the shortest "
         "applicable state window, with a recorded reason; voiding does not extinguish the grant obligation and does not "
         "automatically re-credit the fund (CNV-PAY-002). A reissue requires a confirmed stop or void, verified recipient "
         "eligibility and destination, and a linked replacement chain (UNB-RCN-GRT-005, CNV-PAY-004). Every program keeps a check "
         "fallback and stored verified destination so charities outside partner networks can be paid (CNV-PAY-001)."),
 intended="Implement the check state machine with void acknowledgment and reissue chain; print and mail through a vendor or the sponsor's bank (not selected).",
 prov_refs="UNB-RCN-GRT-005, CNV-PAY-002, UNB-XIN-BNK-006, CNV-PAY-004, CNV-PAY-001",
 statement="Planned: check payments are specified with mandatory positive pay, 90-day default voiding that preserves the grant obligation, and reissue only after a confirmed void. Not implemented.",
 controls=["ECTL-FRD-005", "ECTL-PAY-008"], evidence=["EVR-FRD-005", "EVR-PAY-007"],
 requirements=["UNB-RCN-GRT-005", "CNV-PAY-002", "UNB-XIN-BNK-006", "CNV-PAY-004", "CNV-PAY-001", "RR-UNB-PAY-006-r1"],
 impl_cost="low", rec_cost="medium",
 questions=[
  Q("How are grant checks voided, and does voiding a check automatically return the money to the donor's fund?",
    "check-voids", "Void handling affects grantee rights and escheat.", "Improper re-credit of funds owed to a charity.",
    [D(U), D(UP)], "legal-regulatory", "high", juris=["US-states"], authority="State unclaimed property administrators"),
  Q("How do you prevent both an original check and its replacement from being paid?",
    "check-reissue", "Double payment on reissue is common.", "Duplicate payment.",
    [D(U)], "customer-preference", "critical", reqs=["UNB-RCN-GRT-005", "CNV-PAY-004", "UNB-XIN-BNK-006"]),
  Q("How long are grant checks valid, and what outreach happens when a check is not cashed?",
    "stale-checks", "Uncashed grant checks mean the charity has not received support.", "Grant purpose unfulfilled; escheat exposure.",
    [D(U)], "customer-preference", "medium", reqs=["UNB-RCN-GRT-005", "UNB-XIN-BNK-007", "CNV-PAY-002"]),
  Q("Who can print, sign and release checks, and how are check stock and signatures protected?",
    "check-issuance", "Physical check controls remain a fraud vector.", "Unauthorized checks issued.",
    [D(U), S(COSO, "Principle 10")], "customer-preference", "high", reqs=["UNB-XIN-BNK-006", "CNV-GOV-003"],
    oq=["Check printing and mailing provider, signature handling and check stock custody are not specified in Unbound requirements."]),
 ]),
dict(
 title="Unclaimed property for uncashed grant and refund checks",
 target=("Unbound maintains a counsel-approved UnclaimedPropertyRule table per state covering owner type, property type, dormancy "
         "period, business-to-business or charitable exemption flags, due-diligence notice window and content, and report and "
         "remittance dates; the state is determined by the payee's last known address with the sponsor's state of incorporation "
         "as fallback per counsel (UNB-XIN-BNK-007). Outstanding uncashed grant checks are presumed reportable property owed to the "
         "payee charity; before dormancy the system makes two outreach attempts including an offer to reissue by ACH. Void-and-"
         "re-credit to the fund is permitted only if the grant was cancelled before cashing with notice to the charity and the state "
         "row records that cancellation defeats the holder obligation. A VoidDisposition record decides re-credit, hold as payable "
         "or report; unknown inputs default to Hold and report at dormancy, and business-to-business exemptions default to not "
         "applicable to grants (CNV-PAY-003). Items with no applicable rule stay in review and are never re-credited."),
 intended="Populate state rule rows from statute text starting with states where sponsors concentrate; generate report and remittance data for the sponsor as holder.",
 prov_refs="UNB-XIN-BNK-007, CNV-PAY-003, UNB-RCN-GRT-005, UNB-RCN-ENT-005",
 statement="Planned: uncashed grant checks are specified to be treated as presumptively reportable unclaimed property under counsel-approved state rules, never silently returned to the fund. Not implemented; no state rule rows have been populated or reviewed by counsel.",
 controls=["ECTL-PAY-009"], evidence=["EVR-PAY-008"],
 requirements=["UNB-XIN-BNK-007", "CNV-PAY-003", "UNB-RCN-GRT-005", "UNB-RCN-ENT-005", "ADM-024"],
 mechanism="periodic-automated", freshness="P1Y", impl_cost="medium", rec_cost="medium",
 residual=["State law varies and changes; rule rows need periodic legal review."],
 questions=[
  Q("How do you handle uncashed grant checks under state unclaimed property laws?",
    "unclaimed-property", "Holders must report and remit dormant property.", "Penalties and interest for unreported property.",
    [D(UP), D(U)], "legal-regulatory", "high", juris=["US-states"], authority="State unclaimed property administrators",
    alts=["Do you support escheatment reporting?"]),
  Q("Which state's unclaimed property rules apply to an uncashed grant, and how is that determined?",
    "unclaimed-property", "Priority rules decide which state is owed.", "Reporting to the wrong state.",
    [D(UP), D(U)], "legal-regulatory", "medium", juris=["US-states"], authority="State unclaimed property administrators", reqs=["UNB-XIN-BNK-007", "CNV-PAY-003"]),
  Q("Do you perform due-diligence outreach to payees before reporting property, and how is it evidenced?",
    "unclaimed-property", "Most states require owner notice before reporting.", "Noncompliant reporting.",
    [D(UP), D(U)], "legal-regulatory", "medium", juris=["US-states"], authority="State unclaimed property administrators", reqs=["UNB-XIN-BNK-007"]),
  Q("Does the platform ever treat dormant donor fund balances themselves as unclaimed property?",
    "dormant-accounts", "Dormant DAF accounts raise different questions than uncashed checks.", "Incorrect escheat of fund assets.",
    [D(U), S(UP)], "legal-regulatory", "low", juris=["US-states"], authority="State unclaimed property administrators",
    reqs=["UNB-RCN-ENT-005", "ADM-024"]),
 ]),
dict(
 title="Payment file security and bank integration authentication",
 target=("Every bank, payment-partner and custodian integration documents its authentication method, credential rotation, least "
         "privilege, webhook signature verification, replay defense, partner context binding and outage behavior "
         "(UNB-API-STD-005, UNB-CUST-017). Inbound files and callbacks require verifiable origin, freshness, deduplication, ordering "
         "and replay protection (UNB-CUST-009, RR-REQ-X-083-r1). Credentials are scoped per sponsor; secrets are never hardcoded "
         "and are managed with approved libraries, managed keys, scanning and rotation (SEC-CRYPTO-001). Sandbox tenants are bound "
         "to mock adapters and cannot resolve or authenticate to any production bank, payment or custody endpoint, and the "
         "simulated adapter never calls a real rail (UNB-XIN-SAS-010, UNB-SCTRL-030). Payment data, including account numbers, "
         "is classified and encrypted under the platform data policy (SOC2-014), and Unbound would accept Nacha data security "
         "obligations as a TPSP (CNV-PAY-001)."),
 intended="Select per-bank transport (bank API with mutual TLS or signed requests, or SFTP with file-level encryption and signing as the bank supports); keep integration credentials in a managed secret store with per-sponsor scope.",
 prov_refs="UNB-API-STD-005, UNB-CUST-017, UNB-CUST-009, RR-REQ-X-083-r1, UNB-XIN-SAS-010, SOC2-014, CNV-PAY-001",
 statement="Planned: bank and payment integrations are specified to use authenticated, replay-protected channels with scoped, rotated credentials; sandboxes cannot reach production rails. No bank integration exists, and specific file encryption and account-number protection requirements are not yet written.",
 controls=["ECTL-PAY-010", "ECTL-PAY-011", "ECTL-TXI-009"], evidence=["EVR-PAY-009", "EVR-PAY-010", "EVR-TXI-009"],
 policies=["SEC-CRYPTO-001", "SEC-DATA-001", "SOC2-014"],
 requirements=["UNB-API-STD-005", "UNB-CUST-017", "UNB-CUST-009", "RR-REQ-X-083-r1", "UNB-XIN-SAS-010", "CNV-PAY-001", "UNB-PAY-007", "UNB-TEN-006"],
 impl_cost="medium", rec_cost="low",
 open_questions=["Unbound requirements do not explicitly require rendering stored ACH account numbers unreadable, as the Nacha Supplementing Data Security Requirements do for covered parties. Recommend an explicit requirement.",
                 "Transport choice (bank API, SFTP, file encryption and signing format) depends on banks not yet selected."],
 questions=[
  Q("How are payment files and payment instructions protected in transit and at rest, including encryption and integrity protection?",
    "payment-file-security", "Altered or intercepted files cause misdirected payments.", "File tampering or account data exposure.",
    [D(NDS), S(N53, "SC-8"), S(N53, "SC-28")], "contractual-common", "critical", alts=["Do you encrypt and sign ACH files?"]),
  Q("Do you render bank account numbers unreadable when stored electronically, as required by Nacha data security rules for covered parties?",
    "account-data", "Nacha requires protection of stored account numbers for covered parties.", "Exposure of account numbers.",
    [D(NDS), S("SRC-PCI-DSS-4.0.1")], "contractual-common", "high", reqs=["CNV-PAY-001", "UNB-PAY-005", "SOC2-014"],
    oq=["No explicit Unbound requirement; see answer unit open questions."]),
  Q("How does your platform authenticate to our bank or payment provider, and how are those credentials stored, scoped and rotated?",
    "bank-authentication", "Stolen integration credentials enable fraudulent instructions.", "Unauthorized instructions via stolen credentials.",
    [D(U), S(N53, "IA-5"), S("SRC-CSA-CCM-V4")], "customer-preference", "critical", reqs=["UNB-API-STD-005", "UNB-CUST-017", "UNB-TEN-006"]),
  Q("How do you verify that status updates and files received from banks and providers are genuine and not replayed?",
    "bank-authentication", "Spoofed confirmations can trigger reissue or false completion.", "Fraudulent status changes.",
    [D(U), S(N53, "SC-23")], "customer-preference", "high", reqs=["RR-REQ-X-083-r1", "UNB-CUST-009", "UNB-API-STD-005"]),
  Q("How do you ensure that test or sandbox environments can never send a real payment?",
    "environment-separation", "Test systems sending live payments is a known failure.", "Unintended live disbursement.",
    [D(U)], "customer-preference", "high", reqs=["UNB-XIN-SAS-010", "UNB-PAY-007", "UNB-SCTRL-030"]),
 ]),
dict(
 title="Dual control on payment release, limits and no out-of-band origination",
 target=("No grant recommendation, AI proposal or internal journal authorizes outbound funds; release requires sponsor reserved "
         "authority, independent release control, payee verification and least privilege (UNB-PAY-003). Until a deterministic "
         "release gate is accepted by the sponsor's auditor and board, release requires three distinct people (CNV-GOV-003). "
         "Approvals are checked against delegation-of-authority limits, and rail eligibility carries per-payment and daily limits "
         "(UNB-XIN-ERP-005, UNB-XIN-BNK-004). A batch carries no approval or release authority itself; each item is released and "
         "re-checked against holds immediately before transmission (UNB-XIN-EVA-011, CNV-ARC-003). No payment may originate outside "
         "the platform gate, manual fallback runs through the gate with dual control, and bank portal entitlements give no "
         "unilateral release rights outside it (TVR-PAY-004). When bank feeds are stale, releases of already-reserved grants may "
         "proceed only on a balance attestation by two treasury staff distinct from the releasing approvers, valid one business day "
         "(CNV-PAY-007). Any platform hold leaves the sponsor able to pay through its own bank channel (CNV-PLT-007)."),
 intended="Implement the release gate with distinct-person enforcement and limit checks; document each sponsor's bank portal entitlement configuration and review it quarterly.",
 prov_refs="UNB-PAY-003, CNV-GOV-003, UNB-XIN-ERP-005, UNB-XIN-BNK-004, UNB-XIN-EVA-011, CNV-ARC-003, TVR-PAY-004, CNV-PAY-007, CNV-PLT-007",
 statement="Planned: payment release is specified to require three distinct people (or an auditor-accepted deterministic gate plus humans), limit checks and a re-check against holds at transmission; payments outside the platform gate are prohibited by design. Not implemented.",
 controls=["ECTL-PAY-011", "ECTL-FCT-001", "ECTL-FCT-002", "ECTL-TXI-004"], evidence=["EVR-PAY-010", "EVR-FCT-001", "EVR-TXI-004"],
 policies=["SOC2-018", "SEC-AUTH-001"],
 requirements=["UNB-PAY-003", "CNV-GOV-003", "UNB-XIN-ERP-005", "UNB-XIN-BNK-004", "UNB-XIN-EVA-011", "CNV-ARC-003", "TVR-PAY-004", "CNV-PAY-007", "CNV-PLT-007", "UNB-SCTRL-029"],
 impl_cost="medium", rec_cost="medium",
 residual=["Bank portal entitlements are configured at the sponsor's bank; Unbound can review but not enforce them."],
 open_questions=["Emergency payments during a platform outage (TVR-PAY-004-Q) are unresolved."],
 challenge=dict(
  customer_intent="Ensure no single person can send money.",
  adverse_outcome="Single-person fraud or error in payment release.",
  conventional_control_effectiveness="Dual approval in the bank portal is standard but often undermined by shared tokens, broad entitlements and rubber-stamping.",
  legally_required="No statute; bank agreements and auditor expectations.", contractually_required="Commonly in bank agreements and sponsor policies.",
  historical_convention="Maker-checker in the bank portal.",
  architectural_elimination="Within the platform, single-person release is impossible because the gate requires distinct principals; out-of-band release is addressed by limiting portal entitlements, which Unbound cannot enforce.",
  automatic_enforcement="Distinct-person check, limits and hold re-check at transmission.",
  continuous_evidence="Release records with approvers, limits and hold versions per item.",
  stronger_alternative="Platform gate as the only release path, bank portal limited to view and emergency use under dual control, plus daily unmatched-debit detection.",
  alternative_verifiable="Partly: platform gate is verifiable; portal entitlements require sponsor and bank evidence.",
  customer_acceptance_likelihood="Likely; some sponsors will want to keep portal release rights.",
  invalidating_conditions="Sponsor keeps broad portal release entitlements.",
  conventional_cost="Low.", alternative_cost="Medium; operational dependence on platform availability.",
  alternative_risks="Outage blocks payments unless an emergency procedure exists (open question).",
  supporting_arguments=["Closes the organizational double-payment and bypass path.", "Evidence per item."],
  opposing_arguments=["Sponsors and banks may require retaining portal-based release.", "Platform outage risk."],
  technical_effectiveness="stronger", institutional_acceptance="uncertain"),
 questions=[
  Q("Does payment release require approval by at least two different people, and is that enforced by the system?",
    "dual-control", "Dual control is a baseline payment control.", "Single-person release of fraudulent or erroneous payments.",
    [D(U), D(COSO, "Principle 10"), S(N53, "AC-5")], "industry-convention", "critical",
    alts=["Is maker-checker enforced on payment release?"]),
  Q("Can a payment batch or file be approved as a whole, and if so, how do you ensure each payment in it was individually authorized and still valid at transmission?",
    "batch-release", "Batch approval hides individual items.", "Unauthorized items slipped into an approved batch.",
    [D(U)], "customer-preference", "high", reqs=["UNB-XIN-EVA-011", "CNV-ARC-003"]),
  Q("What per-payment and daily limits apply to releases, and who can change them?",
    "payment-limits", "Limits bound the impact of compromise.", "Large unauthorized releases.",
    [D(U)], "customer-preference", "high", reqs=["UNB-XIN-BNK-004", "UNB-XIN-ERP-005", "RR-UNB-ACC-018-r1"]),
  Q("If your platform is unavailable, how would we make urgent grant payments, and what controls apply to that path?",
    "emergency-payments", "Continuity of payments without losing control.", "Uncontrolled manual payments during outages.",
    [D(U), S("SRC-FFIEC-BCM-BOOKLET")], "customer-preference", "high", reqs=["TVR-PAY-004", "CNV-PLT-007"],
    oq=["TVR-PAY-004-Q: emergency payments during outage is unresolved."]),
  Q("How do you decide that enough cash is available to release a payment, especially if the bank balance feed is delayed?",
    "funds-availability", "Releasing against stale balances risks overdrafts and failures.", "Overdraft or failed payments.",
    [D(U)], "customer-preference", "medium", reqs=["CNV-PAY-007", "CNV-FIN-012"]),
  Q("Can your company's staff approve or release payments on our behalf?",
    "vendor-authority", "Vendor staff should not hold sponsor payment authority.", "Vendor insiders releasing funds.",
    [D(U)], "customer-preference", "critical", reqs=["CNV-PAY-001", "CNV-LEG-001", "UNB-XIN-IAM-005"], products=["unbound", "echelon-organization"]),
 ]),
]

for _au in aus:
    for _q in _au["questions"]:
        if _q["authority"] is None and any(r["source_id"].startswith("SRC-NACHA") for r in _q["srcs"]):
            _q["authority"] = "Nacha (private rules; enforced through ODFI agreements)"

controls = [
 C("Funds-flow conformance and role table activation check", "Block activation of any deployment whose FundsFlow declaration shows the operator holding title, receiving funds or originating on its own authority, or whose role table is incomplete.",
   "preventive-gate", "L1-eliminated-in-scope", ["Unbound deployment and tenant activation (specified, not built)"], ["EVR-PAY-001"],
   related=["UNB-CTRL-049"], refs=[D("SRC-NACHA-RULES")],
   notes="Scope: operator custody of sponsor or donor funds in conforming deployments. Elimination depends on account titling and contracts, verified at activation."),
 C("RailObligation register and RailGoLive gate", "Prevent production enablement of any rail for any sponsor until every binding obligation row maps to an implemented, tested control and the listed preconditions are met.",
   "preventive-gate", "L5-build-release-gate", ["Unbound payment component and release governance (specified, not built)"], ["EVR-PAY-002"],
   related=["UNB-SCTRL-030", "UNB-CTRL-050"]),
 C("Authorization capture and protected retention class", "Capture complete debit authorizations and revocations and assign a retention class that cannot expire before termination plus two years or while claims are possible.",
   "preventive-structural", "L3-restricted-interface", ["Unbound contributions component (specified, not built)"], ["EVR-PAY-003"], refs=[D("SRC-NACHA-RULES")]),
 C("Deterministic return and NOC matching with exception queue and NOC timer", "Match returns and NOCs on trace-based keys; queue fallback matches for people; track NOC application against the six-banking-day rule.",
   "preventive-structural", "L3-restricted-interface", ["Unbound payment component (specified, not built)"], ["EVR-PAY-004"], refs=[D("SRC-NACHA-RULES")]),
 C("Reinitiation rule enforcement", "Permit reinitiation only for allowed return codes, count and window, with required description and identical company data; refuse unauthorized-coded returns without new authorization.",
   "preventive-structural", "L3-restricted-interface", ["Unbound payment component (specified, not built)"], ["EVR-PAY-005"], refs=[D("SRC-NACHA-RULES")]),
 C("Return-rate monitoring against Nacha thresholds", "Compute rolling 60-day return rates per Originator and alert or suspend debit origination at configured limits.",
   "detective-automated", "L9-runtime-monitored", ["Unbound payment monitoring (specified, not built)"], ["EVR-PAY-005"], refs=[D("SRC-NACHA-RULES")]),
 C("Irrevocable-rail destination confirmation and wire instruction checks", "For wires and other irrevocable rails, require independent destination confirmation above threshold, beneficiary name and account consistency, sanctions screening of the bank chain and fee instructions before release.",
   "preventive-gate", "L3-restricted-interface", ["Unbound payment component (specified, not built)"], ["EVR-PAY-006"],
   refs=[S("SRC-UCC-4A", "4A-207")], cwe=["CWE-345"]),
 C("Check state machine with void-before-reissue", "Enforce check states and require bank-acknowledged void before any reissue, linking replacement chains.",
   "preventive-structural", "L3-restricted-interface", ["Unbound check rail adapter (specified, not built)"], ["EVR-PAY-007"], cwe=["CWE-837"]),
 C("Unclaimed property rule table with default hold", "Determine disposition of uncashed checks from counsel-approved state rows; unknown inputs default to Hold and report at dormancy; no re-credit without a qualifying rule.",
   "preventive-structural", "L3-restricted-interface", ["Unbound payment component (specified, not built)"], ["EVR-PAY-008"],
   refs=[D("SRC-STATE-UNCLAIMED-PROPERTY")], residual=["Rule rows may be outdated"]),
 C("Scoped integration credentials and authenticated transport", "Store bank and provider credentials in a managed secret store scoped per sponsor, rotate them, authenticate every channel and verify signatures on inbound messages.",
   "preventive-structural", "L3-restricted-interface", ["Managed secret store (not selected)", "Unbound integration adapters (specified, not built)"], ["EVR-PAY-009"],
   policies=["SEC-CRYPTO-001"], related=["UNB-SCTRL-039"], cwe=["CWE-798", "CWE-522"], refs=[S("SRC-NACHA-DATA-SECURITY"), S("SRC-NIST-SP800-53-R5", "IA-5")]),
 C("Distinct-person payment release gate with limits and sandbox isolation", "Release requires the configured number of distinct authorized principals, passes limit and eligibility checks, re-checks holds at transmission, and sandbox tenants cannot reach production rails.",
   "preventive-structural", "L3-restricted-interface", ["Unbound payment release gate (specified, not built)"], ["EVR-PAY-010"],
   related=["UNB-SCTRL-029", "UNB-SCTRL-030", "UNB-CTRL-049", "UNB-CTRL-051"], policies=["SEC-AUTH-001"], cwe=["CWE-841"],
   refs=[S("SRC-COSO-2013", "Principle 10"), S("SRC-NIST-SP800-53-R5", "AC-5")]),
]

evidence = [
 E("Program role table and FundsFlow declaration", "Per program role table (Originator, ODFI, TPSP, any Third-Party Sender, authorization holder) and FundsFlow declaration with account titling evidence and conformance result.", NOT_ASSIGNED.format("Unbound tenant activation"), "event-driven-automated", "per-event", disclosure="customer-only"),
 E("RailGoLive gate record", "Obligation rows, mapped controls and test evidence, provider idempotency evidence, fraud program, legal review and sponsor approvals at rail activation.", NOT_ASSIGNED.format("Unbound release governance"), "event-driven-automated", "per-event"),
 E("Authorization and revocation records", "Authorization content, delivery evidence, revocations and retention class.", NOT_ASSIGNED.format("Unbound contributions component"), "event-driven-automated", "per-event"),
 E("Return and NOC processing log", "Each return and NOC with match key, match outcome, queue handling and NOC application date versus deadline.", NOT_ASSIGNED.format("Unbound payment component"), "event-driven-automated", "per-event"),
 E("Return-rate and reinitiation report", "Rolling return rates per Originator, alerts, suspensions and reinitiations with eligibility checks.", NOT_ASSIGNED.format("Unbound payment monitoring"), "periodic-automated", "P1D"),
 E("Wire release and confirmation records", "Destination confirmation, consistency and screening checks, release approvals and IMAD/OMAD or beneficiary-bank confirmation.", NOT_ASSIGNED.format("Unbound payment component"), "event-driven-automated", "per-event"),
 E("Check lifecycle records", "Check states with issue and void acknowledgments, stale dating, outreach and reissue chains.", NOT_ASSIGNED.format("Unbound check rail adapter"), "event-driven-automated", "per-event"),
 E("Unclaimed property disposition register", "Per item rule row applied, outreach evidence, report and remittance data or counsel-approved alternative disposition.", NOT_ASSIGNED.format("Unbound payment component"), "periodic-automated", "P1Y"),
 E("Integration credential inventory and rotation log", "Per sponsor and integration: credential type, scope, storage location, rotation dates and authentication failures.", NOT_ASSIGNED.format("Unbound integration adapters"), "periodic-automated", "P90D", disclosure="internal"),
 E("Payment release records", "Per item approvers, distinctness check, limits evaluated, hold version at transmission and sandbox-to-production denial events.", NOT_ASSIGNED.format("Unbound payment release gate"), "event-driven-automated", "per-event"),
]
