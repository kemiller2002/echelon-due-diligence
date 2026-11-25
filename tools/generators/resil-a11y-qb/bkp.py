from rqb_common import *
c = Cat("BKP", {"industries": ["all"], "jurisdictions": ["US-federal"], "products": ["unbound"]})
OWN = "Proposed: SRE Lead (role not yet staffed)"
RAT = "No production data, backup system or restore test exists as of 2026-11-25; backup design appears only in Unbound requirements."
FIN = ["banking", "financial-services", "wealth-management", "donor-advised-funds"]

e1 = c.E(1, "Backup inventory and schedule", "Generated list of every backed-up data store (databases, object storage, issued documents, configuration, secrets metadata, source repositories) with frequency, retention, copy locations and the data class it serves; stores intentionally excluded are listed with the rebuild path.",
         mechanism="continuous-automated", freshness="P1D", disc="customer-only", fmt="JSON generated from backup configuration")
e2 = c.E(2, "Backup job outcome stream", "Per-job success or failure, size, duration and digest, with an alert and control exception raised when an expected backup is missing.",
         mechanism="continuous-automated", freshness="P1D", disc="auditor-only", prov=["job_id", "store", "start", "end", "digest", "status"],
         notes="SOC2-027 treats a missing expected heartbeat as a control exception.")
e3 = c.E(3, "Backup immutability and separation configuration attestation", "Automated read of backup vault configuration showing object-lock or equivalent retention mode, separate account or tenancy, separate credentials, and absence of delete permissions for production and agent identities.",
         mechanism="periodic-automated", freshness="P1D", disc="nda", prov=["vault_id", "lock_mode", "retention_days", "principals_with_delete"])
e4 = c.E(4, "Backup encryption and key recovery record", "Encryption algorithm, key hierarchy, key custody (separate from production keys) and the dated result of recovering a backup key from escrow.",
         mechanism="periodic-manual", freshness="P1Y", disc="auditor-only")
e5 = c.E(5, "Restore test with integrity verification", "Dated restore of each data class into an isolated environment, followed by hash-chain or signed-checkpoint verification, trial balances per fund and record counts compared with the source.",
         mechanism="periodic-automated", freshness="P90D", disc="nda", prov=["restore_id", "source_point", "checkpoint_digest", "trial_balance_match", "record_count_match"])
e6 = c.E(6, "Deterministic replay equivalence test", "Result of rebuilding projections and balances by replaying the append-only journal and comparing them with the live projections, including a check that no external effect was emitted during replay.",
         mechanism="periodic-automated", freshness="P30D", disc="nda", prov=["journal_watermark", "projection_digest_live", "projection_digest_replayed", "external_effects_emitted"])
e7 = c.E(7, "Backup expiry and destruction record", "For each deletion request, tenant exit or retention expiry: which backups still contain the data, their expiry dates, legal holds applied and the destruction certificate issued.",
         mechanism="event-driven-automated", freshness="per-event", disc="customer-only", retention="P7Y")

k1 = c.C(1, "Declared backup coverage generated from configuration", "Ensure every authoritative store is backed up at a frequency that meets its data-class RPO and that exclusions are explicit and justified by a tested rebuild path.",
         "detective-automated", "L6-automated-analysis", ["not yet assigned"], [e1, e2], OWN, related=["SOC2-015", "SOC2-027"],
         fw=[R("SRC-NIST-SP800-53-R5", "CP-9"), R("SRC-ISO-27002-2022", "8.13"), R("SRC-NIST-CSF-2.0", "PR.DS-11")])
k2 = c.C(2, "Immutable backups in a separate security domain", "Prevent deletion or alteration of backups by any production, administrator or agent identity during the retention period, by storing them in a separate account with retention lock.",
         "preventive-structural", "L3-restricted-interface", ["Cloud backup vault with retention lock (provider not selected)"], [e3], OWN,
         related=["SOC2-006", "UNB-DATA-008"], fw=[R("SRC-NIST-SP800-53-R5", "CP-9"), R("SRC-EU-DORA", "Article 12")],
         residual=["Compliance-mode retention locks cannot be shortened, which conflicts with deletion requests until expiry."])
k3 = c.C(3, "Backup encryption with independently recoverable keys", "Encrypt backups with keys held outside production key scope and keep an escrowed recovery path tested annually.",
         "preventive-structural", "L3-restricted-interface", ["Key management service (provider not selected)"], [e4], "Proposed: Security Lead (role not yet staffed)",
         policies=["SEC-CRYPTO-001"], fw=[R("SRC-NIST-SP800-53-R5", "CP-9(8)")])
k4 = c.C(4, "Dual-controlled restore operations", "Require two authorized people for any restore into production, log the action as tamper-evident evidence, and deny agents the ability to initiate production restores.",
         "preventive-gate", "L3-restricted-interface", ["not yet assigned"], [e3], OWN, policies=["SEC-AUTH-001"], related=["SOC2-017"])
k5 = c.C(5, "Scheduled restore with financial integrity verification", "Restore a sample of each data class on a schedule and verify integrity cryptographically and by trial balance, not only by successful job completion.",
         "detective-automated", "L7-property-tested", ["Unbound integrity verification (not built)"], [e5], OWN, related=["UNB-DATA-012", "UNB-TEC-STRATA-004"],
         fw=[R("SRC-NIST-SP800-53-R5", "CP-9(1)")])
k6 = c.C(6, "Append-only journal with side-effect-free replay", "Make the authoritative ledger strictly append-only and make replay deterministic and incapable of emitting external effects, so state can be reconstructed to any point.",
         "preventive-structural", "L2-type-system", ["Unbound ledger component (not built)", "Managed PostgreSQL"], [e6], "Proposed: Unbound architecture owner",
         related=["ACC-MDL-002", "ACC-MDL-007", "UNB-DATA-008"])
k7 = c.C(7, "Backup-aware retention and destruction", "Track personal and tenant data in backups through expiry, honor legal holds, and state residual backup copies in destruction certificates rather than claiming immediate deletion.",
         "administrative", "L9-runtime-monitored", ["Unbound retention policy component (not built)"], [e7], "Proposed: Privacy Lead (role not yet staffed)",
         related=["RR-UNB-TEN-016-r1", "UNB-IMM-008", "REQ-X-036", "REQ-X-038", "SOC2-032"])

a1 = c.A(1, "Backup scope, frequency, retention and location", "proposed-target-state", RAT,
    "All authoritative stores are backed up at frequencies meeting their data-class RPO: continuous write-ahead-log archiving plus daily snapshots for the ledger database, versioned object storage for issued documents, and daily backups of configuration and source repositories. Rebuildable projections, search indexes and embeddings are excluded by design and rebuilt from the journal. Backups are retained at least 35 days for operational recovery, with longer retention for financial records governed by the retention policy, and copies are kept in a second location within the tenant's residency jurisdiction. Customers may also take their own complete, verifiable export at any time.",
    "Not established.", "Configure backups with the first production-like environment; generate the inventory from configuration.",
    "Nothing.",
    "No production backups exist because no production system exists. Our design covers all authoritative data with frequencies set by data class.",
    "planned", [k1], [e1, e2], OWN, freshness="P1D", mechanism="continuous-automated", automation="full", impl="low", rec="low",
    requirements=["SOC2-015", "RR-UNB-RES-003-r2", "RR-UNB-TEN-016-r1"])
a2 = c.A(2, "Backup protection: immutability, separation, encryption and access", "proposed-target-state", RAT,
    "Backups are written to a vault in a separate cloud account with separate credentials and a compliance-mode retention lock, so no production administrator, compromised credential or AI agent can delete or alter them during retention. Backups are encrypted with keys outside production key scope, with an escrowed recovery path tested annually. Restores into production require two authorized people and are logged as tamper-evident evidence; agents cannot initiate them.",
    "Not established. SOC2-006 and UNB-DATA-008 require protected, independent backup storage.",
    "Adopt a separate backup account and retention lock from the first environment.",
    "Nothing.",
    "We plan immutable, encrypted backups held in a separate account that production administrators cannot delete. Not yet implemented.",
    "planned", [k2, k3, k4], [e3, e4], OWN, freshness="P1D", mechanism="periodic-automated", automation="high", impl="low", rec="low",
    requirements=["SOC2-006", "UNB-DATA-008", "UNB-GAP-034"], policies=["SEC-CRYPTO-001", "SEC-AUTH-001"],
    challenge={
        "customer_intent": "Make sure an attacker or rogue insider cannot destroy both production data and its backups.",
        "adverse_outcome": "Ransomware or malicious deletion leaves no recoverable copy.",
        "conventional_control_effectiveness": "Policy-based restrictions on backup deletion are routinely defeated by compromised administrator credentials; questionnaires accept 'backups are encrypted' without asking who can delete them.",
        "legally_required": "No statute for Echelon. EU DORA Article 12 requires EU financial entities to keep backups physically and logically segregated; NYDFS Part 500 as amended requires covered entities to maintain backups protected from unauthorized alteration.",
        "contractually_required": "Increasingly in cyber insurance applications and bank contracts.",
        "historical_convention": "Offsite tape rotation.",
        "architectural_elimination": "Deletion within the retention period is eliminated in scope by compliance-mode retention lock in a separate account.",
        "automatic_enforcement": "Enforced by the storage service, not by procedure.",
        "continuous_evidence": "Daily automated read of vault configuration and principals with delete permission.",
        "stronger_alternative": "Structural immutability with continuous configuration evidence instead of an annual attestation.",
        "alternative_verifiable": "Yes, configuration evidence is machine-checkable.",
        "customer_acceptance_likelihood": "Likely.",
        "invalidating_conditions": "If the separate account shares an identity provider or organization root that the attacker controls.",
        "conventional_cost": "low", "alternative_cost": "low",
        "alternative_risks": "Immutable retention complicates honoring deletion requests before expiry.",
        "supporting_arguments": ["Defeats the most common ransomware recovery failure."],
        "opposing_arguments": ["Privacy regulators may question retention of deleted personal data in locked backups."],
        "technical_effectiveness": "stronger", "institutional_acceptance": "likely"})
a3 = c.A(3, "Restore testing and integrity verification", "proposed-target-state", RAT,
    "Restores of each data class run at least quarterly into isolated environments and are verified by hash-chain or signed-checkpoint verification, record counts and per-fund trial balances, not only by job success. Missing or failed backups raise monitored control exceptions. Results are retained as evidence and summarized for customers under NDA.",
    "Not established. UNB-DATA-012 requires integrity verification that detects omitted, altered, duplicated and reordered records, including after restore.",
    "Implement integrity verification with the ledger; schedule restore tests from the first pre-production environment.",
    "Nothing.",
    "No restore tests have been performed. We plan quarterly restore tests verified against cryptographic checkpoints and trial balances.",
    "planned", [k5, k1], [e5, e2], OWN, freshness="P90D", mechanism="periodic-automated", automation="full", impl="medium", rec="low",
    requirements=["UNB-DATA-012", "UNB-TEC-STRATA-004", "SOC2-027"])
a4 = c.A(4, "Point-in-time recovery and deterministic replay", "proposed-target-state", RAT,
    "The authoritative ledger is strictly append-only; corrections are new linked records, never updates. Point-in-time recovery is available to the second within the retention window through write-ahead-log archiving, and every balance and projection can be reconstructed by deterministic replay of the journal to any prior point. Replay is side-effect free: it cannot send payments, emails or provider calls. Replay equivalence against live projections is tested monthly.",
    "Not established. ACC-MDL-002 (append-only journals), ACC-MDL-007 (idempotent posting, replay without duplicate effects) and UNB-IMM-010 (load tests for historical replay) specify the design.",
    "Build the ledger as append-only with typed separation of replay from effect dispatch.",
    "Nothing.",
    "Our ledger design is append-only so that state can be reconstructed by replaying history without re-sending payments. Not yet built or tested.",
    "planned", [k6], [e6], "Proposed: Unbound architecture owner", freshness="P30D", mechanism="periodic-automated", automation="full", impl="medium", rec="low",
    requirements=["ACC-MDL-002", "ACC-MDL-007", "UNB-IMM-010", "UNB-GAP-030"],
    challenge={
        "customer_intent": "Be able to recover data as of a specific time, for example just before an erroneous bulk change.",
        "adverse_outcome": "Erroneous changes cannot be unwound precisely; history is lost.",
        "conventional_control_effectiveness": "Point-in-time database restore recovers state but discards everything after the restore point, including legitimate later transactions, and requires manual re-entry.",
        "legally_required": "No. Record-keeping rules such as SEC Rule 17a-4 bind broker-dealer customers, not Echelon.",
        "contractually_required": "Rarely specified.",
        "historical_convention": "Nightly backups plus transaction log shipping.",
        "architectural_elimination": "Destructive overwrite of financial history is eliminated in scope by append-only design; an erroneous change is reversed with a new record rather than a restore.",
        "automatic_enforcement": "Database permissions and ledger API deny update and delete on posted entries.",
        "continuous_evidence": "Monthly replay equivalence test.",
        "stronger_alternative": "Correction by compensating entries plus replay, with database restore reserved for infrastructure loss.",
        "alternative_verifiable": "Yes.",
        "customer_acceptance_likelihood": "Likely among finance and audit buyers.",
        "invalidating_conditions": "If any authoritative state lives outside the journal, or replay depends on mutable reference data that was not versioned.",
        "conventional_cost": "low", "alternative_cost": "medium",
        "alternative_risks": "Replay time grows with history; requires snapshots and load testing.",
        "supporting_arguments": ["Preserves legitimate later transactions.", "Supports audit reconstruction."],
        "opposing_arguments": ["Append-only does not protect against infrastructure loss; backups remain necessary.", "Replay performance at large scale is unproven."],
        "technical_effectiveness": "stronger", "institutional_acceptance": "likely"})
a5 = c.A(5, "Backups, retention, legal hold and deletion", "proposed-target-state", RAT,
    "Backups honor the retention policy, including the seven-year minimum for financial records and legal holds. When personal data is deleted or a tenant exits, Echelon states which backups still contain the data and when they expire (no more than 35 days after the exit package is delivered for operational backups), and the destruction certificate lists residual copies and records retained by legal obligation. Echelon does not claim cryptographic erasure where plaintext remains in backups, logs or exports.",
    "Not established. RR-UNB-TEN-016-r1, UNB-IMM-008, REQ-X-036 and SOC2-032 define the policy.",
    "Implement retention policy engine and backup expiry tracking before production.",
    "Nothing.",
    "We plan to disclose how long data persists in backups after deletion and to issue destruction certificates listing any residual copies. Not yet implemented.",
    "planned", [k7], [e7], "Proposed: Privacy Lead (role not yet staffed)", freshness="per-event", mechanism="event-driven-automated", automation="high", impl="medium", rec="low",
    requirements=["RR-UNB-TEN-016-r1", "UNB-IMM-008", "REQ-X-036", "REQ-X-038", "SOC2-032"])

c.Q(1, "Backup scope", "What data and systems do you back up, including databases, document storage, configuration, source code and secrets?",
    ["Describe the scope of your backups."],
    "Gaps in backup scope cause unrecoverable loss.", "A store that was assumed backed up is not.",
    [R("SRC-NIST-SP800-53-R5", "CP-9"), R("SRC-ISO-27002-2022", "8.13"), R("SRC-NIST-CSF-2.0", "PR.DS-11"), R("SRC-SA-SIG"), R("SRC-CSA-CAIQ-V4"), R("SRC-EDUCAUSE-HECVAT")],
    "industry-convention", "high")
c.Q(1, "Backup frequency and retention", "How often is each type of data backed up and how long are backups kept?",
    ["What is your backup frequency and retention period?"],
    "Frequency determines possible data loss; retention determines how far back recovery reaches.", "Corruption discovered after backups containing good data expired.",
    [R("SRC-NIST-SP800-53-R5", "CP-9"), R("SRC-AICPA-TSC", "A1.2"), R("SRC-FFIEC-BCM-BOOKLET")], "industry-convention", "high")
c.Q(1, "Backup location and residency", "Where are backup copies stored, are they geographically separated from production, and do they stay within our required jurisdiction?",
    ["Are backups stored offsite and in-country?"],
    "Co-located backups fail with production; out-of-jurisdiction backups may breach residency commitments.", "Loss of both production and backup, or residency violation.",
    [R("SRC-NIST-SP800-53-R5", "CP-6"), R("SRC-GDPR", rel="informed-by"), R("SRC-EU-DORA", "Article 12")], "contractual-common", "medium", juris=["US-federal", "EU"])
c.Q(1, "SaaS and toolchain backups", "Do you back up the third-party systems you rely on to build and run the service, such as source hosting, ticketing and CI configuration?",
    ["Are your source code repositories backed up independently of the hosting provider?"],
    "Loss of source or build configuration prevents recovery and patching.", "Cannot rebuild or patch after a toolchain provider loss.",
    [R("SRC-NIST-SP800-53-R5", "CP-9"), R("SRC-SLSA", rel="informed-by")], "customer-preference", "medium", products=["all-echelon-products"])
c.Q(1, "Customer-held copy", "Can we obtain our own complete, verifiable copy of our data on a schedule we choose, so that we do not depend solely on your backups?",
    ["Can we export a full backup of our tenant?"],
    "Customer-held copies protect against vendor failure and disputes.", "Customer has no copy if the vendor fails.",
    [R("SRC-EU-DORA", "Article 28"), UNB], "customer-preference", "high", industries=FIN, juris=["US-federal", "EU"])
c.Q(2, "Backup separation", "Are backups stored in a separate account or tenancy, with separate credentials, so that compromise of production administrator access cannot reach them?",
    ["Are backups logically and physically segregated from production?"],
    "Attackers target backups first.", "Ransomware deletes backups using production credentials.",
    [R("SRC-EU-DORA", "Article 12"), R("SRC-NYDFS-PART-500", "500.16"), R("SRC-CIS-CONTROLS-V8.1")], "supervisory-guidance", "critical",
    industries=FIN, juris=["US-federal", "US-state:NY", "EU"], authority="NYDFS; EU competent authorities")
c.Q(2, "Backup immutability", "Are backups immutable for a defined period, so that no one, including your own administrators, can delete or alter them?",
    ["Do you use write-once or object-lock backups?"],
    "Mutable backups can be corrupted or destroyed.", "Silent alteration or deletion of backups.",
    [R("SRC-NIST-CSF-2.0", "PR.DS-11"), R("SRC-CIS-CONTROLS-V8.1")], "industry-convention", "critical")
c.Q(2, "Backup encryption", "Are backups encrypted at rest and in transit, and are backup encryption keys managed separately from production keys?",
    ["How are backups encrypted?"],
    "Backup media is a common source of data exposure.", "Disclosure of customer data from a backup copy.",
    [R("SRC-NIST-SP800-53-R5", "CP-9(8)"), R("SRC-PCI-DSS-4.0.1", rel="informed-by"), SCS], "industry-convention", "high")
c.Q(2, "Backup key escrow", "If the keys that encrypt your backups were lost, could you still decrypt them, and how often is that recovery path tested?",
    ["Are backup encryption keys escrowed?"],
    "Encryption without key recovery converts key loss into data loss.", "Backups exist but are permanently unreadable.",
    [R("SRC-NIST-SP800-53-R5", "SC-12"), SCS], "industry-convention", "high", disc="nda")
c.Q(2, "Restore authorization", "Who can restore data into production, is approval by a second person required, and is every restore logged?",
    ["How is access to backups controlled?"],
    "Restores can roll back or overwrite legitimate data.", "Unauthorized restore used to reverse transactions or hide activity.",
    [R("SRC-NIST-SP800-53-R5", "AC-6"), R("SRC-AICPA-TSC", "CC6.1")], "industry-convention", "high")
c.Q(2, "AI agents and backups", "Can any AI agent used in your operations read, delete or restore backups?",
    ["What access do automated agents have to backup systems?"],
    "Agents with broad operational permissions expand the attack surface for destructive actions.", "Prompt-injected or malfunctioning agent deletes or restores backups.",
    [R("SRC-OWASP-LLM-TOP10-2025", rel="informed-by"), R("SRC-OWASP-AGENTIC-AI", rel="informed-by"), SOC2D], "customer-preference", "high", products=["all-echelon-products"])
c.Q(3, "Restore testing", "How often do you test restoring from backup, what is restored, and what were the results of the most recent test?",
    ["When was your last successful restore test?"],
    "Backups that cannot be restored provide no protection.", "Backup corruption discovered only during a real incident.",
    [R("SRC-NIST-SP800-53-R5", "CP-9(1)"), R("SRC-AICPA-TSC", "A1.3"), R("SRC-NIST-CSF-2.0", "PR.DS-11"), R("SRC-FFIEC-BCM-BOOKLET")], "supervisory-guidance", "critical", authority="FFIEC member agencies")
c.Q(3, "Restored data integrity", "After a restore, how do you verify that financial records are complete and unaltered, rather than only that the restore job succeeded?",
    ["Do you validate data integrity after restoration?"],
    "A successful job can restore incomplete or corrupted data.", "Silent loss or alteration of transactions after restore.",
    [R("SRC-NIST-SP800-53-R5", "CP-9(1)"), R("SRC-AICPA-TSC", "PI1.5", rel="informed-by"), UNB], "customer-preference", "critical", industries=FIN)
c.Q(3, "Backup monitoring", "How are backup failures detected and escalated, and is a missing backup treated as an incident?",
    ["Are backup jobs monitored and alerted?"],
    "Backup jobs fail silently for long periods.", "Weeks of missing backups discovered during recovery.",
    [R("SRC-NIST-CSF-2.0", rel="informed-by"), SOC2D], "industry-convention", "medium")
c.Q(4, "Point-in-time recovery", "Can you recover our data to any point in time within the retention window, and at what granularity?",
    ["Do you support point-in-time recovery?"],
    "Customers need to recover to just before a specific error.", "Recovery only to last nightly backup loses a day of work.",
    [R("SRC-NIST-SP800-53-R5", "CP-10"), R("SRC-CSA-CCM-V4")], "customer-preference", "medium")
c.Q(4, "Journal replay", "Is your ledger append-only, and can balances and reports be reconstructed deterministically by replaying the transaction history to any prior date?",
    ["Can you rebuild account balances from transaction history?"],
    "Reconstruction from history is stronger evidence than a snapshot.", "Inability to prove how a balance was derived after a recovery.",
    [R("SRC-SEC-17A-4", rel="informed-by"), R("SRC-FASB-ASC-958", rel="informed-by"), UNB], "customer-preference", "high", industries=FIN)
c.Q(4, "Rebuildable data exclusions", "Is any data excluded from backup because it can be rebuilt, and how do you prove that the rebuild works and how long it takes?",
    ["Are derived data stores backed up?"],
    "Untested rebuild paths turn exclusions into data loss.", "Search, statements or projections unavailable for days after recovery.",
    [UNB], "customer-preference", "medium")
c.Q(4, "Replay side effects", "When you replay or reprocess historical transactions, how do you guarantee that payments, notifications or external calls are not triggered again?",
    ["Can reprocessing cause duplicate payments or emails?"],
    "Replays are a known source of duplicate external effects.", "Duplicate grant payments or donor notices during recovery.",
    [R("SRC-NACHA-RULES", rel="informed-by"), UNB], "customer-preference", "critical", industries=["donor-advised-funds", "financial-services"])
c.Q(5, "Deletion and backups", "When we or a donor request deletion of personal data, how long does it remain in backups, and will you tell us when it is gone?",
    ["How do you handle data subject deletion requests with respect to backups?"],
    "Privacy laws and contracts require disclosure of residual copies.", "Personal data retained without disclosure.",
    [R("SRC-GDPR", "Art. 17", rel="informed-by"), R("SRC-CCPA-CPRA", rel="informed-by"), R("SRC-EDPB-GL-07-2020", rel="informed-by"), UNB], "legal-regulatory", "high",
    juris=["US-states", "EU"], authority="EU supervisory authorities; California Privacy Protection Agency",
    note="Deletion rights bind the controller (the sponsor); Echelon as processor must support them and disclose backup persistence.")
c.Q(5, "Legal hold and financial retention", "Do backups and retention rules preserve financial records for required periods and respect legal holds that we place?",
    ["How do backups interact with record retention requirements?"],
    "Financial records must survive for statutory periods.", "Records needed for audit or litigation destroyed.",
    [R("SRC-SEC-17A-4", rel="informed-by"), R("SRC-IRC-170", rel="informed-by"), UNB], "contractual-common", "high", industries=FIN)
c.Q(5, "Cryptographic erasure claims", "If you rely on destroying encryption keys to delete our data, does that cover backups, logs and exports, and what plaintext copies could remain?",
    ["Do you use crypto-shredding for tenant deletion?"],
    "Crypto-shredding claims are often overstated.", "Customer believes data destroyed while plaintext copies remain.",
    [R("SRC-NIST-SP800-88"), UNB], "customer-preference", "medium")
c.write()
