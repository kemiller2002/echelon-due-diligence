import json, glob, os, re, copy, collections

ROOT = '/home/user/echelon-due-diligence'
BK = '/tmp/claude-0/-home-user/b7b453f6-b4f4-5ac1-8185-da750ab26d41/scratchpad/ref/backup'
DATE = '2026-11-25'
BY = 'refinement-agent'
DIRS = ['questions', 'answers', 'controls', 'evidence-requirements']

files = {}   # dir -> {basename: [records]}
index = {}   # id -> (dir, basename, record)
for d in DIRS:
    files[d] = {}
    for f in sorted(glob.glob(f'{BK}/{d}/*.jsonl')):
        b = os.path.basename(f)
        recs = [json.loads(l) for l in open(f) if l.strip()]
        files[d][b] = recs
        for r in recs:
            index[r['id']] = (d, b, r)

SOURCES = set()
for f in glob.glob(f'{ROOT}/sources/*.jsonl'):
    for l in open(f):
        if l.strip():
            SOURCES.add(json.loads(l)['id'])

stats = collections.Counter()
log = collections.defaultdict(list)


def R(i):
    return index[i][2]


def note(r, change):
    d = index[r['id']][0]
    if d in ('questions', 'answers'):
        r.setdefault('history', []).append({'date': DATE, 'change': change, 'by': BY})
    else:
        prev = r.get('notes', '')
        add = f'{DATE} {BY}: {change}'
        r['notes'] = (prev + ' ' + add).strip() if prev else add
    log[r['id']].append(change)


def chk_src(s):
    assert s in SOURCES, s


def add_ref(r, sid, basis='directly-documented', relation='maps-to', locator=None, field='source_refs'):
    chk_src(sid)
    refs = r.setdefault(field, [])
    for x in refs:
        if x['source_id'] == sid and x.get('locator') == locator:
            return False
    e = {'source_id': sid, 'relation': relation, 'basis': basis}
    if locator:
        e['locator'] = locator
    refs.append(e)
    return True


def add_alt(qid, text, srcs, topic):
    q = R(qid)
    assert index[qid][0] == 'questions'
    alts = q.setdefault('alternatives', [])
    assert text not in alts
    assert '—' not in text
    alts.append(text)
    stats['alternatives_added'] += 1
    added = []
    for s in srcs:
        sid, basis = (s, 'directly-documented') if isinstance(s, str) else s
        if add_ref(q, sid, basis):
            added.append(sid)
            stats['srcq_refs_added'] += 1
    note(q, f'Added real-world alternative wording from DD-QNR-001 topic {topic}' + (f' and source reference(s) {", ".join(added)} (maps-to)' if added else ''))


def replace_ref(r, old, new, field='source_refs', basis=None, relation=None, locmap=None, why=''):
    chk_src(new)
    refs = r.get(field, [])
    out = []
    changed = False
    for x in refs:
        if x['source_id'] == old:
            y = dict(x)
            y['source_id'] = new
            if basis:
                y['basis'] = basis
            if relation:
                y['relation'] = relation
            if locmap is not None and 'locator' in y:
                nl = locmap(y['locator'])
                if nl:
                    y['locator'] = nl
                else:
                    del y['locator']
            # dedupe
            if any(z['source_id'] == new and z.get('locator') == y.get('locator') for z in out + [w for w in refs if w['source_id'] == new]):
                changed = True
                continue
            out.append(y)
            changed = True
        else:
            out.append(x)
    assert changed, (r['id'], old)
    r[field] = out
    stats['stale_refs_replaced'] += 1
    return changed


def set_text(r, path, old, new):
    """Replace substring old with new in r[path] (path may be 'challenge.legally_required' or list index)."""
    obj = r
    keys = path.split('.')
    keys = [int(k) if k.isdigit() else k for k in keys]
    for k in keys[:-1]:
        obj = obj[k]
    k = keys[-1]
    assert old in obj[k], (r['id'], path, old)
    obj[k] = obj[k].replace(old, new)


def new_record(d, cat, rec):
    b = f'{cat}.jsonl'
    assert rec['id'] not in index, rec['id']
    for s in rec.get('source_refs', []) + rec.get('framework_refs', []):
        chk_src(s['source_id'])
    files[d][b].append(rec)
    index[rec['id']] = (d, b, rec)


def H(change='created'):
    return [{'date': DATE, 'change': change, 'by': BY}]


def ref(sid, basis='directly-documented', relation='maps-to', locator=None):
    e = {'source_id': sid, 'relation': relation, 'basis': basis}
    if locator:
        e['locator'] = locator
    return e


def new_q(qid, ans, text, sub, concern, risk, refs, industries, juris, cls, imp, topic, scope=None, products=None, alts=None, authority=None):
    a = R(ans)
    q = {'id': qid, 'question': text}
    if alts:
        q['alternatives'] = alts
    q.update({'category': qid.split('-')[1], 'subcategory': sub, 'business_concern': concern,
              'risk_addressed': risk, 'source_refs': refs, 'industries': industries,
              'jurisdictions': juris, 'products': products or ['all-echelon-products']})
    if authority:
        q['regulatory_authority'] = authority
    q.update({'requirement_classification': cls, 'customer_importance': imp, 'answer_unit': ans})
    if scope:
        q['answer_scope_note'] = scope
    q['controls'] = list(a.get('controls', []))
    if a.get('policies'):
        q['policies'] = list(a['policies'])
    if a.get('requirements'):
        q['requirements'] = list(a['requirements'])
    q['evidence_requirements'] = list(a.get('evidence_requirements', []))
    q['disclosure_classification'] = a.get('disclosure_classification', 'nda')
    q['history'] = H(f'created from DD-QNR-001 topic {topic}' if isinstance(topic, int) else f'created ({topic})')
    for t in [text] + (alts or []):
        assert '—' not in t
    new_record('questions', qid.split('-')[1], q)
    stats['new_questions'] += 1
    log[qid].append('created')
    return q


def next_id(prefix, cat, width):
    mx = 0
    for i in index:
        p = i.split('-')
        if p[0] == prefix and p[1] == cat:
            mx = max(mx, int(p[2]))
    return f'{prefix}-{cat}-{mx + 1:0{width}d}'


# ============================================================
# TASK 1: real-world topics (DD-QNR-001)
# ============================================================
MSMIN = 'SRC-Q-MS-MIN-SECURITY-STANDARDS'
MSSEC = 'SRC-Q-MS-SECURITY-STANDARDS-IT-CYBER'
MSTP = 'SRC-Q-MS-THIRD-PARTY-REG-REQS'
MSDPT = 'SRC-Q-MS-DATA-PROCESSING-TERMS'
TRUIST = 'SRC-Q-TRUIST-TPISS'
FID = 'SRC-Q-FIDELITY-SUPPLIER-POLICIES'
NYDFS = 'SRC-Q-NYDFS-IL-20251021-TPSP'
RI = 'reasonably-inferred'

# 1 AI disclosure and basis of model
add_alt('DDQ-AIG-0039', 'Will you tell us proactively when any service you deliver to us relies on a model or generative AI, and explain how the model works and the basis for its outputs?',
        [MSMIN, 'SRC-Q-FSISAC-GENAI-VENDOR-GUIDE'], 1)
# 2 training on customer data
add_alt('DDQ-AIG-0027', 'Will the contract state that our data may not be used to train or improve any AI model, yours or a provider\'s, without our written consent?',
        [NYDFS, 'SRC-Q-ACLU-GENAI-VENDOR-Q', 'SRC-Q-FSISAC-GENAI-VENDOR-GUIDE'], 2)
# 3 staff use of third-party GenAI tools
add_alt('DDQ-AIG-0009', 'Are your personnel prohibited from entering our data into third-party or open-source generative AI tools, and how is that prohibition enforced?',
        [TRUIST, MSMIN], 3)
# 5 named human oversight role
add_alt('DDQ-AIA-0024', 'Which named role oversees AI outputs before they are relied on, and what evidence shows that the oversight actually took place, beyond a general human-in-the-loop statement?',
        ['SRC-Q-PURDUE-AI-VENDOR-Q', 'SRC-Q-MEMPHIS-VENDOR-SEC-PRIV-TEMPLATE'], 5)
# 6 AI copyright and IP indemnity
add_alt('DDQ-LEG-0017', 'Will you indemnify us if an AI feature or AI-generated code or content infringes a third party\'s copyright, including through the model\'s training data?',
        ['SRC-Q-ACLU-GENAI-VENDOR-Q', ('SRC-Q-AU-AI-PROCUREMENT', RI)], 6)
# 8 background investigation depth and cost
add_alt('DDQ-HR-0001', 'Do your background checks include a seven-year county criminal search, a credit report, Social Security number verification, and education and employment verification?',
        [FID], 8)
add_alt('DDQ-HR-0001', 'Will you reimburse us for background checks that we perform ourselves on your personnel?', [], 8)
add_alt('DDQ-HR-0007', 'Are personnel who need unescorted access to our premises fingerprinted?', [FID], 8)
# 9 location of personnel remote access
add_alt('DDQ-HR-0036', 'Is remote access by your personnel and subcontractors limited to the United States unless we approve otherwise in writing?',
        [TRUIST, 'SRC-Q-WI-DOA-10816'], 9)
# 10 SSO federation to customer IdP
add_alt('DDQ-AUN-0012', 'Will the service federate to our enterprise identity provider for all of our users, so that none of them hold a separate password with you?',
        [TRUIST, 'SRC-Q-GS-VENDOR-TECH-RISK-EXPECTATIONS'], 10)
# 11 privileged access cadence and deprovisioning
add_alt('DDQ-IAM-0007', 'Is privileged access reviewed at least quarterly?', [TRUIST, MSMIN], 11)
add_alt('DDQ-HR-0016', 'Is privileged access removed within 24 hours when someone leaves or no longer needs it?', [TRUIST], 11)
add_alt('DDQ-IAM-0014', 'Do you use just-in-time privileged access rather than standing administrator accounts?', [MSMIN], 11)
# 12 PII in logs
add_alt('DDQ-MON-0014', 'Do you prohibit writing personal information, such as Social Security numbers, to application and system logs?', [MSMIN], 12)
# 13 production data in non-production
add_alt('DDQ-PRV-0042', 'Is copying production data into development, test or other lower environments prohibited?', [MSMIN], 13)
if add_ref(R('DDQ-INF-0027'), MSMIN):
    stats['srcq_refs_added'] += 1
    note(R('DDQ-INF-0027'), f'Added source reference {MSMIN} (maps-to) for DD-QNR-001 topic 13')
# 14 per-customer cryptography
add_alt('DDQ-TEN-0029', 'Will the services you run for us in public cloud use encryption keys dedicated to us rather than shared with other customers?', [MSMIN, TRUIST], 14)
add_alt('DDQ-ENC-0016', 'Are encryption keys rotated at least every 24 months?', [TRUIST], 14)
add_alt('DDQ-ENC-0013', 'Do you keep an inventory of keys, use a hardware security module for high-value keys and use each key for a single purpose?', [MSMIN], 14)
# 15 remediation of customer assessment findings
add_alt('DDQ-AUD-0028', 'Will you remediate material findings from our assessment of you within five business days, or agree a remediation plan with us within that time?', [TRUIST], 15)
# 16 audit and testing rights
add_alt('DDQ-AUD-0025', 'Will you permit on-site audits with 48 hours\' notice?', [MSTP], 16)
add_alt('DDQ-AUD-0024', 'Will our regulators be able to inspect, and take copies of, records relating to the services you provide to us?', [MSTP], 16)
add_alt('DDQ-AUD-0022', 'Will you allow us to perform, or commission, penetration tests of the services you provide to us?', [MSSEC], 16)
# 17 subprocessor consent and notice
add_alt('DDQ-SUB-0006', 'Will you obtain our prior written consent before any new subprocessor processes our data?', [MSDPT, NYDFS], 17)
add_alt('DDQ-SUB-0005', 'Will you give us at least 90 days\' notice before a material change in subcontracting that affects our services?', [MSTP], 17)
# 18 government access requests
add_alt('DDQ-REG-0014', 'If a government agency or law enforcement body asks you for our data, will you notify us within a fixed period unless the law prohibits it?', [MSDPT], 18)
# 19 breach deadlines
add_alt('DDQ-IR-0015', 'Will you notify us within 24 hours of an incident involving our personal information?', [MSDPT, TRUIST], 19)
add_alt('DDQ-IR-0026', 'Will you support the notice we must give affected individuals within 30 days under amended Regulation S-P?', ['SRC-Q-SEC-REG-SP-2024-FACT-SHEET'], 19)
# 20 certified deletion
add_alt('DDQ-RET-0029', 'Does your certification of deletion cover backups and cached copies as well as primary storage?', [NYDFS, MSMIN], 20)
# 21 exit assistance fees
add_alt('DDQ-TRM-0024', 'Will exit assistance be provided at the fees in effect immediately before termination?', [MSTP], 21)
# 22 SOC report acceptability
add_alt('DDQ-AUD-0005', 'Is the opinion in your SOC 2 Type 2 report unqualified for the common criteria on risk assessment, logical access and system operations (CC3, CC6 and CC7)?', ['SRC-Q-MD-STD-317-SA-01'], 22)
add_alt('DDQ-AUD-0001', 'Does your SOC 1 or SOC 2 Type II report cover the most recent 12 months?', [MSTP], 22)
# 25 EOL components disclosure
add_alt('DDQ-INF-0030', 'Will you disclose to us any unsupported components in the service and how you are treating the risk they create?', [MSMIN, 'SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022'], 25)
# 26 cloud drift and shared responsibility
add_alt('DDQ-CLD-0008', 'Does your shared responsibility matrix with your cloud provider cover resilience and recovery as well as security?', [MSMIN], 26)
add_alt('DDQ-ASM-0019', 'How do you prevent cloud configuration drift?', [MSMIN], 26)
# 27 DNS security
add_alt('DDQ-NET-0026', 'Do your systems use encrypted DNS and a protective DNS service, and are DNS queries logged?', [MSMIN, ('SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022', RI)], 27)
# 28 session security specifics
add_alt('DDQ-APP-0046', 'Do you prevent concurrent logins with the same credentials?', [MSMIN], 28)
add_alt('DDQ-APP-0043', 'Is the session ID rotated after login?', [MSMIN], 28)
add_alt('DDQ-AUN-0026', 'Are session timeouts configurable by our administrators within limits you set?', [MSMIN], 28)
# 29 accessibility evidence
add_alt('DDQ-A11Y-0007', 'Is your accessibility conformance report prepared by an independent third-party auditor rather than self-assessed?', [FID, 'SRC-Q-YALE-ACCESSIBLE-PURCHASING'], 29)
add_alt('DDQ-A11Y-0008', 'Is your accessibility conformance report dated within the last 18 months?', [FID], 29)
add_alt('DDQ-A11Y-0017', 'What is your plan for adopting newer WCAG versions and your schedule for remediating known issues?', ['SRC-Q-MTU-ICT-ACCESSIBILITY-PROCUREMENT', MSTP], 29)
# 31 consent-based support access
add_alt('DDQ-SUP-0012', 'Can your staff log in to a donor\'s account only with the donor\'s or sponsor\'s consent, and is every such login recorded?',
        ['SRC-Q-GKCCF-PRIVACY-POLICY', 'SRC-Q-VANGUARD-CHARITABLE-PRIVACY'], 31)
# 32 payments fraud controls
add_alt('DDQ-FRD-0007', 'Do you verify changes to payee bank details by calling back a telephone number already on file?',
        ['SRC-Q-TMHCC-NETGUARD-APP-2026', 'SRC-Q-INDIANA-CYBER-INSURANCE-TOOLKIT'], 32)
add_alt('DDQ-AUZ-0018', 'Is dual authorization required for any disbursement above a set dollar threshold?', ['SRC-Q-ATBAY-CYBER-APP-2026'], 32)
# 33 ransomware backup assurance
add_alt('DDQ-BKP-0006', 'Do you keep an offline or logically isolated encrypted copy of your backups?', ['SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022', 'SRC-Q-ATBAY-CYBER-APP-2026'], 33)
add_alt('DDQ-BKP-0009', 'Are copies of backup decryption keys kept offline?', [('SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022', RI), ('SRC-Q-AXIS-RANSOMWARE-SUPP', RI)], 33)
add_alt('DDQ-BKP-0012', 'How long did a full restore take in your most recent test?', ['SRC-Q-ATBAY-CYBER-APP-2026', 'SRC-Q-AXIS-RANSOMWARE-SUPP'], 33)
# 34 recovery exercise
add_alt('DDQ-DR-0010', 'In the last 12 months, did a recovery exercise actually recover every system the service depends on?', ['SRC-Q-OHIO-U-VENDOR-BCP-Q', 'SRC-Q-SIFMA-COB-ASSESSMENT'], 34)
# 35 recovery objectives aligned to customer
add_alt('DDQ-DR-0001', 'Can your recovery objectives for this service be set to meet our required recovery time and recovery point?', [MSMIN, 'SRC-Q-SIFMA-COB-ASSESSMENT'], 35)
# 36 change notification
add_alt('DDQ-CHG-0004', 'Will you proactively notify us of any change that may affect us?', [MSMIN, MSTP], 36)

# ---- New questions for uncovered topics ----
new_q(next_id('DDQ', 'AIS', 4), 'ANS-AIS-005',
      'Is access to model artifacts, prompts, fine-tuning data, retrieval corpora and evaluation datasets limited to named roles and jobs, and is every read and change logged?',
      'AI data access', 'Model and dataset stores concentrate data derived from the customer and can be altered to change AI behavior.',
      'Unlogged or broad access to model data allows silent exfiltration or poisoning.',
      [ref(MSMIN), ref('SRC-CSA-AICM', RI)], ['financial-services', 'banking', 'enterprise-software'], ['global'],
      'contractual-common', 'medium', 4,
      scope='ANS-AIS-005 limits write access to retrieval corpora and evaluation sets to deterministic ingestion jobs; logged and role-restricted read access to model data is part of the same target and is not yet established.')

# 6 environmental footprint: new answer unit
aig_ans = next_id('ANS', 'AIG', 3)
new_record('answers', 'AIG', {
    'id': aig_ans, 'title': 'Environmental footprint of AI use', 'status': 'unknown',
    'status_rationale': 'No measurement or estimate of the energy use or emissions of AI coding agents used to build Echelon software, or of planned Unbound AI features, was located. AI provider environmental disclosures have not been collected, and no AI inventory exists (ANS-AIG-001).',
    'target_answer': 'Echelon records, for each AI provider and use in its AI inventory, the provider\'s published energy or emissions disclosure where one exists, estimates its own consumption from metered token or compute usage, and discloses the method and its limitations to customers on request. It makes no carbon neutrality or offset claim without an external basis.',
    'current_practice': 'Unknown; no measurement located.',
    'intended_practice': 'Add provider environmental disclosures and metered usage to the AI inventory (ANS-AIG-001) once that inventory exists.',
    'provable': 'Nothing.',
    'customer_statement': 'Echelon does not currently measure the environmental footprint of its AI use. It plans to report provider disclosures and usage-based estimates, with their limitations, on request.',
    'customer_statement_kind': 'not-available', 'assurance_independence': 'none',
    'controls': [], 'evidence_requirements': [],
    'evidence_freshness': 'P1Y', 'evidence_mechanism': 'not-defined', 'automation_potential': 'partial',
    'disclosure_classification': 'authenticated-prospect', 'implementation_cost': 'low', 'recurring_cost': 'low',
    'cost_basis': 'order-of-magnitude judgment, not sourced',
    'owner': 'Not assigned (proposed: Echelon AI governance owner)',
    'residual_risks': ['Provider disclosures are inconsistent and may not support a reliable per-customer estimate.'],
    'open_questions': ['Which AI providers used by Echelon publish usable energy or emissions data for the models in use?'],
    'history': H('created from DD-QNR-001 topic 6')})
stats['new_answer_units'] += 1
new_q(next_id('DDQ', 'AIG', 4), aig_ans,
      'Do you measure or estimate the energy use and environmental footprint of the AI features and AI tools used to deliver the service, and will you disclose it to us?',
      'AI environmental footprint', 'Mission-driven buyers weigh the environmental cost of AI use against their own commitments.',
      'The customer adopts AI-dependent services whose footprint conflicts with its stated commitments.',
      [ref('SRC-Q-ACLU-GENAI-VENDOR-Q'), ref('SRC-Q-AU-AI-PROCUREMENT', RI)],
      ['nonprofit', 'higher-education', 'donor-advised-funds'], ['US-states'], 'customer-preference', 'low', 6)

# 7 training for assigned personnel
new_q(next_id('DDQ', 'HR', 4), 'ANS-HR-002',
      'Does training for personnel assigned to our account cover safe use of AI tools and operational resilience as well as security, and will you report completion and other training metrics to us?',
      'Training content and reporting', 'Large buyers specify training content for the people who serve them and expect metrics, not only a statement that training exists.',
      'Personnel misuse AI tools or mishandle disruptions because training omitted those topics, and the customer cannot see it.',
      [ref(MSMIN)], ['financial-services', 'banking', 'wealth-management'], ['US-federal'], 'contractual-common', 'medium', 7)

# 9 countries of development, maintenance and support
new_q(next_id('DDQ', 'HR', 4), 'ANS-HR-007',
      'In which countries is the software developed and maintained, from which countries is support delivered, and will you give us advance notice before any of these locations change?',
      'Location of development and support', 'Buyers treat the location of development, maintenance and support as a risk and sometimes as a tax and invoicing disclosure.',
      'Work is moved to a jurisdiction the customer has not approved without notice.',
      [ref(FID), ref(MSTP), ref('SRC-Q-WI-DOA-10816')],
      ['financial-services', 'banking', 'wealth-management', 'public-sector', 'donor-advised-funds'], ['US-federal', 'US-states'],
      'contractual-common', 'high', 9,
      scope='ANS-HR-007 covers where personnel and contractors work; where customer data is stored and processed is answered by ANS-SUB-004.')

# 10 customer participation in entitlement reviews
new_q(next_id('DDQ', 'IAM', 4), 'ANS-IAM-008',
      'Can our designated managers approve access for our own users and periodically review their entitlements in your service, using a complete entitlement report that you provide?',
      'Customer entitlement review', 'The customer must govern its own employees\' access to vendor systems as part of its access control program.',
      'Customer users keep entitlements in the vendor system that the customer never approved or reviewed.',
      [ref(MSMIN)], ['financial-services', 'banking', 'wealth-management', 'donor-advised-funds'], ['US-federal'],
      'contractual-common', 'high', 10)

# 15 customer monitoring of vendor
new_q(next_id('DDQ', 'VUL', 4), 'ANS-VUL-005',
      'Will you accept our non-intrusive monitoring of your internet-facing assets, such as attack surface scanning, open-source intelligence and threat hunting, and how do you receive and act on findings we send you?',
      'Customer external monitoring', 'Some banks monitor higher-risk suppliers directly instead of relying only on questionnaires.',
      'Exposures the customer can see from outside are not received or acted on by the vendor.',
      [ref(TRUIST)], ['banking', 'financial-services'], ['US-federal'], 'contractual-common', 'medium', 15,
      scope='ANS-VUL-005 covers intake of externally reported vulnerabilities; agreement to customer-run external monitoring itself is not established.')

# 20 revocation of integrations at exit
new_q(next_id('DDQ', 'TRM', 4), 'ANS-TRM-002',
      'At exit, how do you revoke every API credential, federated trust relationship, webhook and partner integration tied to our tenant, and can you show evidence that each was revoked?',
      'Revocation at exit', 'Offboarding must remove technical access paths as well as data.',
      'An integration or federated trust left active after exit allows continued access to or from the customer\'s environment.',
      [ref(NYDFS), ref(MSMIN, RI)], ['financial-services', 'banking', 'donor-advised-funds'], ['US-state:NY', 'US-federal'],
      'supervisory-guidance', 'high', 20, authority='NYDFS (for covered entities)',
      scope='ANS-TRM-002 describes data return and deletion at exit; revocation evidence for credentials and integrations is part of the same offboarding target.')

# 21 continuity through resolution: new answer unit
trm_ans = next_id('ANS', 'TRM', 3)
new_record('answers', 'TRM', {
    'id': trm_ans, 'title': 'Service continuity through a customer\'s recovery, resolution or divestiture', 'status': 'unknown',
    'status_rationale': 'No Echelon contract position exists. Unbound exit requirements address customer-initiated termination and Echelon failure (ANS-TRM-001, ANS-TRM-003), not continuity while the customer is in recovery or resolution or divests part of its business.',
    'target_answer': 'Echelon\'s master agreement does not treat a customer\'s recovery, resolution or divestiture as a termination or default event. The service continues for a defined period at the fees and service levels in effect, may be extended to a successor or divested entity under a transitional order, and the tenant\'s data can be separated by legal entity through the standard export. Echelon\'s remedies in that period are limited to non-payment.',
    'current_practice': 'Not established.',
    'intended_practice': 'Decide a contract position before contracting with any bank-affiliated sponsor, and confirm that the export can be partitioned by legal entity.',
    'provable': 'Nothing.',
    'customer_statement': 'Echelon has not yet adopted a contract position on service continuity during a customer\'s recovery, resolution or divestiture. It expects to address it in its master agreement.',
    'customer_statement_kind': 'not-available', 'assurance_independence': 'none',
    'controls': [], 'evidence_requirements': [],
    'evidence_freshness': 'per-event', 'evidence_mechanism': 'not-defined', 'automation_potential': 'low',
    'disclosure_classification': 'nda', 'implementation_cost': 'low', 'recurring_cost': 'low',
    'cost_basis': 'order-of-magnitude judgment, not sourced',
    'owner': 'Not assigned (proposed: Echelon counsel)',
    'residual_risks': ['A small vendor that commits to continue service at existing fees during a customer resolution carries unpriced cost and collection risk.'],
    'open_questions': ['Can a tenant\'s data be partitioned by legal entity for a divestiture without breaking ledger integrity?'],
    'history': H('created from DD-QNR-001 topic 21')})
stats['new_answer_units'] += 1
new_q(next_id('DDQ', 'TRM', 4), trm_ans,
      'If we enter a recovery, resolution or divestiture event, will you continue the service on existing terms and allow a successor or divested entity to use it during the transition?',
      'Continuity in customer resolution', 'Bank resolution planning requires that critical services continue when the bank is in resolution or sells a business.',
      'A vendor terminates or reprices the service when the customer is most dependent on it.',
      [ref(MSTP)], ['banking', 'financial-services'], ['US-federal'], 'contractual-common', 'medium', 21)

# 23 reports before signature
new_q(next_id('DDQ', 'AUD', 4), 'ANS-AUD-001',
      'Will you make your assurance reports and security documentation available for our review before we sign the contract, and under what confidentiality terms?',
      'Pre-signature access to assurance', 'Buyers decide on the basis of assurance evidence and need it before committing.',
      'The customer signs before seeing evidence that would have changed its decision.',
      [ref('SRC-Q-ARIZONA-3P-SEC-PRIV-Q')], ['public-sector', 'higher-education', 'all'], ['US-states'], 'customer-preference', 'medium', 23,
      scope='No SOC 2 report exists; ANS-AUD-001 states what Echelon can share today.')

# 24 public records: new answer unit
aud_ans = next_id('ANS', 'AUD', 3)
new_record('answers', 'AUD', {
    'id': aud_ans, 'title': 'Security documentation for customers subject to public records laws', 'status': 'proposed-target-state',
    'status_rationale': 'No customer security documentation package exists, and no public-sector customer is planned or excluded. Records in this repository already carry a disclosure classification that could drive redaction.',
    'target_answer': 'Echelon prepares each customer-facing security document in two forms: a full version for the customer\'s evaluators and a redacted version suitable for release under public records laws. Confidentiality markings identify the specific passages and the exemption claimed (for example security-sensitive information) rather than marking whole documents. The redacted version is generated from the disclosure classification on each record rather than edited by hand.',
    'current_practice': 'Not established.',
    'intended_practice': 'Generate full and redacted documentation sets from the disclosure classification fields when a trust center or documentation package is built.',
    'provable': 'Nothing.',
    'customer_statement': 'Echelon does not yet have a security documentation package. It plans to provide full and redacted versions, with specific confidentiality markings, for customers subject to public records laws.',
    'customer_statement_kind': 'planned', 'assurance_independence': 'none',
    'controls': [], 'evidence_requirements': [],
    'evidence_freshness': 'per-event', 'evidence_mechanism': 'not-defined', 'automation_potential': 'high',
    'disclosure_classification': 'public', 'implementation_cost': 'low', 'recurring_cost': 'low',
    'cost_basis': 'order-of-magnitude judgment, not sourced',
    'owner': 'Not assigned (proposed: Echelon trust and assurance owner)',
    'residual_risks': ['A public body may still release material Echelon marked confidential if its own counsel decides no exemption applies.'],
    'open_questions': ['Does Echelon intend to sell to public universities or state entities whose submissions are subject to public records requests?'],
    'history': H('created from DD-QNR-001 topic 24')})
stats['new_answer_units'] += 1
new_q(next_id('DDQ', 'AUD', 4), aud_ans,
      'Because our procurement records are subject to public records laws, will you give us both a redacted and an unredacted copy of your security documentation, and how do you mark material you consider exempt from disclosure?',
      'Public records', 'Public-sector buyers can be compelled to release vendor submissions.',
      'Security-sensitive vendor documentation is released to the public.',
      [ref('SRC-Q-WI-DOA-10816')], ['public-sector', 'higher-education'], ['US-states'], 'contractual-common', 'low', 24)

# 29 overlay disclosure
new_q(next_id('DDQ', 'A11Y', 4), 'ANS-A11Y-001',
      'Does the product use an accessibility overlay or automated remediation widget, and will you commit not to add one as a substitute for conforming code?',
      'Overlay disclosure', 'Buyers view overlays as an unreliable substitute for accessible design.',
      'An overlay masks non-conformance and introduces its own barriers and legal exposure.',
      [ref('SRC-Q-YALE-ACCESSIBLE-PURCHASING')], ['higher-education', 'public-sector', 'all'], ['US-states', 'US-federal'],
      'customer-preference', 'medium', 29)

# 30 credential sharing
new_q(next_id('DDQ', 'API', 4), 'ANS-API-002',
      'Does any integration with the service, or with our accounts at other institutions, require donors or advisors to share their login credentials with you or with a third-party tool?',
      'Credential-free integration', 'A DAF sponsor warns donors never to share sponsor credentials with third-party tools.',
      'Credential sharing or screen scraping exposes donor accounts and breaks the sponsor\'s security model.',
      [ref('SRC-Q-FC-SECURITY-PAGE')], ['donor-advised-funds', 'wealth-management'], ['US-federal'], 'customer-preference', 'high', 30,
      products=['unbound'],
      scope='ANS-API-002 targets delegated, tenant-bound credentials for integrations; integration models that rely on donor or advisor credentials or screen scraping are not part of the target.')

# 34 turnover of key recovery staff
new_q(next_id('DDQ', 'BCP', 4), 'ANS-BCP-004',
      'Since your last recovery exercise, have any people with key recovery roles left or changed roles, and how do you confirm that their replacements can perform the recovery?',
      'Recovery staff turnover', 'An exercise proves capability only for the people who took part.',
      'Recovery fails because the people who knew how to perform it have left.',
      [ref('SRC-Q-SIFMA-COB-ASSESSMENT'), ref('SRC-Q-OHIO-U-VENDOR-BCP-Q')], ['financial-services', 'higher-education', 'all'], ['US-federal'],
      'industry-convention', 'medium', 34)

# 35 DR capacity parity
new_q(next_id('DDQ', 'DR', 4), 'ANS-DR-002',
      'Does your recovery environment have the capacity to run the service at normal production load, or will it run at reduced capacity after failover, and for how long?',
      'Recovery capacity', 'A recovery site that cannot carry production load turns a disaster into a long degradation.',
      'After failover the service cannot meet the customer\'s volume, for example during year-end giving.',
      [ref(MSMIN), ref('SRC-Q-SIFMA-COB-ASSESSMENT', RI)], ['financial-services', 'banking', 'donor-advised-funds'], ['US-federal'],
      'contractual-common', 'medium', 35)

# 36 material impairment notice
new_q(next_id('DDQ', 'FST', 4), 'ANS-FST-002',
      'Will you notify us promptly of any development that could materially impair your ability to provide the service, such as financial distress, litigation, regulatory action or loss of a critical provider?',
      'Material impairment notice', 'The customer needs early warning to activate contingency plans.',
      'The customer learns of a vendor\'s inability to perform only when the service fails.',
      [ref(MSTP)], ['banking', 'financial-services', 'donor-advised-funds'], ['US-federal'], 'contractual-common', 'high', 36,
      scope='ANS-FST-002 commits to notice on financial triggers; notice of non-financial developments such as litigation, regulatory action or loss of a critical provider is not yet covered by a stated commitment.')

# 37 sustainability and human rights: new answer unit
gov_ans1 = next_id('ANS', 'GOV', 3)
new_record('answers', 'GOV', {
    'id': gov_ans1, 'title': 'Supplier sustainability, human rights and modern slavery due diligence', 'status': 'unknown',
    'status_rationale': 'No Echelon policy or statement on human rights, modern slavery or environmental sustainability was located. Echelon\'s own supply chain is mainly cloud, AI and software providers, none of which has been assessed on these topics.',
    'target_answer': 'Echelon adopts a short supplier code covering human rights, forced and child labor, anti-corruption and environmental practices, keeps the published statements of its material providers (cloud, AI and payment providers), and answers customer sustainability questionnaires from that record. It does not claim certifications or emissions figures it has not measured.',
    'current_practice': 'Unknown; no policy or statement located.',
    'intended_practice': 'Adopt a supplier code and collect material providers\' published statements when the vendor inventory (ANS-TPR-001) is built.',
    'provable': 'Nothing.',
    'customer_statement': 'Echelon has not adopted a supplier code or sustainability statement. It can describe its small supply chain on request.',
    'customer_statement_kind': 'not-available', 'assurance_independence': 'none',
    'controls': [], 'evidence_requirements': [],
    'evidence_freshness': 'P1Y', 'evidence_mechanism': 'periodic-manual', 'automation_potential': 'low',
    'disclosure_classification': 'authenticated-prospect', 'implementation_cost': 'low', 'recurring_cost': 'low',
    'cost_basis': 'order-of-magnitude judgment, not sourced',
    'owner': 'Not assigned (proposed: Echelon governance owner)',
    'open_questions': ['Which customers require a formal supplier sustainability or modern slavery statement as a condition of onboarding?'],
    'history': H('created from DD-QNR-001 topic 37')})
stats['new_answer_units'] += 1
new_q(next_id('DDQ', 'GOV', 4), gov_ans1,
      'Do you perform and document due diligence on human rights, modern slavery and environmental sustainability in your own operations and supply chain, and will you complete our supplier sustainability questionnaire?',
      'Supplier sustainability and human rights', 'Large banks screen all suppliers, including software vendors, against their supplier codes.',
      'Onboarding stalls or the customer takes on supply-chain reputational risk.',
      [ref('SRC-Q-GS-VENDOR-CODE'), ref('SRC-Q-MS-SUPPLIER-CODE'), ref('SRC-Q-BOA-SUPPLIER-EXPECTATIONS')],
      ['banking', 'financial-services', 'wealth-management'], ['global'], 'customer-preference', 'low', 37)

# 38 gap disclosure and remediation plans: new answer unit, control, evidence requirement
gov_ans2 = next_id('ANS', 'GOV', 3)
gov_ctl = next_id('ECTL', 'GOV', 3)
gov_evr = next_id('EVR', 'GOV', 3)
new_record('evidence-requirements', 'GOV', {
    'id': gov_evr, 'title': 'Customer requirement gap register extract',
    'description': 'Per customer: each requirement not yet met, the answer unit and status it maps to, the agreed compensating control or dated remediation plan, the accountable owner, progress reports and the evidence that closed each item.',
    'producer': 'not yet assigned', 'mechanism': 'periodic-manual', 'freshness': 'P90D', 'format': 'JSON Lines or CSV extract',
    'independence': 'first-party', 'disclosure_classification': 'customer-only', 'status': 'proposed-target-state',
    'notes': f'{DATE} {BY}: created from DD-QNR-001 topic 38.'})
new_record('controls', 'GOV', {
    'id': gov_ctl, 'title': 'Customer requirement gap register tied to answer unit status',
    'objective': 'Every customer requirement Echelon cannot yet meet is disclosed before signature, carries a compensating control or dated remediation plan with an owner, and can be closed only with the evidence named by the corresponding answer unit.',
    'control_type': 'administrative', 'assurance_level': 'L10-external-or-manual',
    'implementing_systems': ['not yet assigned'],
    'status': 'proposed-target-state', 'evidence_requirements': [gov_evr],
    'owner': 'Not assigned (proposed: Echelon governance owner)',
    'residual_risks': ['A register maintained by hand can drift from the answer unit statuses it is meant to reflect.'],
    'notes': f'{DATE} {BY}: created from DD-QNR-001 topic 38.'})
new_record('answers', 'GOV', {
    'id': gov_ans2, 'title': 'Disclosure and remediation plans for customer requirements not yet met', 'status': 'proposed-target-state',
    'status_rationale': 'This repository records, per answer unit, whether a capability is operating, planned or unknown, but no customer-facing gap register, remediation plan format or progress reporting exists, and no remediation dates have been committed.',
    'target_answer': 'For each customer requirement Echelon cannot yet meet, Echelon discloses the gap before contract signature using the status of the corresponding answer unit, proposes a compensating control or a dated remediation plan with an accountable owner, records the agreed item in a gap register tied to the contract, and reports progress at an agreed cadence. An item cannot be closed without the evidence named by the answer unit\'s evidence requirements. Where a customer offers an accommodation path for small suppliers, Echelon uses it rather than overstating its maturity.',
    'current_practice': 'Not established. Answer unit statuses in this repository are the only existing record of gaps.',
    'intended_practice': 'Generate the customer gap register from answer unit statuses and contract requirements, with remediation plans added by the accountable owner.',
    'provable': 'Only the first-party answer unit statuses in this repository; no customer gap register exists.',
    'customer_statement': 'Echelon will tell you which of your requirements it does not yet meet. A formal gap register with remediation plans and progress reporting is planned.',
    'customer_statement_kind': 'planned', 'assurance_independence': 'none',
    'controls': [gov_ctl], 'evidence_requirements': [gov_evr],
    'evidence_freshness': 'P90D', 'evidence_mechanism': 'periodic-manual', 'automation_potential': 'high',
    'disclosure_classification': 'customer-only', 'implementation_cost': 'low', 'recurring_cost': 'low',
    'cost_basis': 'order-of-magnitude judgment, not sourced',
    'owner': 'Not assigned (proposed: Echelon governance owner)',
    'challenge': {
        'customer_intent': 'The customer wants to know which of its requirements are unmet and whether the vendor will close them, before it relies on the vendor.',
        'adverse_outcome': 'A vendor answers yes to requirements it does not meet, and the gap is found after an incident or an examination.',
        'conventional_control_effectiveness': 'Questionnaire answers are usually self-reported yes or no responses with remediation promised informally; customers rarely track the promises.',
        'legally_required': 'No law requires this of Echelon. Supervisory third-party risk guidance expects banks to track vendor issues, which flows to vendors through contracts.',
        'contractually_required': 'Some bank supplier documents set remediation deadlines for assessment findings and describe accommodation paths for small suppliers.',
        'historical_convention': 'Plans of action and milestones are common in federal security programs and attestation forms.',
        'architectural_elimination': 'Not applicable; this is a disclosure and tracking control.',
        'automatic_enforcement': 'Answer unit status is a controlled field, so a gap can be derived mechanically and an item cannot be reported closed while the underlying status is not operational.',
        'continuous_evidence': 'The register extract and the status history of the linked answer units.',
        'stronger_alternative': 'Derive customer gap disclosures from answer unit status instead of writing them per questionnaire.',
        'alternative_verifiable': 'The customer can compare register items with the answer units and evidence requirements they cite.',
        'customer_acceptance_likelihood': 'Likely for buyers with small-supplier programs; uncertain for buyers that require full compliance at onboarding.',
        'invalidating_conditions': 'Fails if answer unit statuses are not kept current or are changed upward without evidence.',
        'conventional_cost': 'low',
        'alternative_cost': 'low',
        'alternative_risks': 'Candid disclosure of many gaps may lose deals that an overstated answer would have won in the short term.',
        'supporting_arguments': ['Honest gap disclosure is consistent with the operating contract\'s rule against presenting planned controls as current.', 'Generated disclosures reduce inconsistency between questionnaires.'],
        'opposing_arguments': ['Customers may treat a long gap list as disqualifying regardless of remediation plans.', 'Remediation dates committed by a pre-revenue vendor may not be credible.'],
        'technical_effectiveness': 'stronger',
        'institutional_acceptance': 'uncertain'},
    'open_questions': ['Which target customers publish an accommodation or remediation path for small suppliers?'],
    'history': H('created from DD-QNR-001 topic 38')})
stats['new_answer_units'] += 1
stats['new_controls'] += 1
stats['new_evidence_requirements'] += 1
new_q(next_id('DDQ', 'GOV', 4), gov_ans2,
      'Where you cannot yet meet one of our supplier requirements, will you disclose the gap, propose a dated remediation plan or compensating control, and report progress until it is closed?',
      'Gap disclosure and remediation', 'Some buyers document a path for small suppliers that cannot yet meet every expectation.',
      'Unmet requirements are concealed or never closed.',
      [ref('SRC-Q-BOA-SUPPLIER-EXPECTATIONS')], ['all'], ['US-federal'], 'customer-preference', 'medium', 38)

# Topic 29: overlay statement in ANS-A11Y-001 target
a = R('ANS-A11Y-001')
a['target_answer'] = a['target_answer'].rstrip() + ' Conformance is achieved in the code and components themselves; Echelon does not use accessibility overlays or automated remediation widgets.'
note(a, 'Target answer states that no accessibility overlay is used (DD-QNR-001 topic 29); status unchanged')

# ============================================================
# TASK 2: stale-reference sweep
# ============================================================
# --- SR 11-7 and SR 21-8 superseded by SR 26-2
SRNOTE = 'Replaced superseded SRC-SR-11-7 with SRC-SR-26-2 (SR 26-2 superseded SR 11-7 and SR 21-8 on 2026-04-17); basis set to reasonably-inferred because the SR 26-2 guidance attachment has not been read'
q = R('DDQ-AIG-0035')
replace_ref(q, 'SRC-SR-11-7', 'SRC-SR-26-2', basis=RI)
add_ref(q, 'SRC-SR-11-7', RI, 'informed-by')
q['alternatives'].append('Will your models meet our SR 11-7 model risk management requirements?')
q['regulatory_authority'] = 'Federal Reserve; OCC; FDIC'
q['answer_scope_note'] = 'SR 26-2 (2026-04-17, Federal Reserve, OCC and FDIC) superseded SR 11-7 and SR 21-8; bank questionnaires may still cite SR 11-7, which is kept here as a historical reference. This is supervisory guidance to banks and reaches Echelon only through the bank\'s contract.'
note(q, SRNOTE + '; kept SRC-SR-11-7 as informed-by for historical questionnaire wording; added legacy SR 11-7 wording as an alternative; regulatory authority now includes FDIC')
for qid in ['DDQ-AIG-0036', 'DDQ-AIG-0037']:
    q = R(qid)
    replace_ref(q, 'SRC-SR-11-7', 'SRC-SR-26-2', basis=RI)
    q['regulatory_authority'] = 'Federal Reserve; OCC; FDIC'
    note(q, SRNOTE + '; regulatory authority now includes FDIC')
for qid in ['DDQ-AIG-0038', 'DDQ-AML-0013', 'DDQ-AML-0016', 'DDQ-FRD-0036']:
    q = R(qid)
    replace_ref(q, 'SRC-SR-11-7', 'SRC-SR-26-2', basis=RI)
    note(q, SRNOTE)
for cid in ['ECTL-AIG-010', 'ECTL-AML-004']:
    c = R(cid)
    replace_ref(c, 'SRC-SR-11-7', 'SRC-SR-26-2', field='framework_refs', basis=RI)
    note(c, 'framework_refs: replaced superseded SRC-SR-11-7 with SRC-SR-26-2.')
a = R('ANS-AIG-008')
a['title'] = 'Model risk management support for bank customers (SR 26-2 expectations, which superseded SR 11-7 and OCC 2011-12, applied to vendor models)'
set_text(a, 'challenge.conventional_control_effectiveness', 'Classic SR 11-7 validation', 'Traditional model validation of the kind described in SR 11-7 (now superseded by SR 26-2)')
a['challenge']['legally_required'] = 'SR 26-2, which superseded SR 11-7 and SR 21-8 on 2026-04-17, is supervisory guidance to banks, not a law binding Echelon; banks apply it to vendor products through contracts. SR 26-2 emphasizes a risk-based, tailored approach; whether it addresses generative AI specifically has not been verified.'
a.setdefault('open_questions', []).append('Does SR 26-2 change documentation or validation expectations for vendor models or generative AI compared with SR 11-7? The guidance attachment has not been read.')
note(a, 'Stale reference corrected: SR 11-7 and SR 21-8 superseded by SR 26-2 (SRC-SR-26-2); title, challenge text and open questions updated; status unchanged')
stats['stale_records_corrected'] += 0  # counted below via log

# --- Colorado AI Act repealed and reenacted by SB 26-189
CONOTE = 'Replaced SRC-COLORADO-AI-ACT with SRC-COLORADO-SB26-189 (SB 26-189, signed 2026-05-14, repealed and reenacted the Colorado AI Act as an automated decision-making technology law)'
for qid in ['DDQ-AIG-0017', 'DDQ-AIG-0018', 'DDQ-AIA-0025', 'DDQ-SUP-0016']:
    q = R(qid)
    replace_ref(q, 'SRC-COLORADO-AI-ACT', 'SRC-COLORADO-SB26-189')
    note(q, CONOTE)
q = R('DDQ-AIG-0031')
old = q['question']
q['question'] = 'Does Colorado\'s automated decision-making technology law (SB 26-189, which repealed and reenacted the Colorado AI Act) apply to any of your systems as a developer or deployer, and what documentation will you provide to us as deployer?'
q['alternatives'] = [old]
q['subcategory'] = 'Colorado ADMT law'
q['business_concern'] = 'Colorado imposes documentation duties on developers of covered automated decision-making technology from 2027-01-01, and duties on deployers.'
q['source_refs'] = [ref('SRC-COLORADO-SB26-189', RI)]
stats['stale_refs_replaced'] += 2
q['open_questions'] = ['Does any Unbound function materially influence a consequential decision about a Colorado individual, such as a decision on financial services, under SB 26-189?']
note(q, CONOTE + '; question reworded with the former wording kept as an alternative; SB 24-205 section locators removed because the reenacted law was not mapped; open question on the SB 24-205 effective date replaced')
q = R('DDQ-LEG-0040')
replace_ref(q, 'SRC-COLORADO-AI-ACT', 'SRC-COLORADO-SB26-189')
add_ref(q, 'SRC-EU-AI-OMNIBUS-2026', RI, 'informed-by')
q['alternatives'].append('Is your system covered by Colorado\'s automated decision-making technology law?')
note(q, CONOTE + '; added SRC-EU-AI-OMNIBUS-2026 because EU AI Act high-risk application dates changed; added current Colorado wording as an alternative')
for cid in ['ECTL-AIG-009', 'ECTL-AIG-011']:
    c = R(cid)
    replace_ref(c, 'SRC-COLORADO-AI-ACT', 'SRC-COLORADO-SB26-189', field='framework_refs')
    if cid == 'ECTL-AIG-009':
        add_ref(c, 'SRC-EU-AI-OMNIBUS-2026', RI, field='framework_refs')
        note(c, 'framework_refs: replaced SRC-COLORADO-AI-ACT with SRC-COLORADO-SB26-189 and added SRC-EU-AI-OMNIBUS-2026 (amended EU AI Act application dates).')
    else:
        note(c, 'framework_refs: replaced SRC-COLORADO-AI-ACT with SRC-COLORADO-SB26-189.')
a = R('ANS-AIG-007')
a['title'] = 'Applicability of AI-specific law (EU AI Act as amended by Regulation (EU) 2026/1744, Colorado ADMT law SB 26-189, state automated decision rules, NAIC bulletin)'
set_text(a, 'target_answer', 'For EU AI Act, Echelon records whether any system falls in Article 6 and Annex III,',
         'For the EU AI Act, using the application dates set by Regulation (EU) 2026/1744 (Annex III high-risk obligations from 2027-12-02, Annex I from 2028-08-02), Echelon records whether any system falls in Article 6 and Annex III,')
set_text(a, 'target_answer', 'For the Colorado AI Act, Echelon records whether any AI use is a substantial factor in a consequential decision and, if so, provides deployers the documentation the law requires.',
         'For Colorado SB 26-189, which repealed and reenacted the Colorado AI Act as an automated decision-making technology law with developer documentation duties from 2027-01-01, Echelon records whether any function materially influences a consequential decision about a Colorado individual and, if so, provides deployers the documentation the law requires.')
a['open_questions'][0] = 'Does any Unbound function qualify as covered automated decision-making technology under Colorado SB 26-189, whose developer duties begin 2027-01-01?'
note(a, 'Stale references corrected: Colorado AI Act replaced by SB 26-189 (SRC-COLORADO-SB26-189) and EU AI Act dates changed by Regulation (EU) 2026/1744 (SRC-EU-AI-OMNIBUS-2026); title, target answer and open question updated; status unchanged')
a = R('ANS-AIG-004')
set_text(a, 'target_answer', '(EU AI Act, Colorado AI Act)', '(EU AI Act as amended by Regulation (EU) 2026/1744, Colorado SB 26-189)')
note(a, 'Stale reference corrected: Colorado AI Act replaced by SB 26-189; EU AI Act noted as amended by Regulation (EU) 2026/1744; status unchanged')

# --- EU AI Act dates changed by the omnibus
q = R('DDQ-AIG-0030')
add_ref(q, 'SRC-EU-AI-OMNIBUS-2026', 'directly-documented', 'maps-to')
q['answer_scope_note'] += ' As amended by Regulation (EU) 2026/1744, Annex III high-risk obligations apply from 2027-12-02 and Annex I high-risk obligations from 2028-08-02.'
note(q, 'Added SRC-EU-AI-OMNIBUS-2026 and the amended high-risk application dates to the scope note')
q = R('DDQ-AIG-0034')
add_ref(q, 'SRC-EU-AI-OMNIBUS-2026', RI, 'maps-to')
q['answer_scope_note'] = 'Applies only if Echelon places AI systems on the EU market or their output is used in the EU; no EU exposure is established. Under Regulation (EU) 2026/1744, Article 50(2) applies from 2026-12-02 to synthetic-content systems placed on the market before 2026-08-02.'
note(q, 'Added SRC-EU-AI-OMNIBUS-2026 and the amended Article 50(2) date in a new scope note')

# --- OMB M-22-18 rescinded by M-26-05; NTIA SBOM elements replaced by CISA 2026
OMBNOTE = 'Replaced rescinded SRC-OMB-M-22-18 with SRC-OMB-M-26-05 (M-26-05, 2026-01-23, rescinded M-22-18 and M-23-16; agencies no longer must collect the CISA attestation form)'
NTIANOTE = 'Replaced superseded SRC-NTIA-SBOM-MIN with SRC-CISA-SBOM-MIN (the CISA 2026 minimum elements replace the NTIA 2021 elements)'


def ntia(r, field='source_refs'):
    replace_ref(r, 'SRC-NTIA-SBOM-MIN', 'SRC-CISA-SBOM-MIN', field=field)


q = R('DDQ-ASM-0005')
ntia(q)
replace_ref(q, 'SRC-OMB-M-22-18', 'SRC-OMB-M-26-05')
q['answer_scope_note'] = 'OMB M-26-05 (2026-01-23) rescinded M-22-18; federal agencies now choose risk-based assurance and may request an SBOM. For private-sector customers an SBOM request is a customer preference.'
note(q, NTIANOTE + '; ' + OMBNOTE + '; scope note updated')
q = R('DDQ-IPR-0013')
ntia(q)
replace_ref(q, 'SRC-OMB-M-22-18', 'SRC-OMB-M-26-05')
for x in q['source_refs']:
    if x['source_id'] == 'SRC-CISA-SBOM-MIN':
        x['relation'], x['basis'] = 'maps-to', 'directly-documented'
note(q, NTIANOTE + ' (the CISA 2026 elements include component license); ' + OMBNOTE)
q = R('DDQ-SCS-0011')
ntia(q)
replace_ref(q, 'SRC-OMB-M-22-18', 'SRC-OMB-M-26-05', relation='informed-by')
note(q, NTIANOTE + '; ' + OMBNOTE)
q = R('DDQ-SCS-0013')
old = q['question']
q['question'] = 'Will you provide SBOMs and related artifacts when a federal agency requests them under its risk-based software assurance approach?'
q['alternatives'] = [old]
replace_ref(q, 'SRC-OMB-M-22-18', 'SRC-OMB-M-26-05', basis='directly-documented')
for x in q['source_refs']:
    if x['source_id'] == 'SRC-CISA-SSDF-ATTESTATION':
        x['relation'] = 'informed-by'
q['answer_scope_note'] = 'OMB M-26-05 (2026-01-23) rescinded M-22-18 and M-23-16. Agencies no longer must collect the CISA attestation form but may still request an SBOM (for cloud services, of the runtime production environment).'
note(q, OMBNOTE + '; question reworded because federal SBOM provision is now on request rather than required, with the former wording kept as an alternative; attestation form reference changed to informed-by')
for qid in ['DDQ-SDL-0039', 'DDQ-SDL-0040']:
    q = R(qid)
    replace_ref(q, 'SRC-OMB-M-22-18', 'SRC-OMB-M-26-05', relation='informed-by')
    q['answer_scope_note'] = 'No longer required for federal sales: OMB M-26-05 (2026-01-23) rescinded M-22-18 and M-23-16, so agencies no longer have to collect the CISA common form, though they may still choose to use it; some private buyers borrow its questions.'
    note(q, OMBNOTE + '; scope note updated')
c = R('ECTL-SDL-008')
replace_ref(c, 'SRC-OMB-M-22-18', 'SRC-OMB-M-26-05', field='framework_refs', relation='informed-by')
note(c, 'framework_refs: replaced rescinded SRC-OMB-M-22-18 with SRC-OMB-M-26-05 (informed-by); the attestation form is now optional for agencies.')
a = R('ANS-SCS-005')
a['challenge']['legally_required'] = 'No. OMB M-22-18, which tied federal software purchases to a secure development attestation that referenced provenance practices, was rescinded by OMB M-26-05 (2026-01-23); agencies now choose risk-based assurance and may still ask for provenance or SBOM artifacts.'
note(a, 'Stale reference corrected: OMB M-22-18 rescinded by M-26-05; challenge text updated; status unchanged')
a = R('ANS-SDL-008')
a['status_rationale'] += ' OMB M-26-05 (2026-01-23) rescinded M-22-18 and M-23-16, so federal agencies no longer must collect the CISA attestation form; demand for an attestation now comes from customers that choose to use it.'
note(a, 'Stale reference corrected: OMB M-22-18 rescinded by M-26-05; status rationale updated; status unchanged')
for qid in ['DDQ-AIS-0025', 'DDQ-ESC-0002', 'DDQ-ESC-0013', 'DDQ-INF-0014', 'DDQ-IPR-0008', 'DDQ-IPR-0010', 'DDQ-IPR-0011',
            'DDQ-IPR-0012', 'DDQ-SCS-0012', 'DDQ-SCS-0015', 'DDQ-SCS-0016', 'DDQ-VUL-0017', 'DDQ-VUL-0032']:
    q = R(qid)
    ntia(q)
    note(q, NTIANOTE)
for cid in ['ECTL-ASM-002', 'ECTL-IPR-001', 'ECTL-SCS-003']:
    c = R(cid)
    ntia(c, 'framework_refs')
    note(c, 'framework_refs: replaced superseded SRC-NTIA-SBOM-MIN with SRC-CISA-SBOM-MIN.')
a = R('ANS-SCS-003')
for f in ['target_answer', 'intended_practice']:
    set_text(a, f, 'meeting NTIA minimum elements', 'meeting the CISA 2026 SBOM minimum elements, which replaced the NTIA 2021 minimum elements')
note(a, 'Stale reference corrected: NTIA SBOM minimum elements replaced by CISA 2026 minimum elements; target and intended practice updated; status unchanged')
e = R('EVR-SCS-003')
set_text(e, 'description', 'meeting NTIA minimum elements', 'meeting the CISA 2026 SBOM minimum elements')
note(e, 'NTIA minimum elements replaced by CISA 2026 SBOM minimum elements.')

# --- CISA BOD 22-01 replaced by BOD 26-04
BODNOTE = 'Replaced revoked SRC-CISA-BOD-22-01 with SRC-CISA-BOD-26-04 (BOD 26-04 replaced BOD 22-01 on 2026-06-10)'
for qid in ['DDQ-CHG-0020', 'DDQ-INF-0009', 'DDQ-ISP-0025', 'DDQ-VUL-0009']:
    q = R(qid)
    replace_ref(q, 'SRC-CISA-BOD-22-01', 'SRC-CISA-BOD-26-04')
    if qid == 'DDQ-VUL-0009':
        q['answer_scope_note'] = 'BOD 26-04, which replaced BOD 22-01 on 2026-06-10 and carries forward the KEV criteria, binds federal civilian agencies only; cited as a benchmark for timelines.'
        note(q, BODNOTE + '; scope note updated')
    else:
        note(q, BODNOTE)
a = R('ANS-INF-003')
set_text(a, 'challenge.legally_required', 'Federal agencies are bound by BOD 22-01 for KEV entries', 'Federal civilian agencies are bound by BOD 26-04 (which replaced BOD 22-01 on 2026-06-10) for KEV entries')
note(a, 'Stale reference corrected: BOD 22-01 replaced by BOD 26-04; challenge text updated; status unchanged')
a = R('ANS-VUL-002')
set_text(a, 'challenge.legally_required', 'BOD 22-01 KEV deadlines', 'KEV deadlines under BOD 26-04 (which replaced BOD 22-01 on 2026-06-10)')
note(a, 'Stale reference corrected: BOD 22-01 replaced by BOD 26-04; challenge text updated; status unchanged')

# --- OWASP LLM Top 10 2025 superseded by 2026
# 2025 -> 2026 numbering verified against genai.owasp.org 2026 list on 2026-11-25:
# 01 Prompt Injection -> 01; 02 Sensitive Information Disclosure -> 02; 03 Supply Chain -> 04;
# 04 Data and Model Poisoning -> 05; 05 Improper Output Handling -> 10; 06 Excessive Agency -> 03;
# 07 System Prompt Leakage -> no verified equivalent; 08 Vector and Embedding Weaknesses -> 09;
# 09 Misinformation -> 07; 10 Unbounded Consumption -> 06
LLMMAP = {1: 1, 2: 2, 3: 4, 4: 5, 5: 10, 6: 3, 8: 9, 9: 7, 10: 6}
dropped = []


def llm_loc(loc):
    m = re.match(r'^LLM(\d\d)(?::2025)?$', loc)
    assert m, loc
    n = int(m.group(1))
    if n not in LLMMAP:
        dropped.append(loc)
        return None
    return f'LLM{LLMMAP[n]:02d}:2026'


for d in ['questions', 'controls']:
    field = 'source_refs' if d == 'questions' else 'framework_refs'
    for b, recs in files[d].items():
        for r in recs:
            if any(x['source_id'] == 'SRC-OWASP-LLM-TOP10-2025' for x in r.get(field, [])):
                olds = [x.get('locator') for x in r[field] if x['source_id'] == 'SRC-OWASP-LLM-TOP10-2025']
                replace_ref(r, 'SRC-OWASP-LLM-TOP10-2025', 'SRC-OWASP-LLM-TOP10-2026', field=field, locmap=llm_loc)
                news = [x.get('locator') for x in r[field] if x['source_id'] == 'SRC-OWASP-LLM-TOP10-2026']
                msg = 'Replaced superseded SRC-OWASP-LLM-TOP10-2025 with SRC-OWASP-LLM-TOP10-2026'
                if any(olds):
                    msg += f'; locators remapped to 2026 numbering ({", ".join(str(o) for o in olds)} to {", ".join(str(n) if n else "no locator" for n in news)})'
                    if any(o and re.match(r'^LLM07', o) for o in olds):
                        msg += '; LLM07:2025 (system prompt leakage) has no verified 2026 equivalent, so its locator was dropped'
                if d == 'controls':
                    msg = 'framework_refs: ' + msg + '.'
                note(r, msg)
q = R('DDQ-AIS-0029')
old = q['question']
q['question'] = 'Have you threat-modeled your AI features against the OWASP Top 10 for LLM Applications 2026? Can you share coverage?'
q['alternatives'].append(old)
note(q, 'Question updated to the 2026 OWASP LLM Top 10 edition; 2025 wording kept as an alternative')
a = R('ANS-AIS-006')
set_text(a, 'target_answer', 'OWASP LLM Top 10 2025 item', 'OWASP LLM Top 10 2026 item')
note(a, 'Stale reference corrected: OWASP LLM Top 10 2025 superseded by the 2026 edition; target answer updated; status unchanged')
a = R('ANS-AUZ-008')
set_text(a, 'challenge.supporting_arguments.1', 'OWASP LLM06 excessive agency', 'OWASP LLM03:2026 excessive agency (LLM06 in the 2025 edition)')
note(a, 'Stale reference corrected: OWASP LLM Top 10 numbering updated to the 2026 edition; status unchanged')

# --- SEC adviser outsourcing proposal withdrawn
for qid in ['DDQ-IR-0027', 'DDQ-REG-0011']:
    q = R(qid)
    q['source_refs'] = [x for x in q['source_refs'] if x['source_id'] != 'SRC-SEC-ADVISER-OUTSOURCING-PROPOSAL']
    add_ref(q, 'SRC-SEC-PROPOSAL-WITHDRAWAL-2025', 'directly-documented', 'informed-by')
    stats['stale_refs_replaced'] += 1
    sn = 'The SEC proposal on outsourcing by investment advisers (S7-25-22) was withdrawn on 2025-06-17 and is not a source of obligations; adviser vendor oversight rests on existing rules such as Regulation S-P.'
    q['answer_scope_note'] = (q['answer_scope_note'] + ' ' + sn) if q.get('answer_scope_note') else sn
    note(q, 'Removed reference to the withdrawn SEC adviser outsourcing proposal (SRC-SEC-ADVISER-OUTSOURCING-PROPOSAL) and cited its withdrawal (SRC-SEC-PROPOSAL-WITHDRAWAL-2025) as informed-by; scope note added')

# --- Nacha fraud monitoring Phase 2 in force for all TPSPs
a = R('ANS-FRD-008')
oq0 = a['open_questions'][0]
assert oq0.startswith('Which Nacha fraud-monitoring phase')
a['open_questions'][0] = 'For each ODFI relationship, is Unbound a Third-Party Service Provider or closer to a Third-Party Sender (CNV-PAY-001 versus CNV-LEG-001), and does that change which fraud monitoring duties it carries?'
a['status_rationale'] += ' Nacha fraud monitoring Phase 2 took effect June 19, 2026 (practically June 22, 2026) and removed the volume threshold, so the risk-based fraud monitoring rule applies to Unbound in any TPSP role and to every sponsor Originator regardless of volume (SRC-NACHA-FRAUD-MONITORING-2026).'
a['challenge']['legally_required'] += ' Since Phase 2 took effect in June 2026 the rule applies to all TPSPs, Third-Party Senders and non-consumer Originators regardless of volume.'
note(a, 'Stale fact corrected: open question on which Nacha phase and volume threshold apply resolved (Phase 2 in force since June 2026 for all TPSPs regardless of volume); replaced with the remaining role question; status unchanged')
q = R('DDQ-FRD-0032')
q['answer_scope_note'] = 'Phase 2 of the Nacha fraud monitoring amendments took effect June 19, 2026 (practically June 22, 2026) and removed the volume threshold; the rule now applies to all non-consumer Originators, TPSPs and Third-Party Senders.'
note(q, 'Scope note added: Nacha fraud monitoring Phase 2 in force for all TPSPs since June 2026')

# --- ADA Title II compliance dates extended
q = R('DDQ-A11Y-0028')
set_text(q, 'answer_scope_note', 'Compliance dates should be verified against current DOJ publications.',
         'A DOJ interim final rule (effective 2026-04-20) extended compliance dates to 2027-04-26 for public entities with a population of 50,000 or more and 2028-04-26 for smaller entities and special districts.')
note(q, 'Stale fact corrected: ADA Title II web rule compliance dates extended (SRC-ADA)')
a = R('ANS-A11Y-007')
oq = 'What are the current DOJ Title II compliance dates? Verify, as they may have been revised after the 2024 rule.'
a['open_questions'].remove(oq)
a['status_rationale'] += ' The DOJ Title II web rule compliance dates were extended by interim final rule (effective 2026-04-20) to 2027-04-26 for public entities of 50,000 or more population and 2028-04-26 for smaller entities (SRC-ADA).'
note(a, 'Stale fact corrected: open question on DOJ Title II compliance dates resolved with the extended dates; status unchanged')

# --- FinCEN investment adviser AML rule postponed
a = R('ANS-AML-006')
assert a['open_questions'][0].startswith('Does the FinCEN investment adviser AML rule')
a['open_questions'][0] = 'The FinCEN investment adviser AML rule now takes effect January 1, 2028 (SRC-FINCEN-IA-AML-RULE-2024); will it change any target customer\'s expectations of Unbound before or after that date?'
note(a, 'Stale fact corrected: FinCEN investment adviser AML rule effective date postponed to 2028-01-01; open question updated; status unchanged')

# --- IRC 170 amended by Pub. L. 119-21: new question on donor-facing tax content
new_q(next_id('DDQ', 'RRP', 4), 'ANS-RRP-002',
      'Do donor-facing tax disclosures and acknowledgments reflect the 2025 amendments to IRC 170 by Pub. L. 119-21, including that the new deduction for donors who do not itemize excludes contributions to donor-advised funds?',
      'Tax disclosure currency', 'Donor-facing tax content must track changes in the law it describes.',
      'Donors are told, or led to believe, that a DAF contribution qualifies for the non-itemizer deduction.',
      [ref('SRC-IRC-170')], ['donor-advised-funds', 'nonprofit'], ['US-federal'], 'industry-convention', 'high', 'stale-reference sweep: IRC 170 amended by Pub. L. 119-21',
      products=['unbound'], authority='IRS',
      scope='ANS-RRP-002 already requires that tax disclosures never imply non-itemizer deductibility. The 0.5 percent floor added by Pub. L. 119-21 affects donors\' own deduction calculations, which Unbound does not compute.')

# --- Prose correction: XID-BNK-003 is an open counsel question, not a fixed rule
a = R('ANS-RRP-007')
for f in ['target_answer', 'intended_practice']:
    set_text(a, f, '(fixed rule XID-BNK-003)', '(pending counsel question XID-BNK-003 in the Unbound cross-industry discovery)')
note(a, 'Corrected citation: XID-BNK-003 is an open counsel question in Unbound cross-industry discovery, not a fixed rule; status unchanged')

# ============================================================
# TASK 3: duplicates and overlaps
# ============================================================
# D1: merge DDQ-FCT-0015 into DDQ-FEE-0015 (build NEAR-DUP, jaccard 0.86)
src = R('DDQ-FCT-0015')
dst = R('DDQ-FEE-0015')
dst.setdefault('alternatives', []).append(src['question'])
for x in src['source_refs']:
    if not any(y['source_id'] == x['source_id'] and y.get('locator') == x.get('locator') for y in dst['source_refs']):
        dst['source_refs'].append(x)
for f in ['industries']:
    for v in src[f]:
        if v not in dst[f]:
            dst[f].append(v)
note(dst, 'Merged DDQ-FCT-0015 (near-duplicate wording) into this question as an alternative; DDQ-FCT-0015 retired', )
dst['history'][-1]['decision_ref'] = 'DDD-002'
files['questions']['FCT.jsonl'].remove(src)
del index['DDQ-FCT-0015']
stats['dedup_decisions'] += 1

# D2: ASM versus SCS SBOM overlap
q = R('DDQ-ASM-0005')
s = R('ANS-SCS-003')
q['answer_unit'] = 'ANS-SCS-003'
q['controls'] = list(s['controls'])
q['evidence_requirements'] = list(s['evidence_requirements'])
q['answer_scope_note'] += ' Redundant with DDQ-SCS-0011: SBOM production and sharing is answered once in ANS-SCS-003; ANS-ASM-002 covers the broader component inventory, including internal frameworks and AI components (DDQ-ASM-0006 to DDQ-ASM-0009).'
note(q, 'Repointed from ANS-ASM-002 to ANS-SCS-003 to resolve the ASM versus SCS SBOM overlap; controls and evidence requirements aligned to ANS-SCS-003')
q['history'][-1]['decision_ref'] = 'DDD-002'
q2 = R('DDQ-SCS-0011')
q2['alternatives'].append(q['question'])
note(q2, 'Added the wording of DDQ-ASM-0005 as an alternative (SBOM overlap resolution)')
q2['history'][-1]['decision_ref'] = 'DDD-002'
stats['dedup_decisions'] += 1

# D3: LEG-0011 is the same bank incident notification question as IR-0021
q = R('DDQ-LEG-0011')
s = R('ANS-IR-005')
q['answer_unit'] = 'ANS-IR-005'
q['controls'] = list(s['controls'])
q['evidence_requirements'] = list(s['evidence_requirements'])
q['answer_scope_note'] += ' Redundant with DDQ-IR-0021 (same Computer-Security Incident Notification rule duty); answered once in ANS-IR-005. ANS-LEG-003 covers notification obligations generally.'
note(q, 'Repointed from ANS-LEG-003 to ANS-IR-005, which answers the bank service provider notification duty; controls and evidence requirements aligned')
q['history'][-1]['decision_ref'] = 'DDD-002'
stats['dedup_decisions'] += 1

# D4: ACT-0034 duplicates RRP-0002 (Schedule D reconciliation)
q = R('DDQ-ACT-0034')
s = R('ANS-RRP-001')
q['answer_unit'] = 'ANS-RRP-001'
q['controls'] = list(s['controls'])
q['evidence_requirements'] = list(s['evidence_requirements'])
q['answer_scope_note'] = 'Redundant with DDQ-RRP-0002; Schedule D reconciliation is answered once in ANS-RRP-001. ANS-ACT-008 covers reproducible statements and audit support generally.'
note(q, 'Repointed from ANS-ACT-008 to ANS-RRP-001 (Schedule D reconciliation duplicate of DDQ-RRP-0002); controls and evidence requirements aligned')
q['history'][-1]['decision_ref'] = 'DDD-002'
stats['dedup_decisions'] += 1

# D5: CHG-0027 versus INF-0023 and ASM-0019 (kept distinct, scope note)
q = R('DDQ-CHG-0027')
q['answer_scope_note'] = 'Covers unauthorized changes to deployed code, infrastructure definitions and production data paths. Drift of configuration settings is answered by ANS-INF-007 (DDQ-INF-0023) and drift from secure baselines by ANS-ASM-005 (DDQ-ASM-0019).'
note(q, 'Scope note added after overlap review with DDQ-INF-0023 and DDQ-ASM-0019; kept distinct')
q['history'][-1]['decision_ref'] = 'DDD-002'
stats['dedup_decisions'] += 1
# D6 (AIG-0011 vs INV-0025) is a lexical false positive: recorded in DDD-002 only.
stats['dedup_decisions'] += 1

# ============================================================
# write
# ============================================================
for d in DIRS:
    for b, recs in files[d].items():
        with open(f'{ROOT}/{d}/{b}', 'w') as fh:
            for r in recs:
                s = json.dumps(r, ensure_ascii=False)
                assert '—' not in s, r['id']
                fh.write(s + '\n')

stale_ids = [i for i, ch in log.items() if any(k in ' '.join(ch) for k in ['Replaced', 'Stale', 'stale', 'Removed reference', 'Added SRC-EU-AI-OMNIBUS', 'framework_refs', 'Question updated to the 2026', 'Scope note added: Nacha', 'NTIA minimum', 'Corrected citation'])]
print(dict(stats))
print('records touched', len(log), 'stale-corrected records', len(stale_ids))
print('dropped OWASP locators', dropped)
json.dump({'stats': stats, 'log': log, 'stale_ids': stale_ids}, open('/tmp/claude-0/-home-user/b7b453f6-b4f4-5ac1-8185-da750ab26d41/scratchpad/ref/run.json', 'w'), indent=1)
