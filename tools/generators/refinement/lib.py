import json, glob, os, re
ROOT='/home/user/echelon-due-diligence'
def load(d):
    out={}
    for f in sorted(glob.glob(f'{ROOT}/{d}/*.jsonl')):
        out[f]=[json.loads(l) for l in open(f) if l.strip()]
    return out
def save(d, data):
    for f,recs in data.items():
        with open(f,'w') as fh:
            for r in recs: fh.write(json.dumps(r, ensure_ascii=False)+'\n')
def allrecs(data):
    for f,recs in data.items():
        for r in recs: yield r
STOP=set("the a an of to and or for in on is are do does you your with how what which by be that this any all it its as at from".split())
def toks(s): return set(t for t in re.findall('[a-z0-9]+',s.lower()) if t not in STOP)
def jac(a,b):
    u=len(a|b); return len(a&b)/u if u else 0
def sources():
    ids={}
    for f in glob.glob(f'{ROOT}/sources/*.jsonl'):
        for l in open(f):
            if l.strip():
                r=json.loads(l); ids[r['id']]=(os.path.basename(f),r)
    return ids
