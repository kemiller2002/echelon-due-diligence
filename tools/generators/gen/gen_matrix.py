import csv, json, sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from families import FAMILIES
from mapping import FAM, O, FINANCIAL_EXTRA

CWE_DIR = sys.argv[1]
OUT_DIR = sys.argv[2]
weak = json.load(open(os.path.join(CWE_DIR, "weak.json")))
om = json.load(open(os.path.join(CWE_DIR, "owasp_map.json")))
o25, o21 = om["o25"], om["o21"]
TOP25 = ['79','89','352','862','787','22','416','125','78','94','120','434','476','121','502','122','863','20','284','200','306','918','77','639','770']
rank = {c: i + 1 for i, c in enumerate(TOP25)}

ids = set(TOP25)
ids |= {c for c in o25}
ids |= {c for c in o21 if c in weak}
ids |= set(FINANCIAL_EXTRA)
# Keep grouping-level entries 16 and 2 only if listed (they are not Weakness elements)
NONWEAK_NAMES = {"16": "Configuration (grouping-level entry in CWE 5.0)", "2": "7PK - Environment (grouping-level entry in CWE 5.0)"}
ids = {c for c in ids if c in weak or c in NONWEAK_NAMES}

LIMEN = "limen@743cdb9b:docs/29-binding-security.md; limen@743cdb9b:src/kernel/binding-policy.ts; limen@743cdb9b:scripts/smoke-security.ts (run in limen@743cdb9b:.github/workflows/ci.yml)"
FORMA_COUNTER = "Counter-evidence: forma@c8f40b4c:packages/workflow/src/forma-workflow.js line 127 assigns engine HTML to innerHTML"
COMP = {
 "XSS": LIMEN + ". " + FORMA_COUNTER,
 "BROWSER": "limen@743cdb9b:docs/29-binding-security.md (CSP with frame-ancestors 'none', URL scheme allowlist)",
 "CSRF": "limen@743cdb9b:docs/29-binding-security.md (connect-src 'self' in the Limen strict policy; not a CSRF control by itself)",
 "MEM": "No unsafe or P/Invoke usage found by text search in strata@c6a384ec, tutela@476dc682, ordo@db6d39ed or praxis@12bf9951 sources (search, not IL proof)",
 "ERR": "FS0025 as error: limen@743cdb9b:libraries/fsharp/*/*.fsproj (--warnaserror:25); ordo@db6d39ed:Directory.Build.props (TreatWarningsAsErrors with FS0025 comment); strata@c6a384ec:Directory.Build.props (TreatWarningsAsErrors, WarningLevel 5)",
 "NULL": "Nullable enable in ordo@db6d39ed:Directory.Build.props and vigila Directory.Build.props",
 "SQL": "Pattern only: strata@c6a384ec:scripts/check-semantic-architecture.sh enforces project reference tiers; strata@c6a384ec:src/Strata.Host.Postgres/Strata.Host.Postgres.fsproj is the only Npgsql reference. No application query interface exists.",
 "TENANT": "strata@c6a384ec:src/Strata.Host.Postgres/CatalogQueries.fs models RLS policies and reports tables with RLS enabled and no policies (schema management, not runtime enforcement)",
 "LOG": "Change provenance only: praxis@12bf9951 provenance records; not runtime audit",
 "AI": "Change provenance only: praxis@12bf9951 agent provenance (docs/agent-provenance.md in this repository)",
 "CONC": "Method only: ordo@db6d39ed State-Directed Engineering",
 "DESIGN": "Method only: tutela@476dc682 security engineering model",
}
SCAN_LABEL = {"yes": "yes", "partial": "partial", "no": "no"}

rows = []
unmapped = []
for c in sorted(ids, key=int):
    if c not in FAM:
        unmapped.append(c); continue
    fam, _ = FAM[c]
    f = dict(FAMILIES[fam])
    ov = O.get(c, {})
    name = weak[c]["name"] if c in weak else NONWEAK_NAMES[c]
    abs_ = weak[c]["abs"] if c in weak else "Grouping"
    st = weak[c]["status"] if c in weak else "n/a"
    basis = []
    if c in rank: basis.append("cwe-top25-2025")
    if c in o25: basis.append("owasp-top10-2025-rc1-cwe-view")
    if c in o21: basis.append("owasp-top10-2021-cwe-view")
    if c in FINANCIAL_EXTRA: basis.append("financial-application-relevance")
    rel = ov.get("relevance", f["relevance"])
    if c in rank and rel in ("low", "medium"):
        rel = "high"
    status = "proposed-target-state"
    status_ev = "No Unbound implementation exists (architecture/ECHELON-CURRENT-STATE-BRIEF.md; unbound@9b38de47 is requirements only). Control is a target under the proposed Standard (" + "echelon-organization-administration@2763e576:policies/security/secure-construction-standard.md)."
    if rel == "not-applicable-in-scope":
        status = "proposed-target-state"
    row = collections.OrderedDict([
        ("cwe_id", "CWE-" + c),
        ("cwe_name", name),
        ("cwe_abstraction", abs_),
        ("cwe_status", st),
        ("cwe_top25_2025_rank", rank.get(c, "")),
        ("owasp_2025_rc1_category", ";".join(o25.get(c, []))),
        ("owasp_2021_category", ";".join(o21.get(c, []))),
        ("inclusion_basis", ";".join(basis)),
        ("relevance_financial_web", rel),
        ("control_family", fam),
        ("echelon_controls", ov.get("controls", f["controls"])),
        ("strongest_achievable_level", ov.get("level", f["level"])),
        ("supporting_levels", ov.get("supporting", f["supporting"])),
        ("assurance_scope", ov.get("scope", f["scope"])),
        ("known_bypasses", ov.get("bypasses", f["bypasses"])),
        ("residual_risk", ov.get("residual", f["residual"])),
        ("evidence_required", ov.get("evidence", f["evidence"])),
        ("current_status", status),
        ("current_status_evidence", status_ev),
        ("current_demonstrated_level", "none"),
        ("component_evidence", COMP.get(fam, "")),
        ("conventional_scanning_detects", ov.get("scan", f["scan"])),
        ("scanning_notes", ov.get("scan_notes", f["scan_notes"])),
        ("architecture_vs_scanning", ov.get("vs", f["vs"])),
        ("notes", ov.get("notes", "")),
    ])
    rows.append(row)

if unmapped:
    print("UNMAPPED", unmapped); sys.exit(1)

# lint: no em dash
for r in rows:
    for k, v in r.items():
        if "—" in str(v) or "–" in str(v):
            print("dash in", r["cwe_id"], k); sys.exit(1)

csv_path = os.path.join(OUT_DIR, "cwe-architectural-prevention-matrix.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    w.writeheader(); w.writerows(rows)

# ---------- Markdown summary ----------
def cnt(key):
    return collections.Counter(r[key] for r in rows)
lv_order = ["L%d" % i for i in range(1, 11)]
LV_NAME = {"L1":"Eliminated within defined scope","L2":"Type system","L3":"Restricted interface","L4":"Compiler enforcement","L5":"Build or release gate","L6":"Automated analysis","L7":"Property-based testing","L8":"Adversarial testing","L9":"Runtime monitoring","L10":"External or manual evaluation only"}
n = len(rows)
top = [r for r in rows if r["cwe_top25_2025_rank"] != ""]
top.sort(key=lambda r: int(r["cwe_top25_2025_rank"]))
o25n = sum(1 for r in rows if "owasp-top10-2025" in r["inclusion_basis"])
o21n = sum(1 for r in rows if "owasp-top10-2021" in r["inclusion_basis"])
fin = sum(1 for r in rows if r["inclusion_basis"] == "financial-application-relevance")

L = []
A = L.append
A("---")
A("id: DD-SBC-002")
A("title: CWE architectural prevention matrix (generated summary)")
A("status: draft")
A("version: 0.1.0")
A("created: 2026-11-25")
A("updated: 2026-11-25")
A("tags: [security-by-construction, cwe, assurance, due-diligence]")
A("related_documents:")
A("  - security-by-construction/SECURITY-BY-CONSTRUCTION-RESEARCH-REPORT.md")
A("  - security-by-construction/cwe-architectural-prevention-matrix.csv")
A("  - security-by-construction/proposed-construction-rules.jsonl")
A("---")
A("")
A("# CWE architectural prevention matrix (summary)")
A("")
A("This file is generated from `cwe-architectural-prevention-matrix.csv`, which is the canonical record. Do not edit this summary by hand; regenerate it. The generator script was run from a scratch location during research and is not committed; regenerating requires the same inputs (CWE 5.0 XML and the family definitions captured in the report's method section).")
A("")
A("**Every row is a target.** No Unbound code exists, so `current_status` is `proposed-target-state` and `current_demonstrated_level` is `none` for all %d rows. `strongest_achievable_level` is the strongest level the architecture could support within the stated scope if the evidence listed were produced; it is not a claim about today." % n)
A("")
A("## Source catalog")
A("")
A("- CWE List version 5.0, schema 8.0, catalog date 2026-10-28, downloaded 2026-11-25 from `https://cwe.mitre.org/data/xml/cwec_latest.xml.zip` (archive SHA-256 `bcda44c9abf61ff977f50c3c6649eea5a97a7b0626b0396c2c3ec4bfb973a3dc`; `cwec_v5.0.xml` SHA-256 `47165a9593def89c69b9ef50c34d99ac68db55df8373613e85e9cc9ceecefb1d`). The XML holds 984 Weakness elements, 956 not deprecated, matching the 956 weaknesses MITRE reports for 5.0. CWE 5.0 replaced Category elements with Grouping elements.")
A("- 2025 CWE Top 25: view CWE-1435 in the catalog, ranks confirmed against `https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html` (page updated 2025-12-15). No 2026 Top 25 was published as of 2026-11-25.")
A("- OWASP Top 10 2025: the CWE catalog's view CWE-1450 is labeled 'OWASP Top Ten RC1 (2025)' with groupings CWE-1436 to CWE-1445. The OWASP site presents the 2025 release; any differences between the final OWASP mappings and the RC1 view in CWE 5.0 were not reconciled here (open question).")
A("- OWASP Top 10 2021: view CWE-1344, included for continuity because many questionnaires still cite 2021 categories.")
A("")
A("## Coverage")
A("")
A("| Measure | Count |")
A("|---|---|")
A("| Total CWE rows | %d |" % n)
A("| 2025 Top 25 entries | %d |" % len(top))
A("| Rows mapped to OWASP 2025 RC1 view | %d |" % o25n)
A("| Rows mapped to OWASP 2021 view | %d |" % o21n)
A("| Rows added only for financial web application relevance | %d |" % fin)
A("| Deprecated CWE entries retained for traceability | %d |" % sum(1 for r in rows if r["cwe_status"] == "Deprecated"))
A("")
A("## Strongest achievable assurance level (target, not current)")
A("")
A("| Level | Meaning | Rows |")
A("|---|---|---|")
c = cnt("strongest_achievable_level")
for lv in lv_order:
    A("| %s | %s | %d |" % (lv, LV_NAME[lv], c.get(lv, 0)))
A("")
A("## Relevance to a financial web application")
A("")
A("| Relevance | Rows |")
A("|---|---|")
for k, v in sorted(cnt("relevance_financial_web").items(), key=lambda x: ["critical","high","medium","low","not-applicable-in-scope"].index(x[0])):
    A("| %s | %d |" % (k, v))
A("")
A("## Architecture compared with conventional scanning")
A("")
A("`architecture_vs_scanning` values: `beyond` means the architecture can establish a property that scanning cannot (absence of a capability, a type-level guarantee, or coverage of a class scanners do not model); `comparable` means scanners are already the principal control and architecture adds little; `complementary` means both are needed and neither dominates; `less` is not used for any whole class, but the report lists specific areas where the architecture provides less assurance than scanning would.")
A("")
A("| Value | Rows |")
A("|---|---|")
for k, v in cnt("architecture_vs_scanning").most_common():
    A("| %s | %d |" % (k, v))
A("")
A("| Conventional scanning detects | Rows |")
A("|---|---|")
for k, v in cnt("conventional_scanning_detects").most_common():
    A("| %s | %d |" % (k, v))
A("")
A("## Control families")
A("")
A("| Family | Name | Rows | Strongest level | Scanning | Architecture vs scanning |")
A("|---|---|---|---|---|---|")
fc = cnt("control_family")
for fam, f in FAMILIES.items():
    if fc.get(fam):
        A("| %s | %s | %d | %s | %s | %s |" % (fam, f["name"], fc[fam], f["level"], f["scan"], f["vs"]))
A("")
A("## 2025 CWE Top 25")
A("")
A("| Rank | CWE | Name | Family | Strongest achievable | Scope note | Scanning | Arch vs scan |")
A("|---|---|---|---|---|---|---|---|")
for r in top:
    note = r["notes"].split(". ")[1] if r["notes"].startswith("Rank") and ". " in r["notes"] else ""
    A("| %s | %s | %s | %s | %s | %s | %s | %s |" % (r["cwe_top25_2025_rank"], r["cwe_id"], r["cwe_name"], r["control_family"], r["strongest_achievable_level"], note.replace("|", "/"), r["conventional_scanning_detects"], r["architecture_vs_scanning"]))
A("")
A("## All rows")
A("")
A("| CWE | Name | Basis | Relevance | Family | Level | Supporting | Scan | Arch vs scan |")
A("|---|---|---|---|---|---|---|---|---|")
ab = {"cwe-top25-2025":"T25","owasp-top10-2025-rc1-cwe-view":"O25","owasp-top10-2021-cwe-view":"O21","financial-application-relevance":"FIN"}
for r in rows:
    b = ",".join(ab[x] for x in r["inclusion_basis"].split(";") if x)
    A("| %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (r["cwe_id"], r["cwe_name"].replace("|", "/"), b, r["relevance_financial_web"], r["control_family"], r["strongest_achievable_level"], r["supporting_levels"].replace(";", ", "), r["conventional_scanning_detects"], r["architecture_vs_scanning"]))
A("")
A("Basis codes: T25 = 2025 CWE Top 25; O25 = CWE view of OWASP Top 10 2025 RC1; O21 = CWE view of OWASP Top 10 2021; FIN = added for financial web application relevance.")
A("")
open(os.path.join(OUT_DIR, "CWE-ARCHITECTURAL-PREVENTION-MATRIX.md"), "w", encoding="utf-8").write("\n".join(L))
print("rows", n, "top25", len(top), "o25", o25n, "o21", o21n, "fin", fin)
print(c)
print(cnt("control_family"))
print(cnt("architecture_vs_scanning"), cnt("conventional_scanning_detects"), cnt("relevance_financial_web"))
