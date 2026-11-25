"""Shared helpers for building the GOV..PHY question bank records."""

H = [{"date": "2026-11-25", "change": "created", "by": "research-agent"}]
COST = "order-of-magnitude judgment, not sourced"
OWNER = "Managing member of Echelon Foundry, LLC (role not yet formally assigned)"

FIN = ["financial-services", "banking", "wealth-management"]
DAF = ["donor-advised-funds", "nonprofit"]
ALLI = ["all"]
ORG = ["echelon-organization"]
ALLP = ["all-echelon-products"]
UNB = ["unbound"]
USF = ["US-federal"]
GLB = ["global"]

CATS = {}


def cat(code):
    return CATS.setdefault(code, {"aus": [], "questions": [], "controls": [], "evrs": []})


def S(sid, loc=None, rel="maps-to", basis="reasonably-inferred"):
    d = {"source_id": sid, "relation": rel, "basis": basis}
    if loc:
        d["locator"] = loc
    return d


def D(sid, loc=None, rel="maps-to"):
    return S(sid, loc, rel, "directly-documented")


def Q(text, alts=None, **ov):
    d = {"q": text, "alts": alts or []}
    d.update(ov)
    return d


def CH(**kw):
    return kw


def au(code, n, *, title, status, rationale, target, current, intended, provable,
       statement, kind, controls, evrs, qd, questions, indep="none", **kw):
    c = cat(code)
    aid = f"ANS-{code}-{n:03d}"
    rec = {
        "id": aid, "title": title, "status": status, "status_rationale": rationale,
        "target_answer": target, "current_practice": current,
        "intended_practice": intended, "provable": provable,
        "customer_statement": statement, "customer_statement_kind": kind,
        "assurance_independence": indep,
        "controls": [f"ECTL-{x}" for x in controls],
        "evidence_requirements": [f"EVR-{x}" for x in evrs],
    }
    opt_map = {
        "external_assurance": "external_assurance", "policies": "policies",
        "requirements": "requirements", "freshness": "evidence_freshness",
        "mechanism": "evidence_mechanism", "automation": "automation_potential",
        "disc": "disclosure_classification", "impl": "implementation_cost",
        "recur": "recurring_cost", "residual": "residual_risks",
        "oq": "open_questions", "challenge": "challenge",
    }
    for k, f in opt_map.items():
        if k in kw:
            rec[f] = kw[k]
    rec.setdefault("evidence_mechanism", "not-defined")
    rec.setdefault("disclosure_classification", "nda")
    if "implementation_cost" in rec or "recurring_cost" in rec:
        rec["cost_basis"] = kw.get("cost_basis", COST)
    rec["owner"] = kw.get("owner", OWNER)
    rec["history"] = H
    c["aus"].append(rec)
    for q in questions:
        m = dict(qd)
        m.update(q)
        c["questions"].append((aid, rec, m))
    return aid


def ctl(code, n, *, title, objective, ctype, level, systems, status, evrs,
        owner=OWNER, policies=None, ext=None, refs=None, residual=None, notes=None):
    rec = {
        "id": f"ECTL-{code}-{n:03d}", "title": title, "objective": objective,
        "control_type": ctype, "assurance_level": level,
        "implementing_systems": systems,
    }
    if policies:
        rec["policies"] = policies
    if ext:
        rec["related_external_controls"] = ext
    if refs:
        rec["framework_refs"] = refs
    rec["status"] = status
    rec["evidence_requirements"] = [f"EVR-{x}" for x in evrs]
    rec["owner"] = owner
    if residual:
        rec["residual_risks"] = residual
    if notes:
        rec["notes"] = notes
    cat(code)["controls"].append(rec)


def evr(code, n, *, title, desc, producer, mech, fresh, indep, disc, status,
        fmt=None, prov=None, signing=None, retention=None, notes=None):
    rec = {
        "id": f"EVR-{code}-{n:03d}", "title": title, "description": desc,
        "producer": producer, "mechanism": mech, "freshness": fresh,
    }
    if fmt:
        rec["format"] = fmt
    if prov:
        rec["provenance_fields"] = prov
    if signing:
        rec["signing"] = signing
    if retention:
        rec["retention"] = retention
    rec["independence"] = indep
    rec["disclosure_classification"] = disc
    rec["status"] = status
    if notes:
        rec["notes"] = notes
    cat(code)["evrs"].append(rec)


def build_questions(code):
    out = []
    for i, (aid, au_rec, m) in enumerate(cat(code)["questions"], start=1):
        rec = {"id": f"DDQ-{code}-{i:04d}", "question": m["q"]}
        if m.get("alts"):
            rec["alternatives"] = m["alts"]
        rec.update({
            "category": code, "subcategory": m["sub"],
            "business_concern": m["concern"], "risk_addressed": m["risk"],
            "source_refs": m["src"], "industries": m.get("ind", ALLI),
            "jurisdictions": m.get("jur", USF), "products": m.get("prod", ORG),
        })
        if m.get("auth"):
            rec["regulatory_authority"] = m["auth"]
        rec["requirement_classification"] = m.get("rc", "contractual-common")
        rec["customer_importance"] = m.get("imp", "high")
        rec["answer_unit"] = aid
        if m.get("scope"):
            rec["answer_scope_note"] = m["scope"]
        rec["controls"] = m.get("controls", au_rec["controls"])
        if m.get("pols") or au_rec.get("policies"):
            rec["policies"] = m.get("pols", au_rec.get("policies", []))
        reqs = m.get("reqs", au_rec.get("requirements"))
        if reqs:
            rec["requirements"] = reqs
        rec["evidence_requirements"] = m.get("evrs", au_rec["evidence_requirements"])
        rec["disclosure_classification"] = m.get("disc", "public")
        if m.get("oq"):
            rec["open_questions"] = m["oq"]
        rec["history"] = H
        out.append(rec)
    return out
