from lib import *

C = Category("ASM")
STRATA = "strata@c6a384ec"

C.au(1, "Infrastructure, cloud resource and endpoint inventory",
     "Infrastructure and endpoint inventory",
     "The customer needs the vendor to know every system and device that can hold or reach customer data, because unknown assets are unpatched and unmonitored.",
     "unknown",
     "No production infrastructure exists for Unbound and no hosting provider is selected. No inventory of Echelon corporate endpoints or cloud accounts was located.",
     "Echelon derives its infrastructure inventory automatically from infrastructure-as-code and cloud provider APIs, reconciles the two daily, and treats any resource present in the cloud but absent from code as an unauthorized-asset finding. Every resource carries owner, environment, data classification and, where it stores tenant data, the tenant or sponsor cell it serves. Workforce endpoints are enrolled in device management before receiving access; unmanaged devices cannot obtain workforce sessions.",
     "Unknown; no evidence located. No production environment exists.",
     "Select hosting and device management; generate the inventory from code and provider APIs from the first environment.",
     "Nothing.",
     "Echelon has no production infrastructure yet. An automatically generated and reconciled infrastructure and endpoint inventory is planned from the first environment.",
     "not-available",
     controls=[1], evrs=[1],
     reqs=["SOC2-013", "UNB-TEN-009"],
     fresh="P1D", mech="continuous-automated", auto="full", impl="low", rec="low",
     owner="Unassigned; proposed Engineering Lead",
     residual=["Resources created outside the provider APIs the reconciler reads (for example a personal SaaS account) are not detected."],
     oq=["Which cloud and managed PostgreSQL provider will host Unbound (CNV-ARC-001 requires managed PostgreSQL; provider not selected)?"])

C.au(2, "Software, dependency and AI component inventory",
     "Software and component inventory",
     "The customer needs to know what software, open-source components, internal frameworks and AI models make up the service so that vulnerabilities, licenses and end-of-life risks can be managed.",
     "proposed-target-state",
     "SEC-SUPPLY-001 (proposed) requires locked versions, provenance and SBOM; CNV-GOV-009 requires an SBOM license check. Praxis offers an inventory command for Echelon tools. No product SBOM exists because no product build exists.",
     "Every Echelon release produces a signed SBOM in SPDX or CycloneDX listing all components with versions, hashes, licenses and provenance, including Echelon's own frameworks (for example Strata, Limen, Forma, Folio) and their PolyForm Noncommercial or commercial license status. The SBOM is extended with an AI component inventory: models and versions, providers, prompts and tool definitions used by product agents. Unsupported runtimes and database majors are flagged automatically; only allowlisted, locked dependencies can enter a build.",
     "No product SBOM exists. Praxis (praxis@12bf9951) provides an `echelon inventory` command that distinguishes native Echelon tools, repository-installed lifecycle components and installed @echelon-foundry npm packages for a repository; this is a development-tool inventory, not a product SBOM.",
     "Generate SBOMs at build using standard tooling, attach to releases, and fail builds on unapproved or unlicensed components.",
     "The Praxis inventory command and the proposed SEC-SUPPLY-001 rule text can be shown. No SBOM.",
     "Echelon plans to publish a signed SBOM with every release, including its own frameworks and AI components. Today only a development-tool inventory exists in Echelon repositories.",
     "planned",
     controls=[2, 3], evrs=[2, 3],
     policies=["SEC-SUPPLY-001"],
     reqs=["CNV-GOV-009", "SOC2-016"],
     fresh="per-event", mech="event-driven-automated", auto="full", impl="low", rec="low",
     owner="Unassigned; proposed Engineering Lead",
     residual=["SBOMs describe declared components; vendored or dynamically loaded code may be missed.",
               "AI model behavior can change behind a stable model identifier at some providers."],
     oq=["Will Echelon components used in Unbound be covered by an executed commercial license before launch (CNV-GOV-007, CNV-GOV-009)?"])

C.au(3, "Data inventory, data flows and isolation map",
     "Data inventory and flows",
     "The customer needs to know where its data and its donors' and clients' personal and financial data live, flow and are copied, including secondary stores and AI artifacts.",
     "proposed-target-state",
     "Unbound requirements call for an isolation map per data class (UNB-RCN-PLT-001), a SharedStoreRegister (CNV-TEN-001) and isolation of secondary stores including embeddings and logs (UNB-TEN-009). None is built.",
     "Echelon maintains a machine-readable data inventory generated from the declared database schema and service contracts rather than maintained by hand: each data class has classification, legal basis, owner, isolation key (sponsor tenant or partner), retention rule and permitted cross-partner sharing. The inventory covers primary tables, event streams, caches, queues, search indexes, object storage, logs, telemetry, backups, non-production environments, prompts, embeddings and evaluation datasets. A release fails if a new store or column lacks an inventory entry (CNV-TEN-001 AC-2 and AC-3). Data flow diagrams are generated from the same source.",
     "No data inventory exists. Requirements specify it. Strata (" + STRATA + ") compiles declared schema into an artifact that could serve as the relational source of truth, but no Unbound schema exists.",
     "Implement the isolation map and SharedStoreRegister as schema-checked registers; generate flow diagrams.",
     "Requirement text only.",
     "Echelon plans a data inventory generated from its declared schema and service contracts, covering secondary stores and AI artifacts, with each data class mapped to its tenant isolation key. It does not exist yet.",
     "planned",
     controls=[4], evrs=[4],
     reqs=["UNB-RCN-PLT-001", "CNV-TEN-001", "UNB-TEN-009", "UNB-TEN-007", "SOC2-014"],
     fresh="per-event", mech="event-driven-automated", auto="high", impl="medium", rec="low",
     owner="Unassigned; proposed data owner (Unbound architecture)",
     residual=["Data copied by people (spreadsheets, email attachments, support tickets) is outside schema-derived inventories."],
     challenge={
         "customer_intent": "Be able to answer where our data is at any time, for breach scoping, privacy rights and examiner questions.",
         "adverse_outcome": "A breach or privacy request cannot be scoped because data copies are unknown.",
         "conventional_control_effectiveness": "Manually maintained data inventories and diagrams are typically incomplete and stale within months of creation.",
         "legally_required": "FTC Safeguards Rule 16 CFR 314.4(c)(2) and NYDFS 500.13 require covered entities to identify and manage data and systems; GDPR Article 30 records apply to EU processing. These bind customers, and in some cases Echelon if it is itself covered; they flow to vendors contractually.",
         "contractually_required": "Common in data protection addenda and bank questionnaires.",
         "historical_convention": "Spreadsheet data inventory plus annual review.",
         "architectural_elimination": "Not eliminable, but staleness can be eliminated in scope: if every persistent store must be declared to deploy, the inventory cannot omit a store that the deployment created.",
         "automatic_enforcement": "Release check fails on undeclared stores or columns (CNV-TEN-001).",
         "continuous_evidence": "Inventory regenerated on every release with commit hash.",
         "stronger_alternative": "Schema-derived inventory with a deploy gate, plus periodic discovery scans to catch data outside declared stores.",
         "alternative_verifiable": "Yes; an assessor can compare the generated inventory with the deployed schema and cloud resource list.",
         "customer_acceptance_likelihood": "Likely, provided a human-readable inventory and diagrams are also produced.",
         "invalidating_conditions": "Data stored outside declared stores (manual exports, third-party SaaS) is invisible to the gate.",
         "conventional_cost": "Recurring manual effort.",
         "alternative_cost": "Upfront engineering; low recurring.",
         "alternative_risks": "False confidence about completeness.",
         "supporting_arguments": ["Generated inventories cannot drift from deployed schema."],
         "opposing_arguments": ["Unstructured copies made by people are the usual breach-scoping problem and are not covered."],
         "technical_effectiveness": "stronger",
         "institutional_acceptance": "likely"})

C.au(4, "Third-party service and external attack-surface inventory",
     "Service and attack-surface inventory",
     "The customer needs the vendor to know every external service that supports delivery or receives data, and every endpoint exposed to the internet.",
     "unknown",
     "No production service and no subservice organizations are selected. SOC2-013 requires a critical service inventory. No inventory of corporate SaaS tools was located.",
     "Echelon maintains a service inventory listing each third-party and subservice organization, the data classes it receives, the tenants affected, criticality, contract and assurance status, and a fallback. New SaaS tools, including AI assistants, require approval before receiving company or customer data. An external attack-surface inventory of domains, certificates and endpoints is generated from DNS and deployment configuration and monitored for unexpected exposure.",
     "Unknown; no evidence located.",
     "Create the service inventory alongside vendor risk management; automate attack-surface inventory from deployment configuration.",
     "Nothing.",
     "Echelon has not yet selected production service providers. A service inventory and an external attack-surface inventory are planned.",
     "not-available",
     controls=[5], evrs=[5],
     reqs=["SOC2-013", "SOC2-022", "UNB-TEN-007"],
     fresh="P30D", mech="periodic-automated", auto="partial", impl="low", rec="low",
     owner="Unassigned; proposed Security Lead",
     residual=["Staff adoption of free AI tools can bypass procurement."])

C.au(5, "Secure configuration baselines and drift detection, including database privileges",
     "Configuration baselines",
     "The customer needs systems configured securely from a known baseline and kept there, because misconfiguration is a leading cause of cloud data exposure.",
     "proposed-target-state",
     "Strata exists as a pilot declarative PostgreSQL schema tool that compares tables, grants and row-level security policies for drift and discloses what it could not compare. CNV-ARC-004 selects Strata for declarative schema governance. Strata is not operated against any Unbound database; host and cloud baselines are not defined.",
     "All infrastructure, container, cloud service and database configuration is declared in version control and deployed only through reviewed pipelines. Baselines derive from CIS Benchmarks where applicable, with documented deviations. Drift is detected continuously and either reverted automatically or raised as an incident. For PostgreSQL, Strata compiles declared schema, grants and row-level security policies into an artifact, diffs it against the live database before every deployment, and reports items it could not compare as not-compared or unverifiable rather than as matches, so an unverifiable configuration is never reported as compliant.",
     "Strata (" + STRATA + ") is a pilot tool tested against PostgreSQL 16: it creates and compares grants and RLS policies per its README coverage table and refuses deployment across PostgreSQL major versions. It has not been run against an Unbound database or a large migration history. No host or cloud baselines exist.",
     "Adopt Strata for schema, grant and policy baselines; adopt infrastructure-as-code with CIS-derived baselines; run drift detection continuously.",
     "Strata's source, tests and coverage table at commit c6a384ec can be shown as a tool capability. Nothing shows a configured Echelon production baseline.",
     "Echelon's own Strata tool can declare PostgreSQL schema, grants and row-level security policies and detect drift, disclosing anything it could not verify. It has not yet been used on a production Unbound database. Host and cloud configuration baselines are planned.",
     "planned",
     controls=[6, 7], evrs=[6, 7],
     policies=["SEC-DB-001"],
     reqs=["CNV-ARC-004", "UNB-TEC-STRATA-004", "SOC2-011"],
     fresh="P1D", mech="continuous-automated", auto="full", impl="medium", rec="low",
     owner="Unassigned; proposed Engineering Lead",
     residual=["Strata supports only PostgreSQL 16 and is pilot status; managed-provider defaults outside the declared schema (for example provider-created roles) may not be modeled.",
               "Configuration items not modeled by any tool remain manual."],
     challenge={
         "customer_intent": "Be confident that systems are hardened and stay hardened.",
         "adverse_outcome": "Misconfigured storage, excessive database grants or disabled row-level security expose data.",
         "conventional_control_effectiveness": "Periodic manual configuration reviews and scanner snapshots catch drift late and miss items the scanner does not model while reporting them as passing.",
         "legally_required": "Not specifically required by statute for a vendor; PCI DSS requires configuration standards for in-scope systems, which Unbound is not expected to have.",
         "contractually_required": "Common questionnaire item; rarely a contract term.",
         "historical_convention": "Hardening checklists, annual review, configuration scans.",
         "architectural_elimination": "Manual production changes can be eliminated by removing interactive administrative paths (CNV-PLT-010 makes database admin roles break-glass only).",
         "automatic_enforcement": "Declarative deployment with pre-deploy diff and fail-closed handling of not-compared items.",
         "continuous_evidence": "Each deployment yields a diff report with explicit matches, differs, not-compared and unverifiable states.",
         "stronger_alternative": "Declarative configuration with honest coverage disclosure, as Strata implements for PostgreSQL.",
         "alternative_verifiable": "Yes; the diff artifact and coverage table are inspectable.",
         "customer_acceptance_likelihood": "Likely for the concept; customers will still ask for CIS benchmark scan output.",
         "invalidating_conditions": "If administrators retain interactive write access, or if the tool silently fails to compare an object class.",
         "conventional_cost": "Recurring review effort and scanner licenses.",
         "alternative_cost": "Engineering investment already being made in Strata; pilot maturity risk.",
         "alternative_risks": "A single tool defect could mask drift across all tenants; Strata's own history records five such defects found and fixed during development.",
         "supporting_arguments": ["Six-state reporting prevents the common failure of treating not-checked as passing."],
         "opposing_arguments": ["Strata is pilot status and has not been independently validated.", "Only PostgreSQL 16 is supported."],
         "technical_effectiveness": "stronger",
         "institutional_acceptance": "uncertain"})

C.au(6, "Asset ownership, classification and secure decommissioning",
     "Asset lifecycle",
     "The customer needs each asset to have an accountable owner and classification, and needs data destroyed verifiably when assets or tenants are retired.",
     "proposed-target-state",
     "UNB-TEN-016 (refined by RR-UNB-TEN-016-r1) specifies cryptographic erasure under dual control and a destruction certificate on sponsor exit. No asset register or decommissioning procedure exists.",
     "Every inventoried asset has an owner, classification and lifecycle state. Decommissioning follows a recorded plan: credentials and certificates revoked, data destroyed by tenant-scoped key destruction under dual control or by media sanitization consistent with NIST SP 800-88 on provider-managed media (relying on provider attestations), and a destruction certificate issued that states what persists (for example immutable backups until expiry). Orphaned resources are found by daily reconciliation against provider billing and APIs.",
     "Unknown for assets. The tenant exit and cryptographic erasure requirement exists in Unbound requirements.",
     "Implement owner and classification fields in the generated inventory; implement tenant key destruction and certificates.",
     "Requirement text only.",
     "Echelon plans owner and classification for every asset and verifiable destruction on decommissioning and tenant exit, including a destruction certificate stating what persists. None is operating today.",
     "planned",
     controls=[8], evrs=[8],
     reqs=["UNB-TEN-016", "RR-UNB-TEN-016-r1", "UNB-TEN-011", "OPS-021"],
     fresh="per-event", mech="event-driven-automated", auto="high", impl="medium", rec="low",
     owner="Unassigned; proposed Engineering Lead",
     residual=["Physical media sanitization on managed cloud services relies on the provider's attestation."])

# ---------------- Controls ----------------
C.ctl(1, "Code-derived infrastructure inventory reconciled to provider APIs",
      "Detect any cloud resource or endpoint not declared in infrastructure-as-code or device management, and record owner, environment, classification and tenant cell for each.",
      "detective-automated", "L9-runtime-monitored", ["not yet assigned"], evrs=[1],
      refs=[d("SRC-CIS-CONTROLS-V8.1", "1.1"), d("SRC-NIST-SP800-53-R5", "CM-8"), d("SRC-NIST-CSF-2.0", "ID.AM-01"), d("SRC-NYDFS-PART-500", "500.13", "informed-by"), s("SRC-PCI-DSS-4.0.1", "Req 12.5.1", "informed-by")])
C.ctl(2, "Signed SBOM per release including Echelon frameworks and AI components",
      "Produce a complete, signed component inventory for every release with versions, hashes, licenses and provenance, extended with AI models, prompts and tools.",
      "preventive-gate", "L5-build-release-gate", ["not yet assigned (SBOM generator)", "Praxis (proposed release gate)"], evrs=[2],
      policies=["SEC-SUPPLY-001"], related=["CNV-GOV-009"],
      refs=[d("SRC-NTIA-SBOM-MIN"), s("SRC-CYCLONEDX", rel="informed-by"), s("SRC-SPDX", rel="informed-by"), d("SRC-NIST-CSF-2.0", "ID.AM-02"), s("SRC-OWASP-LLM-TOP10-2025", "LLM03:2025", "informed-by")])
C.ctl(3, "Dependency allowlist and end-of-life detection",
      "Prevent unapproved, unlicensed or unsupported components (including unsupported runtimes and PostgreSQL majors) from entering a build.",
      "preventive-gate", "L5-build-release-gate", ["not yet assigned", "Strata (refuses deployment across PostgreSQL major versions)"], evrs=[3],
      policies=["SEC-SUPPLY-001"], related=["CNV-GOV-009", "CNV-ARC-004"],
      refs=[s("SRC-CIS-CONTROLS-V8.1", "2.2"), s("SRC-NIST-SP800-53-R5", "CM-7"), s("SRC-OPENSSF-S2C2F", rel="informed-by")])
C.ctl(4, "Schema-checked data inventory and SharedStoreRegister",
      "Fail a release when a persistent store, cross-tenant store or column is deployed without an inventory entry naming classification, isolation key and sharing rule.",
      "preventive-gate", "L5-build-release-gate", ["not yet assigned", "Strata (candidate source of declared relational schema)"], evrs=[4],
      related=["CNV-TEN-001", "UNB-RCN-PLT-001", "UNB-CTRL-008"],
      refs=[d("SRC-NIST-CSF-2.0", "ID.AM-07"), d("SRC-FTC-SAFEGUARDS-RULE", "314.4(c)(2)", "informed-by"), s("SRC-NIST-SP800-53-R5", "PM-5(1)"), s("SRC-GDPR", "Art. 30", "informed-by")],
      residual=["Does not cover unstructured copies outside declared stores."])
C.ctl(5, "Third-party service register and attack-surface monitoring",
      "Maintain a register of third-party services with data received and criticality, require approval of new SaaS and AI tools, and monitor external exposure for unexpected endpoints.",
      "detective-automated", "L9-runtime-monitored", ["not yet assigned"], evrs=[5],
      related=["SOC2-013"],
      refs=[d("SRC-NIST-CSF-2.0", "ID.AM-04"), s("SRC-ISO-27002-2022", "5.23"), s("SRC-CIS-CONTROLS-V8.1", "2.1")])
C.ctl(6, "Declarative database schema, grants and RLS with pre-deploy diff",
      "Ensure PostgreSQL schema, privileges and row-level security policies are declared in version control and compared to the live database before every deployment, with not-compared and unverifiable items disclosed and treated as failures for mandatory objects.",
      "preventive-gate", "L5-build-release-gate", ["Strata (pilot; PostgreSQL 16)"], evrs=[6],
      policies=["SEC-DB-001", "SEC-AUTH-001"], related=["CNV-ARC-004", "UNB-TEC-STRATA-004"],
      refs=[d("SRC-NIST-SP800-53-R5", "CM-2"), d("SRC-NIST-SP800-53-R5", "CM-6"), d("SRC-ISO-27002-2022", "8.9"), s("SRC-CIS-BENCHMARKS", rel="informed-by")],
      residual=["Strata is pilot status and not independently validated.", "Objects Strata reports as not-modelled require separate review."],
      notes="Strata's README states RLS policies are created and compared and are never dropped automatically; grants are compared per grantee and a grantee the project never names is untouched, which means undeclared roles' privileges are not reported unless separately checked.")
C.ctl(7, "Infrastructure-as-code with CIS-derived baselines and continuous drift detection",
      "Ensure hosts, containers and cloud services are configured from versioned baselines derived from CIS Benchmarks, with drift detected and reverted or escalated.",
      "detective-automated", "L6-automated-analysis", ["not yet assigned"], evrs=[7],
      related=["SOC2-011"],
      refs=[d("SRC-CIS-CONTROLS-V8.1", "4.1"), d("SRC-CIS-BENCHMARKS"), d("SRC-NIST-SP800-53-R5", "CM-6"), d("SRC-NIST-CSF-2.0", "PR.PS-01"), s("SRC-AICPA-TSC", "CC7.1")])
C.ctl(8, "Asset lifecycle with verifiable tenant-scoped destruction",
      "Ensure retired assets and exiting tenants have credentials revoked, data destroyed by tenant-key destruction under dual control or provider-attested sanitization, and a destruction certificate that states what persists.",
      "corrective", "L10-external-or-manual", ["not yet assigned"], evrs=[8],
      related=["UNB-TEN-016", "RR-UNB-TEN-016-r1"],
      refs=[d("SRC-NIST-SP800-88"), d("SRC-NIST-CSF-2.0", "ID.AM-08"), s("SRC-ISO-27017", "CLD.8.1.5", "informed-by")])

# ---------------- Evidence ----------------
C.evr(1, "Daily infrastructure inventory reconciliation report",
      "Generated list of resources from code and provider APIs, with unmatched resources flagged and their disposition.",
      "not yet assigned", "periodic-automated", "P1D", fmt="JSON Lines", prov=["generation time", "provider account", "code commit"], disc="customer-only")
C.evr(2, "Release SBOM",
      "SPDX or CycloneDX SBOM for each release with AI component extension, attached to the release and signed.",
      "not yet assigned (SBOM generator in CI)", "event-driven-automated", "per-event", fmt="SPDX or CycloneDX JSON",
      prov=["release version", "artifact digest", "generator version", "commit hash"], signing="Signed with release signing key (proposed)", disc="customer-only")
C.evr(3, "Dependency gate results",
      "Per-build record of blocked components, license findings and end-of-life findings.",
      "not yet assigned", "event-driven-automated", "per-event", fmt="JSON", prov=["commit hash", "rule version"], disc="internal")
C.evr(4, "Generated data inventory and isolation map",
      "Per-release export of data classes, stores, classification, isolation key, sharing rule and retention, with a release-check result.",
      "not yet assigned", "event-driven-automated", "per-event", fmt="JSON plus generated diagram", prov=["release version", "schema artifact hash"], disc="nda")
C.evr(5, "Third-party service register export",
      "List of third-party and subservice organizations with data classes, criticality and assurance status.",
      "not yet assigned", "periodic-manual", "P90D", fmt="Spreadsheet or JSON", prov=["review date", "reviewer"], disc="nda")
C.evr(6, "Strata deployment diff report",
      "Pre-deployment comparison of declared schema, grants and RLS policies to the live database with matches, differs, not-compared, not-modelled, unverifiable and absent states.",
      "Strata (pilot tool; exists, not operated for production)", "event-driven-automated", "per-event", fmt="Strata report output",
      prov=["artifact hash", "target database identifier", "PostgreSQL version", "Strata version"], disc="customer-only",
      notes="Tool exists at strata@c6a384ec; evidence would be produced only once Unbound databases exist.")
C.evr(7, "Configuration drift findings",
      "Continuous drift detection results for hosts, containers and cloud services with remediation records.",
      "not yet assigned", "continuous-automated", "P1D", fmt="JSON", prov=["resource id", "baseline version", "detection time"], disc="customer-only")
C.evr(8, "Destruction certificate",
      "Certificate for decommissioned assets or exiting tenants stating what was destroyed, by what method, under whose dual control, and what persists with expiry dates.",
      "not yet assigned", "event-driven-automated", "per-event", fmt="Signed PDF and JSON", prov=["tenant id", "key ids destroyed", "approvers", "legal holds"],
      signing="Signed (proposed)", disc="customer-only")

# ---------------- Questions ----------------
C.q(1, "Do you maintain a complete inventory of the hardware, virtual machines, containers, managed services and cloud accounts that store or process customer data, with an owner for each?",
    "Unknown assets are unpatched, unmonitored and excluded from incident scoping.",
    [d("SRC-CIS-CONTROLS-V8.1", "1.1"), d("SRC-NIST-SP800-53-R5", "CM-8"), d("SRC-NIST-CSF-2.0", "ID.AM-01"), d("SRC-NYDFS-PART-500", "500.13", "informed-by"), s("SRC-SA-SIG"), s("SRC-CSA-CAIQ-V4", "UEM domain")],
    cls="contractual-common", imp="high", ind=ALL, jur=GLOBAL, prod=ORGALL,
    alts=["Describe your asset management program.", "Is there an inventory of all information assets?"])
C.q(1, "How is your cloud resource inventory generated and kept current, and how quickly does a newly created resource appear in it?",
    "Manually maintained inventories lag reality, especially in automated or agent-driven environments that create resources quickly.",
    [s("SRC-CIS-CONTROLS-V8.1", "1.1"), s("SRC-NIST-SP800-53-R5", "CM-8(1)"), s("SRC-ISO-27017", rel="informed-by")],
    cls="industry-convention", imp="medium", ind=ENT, jur=GLOBAL, prod=ORGALL)
C.q(1, "How do you detect unauthorized or unmanaged assets, such as cloud accounts, databases or storage created outside your approved process?",
    "Shadow infrastructure holds customer data without controls.",
    [d("SRC-CIS-CONTROLS-V8.1", "1.2"), s("SRC-NIST-SP800-53-R5", "CM-8(3)"), s("SRC-AICPA-TSC", "CC7.1")],
    cls="industry-convention", imp="medium", ind=ALL, jur=GLOBAL, prod=ORGALL)
C.q(1, "Are laptops and other devices used by staff and contractors to access your systems inventoried and centrally managed, and can unmanaged or personal devices access customer data?",
    "An unmanaged or compromised personal device becomes an access path to customer data.",
    [s("SRC-CIS-CONTROLS-V8.1", "1.1"), s("SRC-NIST-SP800-53-R5", "AC-19"), s("SRC-ISO-27002-2022", "8.1"), s("SRC-VSA-CORE")],
    cls="contractual-common", imp="high", ind=ALL, jur=GLOBAL, prod=ORG)

C.q(2, "Can you provide a software bill of materials for your product in SPDX or CycloneDX format, and how often is it updated?",
    "The customer cannot assess exposure to a newly disclosed vulnerable component.",
    [d("SRC-NTIA-SBOM-MIN"), s("SRC-CISA-SBOM-MIN", rel="informed-by"), s("SRC-OMB-M-22-18", rel="informed-by"), d("SRC-NIST-CSF-2.0", "ID.AM-02"), s("SRC-CYCLONEDX"), s("SRC-SPDX")],
    cls="customer-preference", imp="high", ind=ENT + ["public-sector"], jur=USF, prod=ALLP,
    note="OMB M-22-18 applies to federal agencies acquiring software; for private-sector customers an SBOM request is a customer preference.",
    alts=["Do you maintain an inventory of third-party and open-source software components in your product?"])
C.q(2, "Do your inventories include the internal frameworks and tools you build yourselves, with their versions in each release and their license terms for commercial use?",
    "Vendor-internal components escape vulnerability and license management, or are licensed in a way that does not permit the customer's commercial use.",
    [e("SRC-ECH-UNB-BASELINE", "CNV-GOV-009"), e("SRC-ECH-SCS-0.1", "SEC-SUPPLY-001"), s("SRC-OPENSSF-S2C2F", rel="informed-by")],
    cls="echelon-internal", imp="high", ind=ENT, jur=GLOBAL, prod=ALLP,
    oq=["Which Echelon components in the Unbound build are under PolyForm Noncommercial terms and what commercial license will cover them?"])
C.q(2, "How do you prevent unapproved software or dependencies from being introduced into production builds?",
    "A malicious or vulnerable package enters the product through an uncontrolled dependency change.",
    [e("SRC-ECH-SCS-0.1", "SEC-SUPPLY-001"), s("SRC-CIS-CONTROLS-V8.1", "2.5"), s("SRC-NIST-SP800-53-R5", "CM-7(5)"), s("SRC-SLSA", rel="informed-by")],
    cls="industry-convention", imp="high", ind=ENT, jur=GLOBAL, prod=ALLP)
C.q(2, "Do you inventory the AI models, model versions, providers, prompts and agent tools used in your product and in your engineering process?",
    "Model or prompt changes alter product behavior or data handling without review; a compromised model or tool is not traceable.",
    [d("SRC-OWASP-LLM-TOP10-2025", "LLM03:2025", "informed-by"), s("SRC-NIST-AI-600-1", rel="informed-by"), s("SRC-CSA-AICM", rel="informed-by"), e("SRC-ECH-UNB-BASELINE", "AIN-027")],
    cls="customer-preference", imp="medium", ind=ALL, jur=GLOBAL, prod=ALLP)
C.q(2, "How do you identify and plan replacement of end-of-life or unsupported components, such as runtimes, frameworks and database major versions?",
    "Unsupported components stop receiving security fixes.",
    [d("SRC-CIS-CONTROLS-V8.1", "2.2"), s("SRC-NIST-SP800-53-R5", "SA-22"), e("SRC-ECH-UNB-BASELINE", "CNV-ARC-004")],
    cls="industry-convention", imp="medium", ind=ALL, jur=GLOBAL, prod=ALLP)

C.q(3, "Do you maintain a data inventory showing where customer, donor, advisor and client personal and financial data is stored, including backups, logs, caches and non-production copies?",
    "Data in unexpected locations is unprotected and is missed in breach scoping and deletion.",
    [d("SRC-NIST-CSF-2.0", "ID.AM-07"), d("SRC-FTC-SAFEGUARDS-RULE", "314.4(c)(2)", "informed-by"), s("SRC-NIST-SP800-53-R5", "PM-5(1)"), s("SRC-CIS-CONTROLS-V8.1", "3.2"), s("SRC-GDPR", "Art. 30", "informed-by"), s("SRC-SA-SIG")],
    cls="contractual-common", imp="critical", ind=ALL, jur=GLOBAL,
    alts=["Provide your data inventory and data classification for the service.", "Where is our data stored, and in which locations and systems?"])
C.q(3, "Can you provide data flow diagrams showing every system, location and third party that receives our data?",
    "Undisclosed onward transfers of customer data.",
    [d("SRC-NIST-CSF-2.0", "ID.AM-03"), s("SRC-AICPA-TSC", "CC2.3", "informed-by"), s("SRC-EDUCAUSE-HECVAT"), s("SRC-GDPR", rel="informed-by")],
    cls="contractual-common", imp="high", ind=ALL, jur=GLOBAL, disc="nda")
C.q(3, "For each type of data you hold, what is its tenant isolation key (sponsor or partner), and may it be shared across partners serving the same sponsor?",
    "Data classes without a defined isolation key are shared across partners or sponsors by default.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-RCN-PLT-001"), e("SRC-ECH-UNB-BASELINE", "CNV-TEN-001"), s("SRC-ISO-27018", rel="informed-by")],
    cls="echelon-internal", imp="high", ind=DAF + ["banking"], jur=USF)
C.q(3, "Is your data inventory generated from the deployed schema and service definitions, or maintained manually, and how do you prove it is complete?",
    "A manually maintained inventory silently omits newly added stores or fields.",
    [e("SRC-ECH-UNB-BASELINE", "CNV-TEN-001"), s("SRC-NIST-CSF-2.0", "ID.AM-07")],
    cls="customer-preference", imp="medium", ind=FS, jur=USF)
C.q(3, "Does your data inventory include AI artifacts derived from our data, such as prompts, retrieval indexes, embeddings, model evaluation datasets and agent memory?",
    "Derived AI artifacts retain and expose customer data after the source is deleted.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-TEN-009"), d("SRC-OWASP-LLM-TOP10-2025", "LLM08:2025", "informed-by"), s("SRC-NIST-AI-600-1", rel="informed-by")],
    cls="customer-preference", imp="high", ind=ALL, jur=GLOBAL)

C.q(4, "Do you maintain an inventory of third-party services and subservice organizations that support your service, including the data each receives and whether it is critical to delivery?",
    "Fourth-party risk is unknown to the customer.",
    [d("SRC-NIST-CSF-2.0", "ID.AM-04"), e("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-013"), s("SRC-INTERAGENCY-TPRM-2023", rel="informed-by"), s("SRC-AICPA-SOC2-GUIDE", rel="informed-by"), s("SRC-SA-SIG")],
    cls="supervisory-guidance", imp="high", ind=BANK + WM, jur=USF, prod=ORGALL, reg="Customer's primary regulator",
    alts=["List all subcontractors and subprocessors with access to our data."])
C.q(4, "How do you approve new software-as-a-service tools, including AI assistants, before staff connect them to company or customer data?",
    "Staff paste customer data into unapproved SaaS or AI tools.",
    [s("SRC-NIST-SP800-53-R5", "CM-11"), s("SRC-ISO-27002-2022", "5.23"), s("SRC-NIST-AI-600-1", rel="informed-by")],
    cls="customer-preference", imp="medium", ind=ALL, jur=GLOBAL, prod=ORG)
C.q(4, "Do you maintain and monitor an inventory of your internet-facing domains, endpoints and certificates for the service?",
    "Forgotten endpoints or expired or unmanaged certificates create exposure or outages.",
    [s("SRC-CIS-CONTROLS-V8.1"), s("SRC-NIST-SP800-53-R5", "CM-8"), s("SRC-MITRE-ATTACK", rel="informed-by")],
    cls="industry-convention", imp="medium", ind=ENT, jur=GLOBAL, prod=ALLP)

C.q(5, "Do you maintain documented secure configuration baselines for operating systems, containers, cloud services and databases, and on what standard are they based?",
    "Default or inconsistent configurations leave exploitable weaknesses.",
    [d("SRC-CIS-CONTROLS-V8.1", "4.1"), d("SRC-NIST-SP800-53-R5", "CM-2"), d("SRC-NIST-SP800-53-R5", "CM-6"), d("SRC-ISO-27002-2022", "8.9"), s("SRC-CIS-BENCHMARKS"), s("SRC-SA-SIG"), s("SRC-CSA-CAIQ-V4", "CCC domain")],
    cls="contractual-common", imp="high", ind=ALL, jur=GLOBAL, prod=ALLP,
    alts=["Do you harden systems according to CIS Benchmarks or vendor guidance?"])
C.q(5, "How is configuration drift from your baselines detected, how quickly, and is it corrected automatically?",
    "Configuration weakens over time through manual changes.",
    [d("SRC-NIST-SP800-53-R5", "CM-6"), s("SRC-NIST-SP800-53-R5", "CM-3"), s("SRC-AICPA-TSC", "CC7.1"), d("SRC-NIST-CSF-2.0", "PR.PS-01")],
    cls="industry-convention", imp="medium", ind=ALL, jur=GLOBAL, prod=ALLP)
C.q(5, "Are database objects, privileges, grants and row-level security policies declared in version control and compared to the live database before each deployment?",
    "Excess database privileges or altered security policies persist unnoticed and bypass application-level controls.",
    [e("SRC-ECH-UNB-BASELINE", "CNV-ARC-004"), e("SRC-ECH-SCS-0.1", "SEC-DB-001"), s("SRC-NIST-SP800-53-R5", "CM-2"), s("SRC-CIS-BENCHMARKS", rel="informed-by")],
    cls="customer-preference", imp="high", ind=FS, jur=USF)
C.q(5, "When your configuration or compliance tooling cannot check an item, does it report that item as unverified, or does it report it as compliant?",
    "Scanners and drift tools report items they did not examine as passing, producing false assurance.",
    [s("SRC-NIST-SP800-53-R5", "CA-7"), s("SRC-SAST-ACADEMIC-EVALS", rel="informed-by"), e("SRC-ECH-SCS-0.1")],
    cls="customer-preference", imp="medium", ind=ENT, jur=GLOBAL, prod=ALLP)
C.q(5, "Can administrators change production configuration directly, outside version-controlled and reviewed pipelines, and how are any such changes detected?",
    "Undocumented emergency changes create drift and hide malicious modification.",
    [s("SRC-NIST-SP800-53-R5", "CM-5"), s("SRC-AICPA-TSC", "CC8.1"), e("SRC-ECH-UNB-BASELINE", "CNV-PLT-010")],
    cls="contractual-common", imp="high", ind=FS, jur=USF, prod=ALLP)

C.q(6, "Is every asset assigned an accountable owner and a data classification, and how is that kept current?",
    "Assets without owners are not maintained or protected according to their sensitivity.",
    [d("SRC-ISO-27002-2022", "5.9"), d("SRC-ISO-27002-2022", "5.12"), s("SRC-NIST-CSF-2.0", "ID.AM-05"), s("SRC-NIST-SP800-53-R5", "RA-2")],
    cls="contractual-common", imp="medium", ind=ALL, jur=GLOBAL, prod=ORGALL)
C.q(6, "How are assets decommissioned, including revoking their credentials and certificates and destroying the data they held?",
    "Retired assets retain credentials or data that later leak.",
    [d("SRC-NIST-SP800-88"), d("SRC-NIST-CSF-2.0", "ID.AM-08"), s("SRC-ISO-27002-2022", "7.14"), s("SRC-ISO-27017", "CLD.8.1.5", "informed-by")],
    cls="contractual-common", imp="medium", ind=ALL, jur=GLOBAL, prod=ORGALL)
C.q(6, "How often do you reconcile your inventory against cloud provider billing and APIs to find orphaned resources, and what did the last reconciliation find?",
    "Orphaned resources holding data continue to run unmonitored.",
    [s("SRC-CIS-CONTROLS-V8.1", "1.2"), s("SRC-NIST-SP800-53-R5", "CM-8")],
    cls="customer-preference", imp="low", ind=ENT, jur=GLOBAL, prod=ORGALL)

C.q(1, "Is each infrastructure resource that stores customer data labeled with the customer tenant or sponsor cell whose data it holds, so that the blast radius of an incident on that resource can be determined immediately?",
    "Incident responders cannot tell which customers are affected by a compromised resource, delaying notification.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-TEN-009"), e("SRC-ECH-UNB-BASELINE", "UNB-TEN-017"), s("SRC-CIRN-RULE-2021", rel="informed-by"), s("SRC-NIST-SP800-61-R3", rel="informed-by")],
    cls="customer-preference", imp="medium", ind=BANK + DAF, jur=USF)
C.q(5, "Are unnecessary services, ports, default accounts, sample content and administrative interfaces removed or disabled on production systems and managed services?",
    "Default accounts and unused services provide easy entry points.",
    [d("SRC-NIST-SP800-53-R5", "CM-7"), s("SRC-CIS-CONTROLS-V8.1", "4.8"), s("SRC-CIS-BENCHMARKS"), s("SRC-PCI-DSS-4.0.1", "Req 2.2", "informed-by")],
    cls="industry-convention", imp="medium", ind=ALL, jur=GLOBAL, prod=ALLP)

print(C.emit())
