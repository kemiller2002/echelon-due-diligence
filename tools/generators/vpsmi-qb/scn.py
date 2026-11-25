from common import *

def build():
    c = Cat("SCN")
    PRAXIS = "Praxis (CI workflow and provenance tooling exists; no security scanning step is configured)"
    e1 = c.evr(1, "Per-release scan evidence bundle",
               "For each release: commit and artifact hashes, each scanner's name, version, rule set and database version, scope and exclusions, coverage, findings, suppressions, gate outcome and reviewer identity, as required by the Secure Construction Standard assurance deliverables.",
               PRAXIS, "event-driven-automated", "per-event", fmt="SARIF plus signed JSON manifest",
               prov=["commit hash", "artifact hash", "tool name and version", "rule set version", "database version", "run time", "runner identity"],
               signing="Proposed: signed by CI identity", retention="Not established (SOC2-023)")
    e2 = c.evr(2, "Scanner coverage matrix",
               "Matrix of repositories, services, artifact types and languages against each scanner class (SAST, SCA, secrets, DAST, IaC, container), with uncovered cells listed explicitly.",
               "not yet assigned", "periodic-automated", "P30D")
    e3 = c.evr(3, "Scanner validation report",
               "Per scanner release: benchmark suites used (NIST SARD/Juliet, OWASP Benchmark where applicable, Echelon F# fixtures and holdout cases), precision, recall, false positive and false negative rates by weakness class, bypass and mutation results, and limitations.",
               "not yet assigned (Secure Construction Standard proposes Dokimos; Dokimos is a code-quality system and its scanner benchmarking role is unverified)",
               "event-driven-automated", "per-event", disclosure="public",
               notes="Benchmarking is not accreditation or government endorsement (Secure Construction Standard).")
    e4 = c.evr(4, "Secret detection and response record",
               "Each detected secret: location, detection time, blocking or post-hoc, rotation and revocation times, usage investigation result, and closure.",
               "not yet assigned", "event-driven-automated", "per-event", disclosure="internal")
    e5 = c.evr(5, "Suppression and false-positive register",
               "Each suppression: rule, location, justification, approver distinct from author (and never an AI agent), expiry and re-review result.",
               "not yet assigned", "event-driven-automated", "per-event", disclosure="nda")
    e6 = c.evr(6, "Customer scan summary",
               "Signed summary per production release: counts by severity and scanner, open critical findings, coverage, gate outcome, labeled as first-party evidence and tied to the release hash.",
               "not yet assigned (Folio is a candidate renderer for reports)", "event-driven-automated", "per-event", disclosure="customer-only")

    k1 = c.ctl(1, "SAST with F# semantic analysis and custom rules",
               "All first-party code is analyzed before merge by available .NET analyzers, F# analyzers (FSharp.Analyzers.SDK based) and Echelon custom semantic rules for prohibited constructs (dynamic SQL, dynamic code loading, unsafe interop, unrestricted deserialization); generated JavaScript bundles are analyzed separately.",
               "detective-automated", "L6-automated-analysis", [PRAXIS, "not yet assigned (custom F# analyzers do not yet exist)"], [e1],
               policies=["SEC-DB-001", "SEC-EXEC-001", "SEC-DATA-001", "SEC-LANG-001", "SEC-UI-002"],
               cwe=["CWE-89", "CWE-94", "CWE-502", "CWE-79"],
               fw=[R("SRC-NIST-SP800-53-R5", "SA-11(1)"), R("SRC-NIST-SP800-218", "PW.7"), R("SRC-FSHARP-ANALYZERS"), R("SRC-ROSLYN-SECURITY")],
               residual=["Mainstream SAST engines (for example CodeQL) do not analyze F#; Roslyn security analyzers target C# and VB syntax; F# coverage depends on custom rules and compiler-enforced structure."])
    k2 = c.ctl(2, "Software composition analysis on build and deployed inventory",
               "Every build and every deployed artifact SBOM is checked against vulnerability and license policy; unapproved or known-vulnerable dependencies above threshold fail the gate; deployed SBOMs are rescanned daily.",
               "preventive-gate", "L5-build-release-gate", [PRAXIS], [e1, e2], policies=["SEC-SUPPLY-001"], related=["SOC2-016"],
               fw=[R("SRC-CSA-CCM-V4", "TVM-05"), R("SRC-OSV"), R("SRC-CIS-CONTROLS-V8.1", "16.4", rel="informed-by")])
    k3 = c.ctl(3, "Secret scanning with push-time blocking",
               "Secrets are blocked before reaching shared repositories, history, logs, images and AI agent transcripts are scanned, and any detected secret is treated as compromised and rotated.",
               "preventive-gate", "L5-build-release-gate", ["not yet assigned (candidate: Gitleaks)"], [e4],
               policies=["SEC-CRYPTO-001"], related=["SOC2-003"], cwe=["CWE-798"],
               fw=[R("SRC-GITLEAKS"), R("SRC-NIST-SP800-53-R5", "IA-5(7)")])
    k4 = c.ctl(4, "Authenticated DAST and schema-driven API and boundary fuzzing",
               "A deployed test instance is scanned with authenticated DAST and schema-driven API tests including cross-tenant object access, and Limen boundary messages are fuzzed with invalid and oversized inputs.",
               "detective-automated", "L6-automated-analysis", ["not yet assigned (candidate: ZAP, Nuclei)"], [e1],
               policies=["SEC-AUTH-001", "SEC-DATA-001", "SEC-UI-001"], cwe=["CWE-639", "CWE-79", "CWE-20"],
               fw=[R("SRC-NIST-SP800-53-R5", "SA-11(8)"), R("SRC-OWASP-ZAP"), R("SRC-OWASP-API-TOP10-2023", "API1:2023")])
    k5 = c.ctl(5, "IaC, container and schema migration scanning with drift detection",
               "Infrastructure definitions, container images and Strata schema diffs are scanned before deploy for misconfiguration and security-relevant changes (grants, disabled row-level security, dropped audit triggers); deployed cloud configuration is compared continuously with the approved baseline.",
               "preventive-gate", "L5-build-release-gate", ["not yet assigned (candidate: Trivy)", "Strata (schema diff exists, pilot status, PG16 only; no security rules)"], [e1],
               fw=[R("SRC-TRIVY"), R("SRC-CIS-BENCHMARKS"), R("SRC-NIST-CSF-2.0", "PR.PS-01")])
    k6 = c.ctl(6, "Scanner validation against benchmarks and holdout fixtures",
               "Each scanner and rule set version is measured against public benchmarks and Echelon F# vulnerable and safe fixtures, including independently constructed holdout cases; regressions in recall block adoption of the new version; escaped defects become fixtures.",
               "detective-automated", "L7-property-tested", ["not yet assigned"], [e3],
               fw=[D("SRC-ECH-SCS-0.1", "Scanner validation", "derived-from"), R("SRC-NIST-SARD"), R("SRC-NIST-SAMATE"), R("SRC-NIST-SATE"), R("SRC-OWASP-BENCHMARK")])
    k7 = c.ctl(7, "Fail-closed scan gates with protected configuration and governed suppressions",
               "Mandatory scans run on every merge and release from configuration the repository cannot change; missing evidence fails the gate; suppressions require a non-author human approver and expire; AI agents cannot alter scanner configuration or suppressions.",
               "preventive-gate", "L5-build-release-gate", [PRAXIS], [e1, e5], related=["CNV-PLT-010", "SOC2-017"],
               fw=[D("SRC-ECH-SCS-0.1", "Enforcement model", "derived-from"), R("SRC-SLSA"), R("SRC-NIST-SP800-218A")])
    k8 = c.ctl(8, "First-party scan summaries for customers",
               "Signed, release-specific scan summaries labeled as first-party evidence are produced from the evidence bundle without manual assembly.",
               "administrative", "L6-automated-analysis", ["not yet assigned (Folio candidate renderer)"], [e6],
               fw=[D("SRC-ECH-SCS-0.1", "Assurance deliverables", "derived-from")])

    ch_sast = challenge(
        customer_intent="Confidence that common coding weaknesses are caught before release.",
        adverse_outcome="Injection, deserialization or similar flaws reach production.",
        conventional_control_effectiveness="Commercial and open-source SAST tools largely do not support F#; running a C#-oriented tool over an F# codebase produces a clean report that proves nothing. Academic evaluations show substantial false negative rates even in supported languages.",
        legally_required="No.", contractually_required="Commonly asked as yes or no; rarely specified by tool.",
        historical_convention="Questionnaires ask whether SAST runs and which tool.",
        architectural_elimination="SEC-DB-001 (no dynamic SQL, typed access), SEC-EXEC-001 and SEC-DATA-001 aim to make the dangerous sinks unavailable, so the weakness classes SAST hunts become structurally absent within scope, if bypass is independently verified.",
        automatic_enforcement="Compiler warnings as errors, private constructors, restricted interfaces, and custom analyzers that detect bypass of approved interfaces.",
        continuous_evidence="Per-release evidence that prohibited APIs are absent and bypass tests pass.",
        stronger_alternative="Structural elimination plus bypass-detecting custom F# rules, validated against fixtures, instead of relying on generic SAST coverage claims.",
        alternative_verifiable="Yes, if fixtures, rules and bypass tests are published and reproducible.",
        customer_acceptance_likelihood="Uncertain: customers recognize brand-name SAST tools; a structural argument requires explanation and independent confirmation.",
        invalidating_conditions="Strata typed query interface not available (current-state brief says no verified runtime typed query interface); trusted infrastructure code outside rules; native interop.",
        conventional_cost="low to medium", alternative_cost="medium",
        alternative_risks="Custom analyzers maintained by a small team may lag; claims of elimination could be overstated, which the Standard itself warns against.",
        supporting_arguments=["The Standard requires scoped evidence before claiming elimination.", "Structural prevention fails closed; detection fails open."],
        opposing_arguments=["Auditors and questionnaires expect a named SAST tool.", "Structural guarantees depend on Strata capabilities not yet verified."],
        technical_effectiveness="stronger", institutional_acceptance="uncertain")
    ch_dast = challenge(
        customer_intent="Confidence that the running application resists common attacks.",
        adverse_outcome="Exploitable runtime flaws.",
        conventional_control_effectiveness="Generic DAST finds configuration and reflected-input issues but is weak at authorization and business-logic flaws; IAST support for F# on .NET is uncertain.",
        legally_required="No; PCI ASV external scans apply only where PCI DSS applies.", contractually_required="Sometimes asked; rarely specified.",
        historical_convention="DAST commonly listed alongside SAST.",
        architectural_elimination="Server-side deny-by-default authorization (SEC-AUTH-001) and validated typed inputs reduce DAST yield.",
        automatic_enforcement="Schema-driven negative authorization tests in CI.",
        continuous_evidence="Per-release cross-tenant negative test results.",
        stronger_alternative="Schema-driven negative authorization tests and boundary fuzzing as primary dynamic testing, with generic DAST as a supplement; skip IAST unless a tool demonstrably supports the stack.",
        alternative_verifiable="Yes, via test results tied to release hashes.",
        customer_acceptance_likelihood="Likely if DAST is still run.",
        invalidating_conditions="Missing API schemas or incomplete role models.",
        conventional_cost="low", alternative_cost="medium",
        alternative_risks="Tests only cover the authorization model as specified, not as misunderstood.",
        supporting_arguments=["Broken object level authorization is the top API risk and is best tested with knowledge of the object model."],
        opposing_arguments=["Questionnaires may score absence of IAST negatively."],
        technical_effectiveness="stronger", institutional_acceptance="likely")
    ch_val = challenge(
        customer_intent="Know whether scanner output can be trusted.",
        adverse_outcome="False assurance from scanners that miss whole classes of weaknesses.",
        conventional_control_effectiveness="Most vendors never measure scanner false negative rates; a clean report is treated as evidence of absence.",
        legally_required="No.", contractually_required="Almost never asked.",
        historical_convention="Tool selection by reputation, not measurement.",
        architectural_elimination="Not applicable.", automatic_enforcement="Validation suite runs on every scanner or rule update.",
        continuous_evidence="Versioned validation reports with precision and recall by weakness class.",
        stronger_alternative="Published, reproducible scanner validation with F# fixtures and holdouts, as the Standard proposes.",
        alternative_verifiable="Yes, if fixtures and methodology are published.",
        customer_acceptance_likelihood="Likely as a differentiator; may be ignored by checklist reviewers.",
        invalidating_conditions="Fixtures written by the same people or agents who write rules (overfitting); benchmark suites not representative of F#.",
        conventional_cost="none", alternative_cost="medium",
        alternative_risks="Published fixtures could help attackers understand gaps; publish methodology and limitations while withholding exploitable specifics.",
        supporting_arguments=["Measurement converts a tool claim into evidence."],
        opposing_arguments=["Cost and effort for a small team before any customer asks for it.", "Benchmarks may give false precision."],
        technical_effectiveness="stronger", institutional_acceptance="uncertain")

    a1 = c.au(1, "Static application security testing, including F# coverage", "proposed-target-state",
              "The Secure Construction Standard proposes compiler semantic analysis to fill F# gaps and semantic checks for prohibited constructs; no SAST is configured in Echelon repositories reviewed, and the proposed owner (Aegis) is actually a fault-handling library, not a SAST orchestrator.",
              "Every merge runs available .NET analyzers, F# analyzers built on FSharp.Analyzers.SDK, and Echelon custom semantic rules that detect use or bypass of prohibited constructs (dynamic SQL outside Strata, dynamic code loading, unsafe interop, unrestricted deserialization, application JavaScript outside Limen); generated JavaScript bundles are scanned with a JavaScript-capable engine; coverage limits are stated per weakness class.",
              "Not established. No security static analysis workflow found. Dokimos measures code quality, not security.",
              "Select and build F# analyzers, assign an owner (not Aegis), and integrate into Praxis gates.",
              "Nothing.",
              "Static security analysis for Unbound is planned, including custom F# rules, because mainstream SAST tools do not analyze F#. It is not yet operating.",
              "planned", [k1], [e1], policies=["SEC-DB-001", "SEC-EXEC-001", "SEC-DATA-001", "SEC-LANG-001", "SEC-UI-002"],
              mechanism="event-driven-automated", automation="full", impl="medium", rec="low", challenge=ch_sast,
              oq=["Which system will own the security rule registry, given that Aegis is not a SAST orchestrator?"])
    a2 = c.au(2, "Software composition analysis", "proposed-target-state",
              "SEC-SUPPLY-001 proposes locked versions, provenance, SBOM, vulnerability and license checks; not implemented.",
              "Every build generates an SBOM and runs SCA against OSV and GitHub advisory data for NuGet and npm, including transitive dependencies, with license policy; deployed SBOMs are rescanned daily so new advisories against released artifacts are detected.",
              "Not established.", "Implement in CI with SEC-SUPPLY-001.", "Nothing.",
              "Dependency scanning is planned under Echelon's proposed supply-chain rule; not yet operating.", "planned", [k2], [e1, e2],
              policies=["SEC-SUPPLY-001"], requirements=["SOC2-016"], mechanism="continuous-automated", automation="full", impl="low", rec="low")
    a3 = c.au(3, "Secret scanning and response", "proposed-target-state",
              "SEC-CRYPTO-001 proposes secret scanning and rotation; SOC2-003 prohibits secrets in logs; neither is implemented.",
              "Pre-commit and push-time scanning blocks secrets; scheduled scans cover full history, CI logs, container images and persisted AI agent transcripts; any detected secret is treated as compromised, rotated and revoked, and its use investigated; scanning applies to all Echelon repositories.",
              "Unknown; no secret scanning configuration was located in reviewed repositories.",
              "Enable push-time blocking and history scans across Echelon repositories.", "Nothing.",
              "Secret scanning is planned under Echelon's proposed cryptography rule; not yet verified as operating.", "planned", [k3], [e4],
              policies=["SEC-CRYPTO-001"], requirements=["SOC2-003"], mechanism="event-driven-automated", automation="full", impl="low", rec="low")
    a4 = c.au(4, "Dynamic testing (DAST, API testing, IAST, ASV)", "proposed-target-state",
              "No dynamic testing is defined in Echelon sources beyond the Standard's general reference to DAST reuse; PCI DSS is not expected to apply because Unbound is not known to process card data.",
              "Each release candidate deployed to a test cell is scanned with authenticated DAST and schema-driven API tests across all roles, including cross-tenant object access attempts; Limen boundary messages and other serialized inputs are fuzzed. IAST is not used unless a tool demonstrably supports F# on .NET. ASV scans are performed only if PCI DSS scope is ever introduced.",
              "Not established.", "Implement once a deployable test environment exists.", "Nothing.",
              "Dynamic security testing is planned; not yet operating.", "planned", [k4], [e1],
              policies=["SEC-AUTH-001", "SEC-DATA-001", "SEC-UI-001"], mechanism="event-driven-automated", automation="high", impl="medium", rec="low", challenge=ch_dast,
              oq=["Will Unbound ever accept card payments (which would bring PCI DSS and ASV scanning into scope)?"])
    a5 = c.au(5, "Infrastructure-as-code, container, configuration and schema scanning", "proposed-target-state",
              "Hosting and IaC are not selected; Strata provides schema diff (pilot, PG16) but no security rules.",
              "IaC, container images and Strata schema diffs are scanned before deployment; deployed cloud configuration is continuously compared to the approved baseline (CIS Benchmarks) and drift outside the pipeline raises an alert.",
              "Not established.", "Implement once hosting and IaC are selected.", "Nothing.",
              "Infrastructure and configuration scanning is planned; Unbound has no deployed infrastructure.", "planned", [k5], [e1],
              mechanism="continuous-automated", automation="high", impl="medium", rec="low")
    a6 = c.au(6, "Scanner validation and false negative measurement", "proposed-target-state",
              "The Secure Construction Standard specifies benchmarking with NIST SAMATE, SARD and SATE and OWASP Benchmark, F#-specific fixtures, holdout cases and publication of methodology; nothing has been built.",
              "Each scanner and rule set release is validated against public suites where applicable and Echelon F# vulnerable and safe fixtures with independently constructed holdouts; precision, recall, false positive and false negative rates are reported by weakness class; recall regressions block adoption; vulnerabilities that escaped scanners become new fixtures; methodology, fixtures and limitations are published, and benchmarking is never represented as accreditation.",
              "Not established.", "Build the fixture corpus and validation harness as part of the scanner program.", "Nothing.",
              "Echelon plans to measure and publish scanner detection rates, including false negatives, for its F# stack; no results exist yet.",
              "planned", [k6], [e3], mechanism="event-driven-automated", automation="high", disclosure="public", impl="medium", rec="low", challenge=ch_val)
    a7 = c.au(7, "Scan frequency, coverage, gating and suppression governance", "proposed-target-state",
              "The Standard requires fail-closed merge and release gates on mandatory rule failures or missing evidence; CNV-PLT-010 requires two approvers on control-relevant modules and signed builds; none is implemented.",
              "SAST, SCA and secret scans run on every merge; DAST and IaC scans on every release candidate; deployed artifacts rescanned daily; scan evidence older than the release commit blocks release. Gates fail closed on missing evidence. Scanner configuration lives outside the repository under change control. Suppressions need a non-author human approver, expire and are re-reviewed; AI agents cannot alter scanner configuration, gates or suppressions. Coverage is reported against the full inventory.",
              "Not established. Praxis CI workflows exist for repository governance but contain no security scanning step.",
              "Add scanning gates to Praxis-managed CI.", "Nothing.",
              "Fail-closed security gates are planned; not yet operating.", "planned", [k7], [e1, e2, e5], requirements=["CNV-PLT-010", "SOC2-017"],
              mechanism="event-driven-automated", automation="full", impl="low", rec="low")
    a8 = c.au(8, "Sharing scan results with customers", "proposed-target-state",
              "The Standard lists a continuous security assurance summary monthly and labeling of first-party reports; none produced.",
              "Customers receive a signed, release-specific scan summary (counts by severity and scanner, open critical findings, coverage, gate outcome) labeled as first-party evidence, plus a monthly assurance summary; raw SARIF is available under NDA on request.",
              "Nothing produced.", "Generate from the evidence bundle once scanning operates.", "Nothing.",
              "Scan summaries are planned; none exist because scanning is not yet operating.", "not-available", [k8], [e6],
              mechanism="event-driven-automated", automation="full", disclosure="nda", impl="low", rec="low")

    c.q(1, "sast", "Do you run static application security testing on all first-party source code before release?",
        "Early detection of coding weaknesses.", "Exploitable code defects.", [R("SRC-NIST-SP800-53-R5", "SA-11(1)"), R("SRC-NIST-SP800-218", "PW.7"), R("SRC-CIS-CONTROLS-V8.1", "16.12"), R("SRC-EDUCAUSE-HECVAT"), R("SRC-SA-SIG")],
        "industry-convention", "high", alts=["Do you perform static code analysis?", "Is source code scanned for security vulnerabilities prior to deployment?"])
    c.q(1, "sast-fsharp", "Your application is written in F#. Which static analysis tools actually parse F# for security weaknesses, and which weakness classes can they detect?",
        "Real versus nominal SAST coverage.", "Clean reports from tools that cannot read the language.", [R("SRC-FSHARP-ANALYZERS"), R("SRC-ROSLYN-SECURITY"), R("SRC-CODEQL", rel="informed-by")], "customer-preference", "high", jur=["global"])
    c.q(1, "sast-fsharp", "For weakness classes no scanner can detect in F#, what compensates: compiler-enforced types, restricted interfaces, custom analyzers or manual review?",
        "Compensating assurance.", "Uncovered weakness classes.", [D("SRC-ECH-SCS-0.1", "Scanner validation", "derived-from")], "customer-preference", "medium", jur=["global"])
    c.q(1, "sast", "Are static analysis rules customized for your frameworks and prohibited APIs, such as dynamic SQL, dynamic code loading and unsafe native interop?",
        "Rules matched to the actual architecture.", "Bypass of approved interfaces undetected.", [D("SRC-ECH-SCS-0.1", "Mandatory target rules", "derived-from"), R("SRC-SEMGREP", rel="informed-by")], "echelon-internal", "medium")
    c.q(1, "sast", "Do you scan generated artifacts, such as JavaScript bundles compiled from F#, in addition to source code?",
        "Coverage of what actually runs in the browser.", "Flaws introduced by code generation.", [D("SRC-ECH-SCS-0.1", "SEC-UI-002", "derived-from")], "echelon-internal", "medium")
    c.q(2, "sca", "Do you run software composition analysis on every build to find known-vulnerable open-source dependencies, including transitive packages?",
        "Dependency risk visibility.", "Known-vulnerable libraries in production.", [R("SRC-CSA-CCM-V4", "TVM-05"), R("SRC-OSV"), R("SRC-OWASP-TOP10", rel="informed-by")], "industry-convention", "high",
        alts=["Do you scan third-party libraries for known vulnerabilities?"])
    c.q(2, "sca", "Which vulnerability databases does your composition analysis consult, and how do you handle an advisory present in one database but not another?",
        "Data source completeness.", "Missed advisories.", [R("SRC-OSV")], "customer-preference", "low", jur=["global"])
    c.q(2, "sca", "Does dependency scanning also enforce license policy and block unapproved dependencies?",
        "Legal and supply-chain hygiene.", "Unapproved or incompatible components.", [D("SRC-ECH-SCS-0.1", "SEC-SUPPLY-001", "derived-from")], "customer-preference", "medium")
    c.q(2, "sca", "Do you rescan deployed artifacts for newly disclosed vulnerabilities after release, rather than only at build time?",
        "Post-release awareness.", "New advisories against running software go unnoticed.", [R("SRC-CIS-CONTROLS-V8.1", "7.5"), R("SRC-NIST-SP800-53-R5", "RA-5")], "industry-convention", "high")
    c.q(3, "secrets", "Do you scan source repositories, commit history, build logs and container images for hardcoded secrets?",
        "Credential exposure prevention.", "Leaked credentials enabling compromise.", [R("SRC-GITLEAKS"), R("SRC-NIST-SP800-53-R5", "IA-5(7)"), D("SRC-ECH-SCS-0.1", "SEC-CRYPTO-001", "derived-from")], "industry-convention", "high")
    c.q(3, "secrets", "Are secrets blocked before they reach a shared repository, or only detected afterward?",
        "Prevention versus detection.", "Window of exposure for committed secrets.", [R("SRC-GITLEAKS")], "customer-preference", "medium")
    c.q(3, "secrets", "When a secret is detected, what happens: rotation, revocation, investigation of whether it was used, and notification?",
        "Response to exposed credentials.", "Use of leaked credentials.", [R("SRC-NIST-SP800-53-R5", "IA-5"), R("SRC-CSA-CCM-V4")], "industry-convention", "high")
    c.q(3, "secrets", "Do secret scans cover AI agent transcripts, prompts and tool outputs that may be persisted in repositories or logs?",
        "AI-era credential leakage.", "Secrets exposed through agent records.", [R("SRC-OWASP-LLM-TOP10-2025", "LLM02:2025"), D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-003")], "customer-preference", "medium", jur=["global"])
    c.q(4, "dast", "Do you run dynamic application security testing against a running instance, and is it authenticated?",
        "Runtime weakness detection.", "Exploitable deployed flaws.", [R("SRC-NIST-SP800-53-R5", "SA-11(8)"), R("SRC-OWASP-ZAP"), R("SRC-CIS-CONTROLS-V8.1", "16.12")], "industry-convention", "medium")
    c.q(4, "api-testing", "Do you test APIs dynamically from their schema definitions, including authorization checks between objects and tenants?",
        "API authorization assurance.", "Broken object level authorization.", [R("SRC-OWASP-API-TOP10-2023", "API1:2023"), R("SRC-OWASP-WSTG")], "customer-preference", "high")
    c.q(4, "iast", "Do you use interactive application security testing or runtime instrumentation, and if not, why not?",
        "Depth of runtime analysis.", "Missed runtime-only flaws.", [R("SRC-NIST-IR-8397")], "customer-preference", "low")
    c.q(4, "asv", "Does PCI DSS apply to the service, and if so are external-facing endpoints scanned quarterly by an approved scanning vendor?",
        "Card data compliance.", "PCI non-compliance.", [R("SRC-PCI-ASV-PROGRAM"), R("SRC-PCI-DSS-4.0.1", "Req 11.3.2")], "certification-criteria", "low", jur=["global"], reg="none (PCI SSC program; card brands)",
        note="Applies only if card data enters scope; Unbound is not known to process card data.")
    c.q(4, "fuzzing", "Are trust-boundary inputs, such as browser boundary messages and serialized payloads, fuzzed with malformed and oversized inputs?",
        "Robustness of input validation.", "Deserialization and parsing flaws.", [D("SRC-ECH-SCS-0.1", "SEC-DATA-001", "derived-from"), R("SRC-NIST-IR-8397")], "echelon-internal", "medium")
    c.q(5, "iac", "Do you scan infrastructure-as-code and cloud configuration for misconfiguration before deployment?",
        "Secure infrastructure configuration.", "Misconfigured storage, network or identity.", [R("SRC-TRIVY"), R("SRC-CIS-BENCHMARKS")], "industry-convention", "high")
    c.q(5, "container", "Do you scan container images and base images for vulnerabilities and misconfiguration, and block deployment of images with critical findings?",
        "Image hygiene.", "Vulnerable images in production.", [R("SRC-TRIVY"), R("SRC-CIS-BENCHMARKS")], "industry-convention", "medium")
    c.q(5, "configuration-drift", "Is deployed cloud configuration continuously compared with the approved baseline to detect changes made outside the pipeline?",
        "Configuration integrity.", "Unauthorized or accidental changes.", [R("SRC-NIST-CSF-2.0", "PR.PS-01"), R("SRC-CIS-BENCHMARKS")], "industry-convention", "medium")
    c.q(5, "schema", "Do you scan database schema changes for security-relevant effects such as new grants, disabled row-level security or removed audit triggers?",
        "Database security posture.", "Silent weakening of data access controls.", [D("SRC-ECH-SCS-0.1", "SEC-DB-001", "informed-by")], "customer-preference", "medium")
    c.q(6, "validation", "How do you know your scanners actually detect the weaknesses they claim to? Have you measured their false negative rates?",
        "Trustworthiness of scan evidence.", "False assurance.", [D("SRC-ECH-SCS-0.1", "Scanner validation", "derived-from"), R("SRC-NIST-SAMATE"), R("SRC-OWASP-BENCHMARK"), R("SRC-SAST-ACADEMIC-EVALS")], "customer-preference", "medium", jur=["global"])
    c.q(6, "validation", "Do you maintain vulnerable and safe test fixtures for F# and your own frameworks, including independently constructed holdout cases, to measure scanner precision and recall?",
        "Language-specific scanner assurance.", "Overfitted or untested rules.", [D("SRC-ECH-SCS-0.1", "Scanner validation", "derived-from"), R("SRC-NIST-SARD")], "echelon-internal", "low", jur=["global"])
    c.q(6, "validation", "When a scanner, rule set or vulnerability database version changes, do you revalidate detection to catch silent regressions?",
        "Stable detection over time.", "Silent loss of detection.", [D("SRC-ECH-SCS-0.1", "Scanner validation", "derived-from")], "customer-preference", "medium")
    c.q(6, "validation", "Do you publish your scanner validation methodology and results, and how do you avoid presenting benchmark results as accreditation?",
        "Transparency and honest representation.", "Misleading assurance claims.", [D("SRC-ECH-SCS-0.1", "Scanner validation", "derived-from"), R("SRC-NIST-SATE")], "echelon-internal", "low", jur=["global"], disc="public")
    c.q(6, "validation", "When a penetration tester, researcher or incident reveals a vulnerability your scanners missed, is it recorded as a false negative and added as a test case?",
        "Learning from escapes.", "Repeated misses.", [D("SRC-ECH-SCS-0.1", "Scanner validation", "derived-from")], "customer-preference", "medium")
    c.q(7, "gating", "Which scan results block a merge or release, at what thresholds, and who can override the gate?",
        "Enforcement, not just detection.", "Known issues shipped.", [D("SRC-ECH-SCS-0.1", "Enforcement model", "derived-from"), R("SRC-NIST-SP800-218", "PW.8")], "customer-preference", "high")
    c.q(7, "frequency", "How often does each scanner run, and what is the maximum age of scan evidence permitted for a production release?",
        "Freshness of evidence.", "Releases based on stale scans.", [R("SRC-CIS-CONTROLS-V8.1", "16.12"), R("SRC-SA-SIG")], "industry-convention", "medium")
    c.q(7, "coverage", "What share of repositories, services and deployed artifacts is covered by each scanner type, and how are uncovered components identified?",
        "Coverage transparency.", "Unscanned components.", [R("SRC-CSA-CCM-V4", "TVM-10"), D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-034")], "customer-preference", "medium")
    c.q(7, "suppression", "How are scanner findings suppressed as false positives, who approves suppressions, and are they periodically re-reviewed?",
        "Integrity of suppressions.", "Real findings hidden as false positives.", [D("SRC-ECH-SCS-0.1", "Enforcement model", "derived-from")], "customer-preference", "high")
    c.q(7, "ai-agents", "Is code written by AI agents subject to the same or stronger scanning and gates as human code, and can an agent change scanner configuration or suppressions?",
        "Control of AI-authored code.", "Agents weakening their own checks.", [R("SRC-NIST-SP800-218A"), R("SRC-OWASP-AGENTIC-AI"), D("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-017")], "customer-preference", "high", jur=["global"])
    c.q(7, "gating", "Are scanners run from protected CI configuration so that a change to a repository cannot disable its own security checks?",
        "Tamper resistance of the pipeline.", "Checks disabled in the same change that introduces a flaw.", [R("SRC-SLSA"), R("SRC-OPENSSF-SCORECARD")], "customer-preference", "medium")
    c.q(8, "results-sharing", "Will you share recent scan results or a summary, such as counts by severity, open critical findings and coverage?",
        "Ongoing visibility.", "Unverifiable claims.", [D("SRC-ECH-SCS-0.1", "Assurance deliverables", "derived-from"), R("SRC-SA-SIG")], "customer-preference", "medium", disc="nda")
    c.q(8, "results-sharing", "Can you provide machine-readable scan results or a signed summary tied to a release hash rather than screenshots or narrative?",
        "Verifiable evidence.", "Manipulable evidence.", [D("SRC-ECH-SCS-0.1", "Assurance deliverables", "derived-from")], "customer-preference", "low", disc="nda")
    c.q(8, "results-sharing", "Are scan summaries labeled as first-party evidence and tied to the specific release we are running?",
        "Honest and specific assurance.", "Customer mistaking internal scans for independent testing.", [D("SRC-ECH-SCS-0.1", "Assurance deliverables", "derived-from")], "echelon-internal", "medium", disc="nda")
    return c
