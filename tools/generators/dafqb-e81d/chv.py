from dafcommon import *

TEOS = lambda b="directly-documented": S("SRC-IRS-TEOS", rel="informed-by", basis=b)
TCG = lambda b="directly-documented": S("SRC-TREASURY-CHARITY-GUIDELINES", rel="informed-by", basis=b)
units = []

u = AU("irs-sources", "Eligibility verification against IRS primary data",
    "Recipient status is established from first-party ingestion of IRS primary sources (Tax Exempt Organization Search "
    "and Pub 78 data, the EO Business Master File, automatic revocation lists, Form 990 series and 990-N data, and "
    "determination letters where available), each observation stored with source, posting date, retrieval time and "
    "checksum. Public charity status under section 170(b)(1)(A) is distinguished from private foundation status, "
    "grants are made to the listed legal name, group-exemption subordinates are flagged for additional verification, "
    "and absence from a dataset is never treated by itself as proof of ineligibility.",
    "First-party connectors per UNB-CHAR-010 and UNB-EXT-001, provenance per UNB-CHAR-008, approval and release checks per CNV-GRT-003.",
    "charity status would be verified from IRS primary data with full provenance.",
    ["UNB-EXT-001", "UNB-CHAR-008", "UNB-CHAR-010", "UNB-CHAR-011", "UNB-CHAR-016", "CNV-GRT-003", "CNV-GRT-002"],
    policies=["SEC-DATA-001"], mech="periodic-automated", fresh="P1D", impl="high", rec="medium",
    oq=["IRS bulk data publication cadence and gaps for 2026 need verification before freshness targets are committed."],
    controls=[CTL("Provenance-preserving IRS data ingestion",
        "Store every IRS observation with source, posting date, retrieval time and checksum, and expose freshness and coverage gaps.",
        "detective-automated", "L6-automated-analysis", ext=["UNB-CTRL-010", "UNB-CTRL-011"])],
    evrs=[EVR("Source ingestion and freshness log",
        "Per-source ingestion runs with posting dates, record counts, checksums, failures and coverage gaps.",
        mech="periodic-automated", fresh="P1D",
        prov=["source", "publication date", "retrieval time", "checksum", "record count", "errors"])])
u["questions"] = [
    Q("irs-datasets", "Which IRS data sources does the platform use to verify a grantee's tax-exempt and public charity status?",
      "Eligibility decisions are only as good as their sources.",
      "Grants to organizations that are not eligible.",
      [TEOS(), UNB()], cls="legal-regulatory", imp="critical", auth="IRS",
      alts=["How do you verify 501(c)(3) status?", "Do you rely on a third-party charity database or primary IRS data?"]),
    Q("public-charity-vs-pf", "How does the platform distinguish public charities from private foundations and other exempt organizations, given that grants to some recipients require expenditure responsibility?",
      "Grants to non-operating private foundations from DAFs are taxable distributions unless expenditure responsibility is exercised.",
      "Taxable distributions from misclassified recipients.",
      [TEOS(), S("SRC-IRC-4966", "§4966(c)", "informed-by", "reasonably-inferred")], cls="legal-regulatory", imp="critical", auth="IRS"),
    Q("legal-name", "Are grants made and checks issued to the legal name listed in IRS data, and how are DBA names handled?",
      "Payments to a DBA can be diverted or fail.",
      "Misdirected payments or payments to impostors using similar names.",
      [TEOS(), UNB()], imp="medium"),
    Q("absence-from-data", "How does the platform treat an organization that does not appear in IRS bulk data?",
      "Many eligible organizations (churches, new organizations, subordinates) are absent.",
      "Either wrongful decline or wrongful approval.",
      [TEOS(), UNB()], imp="high"),
    Q("group-exemptions", "How are subordinate organizations covered by a group exemption verified?",
      "Subordinates often do not appear individually in Pub 78 data.",
      "Grants to entities falsely claiming group coverage.",
      [TEOS(), UNB()], imp="medium"),
    Q("source-provenance", "For each eligibility decision, can the platform show which source records, with which publication dates, were relied upon?",
      "Auditors and counsel need the basis of each decision.",
      "Undefendable decisions.",
      [UNB(), S("SRC-AICPA-TSC", "PI1.2")], imp="high"),
]
units.append(u)

u = AU("freshness", "Status freshness, reverification cadence and event-triggered reevaluation",
    "Status is checked at approval and again at release against the latest published IRS data, with each source's "
    "posting date recorded and a retrieval target of 24 hours from publication (an operational target, not a legal "
    "threshold). Deep reviews expire by default after 180 days (sponsors may tighten) with refresh 30 days before expiry, "
    "and any primary-source change, policy change or grant purpose change triggers reevaluation of only the impacted "
    "decisions. When a source is unavailable or stale beyond policy, release holds rather than proceeding.",
    "Freshness rules per CNV-GRT-003, reevaluation per UNB-CHAR-024 and UNB-GEX-019, release recheck per UNB-GRANT-009.",
    "status would be rechecked at approval and release with event-triggered reevaluation and fail-closed behavior on stale data.",
    ["CNV-GRT-003", "UNB-CHAR-015", "UNB-CHAR-024", "UNB-GEX-019", "UNB-GRANT-009", "UNB-CHAR-011"],
    mech="continuous-automated", fresh="P1D", auto="full", impl="medium",
    challenge=CH(
        "Sponsors want assurance that grantees are still eligible when paid.",
        "Payment to an organization whose status was revoked after initial vetting.",
        "Annual or periodic reverification leaves gaps of up to a year between a status change and detection.",
        "No statute sets a reverification interval; sponsors must not make taxable distributions, and IRS guidance allows reliance on IRS data with conditions.",
        "Some sponsor agreements specify periodic reverification.",
        "Annual batch reverification of the grantee list.",
        "Not eliminable; status is external.",
        "Check at approval and at release against the latest data; event-triggered reevaluation on source change.",
        "Each decision carries source posting dates, making freshness provable per payment.",
        "Per-payment verification against latest data plus event-driven invalidation.",
        "Yes, through per-decision provenance.",
        "Likely; this exceeds common practice.",
        "IRS data itself lags real-world status changes; freshness to the source does not mean truth.",
        "Low compute, weak coverage.", "Medium (ingestion pipeline and change detection).",
        "False sense of certainty from fresh but lagging data.",
        ["Narrows exposure window to the IRS publication lag", "Evidence per payment"],
        ["IRS publication lag remains", "Source outages could block releases"],
        "stronger", "likely"),
    controls=[CTL("Release-time status recheck with fail-closed on stale data",
        "Block payment release when eligibility evidence is older than policy or a source is unavailable.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-016", "UNB-CTRL-017"]),
        CTL("Event-triggered reevaluation of impacted decisions",
        "Reevaluate only decisions whose evidence changed when a source, policy or purpose changes.",
        "detective-automated", "L9-runtime-monitored", ext=["UNB-CTRL-017"])],
    evrs=[EVR("Eligibility check timeline per payment",
        "Approval-time and release-time checks with source posting dates, cache age and reevaluation triggers.",
        mech="continuous-automated", fresh="per-event",
        prov=["grant id", "check stage", "source posting dates", "cache age", "trigger", "outcome", "time"])])
u["questions"] = [
    Q("check-timing", "At which points in the grant lifecycle is recipient status checked (recommendation, approval, payment release)?",
      "Status can change between approval and payment.",
      "Payment to a recently revoked organization.",
      [TEOS("reasonably-inferred"), UNB()], imp="critical"),
    Q("reverification-cadence", "How often are previously vetted grantees reverified, and can the sponsor set a shorter interval?",
      "Sponsors set diligence freshness in policy.",
      "Stale diligence relied upon.",
      [UNB()], imp="high", alts=["How often do you refresh charity data?"]),
    Q("event-triggered", "What events trigger reevaluation of a charity's eligibility outside the normal cadence?",
      "Material changes should prompt immediate review.",
      "Material changes go unnoticed until the next cycle.",
      [UNB()], imp="medium"),
    Q("source-outage", "If IRS data or another source is unavailable or stale, does the platform hold payments or proceed on cached data?",
      "Fail-open behavior defeats verification.",
      "Payments released on outdated evidence during outages.",
      [UNB(), S("SRC-NIST-SP800-53-R5", "SI-17")], imp="high"),
    Q("data-lag", "How quickly after the IRS publishes a revocation or status change does the platform reflect it?",
      "Sponsors want to understand the exposure window.",
      "Payments during the lag period.",
      [TEOS(), UNB()], imp="medium"),
]
units.append(u)

u = AU("revocation", "Revocation and reinstatement handling",
    "When IRS data shows an automatic or other revocation or removal from Pub 78 data, the platform re-verifies the fact "
    "from the primary source, places a legally mandatory hold on pending and recurring grants to that organization, "
    "routes in-flight payments for recall where possible, notifies affected donors with neutral wording, and records "
    "reinstatement (including retroactive reinstatement) as a new linked fact without erasing history.",
    "Revocation holds per CNV-GRT-004 and UNB-CHAR-015; hold propagation per CNV-ARC-003; cancellation rules per TVR-GR-004.",
    "revocations would place automatic legally mandatory holds and reinstatements would be recorded as linked facts.",
    ["CNV-GRT-004", "UNB-CHAR-015", "UNB-CHAR-024", "TVR-GR-004", "UNB-GRANT-027", "UNB-CHAR-004"], auto="full", impl="medium",
    controls=[CTL("Automatic mandatory hold on revocation",
        "Hold all pending, scheduled and recurring grants to an organization upon verified revocation; mandatory holds do not auto-release.",
        "preventive-gate", "L9-runtime-monitored", ext=["UNB-CTRL-016"])],
    evrs=[EVR("Revocation hold records",
        "Revocation facts, holds created, affected grants, recall attempts, notices and release on reinstatement.",
        prov=["charity id", "revocation source", "posting date", "hold id", "affected grants", "release reason", "time"])])
u["questions"] = [
    Q("revocation-hold", "When a grantee's exemption is revoked, what happens automatically to pending, scheduled and recurring grants?",
      "Revocation makes grants potentially taxable distributions.",
      "Payments continue after revocation.",
      [TEOS(), UNB()], cls="legal-regulatory", imp="critical", auth="IRS"),
    Q("in-flight-payments", "What does the platform do about payments already submitted when a revocation is detected?",
      "Some payments may still be recalled.",
      "Unrecalled payments to ineligible recipients.",
      [UNB()], imp="high"),
    Q("reinstatement", "How is reinstatement, including retroactive reinstatement, recorded and applied to held grants?",
      "Reinstated organizations should be able to receive held grants.",
      "Wrongful continued holds or erased history.",
      [TEOS(), UNB()], imp="medium"),
    Q("donor-notice-revocation", "How are donors told that a recommended grant is held because of a recipient's status change?",
      "Donors need actionable, accurate information.",
      "Defamatory or confusing communications.",
      [UNB()], cls="customer-preference", imp="low"),
]
units.append(u)

u = AU("foreign", "Foreign grantees, equivalency determinations and intermediaries",
    "Direct foreign grants are architecturally supported but disabled in release 1. When enabled, the routine path "
    "requires a current EquivalencyDetermination record (practitioner identity and Circular 230 standing, advice date, "
    "grantee taxable year, currency under the applicable regulation) or sponsor-exercised expenditure responsibility. "
    "Recommendations naming a foreign organization without either are redirected to the sponsor's catalog of domestic "
    "intermediaries whose outbound wording may name a program, country or cause but never the foreign organization. "
    "Foreign-related grants add OFAC general licence versioning, risk-based anti-corruption diligence, staged payments "
    "and use reporting.",
    "Foreign path per CNV-GRT-002, CNV-GRT-007, CNV-GRT-008, UNB-GRANT-041, UNB-XIN-NPG-001/002.",
    "foreign grants would be disabled in release 1 and, when enabled, require equivalency determinations or expenditure responsibility.",
    ["CNV-GRT-002", "CNV-GRT-007", "CNV-GRT-008", "UNB-GRANT-041", "UNB-XIN-NPG-001", "UNB-XIN-NPG-002", "UNB-WF-006", "CNV-GRT-011"],
    impl="high", rec="high", auto="partial",
    oq=["Treasury Regulation 53.4945-5(a)(5) on equivalency determinations is not a seeded source.",
        "Expenditure responsibility workflow is not specified in detail."],
    controls=[CTL("Equivalency determination or expenditure responsibility gate",
        "Block routine-path foreign grants lacking a current equivalency determination or approved expenditure responsibility.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-016"]),
        CTL("Intermediary outbound wording control",
        "Prevent outbound requests to intermediaries from naming a specific foreign organization.",
        "preventive-structural", "L3-restricted-interface")],
    evrs=[EVR("Foreign grant diligence file",
        "Equivalency determination or expenditure responsibility records, sanctions and licence reliance, anti-corruption declarations and payment stages.",
        prov=["grant id", "determination id", "practitioner", "advice date", "licence reliance version", "declarations", "time"])])
u["questions"] = [
    Q("foreign-support", "Does the platform support grants to foreign organizations, and if not, how are such recommendations handled?",
      "Donors frequently recommend international causes.",
      "Taxable distributions or unsupported workarounds.",
      [TCG(), S("SRC-IRC-4966", "§4966(c)", "informed-by", "reasonably-inferred"), UNB()], cls="legal-regulatory", imp="high", jur=["US-federal", "global"], auth="IRS"),
    Q("equivalency-determinations", "How are equivalency determinations obtained, recorded and kept current, and whose written advice does the sponsor rely on?",
      "Reliance on equivalency determinations has specific currency and practitioner conditions.",
      "Reliance on stale or unqualified determinations.",
      [TCG("reasonably-inferred"), UNB()], cls="legal-regulatory", imp="high", jur=["US-federal", "global"], auth="IRS",
      oq=["Seed the equivalency determination regulation as a source."]),
    Q("expenditure-responsibility", "Does the platform support expenditure responsibility (pre-grant inquiry, written agreement, reports, IRS reporting) for grants that require it?",
      "ER is required for some recipients to avoid taxable distributions.",
      "ER steps missed, making the grant taxable.",
      [S("SRC-IRC-4966", "§4966(c)", "informed-by", "directly-documented"), UNB()], cls="legal-regulatory", imp="high", auth="IRS"),
    Q("intermediary-earmarking", "When a donor wants to support a foreign charity through a US intermediary, how does the platform avoid earmarking that would make the grant a conduit?",
      "Earmarked pass-through grants defeat the intermediary's discretion.",
      "Conduit treatment of grants.",
      [TCG("reasonably-inferred"), UNB()], cls="legal-regulatory", imp="medium", auth="IRS"),
    Q("anti-diversion", "What anti-diversion and anti-corruption diligence applies to foreign-related grants (government ownership, officials, staged payments, use reports)?",
      "Foreign grants carry terrorism financing and corruption risk.",
      "Diversion of funds to sanctioned or corrupt actors.",
      [TCG(), S("SRC-OFAC-COMPLIANCE-FRAMEWORK")], cls="supervisory-guidance", imp="high", jur=["US-federal", "global"], auth="OFAC (Treasury)"),
]
units.append(u)

u = AU("entity-types", "Fiscal sponsors, churches, government units, supporting organizations and non-filers",
    "A counsel-approved entity-type evidence matrix defines accepted evidence for churches and conventions not required "
    "to file, government units, group-exemption subordinates, disregarded entities of an eligible parent and newly "
    "recognized organizations not yet in bulk files. Fiscally sponsored projects record arrangement type, evidence "
    "source and the fiscal sponsor's own eligibility, with the fiscal sponsor as legal payee. Supporting organizations "
    "are classified by type, and Type I or II and grants to Type III supporting organizations route to enhanced review "
    "under §4966 rules. Charity identity, legal payee, fiscal sponsor and project remain separate entities.",
    "Entity evidence matrix per UNB-RCN-GRT-013, fiscal sponsorship evidence per UNB-XIN-NPG-003, separation per UNB-RULE-011 and UNB-KNOW-007.",
    "non-standard recipients would be verified through a counsel-approved evidence matrix.",
    ["UNB-CHAR-003", "UNB-RCN-GRT-013", "UNB-XIN-NPG-003", "UNB-RULE-011", "UNB-KNOW-007", "CNV-GRT-011", "UNB-CHAR-009"],
    impl="medium", auto="partial",
    oq=["Disqualified supporting organization classification depends on data that IRS bulk files may not provide reliably."],
    controls=[CTL("Entity-type evidence matrix enforcement",
        "Require the counsel-approved evidence for each non-standard recipient type before an Eligible decision.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-016", "UNB-CTRL-018"])],
    evrs=[EVR("Entity-type evidence records",
        "Evidence items satisfying the matrix per recipient, including fiscal sponsorship arrangements.",
        prov=["charity id", "entity type", "matrix version", "evidence items", "reviewer", "time"])])
u["questions"] = [
    Q("fiscal-sponsors", "How does the platform verify grants to fiscally sponsored projects, and who is the legal recipient?",
      "Fiscal sponsorship is common for emerging causes.",
      "Payment to an unincorporated project or misrepresented sponsorship.",
      [UNB(), TEOS("reasonably-inferred")], imp="high"),
    Q("churches", "How are churches and other organizations not required to file with the IRS verified?",
      "Churches are a large share of DAF grants but may not appear in IRS lists.",
      "Wrongful declines or grants to impostor churches.",
      [TEOS("reasonably-inferred"), UNB()], imp="high"),
    Q("government-units", "Can grants be made to government units such as public schools and municipalities, and how is the exclusively public purpose established?",
      "Government grants are permitted for public purposes.",
      "Grants to government units for non-public purposes.",
      [S("SRC-IRC-170", rel="informed-by"), UNB()], imp="medium"),
    Q("supporting-organizations", "How does the platform identify supporting organizations and their type, given that some supporting organizations require expenditure responsibility?",
      "Grants to certain supporting organizations can be taxable distributions.",
      "Taxable distributions to disqualified supporting organizations.",
      [S("SRC-IRC-4966", "§4966(c)", "informed-by", "reasonably-inferred"), TEOS()], cls="legal-regulatory", imp="high", auth="IRS"),
    Q("new-organizations", "How are newly recognized organizations not yet in IRS bulk files verified?",
      "New charities need timely access to grants.",
      "Wrongful declines or reliance on forged determination letters.",
      [TEOS(), UNB()], imp="medium"),
    Q("universities-hospitals", "How are large complex recipients (universities, hospital systems, affiliated foundations) resolved to the correct legal entity?",
      "Complex organizations have many affiliates and EINs.",
      "Payment to the wrong affiliate.",
      [UNB()], imp="low", req=["UNB-EXT-012"]),
]
units.append(u)

u = AU("sanctions", "Sanctions screening of grantees, donors and payment parties",
    "A counsel-approved screening scope matrix covers recipient legal entity, fiscal sponsor and project, payee account "
    "holder, intermediary and beneficiary banks for cross-border payments, destination country, donors, advisors and "
    "successors. Parties are screened at onboarding, delta-screened automatically on list updates and screened before "
    "each grant release against the current list version. Confirmed matches resolve to Block, Reject or Proceed under a "
    "licence or exemption, never automatically, and produce OFAC report data within required timelines. Licence "
    "reliance is versioned and re-verified at release.",
    "Screening per CNV-GRT-006/007 and UNB-RCN-GRT-007; restricted lists per UNB-CHAR-031.",
    "sanctions screening would occur at onboarding, on list updates and before each release, with human match resolution.",
    ["CNV-GRT-006", "CNV-GRT-007", "UNB-RCN-GRT-007", "UNB-CHAR-031", "UNB-CHAR-026", "CNV-PLT-004"],
    mech="continuous-automated", fresh="P1D", impl="medium", rec="medium",
    oq=["Screening data provider not selected; list coverage beyond OFAC (for example other jurisdictions' lists) not decided."],
    controls=[CTL("Release-time sanctions screening against current list version",
        "Screen all in-scope parties before each release and block release on unresolved potential matches.",
        "preventive-gate", "L9-runtime-monitored", ext=["UNB-CTRL-016"],
        fw=[S("SRC-OFAC-COMPLIANCE-FRAMEWORK"), S("SRC-OFAC-REGS")]),
        CTL("Human resolution of potential matches",
        "Require a trained reviewer to resolve potential matches as Block, Reject or Proceed with documented basis.",
        "detective-manual", "L10-external-or-manual", ext=["UNB-CTRL-018"])],
    evrs=[EVR("Screening results and match dispositions",
        "Per-party screening results with list versions, potential matches, dispositions and OFAC report data.",
        mech="continuous-automated", prov=["party id", "list version", "match score", "disposition", "reviewer", "report reference", "time"],
        retention="10 years after transaction per CNV-PLT-004 (proposed)")])
u["questions"] = [
    Q("screening-scope", "Which parties are screened against sanctions lists: grantees, their officers, fiscal sponsors, banks, donors, advisors and successors?",
      "OFAC obligations apply to dealings with blocked persons.",
      "Dealings with sanctioned parties.",
      [S("SRC-OFAC-REGS", rel="informed-by", basis="directly-documented"), S("SRC-OFAC-COMPLIANCE-FRAMEWORK"), UNB()], cls="legal-regulatory", imp="critical", auth="OFAC (Treasury)"),
    Q("screening-timing", "When does screening occur, and are existing relationships rescreened when sanctions lists change?",
      "List updates create new matches among existing parties.",
      "Stale screening misses newly designated parties.",
      [S("SRC-OFAC-COMPLIANCE-FRAMEWORK", rel="informed-by", basis="directly-documented"), UNB()], cls="supervisory-guidance", imp="critical", auth="OFAC (Treasury)"),
    Q("match-resolution", "How are potential matches resolved, by whom, and what prevents automatic blocking or automatic clearing?",
      "False positives and false negatives both cause harm.",
      "Wrongful blocking or missed true matches.",
      [S("SRC-OFAC-COMPLIANCE-FRAMEWORK"), UNB()], imp="high"),
    Q("ofac-reporting", "Does the platform produce the data needed for OFAC blocked and rejected transaction reports and annual blocked property reports?",
      "Reports have short deadlines.",
      "Late or missing OFAC reports.",
      [S("SRC-OFAC-REGS", "31 CFR 501.603", "informed-by", "directly-documented"), UNB()], cls="legal-regulatory", imp="high", auth="OFAC (Treasury)"),
    Q("general-licences", "How does the platform record and re-verify reliance on OFAC general licences for humanitarian grants?",
      "Licence conditions change.",
      "Reliance on expired or inapplicable licences.",
      [S("SRC-OFAC-REGS"), UNB()], cls="legal-regulatory", imp="medium", jur=["US-federal", "global"], auth="OFAC (Treasury)"),
]
units.append(u)

u = AU("adverse-media", "Adverse media, discretionary holds and explainable risk signals",
    "Discretionary holds are permitted only under a board-approved policy listing criteria (adjudicated findings, "
    "regulator actions, official pending matters; media allegations only with elevated approval and a shorter maximum). "
    "Each hold records reason, evidence, owner and review deadline (maximum 90 days, renewable once on new evidence) and "
    "auto-releases, while legally mandatory holds never auto-release. Monitoring alerts carry materiality, confidence, "
    "freshness and ownership; no black-box AI risk score decides eligibility.",
    "Discretionary hold policy per CNV-GRT-005; alerting per UNB-CHAR-033; AI limits per UNB-CHAR-022.",
    "adverse information would lead only to time-limited, policy-based holds with human review and explainable signals.",
    ["CNV-GRT-005", "UNB-CHAR-033", "UNB-CHAR-022", "UNB-CHAR-030", "CNV-GRT-011"], impl="medium", rec="medium", auto="partial",
    challenge=CH(
        "Sponsors want to avoid grants to charities involved in fraud, extremism or scandal.",
        "Reputational harm or diversion of funds to bad actors.",
        "Commercial adverse media screening produces high false-positive rates and unverifiable allegations; acting on it risks defamation and viewpoint bias claims.",
        "Not legally required for domestic grants to public charities; sanctions screening is the legal floor.",
        "Some bank-affiliated sponsors require adverse media screening by their own policy.",
        "Screening vendors provide adverse media hits reviewed by analysts.",
        "Not eliminable.",
        "Holds allowed only under board-approved criteria with automatic expiry.",
        "Hold records with reasons and deadlines.",
        "Policy-bounded discretionary holds tied to official or adjudicated facts, with media only under elevated approval.",
        "Yes, through hold records.",
        "Uncertain; risk-averse sponsors may want broader screening.",
        "If a sponsor's board wants viewpoint-based exclusions, the policy framework will be used for them.",
        "Medium to high recurring screening cost.", "Low.",
        "Missed genuine signals that appear only in media.",
        ["Limits defamation and bias exposure", "Concentrates review on official facts"],
        ["Some reputational risks surface first in media", "Bank-affiliated sponsors may require screening anyway"],
        "equivalent", "uncertain"),
    oq=["No requirement defines whether adverse media screening is offered at all; current requirements only bound its use in holds."],
    controls=[CTL("Board-approved discretionary hold policy with automatic expiry",
        "Limit discretionary holds to policy criteria and enforce review deadlines and automatic release.",
        "preventive-structural", "L3-restricted-interface", ext=["UNB-CTRL-018"])],
    evrs=[EVR("Discretionary hold register",
        "All discretionary holds with criteria, evidence, approver, deadlines, renewals and release.",
        prov=["hold id", "charity id", "criterion", "evidence", "approver", "deadline", "release", "time"])])
u["questions"] = [
    Q("adverse-media", "Does the platform screen grantees for adverse media, and how are results used in grant decisions?",
      "Reputation risk matters to sponsors.",
      "Grants to charities embroiled in scandal or fraud.",
      [TCG("reasonably-inferred"), UNB()], cls="customer-preference", imp="medium",
      oq=["Whether adverse media screening will be offered is undecided."]),
    Q("discretionary-holds", "Under what criteria can the sponsor place a discretionary hold on a charity, and how long can a hold last?",
      "Holds must be fair, bounded and defensible.",
      "Indefinite or arbitrary holds harm charities and donors.",
      [UNB()], imp="high"),
    Q("ai-risk-scores", "Does any AI or opaque risk score decide whether a charity is eligible or held?",
      "Sponsors and charities expect explainable decisions.",
      "Unexplainable or biased exclusions.",
      [UNB(), S("SRC-NIST-AI-RMF-1.0")], cls="customer-preference", imp="high"),
    Q("hate-and-extremism", "How does the platform support sponsor policies excluding organizations associated with hate or violent extremism, and what evidence standard applies?",
      "Several sponsors have such policies and face scrutiny over them.",
      "Inconsistent or politically contested exclusions.",
      [UNB(), S("SRC-ECH-DAF-LANDSCAPE")], cls="customer-preference", imp="medium"),
]
units.append(u)

u = AU("shared-registry", "Shared charity registry: public facts versus sponsor-private investigations",
    "The common charity registry shares only non-sensitive canonical identity facts and holds derived from verified public "
    "facts (IRS revocation, Pub 78 removal, OFAC listing, published judgments), each re-verified by the platform from the "
    "primary source. Sponsor-private investigation content, suspicions and decisions never propagate to other sponsors; "
    "sponsor-originated corrections are re-verified before updating the registry, and release 1 does not offer any "
    "cross-sponsor 'enhanced review' flag. Investigation cases are restricted to the sponsor's investigation role. "
    "Charities have a correction and right-of-response process.",
    "Sharing rules per CNV-GRT-004, UNB-CHAR-036/037; investigation isolation per UNB-XIN-CLM-004; correction per UNB-CHAR-014/017.",
    "only verified public facts would be shared across sponsors; private investigations would stay within the sponsor.",
    ["CNV-GRT-004", "UNB-CHAR-036", "UNB-CHAR-037", "UNB-CHAR-017", "UNB-CHAR-014", "UNB-XIN-CLM-004", "UNB-API-005", "UNB-TEN-007"],
    policies=["SEC-AUTH-001"], impl="medium",
    challenge=CH(
        "Sponsors want to benefit from others' diligence while protecting their own confidential investigations.",
        "One sponsor's unproven suspicion blacklists a charity across the market, or confidential investigations leak.",
        "Shared watch lists among sponsors are rare and contractually fragile; informal sharing occurs by phone.",
        "No statute requires sharing; defamation, antitrust and confidentiality law constrain it.",
        "Inter-sponsor information sharing would require written agreements.",
        "Each sponsor vets independently; vendors sometimes maintain shared databases with mixed provenance.",
        "Typed separation of public-fact holds from private case content prevents propagation by construction.",
        "Registry writes require primary-source re-verification.",
        "Registry entries carry primary-source provenance.",
        "Share only re-verified public facts; keep investigations tenant-private.",
        "Yes, through provenance and tenant-scoped case access tests.",
        "Likely.",
        "If sponsors demand shared risk flags, pressure to weaken the boundary will arise.",
        "Low.", "Low to medium.",
        "Sponsors lose early warning that others' private reviews could provide.",
        ["Prevents one sponsor's suspicion from becoming market-wide exclusion", "Protects investigation confidentiality"],
        ["Fraud rings may exploit lack of shared signals"],
        "stronger", "likely"),
    controls=[CTL("Typed separation of public-fact registry and private investigation cases",
        "Prevent sponsor-private investigation content from reaching the shared registry or other tenants.",
        "preventive-structural", "L2-type-system", ext=["UNB-CTRL-007", "UNB-CTRL-013"], policies=["SEC-AUTH-001"], cwe=["CWE-200"]),
        CTL("Primary-source re-verification of registry updates",
        "Require platform re-verification against the primary source before any shared registry change.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-014"])],
    evrs=[EVR("Registry change provenance and cross-tenant negative tests",
        "Provenance of each shared registry change plus results of negative tests proving private case data does not cross tenants.",
        mech="continuous-automated", prov=["registry fact id", "primary source", "verifier", "originating tenant", "test run id", "time"])])
u["questions"] = [
    Q("cross-sponsor-effects", "If another sponsor on the platform investigates or declines a charity, does that affect our grants to it?",
      "Sponsors want independent decisions.",
      "One sponsor's unverified suspicion affects others.",
      [UNB()], imp="high"),
    Q("what-is-shared", "What charity information is shared across sponsors on the platform, and what remains private to each sponsor?",
      "Sponsors need to know their confidential diligence stays private.",
      "Leakage of confidential investigations or donor patterns.",
      [UNB(), S("SRC-AICPA-TSC", "C1.1")], imp="critical"),
    Q("sponsor-derived-intelligence", "Does the vendor use one sponsor's corrections, decisions or data to improve the shared registry, and under what agreement?",
      "Sponsor-derived intelligence is sponsor data.",
      "Unauthorized secondary use of sponsor data.",
      [UNB()], cls="contractual-common", imp="medium"),
    Q("charity-disputes", "Can a charity see and dispute the facts the registry holds about it?",
      "Fairness and accuracy of charity data.",
      "Persistent errors harm charities.",
      [UNB()], cls="customer-preference", imp="low"),
    Q("investigation-access", "Who can see a sponsor's fraud or sanctions investigation cases, and are they excluded from search and donor-facing views?",
      "Investigations are highly sensitive.",
      "Tipping off or internal misuse.",
      [UNB(), S("SRC-AICPA-TSC", "CC6.1")], imp="high"),
]
units.append(u)

u = AU("identity-quality", "Charity identity resolution, impersonation and data quality",
    "Each organization has an immutable internal identifier independent of EIN, name and address, with legal names, "
    "aliases, historic names, EIN changes, mergers and successor relationships modeled explicitly. Duplicate candidates "
    "are detected deterministically and probabilistically but merged only with confirmation. Impersonation signals "
    "(similar names, mismatched EIN and bank details, suspicious address or bank changes, charity hijacking) open cases. "
    "Legacy sponsor records are imported as unverified claims, and charities can submit evidence through a controlled "
    "verification workflow.",
    "Identity model per UNB-CHAR-001..006, impersonation per UNB-CHAR-028, migration per UNB-CHAR-041, charity workflows per UNB-CHAR-014.",
    "charity identities would be resolved with provenance, duplicate detection and impersonation signals.",
    ["UNB-CHAR-001", "UNB-CHAR-002", "UNB-CHAR-004", "UNB-CHAR-005", "UNB-CHAR-006", "UNB-CHAR-028", "UNB-CHAR-041", "UNB-CHAR-014", "UNB-GRANT-044"],
    impl="high", rec="medium", auto="partial",
    controls=[CTL("Confirmed-merge-only identity resolution",
        "Prevent automatic merges of charity identities without confirmation and preserve all source claims.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-013"]),
        CTL("Impersonation signal detection",
        "Detect similar-name, mismatched EIN and bank, and suspicious change patterns and open cases.",
        "detective-automated", "L6-automated-analysis", ext=["UNB-CTRL-033"])],
    evrs=[EVR("Identity resolution and impersonation case log",
        "Merge decisions, conflicting claims retained, impersonation signals and case outcomes.",
        prov=["charity id", "claim sources", "merge decision", "signal", "case id", "time"])])
u["questions"] = [
    Q("impersonation", "How does the platform detect impostor charities using names or EINs similar to legitimate organizations?",
      "Charity impersonation is a known fraud pattern.",
      "Grants paid to impostors.",
      [UNB(), TCG("reasonably-inferred")], imp="high"),
    Q("mergers-ein-changes", "How are charity mergers, name changes and EIN changes tracked so that history and eligibility remain correct?",
      "Identity changes break naive EIN-keyed systems.",
      "Payments to the wrong or dissolved entity.",
      [UNB(), TEOS()], imp="medium"),
    Q("duplicates", "How are duplicate charity records detected and merged?",
      "Duplicates fragment grant history and diligence.",
      "Inconsistent diligence across duplicate records.",
      [UNB()], imp="low"),
    Q("legacy-import", "When migrating a sponsor's existing grantee records, are legacy approval flags trusted or re-verified?",
      "Legacy data may be stale or wrong.",
      "Importing ineligible charities as approved.",
      [UNB()], imp="medium"),
    Q("charity-evidence-submission", "Can charities submit documents and payment details through a controlled workflow, and how are those submissions verified?",
      "Charity self-service reduces staff work but is an attack surface.",
      "Forged documents or bank details accepted.",
      [UNB()], imp="medium", req=["UNB-GRANT-026"]),
]
units.append(u)

u = AU("decisions", "Sponsor-specific eligibility decisions, overrides and reproducibility",
    "Eligibility is a time-bound, evidence-backed decision for a specific sponsor, program, purpose and date, with "
    "results Eligible, Ineligible, NeedsReview or InsufficientEvidence plus reasons and rule versions. Factual "
    "organization status, sponsor-specific eligibility and payment beneficiary verification are separate. Sponsor "
    "overrides are permitted only within lawful policy boundaries with reason, evidence and approver. Historical "
    "decisions are reproducible from pinned evidence, and state registration status such as the California Attorney "
    "General Registry is shown as a recipient attribute with sponsor-selected hold or warn behavior.",
    "Decision model per UNB-CHAR-018..021, overrides per UNB-CHAR-023, reproducibility per UNB-CHAR-025, state registry per CNV-GRT-015.",
    "eligibility would be a reproducible, sponsor-specific decision record with bounded overrides.",
    ["UNB-CHAR-018", "UNB-CHAR-019", "UNB-CHAR-020", "UNB-CHAR-021", "UNB-CHAR-023", "UNB-CHAR-025", "UNB-CHAR-039", "CNV-GRT-015", "UNB-CHAR-031"],
    impl="medium",
    controls=[CTL("Bounded sponsor override with reason and approver",
        "Permit eligibility overrides only within lawful policy boundaries and record reason, evidence and approver.",
        "preventive-gate", "L3-restricted-interface", ext=["UNB-CTRL-017", "UNB-CTRL-018"])],
    evrs=[EVR("Eligibility decision records and verification packs",
        "Decision results with reasons, rule versions, pinned evidence and Folio-rendered verification packs.",
        fmt="JSON record and PDF", prov=["decision id", "charity id", "sponsor id", "rule version", "evidence ids", "result", "override approver", "time"])])
u["questions"] = [
    Q("decision-model", "Is charity eligibility recorded as a dated, sponsor-specific decision with reasons, or as a global yes or no flag?",
      "Eligibility depends on sponsor policy and purpose.",
      "One sponsor's flags applied to another or decisions without reasons.",
      [UNB()], imp="high"),
    Q("overrides", "Can sponsor staff override an eligibility result, within what limits, and how is that recorded?",
      "Overrides are necessary but risky.",
      "Overrides that create taxable distributions.",
      [UNB(), S("SRC-COSO-2013")], imp="high"),
    Q("exclusion-lists", "Can the sponsor maintain its own exclusion lists and program-specific eligibility rules?",
      "Sponsors have mission and policy exclusions.",
      "Grants contrary to sponsor policy.",
      [UNB()], cls="customer-preference", imp="medium"),
    Q("state-registration", "Does the platform show state charitable registration status (for example California Attorney General Registry status) and let the sponsor act on it?",
      "Some sponsors avoid grants to organizations delinquent in state registration.",
      "Grants to organizations not in good standing with state regulators.",
      [S("SRC-STATE-CHARITABLE-SOLICITATION"), UNB()], cls="customer-preference", imp="low", jur=["US-states"]),
    Q("reproducibility", "Can the sponsor reproduce a past eligibility decision exactly, using the evidence and rules in force at that time?",
      "Audits and disputes test past decisions.",
      "Inability to defend decisions after source data changes.",
      [UNB(), S("SRC-AICPA-TSC", "PI1.5")], imp="high"),
]
units.append(u)
