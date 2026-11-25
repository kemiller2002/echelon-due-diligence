from dafcommon import *

FI = ["donor-advised-funds", "nonprofit", "banking", "wealth-management"]
N63 = lambda b="directly-documented": S("SRC-NIST-SP800-63-4", rel="informed-by", basis=b)
units = []

u = AU("proofing", "Donor and advisor identity proofing",
    "Identity proofing is risk-based: core attributes are validated against authoritative sources, the funding account "
    "owner is matched, and a validated address or phone is confirmed; failure or elevated risk steps up to document and "
    "selfie or a non-biometric live-video alternative. Entities are verified by registration and signatory authority. "
    "Knowledge-based verification is never used for proofing. Accessible alternatives (mailed code, outbound call to a "
    "verified number, assisted captioned video, in-person or notarized verification) each reach a defined assurance "
    "level.",
    "Proofing per CNV-PLT-003, accessible assurance per CNV-PLT-011, onboarding per UNB-PART-007, recovery per REQ-X-072.",
    "donors would be identity-proofed by risk-based methods without knowledge-based questions.",
    ["CNV-PLT-003", "CNV-PLT-011", "UNB-PART-007", "REQ-X-072"], impl="medium", rec="medium",
    challenge=CH(
        "Sponsors want to know donors are who they claim to be, to prevent fraud and misattributed gifts.",
        "Impostor accounts used to redirect grants or launder funds.",
        "Knowledge-based questions are defeated by breached data and social media; they provide little assurance.",
        "DAF sponsors that are public charities are generally not subject to customer identification program rules; bank-affiliated sponsors may apply their affiliate's standards by policy.",
        "Bank and wealth-manager partners may contractually require specific identity verification.",
        "Knowledge-based verification and manual document review.",
        "Not eliminable.",
        "Risk-based validation with funding account owner match and step-up.",
        "Proofing evidence per person with assurance level.",
        "Attribute validation plus account owner match, stepping up to document and liveness or live video.",
        "Yes, from proofing records.",
        "Likely; aligns with current NIST guidance.",
        "Synthetic identities with real funding accounts may pass; biometric steps raise privacy and accessibility concerns.",
        "Low cost, low assurance.", "Medium per-check vendor cost.",
        "Vendor dependence for document and liveness checks; exclusion of people without documents.",
        ["Removes a weak, easily defeated method", "Provides accessible alternatives"],
        ["Higher friction for donors", "Per-check costs"],
        "stronger", "likely"),
    controls=[CTL("Risk-based identity proofing with prohibited knowledge-based verification",
        "Establish donor identity to a defined assurance level using validated attributes and owner match, never KBA.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-019", "UNB-CTRL-005"],
        fw=[S("SRC-NIST-SP800-63-4")])],
    evrs=[EVR("Identity proofing records",
        "Per-person proofing method, attributes validated, owner match result and assurance level achieved.",
        disclosure="internal", prov=["party id", "method", "attributes validated", "owner match", "assurance level", "verifier", "time"])])
u["questions"] = [
    Q("proofing-method", "How does the platform verify the identity of new donors and advisors?",
      "Sponsors must know who controls each fund.",
      "Impostor or synthetic identities open funds.",
      [N63(), UNB()], imp="critical", ind=FI,
      alts=["Do you perform KYC on donors?", "What identity assurance level do donor accounts reach?"]),
    Q("kba", "Does the platform rely on knowledge-based questions for identity verification or account recovery?",
      "KBA is widely considered weak.",
      "Account opening or takeover using breached personal data.",
      [N63(), UNB()], imp="high"),
    Q("entity-donors", "How are corporate, trust and foundation donors verified, including the authority of the individual acting for them?",
      "Entity donors act through signatories.",
      "Unauthorized individuals act for an entity.",
      [UNB(), S("SRC-FINCEN-CDD-RULE")], imp="medium", ind=FI),
    Q("funding-account-match", "Does the platform confirm that a donor owns the bank or brokerage account funding their contributions?",
      "Ownership mismatch signals fraud.",
      "Contributions from stolen or third-party accounts.",
      [UNB(), S("SRC-NACHA-FRAUD-MONITORING-2026")], imp="medium"),
    Q("accessible-verification", "What alternatives exist for donors who cannot complete digital identity verification, for example due to disability or lack of documents?",
      "Verification must not exclude donors.",
      "Discrimination claims and lost donors.",
      [UNB(), S("SRC-ADA"), N63("reasonably-inferred")], cls="legal-regulatory", imp="medium", auth="DOJ (ADA)",
      note="ADA applicability to a given sponsor's digital services depends on the sponsor's status; classification reflects the sponsor's potential obligation."),
]
units.append(u)

u = AU("ato", "Donor account takeover protection and recovery",
    "Donor accounts support phishing-resistant authenticators (passkeys or security keys) with device-bound options; a "
    "synced passkey alone is insufficient to add a new grant recipient. Any change to a verified contact channel "
    "notifies the previous channel with a self-service revert link and, for a sponsor-set period (default 72 hours), "
    "holds successor, beneficiary and authority changes and grant recommendations above a threshold for confirmation. "
    "Phone and support interactions reach only defined contact assurance levels, recovery requires identity-proofed "
    "paths, and suspected takeover cases are handled as restricted investigations.",
    "Contact change hold per CNV-PLT-011, recipient novelty per TVR-SEC-010, assurance levels per CNV-PLT-003, cases per UNB-XIN-CLM-004.",
    "donor accounts would use phishing-resistant authentication with holds after contact changes and identity-proofed recovery.",
    ["CNV-PLT-011", "TVR-SEC-010", "CNV-PLT-003", "UNB-XIN-CLM-004", "REQ-X-072", "UNB-RCN-WF-013"],
    policies=["SEC-AUTH-001"], mech="continuous-automated", impl="medium", rec="medium",
    controls=[CTL("Contact-change notification with protective hold",
        "Notify the prior channel on contact changes and hold sensitive actions during the sponsor-set window.",
        "preventive-structural", "L3-restricted-interface", ext=["UNB-CTRL-019"],
        fw=[S("SRC-FFIEC-AUTH-GUIDANCE-2021")]),
        CTL("Phishing-resistant authentication for donors and step-up for new recipients",
        "Require phishing-resistant or device-bound authentication for high-risk actions such as new recipients.",
        "preventive-gate", "L3-restricted-interface", fw=[S("SRC-NIST-SP800-63-4")], ext=["UNB-CTRL-004"])],
    evrs=[EVR("Authentication, contact change and hold events",
        "Authenticator types used, contact changes, notifications, holds and reverts per account.",
        mech="continuous-automated", disclosure="internal",
        prov=["party id", "event", "authenticator type", "old channel notified", "hold id", "revert", "time"])])
u["questions"] = [
    Q("donor-mfa", "What authentication options do donors have, and are phishing-resistant methods such as passkeys or security keys supported or required?",
      "Donor accounts control charitable grants worth significant sums.",
      "Credential phishing leads to fraudulent grants.",
      [N63(), S("SRC-FFIEC-AUTH-GUIDANCE-2021")], imp="critical", ind=FI),
    Q("contact-change-protection", "When a donor's email or phone changes, how is the donor alerted and what actions are held?",
      "Contact changes precede most account takeovers.",
      "Attacker changes contact details then redirects grants.",
      [UNB(), S("SRC-SEC-REG-S-ID")], imp="high", ind=FI),
    Q("new-recipient-stepup", "Is additional verification required before a donor recommends a grant to a charity they have never supported?",
      "New recipients are the main payoff for takeover.",
      "Grants to attacker-controlled charities.",
      [UNB()], imp="high"),
    Q("support-social-engineering", "How do support staff verify callers before discussing or changing a fund, and what can be done by phone?",
      "Call centers are a social engineering target.",
      "Account changes by impostor callers.",
      [UNB(), N63("reasonably-inferred")], imp="high"),
    Q("account-recovery", "How does a donor recover access after losing credentials, and how is recovery protected from attackers?",
      "Recovery is the weakest link in authentication.",
      "Takeover through recovery flows.",
      [N63(), UNB()], imp="high"),
    Q("ato-detection", "How does the platform detect and respond to suspected account takeover?",
      "Detection limits damage.",
      "Undetected takeover until grants are paid.",
      [UNB(), S("SRC-NIST-CSF-2.0", "DE.CM-03")], imp="medium"),
]
units.append(u)

u = AU("privacy-prefs", "Donor anonymity and privacy preferences across channels",
    "Anonymity, recognition and communication elections are authority facts owned by the identity and delegation "
    "capability, stored append-only with effective and recorded times. Every outbound use (grant letters, sponsor annual "
    "reports, partner views, statements) derives disclosure from the current election, and notifications re-read the "
    "election immediately before external send. Other participants on a fund see only what the grantor's scope allows.",
    "Authority facts per UNB-XIN-EVA-014, send-time re-check per UNB-XIN-EVA-015, naming per ADM-013, privacy gap per UNB-GAP-021.",
    "privacy elections would be enforced at the moment of every outbound disclosure.",
    ["ADM-013", "UNB-GRANT-025", "UNB-XIN-EVA-014", "UNB-XIN-EVA-015", "UNB-GAP-021", "UNB-PART-006"], impl="low",
    controls=[CTL("Election-derived disclosure at every outbound channel",
        "Ensure no outbound channel discloses donor identity or giving contrary to the current election.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-085"], fw=[S("SRC-AICPA-TSC", "P6.1")])],
    evrs=[EVR("Privacy election history and disclosure log",
        "Election versions and, for each outbound disclosure, the election version applied.",
        prov=["party id", "election type", "version", "channel", "message id", "time"])])
u["questions"] = [
    Q("fund-anonymity", "Can a donor make the fund itself anonymous, use a fund name instead of a personal name, or appear differently to different audiences?",
      "Donor privacy preferences are central to DAF appeal.",
      "Unwanted public association with causes.",
      [UNB()], cls="customer-preference", imp="high"),
    Q("annual-report-listing", "Are donors listed in sponsor annual reports or donor rolls only with their consent?",
      "Sponsor publications are a disclosure channel.",
      "Publishing names against preference.",
      [UNB(), S("SRC-AICPA-TSC", "P2.1")], cls="customer-preference", imp="medium"),
    Q("co-participant-visibility", "What can co-advisors and family participants see about each other's grants and contributions?",
      "Family members may not share preferences.",
      "Intra-family privacy breaches.",
      [UNB()], cls="customer-preference", imp="medium"),
    Q("preference-in-partner-channels", "Are anonymity and privacy preferences honored when donors interact through a partner, advisor portal or embedded widget?",
      "Partner channels must apply the same rules.",
      "Partners display or log data contrary to preferences.",
      [UNB()], imp="high"),
]
units.append(u)

u = AU("advisor-delegation", "Professional advisor access delegation and firm changes",
    "Donors may delegate scoped, revocable, effective-dated access to professional advisors (view, investment "
    "recommendation, or grant preparation without submission). A professional-advisor relationship is scoped to the pair "
    "of individual advisor and firm; when the firm or a verified HR or SCIM feed reports the advisor's departure, or the "
    "advisor reports a new firm, the delegated access is suspended pending donor reconfirmation. Partner identity "
    "mapping uses a permanent identifier, never an email, and mapping changes require dual control and donor notice. "
    "Agents under a power of attorney act only with verified authority.",
    "Delegation per UNB-ADV-001, advisor-firm pair per UNB-XIN-CRM-007, identity mapping per AUTH-I8, POA per CNV-ENT-001.",
    "advisor access would be scoped to the advisor and firm, revocable, and suspended on firm change.",
    ["UNB-ADV-001", "UNB-ADV-002", "UNB-XIN-CRM-007", "AUTH-I8", "UNB-PART-006", "UNB-CUST-014", "CNV-ENT-001"],
    policies=["SEC-AUTH-001"], impl="medium",
    controls=[CTL("Advisor-firm pair scoping with suspension on departure",
        "Suspend delegated advisor access when the advisor leaves the firm the delegation names.",
        "preventive-structural", "L3-restricted-interface", ext=["UNB-CTRL-019", "UNB-CTRL-020"],
        fw=[S("SRC-NIST-SP800-53-R5", "AC-2")])],
    evrs=[EVR("Advisor delegation lifecycle records",
        "Delegations granted, scope, firm, departure signals, suspensions and reconfirmations.",
        prov=["fund id", "advisor id", "firm id", "scope", "event", "source of signal", "time"])])
u["questions"] = [
    Q("advisor-access", "Can donors give their financial advisor, attorney or accountant access to their fund, and with what scopes?",
      "Wealth-management channels depend on advisor access.",
      "Advisors receive more access than intended.",
      [UNB(), S("SRC-FINRA-RN-21-29")], imp="high", ind=FI),
    Q("advisor-firm-change", "What happens to an advisor's access when they leave their firm or join another?",
      "Departing advisors should not retain access through old firm relationships.",
      "Former advisors keep access to donor data.",
      [UNB(), S("SRC-SEC-REG-SP-2024")], imp="high", ind=FI),
    Q("advisor-identity-mapping", "How does the platform map advisor identities from a partner's systems, and what prevents a mapping error from exposing another donor's fund?",
      "Identity mapping errors cause cross-donor exposure.",
      "Wrong advisor linked to a fund.",
      [UNB(), S("SRC-OWASP-API-TOP10-2023", "API1:2023")], imp="high", ind=FI),
    Q("power-of-attorney", "How does the platform handle agents acting under a power of attorney or guardianship for an incapacitated donor?",
      "Incapacity is common among older donors.",
      "Unverified agents act on funds, or valid agents are blocked.",
      [UNB()], imp="medium"),
    Q("advisor-revocation", "Can the donor see all delegated access and revoke it immediately?",
      "Donors control their delegations.",
      "Forgotten delegations remain active.",
      [UNB()], imp="medium"),
]
units.append(u)

u = AU("communications", "Donor communications classification, consent and accuracy",
    "Every message template is classified (commercial, transactional or relationship, mandatory legal, security) before "
    "activation, with a declared sender legal entity; promotional email in white-label programs is sent with the sponsor "
    "as sender, opt-outs are honored within 10 business days across all platforms sending for that sender, and texts or "
    "automated calls require prior express written consent naming the sponsor. Each notification records the fact and "
    "version it describes and is re-validated against the current fact and the recipient's consent state immediately "
    "before sending. Statements are generated for every configured period.",
    "Classification per CNV-PLT-001, UNB-XIN-CRM-003, UNB-XIN-REG-003; send-time validation per UNB-XIN-EVA-015; statements per CNV-PLT-005 and REQ-X-032.",
    "donor messages would be legally classified, consent-checked and re-validated at send time.",
    ["CNV-PLT-001", "UNB-XIN-CRM-003", "UNB-XIN-REG-003", "UNB-XIN-EVA-015", "CNV-PLT-005", "REQ-X-032", "REQ-X-027"],
    impl="medium",
    oq=["CAN-SPAM (16 CFR 316) and TCPA/FCC rules are cited in requirements but not seeded as sources."],
    controls=[CTL("Template legal classification gate",
        "Block activation of any message template without a legal classification and sender entity.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-061"]),
        CTL("Send-time fact and consent re-validation",
        "Suppress messages whose underlying fact was superseded or whose recipient consent changed.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-062"])],
    evrs=[EVR("Message classification and delivery log",
        "Template classifications, consent state at send, suppression decisions and delivery outcomes.",
        prov=["template id", "classification", "sender entity", "fact id and version", "consent state", "outcome", "time"])])
u["questions"] = [
    Q("message-classification", "How are donor emails and texts classified as commercial or transactional, and who is the legal sender in white-label programs?",
      "Commercial messaging law applies differently by class and sender.",
      "Regulatory violations and sponsor liability for vendor-sent messages.",
      [UNB()], cls="legal-regulatory", imp="medium", auth="FTC; FCC",
      oq=["Seed CAN-SPAM and TCPA sources."]),
    Q("opt-outs", "How are opt-outs honored across all channels and platforms sending on the sponsor's behalf?",
      "Opt-outs must be honored consistently.",
      "Continued messages after opt-out.",
      [UNB()], cls="legal-regulatory", imp="medium", auth="FTC; FCC"),
    Q("sms-consent", "What consent is collected before sending texts or automated calls to donors?",
      "Text messaging consent rules are strict.",
      "Statutory damages for unconsented texts.",
      [UNB()], cls="legal-regulatory", imp="medium", auth="FCC"),
    Q("message-accuracy", "How does the platform avoid sending outdated messages, such as a 'grant paid' notice for a payment that was returned?",
      "Inaccurate messages mislead donors.",
      "Donors rely on false status information.",
      [UNB()], imp="medium"),
    Q("statements", "What statements do donors receive, how often, and can the sponsor configure content and delivery?",
      "Statements are core donor communications.",
      "Missing or inaccurate statements.",
      [UNB()], cls="customer-preference", imp="medium"),
]
units.append(u)

u = AU("data-use", "Donor data use limits, secondary use, AI training and privacy rights",
    "Donor data is processed only to provide services for the sponsor that controls it. The vendor does not sell donor "
    "data, does not use it for its own marketing, and does not use one sponsor's donor data to train models or benefit "
    "other sponsors except as the sponsor contractually authorizes. Cross-sponsor personal data exposure is prevented by "
    "tenant boundaries, and shared data requires separate rights and provenance. Privacy requests are fulfilled through "
    "reviewed procedures compatible with append-only records (for example cryptographic erasure or redaction of personal "
    "fields while preserving financial integrity) and legal retention.",
    "Purpose limitation per UNB-API-005, UNB-CHAR-035/037 and UNB-TEN-007; privacy procedures per UNB-DATA-007 and UNB-GAP-021.",
    "donor data would be used only for the sponsor's services, never sold or used to train models without sponsor authorization.",
    ["UNB-DATA-007", "UNB-GAP-021", "UNB-API-005", "UNB-CHAR-037", "UNB-TEN-007", "CNV-TEN-001", "UNB-DATA-011"],
    policies=["SEC-AUTH-001"], status="proposed-target-state", impl="medium", rec="low", auto="partial",
    oq=["Echelon has no privacy policy, data processing agreement template or AI training policy; all are needed before sales.",
        "Applicability of GLBA, CCPA and other state privacy laws to nonprofit sponsors and to Echelon as service provider needs counsel review."],
    controls=[CTL("Purpose-limited data access and tenant boundary",
        "Prevent use of donor data outside the controlling sponsor's purposes and tenant.",
        "preventive-structural", "L3-restricted-interface", ext=["UNB-CTRL-085", "UNB-CTRL-007"],
        fw=[S("SRC-AICPA-TSC", "P4.1")], policies=["SEC-AUTH-001"], cwe=["CWE-359"]),
        CTL("Contractual prohibition of sale, own-marketing and unauthorized model training",
        "Commit contractually that donor data is not sold, used for vendor marketing or used to train models without sponsor authorization.",
        "administrative", "L10-external-or-manual", ext=["UNB-CTRL-087"])],
    evrs=[EVR("Data use register and privacy request log",
        "Register of processing purposes and data flows per sponsor, plus privacy requests and their resolution.",
        mech="event-driven-automated", disclosure="customer-only",
        prov=["sponsor id", "purpose", "data categories", "recipient", "request id", "resolution", "time"])])
u["questions"] = [
    Q("secondary-use", "Does the vendor use donor data for any purpose other than providing services to the sponsor, including its own marketing or analytics?",
      "Donor data belongs to the sponsor relationship.",
      "Unauthorized secondary use harms donors and sponsor trust.",
      [S("SRC-AICPA-TSC", "P4.1"), S("SRC-GLBA-REG-P")], cls="contractual-common", imp="critical", ind=FI,
      alts=["Will you sell or share our donor data?"]),
    Q("ai-training", "Is donor or sponsor data used to train or fine-tune AI models, including vendor-wide models?",
      "AI training is a new form of secondary use.",
      "Donor data embedded in models available to others.",
      [S("SRC-NIST-AI-RMF-1.0"), S("SRC-NIST-PRIVACY-FW")], cls="customer-preference", imp="high"),
    Q("cross-sponsor-aggregation", "Does the vendor aggregate donor data across sponsors, for example to identify a donor with funds at several sponsors?",
      "Donors may not want sponsors to know of each other.",
      "Cross-sponsor profiling and disclosure.",
      [UNB()], imp="high"),
    Q("privacy-rights", "How are donor requests to access, correct or delete personal data handled, given that financial records must be retained and history is append-only?",
      "Privacy rights and record retention can conflict.",
      "Either unlawful deletion of records or failure to honor rights.",
      [S("SRC-CCPA-CPRA"), S("SRC-US-STATE-PRIVACY-LAWS"), UNB()], cls="legal-regulatory", imp="medium", jur=["US-states"], auth="state privacy regulators",
      note="Many state privacy laws exempt nonprofits; applicability depends on the sponsor and the vendor's role."),
    Q("data-sharing-partners", "With which third parties (processors, partners, advisors) is donor data shared, and can the sponsor approve or restrict them?",
      "Sponsors must control downstream sharing.",
      "Uncontrolled disclosure to subprocessors or partners.",
      [S("SRC-INTERAGENCY-TPRM-2023"), S("SRC-AICPA-TSC", "P6.1")], cls="contractual-common", imp="high", ind=FI),
]
units.append(u)

u = AU("deceased", "Deceased and incapacitated donor handling",
    "On credible notice of a donor's death the platform holds new actions by that person; on verification it suspends, "
    "in one transaction, all rights, sessions and delegated agent principals deriving from that person. Valid "
    "sponsor-approved unpaid grants continue unless sponsor policy says otherwise, future instructions are suspended until "
    "successor authority is verified, marketing to the deceased stops, and executors or estate representatives receive "
    "only the information the sponsor's policy permits.",
    "Death handling per CNV-ENT-001, UNB-RCN-ENT-004, REQ-X-008, ADM-022 and UNB-WF-013.",
    "a verified death would suspend the donor's access immediately while honoring approved grants and stopping marketing.",
    ["CNV-ENT-001", "UNB-RCN-ENT-004", "REQ-X-008", "ADM-022", "UNB-WF-013", "UNB-GAP-015"], impl="medium", auto="partial",
    oq=["Executor and estate representative information access policy is not specified."],
    controls=[CTL("Hold on death notice and atomic suspension on verification",
        "Prevent actions by or in the name of a deceased donor after credible notice and verification.",
        "preventive-structural", "L3-restricted-interface", ext=["UNB-CTRL-022"])],
    evrs=[EVR("Death notice and suspension records",
        "Notice source, holds, verification evidence, suspensions and communications changes.",
        disclosure="internal", prov=["party id", "notice source", "hold id", "verification evidence", "suspended principals", "time"])])
u["questions"] = [
    Q("death-notice", "What happens when the sponsor learns a donor has died, before formal verification?",
      "Fraudsters exploit the period after death.",
      "Actions taken in a deceased donor's name.",
      [UNB()], imp="high"),
    Q("session-suspension", "Are a deceased donor's sessions, tokens and any agents acting for them suspended immediately on verification?",
      "Lingering sessions are an abuse path.",
      "Use of a deceased donor's active session.",
      [UNB()], imp="high"),
    Q("executor-access", "What information can an executor or estate representative obtain about a deceased donor's fund?",
      "Executors often request information; the fund is not estate property.",
      "Over-disclosure or confusion about ownership.",
      [UNB()], cls="customer-preference", imp="medium"),
    Q("stop-marketing", "Does the platform stop marketing and routine communications to deceased donors?",
      "Messages to deceased donors cause distress.",
      "Reputational harm.",
      [UNB()], cls="customer-preference", imp="low"),
]
units.append(u)
