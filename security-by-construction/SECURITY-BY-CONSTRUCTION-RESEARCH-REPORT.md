---
id: DD-SBC-001
title: Security by construction research report and architectural assurance model
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
owners:
  - due-diligence-research
tags: [security-by-construction, assurance, cwe, secure-construction-standard, due-diligence]
related_documents:
  - docs/DUE-DILIGENCE-OPERATING-CONTRACT.md
  - architecture/ECHELON-CURRENT-STATE-BRIEF.md
  - security-by-construction/CWE-ARCHITECTURAL-PREVENTION-MATRIX.md
  - security-by-construction/cwe-architectural-prevention-matrix.csv
  - security-by-construction/proposed-construction-rules.jsonl
  - recommendations/security-by-construction-recommendations.jsonl
source_standard: echelon-organization-administration@2763e576:policies/security/secure-construction-standard.md
---

# Security by construction: research report and architectural assurance model

## 1. Summary

The Echelon Secure Construction Standard v0.1 (proposed, not adopted) sets ten rules
intended to prevent vulnerability classes by construction rather than detect them after
the fact. This report expands those rules into an assurance model that states, for each
principle and for 353 CWE entries, the strongest assurance level the architecture could
support, the scope in which that level holds, the known bypasses, the residual risk,
and the evidence that would be needed to make the claim.

**Nothing in this report is a claim about current capability.** Unbound has no code
(`unbound@9b38de47` is requirements only), Echelon has no production deployment, no
external penetration test and no adopted policy set. Every matrix row has
`current_status = proposed-target-state` and `current_demonstrated_level = none`. Where an
Echelon repository demonstrates part of a control at component level, the row cites it
as `component_evidence`, never as Unbound evidence. All evidence discussed here is
first-party; none of it is independent assurance.

### Key findings

1. **The architecture can plausibly reach L1 (eliminated within defined scope) only for
   capability-absence classes,** and only with build evidence: SQL injection, OS command
   injection, dynamic code evaluation, unsafe deserialization, and memory corruption,
   each restricted to application F# assemblies whose compiled IL lacks the relevant
   references. 32 of 353 rows target L1, and 14 of those are platform-specific weaknesses
   (PHP, Struts, Android, J2EE) that are out of scope only while a language inventory gate
   proves it. None of these is L1 today.
2. **The largest assurance gains over conventional scanning are in classes that scanners
   do not model:** missing authorization (CWE-862), tenant isolation (CWE-639, CWE-668),
   workflow and idempotency integrity (CWE-841, CWE-837, CWE-362), money arithmetic
   (CWE-682, CWE-1339, CWE-190), and exhaustive handling of exceptional states (OWASP
   2025 A10). Types can make a missing check a compile error; scanners rarely find these
   at all. 202 rows are rated `beyond` scanning, 62 `complementary`, 89 `comparable`.
3. **The architecture gives less than scanning in specific places,** not whole classes:
   known-vulnerable components, secrets, transport and header configuration, and
   infrastructure misconfiguration, where mature scanners are the primary control and
   construction rules add little; and wherever the F# toolchain lacks analyzer coverage,
   because Roslyn-based analyzers (C# and Visual Basic) do not run on F# and common SAST
   tools' F# support is unverified. Construction assurance also says nothing about
   whether a correct-by-type authorization policy is the right policy.
4. **SEC-DB-001 depends on a capability that does not exist.** Strata at `c6a384ec` is
   declarative schema management. No runtime typed query interface was found. Strata's
   own host generates DDL dynamically with identifier quoting
   (`strata@c6a384ec:src/Strata.Host.Postgres/ReferenceData.fs`), which is expected for a
   schema tool and shows that trusted infrastructure must be inside the assurance scope.
5. **The trusted database boundary is the main bypass of the SQL and tenancy rules.**
   PostgreSQL documents that `EXECUTE` performs no variable substitution, that new
   functions grant `EXECUTE` to `PUBLIC`, that `SECURITY DEFINER` needs a safe
   `search_path`, and that superusers, `BYPASSRLS` roles and table owners (absent
   `FORCE ROW LEVEL SECURITY`) bypass row security, while referential integrity checks
   always bypass it. Proposed rules SEC-DB-002, SEC-DB-003 and SEC-DB-004 address this.
6. **A component library already contradicts SEC-UI-001 and SEC-UI-002 in spirit:**
   `forma@c8f40b4c:packages/workflow/src/forma-workflow.js` line 127 assigns engine-built
   HTML to `innerHTML`. Limen's documented policy (Trusted Types with no policy defined)
   would block it. Limen itself is the strongest component evidence found
   (`limen@743cdb9b:docs/29-binding-security.md`, CI-run `smoke:security`).
7. **Runtime support status is now a finding.** .NET 8 and .NET 9 reached end of support
   on 2026-11-10. Strata and Ordo target `net8.0`. Memory-safety claims rest on a
   patched runtime, so SEC-RUNTIME-001 is proposed.
8. **F# compiler defaults are weaker than the Standard assumes.** FS0025 (incomplete
   match) is a warning by default; integer arithmetic is unchecked by default; nullness
   checking (F# 9 and later) is off by default and reports warnings; several useful
   warnings are opt-in and the `WarnOn` property honors only its last occurrence. Limen,
   Ordo and Strata each set some of these, inconsistently.
9. **28 additional rules are proposed** for `echelon-organization-administration` (not
   adopted). The most consequential are SEC-DB-002/003, SEC-NUM-001/002, SEC-AUTH-002,
   SEC-TENANT-001, SEC-STATE-001, SEC-BUILD-001 and SEC-RUNTIME-001.

## 2. Scope, method and sources

### 2.1 Inputs read

- `docs/DUE-DILIGENCE-OPERATING-CONTRACT.md` (DD-GOV-001) and
  `architecture/ECHELON-CURRENT-STATE-BRIEF.md` (DD-ARC-001).
- `echelon-organization-administration@2763e576:policies/security/secure-construction-standard.md`
  (Standard v0.1, ten rules SEC-DB-001 through SEC-SUPPLY-001).
- Read-only clones at the commits named in the brief: `limen@743cdb9b`, `strata@c6a384ec`,
  `tutela@476dc682`, `praxis@12bf9951`, `forma@c8f40b4c`, `ordo@db6d39ed`. Inspection was by
  reading files and text search; nothing was built or executed, so statements about these
  repositories describe source, not verified behavior.

### 2.2 External verification (accessed 2026-11-25)

| Claim | Source | Result |
|---|---|---|
| Current CWE version | MITRE CWE downloads and 2026 news | CWE 5.0, schema 8.0, released 2026-10-28; 956 weaknesses; Category replaced by Grouping; CWE-377, CWE-391, CWE-613 deprecated; CWE-1462 to CWE-1472 session and credential entries added |
| Catalog file used | `https://cwe.mitre.org/data/xml/cwec_latest.xml.zip` | Archive SHA-256 `bcda44c9...a3dc`, XML SHA-256 `47165a95...efb1d` (full values in DD-SBC-002) |
| Latest CWE Top 25 | `https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html` and view CWE-1435 | 2025 list (page updated 2025-12-15); no 2026 list found |
| OWASP Top 10 mappings | OWASP `https://top10.owasp.org/2025` and CWE views 1450, 1344 | OWASP site presents the 2025 release; the CWE catalog's view is labeled RC1 (2025). Final versus RC1 mapping differences not reconciled (open question OQ-SBC-01) |
| BinaryFormatter | Microsoft Learn, BinaryFormatter migration guide | From .NET 9 the runtime has no implementation; APIs throw `PlatformNotSupportedException`; an unsupported `System.Runtime.Serialization.Formatters` package restores it |
| System.Text.Json polymorphism | Microsoft Learn, polymorphism article | Opt-in through `JsonDerivedType`; unregistered derived types throw unless `UnknownDerivedTypeHandling` is changed; .NET 11 adds closed-hierarchy inference |
| Newtonsoft `TypeNameHandling` | Newtonsoft API documentation | Use with caution for external JSON; validate types with a custom `SerializationBinder` for values other than `None` |
| F# compiler options and opt-in warnings | Microsoft Learn, F# compiler options | `--checked`, `--checknulls`, `--warnon`, `--warnaserror`, `--reflectionfree`; opt-in warnings include 1182, 3388, 3389, 3395, 3559, 3579; only the last `WarnOn` property is used |
| F# null | Microsoft Learn, F# null values | Null arises from interop, `Unchecked.defaultof`, `Array.zeroCreate`; F# 9 nullness is off by default and enabled with `<Nullable>enable</Nullable>` |
| F# checked arithmetic | FSharp.Core `Checked` module documentation | Provides overflow-checked operators and conversions |
| Decimal and integer overflow | Microsoft Learn, checked and unchecked | Integral arithmetic is unchecked by default; `decimal` operations throw in both checked and unchecked contexts |
| Stack overflow | Microsoft Learn, `StackOverflowException` | Cannot be caught; the process is terminated by default |
| Regex | Microsoft Learn, regex best practices | Default timeout is infinite; `NonBacktracking` guarantees linear time in input length; neither is a security boundary against malicious patterns |
| Package build logic | Microsoft Learn, MSBuild props and targets in a package | `build`, `buildMultiTargeting`, `buildTransitive` props and targets are imported into consuming projects through generated files |
| Type providers | Microsoft Learn, F# type providers | Provided types are generated by the compiler from inputs such as files, URLs or connection strings |
| Row-level security | PostgreSQL 19 documentation (current), section on row security policies | Superusers and `BYPASSRLS` bypass; owners bypass unless `FORCE`; referential integrity checks always bypass |
| Dynamic SQL in PL/pgSQL | PostgreSQL documentation, PL/pgSQL basic statements | No substitution in `EXECUTE`; `USING` preferred; `format()` `%I` and `%L`; utility statements need textual insertion |
| `SECURITY DEFINER` | PostgreSQL documentation, `CREATE FUNCTION` | Set `search_path` excluding untrusted schemas with `pg_temp` last; revoke default `PUBLIC` execute in the same transaction |
| .NET support | Microsoft .NET support policy page | .NET 8 and 9 out of support since 2026-11-10; .NET 10 LTS to 2028-11-14; .NET 11 STS released 2026-11-10 |
| Trusted Types | MDN Trusted Types API | Baseline 2026, newly available since February 2026; `require-trusted-types-for` enforces typed values at DOM XSS sinks |
| DOM clobbering | OWASP DOM Clobbering Prevention Cheat Sheet | HTML-only technique using `id` or `name`; restrictive `script-src` does not stop clobbering that abuses code already on the page |
| System.Text.Json source generation | Microsoft Learn, source generation | Available in C# projects (C# 9 or later); F# is not listed |

### 2.3 How the matrix was built

1. Parsed CWE 5.0 XML. Took the 25 members of view CWE-1435 (2025 Top 25), every
   weakness in the ten groupings of view CWE-1450 (OWASP Top 10 2025 RC1), every weakness
   in view CWE-1344 (OWASP Top 10 2021), and 79 additional weaknesses chosen for a
   multi-tenant financial web application (numeric correctness, concurrency, resource
   bounds, session management entries new in CWE 5.0, AI integration, export injection).
   Two grouping-level entries listed by OWASP views (CWE-16) were retained for traceability.
2. Assigned each CWE to one of 30 control families. Each family carries default text
   for controls, scope, bypasses, residual risk, evidence and scanning; about 300
   per-CWE overrides refine relevance, level and notes.
3. Rated `strongest_achievable_level` as the strongest level the architecture could
   support for that CWE within the stated scope if the listed evidence existed;
   `supporting_levels` lists the weaker levels that also contribute.
4. Rated conventional scanning (SAST, DAST, SCA, secret and configuration scanning)
   as `yes`, `partial` or `no`, and compared it with the architecture as `beyond`,
   `comparable` or `complementary`.

The ratings are research judgments supported by the cited documentation; they are not
measurements. The proposed F# fixture corpus (REC-SBC-016) is the way to replace the
scanning judgments with data.

## 3. Assurance model

### 3.1 Levels

| Level | Name | Meaning in this model | Typical evidence |
|---|---|---|---|
| L1 | Eliminated within defined scope | The scope cannot express the weakness: the capability is absent from the compiled artifact and the absence is checked on every build | IL reference scan, dependency graph, language inventory, each with commit and artifact hash |
| L2 | Type system | Well-typed code cannot reach the weakness without a visible, reviewable escape (reflection, `Unchecked`, interop) | Type and module visibility review, signature files, escape-hatch scan |
| L3 | Restricted interface | All access goes through an approved interface that is safe by design; bypass requires adding a forbidden dependency | Interface API review, reference gate |
| L4 | Compiler enforcement | A compiler diagnostic turns the defect into a build failure | Effective compiler options from binary logs; suppression inventory |
| L5 | Build or release gate | A fail-closed gate blocks merge or release on a detectable condition | Gate definition, logs, negative tests proving the gate fails |
| L6 | Automated analysis | Static or dynamic analysis finds instances with measured precision and recall | Scanner results plus benchmark data for the weakness family |
| L7 | Property-based testing | Generated tests check a stated property across large input spaces | Properties, generators, seeds, results |
| L8 | Adversarial testing | Humans or tools attempt to defeat the control | Test plan, findings, retest evidence |
| L9 | Runtime monitoring | Violations are detected in operation | Telemetry, alerts, response records |
| L10 | External or manual evaluation only | Only review or independent assessment can judge it | Review records, independent reports |

Lower numbers are stronger. A level is always paired with a scope. "L1 for CWE-89"
without a scope is not a valid claim in this model. Levels compose: a strong claim at
L1 needs an L5 gate and L6 scan as the evidence that keeps it true over time.

### 3.2 Claim structure

Every assurance statement derived from this work should have this shape:

> Within *scope*, *weakness* is *level* because *mechanism*, as shown by *evidence at
> repo@commit:path*, except for *known bypasses*, leaving *residual risk*.

The proposed amendment in REC-SBC-002 asks the Standard to require this structure.

## 4. Current-state evidence relevant to construction rules

| Item | Observation | Location | Bearing |
|---|---|---|---|
| Limen binding policy | Text bindings always `textContent`; event handlers, `style`, `srcdoc` and dangerous elements refused at page start; URL attributes limited to `http`, `https`, `mailto`, `tel` or relative after browser-equivalent parsing; diagnostics never carry values | `limen@743cdb9b:docs/29-binding-security.md`, `src/kernel/binding-policy.ts` | Component evidence for SEC-UI-001 and SEC-UI-002 |
| Limen strict CSP smoke test | Kernel and F#, C# and Rust WebAssembly guests run under `require-trusted-types-for 'script'; trusted-types 'none'` with zero violations in Chromium; guests need `'wasm-unsafe-eval'`; runs in CI | `limen@743cdb9b:scripts/smoke-security.ts`, `.github/workflows/ci.yml` | Strongest XSS component evidence; Chromium only |
| Limen F# projects | `--warnaserror:25`, `--warnon:1182`, several with `--reflectionfree` | `limen@743cdb9b:libraries/fsharp/*/*.fsproj` | FS0025 as error at component level |
| Forma workflow component | `this.#root.innerHTML = reply.html` with a comment that the engine escapes text and attributes | `forma@c8f40b4c:packages/workflow/src/forma-workflow.js` line 127 | Counter-evidence for SEC-UI-001/002 |
| Strata architecture check | Script fails if the semantic tier references packages; only `Strata.Host.Postgres` references Npgsql | `strata@c6a384ec:scripts/check-semantic-architecture.sh`, `src/Strata.Host.Postgres/Strata.Host.Postgres.fsproj` | Pattern for an L3/L5 data-access restriction |
| Strata dynamic DDL | Local `quoteIdent` and `quoteName` helpers; `sprintf` composition of DDL; shadow schema names from GUIDs | `strata@c6a384ec:src/Strata.Host.Postgres/ReferenceData.fs`, `src/Strata.Application/SchemaDiff/PostgresDdl.fs` | Trusted infrastructure inside the scope of SEC-DB-002 |
| Strata RLS modeling | Catalog queries model RLS policies; reports tables with RLS on and no policies; notes default `PUBLIC` EXECUTE on functions | `strata@c6a384ec:src/Strata.Host.Postgres/CatalogQueries.fs` | Basis for SEC-DB-003 gates |
| Strata compiler settings | `TreatWarningsAsErrors`, `WarningLevel 5`, Release default, deterministic | `strata@c6a384ec:Directory.Build.props` | Partial baseline |
| Strata runtime | `net8.0` hosts, `global.json` SDK 8.0.0; Npgsql 8.0.5; `pgsqlparser` 1.0.0 | `strata@c6a384ec:global.json`, project files | Out-of-support runtime; native code status of parser unknown |
| Ordo build | `Nullable` enable, `TreatWarningsAsErrors`, comment that FS0025 stays an error, `net8.0` | `ordo@db6d39ed:Directory.Build.props` | Partial baseline; out-of-support runtime |
| Praxis | CI validation workflows, agent provenance, `TreatWarningsAsErrors`, `net10.0` | `praxis@12bf9951:Directory.Build.props`, `.github/workflows/` | Candidate gate and provenance host; no security gates found |
| Tutela | Security engineering model (asset to release posture), F# and Python tooling | `tutela@476dc682:README.md` | Candidate rule registry owner |
| Unsafe and P/Invoke | Text search found no `NativePtr`, `stackalloc`, `DllImport`, `LibraryImport` or `Marshal` use in Strata, Tutela, Ordo or Praxis sources | Search only | Not IL proof; dependencies not examined |

## 5. Principle-by-principle analysis

Each subsection gives the principle, the mechanism that could enforce it, the strongest
achievable level and scope, bypasses and limits, and the evidence needed. Status for
all is `proposed-target-state`.

### 5.1 No dynamically constructed SQL; all access through Strata; mandatory parameterization (SEC-DB-001)

- **Mechanism.** Application projects never reference Npgsql or ADO.NET command
  types. A Strata runtime interface accepts only precompiled, named query definitions
  with typed parameters bound by the driver. A reference gate and an IL scan of every
  shipped assembly enforce the absence.
- **Strongest achievable.** L1 for CWE-89 within application assemblies; L5 to L8 for
  database routines, migrations and tooling.
- **Bypasses and limits.**
  - The interface does not exist yet (finding 4). Until it does, SEC-DB-001 has no
    implementation path.
  - Identifiers cannot be parameters. PostgreSQL requires textual insertion of table and
    column names and of values in utility statements. Any feature that needs dynamic
    sorting or column choice must map user choices to a closed set of identifiers in F#,
    never pass strings.
  - PL/pgSQL `EXECUTE` with concatenation or `format('%s')` reintroduces injection inside
    the trusted boundary. Second-order injection arises when stored data is later used in
    dynamic DDL or `EXECUTE`.
  - Migrations, administrative SQL and reporting tools run with broader privileges.
  - Type providers that generate SQL at compile time (for example SQL type providers)
    are a different construction path that needs its own review.
  - Strata's own DDL generation must be tested as trusted infrastructure, including
    identifier quoting of every user-declared name.
- **Evidence.** IL reference scan report per build; Strata API listing proving no raw-SQL
  entry point; catalog inventory of `EXECUTE` and `SECURITY DEFINER` routines with
  reviewed allowlist (SEC-DB-002); negative build tests that add each bypass.

### 5.2 No user-supplied HTML; contextually safe rendering (SEC-UI-001)

- **Mechanism.** Inputs are plain text or structured data. Output reaches the DOM only
  through Limen bindings, which write text with `textContent`, refuse dangerous targets
  and scheme-check URLs after browser-equivalent normalization.
- **Strongest achievable.** L3 for CWE-79 within Limen-rendered pages served under the
  strict CSP, backed by L5 (smoke test as a gate) and L9 (CSP violation reports).
- **Bypasses and limits.**
  - No HTML input does not eliminate XSS (the Standard says so). Values rendered into
    URL, attribute, CSS and script contexts each need their own rule; Limen covers URL
    and attribute contexts and refuses style and script targets.
  - Component libraries with their own DOM writes (Forma finding).
  - Non-browser renderers: emails, PDF via Folio, CSV and spreadsheet exports (CWE-1236),
    and log viewers.
  - DOM clobbering needs only `id` or `name`; Limen's general `setAttribute` category
    appears to include them (REC-SBC-009 asks Limen to evaluate this).
  - CSS injection through `class` values or attribute selectors can exfiltrate data
    without script; Limen refuses `data-bind-style` but not `class`.
  - `javascript:` and other schemes: Limen allows only listed schemes, but same-scheme
    redirects to other hosts remain an open redirect concern (CWE-601).
- **Evidence.** Smoke tests per product page in CI; bundle scan for HTML-string sinks;
  payload corpus covering URL, attribute, DOM and CSS contexts; CSP reports.

### 5.3 No application-authored JavaScript outside Limen (SEC-UI-002)

- **Mechanism.** Application logic is F# compiled to WebAssembly or runs server side.
  The only JavaScript is the Limen kernel. CSP `script-src 'self'` and Trusted Types with
  no policy prevent other script from running in conforming browsers.
- **Strongest achievable.** L3 with L5 bundle inventory and L9 CSP reporting.
- **Bypasses and limits.** .NET WebAssembly guests require `'wasm-unsafe-eval'`, which
  allows WebAssembly compilation but not JavaScript `eval`. Trusted Types reached
  Baseline only in February 2026, so older browsers ignore the directive. The .NET
  runtime's own JavaScript glue and any marshalling files (Limen notes a small C#
  `[JSExport]` file) are JavaScript or interop not authored as application logic but
  inside the trust boundary. Third-party analytics, support chat or payment widgets
  would breach the rule and must be refused or isolated in separate origins.
- **Evidence.** Bundle inventory with hashes; CSP header conformance; third-party script
  inventory that is empty or approved.

### 5.4 F# as the application language; managed memory and bounds checking; no unsafe memory operations; restricted native interop (SEC-LANG-001)

- **Mechanism.** Verifiable managed IL with array bounds checks and garbage collection.
  F# reports FS0009 for constructs that may produce unverifiable IL (pointer operations
  through `NativePtr`, `fixed`, `stackalloc`); with warnings as errors and no
  suppression, these fail the build. Proposed SEC-MEM-001 adds an IL scan for
  `System.Runtime.CompilerServices.Unsafe`, `MemoryMarshal` reinterpretation,
  `DllImport`, `LibraryImport`, `NativeLibrary`, `Marshal` and function pointers.
- **Strongest achievable.** L1 for CWE-787, CWE-125, CWE-120, CWE-121, CWE-122,
  CWE-416 and CWE-843 within verifiable application assemblies.
- **Bypasses and limits.**
  - Memory corruption remains possible in CoreCLR, the JIT, base library native shims,
    the WebAssembly runtime, and native libraries brought by dependencies. These are
    addressed by patch cadence and SCA, not construction.
  - Running an out-of-support runtime voids the patch premise (finding 7).
  - `Span<T>` and `MemoryMarshal` can reinterpret memory without `unsafe` syntax in some
    APIs; ArrayPool buffers returned while still referenced produce data exposure
    (a managed analog of use after free).
  - A C# helper project with `AllowUnsafeBlocks` bypasses F# rules.
  - Memory safety does not prevent denial of service, arithmetic errors or authorization
    flaws (the Standard states this).
- **Evidence.** Effective compiler options; IL verification report; IL reference scan
  over all shipped assemblies; native dependency inventory; runtime version per release.

### 5.5 Exhaustive security-sensitive pattern matching; FS0025 as error (SEC-LANG-002)

- **Mechanism.** Security-relevant decisions are unions; FS0025 as error forces every
  match to handle every case, so adding a case forces every decision site to change.
- **Strongest achievable.** L4 for CWE-478 and the A10:2025 family within F# code;
  L1 for CWE-484 (F# has no fall-through).
- **Bypasses and limits.** Wildcard (`_`) cases compile and silently absorb new cases;
  `when` guards can make matches incomplete in ways the compiler accepts with a catch-all;
  matches over strings, integers or .NET enums are rarely exhaustive in a meaningful way;
  FS0025 must be an error in every project (Limen and Ordo do this, the Standard does not
  say how). A proposed analyzer rule bans wildcard cases on unions annotated as
  security-sensitive (SEC-LANG-003).
- **Evidence.** Binary log extract of effective options; suppression inventory; analyzer
  results for wildcard use on annotated unions.

### 5.6 Explicit domain states

- **Mechanism.** Workflow states (grant requested, approved, disbursed, reversed) are
  union cases, and transition functions are the only producers of successor states, so
  illegal transitions do not type-check. Ordo's state-directed method is a candidate.
- **Strongest achievable.** L2 for CWE-841 within the domain model; L3 plus L7 for
  concurrency classes (CWE-362, CWE-367, CWE-837) because type-level legality does not
  prevent two valid transitions racing on the same record.
- **Bypasses and limits.** Persistence that writes state columns directly; READ
  COMMITTED anomalies; retries without idempotency keys; external effects before commit.
  SEC-STATE-001 adds idempotency keys under unique constraints and concurrency control.
- **Evidence.** State models; property-based and model-based tests; concurrency stress
  tests; constraint inventory.

### 5.7 Validated domain types with private constructors

- **Mechanism.** Smart constructors validate after canonicalization; private
  constructors or signature files prevent construction elsewhere.
- **Strongest achievable.** L2 for CWE-20, CWE-1284, CWE-1286, CWE-1287 within domain
  modules.
- **Bypasses and limits.** Reflection-based serializers can construct F# records
  without calling smart constructors and can leave reference fields null; `CLIMutable`
  adds setters; `Unchecked.defaultof` and `Array.zeroCreate` create default values;
  validation rules may be wrong. System.Text.Json does not natively handle F# unions in
  the shape F# developers expect, so a converter library or hand-written decoders are
  needed, which is a dependency decision under SEC-SUPPLY-001.
- **Evidence.** Visibility review; decoder property tests including null and missing
  fields (SEC-NULL-001); serializer configuration tests.

### 5.8 No arbitrary code evaluation (SEC-EXEC-001)

- **Mechanism.** IL scan bans FSI and FSharp.Compiler.Service hosting,
  `System.Reflection.Emit`, `Assembly.Load*`, `AssemblyLoadContext`, LINQ expression
  compilation, `Activator.CreateInstance` and `Type.GetType` by string name, and
  `System.Diagnostics.Process` (SEC-EXEC-002).
- **Strongest achievable.** L1 for CWE-94, CWE-95, CWE-470, CWE-913, CWE-78 and CWE-77
  within application runtime code.
- **Bypasses and limits.** Many libraries use Reflection.Emit or expression compilation
  internally (serializers, dependency injection, mocking, proxies). F# quotations are
  data until a third-party evaluator compiles them. Compile-time execution (type
  providers, MSBuild targets in packages, analyzers) is a separate path covered by
  SEC-BUILD-001. CI workflows that interpolate untrusted pull request text into shell
  steps are code injection outside the runtime scope.
- **Evidence.** IL scan including transitive assemblies with an exception allowlist;
  negative build tests.

### 5.9 No unrestricted deserialization (SEC-DATA-001)

- **Mechanism.** DTO decoding with no type metadata; polymorphism only through closed,
  registered discriminators; banned packages and settings.
- **Strongest achievable.** L1 for CWE-502 on .NET 9 or later without the compatibility
  package; L2 for CWE-915 (mass assignment) through explicit command types.
- **Bypasses and limits.** Adding `System.Runtime.Serialization.Formatters` restores
  BinaryFormatter with its risks. Newtonsoft with `TypeNameHandling` other than `None`.
  System.Text.Json's `JsonUnknownDerivedTypeHandling` fallbacks and
  `AllowOutOfOrderMetadataProperties` (documented over-buffering risk). Custom converters
  that create types by name. Queue, cache and file formats chosen later.
- **Evidence.** Dependency graph proof; IL scan for settings; decoder rejection tests.

### 5.10 No custom cryptography (SEC-CRYPTO-001)

- **Mechanism.** Approved facade over platform cryptography and a managed key service.
- **Strongest achievable.** L3 within the facade; L5 for banned algorithm use
  (SEC-CRYPTO-002).
- **Bypasses and limits.** Correct primitives misused (ECB, static IVs, PKCS#1 v1.5
  encryption, `System.Random` for tokens, non-constant-time comparison); certificate
  validation callbacks that accept everything; crypto inside dependencies; TLS at
  infrastructure. Platform library CVEs. Conventional SAST already detects most of
  these, so architecture is `comparable` here.

### 5.11 No unapproved dependencies (SEC-SUPPLY-001)

- **Mechanism.** Allowlisted packages, lock files, approved feeds, SBOM, SCA as a gate.
- **Strongest achievable.** L5. Construction cannot establish that an approved package
  is free of malicious or vulnerable code (CWE-506 is L10).
- **Bypasses and limits.** Transitive code runs with the application's privileges and
  can contain any banned capability; the IL scans in 5.4 and 5.8 should cover transitive
  assemblies for this reason. Build-time code execution: NuGet imports package
  `build` and `buildTransitive` props and targets into consumers; F# type providers run
  inside the compiler against files, URLs or connection strings; C# source generators
  and Roslyn analyzers run in C# helper projects. Unpinned CI actions are dependencies too.

### 5.12 Explicit server-side authorization (SEC-AUTH-001)

- **Mechanism.** SEC-AUTH-002 makes each state-changing operation require an
  `Authorized` command value constructible only by the policy module.
- **Strongest achievable.** L2 for CWE-862 (a missing check does not compile); L7 for
  CWE-863 (wrong policy is found only by testing against a specification), with L8 and
  L10 as further evidence.
- **Bypasses and limits.** Background jobs, support consoles and administrative tools
  that call repositories directly; reflection or deserialization constructing the
  decision type; caches keyed without tenant or principal; client-side checks. Business
  logic flaws in policy are the dominant residual risk and are the right focus for the
  external penetration test (REC-SBC-017).

### 5.13 Tenant isolation by construction

- **Mechanism.** Two independent layers: a `TenantContext` type required by every data
  interface (SEC-TENANT-001), and PostgreSQL row-level security forced for the
  application role (SEC-DB-003).
- **Strongest achievable.** L2 for CWE-639 and CWE-668 within interfaces requiring the
  tenant type, with database enforcement as a second layer.
- **Bypasses and limits.** Superuser, owner and `BYPASSRLS` roles bypass row security;
  referential integrity checks always bypass it (covert channel); session-level
  `SET` on pooled connections can carry a tenant into the next request, so tenant
  context should use `set_config(..., true)` scoped to the transaction; `SECURITY
  DEFINER` functions run as their owner; caches, object storage, search indexes,
  queues, exports and analytics are outside row security.
- **Evidence.** Catalog gate output; role report; cross-tenant property and adversarial
  tests across every store.

### 5.14 Mandatory evidence provenance

- **Mechanism.** SEC-EVID-001 requires every evidence artifact to carry repository,
  commit, artifact hash, tool and rule versions, scope, time and actor, signed or hash
  chained; runtime audit history is hash chained and verified.
- **Strongest achievable.** L5 for evidence completeness; L3 for audit emission when
  the transition engine emits audit events automatically.
- **Bypasses and limits.** Direct writes outside the transition engine; administrators
  able to delete audit records; signing key compromise; authentic evidence of the wrong
  property. Praxis provenance covers change evidence, not runtime audit.

## 6. Cross-cutting bypasses and limits

### 6.1 Trusted infrastructure boundaries

| Boundary | Hazard | Proposed control |
|---|---|---|
| PL/pgSQL `EXECUTE` | No substitution; concatenation and `%s` reintroduce injection | SEC-DB-002 |
| `SECURITY DEFINER` routines | Run as owner; `search_path` hijack through `pg_temp`; default `PUBLIC` execute | SEC-DB-002 |
| Row-level security | Owners, superusers, `BYPASSRLS` bypass; RI checks bypass; policies can be missing on new tables | SEC-DB-003 |
| Connection pooling | Session settings leak between requests | SEC-DB-003 (transaction-local settings) |
| Migrations and admin access | Privileged roles; ad hoc SQL | SEC-DB-004 |
| Strata itself | Generates DDL dynamically with quoting helpers | Treat as trusted infrastructure under test (REC-SBC-005) |

### 6.2 Third-party dependencies and transitive code

Transitive packages are part of the executable and can contain unsafe code, P/Invoke,
Reflection.Emit, process launching, their own deserialization and their own
cryptography. The capability scans in SEC-MEM-001 and SEC-EXEC-002 must run over the
full shipped assembly set, with a reviewed exception list. Native assets in package
`runtimes` folders need an inventory (REC-SBC-018 for Strata's parser dependency).

### 6.3 Compiler behavior

- FS0025 (incomplete match) is a warning unless promoted; wildcard cases defeat it.
- Useful warnings are opt-in (1182 unused variables, 3559 type inferred as `obj`, 3579
  untyped interpolation, 3388, 3389 and 3395 implicit conversions), and the F#
  documentation states only the last `WarnOn` property is used, so baselines can regress
  silently. SEC-LANG-003 reads effective options from binary logs.
- Null: F# types exclude null in normal use, but interop, `Unchecked.defaultof`,
  `Array.zeroCreate` and reflection-based deserializers introduce it; nullness checking is
  off by default and reports warnings (SEC-NULL-001).
- Integer overflow is unchecked by default; `--checked+` or the `Checked` module raise
  `OverflowException` (SEC-NUM-002).
- Reflection bypasses private constructors and module visibility.
- `--reflectionfree` changes structural formatting; redaction designs that rely on
  `%A` or `ToString` must be tested under the chosen option.
- Type providers execute during compilation; C# source generators and Roslyn analyzers
  run only in C# projects, so a C# companion project (for example for System.Text.Json
  source generation) adds a build-time execution surface and a second language.
- MSBuild props and targets in packages execute during build (SEC-BUILD-001).

### 6.4 Runtime limitations

- Runtime and native library CVEs: construction rules do not help; patch cadence and
  supported versions do (SEC-RUNTIME-001; .NET 8 and 9 out of support since 2026-11-10).
- Regular expressions: default timeout infinite; use `NonBacktracking` or timeouts, and
  never accept patterns from users (SEC-REGEX-001).
- Integer overflow: unchecked by default in F#.
- Money: `decimal` overflow always throws, which is the desired failure; `float` and
  `double` cannot represent most decimal fractions; `Math.Round` defaults to banker's
  rounding unless a `MidpointRounding` mode is given (SEC-NUM-001).
- Stack overflow: cannot be caught and terminates the process; recursive decoders need
  depth limits (SEC-RES-001).
- Unbounded allocation: managed memory makes exhaustion a denial of service rather than
  corruption, but it is still rank 25 in the 2025 Top 25 (SEC-RES-001).

### 6.5 Browser limitations

- CSP and Trusted Types work only in browsers that enforce them; Trusted Types became
  Baseline in February 2026.
- `'wasm-unsafe-eval'` is needed for .NET WebAssembly.
- Third-party scripts would break SEC-UI-002 and are effectively prohibited.
- DOM clobbering needs no script; restrictive `script-src` does not stop clobbering that
  abuses existing code (OWASP).
- URL schemes: Limen parses URLs as the browser does before checking the scheme; other
  renderers (email, PDF, exports) need their own checks.
- CSS injection through class or attribute selectors can leak data without script.

### 6.6 AI agent authored code

AI agents write plausible code quickly and can satisfy tests while weakening a control
(for example adding a wildcard match case, a `#nowarn`, a raw SQL escape hatch, or an
exception record). Construction rules are especially valuable here because they bind
the artifact regardless of author. The residual risk is that an agent changes the gate
itself or the exception registry. SEC-AI-001 requires provenance, identical gates,
human review of security-sensitive paths and human approval for gate configuration
changes. Runtime AI features are a separate concern: model output is untrusted input
and may act only through typed, authorized commands (CWE-1426, CWE-1427).

## 7. CWE architectural prevention matrix

The canonical matrix is `security-by-construction/cwe-architectural-prevention-matrix.csv`
(353 rows, 25 columns). The generated summary is
`security-by-construction/CWE-ARCHITECTURAL-PREVENTION-MATRIX.md` (DD-SBC-002).

Coverage: all 25 entries of the 2025 Top 25; every weakness in the CWE 5.0 view of
OWASP Top 10 2025 RC1 (246 weaknesses plus grouping-level CWE-16); the weaknesses of
the OWASP Top 10 2021 view; and 79 additions for financial web applications.

Strongest achievable level distribution (targets): L1 32, L2 89, L3 178, L4 18, L5 22,
L7 2, L9 1, L10 11. The concentration at L2 and L3 reflects that most classes can be
moved behind types or restricted interfaces but not eliminated.

Selected rows:

| CWE | Top 25 rank | Strongest achievable | Scope summary | Scanning | Architecture vs scanning |
|---|---|---|---|---|---|
| CWE-79 | 1 | L3 | Limen-rendered pages under strict CSP and Trusted Types | partial | beyond |
| CWE-89 | 2 | L1 | Application assemblies with no driver references and a Strata interface without raw SQL | partial | beyond |
| CWE-352 | 3 | L3 | Routes registered through a central anti-forgery check | partial | beyond |
| CWE-862 | 4 | L2 | Operations whose signatures require an `Authorized` value | no | beyond |
| CWE-787 | 5 | L1 | Verifiable managed application IL; excludes runtime and native code | partial | beyond |
| CWE-502 | 15 | L1 | .NET 9 or later without the compatibility package; DTO decoding without type metadata | yes | beyond |
| CWE-863 | 17 | L7 | Policy correctness checked against a specification | no | beyond |
| CWE-639 | 24 | L2 | Interfaces requiring `TenantContext` plus forced RLS | no | beyond |
| CWE-770 | 25 | L3 | Bounded input types and server limits | partial | complementary |
| CWE-190 | n/a | L4 | Domain assemblies compiled with overflow checks | partial | beyond |
| CWE-1339 | n/a | L2 | Money as a decimal-backed type | partial | beyond |
| CWE-837 | n/a | L3 | Idempotency keys under unique constraints | no | beyond |
| CWE-1104 | n/a | L5 | Allowlisted, locked dependencies with SCA gate | yes | comparable |
| CWE-798 | n/a | L5 | Secret scanning gate and managed secrets | yes | comparable |

## 8. Where the architecture exceeds conventional scanning, and where it gives less

### 8.1 Beyond scanning

- **Absence of capability.** A scanner reports what it found; it never reports that a
  capability is absent. An IL scan proving no reference to Npgsql command types,
  `Process`, `Reflection.Emit` or `BinaryFormatter` in the shipped artifact establishes a
  property no SAST report can.
- **Type-level guarantees.** Missing authorization, unhandled states, unvalidated
  domain values and money arithmetic errors become compile errors. Scanners have no
  policy or domain model to compare against.
- **Business and tenancy invariants.** Tenant isolation, idempotent disbursement,
  balanced journals and valid workflow transitions are not in any scanner's rule set.
- **F# coverage gap.** Where common SAST tools have limited or unverified F# support,
  structural rules may be the only systematic control.

### 8.2 Less than scanning, or not addressed

- **Known vulnerable components and runtime CVEs.** SCA is the primary control;
  construction rules do not detect a vulnerable version.
- **Secrets.** Secret scanners are mature; architecture contributes managed identity but
  not detection.
- **Transport, headers, cookies and infrastructure configuration.** DAST and
  configuration scanners find these directly; construction applies only if configuration
  is generated by gated code.
- **Code outside the F# scope.** Limen's TypeScript kernel, any C# helper projects,
  CI scripts, SQL routines and infrastructure code are outside F# compiler guarantees
  and need conventional scanning.
- **Policy correctness.** Types guarantee that a decision exists, not that it is right.
- **Regression of the rules themselves.** If gates are misconfigured, the architecture
  silently stops providing assurance; scanners at least produce independent output.
  This is why L6 analysis and L8 adversarial testing remain in the stack even for L1
  targets.

Conventional scanning should therefore remain in place for SCA, secrets, configuration,
non-F# code and DAST, while construction rules carry the classes scanners do not model.
Whether this reduces scanning license or assessment cost is not established; the
Standard itself says not to assume savings before measurement.

## 9. Proposed additional construction rules (proposals only)

`security-by-construction/proposed-construction-rules.jsonl` contains 28 rules. **They
are proposals for `echelon-organization-administration` and are not adopted Echelon
rules.** Each record carries `status: proposed` and a `proposal_label` saying so.

| ID | Title | Target level |
|---|---|---|
| SEC-DB-002 | Dynamic SQL discipline inside PostgreSQL routines | L5 |
| SEC-DB-003 | Database-enforced tenant isolation | L5 |
| SEC-DB-004 | Privileged database paths and migrations | L5 |
| SEC-NUM-001 | Money representation and rounding | L2 |
| SEC-NUM-002 | Overflow-checked integer arithmetic | L4 |
| SEC-REGEX-001 | Regular expression safety | L5 |
| SEC-NULL-001 | Nullness discipline | L4 |
| SEC-LANG-003 | F# compiler diagnostic baseline | L4 |
| SEC-MEM-001 | Unsafe code and native interop prohibition | L5 |
| SEC-EXEC-002 | Banned dynamic execution capability list | L5 |
| SEC-BUILD-001 | Control code that executes during the build | L5 |
| SEC-RUNTIME-001 | Supported runtime and patch currency | L5 |
| SEC-DESER-001 | Deserialization contracts | L5 |
| SEC-RES-001 | Bounded resource consumption | L3 |
| SEC-UI-003 | Browser hardening baseline including component libraries | L3 |
| SEC-AUTH-002 | Authorization by construction | L2 |
| SEC-AUTH-003 | Authentication by default and approved identity | L3 |
| SEC-TENANT-001 | Tenant isolation across all stores | L2 |
| SEC-STATE-001 | Explicit domain states and idempotent effects | L2 |
| SEC-EVID-001 | Mandatory evidence provenance | L5 |
| SEC-AI-001 | AI-authored code and AI runtime authority | L5 |
| SEC-ERR-001 | Fail-closed exceptional condition handling | L4 |
| SEC-LOG-001 | Structured logging and sensitive data types | L2 |
| SEC-EGRESS-001 | Outbound request control | L3 |
| SEC-FILE-001 | Uploads and file handling | L3 |
| SEC-CRYPTO-002 | Banned cryptographic algorithms and APIs | L5 |
| SEC-CONFIG-001 | Secure configuration as code | L5 |
| SEC-DATA-002 | Canonicalize, validate and encode at single boundaries | L2 |

## 10. Recommendations

Eighteen recommendations are recorded in
`recommendations/security-by-construction-recommendations.jsonl` (REC-SBC-001 to
REC-SBC-018). P0: REC-SBC-004 (decide and build the Strata typed query interface that
SEC-DB-001 assumes). P1: adopt or reject the proposals; require level, scope and evidence
for claims; correct system ownership in the Standard; Strata catalog gates; Strata
runtime upgrade; remove Forma's `innerHTML` sink; Tutela as rule registry; Praxis gates
on compiled artifacts; a shared F# compiler baseline; Unbound construction requirements.

## 11. Objections and contradictory evidence (preserved)

- **"F# and managed memory eliminate memory safety bugs."** Only for verifiable
  application IL. The runtime, JIT, native dependencies and an out-of-support runtime are
  outside the claim, and two Echelon repositories currently target an out-of-support
  runtime.
- **"No HTML input means no XSS."** The Standard rejects this, and Forma's `innerHTML`
  use shows that rendering code, not input policy, determines the risk.
- **"Strata provides typed parameterized access."** Not at the reviewed commit; the
  brief already flags this.
- **"Architecture can replace scanners."** Not for SCA, secrets, configuration,
  non-F# code or DAST; and the F# fixture corpus needed to compare scanners has not
  been built.
- **"Types prove authorization."** Types prove a decision exists. Whether the decision
  is correct is a testing and review question.
- **Cost of the model.** IL scans, binary log extraction, catalog gates and property
  test suites are real engineering costs; the Standard asks that costs be measured, and
  none has been.
- **Scale risk.** A 353-row matrix with family-level defaults can create an impression of
  precision it does not have. Family text is shared; per-row overrides exist only where
  noted. Readers should rely on the cited mechanisms, not on the row count.

## 12. Open questions

| ID | Question | Blocking |
|---|---|---|
| OQ-SBC-01 | Do the final OWASP Top 10 2025 CWE mappings differ from the RC1 view (CWE-1450) shipped in CWE 5.0? | No |
| OQ-SBC-02 | Will Strata provide a runtime query interface, and what API shape prevents raw SQL? | Yes, for SEC-DB-001 |
| OQ-SBC-03 | Which SAST tools are under consideration, and what is their measured F# detection by family? | Yes, for scanning comparisons |
| OQ-SBC-04 | Does `pgsqlparser` 1.0.0 load native code? | No |
| OQ-SBC-05 | Will Unbound use ASP.NET Core, and which identity provider? Several authentication rows depend on it | No |
| OQ-SBC-06 | Should Limen refuse engine-supplied `id` and `name` values? | No |
| OQ-SBC-07 | Which browsers must Unbound support, and what is the fallback where Trusted Types are not enforced? | No |
| OQ-SBC-08 | Who owns the rule registry if not Aegis (Tutela is recommended)? | Yes, for adoption |
| OQ-SBC-09 | How will reflection-based JSON decoding of F# records be prevented from producing null fields, and is a converter dependency acceptable? | No |

These questions are recorded here rather than in `research/open-questions.jsonl`
because this task owns only the listed output files.

## 13. Sources

All accessed 2026-11-25.

- MITRE CWE, XML download: https://cwe.mitre.org/data/xml/cwec_latest.xml.zip
- MITRE CWE, downloads page: https://cwe.mitre.org/data/index.html
- MITRE CWE, 2026 news archive (CWE 5.0 release): https://cwe.mitre.org/news/archives/news2026.html
- MITRE CWE, 2025 CWE Top 25: https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html
- OWASP Top 10 2025: https://top10.owasp.org/2025
- OWASP DOM Clobbering Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/DOM_Clobbering_Prevention_Cheat_Sheet.html
- Microsoft Learn, BinaryFormatter migration guide: https://learn.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-migration-guide/
- Microsoft Learn, System.Text.Json polymorphism: https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/polymorphism
- Microsoft Learn, System.Text.Json source generation: https://learn.microsoft.com/dotnet/standard/serialization/system-text-json/source-generation
- Microsoft Learn, F# compiler options: https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/compiler-options
- Microsoft Learn, F# null values: https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/values/null-values
- Microsoft Learn, F# type providers: https://learn.microsoft.com/en-us/dotnet/fsharp/tutorials/type-providers/
- FSharp.Core Checked module: https://fsharp.github.io/fsharp-core-docs/reference/fsharp-core-operators-checked.html
- Microsoft Learn, checked and unchecked statements: https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/checked-and-unchecked
- Microsoft Learn, StackOverflowException: https://learn.microsoft.com/en-us/dotnet/api/system.stackoverflowexception
- Microsoft Learn, regular expression best practices: https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-regex
- Microsoft Learn, MSBuild props and targets in a package: https://learn.microsoft.com/en-us/nuget/concepts/msbuild-props-and-targets
- Microsoft, .NET support policy: https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core
- Newtonsoft.Json TypeNameHandling: https://www.newtonsoft.com/json/help/html/T_Newtonsoft_Json_TypeNameHandling.htm
- PostgreSQL row security policies: https://www.postgresql.org/docs/current/ddl-rowsecurity.html
- PostgreSQL PL/pgSQL basic statements: https://www.postgresql.org/docs/current/plpgsql-statements.html
- PostgreSQL CREATE FUNCTION: https://www.postgresql.org/docs/current/sql-createfunction.html
- MDN Trusted Types API: https://developer.mozilla.org/en-US/docs/Web/API/Trusted_Types_API
- FSharp.Analyzers.SDK: https://github.com/ionide/FSharp.Analyzers.SDK
