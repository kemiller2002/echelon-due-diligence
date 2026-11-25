import json,glob,jsonschema,re,collections
DD='/home/user/echelon-due-diligence'
schema=json.load(open(DD+'/schemas/dd/proposed-requirement.schema.json'))
recs=[json.loads(l) for l in open(DD+'/product-profiles/unbound/proposed-requirements.jsonl')]
base={json.loads(l)['id'] for l in open('/home/user/unbound/requirements/baseline/baseline.jsonl')}
qids={json.loads(l)['id'] for f in glob.glob(DD+'/questions/*.jsonl') for l in open(f) if l.strip()}
src={json.loads(l)['id'] for f in glob.glob(DD+'/sources/*.jsonl') for l in open(f) if l.strip()}
evr={json.loads(l)['id'] for f in glob.glob(DD+'/evidence-requirements/*.jsonl') for l in open(f) if l.strip()}
ids=[r['id'] for r in recs]
errs=0
v=jsonschema.Draft202012Validator(schema)
for r in recs:
    for e in v.iter_errors(r): print('SCHEMA',r['id'],e.message); errs+=1
    for q in r['originating_questions']:
        if q not in qids: print('Q',r['id'],q); errs+=1
    for s in r['source_refs']:
        if s['source_id'] not in src: print('S',r['id'],s['source_id']); errs+=1
    for x in r['existing_requirement_refs']:
        if x not in base: print('REQ',r['id'],x); errs+=1
    for x in r['evidence_requirements']:
        if x not in evr: print('EVR',r['id'],x); errs+=1
    for d in r['dependencies']:
        if d.startswith('DD-UNB') and d not in ids: print('DEP',r['id'],d); errs+=1
    s=json.dumps(r,ensure_ascii=False)
    if '—' in s: print('EMDASH',r['id']); errs+=1
dup=[k for k,c in collections.Counter(ids).items() if c>1]
print('dups',dup)
print('records',len(recs),'errors',errs)
print(collections.Counter(r['priority'] for r in recs))
print(collections.Counter(r['id'].split('-')[2] for r in recs))
