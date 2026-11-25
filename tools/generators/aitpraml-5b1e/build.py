import json, re, sys, csv, itertools
import jsonschema
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import aig, ais, aia, tpr, sub, reg, aml

ROOT = "/home/user/echelon-due-diligence"
WRITE = "--write" in sys.argv
cats = [aig.C, ais.C, aia.C, tpr.C, sub.C, reg.C, aml.C]

schemas = {k: json.load(open(f"{ROOT}/schemas/dd/{k}.schema.json")) for k in
           ["question", "answer-unit", "control", "evidence-requirement"]}

seed = json.load(open(f"{ROOT}/sources/SEED-IDS.json"))
seed_ids = {x["id"] for v in seed.values() for x in v if not x["id"].endswith("*")}

baseline_ids = {json.loads(l)["id"] for l in open("/home/user/unbound/requirements/baseline/baseline.jsonl")}
matrix_ids = {r["control_id"] for r in csv.DictReader(open("/home/user/unbound/requirements/governance/MASTER-ENTERPRISE-CONTROL-MATRIX.csv"))}
sec_ids = {"SEC-DB-001", "SEC-UI-001", "SEC-UI-002", "SEC-LANG-001", "SEC-LANG-002", "SEC-EXEC-001",
           "SEC-DATA-001", "SEC-CRYPTO-001", "SEC-AUTH-001", "SEC-SUPPLY-001"}
known_ext = baseline_ids | matrix_ids | sec_ids

errors = []
unknown_src = set()
stop = set("the a an of to and or for in on is are do does you your with how what which by be that this any all it its as at from".split())

def tok(s):
    return {t for t in re.findall(r"[a-z0-9]+", s.lower()) if t not in stop}

def all_strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from all_strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from all_strings(v)

summary = {}
all_q = []
for c in cats:
    out = {"questions": c.build_qs(), "answers": c.build_aus(),
           "controls": c.build_ctls(), "evidence-requirements": c.build_evrs()}
    kinds = {"questions": "question", "answers": "answer-unit", "controls": "control",
             "evidence-requirements": "evidence-requirement"}
    ctl_ids = {r["id"] for r in out["controls"]}
    evr_ids = {r["id"] for r in out["evidence-requirements"]}
    au_ids = {r["id"] for r in out["answers"]}
    used_ctl, used_evr, used_au = set(), set(), set()
    for d, recs in out.items():
        for r in recs:
            try:
                jsonschema.validate(r, schemas[kinds[d]])
            except jsonschema.ValidationError as e:
                errors.append(f"{r['id']}: {e.message}")
            for s in all_strings(r):
                if "—" in s:
                    errors.append(f"{r['id']}: em dash")
            for ref in r.get("source_refs", []) + r.get("framework_refs", []):
                sid = ref["source_id"]
                if not (sid in seed_ids or sid.startswith("SRC-ECH-")):
                    unknown_src.add(sid)
                if sid.startswith("SRC-ECH-") and sid not in seed_ids:
                    unknown_src.add(sid)
            for x in r.get("controls", []):
                if x not in ctl_ids: errors.append(f"{r['id']}: dangling {x}")
                used_ctl.add(x)
            for x in r.get("evidence_requirements", []):
                if x not in evr_ids: errors.append(f"{r['id']}: dangling {x}")
                used_evr.add(x)
            if "answer_unit" in r:
                if r["answer_unit"] not in au_ids: errors.append(f"{r['id']}: dangling AU")
                used_au.add(r["answer_unit"])
            for k in ("requirements", "related_external_controls", "policies"):
                for x in r.get(k, []):
                    if x not in known_ext:
                        errors.append(f"{r['id']}: {k} unknown {x}")
            for ref in r.get("source_refs", []):
                if ref["source_id"].startswith("SRC-ECH-UNB") and ref.get("locator") and re.match(r"^[A-Z]", ref["locator"]):
                    if ref["locator"] not in known_ext:
                        errors.append(f"{r['id']}: locator unknown {ref['locator']}")
            if d == "answers":
                if r["customer_statement_kind"] == "current-fact" and r["status"] not in ("verified-operational", "implemented-not-independently-verified"):
                    errors.append(f"{r['id']}: aspirational current-fact")
                if r["customer_statement_kind"] == "qualified-current-fact" and r["status"] not in ("verified-operational", "implemented-not-independently-verified", "partially-implemented"):
                    errors.append(f"{r['id']}: aspirational qualified")
    for x in ctl_ids - used_ctl: errors.append(f"orphan control {x}")
    for x in evr_ids - used_evr: errors.append(f"orphan evr {x}")
    for x in au_ids - used_au: errors.append(f"orphan au {x}")
    all_q += out["questions"]
    summary[c.code] = {d: len(v) for d, v in out.items()}
    summary[c.code]["challenge"] = sum(1 for a in out["answers"] if "challenge" in a)
    if WRITE:
        for d, recs in out.items():
            with open(f"{ROOT}/{d}/{c.code}.jsonl", "w", encoding="utf-8") as f:
                for r in recs:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")

# near duplicates
toks = [(q["id"], tok(q["question"])) for q in all_q]
for (ia, ta), (ib, tb) in itertools.combinations(toks, 2):
    u = len(ta | tb)
    if u and len(ta & tb) / u >= 0.6:
        print("NEAR", ia, ib, round(len(ta & tb) / u, 2))

print(json.dumps(summary, indent=1))
print("unknown sources:", sorted(unknown_src))
print("errors:", len(errors))
for e in errors: print(" ", e)
