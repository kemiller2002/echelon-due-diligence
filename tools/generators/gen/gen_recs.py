import json, sys
OUT = sys.argv[1]
STD = "echelon-organization-administration@2763e576:policies/security/secure-construction-standard.md"
R = []
def rec(target, title, recommendation, rationale, traces, priority, effort):
    R.append(dict(id="REC-SBC-%03d" % (len(R) + 1), target=target, title=title, recommendation=recommendation,
                  rationale=rationale, traces_to=traces, priority=priority, effort=effort, status="proposed"))

rec("echelon-organization-administration", "Review the proposed construction rules for adoption",
 "Review the 28 proposed rules in security-by-construction/proposed-construction-rules.jsonl (SEC-DB-002 through SEC-DATA-002). Adopt, amend or reject each one explicitly, assign an owner and version, and record the decision. None of them is adopted by being listed here.",
 "The Standard's ten rules state principles but leave material bypasses uncovered: trusted database code, tenant isolation at the database, numeric correctness, regex denial of service, nullness, build-time code execution, runtime support status and AI-authored changes.",
 ["DD-SBC-001", "DD-SBC-002", STD], "P1", "medium")

rec("echelon-organization-administration", "Require level, scope and evidence for every assurance claim",
 "Amend the Standard so that any statement that a weakness class is prevented must name an assurance level from the ten-level scale, the scope within which it holds, the evidence artifact and its commit, and the known bypasses. Prohibit the words 'eliminated' or 'impossible' in customer-facing material unless L1 evidence exists for the stated scope.",
 "The Standard already says not to claim elimination without scoped evidence. A required structure makes the rule checkable and prevents marketing drift.",
 ["DD-SBC-001", STD], "P1", "low")

rec("echelon-organization-administration", "Correct the proposed system ownership in the Standard",
 "Replace the proposed ownership assignments that conflict with verified repository purposes: Aegis is an operational fault handling library, not a rule registry or SAST orchestrator; Vigila is a task organizer, not runtime monitoring; Dokimos routes security analysis to Tutela. Assign the rule registry and CWE mapping to Tutela or a new component, and runtime monitoring to an identified system.",
 "Ownership that does not match what a repository does leaves controls without an implementer, and due diligence reviewers will notice the mismatch.",
 ["architecture/ECHELON-CURRENT-STATE-BRIEF.md", STD], "P1", "low")

rec("strata", "Decide and build the application-facing typed query interface",
 "Decide whether Strata will provide the runtime interface that SEC-DB-001 assumes (precompiled named queries with typed bound parameters, no raw SQL entry point, tenant context required). If yes, design it so the only assembly that references Npgsql is Strata's host, reusing the tier check pattern in scripts/check-semantic-architecture.sh. If no, tell the Standard's owner so SEC-DB-001 names a different mechanism.",
 "Strata at c6a384ec is declarative schema management; no runtime typed query interface was found. SEC-DB-001 and the strongest SQL injection claim in the matrix depend on that interface.",
 ["strata@c6a384ec:README.md", "strata@c6a384ec:scripts/check-semantic-architecture.sh", "DD-SBC-002 CWE-89"], "P0", "high")

rec("strata", "Add catalog gates for dynamic SQL, SECURITY DEFINER and forced row-level security",
 "Extend Strata's catalog analysis to report (a) routines using EXECUTE with concatenation or %s in format(), (b) SECURITY DEFINER routines without a fixed search_path or with EXECUTE granted to PUBLIC, (c) tenant tables without ENABLE and FORCE ROW LEVEL SECURITY, and (d) roles with BYPASSRLS or ownership used by the application, as inputs to proposed SEC-DB-002 and SEC-DB-003.",
 "Strata already parses routines, models function privileges and reports tables with RLS enabled and no policies (src/Strata.Host.Postgres/CatalogQueries.fs). PostgreSQL documents that owners, superusers and BYPASSRLS roles bypass row security and that new functions grant EXECUTE to PUBLIC.",
 ["strata@c6a384ec:src/Strata.Host.Postgres/CatalogQueries.fs", "SEC-DB-002", "SEC-DB-003"], "P1", "medium")

rec("strata", "Move off the out-of-support .NET 8 runtime",
 "Retarget net8.0 projects to an in-support runtime (.NET 10 LTS, supported to 2028-11-14) and update global.json, Npgsql and related packages; record the change as release evidence.",
 ".NET 8 reached end of support on 2026-11-10. Strata.Cli, Strata.Host.Files, Strata.Host.PgParser and Strata.Host.Postgres target net8.0 and global.json pins SDK 8.0.0 with latestFeature roll forward.",
 ["strata@c6a384ec:global.json", "strata@c6a384ec:src/Strata.Host.Postgres/Strata.Host.Postgres.fsproj", "SEC-RUNTIME-001"], "P1", "medium")

rec("ordo", "Move off the out-of-support .NET 8 runtime",
 "Retarget Directory.Build.props from net8.0 to an in-support runtime and publish the change.",
 ".NET 8 reached end of support on 2026-11-10; ordo@db6d39ed:Directory.Build.props sets TargetFramework net8.0.",
 ["ordo@db6d39ed:Directory.Build.props", "SEC-RUNTIME-001"], "P2", "low")

rec("forma", "Remove the innerHTML sink from the workflow component",
 "Replace `this.#root.innerHTML = reply.html` in packages/workflow/src/forma-workflow.js with DOM construction from a structured tree or with Limen projection, and add a test that runs the component under the Limen strict CSP with require-trusted-types-for 'script' and trusted-types 'none'.",
 "The comment states the engine escapes all text and attributes, but this is an HTML-string sink that bypasses the structural guarantee SEC-UI-001 and SEC-UI-002 rely on, and it would be blocked by the Trusted Types policy Limen documents. A single escaping defect in the engine becomes XSS.",
 ["forma@c8f40b4c:packages/workflow/src/forma-workflow.js", "limen@743cdb9b:docs/29-binding-security.md", "SEC-UI-003", "DD-SBC-002 CWE-79"], "P1", "medium")

rec("limen", "Evaluate refusing id and name binding targets and extend the security smoke tests",
 "Assess whether engine-supplied values should be allowed to set id and name attributes (currently in the general setAttribute category), given DOM clobbering needs only those attributes. Add DOM clobbering, CSS injection through class or attribute selectors, and URL normalization edge cases to scripts/smoke-security.ts.",
 "Limen's binding policy is the strongest XSS evidence found, but DOM clobbering and CSS injection are HTML-only and CSS-only techniques that CSP and Trusted Types do not fully address (OWASP DOM Clobbering Prevention Cheat Sheet).",
 ["limen@743cdb9b:docs/29-binding-security.md", "limen@743cdb9b:src/kernel/binding-policy.ts", "SEC-UI-003"], "P2", "low")

rec("limen", "Document browser and WebAssembly residuals of the strict policy",
 "State in the binding security documentation that Trusted Types enforcement depends on browser support (MDN lists Baseline newly available since February 2026) and that .NET WebAssembly guests require 'wasm-unsafe-eval', and describe what protection remains in browsers that ignore the directives.",
 "Customers and reviewers will ask which guarantees hold in older or non-conforming browsers; the documentation currently describes the Chromium smoke result.",
 ["limen@743cdb9b:docs/29-binding-security.md", "DD-SBC-001"], "P3", "low")

rec("tutela", "Host the machine-readable construction rule registry and CWE mapping",
 "Model each Standard rule and adopted proposal as Tutela controls with invariants, CWE mappings, evidence requirements and release posture effects, importing security-by-construction/cwe-architectural-prevention-matrix.csv as the initial mapping.",
 "The Standard assigns the rule registry to Aegis, which is a fault handling library. Tutela's model (asset, boundary, threat, invariant, control, evidence, release posture) matches the registry's needs and Dokimos already names Tutela as the security authority.",
 ["tutela@476dc682:README.md", "DD-SBC-002", "REC-SBC-003"], "P1", "medium")

rec("praxis", "Provide fail-closed security gates that read compiled artifacts",
 "Add gate steps (or a hosted gate contract) that: scan compiled IL of all shipped assemblies for banned API references (SEC-EXEC-002, SEC-MEM-001, SEC-CRYPTO-002); extract effective compiler options from MSBuild binary logs (SEC-LANG-003, SEC-NULL-001, SEC-NUM-002); inventory package build assets, analyzers and type providers (SEC-BUILD-001); check target framework support (SEC-RUNTIME-001); and refuse release on missing evidence.",
 "F# compilations are not served by Roslyn analyzers such as banned-API analyzers, and project files can be overridden, so checks on compiled output and effective options are the reliable enforcement point. Praxis already operates validation workflows and provenance.",
 ["praxis@12bf9951", "SEC-EXEC-002", "SEC-LANG-003", "SEC-BUILD-001"], "P1", "high")

rec("praxis", "Protect gate configuration from AI-authored changes",
 "Require human approval for any change, by any author, to gate configuration, suppression lists, exception records and ownership files, and record agent provenance on all changes (SEC-AI-001).",
 "Construction rules are valuable because they bind AI-authored code; that value disappears if an agent can relax the gate in the same change.",
 ["SEC-AI-001", "docs/agent-provenance.md"], "P2", "low")

rec("echelon-organization-administration", "Publish a shared F# compiler baseline",
 "Define a shared Directory.Build.props baseline for Echelon F# products: TreatWarningsAsErrors; FS0025 and FS0009 errors with no suppression; Nullable enable; --checked+ for domain assemblies; WarnOn 1182,3559,3579,3388,3389,3395 in a single property; Deterministic builds; Release default. Record exceptions centrally.",
 "Practices differ across repositories (limen uses --warnaserror:25 and --reflectionfree; ordo enables Nullable; strata uses WarningLevel 5) and the F# documentation notes that only the last WarnOn property is used.",
 ["limen@743cdb9b:libraries/fsharp/Limen.Store/Limen.Store.fsproj", "ordo@db6d39ed:Directory.Build.props", "strata@c6a384ec:Directory.Build.props", "SEC-LANG-003"], "P1", "low")

rec("unbound", "Add construction-level requirements for money, authorization, tenancy and state",
 "Add Unbound requirements that trace the stated invariants to proposed rules: Money type and rounding (SEC-NUM-001), Authorized command values (SEC-AUTH-002), TenantContext across all stores (SEC-TENANT-001, SEC-DB-003), explicit workflow states and idempotency keys (SEC-STATE-001), with property-based tests as acceptance criteria.",
 "The Standard lists balanced journals, tenant-scoped access, idempotent disbursements and valid transitions as invariants; the matrix shows these are where the architecture gives assurance that scanning cannot.",
 ["unbound@9b38de47", STD, "DD-SBC-002"], "P1", "medium")

rec("dokimos", "Build an F# weakness fixture corpus to measure scanner coverage",
 "Create versioned vulnerable and safe F# fixtures for the matrix families where scanning is rated partial (SQL, command, code, deserialization, path, SSRF, null, numeric) and measure detection by the SAST tools under consideration, with holdout cases built independently. Confirm ownership with Tutela first.",
 "The matrix marks F# coverage by common SAST tools as unverified. The Standard calls for F#-specific fixtures; without them, claims about scanner equivalence cannot be made either way.",
 [STD, "DD-SBC-002", "dokimos@6ea86246:requirements/REQUIREMENTS.md"], "P2", "high")

rec("unbound", "Scope independent testing toward classes where architecture gives less",
 "When planning the external penetration test, direct effort to authorization policy correctness, business logic and workflow abuse, tenant isolation across all stores, identity and session flows, infrastructure configuration and third-party components, and provide testers with the matrix and residual risk list without limiting their scope.",
 "These are the classes where the matrix rates strongest achievable assurance at L7 to L10 or where construction rules do not apply, and where internal evidence is least persuasive to customers.",
 ["DD-SBC-001", STD], "P2", "medium")

rec("strata", "Record native code in the parser dependency",
 "Determine whether pgsqlparser 1.0.0 (used by Strata.Host.PgParser) loads native code, and list it in a native dependency inventory with version and patch source.",
 "Memory safety claims exclude native code; whether this dependency wraps a native PostgreSQL parser was not established in this research.",
 ["strata@c6a384ec:src/Strata.Host.PgParser/Strata.Host.PgParser.fsproj", "SEC-MEM-001"], "P3", "low")

with open(OUT, "w", encoding="utf-8") as fh:
    for r in R:
        s = json.dumps(r, ensure_ascii=False)
        assert "—" not in s
        fh.write(s + "\n")
print(len(R))
