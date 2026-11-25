"""Shared helpers for building AIG/AIS/AIA/TPR/SUB/REG/AML question bank records as data."""

HIST = [{"date": "2026-11-25", "change": "created", "by": "research-agent"}]
COST_BASIS = "order-of-magnitude judgment, not sourced"

BASIS = {"d": "directly-documented", "r": "reasonably-inferred", "u": "unknown"}
REL = {"m": "maps-to", "i": "informed-by", "f": "derived-from", "c": "contradicts"}


def ref(spec):
    """'SRC-ID|locator|basis|relation'; locator may be empty; basis and relation optional."""
    parts = spec.split("|")
    sid = parts[0]
    loc = parts[1] if len(parts) > 1 else ""
    basis = parts[2] if len(parts) > 2 and parts[2] else ("d" if sid.startswith("SRC-ECH") else "r")
    rel = parts[3] if len(parts) > 3 and parts[3] else ("i" if sid.startswith("SRC-ECH") else "m")
    out = {"source_id": sid, "relation": REL[rel], "basis": BASIS[basis]}
    if loc:
        out["locator"] = loc
    return out


class Cat:
    def __init__(self, code, industries, jurisdictions, products, disclosure="nda",
                 regulatory_authority=None):
        self.code = code
        self.industries = industries
        self.jurisdictions = jurisdictions
        self.products = products
        self.disclosure = disclosure
        self.regulatory_authority = regulatory_authority
        self.aus, self.ctls, self.evrs, self.qs = [], [], [], []

    def aid(self, n):
        return f"ANS-{self.code}-{n:03d}"

    def cid(self, n):
        return f"ECTL-{self.code}-{n:03d}"

    def eid(self, n):
        return f"EVR-{self.code}-{n:03d}"

    def au(self, n, **kw):
        kw["n"] = n
        self.aus.append(kw)

    def ctl(self, n, **kw):
        kw["n"] = n
        self.ctls.append(kw)

    def evr(self, n, **kw):
        kw["n"] = n
        self.evrs.append(kw)

    def q(self, au, sub, text, concern, risk, refs, cls, imp, alts=None, **kw):
        self.qs.append(dict(au=au, sub=sub, text=text, concern=concern, risk=risk, refs=refs,
                            cls=cls, imp=imp, alts=alts or [], kw=kw))

    def build_aus(self):
        out = []
        for a in self.aus:
            r = {
                "id": self.aid(a["n"]),
                "title": a["title"],
                "status": a["status"],
                "status_rationale": a["rationale"],
                "target_answer": a["target"],
                "current_practice": a["current"],
                "intended_practice": a["intended"],
                "provable": a["provable"],
                "customer_statement": a["statement"],
                "customer_statement_kind": a["kind"],
                "assurance_independence": a.get("independence", "none"),
                "controls": [self.cid(x) for x in a["controls"]],
                "evidence_requirements": [self.eid(x) for x in a["evrs"]],
            }
            for k in ("policies", "requirements"):
                if a.get(k):
                    r[k] = a[k]
            r["evidence_freshness"] = a.get("freshness", "P90D")
            r["evidence_mechanism"] = a.get("mechanism", "not-defined")
            r["automation_potential"] = a.get("automation", "partial")
            r["disclosure_classification"] = a.get("disclosure", self.disclosure)
            r["implementation_cost"] = a.get("impl_cost", "medium")
            r["recurring_cost"] = a.get("rec_cost", "low")
            r["cost_basis"] = COST_BASIS
            r["owner"] = a["owner"]
            if a.get("residual"):
                r["residual_risks"] = a["residual"]
            if a.get("open"):
                r["open_questions"] = a["open"]
            if a.get("challenge"):
                r["challenge"] = a["challenge"]
            r["history"] = HIST
            out.append(r)
        return out

    def build_ctls(self):
        out = []
        for c in self.ctls:
            r = {
                "id": self.cid(c["n"]),
                "title": c["title"],
                "objective": c["objective"],
                "control_type": c["type"],
                "assurance_level": c["level"],
                "implementing_systems": c["systems"],
            }
            if c.get("policies"):
                r["policies"] = c["policies"]
            if c.get("related"):
                r["related_external_controls"] = c["related"]
            if c.get("cwe"):
                r["cwe"] = c["cwe"]
            if c.get("refs"):
                r["framework_refs"] = [ref(x) for x in c["refs"]]
            r["status"] = c.get("status", "proposed-target-state")
            r["evidence_requirements"] = [self.eid(x) for x in c["evrs"]]
            r["owner"] = c["owner"]
            if c.get("residual"):
                r["residual_risks"] = c["residual"]
            if c.get("notes"):
                r["notes"] = c["notes"]
            out.append(r)
        return out

    def build_evrs(self):
        out = []
        for e in self.evrs:
            r = {
                "id": self.eid(e["n"]),
                "title": e["title"],
                "description": e["description"],
                "producer": e.get("producer", "not yet assigned"),
                "mechanism": e["mechanism"],
                "freshness": e["freshness"],
            }
            if e.get("format"):
                r["format"] = e["format"]
            if e.get("fields"):
                r["provenance_fields"] = e["fields"]
            if e.get("signing"):
                r["signing"] = e["signing"]
            if e.get("retention"):
                r["retention"] = e["retention"]
            r["independence"] = e.get("independence", "first-party")
            r["disclosure_classification"] = e.get("disclosure", self.disclosure)
            r["status"] = e.get("status", "proposed-target-state")
            if e.get("notes"):
                r["notes"] = e["notes"]
            out.append(r)
        return out

    def build_qs(self):
        aus = {a["n"]: a for a in self.aus}
        out = []
        for i, q in enumerate(self.qs, 1):
            a = aus[q["au"]]
            kw = q["kw"]
            r = {"id": f"DDQ-{self.code}-{i:04d}", "question": q["text"]}
            if q["alts"]:
                r["alternatives"] = q["alts"]
            r.update({
                "category": self.code,
                "subcategory": q["sub"],
                "business_concern": q["concern"],
                "risk_addressed": q["risk"],
                "source_refs": [ref(x) for x in q["refs"]],
                "industries": kw.get("industries", self.industries),
                "jurisdictions": kw.get("jurisdictions", self.jurisdictions),
                "products": kw.get("products", self.products),
            })
            ra = kw.get("authority", self.regulatory_authority)
            if ra:
                r["regulatory_authority"] = ra
            r["requirement_classification"] = q["cls"]
            r["customer_importance"] = q["imp"]
            r["answer_unit"] = self.aid(q["au"])
            if kw.get("scope"):
                r["answer_scope_note"] = kw["scope"]
            r["controls"] = [self.cid(x) for x in a["controls"]]
            if a.get("policies"):
                r["policies"] = a["policies"]
            if a.get("requirements"):
                r["requirements"] = a["requirements"]
            r["evidence_requirements"] = [self.eid(x) for x in a["evrs"]]
            r["disclosure_classification"] = kw.get("disclosure", self.disclosure)
            if kw.get("open"):
                r["open_questions"] = kw["open"]
            r["history"] = HIST
            out.append(r)
        return out


def challenge(**kw):
    keys = {
        "intent": "customer_intent", "adverse": "adverse_outcome",
        "conv_eff": "conventional_control_effectiveness", "legal": "legally_required",
        "contract": "contractually_required", "history": "historical_convention",
        "elim": "architectural_elimination", "auto": "automatic_enforcement",
        "cont": "continuous_evidence", "alt": "stronger_alternative",
        "verif": "alternative_verifiable", "accept": "customer_acceptance_likelihood",
        "invalid": "invalidating_conditions", "conv_cost": "conventional_cost",
        "alt_cost": "alternative_cost", "alt_risk": "alternative_risks",
        "pro": "supporting_arguments", "con": "opposing_arguments",
        "tech": "technical_effectiveness", "inst": "institutional_acceptance",
    }
    return {keys[k]: v for k, v in kw.items()}
