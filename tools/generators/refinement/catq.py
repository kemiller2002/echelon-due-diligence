from lib import *
import sys
cs=sys.argv[1].split(',')
for q in allrecs(load('questions')):
    if q['category'] in cs: print(q['id'],q['answer_unit'],q['question'][:160])
