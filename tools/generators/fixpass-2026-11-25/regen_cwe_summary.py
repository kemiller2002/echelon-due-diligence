"""Regenerate security-by-construction/CWE-ARCHITECTURAL-PREVENTION-MATRIX.md from the canonical CSV.

Unlike tools/generators/gen/gen_matrix.py (batch 1, which needs the CWE 5.0 XML and scratch inputs), this
script needs only the committed CSV, so the summary is reproducible from the repository. Run from the
repository root. Added in the 2026-11-25 fix pass (BL-015).
"""
import collections
import csv

CSV = "security-by-construction/cwe-architectural-prevention-matrix.csv"
OUT = "security-by-construction/CWE-ARCHITECTURAL-PREVENTION-MATRIX.md"
FAMILIES = collections.OrderedDict([
    ("SQL", "Database query injection"), ("INTERP", "Other interpreter and output-format injection"),
    ("OSCMD", "OS command and argument injection"), ("CODE", "Dynamic code generation and evaluation"),
    ("XSS", "Cross-site scripting and unsafe rendering"), ("BROWSER", "Browser policy, origin and navigation controls"),
    ("CSRF", "Cross-site request forgery"), ("MEM", "Memory safety (managed code)"),
    ("NULL", "Null dereference and uninitialized values"), ("NUM", "Numeric correctness and money arithmetic"),
    ("RES", "Resource exhaustion and algorithmic complexity"), ("DESER", "Unsafe deserialization and mass assignment"),
    ("FILE", "File system, path and upload handling"), ("SSRF", "Server-side request forgery and outbound reference control"),
    ("XML", "XML parsing hazards"), ("AUTHZ", "Authorization and access control"), ("TENANT", "Tenant isolation"),
    ("AUTHN", "Authentication and session management"), ("CRYPTO", "Cryptography and randomness"),
    ("SECRETS", "Credentials and secrets in code or configuration"), ("INFO", "Sensitive information exposure"),
    ("ERR", "Exceptional condition handling"), ("INPUT", "Input validation and canonicalization"),
    ("SUPPLY", "Software supply chain and third-party components"), ("CONFIG", "Security configuration and insecure defaults"),
    ("LOG", "Security logging, audit and evidence provenance"), ("CONC", "Concurrency, idempotency and workflow integrity"),
    ("DESIGN", "Secure design principles"), ("AI", "AI components and AI-authored changes"),
    ("NA", "Platform-specific weakness outside the F# and .NET scope"),
])
LV = ["L%d" % i for i in range(1, 11)]
LV_NAME = {"L1": "Eliminated within defined scope", "L2": "Type system", "L3": "Restricted interface",
           "L4": "Compiler enforcement", "L5": "Build or release gate", "L6": "Automated analysis",
           "L7": "Property-based testing", "L8": "Adversarial testing", "L9": "Runtime monitoring",
           "L10": "External or manual evaluation only"}

rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
n = len(rows)
cnt = lambda k, rs=rows: collections.Counter(r[k] for r in rs)
top = sorted([r for r in rows if r["cwe_top25_2025_rank"]], key=lambda r: int(r["cwe_top25_2025_rank"]))
o25 = sum("owasp-top10-2025" in r["inclusion_basis"] for r in rows)
o21 = sum("owasp-top10-2021" in r["inclusion_basis"] for r in rows)
fin = sum(r["inclusion_basis"] == "financial-application-relevance" for r in rows)
lv = cnt("strongest_achievable_level")
l1_unbuilt = sum(1 for r in rows if r["strongest_achievable_level"] == "L1" and r["prerequisite_components_exist"].startswith("no:"))
unbuilt = sum(1 for r in rows if r["prerequisite_components_exist"].startswith("no:"))
partial = sum(1 for r in rows if r["prerequisite_components_exist"].startswith("partial"))
hyp = "hypothesized_architecture_vs_scanning"

L = []
A = L.append
A("---\nid: DD-SBC-002\ntitle: CWE architectural prevention matrix (generated summary)\nstatus: draft\nversion: 0.2.0\n"
  "created: 2026-11-25\nupdated: 2026-11-25\ntags: [security-by-construction, cwe, assurance, due-diligence]\n"
  "related_documents:\n  - security-by-construction/SECURITY-BY-CONSTRUCTION-RESEARCH-REPORT.md\n"
  "  - security-by-construction/cwe-architectural-prevention-matrix.csv\n"
  "  - security-by-construction/proposed-construction-rules.jsonl\n---\n")
A("# CWE architectural prevention matrix (summary)\n")
A("This file is generated from `cwe-architectural-prevention-matrix.csv`, which is the canonical record, by "
  "`tools/generators/fixpass-2026-11-25/regen_cwe_summary.py`. Do not edit this summary by hand; regenerate it. "
  "The batch 1 generator that produced the CSV from the CWE 5.0 XML is preserved at "
  "`tools/generators/gen/gen_matrix.py`, but its input files were in a scratch location and are not committed, so "
  "the CSV itself cannot yet be rebuilt from the XML (OBJ-SKEPTIC-006 remains partly open). Corrections made in the "
  "2026-11-25 fix pass (`tools/generators/fixpass-2026-11-25/cwe_matrix_fix.py`) are recorded in each changed row's "
  "`notes`.\n")
A("**Every row is a target, and this is internal design analysis.** No Unbound code exists, so `current_status` is "
  "`proposed-target-state` and `current_demonstrated_level` is `none` for all %d rows. `strongest_achievable_level` "
  "is the strongest level the architecture could support within the stated scope if the evidence listed were "
  "produced; it is not a claim about today, and the L-scale is Echelon's own, not a recognized external scale. Do "
  "not quote these counts to customers before independent review.\n" % n)
A("**Scope of every claim.** By-construction claims apply only to server-side F# assemblies (column `claim_scope`). "
  "F# compiled to WebAssembly and executed in the browser runs on an attacker-controlled machine: the attacker can "
  "patch it, replay boundary messages or call the server directly, so no type-level guarantee there is a security "
  "control. Browser-resident code, including the Limen kernel, is defense in depth for honest clients only. No "
  "authorization, tenant, money, eligibility or workflow decision may rely on client-resident code.\n")
A("## Source catalog\n")
A("- CWE List version 5.0, schema 8.0, catalog date 2026-10-28, downloaded 2026-11-25 from `https://cwe.mitre.org/data/xml/cwec_latest.xml.zip` (archive SHA-256 `bcda44c9abf61ff977f50c3c6649eea5a97a7b0626b0396c2c3ec4bfb973a3dc`; `cwec_v5.0.xml` SHA-256 `47165a9593def89c69b9ef50c34d99ac68db55df8373613e85e9cc9ceecefb1d`). The XML holds 984 Weakness elements, 956 not deprecated, matching the 956 weaknesses MITRE reports for 5.0. CWE 5.0 replaced Category elements with Grouping elements.")
A("- 2025 CWE Top 25: view CWE-1435 in the catalog, ranks confirmed against `https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html` (page updated 2025-12-15). No 2026 Top 25 was published as of 2026-11-25.")
A("- OWASP Top 10 2025: the CWE catalog's view CWE-1450 is labeled 'OWASP Top Ten RC1 (2025)' with groupings CWE-1436 to CWE-1445. The OWASP site presents the 2025 release; any differences between the final OWASP mappings and the RC1 view in CWE 5.0 were not reconciled here (open question).")
A("- OWASP Top 10 2021: view CWE-1344, included for continuity because many questionnaires still cite 2021 categories.\n")
A("## Coverage\n")
A("| Measure | Count |\n|---|---|")
for k, v in [("Total CWE rows", n), ("2025 Top 25 entries", len(top)), ("Rows mapped to OWASP 2025 RC1 view", o25),
             ("Rows mapped to OWASP 2021 view", o21), ("Rows added only for financial web application relevance", fin),
             ("Deprecated CWE entries retained for traceability", sum(r["cwe_status"] == "Deprecated" for r in rows))]:
    A("| %s | %d |" % (k, v))
A("")
A("## Strongest achievable assurance level (target, not current)\n")
A("| Level | Meaning | Rows |\n|---|---|---|")
for l in LV:
    A("| %s | %s | %d |" % (l, LV_NAME[l], lv.get(l, 0)))
A("| not-applicable | Platform absent from the product (statement of absence, not elimination) | %d |" % lv.get("not-applicable", 0))
A("")
A("L1 rows: %d, all outside the not-applicable platform family. %d of them depend on a component that does not exist "
  "(prerequisite_components_exist starts with no), and the CWE-89 and CWE-564 L1 targets are conditional on a Strata runtime query interface that "
  "does not exist.\n" % (lv.get("L1", 0), l1_unbuilt))
A("## Prerequisite components\n")
A("| `prerequisite_components_exist` | Rows |\n|---|---|")
A("| no (the mechanism depends on a component that does not exist) | %d |" % unbuilt)
A("| partial (a component-level pattern exists in another Echelon repository; no Unbound implementation) | %d |" % partial)
A("| not-applicable | %d |" % lv.get("not-applicable", 0))
A("")
A("## Relevance to a financial web application\n")
A("| Relevance | Rows |\n|---|---|")
order = ["critical", "high", "medium", "low", "not-applicable-in-scope"]
for k, v in sorted(cnt("relevance_financial_web").items(), key=lambda x: order.index(x[0])):
    A("| %s | %d |" % (k, v))
A("")
A("## Architecture compared with conventional scanning (hypothesized)\n")
A("`demonstrated_architecture_vs_scanning` is `not-demonstrated` for every row: nothing has been built or measured. "
  "`hypothesized_architecture_vs_scanning` compares an unbuilt target architecture with shipping scanners and is a "
  "research hypothesis, not a finding. `beyond` means the target architecture could establish a property that "
  "scanning cannot (absence of a capability, a type-level guarantee, or coverage of a class scanners do not model); "
  "`comparable` means scanners are already the principal control and architecture adds little; `complementary` "
  "means both are needed and neither dominates. The proposed F# fixture corpus (REC-SBC-016) is the way to test "
  "these hypotheses.\n")
A("| Demonstrated | Rows |\n|---|---|")
for k, v in cnt("demonstrated_architecture_vs_scanning").most_common():
    A("| %s | %d |" % (k, v))
A("")
A("| Hypothesized | Rows |\n|---|---|")
for k, v in cnt(hyp).most_common():
    A("| %s | %d |" % (k, v))
A("")
A("| Conventional scanning detects | Rows |\n|---|---|")
for k, v in cnt("conventional_scanning_detects").most_common():
    A("| %s | %d |" % (k, v))
A("")
A("## Control families\n")
A("Strongest level is the strongest target in the family; scanning and the hypothesized comparison are the most common "
  "row values.\n")
A("| Family | Name | Rows | Strongest level (target) | Scanning | Hypothesized vs scanning |\n|---|---|---|---|---|---|")
for fam, name in FAMILIES.items():
    rs = [r for r in rows if r["control_family"] == fam]
    if not rs:
        continue
    lvls = [r["strongest_achievable_level"] for r in rs if r["strongest_achievable_level"] in LV]
    best = min(lvls, key=lambda x: int(x[1:])) if lvls else "not-applicable"
    A("| %s | %s | %d | %s | %s | %s |" % (fam, name, len(rs), best, cnt("conventional_scanning_detects", rs).most_common(1)[0][0],
                                           cnt(hyp, rs).most_common(1)[0][0]))
A("")
A("## 2025 CWE Top 25\n")
A("| Rank | CWE | Name | Family | Strongest achievable (target) | Prerequisite components exist | Scope note | Scanning | Hypothesized vs scan |")
A("|---|---|---|---|---|---|---|---|---|")
for r in top:
    note = r["notes"].split(". ")[1] if r["notes"].startswith("Rank") and ". " in r["notes"] else ""
    note = note.split("Fix pass")[0].strip()
    pre = r["prerequisite_components_exist"].split(":")[0]
    A("| %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (r["cwe_top25_2025_rank"], r["cwe_id"], r["cwe_name"], r["control_family"],
      r["strongest_achievable_level"], pre, note.replace("|", "/"), r["conventional_scanning_detects"], r[hyp]))
A("")
A("## All rows\n")
A("| CWE | Name | Basis | Relevance | Family | Level (target) | Supporting | Prerequisites exist | Scan | Hypothesized vs scan |")
A("|---|---|---|---|---|---|---|---|---|---|")
ab = {"cwe-top25-2025": "T25", "owasp-top10-2025-rc1-cwe-view": "O25", "owasp-top10-2021-cwe-view": "O21",
      "financial-application-relevance": "FIN"}
for r in rows:
    b = ",".join(ab[x] for x in r["inclusion_basis"].split(";") if x)
    A("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (r["cwe_id"], r["cwe_name"].replace("|", "/"), b, r["relevance_financial_web"],
      r["control_family"], r["strongest_achievable_level"], r["supporting_levels"].replace(";", ", "),
      r["prerequisite_components_exist"].split(":")[0], r["conventional_scanning_detects"], r[hyp]))
A("")
A("Basis codes: T25 = 2025 CWE Top 25; O25 = CWE view of OWASP Top 10 2025 RC1; O21 = CWE view of OWASP Top 10 2021; FIN = added for financial web application relevance.")
A("")
open(OUT, "w", encoding="utf-8").write("\n".join(L))
print("rows", n, dict(lv), "unbuilt", unbuilt, "partial", partial, "l1_unbuilt", l1_unbuilt)
