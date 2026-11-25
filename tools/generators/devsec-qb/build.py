import json, re, sys, os, itertools, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jsonschema
import app, api, sdl, arc, chg, scs

ROOT = "/home/user/echelon-due-diligence"
WRITE = "--write" in sys.argv
mods = {"APP": app, "API": api, "SDL": sdl, "ARC": arc, "CHG": chg, "SCS": scs}

schemas = {k: json.load(open(f"{ROOT}/schemas/dd/{f}.schema.json")) for k, f in
           [("q", "question"), ("a", "answer-unit"), ("c", "control"), ("e", "evidence-requirement")]}
seed = json.load(open(f"{ROOT}/sources/SEED-IDS.json"))
src_ids = {x["id"] for g in seed.values() for x in g}
base_ids = {json.loads(l)["id"] for l in open("/home/user/unbound/requirements/baseline/baseline.jsonl")}
ctrl_ids = {r["control_id"] for r in csv.DictReader(open("/home/user/unbound/requirements/governance/MASTER-ENTERPRISE-CONTROL-MATRIX.csv"))}
sec_ids = {"SEC-DB-001", "SEC-UI-001", "SEC-UI-002", "SEC-LANG-001", "SEC-LANG-002", "SEC-EXEC-001", "SEC-DATA-001", "SEC-CRYPTO-001", "SEC-AUTH-001", "SEC-SUPPLY-001"}
errors = []
allq = []
summary = {}
for code, m in mods.items():
    q, a, c, e = m.RECORDS
    summary[code] = (len(q), len(a), len(c), len(e), sum(1 for x in a if "challenge" in x))
    for kind, recs in (("q", q), ("a", a), ("c", c), ("e", e)):
        v = jsonschema.Draft202012Validator(schemas[kind])
        for r in recs:
            for err in v.iter_errors(r):
                errors.append(f"SCHEMA {r['id']}: {err.message[:200]}")
            s = json.dumps(r, ensure_ascii=False)
            if "—" in s or "–" in s:
                errors.append(f"DASH {r['id']}")
            for ref in r.get("source_refs", []) + r.get("framework_refs", []):
                if ref["source_id"] not in src_ids:
                    errors.append(f"SRC {r['id']}: {ref['source_id']}")
            for p in r.get("policies", []):
                if p not in sec_ids:
                    errors.append(f"POLICY {r['id']}: {p}")
            for x in r.get("requirements", []) + r.get("related_external_controls", []):
                if x not in base_ids and x not in ctrl_ids:
                    errors.append(f"REQ {r['id']}: {x}")
    cids = {x["id"] for x in c}; eids = {x["id"] for x in e}; aids = {x["id"] for x in a}
    for r in q + a + c:
        for x in r.get("controls", []):
            if x not in cids: errors.append(f"DANGLING ctl {r['id']} {x}")
        for x in r.get("evidence_requirements", []):
            if x not in eids: errors.append(f"DANGLING evr {r['id']} {x}")
    for r in q:
        if r["answer_unit"] not in aids: errors.append(f"DANGLING au {r['id']}")
    used_a = {r["answer_unit"] for r in q}
    for x in aids - used_a: errors.append(f"ORPHAN AU {x}")
    used_c = {x for r in q + a for x in r.get("controls", [])}
    for x in cids - used_c: errors.append(f"ORPHAN CTL {x}")
    used_e = {x for r in q + a + c for x in r.get("evidence_requirements", [])}
    for x in eids - used_e: errors.append(f"ORPHAN EVR {x}")
    for x in a:
        k = x["customer_statement_kind"]; s = x["status"]
        if k == "current-fact" and s not in ("verified-operational", "implemented-not-independently-verified"): errors.append(f"HONESTY {x['id']}")
        if k == "qualified-current-fact" and s not in ("verified-operational", "implemented-not-independently-verified", "partially-implemented"): errors.append(f"HONESTY {x['id']}")
    cnt = {}
    for r in q: cnt[r["answer_unit"]] = cnt.get(r["answer_unit"], 0) + 1
    for k_, n in cnt.items():
        if n < 3 or n > 8: errors.append(f"RATIO {k_} has {n} questions")
    allq += q

stop = set("the a an of to and or for in on is are do does you your with how what which by be that this any all it its as at from".split())
tok = lambda s: {t for t in re.findall(r"[a-z0-9]+", s.lower()) if t not in stop}
toks = [(r["id"], tok(r["question"])) for r in allq]
for (i, a_), (j, b_) in itertools.combinations(toks, 2):
    u = len(a_ | b_)
    if u and len(a_ & b_) / u >= 0.6:
        errors.append(f"NEARDUP {i} ~ {j} {len(a_ & b_)/u:.2f}")

for k, v in summary.items():
    print(k, "q=%d a=%d c=%d e=%d challenge=%d" % v)
print("\n".join(errors) if errors else "NO ERRORS")

if WRITE and not [x for x in errors if not x.startswith("NEARDUP")]:
    for code, m in mods.items():
        q, a, c, e = m.RECORDS
        for d, recs in (("questions", q), ("answers", a), ("controls", c), ("evidence-requirements", e)):
            path = f"{ROOT}/{d}/{code}.jsonl"
            if os.path.exists(path):
                print("EXISTS, overwriting own file", path)
            with open(path, "w", encoding="utf-8") as f:
                for r in recs:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("written")
