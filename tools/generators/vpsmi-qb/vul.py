from common import *

def build():
    c = Cat("VUL")
    # Evidence requirements
    e1 = c.evr(1, "Vulnerability register with lifecycle timestamps",
               "Machine-readable register of every identified vulnerability: source, affected component and release hash, CVSS v4 vector, EPSS score and date, KEV membership, reachability determination, assigned SLA, owner, status transitions with timestamps, remediation commit and retest result.",
               "not yet assigned", "continuous-automated", "P1D",
               fmt="JSON Lines or SARIF-derived records", prov=["finding id", "source tool and version", "component purl", "release hash", "detected_at", "status history", "actor"],
               signing="Proposed: signed export per reporting period", retention="Not established; set with auditor and counsel (SOC2-023)")
    e2 = c.evr(2, "Remediation SLA performance report",
               "Periodic report of remediation within SLA by severity, aging of open findings, KEV items and overdue counts, with raw denominators and excluded items listed separately.",
               "not yet assigned", "periodic-automated", "P30D", disclosure="nda")
    e3 = c.evr(3, "Vulnerability exception register",
               "Each exception with scope, risk rationale, compensating controls, approver distinct from requester, expiry date, and review outcome; expired exceptions flagged automatically.",
               "not yet assigned", "event-driven-automated", "per-event", disclosure="customer-only")
    e4 = c.evr(4, "Published vulnerability disclosure policy and security.txt",
               "Public disclosure policy (scope, safe harbor, reporting channel, acknowledgment targets) and security.txt files with current contact and expiry on each Echelon domain; automated check that expiry has not lapsed.",
               "not yet assigned", "periodic-automated", "P30D", disclosure="public")
    e5 = c.evr(5, "External report intake log",
               "Log of external researcher reports: received time, acknowledgment time, triage decision, linked register entry, disclosure coordination and closure.",
               "not yet assigned", "event-driven-automated", "per-event", disclosure="internal")
    e6 = c.evr(6, "Customer vulnerability advisory and VEX record",
               "Advisories and VEX statements issued to customers, with affected releases, exploitability status, timestamps of issue and customer acknowledgment.",
               "not yet assigned", "event-driven-automated", "per-event", disclosure="customer-only")
    e7 = c.evr(7, "Deployed component patch currency report",
               "Report comparing deployed runtime, database engine, base image and OS versions against latest security releases and vendor support windows, generated from deployment manifests rather than self-attestation.",
               "not yet assigned", "continuous-automated", "P1D")
    e8 = c.evr(8, "AI-authored remediation verification record",
               "For each fix authored or proposed by an AI agent: agent identity, task authorization, diff hash, independent human or second-tool review, regression and security test results, and gate outcome.",
               "Praxis (work protocol and provenance records exist as tooling; not yet operated for a production Echelon service)",
               "event-driven-automated", "per-event", disclosure="nda")

    # Controls
    k1 = c.ctl(1, "Inventory-driven vulnerability identification",
               "Every deployed component, derived from build manifests and SBOMs, is continuously matched against vulnerability sources; components absent from the inventory are detected as gaps rather than silently excluded.",
               "detective-automated", "L6-automated-analysis", ["not yet assigned (candidate: SCA tooling such as OSV-Scanner or Trivy fed by build SBOMs)"], [e1, e7],
               policies=["SEC-SUPPLY-001"], related=["SOC2-016"],
               fw=[R("SRC-NIST-SP800-53-R5", "RA-5"), R("SRC-CSA-CCM-V4", "TVM-07"), R("SRC-CIS-CONTROLS-V8.1", "7.1")],
               residual=["Advisory databases lag disclosure; F# and niche NuGet packages may have sparse advisory coverage."])
    k2 = c.ctl(2, "Risk-based prioritization with exploitation signals",
               "Findings are prioritized using CVSS v4.0 with environmental metrics, EPSS likelihood and KEV membership, with documented reachability determinations reviewed by someone other than the fixing engineer.",
               "preventive-procedural", "L6-automated-analysis", ["not yet assigned"], [e1],
               fw=[D("SRC-CVSS-4.0"), D("SRC-FIRST-EPSS"), D("SRC-CISA-KEV"), R("SRC-CSA-CCM-V4", "TVM-08")])
    k3 = c.ctl(3, "Remediation SLA enforcement and release gate",
               "Open findings past SLA, and any KEV finding in a release candidate, block release unless covered by an unexpired approved exception.",
               "preventive-gate", "L5-build-release-gate", ["Praxis (candidate release gate host; not yet configured for this control)"], [e2, e3],
               policies=["SEC-SUPPLY-001"], related=["SOC2-016", "CNV-PLT-010"],
               fw=[R("SRC-CSA-CCM-V4", "TVM-03"), R("SRC-NIST-SP800-53-R5", "SI-2")])
    k4 = c.ctl(4, "Time-limited, separately approved vulnerability exceptions",
               "Exceptions are explicit, narrowly scoped, time-limited, approved by an accountable reviewer other than the requester, carry compensating controls and expire automatically; AI agents cannot approve or extend them.",
               "preventive-procedural", "L5-build-release-gate", ["not yet assigned"], [e3],
               related=["SOC2-033", "SOC2-017"], fw=[D("SRC-ECH-SCS-0.1", "Enforcement model", "derived-from")])
    k5 = c.ctl(5, "Coordinated vulnerability disclosure intake",
               "A published policy, security.txt and monitored channel receive external reports, which enter the same register and SLA process as internal findings.",
               "administrative", "L10-external-or-manual", ["not yet assigned"], [e4, e5],
               fw=[D("SRC-ISO-29147-30111"), D("SRC-NIST-CSF-2.0", "ID.RA-08"), D("SRC-NIST-SP800-53-R5", "RA-5(11)")])
    k6 = c.ctl(6, "Customer vulnerability notification and VEX",
               "Customers are notified of vulnerabilities affecting their tenant or release, and receive VEX statements for components determined not affected.",
               "corrective", "L10-external-or-manual", ["not yet assigned"], [e6],
               fw=[D("SRC-OPENVEX"), R("SRC-CSA-CCM-V4", "TVM-09")])
    k7 = c.ctl(7, "Rebuild-and-redeploy patching of platform components",
               "Runtime, database engine, base image and OS security updates are applied by rebuilding immutable artifacts and redeploying; deployed versions are continuously compared to the patched baseline and to vendor support windows.",
               "corrective", "L9-runtime-monitored", ["not yet assigned"], [e7],
               fw=[R("SRC-CIS-CONTROLS-V8.1", "7.3"), R("SRC-CIS-CONTROLS-V8.1", "7.4"), R("SRC-CIS-CONTROLS-V8.1", "2.2")])
    k8 = c.ctl(8, "Independent verification of AI-authored fixes",
               "Fixes authored by AI agents require review by a different principal and passing security regression tests; agents cannot modify the gate, the finding status or the exception register.",
               "preventive-gate", "L5-build-release-gate", ["Praxis (provenance and work records exist; enforcement for this control not implemented)"], [e8],
               related=["SOC2-017", "CNV-PLT-010"], fw=[R("SRC-NIST-SP800-218A"), R("SRC-OWASP-AGENTIC-AI")])

    ch_prio = challenge(
        customer_intent="Customers want assurance that exploitable weaknesses are fixed before attackers use them.",
        adverse_outcome="Compromise through a known, exploited vulnerability left open because it was scored medium, or effort wasted on unreachable critical-scored findings.",
        conventional_control_effectiveness="CVSS base score alone is a severity measure, not a risk measure; FIRST itself states CVSS is not a risk score. Severity-only SLAs over-prioritize unreachable issues and under-prioritize exploited medium issues.",
        legally_required="No law reviewed requires CVSS-based SLAs for a private vendor. BOD 22-01 KEV deadlines bind federal civilian agencies only.",
        contractually_required="Many customer questionnaires and MSAs express SLAs by CVSS severity band; expect requests to commit to them.",
        historical_convention="Severity-banded SLAs (for example critical 15 or 30 days) are widespread industry convention.",
        architectural_elimination="Structural rules (SEC-DB-001, SEC-UI-002, SEC-EXEC-001) can make some dependency vulnerability classes unreachable, but only with scoped evidence that bypass is impossible.",
        automatic_enforcement="Gate releases on KEV and on high EPSS plus reachable findings; keep CVSS bands as a floor.",
        continuous_evidence="Register with EPSS and KEV snapshots, reachability decisions and reviewer identity.",
        stronger_alternative="Hybrid: severity-band SLA as contractual ceiling, accelerated deadlines for KEV or high EPSS, documented reachability-based deferrals reviewed independently and disclosed via VEX.",
        alternative_verifiable="Yes, if reachability decisions and score snapshots are retained and sampled by an independent reviewer.",
        customer_acceptance_likelihood="Likely if CVSS bands remain as ceilings; uncertain if CVSS bands are replaced entirely.",
        invalidating_conditions="Reachability analysis is wrong or unverifiable for F#; EPSS data unavailable; customer contract fixes CVSS-only SLAs.",
        conventional_cost="low", alternative_cost="medium",
        alternative_risks="Reachability determinations can be wrong and become an excuse for deferral; EPSS is probabilistic and can underweight targeted attacks on a niche financial platform.",
        supporting_arguments=["KEV and EPSS directly reflect exploitation evidence.", "VEX lets customers suppress non-affecting findings in their own tooling."],
        opposing_arguments=["Auditors and banks often prefer a simple severity table they can test by sampling.", "Targeted attacks against DAF platforms are unlikely to appear in EPSS, which models broad exploitation."],
        technical_effectiveness="stronger", institutional_acceptance="likely")

    ch_sla = challenge(
        customer_intent="Bound the window of exposure for known weaknesses and make it contractually testable.",
        adverse_outcome="Known vulnerabilities remain exploitable for months.",
        conventional_control_effectiveness="Fixed-day SLAs measured from detection are testable but are routinely missed and quietly converted into exceptions; they measure process, not exposure.",
        legally_required="Not by statute for Echelon. PCI DSS Req 6.3.3 sets a one-month expectation for critical patches only where PCI DSS applies; it is not expected to apply to Unbound.",
        contractually_required="Common in bank and enterprise MSAs and security addenda.",
        historical_convention="Severity-banded SLAs measured in calendar days.",
        architectural_elimination="Rebuild-and-redeploy pipelines and small dependency surfaces shorten time to fix, making shorter SLAs achievable.",
        automatic_enforcement="Release gate blocks on overdue findings; exception register expires automatically.",
        continuous_evidence="Exposure-window metric computed from register timestamps and deployment records, not from ticket closure.",
        stronger_alternative="Measure and commit to exposure window (from public disclosure to deployed fix across all tenants), not only ticket closure time.",
        alternative_verifiable="Yes, from deployment manifests joined to advisory publication dates.",
        customer_acceptance_likelihood="Likely as a supplement; customers still expect the familiar SLA table.",
        invalidating_conditions="No reliable deployment manifest; manual deployments.",
        conventional_cost="low", alternative_cost="low",
        alternative_risks="Small team capacity may make aggressive commitments unachievable during simultaneous events.",
        supporting_arguments=["Exposure window is what matters to the customer."],
        opposing_arguments=["A single-person or very small team cannot credibly promise 24x7 critical remediation without on-call depth."],
        technical_effectiveness="stronger", institutional_acceptance="likely")

    ch_bb = challenge(
        customer_intent="Continuous external scrutiny that finds what internal teams miss.",
        adverse_outcome="Vulnerabilities discovered by criminals first.",
        conventional_control_effectiveness="Bug bounties produce value for mature, internet-scale products; for a pre-production, low-traffic platform they mostly attract low-quality reports and require triage capacity Echelon does not have.",
        legally_required="No.", contractually_required="Rarely; usually asked as a preference.",
        historical_convention="Common among large SaaS vendors; uncommon for early-stage financial platforms.",
        architectural_elimination="Not applicable.", automatic_enforcement="Not applicable.",
        continuous_evidence="A VDP intake log provides evidence of external engagement without paid bounties.",
        stronger_alternative="Start with a VDP plus safe harbor and targeted independent tests; add a private, invite-only bounty after production launch and independent test baseline.",
        alternative_verifiable="Yes: published policy, intake log, independent test letters.",
        customer_acceptance_likelihood="Likely for most financial customers, who rank independent penetration testing above bounties.",
        invalidating_conditions="Large public user base or high-profile target status after launch.",
        conventional_cost="medium", alternative_cost="low",
        alternative_risks="Fewer eyes on the product between independent tests.",
        supporting_arguments=["Triage burden of public bounties is high relative to findings for small products."],
        opposing_arguments=["Some enterprise questionnaires score the absence of a bounty negatively.", "Bounties can find business-logic flaws that scheduled tests miss."],
        technical_effectiveness="equivalent", institutional_acceptance="likely")

    a1 = c.au(1, "Vulnerability management program and identification coverage", "proposed-target-state",
              "SOC2-016 directs that vulnerability programs record findings, prioritization, fixes, exceptions and retest evidence, and SEC-SUPPLY-001 proposes vulnerability checks on dependencies; neither is implemented and no production service exists.",
              "Echelon operates an inventory-driven vulnerability management program: every deployed component is derived from build SBOMs and deployment manifests and continuously matched against OSV, vendor advisories (.NET, PostgreSQL, base images, cloud provider bulletins) and CISA KEV; components missing from the inventory raise gaps; every finding enters one register with lifecycle timestamps; and coverage, aging and exception metrics are reported with raw denominators.",
              "Not established. No vulnerability management policy, register or scanning workflow was located in Echelon repositories reviewed (no CodeQL, dependency or vulnerability scanning workflow found in Praxis or product repositories).",
              "Adopt a vulnerability management procedure under the Secure Construction Standard, implement SBOM-fed SCA in CI, and build the register as a byproduct of the pipeline before Unbound handles real data.",
              "Nothing operational. Only the proposed Standard and Unbound directive text exist.",
              "Echelon has defined, but not yet implemented, a vulnerability management design for Unbound. Unbound is not yet in production; we can share the proposed design and will provide operating evidence once the service is live.",
              "planned", [k1, k7], [e1, e7], policies=["SEC-SUPPLY-001"], requirements=["SOC2-016", "SOC2-034"],
              freshness="P1D", mechanism="continuous-automated", automation="high", impl="medium", rec="low",
              residual=["Advisory coverage for F# and less common NuGet packages may be sparse; absence of findings is not absence of vulnerabilities."],
              oq=["Which hosting provider and managed services will Unbound use, and what vulnerability information do they provide?", "Who is the accountable owner of the vulnerability program?"])
    a2 = c.au(2, "Risk-based vulnerability prioritization (CVSS v4, EPSS, KEV, reachability, VEX)", "proposed-target-state",
              "No prioritization method is documented anywhere in Echelon sources; the target is a recommendation of this research.",
              "Each finding carries a CVSS v4.0 vector including threat and environmental metrics, an EPSS score snapshot, KEV membership and a reachability determination. KEV and high-likelihood reachable findings receive accelerated deadlines. Reachability-based deferrals are reviewed by someone other than the fixing engineer and are published to customers as VEX statements. Defects in structural control components (Strata access layer, Limen boundary, authorization core) are escalated one level because other controls depend on them.",
              "Unknown; no evidence located.", "Implement as part of the register in ANS-VUL-001.", "Nothing.",
              "Echelon intends to prioritize vulnerabilities using CVSS v4.0, EPSS and the CISA KEV catalog; this is not yet operating.",
              "planned", [k2, k6], [e1, e6], freshness="P1D", mechanism="continuous-automated", automation="high", impl="low", rec="low",
              challenge=ch_prio,
              residual=["Reachability analysis tooling for F# is immature; manual determinations may be wrong."])
    a3 = c.au(3, "Remediation SLAs, verification and zero-day response", "proposed-target-state",
              "SOC2-016 requires recording fixes and retests; no SLA values have been set in any Echelon source.",
              "Proposed contractual ceilings: KEV or actively exploited, 7 days or less (mitigation within 48 hours); critical 15 days; high 30 days; medium 90 days; low at next scheduled release; measured from first detection or public disclosure, whichever is earlier, to deployed fix across all tenants. Closure requires rescan or regression test evidence. A zero-day playbook uses the SBOM index to answer exposure within hours. SLA performance is reported monthly with raw counts.",
              "Not established.", "Set SLA values with counsel and early customers before signing, and enforce them via release gates.",
              "Nothing.",
              "Remediation timelines have not yet been adopted. Proposed targets can be discussed, and no SLA performance history exists because Unbound is not in production.",
              "not-available", [k3], [e1, e2], requirements=["SOC2-016", "SOC2-034"], freshness="P30D", mechanism="periodic-automated", automation="high",
              disclosure="nda", impl="low", rec="medium", challenge=ch_sla,
              residual=["Small-team capacity limits; simultaneous critical events could exceed SLA."],
              oq=["What SLA values will Echelon commit to contractually, and has counsel reviewed them?"])
    a4 = c.au(4, "Vulnerability exceptions and risk acceptance", "proposed-target-state",
              "The Secure Construction Standard enforcement model and SOC2-033 specify explicit, scoped, time-limited exceptions with accountable approval and compensating controls; formal adoption and implementation are unestablished.",
              "Exceptions are requested in a register, scoped to specific findings and releases, approved by an accountable reviewer other than the requester, accompanied by compensating controls, expire automatically and are re-reviewed; customers are told when an accepted risk affects a control they rely on. AI agents cannot create, approve, extend or close exceptions or suppressions.",
              "Not established.", "Implement the exception register and gate integration with ANS-VUL-003.", "Nothing.",
              "Echelon's proposed standard requires time-limited, separately approved exceptions with compensating controls; the process is not yet operating.",
              "planned", [k4], [e3], policies=["SEC-SUPPLY-001"], requirements=["SOC2-033", "SOC2-017"], freshness="per-event",
              mechanism="event-driven-automated", automation="partial", disclosure="nda", impl="low", rec="low",
              residual=["With a very small organization, separation between requester and approver may be impossible without an external reviewer."],
              oq=["Who can accept risk on behalf of Echelon while the organization has few or no employees?"])
    a5 = c.au(5, "Vulnerability disclosure program and security.txt", "unknown",
              "No vulnerability disclosure policy, SECURITY.md or security.txt was located in Echelon repositories reviewed; no Echelon source proposes one.",
              "Echelon publishes a vulnerability disclosure policy aligned with ISO/IEC 29147 and 30111 covering all Echelon domains, products and open-source libraries, with good-faith safe harbor language reviewed by counsel, a monitored reporting address, security.txt files with current expiry on each domain, acknowledgment within 3 business days, triage within 10 business days, and coordinated disclosure.",
              "Unknown; no evidence located. No SECURITY.md or security.txt found in reviewed Echelon repositories.",
              "Publish a VDP and security.txt before any public launch; add SECURITY.md to public Echelon repositories.",
              "Nothing.",
              "Echelon does not currently publish a vulnerability disclosure policy. Security reports can be sent to the company's general contact until one is established.",
              "not-available", [k5], [e4, e5], freshness="P30D", mechanism="periodic-automated", automation="partial", disclosure="public",
              impl="low", rec="low", oq=["Does Echelon have a monitored security contact address?", "Has counsel reviewed safe harbor language?"])
    a6 = c.au(6, "Bug bounty program", "unknown",
              "No Echelon source mentions a bug bounty. None is believed to exist; not verified.",
              "No paid bug bounty before production launch; a VDP with safe harbor plus independent penetration testing. Consider a private, invite-only bounty restricted to a dedicated test tenant with synthetic data once Unbound is in production and independently tested.",
              "Unknown; no evidence located.", "Decide after production launch.", "Nothing.",
              "Echelon does not operate a bug bounty program.", "not-available", [k5], [e5],
              disclosure="public", impl="none", rec="none", challenge=ch_bb)
    a7 = c.au(7, "Customer notification of vulnerabilities and advisories", "proposed-target-state",
              "No customer vulnerability notification commitment exists; Unbound requirements define a notification catalog (UNB-RCN-PLT-002) but not vulnerability advisories specifically.",
              "Customers are notified within 2 business days when a vulnerability affecting their tenant or release is confirmed as exploitable and not yet fixed, with interim mitigations; advisories are issued after fixes; VEX statements are provided for non-affecting components; inquiries during public vulnerability events are answered within 1 business day from the SBOM index; subprocessor and platform vulnerabilities affecting the service are included.",
              "Not established.", "Define advisory templates and notification commitments in the security addendum.", "Nothing.",
              "Vulnerability notification commitments have not yet been defined.", "not-available", [k6], [e6],
              mechanism="event-driven-automated", automation="partial", impl="low", rec="low",
              oq=["Will Echelon assign CVE identifiers for vulnerabilities in distributed libraries (for example via a CNA or GitHub advisories)?"])
    a8 = c.au(8, "Platform component patching and end-of-support management", "proposed-target-state",
              "Strata is pilot status and PostgreSQL 16 only; hosting is not selected. Rebuild-and-redeploy is a recommendation of this research, not an Echelon decision.",
              "Platform components (.NET runtime, PostgreSQL engine, container base images, OS) are patched by rebuilding immutable artifacts and redeploying through the gated pipeline; deployed versions are monitored against vendor security releases and support windows, with migration plans at least 6 months before end of support.",
              "Unknown; no production platform exists.", "Adopt immutable build and deploy once hosting is selected.", "Nothing.",
              "Unbound is not yet deployed; patching practices are planned, not operating.", "planned", [k7], [e7],
              freshness="P1D", mechanism="continuous-automated", automation="high", impl="medium", rec="low",
              residual=["Strata supports PostgreSQL 16 only; a forced PostgreSQL major upgrade may depend on Strata changes."])
    a9 = c.au(9, "AI agents in vulnerability remediation and AI tooling vulnerabilities", "proposed-target-state",
              "SOC2-017 requires AI agents to be attributable, bounded and monitored; Praxis provides provenance records for agent work, but no control specific to AI-authored security fixes exists.",
              "AI agents may draft fixes, but every AI-authored change is attributed to the agent and authorizing human, reviewed by a different principal, must pass security regression tests and cannot modify gates, findings or exceptions. Vulnerabilities in agent runtimes, model SDKs and tool integrations are inventoried and managed in the same register.",
              "Praxis records agent provenance for repository work (tooling exists, not operated for a production Echelon service). No security-specific review rule is enforced.",
              "Extend Praxis gates to require independent review of agent-authored security fixes.",
              "Praxis provenance records for repository changes, which show agent attribution but not security verification.",
              "Echelon uses AI agents in engineering and records their provenance in repository tooling; specific verification of AI-authored security fixes is planned, not operating.",
              "planned", [k8], [e8], requirements=["SOC2-017"], mechanism="event-driven-automated", automation="high", impl="low", rec="low",
              residual=["Reviewer may over-trust agent output; correlated errors if the same model family reviews its own work."])

    I_FIN = ["financial-services", "banking", "wealth-management", "donor-advised-funds"]
    # Questions
    c.q(1, "program", "Do you maintain a documented vulnerability management process that covers identification, triage, remediation, verification and reporting for every component used to deliver the service?",
        "Assurance that the vendor systematically finds and fixes weaknesses.", "Unmanaged vulnerabilities leading to compromise of customer data.",
        [D("SRC-CSA-CCM-V4", "TVM-01"), D("SRC-NIST-CSF-2.0", "ID.RA-01"), R("SRC-ISO-27002-2022", "8.8"), D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-016", "derived-from"), R("SRC-SA-SIG")],
        "industry-convention", "high", alts=["Describe your threat and vulnerability management policy.", "Is there a management-approved vulnerability management program?", "Provide your vulnerability management procedure."])
    c.q(1, "identification", "How do you determine which assets are in scope for vulnerability identification, and how would you detect a deployed component that is missing from that inventory?",
        "Coverage completeness.", "Blind spots in unscanned components.", [R("SRC-CIS-CONTROLS-V8.1", "7.1"), R("SRC-NIST-SP800-53-R5", "RA-5")], "industry-convention", "medium")
    c.q(1, "identification", "Which sources feed vulnerability identification (advisory databases, vendor bulletins, scanner output, threat intelligence, researcher reports), and how quickly does a newly published advisory reach a triage decision?",
        "Timeliness of awareness.", "Delayed awareness of new advisories.", [R("SRC-CSA-CCM-V4", "TVM-07"), R("SRC-NIST-CSF-2.0", "ID.RA-02"), R("SRC-OSV", rel="informed-by")], "industry-convention", "medium")
    c.q(1, "identification", "How do you identify vulnerabilities in the .NET runtime, the F# toolchain and NuGet dependencies that mainstream scanners may cover poorly, and how do you avoid treating an empty scan as proof of no vulnerabilities?",
        "Ecosystem-specific coverage for an F# stack.", "False assurance from tools with weak F# coverage.", [R("SRC-FSHARP-ANALYZERS", rel="informed-by"), R("SRC-OSV", rel="informed-by"), D("SRC-ECH-SCS-0.1", "Scanner validation", "informed-by")],
        "customer-preference", "medium")
    c.q(1, "identification", "Are managed platform components (database engine, operating system images, cloud managed services) included in vulnerability identification, and how is responsibility for them split with your hosting provider?",
        "Shared responsibility clarity.", "Vulnerabilities in provider-managed layers that nobody tracks.", [R("SRC-ISO-27017"), R("SRC-CSA-CCM-V4", "TVM-07")], "industry-convention", "medium")
    c.q(1, "program", "Does your vulnerability management meet the expectations our examiners apply to service providers supporting a regulated institution, comparable to the institution's own program?",
        "Regulatory examination readiness of the bank's third-party oversight.", "Examiner criticism of the bank for relying on a weaker vendor program.",
        [R("SRC-FFIEC-IS-BOOKLET"), R("SRC-INTERAGENCY-TPRM-2023"), R("SRC-INTERAGENCY-GLBA-SAFEGUARDS")], "supervisory-guidance", "high", ind=["banking"], reg="OCC, FDIC, Federal Reserve (via the customer)")
    c.q(2, "prioritization", "How do you score vulnerabilities, and do you use CVSS v4.0 including threat and environmental metrics rather than base scores alone?",
        "Consistent, context-aware severity.", "Misprioritization from base-score-only triage.", [D("SRC-CVSS-4.0"), R("SRC-CSA-CCM-V4", "TVM-08")], "industry-convention", "medium",
        alts=["What scoring methodology do you use to rank vulnerabilities?"])
    c.q(2, "prioritization", "Do you use EPSS or other exploitation-likelihood signals in prioritization, and how does likelihood change the remediation deadline?",
        "Focus on what attackers actually exploit.", "Exploited medium-severity issues left open.", [D("SRC-FIRST-EPSS")], "industry-convention", "medium")
    c.q(2, "prioritization", "How do you handle vulnerabilities listed in the CISA Known Exploited Vulnerabilities catalog, and what is your remediation deadline for them?",
        "Speed on actively exploited issues.", "Compromise via a publicly known exploited flaw.", [D("SRC-CISA-KEV"), R("SRC-CISA-BOD-22-01", rel="informed-by")], "industry-convention", "high",
        note="BOD 22-01 binds federal civilian agencies only; cited as a benchmark for timelines.")
    c.q(2, "prioritization", "Before downgrading or deferring a finding as not exploitable in your deployment, how do you establish reachability, and who other than the fixing engineer reviews that determination?",
        "Integrity of deferral decisions.", "Exploitable issues wrongly dismissed.", [R("SRC-CVSS-4.0"), R("SRC-OPENVEX", rel="informed-by")], "customer-preference", "medium")
    c.q(2, "prioritization", "Do you provide VEX statements so that our own scanners stop flagging components in your software that you have determined are not affected?",
        "Reduce false alarms in the customer's tooling.", "Customer effort wasted, or real issues missed amid noise.", [D("SRC-OPENVEX"), R("SRC-CISA-SBOM-MIN", rel="informed-by")], "customer-preference", "low")
    c.q(2, "prioritization", "If a vulnerability is found in a component that provides a structural security guarantee (for example the typed database access layer or the browser boundary library), how is it prioritized given that other controls assume that guarantee holds?",
        "Systemic risk from structural control failure.", "A single defect invalidating many dependent controls.", [D("SRC-ECH-SCS-0.1", "Mandatory target rules", "derived-from")], "echelon-internal", "medium")
    c.q(3, "remediation-sla", "What are your remediation timelines for critical, high, medium and low vulnerabilities, and from what event is the clock measured?",
        "Bounded exposure window.", "Indefinite exposure to known flaws.", [R("SRC-CSA-CCM-V4", "TVM-03"), R("SRC-PCI-DSS-4.0.1", "Req 6.3.3", rel="informed-by"), R("SRC-SA-SIG"), R("SRC-EDUCAUSE-HECVAT")],
        "contractual-common", "critical", alts=["What are your patching SLAs by severity?", "Within how many days are critical vulnerabilities remediated?"])
    c.q(3, "remediation-sla", "What percentage of vulnerabilities were remediated within SLA over the last four quarters, and can you provide aging metrics for open findings?",
        "Evidence that SLAs are met in practice.", "Paper SLAs not operated.", [R("SRC-CSA-CCM-V4", "TVM-10"), D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-034")], "customer-preference", "high", disc="nda")
    c.q(3, "remediation-sla", "Will you commit contractually to remediation timeframes and notify us when a critical or known-exploited vulnerability in the service exceeds its deadline?",
        "Contractual enforceability.", "No recourse when SLAs slip.", [R("SRC-INTERAGENCY-TPRM-2023"), R("SRC-OCC-BULLETIN-2023-17")], "contractual-common", "high", ind=I_FIN)
    c.q(3, "remediation-verification", "How do you verify that a remediation actually fixed the vulnerability (rescan, regression test, exploit reproduction) before closing it?",
        "Closure integrity.", "Findings closed without effective fixes.", [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-016"), R("SRC-NIST-SP800-53-R5", "SI-2")], "industry-convention", "medium")
    c.q(3, "zero-day", "For a zero-day in a widely used component, how quickly can you determine exposure across every deployed version and tenant, and what is your emergency remediation process?",
        "Speed of response to mass-exploitation events.", "Prolonged uncertainty during events such as Log4Shell.", [R("SRC-NTIA-SBOM-MIN"), R("SRC-CISA-KEV")], "customer-preference", "high")
    c.q(4, "exceptions", "When a vulnerability cannot be remediated within SLA, how are exceptions requested, approved, time-limited and tracked?",
        "Controlled deviation from policy.", "Silent permanent deferrals.", [D("SRC-ECH-SCS-0.1", "Enforcement model", "derived-from"), R("SRC-CSA-CCM-V4", "TVM-03"), D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-033")],
        "industry-convention", "high", alts=["Describe your vulnerability risk acceptance process."])
    c.q(4, "exceptions", "Who has authority to accept the risk of an unremediated critical vulnerability, and is that authority separated from the engineer responsible for the fix?",
        "Separation of duties in risk acceptance.", "Self-approved deferrals.", [R("SRC-NIST-CSF-2.0", "ID.RA-06"), R("SRC-COSO-ERM-2017", rel="informed-by")], "industry-convention", "medium")
    c.q(4, "exceptions", "Are customers informed when an accepted vulnerability risk affects a control they rely on, such as a complementary user entity control?",
        "Transparency on residual risk.", "Customer relying on a control that is knowingly weakened.", [R("SRC-AICPA-SOC2-GUIDE", rel="informed-by")], "customer-preference", "medium")
    c.q(4, "exceptions", "Can an AI agent approve, extend or close a vulnerability exception or scanner suppression, and what prevents an agent from suppressing a finding to make a gate pass?",
        "Integrity of risk decisions when agents do engineering work.", "Automated suppression of real findings.", [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-017"), R("SRC-OWASP-AGENTIC-AI"), R("SRC-OWASP-LLM-TOP10-2025", "LLM06:2025")],
        "customer-preference", "high")
    c.q(5, "disclosure-program", "Do you publish a vulnerability disclosure policy that tells external researchers how to report issues, what is in scope, and what legal safe harbor applies?",
        "External reporting path exists and is safe to use.", "Researchers unable or unwilling to report.", [D("SRC-ISO-29147-30111"), D("SRC-NIST-CSF-2.0", "ID.RA-08"), D("SRC-NIST-SP800-53-R5", "RA-5(11)"), R("SRC-BUG-BOUNTY-PLATFORMS")],
        "industry-convention", "medium", jur=["global"], prod=["all-echelon-products"], disc="public", alts=["Do you have a responsible disclosure policy?", "How can a third party report a security vulnerability to you?"])
    c.q(5, "disclosure-program", "Do you publish a security.txt file at the standard well-known location on your domains, and are its contact and expiry fields kept current?",
        "Discoverable security contact.", "Reports sent to unmonitored addresses.", [R("SRC-ISO-29147-30111", rel="informed-by")], "industry-convention", "low", jur=["global"], prod=["all-echelon-products"], disc="public",
        oq=["Seed a source for RFC 9116 (security.txt)."])
    c.q(5, "disclosure-program", "What acknowledgment and status-update timelines do you commit to for external vulnerability reports, and how do you coordinate public disclosure with the reporter?",
        "Predictable handling of reports.", "Uncoordinated public disclosure of unfixed flaws.", [D("SRC-ISO-29147-30111")], "industry-convention", "medium", jur=["global"], prod=["all-echelon-products"], disc="public")
    c.q(5, "disclosure-program", "Are externally reported vulnerabilities routed into the same tracking, prioritization and SLA process as internally found ones?",
        "Consistent treatment.", "External reports lost outside the register.", [D("SRC-ISO-29147-30111"), R("SRC-CSA-CCM-V4", "TVM-07")], "industry-convention", "medium")
    c.q(5, "disclosure-program", "If a vulnerability is reported in one of your published libraries (for example Aegis, Limen or Strata), how is it handled, and are downstream users notified?",
        "Upstream library hygiene affecting the product and other users.", "Unpatched shared library flaws.", [R("SRC-OPENSSF-OSPS-BASELINE"), R("SRC-ISO-29147-30111")], "industry-convention", "low", jur=["global"], prod=["all-echelon-products"], disc="public")
    c.q(6, "bug-bounty", "Do you operate a paid bug bounty program, public or private, and if so on which platform and with what scope?",
        "Breadth of external testing.", "Undiscovered flaws.", [R("SRC-BUG-BOUNTY-PLATFORMS"), R("SRC-VSA-FULL")], "customer-preference", "low", jur=["global"], disc="public")
    c.q(6, "bug-bounty", "If you do not run a bug bounty, what compensates for the absence of continuous external adversarial attention?",
        "Equivalent assurance.", "Gap between scheduled tests.", [R("SRC-BUG-BOUNTY-PLATFORMS")], "customer-preference", "low")
    c.q(6, "bug-bounty", "How do you prevent bug bounty or researcher testing from touching real customer data in production?",
        "Protection of customer data during third-party testing.", "Researcher access to real donor or financial data.", [R("SRC-BUG-BOUNTY-PLATFORMS"), R("SRC-ISO-27002-2022", "8.34")], "customer-preference", "medium", ind=I_FIN)
    c.q(7, "customer-notification", "Will you notify us when a vulnerability affecting the service or our data is discovered, and what will the notice contain?",
        "Customer awareness to adjust its own controls.", "Customer unaware of exposure.", [R("SRC-CSA-CCM-V4", "TVM-09"), R("SRC-INTERAGENCY-TPRM-2023")], "contractual-common", "high",
        alts=["Do you notify clients of critical vulnerabilities in your product?"])
    c.q(7, "customer-notification", "Do you publish security advisories for vulnerabilities fixed in the service, and do you obtain CVE identifiers for vulnerabilities in software you distribute?",
        "Transparency and traceability.", "Silent fixes that customers cannot track.", [R("SRC-ISO-29147-30111")], "industry-convention", "low", jur=["global"], prod=["all-echelon-products"])
    c.q(7, "customer-notification", "During a widely publicized vulnerability event, how quickly will you answer our inquiry about exposure, and through which channel?",
        "Fast answers for the customer's own risk reporting.", "Customer cannot answer its board or regulator.", [R("SRC-NTIA-SBOM-MIN", rel="informed-by")], "customer-preference", "high", ind=I_FIN)
    c.q(7, "customer-notification", "Do you notify customers of vulnerabilities in subprocessors or hosting platform components that affect the service, even when the fix is the provider's responsibility?",
        "Fourth-party visibility.", "Hidden exposure through subcontractors.", [R("SRC-INTERAGENCY-TPRM-2023"), R("SRC-ISO-27036")], "customer-preference", "medium")
    c.q(8, "patching", "How quickly do you apply security updates to the application runtime, database engine, container base images and operating systems, and how do you verify that every instance was updated?",
        "Platform patch currency.", "Exploitation of unpatched platform layers.", [R("SRC-NIST-SP800-53-R5", "SI-2"), R("SRC-CIS-CONTROLS-V8.1", "7.3"), R("SRC-CIS-CONTROLS-V8.1", "7.4")], "industry-convention", "high",
        alts=["Describe your patch management process."])
    c.q(8, "patching", "Do you patch by rebuilding and redeploying immutable artifacts rather than changing running systems, and how do you detect drift between deployed and patched builds?",
        "Reliable and complete patching.", "Partially patched fleets.", [R("SRC-NIST-SP800-53-R5", "CM-2", rel="informed-by"), R("SRC-SLSA", rel="informed-by")], "customer-preference", "medium")
    c.q(8, "end-of-support", "Do you track end-of-support dates for runtimes, frameworks and the database engine, and plan migrations before support ends?",
        "No unsupported software in production.", "Unpatchable components.", [R("SRC-CIS-CONTROLS-V8.1", "2.2")], "industry-convention", "medium")
    c.q(9, "ai-agents", "When AI agents propose or implement vulnerability fixes, how do you verify that the fix is correct and complete and does not introduce new weaknesses, and who is accountable for it?",
        "Quality and accountability of AI-performed engineering.", "Incorrect or weakened fixes from AI agents.", [R("SRC-NIST-SP800-218A"), R("SRC-OWASP-AGENTIC-AI"), D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-017")],
        "customer-preference", "high", jur=["global"])
    c.q(9, "ai-agents", "Are vulnerabilities in the AI tooling used to build and operate the service (model SDKs, agent frameworks, tool integrations) tracked in the same vulnerability program?",
        "Coverage of AI supply chain.", "Compromise through AI tooling.", [R("SRC-OWASP-LLM-TOP10-2025", "LLM03:2025"), R("SRC-NIST-SP800-218A")], "customer-preference", "medium", jur=["global"])
    return c
