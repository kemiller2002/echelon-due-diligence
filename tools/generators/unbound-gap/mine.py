import json,glob,collections,re,csv,sys
DD='/home/user/echelon-due-diligence'; UB='/home/user/unbound'
OUT='/tmp/claude-0/-home-user/b7b453f6-b4f4-5ac1-8185-da750ab26d41/scratchpad/unb/'
base={}
for l in open(UB+'/requirements/baseline/baseline.jsonl'):
    r=json.loads(l); base[r['id']]=r
cnv={}
for l in open(UB+'/requirements/convergence/2026-11-24-master/data/convergence-clauses.jsonl'):
    r=json.loads(l); cnv[r['id']]=r
amended_by=collections.defaultdict(set)
for c in cnv.values():
    for a in c.get('amends',[]): amended_by[a].add(c['id'])
for r in base.values():
    for c in r['converged_by']: amended_by[r['id']].add(c)
qs=[json.loads(l) for f in sorted(glob.glob(DD+'/questions/*.jsonl')) for l in open(f) if l.strip()]
an={json.loads(l)['id']:json.loads(l) for f in glob.glob(DD+'/answers/*.jsonl') for l in open(f) if l.strip()}
secstd=re.compile(r'^SEC-[A-Z]+-\d+$')
rows=[]
for q in qs:
    if not ({'unbound','all-echelon-products'} & set(q.get('products',[]))): continue
    a=an.get(q.get('answer_unit'),{})
    reqs=list(dict.fromkeys(q.get('requirements',[])+a.get('requirements',[])))
    unb=[x for x in reqs if not secstd.match(x)]
    exist=[x for x in unb if x in base]
    missing=[x for x in unb if x not in base]
    governed=[x for x in exist if amended_by.get(x)]
    governed_uncited=[x for x in governed if not (amended_by[x] & set(reqs))]
    weak=[x for x in exist if base[x]['status'] in ('proposed','unvalidated') or base[x]['classification']!='normative']
    deferred=[x for x in exist if base[x]['release_scope'].lower().startswith('defer')]
    strong=[x for x in exist if x not in weak and x not in governed_uncited]
    oq=a.get('open_questions',[])+q.get('open_questions',[])
    if not unb: cls='no-unbound-requirement'
    elif not strong: cls='only-weak-or-missing'
    elif a.get('status') in ('unknown','requires-external-validation'): cls='answer-unknown'
    elif oq: cls='covered-with-open-questions'
    else: cls='covered'
    rows.append(dict(qid=q['id'],cat=q['category'],sub=q.get('subcategory',''),imp=q.get('customer_importance',''),
      ans=q.get('answer_unit',''),astatus=a.get('status',''),cls=cls,n_req=len(unb),strong=len(strong),
      missing=';'.join(missing),governed_uncited=';'.join(f"{x}>{'/'.join(sorted(amended_by[x]))}" for x in governed_uncited),
      weak=';'.join(weak),deferred=';'.join(deferred),oq=len(oq),question=q['question']))
with open(OUT+'mined.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(rows)); print(collections.Counter(r['cls'] for r in rows))
bycat=collections.defaultdict(collections.Counter)
for r in rows: bycat[r['cat']][r['cls']]+=1
for c in sorted(bycat): print(c, dict(bycat[c]))
allmiss=collections.Counter(m for r in rows for m in r['missing'].split(';') if m)
print('MISSING',allmiss.most_common(60))
gov=collections.Counter(m for r in rows for m in r['governed_uncited'].split(';') if m)
print('GOVERNED-UNCITED',gov.most_common(60))
