import json, sys
OUT = sys.argv[1]
LABEL = "PROPOSAL ONLY for echelon-organization-administration. Not an adopted Echelon rule. Drafted by due diligence research DD-SBC-001 on 2026-11-25."
STD = "echelon-organization-administration@2763e576:policies/security/secure-construction-standard.md"
R = []
def rule(id, title, extends, rule, rationale, enforcement, negative_tests, evidence, residual, cwe, level, owner):
    R.append(dict(id=id, title=title, status="proposed", proposal_label=LABEL, proposed_for="echelon-organization-administration",
                  extends_standard_rules=extends, rule=rule, rationale=rationale, enforcement_mechanism=enforcement,
                  negative_tests=negative_tests, evidence=evidence, residual_risks=residual,
                  cwe=["CWE-%s" % c for c in cwe.split()], target_assurance_level=level,
                  candidate_owner=owner, source_standard=STD, traces_to=["DD-SBC-001", "DD-SBC-002"]))

rule("SEC-DB-002", "Dynamic SQL discipline inside PostgreSQL routines", ["SEC-DB-001"],
 "PL/pgSQL and SQL routines must not use EXECUTE except from a reviewed allowlist. Allowed EXECUTE statements pass data only through USING parameters and insert identifiers only through format() with %I (or quote_ident); %s and string concatenation of variable text are prohibited. SECURITY DEFINER routines must set a fixed search_path ending in pg_temp, and EXECUTE on them must be revoked from PUBLIC in the same transaction that creates them.",
 "SEC-DB-001 governs application code, but the Standard itself notes parameterization must cover trusted database internals. PostgreSQL documents that EXECUTE performs no variable substitution, that USING parameters are much less prone to SQL injection, that %I and %L in format() are the safe quoting forms, that new functions grant EXECUTE to PUBLIC by default, and that SECURITY DEFINER functions need a safe search_path.",
 "Catalog scan of pg_proc source for EXECUTE and SECURITY DEFINER in every migration artifact (Strata already parses routines and models function privileges); parser-based check that EXECUTE arguments are format() calls with only %I, %L or $n placeholders; release gate fails on unallowlisted findings.",
 ["Migration adds a function using EXECUTE 'SELECT ... ' || p_name; gate must fail.", "Function uses format('%s', p_value); gate must fail.", "SECURITY DEFINER function without SET search_path; gate must fail.", "SECURITY DEFINER function with EXECUTE still granted to PUBLIC; gate must fail."],
 ["Routine inventory with EXECUTE and SECURITY DEFINER flags per release", "Allowlist entries with reviewer, rationale and expiry", "Gate logs for each release"],
 ["Dynamic SQL in extensions and in ad hoc administrative sessions", "Logic errors in allowlisted routines", "Identifier quoting does not prevent access to unintended but valid objects"],
 "89 943 250 269", "L5", "Strata (schema analysis) with Tutela (control definition)")

rule("SEC-DB-003", "Database-enforced tenant isolation", ["SEC-AUTH-001", "SEC-DB-001"],
 "Every tenant-scoped table must have row-level security enabled and forced (ALTER TABLE ... FORCE ROW LEVEL SECURITY) with at least one policy keyed on the transaction-local tenant setting. The application role must not own tenant tables, must not be superuser and must have NOBYPASSRLS. Tenant context must be set with set_config(name, value, true) inside each transaction, never as a session setting on pooled connections.",
 "PostgreSQL documents that superusers and BYPASSRLS roles always bypass row security, that table owners bypass it unless FORCE is set, and that referential integrity checks always bypass it. Session-level settings persist on pooled connections and can leak tenant context between requests.",
 "Catalog gate over pg_class (relrowsecurity, relforcerowsecurity), pg_policy and pg_roles (rolbypassrls, rolsuper) plus ownership checks; integration test that runs as the application role through the connection pool.",
 ["Add a tenant table without FORCE ROW LEVEL SECURITY; gate must fail.", "Grant BYPASSRLS to the application role; gate must fail.", "Interleave two tenants' requests on one pooled connection with a session-level setting; test must detect cross-tenant reads.", "Query a foreign key or unique constraint to infer another tenant's key; record as residual covert channel."],
 ["Catalog report per release", "Cross-tenant property-based test results", "Role attribute report"],
 ["Covert channels through constraints, timing and error messages", "Migration and administrative roles bypass RLS by design", "Policies that are wrong"],
 "639 566 668 653 1220 250 213", "L5", "Strata with Unbound data layer")

rule("SEC-DB-004", "Privileged database paths and migrations", ["SEC-DB-001", "SEC-SUPPLY-001"],
 "Schema changes are applied only by Strata deploy from reviewed, versioned artifacts using a migration role distinct from the application role. Production ad hoc SQL requires break-glass approval, is recorded with the statement text and approver, and is time-limited.",
 "Migrations and operators run as owners or privileged roles that bypass row-level security and parameterization rules; they are the main trusted-infrastructure bypass of SEC-DB-001.",
 "Role separation in infrastructure as code; deploy pipeline is the only holder of migration credentials; database audit logging of privileged sessions; release gate compares deployed schema with the reviewed artifact (Strata diff).",
 ["Attempt a schema change with application credentials; must be refused.", "Run deploy from an unreviewed artifact; gate must fail.", "Break-glass session without an approval record; alert must fire."],
 ["Role and grant report", "Deploy logs with artifact hashes", "Break-glass records"],
 ["Compromised migration credentials", "Malicious but reviewed migrations"],
 "89 250 269 732 778", "L5", "Strata and Praxis")

rule("SEC-NUM-001", "Money representation and rounding", ["SEC-LANG-002"],
 "Monetary amounts must be represented by a Money type with a private constructor over System.Decimal plus an ISO 4217 currency, created only through validating constructors. Arithmetic across currencies is a compile-time or validated error. float, double and float32 must not appear in money modules. Every rounding operation must state its MidpointRounding mode and scale, and allocation of amounts across parts must preserve totals.",
 "Binary floating point cannot represent most decimal fractions. System.Decimal throws OverflowException in both checked and unchecked contexts, which is the desired failure. Math.Round defaults to banker's rounding, which may differ from contractual rounding. Balanced journal entries are a stated Unbound invariant.",
 "Type design with signature files; IL scan of money assemblies for System.Double and System.Single usage; FSharp.Analyzers.SDK rule or IL rule for Math.Round overloads without MidpointRounding; property-based tests.",
 ["Add a float field to a money record; gate must fail.", "Call Math.Round(amount, 2) without a rounding mode in a money module; gate must fail.", "Property test: allocating any amount across n parts sums to the original amount.", "Property test: posting any generated transaction set keeps debits equal to credits."],
 ["Type inventory", "IL scan report", "Property-based test results with seeds and generator definitions"],
 ["Specification errors in fee rules", "Database column scale mismatch", "Client-side JSON number parsing as double"],
 "682 1339 681 197 1077 1284 190", "L2", "Unbound domain with Ordo")

rule("SEC-NUM-002", "Overflow-checked integer arithmetic", ["SEC-LANG-001"],
 "Domain and persistence assemblies must compile with overflow checking enabled (--checked+ / CheckForOverflowUnderflow) or open the FSharp.Core Checked module in every file that performs integer arithmetic on quantities, counts, indices, timestamps or identifiers. Unchecked arithmetic requires a reviewed annotation.",
 "F# integer operators wrap on overflow by default; the Checked module and --checked option raise OverflowException instead. Wraparound in counts, limits and sequence numbers produces silent logic errors.",
 "Compiler option evidence from binary logs; gate fails if a listed assembly lacks the option; tests at boundary values.",
 ["Build a domain assembly without --checked+; gate must fail.", "Unit test Int32.MaxValue + 1 in a domain function; must raise OverflowException."],
 ["Effective compiler options per assembly", "Boundary test results"],
 ["Libraries compiled without checks", "Performance pressure to disable", "Overflow exceptions become denial of service if unhandled"],
 "190 191 128 197 681 839", "L4", "Echelon F# build baseline")

rule("SEC-REGEX-001", "Regular expression safety", ["SEC-DATA-001"],
 "Regular expressions applied to untrusted input must use RegexOptions.NonBacktracking where the pattern features allow it, otherwise a finite match timeout. Patterns must be compile-time constants (preferably source-generated); user-supplied patterns are prohibited. Input length must be bounded before matching.",
 "The .NET default match timeout is infinite. NonBacktracking guarantees linear time in input length. Microsoft states that timeouts and NonBacktracking protect against accidental performance problems and are not a security boundary against malicious patterns, which is why patterns must not come from users.",
 "IL scan for Regex constructors and static methods lacking NonBacktracking or a timeout argument; check that pattern arguments are literals; optional process-wide REGEX_DEFAULT_MATCH_TIMEOUT as a backstop.",
 ["Regex without timeout or NonBacktracking on a request path; gate must fail.", "Regex built from request data; gate must fail.", "Catastrophic backtracking corpus run against all patterns completes within budget."],
 ["Regex inventory", "Timing test results"],
 ["Regex use inside dependencies", "Validation logic that is wrong even if fast"],
 "1333 400 185 407", "L5", "Echelon F# build baseline")

rule("SEC-NULL-001", "Nullness discipline", ["SEC-LANG-002"],
 "F# projects must set <Nullable>enable</Nullable> (passing --checknulls+) with nullness warnings treated as errors. Unchecked.defaultof, Unchecked.withNull, Array.zeroCreate of reference types, AllowNullLiteral and CLIMutable are prohibited in domain modules. Every boundary decoder must reject null and missing fields before constructing domain values.",
 "F# types do not admit null in normal use, but null enters through .NET interop, Unchecked.defaultof, Array.zeroCreate and reflection-based deserializers. F# 9 nullness checking is off by default and reports warnings.",
 "Project property gate; IL scan for banned APIs in domain assemblies; decoder property tests feeding null and missing fields.",
 ["Domain module uses Unchecked.defaultof; gate must fail.", "JSON payload omits a required string field; decoder must return an error, not a record with null.", "Project without Nullable enable; gate must fail."],
 ["Effective compiler options", "IL scan report", "Decoder test results"],
 ["Unannotated .NET APIs", "Nulls inside third-party types"],
 "476 908 457 665 754", "L4", "Echelon F# build baseline")

rule("SEC-LANG-003", "F# compiler diagnostic baseline", ["SEC-LANG-001", "SEC-LANG-002"],
 "All F# projects must set TreatWarningsAsErrors, keep FS0025 (incomplete matches) and FS0009 (unverifiable IL) as errors with no suppression, and enable selected off-by-default warnings including 1182 (unused variables), 3559 (type inferred as obj), 3579 (untyped string interpolation), 3388, 3389 and 3395 (implicit conversions). #nowarn and NoWarn entries require an exception record. Wildcard patterns on unions designated security-sensitive are prohibited.",
 "Several useful F# warnings are off by default and the WarnOn property only honors its last occurrence, so baselines silently regress. FS0025 being an error is what makes explicit domain states enforceable; limen@743cdb9b and ordo@db6d39ed already use it at component level.",
 "Read effective options from MSBuild binary logs in CI rather than trusting project files; gate on any NoWarn or #nowarn; FSharp.Analyzers.SDK rule for wildcard cases on annotated unions.",
 ["Add a union case without handling it; build must fail.", "Add #nowarn \"25\"; gate must fail.", "Add a second WarnOn property that drops earlier entries; gate must detect the effective loss."],
 ["Binary log extract of effective options per project", "Suppression inventory"],
 ["Wildcard cases still compile", "Analyzer coverage gaps"],
 "478 703 754 1164 561 628", "L4", "Echelon F# build baseline")

rule("SEC-MEM-001", "Unsafe code and native interop prohibition", ["SEC-LANG-001"],
 "Application assemblies must not reference NativePtr, fixed, stackalloc, System.Runtime.CompilerServices.Unsafe, MemoryMarshal reinterpretation methods, DllImport or LibraryImport, NativeLibrary, Marshal, function pointers, or C# projects with AllowUnsafeBlocks. Native code may enter only through reviewed packages listed in a native dependency inventory with version and patch source.",
 "Managed code with bounds checking eliminates memory corruption only while code stays verifiable. F# reports FS0009 for constructs that may produce unverifiable IL; that warning can be suppressed. Native libraries and the runtime remain outside the guarantee.",
 "IL reference scan of all shipped assemblies, IL verification, FS0009 as error with no suppression, native asset inventory from NuGet runtimes folders.",
 ["Introduce NativePtr.read in an application file; build must fail.", "Add a package with a native runtimes asset not in the inventory; gate must fail.", "Add DllImport; gate must fail."],
 ["IL scan and verification reports", "Native dependency inventory"],
 ["Runtime, JIT and native dependency vulnerabilities", "Unsafe code inside approved managed packages"],
 "787 125 120 121 122 416 843 119", "L5", "Echelon F# build baseline with Tutela")

rule("SEC-EXEC-002", "Banned dynamic execution capability list", ["SEC-EXEC-001"],
 "Application assemblies must not reference FSharp.Compiler.Service or FSI hosting, System.Reflection.Emit, Assembly.Load, LoadFrom or LoadFile, AssemblyLoadContext, System.Linq.Expressions compilation, Activator.CreateInstance or Type.GetType with string type names, System.Diagnostics.Process, or scripting engines. Exceptions are infrastructure-only and recorded.",
 "SEC-EXEC-001 states the principle; this rule makes it checkable. Roslyn analyzers such as banned-API analyzers serve C# and Visual Basic compilations; F# needs IL-level or FSharp.Analyzers.SDK checks, so the check must run on compiled IL.",
 "IL reference scan of application and transitive assemblies against the banned list, with an allowlist of reviewed dependency uses.",
 ["Call Expression.Compile in application code; gate must fail.", "Add a package that uses Reflection.Emit; gate must report it for review.", "Call Type.GetType(userValue); gate must fail."],
 ["IL scan report", "Dependency exception records"],
 ["Dynamic code inside approved dependencies", "Runtime defects"],
 "94 95 470 913 78 77 502", "L5", "Echelon F# build baseline with Tutela")

rule("SEC-BUILD-001", "Control code that executes during the build", ["SEC-SUPPLY-001"],
 "Packages that execute code during restore or build (MSBuild props and targets in build, buildMultiTargeting or buildTransitive folders, MSBuild tasks, analyzers, source generators, F# type providers) must be individually approved. Release builds run hermetically from a locked package set with network egress blocked except to the approved feed.",
 "NuGet imports package-supplied props and targets into consuming projects through generated nuget.g.props and nuget.g.targets files, including transitively through buildTransitive. F# type providers run inside the compiler and can read files or contact services given as parameters. These run with the build's privileges, before any runtime control applies.",
 "Inspect obj/*.nuget.g.props and .targets for imports; inventory packages with build, analyzers or type provider assets; hermetic build runner with egress policy; build provenance attestation.",
 ["Add a package with a build/*.targets file; gate must flag it.", "Type provider pointing at a network URL in a release build; build must fail under egress policy."],
 ["Build-asset inventory", "Hermetic build logs", "Provenance attestation"],
 ["Compromise of an approved build-time package", "Developer workstation builds outside the hermetic runner"],
 "829 494 506 1357 1395 912", "L5", "Praxis with SEC-SUPPLY-001 owner")

rule("SEC-RUNTIME-001", "Supported runtime and patch currency", ["SEC-LANG-001", "SEC-SUPPLY-001"],
 "Production and release builds must target an in-support .NET version on its latest patch, and native base images must be patched within a defined window. A release gate fails for out-of-support target frameworks.",
 "Memory safety relies on the runtime. .NET 8 (LTS) and .NET 9 (STS) reached end of support on 2026-11-10; .NET 10 (LTS) is supported to 2028-11-14. strata@c6a384ec and ordo@db6d39ed target net8.0, so their runtime is now out of support.",
 "Gate reads TargetFramework and runtime pack versions; SCA on base images; patch SLA tracking.",
 ["Build a release targeting net8.0 after its end of support; gate must fail."],
 ["Runtime inventory per release", "Patch timeline records"],
 ["Zero-day runtime vulnerabilities", "Upgrade regressions"],
 "1104 1329 1395 787 125", "L5", "Praxis")

rule("SEC-DESER-001", "Deserialization contracts", ["SEC-DATA-001"],
 "External payloads must be decoded with explicit F# decoders or System.Text.Json with explicit contracts (source-generated contexts require a C# companion project because the generator is a C# source generator; verify before adopting) into DTOs, then into validated domain types. Polymorphic deserialization is allowed only through closed, explicitly registered discriminators with unknown discriminators rejected. Newtonsoft.Json may be used only with TypeNameHandling.None. The System.Runtime.Serialization.Formatters compatibility package and other type-embedding formatters are prohibited. Maximum payload size and depth must be set.",
 "Microsoft removed the BinaryFormatter implementation in .NET 9 (APIs throw PlatformNotSupportedException) but provides an unsupported compatibility package that restores it with its risks. System.Text.Json polymorphism is opt-in through JsonDerivedType registrations. Newtonsoft documents that TypeNameHandling other than None needs a custom SerializationBinder for external JSON.",
 "Dependency graph gate for banned packages; IL scan for TypeNameHandling values and formatter types; decoder tests.",
 ["Payload with $type naming an unregistered type; decoder must reject.", "Add System.Runtime.Serialization.Formatters; gate must fail.", "Set TypeNameHandling.Auto; gate must fail.", "Payload nested deeper than the limit; decoder must reject."],
 ["Dependency graph report", "Decoder test results"],
 ["Serialization inside dependencies", "Logic errors in custom converters"],
 "502 915 1321 470 20", "L5", "Unbound platform with Tutela")

rule("SEC-RES-001", "Bounded resource consumption", ["SEC-DATA-001"],
 "Every externally reachable operation must have bounds on request size, collection length, nesting depth, recursion depth, page size, execution time and decompressed size, expressed in validated input types or middleware configuration, with rate limiting per principal and tenant.",
 "Managed memory does not prevent denial of service. StackOverflowException cannot be caught and terminates the process. Allocation without limits is rank 25 in the 2025 Top 25.",
 "Limit inventory generated from route registration; load and fuzz tests; runtime saturation alerts.",
 ["Send a body larger than the limit; must be rejected before buffering.", "Send JSON nested beyond MaxDepth; must be rejected.", "Request page size above cap; must be clamped or rejected.", "Deep recursive structure in a domain decoder; must be rejected before recursion limit."],
 ["Limit inventory", "Load test results", "Runtime telemetry"],
 ["Distributed denial of service", "Expensive legitimate workloads"],
 "770 400 789 674 409 776 834 835 1333 799", "L3", "Unbound platform")

rule("SEC-UI-003", "Browser hardening baseline including component libraries", ["SEC-UI-001", "SEC-UI-002"],
 "All product pages must be served with a strict CSP at least as strong as the Limen documented policy, including require-trusted-types-for 'script' and trusted-types 'none' unless a reviewed exception exists. No component library, including Forma packages, may write HTML strings to the DOM. Engine-supplied values must not set id or name attributes. Session cookies must be Secure, HttpOnly and SameSite. Third-party scripts are prohibited.",
 "Limen demonstrates the policy at component level (limen@743cdb9b:docs/29-binding-security.md). forma@c8f40b4c:packages/workflow/src/forma-workflow.js line 127 assigns engine-built HTML to innerHTML, which a Trusted Types 'none' policy would block and which relies on the engine's escaping. DOM clobbering needs only id or name attributes. Trusted Types reached Baseline (newly available) in February 2026 per MDN, so older browsers will not enforce it.",
 "Limen smoke:security run against every product page in CI; bundle scan for HTML-string sinks; header conformance tests; CSP violation reporting in production.",
 ["Add innerHTML in any bundled component; smoke test must report a Trusted Types violation.", "Bind an engine value to id; static view checker must refuse.", "Load a third-party script; CSP must block and report."],
 ["Smoke test results per release", "Bundle sink inventory", "CSP report telemetry"],
 ["Browsers without Trusted Types", "'wasm-unsafe-eval' required by .NET WebAssembly guests", "Browser vendor defects"],
 "79 80 83 1021 1022 830 829 352 1275 614 1004 601", "L3", "Limen with Forma")

rule("SEC-AUTH-002", "Authorization by construction", ["SEC-AUTH-001"],
 "Every state-changing domain operation must take an Authorized command value whose constructor is private to the policy module and which records principal, tenant, permission and decision time. Repositories and Strata interfaces for tenant data must require a TenantContext obtained from the same decision. A generated negative test matrix must cover every role by every operation.",
 "Missing authorization (rank 4) becomes a compile error when the signature demands a decision value. Incorrect authorization (rank 17) is not prevented by types and needs specification-based tests and adversarial review.",
 "Signature files or private constructors; IL scan for reflection or serializer construction of Authorized types; generated tests from a policy specification.",
 ["Call a command handler without an Authorized value; build must fail.", "Deserialize an Authorized value from JSON; must be impossible or rejected.", "Generated matrix: every forbidden role and operation pair must be denied."],
 ["Type visibility review", "Test matrix results", "Independent penetration test findings"],
 ["Wrong policy rules", "Insider misuse within granted rights"],
 "862 863 285 284 639 566 425 602 1220 841", "L2", "Unbound domain with Tutela")

rule("SEC-TENANT-001", "Tenant isolation across all stores", ["SEC-AUTH-001"],
 "Tenant identity must be a distinct type carried through every data access, cache key, object storage prefix, search index, message, background job, export and log record, and isolation must be tested across each store, not only the database.",
 "Database row-level security does not protect caches, files, search indexes, queues or analytics; cross-tenant leakage in a multi-tenant financial platform is a critical failure.",
 "Typed interfaces; store inventory; cross-tenant property-based and adversarial tests.",
 ["Cache read with another tenant's key; must miss or be refused.", "Background job processing a message for tenant A must not read tenant B data.", "Export for tenant A contains only tenant A rows."],
 ["Store inventory with isolation mechanism", "Cross-tenant test results"],
 ["Shared infrastructure side channels", "Operator access"],
 "639 668 653 200 359 1220", "L2", "Unbound platform")

rule("SEC-STATE-001", "Explicit domain states and idempotent effects", ["SEC-LANG-002"],
 "Workflow states (grants, disbursements, approvals) must be F# unions with transition functions as the only producers of successor states; effects with external consequences must carry idempotency keys enforced by database unique constraints; concurrent updates must use optimistic version checks or SERIALIZABLE transactions with retry.",
 "Valid workflow transitions, idempotent disbursements and separation of duties are stated Unbound invariants. Race conditions and replay are the main financial integrity risks that memory safety does not address.",
 "State model review (Ordo method); property-based and model-based tests; concurrency stress tests; constraint inventory.",
 ["Submit the same disbursement twice concurrently; exactly one must succeed.", "Attempt an approval transition from a state that does not allow it; must not compile or must return an error case.", "Replay a captured request; must be rejected or idempotent."],
 ["State models", "Test results with seeds", "Constraint inventory"],
 ["External payment system inconsistency", "Interleavings not explored by tests"],
 "362 367 837 841 294 1265 820 821", "L2", "Ordo with Unbound domain")

rule("SEC-EVID-001", "Mandatory evidence provenance", ["SEC-SUPPLY-001"],
 "Every security evidence artifact (scan result, test run, gate decision, review) must record repository, commit, artifact hash, tool and rule versions, scope, timestamp and actor (human or agent with model and runtime), be signed or hash-chained, and be stored append-only. Runtime audit history must be hash-chained with periodic verification.",
 "The Standard requires signed evidence and tamper-evident audit history. Evidence without provenance cannot support an assurance claim to customers or auditors. Praxis already records agent provenance for changes (praxis@12bf9951), which is a starting point for change evidence, not runtime audit.",
 "Evidence schema validation in CI; signing; hash chain verification job; release gate refuses missing evidence.",
 ["Release with a gate result lacking a commit hash; gate must fail.", "Alter a stored audit record; verification job must detect it."],
 ["Evidence registry", "Verification job results"],
 ["Compromise of signing keys", "Evidence that is authentic but measures the wrong thing"],
 "778 223 353 345 117", "L5", "Praxis with Tutela")

rule("SEC-AI-001", "AI-authored code and AI runtime authority", ["SEC-SUPPLY-001", "SEC-AUTH-001"],
 "Changes authored by AI agents must carry provenance (agent, model, runtime), pass the same gates as human changes, and receive human review for security-sensitive paths. Agents must not modify gate configuration, exception records or CODEOWNERS without human approval. Runtime AI features may act only through typed commands that pass validation and authorization, with model output treated as untrusted input.",
 "AI agents produce plausible code at volume and can weaken controls while satisfying tests. Construction rules are valuable precisely because they apply equally to AI-authored code. Bounded AI-agent authority is a stated Unbound invariant.",
 "Provenance trailers checked in CI; path-based protection for gate configuration; review requirements; agent tool inventory.",
 ["AI-authored change adds #nowarn \"25\"; gate must fail regardless of author.", "AI-authored change edits the exception registry; merge must require human approval.", "Prompt injection test instructs a runtime agent to disburse funds; command must be refused by authorization."],
 ["Provenance records", "Review logs", "Prompt injection test results"],
 ["Model misbehavior within authorized scope", "Reviewers trusting plausible code"],
 "1426 1427 1434 693 506", "L5", "Praxis with Tutela")

rule("SEC-ERR-001", "Fail-closed exceptional condition handling", ["SEC-LANG-002"],
 "Expected failures must be union cases; broad catch handlers that continue processing are prohibited outside the top-level boundary; the boundary returns generic errors, rolls back transactions and records an event. Authorization and payment decisions must fail closed.",
 "OWASP Top 10 2025 adds A10 Mishandling of Exceptional Conditions. Exceptions converted to defaults are a common path to fail-open behavior.",
 "Analyzer for catch-all handlers; fault injection tests; transaction rollback tests.",
 ["Inject a database timeout during authorization; request must be denied.", "Inject an exception after a partial write; transaction must roll back."],
 ["Fault injection results", "Handler inventory"],
 ["Failures in external systems after commit"],
 "703 754 755 636 248 390 396 460 209", "L4", "Unbound platform with Aegis")

rule("SEC-LOG-001", "Structured logging and sensitive data types", ["SEC-CRYPTO-001"],
 "Logs must be structured with typed fields; string-concatenated log messages from input are prohibited. Classified data must be wrapped in a Sensitive type whose formatting and serialization redact by default and whose reveal function is reviewed.",
 "Log injection and sensitive data in logs are OWASP-mapped weaknesses; structural typing addresses both more reliably than pattern-based scanning.",
 "Type design; IL scan for logger calls with interpolated strings; canary value tests over log output.",
 ["Log a request field via string interpolation; analyzer must fail.", "Canary account number in a request must not appear in any log."],
 ["Canary test results", "Logging configuration"],
 ["Data extracted from the wrapper", "Library logging"],
 "117 532 200 359 209 212 779", "L2", "Aegis with Unbound platform")

rule("SEC-EGRESS-001", "Outbound request control", ["SEC-DATA-001"],
 "Outbound HTTP calls must use typed clients bound to configured base addresses; request data must never determine the host. Redirects to non-allowlisted hosts are refused. Workloads run under an egress allowlist that excludes cloud metadata endpoints unless required.",
 "SSRF is rank 22 in the 2025 Top 25 and is often blind; network policy provides a second layer that application code cannot bypass.",
 "Client inventory; egress policy as code; tests with internal and metadata addresses.",
 ["Configure a webhook to an internal address; must be refused.", "Follow a redirect to a metadata address; must be refused."],
 ["Client inventory", "Egress policy and flow logs"],
 ["Compromised allowlisted destinations", "DNS rebinding"],
 "918 441 610 611", "L3", "Unbound platform")

rule("SEC-FILE-001", "Uploads and file handling", ["SEC-DATA-001"],
 "Application code must not construct file system paths from input. Uploaded content is stored in object storage under server-generated keys, with size limits, content inspection, malware scanning and download with Content-Disposition attachment and nosniff.",
 "Path traversal and dangerous uploads are ranks 6 and 12 in the 2025 Top 25.",
 "IL scan for System.IO usage outside the storage module; upload tests.",
 ["Upload a file named ../../x; stored key must be server-generated.", "Upload an HTML file and fetch it; must be served as attachment."],
 ["Upload test results", "Storage policy"],
 ["Malicious content exploiting viewers"],
 "22 23 36 73 434 646 552", "L3", "Unbound platform")

rule("SEC-AUTH-003", "Authentication by default and approved identity", ["SEC-AUTH-001", "SEC-CRYPTO-001"],
 "Every endpoint requires an authenticated principal through a router fallback policy; anonymous access requires an explicit, reviewed exemption. Authentication uses an approved identity provider and standard protocol libraries with issuer, audience, algorithm and lifetime validation. Privileged roles require phishing-resistant multifactor authentication. Sessions have idle and absolute timeouts and are invalidated on logout and credential change.",
 "Missing authentication for critical functions is rank 21 in the 2025 Top 25. CWE 5.0 deprecated CWE-613 in favor of CWE-1462 and its descendants on session management.",
 "Route inventory from the router with authentication requirement; token validation tests; session tests; external testing.",
 ["Register a route without an exemption; anonymous request must receive 401.", "Present a token with the wrong audience; must be rejected.", "Use a session after logout; must be rejected."],
 ["Route inventory", "Token and session test results", "Identity provider configuration export"],
 ["Credential theft and phishing", "Identity provider compromise", "Support-desk social engineering"],
 "306 287 288 384 1462 1463 1464 1465 1466 1390 307 308", "L3", "Unbound platform")

rule("SEC-CRYPTO-002", "Banned cryptographic algorithms and APIs", ["SEC-CRYPTO-001"],
 "Application code must perform cryptography only through an approved facade. Direct use of MD5, SHA1 for security purposes, DES, TripleDES, RC2, ECB mode, RSA PKCS#1 v1.5 encryption padding, System.Random for security values, non-constant-time secret comparison, and certificate validation callbacks that accept all certificates is prohibited.",
 "SEC-CRYPTO-001 prohibits custom algorithms but does not list weak uses of approved libraries, which are the common failure.",
 "IL reference scan for banned types and members; facade API review; TLS configuration scanning.",
 ["Use MD5.Create in application code; gate must fail.", "Use System.Random to generate a token; gate must fail.", "Set ServerCertificateCustomValidationCallback to return true; gate must fail."],
 ["IL scan report", "Facade review record"],
 ["Platform crypto defects", "Key management failures"],
 "327 328 326 330 338 295 780 208 1240", "L5", "Echelon F# build baseline")

rule("SEC-CONFIG-001", "Secure configuration as code", ["SEC-SUPPLY-001", "SEC-CRYPTO-001"],
 "Deployed configuration is generated from reviewed code with secure defaults; Release builds only; no debug endpoints, verbose errors or sample credentials in production; secrets only from a managed secret service; drift is detected and alerts.",
 "Security Misconfiguration is A02 in OWASP Top 10 2025. Construction rules do not cover runtime configuration unless configuration is itself code with a gate.",
 "Configuration scanner in the release gate; drift detection; assembly metadata check for Release configuration.",
 ["Deploy with a Debug assembly; gate must fail.", "Enable a developer exception page in production configuration; gate must fail."],
 ["Configuration scan results", "Drift reports"],
 ["Console changes outside code", "Provider default changes"],
 "16 1188 11 489 756 260 526 942", "L5", "Praxis with Unbound platform")

rule("SEC-DATA-002", "Canonicalize, validate and encode at single boundaries", ["SEC-DATA-001", "SEC-UI-001"],
 "Each trust boundary has one decoder that canonicalizes (including Unicode normalization where identifiers or names are compared) before validation, and each output sink has one encoder module. Raw-string escape hatches in builders are prohibited.",
 "Validation before canonicalization and ad hoc encoding are recurring causes of injection and confusion weaknesses.",
 "Sink and boundary inventory; IL scan for direct sink use; property-based tests of decoders and encoders.",
 ["Submit an identifier differing only by Unicode normalization form; must compare equal or be rejected consistently.", "Export a value starting with = to CSV; must be neutralized."],
 ["Boundary and sink inventory", "Property test results"],
 ["Unknown downstream interpreters"],
 "20 179 180 176 116 838 1236 74 1007", "L2", "Unbound platform with Forma")

for r in R:
    for k, v in r.items():
        s = json.dumps(v)
        assert "\\u2014" not in s and "—" not in s, (r["id"], k)
with open(OUT, "w", encoding="utf-8") as fh:
    for r in R:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
print(len(R), "rules")
