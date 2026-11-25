import csv, importlib, json, re, sys
import jsonschema
from lib import build, write, ROOT

CATS = sys.argv[1:] or ["FCT", "ACT", "TXI", "FRD", "PAY"]
schemas = {k: json.load(open(f"{ROOT}/schemas/dd/{k}.schema.json")) for k in
           ("question", "answer-unit", "control", "evidence-requirement")}

# known requirement / control ids
known = set()
for l in open("/home/user/unbound/requirements/baseline/baseline.jsonl"):
    known.add(json.loads(l)["id"])
for f, col in (("MASTER-ENTERPRISE-CONTROL-MATRIX.csv", "control_id"), ("SPECIFIC-EXECUTABLE-CONTROLS.csv", "specific_control_id")):
    for r in csv.DictReader(open("/home/user/unbound/requirements/governance/" + f)):
        known.add(r[col])
known |= {"SEC-DB-001", "SEC-UI-001", "SEC-UI-002", "SEC-LANG-001", "SEC-LANG-002", "SEC-EXEC-001", "SEC-DATA-001",
          "SEC-CRYPTO-001", "SEC-AUTH-001", "SEC-SUPPLY-001"}
seed = set()
for grp in json.load(open(f"{ROOT}/sources/SEED-IDS.json")).values():
    for s in grp:
        seed.add(s["id"])

allq, alla, allc, alle = [], [], [], []
for cat in CATS:
    mod = importlib.import_module(cat.lower())
    q, a, c, e = build(cat, mod.aus, mod.controls, mod.evidence, mod.DEF)
    write(cat, q, a, c, e)
    print(cat, "questions", len(q), "answers", len(a), "controls", len(c), "evidence", len(e),
          "challenge", sum(1 for x in a if "challenge" in x))
    allq += q; alla += a; allc += c; alle += e

errors = []
v = {k: jsonschema.Draft202012Validator(s, format_checker=jsonschema.FormatChecker()) for k, s in schemas.items()}
for kind, recs in (("question", allq), ("answer-unit", alla), ("control", allc), ("evidence-requirement", alle)):
    for r in recs:
        for err in v[kind].iter_errors(r):
            errors.append(f"SCHEMA {r['id']}: {err.message}")
        s = json.dumps(r, ensure_ascii=False)
        if "—" in s:
            errors.append(f"EMDASH {r['id']}")
        for m in re.finditer(r'"source_id": "([^"]+)"', s):
            if m.group(1) not in seed:
                errors.append(f"SRC {r['id']}: {m.group(1)}")
        for fld in ("requirements", "policies", "related_external_controls"):
            for i in r.get(fld, []):
                if i not in known:
                    errors.append(f"UNKNOWN-ID {r['id']} {fld}: {i}")

# cross refs (allow existing files from other categories)
import glob, os
ids = {"ECTL": set(), "EVR": set(), "ANS": set()}
for sub, pre in (("controls", "ECTL"), ("evidence-requirements", "EVR"), ("answers", "ANS")):
    for f in glob.glob(f"{ROOT}/{sub}/*.jsonl"):
        for l in open(f):
            ids[pre].add(json.loads(l)["id"])
for r in allq + alla + allc:
    for c in r.get("controls", []):
        if c not in ids["ECTL"]:
            errors.append(f"DANGLING {r['id']} control {c}")
    for e in r.get("evidence_requirements", []):
        if e not in ids["EVR"]:
            errors.append(f"DANGLING {r['id']} evidence {e}")
used_c = {c for r in alla for c in r["controls"]}
used_e = {e for r in alla + allc for e in r["evidence_requirements"]}
for c in allc:
    if c["id"] not in used_c:
        errors.append(f"ORPHAN control {c['id']}")
for e in alle:
    if e["id"] not in used_e:
        errors.append(f"ORPHAN evidence {e['id']}")

stop = set("the a an of to and or for in on is are do does you your with how what which by be that this any all it its as at from".split())
def tok(s): return {t for t in re.findall(r"[a-z0-9]+", s.lower()) if t not in stop}
toks = [(q["id"], tok(q["question"])) for q in allq]
for i in range(len(toks)):
    for j in range(i + 1, len(toks)):
        a_, b_ = toks[i][1], toks[j][1]
        jac = len(a_ & b_) / len(a_ | b_)
        if jac >= 0.6:
            errors.append(f"NEARDUP {toks[i][0]} ~ {toks[j][0]} {jac:.2f}")
print("\n".join(errors) if errors else "ALL CHECKS PASSED")
