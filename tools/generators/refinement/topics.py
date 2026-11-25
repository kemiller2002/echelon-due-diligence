from lib import *
import re,sys,os
T={
1:r'(disclos|notify|tell).{0,60}(AI|model|generative|GenAI)|basis of (the|any) model|explain.{0,30}model',
2:r'train(ing)?.{0,40}(customer|our) data|(customer|our) data.{0,60}train|improve.{0,20}models?',
3:r'(staff|employee|personnel|workforce).{0,80}(AI tool|generative|GenAI|ChatGPT|third-party AI|public AI)|(enter|paste|input).{0,40}(data).{0,60}(AI|GenAI)',
4:r'(training data|model data|dataset).{0,60}(access|restrict|log)|(access|restrict).{0,60}(training data|datasets)',
5:r'human oversight|human review.{0,40}AI|named (role|person|owner).{0,40}(AI|oversight)|oversight role',
6:r'copyright|IP indemn|indemnif.{0,40}(AI|intellectual)|environmental|energy|carbon',
7:r'training.{0,40}(personnel|staff|employees).{0,80}|awareness training|training (records|metrics|completion)',
8:r'background (check|investigation|screen)|credit (check|report)|fingerprint|criminal',
9:r'(countr|offshore|location).{0,60}(develop|support|personnel|staff|remote access|maintain)|remote access.{0,40}(United States|US-only|outside)',
10:r'SSO|single sign-on|federat|SAML|OIDC|identity provider|IdP|entitlement review|access review.{0,40}(our|customer)',
11:r'privileged access review|quarterly|deprovision|24 hours.{0,40}(access|revok)|just-in-time|JIT',
12:r'(PII|personal|SSN|social security|sensitive).{0,40}logs?|logs?.{0,40}(PII|SSN|personal data|sensitive)',
13:r'production data.{0,60}(non-production|test|development|lower)|(test|non-production|development).{0,40}production data',
14:r'(customer|tenant)[- ](specific|dedicated|unique|managed).{0,20}key|BYOK|HSM|key rotation|rotat.{0,20}key|key inventory',
15:r'(remediat|fix).{0,60}(findings|issues).{0,60}(our|customer)|(customer|our).{0,40}(assessment|scan|test|OSINT|attack surface)',
16:r'right to (audit|test|pen)|on-site audit|(audit|inspect).{0,40}(premises|on site|onsite)|(our|customer|regulator).{0,60}(penetration test|pen test).{0,40}(your|service)',
17:r'(subprocessor|sub-processor|subcontractor).{0,80}(consent|object|notice|approv)',
18:r'(government|law enforcement|subpoena|legal (process|demand)|lawful access).{0,80}',
19:r'24 hours|72 hours|Regulation S-P|30 days.{0,40}notice|breach notif',
20:r'(certif|attest|confirm).{0,40}(delet|destruct)|deletion.{0,60}backup|certificate of destruction|revoke.{0,40}(API|federat|token)',
21:r'exit assistance|resolution|recovery and resolution|transition assistance|termination assistance',
22:r'SOC 2.{0,80}(opinion|qualified|period|exception|Type)|bridge letter|report period|SOC report',
23:r'(before|prior to).{0,30}(sign|contract)|pre-contract|pre-signature',
24:r'public records|FOIA|open records|redact',
25:r'end[- ]of[- ]life|unsupported|EOL',
26:r'drift|shared[- ]responsibility|configuration baseline',
27:r'DNS',
28:r'session|cookie|concurrent login|timeout',
29:r'VPAT|ACR|overlay|third-party (accessibility )?audit|WCAG 2\.2|accessibility conformance',
30:r'credential.{0,60}(share|third-party|aggregat|scrap)|screen[- ]scrap|aggregat',
31:r'support.{0,40}(access|impersonat|log in|view).{0,60}(account|donor|consent)|impersonat|consent.{0,40}support|break[- ]glass',
32:r'call[- ]?back|payee.{0,40}(bank|change)|bank (detail|account).{0,40}chang|dual (authoriz|approv|control).{0,60}(payment|disburs|grant)',
33:r'immutab|offline.{0,40}(backup|cop)|air[- ]gap|ransomware.{0,40}backup|restore test',
34:r'(recovery|DR|BCP|continuity).{0,40}(exercise|test).{0,60}|key (recovery )?staff|turnover',
35:r'RTO|RPO|recovery objective|capacity.{0,40}(DR|recovery|failover)',
36:r'notif.{0,60}(change|material)|advance notice|material(ly)? (impair|change|adverse)',
37:r'modern slavery|human rights|sustainab|ESG|supplier code',
38:r'small[- ](business|supplier|vendor)|cannot (yet )?meet|remediation plan|plan of action|compensating',
}
cats={1:'AIG',2:'AIG PRV',3:'AIS HR',4:'AIS',5:'AIA',6:'AIG IPR',7:'HR',8:'HR',9:'GOV REG',10:'AUN IAM',11:'IAM',12:'MON DCL',13:'DCL SDL',14:'ENC TEN',15:'VUL RSK',16:'AUD LEG',17:'SUB',18:'PRV LEG',19:'IR',20:'RET TRM',21:'TRM',22:'AUD',23:'AUD',24:'AUD LEG',25:'ASM VUL',26:'CLD',27:'NET',28:'APP',29:'A11Y',30:'API DON WLB',31:'DON IAM SUP',32:'FRD PAY',33:'BKP',34:'BCP DR',35:'DR AVL',36:'CHG GOV',37:'GOV',38:'GOV TPR'}
Q=list(allrecs(load('questions')))
which=[int(x) for x in sys.argv[1:]] or list(T)
for t in which:
    print(f'=== {t} [{cats[t]}]')
    pref=cats[t].split()
    for q in Q:
        txt=q['question']+' || '+' | '.join(q.get('alternatives',[]))
        if re.search(T[t],txt,re.I) and (q["category"] in pref or os.environ.get("ALL")):
            print(' ',q['id'],q['answer_unit'],txt[:230])
