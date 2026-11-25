from lib import *
import json,re,sys
pat=sys.argv[1]; dirs=sys.argv[2].split(',') if len(sys.argv)>2 else ['questions','answers','controls','evidence-requirements']
def walk(o,path=''):
    if isinstance(o,dict):
        for k,v in o.items(): yield from walk(v,path+'.'+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from walk(v,f'{path}[{i}]')
    elif isinstance(o,str): yield path,o
for d in dirs:
    for f,recs in load(d).items():
        for r in recs:
            for p,s in walk(r):
                for m in re.finditer(pat,s):
                    a=max(0,m.start()-150);print(f"{r['id']}{p}: ...{s[a:m.end()+150]}...")
                    break
