import json, os

REPO = "/home/user/echelon-due-diligence"
HIST = [{"date": "2026-11-25", "change": "created", "by": "research-agent"}]
COST_BASIS = "order-of-magnitude judgment, not sourced"

S = {
    "53": "SRC-NIST-SP800-53-R5", "CSF": "SRC-NIST-CSF-2.0", "CIS": "SRC-CIS-CONTROLS-V8.1",
    "CISB": "SRC-CIS-BENCHMARKS", "TSC": "SRC-AICPA-TSC", "SOC2G": "SRC-AICPA-SOC2-GUIDE",
    "SSAE": "SRC-AICPA-SSAE-18", "CCM": "SRC-CSA-CCM-V4", "CAIQ": "SRC-CSA-CAIQ-V4",
    "SIG": "SRC-SA-SIG", "HEC": "SRC-EDUCAUSE-HECVAT", "VSA": "SRC-VSA-FULL",
    "VSAC": "SRC-VSA-CORE", "VSAQ": "SRC-GOOGLE-VSAQ",
    "I27": "SRC-ISO-27002-2022", "I27001": "SRC-ISO-27001-2022", "I27017": "SRC-ISO-27017",
    "I27018": "SRC-ISO-27018", "PCI": "SRC-PCI-DSS-4.0.1", "ZT": "SRC-NIST-SP800-207",
    "FFIS": "SRC-FFIEC-IS-BOOKLET", "FFAR": "SRC-FFIEC-ARCHITECTURE-BOOKLET",
    "FFOUT": "SRC-FFIEC-OUTSOURCING-BOOKLET", "FFAUTH": "SRC-FFIEC-AUTH-GUIDANCE-2021",
    "TPRM": "SRC-INTERAGENCY-TPRM-2023", "CBG": "SRC-TPRM-COMMUNITY-BANK-GUIDE-2024",
    "NYDFS": "SRC-NYDFS-PART-500", "FTC": "SRC-FTC-SAFEGUARDS-RULE",
    "GLBAI": "SRC-INTERAGENCY-GLBA-SAFEGUARDS", "NACHA": "SRC-NACHA-DATA-SECURITY",
    "NACHAR": "SRC-NACHA-RULES", "DORA": "SRC-EU-DORA", "EBA": "SRC-EBA-OUTSOURCING-GL",
    "GDPR": "SRC-GDPR", "SCC": "SRC-EU-SCC-2021", "DPF": "SRC-EU-US-DPF",
    "ATT": "SRC-MITRE-ATTACK", "CWE": "SRC-MITRE-CWE", "SSDF": "SRC-NIST-SP800-218",
    "SSDFAI": "SRC-NIST-SP800-218A", "SLSA": "SRC-SLSA", "OWCS": "SRC-OWASP-CHEATSHEETS",
    "ASVS": "SRC-OWASP-ASVS", "LLM": "SRC-OWASP-LLM-TOP10-2025", "AGENT": "SRC-OWASP-AGENTIC-AI",
    "FED": "SRC-FEDRAMP", "171": "SRC-NIST-SP800-171-R3", "88": "SRC-NIST-SP800-88",
    "KEV": "SRC-CISA-KEV", "BOD": "SRC-CISA-BOD-22-01", "SBD": "SRC-CISA-SECURE-BY-DESIGN",
    "STAR": "SRC-CSA-STAR", "REGSP": "SRC-SEC-REG-SP-2024", "TRIVY": "SRC-TRIVY",
    "GITLEAKS": "SRC-GITLEAKS", "FSA": "SRC-FSHARP-ANALYZERS", "ROS": "SRC-ROSLYN-SECURITY",
    "CDX": "SRC-CYCLONEDX", "CMMC": "SRC-CMMC-2.0", "FFDAM": "SRC-FFIEC-DAM-BOOKLET",
    "STATERAMP": "SRC-STATERAMP", "CCPA": "SRC-CCPA-CPRA", "BREACH": "SRC-STATE-BREACH-LAWS",
    "OUT": "SRC-SEC-ADVISER-OUTSOURCING-PROPOSAL", "FINRA": "SRC-FINRA-RN-21-29",
    "SCS": "SRC-ECH-SCS-0.1", "UNB": "SRC-ECH-UNB-BASELINE", "UCM": "SRC-ECH-UNB-CONTROL-MATRIX",
    "USOC": "SRC-ECH-UNB-SOC2-DIRECTIVE", "BP": "SRC-ECH-BUSINESS-PLAN",
    "I27036": "SRC-ISO-27036", "800115": "SRC-NIST-SP800-115",
    "EPSS": "SRC-FIRST-EPSS", "NTIA": "SRC-NTIA-SBOM-MIN", "IDG": "SRC-NIST-SP800-63-4",
    "NIST161": "SRC-NIST-SP800-161-R1", "GLBA": "SRC-GLBA", "STATEPRIV": "SRC-US-STATE-PRIVACY-LAWS",
    "UKGDPR": "SRC-UK-GDPR", "AICM": "SRC-CSA-AICM", "OSV": "SRC-OSV", "S2C2F": "SRC-OPENSSF-S2C2F",
}
REL = {"m": "maps-to", "d": "derived-from", "i": "informed-by", "c": "contradicts"}
BAS = {"d": "directly-documented", "r": "reasonably-inferred", "u": "unknown"}


def r(key, loc=None, rel="m", basis="d"):
    o = {"source_id": S[key], "relation": REL[rel], "basis": BAS[basis]}
    if loc:
        o["locator"] = loc
    return o


def Q(cat, n, au, sub, question, concern, risk, refs, alts=None, cls="industry-convention",
      imp="high", ind=None, jur=None, prod=None, reg=None, ctrls=None, evrs=None, pol=None,
      reqs=None, oq=None, note=None, disc="authenticated-prospect"):
    rec = {"id": f"DDQ-{cat}-{n:04d}", "question": question}
    if alts:
        rec["alternatives"] = alts
    rec.update({
        "category": cat, "subcategory": sub, "business_concern": concern, "risk_addressed": risk,
        "source_refs": refs, "industries": ind or ["all"], "jurisdictions": jur or ["global"],
        "products": prod or ["unbound"],
    })
    rec["regulatory_authority"] = reg or "none"
    rec.update({"requirement_classification": cls, "customer_importance": imp,
                "answer_unit": f"ANS-{cat}-{au:03d}"})
    if note:
        rec["answer_scope_note"] = note
    if ctrls:
        rec["controls"] = ctrls
    if pol:
        rec["policies"] = pol
    if reqs:
        rec["requirements"] = reqs
    if evrs:
        rec["evidence_requirements"] = evrs
    rec["disclosure_classification"] = disc
    if oq:
        rec["open_questions"] = oq
    rec["history"] = HIST
    return rec


def write(cat, questions, answers, controls, evrs):
    out = {}
    for sub, recs in (("questions", questions), ("answers", answers), ("controls", controls),
                      ("evidence-requirements", evrs)):
        p = os.path.join(REPO, sub, f"{cat}.jsonl")
        with open(p, "w", encoding="utf-8") as f:
            for x in recs:
                f.write(json.dumps(x, ensure_ascii=False) + "\n")
        out[sub] = len(recs)
    return out


def A(cat, n, title, status, rationale, target, current, intended, provable, stmt, kind,
      ctrls, evrs, pol=None, reqs=None, fresh=None, mech="not-defined", auto="high",
      disc="authenticated-prospect", icost="medium", rcost="low", rr=None, oq=None,
      challenge=None, indep="none", ext=None):
    rec = {"id": f"ANS-{cat}-{n:03d}", "title": title, "status": status,
           "status_rationale": rationale, "target_answer": target, "current_practice": current,
           "intended_practice": intended, "provable": provable, "customer_statement": stmt,
           "customer_statement_kind": kind, "assurance_independence": indep}
    if ext:
        rec["external_assurance"] = ext
    rec.update({"controls": ctrls, "evidence_requirements": evrs})
    if pol:
        rec["policies"] = pol
    if reqs:
        rec["requirements"] = reqs
    if fresh:
        rec["evidence_freshness"] = fresh
    rec.update({"evidence_mechanism": mech, "automation_potential": auto,
                "disclosure_classification": disc, "implementation_cost": icost,
                "recurring_cost": rcost, "cost_basis": COST_BASIS, "owner": "unassigned"})
    if rr:
        rec["residual_risks"] = rr
    if oq:
        rec["open_questions"] = oq
    if challenge:
        rec["challenge"] = challenge
    rec["history"] = HIST
    return rec


def C(cat, n, title, objective, ctype, level, systems, evrs, pol=None, rel=None, cwe=None,
      fw=None, status="proposed-target-state", rr=None, notes=None):
    rec = {"id": f"ECTL-{cat}-{n:03d}", "title": title, "objective": objective,
           "control_type": ctype, "assurance_level": level, "implementing_systems": systems}
    if pol:
        rec["policies"] = pol
    if rel:
        rec["related_external_controls"] = rel
    if cwe:
        rec["cwe"] = cwe
    if fw:
        rec["framework_refs"] = fw
    rec.update({"status": status, "evidence_requirements": evrs, "owner": "unassigned"})
    if rr:
        rec["residual_risks"] = rr
    if notes:
        rec["notes"] = notes
    return rec


def E(cat, n, title, desc, producer, mech, fresh, fmt=None, prov=None, signing=None,
      retention="to be set with auditor and counsel (SOC2-023)", indep="first-party",
      disc="customer-only", status="proposed-target-state", notes=None):
    rec = {"id": f"EVR-{cat}-{n:03d}", "title": title, "description": desc, "producer": producer,
           "mechanism": mech, "freshness": fresh}
    if fmt:
        rec["format"] = fmt
    rec["provenance_fields"] = prov or ["commit", "artifact_digest", "environment", "generated_at", "producer_version"]
    rec["signing"] = signing or "proposed: signed with a KMS-held evidence signing key (see ECTL-ENC-013); not implemented"
    rec["retention"] = retention
    rec.update({"independence": indep, "disclosure_classification": disc, "status": status})
    if notes:
        rec["notes"] = notes
    return rec


def CH(intent, adverse, conv_eff, legal, contract, hist, elim, auto, cont, stronger, verifiable,
       accept, invalid, ccost, acost, arisks, sup, opp, tech, inst):
    return {"customer_intent": intent, "adverse_outcome": adverse,
            "conventional_control_effectiveness": conv_eff, "legally_required": legal,
            "contractually_required": contract, "historical_convention": hist,
            "architectural_elimination": elim, "automatic_enforcement": auto,
            "continuous_evidence": cont, "stronger_alternative": stronger,
            "alternative_verifiable": verifiable, "customer_acceptance_likelihood": accept,
            "invalidating_conditions": invalid, "conventional_cost": ccost,
            "alternative_cost": acost, "alternative_risks": arisks,
            "supporting_arguments": sup, "opposing_arguments": opp,
            "technical_effectiveness": tech, "institutional_acceptance": inst}


HOSTING_OPEN = "Hosting provider, regions and managed services for Unbound are not selected (no verified production infrastructure exists as of 2026-11-25)."
NO_EVIDENCE = "Nothing. No production environment, configuration or operating evidence exists."
