import json, os

REPO = "/home/user/echelon-due-diligence"
HIST = [{"date": "2026-11-25", "change": "created", "by": "research-agent"}]
COST_BASIS = "order-of-magnitude judgment, not sourced"
OWNER = "Unassigned (proposed role: Security Lead, per UNB-CTRL matrix proposed owners)"


def R(sid, loc=None, rel="maps-to", basis="reasonably-inferred"):
    d = {"source_id": sid, "relation": rel, "basis": basis}
    if loc:
        d["locator"] = loc
    return d


def D(sid, loc=None, rel="maps-to"):
    return R(sid, loc, rel, "directly-documented")


class Cat:
    def __init__(self, code):
        self.code = code
        self.questions = []
        self.answers = []
        self.controls = []
        self.evrs = []
        self.au_index = {}

    def evr(self, n, title, description, producer, mechanism, freshness, independence="first-party",
            disclosure="nda", status="proposed-target-state", fmt=None, prov=None, signing=None,
            retention=None, notes=None):
        rid = f"EVR-{self.code}-{n:03d}"
        r = {"id": rid, "title": title, "description": description, "producer": producer,
             "mechanism": mechanism, "freshness": freshness}
        if fmt: r["format"] = fmt
        if prov: r["provenance_fields"] = prov
        if signing: r["signing"] = signing
        if retention: r["retention"] = retention
        r.update({"independence": independence, "disclosure_classification": disclosure, "status": status})
        if notes: r["notes"] = notes
        self.evrs.append(r)
        return rid

    def ctl(self, n, title, objective, ctype, level, systems, evrs, status="proposed-target-state",
            policies=None, related=None, cwe=None, fw=None, residual=None, notes=None):
        cid = f"ECTL-{self.code}-{n:03d}"
        c = {"id": cid, "title": title, "objective": objective, "control_type": ctype,
             "assurance_level": level, "implementing_systems": systems}
        if policies: c["policies"] = policies
        if related: c["related_external_controls"] = related
        if cwe: c["cwe"] = cwe
        if fw: c["framework_refs"] = fw
        c.update({"status": status, "evidence_requirements": evrs, "owner": OWNER})
        if residual: c["residual_risks"] = residual
        if notes: c["notes"] = notes
        self.controls.append(c)
        return cid

    def au(self, n, title, status, status_rationale, target, current, intended, provable, stmt, stmt_kind,
           controls, evrs, independence="none", policies=None, requirements=None, freshness=None,
           mechanism="not-defined", automation="unknown", disclosure="authenticated-prospect",
           impl="unknown", rec="unknown", residual=None, oq=None, challenge=None, external=None):
        aid = f"ANS-{self.code}-{n:03d}"
        a = {"id": aid, "title": title, "status": status, "status_rationale": status_rationale,
             "target_answer": target, "current_practice": current, "intended_practice": intended,
             "provable": provable, "customer_statement": stmt, "customer_statement_kind": stmt_kind,
             "assurance_independence": independence}
        if external: a["external_assurance"] = external
        a["controls"] = controls
        a["evidence_requirements"] = evrs
        if policies: a["policies"] = policies
        if requirements: a["requirements"] = requirements
        if freshness: a["evidence_freshness"] = freshness
        a.update({"evidence_mechanism": mechanism, "automation_potential": automation,
                  "disclosure_classification": disclosure, "implementation_cost": impl,
                  "recurring_cost": rec, "cost_basis": COST_BASIS, "owner": OWNER})
        if residual: a["residual_risks"] = residual
        if oq: a["open_questions"] = oq
        if challenge: a["challenge"] = challenge
        a["history"] = HIST
        self.answers.append(a)
        self.au_index[n] = a
        return aid

    def q(self, au, sub, text, concern, risk, refs, cls, imp, alts=None, ind=None, jur=None, prod=None,
          reg=None, note=None, disc="authenticated-prospect", oq=None):
        n = len(self.questions) + 1
        a = self.au_index[au]
        rec = {"id": f"DDQ-{self.code}-{n:04d}", "question": text}
        if alts: rec["alternatives"] = alts
        rec.update({"category": self.code, "subcategory": sub, "business_concern": concern,
                    "risk_addressed": risk, "source_refs": refs, "industries": ind or ["all"],
                    "jurisdictions": jur or ["US-federal", "US-states"], "products": prod or ["unbound"]})
        rec["regulatory_authority"] = reg or "none"
        rec.update({"requirement_classification": cls, "customer_importance": imp, "answer_unit": a["id"]})
        if note: rec["answer_scope_note"] = note
        rec["controls"] = a["controls"]
        if a.get("policies"): rec["policies"] = a["policies"]
        if a.get("requirements"): rec["requirements"] = a["requirements"]
        rec["evidence_requirements"] = a["evidence_requirements"]
        rec["disclosure_classification"] = disc
        if oq: rec["open_questions"] = oq
        rec["history"] = HIST
        self.questions.append(rec)

    def write(self):
        for d, rows in (("questions", self.questions), ("answers", self.answers),
                        ("controls", self.controls), ("evidence-requirements", self.evrs)):
            with open(os.path.join(REPO, d, f"{self.code}.jsonl"), "w", encoding="utf-8") as f:
                for r in rows:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")


def challenge(**kw):
    return kw
