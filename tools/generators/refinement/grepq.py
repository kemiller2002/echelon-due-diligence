from lib import *
import re,sys
pat=sys.argv[1]
for q in allrecs(load('questions')):
    txt=q['question']+' || '+' | '.join(q.get('alternatives',[]))
    if re.search(pat,txt,re.I): print(' ',q['id'],q['answer_unit'],txt[:260])
