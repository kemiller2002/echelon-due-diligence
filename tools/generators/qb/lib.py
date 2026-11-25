"""Shared builders for the canonical question bank (ISP, ASM, IAM, AUN, AUZ, TEN).

Records are built as data and serialized with json.dumps(ensure_ascii=False).
"""
import json
import os

REPO = "/home/user/echelon-due-diligence"
HIST = [{"date": "2026-11-25", "change": "created", "by": "research-agent"}]
COST_BASIS = "order-of-magnitude judgment, not sourced"

FS = ["financial-services", "banking", "wealth-management", "donor-advised-funds"]
BANK = ["banking", "financial-services"]
DAF = ["donor-advised-funds", "nonprofit", "wealth-management"]
ALL = ["all"]
ENT = ["enterprise-software", "financial-services", "banking", "donor-advised-funds"]
WM = ["wealth-management", "financial-services", "donor-advised-funds"]

USF = ["US-federal"]
GLOBAL = ["global"]
NY = ["US-state:NY"]

UNB = ["unbound"]
ALLP = ["all-echelon-products"]
ORG = ["echelon-organization"]
ORGALL = ["echelon-organization", "all-echelon-products"]


def s(source_id, locator=None, rel="maps-to", basis="reasonably-inferred"):
    r = {"source_id": source_id, "relation": rel, "basis": basis}
    if locator:
        r["locator"] = locator
    return r


def d(source_id, locator=None, rel="maps-to"):
    """Directly documented reference."""
    return s(source_id, locator, rel, "directly-documented")


def e(source_id, locator=None):
    """Echelon-internal reference (directly documented, informed-by)."""
    return s(source_id, locator, "informed-by", "directly-documented")


class Category:
    def __init__(self, code):
        self.code = code
        self.aus = []
        self.controls = []
        self.evrs = []
        self.questions = []
        self.au_meta = {}
        self._qn = 0

    # ---------- answer units ----------
    def au(self, n, title, sub, concern, status, rationale, target, current, intended,
           provable, stmt, kind, controls, evrs, policies=None, reqs=None,
           fresh="P1D", mech="not-defined", auto="high", disc="authenticated-prospect",
           impl="medium", rec="low", owner="Unassigned; proposed Security Lead",
           residual=None, oq=None, challenge=None, assur="none", ext=None):
        aid = f"ANS-{self.code}-{n:03d}"
        rec_ = {
            "id": aid,
            "title": title,
            "status": status,
            "status_rationale": rationale,
            "target_answer": target,
            "current_practice": current,
            "intended_practice": intended,
            "provable": provable,
            "customer_statement": stmt,
            "customer_statement_kind": kind,
            "assurance_independence": assur,
            "controls": [f"ECTL-{self.code}-{c:03d}" for c in controls],
            "evidence_requirements": [f"EVR-{self.code}-{v:03d}" for v in evrs],
            "policies": policies or [],
            "requirements": reqs or [],
            "evidence_freshness": fresh,
            "evidence_mechanism": mech,
            "automation_potential": auto,
            "disclosure_classification": disc,
            "implementation_cost": impl,
            "recurring_cost": rec,
            "cost_basis": COST_BASIS,
            "owner": owner,
            "residual_risks": residual or [],
            "open_questions": oq or [],
            "history": HIST,
        }
        if ext:
            rec_["external_assurance"] = ext
        if challenge:
            rec_["challenge"] = challenge
        self.aus.append(rec_)
        self.au_meta[n] = {"sub": sub, "concern": concern, "rec": rec_}
        return aid

    # ---------- controls ----------
    def ctl(self, n, title, objective, ctype, level, systems, status="proposed-target-state",
            evrs=None, policies=None, related=None, cwe=None, refs=None,
            owner="Unassigned; proposed Security Lead", residual=None, notes=None):
        r = {
            "id": f"ECTL-{self.code}-{n:03d}",
            "title": title,
            "objective": objective,
            "control_type": ctype,
            "assurance_level": level,
            "implementing_systems": systems,
            "status": status,
            "evidence_requirements": [f"EVR-{self.code}-{v:03d}" for v in (evrs or [])],
            "owner": owner,
        }
        if policies:
            r["policies"] = policies
        if related:
            r["related_external_controls"] = related
        if cwe:
            r["cwe"] = cwe
        if refs:
            r["framework_refs"] = refs
        if residual:
            r["residual_risks"] = residual
        if notes:
            r["notes"] = notes
        self.controls.append(r)

    # ---------- evidence requirements ----------
    def evr(self, n, title, description, producer, mech, fresh, fmt=None, prov=None,
            signing=None, retention="Not yet defined; to be set with auditor and counsel (SOC2-023)",
            indep="first-party", disc="customer-only", status="proposed-target-state", notes=None):
        r = {
            "id": f"EVR-{self.code}-{n:03d}",
            "title": title,
            "description": description,
            "producer": producer,
            "mechanism": mech,
            "freshness": fresh,
            "independence": indep,
            "disclosure_classification": disc,
            "status": status,
        }
        if fmt:
            r["format"] = fmt
        if prov:
            r["provenance_fields"] = prov
        if signing:
            r["signing"] = signing
        if retention:
            r["retention"] = retention
        if notes:
            r["notes"] = notes
        self.evrs.append(r)

    # ---------- questions ----------
    def q(self, au, text, risk, srcs, cls="contractual-common", imp="high", ind=None,
          jur=None, alts=None, sub=None, concern=None, reg=None, note=None, oq=None,
          prod=None, disc="public"):
        self._qn += 1
        meta = self.au_meta[au]
        rec = meta["rec"]
        r = {
            "id": f"DDQ-{self.code}-{self._qn:04d}",
            "question": text,
        }
        if alts:
            r["alternatives"] = alts
        r.update({
            "category": self.code,
            "subcategory": sub or meta["sub"],
            "business_concern": concern or meta["concern"],
            "risk_addressed": risk,
            "source_refs": srcs,
            "industries": ind or FS,
            "jurisdictions": jur or USF,
            "products": prod or UNB,
        })
        if reg:
            r["regulatory_authority"] = reg
        r.update({
            "requirement_classification": cls,
            "customer_importance": imp,
            "answer_unit": rec["id"],
        })
        if note:
            r["answer_scope_note"] = note
        r["controls"] = list(rec["controls"])
        if rec["policies"]:
            r["policies"] = list(rec["policies"])
        if rec["requirements"]:
            r["requirements"] = list(rec["requirements"])
        r["evidence_requirements"] = list(rec["evidence_requirements"])
        r["disclosure_classification"] = disc
        if oq:
            r["open_questions"] = oq
        r["history"] = HIST
        self.questions.append(r)

    # ---------- output ----------
    def emit(self):
        out = {
            "questions": self.questions,
            "answers": self.aus,
            "controls": self.controls,
            "evidence-requirements": self.evrs,
        }
        for folder, recs in out.items():
            path = os.path.join(REPO, folder, f"{self.code}.jsonl")
            with open(path, "w", encoding="utf-8") as f:
                for r in recs:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
        return {k: len(v) for k, v in out.items()}
