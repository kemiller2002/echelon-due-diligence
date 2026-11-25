import json,re,sys
base=[json.loads(l) for l in open('/home/user/unbound/requirements/baseline/baseline.jsonl')]
pat=re.compile(sys.argv[1],re.I)
lim=int(sys.argv[2]) if len(sys.argv)>2 else 15
hits=[r for r in base if pat.search(r['text'])]
print(len(hits),'hits')
for r in hits[:lim]:
    m=pat.search(r['text']); s=max(0,m.start()-120)
    print(f"{r['id']} [{r['status'][:22]};{r['release_scope'][:12]}] ...{r['text'][s:m.end()+160]!r}")
