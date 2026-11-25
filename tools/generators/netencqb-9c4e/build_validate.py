import sys, json, re, glob, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jsonschema
from netenc_lib import write, REPO
import net, inf, cld, end, enc
mods = {"NET": net, "INF": inf, "CLD": cld, "END": end, "ENC": enc}
counts = {}
for cat, m in mods.items():
    counts[cat] = write(cat, m.questions, m.answers, m.controls, m.evrs)
print(json.dumps(counts, indent=1))

sch = {k: json.load(open(f"{REPO}/schemas/dd/{k}.schema.json")) for k in ["question", "answer-unit", "control", "evidence-requirement"]}
seed = json.load(open(f"{REPO}/sources/SEED-IDS.json"))
seed_ids = {e["id"] for v in seed.values() if isinstance(v, list) for e in v}
base_ids = {json.loads(l)["id"] for l in open("/home/user/unbound/requirements/baseline/baseline.jsonl")}
ctrl_ids = {l.split(",")[0].strip('"') for l in open("/home/user/unbound/requirements/governance/MASTER-ENTERPRISE-CONTROL-MATRIX.csv")}
soc2 = set(re.findall(r"SOC2-0\d\d", open("/home/user/unbound/requirements/governance/SOC2-CONTROLS-EVIDENCE-AND-ENTERPRISE-DIRECTIVE.md").read()))
known_req = base_ids | ctrl_ids | soc2
SEC = {"SEC-DB-001","SEC-UI-001","SEC-UI-002","SEC-LANG-001","SEC-LANG-002","SEC-EXEC-001","SEC-DATA-001","SEC-CRYPTO-001","SEC-AUTH-001","SEC-SUPPLY-001"}
errs = []
all_ctrl, all_evr, all_au = set(), set(), set()
recs = {}
for cat in mods:
    for kind, folder in [("question","questions"),("answer-unit","answers"),("control","controls"),("evidence-requirement","evidence-requirements")]:
        path = f"{REPO}/{folder}/{cat}.jsonl"
        raw = open(path, encoding="utf-8").read()
        if "—" in raw or "–" in raw: errs.append(f"dash in {path}")
        rs = [json.loads(l) for l in raw.splitlines()]
        recs[(cat, kind)] = rs
        v = jsonschema.Draft202012Validator(sch[kind])
        for x in rs:
            for e in v.iter_errors(x): errs.append(f"{x['id']}: {e.message[:200]}")
        ids = [x["id"] for x in rs]
        if len(ids) != len(set(ids)): errs.append(f"dup ids {path}")
        if kind == "control": all_ctrl |= set(ids)
        if kind == "evidence-requirement": all_evr |= set(ids)
        if kind == "answer-unit": all_au |= set(ids)

def chk_refs(x, refs):
    for r in refs:
        if r["source_id"] not in seed_ids: errs.append(f"{x['id']}: unseeded {r['source_id']}")
for (cat, kind), rs in recs.items():
    for x in rs:
        for c in x.get("controls", []):
            if c not in all_ctrl: errs.append(f"{x['id']}: missing control {c}")
        for c in x.get("evidence_requirements", []):
            if c not in all_evr: errs.append(f"{x['id']}: missing evr {c}")
        for p in x.get("policies", []):
            if p not in SEC: errs.append(f"{x['id']}: bad policy {p}")
        for q in x.get("requirements", []) + x.get("related_external_controls", []):
            if q not in known_req: errs.append(f"{x['id']}: unknown req {q}")
        chk_refs(x, x.get("source_refs", []) + x.get("framework_refs", []))
        if kind == "question" and x["answer_unit"] not in all_au: errs.append(f"{x['id']}: missing AU")
        if kind == "answer-unit":
            if x["customer_statement_kind"] in ("current-fact",) and x["status"] not in ("verified-operational","implemented-not-independently-verified"):
                errs.append(f"{x['id']}: current-fact with status {x['status']}")
    if kind == "answer-unit":
        used = {q["answer_unit"] for q in recs[(cat, "question")]}
        for x in rs:
            if x["id"] not in used: errs.append(f"{x['id']}: no questions")
        per = [sum(1 for q in recs[(cat,'question')] if q['answer_unit']==x['id']) for x in rs]
        print(cat, "questions per AU", per, "challenges", sum(1 for x in rs if "challenge" in x))
# controls/evrs referenced at least once
refd_c = {c for rs in recs.values() for x in rs for c in x.get("controls", [])}
refd_e = {c for rs in recs.values() for x in rs for c in x.get("evidence_requirements", [])}
for c in all_ctrl - refd_c: errs.append(f"unreferenced control {c}")
for c in all_evr - refd_e: errs.append(f"unreferenced evr {c}")
print("ERRORS", len(errs)); print("\n".join(errs[:80]))
