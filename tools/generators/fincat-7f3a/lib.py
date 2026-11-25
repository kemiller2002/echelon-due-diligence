"""Shared helpers for building FCT/ACT/TXI/FRD/PAY question bank records as data."""
import json
import os

ROOT = "/home/user/echelon-due-diligence"
HISTORY = [{"date": "2026-11-25", "change": "created", "by": "research-agent"}]
COST_BASIS = "order-of-magnitude judgment, not sourced"
UNB = "unbound@9b38de47"

CURRENT_NONE = ("Not established. Unbound exists only as requirements ({u}); there is no ledger, "
                "payment, workflow or control implementation, no production deployment and no customer. "
                "Unknown; no operating evidence located.").format(u=UNB)


def S(source_id, locator=None, relation="maps-to", basis="reasonably-inferred"):
    r = {"source_id": source_id, "relation": relation, "basis": basis}
    if locator:
        r["locator"] = locator
    return r


def D(source_id, locator=None, relation="derived-from"):
    """Source that plainly addresses the topic."""
    return S(source_id, locator, relation, "directly-documented")


def Q(question, sub, concern, risk, srcs, cls, imp="high", alts=None, industries=None,
      juris=None, products=None, authority=None, reqs=None, disclosure=None, oq=None, scope=None):
    return dict(question=question, sub=sub, concern=concern, risk=risk, srcs=srcs, cls=cls, imp=imp,
                alts=alts or [], industries=industries, juris=juris, products=products,
                authority=authority, reqs=reqs, disclosure=disclosure, oq=oq, scope=scope)


def build(cat, aus, controls, evidence, defaults):
    out_q, out_a = [], []
    qn = 0
    for an, au0 in enumerate(aus, start=1):
        au = dict(au0)
        aid = "ANS-%s-%03d" % (cat, an)
        qs = au.pop("questions")
        rec = {"id": aid}
        rec["title"] = au["title"]
        rec["status"] = au.get("status", "proposed-target-state")
        rec["status_rationale"] = au.get("status_rationale", (
            "Unbound requirements specify this design but nothing is implemented, operated or tested "
            "(" + UNB + "). The evidence mechanism, freshness and automation fields describe the target design."))
        rec["target_answer"] = au["target"]
        rec["current_practice"] = au.get("current", CURRENT_NONE)
        rec["intended_practice"] = au["intended"]
        rec["provable"] = au.get("provable", (
            "Nothing operational. Only requirements text can be shown: " + au.get("prov_refs", "") +
            " in " + UNB + ":requirements/baseline/baseline.jsonl. No test, operating evidence or auditor review exists."))
        rec["customer_statement"] = au["statement"]
        rec["customer_statement_kind"] = au.get("kind", "planned")
        rec["assurance_independence"] = au.get("independence", "none")
        if au.get("external_assurance"):
            rec["external_assurance"] = au["external_assurance"]
        rec["controls"] = au["controls"]
        rec["evidence_requirements"] = au["evidence"]
        rec["policies"] = au.get("policies", [])
        rec["requirements"] = au["requirements"]
        rec["evidence_freshness"] = au.get("freshness", "per-event")
        rec["evidence_mechanism"] = au.get("mechanism", "event-driven-automated")
        rec["automation_potential"] = au.get("automation", "high")
        rec["disclosure_classification"] = au.get("disclosure", "customer-only")
        rec["implementation_cost"] = au.get("impl_cost", "medium")
        rec["recurring_cost"] = au.get("rec_cost", "low")
        rec["cost_basis"] = au.get("cost_basis", COST_BASIS)
        rec["owner"] = au.get("owner", defaults["owner"])
        rec["residual_risks"] = au.get("residual", [])
        rec["open_questions"] = au.get("open_questions", [])
        if au.get("challenge"):
            rec["challenge"] = au["challenge"]
        rec["history"] = HISTORY
        out_a.append(rec)
        for q in qs:
            qn += 1
            qr = {"id": "DDQ-%s-%04d" % (cat, qn), "question": q["question"]}
            if q["alts"]:
                qr["alternatives"] = q["alts"]
            qr["category"] = cat
            qr["subcategory"] = q["sub"]
            qr["business_concern"] = q["concern"]
            qr["risk_addressed"] = q["risk"]
            qr["source_refs"] = q["srcs"]
            qr["industries"] = q["industries"] or defaults["industries"]
            qr["jurisdictions"] = q["juris"] or defaults["juris"]
            qr["products"] = q["products"] or ["unbound"]
            qr["regulatory_authority"] = q["authority"] or defaults.get("authority", "none")
            qr["requirement_classification"] = q["cls"]
            qr["customer_importance"] = q["imp"]
            qr["answer_unit"] = aid
            if q["scope"]:
                qr["answer_scope_note"] = q["scope"]
            qr["controls"] = rec["controls"]
            qr["policies"] = rec["policies"]
            qr["requirements"] = q["reqs"] or rec["requirements"]
            qr["evidence_requirements"] = rec["evidence_requirements"]
            qr["disclosure_classification"] = q["disclosure"] or "authenticated-prospect"
            if q["oq"]:
                qr["open_questions"] = q["oq"]
            qr["history"] = HISTORY
            out_q.append(qr)
    ctl_out = []
    for i, c in enumerate(controls, start=1):
        r = {"id": "ECTL-%s-%03d" % (cat, i)}
        r.update(c)
        r.setdefault("status", "proposed-target-state")
        r.setdefault("owner", defaults["owner"])
        ctl_out.append(r)
    evr_out = []
    for i, e in enumerate(evidence, start=1):
        r = {"id": "EVR-%s-%03d" % (cat, i)}
        r.update(e)
        r.setdefault("status", "proposed-target-state")
        evr_out.append(r)
    return out_q, out_a, ctl_out, evr_out


def write(cat, q, a, c, e):
    for sub, recs in (("questions", q), ("answers", a), ("controls", c), ("evidence-requirements", e)):
        p = os.path.join(ROOT, sub, cat + ".jsonl")
        with open(p, "w", encoding="utf-8") as f:
            for r in recs:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")


PROV = ["tenant_id", "legal_sponsor_id", "actor_id", "actor_type", "authority_reference", "policy_version",
        "event_id", "correlation_id", "causation_id", "effective_at", "recorded_at", "content_digest"]
SIGN = ("Proposed: tamper-evident digest chained into ledger or evidence digests anchored externally at least "
        "daily (CNV-PLT-010); signing mechanism and key custody not yet selected")
RET = ("Not established; target is the retention class assigned under RR-REQ-X-036-r1 (platform floor of 7 years "
       "from trigger unless sponsor policy, contract, law or legal hold requires longer), subject to counsel review")
NOT_ASSIGNED = "not yet assigned (intended: {0}; not built)"


def C(title, objective, ctype, level, systems, ev, related=None, policies=None, cwe=None, refs=None,
      residual=None, notes=None):
    r = {"title": title, "objective": objective, "control_type": ctype, "assurance_level": level,
         "implementing_systems": systems}
    if policies:
        r["policies"] = policies
    if related:
        r["related_external_controls"] = related
    if cwe:
        r["cwe"] = cwe
    if refs:
        r["framework_refs"] = refs
    r["evidence_requirements"] = ev
    if residual:
        r["residual_risks"] = residual
    if notes:
        r["notes"] = notes
    return r


def E(title, desc, producer, mech, fresh, fmt="JSON evidence event", prov=None, signing=SIGN, retention=RET,
      independence="first-party", disclosure="customer-only", notes=None):
    r = {"title": title, "description": desc, "producer": producer, "mechanism": mech, "freshness": fresh,
         "format": fmt, "provenance_fields": prov or PROV, "signing": signing, "retention": retention,
         "independence": independence, "disclosure_classification": disclosure}
    if notes:
        r["notes"] = notes
    return r
