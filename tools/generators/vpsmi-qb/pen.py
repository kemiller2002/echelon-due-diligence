from common import *

def build():
    c = Cat("PEN")
    e1 = c.evr(1, "Independent penetration test letter of attestation",
               "Letter from the independent testing firm stating firm, test window, scope (components, environments, roles, release hash), methodology, counts of findings by severity, and remediation and retest status.",
               "External penetration testing firm (not yet engaged)", "external-attestation", "P1Y", independence="independent-third-party",
               disclosure="nda", status="proposed-target-state",
               notes="No independent penetration test of Unbound or any Echelon product has occurred as of 2026-11-25; the Secure Construction Standard states it remains planned.")
    e2 = c.evr(2, "Full penetration test report",
               "Complete report with findings, evidence, risk ratings and tester identities, available to customers, auditors and regulators under NDA.",
               "External penetration testing firm (not yet engaged)", "external-attestation", "P1Y", independence="independent-third-party",
               disclosure="customer-only")
    e3 = c.evr(3, "Penetration test scope and rules of engagement record",
               "Signed statement of work and rules of engagement listing in-scope assets, roles, tenant-isolation and business-logic objectives, structural-claim bypass objectives, AI agent interfaces, materials provided to testers, exclusions and their rationale.",
               "not yet assigned", "periodic-manual", "P1Y", disclosure="nda")
    e4 = c.evr(4, "Tester and firm qualification record",
               "Firm accreditations (for example CREST), individual tester certifications, independence declaration and confidentiality terms.",
               "External penetration testing firm (not yet engaged)", "external-attestation", "P1Y", independence="independent-third-party", disclosure="nda")
    e5 = c.evr(5, "Penetration finding remediation and retest record",
               "Each pen test finding linked to the vulnerability register, fix commit, regression test added, and retest result issued by the testing firm.",
               "not yet assigned", "event-driven-automated", "per-event", disclosure="nda")
    e6 = c.evr(6, "Customer-initiated testing authorization record",
               "Requests from customers to test, approvals, test tenant allocation, rules of engagement, window, and findings returned.",
               "not yet assigned", "event-driven-automated", "per-event", disclosure="customer-only")
    e7 = c.evr(7, "First-party adversarial test results",
               "Results of internal adversarial, property-based and negative tests against financial invariants and structural controls, with test author distinct from code author, labeled as first-party.",
               "Tutela (security evidence and release posture model exists; not operated for a production Echelon service)", "event-driven-automated", "per-event", disclosure="nda")

    k1 = c.ctl(1, "Annual and change-triggered independent penetration testing",
               "An independent firm tests Unbound before production data is loaded, at least annually thereafter, and after material architecture, hosting or integration changes.",
               "detective-manual", "L10-external-or-manual", ["External penetration testing firm (not yet engaged)"], [e1, e2, e3],
               related=["SOC2-016"],
               fw=[R("SRC-NIST-SP800-53-R5", "CA-8"), R("SRC-NIST-SP800-53-R5", "CA-8(1)"), R("SRC-CSA-CCM-V4", "TVM-06"), R("SRC-CIS-CONTROLS-V8.1", "18.2")],
               notes="Planned per the Secure Construction Standard; never performed.")
    k2 = c.ctl(2, "Architecture-informed scope including structural-claim bypass",
               "Testers receive threat models, rule catalog and residual attack surfaces and are tasked to bypass structural controls (SEC-DB-001, SEC-UI-002, SEC-AUTH-001), tenant isolation, financial workflow invariants and AI agent tool authority, without suppressing independent discovery.",
               "detective-manual", "L8-adversarial-tested", ["External penetration testing firm (not yet engaged)", "Tutela (threat and invariant model source; not yet applied to Unbound)"], [e3],
               policies=["SEC-DB-001", "SEC-UI-002", "SEC-AUTH-001"], fw=[D("SRC-ECH-SCS-0.1", "External assurance and economics", "derived-from"), R("SRC-OWASP-WSTG"), R("SRC-NIST-SP800-115")])
    k3 = c.ctl(3, "Qualified, accredited and independent testers",
               "Testing firms are independent of Echelon engineering, hold a recognized accreditation, and assign testers with relevant certifications; firms are rotated or re-evaluated at least every three engagements.",
               "administrative", "L10-external-or-manual", ["not yet assigned"], [e4],
               fw=[R("SRC-CREST"), R("SRC-OFFSEC-CERTS"), R("SRC-GIAC-CERTS"), R("SRC-PCI-PENTEST-GUIDANCE", rel="informed-by")])
    k4 = c.ctl(4, "Pen test findings tracked to remediation and independent retest",
               "Every finding enters the vulnerability register under VUL SLAs, receives a regression test or structural fix, and is retested by the testing firm before being reported as closed.",
               "corrective", "L10-external-or-manual", ["not yet assigned"], [e5], related=["SOC2-016"],
               fw=[D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-016", "derived-from")])
    k5 = c.ctl(5, "Customer-initiated testing program",
               "Customers may test a dedicated tenant with synthetic data under published rules of engagement; findings are triaged under VUL SLAs.",
               "administrative", "L10-external-or-manual", ["not yet assigned"], [e6])
    k6 = c.ctl(6, "Continuous first-party adversarial testing",
               "Adversarial, negative and property-based tests against financial invariants and structural controls run on every release, authored independently of the code author, and are labeled first-party.",
               "detective-automated", "L7-property-tested", ["Tutela (model exists, not operated)", "Praxis (candidate CI host)"], [e7],
               fw=[D("SRC-ECH-SCS-0.1", "Financial and business invariants", "derived-from")],
               residual=["First-party tests share the builders' assumptions and cannot substitute for independent testing."])

    ch_annual = challenge(
        customer_intent="Independent evidence that a skilled attacker cannot readily compromise the service or other tenants' data.",
        adverse_outcome="Exploitable flaws in authentication, authorization, tenant isolation or financial workflows reach production.",
        conventional_control_effectiveness="A time-boxed annual black-box test samples a point in time and depends heavily on tester skill; it often misses business-logic and multi-tenant flaws when testers lack architecture context, and is stale soon after release.",
        legally_required="Not for Echelon directly. NYDFS 500.5 and the FTC Safeguards Rule impose testing on covered financial institutions for their own systems; customers may extend expectations to vendors by contract.",
        contractually_required="Very commonly required by bank, wealth and enterprise customers as an annual independent test with summary or letter sharing.",
        historical_convention="Annual independent penetration test with letter of attestation is near-universal in vendor due diligence.",
        architectural_elimination="Structural rules can remove some classes (dynamic SQL, arbitrary JavaScript), focusing testers on authorization, logic and isolation, but cannot remove the need for independent adversarial evaluation.",
        automatic_enforcement="Release gate requiring a current independent test covering the changed attack surface.",
        continuous_evidence="First-party adversarial test results per release (ECTL-PEN-006) between independent tests.",
        stronger_alternative="Architecture-informed independent testing (white-box, with threat models and structural claims) before launch and annually, plus change-triggered focused tests, plus continuous first-party adversarial tests labeled as such.",
        alternative_verifiable="Yes: independent letter covers scope including structural-claim bypass objectives; first-party results are reproducible.",
        customer_acceptance_likelihood="Likely, because it adds to rather than replaces the conventional independent test.",
        invalidating_conditions="If continuous first-party testing were offered as a replacement for independent testing, institutional acceptance would be unlikely.",
        conventional_cost="medium (order-of-magnitude judgment, not sourced)", alternative_cost="high",
        alternative_risks="Providing source and design material can anchor testers on documented assumptions; mitigate by including explicit objectives to find what the documentation does not describe.",
        supporting_arguments=["The Secure Construction Standard already directs providing threat models and residual attack surfaces to external testers.", "Business-logic flaws in grant and payment workflows are unlikely to be found black-box in a short engagement."],
        opposing_arguments=["Cost is significant for a pre-revenue company.", "Some customers specifically want black-box results to approximate an outside attacker."],
        technical_effectiveness="stronger", institutional_acceptance="likely")
    ch_cont = challenge(
        customer_intent="Know that security does not degrade between annual tests.",
        adverse_outcome="New features introduce flaws that persist until the next annual test.",
        conventional_control_effectiveness="Annual tests leave up to a year of untested change.",
        legally_required="No.", contractually_required="Rarely; customers ask but seldom require continuous testing.",
        historical_convention="Annual testing; some vendors add continuous automated attack surface scanning or bounties.",
        architectural_elimination="Invariants enforced at persistence and transaction boundaries reduce what adversarial tests must cover.",
        automatic_enforcement="Adversarial and property-based tests run in CI as release gates.",
        continuous_evidence="Per-release first-party adversarial results.",
        stronger_alternative="Continuous first-party adversarial testing of invariants plus change-triggered independent tests.",
        alternative_verifiable="Partially; first-party results can be sampled by the independent tester or SOC auditor.",
        customer_acceptance_likelihood="Uncertain as a substitute; likely as a supplement.",
        invalidating_conditions="Tests authored by the same agent or person who wrote the code; tests that only confirm intended behavior.",
        conventional_cost="medium", alternative_cost="medium",
        alternative_risks="Risk of presenting first-party evidence as if independent, which the Secure Construction Standard prohibits.",
        supporting_arguments=["Property-based tests can explore input spaces far beyond manual testing."],
        opposing_arguments=["Institutions value independence over volume; first-party evidence is discounted.", "AI-generated tests may share blind spots with AI-generated code."],
        technical_effectiveness="stronger", institutional_acceptance="uncertain")

    a1 = c.au(1, "Independent penetration testing: existence, frequency and triggers", "proposed-target-state",
              "The Secure Construction Standard states that external penetration testing remains planned for Unbound. No independent test of any Echelon product has occurred; no firm has been engaged.",
              "An independent, accredited firm tests Unbound before any customer production data is loaded, at least every 12 months thereafter, and after material changes (new hosting, authentication redesign, new payment or custodian integration, new AI agent authority). Results are shared as a letter of attestation and, under NDA, the full report.",
              "No independent penetration test has been performed on Unbound or any Echelon product. One is planned but not scheduled.",
              "Engage an accredited firm and complete an architecture-informed test before the first customer production data load.",
              "Nothing. No test, report or letter exists.",
              "Unbound has not yet been independently penetration tested. An independent test is planned before customer production data is loaded; we will share the letter of attestation when available.",
              "planned", [k1], [e1, e2], external="None obtained; planned.", freshness="P1Y", mechanism="external-attestation",
              automation="low", disclosure="authenticated-prospect", impl="medium", rec="medium", challenge=ch_annual,
              oq=["When will the first independent test be scheduled, and with which budget?", "Will testing precede any pilot with real donor data?"])
    a2 = c.au(2, "Penetration test scope and methodology", "proposed-target-state",
              "The Secure Construction Standard directs providing testers with threat models, rules, evidence and residual attack surfaces without suppressing independent discovery; no scope has been defined.",
              "Scope covers external attack surface, web application and APIs, every user and administrative role, cross-tenant access attempts, business logic of grant approval, payee change, disbursement and fee workflows, the Limen browser boundary, Strata-backed data access, AI agent interfaces and tool authority, cloud configuration, assumed-breach internal perspective (compromised workforce, CI or agent credential) and environment segregation. Testing is architecture-informed with explicit objectives to bypass claimed structural controls. Methodology references OWASP WSTG, NIST SP 800-115 and PTES.",
              "Not established.", "Define scope and rules of engagement during firm selection.", "Nothing.",
              "Penetration test scope is planned to include tenant isolation, business-logic abuse, structural-control bypass and AI agent interfaces; no test has occurred.",
              "planned", [k2], [e3], policies=["SEC-DB-001", "SEC-UI-002", "SEC-AUTH-001"], mechanism="periodic-manual", automation="low", impl="medium", rec="medium",
              residual=["Scope negotiated by the vendor may exclude weak areas; customers should review exclusions."])
    a3 = c.au(3, "Tester qualifications, firm accreditation and independence", "proposed-target-state",
              "No firm has been selected; criteria are a recommendation of this research.",
              "Testing is performed by a firm independent of Echelon engineering, holding a recognized accreditation such as CREST (or NCSC CHECK where a UK customer requires it), with testers holding certifications such as OSCP or GIAC GPEN or GWAPT and demonstrable web and API testing experience; testers are under confidentiality, background-checked by their firm, and do not access real customer data. Firms or lead testers rotate at least every three engagements.",
              "Not established.", "Apply these criteria in firm selection.", "Nothing.",
              "Tester selection criteria are planned, not yet applied.", "planned", [k3], [e4], mechanism="external-attestation", automation="none",
              impl="low", rec="low", oq=["Which accreditation will Echelon require, given cost differences among firms?"])
    a4 = c.au(4, "Sharing penetration test reports and letters of attestation", "proposed-target-state",
              "No report exists to share; the Secure Construction Standard requires labeling first-party assessments and never implying independent penetration testing.",
              "Prospects receive a letter of attestation under NDA; customers, their auditors and regulators may review the full report under NDA in a controlled viewer; all first-party assessment material is labeled first-party and distinguished from independent tests.",
              "Nothing to share.", "Adopt sharing terms in the security addendum.", "Nothing.",
              "No penetration test report or letter of attestation is available because no independent test has occurred.",
              "not-available", [k1], [e1, e2], external="None.", mechanism="external-attestation", automation="low", disclosure="nda", impl="none", rec="low")
    a5 = c.au(5, "Remediation and retest of penetration test findings", "proposed-target-state",
              "SOC2-016 requires recording findings, prioritization, fixes, exceptions and retest evidence for penetration testing programs; not implemented.",
              "Findings enter the vulnerability register under VUL SLAs; each fix adds a regression test or structural change preventing recurrence of the class; the testing firm retests and issues an updated letter showing remediation status.",
              "Not established.", "Implement with the vulnerability register.", "Nothing.",
              "Remediation and retest processes are planned; no findings exist because no test has occurred.",
              "planned", [k4], [e5], requirements=["SOC2-016"], mechanism="event-driven-automated", automation="partial", impl="low", rec="low")
    a6 = c.au(6, "Customer-initiated penetration testing rights", "unknown",
              "No Echelon source addresses customer testing rights, and hosting provider testing policies are unknown because hosting is not selected.",
              "Customers may test a dedicated tenant seeded with synthetic data, at no charge, with 10 business days' notice, under published rules of engagement that exclude denial-of-service and social engineering of Echelon staff, and that respect hosting provider policies; findings are triaged under VUL SLAs and results shared back with the customer.",
              "Unknown; no evidence located.", "Define in the security addendum once a test tenant capability exists.", "Nothing.",
              "Customer testing rights have not yet been defined.", "not-available", [k5], [e6], disclosure="nda", impl="low", rec="low",
              oq=["Can Unbound provision isolated test tenants with production-equivalent controls?"])
    a7 = c.au(7, "First-party continuous adversarial testing between independent tests", "proposed-target-state",
              "The Secure Construction Standard requires property-based, negative and adversarial tests of financial invariants; Tutela defines the security evidence model and requires that authors not be sole verifiers of critical changes (tutela@476dc682:docs/SECURITY-PROCESS.md). Neither is applied to a running Unbound system.",
              "Every release runs adversarial, negative and property-based tests of financial invariants, authorization and tenant isolation, authored independently of the code author, with results recorded as first-party evidence and made available for sampling by independent testers and auditors.",
              "Tutela tooling exists as a security engineering model; no Unbound code under test exists.",
              "Apply Tutela and Praxis gates to Unbound once implementation begins.",
              "Nothing for Unbound.",
              "First-party adversarial testing is planned as part of Unbound's construction; it is not independent testing and is not yet operating.",
              "planned", [k6], [e7], mechanism="event-driven-automated", automation="high", impl="medium", rec="low", challenge=ch_cont)
    a8 = c.au(8, "Threat-led and red team testing, including regulator-mandated programs", "not-applicable",
              "Unbound targets US DAF sponsors; no EU financial entity customer or DORA TLPT obligation is known. Red teaming beyond penetration testing is not planned in any Echelon source.",
              "If an EU financial entity designates Unbound as supporting a critical or important function, Echelon will participate in its threat-led penetration testing under DORA on agreed terms; red team exercises covering social engineering and supply chain are considered after production maturity.",
              "Not applicable at present.", "Revisit if EU or UK financial customers are pursued.", "Nothing.",
              "Echelon does not currently participate in threat-led penetration testing programs or red team exercises.", "not-available", [k1], [e3],
              impl="unknown", rec="unknown", oq=["Will Echelon pursue EU or UK financial customers?"])

    I_FIN = ["financial-services", "banking", "wealth-management", "donor-advised-funds"]
    c.q(1, "independent-testing", "Has the service been penetration tested by an independent third party within the last twelve months?",
        "Independent evidence of resistance to attack.", "Undetected exploitable flaws.",
        [R("SRC-CSA-CCM-V4", "TVM-06"), R("SRC-CIS-CONTROLS-V8.1", "18.2"), R("SRC-SA-SIG"), R("SRC-EDUCAUSE-HECVAT"), R("SRC-VSA-CORE")], "contractual-common", "critical",
        alts=["When was your last third-party penetration test?", "Do you conduct annual external penetration tests of the application?"])
    c.q(1, "frequency", "How often do you commission independent penetration tests, and which events (major release, architecture change, new integration, new hosting) trigger an additional test?",
        "Testing keeps pace with change.", "Untested new attack surface.", [R("SRC-NIST-SP800-53-R5", "CA-8"), R("SRC-PCI-DSS-4.0.1", "Req 11.4.3", rel="informed-by")], "industry-convention", "high")
    c.q(1, "independent-testing", "If the service has never been independently penetration tested, when is the first test scheduled, what will it cover, and will it be completed before our data is loaded into production?",
        "Risk acceptance for a new vendor.", "Customer data exposed in an untested system.", [D("SRC-ECH-SCS-0.1", "Purpose and business strategy", "informed-by")], "customer-preference", "critical", ind=I_FIN)
    c.q(1, "regulatory-expectation", "Does your testing cadence support our own annual penetration testing obligations under NYDFS Part 500 or the FTC Safeguards Rule where your service is within our scope?",
        "Customer's regulatory compliance.", "Customer program gaps from untested vendor systems.", [D("SRC-NYDFS-PART-500", "500.5"), R("SRC-FTC-SAFEGUARDS-RULE", "314.4(d)(2)")],
        "contractual-common", "high", ind=["financial-services", "banking", "insurance", "wealth-management"], jur=["US-state:NY", "US-federal"], reg="NYDFS; FTC",
        note="These rules bind the covered institution's own information systems; they reach the vendor only through the customer's contract and scoping decisions.")
    c.q(2, "scope", "What is in scope of the penetration test: external network, web application, APIs, authenticated user roles, administrative functions, cloud configuration and tenant isolation?",
        "Adequate coverage.", "Critical areas excluded from testing.", [R("SRC-OWASP-WSTG"), R("SRC-PTES"), R("SRC-NIST-SP800-115")], "contractual-common", "high",
        alts=["Provide the scope of your most recent penetration test."])
    c.q(2, "scope", "Does the test include authenticated testing of every role and deliberate attempts to access another tenant's data?",
        "Tenant isolation assurance.", "Cross-tenant data exposure.", [R("SRC-OWASP-API-TOP10-2023", "API1:2023"), R("SRC-OWASP-WSTG")], "customer-preference", "critical")
    c.q(2, "scope", "Does testing cover business-logic abuse specific to the service, such as bypassing grant approval, tampering with payment instructions, manipulating fees or replaying financial operations?",
        "Financial integrity under attack.", "Fraudulent grants or disbursements.", [R("SRC-OWASP-WSTG"), D("SRC-ECH-SCS-0.1", "Financial and business invariants", "informed-by")], "customer-preference", "high",
        ind=["donor-advised-funds", "financial-services", "wealth-management"])
    c.q(2, "internal-vs-external", "Do you perform internal or assumed-breach testing (compromised workforce account, compromised CI pipeline, compromised AI agent credential) in addition to external testing?",
        "Resilience after initial compromise.", "Lateral movement and privilege escalation.", [R("SRC-CIS-CONTROLS-V8.1", "18.5"), R("SRC-PCI-DSS-4.0.1", "Req 11.4.2", rel="informed-by")], "industry-convention", "medium")
    c.q(2, "architecture-informed", "Do you provide testers with architecture documentation, threat models and source code so they can test the assumptions your security depends on?",
        "Depth of testing.", "Shallow tests that miss design flaws.", [D("SRC-ECH-SCS-0.1", "External assurance and economics", "derived-from"), R("SRC-NIST-SP800-115")], "customer-preference", "medium")
    c.q(2, "architecture-informed", "Will testers be explicitly tasked to bypass the structural controls you claim, such as typed database access, the browser boundary and server-side authorization, rather than only run generic test cases?",
        "Validation of security-by-construction claims.", "Overstated structural guarantees.", [D("SRC-ECH-SCS-0.1", "Enforcement model", "derived-from")], "echelon-internal", "high")
    c.q(2, "scope", "Are AI agent interfaces and tool permissions in scope, including prompt injection leading to unauthorized tool calls and misuse of agent credentials?",
        "AI attack surface tested.", "Agent-mediated compromise.", [R("SRC-OWASP-LLM-TOP10-2025", "LLM01:2025"), R("SRC-OWASP-LLM-TOP10-2025", "LLM06:2025"), R("SRC-OWASP-AGENTIC-AI")], "customer-preference", "high", jur=["global"])
    c.q(2, "scope", "Is separation between production, non-production and build environments tested?",
        "Environment segregation.", "Pivot from weaker environments into production.", [R("SRC-PCI-DSS-4.0.1", "Req 11.4.5", rel="informed-by")], "industry-convention", "medium")
    c.q(3, "independence", "Which firm performs your penetration tests, and is it independent of the people who build and operate the service?",
        "Objectivity.", "Self-assessment presented as independent.", [R("SRC-NIST-SP800-53-R5", "CA-8(1)"), R("SRC-PCI-PENTEST-GUIDANCE")], "contractual-common", "high")
    c.q(3, "qualifications", "What certifications and experience do individual testers hold, for example OSCP, GIAC GPEN or GWAPT, or CREST certifications?",
        "Tester competence.", "Low-skill testing.", [R("SRC-OFFSEC-CERTS"), R("SRC-GIAC-CERTS"), R("SRC-CREST")], "customer-preference", "medium", jur=["global"])
    c.q(3, "accreditation", "Is the testing firm accredited under a recognized scheme such as CREST or, for UK regulated customers, NCSC CHECK?",
        "Firm-level quality assurance.", "Unvetted firms.", [R("SRC-CREST"), R("SRC-NCSC-CHECK")], "customer-preference", "low", jur=["global", "UK"])
    c.q(3, "independence", "Do you rotate testing firms or lead testers periodically to avoid familiarity blind spots?",
        "Fresh perspective.", "Repeated blind spots.", [R("SRC-PCI-PENTEST-GUIDANCE", rel="informed-by")], "customer-preference", "low")
    c.q(3, "tester-controls", "Are testers bound by confidentiality, background-checked by their firm and prevented from accessing real customer data?",
        "Protection of customer data during testing.", "Data exposure to testers.", [R("SRC-ISO-27002-2022", "8.34")], "customer-preference", "medium", ind=I_FIN)
    c.q(4, "report-sharing", "Will you share the full penetration test report, an executive summary or a letter of attestation, and on what terms?",
        "Customer due diligence evidence.", "Unverifiable claims of testing.", [R("SRC-SA-SIG"), R("SRC-EDUCAUSE-HECVAT"), R("SRC-INTERAGENCY-TPRM-2023")], "contractual-common", "high",
        alts=["Can you provide a copy of your most recent penetration test results?"], disc="nda")
    c.q(4, "report-sharing", "Does the letter of attestation state scope, dates, methodology, testing firm, findings by severity, and whether findings were remediated and retested?",
        "Usefulness of the attestation.", "Letters that hide scope gaps.", [R("SRC-PCI-PENTEST-GUIDANCE", rel="informed-by")], "customer-preference", "medium", disc="nda")
    c.q(4, "report-sharing", "Can our auditors or regulators review the full penetration test report under NDA if they require it?",
        "Examination support.", "Customer unable to satisfy examiners.", [R("SRC-INTERAGENCY-TPRM-2023"), R("SRC-FFIEC-OUTSOURCING-BOOKLET")], "supervisory-guidance", "medium", ind=["banking", "financial-services"], reg="OCC, FDIC, Federal Reserve (via the customer)")
    c.q(4, "labeling", "Will you clearly distinguish first-party security assessments from independent penetration tests in anything you send us?",
        "Honest assurance representation.", "Customer over-relying on internal evidence.", [D("SRC-ECH-SCS-0.1", "Assurance deliverables", "derived-from")], "echelon-internal", "high")
    c.q(5, "remediation", "How are penetration test findings tracked to remediation, and what deadlines apply by severity?",
        "Findings actually fixed.", "Known findings left open.", [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-016"), R("SRC-NIST-SP800-53-R5", "CA-8")], "contractual-common", "high")
    c.q(5, "retest", "Are fixes retested by the original testing firm, and is retest evidence included in what you share?",
        "Independent confirmation of fixes.", "Ineffective fixes.", [D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-016")], "customer-preference", "high")
    c.q(5, "remediation", "Are penetration test findings converted into regression tests or structural fixes so that the same class of defect cannot recur?",
        "Durable remediation.", "Recurrence of fixed defect classes.", [D("SRC-ECH-SCS-0.1", "Enforcement model", "informed-by")], "customer-preference", "medium")
    c.q(6, "customer-testing", "May we, or a firm we engage, penetration test the service, and what notice, scope limits and rules of engagement apply?",
        "Customer's own verification.", "Inability to verify vendor claims.", [R("SRC-SA-SIG"), R("SRC-INTERAGENCY-TPRM-2023")], "contractual-common", "medium",
        alts=["Do you permit client-initiated vulnerability scans or penetration tests?"])
    c.q(6, "customer-testing", "Do you provide a dedicated test tenant or sandbox with production-equivalent security controls for customer-initiated testing?",
        "Realistic testing without production risk.", "Tests on non-representative environments.", [R("SRC-ISO-27002-2022", "8.31", rel="informed-by")], "customer-preference", "medium")
    c.q(6, "customer-testing", "If our testing finds a vulnerability, how will you triage and fix it, report back, and protect other customers while it is open?",
        "Handling of customer-found issues.", "Cross-customer exposure.", [R("SRC-ISO-29147-30111", rel="informed-by")], "customer-preference", "medium")
    c.q(6, "customer-testing", "Which components are off-limits to customer testing because of hosting provider or subprocessor policies?",
        "Clarity of testing boundaries.", "Customer breaching provider terms.", [R("SRC-ISO-27017"), R("SRC-CSA-CCM-V4")], "customer-preference", "low")
    c.q(7, "continuous-testing", "Between independent tests, how do you test new code paths adversarially (automated attack simulation, adversarial property tests, internal red team)?",
        "Assurance between point-in-time tests.", "Flaws introduced after the last test.", [D("SRC-ECH-SCS-0.1", "Financial and business invariants", "derived-from"), R("SRC-OWASP-SAMM-2")], "customer-preference", "medium")
    c.q(7, "continuous-testing", "Are internal adversarial tests authored independently of the code they test, and how are their results represented relative to independent tests?",
        "Objectivity of first-party testing.", "Self-confirming tests.", [D("SRC-ECH-SCS-0.1", "Assurance deliverables", "derived-from")], "customer-preference", "medium")
    c.q(8, "threat-led", "If we are an EU financial entity subject to DORA, will you participate in threat-led penetration testing that includes your service?",
        "Customer regulatory obligation.", "Inability to complete mandated TLPT.", [D("SRC-EU-DORA", "Article 26"), R("SRC-EU-DORA", "Article 30"), R("SRC-TIBER-EU")], "legal-regulatory", "low",
        ind=["financial-services", "banking", "insurance"], jur=["EU"], reg="EU financial supervisors (via the customer)",
        note="Applies only if an EU financial entity uses the service for a critical or important function.")
    c.q(8, "red-team", "Do you commission red team exercises that include social engineering of staff or supply-chain compromise scenarios?",
        "Realistic adversary simulation.", "Untested human and supply-chain vectors.", [R("SRC-MITRE-ATTACK"), R("SRC-CBEST", rel="informed-by")], "customer-preference", "low", jur=["global"])
    return c
