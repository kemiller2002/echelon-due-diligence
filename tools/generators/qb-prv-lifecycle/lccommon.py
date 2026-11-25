"""Shared builders for the PRV/DCL/RET/PRT/TRM/ESC question bank records."""

HIST = [{"date": "2026-11-25", "change": "created", "by": "research-agent"}]
COST_BASIS = "order-of-magnitude judgment, not sourced"

REL = {"d": "derived-from", "m": "maps-to", "i": "informed-by", "c": "contradicts"}
BAS = {"D": "directly-documented", "R": "reasonably-inferred", "U": "unknown"}

DAF = ["donor-advised-funds"]
DAFNP = ["donor-advised-funds", "nonprofit"]
DAFFS = ["donor-advised-funds", "financial-services"]
DAFWM = ["donor-advised-funds", "wealth-management"]
DAFBK = ["donor-advised-funds", "banking"]
FINALL = ["donor-advised-funds", "banking", "wealth-management", "financial-services"]
ALL = ["all"]

USF = ["US-federal"]
USS = ["US-states"]
USFS = ["US-federal", "US-states"]
CA = ["US-state:CA"]
EUUK = ["EU", "UK"]
GLOBAL = ["global"]

UNB = ["unbound"]
ALLP = ["all-echelon-products"]


def s(spec):
    """'SRC-X|locator|rel|basis' -> source_ref dict. Empty locator is omitted."""
    sid, loc, rel, bas = spec.split("|")
    r = {"source_id": sid, "relation": REL[rel], "basis": BAS[bas]}
    if loc:
        r["locator"] = loc
    return r


AUS, QS, CTLS, EVRS = {}, [], [], []


def au(id, title, status, rationale, target, current, intended, provable, stmt, kind,
       controls, evrs, policies=None, reqs=None, freshness="per-event",
       mechanism="not-defined", automation="high", disclosure="customer-only",
       impl="medium", rec="low", owner="Privacy Officer (proposed role; not appointed)",
       residual=None, oq=None, challenge=None, products=None):
    rec_ = {
        "id": id, "title": title, "status": status, "status_rationale": rationale,
        "target_answer": target, "current_practice": current,
        "intended_practice": intended, "provable": provable,
        "customer_statement": stmt, "customer_statement_kind": kind,
        "assurance_independence": "none",
        "external_assurance": "None. No SOC 2 report, ISO certification, privacy assessment or other independent assurance exists for any Echelon service as of 2026-11-25.",
        "controls": controls, "evidence_requirements": evrs,
        "policies": policies or [], "requirements": reqs or [],
        "evidence_freshness": freshness, "evidence_mechanism": mechanism,
        "automation_potential": automation, "disclosure_classification": disclosure,
        "implementation_cost": impl, "recurring_cost": rec, "cost_basis": COST_BASIS,
        "owner": owner, "residual_risks": residual or [], "open_questions": oq or [],
        "history": HIST,
    }
    if challenge:
        rec_["challenge"] = challenge
    AUS[id] = (rec_, products or UNB)
    return id


def q(a, sub, text, alts, concern, risk, srcs, cls, imp, ind=DAF, jur=USF, reg=None,
      oq=None, scope=None, disc="authenticated-prospect", products=None):
    QS.append(dict(a=a, sub=sub, text=text, alts=alts, concern=concern, risk=risk,
                   srcs=srcs, cls=cls, imp=imp, ind=ind, jur=jur, reg=reg, oq=oq,
                   scope=scope, disc=disc, products=products))


def ctl(id, title, objective, ctype, level, systems, evrs, owner, policies=None,
        rel=None, frefs=None, status="proposed-target-state", residual=None, notes=None):
    r = {"id": id, "title": title, "objective": objective, "control_type": ctype,
         "assurance_level": level, "implementing_systems": systems,
         "policies": policies or [], "related_external_controls": rel or [],
         "framework_refs": [s(x) for x in (frefs or [])], "status": status,
         "evidence_requirements": evrs, "owner": owner, "residual_risks": residual or []}
    if notes:
        r["notes"] = notes
    CTLS.append(r)


def evr(id, title, desc, producer, mechanism, freshness, fmt, prov, signing,
        retention, disclosure="customer-only", status="proposed-target-state",
        indep="first-party", notes=None):
    r = {"id": id, "title": title, "description": desc, "producer": producer,
         "mechanism": mechanism, "freshness": freshness, "format": fmt,
         "provenance_fields": prov, "signing": signing, "retention": retention,
         "independence": indep, "disclosure_classification": disclosure,
         "status": status}
    if notes:
        r["notes"] = notes
    EVRS.append(r)


def ch(intent, adverse, conv_eff, legal, contractual, history, elim, auto, cont,
       stronger, verifiable, acceptance, invalid, conv_cost, alt_cost, alt_risks,
       sup, opp, tech, inst):
    return {
        "customer_intent": intent, "adverse_outcome": adverse,
        "conventional_control_effectiveness": conv_eff, "legally_required": legal,
        "contractually_required": contractual, "historical_convention": history,
        "architectural_elimination": elim, "automatic_enforcement": auto,
        "continuous_evidence": cont, "stronger_alternative": stronger,
        "alternative_verifiable": verifiable,
        "customer_acceptance_likelihood": acceptance,
        "invalidating_conditions": invalid, "conventional_cost": conv_cost,
        "alternative_cost": alt_cost, "alternative_risks": alt_risks,
        "supporting_arguments": sup, "opposing_arguments": opp,
        "technical_effectiveness": tech, "institutional_acceptance": inst,
    }


NOPROD = "Unbound has no production deployment, no customers and no operating evidence as of 2026-11-25."
PLANNED_PREFIX = "Unbound is not yet in production. Its requirements specify "
PLANNED_SUFFIX = " This is a design commitment, not an operating control, and has not been independently verified."
NOTHING = "Nothing operational. Only requirement text in the Unbound baseline (unbound@9b38de47) can be shown, and it proves intent, not operation."
BL = "SRC-ECH-UNB-BASELINE"
SD = "SRC-ECH-UNB-SOC2-DIRECTIVE"
DL = "SRC-ECH-DAF-LANDSCAPE"
PO = "Privacy Officer (proposed role; not appointed)"
ENG = "Engineering lead (proposed role; not appointed)"
