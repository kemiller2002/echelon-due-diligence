import json, sys, re, collections, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lccommon as C
import prv, dclret, exit  # noqa: F401  (populate registries)
import jsonschema

REPO = "/home/user/echelon-due-diligence"
CATS = ["PRV", "DCL", "RET", "PRT", "TRM", "ESC"]
schemas = {k: json.load(open(f"{REPO}/schemas/dd/{f}")) for k, f in [
    ("q", "question.schema.json"), ("a", "answer-unit.schema.json"),
    ("c", "control.schema.json"), ("e", "evidence-requirement.schema.json")]}

out = collections.defaultdict(lambda: collections.defaultdict(list))
counters = collections.Counter()
for qq in C.QS:
    a, prods = C.AUS[qq["a"]]
    cat = qq["a"].split("-")[1]
    counters[cat] += 1
    rec = {
        "id": f"DDQ-{cat}-{counters[cat]:04d}", "question": qq["text"],
        "alternatives": qq["alts"], "category": cat, "subcategory": qq["sub"],
        "business_concern": qq["concern"], "risk_addressed": qq["risk"],
        "source_refs": [C.s(x) for x in qq["srcs"]], "industries": qq["ind"],
        "jurisdictions": qq["jur"], "products": qq["products"] or prods,
        "requirement_classification": qq["cls"], "customer_importance": qq["imp"],
        "answer_unit": qq["a"], "controls": a["controls"], "policies": a["policies"],
        "requirements": a["requirements"], "evidence_requirements": a["evidence_requirements"],
        "disclosure_classification": qq["disc"], "open_questions": qq["oq"] or [],
        "history": C.HIST,
    }
    if qq["reg"]:
        rec["regulatory_authority"] = qq["reg"]
    if qq["scope"]:
        rec["answer_scope_note"] = qq["scope"]
    out[cat]["questions"].append(rec)

for aid, (a, _) in C.AUS.items():
    out[aid.split("-")[1]]["answers"].append(a)
for c in C.CTLS:
    out[c["id"].split("-")[1]]["controls"].append(c)
for e in C.EVRS:
    out[e["id"].split("-")[1]]["evidence-requirements"].append(e)

# integrity checks
errors = []
ctl_ids = {c["id"] for c in C.CTLS}
evr_ids = {e["id"] for e in C.EVRS}
used_aus = {q["a"] for q in C.QS}
for aid, (a, _) in C.AUS.items():
    if aid not in used_aus:
        errors.append(f"unused AU {aid}")
    for x in a["controls"]:
        if x not in ctl_ids: errors.append(f"{aid} missing control {x}")
    for x in a["evidence_requirements"]:
        if x not in evr_ids: errors.append(f"{aid} missing evr {x}")
for c in C.CTLS:
    for x in c["evidence_requirements"]:
        if x not in evr_ids: errors.append(f"{c['id']} missing evr {x}")
for lst in (C.CTLS, C.EVRS):
    ids = [r["id"] for r in lst]
    dup = [i for i, n in collections.Counter(ids).items() if n > 1]
    if dup: errors.append(f"duplicate ids {dup}")
texts = collections.Counter(q["text"] for q in C.QS)
errors += [f"duplicate question {t[:60]}" for t, n in texts.items() if n > 1]

kinds = {"questions": "q", "answers": "a", "controls": "c", "evidence-requirements": "e"}
for cat in CATS:
    for folder, k in kinds.items():
        recs = sorted(out[cat][folder], key=lambda r: r["id"])
        for r in recs:
            try:
                jsonschema.validate(r, schemas[k])
            except jsonschema.ValidationError as ex:
                errors.append(f"{r['id']}: {ex.message}")
        blob = "\n".join(json.dumps(r, ensure_ascii=False) for r in recs) + "\n"
        if "—" in blob or "–" in blob:
            errors.append(f"dash in {cat}/{folder}")
        out[cat][folder] = recs

if errors:
    print("\n".join(errors)); sys.exit(1)

if "--write" in sys.argv:
    for cat in CATS:
        for folder in kinds:
            with open(f"{REPO}/{folder}/{cat}.jsonl", "w", encoding="utf-8") as f:
                for r in out[cat][folder]:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")

for cat in CATS:
    aus = out[cat]["answers"]
    print(cat, {k: len(out[cat][k]) for k in kinds},
          "challenge:", sum(1 for a in aus if "challenge" in a),
          "status:", dict(collections.Counter(a["status"] for a in aus)))
srcs = sorted({r["source_id"] for q in C.QS for r in (C.s(x) for x in q["srcs"])} |
              {r["source_id"] for c in C.CTLS for r in c["framework_refs"]})
seed = json.load(open(f"{REPO}/sources/SEED-IDS.json"))
seeded = {e["id"] for v in seed.values() for e in v}
print("unseeded:", [x for x in srcs if x not in seeded])
print("q per AU:", sorted(collections.Counter(q["a"] for q in C.QS).items(), key=lambda x: x[1])[:6])
