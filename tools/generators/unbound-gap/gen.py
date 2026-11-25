"""Generate product-profiles/unbound/proposed-requirements.jsonl."""
import json

OUT = '/home/user/echelon-due-diligence/product-profiles/unbound/proposed-requirements.jsonl'

LOW = "Judgment, order of magnitude, not sourced: low (under one person-month of effort or under $10,000 external spend)."
MED = "Judgment, order of magnitude, not sourced: medium (one to six person-months or $10,000 to $50,000 external spend)."
HIGH = "Judgment, order of magnitude, not sourced: high (over six person-months or over $50,000 external spend)."
REC = lambda base, rec: f"{base} Recurring: {rec}."


def S(sid, loc=None, rel='informed-by', basis='reasonably-inferred'):
    d = {'source_id': sid, 'relation': rel, 'basis': basis}
    if loc:
        d['locator'] = loc
    return d


def B(loc):
    return S('SRC-ECH-UNB-BASELINE', loc, 'derived-from', 'directly-documented')


def C(ctrl):
    return S('SRC-ECH-DAF-TECH-AUDIT', ctrl, 'maps-to', 'directly-documented')


R = []


def req(id, title, statement, qs, srcs, refs, rationale, ac, vm, evr, pri, deps, cost, notes=None):
    r = dict(id=id, title=title, statement=statement, originating_questions=qs, source_refs=srcs,
             existing_requirement_refs=refs, rationale=rationale, acceptance_criteria=ac,
             verification_method=vm, evidence_requirements=evr, priority=pri, dependencies=deps,
             cost_impact=cost, status='proposed')
    if notes:
        r['notes'] = notes
    R.append(r)


# ---------------------------------------------------------------- GOV (baseline hygiene)
req('DD-UNB-GOV-001', 'Superseded and contradicted text register',
    'Unbound SHALL maintain a machine-readable register that marks every baseline record whose text is contradicted or narrowed by a convergence clause, including records the clause does not list in its amends field, and every customer-facing or assessor-facing citation SHALL resolve through that register to the governing text.',
    ['DDQ-AIA-0034', 'DDQ-ISP-0016', 'DDQ-AUD-0021'],
    [B('AUTHORITATIVE-BASELINE.md precedence; CNV-GOV-007; CNV-GOV-011'), S('SRC-AICPA-TSC', 'CC2.3')],
    ['CNV-GOV-007', 'CNV-GOV-011'],
    'Verified examples where unamended text contradicts a governing clause: UNB-RCN-WF-005 (donee model) versus CNV-GRT-013 (agent model); UNB-PLAT-003 (Folio for all documents) versus CNV-EXP-001 (Unbound-owned PDF pipeline); RR-UNB-PLAT-008-r1 (dedicated database default) versus CNV-ARC-001; ACC-MDL-011 and other Strata-runtime records versus CNV-ARC-004. In addition, 59 distinct amended records are cited in this repository without their governing clause. An assessor citing the old ID receives a wrong answer.',
    ['Every record in baseline.jsonl that a CNV clause contradicts carries a superseded_by or narrowed_by field naming the clause, verified by a script that diffs clause statements against flagged records.',
     'The five verified contradictions listed in the rationale are flagged.',
     'A validation check fails when an answer unit or customer document cites a flagged record without also citing its governing clause.'],
    'Automated register check in Unbound CI plus manual review of a sample of 30 clause-record pairs.',
    ['EVR-AIA-012', 'EVR-ISP-004'], 'P0', ['Unbound requirements owner time'], LOW)

req('DD-UNB-GOV-002', 'Resolve Strata runtime persistence assumptions',
    'All Unbound requirements and architecture documents that assume Strata provides runtime append-only persistence, ordering, cryptographic integrity or tenant isolation SHALL be rewritten to the CNV-ARC-004 split (Strata for declarative schema governance; an Unbound-owned ledger component for authoritative append-only history) before architecture acceptance.',
    ['DDQ-ARC-0025', 'DDQ-ACT-0009', 'DDQ-APP-0001'],
    [B('CNV-ARC-004; UNB-NAV-051; ACC-MDL-011; UNB-ACC-026'), S('SRC-ECH-SCS-0.1', 'SEC-DB-001', 'informed-by', 'directly-documented')],
    ['CNV-ARC-004', 'UNB-NAV-051', 'ACC-MDL-011', 'UNB-ACC-026', 'UNB-CHAR-040', 'UNB-CUST-013', 'UNB-INV-042', 'UNB-NAV-044', 'SOC2-025', 'GOV-AUTH-022', 'UNB-GAP-030'],
    'Verified: unbound@9b38de47:architecture/CONTINUOUS-CONTROL-MONITORING-AND-EVIDENCE-ASSURANCE.md line 35 states Strata is mandatory as a persistence dependency; CNV-ARC-004 assigns authoritative history to an Unbound-owned component; DD-ARC-002 found no Strata runtime typed query interface. Assessors reading the old text will expect a capability that does not exist.',
    ['Each listed requirement is either amended to the CNV-ARC-004 split or flagged in the DD-UNB-GOV-001 register.',
     'The continuous control monitoring architecture names the component that provides append-only history and integrity verification.',
     'A capability verification record cites the Strata release and the PostgreSQL major versions it supports.'],
    'Document review plus repository search showing no unflagged Strata runtime claims.',
    ['EVR-ARC-006', 'EVR-ASM-006'], 'P1', ['DD-UNB-GOV-001', 'Strata capability verification (DD-ARC-002)'], LOW)

req('DD-UNB-GOV-003', 'Extend the control matrix to infrastructure and security program controls',
    'The Unbound master enterprise control matrix SHALL add controls, owners and evidence definitions for network security, cloud configuration, endpoint security, encryption and key management, vulnerability management, penetration testing, personnel security and vendor management before the SOC 2 readiness assessment.',
    ['DDQ-AUD-0002', 'DDQ-ISP-0012', 'DDQ-ENC-0001', 'DDQ-VUL-0001'],
    [S('SRC-ECH-UNB-CONTROL-MATRIX', 'MASTER-ENTERPRISE-CONTROL-MATRIX.csv', 'derived-from', 'directly-documented'), S('SRC-AICPA-TSC', 'CC6, CC7, CC8, CC9'), S('SRC-CSA-CCM-V4', 'domains IVS, CEK, TVM')],
    ['SOC2-016', 'SOC2-014', 'SOC2-013', 'SOC2-010'],
    'The 90 UNB-CTRL controls are all status Designed with no operating evidence, and the batch 1 infrastructure review found no network, infrastructure, cloud, endpoint or encryption controls. SOC 2 common criteria cannot be met by product controls alone.',
    ['The matrix contains at least one control per listed domain with owner, frequency, evidence requirement ID and test procedure.',
     'Each new control maps to at least one Trust Services Criterion.',
     'Controls remain labeled Designed until operating evidence exists (SOC2-019).'],
    'Control matrix review against the Trust Services Criteria mapping by the readiness assessor.',
    ['EVR-FCT-005', 'EVR-ISP-004'], 'P1', ['DD-UNB-SEC-020'], LOW)

req('DD-UNB-GOV-004', 'Rename or annotate the UNB-RCN prefix',
    'Unbound SHALL annotate every UNB-RCN-* record as a requirement-reconciliation record, distinct from financial reconciliation, in assessor-facing indexes.',
    ['DDQ-RCN-0001'],
    [B('UNB-RCN-* prefix')], ['CNV-FIN-004'],
    'Verified: UNB-RCN-WF, UNB-RCN-GRT, UNB-RCN-FIN, UNB-RCN-ENT and UNB-RCN-PLT records come from requirement reconciliation work; financial reconciliation is governed by CNV-FIN-004. Assessors searching for reconciliation controls are misled by the prefix.',
    ['Assessor-facing indexes show a prefix legend distinguishing requirement reconciliation from financial reconciliation.',
     'No answer unit cites a UNB-RCN-* record as evidence of financial reconciliation unless the record concerns money.'],
    'Document review.', ['EVR-RCN-001'], 'P3', [], LOW)

# ---------------------------------------------------------------- LEG
req('DD-UNB-LEG-001', 'Counsel opinion on the regulatory perimeter',
    'Before the first sponsor activation, Echelon SHALL obtain and record a written counsel opinion on whether Unbound, as specified by CNV-LEG-001 and CNV-PAY-001, requires money transmitter licensing, investment adviser or broker-dealer registration, is a Nacha Third-Party Sender rather than a Third-Party Service Provider, or is a bank service provider, and SHALL block activation of any feature the opinion places outside the perimeter.',
    ['DDQ-REG-0005', 'DDQ-GOV-0035', 'DDQ-PAY-0001', 'DDQ-INV-0001', 'DDQ-GOV-0034'],
    [B('CNV-LEG-001; CNV-PAY-001; UNB-XIN-REG-002'), S('SRC-NACHA-RULES', 'Third-Party Sender and Third-Party Service Provider definitions'), S('SRC-BSCA'), S('SRC-CIRN-RULE-2021')],
    ['CNV-LEG-001', 'CNV-PAY-001', 'UNB-XIN-REG-001', 'UNB-XIN-REG-002'],
    'CNV-LEG-001 labels its UPMIFA delegation analysis an interpretation. CNV-LEG-001 says Unbound SHALL NOT be able to execute a payment, and defines execute so that relaying a sponsor-authorized instruction under the sponsor delegation is not execution; UNB-XIN-REG-001 and CNV-ARC-003 describe exactly such relay at an irreversible dispatch step. The internal text is therefore consistent, but whether a bank or regulator accepts that definition is a legal question: some ODFIs may treat a file-transmitting vendor as a Third-Party Sender. Every bank-affiliated sponsor will ask this first.',
    ['A dated opinion from licensed counsel addresses each listed regime and cites the funds-flow declaration.',
     'The OperatorStatusRegister (UNB-XIN-REG-002) records each conclusion with its basis.',
     'Activation of a program fails when the funds-flow conformance check finds a configuration outside the opinion.'],
    'Legal review record plus activation gate test.', ['EVR-INV-002', 'EVR-GOV-008', 'EVR-REG-002'], 'P0',
    ['Counsel engagement'], MED)

req('DD-UNB-LEG-002', 'Standard contract package',
    'Echelon SHALL publish, before the first sales conversation that reaches procurement, a standard contract package for Unbound consisting of a master services agreement, information security addendum, data processing agreement, service level schedule, exit and transition schedule and subprocessor terms, with a documented position on each common sponsor and bank requirement.',
    ['DDQ-LEG-0001', 'DDQ-LEG-0005', 'DDQ-LEG-0006', 'DDQ-LEG-0016', 'DDQ-PRV-0018'],
    [S('SRC-INTERAGENCY-TPRM-2023', 'contract negotiation'), S('SRC-Q-MS-DATA-PROCESSING-TERMS'), S('SRC-Q-TRUIST-TPISS')],
    ['CNV-GOV-001', 'CNV-ENT-002'],
    'No Unbound requirement specifies contract artifacts beyond right-to-audit (CNV-GOV-001) and exit custody (CNV-ENT-002). Large-bank sponsors will send their own addenda; a prepared position shortens negotiation and prevents commitments the product cannot meet.',
    ['Each listed document exists in draft reviewed by counsel.',
     'A position matrix states accept, modify or reject for each requirement in at least three public large-bank supplier standards.',
     'Every contractual commitment in the package maps to an Unbound requirement or a recorded owner decision.'],
    'Legal review and traceability check.', ['EVR-LEG-001', 'EVR-LEG-002'], 'P1', ['DD-UNB-LEG-001', 'DD-UNB-LEG-004'], MED)

req('DD-UNB-LEG-003', 'Insurance program before production data',
    'Before any production donor data is processed, Echelon SHALL bind cyber liability (first and third party), technology errors and omissions covering financial calculation and AI-assisted output errors, and commercial crime coverage including third-party and social engineering coverage, with limits set by an adequacy analysis tied to contractual liability caps.',
    ['DDQ-INS-0001', 'DDQ-INS-0006', 'DDQ-INS-0008', 'DDQ-INS-0009', 'DDQ-INS-0011'],
    [S('SRC-Q-ATBAY-CYBER-APP-2026'), S('SRC-Q-TMHCC-NETGUARD-APP-2026'), S('SRC-Q-INDIANA-CYBER-INSURANCE-TOOLKIT')],
    [],
    'The Unbound baseline contains no insurance requirement (zero matches). Sponsors and banks routinely require certificates of insurance; carriers treat application answers as representations, so controls must exist before binding.',
    ['Certificates of insurance exist for each coverage line with policy period and limits.',
     'An adequacy analysis relates limits to liability caps in the standard contract.',
     'Insurance application answers are reconciled to evidence before submission (EVR-INS-005).'],
    'Document inspection.', ['EVR-INS-001', 'EVR-INS-002', 'EVR-INS-004', 'EVR-INS-005'], 'P1',
    ['DD-UNB-LEG-004', 'DD-UNB-SEC-017'], REC(MED, 'premiums unknown; obtain quotes'))

req('DD-UNB-LEG-004', 'Contracting entity and IP title',
    'Before contracting, Echelon Foundry, LLC SHALL be formed and in good standing, SHALL hold or license all IP in Unbound and the Echelon components it uses by written assignment from every contributor, and SHALL be the entity that signs customer contracts, employs or engages personnel and holds hosting accounts.',
    ['DDQ-GOV-0001', 'DDQ-GOV-0004', 'DDQ-IPR-0001', 'DDQ-IPR-0002'],
    [S('SRC-ECH-BUSINESS-PLAN')], [],
    'Batch 1 found formation values all TODO in echelon-organization-administration@2763e576 and IP title unknown. No Unbound requirement covers it because it is organizational, yet every procurement process checks it first.',
    ['A certificate of existence dated within 90 days is available.',
     'IP assignment agreements cover every human contributor; AI-generated code ownership position is documented.',
     'The contracting entity, IP holder and hosting account owner are the same legal entity or the relationship is documented.'],
    'Document inspection.', ['EVR-GOV-001', 'EVR-GOV-002', 'EVR-IPR-001'], 'P0', ['Owner decision'], LOW)

req('DD-UNB-LEG-005', 'Platform-generated records are customer data',
    'The standard contract SHALL define customer data to include records the platform generates about the customer, its donors, funds, grants and decisions (audit trails, decision records, acknowledgments, reconciliations and evidence), and SHALL commit to export them in the exit package.',
    ['DDQ-PRT-0007', 'DDQ-PRT-0006', 'DDQ-IPR-0014'],
    [C('C12'), S('SRC-Q-GIVINGCOMPASS-REN-2026', None, 'informed-by', 'unknown')],
    ['CNV-ENT-002', 'RR-UNB-TEN-016-r1'],
    'CNV-ENT-002 makes the sponsor records custodian and requires a reconciled export, but no requirement states the contractual data definition. Batch 1 notes a competitor MSA returns only customer-provided materials; this is a differentiation point that must be contractual to count.',
    ['The MSA data definition lists each record class in the export manifest.',
     'The export manifest (CNV-ENT-002) covers every listed class.'],
    'Contract review against export manifest.', ['EVR-PRT-001', 'EVR-TRM-005'], 'P1', ['DD-UNB-LEG-002'], LOW)

req('DD-UNB-LEG-006', 'Incident notification commitments by customer type',
    'Unbound SHALL define incident notification commitments per customer type: initial notice to the sponsor within 24 hours of reasonable suspicion of an incident affecting its data or service, notice to bank customers as soon as possible for incidents meeting the bank service provider rule, and notice within 72 hours to customers subject to amended Regulation S-P, each with a named channel and authenticated sender.',
    ['DDQ-IR-0015', 'DDQ-IR-0021', 'DDQ-IR-0025', 'DDQ-LEG-0010', 'DDQ-LEG-0011', 'DDQ-LEG-0012', 'DDQ-PRV-0015'],
    [S('SRC-CIRN-RULE-2021', None, 'maps-to', 'directly-documented'), S('SRC-SEC-REG-SP-2024', None, 'maps-to', 'directly-documented'), S('SRC-STATE-BREACH-LAWS')],
    ['UNB-GAP-034', 'SOC2-015', 'CNV-PLT-007'],
    'No Unbound requirement sets a notification time. The 24-hour target is a research recommendation pending owner decision (batch 1); the bank and Regulation S-P timings derive from those rules and apply only through the customer.',
    ['The contract package states each timing and trigger.',
     'A tabletop exercise measures time from simulated detection to sponsor notice under 24 hours.',
     'Notices are sent from a channel the sponsor can verify independently of email.'],
    'Tabletop exercise plus contract review.', ['EVR-IR-004', 'EVR-IR-005', 'EVR-LEG-003'], 'P0', ['DD-UNB-SEC-016'], LOW)

req('DD-UNB-LEG-007', 'Echelon principal sanctions screening and ownership disclosure',
    'Echelon SHALL screen its owners, officers, personnel and contractors against OFAC lists at engagement and on list change, SHALL determine its own ownership for the OFAC 50 percent rule, and SHALL disclose beneficial owners to customers on request.',
    ['DDQ-REG-0016', 'DDQ-GOV-0011', 'DDQ-GOV-0007'],
    [S('SRC-OFAC-REGS', None, 'maps-to', 'directly-documented'), S('SRC-OFAC-COMPLIANCE-FRAMEWORK')],
    [],
    'OFAC binds Echelon directly as a US person (strict liability). The baseline screens donors, advisors and grantees (CNV-GRT-006) but not Echelon itself.',
    ['Screening records exist for every principal and contractor with list version and date.',
     'An ownership statement is approved by the governing body.'],
    'Record inspection.', ['EVR-GOV-007', 'EVR-REG-005'], 'P1', ['DD-UNB-LEG-004'], LOW)

req('DD-UNB-LEG-008', 'Article 4A security procedure allocation',
    'Each program role table SHALL record the commercially reasonable security procedure between the sponsor and its bank for every payment order Unbound prepares, the party that authenticates the instruction, and the contractual allocation of loss for unauthorized orders among sponsor, bank and Unbound.',
    ['DDQ-PAY-0017', 'DDQ-PAY-0019', 'DDQ-PAY-0032'],
    [S('SRC-UCC-4A', None, 'maps-to', 'directly-documented'), B('CNV-PAY-001 role table')],
    ['CNV-PAY-001', 'CNV-PLT-012'],
    'Batch 1 found the UCC 4A security procedure unaddressed. Because the sponsor originates and Unbound prepares, a sponsor will ask who bears loss for a fraudulent instruction transmitted through Unbound.',
    ['The role table schema contains security procedure, authenticating party and loss allocation fields.',
     'Rail activation (RailGoLive) fails when the fields are empty.'],
    'Configuration test plus contract review.', ['EVR-PAY-001', 'EVR-PAY-002'], 'P1', ['DD-UNB-LEG-001'], LOW)

req('DD-UNB-LEG-009', 'Vendor relationship and related-party disclosure',
    'Echelon SHALL maintain and disclose to each sponsor any board, committee, staff, fee-sharing, referral or financial relationship between Echelon, its owners or personnel and the sponsor, its advisors or its investment managers, and SHALL support the sponsor in identifying interested-person transactions.',
    ['DDQ-GOV-0029', 'DDQ-GOV-0032', 'DDQ-FEE-0028', 'DDQ-DAF-0038', 'DDQ-GOV-0031'],
    [S('SRC-IRC-4958'), S('SRC-IRS-FORM-990', 'Schedule L'), S('SRC-ECH-DAF-LANDSCAPE', 'board-vendor overlap findings')],
    ['CNV-GRT-009'],
    'CNV-GRT-009 controls payments from funds to related parties but no requirement covers Echelon itself as a related party. Batch 1 notes board-vendor overlap is documented in the DAF market.',
    ['A conflict-of-interest register exists and is attested annually by every principal.',
     'Each sponsor receives a disclosure statement before contract signature.'],
    'Register inspection.', ['EVR-GOV-005', 'EVR-FEE-008'], 'P2', ['DD-UNB-LEG-004'], LOW)

# ---------------------------------------------------------------- SEC
req('DD-UNB-SEC-001', 'Encryption at rest for every store',
    'All Unbound data stores, including databases, object storage, search indexes, queues, logs, backups and replicas, SHALL be encrypted at rest with AES-256 or stronger using keys managed under DD-UNB-SEC-003, and an automated check SHALL fail deployment of any unencrypted store.',
    ['DDQ-ENC-0001', 'DDQ-ENC-0002'],
    [S('SRC-FTC-SAFEGUARDS-RULE', '16 CFR 314.4(c)(3)'), S('SRC-NIST-SP800-53-R5', 'SC-28'), S('SRC-CSA-CCM-V4', 'CEK')],
    ['SOC2-014', 'UNB-TEN-006'],
    'The baseline mentions encryption only in passing (SOC2-014 "defined and enforced", UNB-TEN-006 for dedicated databases); no requirement states encryption at rest, algorithm or coverage. This is a near-universal critical questionnaire item.',
    ['An inventory of stores shows encryption status and key reference for 100 percent of stores.',
     'An infrastructure-as-code policy test rejects an unencrypted store.',
     'Backups and replicas are included in the inventory.'],
    'Policy-as-code test plus monthly coverage report.', ['EVR-ENC-001', 'EVR-BKP-004'], 'P0', ['DD-UNB-SEC-021', 'DD-UNB-SEC-003'], LOW)

req('DD-UNB-SEC-002', 'Encryption in transit',
    'All external connections SHALL use TLS 1.2 or later with TLS 1.3 preferred and legacy protocols disabled, and all internal connections between application, database, cache, queue and managed services SHALL use TLS with server certificate verification.',
    ['DDQ-ENC-0005', 'DDQ-ENC-0010', 'DDQ-ENC-0012', 'DDQ-ENC-0009'],
    [S('SRC-NIST-SP800-53-R5', 'SC-8'), S('SRC-OWASP-ASVS', 'V9')],
    ['UNB-CUST-017'],
    'No baseline record specifies transport encryption except "secure transport" for custodian integrations (UNB-CUST-017).',
    ['An external TLS scan shows no protocol below TLS 1.2.',
     'Database connections reject non-TLS clients (server-side enforcement).',
     'A code analyzer flags any disabled certificate validation.'],
    'External scan plus configuration test.', ['EVR-ENC-002', 'EVR-ENC-003'], 'P0', ['DD-UNB-SEC-021'], LOW)

req('DD-UNB-SEC-003', 'Key management decision and controls',
    'Unbound SHALL resolve ADR-006 by recording a key management design that names the key service, key hierarchy, per-tenant key scope, rotation periods, dual control for destruction, separation between key administrators and data administrators, and logging of every key operation.',
    ['DDQ-ENC-0013', 'DDQ-ENC-0014', 'DDQ-ENC-0016', 'DDQ-ENC-0023'],
    [S('SRC-NIST-SP800-53-R5', 'SC-12'), S('SRC-CSA-CCM-V4', 'CEK'), B('TENANT-AWARE-PERSISTENCE-DESIGN ADR-006')],
    ['UNB-TEN-008', 'UNB-DATA-007', 'RR-UNB-TEN-016-r1'],
    'Key management appears only as a list item in UNB-TEN-008; ADR-006 (unbound@9b38de47:architecture/TENANT-AWARE-PERSISTENCE-DESIGN.md line 157) is unresolved. Crypto-shredding for erasure and exit (UNB-DATA-007, RR-UNB-TEN-016-r1) depends on it.',
    ['ADR-006 is recorded with the listed elements.',
     'A key inventory export shows owner, scope and rotation date for every key.',
     'A test shows a single administrator cannot both read tenant data and destroy its key.'],
    'Architecture review plus key operation log inspection.', ['EVR-ENC-004', 'EVR-ENC-005', 'EVR-ENC-007'], 'P0',
    ['DD-UNB-SEC-021', 'DD-UNB-TEN-001'], MED)

req('DD-UNB-SEC-004', 'Field-level protection of financial identifiers',
    'Bank account numbers, routing-account pairs, taxpayer identification numbers and Social Security numbers SHALL be stored only in the PII vault, encrypted or tokenized at field level, masked by default in every interface and export, and SHALL never appear in immutable ledger events, logs or AI prompts.',
    ['DDQ-DCL-0010', 'DDQ-DCL-0011', 'DDQ-DCL-0013', 'DDQ-ENC-0030', 'DDQ-MON-0014'],
    [S('SRC-NACHA-DATA-SECURITY', None, 'maps-to', 'directly-documented'), S('SRC-FTC-SAFEGUARDS-RULE')],
    ['CNV-ARC-001', 'UNB-DATA-007', 'UNB-XIN-EVA-014'],
    'CNV-ARC-001 requires PII vault references in event payloads but no requirement names the fields, the protection method or masking. Batch 1 found no requirement to render stored ACH account numbers unreadable.',
    ['A static analysis of event schemas shows no field typed as a financial identifier outside the vault.',
     'A log and prompt scanner run on test traffic finds zero unmasked identifiers.',
     'Unmasking requires a recorded purpose and is logged.'],
    'Property-based tests plus scanner run per release.', ['EVR-ENC-009', 'EVR-DCL-003'], 'P0', ['DD-UNB-SEC-003'], MED)

req('DD-UNB-SEC-005', 'Secrets management and secret scanning',
    'Application secrets, credentials and certificates SHALL be held only in a managed secret store with access by workload identity, rotated on a defined schedule and on personnel change, and every repository, build log and container image SHALL be scanned for secrets on each change with a blocking gate.',
    ['DDQ-ENC-0026', 'DDQ-ENC-0027', 'DDQ-SCN-0010', 'DDQ-SCN-0013'],
    [S('SRC-GITLEAKS'), S('SRC-TRUFFLEHOG'), S('SRC-ECH-TUTELA-OWNERSHIP', 'secret scanning not run in portfolio CI', 'informed-by', 'directly-documented')],
    ['UNB-API-STD-005', 'UNB-CUST-017'],
    'Credential rotation appears only for integrations (UNB-API-STD-005). Tutela records that no portfolio repository runs secret scanning beyond its own self-scan.',
    ['No secret value is present in configuration files in the repository.',
     'The CI gate blocks a planted test secret.',
     'Rotation records exist for every secret within its period.'],
    'CI gate test plus rotation report.', ['EVR-ENC-008', 'EVR-SCN-004', 'EVR-IAM-008'], 'P0', ['DD-UNB-SEC-009'], LOW)

req('DD-UNB-SEC-006', 'Vulnerability management program with remediation targets',
    'Unbound SHALL operate a vulnerability management program covering application dependencies, the .NET runtime, container and operating system images and managed services, with remediation targets from discovery of 7 days for known-exploited vulnerabilities, 15 days for critical, 30 days for high and 90 days for medium, a time-limited exception process, and quarterly performance reporting.',
    ['DDQ-VUL-0001', 'DDQ-VUL-0009', 'DDQ-VUL-0013', 'DDQ-VUL-0014', 'DDQ-INF-0008'],
    [S('SRC-CISA-KEV'), S('SRC-CISA-BOD-26-04'), S('SRC-CVSS-4.0'), S('SRC-FIRST-EPSS')],
    ['SOC2-016'],
    'SOC2-016 requires recording findings but sets no scope, timing or exception rule; it is the only vulnerability requirement in the baseline. The numeric targets are research recommendations pending owner decision (batch 1).',
    ['A vulnerability register shows discovery date, severity, target and closure for each finding.',
     'A quarterly report shows percentage remediated within target.',
     'Every overdue finding has an approved, expiring exception.'],
    'Register inspection and SLA report.', ['EVR-VUL-001', 'EVR-VUL-002', 'EVR-VUL-003'], 'P0', ['DD-UNB-SEC-009', 'Owner decision on targets'], REC(LOW, 'about 0.1 FTE'))

req('DD-UNB-SEC-007', 'Vulnerability disclosure policy',
    'Echelon SHALL publish a vulnerability disclosure policy with safe harbor language reviewed by counsel, a monitored security contact and a security.txt file on every Unbound domain, and SHALL acknowledge external reports within three business days.',
    ['DDQ-VUL-0023'],
    [S('SRC-ISO-29147-30111'), S('SRC-CISA-SECURE-BY-DESIGN')],
    ['SOC2-016'],
    'Batch 1 found no VDP, SECURITY.md or security.txt in any Echelon repository and no requirement for one.',
    ['security.txt is reachable at the well-known path with a current expiry.',
     'A test report sent to the contact is acknowledged within three business days.'],
    'External check plus test submission.', ['EVR-VUL-004', 'EVR-VUL-005'], 'P2', [], LOW)

req('DD-UNB-SEC-008', 'Independent penetration testing before real donor data',
    'An independent firm SHALL perform an authenticated application, API and infrastructure penetration test of the production-equivalent environment before any pilot with real donor data and at least annually and after major architecture change, with scope including every role, cross-tenant access attempts, business logic abuse of grant and payment controls, embedded components and AI interfaces, and remediation retest.',
    ['DDQ-PEN-0001', 'DDQ-PEN-0003', 'DDQ-PEN-0006', 'DDQ-PEN-0007', 'DDQ-PEN-0011', 'DDQ-APP-0057', 'DDQ-TEN-0021', 'DDQ-AUZ-0035'],
    [S('SRC-NIST-SP800-115'), S('SRC-OWASP-WSTG'), S('SRC-PCI-PENTEST-GUIDANCE', None, 'informed-by', 'reasonably-inferred'), C('C09')],
    ['SOC2-016', 'TVR-SEC-007', 'TVR-SEC-010'],
    'SOC2-016 mentions penetration testing only as a program to record. No requirement sets timing, independence or scope, and the coverage screen classed PEN as having no Unbound requirement for 29 of 32 questions.',
    ['A letter of attestation names the firm, dates, scope and finding counts by severity.',
     'Scope documentation shows cross-tenant and business-logic test cases.',
     'All critical and high findings are retested and closed before the pilot.'],
    'Third-party report review.', ['EVR-PEN-001', 'EVR-PEN-002', 'EVR-PEN-003', 'EVR-PEN-004', 'EVR-PEN-005'], 'P0',
    ['DD-UNB-SEC-021', 'Running build'], REC(MED, 'annual test, order of $20,000 to $60,000 (judgment)'))

req('DD-UNB-SEC-009', 'Security scanning gates in the build',
    'Every Unbound build SHALL run dependency vulnerability and license scanning, secret scanning, infrastructure-as-code and container scanning and schema-driven API testing, and SHALL run F# rule analyzers for the Secure Construction Standard prohibitions in place of general SAST, with results normalized and blocking at agreed thresholds.',
    ['DDQ-SCN-0001', 'DDQ-SCN-0002', 'DDQ-SCN-0003', 'DDQ-SCN-0015', 'DDQ-SCN-0019', 'DDQ-SCN-0020'],
    [S('SRC-OSV'), S('SRC-SYFT-GRYPE'), S('SRC-SCHEMATHESIS'), S('SRC-FSHARP-ANALYZERS'), S('SRC-SAST-ACADEMIC-EVALS')],
    ['SOC2-016', 'CNV-GOV-009'],
    'Batch 1 verified that no mature SAST parses F#; language-independent tools apply. The baseline has one scanning reference (UNB-XIN-OTH-004). Assessors will ask what scans F# code; the honest answer requires compensating analyzers.',
    ['The pipeline definition contains each listed scanner with a blocking threshold.',
     'A coverage matrix states which weakness classes each tool covers and which are covered only by design constraints.',
     'A seeded vulnerable commit fails the gate.'],
    'Pipeline inspection and seeded-defect test.', ['EVR-SCN-001', 'EVR-SCN-002', 'EVR-SCN-003', 'EVR-SCN-005'], 'P1',
    ['Tutela rule registry ownership (DD-ARC-002)'], MED)

req('DD-UNB-SEC-010', 'Adopted secure development standard with enforced review',
    'Echelon SHALL formally adopt a secure development standard for Unbound mapped to NIST SSDF, and SHALL enforce branch protection so that no change, including one authored by an AI agent or an administrator, merges to a protected branch or deploys without review by at least one qualified human other than the author, with two non-author approvers for control-relevant modules per CNV-PLT-010.',
    ['DDQ-SDL-0001', 'DDQ-SDL-0003', 'DDQ-SDL-0011', 'DDQ-SDL-0012', 'DDQ-AIA-0037', 'DDQ-AIS-0037'],
    [S('SRC-NIST-SP800-218'), S('SRC-NIST-SP800-218A'), S('SRC-ECH-SCS-0.1', 'adoption status', 'informed-by', 'directly-documented')],
    ['CNV-PLT-010', 'REQ-X-006'],
    'The Secure Construction Standard v0.1 is proposed, not adopted, and has no AI rule. CNV-PLT-010 requires two approvers for control-relevant modules but no requirement covers other modules, AI-authored changes or administrator bypass. Branch protection on Echelon repositories is unknown.',
    ['A signed adoption record exists.',
     'Repository settings export shows required reviews, no administrator bypass and status checks on protected branches.',
     'A sample of 25 merged changes shows a non-author human reviewer on each.'],
    'Settings export plus sample review.', ['EVR-SDL-001', 'EVR-SDL-003', 'EVR-AIA-014'], 'P0', ['DD-UNB-SEC-024'], LOW)

req('DD-UNB-SEC-011', 'Release SBOM and signed provenance',
    'Each Unbound release SHALL produce an SBOM in SPDX or CycloneDX generated from resolved build dependencies including browser-delivered code, and signed build provenance, and deployment SHALL verify the signature before release to production.',
    ['DDQ-SCS-0011', 'DDQ-SCS-0012', 'DDQ-SCS-0023', 'DDQ-SCS-0028', 'DDQ-ASM-0005'],
    [S('SRC-CISA-SBOM-MIN'), S('SRC-SLSA'), S('SRC-SPDX'), S('SRC-CYCLONEDX')],
    ['CNV-PLT-010', 'CNV-GOV-009'],
    'CNV-PLT-010 requires signed builds and CNV-GOV-009 requires an SBOM license check, but no requirement states SBOM content, format or deployment verification. DD-ARC-002 found no Echelon release carries an SBOM; signing exists only in parts of Praxis and Strata.',
    ['Each release artifact has an SBOM and provenance attestation.',
     'An unsigned artifact is refused by the deployment step in a test.'],
    'Release inspection and negative deployment test.', ['EVR-SCS-003', 'EVR-SCS-005', 'EVR-SCS-006', 'EVR-ASM-002'], 'P1',
    ['Signing capability (DD-ARC-002 gap)'], LOW)

req('DD-UNB-SEC-012', 'Threat models as normative release gates',
    'Unbound SHALL maintain a threat model for every command class, external integration, webhook and embedded surface, reviewed at each material change, and a release SHALL be blocked when a changed component lacks a current threat model.',
    ['DDQ-SDL-0009', 'DDQ-APP-0036', 'DDQ-PEN-0009'],
    [S('SRC-OWASP-SAMM-2'), S('SRC-MITRE-CAPEC')],
    ['UNB-GAP-029', 'UNB-GRANT-044', 'REQ-X-006'],
    'UNB-GAP-029 calls for threat models but is classified research-hypothesis, so it is not binding.',
    ['A threat model record exists for each listed element with a review date after its last material change.',
     'The release gate fails a test change to an unmodeled component.'],
    'Gate test plus record review.', ['EVR-ARC-001', 'EVR-ARC-008'], 'P1', ['DD-UNB-SEC-010'], LOW)

req('DD-UNB-SEC-013', 'Application security verification baseline',
    'Unbound SHALL verify each release against OWASP ASVS Level 2, including prohibition of dynamic evaluation facilities reachable from user, partner or AI input, secure session and cookie configuration, CSRF protection, output encoding and file intake controls, and SHALL record the result per requirement.',
    ['DDQ-APP-0007', 'DDQ-APP-0011', 'DDQ-APP-0018', 'DDQ-AUN-0027'],
    [S('SRC-OWASP-ASVS', 'Level 2'), S('SRC-OWASP-TOP10')],
    ['CNV-PLT-010', 'UNB-EVT-003'],
    'The coverage screen found 39 of 60 APP questions with no Unbound requirement. The Secure Construction Standard rules SEC-UI and SEC-EXEC are proposed only.',
    ['An ASVS verification matrix exists per release with pass, fail or not-applicable and evidence per item.',
     'No Level 2 item is failing at release without an expiring exception.'],
    'Verification matrix review.', ['EVR-APP-013', 'EVR-APP-010', 'EVR-APP-005'], 'P1', ['DD-UNB-SEC-009'], MED)

req('DD-UNB-SEC-014', 'Security log retention and tamper evidence',
    'Unbound SHALL retain security and audit logs in a store separate from production with tamper-evident integrity verification for a retention period approved by counsel and the qualified auditor (proposed default: one year online, seven years archive for incident evidence), with legal hold support.',
    ['DDQ-MON-0007', 'DDQ-MON-0008', 'DDQ-MON-0009', 'DDQ-MON-0012'],
    [S('SRC-NIST-SP800-53-R5', 'AU-9, AU-11'), S('SRC-OMB-M-26-05', None, 'informed-by', 'unknown')],
    ['SOC2-023', 'CNV-PLT-009', 'CNV-PLT-004'],
    'SOC2-023 forbids inventing a universal retention period; no requirement sets one, so the answer to retention questions is currently unknown. CNV-PLT-009 sets service-organization evidence retention but not security logs.',
    ['A retention decision record exists signed by counsel and the auditor.',
     'An integrity verification job detects a deleted log record in a test.',
     'Production administrators cannot delete log records (negative test).'],
    'Configuration test plus integrity verification run.', ['EVR-MON-002', 'EVR-MON-003'], 'P1', ['DD-UNB-SEC-021'], LOW)

req('DD-UNB-SEC-015', 'Runtime security monitoring and detection',
    'Unbound SHALL operate runtime security monitoring with a detection catalog covering authentication abuse, cross-tenant probing, privileged access, configuration change, ledger integrity failure and anomalous payment preparation, with alert routing to a named responder and coverage outside business hours.',
    ['DDQ-MON-0001', 'DDQ-MON-0004', 'DDQ-MON-0006', 'DDQ-IR-0006'],
    [S('SRC-NIST-CSF-2.0', 'DE.CM'), S('SRC-MITRE-ATTACK')],
    ['MON-018', 'MON-013', 'SOC2-012'],
    'Specified monitoring (MON-*) covers control evidence, not runtime threat detection, and DD-ARC-002 found no runtime security monitoring in any Echelon system (Vigila is a task organizer, Aegis is fault handling). This is an unverified Echelon capability dependency.',
    ['A detection catalog lists each listed scenario with a test.',
     'Synthetic tests trigger each detection and an alert reaches the on-call responder.',
     'Missing-heartbeat alerts fire when a log source stops.'],
    'Detection tests run quarterly.', ['EVR-MON-004', 'EVR-MON-005', 'EVR-MON-007'], 'P1', ['Monitoring capability (absent per DD-ARC-002)', 'DD-UNB-SEC-021'], REC(MED, 'tooling and on-call coverage'))

req('DD-UNB-SEC-016', 'Approved incident response plan and exercises',
    'Echelon SHALL approve an incident response plan for Unbound naming the incident lead and backup, severity classes, customer and regulator notification steps, evidence preservation, breach counsel and forensic retainer, and SHALL exercise it at least annually with scenarios including ransomware, compromised AI agent and payment instruction tampering.',
    ['DDQ-IR-0001', 'DDQ-IR-0002', 'DDQ-IR-0012', 'DDQ-IR-0041'],
    [S('SRC-NIST-SP800-61-R3'), S('SRC-ISO-27001-2022', 'A.5.24 to A.5.28')],
    ['SOC2-015', 'UNB-GAP-034', 'UNB-OPS-001'],
    'Incident response appears only as list items (UNB-OPS-001, SOC2-015) and a research-hypothesis gap (UNB-GAP-034). No plan owner, retainer or breach counsel exists.',
    ['An approved plan exists with the listed elements.',
     'An exercise report with timeline and corrective actions exists within the last 12 months.'],
    'Document and exercise review.', ['EVR-IR-001', 'EVR-IR-002', 'EVR-IR-003', 'EVR-IR-008'], 'P0', ['DD-UNB-SEC-020'], REC(LOW, 'retainer fees unknown'))

req('DD-UNB-SEC-017', 'Workforce access lifecycle with revocation targets',
    'All workforce access, including cloud consoles, code hosting, secret stores, AI tool accounts and production databases, SHALL be provisioned through recorded requests, reviewed quarterly and revoked within 4 hours of involuntary and 24 hours of voluntary departure, with phishing-resistant authentication per CNV-PLT-003.',
    ['DDQ-HR-0016', 'DDQ-HR-0017', 'DDQ-HR-0020', 'DDQ-IAM-0002'],
    [S('SRC-NIST-SP800-53-R5', 'AC-2, PS-4'), S('SRC-FFIEC-AUTH-GUIDANCE-2021')],
    ['CNV-PLT-003', 'SOC2-010', 'AUTH-I6'],
    'CNV-PLT-003 governs authenticator strength; SOC2-010 lists deprovisioning but sets no time. The revocation targets are judgment and need owner approval.',
    ['A deprovisioning report shows time to revoke per departure against target.',
     'A quarterly recertification record exists for each system.'],
    'Report inspection.', ['EVR-IAM-001', 'EVR-IAM-002', 'EVR-IAM-003', 'EVR-AUN-004'], 'P1', ['DD-UNB-SEC-020'], LOW)

req('DD-UNB-SEC-018', 'Personnel security program',
    'Echelon SHALL perform FCRA-compliant background checks before granting access to customer data or production, require signed confidentiality and acceptable-use agreements, and deliver role-based security, fraud-awareness and secure development training at onboarding and annually, for employees and contractors.',
    ['DDQ-HR-0001', 'DDQ-HR-0003', 'DDQ-HR-0009', 'DDQ-ISP-0026', 'DDQ-ISP-0029', 'DDQ-FRD-0014'],
    [S('SRC-Q-FIDELITY-SUPPLIER-POLICIES', 'background investigations'), S('SRC-ISO-27001-2022', 'A.6.1 to A.6.3')],
    [],
    'The baseline has no personnel security requirement. Batch 1 found Fidelity supplier policies require deep background checks.',
    ['Screening, agreement and training completion records exist for every person with access.'],
    'Record inspection.', ['EVR-HR-001', 'EVR-HR-002', 'EVR-HR-003'], 'P1', ['DD-UNB-LEG-004'], REC(LOW, 'per-hire screening fees'))

req('DD-UNB-SEC-019', 'Workforce endpoint security',
    'Every device used to access Unbound production, code hosting or customer data SHALL be managed, encrypted, patched within defined periods and protected by endpoint detection and response, and unmanaged devices SHALL be denied by conditional access.',
    ['DDQ-END-0001', 'DDQ-END-0002', 'DDQ-END-0005', 'DDQ-END-0007', 'DDQ-END-0008'],
    [S('SRC-CIS-CONTROLS-V8.1', 'Controls 1, 4, 10'), S('SRC-Q-ATBAY-CYBER-APP-2026', 'EDR question')],
    [],
    'Workforce devices are unknown and no requirement covers them; cyber insurers and bank suppliers ask about EDR.',
    ['Device inventory reconciles to personnel.', 'A login attempt from an unmanaged device is denied in a test.'],
    'Conditional access test plus compliance report.', ['EVR-END-001', 'EVR-END-002', 'EVR-END-003', 'EVR-END-004'], 'P1', ['DD-UNB-SEC-020'], REC(LOW, 'per-device licensing'))

req('DD-UNB-SEC-020', 'Information security program charter and qualified individual',
    'Echelon SHALL adopt a written information security program covering Unbound, approved by its governing body, designate a qualified individual responsible for it with direct reporting to that body, maintain a policy register with owners and review dates, and report to the governing body at least annually.',
    ['DDQ-ISP-0001', 'DDQ-ISP-0005', 'DDQ-ISP-0007', 'DDQ-ISP-0012', 'DDQ-GOV-0025'],
    [S('SRC-FTC-SAFEGUARDS-RULE', '16 CFR 314.4(a), (i)'), S('SRC-INTERAGENCY-GLBA-SAFEGUARDS')],
    ['CNV-GOV-003'],
    'CNV-GOV-003 assumes a CISO with access to the audit committee, but no organizational requirement establishes the program. The only policy located is the proposed Secure Construction Standard v0.1.',
    ['A signed program charter and qualified individual designation exist.',
     'The policy register lists each policy with approval date.',
     'An annual report to the governing body exists.'],
    'Document inspection.', ['EVR-ISP-001', 'EVR-ISP-002', 'EVR-ISP-003', 'EVR-ISP-004'], 'P0', ['DD-UNB-LEG-004'], LOW)

req('DD-UNB-SEC-021', 'Hosting provider decision with shared responsibility',
    'Echelon SHALL record a hosting decision for Unbound naming the cloud provider, services, primary and recovery regions in the United States, the provider assurance reports reviewed with complementary user entity controls mapped, and a shared responsibility matrix, before architecture acceptance.',
    ['DDQ-CLD-0001', 'DDQ-CLD-0002', 'DDQ-CLD-0004', 'DDQ-CLD-0008', 'DDQ-CLD-0018', 'DDQ-INF-0001', 'DDQ-PHY-0001'],
    [S('SRC-ISO-27017'), S('SRC-CSA-CCM-V4'), C('C23')],
    ['CNV-ARC-001', 'UNB-TEN-008'],
    'CNV-ARC-001 assumes managed PostgreSQL but no provider is chosen; TENANT-AWARE-PERSISTENCE-DESIGN ADR-001 leaves the engine unchosen. Twenty infrastructure decisions are open (batch 1). Hosting questions are answered unknown today.',
    ['A decision record names provider, services and regions.',
     'A provider SOC report review memo maps provider CUECs to Unbound controls.',
     'A shared responsibility matrix covers every control in DD-UNB-GOV-003.'],
    'Document review.', ['EVR-CLD-001', 'EVR-CLD-002', 'EVR-CLD-003', 'EVR-CLD-006'], 'P0', ['Owner decision'], LOW)

req('DD-UNB-SEC-022', 'Cloud account guardrails and root credential custody',
    'Unbound cloud accounts SHALL separate production, non-production, logging and backup accounts, protect root credentials with hardware keys held under split custody, alert on every root use, and enforce preventive guardrails against public storage, disabled logging and unencrypted resources.',
    ['DDQ-CLD-0023', 'DDQ-CLD-0017', 'DDQ-BKP-0006'],
    [S('SRC-CIS-BENCHMARKS'), S('SRC-CSA-CCM-V4', 'IAM, LOG')],
    ['CNV-PLT-010', 'CNV-ARC-002'],
    'CNV-PLT-010 makes database administration break-glass with two-person activation but no requirement covers cloud account structure or root credentials; for a one-person organization split custody needs a named second holder.',
    ['An account inventory shows separation.', 'A root login test generates an alert.', 'Guardrail denial tests pass.'],
    'Guardrail and alert tests.', ['EVR-CLD-004', 'EVR-CLD-007', 'EVR-BKP-003'], 'P1', ['DD-UNB-SEC-021', 'DD-UNB-BCP-001'], LOW)

req('DD-UNB-SEC-023', 'Network exposure controls',
    'The database tier SHALL not be reachable from the internet or from any system other than the application tier and approved break-glass paths, outbound traffic SHALL be restricted to an allowlist, and public endpoints SHALL sit behind managed edge protection with rate limiting and DDoS mitigation.',
    ['DDQ-NET-0004', 'DDQ-NET-0017'],
    [S('SRC-NIST-SP800-207'), S('SRC-FFIEC-ARCHITECTURE-BOOKLET')],
    ['CNV-ARC-002'],
    'The coverage screen found NET questions answered mostly by unrelated requirements; no requirement specifies network segmentation or egress control.',
    ['An external attack surface scan shows no database endpoint.', 'An egress test to an unlisted host is denied.'],
    'External scan plus egress test.', ['EVR-NET-002', 'EVR-NET-003', 'EVR-NET-004', 'EVR-NET-005'], 'P1', ['DD-UNB-SEC-021'], LOW)

req('DD-UNB-SEC-024', 'Minimum independent personnel for control-relevant operations',
    'Before production, Echelon SHALL have at least two qualified people, neither able to act alone, for control-relevant code approval, production break-glass, key destruction and release signing, documenting any compensating control and its expiry while that condition is unmet.',
    ['DDQ-SDL-0012', 'DDQ-BCP-0017', 'DDQ-GOV-0019', 'DDQ-GOV-0022', 'DDQ-ISP-0008'],
    [B('CNV-PLT-010; CNV-GOV-003; TVR-ORG-003-Q'), S('SRC-COSO-2013', 'segregation of duties')],
    ['CNV-PLT-010', 'CNV-GOV-003', 'TVR-ORG-003-Q'],
    'CNV-PLT-010 requires two non-author approvers and two-person break-glass, and TVR-ORG-003-Q leaves small-scale compensation open. The answer units record that Echelon may have one human engineer (ANS-SDL-003). The product separation of duties design is unenforceable without people.',
    ['A roster shows at least two qualified holders per listed function.',
     'Any single-holder function has a documented, expiring compensating control approved by the governing body.'],
    'Roster and access configuration review.', ['EVR-HR-008', 'EVR-FCT-001', 'EVR-CHG-002'], 'P0', ['Hiring or contracting decision'], REC(HIGH, 'at least one additional qualified person'))

# ---------------------------------------------------------------- PRV
req('DD-UNB-PRV-001', 'Donor-facing privacy notice ownership in branded deployments',
    'Every donor-facing surface SHALL display the legal sponsor, the organization whose privacy notice governs the session and a link to that notice, and each program activation SHALL record which notice applies and who maintains it.',
    ['DDQ-WLB-0006', 'DDQ-PRV-0040', 'DDQ-PRV-0012'],
    [S('SRC-Q-AEF-PRIVACY-POLICY', 'third-party branded services disclaimer', 'derived-from', 'directly-documented'), S('SRC-GLBA-REG-P')],
    ['UNB-RCN-WF-009', 'REQ-X-030', 'UNB-TEN-008'],
    'UNB-RCN-WF-009 requires a legal-sponsor disclosure at activation, but no requirement addresses which privacy notice governs a white-labeled session. A documented sponsor policy disclaims coverage of third-party branded services (DD-IND-DAF-001).',
    ['Activation fails without a recorded governing notice.', 'A UI test confirms the notice link on every donor-facing page.'],
    'UI test plus activation gate test.', ['EVR-WLB-001', 'EVR-PRV-001'], 'P1', ['DD-UNB-LEG-002'], LOW)

req('DD-UNB-PRV-002', 'Processor role and data processing agreement',
    'Echelon SHALL act as processor or service provider for all sponsor personal data, SHALL publish a standard data processing agreement covering purpose limitation, subprocessor flow-down, assistance with rights requests, breach notice, deletion and audit, and SHALL list every purpose for which it uses customer data for its own benefit (expected: none beyond service delivery, security and billing).',
    ['DDQ-PRV-0007', 'DDQ-PRV-0008', 'DDQ-PRV-0018', 'DDQ-PRV-0011', 'DDQ-LEG-0022'],
    [S('SRC-CCPA-CPRA'), S('SRC-US-STATE-PRIVACY-LAWS'), S('SRC-GDPR', 'Art. 28', 'informed-by', 'reasonably-inferred')],
    ['UNB-TEN-008'],
    'UNB-TEN-008 lists data processing agreements as something to support per partner; no requirement fixes Echelon\'s role or terms. CCPA likely does not reach nonprofit sponsors but some state laws cover nonprofits, and for-profit partners need service-provider terms.',
    ['A standard DPA exists reviewed by counsel.', 'A data use register lists each Echelon purpose.'],
    'Legal and register review.', ['EVR-PRV-001', 'EVR-DON-006'], 'P1', ['DD-UNB-LEG-002'], LOW)

req('DD-UNB-PRV-003', 'Safeguards-equivalent program and GLBA applicability determination',
    'Echelon SHALL obtain a counsel determination of whether GLBA, the FTC Safeguards Rule or the Interagency Safeguards Guidelines apply to Echelon or reach it through customers, and regardless of the outcome SHALL commit contractually to safeguards equivalent to the FTC Safeguards Rule elements for donor and advisor data.',
    ['DDQ-PRV-0013', 'DDQ-PRV-0014', 'DDQ-PRV-0016', 'DDQ-LEG-0006'],
    [S('SRC-GLBA'), S('SRC-FTC-SAFEGUARDS-RULE', None, 'maps-to', 'reasonably-inferred'), S('SRC-INTERAGENCY-GLBA-SAFEGUARDS')],
    ['SOC2-014'],
    'Batch 1 records the GLBA status of DAF sponsors and of Echelon as the largest open legal question (OQ-DD-POL-001); no Unbound requirement addresses it.',
    ['A counsel memo states the determination.', 'An annual report against each Safeguards Rule element exists.'],
    'Legal review and annual report.', ['EVR-PRV-005', 'EVR-REG-001'], 'P1', ['DD-UNB-LEG-001', 'DD-UNB-SEC-020'], LOW)

req('DD-UNB-PRV-004', 'Rights requests against append-only records',
    'Unbound SHALL implement, after counsel review, a rights request workflow that verifies requester identity and authority, routes the decision to the sponsor as controller, and executes approved erasure by crypto-shredding vault entries while preserving records the law or the sponsor must retain, and SHALL state in customer materials what persists after erasure, including backups until expiry.',
    ['DDQ-PRV-0023', 'DDQ-PRV-0025', 'DDQ-PRV-0027'],
    [S('SRC-US-STATE-PRIVACY-LAWS'), S('SRC-NIST-SP800-88')],
    ['UNB-DATA-007', 'UNB-IMM-008', 'UNB-XIN-EVA-014', 'UNB-DATA-001', 'CNV-PLT-004'],
    'UNB-DATA-007 and UNB-IMM-008 state principles but defer the design; UNB-DATA-001 forbids deletion of authoritative events. Regulators may treat retained ciphertext as personal data (batch 1). Counsel resolution is required before production.',
    ['A counsel memo approves the erasure method per record class.',
     'A test erases a donor and verifies the vault entry is unrecoverable while ledger integrity verification still passes.',
     'Customer materials list what persists.'],
    'Integration test plus legal review.', ['EVR-DON-006', 'EVR-RET-005', 'EVR-RET-007', 'EVR-PRV-007'], 'P1', ['DD-UNB-SEC-003'], MED)

req('DD-UNB-PRV-005', 'No sale, sharing or third-party tracking',
    'Unbound SHALL NOT sell or share personal data or use it for targeted advertising, SHALL NOT load third-party analytics, advertising, social or session replay scripts on authenticated pages, and SHALL enforce this with a content security policy and a build-time script inventory check, including on sponsor-branded pages.',
    ['DDQ-PRV-0029', 'DDQ-PRV-0043', 'DDQ-PRV-0044', 'DDQ-PRV-0032'],
    [S('SRC-CCPA-CPRA'), S('SRC-OWASP-CHEATSHEETS', 'Content Security Policy')],
    ['UNB-XIN-CRM-003'],
    'No requirement prohibits tracking tags; answer units record the open question whether white-label sponsors will demand their own analytics tags (ANS-PRV-009).',
    ['The script inventory check fails a build that adds an unlisted third-party script.', 'The CSP blocks third-party script origins on authenticated pages in a browser test.'],
    'Build check plus browser test.', ['EVR-PRV-010', 'EVR-APP-003'], 'P1', [], LOW)

req('DD-UNB-PRV-006', 'United States data location and access origin',
    'Customer data, backups, logs, AI inference and support access SHALL remain in and originate from the United States unless a sponsor contract approves otherwise, and every access SHALL record its origin.',
    ['DDQ-PRV-0034', 'DDQ-PRV-0037', 'DDQ-CLD-0020', 'DDQ-SUB-0015', 'DDQ-LEG-0023'],
    [S('SRC-Q-TRUIST-TPISS', 'US-only remote access'), S('SRC-Q-MS-MIN-SECURITY-STANDARDS')],
    ['UNB-TEN-008'],
    'UNB-TEN-008 lists residency as something to support; no default exists. Large-bank supplier standards require US-only access (batch 1).',
    ['A data location inventory shows US regions for every store and subprocessor.', 'Access logs carry origin.'],
    'Inventory plus log inspection.', ['EVR-PRV-008', 'EVR-SUB-005', 'EVR-CLD-006'], 'P1', ['DD-UNB-SEC-021', 'DD-UNB-AIA-001'], LOW)

req('DD-UNB-PRV-007', 'Privacy impact assessment gate',
    'A privacy impact assessment SHALL be completed and approved before any feature introduces a new personal data category, purpose, recipient, AI processing of personal data or cross-sponsor aggregation, and the release gate SHALL check for it.',
    ['DDQ-PRV-0039', 'DDQ-PRV-0041', 'DDQ-PRV-0030'],
    [S('SRC-NIST-PRIVACY-FW'), S('SRC-ISO-27701')],
    ['SOC2-014', 'CNV-TEN-001'],
    'No PIA requirement exists. Answer units leave open whether cross-sponsor analytics will be pursued (ANS-PRV-006, ANS-PRV-012).',
    ['A PIA register exists.', 'The release gate blocks a test change tagged as new data category without a PIA.'],
    'Gate test.', ['EVR-PRV-009'], 'P2', ['DD-UNB-SEC-010'], LOW)

req('DD-UNB-PRV-008', 'Privacy program owner',
    'Echelon SHALL designate a privacy officer accountable for the Unbound privacy program, the record of processing and rights request handling.',
    ['DDQ-PRV-0001', 'DDQ-PRV-0002'],
    [S('SRC-NIST-PRIVACY-FW', 'GV')], [],
    'ANS-PRV-001 records the role as unassigned.',
    ['A designation record exists.', 'A generated record of processing is reviewed by the officer quarterly.'],
    'Document inspection.', ['EVR-PRV-001', 'EVR-PRV-002'], 'P2', ['DD-UNB-SEC-020'], LOW)

# ---------------------------------------------------------------- AIA
req('DD-UNB-AIA-001', 'AI provider inventory and data terms',
    'Echelon SHALL maintain an inventory of every AI model provider and AI tool used to build, operate or deliver Unbound, and SHALL use for any customer data only provider tiers with contractual no-training commitments, zero or bounded retention, United States processing and listing as a subprocessor.',
    ['DDQ-AIG-0001', 'DDQ-AIG-0002', 'DDQ-AIG-0021', 'DDQ-AIG-0026', 'DDQ-AIG-0027', 'DDQ-IPR-0016', 'DDQ-RSK-0021', 'DDQ-SUB-0018'],
    [S('SRC-Q-FSISAC-GENAI-VENDOR-GUIDE'), S('SRC-NIST-AI-600-1'), S('SRC-Q-MS-MIN-SECURITY-STANDARDS', 'GenAI use disclosure')],
    ['UNB-XIN-SAS-009', 'CNV-AIO-001'],
    'No requirement inventories AI providers or their terms; UNB-XIN-SAS-009 only meters model calls. Answer units for training and retention are unknown, and Echelon builds largely with AI coding agents.',
    ['An inventory lists provider, model, tier, terms reference, retention, region and data classes.',
     'A tool broker or egress control denies calls to unlisted AI endpoints in a test.'],
    'Inventory review plus egress test.', ['EVR-AIG-001', 'EVR-AIG-007', 'EVR-AIG-008', 'EVR-SUB-006'], 'P0', [], LOW)

req('DD-UNB-AIA-002', 'No training on customer data',
    'Echelon SHALL NOT use sponsor, donor, advisor or grantee data to train, fine-tune or evaluate models, prompts or agents without the sponsor\'s written opt-in per use, and SHALL state this in the contract.',
    ['DDQ-IPR-0015', 'DDQ-AIG-0029', 'DDQ-PRV-0050'],
    [S('SRC-ECH-BUSINESS-PLAN', 'section 10.04', 'informed-by', 'directly-documented'), S('SRC-Q-FSISAC-GENAI-VENDOR-GUIDE')],
    ['CNV-AIO-001'],
    'Business plan 10.04 is boilerplate and states no position (batch 1); no Unbound requirement exists.',
    ['The contract package contains the commitment.', 'Evaluation datasets are synthetic or opt-in, verified by dataset register.'],
    'Contract and dataset register review.', ['EVR-AIG-011', 'EVR-AIG-008'], 'P0', ['DD-UNB-LEG-002'], LOW)

req('DD-UNB-AIA-003', 'AI coding agent permissions and production isolation',
    'AI coding and operations agents SHALL run under their own identities with least privilege, SHALL NOT push to protected branches, approve changes, modify CI or security gate configuration, or access production data or secrets, and every agent action SHALL be attributable to an execution and accountable human.',
    ['DDQ-AIA-0037', 'DDQ-AIS-0012', 'DDQ-AIS-0039', 'DDQ-END-0017', 'DDQ-HR-0023', 'DDQ-PRV-0051', 'DDQ-SDL-0028'],
    [S('SRC-OWASP-AGENTIC-AI'), S('SRC-NIST-SP800-218A')],
    ['CNV-AIO-001', 'CNV-PLT-010', 'CNV-ARC-002'],
    'CNV-AIO-001 governs AI in the product, not engineering agents. Answer units on agent branch permissions and review are unknown (ANS-AIS-008); Praxis attribution exists but identity is asserted, not cryptographically verified.',
    ['An agent permission manifest exists per agent.', 'Negative tests show an agent token cannot merge, edit protected CI paths or read production.'],
    'Permission tests plus manifest review.', ['EVR-AIA-014', 'EVR-AIA-015', 'EVR-SDL-006', 'EVR-END-005'], 'P0', ['DD-UNB-SEC-010'], LOW)

req('DD-UNB-AIA-004', 'AI security testing before enabling AI features',
    'Before any AI feature is enabled for a sponsor, Unbound SHALL pass a versioned adversarial suite covering direct and indirect prompt injection, cross-tenant retrieval, tool misuse, parameter tampering and unsafe output handling, and SHALL repeat it on every model, prompt or tool change.',
    ['DDQ-AIS-0001', 'DDQ-AIS-0002', 'DDQ-AIS-0003', 'DDQ-AIS-0008', 'DDQ-AIS-0016', 'DDQ-AIS-0020'],
    [S('SRC-OWASP-LLM-TOP10-2026'), S('SRC-MITRE-ATLAS'), S('SRC-GARAK'), S('SRC-PYRIT')],
    ['CNV-AIO-001', 'CNV-AIO-002', 'UNB-AIO-003', 'AIN-012', 'REQ-X-054'],
    'CNV-AIO-002 and UNB-AIO-003 state design boundaries; AIN-012 and UNB-GAP-033 are proposed or hypothesis. No test obligation or release gate exists.',
    ['Suite results per release show zero unauthorized tool executions and zero cross-tenant disclosures.', 'The release gate blocks an AI change without a current suite run.'],
    'Automated suite in CI.', ['EVR-AIS-001', 'EVR-AIS-004', 'EVR-AIS-011'], 'P1', ['DD-UNB-SEC-012'], MED)

req('DD-UNB-AIA-005', 'Model change and provider deprecation control',
    'Unbound SHALL pin model versions, receive or monitor provider deprecation notices, re-run evaluation and adversarial suites before any model change, notify sponsors of material model or provider changes in advance, and keep deterministic paths operable without AI.',
    ['DDQ-AIG-0024', 'DDQ-AIG-0038', 'DDQ-BCP-0024'],
    [S('SRC-NIST-AI-RMF'), S('SRC-SR-26-2', None, 'informed-by', 'reasonably-inferred')],
    ['CNV-AIO-001'],
    'CNV-AIO-001 requires AI unavailability not to stop deterministic paths; no requirement covers model version change.',
    ['Model identifiers are pinned in configuration.', 'A change record shows suite results and sponsor notice before a model switch.'],
    'Change record review.', ['EVR-AIG-010', 'EVR-BCP-007'], 'P2', ['DD-UNB-AIA-004'], LOW)

req('DD-UNB-AIA-006', 'Automated decision applicability determination',
    'Echelon SHALL determine, with counsel, whether any Unbound AI or rules feature is a consequential or automated decision under applicable state law (including Colorado SB 26-189) and whether sponsors need notice or appeal mechanisms, and SHALL record the result per feature.',
    ['DDQ-AIG-0018', 'DDQ-AIG-0039'],
    [S('SRC-COLORADO-SB26-189', None, 'maps-to', 'reasonably-inferred'), S('SRC-US-STATE-AI-LAWS')],
    ['CNV-AIO-001', 'CNV-GRT-012'],
    'Batch 1 records the Colorado AI Act repealed and reenacted as an automated decision-making technology law with duties from 2027-01-01; CNV-GRT-012 provides decline reasons but no applicability analysis exists.',
    ['A determination record exists for each AI or rules feature affecting individuals.'],
    'Legal review.', ['EVR-AIG-009', 'EVR-AIG-005'], 'P2', ['DD-UNB-LEG-001'], LOW)

# ---------------------------------------------------------------- TEN
req('DD-UNB-TEN-001', 'Single isolation default and dependent clause reconciliation',
    'Unbound SHALL record one architecture decision stating the default tenant isolation profile and the conditions for dedicated databases, and SHALL amend CNV-TEN-001, CNV-ARC-003 and RR-UNB-PLAT-008-r1 so that no clause depends on an unaccepted database-per-sponsor decision.',
    ['DDQ-ARC-0024', 'DDQ-TEN-0001', 'DDQ-WLB-0020'],
    [B('CNV-ARC-001; CNV-TEN-001; CNV-ARC-003; RR-UNB-PLAT-008-r1')],
    ['CNV-ARC-001', 'CNV-TEN-001', 'CNV-ARC-003', 'CNV-ARC-002', 'RR-UNB-PLAT-008-r1', 'UNB-PLAT-008'],
    'Verified contradiction: CNV-ARC-001 sets one shared cluster with schema and role per sponsor, RR-UNB-PLAT-008-r1 (adopted-provisional, not amended) sets dedicated database per tenant as the default, and CNV-TEN-001 and CNV-ARC-003 each still state that they depend on acceptance of the database-per-sponsor architecture decision, although both also describe the shared-cluster case. Tenant isolation is the first architecture question every assessor asks.',
    ['One decision record names the default profile.', 'CNV-TEN-001 and CNV-ARC-003 no longer state a dependency on an unaccepted decision.', 'RR-UNB-PLAT-008-r1 is flagged in the DD-UNB-GOV-001 register.'],
    'Document review.', ['EVR-TEN-001', 'EVR-ARC-008'], 'P0', ['DD-UNB-GOV-001'], LOW)

req('DD-UNB-TEN-002', 'Independent verification of tenant isolation',
    'The tenant isolation suite (negative tests across database, cache, search, queue, AI retrieval, exports and embedded widgets) SHALL run on every release and be included in the independent penetration test scope, with continuous cross-tenant canary probes in production.',
    ['DDQ-TEN-0021', 'DDQ-TEN-0025', 'DDQ-PRT-0009', 'DDQ-API-0002'],
    [S('SRC-OWASP-API-TOP10-2023', 'API1'), C('C08')],
    ['CNV-ARC-001', 'CNV-ARC-002', 'ACC-MDL-005', 'UNB-RCN-WF-009'],
    'Negative isolation tests are required at activation (UNB-RCN-WF-009) and in CNV-ARC-001, but no requirement covers continuous production canaries or independent testing.',
    ['Suite results per release show zero cross-tenant reads.', 'Canary telemetry shows probe executions daily with zero leaks.'],
    'CI suite plus canary telemetry.', ['EVR-TEN-006', 'EVR-TEN-007', 'EVR-AIS-004'], 'P1', ['DD-UNB-SEC-008', 'DD-UNB-TEN-001'], LOW)

# ---------------------------------------------------------------- WLB (white labeling and embedded)
req('DD-UNB-WLB-001', 'Custom domains and certificate management',
    'Unbound SHALL support sponsor and partner custom domains with automated certificate issuance and renewal, domain ownership verification, HSTS, certificate expiry monitoring and removal on partner exit.',
    ['DDQ-WLB-0001', 'DDQ-ENC-0007', 'DDQ-ASM-0017'],
    [S('SRC-OWASP-CHEATSHEETS', 'Transport Layer Security')],
    ['REQ-X-030'],
    'ANS-WLB-001 records that custom domain and TLS certificate management for white-label portals is not specified.',
    ['A domain cannot be bound without verification.', 'Certificates renew automatically in a test with a short-lived certificate.', 'Exit removes the domain binding.'],
    'Integration test.', ['EVR-WLB-001', 'EVR-NET-007'], 'P2', ['DD-UNB-SEC-021'], LOW)

req('DD-UNB-WLB-002', 'Embedded component security contract',
    'Unbound SHALL decide the embedding mechanism (ADR-M-03) and specify for every embedded component: per-partner frame-ancestors allowlist, single-use launch tokens with a lifetime of at most 60 seconds bound to origin and user, independent authentication and authorization by Unbound, validated message schemas for host communication, overlay-resistant confirmation for consequential actions and session behavior under third-party cookie restrictions.',
    ['DDQ-WLB-0011', 'DDQ-WLB-0012', 'DDQ-WLB-0013', 'DDQ-WLB-0014', 'DDQ-WLB-0015', 'DDQ-WLB-0018'],
    [S('SRC-OWASP-CHEATSHEETS', 'Clickjacking Defense'), C('C08')],
    ['INT-015', 'AIN-029', 'MON-022', 'AUTH-I1', 'TVR-WID-001'],
    'INT-015 and AIN-029 are one-line Proposed table rows; Limen lacks element or shadow-root roots so ADR-M-03 is unresolved and the interim iframe or web-component approach sits uneasily with SEC-UI-002 (batch 1, verified in 07-ECHELON-CAPABILITY-ASSESSMENT.md line 148). The 60-second value is judgment.',
    ['ADR-M-03 is recorded.', 'Adversarial tests show framing from an unlisted origin fails, a replayed token fails and a host-asserted identity is not trusted.'],
    'Adversarial embedded component test suite.', ['EVR-WLB-003', 'EVR-WLB-004'], 'P1', ['Limen embeddable root (LIMEN-GAP-01)'], MED)

req('DD-UNB-WLB-003', 'Brand attribution rule for white-label surfaces',
    'Unbound SHALL state where Unbound and Echelon attribution appears on sponsor-branded surfaces, reconciling UNB-EXP-002 with the Brand Kit model so that the legal sponsor is always identified and vendor attribution never implies vendor control of funds.',
    ['DDQ-WLB-0006', 'DDQ-WLB-0007'],
    [S('SRC-STATE-CHARITABLE-SOLICITATION', None, 'informed-by', 'reasonably-inferred')],
    ['UNB-EXP-002', 'REQ-X-030', 'CNV-EXP-001'],
    'UNB-EXP-002 requires independent Unbound branding with Echelon attribution while REQ-X-030 and CNV-EXP-001 describe sponsor Brand Kits and an Echelon default theme; the attribution rule for white-label surfaces is not stated.',
    ['A rule exists and Brand Kit validation enforces it.'],
    'Brand Kit validation test.', ['EVR-WLB-001'], 'P3', [], LOW)

# ---------------------------------------------------------------- API
req('DD-UNB-API-001', 'Partner API authentication standard',
    'Partner and integration API access SHALL use OAuth 2.0 client credentials with private-key JWT or mutual TLS and sender-constrained tokens; static API keys SHALL NOT authorize money-affecting, authority-affecting or bulk export operations, and sponsors SHALL see and revoke every credential for their tenant.',
    ['DDQ-API-0008', 'DDQ-API-0009', 'DDQ-API-0010', 'DDQ-WLB-0030'],
    [S('SRC-OWASP-API-TOP10-2023', 'API2'), S('SRC-FFIEC-AUTH-GUIDANCE-2021')],
    ['UNB-API-STD-005', 'CNV-PLT-003', 'UNB-XIN-IAM-003'],
    'No baseline record names an API authentication method (zero matches for OAuth or mTLS); UNB-API-STD-005 requires only documentation. An answer unit notes integrations may only support static keys.',
    ['The API gateway rejects a static key on a money-affecting route in a test.', 'A sponsor credential list shows every client for its tenant.'],
    'API negative tests.', ['EVR-API-002', 'EVR-AUN-009'], 'P1', [], MED)

req('DD-UNB-API-002', 'Developer documentation, changelog and sandbox',
    'Unbound SHALL publish versioned API documentation with schemas, a security changelog, an isolated sandbox that cannot send real payments, and the deprecation lifecycle required by CNV-EXP-001.',
    ['DDQ-API-0019', 'DDQ-API-0020', 'DDQ-PAY-0034', 'DDQ-PEN-0026'],
    [C('C22'), C('C06')],
    ['CNV-EXP-001', 'CNV-AIO-001', 'UNB-API-STD-003'],
    'CNV-EXP-001 sets an 18-month breaking-change notice and CNV-AIO-001 requires machine-readable assistance, but no requirement establishes a sandbox or public changelog. The sponsor audit matrix (C06, C22) asks for repeatable sandbox evidence.',
    ['Documentation and changelog are published per version.', 'A sandbox payment attempt is refused by rail configuration.'],
    'Documentation review plus sandbox test.', ['EVR-API-004', 'EVR-PAY-002'], 'P2', [], MED)

req('DD-UNB-API-003', 'Per-tenant rate and business-flow limits in release 1',
    'Rate limits per client, user and tenant, and business-flow limits on recommendation, contribution form and export endpoints, SHALL be in release 1 rather than deferred, and SHALL be returned in response metadata.',
    ['DDQ-API-0014', 'DDQ-API-0016', 'DDQ-CON-0044'],
    [S('SRC-OWASP-API-TOP10-2023', 'API4, API6')],
    ['UNB-API-STD-003', 'RR-UNB-API-STD-003-r1', 'RR-UNB-API-STD-003-r2'],
    'RR-UNB-API-STD-003-r1 (rate limits per tier and tenant) is unvalidated and deferred; r2 is proposed. Public contribution forms need abuse controls regardless of card deferral.',
    ['Load tests show throttling per tenant without affecting other tenants.'],
    'Load test.', ['EVR-API-003'], 'P2', [], LOW)

# ---------------------------------------------------------------- FIN
req('DD-UNB-FIN-001', 'Scheduled and recurring contributions model',
    'Unbound SHALL either define scheduled and recurring contributions (mandate record, cadence, amount, funding source, authorization evidence under Nacha and Regulation E where applicable, revocation, failure handling and expected-versus-received reconciliation) or record their exclusion from release 1 in customer materials.',
    ['DDQ-CON-0001', 'DDQ-CON-0005', 'DDQ-FRD-0025'],
    [S('SRC-NACHA-RULES', 'recurring entries', 'informed-by', 'reasonably-inferred'), B('CNV-FIN-003; CNV-PAY-005')],
    ['CNV-FIN-003', 'CNV-PAY-005', 'UNB-RCN-WF-001'],
    'The baseline has no requirement for scheduled or recurring contributions (zero matches), and the question bank has no dedicated question; CNV-FIN-003 states release 1 has no donor ACH debit origination. Sponsors offering automatic giving will ask.',
    ['Either a mandate lifecycle specification with acceptance tests exists, or customer materials state the exclusion.',
     'If implemented, a revoked mandate produces no further expected contributions in a test.'],
    'Specification review or customer material review.', ['EVR-CON-001', 'EVR-PAY-003'], 'P2', [], MED)

req('DD-UNB-FIN-002', 'Reconciliation sampling method and break reporting',
    'Unbound SHALL specify the error-bound sampling method used for attestation of auto-passed reconciliation items, default break aging thresholds and escalation, and a sponsor-facing break report with frequency and content.',
    ['DDQ-RCN-0009', 'DDQ-RCN-0014', 'DDQ-RCN-0011', 'DDQ-RCN-0004'],
    [S('SRC-AICPA-SSAE-18', None, 'informed-by', 'reasonably-inferred'), C('C03')],
    ['CNV-FIN-004', 'CNV-FIN-011'],
    'CNV-FIN-004 leaves sample size to the controller and labels numeric values illustrative; ANS-RCN-003 and ANS-RCN-005 record that break reporting and the sampling method are unspecified.',
    ['A documented method computes sample size from an error bound and confidence level.',
     'A sponsor break report sample shows aging, attribution and owner.'],
    'Method review plus report sample.', ['EVR-RCN-004', 'EVR-RCN-007', 'EVR-RCN-003'], 'P1', [], LOW)

req('DD-UNB-FIN-003', 'Advance notice of fee changes',
    'A fee schedule version that increases any charge to a fund or donor SHALL NOT take effect until a sponsor-set notice period (default 30 days) has elapsed after notice to affected donors and the sponsor, and the notice SHALL be recorded.',
    ['DDQ-FEE-0013', 'DDQ-FCT-0012', 'DDQ-FEE-0012'],
    [S('SRC-ECH-DAF-LANDSCAPE', None, 'informed-by', 'reasonably-inferred'), C('C21')],
    ['CNV-FIN-002', 'UNB-SMP-ECN-001'],
    'ANS-FEE-003 records no requirement for advance notice of fee increases. CNV-FIN-002 versions schedules but has no notice rule. The 30-day default is judgment.',
    ['Activation of a higher fee version before the notice period fails in a test.', 'Notice delivery records exist for each affected donor.'],
    'Configuration test.', ['EVR-FEE-004', 'EVR-FEE-001'], 'P2', [], LOW)

req('DD-UNB-FIN-004', 'Information return applicability',
    'Unbound SHALL determine, with counsel, which payments it prepares may require Form 1099 information returns (for example payments to non-charity payees, refunds or vendor fees netted from proceeds), collect taxpayer identification where required, and export the data for the sponsor\'s filing.',
    ['DDQ-RRP-0017', 'DDQ-RRP-0018', 'DDQ-RRP-0019', 'DDQ-RRP-0020'],
    [S('SRC-IRS-FORM-990', None, 'informed-by', 'unknown')],
    ['UNB-ACC-021'],
    'No requirement mentions Form 1099 (zero matches). The relevant IRS instructions are not yet in the source register (batch 1 unseeded list).',
    ['A determination record exists per payment type.', 'An export produces payee, TIN status and amount for flagged payments.'],
    'Legal review plus export test.', ['EVR-RRP-004'], 'P2', ['DD-UNB-LEG-001'], LOW,
    'Source gap: IRS General Instructions for Certain Information Returns should be added to sources before acceptance.')

req('DD-UNB-FIN-005', 'Ledger integrity anchoring mechanism',
    'Unbound SHALL select and benchmark the ledger integrity mechanism required by UNB-DATA-012 and CNV-PLT-010 (hash chain with signed checkpoints anchored daily outside Echelon-controlled infrastructure) and SHALL provide a sponsor-runnable verifier.',
    ['DDQ-ACT-0009', 'DDQ-ARC-0025', 'DDQ-MON-0011', 'DDQ-BKP-0013'],
    [C('C07'), S('SRC-NIST-SP800-53-R5', 'AU-9(3), SI-7')],
    ['UNB-DATA-012', 'CNV-PLT-010', 'ACC-MDL-002', 'UNB-DATA-001'],
    'CNV-PLT-010 requires daily external anchoring and UNB-DATA-012 leaves the mechanism undecided. ANS-ENC-012 records the anchor location as open. Evidence signing exists only partially in Echelon (DD-ARC-002).',
    ['A decision record names the mechanism and anchor location.', 'The verifier detects a deleted, altered, duplicated and reordered record in tests, including after restore.'],
    'Verifier tests.', ['EVR-ACT-003', 'EVR-ENC-013', 'EVR-BKP-005'], 'P1', ['Signing capability (DD-ARC-002 gap)', 'DD-UNB-SEC-003'], MED)

req('DD-UNB-FIN-006', 'Complementary user entity controls published per sponsor',
    'Before a sponsor relies on Unbound for financial reporting, Unbound SHALL publish to that sponsor a list of complementary user entity controls derived from its configuration and SHALL keep the list current on configuration change, in release 1 rather than deferred.',
    ['DDQ-AUD-0006', 'DDQ-CUS-0020', 'DDQ-FCT-0018'],
    [S('SRC-AICPA-SSAE-18'), B('UNB-XIN-ACC-009; CNV-GOV-001')],
    ['UNB-XIN-ACC-009', 'CNV-GOV-001', 'UNB-RCN-PLT-013'],
    'Verified: UNB-XIN-ACC-009 requires the CUEC list but its release scope is Deferred, while CNV-GOV-001 requires CUECs to be mapped before live reliance. Sponsor auditors need the list before the first close.',
    ['A CUEC list exists for each activated sponsor with configuration version.', 'Each convergence clause with cuec true maps to a CUEC entry.'],
    'Document review.', ['EVR-FCT-009', 'EVR-FCT-005'], 'P1', [], LOW)

req('DD-UNB-FIN-007', 'Resolve sponsor-pool NAV and unitization scope',
    'Unbound SHALL mark UNB-NAV-*, UNB-INV-003, UNB-INV-004 and UNB-INV-022 as superseded or narrow them to fund-level valuations derived from external manager or custodian inputs, consistent with CNV-LEG-001 and CNV-FIN-005, and customer materials SHALL state that Unbound does not operate sponsor-maintained investment pools.',
    ['DDQ-INV-0006', 'DDQ-INV-0002', 'DDQ-CUS-0007'],
    [B('CNV-LEG-001; CNV-FIN-005; UNB-INV-003'), S('SRC-UPMIFA', None, 'informed-by', 'reasonably-inferred')],
    ['CNV-LEG-001', 'CNV-FIN-005', 'UNB-INV-003', 'UNB-INV-004', 'UNB-INV-022', 'UNB-NAV-001', 'UNB-NAV-002'],
    'Verified contradiction: CNV-LEG-001 states no sponsor-maintained investment pools SHALL be offered, while UNB-INV-003 (pooled vehicles with unit prices, subscriptions and redemptions), UNB-INV-022 and 53 UNB-NAV records remain original and unamended. An assessor reading UNB-NAV would conclude Unbound computes NAV for sponsor pools.',
    ['Each listed record is flagged or amended.', 'A search of customer materials finds no claim of pool NAV operation.'],
    'Document review.', ['EVR-INV-005', 'EVR-INV-002'], 'P0', ['DD-UNB-GOV-001'], LOW)

req('DD-UNB-FIN-008', 'Remove trade execution APIs',
    'Unbound SHALL NOT expose any API or workflow that submits, routes or executes securities orders for fund accounts; UNB-CUST-007 SHALL be amended to limit Unbound to relaying donor allocation recommendations and recording manager or custodian execution status.',
    ['DDQ-CUS-0021', 'DDQ-CUS-0024', 'DDQ-INV-0003'],
    [B('CNV-LEG-001; UNB-CUST-007')],
    ['CNV-LEG-001', 'UNB-CUST-007', 'UNB-INV-031'],
    'Verified contradiction: UNB-CUST-007 (original, unamended) says execution APIs require separately validated contractual permissions and human authority, while CNV-LEG-001 prohibits routing orders for others\' accounts. ANS-CUS-005 records the conflict.',
    ['UNB-CUST-007 is amended or flagged.', 'An API inventory shows no order submission endpoint.'],
    'API inventory review.', ['EVR-API-004', 'EVR-CUS-007'], 'P0', ['DD-UNB-GOV-001'], LOW)

req('DD-UNB-FIN-009', 'Custodian integration certification',
    'Activation of a custodian integration SHALL require recorded data licensing and entitlement terms, authenticated file or API origin, freshness and gap detection, raw feed retention, a complementary user entity control assignment from the custodian SOC report and a completed recovery drill.',
    ['DDQ-CUS-0002', 'DDQ-CUS-0017', 'DDQ-CUS-0027', 'DDQ-RCN-0001'],
    [C('C13'), C('C15')],
    ['UNB-CUST-009', 'UNB-CUST-017', 'CNV-FIN-013', 'UNB-CUST-024'],
    'Requirements exist piecemeal but no custodian is selected and no activation gate binds them (ANS-CUS-001, ANS-CUS-006).',
    ['The activation gate fails when any listed element is missing.'],
    'Activation gate test.', ['EVR-CUS-001', 'EVR-CUS-002', 'EVR-CUS-006', 'EVR-CUS-009'], 'P1', ['Custodian selection'], MED)

req('DD-UNB-FIN-010', 'Non-cash gift substantiation requirements',
    'Unbound SHALL replace the research-hypothesis gaps UNB-GAP-011 and UNB-GAP-012 with normative requirements for Form 8283 Part V acknowledgment support, Form 8282 disposition tracking within three years, separation of donor-claimed value, appraisal value and sponsor accounting value, and acknowledgment wording that describes rather than values non-cash property.',
    ['DDQ-CON-0015', 'DDQ-CON-0016', 'DDQ-CON-0017', 'DDQ-CON-0018', 'DDQ-RRP-0013', 'DDQ-RRP-0014'],
    [S('SRC-IRC-170'), S('SRC-IRS-PUB-1771')],
    ['UNB-GAP-011', 'UNB-GAP-012', 'CNV-GRT-013', 'UNB-ACC-031'],
    'UNB-GAP-011 and UNB-GAP-012 are classified research-hypothesis. CNV-GRT-013 requires an intermediary that sells on receipt and records the acknowledgment and sale, but detailed substantiation requirements are missing (ANS-CON-004).',
    ['Normative requirements with acceptance tests exist for each listed element.'],
    'Requirements review.', ['EVR-CON-004', 'EVR-RRP-003'], 'P2', [], LOW,
    'Source gap: IRS Form 8283 and 8282 instructions are not in the source register.')

# ---------------------------------------------------------------- PAY
req('DD-UNB-PAY-001', 'Payment file and channel security',
    'Payment instructions and files SHALL be generated in the sponsor cell, signed and encrypted for transmission to the bank or rail over an authenticated channel named per rail, credentials for bank channels SHALL be held in the secret store under workload identity, and the bank SHALL be able to verify origin.',
    ['DDQ-PAY-0030', 'DDQ-PAY-0032', 'DDQ-PAY-0017'],
    [S('SRC-NACHA-DATA-SECURITY'), S('SRC-UCC-4A', None, 'informed-by', 'reasonably-inferred')],
    ['CNV-PAY-001', 'CNV-ARC-003', 'UNB-API-STD-005'],
    'Batch 1 found payment file encryption and signing unspecified; transport depends on unselected banks (ANS-PAY-007).',
    ['A per-rail record names transport, encryption and signing.', 'A tampered file is rejected by the verification step in a test.'],
    'Integration test with bank test environment.', ['EVR-PAY-009', 'EVR-PAY-002'], 'P0', ['Bank selection', 'DD-UNB-SEC-005'], MED)

req('DD-UNB-PAY-002', 'Nacha account number protection',
    'Stored ACH account numbers SHALL be rendered unreadable at rest as required for third-party service providers by the Nacha supplementing data security requirements, independent of volume thresholds.',
    ['DDQ-ENC-0030', 'DDQ-DCL-0010'],
    [S('SRC-NACHA-DATA-SECURITY', None, 'derived-from', 'directly-documented')],
    ['CNV-PAY-001'],
    'CNV-PAY-001 accepts TPSP obligations by contract; no requirement implements this one (batch 1). Applying it regardless of volume avoids a later threshold analysis.',
    ['A data scan of non-vault stores finds no readable account number.'],
    'Data scan.', ['EVR-ENC-009', 'EVR-DCL-003'], 'P0', ['DD-UNB-SEC-004'], LOW)

req('DD-UNB-PAY-003', 'Nacha risk-based fraud monitoring program',
    'Unbound SHALL operate, as a TPSP, a documented risk-based fraud monitoring program for entries it prepares (detection of false pretenses, account takeover and anomalous destinations, review cadence, escalation to the sponsor and ODFI, and annual review), with rules versioned and evidence retained.',
    ['DDQ-FRD-0032', 'DDQ-FRD-0006', 'DDQ-FRD-0020'],
    [S('SRC-NACHA-FRAUD-MONITORING-2026', None, 'derived-from', 'directly-documented')],
    ['CNV-PAY-001', 'CNV-FIN-013', 'UNB-GRANT-044'],
    'Batch 1: Nacha phase 2 (effective June 2026) applies risk-based fraud monitoring to all TPSPs regardless of volume; this is a direct, in-force obligation. CNV-PAY-001 accepts it by contract but no requirement defines the program.',
    ['A program document with rules, owners and review cadence exists.', 'Synthetic anomalous entries generate cases.'],
    'Program review plus synthetic tests.', ['EVR-FRD-010', 'EVR-FRD-009'], 'P0', ['DD-UNB-SEC-015'], MED)

req('DD-UNB-PAY-004', 'Emergency payments during an Unbound outage',
    'Unbound SHALL define and test with each sponsor a procedure for urgent grants during an Unbound outage, in which the sponsor pays through its own bank channel with sanctions, eligibility and dual approval performed manually against a recorded snapshot, and every such payment is reconciled back into the platform before dispatch resumes.',
    ['DDQ-BCP-0026', 'DDQ-BCP-0027', 'DDQ-BCP-0028'],
    [C('C11'), C('C16')],
    ['TVR-PAY-004', 'TVR-PAY-004-Q', 'CNV-PLT-007', 'CNV-ARC-001'],
    'TVR-PAY-004-Q (emergency payments during outage) is an open question; CNV-PLT-007 guarantees the sponsor can pay through its own bank but no procedure or snapshot exists.',
    ['A runbook exists per sponsor.', 'An exercise shows a manually paid grant reconciled and not re-dispatched.'],
    'Exercise.', ['EVR-BCP-008', 'EVR-DR-007'], 'P1', [], LOW)

req('DD-UNB-PAY-005', 'Check production custody',
    'For the check fallback rail, Unbound SHALL specify who prints and mails checks, custody of check stock and signature images, positive pay file delivery timing and controls preventing a vendor or printer from altering payee or amount.',
    ['DDQ-FRD-0015', 'DDQ-PAY-0023'],
    [S('SRC-UCC-4A', None, 'informed-by', 'unknown')],
    ['CNV-PAY-002', 'CNV-PAY-001', 'UNB-XIN-OTH-004'],
    'CNV-PAY-002 covers check lifecycle and positive pay and UNB-XIN-OTH-004 requires print batch manifests and per-piece dispositions from the print vendor; check stock custody, signature image custody and controls against vendor alteration remain unspecified, and CNV-PAY-001 makes a check fallback mandatory for every program.',
    ['A check operations specification exists.', 'Positive pay issue files are produced before release in a test.'],
    'Specification review plus test.', ['EVR-PAY-007', 'EVR-FRD-005'], 'P2', ['Bank selection'], LOW)

req('DD-UNB-PAY-006', 'End-to-end idempotency for ACH',
    'Because ACH lacks an end-to-end idempotency key, Unbound SHALL bind each entry to a stable trace or identification value recorded before transmission and SHALL resolve unknown outcomes only through rail status queries or bank activity matching before any re-initiation.',
    ['DDQ-API-0032', 'DDQ-TXI-0007', 'DDQ-TXI-0033'],
    [C('C06'), S('SRC-NACHA-RULES')],
    ['TVR-PAY-002', 'TVR-PAY-002-Q', 'CNV-PAY-004', 'CNV-ARC-003'],
    'TVR-PAY-002-Q records that ACH lacks an end-to-end key; CNV-PAY-004 governs unknown outcomes. The binding of a stable identifier is not stated.',
    ['A replay test after crash produces no duplicate entry.'],
    'Fault injection test.', ['EVR-TXI-001', 'EVR-TXI-008', 'EVR-TXI-007'], 'P1', ['Bank selection'], LOW)

# ---------------------------------------------------------------- AML / sanctions
req('DD-UNB-AML-001', 'Production sanctions matcher and list provider',
    'Before activation, Unbound SHALL select a sanctions list provider and matcher, validate it against the versioned perturbation suite required by CNV-GRT-006 with recall approved by each sponsor compliance officer, and record subgroup false-alert rates.',
    ['DDQ-AML-0011', 'DDQ-AML-0013', 'DDQ-AML-0001', 'DDQ-AML-0002'],
    [S('SRC-OFAC-COMPLIANCE-FRAMEWORK'), B('CNV-GRT-006')],
    ['CNV-GRT-006', 'UNB-EXT-004'],
    'Verified: CNV-GRT-006 states the reference matcher does not meet the recall test and SHALL NOT be used in production; no replacement or provider is selected.',
    ['A validation report shows recall on the suite meeting the approved target.', 'Subgroup false-alert rates are reported.'],
    'Matcher validation run.', ['EVR-AML-004', 'EVR-AML-005', 'EVR-AML-003'], 'P0', ['Screening provider selection'], REC(MED, 'list data subscription'))

req('DD-UNB-AML-002', 'Adverse media in grantee diligence',
    'Unbound SHALL define whether and how adverse media is used in grantee deep review, including sources, licensing, human review and the rule that adverse media is input for a qualified reviewer, never an automatic decline.',
    ['DDQ-CHV-0032', 'DDQ-TPR-0009'],
    [S('SRC-TREASURY-CHARITY-GUIDELINES')],
    ['CNV-GRT-003', 'CNV-GRT-004'],
    'No requirement mentions adverse media (zero matches). CNV-GRT-003 requires any known adverse public fact to be considered but names no source.',
    ['A policy records the decision.', 'If used, review records show source, date and reviewer.'],
    'Policy review.', ['EVR-CHV-006', 'EVR-CHV-010'], 'P3', [], LOW)

# ---------------------------------------------------------------- CHV / GRT / DON
req('DD-UNB-CHV-001', 'State charity standing beyond California',
    'Unbound SHALL define a plan and data sources to extend state charity standing checks beyond California, prioritized by sponsor grant volume, and SHALL display the coverage limits to reviewers.',
    ['DDQ-CHV-0049'],
    [S('SRC-STATE-CHARITABLE-SOLICITATION')],
    ['CNV-GRT-015'],
    'CNV-GRT-015 covers California first; other states are unspecified.',
    ['A coverage table lists states with source and status.'],
    'Document review.', ['EVR-CHV-001'], 'P3', [], LOW)

req('DD-UNB-GRT-001', 'Expenditure responsibility handling in release 1',
    'Until an expenditure responsibility workflow exists, Unbound SHALL block grants to recipients that would require expenditure responsibility and SHALL tell the recommender why.',
    ['DDQ-CHV-0018', 'DDQ-DAF-0044'],
    [S('SRC-IRC-4966', None, 'maps-to', 'directly-documented')],
    ['CNV-GRT-002', 'CNV-GRT-008'],
    'CNV-GRT-008 (intermediaries and equivalency determinations) is deferred and batch 1 found the expenditure responsibility workflow unspecified; CNV-GRT-002 defines eligible classes but the blocking behavior for ER-requiring grants is not explicit.',
    ['A grant to a non-public-charity recipient class requiring ER is refused in a test with a neutral reason.'],
    'Negative test.', ['EVR-CHV-005', 'EVR-GRT-007'], 'P1', [], LOW)

req('DD-UNB-DON-001', 'Death and incapacity verification sources and executor access',
    'Unbound SHALL specify acceptable evidence and sources for verifying a donor\'s death or incapacity, the verification steps before authority changes, and what an executor or estate representative may see and do.',
    ['DDQ-DAF-0022', 'DDQ-DON-0033', 'DDQ-DON-0032'],
    [S('SRC-IRC-4966', None, 'informed-by', 'reasonably-inferred')],
    ['CNV-ENT-001', 'AUTH-I5', 'REQ-X-008', 'UNB-GAP-015'],
    'CNV-ENT-001 and AUTH-I5 cover suspension and succession, but batch 1 found death-verification sources and executor visibility unspecified; UNB-GAP-015 is a research hypothesis.',
    ['A specification lists evidence types and verification steps.', 'An executor role test shows read-only access limited to the deceased donor\'s funds.'],
    'Specification review plus role test.', ['EVR-DON-007', 'EVR-DAF-005'], 'P2', [], LOW)

# ---------------------------------------------------------------- OPS
req('DD-UNB-OPS-001', 'Support model, severity matrix and status page',
    'Unbound SHALL define support hours and after-hours coverage for critical issues, a severity matrix with response and update targets, an escalation matrix, a status page hosted independently of production with component status and incident history, and maintenance notice periods.',
    ['DDQ-SUP-0001', 'DDQ-SUP-0005', 'DDQ-SUP-0006', 'DDQ-AVL-0009', 'DDQ-AVL-0012'],
    [C('C16'), S('SRC-ISO-20000-1')],
    ['UNB-GAP-028', 'ADM-033', 'CNV-ARC-001'],
    'UNB-GAP-028 (support coverage, SLAs, escalation) is a research hypothesis; CNV-ARC-001 forbids numeric contractual SLAs before benchmark and pilot evidence, so targets must be published as objectives until then.',
    ['A published support policy and severity matrix exist.', 'The status page remains available when production is down in a test.'],
    'Document review plus failover test.', ['EVR-SUP-001', 'EVR-SUP-002', 'EVR-SUP-003', 'EVR-AVL-004'], 'P1', ['DD-UNB-SEC-024'], REC(LOW, 'on-call coverage'))

req('DD-UNB-OPS-002', 'Consent-based support access to donor accounts',
    'Support access to a donor or advisor account SHALL require sponsor-policy approval and, where the sponsor notice requires it, recorded user consent, SHALL be time-bounded and read-only by default, and SHALL be visible to the sponsor and the user afterward.',
    ['DDQ-SUP-0013', 'DDQ-IAM-0023', 'DDQ-NET-0020', 'DDQ-MON-0028'],
    [S('SRC-Q-GKCCF-PRIVACY-POLICY', 'consent-based service provider login', 'derived-from', 'directly-documented')],
    ['CNV-ARC-002', 'CNV-GOV-006'],
    'CNV-ARC-002 requires sponsor pre-approval and evidence for operator access; at least one sponsor privacy notice describes user consent for vendor support login (DD-IND-DAF-001), which no requirement captures.',
    ['A support session without consent is refused where the sponsor requires consent.', 'The access transparency log shows the session to the sponsor.'],
    'Access test plus log review.', ['EVR-SUP-004', 'EVR-IAM-007'], 'P2', [], LOW)

req('DD-UNB-OPS-003', 'Manual intervention register',
    'Every manual operator action that can affect a sponsor\'s data, holds or instruction flow (break-glass, data correction, hold placement, replay, export on request) SHALL be listed in a register with permitted roles, approvals, evidence and sponsor visibility, and any action not on the register SHALL be technically blocked.',
    ['DDQ-FCT-0034', 'DDQ-IAM-0026', 'DDQ-DAF-0034'],
    [S('SRC-AICPA-TSC', 'CC6.1, CC8.1'), C('C04')],
    ['CNV-GOV-006', 'CNV-PLT-007', 'UNB-XIN-IAM-005', 'CNV-ARC-002'],
    'CNV-GOV-006 justifies human steps in the sponsor workflow and CNV-PLT-007 governs platform holds, but operator interventions are spread across clauses with no single register an assessor can review.',
    ['The register exists and maps each action to its governing clause.', 'An unregistered administrative command is rejected in a test.'],
    'Register review plus negative test.', ['EVR-FCT-010', 'EVR-IAM-006', 'EVR-DAF-007'], 'P1', [], LOW)

# ---------------------------------------------------------------- BCP
req('DD-UNB-BCP-001', 'Key-person continuity',
    'Echelon SHALL document a succession arrangement naming a person with legal authority to act if the principal is unavailable, emergency custody of credentials for domains, code hosting, cloud accounts and signing keys, and a key-person dependency register with mitigations.',
    ['DDQ-BCP-0017', 'DDQ-BCP-0018', 'DDQ-GOV-0020', 'DDQ-GOV-0021', 'DDQ-GOV-0022'],
    [S('SRC-ISO-22301-2019'), C('C18')],
    ['UNB-GAP-028'],
    'ANS-BCP-005 records unknown how many people can deploy, restore or rotate credentials and whether a succession arrangement exists. For a founder-led company this is a deciding question.',
    ['A signed succession designation exists.', 'An emergency credential custody record exists and a test recovery by the designee succeeds.'],
    'Document review plus recovery test.', ['EVR-BCP-005', 'EVR-BCP-006', 'EVR-GOV-004'], 'P0', ['DD-UNB-LEG-004'], LOW)

req('DD-UNB-BCP-002', 'Business continuity program',
    'Echelon SHALL adopt a business continuity policy and business impact analysis for Unbound, plans with out-of-band communication, and an annual exercise program including a sponsor-participating exercise.',
    ['DDQ-BCP-0001', 'DDQ-BCP-0013', 'DDQ-BCP-0011'],
    [S('SRC-ISO-22301-2019'), S('SRC-FFIEC-BCM-BOOKLET')],
    ['UNB-OPS-001', 'SOC2-015', 'UNB-LS-011'],
    'Continuity appears only as list items (UNB-OPS-001, SOC2-015) and a hypothesis (UNB-GAP-028).',
    ['Approved policy and BIA exist.', 'An exercise report with remediation exists within 12 months.'],
    'Document and exercise review.', ['EVR-BCP-001', 'EVR-BCP-002', 'EVR-BCP-003', 'EVR-BCP-004'], 'P1', ['DD-UNB-SEC-020'], LOW)

req('DD-UNB-BCP-003', 'Approved recovery objectives and restore tests',
    'Unbound SHALL approve the single recovery objectives table required by CNV-ARC-001 (keyed by data class and isolation profile), retire the per-capability wording of UNB-RES-003, and demonstrate the objectives by failover and restore tests before production.',
    ['DDQ-DR-0001', 'DDQ-DR-0010', 'DDQ-DR-0020', 'DDQ-DR-0021'],
    [S('SRC-NIST-SP800-34-R1'), B('CNV-ARC-001; UNB-RES-003; RR-UNB-RES-003-r2')],
    ['CNV-ARC-001', 'UNB-RES-003', 'RR-UNB-RES-003-r2', 'REQ-X-047'],
    'Verified: UNB-RES-003 (original, not amended) requires RTO and RPO per capability while CNV-ARC-001 requires one table keyed by data class; RR-UNB-RES-003-r2 values are candidates only. Recovery objective questions cannot be answered.',
    ['An approved table exists.', 'A restore test report shows measured RTO and RPO against the table and post-restore payment safety checks.'],
    'Restore and failover test.', ['EVR-DR-001', 'EVR-DR-003', 'EVR-DR-007', 'EVR-BKP-005'], 'P1', ['DD-UNB-SEC-021', 'DD-UNB-GOV-001'], MED)

req('DD-UNB-BCP-004', 'Rebuild from source after account compromise',
    'Unbound SHALL be able to rebuild production in a clean cloud account from source, infrastructure code and immutable backups held in a separate account, and SHALL test this at least annually.',
    ['DDQ-DR-0016', 'DDQ-IR-0041', 'DDQ-BKP-0007'],
    [S('SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022'), S('SRC-NIST-SP800-34-R1')],
    ['UNB-GAP-034', 'CNV-ARC-001'],
    'The coverage screen classed DDQ-DR-0016 as only weakly covered; UNB-GAP-034 (immutable backup, restoration tests) is a hypothesis.',
    ['A rebuild test report shows time to rebuild and integrity verification passing.'],
    'Annual rebuild test.', ['EVR-DR-005', 'EVR-BKP-003', 'EVR-IR-008'], 'P1', ['DD-UNB-SEC-022'], MED)

# ---------------------------------------------------------------- A11Y
req('DD-UNB-A11Y-001', 'Accessibility conformance report with independent validation',
    'Unbound SHALL publish an Accessibility Conformance Report (VPAT, WCAG 2.2 and Section 508 editions) for each major release covering every user role and surface, validated by an independent accessibility specialist, with defect remediation targets by severity.',
    ['DDQ-A11Y-0001', 'DDQ-A11Y-0003', 'DDQ-A11Y-0006', 'DDQ-A11Y-0007', 'DDQ-A11Y-0016'],
    [S('SRC-ITI-VPAT'), S('SRC-WCAG-2.2'), S('SRC-Q-FIDELITY-SUPPLIER-POLICIES', 'third-party ACR')],
    ['CNV-EXP-001', 'UNB-UX-006', 'UNB-EXP-001'],
    'CNV-EXP-001 requires WCAG 2.2 AA and measured conformance before publication, but no requirement produces an ACR or independent validation; a large-bank supplier policy does not accept self-assessment.',
    ['An ACR exists per release with preparer and validator named.', 'A defect register shows remediation against targets.'],
    'Independent review.', ['EVR-A11Y-002', 'EVR-A11Y-004', 'EVR-A11Y-005'], 'P1', ['Running build'], REC(MED, 'per-release validation'))

req('DD-UNB-A11Y-002', 'Accessible PDF pipeline',
    'Unbound SHALL select a PDF renderer that produces tagged PDF conforming to PDF/UA for statements, acknowledgments and grant letters, verify it with automated and manual checks, and amend UNB-PLAT-003 to match CNV-EXP-001.',
    ['DDQ-A11Y-0019'],
    [S('SRC-WCAG-2.2'), S('SRC-EN-301-549')],
    ['CNV-EXP-001', 'UNB-PLAT-003', 'UNB-ACC-025'],
    'Verified: UNB-PLAT-003 requires Folio for all enterprise documents, while CNV-EXP-001 states Folio provides markup only and the PDF pipeline is Unbound-owned until an upstream renderer exists. Folio does not provide tagged PDF (batch 1). No renderer is chosen.',
    ['A renderer decision record exists.', 'PDF/UA validation passes for each document template.'],
    'Automated PDF/UA validation plus screen reader check.', ['EVR-A11Y-006'], 'P1', ['DD-UNB-GOV-001'], MED)

req('DD-UNB-A11Y-003', 'Accessibility legal applicability',
    'Echelon SHALL obtain a determination of which accessibility laws apply through its intended customers (ADA Title III, Title II for public entities, Section 508, European Accessibility Act) and record contractual commitments accordingly.',
    ['DDQ-A11Y-0028'],
    [S('SRC-ADA'), S('SRC-SECTION-508'), S('SRC-EU-ACCESSIBILITY-ACT')],
    ['UNB-GAP-031'],
    'UNB-GAP-031 (assess applicable ADA obligations) is a research hypothesis; ANS-A11Y-007 records customer-type questions open.',
    ['A determination record exists.'],
    'Legal review.', ['EVR-A11Y-008'], 'P2', ['DD-UNB-LEG-001'], LOW)

req('DD-UNB-A11Y-004', 'Accessible authentication and identity proofing',
    'Sign-in, step-up and identity proofing SHALL be completable without cognitive function tests, puzzles or sole reliance on visual or biometric steps, using the AccessibleAssurancePath of CNV-PLT-011, verified by assistive technology testing.',
    ['DDQ-A11Y-0033'],
    [S('SRC-WCAG-2.2', '3.3.8'), S('SRC-NIST-SP800-63-4')],
    ['CNV-PLT-011', 'CNV-PLT-003'],
    'CNV-PLT-011 defines an accessible assurance path; the identity proofing vendor is not selected, so whether the chosen flow meets WCAG 2.2 accessible authentication is unverified.',
    ['Assistive technology test records show completion of each authentication path.'],
    'Assistive technology testing.', ['EVR-A11Y-009', 'EVR-A11Y-004'], 'P2', ['Identity proofing vendor selection'], LOW)

# ---------------------------------------------------------------- EXIT (migration, termination, export)
req('DD-UNB-EXIT-001', 'Inbound migration specification',
    'Unbound SHALL specify inbound migration from a predecessor administrator: source data mapping, identifier preservation and aliases, import of issued acknowledgments as original artifacts, ACH authorizations and donor preferences, re-verification of legacy grantee flags, parallel run with a single authoritative system at any time, and a signed migration reconciliation of balances, units and history before cutover.',
    ['DDQ-PRT-0015', 'DDQ-PRT-0016', 'DDQ-RCN-0035', 'DDQ-DAF-0006', 'DDQ-CHV-0044', 'DDQ-DCL-0017'],
    [C('C17'), C('C12')],
    ['CNV-EXP-002', 'UNB-RCN-WF-009', 'CNV-FIN-004', 'REQ-X-025'],
    'CNV-EXP-002 requires import of full fund history with a reconciliation report and UNB-RCN-WF-009 requires tied-out opening balances, but no requirement specifies mapping, parallel run, authorization transfer or legacy flag re-verification. ANS-PRT-004 records that predecessor exports may be unobtainable.',
    ['A migration specification exists with acceptance tests.', 'A dry run on a synthetic five-year ledger reconciles to the source with zero unexplained differences.'],
    'Migration dry run.', ['EVR-PRT-004', 'EVR-RCN-012'], 'P1', [], MED)

req('DD-UNB-EXIT-002', 'Published export schema and independent reconstruction test',
    'Unbound SHALL publish a versioned export schema and data dictionary available before contract signature, provide self-service full and incremental export during the term at no charge, and demonstrate annually that an independent party can reconstruct balances and statuses from an export without Unbound software.',
    ['DDQ-PRT-0001', 'DDQ-PRT-0002', 'DDQ-PRT-0004', 'DDQ-PRT-0005', 'DDQ-PRT-0008', 'DDQ-PRT-0011'],
    [C('C12'), S('SRC-INTERAGENCY-TPRM-2023', 'termination')],
    ['CNV-ENT-002', 'RR-UNB-TEN-016-r1', 'REQ-X-039'],
    'CNV-ENT-002 requires a full reconciled export and an export manifest covering every class; RR-UNB-TEN-016-r1 (signed manifest, independent verification) is unvalidated, deferred and amended. No requirement publishes a schema or tests independent reconstruction (C12).',
    ['The schema is published with version history.', 'An independent reconstruction test reproduces trial balances per fund and period.'],
    'Reconstruction test.', ['EVR-PRT-001', 'EVR-PRT-002', 'EVR-PRT-005', 'EVR-TRM-004'], 'P1', [], MED)

req('DD-UNB-EXIT-003', 'Termination assistance and in-flight items',
    'The standard contract SHALL commit to a transition period at unchanged service levels, export API availability throughout notice and transition, no suspension of data access during disputes, defined handling of pending recommendations, approved unpaid grants, recurring series and holds, unwinding of TPSP roles with the sponsor\'s bank, and the fees, if any, for transition assistance.',
    ['DDQ-TRM-0001', 'DDQ-TRM-0002', 'DDQ-TRM-0004', 'DDQ-TRM-0010', 'DDQ-TRM-0020', 'DDQ-TRM-0021', 'DDQ-LEG-0027'],
    [S('SRC-INTERAGENCY-TPRM-2023', 'termination'), C('C11')],
    ['CNV-ENT-002', 'CNV-PAY-001'],
    'CNV-ENT-002 covers records custody, read-only access for 90 days and backup expiry, but not transition service levels, dispute access or in-flight item handling.',
    ['The contract schedule covers each element.', 'An exit dry run exercises in-flight items.'],
    'Contract review plus exit dry run.', ['EVR-TRM-001', 'EVR-TRM-002', 'EVR-TRM-005'], 'P1', ['DD-UNB-LEG-002'], LOW)

req('DD-UNB-EXIT-004', 'Insolvency protection: escrow, wind-down plan and reserve',
    'Echelon SHALL offer a SaaS escrow arrangement for Unbound (source, build and deployment materials, infrastructure code, schemas and runbooks, excluding secrets) verified at least annually by build and deployment test, a written wind-down plan, and a funded reserve sized to complete an orderly transition for all customers.',
    ['DDQ-FST-0012', 'DDQ-FST-0013', 'DDQ-FST-0014', 'DDQ-FST-0015', 'DDQ-TRM-0011', 'DDQ-TRM-0012', 'DDQ-ESC-0001', 'DDQ-ESC-0007', 'DDQ-GOV-0023'],
    [S('SRC-SOFTWARE-ESCROW-PRACTICE'), C('C11'), C('C18')],
    ['CNV-GOV-009', 'CNV-ENT-002'],
    'CNV-GOV-009 covers escrow for Echelon dependencies used by Unbound, not escrow for customers. ANS-ESC-001 and ANS-TRM-003 are unknown. The PolyForm Noncommercial license on most components means a successor operator may lack rights to run escrowed code without a commercial license (DD-UNB-VEND-003).',
    ['An escrow agreement and verification report exist.', 'A wind-down plan and reserve evidence exist.'],
    'Document review plus escrow verification report.', ['EVR-ESC-001', 'EVR-ESC-002', 'EVR-FST-003', 'EVR-FST-006'], 'P1', ['DD-UNB-VEND-003', 'DD-UNB-LEG-004'], REC(MED, 'escrow fees and reserve funding'))

req('DD-UNB-EXIT-005', 'Scheduled exports to sponsor-owned storage',
    'Unbound SHALL offer scheduled full and incremental exports, with manifests and control totals, delivered to sponsor-owned storage so that each sponsor holds a current copy of its records independent of Echelon.',
    ['DDQ-TRM-0013', 'DDQ-FST-0016'],
    [C('C11'), C('C12')],
    ['CNV-ENT-002'],
    'No requirement provides continuous customer-held copies; this is the cheapest mitigation for vendor insolvency.',
    ['A scheduled export delivers to a test bucket owned by a separate account with a verifiable manifest.'],
    'Integration test.', ['EVR-TRM-003', 'EVR-PRT-002'], 'P2', ['DD-UNB-EXIT-002'], LOW)

req('DD-UNB-EXIT-006', 'Exit drill',
    'Unbound SHALL run an exit drill at least annually on a synthetic sponsor (notice, export, independent verification, in-flight handling, read-only period, backup expiry and destruction certificate) and offer the drill report to sponsors.',
    ['DDQ-TRM-0003', 'DDQ-TRM-0017'],
    [C('C11'), S('SRC-INTERAGENCY-TPRM-2023', 'termination')],
    ['CNV-ENT-002', 'CNV-PLT-009'],
    'CNV-ENT-002 defines exit outcomes but no requirement tests them; C11 asks for an observed exit drill.',
    ['A drill report exists within 12 months with timeline and findings.'],
    'Exercise.', ['EVR-TRM-001', 'EVR-TRM-004', 'EVR-ASM-008'], 'P2', ['DD-UNB-EXIT-002'], LOW)

# ---------------------------------------------------------------- VEND
req('DD-UNB-VEND-001', 'Subprocessor register and notice in release 1',
    'The tenant-specific subprocessor register and 30-day change notice in UNB-XIN-SAS-011 SHALL be in release 1 scope rather than deferred, with an objection process and AI providers listed.',
    ['DDQ-SUB-0001', 'DDQ-SUB-0005', 'DDQ-PRV-0019', 'DDQ-LEG-0029'],
    [S('SRC-Q-ENVESTNET-TRUST-SUBPROCESSORS'), S('SRC-Q-TRUIST-TPISS', 'per-subprocessor consent')],
    ['UNB-XIN-SAS-011', 'SOC2-013', 'SOC2-022'],
    'Verified: UNB-XIN-SAS-011 has release scope Deferred. Subprocessor lists are expected at first contract, and one large-bank supplier standard requires per-subprocessor prior written consent (batch 1).',
    ['A published register is generated from the vendor inventory.', 'A test subprocessor change produces notices 30 days before effect.'],
    'Register and notice log review.', ['EVR-SUB-001', 'EVR-SUB-003', 'EVR-LEG-004'], 'P1', ['DD-UNB-SEC-021', 'DD-UNB-AIA-001'], LOW)

req('DD-UNB-VEND-002', 'Critical provider selection with due diligence',
    'Before activation, Echelon SHALL select and record due diligence for each critical provider (hosting, bank or payment rail, custodian feeds, sanctions list, identity proofing, email and AI model), including assurance report review, contract term checklist, concentration and exit plan.',
    ['DDQ-RSK-0019', 'DDQ-TPR-0009'],
    [S('SRC-INTERAGENCY-TPRM-2023'), S('SRC-ISO-27036')],
    ['SOC2-013', 'CNV-GOV-002', 'UNB-LS-011', 'TVR-PAY-002'],
    'SOC2-013 and CNV-GOV-002 define vendor monitoring, but no bank, custodian, crypto or screening provider is selected (batch 1), so many answers depend on unknown counterparties.',
    ['A due diligence file exists for each listed provider class.'],
    'File review.', ['EVR-TPR-003', 'EVR-TPR-005', 'EVR-TPR-006', 'EVR-TPR-009'], 'P0', [], MED)

req('DD-UNB-VEND-003', 'Commercial license and customer rights for Echelon components',
    'Before commercial availability, Echelon SHALL execute commercial licenses for every PolyForm Noncommercial component in Unbound and SHALL define customer, auditor, escrow beneficiary and successor operator rights to run and inspect those components.',
    ['DDQ-IPR-0005', 'DDQ-IPR-0006', 'DDQ-IPR-0007', 'DDQ-IPR-0020'],
    [S('SRC-ECH-BUSINESS-PLAN'), B('CNV-GOV-009')],
    ['CNV-GOV-009', 'UNB-PLAT-006'],
    'CNV-GOV-009 makes an executed commercial license a gate; batch 1 notes nearly the whole stack is PolyForm Noncommercial and customer, auditor and escrow rerun rights are unaddressed.',
    ['Executed licenses exist for each component.', 'The SBOM license gate passes.', 'The customer agreement states the rights.'],
    'License gate plus contract review.', ['EVR-IPR-003', 'EVR-IPR-005', 'EVR-SCS-008'], 'P0', ['DD-UNB-LEG-004'], LOW)

# ---------------------------------------------------------------- AUD (assurance plan)
req('DD-UNB-AUD-001', 'SOC 2 Type II plan tied to first production data',
    'Echelon SHALL engage a qualified CPA firm, complete a readiness assessment and begin a SOC 2 Type II observation period no later than the first production processing of real donor data, with scope covering security, availability and confidentiality and the inclusive or carve-out treatment of the hosting provider stated.',
    ['DDQ-AUD-0001', 'DDQ-AUD-0002', 'DDQ-AUD-0004', 'DDQ-AUD-0007', 'DDQ-CLD-0011'],
    [S('SRC-AICPA-SOC2'), S('SRC-AICPA-TSC-2027-ED', None, 'informed-by', 'reasonably-inferred'), C('C09')],
    ['CNV-GOV-001', 'UNB-RCN-PLT-013', 'SOC2-036'],
    'CNV-GOV-001 sets scope by actual reliance and avoids stand-alone Type 1, which suits SOC 1 but leaves no SOC 2 timing. Every assessor asks for SOC 2 Type II first; the incumbent baseline is a Type 1 (batch 1). Timing is judgment requiring owner decision; the 2027 criteria exposure draft may apply.',
    ['An engagement letter exists.', 'A readiness report and observation period start date are recorded.'],
    'Document review.', ['EVR-AUD-001', 'EVR-AUD-006'], 'P1', ['DD-UNB-GOV-003', 'DD-UNB-SEC-020'], REC(HIGH, 'annual audit fees'))

req('DD-UNB-AUD-002', 'Customer and examiner access terms',
    'The contract package SHALL grant sponsors and their auditors a right to audit and examiners of regulated customers access to records, personnel and systems, with notice periods and a standard evidence pack.',
    ['DDQ-AUD-0023', 'DDQ-AUD-0024', 'DDQ-ISP-0037'],
    [S('SRC-INTERAGENCY-TPRM-2023', 'oversight and accountability'), S('SRC-BSCA')],
    ['CNV-GOV-001', 'MON-016'],
    'CNV-GOV-001 requires right-to-audit and an evidence pack in contracts but does not address regulator access for bank customers.',
    ['The contract package contains both rights.'],
    'Contract review.', ['EVR-REG-004', 'EVR-RRP-010'], 'P2', ['DD-UNB-LEG-002'], LOW)

# ---------------------------------------------------------------- additional finance controls
req('DD-UNB-FIN-011', 'Fee recomputation and ledger tie-out',
    'Each fee run SHALL be independently recomputed from the schedule version and source balances by a separate process, with differences raised as exceptions, and fees SHALL tie to the payee and the general ledger before statements publish.',
    ['DDQ-FEE-0008', 'DDQ-FCT-0013'],
    [C('C21')],
    ['CNV-FIN-002', 'CNV-FIN-012'],
    'CNV-FIN-002 versions schedules and requires daily computation but sets no independent recomputation; the sponsor audit matrix (C21) asks for fee and ledger tie-out evidence.',
    ['A recomputation report shows zero unexplained differences for each run.'],
    'Automated recomputation per run.', ['EVR-FCT-004', 'EVR-FEE-002'], 'P2', [], LOW)

req('DD-UNB-FIN-012', 'Retention floor consistency',
    'All Unbound requirements stating a seven-year retention floor for transaction-level financial or grant records SHALL be aligned with the ten-year release-1 floor of CNV-PLT-004, and the retention schedule SHALL be approved by each sponsor compliance owner.',
    ['DDQ-CON-0035', 'DDQ-MON-0012'],
    [B('CNV-PLT-004; REQ-X-045; REQ-X-048')],
    ['CNV-PLT-004', 'REQ-X-045', 'REQ-X-048', 'REQ-X-036', 'REQ-X-037', 'REQ-X-038', 'REQ-X-039', 'REQ-X-040', 'REQ-X-041', 'RR-REQ-X-036-r1'],
    'Verified: REQ-X-037 to REQ-X-041, REQ-X-045 and REQ-X-048 (original, not amended) and RR-REQ-X-036-r1 state a seven-year financial floor, while CNV-PLT-004 applies a ten-year floor to all transaction-level financial and grant records in release 1 and amends only REQ-X-036. The texts are not logically incompatible (ten years satisfies a seven-year minimum), but an assessor quoting the seven-year text will state the wrong release-1 retention period.',
    ['Each listed record states that CNV-PLT-004 governs the release-1 period, or is flagged in the DD-UNB-GOV-001 register.'],
    'Document search.', ['EVR-RET-001', 'EVR-MON-003'], 'P2', ['DD-UNB-GOV-001'], LOW)

with open(OUT, 'w') as f:
    for r in R:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
print(len(R))
