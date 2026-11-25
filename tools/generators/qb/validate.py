import json, jsonschema, re, csv, collections
R="/home/user/echelon-due-diligence"
sch={k:json.load(open(f"{R}/schemas/dd/{v}.schema.json")) for k,v in [("questions","question"),("answers","answer-unit"),("controls","control"),("evidence-requirements","evidence-requirement")]}
seed=json.load(open(f"{R}/sources/SEED-IDS.json"))
seedids={e['id'] for v in seed.values() for e in v}
base={json.loads(l)['id'] for l in open("/home/user/unbound/requirements/baseline/baseline.jsonl")}
ctl={r['control_id'] for r in csv.DictReader(open("/home/user/unbound/requirements/governance/MASTER-ENTERPRISE-CONTROL-MATRIX.csv"))}
soc=set(re.findall(r"^(SOC2-\d+):", open("/home/user/unbound/requirements/governance/SOC2-CONTROLS-EVIDENCE-AND-ENTERPRISE-DIRECTIVE.md").read(), re.M))
sec={"SEC-DB-001","SEC-UI-001","SEC-UI-002","SEC-LANG-001","SEC-LANG-002","SEC-EXEC-001","SEC-DATA-001","SEC-CRYPTO-001","SEC-AUTH-001","SEC-SUPPLY-001"}
known=base|ctl|soc
tot=collections.Counter(); chal=0; errs=0
for cat in ["ISP","ASM","IAM","AUN","AUZ","TEN"]:
    recs={k:[json.loads(l) for l in open(f"{R}/{k}/{cat}.jsonl")] for k in sch}
    ids={k:{r['id'] for r in v} for k,v in recs.items()}
    for k,v in recs.items():
        for r in v:
            try: jsonschema.validate(r, sch[k])
            except jsonschema.ValidationError as ex: print(cat,k,r['id'],ex.message); errs+=1
            s=json.dumps(r,ensure_ascii=False)
            if "—" in s or "–" in s: print("DASH",r['id']); errs+=1
            for ref in r.get('source_refs',[])+r.get('framework_refs',[]):
                if ref['source_id'] not in seedids: print("SRC?",r['id'],ref['source_id']); errs+=1
            for x in r.get('controls',[]):
                if x not in ids['controls']: print("CTL?",r['id'],x); errs+=1
            for x in r.get('evidence_requirements',[]):
                if x not in ids['evidence-requirements']: print("EVR?",r['id'],x); errs+=1
            for x in r.get('policies',[]):
                if x not in sec: print("POL?",r['id'],x); errs+=1
            for x in r.get('requirements',[])+r.get('related_external_controls',[]):
                if x not in known: print("REQ?",r['id'],x); errs+=1
    # questions -> AU
    aucount=collections.Counter(q['answer_unit'] for q in recs['questions'])
    for q in recs['questions']:
        if q['answer_unit'] not in ids['answers']: print("AU?",q['id']); errs+=1
        for ref in q['source_refs']:
            for x in re.findall(r"(?:UNB|CNV|GOV|SOC2|AUTH|TVR|AIN|RR|MON|OPS)-[A-Z0-9-]+", ref.get('locator','')):
                if x not in known: print("LOC?",q['id'],x); errs+=1
    for a in recs['answers']:
        if aucount[a['id']]==0: print("unused AU",a['id'])
        if a['cost_basis']!="order-of-magnitude judgment, not sourced": print("cost",a['id'])
        if 'challenge' in a: chal+=1
    # unused controls / evrs
    usedc={c for a in recs['answers'] for c in a['controls']}
    usede={e for a in recs['answers'] for e in a['evidence_requirements']}|{e for c in recs['controls'] for e in c['evidence_requirements']}
    for c in ids['controls']-usedc: print("unused ctl",c)
    for c in ids['evidence-requirements']-usede: print("unused evr",c)
    # duplicate question text
    qt=collections.Counter(q['question'] for q in recs['questions'])
    for t,n in qt.items():
        if n>1: print("DUPQ",t)
    print(cat,{k:len(v) for k,v in recs.items()},"AU sizes",sorted(aucount.values()),"challenge",sum('challenge' in a for a in recs['answers']))
    for k,v in recs.items(): tot[k]+=len(v)
print(tot,"challenges",chal,"errors",errs)
