from devseclib import *

c = Cat("API")
T = lambda n: f"SRC-OWASP-API-TOP10-2023@API{n}:2023!"
V4 = "SRC-OWASP-ASVS@5.0 V4 API and Web Service"
V8 = "SRC-OWASP-ASVS@5.0 V8 Authorization"
V9 = "SRC-OWASP-ASVS@5.0 V9 Self-contained Tokens"
V10 = "SRC-OWASP-ASVS@5.0 V10 OAuth and OIDC"
B = lambda i: f"SRC-ECH-UNB-BASELINE@{i}!"
FIN = ["financial-services", "banking", "wealth-management", "donor-advised-funds"]
UNB = ["unbound"]

# evidence
c.E("authz", "Object, property and function authorization negative test results",
    "For every API operation, automated negative tests that call it as another tenant, another user in the same tenant, a lower role and an AI agent principal, asserting denial; plus tests that responses omit properties the caller is not entitled to and that writes ignore or reject unauthorized properties.",
    mechanism="event-driven-automated", fmt="Test results plus operation-by-principal coverage matrix",
    prov=["commit", "API contract version", "operation", "principal type", "result"])
c.E("cred", "API credential inventory and lifecycle records",
    "Inventory of partner and service API credentials with owner, tenant binding, scopes, creation, last use, expiry and rotation events; credential secrets stored only as hashes or in a managed secret store.",
    mechanism="continuous-automated", freshness="P1D", fmt="JSON inventory plus lifecycle events",
    prov=["credential identifier (not secret)", "owner", "tenant", "scopes", "event timestamp", "actor"])
c.E("rate", "Rate limit and business-flow limit configuration and test results",
    "Configured per-principal, per-tenant and per-operation request limits and business-flow limits (for example recipients created per day, grant splitting thresholds), with load and abuse test results.",
    mechanism="event-driven-automated", fmt="Configuration export plus test results", prov=["commit", "environment", "limit set version"])
c.E("contract", "Contract conformance and API inventory check",
    "Per-build comparison of the deployed API surface against authoritative OpenAPI and event contracts: undocumented operations, schema drift, unversioned changes, deprecated versions still served, with schema validation enforcement confirmed.",
    mechanism="event-driven-automated", fmt="JSON diff report", prov=["build digest", "contract version", "deployed schema hash"])
c.E("webhook", "Webhook signature, replay and delivery records",
    "Per-event records of signature verification result, timestamp tolerance, deduplication decision and delivery outcome for inbound and outbound webhooks, plus replay and tampering test results.",
    mechanism="event-driven-automated", fmt="Event log entries plus test report", prov=["event identifier", "partner", "signature key identifier", "verification result", "timestamp"])
c.E("idem", "Idempotency and duplicate-effect test results",
    "Tests that replay, retry and concurrently submit mutating requests with the same and different idempotency keys and payloads, asserting a single effect, stable responses and conflict on key reuse with a different payload; plus production reconciliation of effects to keys.",
    mechanism="event-driven-automated", fmt="Test results plus reconciliation report", prov=["commit", "operation", "case", "result"])
c.E("apicfg", "API security configuration baseline snapshot",
    "Captured TLS configuration, CORS policy, security headers, debug and introspection endpoints status and error format for each deployed API host.",
    mechanism="periodic-automated", freshness="P1D", fmt="JSON snapshot", prov=["host", "deployment identifier", "capture timestamp"])

# controls
c.C("authz", "Central deny-by-default authorization for every API operation",
    "Evaluate object, property and function authorization on the server for every request through one policy point covering humans, institutions and agent principals; deny when no rule grants access.",
    "preventive-structural", "L3-restricted-interface", ["Unbound authorization model (not built)"], ["authz"],
    policies=["SEC-AUTH-001"], related=["UNB-CTRL-067"], requirements=["UNB-API-003", "UNB-API-005"], cwe=["CWE-639", "CWE-285", "CWE-863", "CWE-213"],
    refs=[T(1), T(3), T(5), V8, "SRC-ECH-SCS-0.1@SEC-AUTH-001!"])
c.C("authztest", "Generated cross-tenant and cross-role negative tests",
    "Generate negative tests from the API contract and authorization matrix so every operation is exercised by unauthorized principals on every build.",
    "detective-automated", "L7-property-tested", ["Unbound test suite (not built)"], ["authz"], cwe=["CWE-639", "CWE-285"], refs=[T(1), "SRC-NIST-IR-8397"])
c.C("cred", "Scoped, rotatable, tenant-bound partner credentials",
    "Issue partner and service credentials bound to one tenant and least-privilege scopes, with expiry, rotation without downtime, hashed storage, last-use tracking and immediate revocation; prefer sender-constrained tokens (mTLS or proof-of-possession) for high-risk operations.",
    "preventive-structural", "L3-restricted-interface", ["Identity provider (not chosen)", "Unbound API gateway (not built)"], ["cred"],
    policies=["SEC-CRYPTO-001", "SEC-AUTH-001"], requirements=["UNB-API-STD-005"], cwe=["CWE-287", "CWE-798", "CWE-522"],
    refs=[T(2), V9, V10, B("UNB-API-STD-005")])
c.C("rate", "Rate and business-flow limits",
    "Limit request rates and resource consumption per principal, tenant and operation, and limit sensitive business flows by count and value independent of request rate.",
    "preventive-structural", "L9-runtime-monitored", ["Unbound API gateway (not built)"], ["rate"], requirements=["UNB-API-STD-003", "TVR-SEC-004"],
    cwe=["CWE-770", "CWE-799", "CWE-307"], refs=[T(4), T(6), B("UNB-API-STD-003")])
c.C("contract", "Contract-first schema validation and inventory",
    "Generate or verify the API surface from authoritative contracts, reject requests and responses that do not validate, fail builds on undocumented operations, and keep an inventory of versions, hosts and consumers with deprecation dates.",
    "preventive-gate", "L5-build-release-gate", ["Unbound contract tooling (not built)", "Praxis CI workflow (exists for tool repositories)"], ["contract"],
    requirements=["UNB-API-STD-001", "UNB-API-STD-003", "UNB-API-STD-006"], cwe=["CWE-20", "CWE-1059"], refs=[T(9), V4, B("UNB-API-STD-006")])
c.C("webhook", "Signed, replay-safe webhooks and event intake",
    "Sign outbound events and verify inbound ones with per-partner rotating keys, enforce timestamp windows and event-identifier deduplication, validate payload schemas, and deliver only to verified destinations through the egress control.",
    "preventive-structural", "L3-restricted-interface", ["Unbound integration layer (not built)"], ["webhook"],
    requirements=["UNB-API-006", "UNB-EVT-003", "UNB-API-STD-005"], cwe=["CWE-345", "CWE-347", "CWE-294", "CWE-918"],
    refs=[T(10), T(7), B("UNB-API-006")])
c.C("idem", "Idempotency keys on every mutating command",
    "Require a client-supplied idempotency key on every mutating operation, persist it with a payload hash and result in the same transaction as the effect, return the stored result on retry, reject key reuse with a different payload, and carry external idempotency keys to payment rails.",
    "preventive-structural", "L2-type-system", ["Unbound command layer (not built)"], ["idem"],
    requirements=["UNB-API-004", "UNB-IMM-006", "UNB-EVT-002"], cwe=["CWE-837", "CWE-362"], refs=[B("UNB-API-004"), B("UNB-IMM-006")])
c.C("apicfg", "Hardened API configuration baseline",
    "Enforce TLS-only, a restrictive CORS policy, no debug or introspection endpoints in production, uniform error format and security headers, checked continuously against a baseline.",
    "detective-automated", "L9-runtime-monitored", ["Hosting edge (not chosen)"], ["apicfg"], cwe=["CWE-16", "CWE-942", "CWE-215"], refs=[T(8), V4])
c.C("agentapi", "Requests-not-approvals boundary for external and agent callers",
    "Expose external and AI agent write operations only as requests that enter governed approval workflows; no external or agent credential can approve sponsor-reserved decisions, move money or post to the ledger.",
    "preventive-structural", "L3-restricted-interface", ["Unbound API and tool broker (not built)"], ["authz"],
    requirements=["UNB-API-002", "UNB-API-STD-004", "UNB-AGT-002", "UNB-AGT-003"], cwe=["CWE-269", "CWE-284"],
    refs=[B("UNB-API-STD-004"), B("UNB-AGT-002"), "SRC-OWASP-AGENTIC-AI"])

# answer units
a1 = c.A("API object, property and function level authorization",
    "Sponsors need assurance that an API caller can only reach the records, fields and functions it is entitled to, never another sponsor's or donor's data.",
    "Every API operation passes through one deny-by-default policy point that checks tenant, object ownership, property entitlement and function permission for humans, institutions and agent principals alike. Negative tests generated from the contract and authorization matrix exercise every operation as every unauthorized principal type on every build, and the coverage matrix is part of release evidence.",
    ["authz", "authztest", "agentapi"], ["authz"], policies=["SEC-AUTH-001"], requirements=["UNB-API-003", "UNB-API-005", "UNB-IMM-009"],
    mechanism="event-driven-automated", impl="high", rec="low", products=UNB)
a2 = c.A("API authentication and partner API key management",
    "Partners and sponsors need assurance that API credentials are strong, scoped, bound to the right tenant, rotatable and quickly revocable.",
    "Partner and service integrations authenticate with tenant-bound, least-privilege credentials issued through a managed identity provider, preferably OAuth client credentials with sender-constrained tokens (mutual TLS or DPoP) for money-relevant operations; static API keys, where a partner requires them, are scoped, expiring, stored only as hashes, rotatable without downtime and visible with last-use data to the sponsor. Revocation takes effect within minutes and is evidenced.",
    ["cred"], ["cred"], policies=["SEC-CRYPTO-001", "SEC-AUTH-001"], requirements=["UNB-API-STD-005", "UNB-API-003"],
    mechanism="continuous-automated", freshness="P1D", impl="medium", rec="low", products=UNB,
    oq=["Which identity provider and token format will Unbound use? Not chosen."],
    challenge=ch(
        customer_intent="Ensure only the intended partner system can act through the API, and that a leaked credential has limited and short-lived value.",
        adverse_outcome="Stolen partner key used to read donor data or submit fraudulent requests.",
        conventional_control_effectiveness="Static bearer API keys with periodic rotation are common but leak through logs, repositories and partner systems; rotation schedules rarely limit real exposure.",
        legally_required="No specific mechanism is mandated; FFIEC authentication guidance and GLBA safeguards expect risk-appropriate authentication.",
        contractually_required="Partners often ask for API keys and fixed rotation periods.",
        historical_convention="Long-lived API key plus IP allowlist plus 90-day rotation.",
        architectural_elimination="Sender-constrained tokens make a stolen token useless without the private key; short-lived tokens limit replay.",
        automatic_enforcement="Gateway rejects unbound or expired tokens; credential inventory alerts on unused or overdue credentials.",
        continuous_evidence="Credential inventory with last-use and scope, revocation events.",
        stronger_alternative="OAuth client credentials with mTLS or DPoP binding and short token lifetimes.",
        alternative_verifiable="Yes, configuration and token validation tests are reproducible.",
        customer_acceptance_likelihood="Likely for technically mature partners; smaller partners may lack mTLS or DPoP support.",
        invalidating_conditions="A fallback static key path left enabled for all partners.",
        conventional_cost="Low implementation, recurring rotation coordination.", alternative_cost="Higher partner onboarding effort and certificate management.",
        alternative_risks="Certificate lifecycle failures cause outages.",
        supporting_arguments=["Removes the value of leaked credentials.", "Aligns with OAuth security best practice."],
        opposing_arguments=["Partner capability varies; dual paths increase complexity."],
        technical_effectiveness="stronger", institutional_acceptance="likely"))
a3 = c.A("Rate limiting, resource consumption and sensitive business flows",
    "Customers need assurance that APIs cannot be overwhelmed or used to automate abuse of legitimate functions.",
    "Requests are limited per principal, tenant and operation with explicit responses and retry guidance; expensive queries are bounded by page size and complexity; sensitive flows (new recipients, grant recommendations, credential resets, exports) carry count and value limits that defeat splitting regardless of request rate. Limits are configured as code, tested under load and monitored.",
    ["rate"], ["rate"], requirements=["UNB-API-STD-003", "TVR-SEC-004"], mechanism="continuous-automated", freshness="P1D", impl="medium", rec="low", products=UNB)
a4 = c.A("API schema validation, inventory and versioning",
    "Customers need assurance that every exposed API is known, documented, validated and changed predictably.",
    "API and event descriptions are generated from or verified against authoritative contracts; requests and responses are validated against schemas; builds fail on undocumented operations or unversioned breaking changes; an inventory records every version, host and consumer; supported public APIs receive 18 months' notice before breaking change (CNV-EXP-001) with documented emergency exceptions.",
    ["contract"], ["contract"], requirements=["UNB-API-STD-001", "UNB-API-STD-003", "UNB-API-STD-006", "UNB-API-008"],
    mechanism="event-driven-automated", impl="medium", rec="low", products=UNB,
    current="Unbound has five illustrative OpenAPI documents treated as design references only (UNB-API-008); no implemented API exists.")
a5 = c.A("Webhooks, inbound events and consumption of third-party APIs",
    "Partners need assurance that events sent and received are authentic, untampered, processed once and cannot be abused to reach internal systems.",
    "Outbound webhooks are signed with per-partner rotating keys and include timestamps and event identifiers; inbound events are verified, checked against a replay window, deduplicated, schema-validated and treated as untrusted data that cannot by itself grant sponsor approval. Responses from third-party APIs are validated like user input, called with timeouts and circuit breakers, and only over TLS to approved hosts.",
    ["webhook"], ["webhook"], requirements=["UNB-API-006", "UNB-EVT-003", "UNB-API-STD-005"], mechanism="event-driven-automated", impl="medium", rec="low", products=UNB)
a6 = c.A("Idempotency keys and duplicate effect prevention",
    "Sponsors need assurance that retries, network failures and replays cannot duplicate grants, payments or postings.",
    "Every mutating API command requires an idempotency key persisted with a payload hash and the result in the same transaction as the effect. Retries return the stored result; reuse with a different payload is rejected; external effects carry their own idempotency keys to rails and partners; replay of history never re-issues external effects; production effects are reconciled to keys.",
    ["idem"], ["idem"], requirements=["UNB-API-004", "UNB-IMM-006", "UNB-EVT-002", "UNB-RES-002"], mechanism="event-driven-automated", impl="medium", rec="low", products=UNB,
    challenge=ch(
        customer_intent="Never pay twice and never lose an instruction.",
        adverse_outcome="Duplicate disbursement or grant through a client retry or replayed request.",
        conventional_control_effectiveness="Many platforms rely on manual reconciliation and duplicate-detection reports after the fact.",
        legally_required="No statute requires idempotency keys; Nacha rules and sponsor fiduciary duties make duplicate payments costly.",
        contractually_required="Partners increasingly expect idempotent APIs; not usually a contract term.",
        historical_convention="Duplicate payment review and reconciliation exceptions.",
        architectural_elimination="Duplicate effects from retries are eliminated within the command layer when key, payload hash and effect share a transaction; external rails still need their own keys and reconciliation.",
        automatic_enforcement="Command layer rejects missing keys; database uniqueness enforces single use.",
        continuous_evidence="Reconciliation of effects to keys; test results per build.",
        stronger_alternative="Transactional idempotency plus rail-level keys plus reconciliation, instead of detection only.",
        alternative_verifiable="Yes through concurrency and replay tests.",
        customer_acceptance_likelihood="Likely; reconciliation remains expected.",
        invalidating_conditions="Any side effect performed outside the transaction that records the key, or a rail without idempotency support.",
        conventional_cost="Ongoing manual reconciliation.", alternative_cost="Moderate design effort.",
        alternative_risks="Key retention windows shorter than retry windows.",
        supporting_arguments=["Prevents rather than detects duplicate payments."],
        opposing_arguments=["Does not cover rails that lack idempotency; reconciliation is still required."],
        technical_effectiveness="stronger", institutional_acceptance="likely"))
a7 = c.A("API security configuration and agent callers",
    "Customers need assurance that APIs are deployed securely and that automated or AI callers cannot exceed their authority.",
    "API hosts serve TLS only, expose no debug or introspection endpoints, apply a restrictive CORS policy and uniform error format, and are checked daily against a baseline. External and AI agent callers can only submit requests into governed workflows: they cannot approve sponsor-reserved decisions, initiate money movement, modify authoritative events or grant privileges, and each operation publishes a machine-readable contract stating permitted actor types and human approval boundaries.",
    ["apicfg", "agentapi"], ["apicfg", "authz"], requirements=["UNB-API-002", "UNB-API-STD-004", "UNB-AGT-002", "UNB-AGT-003"],
    mechanism="periodic-automated", freshness="P1D", impl="medium", rec="low", products=UNB)

Q = c.Q
# a1 (7)
Q(a1, "BOLA", "How does every API operation verify that the caller is entitled to the specific object identified in the request, and how is this tested for every endpoint?",
  "Broken object level authorization exposes other customers' records by changing an identifier.", [T(1), V8, "SRC-MITRE-CWE@CWE-639!"], imp="critical",
  alt=["Can a user access another user's data by modifying an ID in the API request?"])
Q(a1, "Tenant isolation in APIs", "Can an API credential issued to one sponsor or partner ever return or modify data belonging to another sponsor, including through search, export, bulk or reporting endpoints?",
  "Cross-tenant exposure through aggregate or bulk endpoints.", [T(1), B("UNB-API-005"), B("UNB-IMM-009")], imp="critical", ind=FIN)
Q(a1, "BOPLA", "Do API responses return only the properties the caller is entitled to see, and are writes restricted to properties the caller may change?",
  "Excessive data exposure and mass assignment through object properties.", [T(3), "SRC-MITRE-CWE@CWE-213!", "SRC-MITRE-CWE@CWE-915!"], imp="high")
Q(a1, "BFLA", "How are administrative and privileged API functions separated from ordinary functions, and how do you test that lower-privilege callers cannot invoke them?",
  "Broken function level authorization lets ordinary users invoke administrative operations.", [T(5), V8, "SRC-MITRE-CWE@CWE-285!"], imp="high")
Q(a1, "Agent principals", "Do AI agents and automated integrations call the API under their own identities with their own authorization rules, or do they borrow user or service credentials?",
  "Agents act with borrowed authority that cannot be bounded or attributed.", [B("UNB-API-003"), "SRC-OWASP-AGENTIC-AI", "SRC-ECH-UNB-SOC2-DIRECTIVE@SOC2-017!"], imp="high")
Q(a1, "Authorization model", "Is API authorization deny-by-default and enforced at one central point, or implemented separately in each endpoint handler?",
  "Inconsistent per-endpoint checks leave gaps.", ["SRC-ECH-SCS-0.1@SEC-AUTH-001!", V8, "SRC-NIST-SP800-53-R5@AC-3"], imp="medium")
Q(a1, "Identifier design", "Are object identifiers exposed in APIs unguessable, and do you rely on that unguessability for any access decision?",
  "Security through obscure identifiers fails once identifiers leak.", [T(1), "SRC-MITRE-CWE@CWE-639!"], imp="low")
# a2 (6)
Q(a2, "API authentication", "What authentication methods does the API support for partner systems, and which are permitted for operations that affect money or donor data?",
  "Weak API authentication allows impersonation of partner systems.", [T(2), V10, "SRC-FFIEC-AUTH-GUIDANCE-2021"], imp="critical", ind=FIN,
  alt=["How are API clients authenticated?"])
Q(a2, "Partner API keys", "How are partner API keys issued, scoped, stored, rotated and revoked, and can a sponsor see which keys exist for its tenant and when each was last used?",
  "Unmanaged or overprivileged keys persist after a partner relationship changes.", [T(2), B("UNB-API-STD-005"), "SRC-NIST-SP800-53-R5@IA-5"], imp="high", ind=FIN)
Q(a2, "Token binding", "Are access tokens sender-constrained (mutual TLS or proof of possession) or plain bearer tokens, and what are their lifetimes?",
  "Stolen bearer tokens are replayed from anywhere.", [V9, V10, T(2)], imp="medium")
Q(a2, "Credential leakage", "How do you detect and respond to a partner credential that appears in a public repository, log or ticket?",
  "Leaked credentials remain valid until noticed.", ["SRC-GITLEAKS", "SRC-ECH-SCS-0.1@SEC-CRYPTO-001!", T(2)], imp="medium")
Q(a2, "Token validation", "How does the API validate tokens (issuer, audience, signature algorithm, expiry), and is the algorithm fixed server-side?",
  "Algorithm confusion or missing audience checks accept forged tokens.", [V9, "SRC-MITRE-CWE@CWE-347!"], imp="medium")
Q(a2, "Brute force", "How are API authentication endpoints protected against credential stuffing and brute force?",
  "Automated guessing compromises accounts.", [T(2), "SRC-MITRE-CWE@CWE-307!"], imp="medium")
# a3 (5)
Q(a3, "Rate limiting", "Do you enforce rate limits on API endpoints, at what granularity (user, client, tenant, IP), and what response does a caller receive when limited?",
  "Unlimited requests exhaust capacity or enable scraping.", [T(4), B("UNB-API-STD-003"), "SRC-MITRE-CWE@CWE-770!"], imp="high",
  alt=["Is API throttling in place?"])
Q(a3, "Resource consumption", "How do you bound expensive API operations such as large exports, searches, report generation and document rendering so one caller cannot degrade service for others?",
  "Noisy neighbor or deliberate exhaustion through expensive operations.", [T(4), "SRC-ECH-UNB-BASELINE@CNV-ARC-001!"], imp="medium")
Q(a3, "Sensitive business flows", "Which business flows are protected against automated abuse independent of request rate (for example adding payees, grant recommendations, account recovery), and what limits apply?",
  "Automated abuse of legitimate flows at rates below technical limits.", [T(6), B("TVR-SEC-004")], imp="high", ind=["donor-advised-funds", "wealth-management"])
Q(a3, "Partner-level limits", "Can sponsors or partners configure their own limits on API-originated activity (value per day, recipients per period), and are limits enforced on the server?",
  "A compromised partner integration acts without sponsor-level ceilings.", [T(6), "SRC-ECH-UNB-BASELINE@CNV-PLT-012!"], cls="customer-preference", imp="medium", ind=["donor-advised-funds"])
Q(a3, "Cost exhaustion", "Do any API calls trigger paid third-party services (identity verification, data lookups, AI models), and how do you prevent abuse that drives cost?",
  "Attackers inflict financial loss through metered downstream calls.", [T(4), "SRC-OWASP-LLM-TOP10-2025"], imp="low")
# a4 (6)
Q(a4, "Schema validation", "Are API requests validated against a published schema before processing, and are responses validated so internal fields cannot leak?",
  "Unvalidated requests reach business logic; unvalidated responses leak data.", [V4, B("UNB-API-STD-001"), T(3)], imp="high")
Q(a4, "API inventory", "Do you maintain an inventory of all API hosts, versions and environments, including deprecated and non-production endpoints reachable from the internet?",
  "Forgotten or shadow endpoints lack current protections.", [T(9), "SRC-CIS-CONTROLS-V8.1", "SRC-NIST-CSF-2.0@ID.AM"], imp="high")
Q(a4, "Versioning and deprecation", "What is your API versioning and deprecation policy, how much notice do customers receive before breaking changes, and how are emergency security changes handled?",
  "Unannounced breaking changes disrupt sponsor operations and integrations.", [B("UNB-API-STD-003"), "SRC-ECH-UNB-BASELINE@CNV-EXP-001!"], cls="contractual-common", imp="medium")
Q(a4, "Contract fidelity", "Is the published API documentation generated from or verified against the implementation, so that no undocumented operations exist?",
  "Undocumented operations escape review and testing.", [B("UNB-API-STD-006"), T(9)], imp="medium")
Q(a4, "Contract testing", "Do you run contract tests against partner integrations so schema changes on either side are detected before production?",
  "Silent schema drift corrupts data exchanged with partners.", [B("UNB-API-STD-003"), "SRC-NIST-SP800-218@PW.8"], imp="low")
Q(a4, "Sandbox", "Do you provide a non-production API environment for partner testing, and is it guaranteed to contain no real donor or financial data?",
  "Real data exposed through weaker test environments.", ["SRC-ISO-27001-2022@A.8.33", "SRC-ISO-27001-2022@A.8.31"], cls="customer-preference", imp="medium")
# a5 (5)
Q(a5, "Webhook signing", "Are webhooks you send signed, how can recipients verify them, and how are signing keys rotated?",
  "Recipients accept forged events that appear to come from the platform.", [B("UNB-API-STD-005"), B("UNB-API-006"), "SRC-MITRE-CWE@CWE-347!"], imp="high", ind=FIN)
Q(a5, "Inbound events", "How do you verify the authenticity of inbound webhooks and files from banks, custodians and partners, and can an inbound event by itself change an authoritative record or approve anything?",
  "Forged inbound events alter records or trigger effects.", [B("UNB-EVT-003"), T(10), "SRC-MITRE-CWE@CWE-345!"], imp="critical", ind=FIN)
Q(a5, "Replay defense", "What prevents a captured webhook or partner message from being replayed later?",
  "Replayed messages duplicate effects or restore stale state.", [B("UNB-API-006"), "SRC-MITRE-CWE@CWE-294!"], imp="high")
Q(a5, "Unsafe consumption", "How do you treat data returned from third-party APIs (charity data providers, identity verification, custodians): validated as untrusted input, or trusted?",
  "Compromised or faulty third-party APIs inject bad data or attacks.", [T(10), "SRC-NIST-SP800-161-R1"], imp="medium")
Q(a5, "Delivery failures", "What happens when webhook delivery fails repeatedly, and can delivery retries or redirects be used to reach unintended destinations?",
  "Retry logic follows redirects to internal hosts or floods endpoints.", [T(7), "SRC-MITRE-CWE@CWE-918!"], imp="low")
# a6 (3)
Q(a6, "Idempotency keys", "Do mutating API operations support idempotency keys, and what happens if the same key is reused with a different payload?",
  "Retries create duplicate grants, payments or postings.", [B("UNB-API-004"), B("UNB-IMM-006")], imp="critical", ind=FIN)
Q(a6, "Retry semantics", "If a client times out after submitting a payment- or grant-affecting request, how does it determine safely whether the request took effect?",
  "Uncertain outcomes lead clients to resubmit and duplicate effects.", [B("UNB-API-STD-002"), B("UNB-API-004")], imp="high", ind=FIN)
Q(a6, "Downstream idempotency", "Are idempotency guarantees carried through to banks, payment processors and partners, or do they stop at your API boundary?",
  "Duplicate effects occur downstream despite API-level idempotency.", [B("UNB-IMM-006"), "SRC-ECH-UNB-BASELINE@CNV-ARC-003!", "SRC-NACHA-RULES^"], imp="high", ind=FIN)
# a7 (3)
Q(a7, "Security misconfiguration", "How do you ensure API hosts do not expose debug endpoints, verbose errors, default credentials, permissive CORS or outdated TLS in production?",
  "Misconfiguration exposes internals or weakens transport security.", [T(8), V4, "SRC-CIS-BENCHMARKS"], imp="medium")
Q(a7, "External writes", "Can any external API call approve a grant, release a payment, post to the ledger or change permissions directly, or must it pass through an approval workflow?",
  "API access bypasses sponsor approval controls.", [B("UNB-API-STD-004"), B("UNB-API-002")], imp="critical", ind=FIN)
Q(a7, "AI callers", "When AI assistants or agents use your API, what prevents them from performing operations reserved for human approval, and is this enforced by the platform rather than by prompts?",
  "Prompt-level restrictions are bypassed through injection or model error.", [B("UNB-AGT-003"), "SRC-OWASP-LLM-TOP10-2025", "SRC-OWASP-AGENTIC-AI"], imp="high")

RECORDS = c.records()
