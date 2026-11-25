from lib import *

C = Category("IAM")

# ---------------- Answer units ----------------
C.au(1, "Workforce joiner, mover and leaver lifecycle",
     "Workforce provisioning and deprovisioning",
     "The customer needs vendor personnel to receive only approved access and to lose it promptly when they leave or change roles, across every system including third-party consoles.",
     "unknown",
     "No workforce identity provider, HR system or provisioning process was located. Headcount is not established. SOC2-010 requires provisioning and deprovisioning coverage as a design directive only.",
     "All workforce access derives from a single authoritative identity provider tied to an engagement record (employee or contractor, with end date). Access is granted only through approved role bundles; there is no direct grant on target systems. Termination disables the identity provider account immediately (same business day for voluntary departures, immediately for involuntary), which cascades through federation to every connected system; systems that cannot federate are listed and deprovisioned by an automated task with evidence. Role changes revoke old access before new access is granted. Dormant accounts are disabled after a defined inactivity period. A daily match of identity-provider administrative actions against approved requests detects unapproved grants (TVR-SEC-008).",
     "Unknown; no evidence located.",
     "Select a workforce identity provider before onboarding staff to production; implement role bundles and automated deprovisioning.",
     "Nothing.",
     "Echelon has not yet established a workforce identity provider or a joiner, mover and leaver process for production. Centralized, automated provisioning and same-day deprovisioning are planned.",
     "not-available",
     controls=[1, 2], evrs=[1, 2],
     reqs=["SOC2-010", "CNV-GOV-004", "TVR-SEC-008", "AUTH-I6"],
     fresh="P1D", mech="event-driven-automated", auto="high", impl="low", rec="low",
     owner="Unassigned; proposed Security Lead",
     residual=["Systems that do not support federation require separate deprovisioning and are a common gap."])

C.au(2, "Periodic access recertification and continuous entitlement hygiene",
     "Access reviews",
     "The customer needs assurance that access remains appropriate over time and that excess or stale access is removed, with credible evidence.",
     "proposed-target-state",
     "UNB-XIN-IAM-004 specifies quarterly recertification for privileged and workforce roles, annual for delegated customer roles, no self-certification, and automatic suspension 14 days after the due date. Not implemented.",
     "Access recertification runs quarterly for privileged and workforce roles and at least annually for delegated customer roles (advisors, authorized viewers, agents), and covers third-party authority registers such as bank-portal users and custodian trading authorities. Reviewers cannot certify their own access. Uncertified access is suspended automatically 14 days after the due date and the suspension is recorded and notified. Between reviews, grants carry expiry dates and are revoked by events (termination, role change, death or incapacity, partner exit), so the review confirms a mostly self-cleaning population rather than discovering it. Review evidence includes the complete population with counts reconciled to the system of record.",
     "Not implemented. Requirements exist (UNB-XIN-IAM-004, AUTH-I6, CNV-GOV-006).",
     "Implement the recertification campaign engine with automatic suspension and population reconciliation.",
     "Requirement text only.",
     "Echelon's Unbound design requires quarterly review of privileged and workforce access, annual review of delegated customer roles, no self-certification, and automatic suspension of uncertified access. These are planned, not operating.",
     "planned",
     controls=[3], evrs=[3],
     reqs=["UNB-XIN-IAM-004", "AUTH-I6", "CNV-GOV-006", "GOV-AUTH-025", "SOC2-010", "SOC2-034"],
     fresh="P90D", mech="periodic-automated", auto="high", impl="medium", rec="low",
     residual=["Reviewers may approve without scrutiny; automatic suspension only addresses non-response, not careless approval."],
     challenge={
         "customer_intent": "Prevent access creep and catch access that should have been removed.",
         "adverse_outcome": "Former staff, moved staff or departed advisors retain access to funds and data.",
         "conventional_control_effectiveness": "Periodic manual reviews are widely performed but frequently rubber-stamped; they detect stale access up to a quarter late and depend on reviewer diligence.",
         "legally_required": "NYDFS 500.7 requires covered entities to review access privileges at least annually; PCI DSS 4.0.1 Req 7.2.4 requires reviews at least every six months for in-scope systems. These bind customers or card environments, not Echelon directly.",
         "contractually_required": "Common in bank vendor contracts and SOC 2 control sets (CC6.2, CC6.3).",
         "historical_convention": "Quarterly or semiannual manager attestation campaigns.",
         "architectural_elimination": "Stale access can be largely eliminated by construction: every grant has an expiry and is derived from a parent authority (AUTH-I2), and lifecycle events revoke derived grants automatically (AUTH-I1, UNB-RCN-ENT-004).",
         "automatic_enforcement": "Expiry and event-driven revocation; automatic suspension of uncertified access.",
         "continuous_evidence": "Every grant, expiry and revocation is an append-only event, so the access population at any instant can be reconstructed.",
         "stronger_alternative": "Expiring, event-revoked grants plus a lighter periodic review focused on exceptions and privileged roles.",
         "alternative_verifiable": "Yes, through the event history and population reconciliation.",
         "customer_acceptance_likelihood": "Customers and auditors will still expect a periodic review artifact; the by-construction approach is likely accepted as strengthening, not replacing, it.",
         "invalidating_conditions": "Any grant path that bypasses the authority registry (for example direct database grants or a third-party console).",
         "conventional_cost": "Recurring reviewer time each quarter.",
         "alternative_cost": "Upfront engineering in the authority model, already required by Unbound design.",
         "alternative_risks": "Over-aggressive expiry can lock out legitimate advisors and create pressure for emergency overrides.",
         "supporting_arguments": ["Event-driven revocation closes the window between departure and review."],
         "opposing_arguments": ["Auditors test the review control itself; removing or thinning it may produce findings even if risk is lower."],
         "technical_effectiveness": "stronger",
         "institutional_acceptance": "likely"})

C.au(3, "Privileged access to production infrastructure and databases",
     "Privileged access",
     "The customer needs the most powerful access to the service to be rare, separately authenticated, time-bound, approved and fully recorded, because privileged misuse defeats every other control.",
     "proposed-target-state",
     "CNV-PLT-010 requires production database administrative roles to be break-glass only with two-person activation and requires production data access by engineers to follow CNV-ARC-002. UNB-XIN-IAM-001 requires separate principals per realm. CNV-PLT-003 requires AAL3-grade authenticators for privileged roles. None is implemented.",
     "There is no standing administrative access to production. Privileged access uses a dedicated PlatformWorkforce principal distinct from any customer or everyday identity, authenticated with AAL3-grade hardware or device-bound keys, elevated just in time for a bounded task with approval by a second person, and recorded in logs that the elevated principal cannot alter. Production database administrative roles are break-glass only with two-person activation. Application identities hold INSERT and constrained SELECT on authoritative tables and no UPDATE, DELETE, TRUNCATE or DDL. The number of people eligible for elevation is published to customers.",
     "Not implemented. Requirements exist.",
     "Implement just-in-time elevation with two-person approval and immutable session logging before production.",
     "Requirement text only.",
     "Echelon's Unbound design has no standing production administrative access: privileged access is separately authenticated with hardware-backed keys, time-bound, approved by a second person and logged, and database administrator roles are break-glass only. This is planned, not operating.",
     "planned",
     controls=[4, 5], evrs=[4, 5],
     policies=["SEC-AUTH-001", "SEC-DB-001"],
     reqs=["CNV-PLT-010", "CNV-ARC-002", "UNB-XIN-IAM-001", "CNV-PLT-003", "SOC2-010", "GOV-AUTH-004"],
     fresh="per-event", mech="event-driven-automated", auto="high", impl="medium", rec="low",
     residual=["Cloud provider root or organization-owner credentials remain a standing privilege that must be sealed separately.",
               "A database administrator with physical storage access can still alter data; the design anchors ledger digests externally (CNV-PLT-010) to detect this, not prevent it."],
     challenge={
         "customer_intent": "Ensure that the people with the keys to the kingdom cannot misuse them unnoticed.",
         "adverse_outcome": "Insider fraud, credential theft of an administrator, or ransomware with admin rights.",
         "conventional_control_effectiveness": "Commercial privileged access management vaults reduce password exposure but often leave standing eligibility broad and rely on after-the-fact session review that rarely happens.",
         "legally_required": "NYDFS 500.7 (as amended) requires covered entities to limit and periodically review privileged accounts; customers flow this to vendors. Not directly binding on Echelon.",
         "contractually_required": "Common; banks expect PAM and session recording.",
         "historical_convention": "PAM vault, password checkout, session recording.",
         "architectural_elimination": "Standing database write privilege for application identities is eliminated by grant design (INSERT-only on authoritative tables); interactive administration is eliminated except break-glass.",
         "automatic_enforcement": "Strata-declared grants with drift detection; elevation tooling that requires a second approver.",
         "continuous_evidence": "Elevation requests, approvals and session logs as append-only events; grant diffs on every deploy.",
         "stronger_alternative": "No standing privilege plus INSERT-only application grants plus external anchoring of ledger digests.",
         "alternative_verifiable": "Yes; grants are inspectable and elevation events are reconstructable.",
         "customer_acceptance_likelihood": "Likely, if session recording or equivalent logging of break-glass activity is shown.",
         "invalidating_conditions": "If emergency elevation becomes routine, or if cloud console owners can grant themselves database access outside the process.",
         "conventional_cost": "PAM licensing and administration.",
         "alternative_cost": "Engineering effort for elevation workflow; possibly lower licensing.",
         "alternative_risks": "Operational friction during incidents may push staff toward workarounds.",
         "supporting_arguments": ["Removing standing privilege removes the target attackers seek."],
         "opposing_arguments": ["A small team may lack two qualified people available at all hours for approvals."],
         "technical_effectiveness": "stronger",
         "institutional_acceptance": "likely"})

C.au(4, "Break-glass emergency access",
     "Emergency access",
     "The customer needs emergency access to exist for recovery but to be sealed, rare, narrowly scoped, quickly disclosed and unable to change financial outcomes.",
     "proposed-target-state",
     "UNB-XIN-IAM-005 specifies sealed credentials independent of the workforce IdP, two-person activation, four-hour expiry, security owner paging, tenant notification within one hour, and a prohibition on domain transitions. CNV-PLT-007 governs platform-originated holds. Not implemented.",
     "Break-glass credentials are sealed and independent of the workforce identity provider, require two-person activation, expire automatically within four hours, page the security owner, and notify affected tenants' administrators within one hour. Break-glass sessions are limited to reading, protective actions (payment freeze, hold, credential revocation) and infrastructure recovery; they cannot approve grants, change payees, change authority, post ledger entries or remove holds. Any authoritative state change without a matching command event blocks affected payments until reviewed. Procedures are tested at least annually without using real customer data.",
     "Not implemented. Requirements exist.",
     "Implement sealed credential storage, activation workflow and post-use review before production.",
     "Requirement text only.",
     "Echelon's Unbound design specifies sealed, two-person, time-limited emergency access that notifies affected customers within one hour and cannot change grants, payees, authority or ledger entries. This is planned, not operating.",
     "planned",
     controls=[6], evrs=[6],
     reqs=["UNB-XIN-IAM-005", "CNV-PLT-007", "CNV-PLT-010"],
     fresh="per-event", mech="event-driven-automated", auto="high", impl="medium", rec="low",
     residual=["Two-person activation may be impossible during a severe incident with a very small team; the fallback must be decided in advance."],
     oq=["Who are the two people eligible to activate break-glass at launch, given current staffing is not established?"])

C.au(5, "Vendor staff access to customer tenant data and access transparency",
     "Operator access to customer data",
     "The customer needs control over, and visibility into, when the vendor's people look at or act on its data.",
     "proposed-target-state",
     "UNB-XIN-IAM-002 and CNV-ARC-002 specify deny-by-default operator access, sponsor pre-approved delegations or per-case approval, prohibition on sponsor decisions, and an access transparency view within 15 minutes. TVR-SEC-007 treats assisted-channel commands as low-assurance. Not implemented.",
     "Vendor staff have no access to a customer's non-public data by default. Read diagnostics require an OperatorAccessDelegation pre-approved by the sponsor for listed task classes, scopes and maximum duration; writes require per-case approval by an authorized sponsor approver. Staff cannot perform sponsor decisions (grant approval, payee change, authority change, fund closure) unless the sponsor's delegation names that command class. Revocation takes effect on the next request. Every operator session appears to the customer's administrators within 15 minutes with who, when, scope, reason, case and records touched. Support 'view as' is a distinct low-assurance command kind that cannot add recipients without sponsor-direct confirmation. Support personnel locations and subcontractors are disclosed.",
     "Not implemented. Requirements exist.",
     "Implement OperatorAccessDelegation, per-case approval and the transparency view as part of the authorization core.",
     "Requirement text only.",
     "In Echelon's Unbound design, vendor staff cannot access customer data unless the customer pre-approves a scoped, expiring delegation or approves a specific case, and every access is visible to the customer within 15 minutes. This is planned, not operating.",
     "planned",
     controls=[7], evrs=[7],
     policies=["SEC-AUTH-001"],
     reqs=["UNB-XIN-IAM-002", "CNV-ARC-002", "TVR-SEC-007", "CNV-PLT-010"],
     fresh="P1D", mech="continuous-automated", auto="full", impl="medium", rec="low",
     residual=["Infrastructure operators with storage-level access can bypass application-level transparency; this is addressed by break-glass rules and encryption, not by the transparency view."],
     challenge={
         "customer_intent": "Ensure vendor staff do not browse or alter our clients' data without our knowledge.",
         "adverse_outcome": "Insider snooping, insider fraud, or attacker use of a compromised support account.",
         "conventional_control_effectiveness": "Conventional answers ('access is limited to authorized personnel on a need-to-know basis, and logged') are unverifiable by the customer and depend on vendor-internal review.",
         "legally_required": "Not specifically; GLBA and Regulation S-P service-provider oversight expectations require the customer to ensure appropriate safeguards.",
         "contractually_required": "Increasingly requested by banks and large enterprises (customer approval of support access, access logs).",
         "historical_convention": "Need-to-know policy plus internal logging.",
         "architectural_elimination": "Default access is eliminated; access exists only as a customer-approved delegation object.",
         "automatic_enforcement": "Authorization core refuses operator requests without an active delegation or case approval (CNV-ARC-002 AC-1, AC-2).",
         "continuous_evidence": "Customer-visible access transparency log generated by the same enforcement path.",
         "stronger_alternative": "Customer-controlled, expiring delegations with customer-visible logs, as specified.",
         "alternative_verifiable": "Yes, by the customer directly through the transparency view, and by testing denial without a delegation.",
         "customer_acceptance_likelihood": "Likely; this exceeds common practice.",
         "invalidating_conditions": "Any administrative path (database console, log search, backups) that reads tenant data outside the authorization core.",
         "conventional_cost": "Low.",
         "alternative_cost": "Moderate engineering; support latency when approvals are needed.",
         "alternative_risks": "Customers may pre-approve broad delegations for convenience, recreating standing access.",
         "supporting_arguments": ["Customer-visible evidence beats vendor assertions."],
         "opposing_arguments": ["Logs and telemetry may still expose data to engineers unless redaction (MON-014) is effective."],
         "technical_effectiveness": "stronger",
         "institutional_acceptance": "likely"})

C.au(6, "Service accounts, workload identities and machine credentials",
     "Non-human identities",
     "The customer needs machine identities to be inventoried, least-privileged, short-lived and unusable for interactive login, because leaked service credentials are a common breach path.",
     "proposed-target-state",
     "SEC-CRYPTO-001 (proposed) prohibits hardcoded secrets and requires managed keys, secret scanning and rotation. The tenant-aware persistence design grants application identities INSERT and constrained SELECT only. Limen's publishing workflow uses npm Trusted Publishing over GitHub OIDC with no stored npm token, a real example of federated workload identity in Echelon tooling. No production workload identities exist.",
     "Every workload (service, job, CI pipeline, agent) has its own identity in the Workload realm, registered in an inventory with owner and purpose. Credentials are short-lived and obtained by workload identity federation (for example OIDC from CI) rather than stored static secrets; any unavoidable static secret is held in a managed secret store and rotated automatically. Workload identities cannot log in interactively. Each component uses a distinct least-privilege database role; no application identity can UPDATE or DELETE authoritative event or journal tables. CI can deploy only artifacts that passed gates and only with approval for control-relevant modules.",
     "Not implemented for Unbound. Limen (limen@743cdb9b) publishes its npm package using GitHub OIDC trusted publishing with no stored token, per its README; this is release tooling for an open component, not a production service identity.",
     "Adopt workload identity federation and a secret manager for all Unbound workloads; generate service account inventory from infrastructure code.",
     "The Limen publishing configuration can be shown as an example practice. Nothing for Unbound.",
     "Echelon intends every service and pipeline to use its own short-lived, federated identity with least-privilege database roles and no interactive login. Some Echelon release tooling already publishes without stored tokens; the production design is planned.",
     "planned",
     controls=[8, 9], evrs=[8, 9],
     policies=["SEC-CRYPTO-001", "SEC-DB-001"],
     reqs=["UNB-XIN-IAM-001", "UNB-CUST-017", "UNB-API-STD-005", "SOC2-010", "CNV-PLT-010"],
     fresh="P1D", mech="continuous-automated", auto="full", impl="medium", rec="low",
     residual=["Third-party integrations (custodians, banks) may only support static API keys."])

C.au(7, "AI agent identities, authority bounds and suspension",
     "AI agent identities",
     "The customer needs every AI agent to be an individually attributable, bounded, monitored and interruptible identity that cannot expand its own authority.",
     "proposed-target-state",
     "SOC2-017, UNB-XIN-IAM-001 (Workload realm includes AI agent principals), GOV-AUTH-003, GOV-AUTH-024, UNB-AI-STD-001, UNB-AGT-002, UNB-AGT-003 and AIN-013 specify the target. Engineering agents in Echelon repositories are attributed by Praxis using self-declared identity. Nothing is implemented for production.",
     "Each product agent is a distinct Workload principal with a named human owner, a declared capability manifest and an authority tier. When an agent acts for a user, it holds a delegated grant derived from that user's authority that can never exceed it and ends when the parent ends; the delegation chain is recorded on every action. Agents cannot grant themselves permissions, approve their own consequential actions, change their own policy or clear their own alerts. Prohibited tools are removed by the tool broker rather than forbidden by prompt. A global and per-tenant emergency stop suspends agents and safely parks queued actions. Engineering agents never hold production customer-data credentials; their CI identity is authenticated workload identity rather than self-declared. Agent identities are included in access reviews and deprovisioned when retired.",
     "Requirements only for product agents. Praxis records self-declared engineering-agent identity per execution in development repositories (docs/agent-provenance.md); it is not authenticated.",
     "Implement agent principals, delegation chains, tool broker and emergency stop; bind engineering agent CI runs to authenticated workload identity.",
     "Praxis execution records show declared agent identity for development work; they do not prove identity.",
     "Echelon's Unbound design treats each AI agent as its own bounded, attributable identity that cannot exceed or expand its authority and can be stopped immediately. This is planned. Echelon's development repositories currently record self-declared agent attribution only.",
     "planned",
     controls=[10, 11], evrs=[10, 11],
     policies=["SEC-AUTH-001", "SEC-EXEC-001"],
     reqs=["SOC2-017", "UNB-XIN-IAM-001", "GOV-AUTH-003", "GOV-AUTH-024", "UNB-AI-STD-001", "UNB-AI-STD-003", "UNB-AGT-002", "UNB-AGT-003", "AIN-013", "AUTH-I2"],
     fresh="per-event", mech="event-driven-automated", auto="full", impl="high", rec="low",
     owner="Unassigned; proposed AI Governance owner with Security Lead",
     residual=["Prompt injection can still steer an agent within its granted authority.",
               "Model providers' own staff and systems are outside Echelon's identity controls."],
     challenge={
         "customer_intent": "Make sure AI agents cannot do more than the humans they serve, and that someone can be held responsible.",
         "adverse_outcome": "An agent with shared or excessive credentials moves money, exports data or escalates privilege, with no attributable actor.",
         "conventional_control_effectiveness": "Conventional IAM treats agents as service accounts with static broad permissions, which fails to bound per-user authority and enables confused-deputy attacks.",
         "legally_required": "Not specifically regulated in the US for this use; the EU AI Act may impose obligations depending on classification, not established here.",
         "contractually_required": "Emerging in enterprise AI addenda.",
         "historical_convention": "None; questionnaires are just adding agent identity questions.",
         "architectural_elimination": "Self-escalation can be eliminated by making authority grants a command class agents are never authorized to issue (A5) and enforcing it in the deterministic authorization core.",
         "automatic_enforcement": "Delegated grants computed as a subset of the parent; tool broker removes tools; emergency stop as a platform command.",
         "continuous_evidence": "Every agent action carries principal, delegation chain, policy version and tools available.",
         "stronger_alternative": "Per-agent principals with delegation chains and deterministic enforcement, independent of model behavior.",
         "alternative_verifiable": "Yes, by negative tests (AUTH-T01, AUTH-T08) and inspection of action records.",
         "customer_acceptance_likelihood": "Uncertain; technically strong, but regulated customers have little precedent for evaluating agent identity and may restrict agents to read-only regardless.",
         "invalidating_conditions": "If any agent path writes directly to the database (prohibited by GOV-AUTH-023) or reuses a human session token.",
         "conventional_cost": "Low but ineffective.",
         "alternative_cost": "High upfront engineering.",
         "alternative_risks": "Complexity in the delegation model may itself contain authorization defects.",
         "supporting_arguments": ["Deterministic enforcement does not depend on the model behaving.", "Delegation chains preserve accountability to a human."],
         "opposing_arguments": ["Prompt injection operates within granted authority, so bounding authority does not prevent misuse of what is granted.", "No independent standard yet exists for auditors to test against."],
         "technical_effectiveness": "stronger",
         "institutional_acceptance": "uncertain"})

C.au(8, "Customer administrator delegation and customer-side user management",
     "Customer administration and delegation",
     "The customer needs to manage its own users and administrators safely, delegate limited administration, and recover administrative control without vendor staff granting it unilaterally.",
     "proposed-target-state",
     "UNB-XIN-IAM-001 defines realms including SponsorWorkforce and PartnerWorkforce; UNB-TEN-010 states partner preferences cannot override sponsor reserved authority; CNV-GOV-006 requires delegated customer roles to expire on events with risk-based recertification; GOV-AUTH-015 requires expiring, revocable delegation. Not implemented.",
     "Sponsor administrators manage their own users within the SponsorWorkforce realm and may delegate administration of defined scopes (program, partner, function) to sub-administrators. No administrator can grant a permission they do not hold or assign sponsor-reserved authority. Distribution-partner administrators manage only PartnerWorkforce users for their partner and cannot administer sponsor-reserved functions. Changes to administrator roles require step-up authentication and, for the top administrative tier, a second sponsor approver. Delegated roles expire and are recertified. If a customer loses all administrators, recovery requires verified authorization from the customer's designated officers through an out-of-band, identity-proofed procedure with a waiting period and notification to all prior administrators; vendor staff cannot grant administrative rights on their own.",
     "Not implemented. Requirements exist.",
     "Implement delegated administration with subset-only grants and an administrator recovery procedure.",
     "Requirement text only.",
     "Echelon's Unbound design lets sponsors manage and delegate their own administration, prevents any administrator from granting more than they hold, separates partner administration from sponsor-reserved functions, and requires a verified customer-authorized procedure to recover lost administrator access. This is planned, not operating.",
     "planned",
     controls=[12], evrs=[12],
     policies=["SEC-AUTH-001"],
     reqs=["UNB-XIN-IAM-001", "UNB-TEN-010", "CNV-GOV-006", "GOV-AUTH-015", "UNB-XIN-IAM-003", "UNB-XIN-IAM-004"],
     fresh="per-event", mech="event-driven-automated", auto="high", impl="medium", rec="low",
     residual=["Administrator recovery is a social-engineering target; the procedure's strength depends on the identity proofing of customer officers."],
     oq=["What artifact proves that a person is an authorized officer of a sponsor for administrator recovery (board resolution, signatory list)?"])

C.au(9, "Identity lifecycle for donors, advisors and partner-federated users",
     "Customer identity lifecycle",
     "The customer needs account-holder identities to be proofed at onboarding, mapped stably across federation, kept separate across roles, and suspended correctly at death, incapacity or partner exit.",
     "proposed-target-state",
     "CNV-PLT-003 (risk-based proofing, no KBA), UNB-XIN-IAM-001 (one realm per principal; separate principals per sponsor), UNB-RCN-ENT-004 (suspend rights and agents on death or incapacity in one transaction), AUTH-I5 (unauthenticated death notice is a flag), UNB-XIN-SAS-007 (sponsor-direct credential before partner federation ends) specify the target. Not implemented.",
     "Donors and advisors are identity-proofed by a risk-based process that validates core attributes against authoritative sources, matches the funding account owner, and steps up to document verification or a non-biometric alternative when needed; knowledge-based questions are never used for proofing. Each person has one principal per sponsor and per realm; a staff member who is also a donor has two principals linked only by an audited link that confers no privilege. On verified death or incapacity, all rights, sessions and delegated agent principals derived from that person are suspended in one transaction; an unverified notice only holds new actions. Users federated through a distribution partner are offered a sponsor-direct authenticator at first login so they keep access to their funds if the partner relationship ends.",
     "Not implemented. Requirements exist.",
     "Implement realms, proofing workflow, lifecycle events and sponsor-direct enrollment.",
     "Requirement text only.",
     "Echelon's Unbound design proofs donor and advisor identities without knowledge-based questions, keeps roles and sponsors in separate identities, suspends all derived access at verified death or incapacity, and keeps donors' access to their funds if a distribution partner exits. This is planned, not operating.",
     "planned",
     controls=[13], evrs=[13],
     reqs=["CNV-PLT-003", "UNB-XIN-IAM-001", "UNB-RCN-ENT-004", "AUTH-I5", "AUTH-I3", "UNB-XIN-SAS-007", "CNV-ENT-001"],
     fresh="per-event", mech="event-driven-automated", auto="high", impl="medium", rec="medium",
     residual=["Identity proofing vendors introduce their own data handling and accuracy risks.",
               "Synthetic identities can pass attribute validation."])

# ---------------- Controls ----------------
C.ctl(1, "Authoritative workforce identity with role-bundle provisioning",
      "Grant workforce access only through approved role bundles in a single identity provider tied to an engagement record with end date.",
      "preventive-procedural", "L3-restricted-interface", ["not yet assigned (workforce IdP)"], evrs=[1],
      related=["SOC2-010", "UNB-CTRL-004"],
      refs=[d("SRC-AICPA-TSC", "CC6.2"), d("SRC-NIST-SP800-53-R5", "AC-2"), d("SRC-CIS-CONTROLS-V8.1", "6.1"), d("SRC-ISO-27002-2022", "5.18"), d("SRC-NIST-CSF-2.0", "PR.AA-01")])
C.ctl(2, "Event-driven deprovisioning and dormant account disablement",
      "Revoke all access on termination or role change through federation and automated tasks for non-federated systems, revoke old access before granting new on transfer, and disable dormant accounts.",
      "corrective", "L9-runtime-monitored", ["not yet assigned"], evrs=[2],
      related=["CNV-GOV-004", "TVR-SEC-008", "AUTH-I6"],
      refs=[d("SRC-NIST-SP800-53-R5", "PS-4"), d("SRC-NIST-SP800-53-R5", "PS-5"), d("SRC-CIS-CONTROLS-V8.1", "6.2"), d("SRC-CIS-CONTROLS-V8.1", "5.3"), s("SRC-PCI-DSS-4.0.1", "Req 8.2.6", "informed-by")])
C.ctl(3, "Recertification campaigns with independent reviewers and automatic suspension",
      "Recertify privileged, workforce and delegated customer access on schedule, prevent self-certification, reconcile review population to the system of record, and suspend uncertified access automatically.",
      "detective-automated", "L9-runtime-monitored", ["not yet assigned"], evrs=[3],
      related=["UNB-XIN-IAM-004", "GOV-AUTH-025", "UNB-CTRL-006"],
      refs=[d("SRC-NIST-SP800-53-R5", "AC-6(7)"), d("SRC-NYDFS-PART-500", "500.7", "informed-by"), s("SRC-PCI-DSS-4.0.1", "Req 7.2.4", "informed-by"), s("SRC-AICPA-TSC", "CC6.3")])
C.ctl(4, "Just-in-time privileged elevation with second-person approval",
      "Eliminate standing production administrative access; require separate privileged principals, AAL3-grade authenticators and second-person approval for time-bound elevation.",
      "preventive-gate", "L3-restricted-interface", ["not yet assigned"], evrs=[4],
      policies=["SEC-AUTH-001"], related=["CNV-PLT-010", "UNB-XIN-IAM-001", "CNV-PLT-003"],
      refs=[d("SRC-NIST-SP800-53-R5", "AC-6(5)"), d("SRC-CIS-CONTROLS-V8.1", "5.4"), d("SRC-ISO-27002-2022", "8.2"), s("SRC-NIST-SP800-207", "Section 2.1", "informed-by")],
      cwe=["CWE-269", "CWE-250"])
C.ctl(5, "Least-privilege database grants for application identities",
      "Ensure application database roles have INSERT and constrained SELECT on authoritative event and journal tables and no UPDATE, DELETE, TRUNCATE or destructive DDL, declared in Strata and drift-checked.",
      "preventive-structural", "L3-restricted-interface", ["Strata (grant declaration and drift comparison; pilot)", "PostgreSQL privilege system"], evrs=[5],
      policies=["SEC-DB-001", "SEC-AUTH-001"], related=["CNV-ARC-004", "UNB-TEC-STRATA-004"],
      refs=[d("SRC-NIST-SP800-53-R5", "AC-6"), s("SRC-OWASP-ASVS", rel="informed-by")],
      cwe=["CWE-269"],
      residual=["Superuser and owner roles bypass privileges; these are break-glass only by design."])
C.ctl(6, "Sealed, two-person, time-limited break-glass with tenant notification",
      "Ensure emergency access is independent of the workforce IdP, two-person activated, expires within four hours, is limited to protective and recovery actions, and notifies affected tenants within one hour.",
      "preventive-gate", "L3-restricted-interface", ["not yet assigned"], evrs=[6],
      related=["UNB-XIN-IAM-005", "CNV-PLT-007"],
      refs=[s("SRC-NIST-SP800-53-R5", "AC-2(2)"), s("SRC-ISO-27002-2022", "8.2")])
C.ctl(7, "Customer-approved operator access delegation with transparency log",
      "Deny vendor staff access to tenant non-public data except under a sponsor-approved, scoped, expiring delegation or per-case approval, and publish every access to the tenant within 15 minutes.",
      "preventive-structural", "L3-restricted-interface", ["not yet assigned (Unbound authorization core)"], evrs=[7],
      policies=["SEC-AUTH-001"], related=["UNB-XIN-IAM-002", "CNV-ARC-002", "UNB-CTRL-007"],
      refs=[s("SRC-ISO-27017", "CLD.12.1.5", "informed-by"), s("SRC-ISO-27018", rel="informed-by"), s("SRC-NIST-SP800-53-R5", "AC-3")])
C.ctl(8, "Workload identity federation and managed secrets",
      "Ensure workloads obtain short-lived credentials by federation, any static secret is stored in a managed store and rotated, workload identities cannot log in interactively, and secrets in code are blocked.",
      "preventive-structural", "L3-restricted-interface", ["not yet assigned", "Gitleaks or equivalent secret scanning (proposed)"], evrs=[8],
      policies=["SEC-CRYPTO-001"], related=["UNB-XIN-IAM-001"],
      refs=[d("SRC-CIS-CONTROLS-V8.1", "5.5"), s("SRC-PCI-DSS-4.0.1", "Req 8.6.1", "informed-by"), d("SRC-NIST-SP800-53-R5", "IA-9"), s("SRC-GITLEAKS", rel="informed-by")],
      cwe=["CWE-798"])
C.ctl(9, "Workload and service account inventory",
      "Maintain a generated inventory of every workload identity with owner, purpose, permissions and credential type, reviewed with human access.",
      "detective-automated", "L6-automated-analysis", ["not yet assigned"], evrs=[9],
      refs=[d("SRC-CIS-CONTROLS-V8.1", "5.5"), d("SRC-NIST-CSF-2.0", "PR.AA-01")])
C.ctl(10, "Per-agent principals with derived, bounded delegation",
      "Give each AI agent a distinct Workload principal whose delegated authority is computed as a subset of the delegating principal's authority, ends with the parent, and excludes authority-changing command classes.",
      "preventive-structural", "L2-type-system", ["not yet assigned (Unbound authorization core)"], evrs=[10],
      policies=["SEC-AUTH-001"], related=["SOC2-017", "GOV-AUTH-003", "UNB-CTRL-064", "AUTH-I2"],
      refs=[d("SRC-OWASP-LLM-TOP10-2025", "LLM06:2025", "informed-by"), s("SRC-OWASP-AGENTIC-AI", rel="informed-by"), s("SRC-NIST-CSF-2.0", "PR.AA-05")],
      cwe=["CWE-269", "CWE-441"],
      notes="L2 is the target: delegation types that cannot represent a grant exceeding the parent. Not implemented.")
C.ctl(11, "Agent tool broker and emergency stop",
      "Remove prohibited tools from agents at the broker rather than by instruction, and provide a global and per-tenant emergency stop that parks queued agent actions.",
      "preventive-structural", "L3-restricted-interface", ["not yet assigned"], evrs=[11],
      related=["UNB-AGT-003", "GOV-AUTH-024"],
      refs=[s("SRC-OWASP-AGENTIC-AI", rel="informed-by"), s("SRC-NIST-AI-600-1", rel="informed-by")])
C.ctl(12, "Subset-only delegated administration and verified administrator recovery",
      "Prevent any administrator from granting permissions beyond their own or assigning sponsor-reserved authority; require step-up and second approver for top-tier admin changes; recover lost administration only through a customer-authorized, identity-proofed, waiting-period procedure.",
      "preventive-structural", "L3-restricted-interface", ["not yet assigned"], evrs=[12],
      policies=["SEC-AUTH-001"], related=["UNB-TEN-010", "GOV-AUTH-015"],
      refs=[s("SRC-NIST-SP800-53-R5", "AC-2"), s("SRC-ISO-27002-2022", "5.18")], cwe=["CWE-269"])
C.ctl(13, "Realm-separated principals, risk-based proofing and lifecycle suspension",
      "Ensure one principal per realm and sponsor, risk-based identity proofing without knowledge-based questions, transactional suspension of derived access on verified death or incapacity, and sponsor-direct authenticator enrollment for federated users.",
      "preventive-structural", "L3-restricted-interface", ["not yet assigned"], evrs=[13],
      related=["CNV-PLT-003", "UNB-XIN-IAM-001", "UNB-RCN-ENT-004"],
      refs=[d("SRC-NIST-SP800-63-4", "SP 800-63A"), s("SRC-NIST-SP800-53-R5", "IA-12"), s("SRC-NIST-CSF-2.0", "PR.AA-02")])

# ---------------- Evidence ----------------
C.evr(1, "Provisioning request and approval log",
      "Per grant: requester, approver, role bundle, target, timestamp; reconciled to identity provider state.",
      "not yet assigned", "event-driven-automated", "per-event", fmt="JSON Lines", prov=["request id", "approver", "role bundle version"], disc="auditor-only")
C.evr(2, "Deprovisioning timeliness report",
      "For each departure or role change, time from engagement end or change to access removal per system, with exceptions.",
      "not yet assigned", "periodic-automated", "P30D", fmt="JSON plus summary", prov=["engagement record id", "system", "removal timestamp"], disc="customer-only")
C.evr(3, "Recertification campaign record",
      "Population snapshot with count reconciled to source, reviewer decisions, self-review blocks, suspensions and remediation.",
      "not yet assigned", "periodic-automated", "P90D", fmt="JSON plus Folio report", prov=["campaign id", "population hash", "reviewer", "decision time"], disc="customer-only")
C.evr(4, "Privileged elevation and session log",
      "Every elevation request, approver, scope, duration and session activity, stored where the elevated principal cannot alter it.",
      "not yet assigned", "event-driven-automated", "per-event", fmt="Append-only log", prov=["principal", "approver", "start", "end", "commands"], signing="Tamper-evident chain (proposed)", disc="auditor-only")
C.evr(5, "Database grant declaration and drift report",
      "Declared grants per role and Strata comparison with the live database before each deployment.",
      "Strata (pilot tool; exists, not operated for production)", "event-driven-automated", "per-event", fmt="Strata report", prov=["artifact hash", "database", "Strata version"], disc="customer-only")
C.evr(6, "Break-glass activation record and tenant notices",
      "Activation approvals, scope, duration, actions, security owner page, tenant notifications and post-use review.",
      "not yet assigned", "event-driven-automated", "per-event", fmt="JSON plus case record", prov=["activators", "tenant ids", "notice timestamps"], disc="customer-only")
C.evr(7, "Access transparency log",
      "Customer-visible record of each operator access: who, when, scope, reason, case, delegation, records touched.",
      "not yet assigned (Unbound authorization core)", "continuous-automated", "P1D", fmt="Tenant-scoped view and export", prov=["operator principal", "delegation id", "record ids"], disc="customer-only")
C.evr(8, "Secret scanning and credential age report",
      "Secret scanning results per commit and age of any static credential in the secret store.",
      "not yet assigned", "event-driven-automated", "per-event", fmt="JSON", prov=["commit hash", "scanner version"], disc="internal")
C.evr(9, "Workload identity inventory export",
      "Generated list of workload identities with owner, permissions, credential type and last use.",
      "not yet assigned", "periodic-automated", "P30D", fmt="JSON", prov=["generation time", "source commit"], disc="customer-only")
C.evr(10, "Agent action records with delegation chain",
      "Per agent action: agent principal, owner, delegating principal chain, policy version, authority tier, tools available, decision.",
      "not yet assigned", "event-driven-automated", "per-event", fmt="Append-only events", prov=["agent principal", "delegation chain", "policy version"], disc="customer-only")
C.evr(11, "Emergency stop test and activation record",
      "Results of periodic emergency stop tests and any real activations with queued-action disposition.",
      "not yet assigned", "periodic-automated", "P90D", fmt="Test report", prov=["test id", "build", "outcome"], disc="customer-only")
C.evr(12, "Customer administrator change and recovery log",
      "Administrator grants, delegations, step-up events, second approvals and any recovery procedure with notices.",
      "not yet assigned", "event-driven-automated", "per-event", fmt="Tenant-scoped events", prov=["actor", "approver", "step-up event id"], disc="customer-only")
C.evr(13, "Identity lifecycle event log",
      "Proofing outcomes (without raw documents), realm links, death or incapacity flags and verified suspensions, federation-exit enrollments.",
      "not yet assigned", "event-driven-automated", "per-event", fmt="Tenant-scoped events", prov=["principal", "event type", "evidence reference"], disc="customer-only")

# ---------------- Questions ----------------
C.q(1, "Describe how workforce access to systems holding customer data is requested, approved and provisioned, including how least privilege is applied.",
    "Staff receive excessive or unapproved access.",
    [d("SRC-AICPA-TSC", "CC6.2"), d("SRC-NIST-SP800-53-R5", "AC-2"), d("SRC-CIS-CONTROLS-V8.1", "6.1"), d("SRC-ISO-27002-2022", "5.18"), s("SRC-SA-SIG"), s("SRC-CSA-CAIQ-V4", "IAM domain"), s("SRC-EDUCAUSE-HECVAT")],
    cls="contractual-common", imp="high", ind=ALL, jur=GLOBAL, prod=ORGALL,
    alts=["Is there a formal user access provisioning process?", "How are user access rights approved?"])
C.q(1, "How quickly is all access revoked when an employee or contractor leaves, including involuntary terminations, and can you show evidence for recent departures?",
    "Departed personnel retain access and misuse it.",
    [d("SRC-NIST-SP800-53-R5", "PS-4"), d("SRC-CIS-CONTROLS-V8.1", "6.2"), d("SRC-AICPA-TSC", "CC6.2"), s("SRC-VSA-CORE"), s("SRC-SA-SIG")],
    cls="contractual-common", imp="critical", ind=ALL, jur=GLOBAL, prod=ORGALL,
    alts=["What is your SLA for removing access for terminated users?"])
C.q(1, "When a staff member changes roles or moves between customer teams, is their previous access removed before new access is granted?",
    "Access accumulates across role changes, enabling toxic combinations or cross-customer access.",
    [d("SRC-NIST-SP800-53-R5", "PS-5"), e("SRC-ECH-UNB-BASELINE", "CNV-GOV-004"), s("SRC-ISO-27002-2022", "5.18")],
    cls="industry-convention", imp="medium", ind=FS, jur=USF, prod=ORGALL)
C.q(1, "Is all workforce access driven from one authoritative identity source so that a single deprovisioning action removes access everywhere, including cloud consoles, source control, support tools and third-party portals such as bank or custodian portals?",
    "Accounts in systems outside federation survive deprovisioning.",
    [e("SRC-ECH-UNB-BASELINE", "AUTH-I6"), e("SRC-ECH-UNB-BASELINE", "TVR-SEC-008"), s("SRC-CIS-CONTROLS-V8.1", "6.7"), d("SRC-NIST-CSF-2.0", "PR.AA-01")],
    cls="customer-preference", imp="high", ind=FS, jur=USF, prod=ORGALL)
C.q(1, "How do you detect and disable dormant, orphaned or shared workforce accounts?",
    "Unused accounts are taken over without anyone noticing.",
    [d("SRC-CIS-CONTROLS-V8.1", "5.3"), s("SRC-NIST-SP800-53-R5", "AC-2(3)"), s("SRC-PCI-DSS-4.0.1", "Req 8.2.6", "informed-by"), s("SRC-MITRE-ATTACK", "T1078")],
    cls="industry-convention", imp="medium", ind=ALL, jur=GLOBAL, prod=ORGALL)
C.q(1, "How is access for contractors, consultants and temporary staff controlled, and does it expire automatically at the end of the engagement?",
    "Non-employee access persists after the engagement ends.",
    [s("SRC-NIST-SP800-53-R5", "AC-2"), s("SRC-ISO-27002-2022", "5.18"), s("SRC-INTERAGENCY-TPRM-2023", rel="informed-by")],
    cls="contractual-common", imp="medium", ind=ALL, jur=GLOBAL, prod=ORG)

C.q(2, "How often do you review user access to systems that store or process customer data, who performs the review, and what was the outcome of the last review?",
    "Inappropriate access persists undetected.",
    [d("SRC-NIST-SP800-53-R5", "AC-6(7)"), d("SRC-NYDFS-PART-500", "500.7", "informed-by"), s("SRC-PCI-DSS-4.0.1", "Req 7.2.4", "informed-by"), s("SRC-AICPA-TSC", "CC6.3"), s("SRC-SA-SIG"), s("SRC-CSA-CAIQ-V4", "IAM domain")],
    cls="contractual-common", imp="high", ind=ALL, jur=GLOBAL, prod=ORGALL,
    alts=["Are user access reviews performed at least quarterly for privileged users?", "Provide evidence of the most recent user access recertification."])
C.q(2, "Can a reviewer certify their own access, and how do you prevent access reviews from being approved without scrutiny?",
    "Reviews are rubber-stamped or self-approved and provide no real assurance.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-004"), s("SRC-NIST-SP800-53-R5", "AC-5"), s("SRC-COSO-2013", rel="informed-by")],
    cls="industry-convention", imp="medium", ind=FS, jur=USF, prod=ORGALL)
C.q(2, "What happens to access that is not recertified by the review deadline?",
    "Non-response is treated as approval and stale access remains.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-004"), s("SRC-NIST-SP800-53-R5", "AC-2")],
    cls="customer-preference", imp="medium", ind=FS, jur=USF)
C.q(2, "Do your access reviews include third-party authority registers that can move money or assets, such as bank-portal users and custodian trading authorities?",
    "A person removed from the platform still holds authority at the bank or custodian.",
    [e("SRC-ECH-UNB-BASELINE", "AUTH-I6"), e("SRC-ECH-UNB-BASELINE", "TVR-SEC-008"), s("SRC-FFIEC-AUTH-GUIDANCE-2021", rel="informed-by")],
    cls="customer-preference", imp="high", ind=DAF + ["banking"], jur=USF)
C.q(2, "Are delegated customer roles such as advisors, authorized viewers and AI agents included in periodic recertification, and how often?",
    "Delegated advisory and viewing rights persist long after the relationship ends.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-004"), e("SRC-ECH-UNB-BASELINE", "CNV-GOV-006"), s("SRC-NIST-CSF-2.0", "PR.AA-05")],
    cls="customer-preference", imp="medium", ind=DAF + ["wealth-management"], jur=USF)

C.q(3, "How do you restrict and monitor privileged access to production infrastructure, cloud consoles and databases?",
    "Privileged credentials are misused or stolen, defeating all other controls.",
    [d("SRC-NIST-SP800-53-R5", "AC-6(5)"), d("SRC-ISO-27002-2022", "8.2"), d("SRC-AICPA-TSC", "CC6.1"), d("SRC-NYDFS-PART-500", "500.7", "informed-by"), s("SRC-SA-SIG"), s("SRC-CSA-CAIQ-V4", "IAM domain")],
    cls="contractual-common", imp="critical", ind=ALL, jur=GLOBAL, prod=ORGALL,
    alts=["Describe your privileged access management solution and process."])
C.q(3, "Do administrators use separate privileged accounts that are distinct from their everyday accounts and from any customer accounts they may hold?",
    "Phishing or malware on an everyday account yields administrative access.",
    [d("SRC-CIS-CONTROLS-V8.1", "5.4"), e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-001"), s("SRC-NIST-SP800-53-R5", "AC-6(2)")],
    cls="industry-convention", imp="high", ind=ALL, jur=GLOBAL, prod=ORGALL)
C.q(3, "Is standing privileged access to production eliminated in favor of just-in-time, time-bound elevation approved by a second person?",
    "Standing privilege is always available to an attacker who compromises the account.",
    [e("SRC-ECH-UNB-BASELINE", "CNV-PLT-010"), s("SRC-NIST-SP800-207", "Section 2.1", "informed-by"), s("SRC-NIST-SP800-53-R5", "AC-6")],
    cls="customer-preference", imp="high", ind=BANK + ["enterprise-software"], jur=USF, prod=ORGALL)
C.q(3, "Are privileged sessions and commands logged in a place the privileged user cannot modify or delete?",
    "An administrator erases evidence of misuse.",
    [d("SRC-NIST-SP800-53-R5", "AC-6(9)"), s("SRC-NIST-SP800-53-R5", "AU-9"), e("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-006")],
    cls="contractual-common", imp="high", ind=ALL, jur=GLOBAL, prod=ORGALL)
C.q(3, "How many people currently can obtain administrative access to the production environment and to the production database, and how is each justified?",
    "Too many people hold the ability to access or alter all customers' data.",
    [s("SRC-NIST-SP800-53-R5", "AC-6"), s("SRC-INTERAGENCY-TPRM-2023", rel="informed-by")],
    cls="customer-preference", imp="medium", ind=BANK, jur=USF, prod=ORGALL, disc="nda")
C.q(3, "Can your application's own database credentials update or delete posted financial records, or are authoritative records append-only at the database privilege level?",
    "A compromised application or insider alters financial history through the application's own credentials.",
    [e("SRC-ECH-UNB-BASELINE", "CNV-PLT-010"), e("SRC-ECH-SCS-0.1", "SEC-DB-001"), s("SRC-NIST-SP800-53-R5", "AC-6"), s("SRC-COSO-2013", rel="informed-by")],
    cls="customer-preference", imp="high", ind=FS, jur=USF,
    note="Design is described in unbound@9b38de47:architecture/TENANT-AWARE-PERSISTENCE-DESIGN.md (append-only physical enforcement); not implemented.")

C.q(4, "Do you have an emergency (break-glass) access procedure for production, and how is it controlled and audited?",
    "Emergency access becomes an unmonitored back door.",
    [s("SRC-NIST-SP800-53-R5", "AC-2(2)"), s("SRC-ISO-27002-2022", "8.2"), e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-005"), s("SRC-SA-SIG")],
    cls="industry-convention", imp="high", ind=ALL, jur=GLOBAL, prod=ORGALL)
C.q(4, "Are emergency credentials independent of your primary identity provider, so that an identity provider outage or compromise neither locks you out nor grants an attacker emergency access?",
    "A single identity provider failure causes total lockout or total compromise.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-005"), s("SRC-FFIEC-BCM-BOOKLET", rel="informed-by"), s("SRC-MITRE-ATTACK", "T1556")],
    cls="customer-preference", imp="medium", ind=BANK + ["enterprise-software"], jur=USF, prod=ORGALL)
C.q(4, "What actions are allowed under emergency access, and can emergency access be used to approve grants, change payees or bank details, change authority or post ledger entries?",
    "Emergency access is used to move money or alter records.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-005"), e("SRC-ECH-UNB-BASELINE", "CNV-PLT-007"), s("SRC-NIST-SP800-53-R5", "AC-5")],
    cls="customer-preference", imp="high", ind=DAF + ["banking"], jur=USF)
C.q(4, "Will you notify us when emergency access touches our tenant, and how quickly?",
    "The customer is unaware that its data was accessed under emergency conditions.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-005"), s("SRC-CIRN-RULE-2021", rel="informed-by")],
    cls="contractual-common", imp="medium", ind=BANK + DAF, jur=USF)
C.q(4, "How often do you test the break-glass procedure, and when was it last used in a real event?",
    "Emergency access fails when needed, or is used more often than disclosed.",
    [s("SRC-NIST-SP800-34-R1", rel="informed-by"), s("SRC-FFIEC-BCM-BOOKLET", rel="informed-by")],
    cls="customer-preference", imp="low", ind=BANK, jur=USF, prod=ORGALL, disc="nda")

C.q(5, "Under what circumstances can your staff access our data in production, and do we approve that access in advance?",
    "Vendor staff browse or alter customer data without customer knowledge.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-002"), e("SRC-ECH-UNB-BASELINE", "CNV-ARC-002"), s("SRC-ISO-27018", rel="informed-by"), s("SRC-AICPA-TSC", "CC6.1"), s("SRC-SA-SIG"), s("SRC-CSA-CAIQ-V4", "IAM domain")],
    cls="contractual-common", imp="critical", ind=FS, jur=USF,
    alts=["Which vendor employees can access customer data, and under what controls?", "Is customer approval required before support personnel access our environment?"])
C.q(5, "Can we see a log of every access by your staff to our data, including the reason and the records touched, and how soon after the access does it appear?",
    "The customer cannot verify vendor claims about limited access.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-002"), s("SRC-ISO-27017", "CLD.12.4.5", "informed-by"), s("SRC-NIST-SP800-53-R5", "AU-6")],
    cls="customer-preference", imp="high", ind=BANK + DAF, jur=USF)
C.q(5, "Can your support staff impersonate or 'view as' one of our users, and what can they do while doing so?",
    "Impersonation features let support staff or attackers act as donors or advisors.",
    [e("SRC-ECH-UNB-BASELINE", "TVR-SEC-007"), s("SRC-OWASP-CHEATSHEETS", rel="informed-by"), s("SRC-MITRE-ATTACK", "T1078")],
    cls="customer-preference", imp="high", ind=DAF + ["wealth-management"], jur=USF)
C.q(5, "Can your staff perform decisions reserved to us as the sponsor, such as approving grants, changing payees, changing authority or closing funds?",
    "The vendor exercises the sponsor's legal authority, undermining the sponsor's control of charitable assets.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-002"), s("SRC-IRC-4966", rel="informed-by"), s("SRC-NIST-SP800-53-R5", "AC-5")],
    cls="contractual-common", imp="critical", ind=DAF, jur=USF,
    oq=["Does vendor ability to execute sponsor decisions have tax or legal implications for the sponsor's exclusive legal control? Counsel review needed."])
C.q(5, "Do any offshore staff, subcontractors or affiliates have access to our data, and how is their access restricted and monitored?",
    "Data accessed from jurisdictions or by parties the customer has not approved.",
    [s("SRC-INTERAGENCY-TPRM-2023", rel="informed-by"), s("SRC-FFIEC-OUTSOURCING-BOOKLET", rel="informed-by"), s("SRC-GDPR", rel="informed-by")],
    cls="contractual-common", imp="high", ind=FS, jur=USF + ["EU"], prod=ORGALL)

C.q(6, "How do you inventory and manage service accounts, API keys and other machine credentials?",
    "Unmanaged machine credentials are leaked or abused.",
    [d("SRC-CIS-CONTROLS-V8.1", "5.5"), s("SRC-PCI-DSS-4.0.1", "Req 8.6.1", "informed-by"), d("SRC-NIST-SP800-53-R5", "IA-9"), s("SRC-CSA-CAIQ-V4", "IAM domain"), s("SRC-SA-SIG")],
    cls="industry-convention", imp="high", ind=ALL, jur=GLOBAL, prod=ALLP,
    alts=["Describe the controls over non-human or system accounts."])
C.q(6, "Are service credentials short-lived and obtained through workload identity federation, or are they long-lived static secrets, and how are any static secrets rotated?",
    "Long-lived static secrets leak through code, logs or CI and remain valid.",
    [e("SRC-ECH-SCS-0.1", "SEC-CRYPTO-001"), s("SRC-NIST-SP800-53-R5", "IA-5"), s("SRC-OWASP-CHEATSHEETS", rel="informed-by"), s("SRC-MITRE-ATTACK", "T1552")],
    cls="customer-preference", imp="high", ind=ENT, jur=GLOBAL, prod=ALLP)
C.q(6, "Can service accounts be used for interactive login, and how is that prevented and detected?",
    "Attackers or staff use service accounts to evade individual accountability.",
    [s("SRC-PCI-DSS-4.0.1", "Req 8.6.1", "informed-by"), s("SRC-NIST-SP800-53-R5", "AC-2"), s("SRC-MITRE-ATTACK", "T1078")],
    cls="industry-convention", imp="medium", ind=ALL, jur=GLOBAL, prod=ALLP)
C.q(6, "Does each application component connect to the database with its own least-privilege role, and are any components able to connect as a database owner or superuser?",
    "A compromise of any component yields full database control.",
    [e("SRC-ECH-SCS-0.1", "SEC-DB-001"), e("SRC-ECH-UNB-BASELINE", "UNB-TEN-005"), s("SRC-NIST-SP800-53-R5", "AC-6"), s("SRC-CIS-BENCHMARKS", rel="informed-by")],
    cls="customer-preference", imp="high", ind=FS, jur=USF)
C.q(6, "How are your CI/CD pipeline identities scoped, can the pipeline deploy to production without human approval, and are package publishing credentials stored as long-lived tokens?",
    "A compromised pipeline or publishing token pushes malicious code to production or to downstream consumers.",
    [s("SRC-SLSA", rel="informed-by"), s("SRC-NIST-SP800-218", rel="informed-by"), e("SRC-ECH-UNB-BASELINE", "CNV-PLT-010"), s("SRC-OPENSSF-SCORECARD", rel="informed-by")],
    cls="customer-preference", imp="high", ind=ENT, jur=GLOBAL, prod=ALLP)

C.q(7, "Does each AI agent operating in your product or environment have its own distinct identity, rather than using a human user's session or a shared service account?",
    "Agent actions cannot be attributed or bounded, and shared credentials give agents excess authority.",
    [e("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-017"), e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-001"), e("SRC-ECH-UNB-BASELINE", "AIN-013"), s("SRC-OWASP-AGENTIC-AI", rel="informed-by"), s("SRC-CSA-AICM", rel="informed-by")],
    cls="customer-preference", imp="high", ind=ALL, jur=GLOBAL, prod=ALLP,
    alts=["How are non-human identities, including AI agents, authenticated and authorized?"])
C.q(7, "Can an AI agent grant itself new permissions, approve its own actions, change its own authority policy or clear its own alerts?",
    "An agent escalates its own privileges, either through defect or manipulation.",
    [e("SRC-ECH-UNB-BASELINE", "GOV-AUTH-003"), e("SRC-ECH-UNB-BASELINE", "UNB-AI-STD-003"), d("SRC-OWASP-LLM-TOP10-2025", "LLM06:2025", "informed-by")],
    cls="customer-preference", imp="critical", ind=FS, jur=USF, prod=ALLP)
C.q(7, "When an AI agent acts on behalf of a user, is the agent's authority limited to a subset of that user's authority, and is the delegation chain recorded on each action?",
    "An agent acts beyond the delegating user's rights (confused deputy), or actions cannot be traced to the responsible human.",
    [e("SRC-ECH-UNB-BASELINE", "AUTH-I2"), e("SRC-ECH-UNB-BASELINE", "UNB-AI-STD-001"), s("SRC-MITRE-CWE", "CWE-441", "informed-by"), s("SRC-OWASP-AGENTIC-AI", rel="informed-by")],
    cls="customer-preference", imp="high", ind=FS, jur=USF, prod=ALLP)
C.q(7, "How are AI agent permissions enforced: by the platform removing tools and denying actions, or by instructions in the agent's prompt?",
    "Prompt-only restrictions are bypassed by prompt injection or model error.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-AGT-003"), d("SRC-OWASP-LLM-TOP10-2025", "LLM01:2025", "informed-by"), s("SRC-MITRE-ATLAS", rel="informed-by")],
    cls="customer-preference", imp="high", ind=ALL, jur=GLOBAL, prod=ALLP)
C.q(7, "How quickly can you suspend all AI agent activity across the platform or for a single customer, and what happens to actions the agents had queued?",
    "A misbehaving agent cannot be stopped before causing harm, or stopping it corrupts in-flight work.",
    [e("SRC-ECH-UNB-BASELINE", "GOV-AUTH-024"), e("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-017"), s("SRC-NIST-AI-RMF-1.0", rel="informed-by")],
    cls="customer-preference", imp="high", ind=FS, jur=USF)
C.q(7, "Do AI coding or operations agents used by your engineers have access to production systems, production credentials or customer data, and how is the identity of those agents established?",
    "An engineering agent with production access exfiltrates data or makes unreviewed changes; its identity is only self-declared.",
    [s("SRC-NIST-SP800-218A", rel="informed-by"), s("SRC-OWASP-AGENTIC-AI", rel="informed-by"), e("SRC-ECH-UNB-BASELINE", "CNV-PLT-010")],
    cls="customer-preference", imp="high", ind=ALL, jur=GLOBAL, prod=ALLP)
C.q(7, "Are AI agent identities included in your access reviews, and are they deprovisioned when an agent is retired or its owner leaves?",
    "Orphaned agent identities retain access indefinitely.",
    [e("SRC-ECH-UNB-SOC2-DIRECTIVE", "SOC2-010"), e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-004"), s("SRC-NIST-CSF-2.0", "PR.AA-01")],
    cls="customer-preference", imp="medium", ind=ALL, jur=GLOBAL, prod=ALLP)

C.q(8, "Can our administrators provision, modify and deprovision our own users, and can they delegate administration of a subset of users or functions to sub-administrators?",
    "The customer depends on the vendor for routine access changes, delaying removals.",
    [s("SRC-NIST-SP800-53-R5", "AC-2"), s("SRC-ISO-27017", "CLD.6.3.1", "informed-by"), s("SRC-EDUCAUSE-HECVAT"), s("SRC-CSA-CAIQ-V4", "IAM domain")],
    cls="customer-preference", imp="high", ind=ENT + ["higher-education"], jur=GLOBAL,
    alts=["Does the product support delegated administration?"])
C.q(8, "Can a customer administrator grant a role or permission more privileged than their own, or assign authority that is reserved to the sponsor?",
    "Privilege escalation through the delegated administration feature.",
    [s("SRC-MITRE-CWE", "CWE-269", "informed-by"), e("SRC-ECH-UNB-BASELINE", "UNB-TEN-010"), s("SRC-OWASP-API-TOP10-2023", "API5:2023", "informed-by")],
    cls="customer-preference", imp="high", ind=FS, jur=USF)
C.q(8, "How do you separate the administrative rights of our staff as the sponsoring organization from those of distribution partners or channel administrators who serve our donors?",
    "A partner administrator alters sponsor policy, approvals or users outside the partner's remit.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-TEN-010"), e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-001"), e("SRC-ECH-UNB-BASELINE", "UNB-TEN-020")],
    cls="customer-preference", imp="high", ind=DAF + ["banking"], jur=USF)
C.q(8, "If all of our administrators leave or lose access, how is administrative access restored, and can your staff grant it on their own?",
    "An attacker social-engineers the vendor into granting administrative control of the customer tenant.",
    [s("SRC-NIST-SP800-63-4", "SP 800-63A", "informed-by"), s("SRC-MITRE-ATTACK", "T1098"), s("SRC-FFIEC-AUTH-GUIDANCE-2021", rel="informed-by")],
    cls="customer-preference", imp="high", ind=FS, jur=USF)
C.q(8, "Are changes to administrator roles protected by step-up authentication and notification to other administrators?",
    "A compromised administrator session silently creates additional administrators for persistence.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-003"), s("SRC-MITRE-ATTACK", "T1098"), s("SRC-NIST-SP800-53-R5", "AC-2(4)")],
    cls="customer-preference", imp="medium", ind=FS, jur=USF)

C.q(9, "How do you verify the identity of donors, fund advisors and clients when their accounts are opened, and do you use knowledge-based questions?",
    "Fraudsters open accounts under stolen or synthetic identities.",
    [d("SRC-NIST-SP800-63-4", "SP 800-63A"), e("SRC-ECH-UNB-BASELINE", "CNV-PLT-003"), s("SRC-FINCEN-CDD-RULE", rel="informed-by"), s("SRC-SEC-REG-S-ID", rel="informed-by")],
    cls="contractual-common", imp="high", ind=DAF + ["wealth-management"], jur=USF,
    note="Whether BSA/AML customer identification rules apply depends on the sponsor's and channel's regulatory status; Unbound requirements treat proofing as risk-based design, not a legal determination.")
C.q(9, "When a donor or advisor dies or becomes incapacitated, how are their access, sessions and any AI agents acting for them suspended, and how do you handle an unverified notice?",
    "A deceased person's account is used by others, or a false death notice is used to disrupt or take over an account.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-RCN-ENT-004"), e("SRC-ECH-UNB-BASELINE", "AUTH-I5"), e("SRC-ECH-UNB-BASELINE", "CNV-ENT-001")],
    cls="customer-preference", imp="high", ind=DAF + ["wealth-management"], jur=USF)
C.q(9, "If a person is both one of your staff (or one of our staff) and a donor or advisor, how do you prevent the two roles from combining privileges?",
    "A staff member uses administrative access to act on their own or a relative's fund.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-001"), s("SRC-NIST-SP800-53-R5", "AC-5"), s("SRC-IRC-4958", rel="informed-by")],
    cls="customer-preference", imp="high", ind=DAF, jur=USF)
C.q(9, "If a donor uses the platform through a distribution partner such as a bank or wealth manager, how do they keep access to their fund if that partner's relationship with the sponsor ends?",
    "Donors are locked out of their funds when partner federation ends, or regain access through a weak recovery path.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-XIN-SAS-007"), e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-001"), s("SRC-NIST-SP800-63-4", "SP 800-63C", "informed-by")],
    cls="customer-preference", imp="medium", ind=DAF + ["wealth-management", "banking"], jur=USF)

print(C.emit())
