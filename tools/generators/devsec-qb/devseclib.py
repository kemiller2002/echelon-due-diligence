"""Shared builders for the question bank categories (APP, API, SDL, ARC, CHG, SCS)."""

HIST = [{"date": "2026-11-25", "change": "created", "by": "research-agent"}]
COST_BASIS = "order-of-magnitude judgment, not sourced"
NOT_EST = "Not established for any production Echelon service; no evidence located."
NOTHING = "Nothing for a production service; no Echelon production system exists as of 2026-11-25."
ENG = "Engineering Lead (proposed role, unassigned)"
SEC = "Security Lead (proposed role, unassigned)"


def src(spec):
    """'ID[@locator][!][^]' ; ! = directly-documented, ^ = informed-by."""
    direct = spec.endswith("!") or "!^" in spec or "^!" in spec
    informed = "^" in spec
    spec = spec.rstrip("!^")
    if "@" in spec:
        sid, loc = spec.split("@", 1)
    else:
        sid, loc = spec, None
    rel = "informed-by" if informed else ("derived-from" if sid.startswith("SRC-ECH") else "maps-to")
    r = {"source_id": sid, "relation": rel, "basis": "directly-documented" if direct else "reasonably-inferred"}
    if loc:
        r["locator"] = loc
    return r


class Cat:
    def __init__(self, code):
        self.code = code
        self.aus = []
        self.ctls = {}
        self.evrs = {}
        self.qs = []

    def E(self, key, title, description, producer="not yet assigned", mechanism="not-defined", freshness="per-event",
          fmt=None, prov=None, signing=None, retention=None, independence="first-party", disclosure="nda",
          status="proposed-target-state", notes=None):
        n = len(self.evrs) + 1
        r = {"id": f"EVR-{self.code}-{n:03d}", "title": title, "description": description, "producer": producer,
             "mechanism": mechanism, "freshness": freshness, "independence": independence,
             "disclosure_classification": disclosure, "status": status}
        if fmt: r["format"] = fmt
        if prov: r["provenance_fields"] = prov
        if signing: r["signing"] = signing
        if retention: r["retention"] = retention
        if notes: r["notes"] = notes
        self.evrs[key] = r
        return key

    def C(self, key, title, objective, ctype, level, systems, evr, policies=None, related=None, cwe=None, refs=None,
          status="proposed-target-state", owner=ENG, residual=None, notes=None, requirements=None):
        n = len(self.ctls) + 1
        r = {"id": f"ECTL-{self.code}-{n:03d}", "title": title, "objective": objective, "control_type": ctype,
             "assurance_level": level, "implementing_systems": systems}
        if policies: r["policies"] = policies
        rel = list(related or []) + list(requirements or [])
        if rel: r["related_external_controls"] = rel
        if cwe: r["cwe"] = cwe
        if refs: r["framework_refs"] = [src(s) for s in refs]
        r.update({"status": status, "evidence_requirements": [self.evrs[e]["id"] for e in evr], "owner": owner})
        if residual: r["residual_risks"] = residual
        if notes: r["notes"] = notes
        self.ctls[key] = r
        return key

    def A(self, title, concern, target, ctls, evrs, status="proposed-target-state", rationale=None,
          current=NOT_EST, intended=None, provable=NOTHING, statement=None, kind="planned",
          independence="none", external=None, policies=None, requirements=None, freshness="per-event",
          mechanism="not-defined", automation="high", disclosure="nda", impl="medium", rec="low",
          owner=ENG, residual=None, oq=None, challenge=None, products=None):
        n = len(self.aus) + 1
        r = {"id": f"ANS-{self.code}-{n:03d}", "title": title, "status": status,
             "status_rationale": rationale or ("Echelon has no production deployment; the relevant rules exist only in the proposed "
                                               "Secure Construction Standard v0.1 or Unbound requirements, so this is a target state."),
             "target_answer": target, "current_practice": current,
             "intended_practice": intended or target,
             "provable": provable,
             "customer_statement": statement or ("Echelon intends to implement this as part of Unbound's initial build; it is not in "
                                                 "operation today and no evidence is available yet."),
             "customer_statement_kind": kind, "assurance_independence": independence}
        if external: r["external_assurance"] = external
        r["controls"] = [self.ctls[x]["id"] for x in ctls]
        r["evidence_requirements"] = [self.evrs[x]["id"] for x in evrs]
        if policies: r["policies"] = policies
        if requirements: r["requirements"] = requirements
        r.update({"evidence_freshness": freshness, "evidence_mechanism": mechanism, "automation_potential": automation,
                  "disclosure_classification": disclosure, "implementation_cost": impl, "recurring_cost": rec,
                  "cost_basis": COST_BASIS, "owner": owner})
        if residual: r["residual_risks"] = residual
        if oq: r["open_questions"] = oq
        if challenge: r["challenge"] = challenge
        r["history"] = HIST
        r["_concern"] = concern
        r["_products"] = products
        self.aus.append(r)
        return r

    def Q(self, au, sub, text, risk, srcs, cls="industry-convention", imp="high", alt=(), ind=None, jur=None,
          prod=None, auth=None, oq=None, concern=None, note=None, disclosure=None):
        n = len(self.qs) + 1
        r = {"id": f"DDQ-{self.code}-{n:04d}", "question": text}
        if alt: r["alternatives"] = list(alt)
        r.update({"category": self.code, "subcategory": sub,
                  "business_concern": concern or au["_concern"], "risk_addressed": risk,
                  "source_refs": [src(s) for s in srcs], "industries": ind or ["all"],
                  "jurisdictions": jur or ["global"],
                  "products": prod or au["_products"] or ["all-echelon-products"]})
        if auth: r["regulatory_authority"] = auth
        r.update({"requirement_classification": cls, "customer_importance": imp, "answer_unit": au["id"]})
        if note: r["answer_scope_note"] = note
        r["controls"] = list(au["controls"])
        if au.get("policies"): r["policies"] = list(au["policies"])
        if au.get("requirements"): r["requirements"] = list(au["requirements"])
        r["evidence_requirements"] = list(au["evidence_requirements"])
        r["disclosure_classification"] = disclosure or au["disclosure_classification"]
        if oq: r["open_questions"] = oq
        r["history"] = HIST
        self.qs.append(r)
        return r

    def records(self):
        aus = [{k: v for k, v in a.items() if not k.startswith("_")} for a in self.aus]
        return self.qs, aus, list(self.ctls.values()), list(self.evrs.values())


def ch(**kw):
    return kw
