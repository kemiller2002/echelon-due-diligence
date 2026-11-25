import json, sys, re, glob
sys.path.insert(0, __import__("os").path.dirname(__file__))
from dafcommon import build, write, REPO
import daf, grt, chv, con, don, wlb
import jsonschema

mods = [("DAF", daf), ("GRT", grt), ("CHV", chv), ("CON", con), ("DON", don), ("WLB", wlb)]
schemas = {k: json.load(open(f"{REPO}/schemas/dd/{f}.schema.json")) for k, f in
           (("questions", "question"), ("answers", "answer-unit"), ("controls", "control"), ("evidence", "evidence-requirement"))}
seeds = set()
sd = json.load(open(f"{REPO}/sources/SEED-IDS.json"))
for v in sd.values():
    for x in v:
        if x["id"].startswith("SRC-") and "*" not in x["id"]:
            seeds.add(x["id"])
base = set()
for l in open("/home/user/unbound/requirements/baseline/baseline.jsonl"):
    base.add(json.loads(l)["id"])
import csv
ctl = {r["control_id"] for r in csv.DictReader(open("/home/user/unbound/requirements/governance/MASTER-ENTERPRISE-CONTROL-MATRIX.csv"))}
SEC = {"SEC-DB-001","SEC-UI-001","SEC-UI-002","SEC-LANG-001","SEC-LANG-002","SEC-EXEC-001","SEC-DATA-001","SEC-CRYPTO-001","SEC-AUTH-001","SEC-SUPPLY-001"}
errs = []
tot = {}
for cat, m in mods:
    recs = build(cat, m.units)
    for kind, rows in zip(("questions", "answers", "controls", "evidence"), recs):
        v = jsonschema.Draft202012Validator(schemas[kind])
        for r in rows:
            for e in v.iter_errors(r):
                errs.append((r["id"], e.message))
            s = json.dumps(r, ensure_ascii=False)
            if "—" in s or "–" in s:
                errs.append((r["id"], "dash"))
            for ref in r.get("source_refs", []) + r.get("framework_refs", []):
                if ref["source_id"] not in seeds:
                    errs.append((r["id"], "unseeded " + ref["source_id"]))
            for x in r.get("requirements", []):
                if x not in base:
                    errs.append((r["id"], "missing req " + x))
            for x in r.get("related_external_controls", []):
                if x not in ctl:
                    errs.append((r["id"], "missing ctl " + x))
            for x in r.get("policies", []):
                if x not in SEC:
                    errs.append((r["id"], "bad policy " + x))
    tot[cat] = write(cat, recs)
    tot[cat]["challenge"] = sum(1 for a in recs[1] if "challenge" in a)
    tot[cat]["statuses"] = sorted({a["status"] for a in recs[1]})
print(json.dumps(tot, indent=1))
print(len(errs), "errors")
for e in errs[:50]:
    print(e)
