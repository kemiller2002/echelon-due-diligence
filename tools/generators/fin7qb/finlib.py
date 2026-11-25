"""Shared builders for the question bank categories RCN, CUS, INV, FEE, RRP.

Records are built as data and serialized with json.dumps(ensure_ascii=False).
"""
import json, os

REPO = "/home/user/echelon-due-diligence"
HIST = [{"date": "2026-11-25", "change": "created", "by": "research-agent"}]
COST_BASIS = "order-of-magnitude judgment, not sourced"
UNB = "unbound@9b38de47"

DEF_CURRENT = ("Unknown; no evidence located. Unbound exists only as requirements "
               "(" + UNB + ":requirements/); there is no production system, sponsor, "
               "custodian connection or operating history.")
DEF_PROVABLE = ("Nothing operational. Only requirement text in " + UNB +
                " (cited requirement IDs), which shows design intent, not operation.")
DEF_RATIONALE = ("Specified in Unbound requirements (cited) but not implemented; no "
                 "production deployment, operating evidence or independent review exists "
                 "(architecture/ECHELON-CURRENT-STATE-BRIEF.md).")

DEF_IND = ["donor-advised-funds", "nonprofit", "financial-services"]
DEF_JUR = ["US-federal"]
DEF_PROD = ["unbound"]


def S(sid, loc=None, rel="informed-by", basis="reasonably-inferred"):
    r = {"source_id": sid, "relation": rel, "basis": basis}
    if loc:
        r["locator"] = loc
    return r


def UB(loc):
    return S("SRC-ECH-UNB-BASELINE", loc, "derived-from", "directly-documented")


def Q(sub, q, concern, risk, src, cls, imp, alts=None, ind=None, jur=None,
      prod=None, auth=None, oq=None, scope=None, disc=None):
    return dict(sub=sub, q=q, concern=concern, risk=risk, src=src, cls=cls, imp=imp,
                alts=alts or [], ind=ind, jur=jur, prod=prod, auth=auth, oq=oq or [],
                scope=scope, disc=disc)


def C(title, objective, ctype, level, systems=None, related=None, policies=None,
      residual=None, notes=None, frefs=None, owner=None):
    return dict(title=title, objective=objective, ctype=ctype, level=level,
                systems=systems or ["Unbound (specified, not built)"],
                related=related or [], policies=policies or [], residual=residual or [],
                notes=notes, frefs=frefs or [], owner=owner)


def E(title, desc, mech, fresh, producer="not yet assigned", fmt=None, prov=None,
      signing=None, retention=None, indep="first-party", disc="customer-only",
      notes=None):
    return dict(title=title, desc=desc, mech=mech, fresh=fresh, producer=producer,
                fmt=fmt, prov=prov, signing=signing, retention=retention, indep=indep,
                disc=disc, notes=notes)


def AU(title, target, stmt, reqs, ctls, evrs, qs, status="proposed-target-state",
       rationale=DEF_RATIONALE, current=DEF_CURRENT, intended=None, provable=DEF_PROVABLE,
       stmt_kind="planned", oqs=None, risks=None, mech="continuous-automated",
       autom="high", impl="medium", rec="low", owner=None, disc="nda",
       fresh="P1D", challenge=None, policies=None, external=None):
    return dict(title=title, target=target, stmt=stmt, reqs=reqs, ctls=ctls, evrs=evrs,
                qs=qs, status=status, rationale=rationale, current=current,
                intended=intended or target, provable=provable, stmt_kind=stmt_kind,
                oqs=oqs or [], risks=risks or [], mech=mech, autom=autom, impl=impl,
                rec=rec, owner=owner or "Unassigned (proposed: Unbound product owner)",
                disc=disc, fresh=fresh, challenge=challenge, policies=policies or [],
                external=external)


def build(cat, units, default_ind=None):
    qs_out, au_out, c_out, e_out = [], [], [], []
    qn = cn = en = 0
    for i, u in enumerate(units, 1):
        au_id = f"ANS-{cat}-{i:03d}"
        cids, eids = [], []
        for e in u["evrs"]:
            en += 1
            eid = f"EVR-{cat}-{en:03d}"
            eids.append(eid)
            rec = {"id": eid, "title": e["title"], "description": e["desc"],
                   "producer": e["producer"], "mechanism": e["mech"],
                   "freshness": e["fresh"], "independence": e["indep"],
                   "disclosure_classification": e["disc"],
                   "status": "proposed-target-state"}
            if e["fmt"]: rec["format"] = e["fmt"]
            if e["prov"]: rec["provenance_fields"] = e["prov"]
            if e["signing"]: rec["signing"] = e["signing"]
            if e["retention"]: rec["retention"] = e["retention"]
            if e["notes"]: rec["notes"] = e["notes"]
            e_out.append(rec)
        for c in u["ctls"]:
            cn += 1
            cid = f"ECTL-{cat}-{cn:03d}"
            cids.append(cid)
            rec = {"id": cid, "title": c["title"], "objective": c["objective"],
                   "control_type": c["ctype"], "assurance_level": c["level"],
                   "implementing_systems": c["systems"], "status": "proposed-target-state",
                   "evidence_requirements": eids,
                   "owner": c["owner"] or u["owner"]}
            if c["policies"]: rec["policies"] = c["policies"]
            if c["related"]: rec["related_external_controls"] = c["related"]
            if c["frefs"]: rec["framework_refs"] = c["frefs"]
            if c["residual"]: rec["residual_risks"] = c["residual"]
            if c["notes"]: rec["notes"] = c["notes"]
            c_out.append(rec)
        a = {"id": au_id, "title": u["title"], "status": u["status"],
             "status_rationale": u["rationale"], "target_answer": u["target"],
             "current_practice": u["current"], "intended_practice": u["intended"],
             "provable": u["provable"], "customer_statement": u["stmt"],
             "customer_statement_kind": u["stmt_kind"], "assurance_independence": "none",
             "controls": cids, "evidence_requirements": eids, "owner": u["owner"],
             "history": HIST, "evidence_freshness": u["fresh"],
             "evidence_mechanism": u["mech"], "automation_potential": u["autom"],
             "disclosure_classification": u["disc"], "implementation_cost": u["impl"],
             "recurring_cost": u["rec"], "cost_basis": COST_BASIS}
        if u["policies"]: a["policies"] = u["policies"]
        if u["reqs"]: a["requirements"] = u["reqs"]
        if u["risks"]: a["residual_risks"] = u["risks"]
        if u["oqs"]: a["open_questions"] = u["oqs"]
        if u["external"]: a["external_assurance"] = u["external"]
        if u["challenge"]: a["challenge"] = u["challenge"]
        au_out.append(a)
        for q in u["qs"]:
            qn += 1
            rec = {"id": f"DDQ-{cat}-{qn:04d}", "question": q["q"], "category": cat,
                   "subcategory": q["sub"], "business_concern": q["concern"],
                   "risk_addressed": q["risk"], "source_refs": q["src"],
                   "industries": q["ind"] or default_ind or DEF_IND,
                   "jurisdictions": q["jur"] or DEF_JUR,
                   "products": q["prod"] or DEF_PROD,
                   "requirement_classification": q["cls"],
                   "customer_importance": q["imp"], "answer_unit": au_id,
                   "controls": cids, "evidence_requirements": eids,
                   "disclosure_classification": q["disc"] or u["disc"],
                   "history": HIST}
            if q["alts"]: rec["alternatives"] = q["alts"]
            if q["auth"]: rec["regulatory_authority"] = q["auth"]
            if u["reqs"]: rec["requirements"] = u["reqs"]
            if u["policies"]: rec["policies"] = u["policies"]
            if q["oq"]: rec["open_questions"] = q["oq"]
            if q["scope"]: rec["answer_scope_note"] = q["scope"]
            qs_out.append(rec)
    for sub, recs in (("questions", qs_out), ("answers", au_out),
                      ("controls", c_out), ("evidence-requirements", e_out)):
        path = os.path.join(REPO, sub, f"{cat}.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for r in recs:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return len(qs_out), len(au_out), len(c_out), len(e_out)
