import json,glob,re,sys,csv
DD='/home/user/echelon-due-diligence'
m={r['qid']:r for r in csv.DictReader(open('/tmp/claude-0/-home-user/b7b453f6-b4f4-5ac1-8185-da750ab26d41/scratchpad/unb/mined.csv'))}
qs=[json.loads(l) for f in sorted(glob.glob(DD+'/questions/*.jsonl')) for l in open(f) if l.strip()]
pat=re.compile(sys.argv[1],re.I); cats=sys.argv[2].split(',') if len(sys.argv)>2 and sys.argv[2] else None
lim=int(sys.argv[3]) if len(sys.argv)>3 else 30
n=0
for q in qs:
    if q['id'] not in m: continue
    if cats and q['category'] not in cats: continue
    if pat.search(q['question']+' '+q.get('subcategory','')):
        r=m[q['id']]; n+=1
        if n<=lim: print(q['id'],q['customer_importance'][:4],r['ans'],r['astatus'][:12],r['cls'][:14],'|',q['question'][:150])
print('total',n)
