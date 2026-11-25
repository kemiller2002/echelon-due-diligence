from lib import *

CAT = "FRD"
OWNER = "Not assigned; proposed: Unbound fraud and payments risk owner (role not staffed) with each sponsor's fraud operations owner"
DEF = dict(owner=OWNER, industries=["donor-advised-funds", "nonprofit", "financial-services", "banking", "wealth-management"],
           juris=["US-federal"], authority="none")

U = "SRC-ECH-UNB-BASELINE"
NACHA = "SRC-NACHA-RULES"
NFM = "SRC-NACHA-FRAUD-MONITORING-2026"
FFA = "SRC-FFIEC-AUTH-GUIDANCE-2021"
N63 = "SRC-NIST-SP800-63-4"
ATT = "SRC-MITRE-ATTACK"
COSO = "SRC-COSO-2013"
TSC = "SRC-AICPA-TSC"

aus = [
dict(
 title="Account takeover resistance for donor, advisor, charity and sponsor accounts",
 target=("Platform and sponsor privileged roles use AAL3-grade authenticators (hardware keys or device-bound non-exportable keys, "
         "two per user, no synced passkeys) with identity-proofed recovery; other workforce uses AAL2 phishing-resistant "
         "authenticators; knowledge-based verification is never used for proofing (CNV-PLT-003). A StepUpPolicy matrix maps "
         "high-risk actions (authenticator or recovery change, authority or delegation change, payee or destination change, data "
         "export, large grant recommendations, API credential creation) to required assurance and a maximum authentication age "
         "of five minutes by default, and the step-up event is bound to the command (UNB-XIN-IAM-003). Authority-relevant "
         "credential changes need step-up, a cooling-off period and notice to the prior channel, and grants to recipients added "
         "during cooling-off need sponsor-direct confirmation (AUTH-I7). Auto-approval ceilings depend on session assurance, "
         "aggregate thresholds defeat splitting, and a new recipient from a phishable or agent session needs step-up (TVR-SEC-004); "
         "recipient novelty is measured from the last confirmation through a pre-existing channel, so waiting out a window does "
         "not make a recipient known (TVR-SEC-010)."),
 intended="Implement the StepUpPolicy matrix and cooling-off rules in the authorization component; red-team phishable-session grant attempts before launch.",
 prov_refs="CNV-PLT-003, UNB-XIN-IAM-003, AUTH-I7, TVR-SEC-004, TVR-SEC-010, REQ-X-072",
 statement="Planned: Unbound specifies phishing-resistant authentication for privileged roles, command-bound step-up for high-risk actions and cooling-off after credential changes. Not implemented or red-teamed.",
 controls=["ECTL-FRD-001", "ECTL-FRD-002"], evidence=["EVR-FRD-001", "EVR-FRD-002"], policies=["SEC-AUTH-001", "SOC2-010"],
 requirements=["CNV-PLT-003", "UNB-XIN-IAM-003", "AUTH-I7", "TVR-SEC-004", "TVR-SEC-010", "REQ-X-072", "UNB-SCTRL-005"],
 impl_cost="medium", rec_cost="medium",
 residual=["Accessibility of device-bound factors (TVR-SEC-010 open question).", "Donors may resist hardware authenticators; donor accounts rely on AAL2 and behavioral limits."],
 questions=[
  Q("What controls protect donor and advisor accounts from takeover, and could an attacker who phishes a donor's password recommend grants to a new charity?",
    "account-takeover", "Donor account takeover can divert charitable assets.", "Grants directed to attacker-controlled organizations.",
    [D(FFA), S(N63), D(U), S(ATT, "T1078")], "supervisory-guidance", "critical",
    alts=["How do you detect and prevent account takeover?"], authority="FFIEC member agencies (guidance to banks; flows to service providers by contract)"),
  Q("Do administrators and staff with authority over funds or payments use phishing-resistant multifactor authentication?",
    "account-takeover", "Privileged credentials are the highest-value target.", "Takeover of privileged accounts leads to fund diversion.",
    [D(N63), D(FFA), D(U)], "supervisory-guidance", "critical", reqs=["CNV-PLT-003", "UNB-XIN-IAM-003"],
    authority="FFIEC member agencies (guidance)"),
  Q("Which actions require re-authentication or step-up, and how do you ensure the step-up applied to that specific action rather than to the session generally?",
    "step-up", "Session-level step-up can be abused for other actions.", "Step-up reused to authorize a different high-risk action.",
    [D(U), S(N63), S("SRC-OWASP-ASVS")], "customer-preference", "high", reqs=["UNB-XIN-IAM-003"]),
  Q("What happens after someone changes the email, phone, password or authenticator on an account that can recommend grants or change bank details?",
    "credential-change", "Credential changes are a typical takeover step.", "Attacker changes recovery factors then moves money.",
    [D(U), S(FFA)], "customer-preference", "high", reqs=["AUTH-I7", "UNB-XIN-IAM-003"]),
  Q("How do you prevent an attacker from evading limits by splitting a large fraudulent grant into many small ones?",
    "account-takeover", "Structuring evades thresholds.", "Cumulative fraudulent grants under each limit.",
    [D(U), S("SRC-MITRE-CWE", "CWE-799")], "customer-preference", "medium", reqs=["TVR-SEC-004", "EXC-10", "UNB-XIN-ERP-005"]),
 ]),
dict(
 title="Payee and bank account change fraud controls",
 target=("Destination evidence must exist before the first electronic payment to a charity and after every bank-detail change. "
         "The accepted combinations are exactly: (a) a bank-originated account-owner match plus a cooling-off period plus notice on "
         "both the old and new verified channels, or (b) a charity document plus a callback to a contact sourced from the charity "
         "registry or a prior verified record (never from the change request) plus cooling-off plus notice; a charity-signed letter "
         "alone never suffices (CNV-PAY-002). The cooling-off default is three business days and cannot be shortened below one "
         "(UNB-RCN-WF-028). A callback contact must have been verified at least 30 days before the request by default, and any "
         "contact or signatory change inside that window disqualifies it. Charity users who submit bank changes must authenticate "
         "at CAL3. Treasury publishes a versioned DestinationEvidence table per rail and rails that cannot meet it are ineligible "
         "for automated release (UNB-RCN-GRT-017). For tokenized destinations, a per-payment fingerprint is compared with "
         "sponsor-held verified data and provider self-attestation alone is insufficient (TVR-PAY-005, REQ-X-005)."),
 intended="Implement destination evidence records and the release gate; integrate an account-owner validation service where available.",
 prov_refs="CNV-PAY-002, UNB-RCN-WF-028, UNB-RCN-GRT-017, UNB-GEX-018, TVR-PAY-005, REQ-X-005, UNB-PAY-005",
 statement="Planned: bank detail changes are specified to require independent verification from a separately sourced contact, a cooling-off period and notice to previous channels before any payment. Not implemented.",
 controls=["ECTL-FRD-003"], evidence=["EVR-FRD-003"], policies=["SOC2-018"],
 requirements=["CNV-PAY-002", "UNB-RCN-WF-028", "UNB-RCN-GRT-017", "UNB-GEX-018", "TVR-PAY-005", "REQ-X-005", "UNB-PAY-005", "UNB-GRANT-026", "UNB-SCTRL-020"],
 impl_cost="medium", rec_cost="medium",
 residual=["A compromised charity mailbox that was verified earlier can still receive notices; the callback and cooling-off limit but do not eliminate this."],
 questions=[
  Q("How do you verify a request to change a payee's bank account details before any payment is sent to the new account?",
    "payee-change", "Bank change requests are the dominant payment fraud vector.", "Grants paid to a fraudster's account.",
    [D(U), S(NACHA), S("SRC-MITRE-CAPEC")], "customer-preference", "critical",
    alts=["Describe your vendor bank change verification procedure.", "Do you perform callbacks on bank detail changes?"]),
  Q("When you call back to confirm a bank change, where does the phone number come from, and can it come from the change request itself?",
    "payee-change", "Callbacks to attacker-supplied numbers are worthless.", "Attacker confirms their own change.",
    [D(U)], "customer-preference", "critical", reqs=["CNV-PAY-002", "UNB-RCN-GRT-017"]),
  Q("Is there a waiting period between a bank detail change and the first payment to the new account, and who is notified of the change?",
    "payee-change", "Delay plus notice lets the legitimate party object.", "Funds sent before the victim can respond.",
    [D(U)], "customer-preference", "high", reqs=["UNB-RCN-WF-028", "CNV-PAY-002"]),
  Q("Do you validate that the receiving bank account is actually owned by the intended charity, for example through an account-owner match service?",
    "account-validation", "Name-on-account checks catch substitution.", "Funds credited to an account not owned by the charity.",
    [D(U), S(NACHA)], "customer-preference", "high", reqs=["CNV-PAY-002", "UNB-RCN-GRT-017", "REQ-X-005"]),
  Q("If a payment partner stores bank details as tokens, how do you know the token still points to the account you verified?",
    "tokenized-destination", "Tokenization hides substitution at the provider.", "Provider-side substitution undetected.",
    [D(U)], "customer-preference", "medium", reqs=["TVR-PAY-005", "REQ-X-005", "TVR-PAY-006"]),
 ]),
dict(
 title="Business email compromise and social engineering of payment staff",
 target=("Unbound removes the channel that business email compromise exploits: payment instructions, approvals and destination "
         "changes can only be created through authenticated platform commands, never from an email, phone call or uploaded "
         "letter, and ingestion of external files or messages never grants sponsor approval (UNB-EVT-003, UNB-CTL-002). No payment "
         "may originate outside the platform payment gate; manual fallback also runs through the gate with dual control and "
         "bank portal entitlements are limited so no one can release unilaterally outside it (TVR-PAY-004). Callback contacts are "
         "never sourced from the request (CNV-PAY-002). Grant-specific threats such as payment detail substitution, fake charity "
         "identity, insider override and social engineering are explicitly modeled (UNB-GRANT-044). Staff training is a supporting "
         "control, not the primary one."),
 intended="Provide no API, import or UI path that creates a payee change or payment from unstructured inbound content; review bank portal entitlements quarterly.",
 prov_refs="UNB-EVT-003, UNB-CTL-002, TVR-PAY-004, CNV-PAY-002, UNB-GRANT-044",
 statement="Planned: Unbound is designed so that emailed or phoned instructions cannot create or change a payment; all such actions require authenticated in-platform commands with independent approval. Not implemented.",
 controls=["ECTL-FRD-004", "ECTL-FRD-003"], evidence=["EVR-FRD-004", "EVR-FRD-003"],
 requirements=["UNB-EVT-003", "UNB-CTL-002", "TVR-PAY-004", "CNV-PAY-002", "UNB-GRANT-044", "UNB-XIN-IAM-004"],
 impl_cost="low", rec_cost="low",
 residual=["Sponsor staff can still be deceived into approving a fraudulent in-platform request; independent approval and destination evidence reduce but do not remove this.",
           "Sponsor bank portals remain outside Unbound; their entitlements depend on the sponsor and bank."],
 challenge=dict(
  customer_intent="Stop staff from being tricked into sending money by fake emails or calls.",
  adverse_outcome="Large irrecoverable wire or ACH to a fraudster.",
  conventional_control_effectiveness="Awareness training and callback procedures reduce but do not stop BEC; loss data from law enforcement consistently show large BEC losses despite training.",
  legally_required="No.", contractually_required="Insurers and banks often ask about training and callback procedures.",
  historical_convention="Annual phishing training and a written callback policy.",
  architectural_elimination="Within the Unbound payment scope, the email-to-payment path does not exist: there is no command that accepts unstructured inbound content as an instruction.",
  automatic_enforcement="Authenticated commands, destination evidence gate and independent approval.",
  continuous_evidence="Every payee change and payment carries its command provenance; no record can lack one (UNB-XIN-IAM-005 blocks payments when state changes lack a command event).",
  stronger_alternative="Structural elimination of unstructured instruction channels plus training.",
  alternative_verifiable="Yes, by inspecting command catalogs and testing that no import or integration creates payees or instructions.",
  customer_acceptance_likelihood="Likely, though insurers may still require training attestations.",
  invalidating_conditions="Sponsor staff paying outside the platform through bank portals with broad entitlements.",
  conventional_cost="Low.", alternative_cost="Low if designed in from the start.",
  alternative_risks="Customers may perceive inflexibility in urgent situations.",
  supporting_arguments=["Removes the attack path rather than relying on vigilance."],
  opposing_arguments=["Fraudsters adapt by targeting in-platform approvers with pretexts.", "Training remains required by many insurance applications."],
  technical_effectiveness="stronger", institutional_acceptance="likely"),
 questions=[
  Q("What controls prevent your staff or ours from acting on a fraudulent email that appears to come from an executive or a charity requesting an urgent payment or bank change?",
    "business-email-compromise", "BEC is a leading cause of payment loss.", "Funds sent on a spoofed instruction.",
    [D(U), S(ATT, "T1566"), S("SRC-FFIEC-IS-BOOKLET")], "customer-preference", "critical",
    alts=["How do you mitigate business email compromise?"]),
  Q("Can any payment, grant or bank change be initiated by email, phone, fax or uploaded document rather than through the authenticated application?",
    "business-email-compromise", "Out-of-band instruction channels bypass controls.", "Unauthenticated instruction executed.",
    [D(U)], "customer-preference", "critical", reqs=["UNB-EVT-003", "UNB-CTL-002", "TVR-PAY-004"]),
  Q("Can anyone at our organization or yours send a payment directly through the bank portal and bypass the platform's controls?",
    "out-of-band-payments", "Bank portal access undermines platform controls.", "Unilateral release outside the gate.",
    [D(U), S(COSO, "Principle 10")], "customer-preference", "high", reqs=["TVR-PAY-004", "TVR-SEC-008", "UNB-XIN-IAM-004", "UNB-XIN-BNK-003"]),
  Q("Do you train staff who handle payments to recognize social engineering, and how do you test that training?",
    "training", "Insurers and banks ask for training evidence.", "Staff deceived by pretexting.",
    [S("SRC-NIST-CSF-2.0", "PR.AT-01"), S(U)], "customer-preference", "medium", products=["unbound", "echelon-organization"],
    oq=["Echelon has no security awareness program in operation; see HR and ISP categories."]),
 ]),
dict(
 title="Check fraud controls and positive pay",
 target=("Every check account uses positive pay with daily issue files that include voids (CNV-PAY-002). A check cannot move from "
         "Printed to Released-for-mail until the bank acknowledges an issue file with its number, amount, issue date and, where "
         "supported, payee name (payee positive pay). Positive-pay exception decisions default to Return; a Pay decision needs an "
         "authorized human who did not issue the check and recorded evidence. Voids are transmitted and acknowledged before any "
         "reissue (UNB-XIN-BNK-006, UNB-RCN-GRT-005). Disbursement accounts carry debit blocks that allow only named bank-fee "
         "company IDs, and unmatched debits trigger incidents and holds (UNB-XIN-BNK-003). Positive pay is a sponsor bank service; "
         "Unbound produces and transmits the issue data and records acknowledgments."),
 intended="Implement the check state machine and issue-file generation per the sponsor bank's positive pay format.",
 prov_refs="CNV-PAY-002, UNB-XIN-BNK-006, UNB-RCN-GRT-005, UNB-XIN-BNK-003, UNB-GAP-009",
 statement="Planned: check payments are specified to require bank-acknowledged positive pay issue data before release, with exceptions defaulting to Return. Not implemented; depends on the sponsor's bank offering positive pay.",
 controls=["ECTL-FRD-005", "ECTL-FRD-006"], evidence=["EVR-FRD-005", "EVR-FRD-006"],
 requirements=["CNV-PAY-002", "UNB-XIN-BNK-006", "UNB-RCN-GRT-005", "UNB-XIN-BNK-003", "UNB-GAP-009"],
 impl_cost="low", rec_cost="low",
 questions=[
  Q("Do you use positive pay, including payee name verification, for checks issued from our accounts?",
    "positive-pay", "Check alteration and counterfeiting remain common.", "Altered or counterfeit checks paid.",
    [D(U), S("SRC-FFIEC-IS-BOOKLET")], "customer-preference", "critical", alts=["Is payee positive pay supported?"],
    oq=["Payee positive pay availability depends on each sponsor's bank."]),
  Q("Who decides whether to pay or return a positive pay exception, and what is the default if no one decides?",
    "positive-pay", "Exception handling is where positive pay fails.", "Fraudulent items paid by default.",
    [D(U)], "customer-preference", "high", reqs=["UNB-XIN-BNK-006"]),
  Q("How do you prevent a check from being mailed before the bank has the issue record needed to verify it?",
    "positive-pay", "Timing gaps let altered checks clear.", "Check presented before issue data reaches the bank.",
    [D(U)], "customer-preference", "high", reqs=["UNB-XIN-BNK-006", "UNB-RCN-GRT-005"]),
  Q("What controls stop unauthorized ACH debits or checks from being paid out of grant disbursement accounts?",
    "debit-blocks", "Disbursement accounts attract unauthorized debits.", "Funds drained by unauthorized debits.",
    [D(U), S(NACHA)], "customer-preference", "high", reqs=["UNB-XIN-BNK-003", "CNV-PAY-007"]),
 ]),
dict(
 title="Insider fraud and collusion resistance",
 target=("Insider fraud is addressed structurally first: SoD is engine-enforced, AI cannot approve, payment release needs three "
         "distinct people until an accepted deterministic gate exists, and reconciliation sits outside the payment chain "
         "(CNV-GOV-003). Every business day each linked sponsor account's debits must match exactly one authorized instruction or "
         "an expected-debit class; an unmatched debit opens a high-severity incident within an hour, notifies two independent "
         "sponsor roles and holds further releases (UNB-XIN-BNK-003). The standing-data rule extends to external registers: daily "
         "custody movement match, identity-provider admin action match and bank portal entitlement review (TVR-SEC-008). "
         "Collusion-resistant analytics and enforced leave or rotation apply to payment and reconciliation roles (TVR-SEC-006). "
         "Grants whose recipient matches a sponsor operating vendor or a vendor of a party with privileges on the fund route to "
         "related-party review (UNB-XIN-ERP-004). Echelon engineers and agents cannot change control-relevant modules without two "
         "approvers who are not the author, and production database administration is break-glass only (CNV-PLT-010, UNB-XIN-IAM-005)."),
 intended="Implement daily unmatched-debit control and cross-role analytics; operate quarterly access recertification including bank portal users.",
 prov_refs="CNV-GOV-003, UNB-XIN-BNK-003, TVR-SEC-006, TVR-SEC-008, UNB-XIN-ERP-004, CNV-PLT-010, UNB-XIN-IAM-005, UNB-ACC-035",
 statement="Planned: Unbound specifies engine-enforced SoD, daily matching of every bank debit to an authorized instruction, collusion analytics and two-approver change control for financial modules. Not implemented. Echelon has no personnel security program in operation.",
 controls=["ECTL-FRD-006", "ECTL-FRD-007", "ECTL-FCT-001"], evidence=["EVR-FRD-006", "EVR-FRD-007"], policies=["SOC2-018"],
 requirements=["CNV-GOV-003", "UNB-XIN-BNK-003", "TVR-SEC-006", "TVR-SEC-008", "UNB-XIN-ERP-004", "CNV-PLT-010", "UNB-XIN-IAM-005", "UNB-ACC-035"],
 impl_cost="medium", rec_cost="medium",
 residual=["Collusion of the required number of people; analytics reduce but cannot eliminate it."],
 questions=[
  Q("What controls detect or prevent fraud by your own employees or contractors who have access to our financial data or payment processes?",
    "insider-fraud", "Vendor insiders are a material risk.", "Vendor staff divert funds or alter records.",
    [D(COSO, "Principle 8"), D(U), S(ATT)], "customer-preference", "critical", products=["unbound", "echelon-organization"],
    alts=["How do you mitigate insider threat at your company?"]),
  Q("How would you detect a debit from our disbursement account that did not correspond to an approved grant or payment?",
    "unmatched-debits", "Detection of unauthorized movement is the backstop.", "Unauthorized debits unnoticed until month end.",
    [D(U)], "customer-preference", "critical", reqs=["UNB-XIN-BNK-003", "TVR-SEC-008"]),
  Q("Do you use analytics to detect collusion between people in payment, approval and reconciliation roles?",
    "collusion", "SoD does not stop collusion.", "Coordinated fraud by two insiders.", [D(U), S(COSO, "Principle 8")], "customer-preference", "high",
    reqs=["TVR-SEC-006", "CNV-GOV-003"]),
  Q("How do you detect grants to organizations connected to the sponsor's staff, vendors or the donor's own related parties?",
    "related-party", "Related-party grants can be diversion or prohibited benefit.", "Self-dealing through grants.",
    [D(U), D("SRC-IRC-4967")], "legal-regulatory", "high", reqs=["UNB-XIN-ERP-004", "UNB-LS-008", "UNB-SCTRL-016"], authority="IRS"),
  Q("Can engineers or AI agents with production access change balances, payees or control logic without detection?",
    "privileged-insider", "Technical staff can bypass business controls.", "Silent manipulation via code or database.",
    [D(U), S(TSC, "CC8.1"), S("SRC-OWASP-AGENTIC-AI")], "customer-preference", "high", reqs=["CNV-PLT-010", "UNB-XIN-IAM-005", "UNB-XIN-EVA-016"]),
 ]),
dict(
 title="Synthetic identities, contribution fraud and reversible funding",
 target=("Donor and advisor identity proofing is risk-based: core attributes are validated against authoritative sources, the "
         "funding account owner is matched and an address or phone is validated, stepping up to document and selfie or a "
         "non-biometric live-video alternative when validation fails or risk is elevated; entities are verified by registration "
         "and signatory authority (CNV-PLT-003). Sanctions screening, identity proofing, any customer due diligence and contact "
         "assurance are recorded as separate obligations (RR-UNB-PART-007-r1). Contributions on reversible rails remain "
         "Provisional until the rail's return window passes, per a versioned ReversalWindow table, and per-donor exposure caps "
         "weight un-matured reversible amounts (CNV-FIN-003, RR-TVR-CON-001-r1), so a synthetic donor cannot fund grants with money "
         "that is later returned. A reversed contribution reduces capacity immediately and opens an exposure case (RR-REQ-X-009-r1). "
         "Card contribution endpoints enforce velocity limits, minimum amounts and automatic channel suspension (UNB-XIN-PAY-004)."),
 intended="Integrate an identity verification provider behind a provider-neutral interface; implement provisional availability and exposure caps.",
 prov_refs="CNV-PLT-003, RR-UNB-PART-007-r1, CNV-FIN-003, RR-TVR-CON-001-r1, RR-REQ-X-009-r1, UNB-XIN-PAY-004, TVR-CON-003",
 statement="Planned: donor identity proofing and provisional availability of reversible contributions are specified to stop synthetic or fraudulent donors from funding grants. Not implemented; no identity verification provider selected.",
 controls=["ECTL-FRD-008"], evidence=["EVR-FRD-008"],
 requirements=["CNV-PLT-003", "RR-UNB-PART-007-r1", "CNV-FIN-003", "RR-TVR-CON-001-r1", "RR-REQ-X-009-r1", "UNB-XIN-PAY-004", "TVR-CON-001", "TVR-CON-003"],
 impl_cost="medium", rec_cost="medium",
 questions=[
  Q("How do you verify that a new donor or advisor is a real person or entity and not a synthetic identity?",
    "synthetic-identity", "Synthetic donors can be used to launder or test stolen funds.", "Fraudulent accounts funded with stolen money.",
    [D(N63), D(U), S("SRC-FINCEN-CDD-RULE")], "customer-preference", "high", alts=["Describe donor identity verification."],
    oq=["Whether any sponsor has a legal CDD obligation is sponsor-specific; see AML category."]),
  Q("Can a contribution made by ACH debit or card be used to fund grants before the period in which it could be returned or charged back?",
    "reversible-funding", "Grant-then-chargeback is a known fraud pattern.", "Sponsor loss when funded grants are paid and the contribution reverses.",
    [D(U), S(NACHA)], "customer-preference", "critical", reqs=["CNV-FIN-003", "RR-TVR-CON-001-r1", "TVR-CON-001"]),
  Q("How do you detect card testing or automated abuse of public donation forms?",
    "card-testing", "Donation pages are used to test stolen cards.", "Processor penalties and chargebacks.",
    [D(U), S("SRC-OWASP-API-TOP10-2023")], "customer-preference", "medium", reqs=["UNB-XIN-PAY-004", "CNV-PAY-008"],
    scope="Card contributions are disabled in release 1 (CNV-PAY-008)."),
  Q("What happens to the fund and any grants already paid when a contribution is later reversed as fraudulent?",
    "reversible-funding", "Clear treatment avoids silent negative funds.", "Unrecorded losses or negative fund balances.",
    [D(U)], "customer-preference", "high", reqs=["RR-REQ-X-009-r1", "TVR-CON-003"]),
 ]),
dict(
 title="Grant diversion, fake charities and prohibited benefits",
 target=("Unbound detects impersonation, suspicious address or bank changes, duplicate entities, charity hijacking, mismatched "
         "EIN and name and anomalous grant patterns, presented as evidence-based signals rather than automatic findings of guilt "
         "(UNB-CHAR-028, UNB-GEX-033). Identity confidence, grant eligibility, fraud risk and payment beneficiary verification are "
         "kept separate so a confident identity match never substitutes for destination verification (UNB-CHAR-006). Duplicate or "
         "split grants are detected by recommendation fingerprint while legitimate recurring installments are preserved "
         "(EXC-10, UNB-GRANT-029). Grant purpose rules block restricted purposes and prohibited benefits (UNB-SCTRL-016), and grants "
         "to recipients linked to sponsor vendors or fund privilege holders route to related-party review (UNB-XIN-ERP-004). Only "
         "holds derived from verified public facts propagate across sponsors; private suspicions do not (CNV-GRT-004)."),
 intended="Implement fraud signals as P-class outputs that route to human review and holds, never auto-clear or auto-deny (UNB-CTL-001).",
 prov_refs="UNB-CHAR-028, UNB-CHAR-006, UNB-GEX-033, EXC-10, UNB-GRANT-029, UNB-XIN-ERP-004, CNV-GRT-004, UNB-GRANT-044",
 statement="Planned: Unbound specifies charity impersonation and grant-diversion signals that route to human review, plus related-party routing. Not implemented.",
 controls=["ECTL-FRD-009", "ECTL-FRD-003"], evidence=["EVR-FRD-009", "EVR-FRD-003"],
 requirements=["UNB-CHAR-028", "UNB-CHAR-006", "UNB-GEX-033", "EXC-10", "UNB-GRANT-029", "UNB-XIN-ERP-004", "CNV-GRT-004", "UNB-GRANT-044", "UNB-SCTRL-016"],
 impl_cost="medium", rec_cost="medium",
 questions=[
  Q("How do you detect a fraudster impersonating a legitimate charity to receive grants?",
    "charity-impersonation", "Impersonation diverts grants away from the intended charity.", "Grants paid to impostors.",
    [D(U), D("SRC-TREASURY-CHARITY-GUIDELINES")], "customer-preference", "critical"),
  Q("How do you detect grants that may provide a prohibited benefit to a donor, advisor or related party?",
    "prohibited-benefit", "Excise taxes apply to sponsors and managers.", "Excise taxes and reputational harm.",
    [D("SRC-IRC-4967"), D("SRC-IRC-4958"), D(U)], "legal-regulatory", "high", authority="IRS",
    reqs=["UNB-SCTRL-016", "UNB-XIN-ERP-004", "UNB-LS-008"]),
  Q("How are suspected fraud signals handled, and can an automated fraud score alone block or approve a grant?",
    "fraud-signals", "Automated scores can be wrong both ways.", "False accusations or fraud cleared by a model.",
    [D(U), S("SRC-NIST-AI-RMF-1.0")], "customer-preference", "high", reqs=["UNB-CTL-001", "UNB-CTL-005", "UNB-GEX-033", "UNB-CHAR-028"]),
  Q("If you learn that a charity is fraudulent through one sponsor, is that information shared with other sponsors using your platform?",
    "cross-sponsor-signals", "Network effects versus confidentiality and defamation risk.", "Either missed fraud or improper disclosure.",
    [D(U)], "customer-preference", "medium", reqs=["CNV-GRT-004", "UNB-XIN-CLM-004"]),
 ]),
dict(
 title="Fraud monitoring program, anomaly detection and Nacha 2026 amendments",
 target=("For each sponsor that originates ACH entries, Unbound maintains a documented FraudMonitoringProgram covering at least "
         "destination-change after-the-fact review, first payment to a new destination, amount anomalies against the recipient's "
         "history, request-channel provenance for bank-detail changes and debit-origination anomalies; each rule has a version, "
         "owner, risk rationale and outcome metrics, and new ACH origination is blocked if the last completed program review is "
         "older than 12 months plus a grace period (UNB-XIN-BNK-002). As a Third-Party Service Provider, Unbound accepts by "
         "contract the Nacha risk-based fraud monitoring obligations that apply to it, alongside security and audit cooperation "
         "(CNV-PAY-001); a documented program is a precondition of the RailGoLive gate (RR-UNB-PAY-008-r1). Anomaly and AI signals "
         "are independently reviewable and cannot clear controls alone (UNB-ACC-035, UNB-CTL-005). Suspected fraud and account "
         "takeover cases use a restricted-investigation access class, are excluded from general search and AI context, and the "
         "investigator does not make the sponsor decision on the subject transaction (UNB-XIN-CLM-004)."),
 intended="Build the rule registry and review gate; confirm the applicable Nacha phase and obligations with counsel and each sponsor's ODFI.",
 prov_refs="UNB-XIN-BNK-002, CNV-PAY-001, RR-UNB-PAY-008-r1, UNB-ACC-035, UNB-CTL-005, UNB-XIN-CLM-004",
 statement="Planned: a versioned fraud monitoring program per originating sponsor, aligned to the Nacha risk-based fraud monitoring amendments, is a precondition for enabling ACH. Not implemented; no rail is live and counsel has not confirmed the applicable obligations.",
 controls=["ECTL-FRD-010", "ECTL-FRD-011"], evidence=["EVR-FRD-010", "EVR-FRD-011"], policies=["SOC2-012", "SOC2-018"],
 requirements=["UNB-XIN-BNK-002", "CNV-PAY-001", "RR-UNB-PAY-008-r1", "UNB-ACC-035", "UNB-CTL-005", "UNB-XIN-CLM-004", "UNB-CTL-001"],
 impl_cost="medium", rec_cost="medium",
 open_questions=["Which Nacha fraud-monitoring phase and volume thresholds apply to Unbound as a TPSP and to each sponsor as Originator? CNV-PAY-001 cites Phase 2 effective 22 June 2026; verify against the current Nacha Operating Rules."],
 challenge=dict(
  customer_intent="Detect fraudulent ACH entries before or soon after they are sent, as the Nacha amendments expect.",
  adverse_outcome="Fraudulent credits sent under false pretenses; regulatory or network consequences for the ODFI and Originator.",
  conventional_control_effectiveness="Vendor-supplied fraud scores are opaque and hard to audit; rule-only programs miss novel patterns.",
  legally_required="Not statutory. Nacha Operating Rules bind participants contractually; the 2026 amendments require risk-based processes to identify entries initiated under false pretenses.",
  contractually_required="Yes for Originators and TPSPs through ODFI agreements.",
  historical_convention="Bank-side monitoring only, with little Originator-side control.",
  architectural_elimination="Destination evidence and cooling-off (CNV-PAY-002) remove the most common false-pretenses pattern (bank-change fraud) before monitoring is needed.",
  automatic_enforcement="Program review gate blocks origination when stale.",
  continuous_evidence="Rule versions, alerts, dispositions and outcome metrics.",
  stronger_alternative="Preventive destination controls plus a transparent, versioned rule program, with ML signals as advisory inputs only.",
  alternative_verifiable="Yes; rules and dispositions are auditable.",
  customer_acceptance_likelihood="Likely for sponsors and ODFIs; some may expect a named vendor fraud tool.",
  invalidating_conditions="Rules not tuned to sponsor patterns; alert fatigue.",
  conventional_cost="Medium recurring vendor fees.", alternative_cost="Medium build and tuning.",
  alternative_risks="Lower detection of novel patterns without ML.",
  supporting_arguments=["Explainable and auditable.", "Prevention before detection."],
  opposing_arguments=["ODFIs may expect specific tooling or data sharing.", "Rule programs require ongoing tuning staff."],
  technical_effectiveness="equivalent", institutional_acceptance="likely"),
 questions=[
  Q("How do you comply with the Nacha 2026 risk-based fraud monitoring requirements in your role in our ACH payments?",
    "nacha-fraud-monitoring", "ODFIs must confirm that originators and service providers monitor for fraud.", "Entries initiated under false pretenses go undetected.",
    [D(NFM), D(NACHA), D(U)], "contractual-common", "critical", authority="Nacha (private rules; enforced through ODFI agreements)",
    industries=["banking", "donor-advised-funds", "financial-services"]),
  Q("What rules or models do you use to detect anomalous payments, such as the first payment to a new account or an unusually large amount for a recipient?",
    "anomaly-detection", "Specific detection logic matters more than claims.", "Fraudulent payments that look ordinary in isolation.",
    [D(U), S(NFM)], "customer-preference", "high", reqs=["UNB-XIN-BNK-002", "UNB-ACC-035"]),
  Q("How often is your fraud monitoring program reviewed and updated, and what happens if the review lapses?",
    "program-governance", "Stale programs miss evolving fraud.", "Outdated rules.", [D(U), S(NFM)], "contractual-common", "medium",
    reqs=["UNB-XIN-BNK-002"]),
  Q("Who can see suspected fraud investigations, and how do you prevent tipping off the subject or exposing investigation details to support staff or AI assistants?",
    "investigation-confidentiality", "Leakage compromises investigations.", "Tipping off or defamation.",
    [D(U)], "customer-preference", "medium", reqs=["UNB-XIN-CLM-004"]),
  Q("Can an AI or statistical fraud score automatically clear a flagged payment?",
    "anomaly-detection", "Model-only clearance is a control gap.", "Fraud released by a model false negative.",
    [D(U), S("SRC-SR-11-7")], "customer-preference", "high", reqs=["UNB-CTL-001", "UNB-CTL-005", "UNB-ACC-035"]),
 ]),
]

controls = [
 C("Phishing-resistant authentication with command-bound step-up", "Require AAL3-grade authenticators for privileged roles and a fresh step-up bound to the specific high-risk command.",
   "preventive-structural", "L3-restricted-interface", ["Unbound identity and authorization component (specified, not built)"], ["EVR-FRD-001"],
   related=["UNB-SCTRL-005", "UNB-CTRL-004"], policies=["SEC-AUTH-001"], cwe=["CWE-308", "CWE-306"], refs=[D("SRC-NIST-SP800-63-4"), S("SRC-FFIEC-AUTH-GUIDANCE-2021")]),
 C("Credential-change cooling-off and prior-channel notice", "After authority-relevant credential changes, impose cooling-off, notify the prior channel and require sponsor-direct confirmation for new recipients during the window.",
   "preventive-structural", "L3-restricted-interface", ["Unbound identity component (specified, not built)"], ["EVR-FRD-002"]),
 C("Destination evidence release gate", "Block release to any destination lacking the rail's required evidence combination, cooling-off completion and notices on old and new verified channels.",
   "preventive-gate", "L3-restricted-interface", ["Unbound payment component (specified, not built)"], ["EVR-FRD-003"],
   related=["UNB-SCTRL-020", "UNB-CTRL-031", "UNB-CTRL-032"], cwe=["CWE-345"]),
 C("No unstructured-instruction channel for payments or payee changes", "Payment instructions, approvals and payee changes exist only as authenticated platform commands; no import, email or document ingestion path can create them.",
   "preventive-structural", "L1-eliminated-in-scope", ["Unbound command catalog (specified, not built)"], ["EVR-FRD-004"],
   notes="Scope: the Unbound application and its integrations. Does not cover sponsor bank portals or sponsor staff acting outside Unbound; TVR-PAY-004 addresses those through entitlement limits."),
 C("Bank-acknowledged positive pay before check release", "Hold checks until the bank acknowledges issue data; exceptions default to Return; Pay decisions require a non-issuer with evidence; voids acknowledged before reissue.",
   "preventive-gate", "L3-restricted-interface", ["Unbound check rail adapter (specified, not built)", "Sponsor bank positive pay service (external)"], ["EVR-FRD-005"]),
 C("Daily unmatched-debit detection with protective hold", "Match every debit on linked sponsor accounts to one authorized instruction or expected class; unmatched debits open an incident within one hour and hold releases.",
   "detective-automated", "L9-runtime-monitored", ["Unbound bank feed adapter and monitoring (specified, not built)"], ["EVR-FRD-006"],
   related=["UNB-CTRL-047"]),
 C("Collusion analytics, enforced leave and external register matching", "Cross-role anomaly analytics, enforced leave or rotation where staffed, daily custody and IdP admin action matching, and bank portal entitlement reviews.",
   "detective-automated", "L9-runtime-monitored", ["Unbound monitoring (specified, not built)"], ["EVR-FRD-007"],
   refs=[S("SRC-COSO-2013", "Principle 8")], residual=["Low-and-slow collusion"]),
 C("Identity proofing and provisional availability of reversible contributions", "Proof donor identity at a risk-based level and keep reversible contributions provisional with per-donor exposure caps until return windows pass.",
   "preventive-structural", "L3-restricted-interface", ["Unbound contributions component (specified, not built)", "Identity verification provider (not selected)"], ["EVR-FRD-008"],
   related=["UNB-SCTRL-031", "UNB-CTRL-052"], refs=[S("SRC-NIST-SP800-63-4")]),
 C("Charity impersonation, duplicate grant and related-party signal routing", "Generate evidence-based fraud signals and route matching grants to human review and protective holds; signals cannot auto-clear or auto-deny.",
   "detective-automated", "L6-automated-analysis", ["Unbound charity and grants components (specified, not built)"], ["EVR-FRD-009"],
   related=["UNB-SCTRL-010", "UNB-SCTRL-016"]),
 C("Versioned fraud monitoring rule program with review gate", "Maintain versioned fraud rules with owners and outcome metrics per originating sponsor; block new ACH origination when the annual review lapses.",
   "preventive-gate", "L9-runtime-monitored", ["Unbound fraud monitoring component (specified, not built)"], ["EVR-FRD-010"],
   refs=[D("SRC-NACHA-FRAUD-MONITORING-2026")]),
 C("Restricted-investigation case access class", "Fraud, account takeover and sanctions potential-match cases are visible only to investigation roles, excluded from search, timelines and AI context, with investigator and decision-maker separated.",
   "preventive-structural", "L3-restricted-interface", ["Unbound case management (specified, not built)"], ["EVR-FRD-011"],
   policies=["SEC-AUTH-001"], cwe=["CWE-200"]),
]

evidence = [
 E("Step-up events bound to commands", "Authenticator type, assurance level, authentication age and the command ID each step-up authorized, including rejections.", NOT_ASSIGNED.format("Unbound identity component"), "event-driven-automated", "per-event"),
 E("Credential change and notice records", "Credential or recovery changes, cooling-off windows, prior-channel notices and confirmations.", NOT_ASSIGNED.format("Unbound identity component"), "event-driven-automated", "per-event"),
 E("Destination evidence records", "Per destination the evidence types, callback contact source and verification date, cooling-off and notices.", NOT_ASSIGNED.format("Unbound payment component"), "event-driven-automated", "per-event"),
 E("Command catalog channel attestation", "Generated listing of every command that can create a payee change or payment and its permitted channels, compared with the approved baseline on each release.", NOT_ASSIGNED.format("Unbound build pipeline"), "event-driven-automated", "per-event", disclosure="nda"),
 E("Positive pay acknowledgments and exception decisions", "Issue file acknowledgments, exception items, decisions, deciders and evidence.", NOT_ASSIGNED.format("Unbound check rail adapter"), "event-driven-automated", "per-event"),
 E("Unmatched debit incidents", "Daily match results per account and incidents for unmatched debits with classification.", NOT_ASSIGNED.format("Unbound bank feed adapter"), "periodic-automated", "P1D"),
 E("Collusion analytics and entitlement review results", "Alerts with dispositions, leave or rotation records, and bank portal entitlement reviews.", NOT_ASSIGNED.format("Unbound monitoring"), "periodic-automated", "P90D"),
 E("Identity proofing and exposure records", "Proofing level achieved per donor, step-up outcomes, provisional amounts and exposure cap computations.", NOT_ASSIGNED.format("Unbound contributions component"), "event-driven-automated", "per-event"),
 E("Fraud signal routing cases", "Signals raised, routing, human dispositions and holds.", NOT_ASSIGNED.format("Unbound charity and grants components"), "event-driven-automated", "per-event"),
 E("Fraud monitoring program register and annual review", "Rule versions, owners, rationale, outcome metrics and the completed annual review record.", NOT_ASSIGNED.format("Unbound fraud monitoring component"), "periodic-manual", "P1Y"),
 E("Investigation case access logs", "Access attempts to restricted-investigation cases with allow or deny decisions.", NOT_ASSIGNED.format("Unbound case management"), "event-driven-automated", "per-event", disclosure="internal"),
]
