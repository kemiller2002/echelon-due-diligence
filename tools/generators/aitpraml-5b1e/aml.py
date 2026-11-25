from qbc_aitpraml import Cat, challenge

C = Cat("AML",
        industries=["donor-advised-funds", "nonprofit", "banking", "financial-services", "wealth-management"],
        jurisdictions=["US-federal"],
        products=["unbound"],
        regulatory_authority=None)

OFAC = "SRC-OFAC-REGS"
FW = "SRC-OFAC-COMPLIANCE-FRAMEWORK"
G6 = "SRC-ECH-UNB-BASELINE|CNV-GRT-006"
ALL_PARTIES = "Donors, advisors, successors, grantees and payors"

C.au(1, title="Sanctions screening coverage and timing across parties and the grant lifecycle",
     status="proposed-target-state",
     rationale="CNV-GRT-006 (adopted convergence clause, owner-ratified) requires screening of donors, advisors, successors, grantees and payors at onboarding, automatic delta screening on list updates, and screening before each grant release against the current list version, with dispatch fenced atomically at the irreversible step. UNB-EXT-004 requires screening against legally applicable lists with source freshness and warns against equating name similarity with a match. UNB-RULE-014 blocks grant execution while sanctions status is unresolved. Not implemented. Screening of grantee principals and ownership (50 percent rule) is not specified in located requirements.",
     target=ALL_PARTIES + " are screened at onboarding, re-screened automatically whenever a list changes, and screened again immediately before each irreversible release; a match found during release prevents transmission because the check and the dispatch are one atomic step. Lists include the SDN list and OFAC consolidated non-SDN lists, with other lists (UN, EU, UK) available by sponsor policy. Entity screening covers known owners and principals of grantee organizations where data is available, and the sponsor policy records how the 50 percent rule is addressed. Coverage is complete by construction: no party can be attached to a fund or grant without a screening record.",
     current="Not established.",
     intended="Implement per CNV-GRT-006 and CNV-ARC-003; extend to grantee principals and ownership data.",
     provable="Nothing.",
     statement="Echelon's adopted design screens donors, advisors, successors, grantees and payors at onboarding, on every list update and immediately before each grant release, and blocks release when a potential match is unresolved. Not yet implemented.",
     kind="planned",
     controls=[1, 2], evrs=[1, 2],
     requirements=["CNV-GRT-006", "CNV-ARC-003", "UNB-EXT-004", "UNB-RULE-014", "UNB-LEG-004"],
     freshness="per-event", mechanism="continuous-automated", automation="full",
     impl_cost="medium", rec_cost="low",
     owner="Not assigned (proposed: sponsor compliance officer for policy; Unbound product owner for enforcement)",
     residual=["Ownership data for grantee organizations is often unavailable, limiting 50 percent rule coverage."],
     open=["Which list data provider will be used, and does it include OFAC consolidated non-SDN lists and ownership data?"])

C.au(2, title="Screening list freshness and fail-closed behavior",
     status="proposed-target-state",
     rationale="CNV-GRT-006 requires every release screening to record list version and fetch time, to fail closed when the list is older than a basis-tagged bound or the screening service is unavailable, and to distribute list updates as versioned inter-cell messages covered by the dispatch fence. Not implemented; the freshness bound value is not yet set.",
     target="Echelon ingests official list updates from OFAC (and other configured sources) within a defined bound, verifies integrity of the downloaded data, versions each list snapshot, and triggers delta re-screening of all parties. Every screening records list version and fetch time. If the list is older than the bound or screening is unavailable, releases stop rather than proceed unscreened. Freshness lag is monitored and alerted.",
     current="Not established.",
     intended="Set the freshness bound with the sponsor compliance officer and implement per CNV-GRT-006.",
     provable="Nothing.",
     statement="Echelon's design records the list version used for every screening and stops grant releases if the sanctions list is stale or screening is unavailable. Not yet implemented.",
     kind="planned",
     controls=[3], evrs=[3],
     requirements=["CNV-GRT-006", "UNB-EXT-004"],
     freshness="P1D", mechanism="continuous-automated", automation="full",
     impl_cost="low", rec_cost="low",
     owner="Not assigned (proposed: Unbound product owner)",
     open=["What freshness bound will be set, and on what basis (CNV-GRT-006 requires it to be basis-tagged)?"])

C.au(3, title="Name matching method, threshold tuning, effectiveness testing and subgroup fairness",
     status="proposed-target-state",
     rationale="CNV-GRT-006 requires the matcher to meet a recall target approved by the sponsor compliance officer on a versioned perturbation suite (exact, case and punctuation, dropped character, token reorder, legal suffix, listed names on otherwise clean identifiers) before release and after every matcher or threshold change; no listed name attached to a clean identifier may pass straight through; false-alert rates must be measured by name subgroup including Arabic-origin or Islamic tokens at every change and at least quarterly. It records that the reference matcher in report 14 does not meet this and must not be used in production. Not implemented.",
     target="The matching method (normalization, transliteration, token, phonetic and edit-distance components, secondary identifiers) is documented. Thresholds are approved by the sponsor compliance officer from measured recall on the versioned perturbation suite and false-alert rates by subgroup, and are change-controlled: any change re-runs the suite and blocks release if recall falls below target. Secondary identifiers (date of birth, address, country, EIN) are used to support disposition, not to suppress alerts automatically. AI and machine learning do not close alerts; if used at all they only prioritize review queues and are evaluated like any matcher change.",
     current="Not established. A reference matcher exists in Unbound research materials (report 14) and is recorded as not meeting the recall requirement.",
     intended="Select or build a matcher that meets the perturbation suite, then implement the change gate and subgroup reporting.",
     provable="Nothing.",
     statement="Echelon's design requires its sanctions name matching to meet a compliance-approved recall target on a published perturbation test suite, retested on every change, with false-alert rates measured by name subgroup. No production matcher exists yet.",
     kind="planned",
     controls=[4, 5], evrs=[4, 5],
     requirements=["CNV-GRT-006", "UNB-EXT-004"],
     freshness="P90D", mechanism="event-driven-automated", automation="high",
     impl_cost="medium", rec_cost="low",
     owner="Not assigned (proposed: sponsor compliance officer approves thresholds; Unbound product owner maintains matcher)",
     residual=["Perturbation suites cannot cover every transliteration variant; some true matches may still be missed."],
     challenge=challenge(
         intent="Sponsors and banks want assurance that screening catches listed parties without drowning staff in false alerts or burdening donors and grantees with certain name origins.",
         adverse="A listed party passes screening because of a spelling variant, or legitimate grantees face repeated holds because of their names.",
         conv_eff="Conventional practice relies on a vendor's fuzzy score and a threshold set once; effectiveness is rarely measured, and vendors often do not disclose method or test results.",
         legal="OFAC does not mandate a matching method; it expects risk-based controls and testing (Framework 2019). Liability for dealing with a listed person is strict.",
         contract="Banks may require evidence of screening tuning and testing from service providers.",
         history="Threshold tuning by trial and error and periodic model validation of the screening tool.",
         elim="Not eliminable; matching is inherently probabilistic. The pass-through of listed names on clean identifiers can be eliminated by rule.",
         auto="Release gate re-runs the perturbation suite on every matcher or threshold change.",
         cont="Per-change recall and subgroup false-alert reports; quarterly at minimum.",
         alt="Measured, gated recall against a versioned perturbation suite plus subgroup false-alert reporting, in place of an unvalidated vendor score threshold.",
         verif="Suite, results and thresholds can be reviewed by sponsor compliance, auditors and examiners.",
         accept="Likely among compliance professionals; it exceeds common vendor practice. Some banks will still require their own model validation.",
         invalid="If the perturbation suite is unrepresentative of real list entries and name variants, measured recall overstates real recall.",
         conv_cost="low to medium (vendor tool)",
         alt_cost="medium (suite construction and maintenance)",
         alt_risk="Optimizing to the suite can overfit; the suite must grow from real misses and list changes.",
         pro=["Effectiveness is measured, not assumed.", "Subgroup reporting addresses fairness concerns explicitly."],
         con=["Requires ongoing compliance involvement to approve thresholds.", "Real-world recall is still unknown without production data."],
         tech="stronger", inst="likely"))

C.au(4, title="Alert disposition, blocking and rejecting, and OFAC reporting",
     status="proposed-target-state",
     rationale="CNV-GRT-006 requires confirmed matches to resolve to Block, Reject or Proceed (license or exemption), never automatically to Blocked; block or reject actions to produce 31 CFR 501.603 and 501.604 report data due within 10 business days; blocked property to enter the annual report; potential matches at release to open a disposition task with a sponsor-set due date and escalation, never auto-release; dispositions to record the facts compared and never cite a score as the reason; false-positive dispositions reusable within the deciding sponsor until defined expiry events; donor-facing status to use a neutral catalog without list names or scores. UNB-RCN-REG-003 requires recording blocked property and preventing movement. CNV-GRT-012 requires neutral decline wording. NoAiClearance (EDF) and UNB-AGT-002 bar AI from clearing alerts. Not implemented.",
     target="Potential matches open a disposition task assigned to a qualified sponsor reviewer with a due date and escalation to the compliance officer. Only an authorized human disposes of an alert; AI may assemble evidence but cannot clear. The disposition records the specific facts compared and the reviewer's reasoning; scores are not reasons. True matches resolve to Block, Reject or Proceed under a license, generate report data for filing within 10 business days, and blocked property is held in place and included in the annual report. Prior false-positive dispositions are reused only within the same sponsor and expire on subject or list change, new match, 12 months or reviewer authority revocation. A risk-stratified sample of dispositions receives second-level review. Donors see neutral status only.",
     current="Not established.",
     intended="Implement per CNV-GRT-006, UNB-RCN-REG-003 and CNV-GRT-012.",
     provable="Nothing.",
     statement="Echelon's adopted design requires every potential sanctions match to be disposed of by an authorized human with recorded reasoning, supports blocking, rejecting and OFAC report preparation, and never lets AI clear an alert. Not yet implemented.",
     kind="planned",
     controls=[6, 7], evrs=[6, 7],
     requirements=["CNV-GRT-006", "CNV-GRT-007", "CNV-GRT-012", "UNB-RCN-REG-003", "UNB-AGT-002", "CNV-AIO-002"],
     freshness="per-event", mechanism="event-driven-automated", automation="high",
     impl_cost="medium", rec_cost="medium",
     owner="Not assigned (proposed: sponsor compliance officer)",
     residual=["Disposition quality depends on reviewer skill; the second-level sample is the check."])

C.au(5, title="Sanctions and AML recordkeeping",
     status="proposed-target-state",
     rationale="CNV-PLT-004 requires transaction-level records, screening results, dispositions and license reliance records retained 10 years after the transaction; blocked property records while blocked plus 10 years; legal holds override disposition; and in release 1 a 10-year floor for all transaction-level financial and grant records. SOC2-006 requires append-only records with integrity verification. Not implemented.",
     target="Screening results (with list version and fetch time), alerts, dispositions, license reliance records, blocked and rejected transaction records and reports are retained at least for the periods in CNV-PLT-004, which meet or exceed the OFAC recordkeeping period, in append-only, hash-verified storage. A complete screening history for any party or transaction can be produced for an examiner within a defined time. Retention survives tenant offboarding as required and legal holds override deletion.",
     current="Not established.",
     intended="Implement per CNV-PLT-004 and SOC2-006.",
     provable="Nothing.",
     statement="Echelon's design retains sanctions screening results, dispositions and related transaction records for at least 10 years in tamper-evident storage, producible for examiners. Not yet implemented.",
     kind="planned",
     controls=[8], evrs=[8],
     requirements=["CNV-PLT-004", "SOC2-006", "CNV-GRT-006"],
     freshness="P1D", mechanism="continuous-automated", automation="full",
     impl_cost="low", rec_cost="low",
     owner="Not assigned (proposed: Unbound product owner)",
     open=["Confirm the current OFAC recordkeeping period in 31 CFR 501.601 as of the answer date."])

C.au(6, title="Support for BSA/AML program obligations of bank and broker-dealer sponsors and partners",
     status="requires-external-validation",
     rationale="RR-UNB-PART-007-r1 and UNB-RCN-ENT-014 separate sanctions screening, identity proofing, any customer identification or AML program (enabled only when counsel records that it applies, by law or by contract with a custodian or payment provider) and source-of-funds checks, each with an authority type and owner. CNV-PLT-003 requires risk-based identity proofing. UNB-CHAR-028 and UNB-GRANT-029 require detection of suspicious patterns as signals, not guilt. TVR-CMP-003 notes BSA scope depends on operating model. Whether any BSA program obligation applies to Echelon, to a given sponsor or only to its bank or broker-dealer partners requires counsel determination; Echelon's design (CNV-LEG-001) avoids holding or moving funds.",
     target="Echelon does not itself operate as a BSA financial institution and says so only after counsel confirms it. For sponsors affiliated with or partnered with banks or broker-dealers that must run AML programs, Unbound supports their programs: configurable identity verification and beneficial ownership collection, risk-based monitoring rules that surface unusual patterns (structuring of contributions, rapid pass-through of contributions to grants, unusual grant patterns) as cases for the sponsor's or partner's investigators, case export for SAR decisions made by the responsible institution, strict confidentiality of any SAR-related information with access restricted to named roles, and data and documentation for independent AML testing and examinations. Echelon personnel and AI agents never decide whether to file a SAR.",
     current="Not established; applicability not determined.",
     intended="Obtain counsel determination per RR-UNB-PART-007-r1 for each operating model; build the applicability register UNB-RCN-ENT-014.",
     provable="Nothing.",
     statement="Echelon's design does not hold or move funds and is not intended to make Echelon a BSA financial institution; counsel has not yet confirmed this. Echelon plans to support sponsors' and partners' AML programs with identity verification, monitoring signals and case data, while SAR decisions stay with the responsible institution.",
     kind="not-available",
     controls=[9, 10], evrs=[9, 10],
     requirements=["RR-UNB-PART-007-r1", "UNB-RCN-ENT-014", "CNV-PLT-003", "UNB-CHAR-028", "UNB-GRANT-029", "CNV-LEG-001", "TVR-CMP-003"],
     freshness="per-event", mechanism="event-driven-automated", automation="partial",
     impl_cost="high", rec_cost="medium",
     owner="Not assigned (proposed: Echelon counsel for applicability; sponsor or partner BSA officer for program decisions)",
     open=["Does the FinCEN investment adviser AML rule, as postponed, affect any target customer's expectations of Unbound?",
           "Which target sponsors operate under bank or broker-dealer AML programs that would flow requirements to Unbound?"],
     challenge=challenge(
         intent="Bank and broker-dealer affiliated sponsors need vendors to support their AML programs without creating gaps or tipping-off risks.",
         adverse="Money laundering or terrorist financing through DAF contributions and grants goes undetected, or a SAR is disclosed.",
         conv_eff="Rule-based transaction monitoring generates high false-positive volumes; its effectiveness in the charitable context is not well documented, and DAF sponsors that are not BSA financial institutions often have no monitoring at all.",
         legal="BSA AML program rules bind banks (31 CFR 1020.210) and broker-dealers (31 CFR 1023.210), not charities or software vendors as such. Obligations reach Echelon only by contract or if Echelon's activity made it a financial institution, which its design avoids.",
         contract="Bank and broker-dealer partners commonly flow AML support duties to service providers.",
         history="Vendors expected to run monitoring scenarios like banks.",
         elim="Funds never pass through Echelon (CNV-LEG-001), removing Echelon from the money flow; the responsible institution keeps its program.",
         auto="Deterministic monitoring rules with versioned thresholds generate cases.",
         cont="Case and rule-performance metrics.",
         alt="Signals and evidence delivered to the responsible institution's investigators with clear ownership, instead of Echelon operating an AML program it is not obligated to run.",
         verif="Applicability register, rule definitions and case logs are reviewable.",
         accept="Uncertain; some partners may expect the vendor to operate monitoring end to end.",
         invalid="If counsel finds a BSA obligation applies to Echelon in some operating model, a full program is required.",
         conv_cost="high (vendor-operated AML program)",
         alt_cost="medium",
         alt_risk="Ownership confusion between sponsor, partner and Echelon could leave alerts uninvestigated.",
         pro=["Keeps legal judgments with the obligated institution.", "Avoids Echelon becoming a de facto financial institution."],
         con=["Partners may see it as shifting work back to them.", "Small sponsors without a BSA function will receive signals they cannot act on."],
         tech="equivalent", inst="uncertain"))

C.au(7, title="Charity-specific diligence: Treasury guidelines, foreign grants, prohibited benefits and grant fraud red flags",
     status="proposed-target-state",
     rationale="CNV-GRT-003 requires charity status checks at approval and release against IRS data; CNV-GRT-007 requires versioned reliance on OFAC general licenses and risk-based FCPA diligence for foreign grants; CNV-GRT-008 governs intermediaries and foreign paths and forbids naming specific foreign organizations to intermediaries; CNV-GRT-009 forbids payments benefiting donors, advisors, family or 35 percent controlled entities; CNV-GRT-011 routes risk signals (donor benefit, supporting organizations, intermediaries with country preference, equivalency-based foreign recipients, unusual size or restrictions) to Tier 2 review; UNB-CHAR-028 detects impersonation and suspicious bank changes; UNB-GRANT-029 detects split or repeated grants; UNB-GRANT-041 allows international grants only through separately approved frameworks; CNV-PLT-011 notifies prior channels of contact changes. Not implemented.",
     target="Grantee due diligence follows a risk-based approach informed by Treasury's voluntary anti-terrorist financing guidelines for charities: verify legal status and identity against IRS data at approval and release, screen the organization and known principals, and apply enhanced review to higher-risk grants. Foreign grants are disabled until a sponsor enables an approved framework (equivalency determination or expenditure responsibility, sanctions and license reliance, FCPA diligence, staged payments, use reporting). Red flags route to Tier 2 human review: donor or family benefit (IRC 4967), grants to related parties, intermediaries with stated country or program preferences (earmarking), split or rapid pass-through grants, newly changed bank details, impersonation indicators. Payee bank changes require verification through an independent channel and notice to the prior channel. AI may surface signals; only humans or sponsor-approved deterministic rules decide.",
     current="Not established.",
     intended="Implement per the cited convergence clauses.",
     provable="Nothing.",
     statement="Echelon's adopted design checks grantee status at approval and release, routes prohibited-benefit, earmarking, fraud and foreign-grant risk signals to human review, and keeps foreign grants disabled until a sponsor enables an approved diligence framework. Not yet implemented.",
     kind="planned",
     controls=[11, 12], evrs=[11, 12],
     requirements=["CNV-GRT-003", "CNV-GRT-007", "CNV-GRT-008", "CNV-GRT-009", "CNV-GRT-011", "UNB-CHAR-028", "UNB-GRANT-029", "UNB-GRANT-041", "CNV-PLT-011", "UNB-REM-014"],
     freshness="per-event", mechanism="event-driven-automated", automation="high",
     impl_cost="medium", rec_cost="medium",
     owner="Not assigned (proposed: sponsor grants and compliance officers)",
     residual=["Earmarking through intermediaries can be hidden in off-platform communications."])

# ---------------- Controls ----------------
C.ctl(1, title="Screening record required for every party and grant",
      objective="No donor, advisor, successor, grantee or payor can be attached to a fund or grant without a current screening record; delta re-screening runs on every list update.",
      type="preventive-structural", level="L2-type-system",
      systems=["Unbound screening service and grant workflow (designed, not built)"],
      related=["CNV-GRT-006", "UNB-RULE-014", "UNB-CTRL-031"],
      refs=[f"{FW}|Internal Controls|d", f"{OFAC}||r", "SRC-TREASURY-CHARITY-GUIDELINES||r"],
      evrs=[1], owner="Not assigned (proposed: Unbound product owner)")
C.ctl(2, title="Atomic screening fence at irreversible release",
      objective="The final screening check against the current list version and the release step execute atomically so a match found during release prevents transmission.",
      type="preventive-structural", level="L3-restricted-interface",
      systems=["Unbound dispatch fence (designed, not built)"],
      related=["CNV-GRT-006", "CNV-ARC-003", "UNB-CTRL-049"],
      refs=[f"{FW}|Internal Controls|r"],
      evrs=[2], owner="Not assigned (proposed: Unbound platform owner)")
C.ctl(3, title="List ingestion, versioning and fail-closed freshness bound",
      objective="Official lists are ingested and integrity-checked within a set bound, versioned, and trigger re-screening; releases fail closed when the list is stale or screening is unavailable.",
      type="preventive-gate", level="L9-runtime-monitored",
      systems=["not yet assigned"],
      related=["CNV-GRT-006", "UNB-EXT-004"],
      refs=[f"{FW}|Internal Controls|r", f"{OFAC}||r"],
      evrs=[3], owner="Not assigned (proposed: Unbound product owner)")
C.ctl(4, title="Perturbation-suite recall gate for matcher and threshold changes",
      objective="Any matcher or threshold change re-runs the versioned perturbation suite; release is blocked if recall falls below the compliance-approved target or a listed name on a clean identifier passes.",
      type="preventive-gate", level="L7-property-tested",
      systems=["not yet assigned"],
      related=["CNV-GRT-006"],
      refs=[f"{FW}|Testing and Auditing|r", "SRC-SR-11-7||r"],
      evrs=[4], owner="Not assigned (proposed: Unbound product owner)")
C.ctl(5, title="Subgroup false-alert measurement",
      objective="False-alert rates by name subgroup are measured at each matcher change and at least quarterly and reported to the sponsor compliance officer.",
      type="detective-automated", level="L6-automated-analysis",
      systems=["not yet assigned"],
      related=["CNV-GRT-006"],
      refs=["SRC-NIST-AI-RMF-1.0|MEASURE 2.11|r"],
      evrs=[5], owner="Not assigned (proposed: sponsor compliance officer)")
C.ctl(6, title="Human-only disposition with recorded facts (NoAiClearance)",
      objective="Only authorized human reviewers can dispose of potential matches; dispositions record the facts compared; AI and scores cannot clear; prior dispositions are reused only within sponsor and expiry rules.",
      type="preventive-structural", level="L2-type-system",
      systems=["Unbound case management (designed, not built)"],
      related=["CNV-GRT-006", "UNB-AGT-002", "UNB-CTRL-032"],
      refs=[f"{FW}|Internal Controls|d"],
      evrs=[6], owner="Not assigned (proposed: sponsor compliance officer)")
C.ctl(7, title="Block, reject and report workflow with second-level review",
      objective="True matches resolve to Block, Reject or Proceed under license; report data is prepared within 10 business days; blocked property is held and included in the annual report; a risk-stratified sample of dispositions is reviewed by a second person.",
      type="corrective", level="L10-external-or-manual",
      systems=["not yet assigned"],
      related=["CNV-GRT-006", "UNB-RCN-REG-003", "CNV-GRT-007", "UNB-CTRL-033"],
      refs=[f"{OFAC}|31 CFR 501.603|d", f"{OFAC}|31 CFR 501.604|d", f"{FW}|Testing and Auditing|r"],
      evrs=[7], owner="Not assigned (proposed: sponsor compliance officer)")
C.ctl(8, title="Tamper-evident sanctions recordkeeping with 10-year floor",
      objective="Screening, disposition, license reliance, blocked and rejected records are retained per CNV-PLT-004 in append-only, hash-verified storage with legal hold precedence.",
      type="preventive-structural", level="L3-restricted-interface",
      systems=["not yet assigned"],
      related=["CNV-PLT-004", "SOC2-006"],
      refs=[f"{OFAC}|31 CFR 501.601|r", "SRC-NIST-SP800-53-R5|AU-9|r"],
      evrs=[8], owner="Not assigned (proposed: Unbound product owner)")
C.ctl(9, title="Identity regime applicability register",
      objective="Per sponsor, role and channel, sanctions, identity proofing, CIP or AML and source-of-funds obligations are recorded with authority type, owner and counsel status; AML features enable only when counsel records applicability.",
      type="administrative", level="L10-external-or-manual",
      systems=["not yet assigned"],
      related=["UNB-RCN-ENT-014", "RR-UNB-PART-007-r1"],
      refs=["SRC-BSA-AML||r", "SRC-FINCEN-CDD-RULE||r"],
      evrs=[9], owner="Not assigned (proposed: Echelon counsel)")
C.ctl(10, title="Monitoring signals and restricted SAR-support case export",
       objective="Deterministic rules surface unusual contribution and grant patterns as cases for the responsible institution; case export for SAR decisions is restricted to named roles and logged; Echelon staff and agents do not decide SAR filing.",
       type="detective-automated", level="L6-automated-analysis",
       systems=["not yet assigned"],
       related=["UNB-CHAR-028", "UNB-GRANT-029"],
       refs=["SRC-BSA-AML|31 CFR 1020.320|r", "SRC-BSA-AML|31 CFR 1023.320|r"],
       evrs=[10], owner="Not assigned (proposed: partner BSA officer)")
C.ctl(11, title="Grantee status and identity verification at approval and release",
       objective="Grantee legal status is checked against IRS data at approval and release; organizations and known principals are screened; payee bank changes require independent-channel verification and prior-channel notice.",
       type="preventive-gate", level="L5-build-release-gate",
       systems=["not yet assigned"],
       related=["CNV-GRT-003", "CNV-PLT-011", "UNB-CHAR-028", "UNB-CTRL-016"],
       refs=["SRC-IRS-TEOS||d", "SRC-TREASURY-CHARITY-GUIDELINES||r"],
       evrs=[11], owner="Not assigned (proposed: sponsor grants officer)")
C.ctl(12, title="Tier 2 routing of DAF-specific red flags and foreign-grant framework gate",
       objective="Prohibited-benefit, related-party, earmarking, split or pass-through, impersonation and foreign-grant signals route to human Tier 2 review; foreign grants stay disabled until an approved framework is enabled by the sponsor.",
       type="preventive-gate", level="L5-build-release-gate",
       systems=["not yet assigned"],
       related=["CNV-GRT-009", "CNV-GRT-011", "CNV-GRT-007", "CNV-GRT-008", "UNB-GRANT-041", "UNB-CTRL-028"],
       refs=["SRC-IRC-4967||d", "SRC-IRC-4966||d", "SRC-TREASURY-CHARITY-GUIDELINES||r"],
       evrs=[12], owner="Not assigned (proposed: sponsor compliance officer)")

# ---------------- Evidence ----------------
C.evr(1, title="Screening coverage report", description="Parties and grants with their latest screening record, list version and time; any entity lacking a screening record (expected zero).",
      mechanism="continuous-automated", freshness="P1D", format="Report", disclosure="customer-only",
      fields=["partyId", "role", "listVersion", "screenedAt", "result"])
C.evr(2, title="Release fence records", description="Per release: final screening result, list version, fence outcome and any prevented transmissions.",
      mechanism="continuous-automated", freshness="per-event", format="Append-only event log", disclosure="customer-only")
C.evr(3, title="List ingestion and freshness log", description="Per list update: publication time, ingestion time, integrity check result, version id, re-screening run, and fail-closed events.",
      mechanism="continuous-automated", freshness="P1D", format="Event log", disclosure="customer-only")
C.evr(4, title="Matcher validation report", description="Perturbation suite version, matcher and threshold versions, recall by perturbation type, pass-through test result, approver.",
      mechanism="event-driven-automated", freshness="per-event", format="Report with suite hash", disclosure="customer-only")
C.evr(5, title="Subgroup false-alert report", description="False-alert rates by name subgroup at each change and quarterly.",
      mechanism="periodic-automated", freshness="P90D", format="Report", disclosure="customer-only")
C.evr(6, title="Disposition records", description="Per alert: reviewer, authority, facts compared, decision, timestamps, reuse and expiry of prior dispositions.",
      mechanism="continuous-automated", freshness="per-event", format="Case record", disclosure="customer-only",
      fields=["alertId", "reviewerId", "authorityRef", "factsCompared", "decision", "decidedAt"])
C.evr(7, title="Blocking, rejection and report packages", description="Block or reject decisions with prepared report data, filing due dates and filing confirmation; annual blocked property report data; second-level review samples.",
      mechanism="event-driven-automated", freshness="per-event", format="Report data and case records", disclosure="customer-only")
C.evr(8, title="Sanctions record retention verification", description="Retention configuration, hash-chain verification results and legal hold status for sanctions records.",
      mechanism="periodic-automated", freshness="P30D", format="Verification report", disclosure="auditor-only")
C.evr(9, title="Identity regime applicability determinations", description="Register rows per sponsor, role and channel with authority type, owner and counsel status.",
      mechanism="periodic-manual", freshness="P1Y", format="Register", disclosure="nda")
C.evr(10, title="Monitoring rule definitions and case export log", description="Versioned monitoring rules, generated cases and access log for SAR-support exports.",
       mechanism="event-driven-automated", freshness="per-event", format="Rule repository and access log", disclosure="auditor-only")
C.evr(11, title="Grantee verification records", description="Per grant: IRS status check results at approval and release, grantee and principal screening, bank change verification records.",
       mechanism="event-driven-automated", freshness="per-event", format="Grant evidence record", disclosure="customer-only")
C.evr(12, title="Tier 2 routing and foreign-grant framework records", description="Signals raised, Tier 2 decisions, sponsor framework enablement records and license reliance versions.",
       mechanism="event-driven-automated", freshness="per-event", format="Case records", disclosure="customer-only")

# ---------------- Questions ----------------
DAF = ["donor-advised-funds", "nonprofit"]
C.q(1, "Screening coverage", "Which parties do you screen against OFAC sanctions lists: donors, advisors, successors, grantee organizations, grantee principals, payees and payors?",
    "Every party with an interest in funds or a grant is a sanctions exposure point.",
    "A blocked person participates as an unscreened role.",
    [G6, f"{OFAC}||d", f"{FW}|Internal Controls|d", "SRC-TREASURY-CHARITY-GUIDELINES||r"],
    "legal-regulatory", "critical", authority="OFAC",
    scope="OFAC prohibitions bind the sponsor and Echelon as US persons; screening is the conventional means of compliance.",
    alts=["Describe your OFAC screening program.", "Are all transaction parties screened against the SDN list?"])
C.q(1, "Screening timing", "When is screening performed: at onboarding, whenever lists change, and before each disbursement?",
    "Lists change daily; one-time screening goes stale.",
    "A party designated after onboarding receives a grant.",
    [G6, f"{FW}|Internal Controls|d"],
    "industry-convention", "critical")
C.q(1, "Release-time screening", "Is screening performed at the moment of an irreversible disbursement, and can a match found during release stop the payment?",
    "The gap between approval and payment is when new designations slip through.",
    "Payment to a party designated between approval and release.",
    [G6, "SRC-ECH-UNB-BASELINE|CNV-ARC-003"],
    "customer-preference", "high")
C.q(1, "Lists covered", "Which lists do you screen against, for example the SDN list, OFAC consolidated non-SDN lists, and UN, EU or UK lists?",
    "List scope determines what can be detected.",
    "Prohibited party on an unscreened list.",
    [f"{OFAC}||d", "SRC-ECH-UNB-BASELINE|UNB-EXT-004"],
    "legal-regulatory", "high", jurisdictions=["US-federal", "EU", "UK"], authority="OFAC; EU and UK sanctions authorities",
    scope="Non-US lists bind only where the customer or transaction is subject to those regimes.")
C.q(1, "Ownership rule", "How do you address the OFAC 50 percent rule for entities owned by blocked persons when screening grantees and other organizations?",
    "Entities owned 50 percent or more by blocked persons are blocked even if unlisted.",
    "Grant to an unlisted entity that is blocked by ownership.",
    [f"{OFAC}||d", f"{FW}|Risk Assessment|r"],
    "legal-regulatory", "medium", authority="OFAC")
C.q(1, "Principals and beneficial owners", "Do you screen the officers, directors and bank account holders of grantee organizations, or only organization names?",
    "Listed individuals can control otherwise clean organizations.",
    "Funds reach a listed individual through an organization.",
    ["SRC-TREASURY-CHARITY-GUIDELINES||d", f"{FW}|Internal Controls|r"],
    "industry-convention", "medium", industries=DAF)

C.q(2, "List freshness", "How quickly after OFAC publishes a list update is it applied to your screening?",
    "Delay between designation and screening is exposure time.",
    "Payment to a newly designated party during the lag.",
    [G6, f"{FW}|Internal Controls|d"],
    "industry-convention", "high")
C.q(2, "List version evidence", "Does each screening result record which list version was used and when it was fetched?",
    "Proving a screen was current requires the version.",
    "Inability to demonstrate screening adequacy to an examiner.",
    [G6],
    "customer-preference", "medium")
C.q(2, "Fail-closed", "What happens to disbursements if the list data is stale or the screening service is unavailable?",
    "Failing open turns an outage into a sanctions violation.",
    "Unscreened payments during outages.",
    [G6, f"{FW}|Internal Controls|r"],
    "customer-preference", "high")
C.q(2, "List source integrity", "Where do you obtain list data, and how do you verify its integrity and completeness?",
    "Corrupted or partial list data silently reduces coverage.",
    "Screening against incomplete data.",
    ["SRC-ECH-UNB-BASELINE|UNB-EXT-004", f"{OFAC}||r"],
    "customer-preference", "low")

C.q(3, "Matching method", "What name matching method do you use, including fuzzy, phonetic and transliteration handling, and how are match thresholds set?",
    "Method and thresholds determine both misses and false alerts.",
    "Listed parties missed by exact-only matching or overwhelmed reviewers.",
    [G6, f"{FW}|Internal Controls|d"],
    "industry-convention", "high",
    alts=["Describe your fuzzy logic settings for sanctions screening."])
C.q(3, "Effectiveness testing", "How do you test that screening actually catches listed names and their variants, and who approves the results?",
    "Screening effectiveness is rarely measured.",
    "Undetected gaps in matching.",
    [G6, f"{FW}|Testing and Auditing|d"],
    "industry-convention", "high")
C.q(3, "Tuning change control", "Are changes to matching logic or thresholds change-controlled, tested and approved before use?",
    "Threshold changes made to reduce alert volume can open gaps.",
    "Silent loss of recall after tuning.",
    [G6, f"{FW}|Testing and Auditing|r", "SRC-SR-11-7||r"],
    "industry-convention", "medium")
C.q(3, "Subgroup fairness", "Do you measure false-alert rates by name origin or other subgroups to detect disproportionate impact on particular donors or grantees?",
    "Name matching can burden people with certain names disproportionately.",
    "Discriminatory delays and reputational harm.",
    [G6, "SRC-NIST-AI-RMF-1.0|MEASURE 2.11|r"],
    "customer-preference", "medium", industries=DAF + ["banking"])
C.q(3, "Secondary identifiers", "How are secondary identifiers such as date of birth, address, country and EIN used in screening and alert resolution?",
    "Secondary data improves precision but can wrongly suppress true matches.",
    "True match suppressed because a secondary field differed.",
    [G6, f"{FW}|Internal Controls|r"],
    "industry-convention", "medium")
C.q(3, "AI in screening", "Is AI or machine learning used in matching or alert scoring, and can it ever close an alert on its own?",
    "Automated clearance of sanctions alerts removes human accountability.",
    "True match closed by a model.",
    ["SRC-ECH-UNB-BASELINE|UNB-AGT-002", "SRC-ECH-UNB-BASELINE|RR-UNB-AI-STD-003-r1", "SRC-SR-11-7||r"],
    "customer-preference", "critical")

C.q(4, "Alert review", "Who reviews potential sanctions matches, what qualifications and authority do they have, and within what timeframe?",
    "Disposition quality depends on reviewer competence and timeliness.",
    "Untimely or unqualified dispositions.",
    [G6, f"{FW}|Training|r", f"{FW}|Management Commitment|r"],
    "industry-convention", "high")
C.q(4, "Disposition records", "What does a disposition record contain, and does it show the facts the reviewer compared rather than a score?",
    "Examiners test whether dispositions are reasoned.",
    "Indefensible clearance of an alert.",
    [G6, f"{FW}|Internal Controls|r"],
    "industry-convention", "high")
C.q(4, "Block, reject and report", "When a true match is confirmed, how are funds blocked or a transaction rejected, and how are the required reports to OFAC prepared within 10 business days?",
    "Blocking and reporting are legal obligations with deadlines.",
    "Late or missing OFAC reports; improper release of blocked property.",
    [f"{OFAC}|31 CFR 501.603|d", f"{OFAC}|31 CFR 501.604|d", G6, "SRC-ECH-UNB-BASELINE|UNB-RCN-REG-003"],
    "legal-regulatory", "critical", authority="OFAC",
    scope="Reporting obligations fall on the holder of blocked property or the party rejecting the transaction (the sponsor); Echelon supports preparation.")
C.q(4, "Disposition reuse", "Do you reuse previous false-positive decisions for repeat matches, and when do those decisions expire?",
    "Reuse cuts workload but can hide changes.",
    "A changed list entry or party passes on a stale clearance.",
    [G6],
    "customer-preference", "medium")
C.q(4, "Donor-facing status", "What does a donor see when a grant is held for sanctions review?",
    "Disclosing list details can tip off parties and expose reviewers.",
    "Tipping off or reputational harm from disclosed suspicion.",
    [G6, "SRC-ECH-UNB-BASELINE|CNV-GRT-012"],
    "customer-preference", "medium", industries=DAF)
C.q(4, "Quality assurance", "Is there a second-level review or quality sample of sanctions dispositions?",
    "Independent checks catch reviewer error.",
    "Systematic disposition errors undetected.",
    [f"{FW}|Testing and Auditing|d"],
    "industry-convention", "medium")

C.q(5, "Retention", "How long do you retain screening results, alert dispositions and blocked or rejected transaction records?",
    "OFAC and examiners require records over long periods.",
    "Inability to evidence past screening.",
    [f"{OFAC}|31 CFR 501.601|d", "SRC-ECH-UNB-BASELINE|CNV-PLT-004"],
    "legal-regulatory", "high", authority="OFAC")
C.q(5, "Examination production", "Can you produce the complete screening history for a given party or transaction for an examiner or auditor?",
    "Look-back requests are common in examinations.",
    "Incomplete response to an examiner.",
    ["SRC-ECH-UNB-BASELINE|CNV-PLT-004", f"{FW}|Testing and Auditing|r"],
    "customer-preference", "medium")
C.q(5, "Record integrity", "Are screening and disposition records protected from alteration after the fact?",
    "Altered records destroy evidentiary value.",
    "Backdated or edited dispositions.",
    ["SRC-ECH-UNB-SOC2-DIRECTIVE|SOC2-006", "SRC-NIST-SP800-53-R5|AU-9|r"],
    "customer-preference", "medium")

C.q(6, "BSA applicability", "Are you subject to Bank Secrecy Act anti-money laundering program requirements yourself?",
    "The customer needs to know whether the vendor has independent AML obligations.",
    "Misunderstood allocation of AML responsibilities.",
    ["SRC-BSA-AML||d", "SRC-ECH-UNB-BASELINE|CNV-LEG-001"],
    "legal-regulatory", "medium", authority="FinCEN",
    scope="Depends on whether Echelon's activities make it a financial institution under 31 CFR Chapter X; the Unbound design avoids holding or transmitting funds.")
C.q(6, "CIP and CDD support", "Can your platform support our customer identification and customer due diligence requirements, including beneficial ownership for entity donors?",
    "Bank and broker-dealer affiliated programs must apply CIP and CDD to account holders.",
    "Accounts opened without required identification.",
    ["SRC-FINCEN-CDD-RULE|31 CFR 1010.230|d", "SRC-BSA-AML|31 CFR 1020.220|r", "SRC-BSA-AML|31 CFR 1023.220|r", "SRC-ECH-UNB-BASELINE|RR-UNB-PART-007-r1"],
    "legal-regulatory", "high", industries=["banking", "financial-services", "donor-advised-funds"], authority="FinCEN; federal banking agencies; SEC; FINRA",
    scope="Binding on the bank or broker-dealer customer; flows to Echelon by contract.")
C.q(6, "Suspicious activity monitoring", "Do you monitor for suspicious activity, such as structured contributions or rapid pass-through to grants, and how are alerts provided to us for SAR decisions?",
    "Monitoring supports the obligated institution's SAR program.",
    "Laundering through DAF accounts undetected.",
    ["SRC-BSA-AML|31 CFR 1020.320|r", "SRC-BSA-AML|31 CFR 1023.320|r", "SRC-ECH-UNB-BASELINE|UNB-GRANT-029"],
    "contractual-common", "high", industries=["banking", "financial-services", "donor-advised-funds"])
C.q(6, "SAR confidentiality", "How do you protect the confidentiality of any suspicious activity information, and prevent tipping off, in your platform and among your personnel?",
    "SAR confidentiality is a legal requirement for the filing institution.",
    "Unlawful disclosure of SAR existence.",
    ["SRC-BSA-AML||d", "SRC-ECH-UNB-BASELINE|CNV-GRT-012"],
    "legal-regulatory", "high", industries=["banking", "financial-services"], authority="FinCEN",
    scope="SAR confidentiality binds the filing institution and those it shares SAR information with.")
C.q(6, "AML testing support", "Will you support our independent AML testing and regulatory examinations with data, documentation and access?",
    "Independent testing must cover outsourced components.",
    "AML program testing gaps.",
    ["SRC-BSA-AML|31 CFR 1020.210|r", "SRC-FINRA-RN-21-29||r", "SRC-INTERAGENCY-TPRM-2023||r"],
    "contractual-common", "medium", industries=["banking", "financial-services"])

C.q(7, "Charity due diligence", "Do you support grantee due diligence consistent with Treasury's anti-terrorist financing guidelines for U.S.-based charities?",
    "Sponsors use the guidelines as the reference for risk-based grantee diligence.",
    "Grants diverted to terrorist financing.",
    ["SRC-TREASURY-CHARITY-GUIDELINES||d", "SRC-ECH-UNB-BASELINE|CNV-GRT-003"],
    "industry-convention", "high", industries=DAF)
C.q(7, "Foreign grants", "For grants to foreign organizations or through intermediaries, what diligence is supported, such as equivalency determination or expenditure responsibility, sanctions licenses and anti-corruption checks?",
    "Foreign grants carry elevated legal and sanctions risk.",
    "Taxable distribution, sanctions violation or corruption exposure.",
    ["SRC-IRC-4966||d", "SRC-ECH-UNB-BASELINE|CNV-GRT-007", "SRC-ECH-UNB-BASELINE|UNB-GRANT-041", "SRC-TREASURY-CHARITY-GUIDELINES||r"],
    "legal-regulatory", "high", industries=DAF, jurisdictions=["US-federal", "global"], authority="IRS; OFAC; DOJ and SEC (FCPA)")
C.q(7, "Prohibited benefits", "Do you treat donor-directed benefits, such as grants that pay a donor's personal pledge, tuition, event tickets or a related organization's expenses, as red flags for misuse of the fund, and how are they escalated?",
    "Prohibited benefits trigger excise taxes and reputational harm.",
    "IRC 4967 excise tax and donor misconduct.",
    ["SRC-IRC-4967||d", "SRC-IRC-4958||r", "SRC-ECH-UNB-BASELINE|CNV-GRT-009", "SRC-ECH-UNB-BASELINE|CNV-GRT-011"],
    "legal-regulatory", "high", industries=DAF, authority="IRS",
    scope="Tax liabilities fall on donors, advisors and fund managers; Echelon supports detection.")
C.q(7, "Structuring and pass-through", "Do you detect patterns such as split grants, repeated grants to the same recipient, or contributions quickly followed by grants that may indicate layering?",
    "DAFs can be misused to move funds with charitable cover.",
    "Laundering or circumvention through rapid in-and-out activity.",
    ["SRC-ECH-UNB-BASELINE|UNB-GRANT-029", "SRC-ECH-UNB-BASELINE|CNV-GOV-007"],
    "customer-preference", "medium", industries=DAF)
C.q(7, "Impersonation and payee changes", "How do you detect charity impersonation and verify changes to a grantee's bank account or contact details?",
    "Payee changes are the most common grant fraud vector.",
    "Grant diverted to a fraudster's account.",
    ["SRC-ECH-UNB-BASELINE|UNB-CHAR-028", "SRC-ECH-UNB-BASELINE|CNV-PLT-011", "SRC-NACHA-FRAUD-MONITORING-2026||r"],
    "customer-preference", "critical", industries=DAF)
C.q(7, "Earmarking through intermediaries", "How do you prevent grants to intermediaries from being earmarked for a specific foreign organization chosen by the donor?",
    "Earmarking can defeat foreign grant rules and sanctions controls.",
    "Taxable distribution or sanctions exposure via an intermediary.",
    ["SRC-ECH-UNB-BASELINE|CNV-GRT-008", "SRC-IRC-4966||r"],
    "legal-regulatory", "medium", industries=DAF, authority="IRS")
