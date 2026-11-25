import json, os
REPO = "/home/user/echelon-due-diligence"
HIST = [{"date": "2026-11-25", "change": "created", "by": "research-agent"}]
COST_BASIS = "order-of-magnitude judgment, not sourced"

def R(src, loc=None, rel="maps-to", basis="reasonably-inferred"):
    d = {"source_id": src, "relation": rel, "basis": basis}
    if loc:
        d["locator"] = loc
    return d

def D(src, loc=None, rel="maps-to"):
    return R(src, loc, rel, "directly-documented")

UNB = R("SRC-ECH-UNB-BASELINE", rel="informed-by", basis="directly-documented")
BP = R("SRC-ECH-BUSINESS-PLAN", rel="informed-by", basis="directly-documented")
SOC2D = R("SRC-ECH-UNB-SOC2-DIRECTIVE", rel="informed-by", basis="directly-documented")
CM = R("SRC-ECH-UNB-CONTROL-MATRIX", rel="informed-by", basis="directly-documented")
SCS = R("SRC-ECH-SCS-0.1", rel="informed-by", basis="directly-documented")

class Cat:
    def __init__(self, code, defaults):
        self.code = code
        self.defaults = defaults
        self.qs, self.aus, self.ctls, self.evrs = [], [], [], []
        self.au_index = {}

    def E(self, n, title, desc, producer="not yet assigned", mechanism="not-defined", freshness="P1Y",
          independence="first-party", disc="customer-only", status="proposed-target-state", fmt=None,
          prov=None, retention=None, signing=None, notes=None):
        r = {"id": f"EVR-{self.code}-{n:03d}", "title": title, "description": desc, "producer": producer,
             "mechanism": mechanism, "freshness": freshness, "independence": independence,
             "disclosure_classification": disc, "status": status}
        if fmt: r["format"] = fmt
        if prov: r["provenance_fields"] = prov
        if signing: r["signing"] = signing
        if retention: r["retention"] = retention
        if notes: r["notes"] = notes
        self.evrs.append(r)
        return r["id"]

    def C(self, n, title, objective, ctype, level, systems, evrs, owner, status="proposed-target-state",
          policies=None, related=None, fw=None, residual=None, notes=None):
        r = {"id": f"ECTL-{self.code}-{n:03d}", "title": title, "objective": objective, "control_type": ctype,
             "assurance_level": level, "implementing_systems": systems, "status": status,
             "evidence_requirements": evrs, "owner": owner}
        if policies: r["policies"] = policies
        if related: r["related_external_controls"] = related
        if fw: r["framework_refs"] = fw
        if residual: r["residual_risks"] = residual
        if notes: r["notes"] = notes
        self.ctls.append(r)
        return r["id"]

    def A(self, n, title, status, rationale, target, current, intended, provable, statement, kind,
          controls, evrs, owner, independence="none", mechanism="not-defined", freshness=None,
          automation="unknown", disc="authenticated-prospect", impl="unknown", rec="unknown",
          policies=None, requirements=None, residual=None, oq=None, challenge=None, external=None):
        r = {"id": f"ANS-{self.code}-{n:03d}", "title": title, "status": status, "status_rationale": rationale,
             "target_answer": target, "current_practice": current, "intended_practice": intended,
             "provable": provable, "customer_statement": statement, "customer_statement_kind": kind,
             "assurance_independence": independence, "controls": controls, "evidence_requirements": evrs,
             "owner": owner, "evidence_mechanism": mechanism, "automation_potential": automation,
             "disclosure_classification": disc, "implementation_cost": impl, "recurring_cost": rec,
             "cost_basis": COST_BASIS, "history": HIST}
        if freshness: r["evidence_freshness"] = freshness
        if external: r["external_assurance"] = external
        if policies: r["policies"] = policies
        if requirements: r["requirements"] = requirements
        if residual: r["residual_risks"] = residual
        if oq: r["open_questions"] = oq
        if challenge: r["challenge"] = challenge
        self.aus.append(r)
        self.au_index[n] = r
        return r["id"]

    def Q(self, au, sub, text, alts, concern, risk, refs, cls, imp, industries=None, juris=None,
          products=None, authority=None, note=None, oq=None, disc=None, reqs=None):
        d = self.defaults
        a = self.au_index[au]
        n = len(self.qs) + 1
        r = {"id": f"DDQ-{self.code}-{n:04d}", "question": text}
        if alts: r["alternatives"] = alts
        r.update({"category": self.code, "subcategory": sub, "business_concern": concern,
                  "risk_addressed": risk, "source_refs": refs,
                  "industries": industries or d["industries"], "jurisdictions": juris or d["jurisdictions"],
                  "products": products or d["products"], "regulatory_authority": authority or "none",
                  "requirement_classification": cls, "customer_importance": imp, "answer_unit": a["id"]})
        if note: r["answer_scope_note"] = note
        r["controls"] = list(a["controls"])
        if a.get("policies"): r["policies"] = list(a["policies"])
        if reqs or a.get("requirements"): r["requirements"] = reqs or list(a["requirements"])
        r["evidence_requirements"] = list(a["evidence_requirements"])
        r["disclosure_classification"] = disc or a["disclosure_classification"]
        if oq: r["open_questions"] = oq
        r["history"] = HIST
        self.qs.append(r)

    def write(self):
        for sub, recs in (("questions", self.qs), ("answers", self.aus), ("controls", self.ctls),
                          ("evidence-requirements", self.evrs)):
            p = os.path.join(REPO, sub, f"{self.code}.jsonl")
            with open(p, "w", encoding="utf-8") as f:
                for rec in recs:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(self.code, len(self.qs), len(self.aus), len(self.ctls), len(self.evrs))
