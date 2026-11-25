from devseclib import *

c = Cat("CHG")
B = lambda i: f"SRC-ECH-UNB-BASELINE@{i}!"
FIN = ["financial-services", "banking", "wealth-management", "donor-advised-funds"]

c.E("chgrec", "Change record per production change",
    "Machine-generated record linking the work item, commits, author and reviewer identities, approvals, automated check results, artifact digest, deployment time, environment and outcome for every production change.",
    producer="Praxis work protocol plus source control and deployment pipeline (integration proposed)", mechanism="event-driven-automated",
    fmt="JSON change record", prov=["work item", "commits", "author actor", "approver actors", "artifact digest", "deployment identifier", "timestamps"],
    signing="Signed by the deployment pipeline identity (proposed)", retention="Service-organization evidence class per CNV-PLT-009")
c.E("sod", "Segregation of duties check per deployment",
    "Automated check, recorded per deployment, that the change author did not approve and did not solely trigger the production deployment, with any exception and its approver.",
    mechanism="event-driven-automated", fmt="JSON check result", prov=["deployment identifier", "author", "approvers", "deployer identity", "exception reference"])
c.E("prodaccess", "Production access grants, sessions and break-glass records",
    "Records of every production access grant and session (who, why, scope, approver, start, end, commands or queries executed), break-glass activations with two-person approval, and post-use review.",
    mechanism="event-driven-automated", fmt="Access events plus session logs", prov=["person or agent", "approver(s)", "tenant scope", "start", "end", "reason"])
c.E("emerg", "Emergency change records and retrospective approvals",
    "Records of emergency changes with declared reason, approver, deployment, and retrospective review completed within the defined window.",
    mechanism="event-driven-automated", fmt="Change records flagged emergency plus review record", prov=["change identifier", "declared by", "approver", "review date"])
c.E("rollback", "Deployment and rollback test records",
    "Evidence of each deployment's health verification, of tested rollback for application and schema changes, and of rollback executions with outcome.",
    mechanism="event-driven-automated", fmt="Pipeline logs plus test results", prov=["deployment identifier", "artifact digest", "schema plan digest", "outcome"])
c.E("iac", "Infrastructure as code and drift detection results",
    "Infrastructure definitions in version control with change records, and periodic drift detection comparing deployed infrastructure and database schema to declarations, including unverifiable objects.",
    producer="Strata for database schema (exists); infrastructure tool not chosen", mechanism="periodic-automated", freshness="P1D",
    fmt="Drift report JSON", prov=["environment", "declaration version", "comparison state per object", "timestamp"])
c.E("notice", "Customer change notices",
    "Per-release notices to each sponsor listing changed control-relevant modules, security-relevant changes and breaking changes, with delivery confirmation.",
    mechanism="event-driven-automated", fmt="Release notice document plus delivery log", prov=["release", "sponsor", "delivery time"], disclosure="customer-only")

c.C("approval", "Approved, traceable change through a single pipeline",
    "Deploy to production only through the pipeline, only artifacts built from reviewed and approved commits, with the change record generated automatically.",
    "preventive-gate", "L5-build-release-gate", ["Deployment pipeline (not built)", "Praxis work protocol (exists)"], ["chgrec"],
    related=["UNB-CTRL-070", "UNB-CTRL-071"], requirements=["SOC2-011"],
    refs=["SRC-AICPA-TSC@CC8.1", "SRC-NIST-SP800-53-R5@CM-3", "SRC-ISO-27001-2022@A.8.32", "SRC-CSA-CCM-V4@CCC-01", "SRC-PCI-DSS-4.0.1@Req 6.5.1"])
c.C("sod", "Enforced segregation between authoring, approving and deploying",
    "Prevent any single identity, human or agent, from authoring, approving and deploying the same production change; control-relevant modules need two approvers who are not the author.",
    "preventive-gate", "L5-build-release-gate", ["Source control branch protection", "Deployment pipeline (not built)"], ["sod"],
    related=["UNB-CTRL-070"], requirements=["CNV-PLT-010"], refs=["SRC-NIST-SP800-53-R5@AC-5", "SRC-NIST-SP800-53-R5@CM-5", "SRC-PCI-DSS-4.0.1@Req 6.5.4", "SRC-AICPA-TSC@CC8.1"],
    residual=["Repository and pipeline administrators can change the rules; administrative changes need their own review and alerting."])
c.C("prodaccess", "Default-deny production access with break-glass",
    "Deny standing human and agent access to production data; allow scoped, expiring, pre-approved diagnostics and per-case approved writes; production database administration only through two-person break-glass.",
    "preventive-structural", "L3-restricted-interface", ["Access broker (not chosen)", "Managed PostgreSQL roles (not provisioned)"], ["prodaccess"],
    requirements=["CNV-ARC-002", "CNV-PLT-010"], refs=["SRC-NIST-SP800-53-R5@AC-6", "SRC-ISO-27001-2022@A.8.2", B("CNV-ARC-002")], owner=SEC)
c.C("emerg", "Defined emergency change path",
    "Allow expedited change only through the same pipeline with a declared emergency, a named approver, and retrospective review within a fixed window; no bypass of build provenance.",
    "preventive-procedural", "L5-build-release-gate", ["Deployment pipeline (not built)"], ["emerg"], refs=["SRC-CSA-CCM-V4@CCC-08", "SRC-AICPA-TSC@CC8.1"])
c.C("rollback", "Tested rollback and forward-fix for application and schema",
    "Make every deployment reversible or compensable: immutable artifacts for application rollback, Strata plans reviewed for destructive steps, and tested restore or forward-fix for schema changes.",
    "corrective", "L7-property-tested", ["Deployment pipeline (not built)", "Strata (exists; deploy plans judge breaking changes)"], ["rollback"],
    refs=["SRC-CSA-CCM-V4@CCC-09", "SRC-NIST-SP800-53-R5@CM-4"])
c.C("iac", "Declared infrastructure and schema with drift detection",
    "Declare infrastructure and database schema as code, deploy only from declarations, and detect drift daily, treating unverifiable comparisons as failures.",
    "detective-automated", "L6-automated-analysis", ["Strata (exists; schema drift)", "IaC tool (not chosen)"], ["iac"],
    requirements=["UNB-PLAT-007"], refs=["SRC-CSA-CCM-V4@CCC-07", "SRC-NIST-SP800-53-R5@CM-2", "SRC-CIS-CONTROLS-V8.1@4.1"])
c.C("notice", "Sponsor notice of control-relevant changes",
    "Publish to each sponsor, per release, the list of changed control-relevant modules and security-relevant changes.",
    "administrative", "L5-build-release-gate", ["Release pipeline (not built)"], ["notice"], requirements=["CNV-PLT-010"], refs=[B("CNV-PLT-010")])

a1 = c.A("Change approval and authorization",
    "Customers need assurance that every production change is authorized, reviewed and traceable.",
    "Production changes are deployed only through one pipeline from reviewed, approved commits; the pipeline generates a change record linking work item, commits, author and approvers, check results, artifact digest and deployment; sponsors receive a per-release notice of changed control-relevant modules; change records are retained as service-organization evidence.",
    ["approval", "notice"], ["chgrec", "notice"], requirements=["SOC2-011", "CNV-PLT-010", "CNV-PLT-009"], mechanism="event-driven-automated", impl="medium", rec="low",
    current="No production environment or deployment pipeline exists. Echelon tool repositories use Praxis work items and CI validation for their own releases.")
a2 = c.A("Segregation of duties in development and deployment",
    "Customers need assurance that no single person or agent can change production on their own.",
    "The pipeline enforces that no identity, human or agent, can author, approve and deploy the same change; control-relevant modules need two approvers other than the author; repository and pipeline administrative changes are themselves reviewed and alerted; exceptions are recorded with approver and expiry. Where headcount is insufficient for independent human approval, Echelon will disclose this and use an external reviewer rather than claim segregation it does not have.",
    ["sod", "approval"], ["sod", "chgrec"], requirements=["CNV-PLT-010"], mechanism="event-driven-automated", impl="low", rec="medium",
    current="Not established. Echelon's organizational headcount is not established in reviewed records; Limen's CODEOWNERS names one owner account for guardrail paths.",
    oq=["How many independent humans with production-relevant authority will Echelon have at launch?"],
    challenge=ch(
        customer_intent="Prevent fraud or sabotage by a single insider and catch mistakes.",
        adverse_outcome="One person deploys a malicious or erroneous change to money-moving code.",
        conventional_control_effectiveness="Effective where real independence exists; in very small companies it is often nominal.",
        legally_required="Not by statute for Echelon; SOX 404 applies to public-company customers' own controls and flows down through their reliance on SOC reports.",
        contractually_required="Expected by SOC 2 auditors (CC8.1) and bank vendor reviews.",
        historical_convention="Separate developers, approvers and operations staff.",
        architectural_elimination="Cannot be eliminated by architecture; it is about people. Automation can enforce that rules are followed but not create independent people.",
        automatic_enforcement="Pipeline identity checks per deployment.",
        continuous_evidence="Per-deployment segregation check results.",
        stronger_alternative="Automated enforcement plus provenance plus external reviewer for control-relevant changes when internal independence is absent.",
        alternative_verifiable="Yes from pipeline and source control records.",
        customer_acceptance_likelihood="Uncertain for a founder-led company with AI agents doing most work.",
        invalidating_conditions="A single administrator able to alter branch protection or pipeline rules without detection.",
        conventional_cost="Additional staff.", alternative_cost="External reviewer retainer; tooling.",
        alternative_risks="Agents counted as independent approvers would make segregation illusory.",
        supporting_arguments=["Automation enforces rules consistently."],
        opposing_arguments=["AI agents are not independent humans; counting them would be misleading.", "Small-company reality may not meet customer expectations."],
        technical_effectiveness="weaker", institutional_acceptance="uncertain"))
a3 = c.A("Production access and break-glass",
    "Customers need assurance that engineers and agents cannot browse or change their data in production at will.",
    "No human or agent has standing access to production data. Read diagnostics are scoped, expiring and pre-approved by the sponsor; writes need per-case approval; production database administrative roles are break-glass only with two-person activation; every session is recorded and reviewed after use.",
    ["prodaccess"], ["prodaccess"], requirements=["CNV-ARC-002", "CNV-PLT-010"], mechanism="event-driven-automated", impl="medium", rec="low", owner=SEC, products=["unbound"])
a4 = c.A("Emergency change",
    "Customers need assurance that urgent fixes do not become a route around change controls.",
    "Emergency changes use the same pipeline, artifacts and provenance as normal changes; only the approval timing differs. An emergency is declared with a reason and a named approver, and a retrospective review is completed within two business days; emergency frequency is reported as a metric.",
    ["emerg", "approval"], ["emerg"], mechanism="event-driven-automated", impl="low", rec="low")
a5 = c.A("Deployment, rollback and database migration safety",
    "Customers need assurance that a bad release can be reversed without losing or corrupting their data.",
    "Application releases are immutable artifacts that can be rolled back; database changes are deployed only as Strata plans that are compiled, diffed and judged for breaking effects, with destructive steps blocked by default; schema changes follow expand-and-contract so application rollback remains possible; rollback and restore are tested before release; after any restore, money movement stays blocked until reconciliation (CNV-ARC-001).",
    ["rollback", "iac"], ["rollback", "iac"], requirements=["CNV-ARC-001", "CNV-ARC-004"], mechanism="event-driven-automated", impl="medium", rec="low",
    current="Strata exists as a pilot schema tool that judges what each change would break before applying it (strata@c6a384ec); it is not operated for a production Echelon database.")
a6 = c.A("Change evidence and infrastructure as code",
    "Customers and auditors need complete, tamper-evident evidence of what changed, when, by whom and why.",
    "Infrastructure and database schema are declared as code and deployed only from declarations, with daily drift detection. Change evidence is generated by construction: Praxis records the work item, actor (human or agent with model and runtime) and content digests; the pipeline adds approvals, artifact digests and deployment records; records are signed and retained under the service-organization evidence class. Echelon distinguishes self-reported actor identity from authenticated identity and binds the two through the source control platform's authenticated accounts.",
    ["iac", "approval"], ["iac", "chgrec"], status="partially-implemented",
    rationale="Praxis work protocol and provenance exist and are used for Echelon repositories; integration with a deployment pipeline, signing and infrastructure as code for a production service do not exist.",
    current="Praxis (praxis@12bf9951) records work transitions, actor identity and content digests as append-only events in Echelon repositories. No production infrastructure or deployment pipeline exists.",
    provable="Praxis event logs and provenance in Echelon tool repositories; first-party, not independently verified, not for a production service.",
    statement="Echelon's repositories record each work item and its human or AI contributor through its Praxis tooling. Production change evidence and infrastructure as code are planned with the first production service.",
    kind="qualified-current-fact", requirements=["SOC2-011", "SOC2-004", "CNV-PLT-009"], mechanism="event-driven-automated", impl="medium", rec="low",
    challenge=ch(
        customer_intent="Be able to verify that changes were controlled, without relying on the vendor's word.",
        adverse_outcome="Unauthorized change goes undetected because change records are incomplete or editable.",
        conventional_control_effectiveness="Ticketing systems and change advisory boards produce manual records that are often incomplete and reconstructed for audits.",
        legally_required="No; SOC 2 CC8.1 and customer audits require evidence.",
        contractually_required="Common for SOC 2 and bank customers.",
        historical_convention="Change tickets with CAB approval, sampled by auditors.",
        architectural_elimination="Manual record keeping is eliminated if records are produced by the only path to production.",
        automatic_enforcement="Pipeline is the only path to production; Praxis validation fails on unattributed changes.",
        continuous_evidence="Per-change machine records.",
        stronger_alternative="Evidence by construction from work protocol, source control and pipeline.",
        alternative_verifiable="Yes if records are signed and the pipeline is the only path; auditors can test completeness by comparing deployments to records.",
        customer_acceptance_likelihood="Likely; auditors increasingly accept system-generated change evidence.",
        invalidating_conditions="Any deployment path outside the pipeline; Praxis actor fields accepted without binding to authenticated accounts; editable event logs.",
        conventional_cost="Manual ticket overhead and audit preparation.", alternative_cost="Pipeline integration and signing.",
        alternative_risks="Praxis actor identity is self-reported by the executing process; on its own it is attribution, not authentication or approval.",
        supporting_arguments=["Records cannot be forgotten if they are produced by the only path."],
        opposing_arguments=["Praxis is not an approval system and does not authenticate actors.", "Auditors must still test the pipeline's completeness."],
        technical_effectiveness="stronger", institutional_acceptance="likely"))

Q = c.Q
# a1 (6)
Q(a1, "Change management", "Do you have a documented change management process for production systems, and how is each change authorized before deployment?",
  "Unauthorized changes reach production.", ["SRC-AICPA-TSC@CC8.1!", "SRC-ISO-27001-2022@A.8.32", "SRC-CSA-CCM-V4@CCC-01", "SRC-NIST-SP800-53-R5@CM-3"], cls="certification-criteria", imp="high",
  alt=["Describe your change control procedures.", "Are all changes to production approved and tested?"])
Q(a1, "Change management for regulated customers", "Can you evidence change management procedures for systems that handle our customer information, consistent with our safeguards obligations?",
  "Financial institution cannot show its service provider manages change.", ["SRC-FTC-SAFEGUARDS-RULE@314.4(c)(7)", "SRC-INTERAGENCY-GLBA-SAFEGUARDS", "SRC-FFIEC-DAM-BOOKLET"], cls="legal-regulatory", imp="high",
  ind=["financial-services", "banking", "wealth-management"], jur=["US-federal"], auth="FTC; federal banking agencies",
  note="Obligation falls on covered customers and is overseen through service provider arrangements.")
Q(a1, "Change traceability", "For any production change, can you show the request, the code, the reviewers, the tests and the deployment record?",
  "Changes cannot be reconstructed for investigation or audit.", ["SRC-ECH-UNB-SOC2-DIRECTIVE@SOC2-011!", "SRC-AICPA-TSC@CC8.1"], imp="medium", disclosure="auditor-only")
Q(a1, "Customer notification", "Will you notify us before changes that affect security, controls we rely on, or integrations, and how much notice will we get?",
  "Customers surprised by changes to controls they rely on.", [B("CNV-PLT-010"), "SRC-INTERAGENCY-TPRM-2023"], cls="contractual-common", imp="medium", ind=FIN)
Q(a1, "Post-change verification", "How do you confirm that security requirements still hold after a significant change?",
  "Changes silently break security controls.", ["SRC-PCI-DSS-4.0.1@Req 6.5.2", "SRC-NIST-SP800-53-R5@CM-4"], imp="medium")
Q(a1, "Configuration changes", "Are configuration changes (feature flags, tenant settings, policy parameters) controlled like code changes?",
  "Configuration changes bypass change control.", ["SRC-CSA-CCM-V4@CCC-04", B("UNB-API-STD-001")], imp="medium", prod=["unbound"])
# a2 (5)
Q(a2, "Segregation of duties", "Are the roles of developing, approving and deploying changes to production separated, and how is this enforced?",
  "One person introduces and deploys unauthorized changes.", ["SRC-NIST-SP800-53-R5@AC-5", "SRC-PCI-DSS-4.0.1@Req 6.5.4", "SRC-AICPA-TSC@CC8.1"], cls="certification-criteria", imp="high",
  alt=["Can developers deploy their own code to production?"])
Q(a2, "Administrative override", "Who can change branch protection, pipeline rules or deployment permissions, and are such changes reviewed and alerted?",
  "Administrators disable controls and act alone.", ["SRC-NIST-SP800-53-R5@CM-5", "SRC-OPENSSF-SCORECARD@Branch-Protection"], imp="high")
Q(a2, "AI agents in deployment", "Can AI agents approve or deploy changes, and if so, can an agent approve a change written by another agent?",
  "Segregation of duties becomes illusory with agent approvers.", ["SRC-OWASP-AGENTIC-AI", "SRC-ECH-UNB-SOC2-DIRECTIVE@SOC2-017!"], imp="high")
Q(a2, "Small organization", "Given the size of your organization, how many people can approve and deploy production changes, and what compensating controls apply where duties cannot be separated?",
  "Key-person concentration defeats segregation.", ["SRC-INTERAGENCY-TPRM-2023", "SRC-TPRM-COMMUNITY-BANK-GUIDE-2024"], cls="supervisory-guidance", imp="high",
  ind=["banking", "financial-services"], jur=["US-federal"], auth="Federal banking agencies (guidance to institutions on third-party oversight)")
Q(a2, "Financial control modules", "Do changes to code that implements financial controls receive approval from someone with financial control responsibility, not only engineering?",
  "Engineering changes weaken financial controls without business awareness.", [B("CNV-PLT-010"), "SRC-SOX-404^", "SRC-COSO-2013"], imp="medium", ind=FIN, prod=["unbound"])
# a3 (5)
Q(a3, "Production access", "Which staff have access to production systems and customer data, how is it granted, and how often is it reviewed?",
  "Excessive standing access to customer data.", ["SRC-AICPA-TSC@CC6.1", "SRC-ISO-27001-2022@A.8.2", "SRC-NIST-SP800-53-R5@AC-6"], cls="certification-criteria", imp="critical")
Q(a3, "Engineer data access", "Can your engineers query our production data for support or debugging, and do we approve or see that access?",
  "Vendor staff access customer data without the customer's knowledge.", [B("CNV-ARC-002")], cls="customer-preference", imp="high", ind=FIN, prod=["unbound"])
Q(a3, "Break-glass", "How does emergency privileged access work, who approves it, how long does it last, and how is its use reviewed?",
  "Emergency access becomes permanent or unreviewed.", [B("CNV-PLT-010"), "SRC-NIST-SP800-53-R5@AC-2"], imp="high")
Q(a3, "Direct data fixes", "When data must be corrected in production, is it done through the application with approvals and audit trail, or by direct database changes?",
  "Direct data changes bypass business controls and audit history.", [B("UNB-IMM-002"), "SRC-ECH-SCS-0.1@SEC-DB-001!"], imp="high", ind=FIN)
Q(a3, "Agent production access", "Do any AI agents have access to production systems or data, and with what limits?",
  "Agents with production access are manipulated into harmful actions.", ["SRC-OWASP-AGENTIC-AI", "SRC-ECH-UNB-BASELINE@UNB-AGT-002!"], imp="high")
# a4 (4)
Q(a4, "Emergency change", "What is your emergency change process, and how do you ensure emergency changes are reviewed afterward?",
  "Emergency path used to bypass controls.", ["SRC-CSA-CCM-V4@CCC-08", "SRC-AICPA-TSC@CC8.1", "SRC-ECH-UNB-SOC2-DIRECTIVE@SOC2-011!"], cls="certification-criteria", imp="medium")
Q(a4, "Emergency frequency", "How many emergency changes occurred in the last year, and what share of all changes was that?",
  "Routine use of emergency path indicates control weakness.", ["SRC-AICPA-SOC2-GUIDE"], cls="customer-preference", imp="low")
Q(a4, "Emergency build integrity", "Do emergency fixes still go through the normal build, signing and provenance steps?",
  "Hotfixes deployed from developer machines.", ["SRC-SLSA@Build L3", "SRC-NIST-SP800-218@PS.1"], imp="medium")
Q(a4, "Security patch speed", "How quickly can you deploy a fix for a critical vulnerability, and what controls remain in place when you do?",
  "Slow patching or uncontrolled urgent patching.", ["SRC-CISA-BOD-22-01^", "SRC-NIST-SP800-53-R5@SI-2"], imp="medium")
# a5 (5)
Q(a5, "Rollback", "Can every production deployment be rolled back, how quickly, and how often is rollback tested?",
  "Failed releases cause extended outage or data damage.", ["SRC-CSA-CCM-V4@CCC-09", "SRC-ISO-27001-2022@A.8.32"], imp="medium")
Q(a5, "Database migrations", "How are database schema changes reviewed, tested and deployed, and how do you prevent a migration from destroying or corrupting financial data?",
  "Destructive migrations lose authoritative records.", [B("CNV-ARC-004"), B("UNB-IMM-001"), "SRC-NIST-SP800-53-R5@CM-4"], imp="high", ind=FIN)
Q(a5, "Pre-production testing", "Are changes tested in an environment representative of production before deployment, without real customer data?",
  "Untested changes or real data in test.", ["SRC-CSA-CCM-V4@CCC-02", "SRC-ISO-27001-2022@A.8.31", "SRC-PCI-DSS-4.0.1@Req 6.5.3"], imp="medium")
Q(a5, "Release scheduling", "Do you deploy during customer-critical periods (year-end giving, grant cycles), and can customers request change freezes?",
  "Changes during peak periods disrupt critical operations.", [B("UNB-CTL-006")], cls="customer-preference", imp="low", ind=["donor-advised-funds", "nonprofit"], prod=["unbound"])
Q(a5, "Recovery after rollback", "After a rollback or restore, how do you ensure that payments and grants in flight are neither lost nor duplicated?",
  "Recovery actions duplicate or drop financial effects.", [B("CNV-ARC-001"), B("UNB-RES-002")], imp="high", ind=FIN, prod=["unbound"])
# a6 (5)
Q(a6, "Infrastructure as code", "Is your infrastructure defined as code, versioned and deployed through the same review and pipeline controls as application code?",
  "Manual infrastructure changes are untracked and inconsistent.", ["SRC-CSA-CCM-V4@CCC-03", "SRC-NIST-SP800-53-R5@CM-2", "SRC-CIS-CONTROLS-V8.1@4.1"], imp="medium")
Q(a6, "Drift detection", "How do you detect changes made to production outside the approved process?",
  "Unauthorized changes persist undetected.", ["SRC-CSA-CCM-V4@CCC-07", "SRC-AICPA-TSC@CC7.1", "SRC-NIST-SP800-53-R5@CM-6"], imp="high")
Q(a6, "Evidence generation", "Is change evidence generated automatically by your tools, or compiled manually for audits?",
  "Change evidence is incomplete or reconstructed.", ["SRC-ECH-UNB-SOC2-DIRECTIVE@SOC2-004!", "SRC-AICPA-SOC2-GUIDE"], cls="customer-preference", imp="medium")
Q(a6, "Work protocol as evidence", "You use a repository work protocol (Praxis) that records who performed each change. Is that identity authenticated, can records be altered, and does it record approval or only attribution?",
  "Attribution records mistaken for authenticated approval evidence.", ["SRC-ECH-UNB-SOC2-DIRECTIVE@SOC2-002!", "SRC-AICPA-TSC@CC8.1"], cls="echelon-internal", imp="medium",
  note="Praxis records actor identity as self-reported by the executing process; it is not an approval system.")
Q(a6, "Evidence retention", "How long do you retain change and deployment records, and are they kept after a customer leaves?",
  "Evidence unavailable for audit periods or disputes.", [B("CNV-PLT-009"), "SRC-ECH-UNB-SOC2-DIRECTIVE@SOC2-023!"], imp="low")

RECORDS = c.records()
