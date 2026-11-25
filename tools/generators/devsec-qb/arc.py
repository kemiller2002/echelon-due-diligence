from devseclib import *

c = Cat("ARC")
SSDF = lambda p: f"SRC-NIST-SP800-218@{p}!"
SAMM = lambda p: f"SRC-OWASP-SAMM-2@{p}"
S = lambda r: f"SRC-ECH-SCS-0.1@{r}!"
B = lambda i: f"SRC-ECH-UNB-BASELINE@{i}!"
FIN = ["financial-services", "banking", "wealth-management", "donor-advised-funds"]

c.E("tm", "Threat model records per system and material change",
    "Versioned threat models in Tutela's model (assets, trust boundaries, threats, invariants, controls, evidence, unknowns) for each system and each material change, with reviewer, date and release posture.",
    producer="Tutela (exists as a discipline and toolset; no product threat model located)", mechanism="event-driven-automated",
    fmt="Tutela records plus Folio-rendered Security Evidence Record", prov=["system", "release or commit", "author", "reviewer", "date", "gate outcome"])
c.E("dfd", "Trust boundary and data flow inventory",
    "Machine-readable inventory of trust boundaries, data flows, data classifications crossing each boundary and the enforcing control, checked against deployed configuration.",
    mechanism="event-driven-automated", fmt="JSON or YAML model plus rendered diagram", prov=["model version", "commit", "deployment identifier"])
c.E("aam", "Architectural assurance matrix",
    "Per-release matrix that classifies each security property as proven, structurally enforced, empirically tested or unverified, with scope, exclusions, enforcing mechanism, bypass tests and evidence links.",
    producer="Tutela plus Folio (proposed)", mechanism="event-driven-automated", fmt="JSON matrix plus Folio report",
    prov=["release", "property identifier", "classification", "scope", "exclusions", "evidence reference", "verifier"],
    notes="Named as assurance deliverable 4 in the Secure Construction Standard v0.1.")
c.E("bypass", "Bypass and negative test results for structural claims",
    "Results of tests that attempt to defeat each by-construction claim: raw database connections, stored procedures with dynamic SQL, HTML injection through interop, script injection in generated bundles, unsafe interop, reflection, with seeded fixtures that the checks must detect.",
    mechanism="event-driven-automated", fmt="Test report plus fixture catalog", prov=["commit", "claim identifier", "fixture identifier", "detected or not"])
c.E("types", "Domain type and state machine conformance report",
    "Report listing domain types with private constructors and their validation functions, state machines with their legal transitions, and exhaustive-match enforcement settings; with property test results.",
    mechanism="event-driven-automated", fmt="Generated JSON plus test results", prov=["commit", "type or machine name", "analyzer version"])
c.E("dbarch", "Database access architecture evidence",
    "Database role and grant export, list of database functions and their use of dynamic SQL, row-level security policies per tenant table, Strata drift status for all security-relevant objects, and list of every credential that can connect to the database.",
    producer="Strata (exists; schema compile, diff and drift) plus database catalog export (proposed)", mechanism="event-driven-automated",
    fmt="Strata plan and diff output plus catalog export", prov=["database", "Strata version", "artifact digest", "comparison state per object"])
c.E("browser", "Browser surface inventory",
    "Per-release inventory of every script, WebAssembly module, interop export and third-party resource loaded by each page, with digests, origin and approval, plus the deployed CSP and Subresource Integrity settings.",
    mechanism="event-driven-automated", fmt="JSON inventory", prov=["release", "page", "resource digest", "origin", "approval reference"])
c.E("design", "Security design review and decision records",
    "Records of security design review for new data categories, external APIs, autonomous permissions and financial workflows, with reviewer independence, decision, conditions and linked decision record.",
    mechanism="event-driven-automated", fmt="Decision records (DF-) plus review record", prov=["decision identifier", "reviewer", "date", "scope"])
c.E("failmode", "Failure mode and fail-closed test results",
    "Tests that inject dependency failures, timeouts, unknown states and partial outages into security decisions and assert deny or hold behavior.",
    mechanism="event-driven-automated", fmt="Test report", prov=["commit", "failure injected", "expected outcome", "result"])

c.C("tm", "Threat modeling for each system and material change",
    "Model assets, trust boundaries, threats and invariants before building and on each material change, and derive release posture from evidence against those invariants.",
    "preventive-procedural", "L10-external-or-manual", ["Tutela (exists)"], ["tm"],
    refs=[SSDF("PW.1"), SAMM("Design: Threat Assessment"), "SRC-CIS-CONTROLS-V8.1@16.14", "SRC-NIST-SP800-53-R5@SA-11"], owner=SEC,
    residual=["Threat models reflect the modelers' imagination; independent review is needed to find omissions."])
c.C("dfd", "Declared trust boundaries checked against deployment",
    "Declare trust boundaries and data flows as data and verify deployed network, identity and data access configuration against them.",
    "detective-automated", "L6-automated-analysis", ["Tutela (exists)", "Deployment configuration (not built)"], ["dfd"],
    refs=["SRC-NIST-SP800-53-R5@SA-17", "SRC-NIST-SP800-207"])
c.C("aam", "Scoped architectural assurance matrix",
    "Publish per release which properties are proven, structurally enforced, empirically tested or unverified, with scope and exclusions; never claim elimination outside the evidenced scope.",
    "detective-automated", "L6-automated-analysis", ["Tutela (exists)", "Folio (exists)"], ["aam", "bypass"], policies=["SEC-DB-001", "SEC-UI-001", "SEC-UI-002", "SEC-LANG-001", "SEC-EXEC-001"],
    refs=[S("Assurance deliverables"), S("Enforcement model")], owner=SEC)
c.C("bypass", "Independent bypass testing of structural restrictions",
    "Verify, with seeded fixtures and testers who did not build the restriction, that approved interfaces cannot be bypassed.",
    "detective-automated", "L8-adversarial-tested", ["Dokimos (exists; code-quality measurement, adversarial role unverified)", "External testers (not engaged)"], ["bypass"],
    refs=[S("Enforcement model"), "SRC-NIST-SP800-115"], owner=SEC)
c.C("types", "Validated domain types and explicit states",
    "Model security-relevant values as types with private constructors and validation, model workflows as explicit states with legal transitions only, and enforce exhaustive matching with warnings as errors.",
    "preventive-structural", "L2-type-system", ["F# compiler", "Ordo state-directed engineering method (exists as a method)", "Unbound domain model (not built)"], ["types"],
    policies=["SEC-LANG-002"], cwe=["CWE-20", "CWE-841", "CWE-478"], refs=[S("SEC-LANG-002"), "SRC-OWASP-ASVS@5.0 V15 Secure Coding and Architecture"])
c.C("dbarch", "Restricted database access architecture",
    "Allow only the application's restricted interface and Strata-governed schema deployments to touch authoritative databases; per-tenant roles with row-level security; no dynamic SQL in database functions; break-glass-only administrative roles.",
    "preventive-structural", "L3-restricted-interface", ["Strata (exists; schema governance, pilot, PostgreSQL 16 only)", "Managed PostgreSQL (not provisioned)"], ["dbarch", "bypass"],
    policies=["SEC-DB-001"], requirements=["CNV-ARC-001", "CNV-ARC-004", "UNB-PLAT-007", "CNV-PLT-010"], cwe=["CWE-89", "CWE-250", "CWE-284"],
    refs=[S("SEC-DB-001"), B("CNV-ARC-004")],
    residual=["SEC-DB-001 names Strata as the access path; Strata provides schema governance only, and CNV-ARC-004 assigns authoritative history to an Unbound-owned ledger component. The rule and the architecture disagree."])
c.C("browser", "Confined browser execution",
    "Confine application-authored browser script to Limen's kernel, run application logic in WebAssembly without DOM access, accept no user HTML, load no unapproved third-party script, and pin every loaded resource by digest.",
    "preventive-structural", "L3-restricted-interface", ["Limen (exists)", "Forma (exists)"], ["browser", "bypass"],
    policies=["SEC-UI-001", "SEC-UI-002"], cwe=["CWE-79", "CWE-829", "CWE-494"], refs=[S("SEC-UI-002"), S("SEC-UI-001"), "SRC-OWASP-ASVS@5.0 V3 Web Frontend Security"],
    residual=["Limen's kernel and generated JavaScript glue are themselves script that must be reviewed and tested.", "Limen has no independent security review."])
c.C("design", "Security design review before high-risk change",
    "Require documented security design review, independent of the designer, before introducing new data categories, external APIs, autonomous permissions or financial workflows.",
    "preventive-procedural", "L10-external-or-manual", ["Praxis decision records (exists)", "Tutela (exists)"], ["design"],
    requirements=["SOC2-030"], refs=[SSDF("PW.2"), SAMM("Verification: Architecture Assessment"), "SRC-ECH-UNB-SOC2-DIRECTIVE@SOC2-030!"], owner=SEC)
c.C("failclosed", "Fail-closed security decisions and bounded blast radius",
    "Make unknown, failed or timed-out security decisions deny or hold; isolate control-relevant modules and tenant data so a defect in one area cannot silently affect others.",
    "preventive-structural", "L7-property-tested", ["Unbound architecture (not built)"], ["failmode"],
    requirements=["CNV-ARC-003", "UNB-API-007"], cwe=["CWE-636", "CWE-755"], refs=["SRC-NIST-SP800-53-R5@SA-8", "SRC-CISA-SECURE-BY-DESIGN"])

a1 = c.A("Threat modeling",
    "Customers need assurance that threats to their data and money were systematically considered before the system was built and as it changes.",
    "Each Echelon system has a versioned threat model in Tutela that names assets, trust boundaries, threats, security invariants, controls and evidence; material changes update it before merge; agent, insider, tenant and supply-chain threats are explicitly modeled; release posture is derived from evidence against the invariants; threat models are reviewed by someone other than the author and shared with independent testers.",
    ["tm"], ["tm"], mechanism="event-driven-automated", automation="partial", impl="medium", rec="medium", owner=SEC,
    current="Tutela exists (tutela@476dc682) and defines the method; no threat model for Unbound or another product was located. Unbound requirements contain threat-derived requirements (TVR-SEC-*) from a threat and vulnerability register.")
a2 = c.A("Trust boundaries and data flow",
    "Customers need to understand where their data goes, which components can see it, and where it crosses trust boundaries.",
    "Trust boundaries (browser to server through Limen, tenant to tenant, sponsor to partner, application to database, platform to AI providers, platform to payment rails) and data flows are declared as data with the classification of data crossing each boundary and the enforcing control; deployed configuration is checked against the declaration on every release, and customer-facing data flow diagrams are generated from it.",
    ["dfd"], ["dfd"], mechanism="event-driven-automated", impl="medium", rec="low", products=["unbound"])
a3 = c.A("Security by construction claims and their evidence",
    "Customers need to know which security properties are guaranteed by design, within what scope, and how that guarantee is verified.",
    "Echelon publishes, per release, an architectural assurance matrix that classifies each property as proven, structurally enforced, empirically tested or unverified, with scope, exclusions (trusted infrastructure, stored procedures, interop, generated bundles, third-party scripts), the enforcing mechanism and the bypass tests. No elimination claim is made without scoped, reproducible evidence, and structural claims are independently tested for bypass before they are used to reduce any other testing.",
    ["aam", "bypass"], ["aam", "bypass"], policies=["SEC-DB-001", "SEC-UI-001", "SEC-UI-002", "SEC-LANG-001", "SEC-EXEC-001"],
    mechanism="event-driven-automated", impl="high", rec="medium", owner=SEC,
    current="The Secure Construction Standard v0.1 (proposed) states the structural rules and the matrix as a deliverable. No matrix, bypass test or enforcing analyzer exists. Several components the Standard assigns (Aegis as rule registry, Vigila as runtime monitoring) have different verified purposes.",
    challenge=ch(
        customer_intent="Have confidence that whole classes of vulnerability cannot occur, not just that none were found.",
        adverse_outcome="An overstated elimination claim leads customers and testers to skip testing a class that is in fact present.",
        conventional_control_effectiveness="Conventional programs detect instances after construction; they rarely claim class elimination.",
        legally_required="No.", contractually_required="No; customers ask for test results, not construction claims.",
        historical_convention="Scan, test, remediate.",
        architectural_elimination="Achievable within a precisely defined scope when the unsafe operation is unavailable and every bypass path is enumerated and tested.",
        automatic_enforcement="Restricted interfaces, compiler settings, analyzers and release gates.",
        continuous_evidence="Per-release matrix with bypass test results.",
        stronger_alternative="Construction plus scoped claims plus independent bypass testing.",
        alternative_verifiable="Yes, if fixtures and analyzers are published and reproducible, and an independent party attempts bypass.",
        customer_acceptance_likelihood="Technical reviewers may value it; risk and procurement functions will treat it as first-party until independently verified.",
        invalidating_conditions="Any unscanned path: trusted infrastructure code, stored procedures, interop, generated bundles, third-party scripts, administrative tools.",
        conventional_cost="Recurring scanning and testing.", alternative_cost="Upfront interface and analyzer engineering, plus independent verification.",
        alternative_risks="Institutional overconfidence; enforcing components owned by Echelon itself are a single point of failure.",
        supporting_arguments=["Prevention is cheaper than repeated detection.", "Scoped claims are falsifiable and therefore testable."],
        opposing_arguments=["Several enforcing components do not exist or have different verified purposes.", "First-party claims about first-party tools lack independence."],
        technical_effectiveness="stronger", institutional_acceptance="uncertain"))
a4 = c.A("Explicit domain states and validated domain types",
    "Customers need assurance that the system cannot enter states that violate their policies, such as a payment released without approval.",
    "Security-relevant values (amounts, EINs, routing numbers, tenant identifiers, authority grants) are types whose constructors validate and are private; workflow states are explicit discriminated unions with only legal transitions representable; exhaustive matching is compiler-enforced with warnings as errors; state machines and invariants are property-tested. Echelon is explicit that types prove representability, not that the encoded policy is the right one.",
    ["types"], ["types"], policies=["SEC-LANG-002"], requirements=["CNV-ARC-005"], mechanism="event-driven-automated", impl="medium", rec="low", products=["unbound"],
    current="Not established for a product. Ordo (ordo@db6d39ed) exists as a state-directed engineering method; Limen's README notes that F# can make illegal states unrepresentable but Limen does not create the domain model.",
    challenge=ch(
        customer_intent="Know that the workflow cannot be bypassed or confused into an unapproved state.",
        adverse_outcome="Illegal state such as disbursed-but-unapproved through a code path nobody tested.",
        conventional_control_effectiveness="Conventional assurance relies on test cases and reviews of state handling; illegal combinations of flags often go untested.",
        legally_required="No.", contractually_required="No.",
        historical_convention="Status columns, flags and procedural checks.",
        architectural_elimination="Illegal states can be made unrepresentable in the domain model; persistence and external inputs must still be validated on load.",
        automatic_enforcement="Compiler.",
        continuous_evidence="Conformance report and property tests per build.",
        stronger_alternative="Types plus database constraints plus property tests.",
        alternative_verifiable="Yes by code inspection and tests, but requires reviewers able to read F#.",
        customer_acceptance_likelihood="Likely as engineering evidence; not a substitute for audit sampling.",
        invalidating_conditions="Deserialization or database reads that construct domain values without validation; reflection.",
        conventional_cost="Testing effort.", alternative_cost="Design discipline; low tool cost.",
        alternative_risks="Correctly typed but wrong policy.",
        supporting_arguments=["Compile-time guarantees are cheaper than runtime detection."],
        opposing_arguments=["Customers and auditors may not be able to inspect or interpret the guarantee."],
        technical_effectiveness="stronger", institutional_acceptance="uncertain"))
a5 = c.A("Database access architecture and dynamic SQL elimination",
    "Customers need assurance that the database cannot be reached or manipulated except through governed, parameterized paths.",
    "Only the application's restricted typed interface and Strata-governed schema deployments touch authoritative databases. Each sponsor tenant has its own schema and role with row-level security; authoritative tables are insert-only for the application role; database functions contain no dynamic SQL; administrative roles are break-glass only with two-person activation; Strata drift checks cover grants, triggers and policies and block release on 'not-compared' or 'unverifiable' states. The scope of the no-dynamic-SQL claim, including stored procedures, migrations, reporting and trusted infrastructure, is stated with evidence.",
    ["dbarch", "bypass"], ["dbarch", "bypass"], policies=["SEC-DB-001"], requirements=["CNV-ARC-001", "CNV-ARC-004", "UNB-PLAT-007", "CNV-PLT-010"],
    mechanism="event-driven-automated", impl="high", rec="low", products=["unbound"],
    current="Strata exists as a pilot declarative schema tool for PostgreSQL 16 with explicit not-compared and unverifiable states (strata@c6a384ec). It does not provide a runtime query interface. No Unbound database exists.",
    oq=["SEC-DB-001 requires all application database access through Strata, while CNV-ARC-004 limits Strata to schema governance. Which governs?"],
    challenge=ch(
        customer_intent="Ensure nobody, including Echelon engineers and tools, can alter financial records outside governed paths.",
        adverse_outcome="Injection or direct tampering with ledger data.",
        conventional_control_effectiveness="Parameterized queries plus DBA access controls are effective but rarely cover database-side dynamic SQL and administrative tooling comprehensively.",
        legally_required="No specific technique; safeguards rules require reasonable access control.", contractually_required="Common questionnaire topic.",
        historical_convention="ORM, DBA roles, periodic access review.",
        architectural_elimination="Within scope if all connection paths are enumerated and database functions are inspected; trusted infrastructure and stored procedures are the usual gaps.",
        automatic_enforcement="Role grants declared in Strata, drift detection, analyzer over SQL source.",
        continuous_evidence="Strata drift status per release and grant export.",
        stronger_alternative="Declared grants plus insert-only roles plus drift gating.",
        alternative_verifiable="Yes from catalog exports and Strata output.",
        customer_acceptance_likelihood="Likely for the access model; elimination claim needs independent reproduction.",
        invalidating_conditions="A reporting or support tool with direct database credentials; a function using EXECUTE with concatenated input; a PostgreSQL major version Strata does not support.",
        conventional_cost="DBA effort and audits.", alternative_cost="Strata maturation from pilot; Unbound ledger component.",
        alternative_risks="Pilot-status tool on the critical path.",
        supporting_arguments=["Strata's explicit unknown states avoid false clean diffs."],
        opposing_arguments=["The enforcing runtime component named by SEC-DB-001 does not exist.", "Strata is pilot status and tested only on PostgreSQL 16."],
        technical_effectiveness="stronger", institutional_acceptance="uncertain"))
a6 = c.A("Browser architecture: no user HTML and no application script outside Limen",
    "Customers need assurance that the browser application cannot be turned against its users.",
    "The browser runs only Limen's kernel and application logic compiled to WebAssembly, which has no DOM access; the kernel binds data through a small set of declared attributes; no user HTML is accepted; no third-party script is loaded unless inventoried, approved and pinned by digest; every release inventories scripts, WebAssembly modules and interop exports and checks generated bundles for unsafe sinks. Limen itself is reviewed and tested as security-critical code.",
    ["browser", "bypass"], ["browser", "bypass"], policies=["SEC-UI-001", "SEC-UI-002"], requirements=["UNB-PLAT-006", "UNB-PLAT-002"],
    mechanism="event-driven-automated", impl="medium", rec="low", products=["unbound"],
    current="Limen exists (limen@743cdb9b): a dependency-free TypeScript browser kernel and protocol with F# WebAssembly consumers including a product site; it has an architecture check script and CODEOWNERS guardrails. No Unbound UI exists and Limen has had no independent security review.",
    challenge=ch(
        customer_intent="Prevent script injection and malicious third-party code in the browser.",
        adverse_outcome="Session hijacking, credential theft or display manipulation through injected or supply-chain script.",
        conventional_control_effectiveness="Framework encoding, CSP and script inventories are effective when maintained; third-party scripts are a common failure.",
        legally_required="No; PCI DSS 6.4.3 requires script inventory and authorization on payment pages only.",
        contractually_required="Rarely specified.",
        historical_convention="SPA framework with many npm dependencies, CSP optional.",
        architectural_elimination="Reduces application script to one small kernel; does not eliminate script, and the WebAssembly runtime loader and interop glue are generated JavaScript.",
        automatic_enforcement="Bundle inspection, CSP, Subresource Integrity.",
        continuous_evidence="Per-release browser surface inventory.",
        stronger_alternative="Kernel confinement plus inventory plus CSP.",
        alternative_verifiable="Yes for inventory; kernel correctness needs independent review.",
        customer_acceptance_likelihood="Likely as design; testers will still test.",
        invalidating_conditions="Adding analytics, chat or payment widgets; partner embedding requiring host-page script.",
        conventional_cost="CSP maintenance and scanning.", alternative_cost="Limen maintenance as a single critical component.",
        alternative_risks="Concentration risk in Limen; WebAssembly debugging tools are less mature for security testers.",
        supporting_arguments=["Dramatically smaller script surface than typical SPAs."],
        opposing_arguments=["Script still exists in the kernel; the claim moves rather than removes the surface."],
        technical_effectiveness="stronger", institutional_acceptance="likely"))
a7 = c.A("Security design review and architecture decision governance",
    "Customers need assurance that security-significant design choices are reviewed and recorded, not made ad hoc.",
    "Security design review, independent of the designer, is required before introducing new data categories, external APIs, autonomous agent permissions or financial workflows; decisions and their security rationale are recorded as decision records linked to the affected requirements and threat models; reviews are revisited on material change.",
    ["design"], ["design"], requirements=["SOC2-030"], mechanism="event-driven-automated", automation="partial", impl="low", rec="low", owner=SEC,
    current="Praxis provides decision records (DF-) and is used across Echelon repositories; Unbound requirements include owner decisions (OD-*). No security design review process with independent reviewers is established.")
a8 = c.A("Secure defaults, fail-closed behavior and blast radius",
    "Customers need assurance that failures and defects degrade safely and are contained.",
    "Unknown, failed or timed-out security decisions deny or hold; irreversible steps check current authorization and hold state atomically and fail closed (CNV-ARC-003); control-relevant modules have clear internal boundaries inside the modular monolith; tenant cells and critical command paths have reserved capacity; failure injection tests verify these behaviors.",
    ["failclosed"], ["failmode"], requirements=["CNV-ARC-003", "CNV-ARC-001", "UNB-API-007"], mechanism="event-driven-automated", impl="medium", rec="low", products=["unbound"])

Q = c.Q
# a1 (6)
Q(a1, "Threat modeling", "Do you perform threat modeling for your applications, how often, and with what methodology?",
  "Threats unconsidered until exploited.", [SSDF("PW.1"), SAMM("Design: Threat Assessment"), "SRC-CIS-CONTROLS-V8.1@16.14", "SRC-CSA-CCM-V4@AIS-04"], imp="high",
  alt=["Is threat modeling part of your SDLC?"])
Q(a1, "Threat model currency", "Is the threat model updated when the system changes materially, and how do you detect that a change requires an update?",
  "Threat model drifts from the deployed system.", [SSDF("PW.1"), SAMM("Design: Threat Assessment")], imp="medium")
Q(a1, "Threat model sharing", "Will you share your threat model, or a summary, with us and with our penetration testers?",
  "Customers and testers cannot assess coverage.", [S("External assurance and economics"), "SRC-NIST-SP800-115"], cls="customer-preference", imp="low", disclosure="nda")
Q(a1, "Agent and insider threats", "Does your threat model cover malicious insiders, compromised engineers and compromised or manipulated AI agents with legitimate access?",
  "Trusted-actor threats are excluded from design.", ["SRC-OWASP-AGENTIC-AI", B("TVR-SEC-006"), "SRC-MITRE-ATTACK"], imp="high", ind=FIN)
Q(a1, "Threat-to-control mapping", "Can you show how each identified threat maps to a control and to evidence that the control works?",
  "Threats identified but not mitigated.", ["SRC-ECH-UNB-SOC2-DIRECTIVE@SOC2-035!", SAMM("Design: Threat Assessment")], cls="echelon-internal", imp="medium")
Q(a1, "Threat model review", "Who reviews threat models, and is the reviewer independent of the team that built the system?",
  "Self-review misses the authors' blind spots.", [SAMM("Verification: Architecture Assessment"), "SRC-NIST-SP800-53-R5@SA-11"], imp="low")
# a2 (5)
Q(a2, "Data flow", "Can you provide a data flow diagram showing where our data is stored, processed and transmitted, including third parties?",
  "Customer cannot assess where data is exposed.", ["SRC-CSA-CCM-V4@DSP-05", "SRC-EDUCAUSE-HECVAT", "SRC-INTERAGENCY-TPRM-2023"], cls="contractual-common", imp="high",
  alt=["Provide an architecture diagram of the solution."])
Q(a2, "Trust boundaries", "Where are the trust boundaries in your architecture, and what control enforces each one?",
  "Implicit trust between components enables lateral movement.", ["SRC-NIST-SP800-207", "SRC-NIST-SP800-53-R5@SA-17"], imp="medium")
Q(a2, "Browser boundary", "What can code running in the browser decide or do, and which decisions are always made on the server?",
  "Client-side trust allows manipulation of security decisions.", [S("SEC-UI-002"), B("CNV-PLT-010")], imp="medium")
Q(a2, "AI provider boundary", "Which data crosses to external AI model providers, under which controls, and can the provider retain or train on it?",
  "Donor or financial data leaks through AI services.", ["SRC-OWASP-LLM-TOP10-2025", "SRC-NIST-AI-600-1"], imp="high")
Q(a2, "Boundary verification", "How do you confirm that the deployed system matches the documented architecture and boundaries?",
  "Documentation describes an intended system, not the real one.", ["SRC-NIST-SP800-53-R5@CM-2", "SRC-CSA-CCM-V4@CCC-07"], imp="medium")
# a3 (6)
Q(a3, "By-construction claims", "You state that certain vulnerability classes are prevented by construction. For each claim, what is the exact scope, what is excluded, and what reproducible evidence supports it?",
  "Elimination claims overstated beyond evidenced scope.", [S("Enforcement model"), S("Assurance deliverables")], cls="echelon-internal", imp="high")
Q(a3, "Bypass testing", "How have you tested that the approved interfaces cannot be bypassed through reflection, interop, raw drivers, administrative tools or trusted infrastructure code?",
  "Restricted interfaces bypassed through unexamined paths.", [S("Enforcement model"), "SRC-NIST-SP800-115"], cls="echelon-internal", imp="high")
Q(a3, "Independent verification", "Has anyone independent of the team that built the enforcing tools verified the by-construction claims?",
  "Tool authors verifying their own tools.", ["SRC-AICPA-SSAE-18", S("External assurance and economics")], cls="customer-preference", imp="high")
Q(a3, "Testing scope reduction", "Do you ask independent testers to skip or de-scope any vulnerability class because you consider it eliminated by design?",
  "De-scoping suppresses independent discovery.", [S("External assurance and economics"), "SRC-PTES"], cls="customer-preference", imp="medium")
Q(a3, "Secure by design", "Which secure-by-design commitments do you make (for example eliminating classes of vulnerability, secure defaults), and how do you publish progress?",
  "Vendor shifts security burden to customers.", ["SRC-CISA-SECURE-BY-DESIGN"], cls="customer-preference", imp="medium", ind=["public-sector", "enterprise-software"])
Q(a3, "Enforcing component maturity", "Which of the internal tools that enforce your security rules are in production use, which are pilots, and which are not yet built?",
  "Claims depend on immature or absent tooling.", [S("Proposed system ownership (verify against repositories)")], cls="echelon-internal", imp="medium",
  note="The Standard's proposed ownership differs from verified purpose for Aegis and Vigila.")
# a4 (4)
Q(a4, "Explicit states", "Are workflow states for grants, payments and approvals modeled explicitly with defined legal transitions, and can the system persist a state outside that model?",
  "Illegal or ambiguous states lead to unauthorized effects.", [S("SEC-LANG-002"), B("CNV-ARC-005"), "SRC-MITRE-CWE@CWE-841!"], imp="high", ind=FIN)
Q(a4, "Validated types", "Are identifiers and amounts validated once at the boundary and carried as validated types, or re-validated ad hoc throughout the code?",
  "Inconsistent validation lets bad values through some paths.", [S("SEC-LANG-002"), "SRC-OWASP-ASVS@5.0 V15 Secure Coding and Architecture"], cls="echelon-internal", imp="low")
Q(a4, "Exhaustive handling", "How do you ensure that every possible outcome of a security decision (allow, deny, error, unknown) is handled explicitly?",
  "Unhandled outcomes default to allow.", [S("SEC-LANG-002"), "SRC-MITRE-CWE@CWE-478!"], cls="echelon-internal", imp="medium")
Q(a4, "Process versioning", "When workflow definitions change, what happens to in-flight instances started under the old definition?",
  "Definition changes alter approvals or deadlines of in-flight work.", [B("CNV-ARC-005")], imp="medium", ind=["donor-advised-funds"])
# a5 (6)
Q(a5, "Dynamic SQL", "Do any database functions, stored procedures, triggers or migrations use dynamic SQL, and are they included in your injection analysis?",
  "Database-side dynamic SQL escapes application controls.", [S("SEC-DB-001"), "SRC-MITRE-CWE@CWE-89!"], cls="echelon-internal", imp="high")
Q(a5, "Database access paths", "List every system, person and tool that can connect to the production database, and with which privileges.",
  "Unknown direct access paths bypass application controls.", ["SRC-NIST-SP800-53-R5@AC-6", B("CNV-PLT-010"), "SRC-AICPA-TSC@CC6.1"], imp="high")
Q(a5, "Tenant data separation", "How is each customer's data separated in the database (schema, role, row-level security, separate database), and how is that separation tested?",
  "Cross-tenant data exposure through shared tables.", [B("CNV-ARC-001"), B("UNB-PLAT-008")], imp="critical", ind=FIN)
Q(a5, "Append-only enforcement", "How is the immutability of financial history enforced: by database grants and constraints, or only by application code?",
  "Application bugs or privileged users rewrite history.", [B("UNB-IMM-001"), "SRC-ECH-UNB-SOC2-DIRECTIVE@SOC2-006!"], imp="high", ind=FIN)
Q(a5, "Schema governance", "How are database schema, grants and security policies deployed and checked for drift, and what happens when the tool cannot verify an object?",
  "Unverified schema drift silently weakens controls.", [B("CNV-ARC-004"), "SRC-NIST-SP800-53-R5@CM-3"], imp="medium")
Q(a5, "Strata scope", "Your standard routes all application database access through Strata, but Strata is described as a schema management tool. Which component performs runtime queries, and how is the standard enforced against it?",
  "Policy names an enforcement mechanism that does not exist.", [S("SEC-DB-001"), B("CNV-ARC-004")], cls="echelon-internal", imp="medium")
# a6 (6)
Q(a6, "Browser code inventory", "What scripts and modules does the browser load for our users, including third-party scripts, and how is that list controlled?",
  "Unauthorized or compromised scripts run in user sessions.", [S("SEC-UI-002"), "SRC-PCI-DSS-4.0.1@Req 6.4.3^", "SRC-OWASP-ASVS@5.0 V3 Web Frontend Security"], imp="high")
Q(a6, "Generated bundles", "Your standard limits application-authored JavaScript to Limen. Do generated bundles, WebAssembly loaders and interop glue count as application JavaScript, and how are they inspected?",
  "Generated code escapes the script restriction.", [S("SEC-UI-002")], cls="echelon-internal", imp="medium")
Q(a6, "Third-party scripts", "Do you use analytics, chat, monitoring or advertising scripts in authenticated pages?",
  "Third-party scripts read or alter sensitive pages.", ["SRC-OWASP-ASVS@5.0 V3 Web Frontend Security", "SRC-MITRE-CWE@CWE-829!"], imp="high", ind=FIN)
Q(a6, "Subresource integrity", "Are static resources served from your own origin or pinned by integrity hashes when loaded from elsewhere?",
  "CDN compromise injects script.", ["SRC-MITRE-CWE@CWE-494!", "SRC-OWASP-ASVS@5.0 V3 Web Frontend Security"], imp="low")
Q(a6, "Kernel assurance", "Limen is the only component allowed to run browser script. Has it been independently reviewed, and what happens to every Echelon application if it has a defect?",
  "Concentration of browser risk in one component.", [S("SEC-UI-002"), "SRC-NIST-SP800-161-R1"], cls="customer-preference", imp="medium")
Q(a6, "Partner embedding", "How do partner-embedded or white-labeled experiences preserve the browser restrictions when the host page is controlled by a partner?",
  "Host page script reaches embedded component.", ["SRC-OWASP-ASVS@5.0 V3 Web Frontend Security", "SRC-MITRE-CWE@CWE-1021!"], imp="medium", ind=["donor-advised-funds", "wealth-management"], prod=["unbound"])
# a7 (4)
Q(a7, "Design review", "Are new features and architecture changes reviewed for security before implementation, and by whom?",
  "Insecure designs reach implementation.", [SSDF("PW.2"), SAMM("Verification: Architecture Assessment"), "SRC-ISO-27001-2022@A.8.27"], imp="medium")
Q(a7, "Review triggers", "Which kinds of change require security design review (new data types, external integrations, AI autonomy, money movement), and how is the requirement enforced?",
  "High-risk changes skip review.", ["SRC-ECH-UNB-SOC2-DIRECTIVE@SOC2-030!"], cls="echelon-internal", imp="medium")
Q(a7, "Decision records", "Are security-significant architecture decisions documented with rationale and alternatives, and can you share relevant records?",
  "Decisions cannot be reconstructed or challenged.", ["SRC-ISO-27001-2022@A.8.27", "SRC-NIST-SP800-53-R5@SA-17"], cls="customer-preference", imp="low")
Q(a7, "Security principles", "Which secure engineering principles guide your architecture (least privilege, defense in depth, deny by default), and where are they documented?",
  "No consistent design principles.", ["SRC-NIST-SP800-53-R5@SA-8", "SRC-ISO-27001-2022@A.8.27", "SRC-CSA-CCM-V4@AIS-04"], imp="low")
# a8 (3)
Q(a8, "Fail closed", "If a security-relevant service (authorization, sanctions screening, hold registry) is unavailable, do dependent operations stop or continue?",
  "Fail-open behavior during outages.", [B("CNV-ARC-003"), "SRC-MITRE-CWE@CWE-636!"], imp="high", ind=FIN)
Q(a8, "Blast radius", "If one component or one tenant's environment is compromised, what limits the impact on other components and tenants?",
  "Single compromise cascades across the platform.", ["SRC-NIST-SP800-207", B("CNV-ARC-001")], imp="high")
Q(a8, "Secure defaults", "Are new tenants, features and integrations secure by default, or must customers enable security settings?",
  "Insecure defaults left unchanged.", ["SRC-CISA-SECURE-BY-DESIGN", SSDF("PW.9")], imp="medium")

RECORDS = c.records()
