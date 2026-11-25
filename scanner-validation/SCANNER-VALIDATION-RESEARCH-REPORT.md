---
id: DD-SCN-001
title: Automated security analysis, scanner validation and F# coverage research report
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [due-diligence, sast, dast, sca, fsharp, scanner-validation, benchmarking, tutela]
related_documents:
  - sources/assurance-testing.jsonl
  - external-assurance/EXTERNAL-ASSURANCE-REQUIREMENTS-MATRIX.md
  - cost-avoidance/PENETRATION-TESTING-COST-REDUCTION-STRATEGY.md
  - cost-avoidance/COMPLIANCE-COST-AVOIDANCE-REPORT.md
---

# Automated security analysis, scanner validation and F# coverage

## 1. Scope, method and status

This report answers four questions for Echelon Foundry and Unbound:

1. Which mature open-source tools cover each security testing category, under what
   license, and how well they cover F# and .NET.
2. Whether scanners need accreditation, what validation programs exist, and whether an
   internally developed scanner is acceptable.
3. How to validate a scanner credibly and publish benchmark results that withstand
   scientific scrutiny.
4. What Echelon-native security analysis architecture to build, and which repository
   should own it.

Method: primary sources fetched on 2026-11-25 (tool repositories, license files,
vendor documentation, NIST, PCI SSC, EUR-Lex, academic papers through Crossref and
abstracts). Each source is recorded in `sources/assurance-testing.jsonl` with
`verified: true` only where the content was read. Internal facts cite
`repository@commit:path`.

Governing internal requirement: the proposed Echelon Secure Construction Standard v0.1
(`echelon-organization-administration@2763e576:policies/security/secure-construction-standard.md`,
`SRC-ECH-SCS-0.1`), section "Scanner validation": reuse mature open-source tools, fill F#
gaps with compiler semantic analysis, benchmark with SAMATE/SARD/SATE and OWASP Benchmark
where applicable, build F# fixtures and independent holdouts, measure precision and recall
by weakness class, publish methodology and limitations, and never present benchmarking as
accreditation. Nothing described as a target in this report is implemented today.

## 2. Executive findings

1. **F# has no mature open-source security SAST.** Semgrep (registry of 50 languages, C#
   GA, no F#), Opengrep (no F# in its language list), CodeQL (no F#; C# extractor only),
   Roslyn .NET analyzers (C# and Visual Basic only) and Security Code Scan (C# and VB.NET)
   do not analyze F# source. Every language-independent layer (SCA, SBOM, secrets, IaC,
   containers, DAST, API fuzzing, AI probing) works for F# projects unchanged.
2. **The F# gap is narrow and well defined.** It is source-level semantic detection of
   dangerous API use and data flow in F# code: dynamic SQL and Strata bypass
   (SEC-DB-001), raw HTML rendering (SEC-UI-001), dynamic code execution and process
   launch (SEC-EXEC-001), unsafe and native interop (SEC-LANG-001), unrestricted
   deserialization (SEC-DATA-001), and cryptographic API misuse (SEC-CRYPTO-001).
3. **The right foundation exists.** `FSharp.Analyzers.SDK` (MIT) gives analyzers the F#
   compiler's parse results, check results and typed tree, and its CLI writes SARIF
   (`SRC-FSHARP-ANALYZERS`, read from source). G-Research's analyzer pack (Apache-2.0)
   proves the model in production but contains no security rules.
4. **There is no general accreditation for scanners.** NIST SAMATE and SATE explicitly
   are not certification or ranking programs; SATE V says its analysis "should NOT be
   used as a basis for rating or choosing tools" (`SRC-NIST-SATE`). Approval regimes exist
   only for named activities: PCI ASV scanning, FedRAMP 3PAO testing, CREST/CHECK/CBEST in
   the UK, and DORA TLPT testers in the EU.
5. **Internally developed scanners are acceptable** wherever no named qualified body is
   required, which is most of the SDLC; they are never acceptable as a substitute for an
   ASV scan, a 3PAO test, a CPA attestation or an accredited certification.
6. **Synthetic benchmarks overstate real performance.** Seven Java SAST tools detected
   12.7% of real-world vulnerabilities in one ESEC/FSE 2023 study (`SRC-ACAD-LI-2023`);
   C analyzers missed 47% to 80% of real CVEs in an ISSTA 2022 study
   (`SRC-ACAD-LIPP-2022`). Benchmark publication must include real-world cases, sealed
   holdouts and per-CWE intervals, and must not rank.
7. **Ownership: Tutela, not Aegis.** Dokimos requirements line 118 route security analysis
   to Tutela (`dokimos@6ea8624:requirements/REQUIREMENTS.md`), and Tutela declares itself
   the single owner of security rules, evidence interpretation and release posture
   (`tutela@476dc68:docs/SECURITY-OWNERSHIP.md`). The Standard's proposal that Aegis own
   the rule registry and F# analysis conflicts with both and with Aegis's verified purpose.

## 3. Tool landscape by category

Licenses were read from each repository's LICENSE file on 2026-11-25 unless noted.

| Category | Mature open-source options | License | F# / .NET relevance | Key limits |
|---|---|---|---|---|
| SAST (general) | Semgrep CE engine; Opengrep fork | LGPL-2.1 (both engines); Semgrep-maintained rules under Semgrep Rules License v1.0 | C# GA; no F# | Rules License limits use to internal, non-competing, non-SaaS contexts since 2024-12-13; cross-file analysis documented under commercial Pro engine (Semgrep) |
| SAST (semantic, query) | CodeQL | Proprietary; free only for open-source codebases, research and demonstration; private code requires paid GitHub Advanced Security | C# up to 14; no F# | Not open source; Echelon private repos need a license |
| SAST (.NET compiler) | .NET CA analyzers (Roslyn); Security Code Scan | Roslyn analyzer license not checked in this session; Security Code Scan LGPL-3.0 | C# and VB only | Roslyn analyzers do not run on F# |
| SAST (F#) | FSharp.Analyzers.SDK; G-Research FSharp.Analyzers; FSharpLint; Ionide (editor integration) | MIT; Apache-2.0; MIT; MIT (SDK) | Native F#, typed tree access | No security rule pack exists |
| SCA | OSV-Scanner; Grype; OWASP Dependency-Check | Apache-2.0 (all three) | NuGet lockfiles (`packages.lock.json`, `deps.json`, `packages.config`) supported by OSV-Scanner | Requires lockfiles; advisory data quality varies |
| SBOM | Syft | Apache-2.0 | .NET listed among ecosystems | Metadata driven |
| Secret scanning | Gitleaks; TruffleHog; `tutela scan-secrets` | MIT; AGPL-3.0; PolyForm Noncommercial 1.0.0 (Tutela) | Language independent | Tutela scans current tree only; Gitleaks also scans history; TruffleHog AGPL obligations |
| IaC and containers | Trivy; Checkov | Apache-2.0 | Language independent | Policy coverage varies by provider |
| DAST | ZAP (branded "ZAP by Checkmarx") | Apache-2.0 | Language independent | Weak on authorization and business logic without scripted contexts |
| External exposure | Nuclei with nuclei-templates | MIT; MIT | Language independent | Template driven; not an ASV scan |
| API testing | Schemathesis | MIT | Language independent; needs OpenAPI or GraphQL schema | Robustness and schema conformance, not authorization semantics |
| Authorization testing | No mature general open-source tool located | n/a | Must be Echelon-native: generated negative tests from a policy model | Requires a machine-readable authorization model |
| Financial business logic | No tool located; property-based and model-based testing practice | n/a | Echelon-native invariants (balanced journals, idempotent disbursement, separation of duties) | Only as strong as the invariants written |
| Browser security | ZAP; CSP evaluation; Limen boundary tests | Apache-2.0 | Language independent | Must also inspect generated bundles (SEC-UI-002) |
| AI agent security | garak; PyRIT | Apache-2.0; MIT | Language independent | Generic probes; agent authority abuse requires custom scenarios |
| Supply chain posture | OpenSSF Scorecard; Syft/Grype; OSV | Apache-2.0 | Language independent | Heuristics, not vulnerability proof |

Notes:

- Semgrep rules license: Semgrep announced on 2024-12-13 that Semgrep-maintained rules moved
  to the Semgrep Rules License v1.0, limited to internal, non-competing and non-SaaS
  contexts, and that the engine remains LGPL-2.1 (`SRC-SEMGREP`). Echelon may use the
  rules internally. It must not redistribute them in an Echelon product, or run them as a
  service for others, without checking those terms. Opengrep changes the engine, not the
  terms on Semgrep-maintained rules.
- CodeQL: the CLI license allows use on open-source codebases, academic research and
  demonstration. It prohibits use "in connection with any codebase that is not an Open
  Source Codebase" without a paid GitHub Advanced Security license (`SRC-CODEQL`). Tutela
  records that no Echelon portfolio repository currently runs CodeQL, secret scanning or
  dependency review in CI (`tutela@476dc68:docs/SECURITY-OWNERSHIP.md`).
- Tutela's PolyForm Noncommercial license conflicts with the Standard's stated preference
  for MIT for original public tooling. This is an open question for Echelon, not a
  research finding about the tools.

## 4. F# scanning coverage gap analysis

### 4.1 What each candidate actually covers

| Tool | Analyzes F# source? | Evidence |
|---|---|---|
| Semgrep CE / Code | No | `fsharp` absent from `semgrep-interfaces/lang.json` (50 entries, `csharp` GA, `ocaml` alpha); absent from GA, beta and experimental lists on the supported-languages page |
| Opengrep | No | README language list includes C#, Visual Basic and OCaml, not F# |
| Semgrep generic mode | Text patterns only | Opengrep lists "Generic (ERB, Jinja, etc.)"; any such use on F# would be syntax-unaware grep, not semantic analysis (inference, not tested) |
| CodeQL | No | Supported-languages page lists C# with extensions `.sln`, `.slnx`, `.csproj`, `.cs`, `.cshtml`, `.xaml`; no `.fs` or `.fsproj` |
| Roslyn .NET analyzers (CA rules) | No | Microsoft: analyzers "inspect your C# or Visual Basic code" |
| Security Code Scan | No | README: "Vulnerability Patterns Detector for C# and VB.NET" |
| FSharpLint | Yes (lint) | MIT; style and code quality lint; no security rule set located |
| G-Research FSharp.Analyzers | Yes (typed) | Ten analyzers documented (for example StringAnalyzer, JsonSerializerOptionsAnalyzer, TypedInterpolatedStrings, DisposedBeforeAsyncRun); none documented as security |
| FSharp.Analyzers.SDK | Yes (framework) | `Context` exposes `ParseFileResults`, `CheckFileResults` and `TypedTree: FSharpImplementationFileContents option`; CLI `Report` option writes SARIF via `SarifReport.writeReport`; documented exit codes support CI gating |
| Ionide / FsAutoComplete | Hosts analyzers in editors | SDK README: analyzers are plugins for FSAC and F# editors |
| Commercial SAST with F# | Not assessed | No vendor claim was verified in this session; treat as unknown |

Not evaluated: analyzing compiled IL instead of F# source. IL-level tools could in
principle see calls made by F# code, but no mature open-source IL security analyzer was
verified in this session, and IL analysis loses F# source structure such as pattern
match exhaustiveness. Recorded as an open question.

### 4.2 Gap by Secure Construction rule

| Rule | Language-independent coverage available | F# semantic analysis needed | Gap severity |
|---|---|---|---|
| SEC-DB-001 no dynamic SQL; Strata only | Runtime SQL logging in tests; database permissions | Detect references to raw ADO.NET or other database clients outside the approved interface; detect non-literal command text; detect string building that flows into query APIs | High: no tool does this for F# today |
| SEC-UI-001 no user HTML | DAST (ZAP) for reflected and stored XSS; CSP | Detect raw-HTML rendering functions in whichever F# view library is adopted; inventory needed before rules can be written | High |
| SEC-UI-002 no JS outside Limen | Bundle inspection; CSP; SBOM of scripts | Detect JavaScript interop declarations outside Limen projects | Medium |
| SEC-LANG-001 memory safety | Project file and compiler option checks | Detect native pointer use, address-of operators, platform invoke declarations and unverifiable-code warnings, and require them to be errors | Medium; partly compiler driven (to confirm with fixtures) |
| SEC-LANG-002 exhaustive matching | Compiler: incomplete pattern match warnings promoted to errors | Detect wildcard catch-all cases on security-sensitive union types | Low to medium; compiler does most |
| SEC-EXEC-001 no dynamic code or shell | Runtime sandbox and egress controls | Detect process launch, dynamic assembly loading, reflection emit and F# script evaluation APIs | High |
| SEC-DATA-001 no unrestricted deserialization | Schema validation tests; Schemathesis | Detect unsafe serializer settings (type-name handling, polymorphic binders) and missing size limits | High |
| SEC-CRYPTO-001 no custom crypto or hardcoded secrets | Gitleaks and `tutela scan-secrets` for secrets | Detect weak algorithms, custom primitives and constant keys | Medium |
| SEC-AUTH-001 deny by default | Generated negative tests against running system | Detect endpoints without an authorization declaration, framework specific | Medium; testing matters more than static detection |
| SEC-SUPPLY-001 approved dependencies | OSV-Scanner, Syft/Grype, Scorecard, lockfile enforcement | None | None |

### 4.3 Conclusion on the gap

The gap is not "F# has no security tooling"; it is "F# has no security rule pack and no
data-flow (taint) engine". Pattern-level rules over the typed tree (symbol use of
dangerous APIs, outside approved projects) are cheap to build on the SDK and cover most
of the high-severity rows, because the Standard's strategy is to make unsafe APIs
unavailable rather than to find tainted flows into them. Inter-procedural taint tracking
for F# would be a research-grade investment and should not be started unless structural
restriction proves insufficient.

## 5. Accreditation, validation programs and acceptance of internal scanners

### 5.1 Do scanners require accreditation?

No source located requires a SAST, DAST or SCA tool to be accredited, certified or
approved for general use. Approval regimes attach to specific activities:

| Regime | What is approved | Applies to Echelon? | Source |
|---|---|---|---|
| PCI DSS 11.3.2 ASV | External vulnerability scan solution and company | Only if in PCI scope (not established) | `SRC-PCI-ASV-PROGRAM`, `SRC-PCI-DSS-V4-SAQ-D` |
| PCI DSS 11.4 | Tester must be qualified and organizationally independent; no approval list | Only if in PCI scope | `SRC-PCI-DSS-V4-SAQ-D`, `SRC-PCI-PENTEST-GUIDANCE` |
| FedRAMP | Recognized 3PAO performs penetration testing | Only if FedRAMP pursued | `SRC-FEDRAMP-PENTEST-GUIDANCE` |
| UK CHECK, CREST, CBEST | Companies and individuals for UK public sector, CNI and financial red teaming | No, unless UK markets | `SRC-NCSC-CHECK`, `SRC-CREST`, `SRC-CBEST` |
| DORA TLPT | Testers meeting Art. 27; internal testers only with authority approval | No, unless serving EU financial entities in a TLPT | `SRC-TIBER-EU` |

### 5.2 Validation programs and what they claim

| Program | What it offers | What it does not claim |
|---|---|---|
| NIST SAMATE | Bug classes, reference corpus, tool exposition methodology | No certification or endorsement of tools |
| NIST SARD | Over 450,000 test cases in C, C++, Java, PHP and C#; Juliet C# 1.3 has 28,942 cases; Juliet Java 1.3 has 28,881 | No F# cases; synthetic cases dominate the Juliet suites |
| NIST SATE (V report SP 500-326, 2018; SATE VI workshop 2019) | Methodology for evaluating static analyzers with recall and precision | States it is not a ranking, not a tool testing exercise, and should not be used to choose tools |
| OWASP Benchmark v1.2 | Runnable Java app; 2,740 scored test cases across 11 categories (counted from `expectedresults-1.2.csv`); Python suite also listed; scorecards via BenchmarkUtils | Java and Python only; GPL-2.0; synthetic and tunable |

OWASP Benchmark scoring references Youden's index, which is true positive rate minus false
positive rate (Youden's J equals sensitivity plus specificity minus one). The project page
links to the definition but does not restate the formula; scorecard generation is in
BenchmarkUtils.

### 5.3 When an internally developed scanner is acceptable

Acceptable when all of these hold:

1. No law, standard or contract names a qualified body for that activity (excludes ASV,
   3PAO, TLPT external rotation, CPA attestation, accredited certification).
2. Results are labeled first-party (`assurance_independence: first-party`) and never
   described as independent assurance.
3. The scanner has a published validation report for the exact release (Standard,
   Assurance deliverable 1) with per-weakness recall and precision and known gaps.
4. Where a customer, insurer or auditor will rely on it, their acceptance is obtained in
   writing (Standard, External assurance section).
5. An independent party periodically reviews the scanner's validation (second-party or
   third-party review of methodology and holdout), if Echelon wants auditors to place
   more reliance on it. This is a design option, not a located requirement.

Internal scanners are not acceptable as a replacement for the independent penetration
test planned for Unbound; they are acceptable as evidence that narrows its scope (see
DD-COST-001).

## 6. What credible scanner validation looks like

1. **Explicit claim.** State which rule detects which weakness (CWE), on which language
   constructs and frameworks, under which configuration. Every rule maps to a SEC rule
   identifier and CWE (Standard, Enforcement model).
2. **Three corpora, kept separate.**
   - Development fixtures: vulnerable and safe pairs written by rule authors.
   - Calibration suites: Juliet C# and OWASP Benchmark for the off-the-shelf tools in the
     pipeline (C#, Java, JavaScript), to detect regressions in tool versions and wrappers.
   - Sealed holdout: F# vulnerable and safe cases written by people who do not write rules,
     stored with restricted access, plus real-world cases (historical Echelon defects and
     adapted public CVE patterns) because synthetic cases overstate detection
     (`SRC-ACAD-LI-2023`, `SRC-ACAD-LIPP-2022`).
3. **Adversarial variants.** Mutation of each holdout case (renaming, aliasing through
   intermediate bindings, pipeline versus nested call style, computation expressions,
   partial application, active patterns, type providers) to test that rules key on
   semantics, not syntax.
4. **Bypass testing.** For "unavailable by construction" rules, attempt to reach the
   forbidden capability by reflection, dynamic loading, interop or configuration, and
   confirm a rule or structural control fails closed.
5. **Label quality.** Two independent labelers per case with adjudication; record
   disagreement. Real-world vulnerability datasets showed 20% to 71% inaccurate labels and
   17% to 99% duplication (`SRC-ACAD-CROFT-2023`).
6. **Leakage control.** Deduplicate across corpora by normalized AST hash; never tune on
   the holdout; data leakage and duplication produced over-optimistic results in prior
   static analysis research (`SRC-ACAD-KANG-2022`).
7. **Regression gate.** Every rule change runs all three corpora; a drop in holdout recall
   for any CWE blocks release of the rule pack.
8. **Developer actionability.** Track triage time and false positive dismissals, since
   false positives and workflow fit drive non-adoption (`SRC-ACAD-JOHNSON-2013`,
   `SRC-ACAD-CHRISTAKIS-2016`).

## 7. Benchmark publication methodology

Goal: results a skeptical security researcher can reproduce and cannot accuse of
overfitting.

1. **Preregistration.** Before running the holdout, publish (with timestamp and hash) the
   tool versions, rule pack version, corpus manifests, metrics, primary hypotheses, and
   analysis plan, in the Praxis record system. Deviations are reported as deviations.
2. **Corpus documentation.** For each corpus: origin, authorship, construction rules,
   license, CWE distribution, safe-to-vulnerable ratio, deduplication method, labeling
   protocol and inter-rater agreement. Public fixtures are versioned and MIT licensed
   where Echelon owns them; third-party corpora keep their own licenses (Juliet terms must
   be checked per download; OWASP Benchmark is GPL-2.0).
3. **Holdout discipline.** Keep a sealed holdout that rule authors cannot see. After each
   publication, retire part of the holdout to public fixtures and replace it with newly
   authored cases, so that the published holdout score always comes from unseen cases.
   Log every access to the holdout.
4. **Metrics per CWE, not only aggregate.** Report true positives, false positives,
   false negatives and true negatives per CWE and per SEC rule; recall, precision, false
   positive rate and F1 only where counts support them; Youden's J for comparability with
   OWASP Benchmark. Report location-matching rules (file, line tolerance, symbol).
5. **Uncertainty.** Wilson score 95% intervals for each proportion; bootstrap intervals
   for differences between versions; state sample sizes and refuse to report a rate on
   very small samples (state the threshold in the preregistration).
6. **Real-world validity section.** Report synthetic and real-world results separately
   and expect a gap, as the literature shows.
7. **No ranking and no endorsement language.** Follow SATE's caution: present results as
   evidence for a stated use, not as a ranking of tools, and state that benchmarking is not
   accreditation or government endorsement (Standard, Scanner validation).
8. **Reproducibility package.** Container image digest, tool and rule hashes, corpus
   commit, scripts, raw SARIF, and the scoring code. Sign artifacts and record provenance
   through Praxis.
9. **Conflict of interest disclosure.** Echelon builds the rules and the benchmark; say so.
   Offer the holdout methodology for third-party review.
10. **Negative results.** Publish misses and known blind spots by CWE, including classes
    the tool does not attempt.

## 8. Recommended Echelon-native security analysis architecture

Principle: reuse mature open-source tools for everything language independent; build F#
analysis only for the rules in section 4.2 marked High or Medium; prefer structural
restriction over detection.

### 8.1 Layers

| Layer | Tools | Owner (proposed) | Output |
|---|---|---|---|
| L0 Structural restriction | Strata as sole data path; Limen as sole JS path; Forma for rendering; project reference rules (only approved projects may reference database or interop packages) | Strata, Limen, Forma for the capabilities; Tutela for the rules | Build fails on forbidden references |
| L1 Compiler policy | F# warnings as errors for incomplete matches and unverifiable code; nullable and strict options as adopted | Tutela defines; Conditor or each repository applies | Build result |
| L2 F# semantic rules | Tutela rule pack on FSharp.Analyzers.SDK, one analyzer per SEC rule, SARIF output | Tutela | SARIF with stable rule IDs |
| L3 Off-the-shelf SAST for non-F# code | Semgrep CE or Opengrep for C#, JavaScript, YAML, IaC; Roslyn CA rules for C# | Tutela configures; repositories run | SARIF |
| L4 Supply chain | OSV-Scanner, Syft, Grype, Scorecard, lockfile enforcement | Tutela policy; Praxis gate | SBOM, SARIF |
| L5 Secrets | `tutela scan-secrets` plus Gitleaks for history | Tutela | Tutela secret-scan evidence |
| L6 IaC and containers | Trivy or Checkov | Tutela policy | SARIF |
| L7 Dynamic | ZAP, Schemathesis, Nuclei against test deployments | Tutela policy; Unbound test environment | Findings |
| L8 Invariant and authorization tests | Generated negative authorization tests from a policy model; property-based tests for financial invariants | Unbound (tests), Tutela (evidence contract), Ordo (state legality) | Test evidence |
| L9 AI agent tests | garak, PyRIT scenarios for bounded agent authority | Unbound with Tutela evidence contract | Findings |
| L10 Normalization and gate | SARIF to `tutela.verification/1`; exceptions; release posture | Tutela | Verdict |
| L11 CI enforcement and provenance | Required checks, signed evidence | Praxis | Provenance records |
| L12 Measurement | Longitudinal quality and gate metrics | Dokimos consumes Tutela outputs; does not define security meaning | Trends |
| L13 Reports | Validation and assessment reports | Folio renders | PDF |

### 8.2 Repository ownership

- **Tutela** should own the security rule registry, the F# security analyzer pack, scanner
  configuration policy, findings normalization, exceptions, the scanner validation
  corpus and the benchmark methodology. Evidence: Dokimos R8 line 118 routes security
  analysis to Tutela and states Aegis is not the security authority; Tutela's own
  ownership statement claims security policy, evidence interpretation and release
  posture and forbids competing rule definitions elsewhere.
- **Aegis** should not own any of this. Its verified purpose is operational fault
  handling (`architecture/ECHELON-CURRENT-STATE-BRIEF.md`). The Standard's proposed
  ownership section should be corrected; that change belongs in `recommendations/` and
  in the organization administration repository, not here.
- **Dokimos** may host generic analyzer-adapter and longitudinal measurement machinery
  and consume Tutela outputs, but per its own requirements must not become a competing
  security authority. The Standard assigns Dokimos "independent verification and scanner
  benchmarks"; that role is unverified and conflicts with R8 unless the benchmark is a
  Tutela artifact that Dokimos only measures.
- **Independence inside Echelon**: holdout authorship should sit with a person or agent
  session that does not author Tutela rules, recorded through Praxis provenance. This is
  second-line separation within a first-party program; it is not independent assurance.

### 8.3 Build order (proposed)

1. Turn on language-independent layers in CI across repositories (L4, L5, L6), since
   Tutela records none run today.
2. Define the machine-readable rule schema in Tutela (owner, ID, version, CWE, mechanism,
   negative tests, evidence, residual risk), per the Standard's enforcement model.
3. Build F# analyzers for SEC-DB-001, SEC-EXEC-001 and SEC-DATA-001 first (high gap,
   high consequence), with fixtures and a sealed holdout.
4. Publish the first scanner validation report with the methodology in section 7.
5. Add authorization and financial invariant test generation for Unbound once a domain
   model exists.

## 9. Open questions

- Which F# web, view and serialization libraries will Unbound adopt? Rules depend on them.
- Will Echelon license CodeQL (GitHub Advanced Security) for its C# components, or rely
  on Semgrep CE or Opengrep plus Roslyn rules?
- Is any mature IL-level security analyzer suitable as a cross-check for F#?
- Should Tutela's PolyForm Noncommercial license change for the published validation
  tooling, given the Standard's MIT preference?
- Who outside the rule-authoring team will author and hold the sealed holdout?

## 10. Limitations

- Licenses were verified from repository LICENSE files on the default branch; release
  artifacts may differ.
- Semgrep's commercial feature boundaries were read from documentation navigation and the
  announcement only.
- Academic findings were taken from abstracts; full papers were not read.
- No tool was executed against Echelon code in this research.
