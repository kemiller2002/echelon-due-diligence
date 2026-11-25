import json,sys
base={}
for l in open('/home/user/unbound/requirements/baseline/baseline.jsonl'):
    r=json.loads(l); base[r['id']]=r
cnv={json.loads(l)['id']:json.loads(l) for l in open('/home/user/unbound/requirements/convergence/2026-11-24-master/data/convergence-clauses.jsonl')}
for i in sys.argv[1:]:
    r=base.get(i)
    if not r: print(i,'NOT IN BASELINE'); continue
    t=r['text']
    if i in cnv: t=cnv[i]['statement'] if 'statement' in cnv[i] else t
    print(f"== {i} [{r['status']}; scope={r['release_scope']}; conv={r['converged_by']}; class={r['classification']}]\n{t[:int(__import__('os').environ.get('N','900'))]}\n")
