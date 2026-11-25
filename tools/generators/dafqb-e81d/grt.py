from dafcommon import *

units = []

u = AU("intake", "Grant recommendation intake, affirmation and duplicate detection",
    "A grant recommendation is a typed request that captures recommender, fund, recipient identity, purpose, amount, "
    "timing, restrictions and recognition preference, together with an affirmation evidence record (presented "
    "disclosure text and hash, the donor's no-benefit and no-pledge certifications, channel, time and idempotency key). "
    "Submission never creates an entitlement or moves money. Duplicate and replayed submissions are handled "
    "idempotently, and suspicious repeated or split recommendations are flagged across channels.",
    "Recommendation command per UNB-GRANT-001/002/029 with AffirmationEvidence per UNB-RCN-GRT-010.",
    "recommendations would capture structured intent with recorded donor certifications and idempotent duplicate handling.",
    ["UNB-GRANT-001", "UNB-GRANT-002", "UNB-GRANT-029", "UNB-RCN-GRT-010", "UNB-DON-001", "REQ-X-026", "UNB-API-004"],
    policies=["SEC-DATA-001"], impl="medium",
    controls=[CTL("Affirmation evidence required on submission",
        "Reject any recommendation submission lacking a complete affirmation evidence record bound to the presented disclosure version.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-025"], fw=[S("SRC-AICPA-TSC", "PI1.2")]),
        CTL("Idempotent submission and cross-channel duplicate flag",
        "Prevent double recommendations from retries and flag repeated or split recommendations across channels.",
        "preventive-structural", "L3-restricted-interface", cwe=["CWE-837"])],
    evrs=[EVR("Recommendation and affirmation records",
        "Each recommendation with its affirmation evidence, idempotency key and duplicate flags.",
        prov=["recommendation id", "fund id", "recommender", "disclosure version hash", "certifications", "channel", "idempotency key", "time"])])
u["questions"] = [
    Q("captured-data", "What information is captured with each grant recommendation (purpose, restrictions, timing, recognition preference), and what is required versus optional?",
      "Sponsor needs enough information to evaluate and pay grants correctly.",
      "Incomplete recommendations cause delays or misdirected grants.",
      [UNB()], imp="medium"),
    Q("donor-certifications", "Does the platform capture the donor's certification that no more than incidental benefit results and that the grant does not satisfy a pledge, and is the exact wording presented recorded?",
      "Certifications support the sponsor's diligence on prohibited benefits and pledges.",
      "Sponsor cannot show the donor attested to the terms in force.",
      [S("SRC-IRC-4967", rel="informed-by"), UNB()], cls="industry-convention", imp="high", auth="IRS",
      alts=["Do donors acknowledge grant terms each time they recommend a grant?"]),
    Q("duplicates", "How does the platform handle duplicate or replayed recommendations, and does it detect repeated or split recommendations that may evade thresholds?",
      "Duplicate payments and threshold evasion are common grant errors and fraud patterns.",
      "Double payment or evasion of review thresholds.",
      [UNB(), S("SRC-OWASP-API-TOP10-2023")], imp="high"),
    Q("unauthorized-recommender", "What prevents a person without current grant recommendation privileges on a fund from submitting a recommendation through any channel?",
      "Only authorized advisors may recommend.",
      "Grants recommended by revoked or unauthorized persons.",
      [UNB(), S("SRC-AICPA-TSC", "CC6.1")], imp="critical"),
    Q("recommendation-notes", "Can recommenders attach notes and exchange messages with sponsor staff about a recommendation, and are internal staff comments kept separate from donor-visible messages?",
      "Communication improves grant quality but internal deliberations must stay private.",
      "Internal compliance notes leak to donors.",
      [UNB()], cls="customer-preference", imp="low"),
]
units.append(u)

u = AU("approval", "Grant approval workflow, board-delegated policy approval and segregation of duties",
    "Approval authority derives from a recorded sponsor board or committee resolution. Until such a resolution adopts a "
    "version-pinned policy and names a delegate, deterministic policy only recommends and an accountable person decides. "
    "Once delegated, conforming items may be approved by policy under the delegate's authority, while exceptions and "
    "enhanced-review triggers route to qualified humans by amount, risk and relationship. The engine enforces segregation "
    "of duties, vendor staff and AI agents cannot hold approval authority, decision quality is checked by risk-stratified "
    "sampling, and approval atomically reserves the approved amount.",
    "Policy-delegation model per CNV-GRT-001, routing per UNB-GRANT-012 and CNV-GRT-011, authority per CNV-GOV-003/004/010, reservation per CNV-FIN-001.",
    "approvals would follow sponsor-adopted delegation, with policy-based approval only after a recorded board resolution.",
    ["CNV-GRT-001", "UNB-GRANT-012", "UNB-GRANT-013", "CNV-GRT-011", "CNV-GOV-003", "CNV-GOV-004", "CNV-GOV-010", "CNV-FIN-001", "UNB-AGT-002", "UNB-GRANT-030"],
    policies=["SEC-AUTH-001"], impl="high", rec="medium",
    challenge=CH(
        "Sponsors want every grant to be properly authorized and reviewed so that charitable assets are protected.",
        "An improper or fraudulent grant is paid; sponsor faces excise tax, loss or reputational harm.",
        "Human review of every routine grant to a verified public charity adds delay and fatigue; reviewers rubber-stamp high volumes, so marginal detection is low.",
        "No statute requires human review of each grant; the sponsor must exercise exclusive legal control, which board delegation can satisfy.",
        "Some sponsor policies and bank-affiliated sponsor procedures require dual human approval.",
        "Program officers or grant administrators approve each grant, often with a second approver above a threshold.",
        "Deterministic gates eliminate entire classes of ineligible grants (revoked charities, natural persons, sanctioned recipients) before any human sees them.",
        "Board-adopted policy approves only conforming items; exceptions route to humans.",
        "Each approval records the policy version and delegation; sampling measures error rates with stated bounds.",
        "Deterministic gates plus delegated policy approval and risk-stratified sampling.",
        "Yes, via replay and sampling results; independent verification requires an external examination.",
        "Uncertain: national sponsors already use automation; community foundations and bank-affiliated sponsors may insist on human approval.",
        "If eligibility data is stale or the policy is mis-specified, automation approves errors at scale.",
        "High recurring staff cost.", "Medium build cost, low recurring cost.",
        "Systematic error propagation; regulators or auditors unfamiliar with policy approval may object.",
        ["Concentrates human attention on real risk", "Produces stronger evidence than signatures"],
        ["Errors scale with volume", "Institutional acceptance unproven", "Board must understand what it delegated"],
        "stronger", "uncertain"),
    controls=[CTL("Delegation-gated policy approval",
        "Permit policy-based approval only when a recorded sponsor resolution delegates authority for that policy version.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-025", "UNB-CTRL-027"],
        fw=[S("SRC-COSO-2013")]),
        CTL("Engine-enforced segregation of duties on grant approval",
        "Prevent the recommender, preparer or vendor or agent principal from approving the same grant.",
        "preventive-structural", "L2-type-system", ext=["UNB-CTRL-004"], fw=[S("SRC-NIST-SP800-53-R5", "AC-5")], policies=["SEC-AUTH-001"]),
        CTL("Risk-stratified sampling of approved grants",
        "Measure approval error rates with stated error bounds and report to the sponsor board.",
        "detective-manual", "L10-external-or-manual", ext=["UNB-CTRL-027"])],
    evrs=[EVR("Grant approval decision records",
        "Each approval with route, approver or policy version, delegation resolution reference, reservation id and sampling selection.",
        prov=["grant id", "route", "approver or policy version", "delegation reference", "reservation id", "sample id", "time"]),
        EVR("Approval sampling results report",
        "Periodic sampling results with error rates and bounds for sponsor board review.",
        mech="periodic-manual", fresh="P90D", fmt="Folio-rendered PDF and JSON", disclosure="customer-only")])
u["questions"] = [
    Q("approval-routing", "How are grant approvals routed by amount, risk, recipient type and relationship to the donor, and can the sponsor configure the thresholds?",
      "Sponsors need review proportional to risk.",
      "High-risk grants receive the same light review as routine ones.",
      [UNB()], imp="high"),
    Q("board-delegation", "If grants are approved automatically by policy, what records show that the sponsor's board delegated that authority and to whom?",
      "Automated approval must rest on legitimate sponsor authority.",
      "Grants approved without valid authority, undermining exclusive legal control.",
      [UNB(), S("SRC-IRC-4966", "§4966(d)(2)", "informed-by", "reasonably-inferred")], imp="critical",
      alts=["Who is the approving authority for auto-approved grants?"]),
    Q("segregation-of-duties", "How does the platform prevent the same person from recommending, preparing and approving a grant, and does this apply to sponsor staff who are also donors?",
      "Segregation of duties is a basic financial control.",
      "Self-approval of grants by staff-donors.",
      [UNB(), S("SRC-COSO-2013"), S("SRC-AICPA-TSC", "CC6.3")], imp="critical"),
    Q("ai-role", "What role do AI agents play in grant review, and what prevents an agent from approving, overriding a hold or releasing payment?",
      "Sponsors are wary of AI making fiduciary decisions.",
      "Opaque AI approvals or prompt-injected agents moving funds.",
      [UNB(), S("SRC-NIST-AI-RMF-1.0"), S("SRC-OWASP-AGENTIC-AI")], cls="customer-preference", imp="high", req=["UNB-AGT-003"]),
    Q("approval-quality", "How does the sponsor know that automatically approved or batch-approved grants were correct, and how are error rates measured?",
      "Delegated approval needs ongoing quality assurance.",
      "Systematic approval errors go unnoticed.",
      [UNB()], imp="high"),
    Q("reservation-at-approval", "When a grant is approved, is the amount reserved atomically so that later grants or fees cannot spend the same funds?",
      "Approved grants must be fundable.",
      "Overcommitment leaves approved grants unpaid.",
      [UNB(), S("SRC-AICPA-TSC", "PI1.3")], imp="high", req=["TVR-GR-001"]),
    Q("enhanced-review-triggers", "Which conditions trigger enhanced review (supporting organizations, fiscally sponsored projects, donor affiliation signals, grants large relative to recipient revenue)?",
      "Sponsors focus diligence on higher-risk grants.",
      "Risky grants pass routine review.",
      [UNB(), S("SRC-TREASURY-CHARITY-GUIDELINES")], imp="high"),
]
units.append(u)

u = AU("restrictions", "Grant purpose, restrictions, agreements and post-approval modification",
    "Grant purposes and restrictions are structured data evaluated against sponsor, program and fund policy in explicit "
    "precedence order. Restrictions that would deliver a benefit to the donor or name a foreign organization through an "
    "intermediary are blocked or routed for review. Grant agreements, milestones and reporting obligations are "
    "supported for conditional grants. Material modifications after approval (recipient, amount, purpose, timing, "
    "restrictions) require re-evaluation and human approval.",
    "Restriction evaluation per UNB-GRANT-010 and UNB-GRANT-024; modification control per UNB-GRANT-048; intermediary wording per CNV-GRT-008.",
    "grant restrictions would be structured, policy-checked and re-approved on material change.",
    ["UNB-GRANT-010", "UNB-GRANT-024", "UNB-GRANT-048", "CNV-GRT-008", "CNV-GRT-016"], impl="medium",
    controls=[CTL("Material modification re-approval gate",
        "Require re-evaluation and human approval when a material term of an approved grant changes.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-026"])],
    evrs=[EVR("Grant restriction and modification history",
        "Structured restrictions, policy evaluation results and every post-approval modification with re-approval.",
        prov=["grant id", "restriction terms", "policy precedence result", "modification", "re-approver", "time"])])
u["questions"] = [
    Q("supported-restrictions", "What kinds of grant restrictions can a donor request (program, project, capital, endowment, time-bound), and how are they communicated to the grantee?",
      "Donors want their intent honored; grantees need clear terms.",
      "Restrictions lost or miscommunicated.",
      [UNB()], cls="customer-preference", imp="medium"),
    Q("benefit-restrictions", "How does the platform block restrictions that would benefit the donor, such as earmarking for a named scholarship recipient or a relative's program?",
      "Restrictions can convert a grant into a prohibited benefit or taxable distribution.",
      "Earmarked grants that benefit donors or specific individuals.",
      [S("SRC-IRC-4967", rel="informed-by"), S("SRC-IRC-4966", "§4966(c)", "informed-by", "reasonably-inferred"), UNB()], cls="legal-regulatory", imp="high", auth="IRS"),
    Q("policy-precedence", "When donor intent, fund restrictions, program rules and sponsor policy conflict, which governs and how is that recorded?",
      "Precedence must be predictable and auditable.",
      "Inconsistent handling of conflicting restrictions.",
      [UNB()], imp="medium"),
    Q("post-approval-change", "How are material changes to an approved grant (recipient, amount, purpose, timing) controlled?",
      "Changes after approval are a known fraud vector.",
      "Approved grants redirected without review.",
      [UNB(), S("SRC-COSO-2013")], imp="high"),
    Q("conditional-grants", "Does the platform support conditional, milestone-based and multi-year grants with reporting requirements and conditional release?",
      "Larger sponsors make structured grants.",
      "Conditions tracked outside the system and missed.",
      [UNB()], cls="customer-preference", imp="low"),
]
units.append(u)

u = AU("recurring", "Recurring and scheduled grants with per-instance re-evaluation",
    "Each instance of a recurring or scheduled grant re-checks the template author's current authority, the recipient's "
    "eligibility and sanctions status, fund availability and current sponsor policy at execution, and reserves "
    "individually. Series are paused, not silently skipped, on failure; changes in purpose, class or eligibility require "
    "reconfirmation, and series affected by a recipient merger carry a notice-and-opt-out window.",
    "Per-instance checks per TVR-GR-005, TVR-GR-008 and UNB-GRANT-027; notice rules per CNV-GRT-010.",
    "each recurring grant instance would re-check authority, eligibility and funds before execution.",
    ["UNB-GRANT-003", "UNB-GRANT-027", "TVR-GR-005", "TVR-GR-008", "CNV-GRT-010", "REQ-X-008"], impl="medium",
    controls=[CTL("Per-instance re-evaluation of recurring grants",
        "Ensure each recurring instance passes authority, eligibility, sanctions and funding checks at execution time.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-025"])],
    evrs=[EVR("Recurring instance evaluation records",
        "Per-instance evaluation result, reservation, pause reason and notices.",
        prov=["series id", "instance id", "authority check", "eligibility check", "sanctions list version", "reservation id", "time"])])
u["questions"] = [
    Q("instance-rechecks", "Does each instance of a recurring grant re-verify recipient eligibility, sanctions status and the recommender's authority at the time of payment?",
      "Conditions change between setup and execution.",
      "Payments to revoked charities or under ended authority.",
      [UNB(), S("SRC-OFAC-COMPLIANCE-FRAMEWORK")], imp="critical"),
    Q("insufficient-funds", "What happens to a scheduled or recurring grant when the fund lacks sufficient available balance on the execution date?",
      "Donors and grantees need predictable behavior.",
      "Overdrafts or silently skipped grants.",
      [UNB()], imp="medium", req=["UNB-GEX-016"]),
    Q("advisor-removed", "If the advisor who set up a recurring grant loses privileges, does the series stop, continue or require reconfirmation?",
      "Authority must not outlive its grant.",
      "Grants continue under revoked authority.",
      [UNB()], imp="high"),
    Q("series-cancellation", "How can donors and sponsor staff pause, modify or cancel recurring and scheduled grants, and how is the grantee notified?",
      "Control over future grants is a core donor expectation.",
      "Unwanted payments continue.",
      [UNB()], cls="customer-preference", imp="medium"),
    Q("recipient-merger-recurring", "When a recurring grant's recipient merges or changes legal identity, how is the series handled?",
      "Mergers are common among charities.",
      "Payments to a dissolved entity or to an unvetted successor.",
      [UNB()], imp="medium"),
]
units.append(u)

u = AU("pledges-benefits", "Pledges, event benefits and other prohibited benefit scenarios",
    "Pledge handling is an explicit sponsor policy choice (Prohibited, NonBindingOnly, or conditions consistent with IRS "
    "Notice 2017-73 section 7). Embedded and API giving requests declare a typed host context (donation, event ticket, "
    "sponsorship, auction, membership with benefits), and benefit-bearing contexts are rejected or routed to the benefit "
    "gate. Grants are blocked to purposes that provide tuition, memberships with more than incidental benefits, or "
    "tickets, and bifurcated grants (DAF pays the charitable portion, donor pays the benefit) follow sponsor policy.",
    "Pledge policy per CNV-GRT-010; host context per UNB-RCN-GRT-012; benefit evaluation per UNB-GRANT-011.",
    "pledge and benefit rules would be sponsor-selected and enforced at recommendation and embedded checkout.",
    ["CNV-GRT-010", "UNB-RCN-GRT-012", "UNB-GRANT-011", "CNV-GRT-009", "UNB-LS-008"], impl="medium",
    oq=["IRS Notice 2017-73 is not a seeded source; bifurcated-grant handling policy needs counsel input."],
    controls=[CTL("Typed host context gate for embedded giving",
        "Reject or route to review any embedded or API giving request whose declared or detected context carries a benefit.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-025"])],
    evrs=[EVR("Benefit and pledge gate outcomes",
        "Recorded pledge policy choice per sponsor and per-request benefit gate decisions.",
        prov=["sponsor id", "pledge policy version", "request id", "host context", "gate outcome", "time"])])
u["questions"] = [
    Q("pledge-policy", "How does the platform handle a donor's pledge to a charity when the donor recommends a DAF grant to fulfill it?",
      "Using DAF assets to satisfy a legally binding personal pledge raises prohibited benefit concerns.",
      "Grants that relieve a donor's personal obligation.",
      [S("SRC-IRC-4967", rel="informed-by"), UNB()], cls="legal-regulatory", imp="high", auth="IRS",
      oq=["IRS Notice 2017-73 is not seeded as a source."]),
    Q("event-tickets", "How does the platform prevent DAF grants from paying for gala tickets, auction items, sponsorships with benefits or memberships?",
      "These are common prohibited benefit scenarios.",
      "Donors receive goods or services paid with DAF assets.",
      [S("SRC-IRC-4967", "§4967(a)", "informed-by", "directly-documented"), UNB()], cls="legal-regulatory", imp="critical", auth="IRS"),
    Q("bifurcated-grants", "Does the platform support or prohibit bifurcated grants, where the DAF pays only the charitable portion of an event and the donor pays the benefit portion personally?",
      "Sponsors differ on bifurcation given unsettled guidance.",
      "Inconsistent treatment creating excise tax exposure.",
      [S("SRC-IRS-DAF-PROPOSED-REGS-2023"), UNB()], cls="customer-preference", imp="medium"),
    Q("embedded-context", "When giving is initiated from an embedded charity or partner page, how does the platform know whether the context carries a benefit such as an event registration?",
      "Embedded checkout obscures what the donor is paying for.",
      "Benefit-bearing payments disguised as donations.",
      [UNB()], imp="high"),
    Q("tuition-and-personal", "How are grants for tuition, school fees for a donor's child or payments to entities controlled by the donor blocked?",
      "These are classic benefit and excess benefit patterns.",
      "Personal expenses paid from DAF assets.",
      [S("SRC-IRC-4958", rel="informed-by"), S("SRC-IRC-4967", rel="informed-by"), UNB()], cls="legal-regulatory", imp="critical", auth="IRS"),
]
units.append(u)

u = AU("declines", "Neutral decline reasons and independent reconsideration",
    "Declines use a sponsor-configurable neutral catalog: donor-facing text describes the policy outcome, never facts "
    "about a charity; sanctions, investigation and law-enforcement reasons map to a generic compliance review code; "
    "charity-facing communication is limited to status codes. Reconsideration defaults to a 60-day filing window and a "
    "30-day response target, is decided by a reviewer independent of the original decision, and both records survive "
    "with outcomes Upheld, Reversed, Modified, Withdrawn or Referred.",
    "Decline catalog and reconsideration per CNV-GRT-012; explanations per UNB-GRANT-037.",
    "declines would use neutral, sponsor-approved wording with an independent reconsideration path.",
    ["CNV-GRT-012", "UNB-GRANT-037", "UNB-GRT-002", "UNB-GRANT-028"], impl="low",
    challenge=CH(
        "Sponsors want to explain declines to donors without defaming charities or tipping off subjects of investigations.",
        "Defamation claims, tipping off in sanctions or law enforcement matters, or donor complaints of arbitrary treatment.",
        "Free-text decline notes written by staff are inconsistent and risky.",
        "No statute prescribes decline wording; tipping-off and defamation risk arise from general law.",
        "Not typically contractual.",
        "Staff write ad hoc decline emails.",
        "A closed catalog of neutral codes removes the possibility of factual allegations in donor-facing text.",
        "Only catalog phrases can be sent; free text limited to approved phrases.",
        "Every decline carries its code and reviewer, enabling consistency analysis.",
        "Neutral catalog plus independent reconsideration.",
        "Yes, from decline records.",
        "Likely.",
        "Donors may perceive neutral codes as evasive, increasing reconsideration volume.",
        "Low cost, high latent legal risk.", "Low.",
        "Over-generic messages may frustrate donors.",
        ["Removes defamation and tipping-off risk structurally"],
        ["Some sponsors want to give donors richer explanations"],
        "stronger", "likely"),
    controls=[CTL("Closed neutral decline catalog",
        "Allow only sponsor-approved neutral decline codes and phrases in donor- and charity-facing communications.",
        "preventive-structural", "L3-restricted-interface", ext=["UNB-CTRL-061"]),
        CTL("Independent reconsideration reviewer assignment",
        "Ensure reconsideration is decided by a reviewer other than the original decision maker.",
        "preventive-structural", "L3-restricted-interface", ext=["UNB-CTRL-027"])],
    evrs=[EVR("Decline and reconsideration records",
        "Decline codes, communications sent, reconsideration requests, reviewer independence and outcomes.",
        prov=["grant id", "decline code", "catalog version", "original decider", "reconsideration reviewer", "outcome", "time"])])
u["questions"] = [
    Q("decline-catalog", "What decline reasons does the platform support, and can the sponsor configure the catalog?",
      "Sponsors need consistent, appropriate decline reasons.",
      "Inconsistent or legally risky decline messages.",
      [UNB()], cls="customer-preference", imp="medium"),
    Q("donor-facing-text", "What is the donor told when a grant is declined for sanctions, an investigation or law-enforcement reasons?",
      "Messages must not tip off or defame.",
      "Tipping off a sanctioned party or defaming a charity.",
      [S("SRC-OFAC-REGS", rel="informed-by"), UNB()], imp="high"),
    Q("charity-facing-text", "What, if anything, is the charity told when a grant to it is declined?",
      "Charities may contest or be harmed by declines.",
      "Disclosure of donor identity or unproven allegations to a charity.",
      [UNB()], imp="medium"),
    Q("reconsideration", "Can a donor request reconsideration of a declined grant, within what window, and who decides?",
      "Fairness and error correction.",
      "Erroneous declines persist without recourse.",
      [UNB()], cls="customer-preference", imp="medium"),
    Q("record-survival", "Are original decisions and reconsideration outcomes both preserved and available for audit?",
      "Auditors and boards review decline patterns.",
      "Overwritten decisions hide errors or bias.",
      [UNB(), S("SRC-AICPA-TSC", "PI1.5")], imp="medium"),
]
units.append(u)

u = AU("payee", "Payee substitution, payment destination integrity and partner exclusion from funds flow",
    "Canonical charity identity, legal payee, fiscal sponsor, project and payment destination are resolved separately. "
    "Payee substitution to a merger successor requires a verified legal successor passing eligibility on its own EIN in "
    "the same recipient class, sponsor approval and donor notice. Bank-detail changes require independent verification "
    "(bank-originated account owner match, cooling-off, notice to old and new verified channels) and dual control, and "
    "unverified changes cannot propagate into approved payment instructions. No partner, host or vendor account ever "
    "appears in the payment path.",
    "Payee resolution per UNB-GRANT-007, substitution per CNV-GRT-010, bank change controls per UNB-GEX-018 and CNV-PAY-002, propagation block per UNB-CHAR-032.",
    "payee changes and bank-detail changes would require independent verification and dual control.",
    ["UNB-GRANT-007", "CNV-GRT-010", "UNB-GEX-018", "CNV-PAY-002", "UNB-CHAR-032", "UNB-GRANT-026", "UNB-XIN-OTH-003", "TVR-PAY-005", "UNB-PAY-005"],
    policies=["SEC-AUTH-001"], impl="high", rec="medium",
    controls=[CTL("Independent verification and dual control of payee bank-detail changes",
        "Prevent payment to changed bank details until independently verified and approved by two authorized people.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-031", "UNB-CTRL-049"],
        fw=[S("SRC-NACHA-RULES"), S("SRC-NIST-SP800-53-R5", "AC-5")]),
        CTL("Payee substitution successor verification",
        "Allow substitution only to a verified legal successor that independently passes eligibility.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-016"])],
    evrs=[EVR("Payee change and substitution evidence",
        "Bank-detail change verification artifacts, approvers, notices and substitution decisions.",
        prov=["charity id", "old destination fingerprint", "new destination fingerprint", "verification method", "approvers", "notices", "time"])])
u["questions"] = [
    Q("payee-substitution", "When a recommended charity has merged, dissolved or renamed, under what conditions will the platform pay a different legal entity?",
      "Paying a successor must not bypass vetting.",
      "Payment to an unvetted or unrelated entity.",
      [UNB(), S("SRC-IRS-TEOS")], imp="high"),
    Q("bank-detail-change", "How are changes to a charity's bank account details verified before payment, and who must approve them?",
      "Bank-detail substitution is the most common grant payment fraud.",
      "Business email compromise diverts grants.",
      [UNB(), S("SRC-NACHA-RULES"), S("SRC-NACHA-FRAUD-MONITORING-2026")], cls="industry-convention", imp="critical",
      alts=["How do you prevent payment redirection fraud?"]),
    Q("fiscal-sponsor-payee", "When a grant supports a fiscally sponsored project, who is the legal payee and how is the payment destination verified?",
      "Fiscally sponsored projects are not themselves exempt entities.",
      "Payment to a project's own account rather than the fiscal sponsor.",
      [UNB()], imp="high"),
    Q("partner-in-funds-flow", "Can a distribution partner, embedding host, advisor firm or the vendor itself ever appear as payee or intermediary in a grant payment?",
      "Intermediated flows add custody, licensing and fraud risk.",
      "Funds pass through accounts not controlled by the sponsor.",
      [UNB(), S("SRC-NACHA-RULES")], imp="critical"),
    Q("payment-gate", "Can any person or system originate a grant payment outside the platform's payment gate, including during manual fallback?",
      "All payments must pass the same checks.",
      "Manual payments bypass eligibility and sanctions checks.",
      [UNB()], imp="critical", req=["TVR-PAY-004", "UNB-PAY-003"]),
]
units.append(u)

u = AU("returns", "Returned, uncashed and refunded grant payments",
    "Payment states distinguish prepared, approved, submitted, accepted, rejected, settled, returned and reconciled. "
    "Returns after disbursement are accepted and restore the fund through linked reversal entries, uncashed checks follow "
    "a sponsor-approved aging and reissue or redirect policy that considers state unclaimed property rules, and grantee "
    "refunds are recorded as linked corrections with donor notice. Unknown payment outcomes are never treated as failures "
    "without proof.",
    "Payment state model per UNB-GRANT-022, returns per TVR-GR-002, exceptions per UNB-PAY-006 and CNV-PAY-003/004.",
    "returned, uncashed and refunded grants would follow explicit states and linked reversal entries.",
    ["UNB-GRANT-022", "UNB-GRANT-028", "TVR-GR-002", "UNB-PAY-006", "CNV-PAY-003", "CNV-PAY-004", "TVR-PAY-001"], impl="medium",
    oq=["CNV-PAY-003 references a statute-derived state rule row for uncashed grants; the rule content and counsel review are not established."],
    controls=[CTL("Explicit payment state machine with Unknown state",
        "Prevent treating unknown payment outcomes as failed and reissuing, which causes double payment.",
        "preventive-structural", "L2-type-system", ext=["UNB-CTRL-049"], policies=["SEC-LANG-002"])],
    evrs=[EVR("Payment exception and return records",
        "Returns, voids, reissues, aging status and linked accounting reversals per grant.",
        prov=["grant id", "payment attempt id", "state", "return reason", "linked reversal entry", "time"])])
u["questions"] = [
    Q("returned-payments", "How are returned ACH or wire grant payments handled, and how is the fund balance restored?",
      "Returned payments must be traceable to the fund.",
      "Funds lost or balances misstated.",
      [UNB(), S("SRC-NACHA-RULES")], imp="high"),
    Q("uncashed-checks", "What happens to grant checks that are never cashed, and does the policy consider state unclaimed property rules?",
      "Uncashed checks are frequent with small charities.",
      "Funds stuck indefinitely or escheated incorrectly.",
      [S("SRC-STATE-UNCLAIMED-PROPERTY"), UNB()], cls="legal-regulatory", imp="medium", jur=["US-states"], auth="state unclaimed property administrators"),
    Q("grantee-refunds", "How are refunds from grantees (for example an event cancellation or unused restricted funds) recorded and returned to the fund?",
      "Refunds must not go to the donor.",
      "Refunds paid to donors, creating prohibited benefits.",
      [UNB(), S("SRC-IRC-4967", rel="informed-by")], imp="medium"),
    Q("unknown-outcomes", "How does the platform handle payments whose outcome is unknown (for example a provider timeout), and what prevents double payment?",
      "Unknown states are a classic double-payment cause.",
      "Duplicate grant payments.",
      [UNB()], imp="high"),
]
units.append(u)

u = AU("letters", "Grant letters, acknowledgments to grantees and date distinctions",
    "Grant correspondence is generated from versioned sponsor templates through a reproducible document registry "
    "(Folio rendering) that preserves the exact issued bytes and allows verification. Letters name the sponsor as "
    "grantor, state that no goods or services may be provided to the donor, reflect the donor's recognition preference, "
    "and distinguish award, accounting recognition, payment, settlement and grantee receipt dates.",
    "Document artifact registry per REQ-X-034 and UNB-PLAT-003; date model per UNB-GRANT-039.",
    "grant letters would be generated from versioned templates and archived as verifiable artifacts.",
    ["UNB-GRANT-032", "UNB-PLAT-003", "REQ-X-034", "UNB-GRANT-039", "UNB-GEX-015"], impl="medium",
    controls=[CTL("Immutable document artifact registry for grant correspondence",
        "Preserve exact issued grant letters with template version and content hash for verification.",
        "preventive-structural", "L3-restricted-interface", ["Unbound (proposed; not built)", "Folio (exists; not operated for Unbound)"],
        ext=["UNB-CTRL-088"])],
    evrs=[EVR("Issued grant letter registry entries",
        "Each issued letter with template version, content hash, recipients and delivery status.",
        fmt="PDF plus JSON metadata", prov=["artifact id", "grant id", "template version", "content hash", "recipient", "issued time"])])
u["questions"] = [
    Q("letter-contents", "What does a grant letter to a charity state, and does it identify the sponsor as grantor and say that no benefits may be provided to the donor?",
      "Letters frame the legal nature of the grant.",
      "Charities treat DAF grants as donor gifts and provide benefits or receipts to donors.",
      [UNB(), S("SRC-IRC-4967", rel="informed-by")], imp="high"),
    Q("letter-verification", "Can a charity, donor or auditor verify that a grant letter is authentic and unaltered?",
      "Forged grant letters are used in fraud.",
      "Fake letters used to solicit or misrepresent.",
      [UNB()], cls="customer-preference", imp="medium"),
    Q("date-distinctions", "Does the platform distinguish grant award, accounting recognition, payment, settlement and grantee receipt dates?",
      "Different reports need different dates.",
      "Misstated financials or donor statements.",
      [UNB(), S("SRC-FASB-ASC-958")], imp="medium", req=["CNV-FIN-007"]),
    Q("grantee-receipt", "Does the platform capture grantee acknowledgment of receipt, and is that treated as evidence rather than verified fact?",
      "Sponsors track grantee confirmation.",
      "Unconfirmed grants assumed received.",
      [UNB()], cls="customer-preference", imp="low", req=["UNB-GRANT-042"]),
]
units.append(u)

u = AU("anonymity", "Grant anonymity and recognition preferences",
    "Each grant carries a recognition election (full name, name only, custom attribution, fund name only, anonymous), "
    "stored as an authority fact with effective time. Correspondence, remittance data and payment references are "
    "derived from the election at send time; immediately before external send the delivery worker re-reads the current "
    "election and suppresses or regenerates the message if it changed. Anonymity applies to charities and partners but "
    "does not prevent sponsor compliance screening or legally required disclosure.",
    "Recognition model per UNB-GRANT-002/025, ADM-013; send-time re-check per UNB-XIN-EVA-015.",
    "anonymity elections would be enforced at send time across letters, remittance data and partner channels.",
    ["UNB-GRANT-025", "UNB-GRANT-002", "ADM-013", "UNB-XIN-EVA-014", "UNB-XIN-EVA-015"], impl="low",
    controls=[CTL("Send-time recognition election re-check",
        "Prevent any outbound grant communication or remittance from disclosing donor identity contrary to the current election.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-085"], fw=[S("SRC-AICPA-TSC", "P6.1")])],
    evrs=[EVR("Recognition election and outbound disclosure log",
        "Election history and, for each outbound message, the election version applied.",
        prov=["grant id", "election version", "message id", "fields disclosed", "time"])])
u["questions"] = [
    Q("anonymity-options", "What anonymity and recognition options can a donor choose for each grant, and can they differ from the fund default?",
      "Donor privacy preferences vary by grant.",
      "Donor identity disclosed against preference.",
      [UNB()], cls="customer-preference", imp="high"),
    Q("remittance-leakage", "Can a charity learn an anonymous donor's identity from payment remittance data, check memos, or bank references?",
      "Payment channels often leak names.",
      "Anonymity defeated by payment metadata.",
      [UNB(), S("SRC-NACHA-RULES")], imp="high"),
    Q("election-change", "If a donor changes a recognition preference after approval but before the grant letter is sent, which preference is applied?",
      "Preferences change and timing matters.",
      "Outdated preference applied.",
      [UNB()], imp="medium"),
    Q("anonymity-limits", "How does anonymity interact with sponsor screening, legal process and charity due diligence needs?",
      "Anonymity cannot defeat compliance.",
      "Anonymity used to hide related-party grants.",
      [UNB(), S("SRC-IRC-4958", rel="informed-by")], imp="medium"),
]
units.append(u)
