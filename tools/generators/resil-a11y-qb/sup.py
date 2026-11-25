from rqb_common import *
c = Cat("SUP", {"industries": ["all"], "jurisdictions": ["US-federal"], "products": ["unbound"]})
OWN = "Proposed: Customer Support Lead (role not yet staffed)"
RAT = "No customers, support organization, support contract terms or ticketing system exist as of 2026-11-25."
FIN = ["banking", "financial-services", "wealth-management", "donor-advised-funds"]

e1 = c.E(1, "Support coverage schedule", "Published support hours, channels, languages, holiday and year-end coverage, and the out-of-band channel used when the platform is down.", mechanism="periodic-manual", freshness="P90D", disc="customer-only")
e2 = c.E(2, "Severity matrix and response-time performance report", "Severity definitions with examples, response and resolution targets, and monthly measured performance per customer from ticket timestamps.",
         mechanism="periodic-automated", freshness="P30D", disc="customer-only", prov=["ticket_id", "severity", "opened", "first_response", "resolved"])
e3 = c.E(3, "Escalation matrix and named contacts", "Current escalation path with named roles and people, contact methods and backup for each, reviewed quarterly.", mechanism="periodic-manual", freshness="P90D", disc="customer-only")
e4 = c.E(4, "Support access grant and session log", "For each support access to tenant data: requester, customer approval reference, scope, purpose, start and expiry, actions taken, and visibility in the customer's access view.",
         mechanism="event-driven-automated", freshness="per-event", disc="customer-only", prov=["grant_id", "tenant", "approver", "scope", "expires_at", "action_digest"], retention="P7Y")
e5 = c.E(5, "AI support agent configuration and evaluation record", "Disclosure text, permitted tools and data scopes, escalation triggers, model and prompt versions, and periodic evaluation of answer accuracy and escalation behavior.",
         mechanism="periodic-automated", freshness="P30D", disc="customer-only", prov=["agent_id", "model_version", "prompt_version", "tool_scope", "eval_run_id"])
e6 = c.E(6, "Problem management and known-error register", "Recurring incidents grouped into problems with root cause, workaround, fix status and customer communication.", mechanism="event-driven-automated", freshness="P30D", disc="customer-only")
e7 = c.E(7, "Support personnel location and subcontractor register", "Countries from which support is provided, employment versus subcontracted status, and data access each group has.", mechanism="periodic-manual", freshness="P1Y", disc="nda")

k1 = c.C(1, "Defined support coverage including peak periods", "Guarantee reachable support during business hours and for critical severity at all times, with added coverage at year-end and an out-of-band channel.",
         "administrative", "L10-external-or-manual", ["not yet assigned"], [e1], OWN, related=["UNB-XIN-SVC-008", "UNB-GAP-028"], fw=[R("SRC-ISO-20000-1")])
k2 = c.C(2, "Severity-based response targets measured from ticket data", "Classify every case by defined severity and measure response and resolution against targets automatically.",
         "detective-automated", "L9-runtime-monitored", ["not yet assigned"], [e2], OWN, related=["UNB-XIN-SVC-006", "ADM-016"])
k3 = c.C(3, "Escalation path with backup for each contact", "Ensure every escalation level resolves to a reachable person and a named backup.",
         "administrative", "L10-external-or-manual", ["not yet assigned"], [e3], OWN, related=["RR-OPS-004-r1", "UNB-XIN-CRM-005"])
k4 = c.C(4, "Customer-approved, time-boxed support access", "Deny support staff and agents access to tenant data by default; grant scoped, expiring, customer-approved access, record every action and show it in the customer's access view. Emergency access is two-person break-glass limited to read and protective actions.",
         "preventive-structural", "L3-restricted-interface", ["Unbound authorization engine (not built)", "Identity provider (not selected)"], [e4], "Proposed: Security Lead (role not yet staffed)",
         policies=["SEC-AUTH-001"], related=["UNB-XIN-IAM-005", "CNV-PLT-007", "SOC2-010"], fw=[R("SRC-AICPA-TSC", "CC6.1"), R("SRC-NIST-SP800-53-R5", "AC-6")])
k5 = c.C(5, "Bounded AI support agents with human escalation", "Disclose AI support, restrict agents to read-only knowledge and the requesting user's authorized data, forbid financial or authority actions, and route to a human on request or on defined triggers.",
         "preventive-structural", "L3-restricted-interface", ["Unbound assistance component (not built)"], [e5], OWN, related=["SOC2-017", "REQ-X-055", "REQ-X-017"],
         fw=[R("SRC-OWASP-LLM-TOP10-2025", "LLM06:2025"), R("SRC-NIST-AI-600-1", rel="informed-by")])
k6 = c.C(6, "Problem management", "Group recurring incidents into problems, track root cause and fixes, and communicate known errors to affected customers.", "corrective", "L10-external-or-manual", ["not yet assigned"], [e6], OWN, fw=[R("SRC-ISO-20000-1")])
k7 = c.C(7, "Support location and subcontracting disclosure", "Maintain and disclose where support is provided from and whether by employees or subcontractors.", "administrative", "L10-external-or-manual", ["not yet assigned"], [e7], OWN)

a1 = c.A(1, "Support hours, channels and peak coverage", "proposed-target-state", RAT,
    "Support is available during US business hours in all continental time zones for sponsor staff, with critical-severity coverage at all times. Channels include an in-product case system, email and phone, plus an out-of-band channel that works when the platform is down. Coverage increases in the final weeks of December according to a seasonal capacity plan. Echelon supports sponsor staff; donor-facing support is the sponsor's choice and Unbound provides tools for it.",
    "Not established. UNB-XIN-SVC-008 requires a seasonal capacity plan and surge playbook for live channels.",
    "Define support offering before the first contract.",
    "Nothing.",
    "We have not yet defined a support offering because we have no customers. We plan business-hours support with continuous coverage for critical issues.",
    "planned", [k1], [e1], OWN, freshness="P90D", mechanism="periodic-manual", automation="low", impl="low", rec="medium", requirements=["UNB-XIN-SVC-008", "UNB-GAP-028"])
a2 = c.A(2, "Severity definitions and response targets", "proposed-target-state", RAT,
    "Four severity levels are defined with examples tied to customer consequence (Severity 1 includes inability to approve or release grants, suspected data exposure, or incorrect balances). Response targets are contractual (for example 30 minutes for Severity 1 at any hour) and resolution targets are stated as objectives. Performance is measured from ticket timestamps and reported monthly. Customer commitments made in support cases are recorded with owners and due times.",
    "Not established.",
    "Draft severity matrix with the support offering.",
    "Nothing.",
    "We have not yet set severity levels or response targets. We plan contractual response times for critical issues.",
    "planned", [k2], [e2], OWN, freshness="P30D", mechanism="periodic-automated", automation="high", impl="low", rec="low", requirements=["UNB-XIN-SVC-006", "ADM-016"])
a3 = c.A(3, "Escalation, named contacts and coverage despite small team", "unknown",
    "Staffing is not established; a small team makes named backups for every escalation level a material open issue.",
    "Each customer has a named primary and backup contact and a documented escalation path to executive level; every level resolves to a reachable person with a named backup, enforced the same way control ownership is (owner plus backup always resolvable).",
    "Unknown. No support staff or escalation path documented.",
    "Assign named contacts and backups per customer at onboarding.",
    "Nothing.",
    "We have not yet established an escalation path. As an early-stage company we will disclose staffing and backup arrangements during contracting.",
    "planned", [k3], [e3], OWN, freshness="P90D", mechanism="periodic-manual", automation="low", impl="low", rec="medium", requirements=["RR-OPS-004-r1", "UNB-XIN-CRM-005"],
    oq=["How many people will be available for customer support at launch, and who covers when the primary is unavailable?"])
a4 = c.A(4, "Support access to customer data", "proposed-target-state", RAT,
    "Support staff and support agents have no standing access to tenant data. Access requires a case-linked request approved by the customer, is limited in scope and time, is read-only unless the customer explicitly authorizes a specific change, and is logged with every action visible in the customer's access view. Support can never move money, change payees or change authority on a customer's behalf. Emergency access is two-person break-glass, limited to read and protective actions, auto-expiring within four hours and notified to the customer immediately.",
    "Not established. UNB-XIN-IAM-005 and CNV-PLT-007 specify break-glass limits.",
    "Implement support access as a first-class authorization feature before production.",
    "Nothing.",
    "Our design gives support staff no standing access to customer data; access would require customer approval, be time-limited and be visible to the customer. Not yet built.",
    "planned", [k4], [e4], "Proposed: Security Lead (role not yet staffed)", freshness="per-event", mechanism="event-driven-automated", automation="full", impl="medium", rec="low",
    policies=["SEC-AUTH-001"], requirements=["UNB-XIN-IAM-005", "CNV-PLT-007", "SOC2-010"],
    challenge={
        "customer_intent": "Prevent vendor staff from viewing or changing our donors' data without our knowledge.",
        "adverse_outcome": "Insider snooping, unauthorized changes, or social engineering of support staff to redirect funds.",
        "conventional_control_effectiveness": "Typical answers cite background checks, confidentiality agreements and role-based access; support staff usually retain broad standing access that the customer cannot see.",
        "legally_required": "No specific rule for Echelon; GLBA safeguards and state privacy laws require customers to oversee service providers' access.",
        "contractually_required": "Common in bank and enterprise data protection addenda.",
        "historical_convention": "Vendor support logs in as admin.",
        "architectural_elimination": "Standing access is eliminated in scope; support cannot perform money or authority actions at all.",
        "automatic_enforcement": "Authorization engine enforces customer approval, scope and expiry.",
        "continuous_evidence": "Every access is an event visible to the customer.",
        "stronger_alternative": "Customer-approved just-in-time access with customer-visible logs instead of reliance on staff screening.",
        "alternative_verifiable": "Yes, by the customer directly.",
        "customer_acceptance_likelihood": "Likely.",
        "invalidating_conditions": "If database administrators or infrastructure staff retain unmonitored paths to tenant data outside the application.",
        "conventional_cost": "low", "alternative_cost": "medium",
        "alternative_risks": "Slower resolution when customers are slow to approve access.",
        "supporting_arguments": ["Customer sees exactly what support did."],
        "opposing_arguments": ["Infrastructure-level access remains and needs separate controls.", "Approval friction during urgent incidents."],
        "technical_effectiveness": "stronger", "institutional_acceptance": "likely"})
a5 = c.A(5, "AI support agents", "proposed-target-state",
    "Unbound requirements describe contextual AI assistance (REQ-X-055) but no support agent exists.",
    "Where AI agents answer support questions, users are told they are interacting with AI, can reach a human at any point, and are routed to a human automatically for financial, security, accessibility-accommodation or complaint matters. Agents can read only public documentation and the requesting user's own authorized data, cannot take financial, authority or configuration actions, and their model and prompt versions are recorded per conversation. Support conversations are not used to train third-party models, and evaluation of accuracy and escalation behavior runs on a schedule.",
    "Not established.",
    "Decide whether to use AI support agents; if so, build to this design.",
    "Nothing.",
    "We have not deployed AI support agents. If we do, we plan to disclose them, provide a path to a human, and prevent them from taking financial actions.",
    "planned", [k5], [e5], OWN, freshness="P30D", mechanism="periodic-automated", automation="high", impl="medium", rec="low", requirements=["SOC2-017", "REQ-X-055", "REQ-X-017"],
    challenge={
        "customer_intent": "Ensure automated support does not give wrong answers, leak data or take unauthorized actions, and that a human is reachable.",
        "adverse_outcome": "Donor misled about a deadline or deduction, data from another tenant disclosed, or account change made by a manipulated agent.",
        "conventional_control_effectiveness": "Disclaimers and 'AI may make mistakes' notices do little; questionnaires rarely ask what tools the agent can call.",
        "legally_required": "Partly: some US state laws and the EU AI Act impose disclosure duties for AI interacting with people; applicability to Echelon depends on deployment and jurisdiction.",
        "contractually_required": "Emerging in AI addenda.",
        "historical_convention": "Chatbots with scripted escalation.",
        "architectural_elimination": "Unauthorized actions are eliminated in scope by giving the agent no action tools; cross-tenant leakage is reduced by building context only from the requesting user's authorized data.",
        "automatic_enforcement": "Tool allowlist and tenant-bound context construction.",
        "continuous_evidence": "Per-conversation version records and scheduled evaluations.",
        "stronger_alternative": "Read-only, tenant-bound agents with mandatory human routing for consequential topics.",
        "alternative_verifiable": "Partly; evaluation results can be shared, but behavior is probabilistic.",
        "customer_acceptance_likelihood": "Uncertain; some sponsors will forbid AI support for donors.",
        "invalidating_conditions": "If agents are later given action tools without equivalent authorization checks.",
        "conventional_cost": "low", "alternative_cost": "medium",
        "alternative_risks": "Incorrect but confident answers remain possible within read-only scope.",
        "supporting_arguments": ["Removes the highest-consequence failure (unauthorized action)."],
        "opposing_arguments": ["Wrong information can still cause harm, such as a missed deduction deadline.", "Donors may prefer human support regardless."],
        "technical_effectiveness": "stronger", "institutional_acceptance": "uncertain"})
a6 = c.A(6, "Problem management, case visibility and support workforce", "proposed-target-state", RAT,
    "Recurring incidents are managed as problems with root cause and fix tracking; known errors and workarounds are published to affected customers. Customers see all their cases, history and commitments, and can export them. Support is provided by Echelon employees located in the United States unless a customer agrees otherwise; any subcontracted support is disclosed with its data access.",
    "Not established.",
    "Select a case system integrated with Unbound's case kernel; decide support workforce model.",
    "Nothing.",
    "We have not yet established problem management or a support workforce. We plan to disclose where support is provided from and by whom.",
    "planned", [k6, k7], [e6, e7], OWN, freshness="P30D", mechanism="event-driven-automated", automation="partial", impl="low", rec="low", requirements=["CNV-SVC-001", "UNB-XIN-SVC-006"])

c.Q(1, "Support hours", "What are your support hours and time zones, and is support available at all times for critical issues?",
    ["Do you offer 24x7 support?"],
    "Critical issues outside business hours need a response.", "Severe outage on a weekend with no support.",
    [R("SRC-ISO-20000-1"), R("SRC-EDUCAUSE-HECVAT"), R("SRC-SA-SIG")], "contractual-common", "high")
c.Q(1, "Support channels", "Which support channels do you offer, and how do we reach you if your platform, email or phone system is down?",
    ["How do we contact support during an outage?"],
    "Support channels hosted on the failed platform are unusable.", "Cannot report or track an outage.",
    [R("SRC-ISO-20000-1"), R("SRC-NIST-SP800-53-R5", "CP-8", rel="informed-by")], "customer-preference", "medium")
c.Q(1, "Peak-period coverage", "Do you increase support capacity during our peak periods, such as the last weeks of December?",
    ["How do you staff support at year-end?"],
    "Support demand spikes with giving volume.", "Long queues when donors and staff need help most.",
    [UNB], "customer-preference", "high", industries=["donor-advised-funds", "nonprofit", "wealth-management"])
c.Q(1, "End-user support", "Do you support our end users, such as donors and advisors, directly, or only our staff, and can you do so under our brand?",
    ["Will your support team speak to our donors?"],
    "Customers must know who answers end users and how.", "Donors receive inconsistent or unauthorized answers.",
    [UNB], "customer-preference", "medium", industries=["donor-advised-funds", "wealth-management"])
c.Q(2, "Severity definitions", "How do you define severity levels, and what determines the severity of an issue we report?",
    ["Provide your incident priority matrix."],
    "Severity drives response; vendor-only classification can downgrade urgent issues.", "Critical issue treated as routine.",
    [R("SRC-ISO-20000-1"), R("SRC-NIST-SP800-61-R3", rel="informed-by")], "contractual-common", "high")
c.Q(2, "Response and resolution targets", "What are your response and resolution targets for each severity, and are they contractual?",
    ["What is your guaranteed response time for a critical issue?"],
    "Without targets, urgent issues can wait indefinitely.", "Prolonged unresolved critical issues.",
    [R("SRC-ISO-20000-1"), R("SRC-INTERAGENCY-TPRM-2023")], "contractual-common", "high")
c.Q(2, "Measured support performance", "Do you measure and report how well you meet support targets, and what has your recent performance been?",
    ["Provide support SLA attainment for the last quarter."],
    "Targets matter only if met.", "Chronic misses go unnoticed.",
    [R("SRC-ISO-20000-1")], "customer-preference", "medium", note="No support history exists.")
c.Q(3, "Escalation", "What is the escalation path if an issue is not progressing, and who are the named people at each level?",
    ["Provide your escalation matrix."],
    "Stalled issues need a route to decision makers.", "Critical issue stuck at front-line support.",
    [R("SRC-ISO-20000-1"), R("SRC-INTERAGENCY-TPRM-2023")], "contractual-common", "high")
c.Q(3, "Named account contact", "Will we have a named customer success or technical account contact, and who covers when that person is unavailable?",
    ["Do you assign a dedicated account manager?"],
    "Continuity of relationship and context speeds resolution.", "No one with context available during an incident.",
    [UNB], "customer-preference", "medium")
c.Q(3, "Small-team coverage", "Given the size of your team, how do you ensure someone qualified responds to a critical issue when key staff are on leave, ill or already engaged in another incident?",
    ["How many people can resolve a production issue?"],
    "Small vendors may have one person able to fix critical issues.", "No qualified responder available.",
    [R("SRC-INTERAGENCY-TPRM-2023"), BP], "customer-preference", "high", products=["echelon-organization", "unbound"])
c.Q(4, "Support access to data", "Can your support staff see our data, and if so, which data, under what conditions, and how is that access approved?",
    ["Do support personnel have access to client data?"],
    "Support access is a common path for insider misuse and social engineering.", "Unauthorized viewing of donor data.",
    [R("SRC-AICPA-TSC", "CC6.1"), R("SRC-GLBA", rel="informed-by"), R("SRC-INTERAGENCY-GLBA-SAFEGUARDS", rel="informed-by"), R("SRC-CSA-CAIQ-V4"), R("SRC-SA-SIG")],
    "supervisory-guidance", "high", industries=FIN, authority="Federal banking agencies (for bank customers)")
c.Q(4, "Customer-approved and visible access", "Is our approval required before support accesses our tenant, is that access time-limited, and can we see a log of what support did?",
    ["Can we audit vendor support access?"],
    "Customers need control and visibility of vendor access.", "Vendor access invisible to customer.",
    [R("SRC-ISO-27018", rel="informed-by"), R("SRC-NIST-SP800-53-R5", "AC-6"), UNB], "customer-preference", "high")
c.Q(4, "Support changes on customer's behalf", "Can support staff change our data or perform transactions on our behalf, for example updating a payee, releasing a grant or resetting an approver's access?",
    ["Can support make changes in our account?"],
    "Social engineering of support to redirect funds is a known attack.", "Fraudulent payee change via support request.",
    [R("SRC-NACHA-RULES", rel="informed-by"), R("SRC-FFIEC-AUTH-GUIDANCE-2021"), UNB], "customer-preference", "critical", industries=["donor-advised-funds", "banking", "financial-services"])
c.Q(5, "AI support disclosure", "Do you use AI agents to answer support requests from our staff or end users, and is that disclosed to the person?",
    ["Will our users interact with a chatbot?"],
    "Users and customers want to know when they deal with AI.", "Undisclosed AI responses in regulated communications.",
    [R("SRC-EU-AI-ACT", "Article 50", rel="informed-by"), R("SRC-US-STATE-AI-LAWS", rel="informed-by"), R("SRC-NIST-AI-600-1", rel="informed-by")], "customer-preference", "medium",
    juris=["US-states", "EU"])
c.Q(5, "AI support authority", "What data can AI support agents read, and can they take any action in the system, such as changing settings or initiating transactions?",
    ["What tools does your support bot have access to?"],
    "Agents with tools can be manipulated by prompt injection.", "Agent takes unauthorized action or discloses another customer's data.",
    [R("SRC-OWASP-LLM-TOP10-2025", "LLM06:2025"), R("SRC-OWASP-AGENTIC-AI", rel="informed-by"), SOC2D], "customer-preference", "high")
c.Q(5, "Human escalation", "How can a user reach a human when AI support is not adequate, and which topics always go to a human?",
    ["Is there always a path to a live person?"],
    "Some issues require human judgment and accountability.", "User trapped in automated loop on a financial or accessibility issue.",
    [R("SRC-NIST-AI-RMF-1.0", rel="informed-by"), R("SRC-COLORADO-AI-ACT", rel="informed-by")], "customer-preference", "medium", juris=["US-states"])
c.Q(5, "Support data and AI training", "Are support conversations or tickets used to train or improve AI models, yours or a third party's?",
    ["Do you use our support interactions to train AI?"],
    "Support content contains confidential and personal data.", "Customer data incorporated into third-party models.",
    [R("SRC-NIST-AI-600-1", rel="informed-by"), R("SRC-GDPR", rel="informed-by")], "customer-preference", "high", juris=["US-federal", "EU"])
c.Q(6, "Problem management", "How do you identify and fix the root causes of recurring issues, and do you tell customers about known problems and workarounds?",
    ["Do you have a problem management process?"],
    "Recurring issues indicate unresolved defects.", "Same failure repeatedly affects customers.",
    [R("SRC-ISO-20000-1"), R("SRC-NIST-CSF-2.0", "ID.IM-01", rel="informed-by")], "industry-convention", "medium")
c.Q(6, "Case visibility", "Can we see all our open and closed support cases, their history and any commitments you made, and export them?",
    ["Do you provide a customer support portal?"],
    "Customers need a record of vendor commitments and responses.", "Disputes over what was promised.",
    [UNB], "customer-preference", "low")
c.Q(6, "Support workforce location", "Where are your support personnel located, are any of them subcontractors, and does any support occur outside the United States?",
    ["Is support offshored?"],
    "Location affects data transfer, legal access and oversight.", "Undisclosed offshore access to customer data.",
    [R("SRC-INTERAGENCY-TPRM-2023"), R("SRC-GDPR", "Art. 28", rel="informed-by"), R("SRC-SA-SIG")], "contractual-common", "medium", juris=["US-federal", "EU"])
c.write()
