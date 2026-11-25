import json, csv, re, sys, os
import jsonschema
import vul, pen, scn, mon, ir
from common import REPO

MIN = {"VUL": 35, "PEN": 30, "SCN": 35, "MON": 40, "IR": 40}
cats = [m.build() for m in (vul, pen, scn, mon, ir)]

schemas = {k: json.load(open(f"{REPO}/schemas/dd/{f}.schema.json")) for k, f in
           (("q", "question"), ("a", "answer-unit"), ("c", "control"), ("e", "evidence-requirement"))}
seed = json.load(open(f"{REPO}/sources/SEED-IDS.json"))
seed_ids = {x["id"] for g in seed.values() for x in g}
ub = set(json.loads(l)["id"] for l in open("/home/user/unbound/requirements/baseline/baseline.jsonl"))
for r in csv.DictReader(open("/home/user/unbound/requirements/governance/MASTER-ENTERPRISE-CONTROL-MATRIX.csv")):
    ub.add(r["control_id"])
sec = {"SEC-DB-001", "SEC-UI-001", "SEC-UI-002", "SEC-LANG-001", "SEC-LANG-002", "SEC-EXEC-001", "SEC-DATA-001", "SEC-CRYPTO-001", "SEC-AUTH-001", "SEC-SUPPLY-001"}
known_ext = ub | sec

errs = []
def V(kind, rec):
    for e in jsonschema.Draft202012Validator(schemas[kind]).iter_errors(rec):
        errs.append(f"{rec.get('id')}: {e.message}")

def toks(s):
    stop = set("the a an of to and or for in on is are do does you your with how what which by be that this any all it its as at from".split())
    return {t for t in re.findall(r"[a-z0-9]+", s.lower()) if t not in stop}

for c in cats:
    ctl_ids = {x["id"] for x in c.controls}; evr_ids = {x["id"] for x in c.evrs}; au_ids = {x["id"] for x in c.answers}
    for q in c.questions:
        V("q", q)
        for r in q["source_refs"]:
            if r["source_id"] not in seed_ids: errs.append(f"{q['id']} unseeded {r['source_id']}")
    for a in c.answers:
        V("a", a)
        for x in a["controls"]:
            if x not in ctl_ids: errs.append(f"{a['id']} dangling {x}")
        for x in a["evidence_requirements"]:
            if x not in evr_ids: errs.append(f"{a['id']} dangling {x}")
        for x in a.get("policies", []) + a.get("requirements", []):
            if x not in known_ext: errs.append(f"{a['id']} unknown ext {x}")
        if a["customer_statement_kind"] == "current-fact" and a["status"] not in ("verified-operational", "implemented-not-independently-verified"):
            errs.append(f"{a['id']} honesty")
    for k in c.controls:
        V("c", k)
        for r in k.get("framework_refs", []):
            if r["source_id"] not in seed_ids: errs.append(f"{k['id']} unseeded {r['source_id']}")
        for x in k.get("policies", []) + k.get("related_external_controls", []):
            if x not in known_ext: errs.append(f"{k['id']} unknown ext {x}")
        for x in k["evidence_requirements"]:
            if x not in evr_ids: errs.append(f"{k['id']} dangling {x}")
    for e in c.evrs: V("e", e)
    used_au = {q["answer_unit"] for q in c.questions}
    if used_au != au_ids: errs.append(f"{c.code} orphan AUs {au_ids - used_au}")
    used_ctl = {x for a in c.answers for x in a["controls"]}
    if used_ctl != ctl_ids: errs.append(f"{c.code} orphan controls {ctl_ids - used_ctl}")
    used_evr = {x for a in c.answers for x in a["evidence_requirements"]} | {x for k in c.controls for x in k["evidence_requirements"]}
    if used_evr != evr_ids: errs.append(f"{c.code} orphan evrs {evr_ids - used_evr}")
    if len(c.questions) < MIN[c.code]: errs.append(f"{c.code} only {len(c.questions)}")
    qs = [(q["id"], toks(q["question"])) for q in c.questions]
    for i in range(len(qs)):
        for j in range(i + 1, len(qs)):
            a, b = qs[i][1], qs[j][1]
            s = len(a & b) / len(a | b)
            if s >= 0.5: print("similar", qs[i][0], qs[j][0], round(s, 2))
    blob = json.dumps([c.questions, c.answers, c.controls, c.evrs], ensure_ascii=False)
    if "—" in blob: errs.append(f"{c.code} em dash")
    for w in ("colour", "organisation", "behaviour", "analyse", "prioritis", "authoris", "utilis", "licence"):
        if w in blob.lower(): errs.append(f"{c.code} British spelling {w}")

if errs:
    print("\n".join(errs)); sys.exit(1)
for c in cats:
    c.write()
    print(c.code, "questions", len(c.questions), "answers", len(c.answers), "controls", len(c.controls), "evrs", len(c.evrs),
          "challenges", sum(1 for a in c.answers if "challenge" in a),
          "statuses", {s: sum(1 for a in c.answers if a["status"] == s) for s in sorted({a["status"] for a in c.answers})})
