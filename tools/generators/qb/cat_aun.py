from lib import *

C = Category("AUN")
FFIEC = "Federal banking agencies (FFIEC member agencies)"

C.au(1, "Multi-factor authentication coverage for workforce and administrators",
     "Workforce MFA",
     "The customer needs every person who can reach its data, code or infrastructure to prove identity with more than a password.",
     "proposed-target-state",
     "CNV-PLT-003 requires AAL3-grade authenticators (hardware keys or device-bound non-exportable keys, no synced passkeys, two keys per user) for platform and sponsor privileged roles and AAL2 phishing-resistant authenticators for other workforce. SOC2-010 requires MFA. No workforce identity provider exists, so nothing is enforced.",
     "MFA is enforced at the workforce identity provider for every workforce and contractor account and every system federated to it, including email, source control, package registries, cloud consoles, CI/CD and support tools; systems that cannot federate are listed with their own MFA configuration evidence. All workforce authenticators are phishing-resistant (AAL2 minimum); platform privileged roles use AAL3-grade hardware or device-bound keys with two registered keys per person. There are no standing MFA exceptions; any temporary exception requires CISO approval, an expiry and a compensating control.",
     "Unknown for Echelon workforce systems; no evidence located. Target requirements exist in Unbound.",
     "Select a workforce IdP that enforces phishing-resistant MFA by policy and enroll all personnel before production.",
     "Requirement text only.",
     "Echelon's design requires phishing-resistant multi-factor authentication for all workforce access and hardware-backed keys for privileged roles. Enforcement through a workforce identity provider is planned; Echelon cannot yet evidence workforce MFA coverage.",
     "planned",
     controls=[1], evrs=[1],
     reqs=["CNV-PLT-003", "SOC2-010", "GOV-AUTH-006"],
     fresh="P1D", mech="continuous-automated", auto="full", impl="low", rec="low",
     residual=["Systems outside federation may retain weaker authentication."],
     oq=["Do Echelon's current source control and package publishing accounts enforce MFA today? Not verified in this review."])

C.au(2, "Phishing-resistant authenticators and resistance to MFA bypass",
     "Phishing resistance",
     "The customer needs authentication that cannot be phished, relayed or fatigued, because conventional one-time codes and push approvals are routinely bypassed.",
     "proposed-target-state",
     "CNV-PLT-003 prohibits synced passkeys for privileged roles and requires phishing-resistant authenticators for workforce; TVR-SEC-010 treats a synced passkey alone as insufficient for new recipients; CNV-PLT-011 requires accessible alternatives. Not implemented.",
     "Workforce users authenticate only with phishing-resistant authenticators (FIDO2/WebAuthn security keys or device-bound platform authenticators). Customer users are offered passkeys as the default and phishing-resistant options at no extra cost; SMS and voice codes are not offered for workforce and, for customers, are only a restricted fallback with compensating controls (cooling-off and sponsor-direct confirmation for high-risk actions). Synced passkeys are accepted for sign-in at AAL2 but are not sufficient alone for high-risk actions such as adding a new grant recipient. Push-based approval, if used, requires number matching. Session tokens are bound to the authenticated client where the platform supports it to reduce adversary-in-the-middle token theft. Accessible alternatives exist for users who cannot use device-bound authenticators.",
     "Not implemented. Requirements exist.",
     "Implement WebAuthn for all populations from the first release and treat other factors as restricted.",
     "Requirement text only.",
     "Echelon's Unbound design makes phishing-resistant authentication (security keys and passkeys) the default, restricts SMS and voice codes, and requires stronger confirmation than a synced passkey alone for high-risk actions. This is planned, not operating.",
     "planned",
     controls=[2], evrs=[2],
     reqs=["CNV-PLT-003", "TVR-SEC-010", "CNV-PLT-011", "TVR-SEC-004"],
     fresh="P1D", mech="continuous-automated", auto="high", impl="medium", rec="low",
     residual=["Session token theft by malware on the endpoint is not prevented by phishing-resistant authentication.",
               "Account recovery may reintroduce phishable factors."],
     challenge={
         "customer_intent": "Stop account takeover of donors, advisors and staff.",
         "adverse_outcome": "Phished credentials and codes are used to redirect grants or steal personal data.",
         "conventional_control_effectiveness": "Conventional MFA (SMS, voice, TOTP, push) is widely bypassed by real-time phishing proxies, SIM swaps and push fatigue; it is far better than passwords alone but not phishing-resistant.",
         "legally_required": "FTC Safeguards Rule 16 CFR 314.4(c)(5) and NYDFS 500.12 require MFA for covered entities but do not mandate phishing-resistant factors; FFIEC 2021 guidance is supervisory and risk-based.",
         "contractually_required": "Usually 'MFA' without specifying phishing resistance.",
         "historical_convention": "SMS and TOTP for customers; push for workforce.",
         "architectural_elimination": "Credential phishing and relay are eliminated in scope by origin-bound WebAuthn authenticators for any population that uses them exclusively.",
         "automatic_enforcement": "IdP policy and application configuration refuse weaker factors for workforce and for high-risk customer actions.",
         "continuous_evidence": "Authenticator type per authentication event is recorded and reportable.",
         "stronger_alternative": "Phishing-resistant by default for all populations, with restricted fallbacks guarded by cooling-off and sponsor-direct confirmation.",
         "alternative_verifiable": "Yes; authenticator registrations and policy can be shown and tested.",
         "customer_acceptance_likelihood": "Likely for workforce; uncertain for donor populations, where sponsors may resist anything that adds friction or excludes older donors.",
         "invalidating_conditions": "If SMS or email recovery can reset a phishing-resistant authenticator without step-up and cooling-off.",
         "conventional_cost": "SMS costs and fraud losses.",
         "alternative_cost": "Hardware keys for privileged staff; support cost for donor enrollment.",
         "alternative_risks": "Accessibility exclusion; lockout when devices are lost; pressure to weaken recovery.",
         "supporting_arguments": ["Origin binding defeats real-time phishing proxies.", "Aligns with NIST SP 800-63-4 and CISA guidance on phishing-resistant MFA."],
         "opposing_arguments": ["Customer populations include people without compatible devices.", "Recovery paths are the residual weak point."],
         "technical_effectiveness": "stronger",
         "institutional_acceptance": "uncertain"})

C.au(3, "Customer federation: SSO via SAML 2.0 and OpenID Connect",
     "Federation and SSO",
     "The customer needs its workforce, and partners' users, to sign in with the customer's own identity provider, under its policies, with assertions validated correctly and stable identity mapping.",
     "proposed-target-state",
     "UNB-XIN-IAM-001 provides for federated SponsorWorkforce and PartnerWorkforce realms; AUTH-I8 requires mapping by issuer plus subject or SCIM external ID, never email, with dual control on mapping changes; UNB-XIN-IAM-003 keeps step-up with a sponsor-controlled verifier. No implementation or protocol library selection exists.",
     "Unbound supports SAML 2.0 and OpenID Connect federation for sponsor and partner workforce on all plans without a surcharge. Customers can require SSO-only sign-in and disable local credentials for their realm. Assertions are validated for signature, issuer, audience, recipient, time window and replay using a maintained library, with negative tests for known assertion attacks (signature wrapping, unsigned assertions, algorithm confusion). Identities are mapped by issuer plus subject, never by email; mapping changes need dual control and notice to the affected person. A compromised partner IdP can at most sign users into that partner's realm, and cannot satisfy step-up for high-risk actions, which uses a sponsor-controlled verifier.",
     "Not implemented. Requirements exist.",
     "Select a maintained federation library; implement validation negative tests; implement realm-scoped trust per IdP.",
     "Requirement text only.",
     "Echelon's Unbound design supports SAML and OpenID Connect single sign-on, maps identities by immutable identifiers rather than email, and limits what a compromised partner identity provider can do. This is planned, not operating.",
     "planned",
     controls=[3], evrs=[3],
     policies=["SEC-AUTH-001", "SEC-DATA-001"],
     reqs=["UNB-XIN-IAM-001", "AUTH-I8", "UNB-XIN-IAM-003"],
     fresh="per-event", mech="event-driven-automated", auto="high", impl="medium", rec="low",
     residual=["Customer IdP misconfiguration (weak MFA at the IdP) is outside Echelon's control; this is a complementary user entity control."])

C.au(4, "Automated user lifecycle via SCIM and federated deprovisioning latency",
     "SCIM provisioning",
     "The customer needs user changes in its identity system to propagate automatically and promptly, so that removed users cannot keep using the platform.",
     "proposed-target-state",
     "AUTH-I8 references the SCIM external ID; TVR-WID-006 calls for a contractual maximum deprovisioning latency per partner tier; AUTH-I1 requires sessions and derived tokens to be invalidated or rechecked on authority change. Not implemented.",
     "Unbound exposes a SCIM 2.0 endpoint per customer realm, authenticated with a dedicated, scoped, rotatable credential and rate-limited, that can create, update and deactivate users and group-based role assignments but cannot create platform or sponsor-reserved privileged roles. Deactivation through SCIM revokes sessions, refresh tokens, API tokens and delegated agent grants for that principal on the next request, within a stated maximum latency that is a contractual term. Open items owned by a deactivated user (pending recommendations, approval tasks) are reassigned or held by sponsor policy, never silently executed.",
     "Not implemented. Requirements exist.",
     "Implement SCIM with scoped credentials; define and measure deprovisioning latency.",
     "Requirement text only.",
     "Echelon's Unbound design supports SCIM provisioning and promises a defined maximum time from deprovisioning in the customer's identity system to loss of all platform access. This is planned, not operating.",
     "planned",
     controls=[4], evrs=[4],
     reqs=["AUTH-I8", "TVR-WID-006", "AUTH-I1", "AUTH-I2"],
     fresh="per-event", mech="event-driven-automated", auto="full", impl="medium", rec="low",
     residual=["Customers that do not deploy SCIM rely on manual deprovisioning."],
     oq=["What deprovisioning latency will be offered contractually per partner tier (TVR-WID-006 value is open)?"])

C.au(5, "Password policy aligned to NIST SP 800-63-4 and credential storage",
     "Passwords",
     "The customer needs any remaining password use to resist guessing, stuffing and offline cracking without driving users to weak behavior.",
     "proposed-target-state",
     "No password policy exists. CNV-PLT-003 directs authenticator strength but does not set a password policy. SEC-CRYPTO-001 requires approved cryptographic libraries.",
     "Passwords are optional for customers (passkeys are the default) and not used alone for workforce. Where passwords are used, the policy follows NIST SP 800-63B-4: length-based minimums with no composition rules, a generous maximum length, screening against breached and commonly used passwords, paste and password managers allowed, no security questions, no periodic forced rotation, and forced change on evidence of compromise. Passwords are stored with a memory-hard or iterated, salted password hashing function from an approved library. Online guessing is throttled per account and per source with bot detection, designed so that throttling cannot be used to lock legitimate users out at will. Where a customer contract or PCI-scoped context requires periodic rotation, the conflict is documented and resolved by MFA rather than rotation.",
     "Unknown; no password handling exists.",
     "Implement 800-63B-4 password handling if passwords are supported at all.",
     "Nothing.",
     "Echelon plans to make passkeys the default and to follow NIST SP 800-63B-4 for any passwords: length-based rules, breached-password screening, no forced periodic rotation and strong salted hashing. Nothing is implemented yet.",
     "planned",
     controls=[5], evrs=[5],
     policies=["SEC-CRYPTO-001"],
     reqs=["CNV-PLT-003"],
     fresh="per-event", mech="event-driven-automated", auto="full", impl="low", rec="low",
     residual=["Users reuse passwords across sites; breached-password screening only catches known breaches."],
     oq=["Confirm exact numeric thresholds (minimum lengths for single-factor and multi-factor use) against the final published SP 800-63B-4 text before using them in customer materials."],
     challenge={
         "customer_intent": "Prevent password guessing and reuse attacks.",
         "adverse_outcome": "Account takeover through credential stuffing or cracked hashes.",
         "conventional_control_effectiveness": "Composition rules and forced 60 to 90 day rotation produce predictable passwords and user workarounds; NIST withdrew support for both.",
         "legally_required": "No US statute mandates composition or rotation for this context. PCI DSS 4.0.1 requires rotation or dynamic analysis only where passwords are the sole factor for in-scope systems, which Unbound is not expected to have.",
         "contractually_required": "Many bank questionnaires still ask for rotation intervals and complexity.",
         "historical_convention": "Complexity plus 90-day rotation.",
         "architectural_elimination": "Password attacks are eliminated in scope for users who use passkeys only.",
         "automatic_enforcement": "Policy is enforced in code; breached-password screening at set time.",
         "continuous_evidence": "Configuration and test results show policy; share of passwordless users is measurable.",
         "stronger_alternative": "Passwordless by default; 800-63B-4 rules where passwords remain; MFA everywhere.",
         "alternative_verifiable": "Yes, by configuration review and tests.",
         "customer_acceptance_likelihood": "Likely when the answer cites NIST SP 800-63B-4 explicitly; some assessors with legacy checklists will record an exception.",
         "invalidating_conditions": "If passwords are the only factor for any population.",
         "conventional_cost": "Help-desk resets from forced rotation.",
         "alternative_cost": "Low.",
         "alternative_risks": "Customer auditors with outdated checklists may record findings.",
         "supporting_arguments": ["Current NIST guidance explicitly rejects forced periodic rotation and composition rules."],
         "opposing_arguments": ["Legacy questionnaires and some internal bank standards still require rotation."],
         "technical_effectiveness": "stronger",
         "institutional_acceptance": "likely"})

C.au(6, "Session management, token handling and revocation",
     "Sessions",
     "The customer needs authenticated sessions to be protected from theft, fixation and indefinite reuse, and to end promptly when access should end.",
     "proposed-target-state",
     "AUTH-I1 requires sessions, widget instances, partner tokens and agent privileges derived from changed authority to be invalidated or rechecked with a stated maximum staleness; UNB-RCN-ENT-004 suspends sessions on death or incapacity. Limen keeps browser storage and HTTP in its kernel; whether Unbound session tokens would be stored in browser-accessible storage is not decided. No session implementation exists.",
     "Browser sessions use opaque, server-side session identifiers in cookies marked Secure, HttpOnly and SameSite, never placed in browser-readable storage; new identifiers are issued at login and at any privilege change. Idle and absolute timeouts are risk-tiered (shorter for staff and privileged roles) and configurable by the sponsor within platform limits. Users and administrators can list and terminate sessions. Password, authenticator or contact changes, deactivation and authority changes revoke or recheck all sessions and refresh tokens within a stated maximum staleness. API refresh tokens rotate on use with reuse detection, and long-lived API tokens are scoped, expiring and revocable.",
     "Not implemented. Requirements exist for invalidation; token storage design is not decided.",
     "Decide session architecture compatible with the Limen kernel boundary; implement revocation and timeouts.",
     "Requirement text only.",
     "Echelon's Unbound design uses server-side sessions in protected cookies, risk-tiered timeouts, user-visible session management, and revocation of sessions when credentials or authority change. This is planned, not operating.",
     "planned",
     controls=[6], evrs=[6],
     policies=["SEC-UI-002", "SEC-AUTH-001"],
     reqs=["AUTH-I1", "UNB-RCN-ENT-004", "TVR-WID-001"],
     fresh="per-event", mech="event-driven-automated", auto="high", impl="medium", rec="low",
     residual=["Malware on the user's endpoint can use a live session regardless of cookie flags."],
     oq=["Does the Limen kernel's storage capability need a rule forbidding session or bearer tokens in localStorage for Unbound?"])

C.au(7, "Account recovery, authenticator changes and help-desk resets",
     "Account recovery",
     "The customer needs recovery and credential-change paths to be at least as strong as sign-in, because attackers target the help desk and recovery flows.",
     "proposed-target-state",
     "AUTH-I7 requires step-up, a cooling-off period and notice to the prior channel for authority-relevant credential changes; CNV-PLT-011 requires prior-channel notification with a revert link, a default 72-hour hold on high-risk actions and an AccessibleAssurancePath; UNB-XIN-SVC-004 prohibits knowledge-based answers above the lowest assurance level and staff override of the contact assurance matrix; CNV-PLT-003 prohibits KBA for proofing and requires identity-proofed recovery for privileged roles. Not implemented.",
     "Recovery after loss of all authenticators requires re-proofing at the original assurance level (or a pre-registered second authenticator), never knowledge-based questions or email alone. Enrolling an authenticator, changing email, phone or recovery factors notifies the previous channel with a revert link and starts a cooling-off period (default 72 hours, sponsor-configurable) during which authority changes, successor changes and new-recipient grants above a threshold are held for confirmation. Support staff cannot reset authenticators or change contact details beyond the contact assurance matrix and cannot override it. Accessible recovery paths (mailed code, outbound call to a verified number, captioned assisted video, in-person or notarized verification, relay calls) each reach a defined assurance level.",
     "Not implemented. Requirements exist.",
     "Implement recovery, cooling-off and contact assurance matrix as part of the identity core.",
     "Requirement text only.",
     "Echelon's Unbound design never uses security questions, notifies the previous channel on any credential or contact change, holds high-risk actions during a cooling-off period, and prevents support staff from overriding verification rules. This is planned, not operating.",
     "planned",
     controls=[7], evrs=[7],
     reqs=["AUTH-I7", "CNV-PLT-011", "UNB-XIN-SVC-004", "CNV-PLT-003", "TVR-SEC-007"],
     fresh="per-event", mech="event-driven-automated", auto="high", impl="medium", rec="medium",
     residual=["Cooling-off periods delay legitimate urgent grants; sponsors may press to shorten them.",
               "Deepfake voice or video may defeat assisted verification."],
     challenge={
         "customer_intent": "Make sure attackers cannot take over accounts by convincing support or abusing recovery.",
         "adverse_outcome": "Help-desk social engineering resets MFA and the attacker redirects grants.",
         "conventional_control_effectiveness": "Conventional recovery by security questions or email link is weak; agent verification scripts are routinely socially engineered.",
         "legally_required": "SEC Regulation S-ID requires covered firms to have identity theft red flags programs that address account changes; it binds covered broker-dealers and advisers, not Echelon, and only flows contractually.",
         "contractually_required": "Not usually specified in detail.",
         "historical_convention": "Security questions, email reset, agent judgment.",
         "architectural_elimination": "Staff override is eliminated by enforcing the contact assurance matrix in the support tool; immediate post-change exploitation is eliminated by holds during cooling-off.",
         "automatic_enforcement": "Holds and notifications are automatic and not discretionary.",
         "continuous_evidence": "Every change, notice, hold and release is an event.",
         "stronger_alternative": "Cooling-off with prior-channel revert plus sponsor-direct confirmation for new recipients.",
         "alternative_verifiable": "Yes, through tests and event history.",
         "customer_acceptance_likelihood": "Likely for banks and wealth managers familiar with holds after contact changes; donors may object to delays.",
         "invalidating_conditions": "If any support or sponsor-staff path can waive the hold without independent approval.",
         "conventional_cost": "Fraud losses and remediation.",
         "alternative_cost": "Support cost and donor friction.",
         "alternative_risks": "Attackers may change contacts and wait out the period; TVR-SEC-010 addresses this by measuring recipient novelty from the last pre-existing-channel confirmation.",
         "supporting_arguments": ["The approach does not depend on staff detecting deception."],
         "opposing_arguments": ["Accessibility and urgency exceptions create pressure to weaken holds."],
         "technical_effectiveness": "stronger",
         "institutional_acceptance": "likely"})

C.au(8, "Step-up authentication and transaction binding for high-risk and financial actions",
     "Step-up for financial actions",
     "The customer needs high-risk actions, especially those that move or redirect money or change authority, to require fresh, strong authentication bound to the specific action, consistent with FFIEC risk-based guidance.",
     "proposed-target-state",
     "UNB-XIN-IAM-003 defines a StepUpPolicy matrix (AAL2 phishing-resistant or AAL3 for privileged workforce, maximum authentication age default five minutes, step-up event bound to the command, verifier controlled by the sponsor not the partner IdP). TVR-SEC-004 bounds auto-approval by session assurance and requires step-up for new recipients from phishable or agent sessions. Not implemented.",
     "Each high-risk action class (authenticator or recovery change, authority or delegation change, payee or destination change, data export, grant recommendation above a sponsor threshold, API credential creation, sponsor policy publication) has a required assurance level and maximum authentication age in one StepUpPolicy matrix. The step-up event identifier is bound to the specific command and its parameters; a command without a fresh, matching step-up is rejected, and a step-up cannot be reused for another action. The step-up prompt shows the action's key details so the user confirms what will happen. Step-up is performed by a sponsor-controlled verifier, not delegated to a partner IdP. Auto-approval ceilings depend on session assurance, so a phishable or agent-initiated session cannot obtain an auto-approved grant to a new recipient. This implements the layered, risk-based approach of the FFIEC 2021 authentication guidance for the sponsor's and partner bank's customers.",
     "Not implemented. Requirements exist.",
     "Implement the StepUpPolicy matrix in the authorization core with command binding.",
     "Requirement text only.",
     "Echelon's Unbound design requires fresh, phishing-resistant step-up authentication bound to each specific high-risk action, such as payee changes, large grant recommendations and data exports. This is planned, not operating.",
     "planned",
     controls=[8], evrs=[8],
     policies=["SEC-AUTH-001"],
     reqs=["UNB-XIN-IAM-003", "TVR-SEC-004", "TVR-SEC-010", "GOV-AUTH-006", "AUTH-I7"],
     fresh="per-event", mech="event-driven-automated", auto="full", impl="medium", rec="low",
     residual=["Man-in-the-browser malware may alter what is displayed; transaction detail display mitigates only if the authenticator or a separate channel displays the details."])

C.au(9, "Authentication of APIs, widgets, webhooks and AI agents",
     "Non-human and embedded authentication",
     "The customer needs integrations, embedded components and agents to authenticate strongly, with credentials that cannot exceed the assurance of the humans they act for and cannot be stolen from host pages.",
     "proposed-target-state",
     "UNB-API-STD-005 requires each integration to document authentication method, credential rotation, least privilege, webhook signature verification, replay defense and partner context binding; AIN-029 requires embeds to independently authorize, expire safely and not impersonate the sponsor; TVR-WID-001 requires widget data cleared after authority revision change; TVR-SEC-004 treats agent sessions as needing step-up for new recipients. Not implemented.",
     "Partner and integration APIs use OAuth 2.0 client credentials or mutual TLS with per-client, scoped, expiring credentials; shared static API keys are not issued for new integrations. User-delegated API access uses OAuth authorization code with PKCE and scoped, short-lived access tokens. Embedded widgets run in an isolated origin and receive narrowly scoped, short-lived tokens never exposed to host-page scripts; they expire and clear data when authority changes. Inbound webhooks are signed, timestamped and replay-protected; outbound webhooks are signed. AI agents authenticate as their own Workload principals with delegated grants derived from a user, and an agent session is treated as lower assurance than a fresh human step-up for high-risk actions.",
     "Not implemented. Requirements exist.",
     "Define API authentication standards per UNB-API-STD-005 before the first integration.",
     "Requirement text only.",
     "Echelon's Unbound design uses scoped, expiring OAuth or mutual-TLS credentials for integrations, signed and replay-protected webhooks, isolated widget tokens, and separate lower-assurance identities for AI agents. This is planned, not operating.",
     "planned",
     controls=[9], evrs=[9],
     policies=["SEC-AUTH-001", "SEC-UI-002", "SEC-DATA-001"],
     reqs=["UNB-API-STD-005", "AIN-029", "TVR-WID-001", "TVR-SEC-004", "UNB-CUST-017"],
     fresh="per-event", mech="event-driven-automated", auto="high", impl="medium", rec="low",
     residual=["Custodian and bank counterparties may support only legacy authentication."])

# ---------------- Controls ----------------
C.ctl(1, "Workforce MFA enforced at the identity provider with phishing-resistant factors",
      "Require phishing-resistant MFA for all workforce sign-ins through IdP policy and AAL3-grade keys with two registrations for privileged roles; record and expire any exception.",
      "preventive-gate", "L3-restricted-interface", ["not yet assigned (workforce IdP)"], evrs=[1],
      related=["CNV-PLT-003", "SOC2-010", "UNB-CTRL-004"],
      refs=[d("SRC-FTC-SAFEGUARDS-RULE", "314.4(c)(5)", "informed-by"), d("SRC-NYDFS-PART-500", "500.12", "informed-by"), d("SRC-NIST-SP800-53-R5", "IA-2(1)"), d("SRC-NIST-SP800-53-R5", "IA-2(2)"), d("SRC-CIS-CONTROLS-V8.1", "6.5"), s("SRC-PCI-DSS-4.0.1", "Req 8.4.2", "informed-by")],
      cwe=["CWE-308"])
C.ctl(2, "WebAuthn-first authentication with restricted fallbacks",
      "Offer and default to origin-bound WebAuthn authenticators; restrict SMS and voice; require number matching for any push; treat synced passkeys as insufficient alone for high-risk actions.",
      "preventive-structural", "L3-restricted-interface", ["not yet assigned (Unbound identity core)"], evrs=[2],
      related=["CNV-PLT-003", "TVR-SEC-010"],
      refs=[d("SRC-NIST-SP800-63-4", "SP 800-63B"), s("SRC-CISA-SECURE-BY-DESIGN", rel="informed-by"), s("SRC-MITRE-ATTACK", "T1621"), s("SRC-MITRE-ATTACK", "T1539")],
      cwe=["CWE-308", "CWE-287"])
C.ctl(3, "Federation assertion validation with negative tests and immutable identity mapping",
      "Validate SAML and OIDC assertions fully using a maintained library with negative tests for known attacks; map identities by issuer plus subject; require dual control for mapping changes; scope each IdP's trust to its realm.",
      "preventive-structural", "L7-property-tested", ["not yet assigned"], evrs=[3],
      policies=["SEC-DATA-001"], related=["AUTH-I8", "UNB-XIN-IAM-001"],
      refs=[d("SRC-NIST-SP800-63-4", "SP 800-63C"), s("SRC-NIST-CSF-2.0", "PR.AA-04"), s("SRC-OWASP-CHEATSHEETS", rel="informed-by")],
      cwe=["CWE-347", "CWE-287", "CWE-290"])
C.ctl(4, "Scoped SCIM endpoint with bounded deprovisioning latency",
      "Accept SCIM changes only with a scoped, rotatable credential that cannot create reserved privileged roles, and propagate deactivation to all sessions, tokens and delegated grants within a contractual maximum.",
      "corrective", "L9-runtime-monitored", ["not yet assigned"], evrs=[4],
      related=["TVR-WID-006", "AUTH-I1"],
      refs=[s("SRC-NIST-SP800-53-R5", "AC-2"), s("SRC-NIST-CSF-2.0", "PR.AA-01")])
C.ctl(5, "NIST SP 800-63B-4 password handling and throttling",
      "Enforce length-based password rules with breached-password screening, no composition or periodic rotation rules, approved salted password hashing, and per-account and per-source throttling that resists lockout abuse.",
      "preventive-structural", "L3-restricted-interface", ["not yet assigned"], evrs=[5],
      policies=["SEC-CRYPTO-001"],
      refs=[d("SRC-NIST-SP800-63-4", "SP 800-63B"), d("SRC-NIST-SP800-53-R5", "IA-5(1)"), d("SRC-NIST-SP800-53-R5", "AC-7"), s("SRC-OWASP-CHEATSHEETS", rel="informed-by")],
      cwe=["CWE-521", "CWE-307", "CWE-916"])
C.ctl(6, "Server-side session management with revocation on credential and authority change",
      "Use opaque server-side sessions in Secure, HttpOnly, SameSite cookies, regenerate on login and privilege change, enforce risk-tiered timeouts, and revoke or recheck sessions and tokens on credential, contact, deactivation or authority change within a stated staleness bound.",
      "preventive-structural", "L3-restricted-interface", ["not yet assigned", "Limen (browser boundary; token storage rule to be defined)"], evrs=[6],
      policies=["SEC-UI-002"], related=["AUTH-I1"],
      refs=[d("SRC-NIST-SP800-53-R5", "AC-12"), d("SRC-NIST-SP800-53-R5", "SC-23"), s("SRC-NIST-SP800-53-R5", "AC-11"), s("SRC-OWASP-CHEATSHEETS", rel="informed-by"), s("SRC-PCI-DSS-4.0.1", "Req 8.2.8", "informed-by")],
      cwe=["CWE-384", "CWE-613", "CWE-614", "CWE-1004"])
C.ctl(7, "Recovery and contact-change controls with cooling-off holds",
      "Prohibit knowledge-based recovery; notify the prior channel with revert link on any credential or contact change; hold high-risk actions during a cooling-off period; enforce the contact assurance matrix in support tools without override.",
      "preventive-structural", "L3-restricted-interface", ["not yet assigned"], evrs=[7],
      related=["AUTH-I7", "CNV-PLT-011", "UNB-XIN-SVC-004"],
      refs=[d("SRC-NIST-SP800-63-4", "SP 800-63B"), s("SRC-SEC-REG-S-ID", rel="informed-by"), s("SRC-MITRE-ATTACK", "T1098")],
      cwe=["CWE-640"])
C.ctl(8, "Command-bound step-up policy matrix",
      "Require a fresh step-up of the specified assurance, bound to the exact command and parameters and performed by a sponsor-controlled verifier, for each high-risk action class; reject commands without it.",
      "preventive-structural", "L3-restricted-interface", ["not yet assigned (Unbound authorization core)"], evrs=[8],
      policies=["SEC-AUTH-001"], related=["UNB-XIN-IAM-003", "TVR-SEC-004"],
      refs=[s("SRC-FFIEC-AUTH-GUIDANCE-2021", rel="informed-by"), d("SRC-NIST-SP800-53-R5", "IA-11"), s("SRC-NIST-SP800-63-4", "SP 800-63B")],
      cwe=["CWE-306", "CWE-294"])
C.ctl(9, "Scoped, expiring credentials for APIs, widgets, webhooks and agents",
      "Authenticate integrations with OAuth client credentials or mutual TLS, users with authorization code plus PKCE, widgets with isolated short-lived tokens, webhooks with signatures and replay protection, and agents as their own lower-assurance principals.",
      "preventive-structural", "L3-restricted-interface", ["not yet assigned"], evrs=[9],
      policies=["SEC-AUTH-001", "SEC-DATA-001"], related=["UNB-API-STD-005", "AIN-029", "UNB-CTRL-067"],
      refs=[d("SRC-OWASP-API-TOP10-2023", "API2:2023"), s("SRC-NIST-SP800-53-R5", "IA-9"), s("SRC-NIST-SP800-53-R5", "IA-2(8)")],
      cwe=["CWE-287", "CWE-294", "CWE-345"])

# ---------------- Evidence ----------------
C.evr(1, "Workforce MFA coverage report",
      "Every workforce account and federated application with enforced factor types, plus list of non-federated systems with their MFA configuration and any exceptions.",
      "not yet assigned (workforce IdP export)", "periodic-automated", "P1D", fmt="JSON plus summary", prov=["IdP tenant", "policy version", "generation time"], disc="customer-only")
C.evr(2, "Authenticator type distribution and policy",
      "Share of authentications and of registered users by authenticator type and population; policy configuration snapshot.",
      "not yet assigned", "periodic-automated", "P30D", fmt="JSON", prov=["period", "population counts"], disc="customer-only")
C.evr(3, "Federation negative-test results",
      "Results of tests for signature wrapping, unsigned assertions, wrong audience, replay and algorithm confusion per release.",
      "not yet assigned", "event-driven-automated", "per-event", fmt="Test report", prov=["build", "library version", "test ids"], disc="customer-only")
C.evr(4, "Deprovisioning latency measurements",
      "Measured time from SCIM deactivation to last accepted request per principal, with distribution per customer.",
      "not yet assigned", "continuous-automated", "P1D", fmt="JSON", prov=["principal", "deactivation time", "last accepted request time"], disc="customer-only")
C.evr(5, "Password policy configuration and test results",
      "Configured parameters, hashing parameters and tests for breached-password rejection and throttling.",
      "not yet assigned", "event-driven-automated", "per-event", fmt="Configuration export plus test report", prov=["build", "configuration hash"], disc="authenticated-prospect")
C.evr(6, "Session configuration and revocation tests",
      "Cookie attributes, timeouts, and tests demonstrating revocation on credential, contact and authority change within the stated bound.",
      "not yet assigned", "event-driven-automated", "per-event", fmt="Test report", prov=["build", "test ids"], disc="customer-only")
C.evr(7, "Credential and contact change event log",
      "Changes, prior-channel notices, reverts, holds and releases per principal.",
      "not yet assigned", "event-driven-automated", "per-event", fmt="Tenant-scoped events", prov=["principal", "channel", "hold id"], disc="customer-only")
C.evr(8, "Step-up binding records and negative tests",
      "Per high-risk command: step-up event id, assurance achieved, age, bound parameters; tests proving rejection without a fresh matching step-up.",
      "not yet assigned", "event-driven-automated", "per-event", fmt="Events plus test report", prov=["command id", "step-up event id", "policy matrix version"], disc="customer-only")
C.evr(9, "Integration credential register",
      "Per integration: authentication method, scopes, expiry, rotation date, webhook signing status.",
      "not yet assigned", "periodic-automated", "P30D", fmt="JSON", prov=["client id", "owner", "last rotation"], disc="customer-only")

# ---------------- Questions ----------------
C.q(1, "Is multi-factor authentication enforced for all workforce access to systems that store or process customer data, including email, source code, cloud consoles and deployment pipelines?",
    "A stolen password gives an attacker access to customer data or production.",
    [d("SRC-FTC-SAFEGUARDS-RULE", "314.4(c)(5)", "informed-by"), d("SRC-NYDFS-PART-500", "500.12", "informed-by"), d("SRC-NIST-SP800-53-R5", "IA-2(1)"), d("SRC-CIS-CONTROLS-V8.1", "6.3"), s("SRC-PCI-DSS-4.0.1", "Req 8.4.2", "informed-by"), s("SRC-SA-SIG"), s("SRC-CSA-CAIQ-V4", "IAM domain"), s("SRC-VSA-CORE")],
    cls="contractual-common", imp="critical", ind=ALL, jur=GLOBAL, prod=ORGALL,
    alts=["Is MFA required for all users with access to sensitive data?", "Do you enforce MFA for remote access and administrative access?"])
C.q(1, "Are there any exceptions to workforce MFA, and if so, who approved them, for how long, and what compensating controls apply?",
    "Exceptions become permanent gaps exploited by attackers.",
    [d("SRC-NYDFS-PART-500", "500.12", "informed-by"), s("SRC-FTC-SAFEGUARDS-RULE", "314.4(c)(5)", "informed-by")],
    cls="contractual-common", imp="high", ind=BANK + WM, jur=USF + NY, prod=ORG, reg="NYDFS; FTC (customer's obligations)",
    note="NYDFS 500.12 and 16 CFR 314.4(c)(5) bind covered entities for their own information systems and allow approved equivalent controls; vendors receive the expectation through third-party service provider policies (NYDFS 500.11, 16 CFR 314.4(f)) and contracts, not directly.")
C.q(1, "Is MFA required on the accounts used to manage source code repositories, build systems and package publishing, where a compromise could insert malicious code into the product?",
    "Software supply-chain compromise through a developer or publisher account.",
    [s("SRC-NIST-SP800-218", rel="informed-by"), s("SRC-OPENSSF-SCORECARD", rel="informed-by"), s("SRC-SLSA", rel="informed-by"), s("SRC-CISA-SSDF-ATTESTATION", rel="informed-by")],
    cls="industry-convention", imp="high", ind=ENT, jur=GLOBAL, prod=ALLP)
C.q(1, "Do privileged users authenticate with hardware-backed or device-bound authenticators, and does each have a second registered authenticator?",
    "Privileged accounts protected by phishable factors are taken over; loss of a single key forces weak recovery.",
    [e("SRC-ECH-UNB-BASELINE", "CNV-PLT-003"), d("SRC-NIST-SP800-63-4", "SP 800-63B", "informed-by"), d("SRC-CIS-CONTROLS-V8.1", "6.5")],
    cls="customer-preference", imp="high", ind=BANK + ["enterprise-software"], jur=USF, prod=ORGALL)
C.q(1, "How do you enforce MFA for third-party vendors, contractors and support providers who access your environment?",
    "Third-party accounts are the weakest path into the environment.",
    [s("SRC-NIST-SP800-53-R5", "IA-8"), s("SRC-INTERAGENCY-TPRM-2023", rel="informed-by"), s("SRC-CIS-CONTROLS-V8.1", "6.4")],
    cls="contractual-common", imp="medium", ind=ALL, jur=GLOBAL, prod=ORG)

C.q(2, "Do you support phishing-resistant authenticators such as FIDO2/WebAuthn security keys and passkeys, for both your workforce and our users?",
    "Real-time phishing proxies capture one-time codes and session cookies.",
    [d("SRC-NIST-SP800-63-4", "SP 800-63B"), s("SRC-CISA-SECURE-BY-DESIGN", rel="informed-by"), s("SRC-FFIEC-AUTH-GUIDANCE-2021", rel="informed-by"), s("SRC-EDUCAUSE-HECVAT")],
    cls="customer-preference", imp="high", ind=ALL, jur=GLOBAL,
    alts=["Is phishing-resistant MFA available?", "Does the application support passkeys?"])
C.q(2, "Do you rely on SMS, voice or email one-time codes for any user population, and if so, what additional risk controls apply?",
    "SIM swap, number porting or mailbox compromise defeats the second factor.",
    [d("SRC-NIST-SP800-63-4", "SP 800-63B"), s("SRC-FFIEC-AUTH-GUIDANCE-2021", rel="informed-by"), s("SRC-MITRE-ATTACK", "T1111")],
    cls="supervisory-guidance", imp="high", ind=BANK + WM + DAF, jur=USF, reg=FFIEC)
C.q(2, "Do you treat synced (cloud-backed) passkeys differently from device-bound keys for high-risk actions such as adding a new payment recipient?",
    "Takeover of the user's cloud account syncs their passkey to an attacker device.",
    [e("SRC-ECH-UNB-BASELINE", "TVR-SEC-010"), e("SRC-ECH-UNB-BASELINE", "CNV-PLT-003"), s("SRC-NIST-SP800-63-4", "SP 800-63B", "informed-by")],
    cls="customer-preference", imp="medium", ind=DAF + ["wealth-management", "banking"], jur=USF)
C.q(2, "How do you defend against MFA fatigue (repeated push prompts) and adversary-in-the-middle attacks that steal session tokens after MFA?",
    "Users approve attacker prompts or attackers replay stolen post-MFA sessions.",
    [s("SRC-MITRE-ATTACK", "T1621"), s("SRC-MITRE-ATTACK", "T1539"), s("SRC-MITRE-ATTACK", "T1557"), d("SRC-NIST-SP800-53-R5", "IA-2(8)")],
    cls="industry-convention", imp="high", ind=ALL, jur=GLOBAL)
C.q(2, "If a user cannot use a security key or passkey because of disability or lack of a compatible device, what equally secure alternative do you provide?",
    "Accessibility exclusions push users onto weak fallback factors that attackers then target.",
    [e("SRC-ECH-UNB-BASELINE", "CNV-PLT-011"), s("SRC-WCAG-2.2", rel="informed-by"), s("SRC-ADA", rel="informed-by"), s("SRC-NIST-SP800-63-4", rel="informed-by")],
    cls="customer-preference", imp="medium", ind=DAF + ["financial-services"], jur=USF,
    note="Whether ADA obligations reach a customer's digital services depends on the customer's status and is not established here; the authentication alternative itself is a design choice.")

C.q(3, "Do you support single sign-on for our workforce through SAML 2.0 and OpenID Connect, and is it included on all plans without additional charge?",
    "The customer cannot apply its own MFA and lifecycle controls to the vendor application.",
    [d("SRC-NIST-SP800-63-4", "SP 800-63C"), s("SRC-CISA-SECURE-BY-DESIGN", rel="informed-by"), s("SRC-EDUCAUSE-HECVAT"), s("SRC-CSA-CAIQ-V4", "IAM domain"), s("SRC-SA-SIG")],
    cls="customer-preference", imp="high", ind=ENT + ["higher-education"], jur=GLOBAL,
    alts=["Does your application integrate with our identity provider (for example Entra ID or Okta)?"])
C.q(3, "Can we require that our users sign in only through our SSO and disable local passwords for our organization?",
    "Users bypass the customer's IdP controls through a local password.",
    [s("SRC-NIST-SP800-63-4", "SP 800-63C"), s("SRC-CIS-CONTROLS-V8.1", "6.7")],
    cls="customer-preference", imp="medium", ind=ENT, jur=GLOBAL)
C.q(3, "How do you validate SAML and OpenID Connect responses (signature, issuer, audience, expiry, replay), and do you test against known federation attacks such as signature wrapping?",
    "A forged or replayed assertion signs an attacker in as any user.",
    [d("SRC-NIST-SP800-63-4", "SP 800-63C"), s("SRC-MITRE-CWE", "CWE-347", "informed-by"), s("SRC-OWASP-WSTG", rel="informed-by"), s("SRC-MITRE-ATTACK", "T1606")],
    cls="industry-convention", imp="high", ind=ENT + BANK, jur=GLOBAL)
C.q(3, "Do you link federated identities to platform accounts by an immutable identifier such as issuer plus subject, rather than by email address, and how are mapping changes controlled?",
    "An attacker who controls a matching email address at another IdP or after a domain change takes over an account.",
    [e("SRC-ECH-UNB-BASELINE", "AUTH-I8"), s("SRC-NIST-SP800-63-4", "SP 800-63C"), s("SRC-MITRE-CWE", "CWE-290", "informed-by")],
    cls="customer-preference", imp="high", ind=FS, jur=USF)
C.q(3, "If one of our distribution partners' identity providers is compromised, what can the attacker do on your platform, and which actions still require verification that the partner IdP cannot provide?",
    "A partner IdP compromise becomes a takeover of all of that partner's donors' ability to move money.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-003"), e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-001"), s("SRC-NIST-SP800-207", "Section 2.1", "informed-by")],
    cls="customer-preference", imp="high", ind=DAF + ["banking", "wealth-management"], jur=USF)

C.q(4, "Do you support automated user provisioning and deprovisioning from our identity provider through SCIM 2.0?",
    "Manual user management leaves removed users active.",
    [s("SRC-NIST-SP800-53-R5", "AC-2"), s("SRC-EDUCAUSE-HECVAT"), s("SRC-CSA-CAIQ-V4", "IAM domain")],
    cls="customer-preference", imp="medium", ind=ENT + ["higher-education"], jur=GLOBAL)
C.q(4, "When we disable a user in our identity provider, how quickly are that user's active sessions, refresh tokens and API tokens on your platform terminated, and is that time a contractual commitment?",
    "A terminated user keeps working in an existing session or with a token after removal.",
    [e("SRC-ECH-UNB-BASELINE", "TVR-WID-006"), e("SRC-ECH-UNB-BASELINE", "AUTH-I1"), s("SRC-NIST-SP800-53-R5", "AC-12")],
    cls="customer-preference", imp="high", ind=BANK + ENT, jur=USF)
C.q(4, "What happens to pending recommendations, approvals or scheduled actions owned by a user who is deprovisioned?",
    "Scheduled actions of a removed user execute after removal, or are lost.",
    [e("SRC-ECH-UNB-BASELINE", "AUTH-I2"), e("SRC-ECH-UNB-BASELINE", "AUTH-I3")],
    cls="customer-preference", imp="medium", ind=DAF + ["wealth-management"], jur=USF)
C.q(4, "How is your SCIM endpoint protected, given that it can create users and assign roles, and can it ever create administrator or other privileged roles?",
    "A leaked SCIM token is used to create privileged users.",
    [s("SRC-OWASP-API-TOP10-2023", "API5:2023", "informed-by"), s("SRC-MITRE-ATTACK", "T1136"), s("SRC-NIST-SP800-53-R5", "AC-6")],
    cls="customer-preference", imp="medium", ind=ENT, jur=GLOBAL)

C.q(5, "Describe your password requirements for workforce and customer accounts, including length, complexity, expiration and screening against breached passwords.",
    "Weak or reused passwords are guessed or stuffed.",
    [d("SRC-NIST-SP800-63-4", "SP 800-63B"), d("SRC-NIST-SP800-53-R5", "IA-5(1)"), s("SRC-PCI-DSS-4.0.1", "Req 8.3.6", "informed-by"), s("SRC-SA-SIG"), s("SRC-CSA-CAIQ-V4", "IAM domain"), s("SRC-EDUCAUSE-HECVAT")],
    cls="contractual-common", imp="medium", ind=ALL, jur=GLOBAL, prod=ALLP,
    alts=["What is your password policy?", "Do passwords meet minimum complexity requirements?"])
C.q(5, "Do you require users to change their passwords periodically? If not, how do you justify that to auditors who expect rotation?",
    "Either predictable rotated passwords, or audit findings for non-rotation.",
    [d("SRC-NIST-SP800-63-4", "SP 800-63B"), s("SRC-PCI-DSS-4.0.1", "Req 8.3.9", "contradicts")],
    cls="customer-preference", imp="low", ind=BANK + ["insurance"], jur=USF, prod=ALLP)
C.q(5, "How are passwords stored, including the hashing algorithm, salting and work factor?",
    "A database leak allows offline cracking of user passwords.",
    [d("SRC-NIST-SP800-63-4", "SP 800-63B"), s("SRC-MITRE-CWE", "CWE-916", "informed-by"), s("SRC-OWASP-CHEATSHEETS", rel="informed-by"), e("SRC-ECH-SCS-0.1", "SEC-CRYPTO-001")],
    cls="industry-convention", imp="high", ind=ALL, jur=GLOBAL, prod=ALLP)
C.q(5, "How do you protect sign-in against credential stuffing and brute force, and how do you prevent lockout controls from being abused to lock legitimate users out?",
    "Automated guessing succeeds, or attackers deny service by triggering lockouts.",
    [d("SRC-NIST-SP800-53-R5", "AC-7"), s("SRC-MITRE-ATTACK", "T1110"), s("SRC-MITRE-CWE", "CWE-307", "informed-by"), d("SRC-OWASP-API-TOP10-2023", "API2:2023"), s("SRC-PCI-DSS-4.0.1", "Req 8.3.4", "informed-by")],
    cls="industry-convention", imp="high", ind=ALL, jur=GLOBAL, prod=ALLP)
C.q(5, "Do you allow pasting into password fields and use of password managers, and have you eliminated security questions?",
    "Users choose short memorable passwords, and security answers are discoverable.",
    [d("SRC-NIST-SP800-63-4", "SP 800-63B"), e("SRC-ECH-UNB-BASELINE", "CNV-PLT-003")],
    cls="industry-convention", imp="low", ind=ALL, jur=GLOBAL, prod=ALLP)
C.q(5, "Can our users sign in without a password at all (passwordless), and can we require that for our organization?",
    "Password-related attacks remain possible as long as a password exists on the account.",
    [s("SRC-NIST-SP800-63-4", "SP 800-63B"), s("SRC-CISA-SECURE-BY-DESIGN", rel="informed-by")],
    cls="customer-preference", imp="medium", ind=ENT + DAF, jur=GLOBAL)

C.q(6, "What are your session idle and absolute timeouts for customer users and for staff, and can we configure them?",
    "Unattended sessions are used by others.",
    [d("SRC-NIST-SP800-53-R5", "AC-12"), d("SRC-NIST-SP800-53-R5", "AC-11"), s("SRC-PCI-DSS-4.0.1", "Req 8.2.8", "informed-by"), s("SRC-SA-SIG"), s("SRC-EDUCAUSE-HECVAT")],
    cls="contractual-common", imp="medium", ind=ALL, jur=GLOBAL,
    alts=["Does the application automatically log out inactive users?"])
C.q(6, "How are session tokens protected against theft (cookie attributes, storage location in the browser, transport), and are bearer tokens ever stored in browser-readable storage?",
    "Cross-site scripting or malicious browser extensions steal tokens from browser storage.",
    [d("SRC-NIST-SP800-53-R5", "SC-23"), s("SRC-OWASP-CHEATSHEETS", rel="informed-by"), s("SRC-MITRE-CWE", "CWE-1004", "informed-by"), e("SRC-ECH-SCS-0.1", "SEC-UI-002")],
    cls="industry-convention", imp="high", ind=ALL, jur=GLOBAL,
    oq=["Unbound's browser UI is planned on Limen, whose kernel exposes localStorage; a rule against storing tokens there is not yet defined."])
C.q(6, "When a user's password, authenticator or contact details change, or the user is disabled, are their other active sessions and refresh tokens revoked immediately?",
    "An attacker's existing session survives the victim's credential reset.",
    [e("SRC-ECH-UNB-BASELINE", "AUTH-I1"), e("SRC-ECH-UNB-BASELINE", "AUTH-I7"), s("SRC-NIST-SP800-63-4", "SP 800-63B", "informed-by"), s("SRC-MITRE-CWE", "CWE-613", "informed-by")],
    cls="industry-convention", imp="high", ind=ALL, jur=GLOBAL)
C.q(6, "Can users and our administrators see all active sessions for an account and terminate them?",
    "A user who suspects compromise cannot evict the attacker.",
    [s("SRC-NIST-SP800-53-R5", "AC-12"), s("SRC-OWASP-CHEATSHEETS", rel="informed-by")],
    cls="customer-preference", imp="low", ind=ALL, jur=GLOBAL)
C.q(6, "How do you prevent session fixation and session hijacking, including issuing a new session identifier on login and when privileges change?",
    "An attacker plants or reuses a session identifier to inherit the victim's authenticated session.",
    [d("SRC-NIST-SP800-53-R5", "SC-23"), s("SRC-MITRE-CWE", "CWE-384", "informed-by"), s("SRC-OWASP-WSTG", rel="informed-by")],
    cls="industry-convention", imp="medium", ind=ALL, jur=GLOBAL)
C.q(6, "How are API access and refresh tokens governed, including lifetime, rotation, reuse detection, scope and revocation?",
    "Long-lived tokens are stolen and used indefinitely.",
    [d("SRC-OWASP-API-TOP10-2023", "API2:2023"), s("SRC-MITRE-ATTACK", "T1550"), s("SRC-NIST-SP800-53-R5", "IA-5")],
    cls="industry-convention", imp="medium", ind=ENT, jur=GLOBAL)

C.q(7, "How does a user regain access after losing all authenticators, and how is that process protected against social engineering?",
    "Account recovery becomes the easiest path to account takeover.",
    [d("SRC-NIST-SP800-63-4", "SP 800-63B"), s("SRC-MITRE-CWE", "CWE-640", "informed-by"), s("SRC-SA-SIG"), s("SRC-FFIEC-AUTH-GUIDANCE-2021", rel="informed-by")],
    cls="supervisory-guidance", imp="high", ind=FS, jur=USF, reg=FFIEC,
    alts=["Describe your account recovery and password reset process."])
C.q(7, "Can your help desk or support staff reset a user's MFA, change their email or phone number, or unlock their account, and what verification must they perform first?",
    "Attackers call support, impersonate the user and obtain an MFA reset.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-XIN-SVC-004"), e("SRC-ECH-UNB-BASELINE", "TVR-SEC-007"), s("SRC-MITRE-ATTACK", "T1656"), s("SRC-FFIEC-AUTH-GUIDANCE-2021", rel="informed-by")],
    cls="supervisory-guidance", imp="critical", ind=FS, jur=USF, reg=FFIEC)
C.q(7, "When an authenticator, email, phone number or recovery method is changed, is the previous contact channel notified, and are high-risk actions held for a cooling-off period afterward?",
    "An attacker changes contact details and immediately redirects grants before the real user notices.",
    [e("SRC-ECH-UNB-BASELINE", "AUTH-I7"), e("SRC-ECH-UNB-BASELINE", "CNV-PLT-011"), s("SRC-SEC-REG-S-ID", rel="informed-by")],
    cls="customer-preference", imp="high", ind=DAF + ["wealth-management", "banking"], jur=USF)
C.q(7, "Is knowledge-based verification (security questions or credit-history questions) used anywhere in sign-in, recovery or support verification?",
    "Answers to knowledge questions are obtained from breaches or social media.",
    [d("SRC-NIST-SP800-63-4", "SP 800-63A"), e("SRC-ECH-UNB-BASELINE", "CNV-PLT-003"), e("SRC-ECH-UNB-BASELINE", "UNB-XIN-SVC-004")],
    cls="industry-convention", imp="medium", ind=FS, jur=USF)
C.q(7, "What accessible recovery and verification options exist for users who are elderly, have disabilities, or cannot use smartphones, and what assurance does each provide?",
    "Users without modern devices are either excluded or served by weak exceptions that attackers exploit.",
    [e("SRC-ECH-UNB-BASELINE", "CNV-PLT-011"), s("SRC-WCAG-2.2", rel="informed-by"), s("SRC-NIST-SP800-63-4", rel="informed-by")],
    cls="customer-preference", imp="medium", ind=DAF + ["wealth-management"], jur=USF)

C.q(8, "Do you require step-up (fresh) authentication for high-risk actions such as changing payees or bank details, recommending large grants, exporting data, or changing who has authority on an account?",
    "A hijacked session is used to commit fraud without further challenge.",
    [d("SRC-FFIEC-AUTH-GUIDANCE-2021", rel="informed-by"), d("SRC-NIST-SP800-53-R5", "IA-11"), e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-003"), s("SRC-SA-SIG")],
    cls="supervisory-guidance", imp="critical", ind=FS, jur=USF, reg=FFIEC,
    alts=["Does the application require re-authentication for sensitive transactions?"])
C.q(8, "Is the step-up authentication bound to the specific action and its details, so that it cannot be replayed or reused to authorize a different action?",
    "An attacker reuses a legitimate step-up to authorize a different payee or amount.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-XIN-IAM-003"), s("SRC-MITRE-CWE", "CWE-294", "informed-by"), d("SRC-NIST-SP800-53-R5", "IA-2(8)")],
    cls="customer-preference", imp="high", ind=FS, jur=USF)
C.q(8, "How does your authentication approach implement layered, risk-based security for financial transactions consistent with the FFIEC 2021 authentication guidance, including anomaly detection and controls for higher-risk users?",
    "Single-layer authentication is insufficient for the risk of fund movement.",
    [d("SRC-FFIEC-AUTH-GUIDANCE-2021"), s("SRC-FFIEC-IS-BOOKLET", rel="informed-by"), e("SRC-ECH-UNB-BASELINE", "TVR-SEC-004")],
    cls="supervisory-guidance", imp="high", ind=BANK + ["wealth-management"], jur=USF, reg=FFIEC,
    note="FFIEC guidance is directed at financial institutions; it applies to Echelon only through the bank or partner customer's oversight and contract.")
C.q(8, "Are automatic approval limits tied to how strongly the user authenticated, so that a phishable session or an AI agent session cannot obtain an automatically approved grant to a new recipient?",
    "Account takeover yields auto-approved grants to attacker-controlled recipients.",
    [e("SRC-ECH-UNB-BASELINE", "TVR-SEC-004"), e("SRC-ECH-UNB-BASELINE", "TVR-SEC-010"), s("SRC-NACHA-FRAUD-MONITORING-2026", rel="informed-by")],
    cls="customer-preference", imp="high", ind=DAF, jur=USF)
C.q(8, "During step-up for a payment or grant, are the transaction details (recipient, amount) shown to the user so they confirm exactly what will execute?",
    "Malware alters transaction details while the user approves what they believe is a different transaction.",
    [s("SRC-FFIEC-AUTH-GUIDANCE-2021", rel="informed-by"), s("SRC-NIST-SP800-63-4", "SP 800-63B", "informed-by"), s("SRC-MITRE-ATTACK", "T1185")],
    cls="customer-preference", imp="medium", ind=FS, jur=USF)

C.q(9, "How do partner systems and integrations authenticate to your APIs, and do you ever issue shared static API keys?",
    "Static API keys are leaked and abused with broad scope.",
    [d("SRC-OWASP-API-TOP10-2023", "API2:2023"), e("SRC-ECH-UNB-BASELINE", "UNB-API-STD-005"), s("SRC-NIST-SP800-53-R5", "IA-9"), s("SRC-CSA-CAIQ-V4", "IAM domain")],
    cls="industry-convention", imp="high", ind=ENT + BANK, jur=GLOBAL,
    alts=["Describe the authentication mechanisms supported by your API."])
C.q(9, "When your giving widget or component is embedded on a partner's website, how is the user authenticated, and can scripts on the partner's page read the user's tokens or data?",
    "A compromised or malicious host page steals tokens or data from the embedded component.",
    [e("SRC-ECH-UNB-BASELINE", "AIN-029"), e("SRC-ECH-UNB-BASELINE", "TVR-WID-001"), s("SRC-OWASP-CHEATSHEETS", rel="informed-by"), s("SRC-PCI-DSS-4.0.1", "Req 6.4.3", "informed-by")],
    cls="customer-preference", imp="high", ind=DAF + ["banking", "wealth-management"], jur=USF)
C.q(9, "How do AI agents authenticate to your platform when acting for a user, and can an agent's credential ever carry more assurance or authority than the user who delegated to it?",
    "Agent credentials become a more powerful, less protected path than the user's own login.",
    [e("SRC-ECH-UNB-BASELINE", "TVR-SEC-004"), e("SRC-ECH-UNB-BASELINE", "UNB-AI-STD-001"), s("SRC-OWASP-AGENTIC-AI", rel="informed-by")],
    cls="customer-preference", imp="high", ind=ALL, jur=GLOBAL)
C.q(9, "How do you authenticate inbound webhooks and callbacks, and how do you prevent replay of captured messages?",
    "Forged or replayed callbacks change payment or grant status.",
    [e("SRC-ECH-UNB-BASELINE", "UNB-API-STD-005"), s("SRC-MITRE-CWE", "CWE-294", "informed-by"), s("SRC-MITRE-CWE", "CWE-345", "informed-by")],
    cls="industry-convention", imp="medium", ind=ENT, jur=GLOBAL)

print(C.emit())
