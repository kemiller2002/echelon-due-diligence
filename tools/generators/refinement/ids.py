import json,csv,re
ids=set()
for l in open('/home/user/unbound/requirements/baseline/baseline.jsonl'):
    if l.strip():
        r=json.loads(l); ids.add(r['id'])
for f in ['MASTER-ENTERPRISE-CONTROL-MATRIX.csv','SPECIFIC-EXECUTABLE-CONTROLS.csv']:
    rows=list(csv.reader(open('/home/user/unbound/requirements/governance/'+f)))
    for row in rows[1:]:
        if row: ids.add(row[0])
sec=set(re.findall(r'\bSEC-[A-Z0-9]+-[0-9]{3}\b',open('/home/user/echelon-organization-administration/policies/security/secure-construction-standard.md').read()))
