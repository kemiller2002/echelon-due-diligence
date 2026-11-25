import json, os

REPO = "/home/user/echelon-due-diligence"
HIST = [{"date": "2026-11-25", "change": "created", "by": "research-agent"}]
COST_BASIS = "order-of-magnitude judgment, not sourced"
OWNER = "Unbound product owner (proposed role; not yet assigned)"
CUR = ("Not established. Unbound is requirements-only with no production system, customers "
       "or operating evidence (unbound@9b38de47).")
PROV = ("Nothing operational. Only requirement text exists in unbound@9b38de47 "
        "(requirements/baseline/baseline.jsonl); no implementation, test execution or operating evidence.")
EXT = "None. No SOC report, audit, penetration test or independent review covers this area."


def S(sid, loc=None, rel="informed-by", basis="reasonably-inferred"):
    d = {"source_id": sid, "relation": rel, "basis": basis}
    if loc:
        d["locator"] = loc
    return d


def UNB(rel="informed-by"):
    return S("SRC-ECH-UNB-BASELINE", rel=rel, basis="directly-documented")


def AU(key, title, target, intended, planned, reqs, *, policies=None, status="proposed-target-state",
       rationale=None, mech="event-driven-automated", fresh="per-event", auto="high", impl="medium",
       rec="low", residual=None, oq=None, challenge=None, disclosure="authenticated-prospect",
       controls=None, evrs=None):
    return dict(key=key, title=title, target=target, intended=intended, planned=planned, reqs=reqs,
                policies=policies or [], status=status, rationale=rationale, mech=mech, fresh=fresh,
                auto=auto, impl=impl, rec=rec, residual=residual or [], oq=oq or [], challenge=challenge,
                disclosure=disclosure, controls=controls or [], evrs=evrs or [], questions=[])


def CTL(title, objective, ctype, level, systems=None, ext=None, fw=None, residual=None, notes=None,
        policies=None, cwe=None):
    return dict(title=title, objective=objective, ctype=ctype, level=level,
                systems=systems or ["Unbound (proposed; not built)"], ext=ext or [], fw=fw or [],
                residual=residual or [], notes=notes, policies=policies or [], cwe=cwe or [])


def EVR(title, desc, mech="event-driven-automated", fresh="per-event", fmt="JSON record",
        prov=None, retention=None, notes=None, disclosure="customer-only", producer="not yet assigned"):
    return dict(title=title, desc=desc, mech=mech, fresh=fresh, fmt=fmt,
                prov=prov or ["record id", "tenant id", "actor", "authority", "policy version", "recorded time"],
                retention=retention, notes=notes, disclosure=disclosure, producer=producer)


def Q(sub, q, concern, risk, src, cls="industry-convention", imp="high", alts=None, oq=None, req=None,
      ind=None, jur=None, auth="none", note=None):
    return dict(sub=sub, q=q, concern=concern, risk=risk, src=src, cls=cls, imp=imp, alts=alts or [],
                oq=oq or [], req=req or [], ind=ind, jur=jur, auth=auth, note=note)


def CH(intent, adverse, conv_eff, legal, contract, history, elim, auto, cont, stronger, verif, accept,
       invalid, conv_cost, alt_cost, alt_risks, sup, opp, tech, inst):
    return {"customer_intent": intent, "adverse_outcome": adverse,
            "conventional_control_effectiveness": conv_eff, "legally_required": legal,
            "contractually_required": contract, "historical_convention": history,
            "architectural_elimination": elim, "automatic_enforcement": auto,
            "continuous_evidence": cont, "stronger_alternative": stronger,
            "alternative_verifiable": verif, "customer_acceptance_likelihood": accept,
            "invalidating_conditions": invalid, "conventional_cost": conv_cost,
            "alternative_cost": alt_cost, "alternative_risks": alt_risks,
            "supporting_arguments": sup, "opposing_arguments": opp,
            "technical_effectiveness": tech, "institutional_acceptance": inst}


def build(cat, units, default_ind=None):
    default_ind = default_ind or ["donor-advised-funds", "nonprofit"]
    questions, answers, controls, evrs = [], [], [], []
    qn = cn = en = 0
    for an, u in enumerate(units, 1):
        aid = f"ANS-{cat}-{an:03d}"
        cids, eids = [], []
        for e in u["evrs"]:
            en += 1
            eid = f"EVR-{cat}-{en:03d}"
            eids.append(eid)
            r = {"id": eid, "title": e["title"], "description": e["desc"], "producer": e["producer"],
                 "mechanism": e["mech"], "freshness": e["fresh"], "format": e["fmt"],
                 "provenance_fields": e["prov"],
                 "signing": "Proposed: content hash recorded in the append-only evidence store; signing method not yet selected",
                 "retention": e["retention"] or "Proposed: at least 10 years for transaction-level records per CNV-PLT-004; not yet adopted",
                 "independence": "first-party", "disclosure_classification": e["disclosure"],
                 "status": "proposed-target-state"}
            r["notes"] = (e["notes"] + " " if e["notes"] else "") + "Producer not built; the intended producer is the Unbound component named in the description."
            evrs.append(r)
        for c in u["controls"]:
            cn += 1
            cid = f"ECTL-{cat}-{cn:03d}"
            cids.append(cid)
            r = {"id": cid, "title": c["title"], "objective": c["objective"], "control_type": c["ctype"],
                 "assurance_level": c["level"], "implementing_systems": c["systems"],
                 "status": "proposed-target-state", "evidence_requirements": eids, "owner": OWNER}
            if c["policies"]:
                r["policies"] = c["policies"]
            if c["ext"]:
                r["related_external_controls"] = c["ext"]
            if c["fw"]:
                r["framework_refs"] = c["fw"]
            if c["cwe"]:
                r["cwe"] = c["cwe"]
            if c["residual"]:
                r["residual_risks"] = c["residual"]
            r["notes"] = (c["notes"] + " " if c["notes"] else "") + "Design intent only; no implementation exists."
            controls.append(r)
        a = {"id": aid, "title": u["title"], "status": u["status"],
             "status_rationale": u["rationale"] or ("Specified only in Unbound requirements "
                 f"({', '.join(u['reqs'][:4])}); no implementation, test or operating evidence exists."),
             "target_answer": u["target"], "current_practice": CUR, "intended_practice": u["intended"],
             "provable": PROV,
             "customer_statement": "Planned, not available today: " + u["planned"] +
                 " Unbound has no production deployment; this describes intended design only.",
             "customer_statement_kind": "planned", "assurance_independence": "none",
             "external_assurance": EXT, "controls": cids, "evidence_requirements": eids,
             "policies": u["policies"], "requirements": u["reqs"], "evidence_freshness": u["fresh"],
             "evidence_mechanism": u["mech"], "automation_potential": u["auto"],
             "disclosure_classification": u["disclosure"], "implementation_cost": u["impl"],
             "recurring_cost": u["rec"], "cost_basis": COST_BASIS, "owner": OWNER,
             "residual_risks": u["residual"], "open_questions": u["oq"], "history": HIST}
        if u["challenge"]:
            a["challenge"] = u["challenge"]
        answers.append(a)
        for q in u["questions"]:
            qn += 1
            r = {"id": f"DDQ-{cat}-{qn:04d}", "question": q["q"]}
            if q["alts"]:
                r["alternatives"] = q["alts"]
            r.update({"category": cat, "subcategory": q["sub"], "business_concern": q["concern"],
                      "risk_addressed": q["risk"], "source_refs": q["src"],
                      "industries": q["ind"] or default_ind, "jurisdictions": q["jur"] or ["US-federal"],
                      "products": ["unbound"], "regulatory_authority": q["auth"],
                      "requirement_classification": q["cls"], "customer_importance": q["imp"],
                      "answer_unit": aid})
            if q["note"]:
                r["answer_scope_note"] = q["note"]
            allreq = []
            for x in u["reqs"] + q["req"]:
                if x not in allreq:
                    allreq.append(x)
            r.update({"controls": cids, "policies": u["policies"], "requirements": allreq,
                      "evidence_requirements": eids, "disclosure_classification": "authenticated-prospect"})
            if q["oq"]:
                r["open_questions"] = q["oq"]
            r["history"] = HIST
            questions.append(r)
    return questions, answers, controls, evrs


def write(cat, recs):
    q, a, c, e = recs
    for d, rows in (("questions", q), ("answers", a), ("controls", c), ("evidence-requirements", e)):
        with open(os.path.join(REPO, d, f"{cat}.jsonl"), "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return {k: len(v) for k, v in zip(("questions", "answers", "controls", "evidence"), recs)}
