"""Move objections addressed by the 2026-11-25 fix pass to accepted-changed and list the changes."""
import json

SBC = ["security-by-construction/cwe-architectural-prevention-matrix.csv", "security-by-construction/CWE-ARCHITECTURAL-PREVENTION-MATRIX.md",
       "security-by-construction/SECURITY-BY-CONSTRUCTION-RESEARCH-REPORT.md"]
AQR = "architecture/AUTOMATED-QUESTIONNAIRE-RESPONSE-REQUIREMENTS.md"
TCR = "trust-center/TRUST-CENTER-REQUIREMENTS.md"
CH = {
    "OBJ-BANKCISO-001": (["EVR-PAY-011", "EVR-PAY-012", "EVR-PAY-013", "EVR-RCN-013", "EVR-GRT-012", "EVR-FEE-009", "EVR-AML-013", "EVR-TEN-014"], "Independent evidence is now planned for money movement and tenant isolation; none exists yet, so the substance (no independent assurance today) remains."),
    "OBJ-BANKCISO-002": (["ANS-HR-006", "ANS-ISP-007", AQR], None),
    "OBJ-BANKCISO-004": (["ANS-SDL-003", "ANS-CHG-002", "ANS-IAM-003", "ANS-IAM-004", "ANS-BKP-002", "ANS-PAY-008", AQR], "Second-person roles and compensating controls are named; no headcount answer unit or staffing tag was added, and no second person is contracted."),
    "OBJ-BANKCISO-005": (SBC, "The comparison is relabeled hypothesized with a not-demonstrated column and the summary says not to quote counts externally; mapping claims to ASVS or SSDF identifiers was not done."),
    "OBJ-BANKCISO-007": (["ANS-TEN-005", "EVR-TEN-014"], None),
    "OBJ-BANKCISO-012": (["ANS-LEG-003", "ANS-IR-004", AQR], "LEG-003 and IR-004 now share one trigger; AVL-003 and DR-007 outage notices were not folded into a single matrix."),
    "OBJ-BANKCISO-015": ([TCR], None),
    "OBJ-BANKCISO-016": (["DDQ-MON-0043", "ANS-MON-011"], None),
    "OBJ-VRM-002": (["DDQ-GOV-0039", "DDQ-GOV-0040", "ANS-GOV-010"], None),
    "OBJ-VRM-005": ([AQR], None),
    "OBJ-VRM-006": ([AQR, "DDQ-AIA-0042", "ANS-AIA-009"], None),
    "OBJ-VRM-007": (["ANS-AIA-007"], "No answer is human-approved yet; counsel review of agent-verified citations remains open (BL-023)."),
    "OBJ-VRM-014": (["EVR-PAY-013", "ANS-PAY-001", "ANS-PAY-002", "ANS-PAY-003"], None),
    "OBJ-VRM-019": (["answers/"], "All 168 challenge objects now carry institutional_acceptance unknown; a schema basis field was not added."),
    "OBJ-SOC2AUD-001": (["ANS-AUD-001", "ANS-AUD-002", "ANS-FCT-004", "ANS-RCN-005"], None),
    "OBJ-SOC2AUD-002": (["external-assurance/EXTERNAL-ASSURANCE-REQUIREMENTS-MATRIX.md", "external-assurance/external-assurance-matrix.csv", "cost-avoidance/COMPLIANCE-COST-AVOIDANCE-REPORT.md"], "SOC 1 cost is recorded as unknown; no sourced cost exists."),
    "OBJ-SOC2AUD-007": (["ANS-CHG-006", "ANS-HR-006"], None),
    "OBJ-SOC2AUD-008": (["architecture/EVIDENCE-ARCHITECTURE-SPECIFICATION.md"], None),
    "OBJ-SOC2AUD-009": (["ANS-FCT-007", "ANS-PAY-008"], None),
    "OBJ-SOC2AUD-011": ([TCR, "trust-center/TRUST-CENTER-RESEARCH.md"], None),
    "OBJ-REGULATOR-002": (["SRC-OCC-12CFR9", "DDQ-REG-0032", "ANS-REG-008", "EVR-REG-010"], None),
    "OBJ-REGULATOR-003": (["ANS-IR-005", "ANS-REG-007"], "The fallback is added; IR-005 status was left at unknown because fix passes never raise a status."),
    "OBJ-REGULATOR-005": (["EVR-TEN-014", "EVR-AML-014", "EVR-DAF-011", "EVR-AIG-012", "EVR-WLB-009"], "A build rule requiring non-first-party evidence for requires-external-validation answers was not added to tools/build.fsx."),
    "OBJ-REGULATOR-007": (["ANS-TRM-006", "DDQ-TRM-0029"], None),
    "OBJ-REGULATOR-013": (["SRC-FTC-ACT-5", "ANS-DON-008", "DDQ-DON-0036", "DDQ-DON-0037"], None),
    "OBJ-DAFSPONSOR-002": (["ANS-DAF-011", "DDQ-DAF-0055", "DDQ-DAF-0056", "EVR-DAF-012"], None),
    "OBJ-DAFSPONSOR-003": (["ANS-FEE-007", "DDQ-FEE-0031", "DDQ-FEE-0032"], None),
    "OBJ-DAFSPONSOR-004": (["ANS-LEG-010", "DDQ-LEG-0042", "ANS-LEG-004"], None),
    "OBJ-DAFSPONSOR-005": (["ANS-AUD-001", "ANS-FCT-004"], None),
    "OBJ-DAFSPONSOR-006": (["ANS-DON-008", "DDQ-DON-0036", "ANS-DON-005"], "DDQ-RRP-0040 and ANS-RRP-002 already covered section 170(p); no duplicate question was added."),
    "OBJ-DAFSPONSOR-009": (["ANS-FST-003", "ANS-TRM-003"], "Statements are now honest about the unfunded wind-down; the protections themselves still do not exist."),
    "OBJ-DAFSPONSOR-011": (["ANS-PAY-008", "ANS-RCN-004"], "Tiers are defined; the staffing assumption has not been tested with sponsors."),
    "OBJ-DAFSPONSOR-019": (["ANS-GOV-011", "DDQ-GOV-0041"], None),
    "OBJ-PENTEST-002": (["ANS-PEN-002", "cost-avoidance/PENETRATION-TESTING-COST-REDUCTION-STRATEGY.md"], None),
    "OBJ-PENTEST-003": (SBC + ["ANS-PEN-002"], "The construction rule and build check forbidding control decisions in WASM guest projects is a target, not built."),
    "OBJ-PENTEST-004": (["ANS-TEN-004", "ECTL-TEN-006", "ECTL-TEN-007"], None),
    "OBJ-PENTEST-006": (["security-by-construction/cwe-architectural-prevention-matrix.csv", "ANS-PEN-002"], "CWE-639 is kept as one row rated at its weaker intra-tenant part (L7, AUTHZ) rather than split into two rows."),
    "OBJ-PENTEST-007": (SBC, None),
    "OBJ-PENTEST-011": (["ANS-AIS-001"], "Only the customer statement wording and residual risks changed; read-scope exfiltration remains a residual risk."),
    "OBJ-PENTEST-012": (["ECTL-AIS-018", "EVR-AIS-016", "ANS-AIS-001", "ANS-AIS-008", "ANS-PEN-002"], None),
    "OBJ-PENTEST-016": (["ECTL-APP-017", "EVR-APP-015", "ANS-APP-005", "ANS-ARC-002", "ECTL-APP-007", "ANS-PEN-002"], "No document-rendering CWE row set was added to the matrix."),
    "OBJ-PENTEST-019": ([TCR, "ANS-AUD-005", "ANS-AUD-008", "ANS-AUD-009"], None),
    "OBJ-PENTEST-021": (["cost-avoidance/PENETRATION-TESTING-COST-REDUCTION-STRATEGY.md"], None),
    "OBJ-PRIVACY-001": (["ANS-PRV-013", "DDQ-PRV-0057", "DDQ-PRV-0058", "DDQ-PRV-0059", "EVR-PRV-014", "EVR-PRV-015", "ANS-PRV-001", "ANS-PRV-004"], "The documents are planned; none exists and no owner is named."),
    "OBJ-PRIVACY-002": (["SRC-IN-CDPA", "ANS-PRV-014", "DDQ-PRV-0060", "DDQ-PRV-0061", "EVR-PRV-016"], "The register is planned with Indiana analyzed at research level; counsel has not signed any row."),
    "OBJ-PRIVACY-005": (["ANS-RET-008", "DDQ-RET-0032", "DDQ-RET-0033", "EVR-RET-008", "ANS-RET-005", "ANS-PRV-005", "ANS-RET-002"], None),
    "OBJ-PRIVACY-007": (["ANS-DON-003", "DDQ-DON-0035"], None),
    "OBJ-PRIVACY-008": (["ANS-PRV-015", "DDQ-PRV-0062", "DDQ-PRV-0063", "EVR-PRV-017"], None),
    "OBJ-PRIVACY-009": (["ANS-PRV-011", "ANS-IPR-004", "ANS-AIG-008"], None),
    "OBJ-PRIVACY-011": ([AQR, "ANS-AIA-007", "ANS-AIA-009"], "Which AI tools have already processed customer material is still not recorded."),
    "OBJ-PROCURE-004": (["ANS-SUP-001", "ANS-SUP-002", "ANS-AVL-003", "ANS-IR-002", "ANS-MON-004", "ANS-TRM-001", "ANS-LEG-006", "ANS-FST-003", "ANS-TRM-003"], "Commitments are restated as conditional with the current position; no capacity-constraint field was added to the schema."),
    "OBJ-PROCURE-008": (["ANS-GOV-010", "DDQ-GOV-0039", "DDQ-GOV-0040"], None),
    "OBJ-PROCURE-014": (["ANS-AIA-007"], "No named signatory exists yet; only the description of the build check and the release position changed."),
    "OBJ-SKEPTIC-002": (["ANS-AIA-007"], None),
    "OBJ-SKEPTIC-003": (SBC, None),
    "OBJ-SKEPTIC-004": (["security-by-construction/cwe-architectural-prevention-matrix.csv", "security-by-construction/SECURITY-BY-CONSTRUCTION-RESEARCH-REPORT.md"], "The automated consistency check between L1 rows and their bypasses was not added."),
    "OBJ-SKEPTIC-005": (["security-by-construction/cwe-architectural-prevention-matrix.csv"], "CWE-1321 is fixed; an audit of all rows for bypass text that does not match scope was not performed."),
    "OBJ-SKEPTIC-006": (["tools/generators/fixpass-2026-11-25/regen_cwe_summary.py", "tools/generators/fixpass-2026-11-25/cwe_matrix_fix.py", "security-by-construction/CWE-ARCHITECTURAL-PREVENTION-MATRIX.md"], "The summary is now reproducible from the committed CSV; the CSV still cannot be rebuilt from the CWE XML because the batch 1 inputs were not committed."),
    "OBJ-SKEPTIC-008": (SBC, None),
    "OBJ-SKEPTIC-010": (["ANS-HR-006"], None),
    "OBJ-SKEPTIC-012": (["cost-avoidance/PENETRATION-TESTING-COST-REDUCTION-STRATEGY.md", "ANS-PEN-002"], None),
    "OBJ-SKEPTIC-014": (["answers/"], "Ratings are reset to unknown; sponsor conversations to replace judgment have not happened."),
    "OBJ-SKEPTIC-015": ([AQR], None),
    "OBJ-SKEPTIC-016": ([AQR], None),
}
moved = {}
for path in ("validation/objections-financial.jsonl", "validation/objections-security-buyer.jsonl"):
    recs = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    n = 0
    for o in recs:
        if o["id"] in CH:
            assert o["disposition"] == "accepted-open", o["id"]
            changes, remaining = CH.pop(o["id"])
            o["disposition"] = "accepted-changed"
            o["changes"] = changes
            o["response"] += " Fix pass 2026-11-25 (fix-pass-agent): changed as listed in changes." + (" Remaining: " + remaining if remaining else "")
            n += 1
    moved[path] = n
    open(path, "w", encoding="utf-8").write("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in recs))
assert not CH, CH
print(moved)
