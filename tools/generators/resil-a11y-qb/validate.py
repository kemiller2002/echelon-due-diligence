import json, sys, re, jsonschema, itertools
REPO = "/home/user/echelon-due-diligence"
S = {k: json.load(open(f"{REPO}/schemas/dd/{f}.schema.json")) for k, f in
     [("questions", "question"), ("answers", "answer-unit"), ("controls", "control"), ("evidence-requirements", "evidence-requirement")]}
seed = json.load(open(f"{REPO}/sources/SEED-IDS.json"))
srcs = {e["id"] for v in seed.values() for e in v}
cats = sys.argv[1:]
stop = set("the a an of to and or for in on is are do does you your with how what which by be that this any all it its as at from".split())
tok = lambda s: {t for t in re.findall("[a-z0-9]+", s.lower()) if t not in stop}
errs = 0; allq = []
for c in cats:
    recs = {k: [json.loads(l) for l in open(f"{REPO}/{k}/{c}.jsonl")] for k in S}
    ids = {k: {r["id"] for r in v} for k, v in recs.items()}
    for k, v in recs.items():
        v_ = jsonschema.Draft202012Validator(S[k])
        for r in v:
            for e in v_.iter_errors(r):
                print("SCHEMA", r["id"], e.message[:200]); errs += 1
            s = json.dumps(r, ensure_ascii=False)
            if "—" in s: print("EMDASH", r["id"]); errs += 1
            for ref in r.get("source_refs", []) + r.get("framework_refs", []):
                if ref["source_id"] not in srcs: print("SRC", r["id"], ref["source_id"]); errs += 1
            for x in r.get("controls", []):
                if x not in ids["controls"]: print("DANGLING CTL", r["id"], x); errs += 1
            for x in r.get("evidence_requirements", []):
                if x not in ids["evidence-requirements"]: print("DANGLING EVR", r["id"], x); errs += 1
            if k == "questions" and r["answer_unit"] not in ids["answers"]: print("DANGLING AU", r["id"]); errs += 1
            if k == "answers":
                if r["customer_statement_kind"] in ("current-fact",) and r["status"] not in ("verified-operational", "implemented-not-independently-verified"):
                    print("HONESTY", r["id"]); errs += 1
                if r["customer_statement_kind"] == "qualified-current-fact" and r["status"] not in ("verified-operational", "implemented-not-independently-verified", "partially-implemented"):
                    print("HONESTY", r["id"]); errs += 1
    used_au = {q["answer_unit"] for q in recs["questions"]}
    used_ctl = {x for kk in ("questions", "answers") for r in recs[kk] for x in r.get("controls", [])}
    used_evr = {x for kk in ("questions", "answers", "controls") for r in recs[kk] for x in r.get("evidence_requirements", [])}
    for i in ids["answers"] - used_au: print("ORPHAN AU", i)
    for i in ids["controls"] - used_ctl: print("ORPHAN CTL", i)
    for i in ids["evidence-requirements"] - used_evr: print("ORPHAN EVR", i)
    from collections import Counter
    cnt = Counter(q["answer_unit"] for q in recs["questions"])
    print(c, {k: len(v) for k, v in recs.items()}, "challenge:", sum(1 for a in recs["answers"] if "challenge" in a), "q/au:", dict(cnt))
    allq += [(q["id"], tok(q["question"])) for q in recs["questions"]]
for (a, ta), (b, tb) in itertools.combinations(allq, 2):
    j = len(ta & tb) / max(1, len(ta | tb))
    if j >= 0.5: print("SIMILAR", a, b, round(j, 2))
print("errors", errs)
