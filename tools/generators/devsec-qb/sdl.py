from devseclib import *

c = Cat("SDL")
SSDF = lambda p: f"SRC-NIST-SP800-218@{p}!"
SAMM = lambda p: f"SRC-OWASP-SAMM-2@{p}"
FIN = ["financial-services", "banking", "wealth-management", "donor-advised-funds"]
GOVBUY = ["public-sector", "higher-education"]

c.E("sdlpolicy", "Adopted secure development standard and SSDF/SAMM self-assessment",
    "The formally adopted secure development standard with approval record, and a dated self-assessment mapping practices to NIST SSDF tasks and OWASP SAMM maturity levels, with gaps and owners.",
    mechanism="periodic-manual", freshness="P1Y", fmt="Markdown policy with front matter plus assessment table",
    prov=["document version", "approver", "approval date", "assessment date", "assessor"])
c.E("reqtrace", "Security requirement traceability report",
    "Generated traceability from security requirements and invariants to code changes, tests and evidence, with gaps (requirements with no test, changes with no mapped control) listed.",
    producer="Praxis validation (exists for record integrity; security traceability not configured)", mechanism="event-driven-automated",
    fmt="JSON registry plus rendered report", prov=["requirement identifier", "commit", "test identifier", "evidence reference"])
c.E("review", "Code review and approval records per change",
    "For each merged change: author identity (human or agent), reviewers and their independence from the author, whether the change touched control-relevant modules, automated check results and approval timestamps.",
    producer="Source control platform plus Praxis provenance events (proposed integration)", mechanism="event-driven-automated",
    fmt="Pull request metadata export plus provenance events", prov=["change identifier", "author actor", "reviewer actors", "commit", "approval time", "module tags"])
c.E("sectest", "Security testing results per build",
    "Results of static analysis, dependency analysis, secret scanning, property and negative tests and dynamic tests per build, with tool versions, rule sets, suppressions and gate outcome.",
    mechanism="event-driven-automated", fmt="SARIF plus test reports plus gate summary",
    prov=["commit", "tool and rule versions", "suppressions with justification", "gate outcome"])
c.E("training", "Developer and agent security competence records",
    "Records of role-based secure development training completion for human developers, and version-controlled security instructions, guardrails and evaluation results for AI coding agents.",
    mechanism="periodic-manual", freshness="P1Y", fmt="Training records plus agent instruction file versions",
    prov=["person or agent identifier", "content version", "completion date or evaluation date"])
c.E("agentprov", "AI coding agent provenance and permission records",
    "Per-change records identifying the agent, model, runtime, session, tools and permissions used, files changed and the human accountable for acceptance; plus the agent permission configuration in force.",
    producer="Praxis work protocol and provenance (exists in tool repositories; not operated for a product)", mechanism="event-driven-automated",
    fmt="Praxis events (JSON Lines) plus agent configuration snapshot",
    prov=["execution identifier", "actor kind", "provider", "model", "runtime", "commit", "accountable human"],
    status="partially-implemented",
    notes="Praxis records agent actor identity and content digests for repository work (praxis@12bf9951 docs/work-protocol.md, docs/agent-provenance.md). Actor identity is self-reported by the executing process and is not independently authenticated.")
c.E("lang", "Language, unsafe code and native interop inventory",
    "Per-build inventory of languages and runtimes in the shipped product, compiler settings (warnings as errors, unsafe code disallowed), every native interop or unsafe block, and every non-F# component with its approval.",
    mechanism="event-driven-automated", fmt="JSON inventory", prov=["commit", "project", "language", "compiler flags", "interop site", "approval reference"])
c.E("attest", "Secure software development attestation package",
    "Signed attestation of conformance to secure development practices (for example the CISA common form) with supporting SSDF evidence, plan of action for gaps and the officer who signed.",
    mechanism="periodic-manual", freshness="P1Y", fmt="Signed PDF plus evidence index", prov=["product", "version range", "signer", "date"], disclosure="customer-only")
c.E("devenv", "Development environment and test data controls evidence",
    "Configuration evidence that development, test and production are separated, that production data is not used in non-production without approved masking, and that secrets are absent from source and injected at runtime.",
    mechanism="periodic-automated", freshness="P30D", fmt="Configuration snapshots plus secret scan results", prov=["environment", "scan tool version", "timestamp"])

c.C("sdlstd", "Adopted secure development standard aligned to SSDF",
    "Adopt and version a secure development standard that maps to NIST SSDF practices, assign owners and review it on material change.",
    "administrative", "L10-external-or-manual", ["Echelon governance (not established)"], ["sdlpolicy"],
    policies=["SEC-DB-001", "SEC-UI-001", "SEC-UI-002", "SEC-LANG-001", "SEC-LANG-002", "SEC-EXEC-001", "SEC-DATA-001", "SEC-CRYPTO-001", "SEC-AUTH-001", "SEC-SUPPLY-001"],
    refs=[SSDF("PO.1"), SAMM("Governance: Policy and Compliance"), "SRC-ISO-27001-2022@A.8.25"], owner=SEC,
    residual=["The Standard is proposed, not adopted; no approval record exists."])
c.C("reqtrace", "Machine-checked security requirement traceability",
    "Link every security requirement and invariant to implementing changes, tests and evidence; fail validation when a control-relevant change has no mapped requirement or a requirement has no test.",
    "preventive-gate", "L5-build-release-gate", ["Praxis (exists; record validation)", "Tutela (exists; invariant and evidence model)"], ["reqtrace"],
    requirements=["SOC2-007", "UNB-TRACE-002"], refs=[SSDF("PO.1"), SAMM("Design: Security Requirements")])
c.C("review", "Independent review of every change; two approvers for control-relevant modules",
    "Require review by someone other than the author for every change and two approvers, neither the author, for control-relevant modules; an AI agent cannot be the sole reviewer of an AI-authored change.",
    "preventive-gate", "L5-build-release-gate", ["Source control branch protection (not configured for a product)"], ["review"],
    related=["UNB-CTRL-070"], requirements=["CNV-PLT-010"], refs=[SSDF("PW.7"), "SRC-PCI-DSS-4.0.1@Req 6.2.3", "SRC-ISO-27001-2022@A.8.28"],
    residual=["With a very small team, two independent human approvers may not exist; the requirement cannot be met by headcount alone."])
c.C("sectest", "Security testing gates in the build",
    "Run static analysis including F#-specific rules, dependency and secret scanning, negative and property tests on every change; block merge on failures or on a tool failing to run.",
    "preventive-gate", "L5-build-release-gate", ["Praxis CI workflow (exists for tool repositories)", "F# analyzers (ecosystem exists; rules not selected)"], ["sectest"],
    refs=[SSDF("PW.7"), SSDF("PW.8"), "SRC-NIST-IR-8397", "SRC-FSHARP-ANALYZERS"],
    residual=["Mainstream SAST coverage of F# is limited; detection depends on structural rules and custom analyzers."])
c.C("training", "Role-based secure development competence for humans and agents",
    "Provide role-based secure development training to human developers at onboarding and annually, and maintain versioned, tested security instructions and tool restrictions for AI coding agents.",
    "administrative", "L10-external-or-manual", ["Echelon governance (not established)", "Agent instruction files (AGENTS.md exists in repositories)"], ["training"],
    refs=[SSDF("PO.2"), "SRC-PCI-DSS-4.0.1@Req 6.2.2", SAMM("Governance: Education and Guidance")], owner=SEC)
c.C("agentperm", "Bounded AI coding agent permissions and provenance",
    "Run coding agents with least-privilege repository and tool permissions, no production credentials, no ability to merge or release, and record actor, model, runtime and accountable human for every change.",
    "preventive-structural", "L3-restricted-interface", ["Praxis work protocol and provenance (exists)", "Agent runtime permission settings"], ["agentprov", "review"],
    requirements=["SOC2-017"], refs=["SRC-NIST-SP800-218A", "SRC-OWASP-AGENTIC-AI", SSDF("PO.5")],
    residual=["Agent actor identity in Praxis is self-reported.", "Prompt injection through repository content, issues or dependencies can steer an agent."])
c.C("lang", "Memory-safe language policy enforced by build configuration",
    "Restrict shipped application code to approved memory-safe languages with F# as default, disallow unsafe code and unreviewed native interop through compiler settings and analyzers, and inventory exceptions.",
    "preventive-gate", "L4-compiler-enforced", ["F# compiler and MSBuild configuration", "Directory.Build.props (TreatWarningsAsErrors set in Praxis and Strata)"], ["lang"],
    policies=["SEC-LANG-001", "SEC-LANG-002"], cwe=["CWE-119", "CWE-787", "CWE-416", "CWE-111"], refs=["SRC-ECH-SCS-0.1@SEC-LANG-001!", SSDF("PW.6")],
    residual=["The .NET runtime, WebAssembly runtime and native dependencies are not memory-safe by this policy.", "Limen's kernel is TypeScript and a C# interop file exists."])
c.C("attest", "Customer-facing secure development attestation",
    "Produce and sign a secure development attestation only when supporting evidence exists, with an explicit plan of action for unmet practices.",
    "administrative", "L10-external-or-manual", ["Echelon governance (not established)"], ["attest"],
    refs=["SRC-CISA-SSDF-ATTESTATION", "SRC-OMB-M-22-18"], owner=SEC)
c.C("devenv", "Separated environments, no production data in development, no secrets in source",
    "Separate development, test and production accounts and credentials, prohibit production data in non-production without approved masking, and block secrets in source through scanning.",
    "preventive-gate", "L5-build-release-gate", ["Secret scanner (not selected)", "Cloud account structure (not chosen)"], ["devenv"],
    policies=["SEC-CRYPTO-001"], cwe=["CWE-798", "CWE-540"], refs=["SRC-ISO-27001-2022@A.8.31", "SRC-ISO-27001-2022@A.8.33", SSDF("PO.5"), "SRC-GITLEAKS"])

a1 = c.A("Secure development lifecycle framework and maturity",
    "Customers need to know whether software is built under a defined, followed and improving secure development process.",
    "Echelon builds all products under an adopted secure development standard that maps every practice to NIST SSDF tasks, measures maturity against OWASP SAMM annually, and enforces most practices as automated gates whose results are retained as evidence. The Secure Construction Standard's structural rules are the technical core.",
    ["sdlstd"], ["sdlpolicy"], policies=["SEC-DB-001", "SEC-UI-001", "SEC-UI-002", "SEC-LANG-001", "SEC-SUPPLY-001"],
    current="The Echelon Secure Construction Standard v0.1 is proposed; formal adoption is not established. No SSDF or SAMM self-assessment exists. Tool repositories use Praxis governance and CI validation.",
    statement="Echelon has a proposed Secure Construction Standard (v0.1) that is not yet formally adopted. An SSDF-mapped secure development standard is planned.",
    kind="planned", mechanism="periodic-manual", freshness="P1Y", automation="partial", impl="low", rec="low", owner=SEC)
a2 = c.A("Security requirements and traceability",
    "Customers need assurance that security requirements are defined before building and verifiably implemented.",
    "Security requirements and invariants are recorded as identified, versioned records; every control-relevant change maps to requirements, tests and evidence, and validation fails on gaps. Abuse cases and negative requirements are written alongside functional ones.",
    ["reqtrace"], ["reqtrace"], requirements=["SOC2-007", "UNB-TRACE-002", "UNB-TRACE-004"], mechanism="event-driven-automated", impl="medium", rec="low",
    current="Unbound has an extensive requirements baseline (1,653 records, unbound@9b38de47) including security-relevant requirements; traceability to code and tests cannot exist because no code exists. Praxis validates record integrity in its own repositories.")
a3 = c.A("Code review and independent verification of changes",
    "Customers need assurance that no single person or agent can introduce unreviewed code into the product.",
    "Every change is reviewed by someone other than its author; changes to control-relevant modules (gate, ledger, reservations, holds, authority, dispatch) need two approvers, neither the author; an AI agent is never the sole reviewer of agent-authored code; review records and automated check results are retained per change. Review focuses on design and invariants; mechanical weakness detection is delegated to automated gates.",
    ["review", "sectest"], ["review", "sectest"], requirements=["CNV-PLT-010", "SOC2-011"], mechanism="event-driven-automated", impl="low", rec="medium",
    current="Not established for a product. Limen's CODEOWNERS (limen@743cdb9b:.github/CODEOWNERS) requires the single repository owner's review for guardrail paths; no two-person review is evidenced.",
    oq=["How will two-approver review be met if Echelon has one human engineer? Not established."],
    challenge=ch(
        customer_intent="Prevent malicious or careless code from reaching production unseen.",
        adverse_outcome="Backdoor, logic bomb or vulnerability introduced by one actor.",
        conventional_control_effectiveness="Peer review catches some defects and deters insiders, but reviewers miss most injection-class bugs and rubber-stamping is common; effectiveness depends on reviewer independence and attention.",
        legally_required="No; PCI DSS 6.2.3 requires review of bespoke code for card environments only.",
        contractually_required="Commonly asked and expected by SOC 2 auditors under CC8.1.",
        historical_convention="Pull request approval by one peer.",
        architectural_elimination="Weakness classes removed structurally need less reviewer attention; review can concentrate on invariants and authority.",
        automatic_enforcement="Branch protection, required checks, module tagging that raises approval count.",
        continuous_evidence="Per-change review metadata and provenance.",
        stronger_alternative="Structural restriction plus automated gates plus human review of control-relevant changes only, with AI review as an addition.",
        alternative_verifiable="Yes from source control metadata.",
        customer_acceptance_likelihood="Uncertain; auditors expect independent human review and segregation regardless of team size.",
        invalidating_conditions="A single human with administrative rights over branch protection can bypass the control.",
        conventional_cost="Reviewer time.", alternative_cost="Gate engineering plus external reviewer retainer if headcount is insufficient.",
        alternative_risks="Overreliance on AI review that shares the authoring model's blind spots.",
        supporting_arguments=["Concentrates scarce human attention where it matters."],
        opposing_arguments=["Independence is the point of the control and cannot be automated away.", "Small team cannot meet two-approver rule today."],
        technical_effectiveness="equivalent", institutional_acceptance="uncertain"))
a4 = c.A("Security testing integrated into the development pipeline",
    "Customers need assurance that security testing happens on every change, not only before audits.",
    "Every change runs static analysis (including F#-specific semantic rules for the Secure Construction Standard), dependency and secret scanning, property-based and negative tests, and pre-production dynamic testing; merges and releases are blocked on failures or on a tool failing to run; scanners are benchmarked against known-vulnerable and safe fixtures so their limits are documented.",
    ["sectest"], ["sectest"], mechanism="event-driven-automated", impl="medium", rec="low",
    current="Echelon tool repositories run CI validation and treat compiler warnings as errors (praxis@12bf9951 and strata@c6a384ec Directory.Build.props). No security scanning pipeline for a product exists, and F# scanner validation has not been performed.")
a5 = c.A("Developer security training and agent security instructions",
    "Customers need assurance that people and agents writing code know how to avoid common vulnerabilities.",
    "Human developers complete role-based secure development training at onboarding and annually, with completion recorded. AI coding agents operate under versioned security instructions and tool restrictions that are evaluated against known-vulnerable tasks when changed. Because most weakness classes are removed structurally, training emphasizes authority, invariants and threat modeling over syntax-level rules.",
    ["training"], ["training"], mechanism="periodic-manual", freshness="P1Y", automation="partial", impl="low", rec="low", owner=SEC,
    current="No training program located. Repositories contain agent instruction files (AGENTS.md, CLAUDE.md) that govern work protocol, not security training.",
    statement="Echelon has not established a developer security training program. One is planned.", kind="planned",
    challenge=ch(
        customer_intent="Reduce vulnerabilities introduced through developer ignorance.",
        adverse_outcome="Recurring preventable weaknesses.",
        conventional_control_effectiveness="Evidence that annual awareness-style training reduces vulnerability rates is weak; it mainly produces completion records.",
        legally_required="No general statute; PCI DSS 6.2.2 requires annual training for developers of bespoke software in card environments.",
        contractually_required="Frequently asked; auditors test completion records.",
        historical_convention="Annual secure coding course with completion certificate.",
        architectural_elimination="Weakness classes made unavailable (no dynamic SQL, no user HTML) do not depend on developer knowledge.",
        automatic_enforcement="Gates catch violations regardless of training.",
        continuous_evidence="Gate results are better evidence of outcome than training records.",
        stronger_alternative="Structural rules plus gates, with targeted training on design and authority, and evaluated agent instructions.",
        alternative_verifiable="Partially; gate results are verifiable, agent evaluation is first-party.",
        customer_acceptance_likelihood="Training records will still be requested; replacement unlikely to be accepted.",
        invalidating_conditions="Work outside gated paths (infrastructure, scripts) still depends on knowledge.",
        conventional_cost="Low.", alternative_cost="Low to medium for agent evaluation.",
        alternative_risks="Agents may not generalize instructions.",
        supporting_arguments=["Outcome evidence beats attendance evidence."],
        opposing_arguments=["Training is cheap and expected; dropping it creates questionnaire failures for little saving."],
        technical_effectiveness="stronger", institutional_acceptance="unlikely"))
a6 = c.A("AI coding agents writing production code",
    "Customers need assurance that code written by AI agents is attributable, bounded, reviewed and no less secure than human-written code.",
    "AI coding agents work under least-privilege permissions with no production credentials and cannot merge or release; every agent change records the agent, model, runtime, execution and accountable human through Praxis provenance; agent-authored changes pass the same gates plus human review for control-relevant modules; repository content is treated as untrusted input to agents; agent configurations and instructions are version-controlled and change-reviewed.",
    ["agentperm", "review"], ["agentprov", "review"], status="partially-implemented",
    rationale="Praxis provenance recording of agent actors exists and is used in Echelon repositories; the permission boundary, review rule and product scope are not established.",
    current="Echelon repositories are worked on by AI agents and record agent provenance through Praxis (for example AGENTS.md provenance blocks naming openai/codex). Actor identity is self-reported. No product code exists; agent permissions for production are undefined.",
    provable="Praxis provenance events in Echelon tool repositories showing agent actor attribution; not independently verified and not for a production product.",
    statement="Echelon's development tooling records which AI agent, model and runtime contributed each change in its repositories. Controls for agent-authored production code (permissions, review rules) are planned, not in operation.",
    kind="qualified-current-fact", requirements=["SOC2-017", "SOC2-029"], mechanism="event-driven-automated", impl="medium", rec="low",
    challenge=ch(
        customer_intent="Know who or what wrote the code that handles their money and data, and that it was checked.",
        adverse_outcome="Insecure or malicious code introduced by an agent, including through prompt injection, without accountable review.",
        conventional_control_effectiveness="Conventional SDLC controls assume human authors; many questionnaires do not yet ask about agents at all.",
        legally_required="No statute specific to AI-written code; EU AI Act obligations do not attach to coding assistants as such.",
        contractually_required="Emerging; some customers now ask whether AI generates code and whether it is reviewed.",
        historical_convention="Treat AI suggestions as developer output under normal review.",
        architectural_elimination="Structural rules apply equally to agent output; unavailable operations cannot be generated into working code.",
        automatic_enforcement="Same gates; permissions enforced by runtime and source control.",
        continuous_evidence="Per-change provenance with actor and model.",
        stronger_alternative="Provenance by construction plus structural rules plus human review where authority matters.",
        alternative_verifiable="Partially; provenance is self-reported by the agent process.",
        customer_acceptance_likelihood="Uncertain; heavy agent use may concern conservative financial customers regardless of controls.",
        invalidating_conditions="Agents holding credentials that allow merging or deploying; provenance records that can be edited.",
        conventional_cost="Review time.", alternative_cost="Low; Praxis exists.",
        alternative_risks="Volume of agent changes overwhelms human review.",
        supporting_arguments=["Attribution is more complete than typical human-only teams record."],
        opposing_arguments=["Self-reported identity is not authentication.", "Review capacity may not scale with agent output."],
        technical_effectiveness="unknown", institutional_acceptance="uncertain"))
a7 = c.A("Language choice and memory safety",
    "Customers need assurance that the product is not exposed to memory corruption vulnerabilities and understand the risks of a less common language.",
    "Application code is F# on .NET, a memory-safe, bounds-checked runtime; unsafe code and unreviewed native interop are disabled by compiler configuration and inventoried per build; non-F# code (the TypeScript Limen kernel, interop glue) is minimal, listed and reviewed. Echelon states plainly that memory safety does not prevent logic, authorization, arithmetic or denial-of-service defects, nor defects in the runtime and native dependencies, and that F# has a smaller security tooling and talent ecosystem, which it compensates for with structural rules and custom analyzers.",
    ["lang"], ["lang"], policies=["SEC-LANG-001", "SEC-LANG-002"], requirements=["UNB-PLAT-006"],
    current="Echelon tool repositories are F# and .NET with warnings as errors. Limen's browser kernel is TypeScript and its WebAssembly site includes a small C# JSExport marshalling file. No product exists.",
    mechanism="event-driven-automated", impl="low", rec="low",
    challenge=ch(
        customer_intent="Avoid the memory corruption vulnerability class and be confident the stack is supportable.",
        adverse_outcome="Remote code execution through memory corruption; or inability to staff and patch an uncommon stack.",
        conventional_control_effectiveness="Conventional programs rely on scanning C and C++ code; memory-safe languages remove the class at the language level.",
        legally_required="No; CISA and partner agencies recommend memory-safe languages as guidance.",
        contractually_required="Rarely asked directly.",
        historical_convention="Mainstream languages (Java, C#, Python, JavaScript).",
        architectural_elimination="Eliminates memory corruption in managed code within scope; not in the runtime, native libraries or interop.",
        automatic_enforcement="Compiler flags and analyzers.",
        continuous_evidence="Per-build language and interop inventory.",
        stronger_alternative="F# with exhaustive matching and validated types adds logic-level safety beyond C#.",
        alternative_verifiable="Yes for build configuration.",
        customer_acceptance_likelihood="Memory safety likely accepted; F# talent and tooling concerns may be raised by procurement.",
        invalidating_conditions="Unreviewed native dependencies, unsafe blocks or P/Invoke.",
        conventional_cost="Not applicable.", alternative_cost="Smaller hiring pool; fewer commercial SAST tools support F#.",
        alternative_risks="Key-person dependence on F# expertise; limited third-party security tool coverage.",
        supporting_arguments=["Removes a major vulnerability class by construction.", "Type system supports validated domain types."],
        opposing_arguments=["Memory safety is common to most modern managed languages; it is not a differentiator against Java or C#.", "F# scanner coverage gap is real."],
        technical_effectiveness="stronger", institutional_acceptance="likely"))
a8 = c.A("Secure software attestation and SDLC evidence for customers",
    "Regulated and public-sector customers need formal evidence of secure development practices to meet their own obligations.",
    "Echelon provides on request an SSDF-mapped practice statement with evidence index, and, where a customer requires it, signs a secure software development attestation only for practices it can evidence, with a plan of action for the rest. Supporting evidence is generated from build and review records rather than assembled manually.",
    ["attest", "sdlstd"], ["attest", "sdlpolicy"], mechanism="periodic-manual", freshness="P1Y", automation="partial", impl="low", rec="low", owner=SEC,
    current="No attestation has been made or could truthfully be made today.",
    statement="Echelon cannot currently provide a secure software development attestation; it has no production software. This is planned before selling to customers that require it.", kind="not-available")
a9 = c.A("Development environment separation, secrets and test data",
    "Customers need assurance that their data is not used in development and that code and credentials are protected during development.",
    "Development, test and production use separate accounts, credentials and networks; production data is never copied to non-production unless masked through an approved, logged process; secrets are injected at runtime from a managed store and blocked from source by scanning on every push; access to source repositories requires MFA and is reviewed.",
    ["devenv"], ["devenv"], policies=["SEC-CRYPTO-001"], mechanism="periodic-automated", freshness="P30D", impl="low", rec="low")

Q = c.Q
# a1 (6)
Q(a1, "SDLC framework", "Do you follow a documented secure software development lifecycle, and which framework is it based on?",
  "Software built without defined security practices.", [SSDF("PO.1"), "SRC-ISO-27001-2022@A.8.25", "SRC-CSA-CCM-V4@AIS-01", "SRC-EDUCAUSE-HECVAT"], imp="high",
  alt=["Describe your secure development methodology.", "Is your SDLC aligned to NIST SSDF, OWASP SAMM or BSIMM?"])
Q(a1, "SDLC maturity", "Have you assessed your secure development practices against a maturity model such as OWASP SAMM or BSIMM, and what were the results and improvement targets?",
  "No measurement of whether practices are improving or followed.", [SAMM("Governance: Strategy and Metrics"), "SRC-BSIMM"], cls="customer-preference", imp="medium")
Q(a1, "Policy adoption", "Is your secure development standard formally approved by management, versioned and reviewed on a schedule, and who owns it?",
  "Unapproved standards are not binding and erode under schedule pressure.", ["SRC-ECH-SCS-0.1!", "SRC-AICPA-TSC@CC5.3", SSDF("PO.1")], cls="certification-criteria", imp="medium")
Q(a1, "Regulated outsourced development", "As a provider of externally developed software to a regulated institution, can you document the secure development practices our examiners will expect us to have evaluated?",
  "Institution cannot evidence oversight of its software vendor's development practices.", ["SRC-FFIEC-DAM-BOOKLET", "SRC-INTERAGENCY-TPRM-2023"], cls="supervisory-guidance", imp="high",
  ind=["banking", "financial-services"], jur=["US-federal"], auth="Federal banking agencies (FFIEC members)")
Q(a1, "Subcontracted development", "Is any development performed by contractors, offshore teams or third parties, and are they bound to the same secure development requirements?",
  "Outsourced code bypasses internal practices.", ["SRC-ISO-27001-2022@A.8.30", "SRC-NIST-SP800-53-R5@SA-4"], imp="medium")
Q(a1, "SDL metrics", "Which metrics do you track for the secure development process (gate failures, time to fix, escaped defects), and can you share recent values?",
  "Process exists on paper without measurable operation.", [SAMM("Governance: Strategy and Metrics"), "SRC-ECH-UNB-SOC2-DIRECTIVE@SOC2-034!"], cls="customer-preference", imp="low")
# a2 (4)
Q(a2, "Security requirements", "How are security requirements identified and documented for new features before development begins?",
  "Security considered only after implementation.", [SSDF("PO.1"), SAMM("Design: Security Requirements"), "SRC-ISO-27001-2022@A.8.26"], imp="medium")
Q(a2, "Traceability", "Can you trace a given security requirement to the code that implements it, the tests that verify it and the evidence that it operates?",
  "Requirements are declared but never verified.", ["SRC-ECH-UNB-SOC2-DIRECTIVE@SOC2-007!", "SRC-ECH-UNB-BASELINE@UNB-TRACE-002!"], cls="echelon-internal", imp="medium")
Q(a2, "Abuse cases", "Do you write abuse and misuse cases (for example grant splitting, account takeover, insider fraud) as testable requirements?",
  "Only intended behavior is specified and tested.", [SAMM("Design: Security Requirements"), "SRC-ECH-UNB-BASELINE@UNB-TRACE-004!"], imp="medium", ind=FIN)
Q(a2, "Customer requirements", "How do contractual or regulatory security requirements from customers like us flow into your product requirements and get verified?",
  "Customer-specific obligations are agreed but not implemented.", ["SRC-INTERAGENCY-TPRM-2023", "SRC-ISO-27001-2022@A.8.26"], cls="contractual-common", imp="medium", ind=FIN)
# a3 (6)
Q(a3, "Code review", "Is all code peer reviewed before release, and does the review include security considerations?",
  "Unreviewed changes introduce vulnerabilities or malicious code.", [SSDF("PW.7"), "SRC-PCI-DSS-4.0.1@Req 6.2.3", "SRC-CSA-CCM-V4@AIS-04"], imp="high",
  alt=["Describe your code review process.", "Are code changes reviewed by someone other than the author?"])
Q(a3, "Reviewer independence", "Can a developer merge or release their own change without another person's approval, including administrators with rights over branch protection?",
  "Administrators bypass review controls.", ["SRC-AICPA-TSC@CC8.1", "SRC-NIST-SP800-53-R5@CM-5", "SRC-ECH-UNB-BASELINE@CNV-PLT-010!"], cls="certification-criteria", imp="high")
Q(a3, "Control-relevant modules", "Do changes to code that controls money movement, authorization or ledger postings receive stricter review than other changes, and how are those modules identified?",
  "High-risk code receives the same light review as low-risk code.", ["SRC-ECH-UNB-BASELINE@CNV-PLT-010!", "SRC-SOX-404^"], imp="high", ind=FIN, prod=["unbound"])
Q(a3, "Review evidence", "What evidence of code review can you provide for a sample of changes in the period, including reviewer identity and timing?",
  "Review claims cannot be tested by auditors.", ["SRC-AICPA-TSC@CC8.1", "SRC-AICPA-SOC2-GUIDE"], cls="certification-criteria", imp="medium", disclosure="auditor-only")
Q(a3, "Small team review", "With a small engineering team, how do you achieve independent review when the reviewer may also be the only other person who understands the code?",
  "Independence is nominal in very small teams.", ["SRC-ECH-UNB-BASELINE@CNV-PLT-010!", "SRC-INTERAGENCY-TPRM-2023"], cls="customer-preference", imp="medium")
Q(a3, "AI-assisted review", "If AI tools assist or perform code review, what decisions are they allowed to make, and is a human accountable for approval?",
  "AI review substitutes for human accountability.", ["SRC-NIST-SP800-218A", "SRC-OWASP-AGENTIC-AI"], imp="medium")
# a4 (5)
Q(a4, "Pipeline security testing", "Which security tests run automatically on every code change, and do failures block the change?",
  "Security testing is periodic and does not prevent defective releases.", [SSDF("PW.7"), SSDF("PW.8"), "SRC-CSA-CCM-V4@AIS-05", "SRC-NIST-IR-8397"], imp="high",
  alt=["Do you perform SAST and DAST as part of your build pipeline?"])
Q(a4, "F# tooling", "Your product is written in F#, which many commercial static analysis tools support poorly. How do you obtain static analysis coverage, and how have you measured what your tools miss?",
  "Static analysis gives false assurance on an unsupported language.", ["SRC-FSHARP-ANALYZERS", "SRC-NIST-SAMATE", "SRC-OWASP-BENCHMARK", "SRC-ECH-SCS-0.1@Scanner validation!"], cls="customer-preference", imp="medium")
Q(a4, "Suppressions", "Can a developer or coding agent override a failing security gate to merge a change, and if so, who must approve the override, is it recorded with the change, and when does it lapse?",
  "Suppressions silently hide real defects.", [SSDF("RV.2"), "SRC-ECH-SCS-0.1@Enforcement model!"], imp="medium")
Q(a4, "Fuzzing and property testing", "Do you use fuzzing or property-based testing for parsers, financial calculations and state machines?",
  "Edge-case defects escape example-based tests.", ["SRC-NIST-IR-8397", "SRC-OPENSSF-SCORECARD@Fuzzing"], cls="customer-preference", imp="low")
Q(a4, "Release criteria", "What security criteria must a release meet before production deployment, and who can override them?",
  "Releases ship with known security failures.", [SSDF("PO.4"), "SRC-ISO-27001-2022@A.8.29"], imp="medium")
# a5 (4)
Q(a5, "Developer training", "Do developers receive secure coding training at hire and at least annually, and can you provide completion records?",
  "Developers unaware of common weaknesses.", ["SRC-PCI-DSS-4.0.1@Req 6.2.2", SSDF("PO.2"), "SRC-CIS-CONTROLS-V8.1@16.9", "SRC-ISO-27001-2022@A.6.3"], cls="contractual-common", imp="medium",
  alt=["Are developers trained in OWASP Top 10?"])
Q(a5, "Training content", "Is developer training specific to your technology stack and threat profile, rather than generic awareness content?",
  "Generic training does not address the vulnerabilities actually possible.", [SAMM("Governance: Education and Guidance")], cls="customer-preference", imp="low")
Q(a5, "Agent instructions", "When AI agents write code, how are secure coding expectations given to them, versioned and tested for effect?",
  "Agents ignore or misapply security practices.", ["SRC-NIST-SP800-218A", "SRC-OWASP-AGENTIC-AI"], imp="medium")
Q(a5, "Security champions", "Is there a designated person with security expertise who supports developers and reviews designs?",
  "No security expertise available during development.", [SAMM("Governance: Education and Guidance"), "SRC-BSIMM"], cls="customer-preference", imp="low")
# a6 (7)
Q(a6, "AI-generated code", "Do you use AI tools or agents to write production code, and if so, what share of code is AI-generated?",
  "Unknown extent of AI-generated code in critical systems.", ["SRC-NIST-SP800-218A", "SRC-NIST-AI-600-1"], cls="customer-preference", imp="high")
Q(a6, "Agent attribution", "Can you identify, for any line of production code, whether it was written by a person or an AI agent, which model and tool, and which human accepted it?",
  "AI contributions cannot be attributed or audited.", ["SRC-NIST-SP800-218A", "SRC-ECH-UNB-SOC2-DIRECTIVE@SOC2-017!"], cls="customer-preference", imp="medium")
Q(a6, "Agent permissions", "What permissions do AI coding agents have: can they push to protected branches, approve changes, access secrets, run deployments or reach production data?",
  "Agents with broad permissions become a privileged attack path.", ["SRC-OWASP-AGENTIC-AI", SSDF("PO.5"), "SRC-NIST-SP800-53-R5@AC-6"], imp="critical")
Q(a6, "Prompt injection in development", "How do you protect coding agents from instructions embedded in repository content, issues, dependencies or web pages they read?",
  "Injected instructions cause agents to insert malicious code or leak secrets.", ["SRC-OWASP-LLM-TOP10-2025", "SRC-OWASP-AGENTIC-AI", "SRC-MITRE-ATLAS"], imp="high")
Q(a6, "Model provider data", "When coding agents run, what repository content, secrets, logs or production-derived data can enter their prompts and context, and is anything prevented from leaving your environment?",
  "Code or data disclosure to model providers.", ["SRC-NIST-AI-600-1", "SRC-ISO-42001-2023^"], imp="medium")
Q(a6, "Agent output quality", "How do you verify that AI-generated code does not include insecure patterns, fabricated dependencies or licensed code copied from training data?",
  "Hallucinated packages and insecure suggestions reach production.", ["SRC-NIST-SP800-218A", "SRC-OPENSSF-S2C2F"], imp="medium")
Q(a6, "Agent changes to controls", "Can an AI agent modify CI workflows, branch protection, security tests or its own instructions, and how are such changes controlled?",
  "Agents weaken the controls that supervise them.", ["SRC-OWASP-AGENTIC-AI", "SRC-OPENSSF-SCORECARD@Dangerous-Workflow"], imp="high")
# a7 (6)
Q(a7, "Memory safety", "Is the product written in memory-safe languages, and where does it depend on memory-unsafe code (runtimes, native libraries, interop)?",
  "Memory corruption vulnerabilities in the product or its native dependencies.", ["SRC-ECH-SCS-0.1@SEC-LANG-001!", "SRC-CISA-SECURE-BY-DESIGN", "SRC-MITRE-CWE@CWE-787!"], cls="customer-preference", imp="medium")
Q(a7, "Unsafe code", "Is unsafe code, pointer use or native interop permitted in your application code, and how is it detected and approved?",
  "Unsafe blocks reintroduce memory corruption in a managed language.", ["SRC-ECH-SCS-0.1@SEC-LANG-001!", "SRC-MITRE-CWE@CWE-111!"], cls="echelon-internal", imp="low")
Q(a7, "Language choice risk", "Why did you choose F#, and how do you manage the risks of a smaller talent pool and narrower security tool support?",
  "Key-person dependence and tooling gaps for an uncommon language.", ["SRC-FSHARP-ANALYZERS", "SRC-ECH-UNB-BASELINE@UNB-PLAT-006!"], cls="customer-preference", imp="medium",
  ind=["banking", "financial-services", "enterprise-software"])
Q(a7, "Memory safety limits", "Which vulnerability classes does your language choice not protect against, and what controls cover them?",
  "Overstated benefits of memory safety.", ["SRC-ECH-SCS-0.1@SEC-LANG-001!", "SRC-MITRE-CWE-TOP25"], cls="echelon-internal", imp="medium",
  note="The Standard states memory safety does not prevent denial of service, arithmetic errors, authorization flaws or runtime defects.")
Q(a7, "Browser code", "What code runs in the user's browser, in which languages, and who wrote it?",
  "Browser-side code is an unexamined attack surface.", ["SRC-ECH-SCS-0.1@SEC-UI-002!", "SRC-OWASP-ASVS@5.0 V3 Web Frontend Security"], imp="medium")
Q(a7, "Compiler settings", "Are compiler warnings treated as errors and is exhaustive pattern matching enforced for security-sensitive code?",
  "Incomplete case handling leaves undefined behavior in security decisions.", ["SRC-ECH-SCS-0.1@SEC-LANG-002!", SSDF("PW.6")], cls="echelon-internal", imp="low")
# a8 (4)
Q(a8, "CISA attestation", "Can you provide a signed secure software development attestation consistent with the CISA common form for the software we will use?",
  "Customer cannot meet federal or contractual attestation requirements.", ["SRC-CISA-SSDF-ATTESTATION", "SRC-OMB-M-22-18"], cls="contractual-common", imp="high",
  ind=GOVBUY + ["enterprise-software"], jur=["US-federal"], note="Legally required only for software sold to US federal agencies; others ask contractually.")
Q(a8, "Plan of action", "If you cannot attest to some secure development practices, will you provide a plan of action with dates for closing the gaps?",
  "Unmet practices remain open indefinitely.", ["SRC-OMB-M-22-18", "SRC-CISA-SSDF-ATTESTATION"], cls="contractual-common", imp="medium", ind=GOVBUY, jur=["US-federal"])
Q(a8, "Externally developed applications", "What documentation of your development security will you provide so we can satisfy our regulator's expectation that we assess externally developed applications?",
  "Regulated customer's own application security obligation unmet.", ["SRC-NYDFS-PART-500@500.8", "SRC-FTC-SAFEGUARDS-RULE@314.4(c)(4)", "SRC-INTERAGENCY-GLBA-SAFEGUARDS"], cls="legal-regulatory", imp="high",
  ind=["financial-services", "banking", "insurance", "wealth-management"], jur=["US-state:NY", "US-federal"], auth="NYDFS; FTC; federal banking agencies",
  note="The obligation falls on covered customers and flows to Echelon through their vendor assessment.")
Q(a8, "SDLC evidence generation", "Is evidence of your secure development practices generated automatically by your build and review systems, or assembled manually before assessments?",
  "Evidence assembled for audits does not reflect normal operation.", ["SRC-ECH-UNB-SOC2-DIRECTIVE@SOC2-004!", SSDF("PO.3")], cls="customer-preference", imp="low")
# a9 (3)
Q(a9, "Environment separation", "Are development, test and production environments separated, and can developers access production from development systems?",
  "Development compromise reaches production.", ["SRC-ISO-27001-2022@A.8.31", "SRC-PCI-DSS-4.0.1@Req 6.5.3", "SRC-CSA-CCM-V4@AIS-01"], imp="high")
Q(a9, "Production data in test", "Is production or customer data ever used in development or testing, and if so, how is it masked and approved?",
  "Customer data exposed in less protected environments.", ["SRC-ISO-27001-2022@A.8.33", "SRC-PCI-DSS-4.0.1@Req 6.5.5"], imp="high", ind=FIN)
Q(a9, "Secrets in source", "How do you prevent credentials and keys from being committed to source code, and what happens when one is found?",
  "Hardcoded secrets leak through repositories.", ["SRC-ECH-SCS-0.1@SEC-CRYPTO-001!", "SRC-MITRE-CWE@CWE-798!", "SRC-GITLEAKS", "SRC-NIST-IR-8397"], imp="high")

RECORDS = c.records()
