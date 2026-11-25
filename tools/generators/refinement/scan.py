from lib import *
import json,re,sys
pats={
'SR11-7':r'SR[ -]?11-7|SRC-SR-11-7|OCC 2011-12',
'SR21-8':r'SR[ -]?21-8',
'COLO':r'Colorado|SB ?24-205|SRC-COLORADO-AI-ACT',
'EUAI':r'EU AI Act|SRC-EU-AI-ACT|Artificial Intelligence Act|AI Act',
'M22-18':r'M-22-18|M-23-16|SRC-OMB-M-22-18|attestation form|SSDF attestation|self-attestation|CISA-SSDF-ATTESTATION',
'BOD':r'BOD 22-01|BOD-22-01|Binding Operational Directive',
'NTIA':r'NTIA|SRC-NTIA',
'OWASPLLM':r'LLM Top 10|LLM-TOP10|Top 10 for LLM|LLM0\d|LLM\d\d',
'FFIEC-CAT':r'FFIEC-CAT|Cybersecurity Assessment Tool|\bCAT\b',
'SEC-OUT':r'SEC-ADVISER-OUTSOURCING|outsourcing proposal|Outsourcing by Investment Advisers|S7-25-22',
'NACHA':r'Nacha|NACHA',
'ADA':r'Title II|SRC-ADA',
'IRC170':r'IRC 170|SRC-IRC-170|section 170|Section 170|charitable deduction|itemiz',
'FINCEN-IA':r'FINCEN-IA-AML|investment adviser AML|investment advisers? .*AML|FinCEN.*advis',
}
dirs=sys.argv[1:] or ['questions','answers','controls','evidence-requirements']
for d in dirs:
    for f,recs in load(d).items():
        for r in recs:
            s=json.dumps(r,ensure_ascii=False)
            hits=[k for k,p in pats.items() if re.search(p,s)]
            if hits: print(d, r['id'], hits)
