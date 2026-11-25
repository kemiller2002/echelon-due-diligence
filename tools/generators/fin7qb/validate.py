import json, sys, re, jsonschema
R = "/home/user/echelon-due-diligence"
schemas = {k: json.load(open(f"{R}/schemas/dd/{v}.schema.json")) for k, v in
           [("questions", "question"), ("answers", "answer-unit"), ("controls", "control"),
            ("evidence-requirements", "evidence-requirement")]}
seeds = set()
for grp in json.load(open(f"{R}/sources/SEED-IDS.json")).values():
    for s in grp: seeds.add(s["id"])
reqids = set(json.loads(l)["id"] for l in open("/home/user/unbound/requirements/baseline/baseline.jsonl"))
import csv
ext = set(r["control_id"] for r in csv.DictReader(open("/home/user/unbound/requirements/governance/MASTER-ENTERPRISE-CONTROL-MATRIX.csv")))
ext |= set(r["specific_control_id"] for r in csv.DictReader(open("/home/user/unbound/requirements/governance/SPECIFIC-EXECUTABLE-CONTROLS.csv")))
ext |= reqids
bad = 0
for cat in sys.argv[1:]:
    recs = {}
    for k, sch in schemas.items():
        recs[k] = [json.loads(l) for l in open(f"{R}/{k}/{cat}.jsonl", encoding="utf-8")]
        for r in recs[k]:
            for e in jsonschema.Draft202012Validator(sch).iter_errors(r):
                print(cat, k, r["id"], e.message); bad += 1
            txt = json.dumps(r, ensure_ascii=False)
            if "—" in txt or "–" in txt:
                print("DASH", r["id"]); bad += 1
            for ref in r.get("source_refs", []) + r.get("framework_refs", []):
                if ref["source_id"] not in seeds:
                    print("UNSEEDED", r["id"], ref["source_id"]); bad += 1
            for rq in r.get("requirements", []):
                if rq not in reqids: print("NOREQ", r["id"], rq); bad += 1
            for x in r.get("related_external_controls", []):
                if x not in ext: print("NOEXT", r["id"], x); bad += 1
    au = {a["id"] for a in recs["answers"]}
    for q in recs["questions"]:
        if q["answer_unit"] not in au: print("NOAU", q["id"]); bad += 1
    texts = [q["question"].lower() for q in recs["questions"]]
    if len(set(texts)) != len(texts): print("DUPQ", cat); bad += 1
    ch = sum(1 for a in recs["answers"] if "challenge" in a)
    st = {a["status"] for a in recs["answers"]} | {c["status"] for c in recs["controls"]}
    print(cat, {k: len(v) for k, v in recs.items()}, "challenge", ch, "statuses", st)
print("errors", bad)
