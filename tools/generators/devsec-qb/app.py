from devseclib import *

c = Cat("APP")
V1 = "SRC-OWASP-ASVS@5.0 V1 Encoding and Sanitization"
V2 = "SRC-OWASP-ASVS@5.0 V2 Validation and Business Logic"
V3 = "SRC-OWASP-ASVS@5.0 V3 Web Frontend Security"
V5 = "SRC-OWASP-ASVS@5.0 V5 File Handling"
V7 = "SRC-OWASP-ASVS@5.0 V7 Session Management"
V15 = "SRC-OWASP-ASVS@5.0 V15 Secure Coding and Architecture"
V16 = "SRC-OWASP-ASVS@5.0 V16 Security Logging and Error Handling"
CWE = lambda n: f"SRC-MITRE-CWE@CWE-{n}!"
FIN = ["financial-services", "banking", "wealth-management", "donor-advised-funds"]

# ---------------- evidence requirements ----------------
c.E("sqlscan", "Dynamic SQL and database bypass scan result per commit",
    "Result of a semantic check over every application and infrastructure project that finds string-built SQL, raw ADO.NET/Npgsql command text, "
    "dynamic EXECUTE in database functions and any database access path that does not use the approved interface, with the analyzer version and rule set.",
    mechanism="event-driven-automated", freshness="per-event", fmt="SARIF 2.1.0 plus a summary JSON",
    prov=["repository", "commit", "analyzer name and version", "rule set version", "scope and exclusions", "run timestamp"],
    signing="Build-provenance attestation over the result file (proposed)", retention="Life of the release plus audit period (to be set)")
c.E("injtest", "Negative injection test suite results",
    "Executed negative test cases (SQL, command, template, header, log and LDAP injection payloads) against each externally reachable input, "
    "with pass/fail per case and mapping to CWE identifiers.",
    mechanism="event-driven-automated", fmt="JUnit XML or TRX plus CWE mapping table",
    prov=["commit", "test suite version", "environment", "case-to-CWE mapping"])
c.E("xsscheck", "Rendering-sink and script inventory check",
    "Automated inspection of source, generated bundles and WebAssembly interop for unsafe HTML sinks (innerHTML, document.write, raw HTML "
    "rendering helpers), application-authored script outside Limen and third-party script references, plus the deployed Content Security Policy.",
    mechanism="event-driven-automated", fmt="JSON report plus captured CSP header",
    prov=["commit", "bundle digest", "checker version", "CSP value", "third-party script list"])
c.E("dast", "Authenticated dynamic scan of pre-production build",
    "Dynamic application security test of a pre-production deployment, authenticated as each role, covering XSS, CSRF, SSRF, header and session findings, with tool version and coverage of routes exercised.",
    mechanism="event-driven-automated", freshness="per-event", fmt="Scanner report (for example ZAP JSON) plus route coverage",
    prov=["deployment identifier", "build digest", "tool and rule versions", "authenticated roles", "routes covered"])
c.E("csrfcfg", "Cookie, CSRF and cross-origin configuration snapshot",
    "Captured response headers and cookie attributes (SameSite, Secure, HttpOnly, host prefix), anti-forgery validation configuration, CORS policy and frame-ancestors policy for each deployed origin.",
    mechanism="periodic-automated", freshness="P1D", fmt="JSON snapshot",
    prov=["origin", "deployment identifier", "capture timestamp"])
c.E("egress", "Outbound request allowlist and SSRF test results",
    "The approved outbound destination list for server-initiated requests, the egress enforcement configuration, and results of SSRF test cases (internal addresses, metadata endpoints, redirects, DNS rebinding, alternate IP encodings).",
    mechanism="event-driven-automated", fmt="JSON allowlist plus test results",
    prov=["commit", "environment", "allowlist version", "test suite version"])
c.E("deser", "Deserializer configuration and schema inventory",
    "Inventory of every deserialization entry point with its schema, type-binding mode, maximum size and depth, and a check that no polymorphic or type-name-driven deserialization and no BinaryFormatter-family serializer is reachable.",
    mechanism="event-driven-automated", fmt="JSON inventory plus analyzer output",
    prov=["commit", "entry point", "schema reference", "limit values", "analyzer version"])
c.E("upload", "File intake pipeline test and malware scan records",
    "Per-upload records showing type validation, size limits, storage location outside the web root, malware scan verdict and engine version, and periodic test results using known-bad samples (polyglots, oversized archives, path traversal names, formula payloads).",
    mechanism="event-driven-automated", fmt="Event log entries plus test report",
    prov=["upload identifier", "tenant", "scan engine and signature version", "verdict", "timestamp"])
c.E("logic", "Workflow invariant property and negative test results",
    "Property-based and negative test results for state machines and financial invariants (illegal transitions, double submission, concurrent approval, client-supplied computed values, mass assignment), with seeds and generators recorded.",
    mechanism="event-driven-automated", fmt="Test runner output plus invariant catalog",
    prov=["commit", "invariant identifiers", "generator seed", "case count", "result"])
c.E("session", "Session management configuration and test results",
    "Session lifetime, idle timeout, rotation on privilege change, revocation latency and concurrent session policy as configured, plus automated tests demonstrating fixation resistance, logout invalidation and revocation.",
    mechanism="event-driven-automated", fmt="Configuration export plus test results",
    prov=["commit", "identity provider configuration version", "test suite version"])
c.E("errors", "Error response and log content inspection",
    "Automated tests asserting that error responses use stable machine-readable codes without stack traces, internal identifiers or data from other tenants, and a periodic scan of log samples for secrets and restricted data.",
    mechanism="periodic-automated", freshness="P7D", fmt="Test results plus log-scan summary",
    prov=["commit", "log sample window", "scanner rules version"])
c.E("limits", "Input limit and resource exhaustion test results",
    "Tests for request size, collection length, nesting depth, regular expression timeouts and pagination caps on each entry point, with the configured limits.",
    mechanism="event-driven-automated", fmt="Test results plus limits table", prov=["commit", "entry point", "limit", "result"])
c.E("asvsmatrix", "ASVS verification matrix per release",
    "A per-release matrix listing each applicable ASVS requirement, the target level, the verification method (structural, automated test, manual review, external test), result and evidence link, distinguishing first-party from independent verification.",
    mechanism="event-driven-automated", freshness="per-event", fmt="CSV or JSON matrix plus Folio-rendered report",
    prov=["release", "ASVS version", "verifier identity", "independence"], disclosure="nda")
c.E("pentest", "Independent application penetration test report",
    "Report from an independent third-party application penetration test covering the production-equivalent release, with scope, methodology, findings, retest results and tester qualifications.",
    producer="External testing firm (not yet engaged)", mechanism="external-attestation", freshness="P1Y",
    fmt="PDF report plus findings register", independence="independent-third-party", disclosure="nda")

# ---------------- controls ----------------
c.C("db", "Approved database interface only; no dynamically constructed SQL",
    "Make string-constructed SQL unavailable to application code and detect any database access path that bypasses the approved typed, parameterized interface, including infrastructure code, migrations and database functions.",
    "preventive-structural", "L3-restricted-interface", ["Unbound application (not built)", "Strata (schema governance only; runtime query interface not found)", "F# semantic analyzer (not built)"],
    ["sqlscan", "injtest"], policies=["SEC-DB-001"], related=["UNB-CTRL-068"], cwe=["CWE-89", "CWE-564"],
    refs=["SRC-ECH-SCS-0.1@SEC-DB-001!", V1, CWE(89)],
    residual=["Strata as verified provides declarative schema management, not a runtime query interface, so the enforcing component does not yet exist.",
              "Database functions using dynamic EXECUTE, migrations and administrative scripts can reintroduce injection outside the application interface.",
              "Second-order injection through stored values consumed by reporting or export tools."])
c.C("dbgate", "Release gate on database bypass findings",
    "Block merge and release when the dynamic-SQL or bypass scan reports a finding or cannot run, unless a time-limited approved exception exists.",
    "preventive-gate", "L5-build-release-gate", ["Praxis CI workflow (exists for tool repositories; not configured for a product)"], ["sqlscan"],
    policies=["SEC-DB-001"], cwe=["CWE-89"], refs=["SRC-NIST-SP800-218@PW.7", "SRC-ECH-SCS-0.1!"])
c.C("exec", "No dynamic evaluation, code loading or shell construction",
    "Remove interpreter, reflection-emit, dynamic assembly loading, template evaluation of untrusted input and shell invocation from application code; route unavoidable process execution through fixed argument vectors in reviewed infrastructure.",
    "preventive-structural", "L6-automated-analysis", ["F# semantic analyzer (not built)", "Unbound application (not built)"], ["injtest"],
    policies=["SEC-EXEC-001"], cwe=["CWE-78", "CWE-94", "CWE-95", "CWE-1336", "CWE-470", "CWE-90", "CWE-643", "CWE-117", "CWE-113"],
    refs=["SRC-ECH-SCS-0.1@SEC-EXEC-001!", V1, CWE(78)],
    residual=["Build scripts, CI workflows and developer tooling are outside application scope and still execute shells.",
              "Third-party libraries may evaluate expressions internally."])
c.C("xss", "No user HTML, contextual encoding and no unsafe sinks",
    "Accept only plain text or validated structured input, render through components that encode by context, and prohibit unsafe rendering sinks in source and generated bundles.",
    "preventive-structural", "L3-restricted-interface", ["Limen (exists; kernel binds data through declared attributes)", "Forma (exists; CSS design system)", "Unbound application (not built)"],
    ["xsscheck", "dast"], policies=["SEC-UI-001", "SEC-UI-002"], cwe=["CWE-79", "CWE-116", "CWE-80"],
    refs=["SRC-ECH-SCS-0.1@SEC-UI-001!", V3, V1, CWE(79)],
    residual=["The Standard itself states that refusing HTML input alone does not eliminate XSS; URL, attribute and DOM contexts remain.",
              "Limen's browser kernel is TypeScript, so script exists inside the boundary and must itself be free of unsafe sinks.",
              "Folio-generated HTML documents and email templates are separate rendering paths."])
c.C("csp", "Restrictive Content Security Policy and script inventory",
    "Deploy a nonce- or hash-based CSP without unsafe-inline or unsafe-eval (WebAssembly evaluation permitted only as narrowly as the runtime needs), frame-ancestors restrictions and an inventory of every third-party script.",
    "preventive-structural", "L9-runtime-monitored", ["Hosting edge configuration (not chosen)", "Limen"], ["xsscheck", "csrfcfg"],
    policies=["SEC-UI-002"], cwe=["CWE-79", "CWE-1021", "CWE-829"], refs=[V3, "SRC-PCI-DSS-4.0.1@Req 6.4.3^"],
    residual=["Blazor or .NET WebAssembly runtimes may require wasm-unsafe-eval; the exact directive set is not yet tested."])
c.C("csrf", "Cross-site request forgery and cross-origin protection",
    "Require anti-forgery tokens or equivalent origin verification on every state-changing browser request, SameSite cookies, a restrictive CORS allowlist and framing denial.",
    "preventive-structural", "L3-restricted-interface", ["Unbound application (not built)", "Limen kernel fetch binding"], ["csrfcfg", "dast"],
    cwe=["CWE-352", "CWE-1021", "CWE-942"], refs=[V3, CWE(352)])
c.C("ssrf", "Server-side request destination control",
    "Allow server-initiated outbound requests only to an approved destination list enforced at the network egress layer and in the HTTP client, blocking private, link-local and metadata ranges and re-validating after redirects.",
    "preventive-structural", "L3-restricted-interface", ["Network egress proxy (not chosen)", "Unbound outbound HTTP client wrapper (not built)"], ["egress"],
    cwe=["CWE-918"], refs=["SRC-OWASP-API-TOP10-2023@API7:2023", CWE(918), V15])
c.C("deser", "Schema-bound deserialization with limits",
    "Deserialize external data only into explicit schemas and validated domain types, with size, depth and count limits, no type-name-driven polymorphism and no BinaryFormatter-family serializers.",
    "preventive-structural", "L2-type-system", ["F# domain types (not built)", "System.Text.Json source-generated contracts (proposed)"], ["deser"],
    policies=["SEC-DATA-001"], cwe=["CWE-502", "CWE-611", "CWE-776", "CWE-20"], refs=["SRC-ECH-SCS-0.1@SEC-DATA-001!", V2, CWE(502)])
c.C("upload", "Isolated file intake pipeline",
    "Accept uploads only for declared document types, verify content signatures and size, store outside any served path under generated names, scan for malware before release to users or agents, and neutralize formula content in exports.",
    "preventive-structural", "L3-restricted-interface", ["Unbound document intake service (not built)", "Malware scanning engine (not chosen)"], ["upload"],
    cwe=["CWE-434", "CWE-22", "CWE-409", "CWE-1236"], refs=[V5, CWE(434)])
c.C("logic", "Explicit state machines and server-side recomputation",
    "Represent workflow states explicitly, permit only legal transitions inside the command transaction, recompute every authorization, fee, eligibility and amount on the server, and bind updates to explicit allowed fields.",
    "preventive-structural", "L2-type-system", ["Unbound domain model (not built)", "Ordo state-directed engineering method (exists as a method)"], ["logic"],
    policies=["SEC-LANG-002"], requirements=None if False else None, related=["UNB-CTRL-026"], cwe=["CWE-840", "CWE-841", "CWE-362", "CWE-915", "CWE-602"],
    refs=[V2, "SRC-ECH-UNB-BASELINE@CNV-PLT-010!"],
    residual=["Business rules can be legal state transitions that are still wrong; types do not prove the policy is correct.",
              "Concurrency anomalies under PostgreSQL isolation levels require targeted tests."])
c.C("logicprop", "Property-based and adversarial testing of financial invariants",
    "Exercise invariants (balanced journals, idempotent disbursement, separation of duties, legal transitions) with generated and adversarial sequences including concurrency and replay.",
    "detective-automated", "L7-property-tested", ["Unbound test suite (not built)"], ["logic"], cwe=["CWE-362", "CWE-840"],
    refs=["SRC-ECH-SCS-0.1!", "SRC-NIST-IR-8397"])
c.C("session", "Server-controlled session lifecycle",
    "Issue sessions server-side with rotation at authentication and privilege change, idle and absolute timeouts, immediate revocation on logout or administrative action, and no long-lived bearer tokens in script-readable storage.",
    "preventive-structural", "L3-restricted-interface", ["Identity provider (not chosen)", "Unbound application (not built)"], ["session", "csrfcfg"],
    cwe=["CWE-384", "CWE-613", "CWE-614", "CWE-1004", "CWE-922"], refs=[V7, CWE(384)])
c.C("errors", "Fail-closed error handling with redacted responses",
    "Map every failure to an explicit result with a stable error code, return no internal detail to callers, redact secrets and restricted data before logging, and deny on unknown states.",
    "preventive-structural", "L2-type-system", ["Aegis (exists; .NET fault capture, recovery and redaction library)", "Unbound application (not built)"], ["errors"],
    policies=["SEC-LANG-002"], cwe=["CWE-209", "CWE-532", "CWE-755", "CWE-636"], refs=[V16, CWE(209)])
c.C("limits", "Bounded input and resource consumption",
    "Enforce limits on request size, collection length, nesting depth, string length, regular expression execution time and page size at every trust boundary.",
    "preventive-structural", "L3-restricted-interface", ["Unbound application (not built)"], ["limits"],
    policies=["SEC-DATA-001"], cwe=["CWE-400", "CWE-770", "CWE-1333", "CWE-20"], refs=[V2, "SRC-OWASP-API-TOP10-2023@API4:2023"])
c.C("asvs", "Release-level ASVS verification matrix",
    "Verify each release against a declared ASVS level, recording method, result and independence for each requirement so structural, automated and external evidence are not conflated.",
    "detective-automated", "L6-automated-analysis", ["Tutela (exists; security evidence and release posture discipline)", "Folio (exists; report rendering)"], ["asvsmatrix"],
    refs=["SRC-OWASP-ASVS", "SRC-ECH-SCS-0.1@Assurance deliverables!"], owner=SEC)
c.C("pentest", "Independent application penetration testing",
    "Commission independent testing of the production-equivalent application before launch and at least annually or on major change, supplying threat models without restricting tester discovery.",
    "detective-manual", "L10-external-or-manual", ["External testing firm (not engaged)"], ["pentest"],
    refs=["SRC-NIST-SP800-115", "SRC-ECH-SCS-0.1@External assurance and economics!"], owner=SEC)

# ---------------- answer units ----------------
a1 = c.A("SQL and database injection prevention",
    "Customers need assurance that donor, grant and ledger data cannot be read or altered through injected database commands.",
    "All Unbound database access goes through one restricted, typed interface that only accepts bound parameters and fixed, reviewed query definitions; no application code can build SQL from strings. A semantic check on every commit finds raw command text, dynamic EXECUTE in database functions and any bypass of the approved interface, and blocks release on findings or on failure to run. Negative injection tests cover every input. Elimination of SQL injection is claimed only for the scanned scope, with the scan result and its exclusions published to customers under NDA.",
    ["db", "dbgate"], ["sqlscan", "injtest"],
    current="No Unbound code exists. The Secure Construction Standard v0.1 (proposed) states SEC-DB-001. Strata exists as a pilot declarative PostgreSQL schema tool (strata@c6a384ec) but no runtime typed query interface was found, so the enforcing mechanism named by SEC-DB-001 does not yet exist.",
    policies=["SEC-DB-001"], requirements=["UNB-PLAT-007", "CNV-ARC-004"], mechanism="event-driven-automated", impl="high", rec="low",
    residual=["Enforcing component does not exist; SEC-DB-001 currently names a capability Strata does not provide.",
              "Dynamic SQL in PostgreSQL functions, migrations and operational scripts."],
    oq=["Which component will provide the runtime typed query interface: a Strata extension, an Unbound-owned ledger component (CNV-ARC-004) or a third-party library?"],
    challenge=ch(
        customer_intent="Know that injection cannot be used to read or tamper with financial and donor records.",
        adverse_outcome="Cross-tenant data disclosure or ledger tampering through injected SQL.",
        conventional_control_effectiveness="Secure coding guidance plus SAST and penetration testing finds many but not all injection paths; regressions recur.",
        legally_required="No statute requires a specific technique; GLBA and state safeguards rules require reasonable safeguards for customer information held by financial institutions and their service providers.",
        contractually_required="Commonly asked in bank and enterprise questionnaires; usually satisfied by attestation plus pen test results.",
        historical_convention="Parameterized queries, ORM usage, SAST and annual pen test.",
        architectural_elimination="Possible within a defined scope if string-built SQL is unavailable to application code and every path to the database is enumerated; trusted infrastructure, stored procedures and migrations must be in scope or listed as exclusions.",
        automatic_enforcement="Semantic analysis over compiled F# and SQL source, fail-closed release gate.",
        continuous_evidence="Per-commit scan result with analyzer version and scope, signed and retained.",
        stronger_alternative="Restricted interface plus per-commit bypass scan plus negative tests, with elimination scoped to the scanned code.",
        alternative_verifiable="Yes, if the scanner is validated against seeded bypass fixtures and an independent tester attempts injection without restriction.",
        customer_acceptance_likelihood="Engineering reviewers likely accept; procurement and auditors will still ask for an independent pen test result.",
        invalidating_conditions="Any raw ADO.NET or Npgsql use, dynamic EXECUTE in a database function, an unscanned project, or a reporting tool with direct database credentials.",
        conventional_cost="SAST license or tuning plus pen test fees.",
        alternative_cost="Building the restricted interface and analyzer; ongoing rule maintenance.",
        alternative_risks="Overconfidence: an elimination claim that silently excludes infrastructure code.",
        supporting_arguments=["Making the unsafe operation unavailable is stronger than finding it after the fact.", "Evidence is produced on every change rather than annually."],
        opposing_arguments=["The enforcing component does not exist yet.", "Assessors will not accept first-party elimination claims without independent reproduction.", "Database-side code is easy to forget."],
        technical_effectiveness="stronger", institutional_acceptance="uncertain"))
a2 = c.A("Command, code and interpreter injection prevention",
    "Customers need assurance that no input can cause the platform to run attacker-chosen commands or code.",
    "Unbound application code has no access to shell execution, dynamic code evaluation, runtime assembly loading or template evaluation of untrusted input; these capabilities are absent from the application dependency graph and detected by a semantic check if introduced. Log, header and directory-query outputs are built through encoding APIs. Any infrastructure exception uses fixed argument vectors, is reviewed and time-limited, and is listed in the release evidence.",
    ["exec"], ["injtest"], policies=["SEC-EXEC-001"], mechanism="event-driven-automated", impl="medium", rec="low",
    current="Not established. SEC-EXEC-001 exists only as a proposed rule; no analyzer that enforces it was located.")
a3 = c.A("Cross-site scripting prevention and output encoding",
    "Customers need assurance that donors, advisors and sponsor staff cannot have their sessions hijacked or screens altered through injected script.",
    "Unbound never accepts user-supplied HTML (SEC-UI-001); free text is stored as text and rendered through encoding components. Application-authored browser script exists only inside Limen's kernel (SEC-UI-002), and application logic runs in F# compiled to WebAssembly that cannot touch the DOM directly. Source, generated bundles and interop glue are checked on every build for unsafe sinks and unapproved scripts, a nonce- or hash-based CSP blocks inline and injected script, and DAST tests URL, attribute and DOM contexts. Echelon states the scope and residual risks rather than claiming XSS is eliminated.",
    ["xss", "csp"], ["xsscheck", "dast"], policies=["SEC-UI-001", "SEC-UI-002"], requirements=["UNB-PLAT-006"],
    current="No Unbound UI exists. Limen exists (limen@743cdb9b) and separates browser kernel from application engine; its kernel and protocol are TypeScript and its F# WebAssembly consumers are demonstration sites. No CSP, DAST or sink checking for an Echelon product was located.",
    mechanism="event-driven-automated", impl="medium", rec="low",
    residual=["Limen kernel script, Folio HTML output and email templates are rendering paths that need their own checks.", "Third-party scripts such as analytics or support widgets would breach the model if added."],
    challenge=ch(
        customer_intent="Prevent account takeover and fraudulent grant recommendations through script injection.",
        adverse_outcome="Session theft or forged actions in a donor or sponsor session.",
        conventional_control_effectiveness="Framework auto-encoding plus scanning is reasonably effective but DOM-based XSS and unsafe helper use are frequently missed.",
        legally_required="No.", contractually_required="Commonly asked; usually answered with pen test results.",
        historical_convention="Output encoding guidance, SAST, DAST, annual pen test.",
        architectural_elimination="Partial. Refusing HTML input and confining script to a small kernel removes most sinks, but the Standard itself says this alone does not eliminate XSS; URL, attribute and DOM contexts and the kernel's own code remain.",
        automatic_enforcement="Build-time sink and script inventory checks over generated bundles, CSP as a runtime backstop.",
        continuous_evidence="Per-build check result with bundle digest and deployed CSP capture.",
        stronger_alternative="Small, audited kernel plus CSP plus per-build bundle inspection.",
        alternative_verifiable="Yes for the inspected bundle; requires independent testing for the kernel and context handling.",
        customer_acceptance_likelihood="Likely as defense in depth; unlikely as a replacement for independent testing.",
        invalidating_conditions="Any added third-party script, an unsafe sink in Limen, a CSP relaxation, or a Folio template rendering untrusted strings unencoded.",
        conventional_cost="Scanner licenses and pen test fees.", alternative_cost="Checker development and Limen maintenance.",
        alternative_risks="Limen becomes a single high-value component; a defect there affects every application.",
        supporting_arguments=["Very small script surface.", "WebAssembly application code cannot call DOM APIs directly."],
        opposing_arguments=["Kernel is TypeScript; script still exists.", "WebAssembly runtimes may need CSP relaxations.", "No independent test of Limen exists."],
        technical_effectiveness="stronger", institutional_acceptance="uncertain"))
a4 = c.A("Cross-site request forgery and cross-origin protections",
    "Customers need assurance that an authenticated user's browser cannot be tricked into submitting grants, changes or approvals.",
    "Every state-changing browser request carries an anti-forgery token or verified origin, session cookies are SameSite and host-prefixed, CORS admits only listed Echelon origins without credentials for others, framing is denied, and high-risk actions (new payee, grant above threshold, authority change) require explicit step-up confirmation. Configuration is captured daily and tested on every release.",
    ["csrf", "csp"], ["csrfcfg", "dast"], mechanism="periodic-automated", freshness="P1D", impl="low", rec="low")
a5 = c.A("Server-side request forgery and outbound request control",
    "Customers need assurance that the platform cannot be used to reach internal systems, cloud metadata or partner endpoints on an attacker's behalf.",
    "Server-initiated requests (webhook delivery, charity data lookups, document fetches, AI tool calls) go through one outbound client and an egress proxy that permit only approved destinations, block private and metadata ranges, re-check every redirect and resolved address, and log every call. SSRF test cases run on every release.",
    ["ssrf"], ["egress"], mechanism="event-driven-automated", impl="medium", rec="low",
    oq=["Which hosting platform and egress control will be used? None is chosen."])
a6 = c.A("Safe deserialization and structured input parsing",
    "Customers need assurance that crafted files, messages or API payloads cannot execute code or exhaust the service.",
    "External data is parsed only into explicit schemas and validated F# domain types with size, depth and count limits; type-name-driven polymorphism, BinaryFormatter-family serializers and DTD processing are absent. Every entry point is inventoried with its schema and limits and checked on each build.",
    ["deser", "limits"], ["deser", "limits"], policies=["SEC-DATA-001"], mechanism="event-driven-automated", impl="low", rec="low")
a7 = c.A("File upload, document intake and export safety",
    "Customers need assurance that uploaded charity documents, contribution records and imports cannot deliver malware or attacks, and exports cannot attack recipients.",
    "Uploads are accepted only for declared types and sizes, verified by content, stored outside served paths under generated names, malware-scanned before any person or AI agent can open them, and parsed in an isolated worker. CSV and spreadsheet exports neutralize formula content. Each upload produces an event with scan verdict and engine version.",
    ["upload", "deser"], ["upload"], mechanism="event-driven-automated", impl="medium", rec="medium", products=["unbound"])
a8 = c.A("Business logic and workflow integrity",
    "Sponsors need assurance that grants, payments and fee changes follow the approved workflow and cannot be skipped, replayed, raced or manipulated by altering client data.",
    "Workflow states are explicit types with only legal transitions representable; every authorization, eligibility, fee and amount is recomputed on the server inside the command transaction (CNV-PLT-010); updates bind only to declared fields; and financial invariants are tested with property-based, concurrency and replay tests on every change. Business-logic weaknesses are treated as a verification problem, not a scanning problem.",
    ["logic", "logicprop"], ["logic"], policies=["SEC-LANG-002"], requirements=["CNV-PLT-010", "UNB-API-004", "UNB-IMM-006"],
    mechanism="event-driven-automated", impl="high", rec="medium", products=["unbound"],
    challenge=ch(
        customer_intent="Ensure no one can move money or approve grants outside the sponsor's policy.",
        adverse_outcome="Unauthorized or duplicated disbursement, skipped approval, manipulated fee.",
        conventional_control_effectiveness="Scanners rarely find business-logic flaws; pen tests find some within limited time.",
        legally_required="Sponsors bear IRC 4966/4967 exposure for improper distributions; the platform's control is how they meet it, not a statute on Echelon.",
        contractually_required="Expected by sponsors and their auditors.",
        historical_convention="Manual test cases, UAT and pen testing.",
        architectural_elimination="Illegal transitions can be made unrepresentable in types; wrong but legal policy cannot.",
        automatic_enforcement="Type system, transaction-bound server recomputation, property tests in CI.",
        continuous_evidence="Invariant test results per commit with generator seeds.",
        stronger_alternative="Explicit state machines plus generated adversarial sequences.",
        alternative_verifiable="Yes, tests are reproducible from seeds.",
        customer_acceptance_likelihood="Likely if presented with reproducible results; auditors will still sample transactions.",
        invalidating_conditions="Any path that writes authoritative state outside the command handler, or client-computed values accepted by an API.",
        conventional_cost="Manual QA and pen test time.", alternative_cost="Property test design and maintenance.",
        alternative_risks="Generators that miss realistic sequences give false confidence.",
        supporting_arguments=["Covers a class scanners cannot see.", "Directly tied to sponsor financial risk."],
        opposing_arguments=["No implementation exists to test.", "Property tests only check the properties someone thought to write."],
        technical_effectiveness="stronger", institutional_acceptance="likely"))
a9 = c.A("Session management",
    "Customers need assurance that sessions cannot be stolen, fixed or kept alive after a user leaves or is removed.",
    "Sessions are server-controlled, rotated at sign-in and privilege change, bound to secure host-prefixed HttpOnly SameSite cookies, expire on idle and absolute timeouts appropriate to the role, and are revoked immediately on logout, deprovisioning or administrative action. No bearer token is placed in script-readable browser storage. Tests prove fixation resistance and revocation latency.",
    ["session", "csrf"], ["session", "csrfcfg"], mechanism="event-driven-automated", impl="medium", rec="low",
    oq=["Limen's kernel exposes localStorage bindings; does Unbound need a rule that no credential or session material passes through them?"])
a10 = c.A("Error handling and information exposure",
    "Customers need assurance that failures do not leak internal details or other customers' data and do not fail open.",
    "Failures are explicit result values with stable machine-readable codes; responses never contain stack traces, SQL, internal hostnames or other tenants' identifiers; logs are redacted before write; unknown or failed states deny the action. Aegis provides fault capture and redaction primitives for .NET; tests assert response content and periodic log scans look for secrets and restricted data.",
    ["errors"], ["errors"], policies=["SEC-LANG-002"], requirements=["SOC2-003"], mechanism="periodic-automated", freshness="P7D", impl="low", rec="low",
    current="No Unbound code exists. Aegis (aegis@711e0260) exists as an operational fault handling library with redaction; it has not been applied to an Echelon production service.")
a11 = c.A("Input validation, validated domain types and resource limits",
    "Customers need assurance that malformed or oversized input cannot corrupt records or degrade service.",
    "Every external input is parsed at the trust boundary into validated domain types with private constructors, so unvalidated values cannot reach business logic; size, count, depth and regular-expression time limits apply at every entry point; violations produce explicit errors and are logged without echoing payloads.",
    ["deser", "limits"], ["limits", "deser"], policies=["SEC-DATA-001", "SEC-LANG-002"], mechanism="event-driven-automated", impl="low", rec="low")
a12 = c.A("Application security verification standard and testing evidence",
    "Customers need a verifiable statement of what application security testing has been performed, to what standard, and by whom.",
    "Each production release is verified against OWASP ASVS Level 2 (Level 3 for payment, authority and ledger functions), with a per-requirement matrix showing whether the property is structurally enforced, automatically tested, manually reviewed or independently tested. An independent application penetration test is performed before launch and annually, and results with retest evidence are shared under NDA. First-party reports are labeled as such.",
    ["asvs", "pentest"], ["asvsmatrix", "pentest"], mechanism="event-driven-automated", impl="medium", rec="medium", owner=SEC,
    current="No application security verification of an Echelon product has been performed. No penetration test exists. The Standard plans an external pen test for Unbound.",
    statement="No application security testing of an Echelon production service has been performed yet. Echelon plans ASVS-based verification per release and an independent penetration test of Unbound before launch.",
    kind="not-available",
    challenge=ch(
        customer_intent="Obtain independent confidence that the application resists common attacks.",
        adverse_outcome="Undetected exploitable weaknesses in production.",
        conventional_control_effectiveness="Annual pen tests are time-boxed snapshots; quality varies with tester skill.",
        legally_required="Not by statute for Echelon; NYDFS 500.8 and FTC Safeguards 314.4(c)(4) require covered customers to evaluate externally developed applications, which drives the request.",
        contractually_required="Bank and insurer contracts commonly require an annual independent pen test summary.",
        historical_convention="Annual third-party pen test with executive summary letter.",
        architectural_elimination="Not applicable; verification is still needed.",
        automatic_enforcement="Per-release ASVS matrix generated from structural checks and automated tests.",
        continuous_evidence="Per-release matrix with method and independence labels.",
        stronger_alternative="Continuous first-party verification plus a focused independent test supplied with threat models and the matrix.",
        alternative_verifiable="First-party evidence is reproducible but not independent.",
        customer_acceptance_likelihood="Independent test still expected; continuous matrix is an addition, not a substitute.",
        invalidating_conditions="If structural claims are not independently reproduced, they should not reduce pen test scope.",
        conventional_cost="Independent test fees per year.", alternative_cost="Matrix generation and maintenance.",
        alternative_risks="Customers may misread first-party evidence as independent assurance.",
        supporting_arguments=["Evidence per release rather than per year."],
        opposing_arguments=["Institutions require independence; internal evidence cannot replace it (Standard, External assurance section)."],
        technical_effectiveness="stronger", institutional_acceptance="unlikely"))

# ---------------- questions ----------------
Q = c.Q
# a1 SQL injection (5)
Q(a1, "SQL injection", "How does the application prevent SQL injection across all database access paths, including reporting, administrative and batch components?",
  "Injected SQL reads or alters donor, grant or ledger data.", [V1, CWE(89), "SRC-MITRE-CWE-TOP25", "SRC-CSA-CCM-V4@AIS-04"], imp="critical",
  alt=["Do you use parameterized queries or prepared statements for all database interactions?", "Describe your controls against injection flaws in custom code."])
Q(a1, "SQL injection", "Is any SQL constructed by string concatenation or interpolation anywhere in the codebase, including database functions using dynamic EXECUTE, migrations and operational scripts, and how would you know?",
  "Dynamic SQL hidden in database-side code or tooling bypasses application-level parameterization.", ["SRC-ECH-SCS-0.1@SEC-DB-001!", CWE(89), V1], cls="echelon-internal", imp="high",
  note="Probes the Standard's note that parameterization must also cover trusted database internals.")
Q(a1, "SQL injection", "Your standard says all database access goes through Strata. Which component actually executes application queries today, how is a bypass (raw Npgsql, a second connection string, a reporting tool with direct credentials) detected, and what reproducible evidence scopes the elimination claim?",
  "An elimination claim that relies on a component that does not provide the stated capability, or that omits bypass paths.", ["SRC-ECH-SCS-0.1@SEC-DB-001!", "SRC-ECH-UNB-BASELINE@CNV-ARC-004!", CWE(89)],
  cls="echelon-internal", imp="high", oq=["Strata has no verified runtime query interface; confirm the enforcing component."])
Q(a1, "SQL injection", "How do you test for second-order injection, where data stored safely is later used unsafely in a query, report, search filter or export?",
  "Stored values become executable in a later context such as reporting or full-text search.", [CWE(89), "SRC-OWASP-WSTG", V1], imp="medium")
Q(a1, "SQL injection", "Does your secure development process require that bespoke software be protected against injection attacks, and can you show evidence of this for the release we will use?",
  "Vendor cannot evidence protection against injection in the version deployed to the customer.", ["SRC-PCI-DSS-4.0.1@Req 6.2.4", "SRC-ISO-27001-2022@A.8.28", "SRC-NIST-SP800-53-R5@SI-10"],
  cls="contractual-common", imp="high", ind=FIN, alt=["Provide evidence that common software attacks are addressed in your custom code."])
# a2 command/code injection (5)
Q(a2, "OS command injection", "Does any application component invoke an operating system shell or external process, and if so, how are arguments constructed and constrained?",
  "Attacker-controlled input executes commands on application hosts.", [CWE(78), V1, "SRC-ECH-SCS-0.1@SEC-EXEC-001!"], imp="high")
Q(a2, "Code injection", "Can any user, partner or AI agent input reach a dynamic evaluation facility such as expression evaluators, scripting engines, runtime compilation or dynamic assembly loading?",
  "Remote code execution through evaluation of untrusted input.", [CWE(94), "SRC-MITRE-CWE@CWE-95!", "SRC-ECH-SCS-0.1@SEC-EXEC-001!", V15], imp="critical")
Q(a2, "Template injection", "Are document, email or notification templates (including sponsor-customizable white-label templates) rendered with an engine that can evaluate expressions, and how is template injection prevented?",
  "Sponsor- or user-editable templates become a code execution or data exfiltration channel.", ["SRC-MITRE-CWE@CWE-1336!", V1], imp="medium",
  ind=["donor-advised-funds", "wealth-management", "financial-services"], prod=["unbound"])
Q(a2, "Log and header injection", "How do you prevent injection into logs, HTTP headers, directory queries and other interpreters (CRLF, LDAP, XPath) where user input is written?",
  "Forged log entries undermine audit evidence; header injection enables response splitting or cache poisoning.", ["SRC-MITRE-CWE@CWE-117!", "SRC-MITRE-CWE@CWE-113!", "SRC-MITRE-CWE@CWE-90!", V1, V16], imp="medium")
Q(a2, "Infrastructure exceptions", "What exceptions to the no-shell and no-dynamic-code rule exist in build tooling, deployment automation or operational scripts, who approved them, and when do they expire?",
  "Unreviewed infrastructure scripts reintroduce command injection outside application scanning scope.", ["SRC-ECH-SCS-0.1@Enforcement model!", "SRC-NIST-SP800-218@PO.4"], cls="echelon-internal", imp="medium")
# a3 XSS (6)
Q(a3, "Cross-site scripting", "How does the application prevent stored, reflected and DOM-based cross-site scripting?",
  "Injected script hijacks donor or sponsor sessions or alters displayed financial information.", [V3, V1, CWE(79), "SRC-MITRE-CWE-TOP25", "SRC-CSA-CCM-V4@AIS-04"], imp="critical",
  alt=["Describe output encoding and input sanitization practices for web interfaces.", "Is your application tested for XSS vulnerabilities?"])
Q(a3, "Output encoding", "Is output encoding applied according to context (HTML body, attribute, URL, JavaScript, CSS), and which component is responsible for each context?",
  "Correct encoding for one context fails in another, leaving injectable sinks.", [V1, "SRC-MITRE-CWE@CWE-116!", "SRC-OWASP-CHEATSHEETS"], imp="high")
Q(a3, "Rich text", "Your standard says the platform never accepts user-supplied HTML. How do grant purpose notes, donor messages and sponsor-authored content support formatting, and what prevents a future feature from adding an HTML or Markdown renderer?",
  "Feature pressure introduces rich text rendering that reopens the HTML injection class.", ["SRC-ECH-SCS-0.1@SEC-UI-001!", V1], cls="echelon-internal", imp="medium", prod=["unbound"])
Q(a3, "Content Security Policy", "Do you deploy a Content Security Policy, and does it permit unsafe-inline, unsafe-eval or broad source allowlists? If WebAssembly requires evaluation permissions, what exactly is allowed?",
  "A permissive CSP provides no backstop when an encoding defect occurs.", [V3, "SRC-OWASP-CHEATSHEETS"], imp="medium")
Q(a3, "Generated content", "Which channels other than the web UI render user-controlled text (PDF statements, acknowledgment letters, emails, CSV exports, partner embeds), and how is each protected against injection?",
  "Secondary rendering paths such as Folio documents or email templates bypass web UI protections.", [V1, "SRC-MITRE-CWE@CWE-1236!", "SRC-MITRE-CWE@CWE-79!"], imp="medium", prod=["unbound"])
Q(a3, "Embedded components", "When your interface is embedded in a partner or sponsor site, how is script isolation maintained and how do you prevent the host page or your component from injecting script into each other?",
  "White-label embedding creates cross-origin script exposure between partner and platform.", [V3, "SRC-MITRE-CWE@CWE-1021!", "SRC-ECH-SCS-0.1@SEC-UI-002!"], imp="high",
  ind=["donor-advised-funds", "wealth-management"], prod=["unbound"])
# a4 CSRF (4)
Q(a4, "CSRF", "How are state-changing requests protected against cross-site request forgery?",
  "A malicious site causes a logged-in user's browser to submit a grant or change.", [V3, CWE(352), "SRC-OWASP-CHEATSHEETS"], imp="high",
  alt=["Do you implement anti-CSRF tokens on all forms?"])
Q(a4, "Cookie attributes", "What SameSite, Secure, HttpOnly and prefix attributes are set on session and authentication cookies, and how is drift detected after deployment?",
  "Weak cookie attributes permit cross-site use or script access to session cookies.", [V7, V3, "SRC-MITRE-CWE@CWE-1004!", "SRC-MITRE-CWE@CWE-614!"], imp="medium")
Q(a4, "CORS", "What is your cross-origin resource sharing policy, does any endpoint reflect arbitrary origins or allow credentials from origins you do not control, and how is the allowlist governed for partner domains?",
  "A permissive CORS policy lets any site read authenticated responses.", [V3, "SRC-MITRE-CWE@CWE-942!", "SRC-OWASP-API-TOP10-2023@API8:2023"], imp="medium")
Q(a4, "Clickjacking", "How do you prevent the application from being framed by unauthorized sites to trick users into approving actions?",
  "UI redressing causes users to approve grants or authority changes unknowingly.", [V3, "SRC-MITRE-CWE@CWE-1021!"], imp="low")
# a5 SSRF (5)
Q(a5, "SSRF", "Which features cause the server to make requests to URLs or hosts influenced by users, partners or AI agents, and how are destinations restricted?",
  "Server-side request forgery reaches internal services or cloud metadata to obtain credentials.", [CWE(918), "SRC-MITRE-CWE-TOP25", V15, "SRC-OWASP-API-TOP10-2023@API7:2023"], imp="high")
Q(a5, "SSRF", "Is outbound network access from application workloads restricted at the network layer as well as in code, and are cloud instance metadata endpoints unreachable from application processes?",
  "Code-only URL validation is bypassed through redirects, DNS rebinding or alternate address encodings.", [CWE(918), "SRC-NIST-SP800-53-R5@SC-7", "SRC-CIS-CONTROLS-V8.1"], imp="high")
Q(a5, "SSRF", "How do you test SSRF defenses against redirects, DNS rebinding, IPv6 and decimal or octal IP encodings, and alternate URL schemes?",
  "Partial validation logic passes encoded internal addresses.", ["SRC-OWASP-WSTG", CWE(918)], imp="medium")
Q(a5, "AI tool calls", "Can an AI agent or assistant feature fetch arbitrary URLs or call arbitrary tools, and how are its outbound requests constrained and logged?",
  "Prompt injection directs an agent to fetch internal resources or exfiltrate data.", ["SRC-OWASP-LLM-TOP10-2025", "SRC-OWASP-AGENTIC-AI", CWE(918), "SRC-ECH-UNB-BASELINE@UNB-AGT-003!"], imp="high")
Q(a5, "Partner callbacks", "When sponsors or partners register callback or webhook URLs, how do you prevent those URLs from targeting your internal network or other tenants' endpoints?",
  "Registered callback URLs are used as an SSRF vector.", [CWE(918), "SRC-OWASP-API-TOP10-2023@API7:2023", "SRC-ECH-UNB-BASELINE@UNB-API-STD-005!"], imp="medium",
  ind=["donor-advised-funds", "financial-services"], prod=["unbound"])
# a6 deserialization (5)
Q(a6, "Deserialization", "Does the application deserialize data from untrusted sources, which serializers are used, and how is type binding restricted?",
  "Insecure deserialization leads to remote code execution or object injection.", [CWE(502), "SRC-MITRE-CWE-TOP25", V2, "SRC-ECH-SCS-0.1@SEC-DATA-001!"], imp="high")
Q(a6, "Deserialization", "Is BinaryFormatter, NetDataContractSerializer, or JSON type-name handling (polymorphic type resolution from payload) used anywhere, including in third-party libraries or caching layers?",
  "Known .NET gadget-chain serializers reachable through caches, queues or libraries.", [CWE(502), "SRC-ROSLYN-SECURITY", "SRC-FSHARP-ANALYZERS"], imp="high")
Q(a6, "XML processing", "If the platform parses XML (bank files, custodian statements, IRS data, SAML), how are external entities, DTDs and entity expansion disabled?",
  "XXE reads local files or causes denial of service through entity expansion.", ["SRC-MITRE-CWE@CWE-611!", "SRC-MITRE-CWE@CWE-776!", V1], imp="medium",
  ind=["donor-advised-funds", "financial-services", "banking"], prod=["unbound"])
Q(a6, "Structured input", "Do inbound files and messages from banks, custodians and partners pass schema validation with size and record limits before any processing, and what happens to a file that fails?",
  "Malformed partner files corrupt records or exhaust resources; partial processing creates inconsistent state.", [V2, "SRC-ECH-SCS-0.1@SEC-DATA-001!", "SRC-ECH-UNB-BASELINE@UNB-EVT-003!"], imp="high", prod=["unbound"])
Q(a6, "Message queues", "Are internal messages, cached objects and outbox events treated as untrusted when deserialized, or does the design rely on infrastructure being trusted?",
  "Compromise of an internal store pivots to code execution through trusted deserialization.", [CWE(502), "SRC-NIST-SP800-207"], imp="low")
# a7 upload (5)
Q(a7, "File upload", "What file types can users upload, how are type, size and content validated, and where are files stored relative to anything the web tier serves?",
  "Malicious uploads are executed, served to other users or overwrite application files.", [V5, "SRC-MITRE-CWE@CWE-434!", "SRC-MITRE-CWE-TOP25"], imp="high")
Q(a7, "Malware scanning", "Are uploaded documents (for example charity determination letters, contribution records, appraisals) scanned for malware before staff, donors or AI agents can open them, and what engine and update frequency are used?",
  "Staff or agents open weaponized documents.", [V5, "SRC-NIST-SP800-53-R5@SI-3"], imp="high", ind=["donor-advised-funds", "nonprofit"], prod=["unbound"])
Q(a7, "Path traversal", "How do you prevent path traversal or overwrite through file names, archive entries or export paths?",
  "Attacker-chosen file names write or read outside the intended location.", ["SRC-MITRE-CWE@CWE-22!", V5], imp="medium")
Q(a7, "Archive handling", "Do you accept compressed archives or multi-part imports, and how do you prevent decompression bombs and nested archive abuse?",
  "Decompression bombs exhaust storage or memory.", ["SRC-MITRE-CWE@CWE-409!", V5], imp="low")
Q(a7, "Export safety", "Are CSV and spreadsheet exports protected against formula injection when they contain donor-, charity- or partner-supplied text?",
  "Exported data executes formulas on a recipient's workstation.", ["SRC-MITRE-CWE@CWE-1236!", V1], imp="medium")
# a8 business logic (6)
Q(a8, "Business logic", "How do you identify and test business logic weaknesses (skipped steps, out-of-order actions, limit circumvention) that automated scanners cannot detect?",
  "Workflow abuse moves money or approves grants outside policy.", [V2, "SRC-MITRE-CWE@CWE-840!", "SRC-MITRE-CWE@CWE-841!", "SRC-OWASP-WSTG"], imp="critical",
  ind=FIN, prod=["unbound"])
Q(a8, "Race conditions", "How are concurrent requests handled for approvals, disbursements and balance-affecting operations so that double spending or double approval cannot occur?",
  "Race conditions allow duplicate disbursement or approval.", ["SRC-MITRE-CWE@CWE-362!", V2, "SRC-ECH-UNB-BASELINE@UNB-IMM-006!"], imp="critical", ind=FIN, prod=["unbound"])
Q(a8, "Client-trusted values", "Are any amounts, fees, eligibility results or authorization outcomes computed in the browser and accepted by the server?",
  "Manipulated client calculations change financial outcomes.", ["SRC-MITRE-CWE@CWE-602!", "SRC-ECH-UNB-BASELINE@CNV-PLT-010!", V2], imp="high", prod=["unbound"])
Q(a8, "Mass assignment", "How do you prevent requests from setting fields the caller should not control, such as status, approver, tenant or fee fields?",
  "Mass assignment escalates privilege or bypasses approval.", ["SRC-MITRE-CWE@CWE-915!", "SRC-OWASP-API-TOP10-2023@API3:2023", V2], imp="high")
Q(a8, "Explicit states", "Are workflow states represented explicitly so that illegal states and transitions cannot be constructed, and what evidence shows that every transition path is tested?",
  "Implicit state in flags and nullable fields permits illegal combinations.", ["SRC-ECH-SCS-0.1@SEC-LANG-002!", V2], cls="echelon-internal", imp="medium", prod=["unbound"])
Q(a8, "Abuse limits", "What limits prevent abuse of legitimate functions at scale, such as enumerating charities, repeatedly splitting grants to stay under approval thresholds, or creating many recipients?",
  "Threshold splitting and automated abuse defeat per-transaction controls.", [V2, "SRC-ECH-UNB-BASELINE@TVR-SEC-004!", "SRC-OWASP-API-TOP10-2023@API6:2023"], imp="high",
  ind=["donor-advised-funds", "wealth-management"], prod=["unbound"])
# a9 sessions (5)
Q(a9, "Session management", "What are the idle and absolute session timeouts for donors, advisors, sponsor staff and administrators, and how were they chosen?",
  "Unattended sessions are reused by others.", [V7, "SRC-MITRE-CWE@CWE-613!", "SRC-NIST-SP800-63-4"], imp="medium",
  alt=["Do sessions time out after a period of inactivity?"])
Q(a9, "Session fixation", "Is the session identifier regenerated at authentication and at privilege elevation, and how is this tested?",
  "Session fixation lets an attacker ride a victim's authenticated session.", [V7, "SRC-MITRE-CWE@CWE-384!"], imp="medium")
Q(a9, "Revocation", "When a user logs out, is deprovisioned or has a role removed, how quickly are all of their active sessions and tokens invalidated, including on other devices?",
  "Removed users retain access through existing sessions.", [V7, "SRC-NIST-SP800-53-R5@AC-12"], imp="high")
Q(a9, "Token storage", "Where are session or access tokens stored in the browser, and can any script read them?",
  "Tokens in script-readable storage are stolen by any script injection.", [V7, "SRC-MITRE-CWE@CWE-922!", V3], imp="medium")
Q(a9, "Concurrent sessions", "Are concurrent sessions limited or visible to users, and can users or administrators see and terminate active sessions?",
  "Account compromise goes unnoticed because parallel sessions are invisible.", [V7, "SRC-FFIEC-AUTH-GUIDANCE-2021"], imp="low", ind=FIN)
# a10 error handling (4)
Q(a10, "Error handling", "Do error messages returned to users or API callers ever include stack traces, query text, internal identifiers or configuration details?",
  "Verbose errors disclose internals that aid attack.", [V16, "SRC-MITRE-CWE@CWE-209!", "SRC-NIST-SP800-53-R5@SI-11"], imp="medium",
  alt=["How are application errors handled and displayed?"])
Q(a10, "Fail closed", "When an authorization service, policy engine or dependency fails or times out, does the application deny the action or allow it?",
  "Failures in security dependencies result in fail-open behavior.", [V16, "SRC-MITRE-CWE@CWE-636!", "SRC-ECH-SCS-0.1@SEC-LANG-002!"], imp="high")
Q(a10, "Sensitive data in logs", "When an exception occurs, what prevents request payloads, bank account numbers, donor details or secrets captured in the exception context from flowing into error reports, crash telemetry or third-party error tracking services?",
  "Logs become a secondary store of sensitive data with weaker controls.", [V16, "SRC-MITRE-CWE@CWE-532!", "SRC-ECH-UNB-SOC2-DIRECTIVE@SOC2-003!"], imp="high")
Q(a10, "Exception paths", "How do you test exceptional and failure paths (timeouts, partial failures, unexpected states) for security-relevant behavior rather than only success paths?",
  "Untested error paths leave inconsistent state or bypass checks.", ["SRC-MITRE-CWE@CWE-755!", "SRC-NIST-IR-8397", V16], imp="medium")
# a11 input validation (5)
Q(a11, "Input validation", "Is all input validated on the server at the trust boundary using allowlist rules, regardless of client-side validation?",
  "Reliance on client-side validation lets crafted requests bypass checks.", [V2, "SRC-MITRE-CWE@CWE-20!", "SRC-NIST-SP800-53-R5@SI-10", "SRC-CSA-CCM-V4@AIS-04"], imp="high",
  alt=["Describe your input validation approach."])
Q(a11, "Validated domain types", "Can unvalidated values (for example raw strings for EINs, routing numbers or amounts) reach business logic, or does the type system require validation at construction?",
  "Unvalidated values propagate and are trusted downstream.", ["SRC-ECH-SCS-0.1@SEC-LANG-002!", V2], cls="echelon-internal", imp="medium", prod=["unbound"])
Q(a11, "Regular expressions", "How do you prevent regular expression denial of service in validation logic?",
  "Catastrophic backtracking exhausts CPU.", ["SRC-MITRE-CWE@CWE-1333!", V2], imp="low")
Q(a11, "Resource limits", "What limits apply to request body size, array lengths, nesting depth, page size and query complexity, and how are they tested?",
  "Unbounded input exhausts memory or database capacity.", ["SRC-MITRE-CWE@CWE-770!", "SRC-OWASP-API-TOP10-2023@API4:2023", V2], imp="medium")
Q(a11, "Numeric integrity", "How are monetary amounts represented and validated to prevent rounding, overflow and precision errors in financial calculations?",
  "Arithmetic errors misstate balances, fees or grants.", ["SRC-MITRE-CWE@CWE-190!", "SRC-MITRE-CWE@CWE-681!", V2], imp="high", ind=FIN, prod=["unbound"],
  note="Memory safety does not prevent arithmetic errors; the Standard says so explicitly.")
# a12 verification (5)
Q(a12, "Verification standard", "Which application security verification standard and level do you test against, and can you provide the results for the current release?",
  "Customer cannot judge depth or coverage of application testing.", ["SRC-OWASP-ASVS", "SRC-CSA-CCM-V4@AIS-05", "SRC-EDUCAUSE-HECVAT"], imp="high",
  alt=["Do you follow OWASP guidelines for application development and testing?"])
Q(a12, "Independent testing", "Has an independent third party performed an application penetration test on the version we will use, and will you share the report or summary and remediation status?",
  "No independent verification of application resistance to attack.", ["SRC-NIST-SP800-115", "SRC-FFIEC-IS-BOOKLET", "SRC-AICPA-TSC@CC4.1"], cls="contractual-common", imp="critical",
  ind=FIN + ["insurance"])
Q(a12, "Regulated customer testing", "What security testing results can you provide so that we can meet our own obligation to evaluate the security of externally developed applications we use?",
  "Regulated customer cannot meet its own application security evaluation obligation.", ["SRC-NYDFS-PART-500@500.8", "SRC-FTC-SAFEGUARDS-RULE@314.4(c)(4)"],
  cls="legal-regulatory", imp="high", ind=["financial-services", "banking", "insurance", "wealth-management"], jur=["US-state:NY", "US-federal"],
  auth="NYDFS; FTC", note="The obligation falls on covered customers; it flows to Echelon through their vendor assessment.")
Q(a12, "Coverage by weakness class", "For each major weakness class (injection, XSS, access control, deserialization, SSRF), which verification method gives you confidence: structural prevention, automated testing, manual review or external testing?",
  "Coverage gaps are hidden by aggregate claims.", ["SRC-ECH-SCS-0.1@Assurance deliverables!", "SRC-MITRE-CWE-TOP25", "SRC-OWASP-TOP10"], cls="customer-preference", imp="medium")
Q(a12, "First-party reports", "If you provide internally produced security assessment reports, how are they distinguished from independent assessments, and who reviewed them?",
  "Customers mistake first-party evidence for independent assurance.", ["SRC-ECH-SCS-0.1@Assurance deliverables!", "SRC-AICPA-SSAE-18"], cls="customer-preference", imp="medium")

RECORDS = c.records()
