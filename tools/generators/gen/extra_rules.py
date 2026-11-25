rule("SEC-AUTH-003", "Authentication by default and approved identity", ["SEC-AUTH-001", "SEC-CRYPTO-001"],
 "Every endpoint requires an authenticated principal through a router fallback policy; anonymous access requires an explicit, reviewed exemption. Authentication uses an approved identity provider and standard protocol libraries with issuer, audience, algorithm and lifetime validation. Privileged roles require phishing-resistant multifactor authentication. Sessions have idle and absolute timeouts and are invalidated on logout and credential change.",
 "Missing authentication for critical functions is rank 21 in the 2025 Top 25. CWE 5.0 deprecated CWE-613 in favor of CWE-1462 and its descendants on session management.",
 "Route inventory from the router with authentication requirement; token validation tests; session tests; external testing.",
 ["Register a route without an exemption; anonymous request must receive 401.", "Present a token with the wrong audience; must be rejected.", "Use a session after logout; must be rejected."],
 ["Route inventory", "Token and session test results", "Identity provider configuration export"],
 ["Credential theft and phishing", "Identity provider compromise", "Support-desk social engineering"],
 "306 287 288 384 1462 1463 1464 1465 1466 1390 307 308", "L3", "Unbound platform")

rule("SEC-CRYPTO-002", "Banned cryptographic algorithms and APIs", ["SEC-CRYPTO-001"],
 "Application code must perform cryptography only through an approved facade. Direct use of MD5, SHA1 for security purposes, DES, TripleDES, RC2, ECB mode, RSA PKCS#1 v1.5 encryption padding, System.Random for security values, non-constant-time secret comparison, and certificate validation callbacks that accept all certificates is prohibited.",
 "SEC-CRYPTO-001 prohibits custom algorithms but does not list weak uses of approved libraries, which are the common failure.",
 "IL reference scan for banned types and members; facade API review; TLS configuration scanning.",
 ["Use MD5.Create in application code; gate must fail.", "Use System.Random to generate a token; gate must fail.", "Set ServerCertificateCustomValidationCallback to return true; gate must fail."],
 ["IL scan report", "Facade review record"],
 ["Platform crypto defects", "Key management failures"],
 "327 328 326 330 338 295 780 208 1240", "L5", "Echelon F# build baseline")

rule("SEC-CONFIG-001", "Secure configuration as code", ["SEC-SUPPLY-001", "SEC-CRYPTO-001"],
 "Deployed configuration is generated from reviewed code with secure defaults; Release builds only; no debug endpoints, verbose errors or sample credentials in production; secrets only from a managed secret service; drift is detected and alerts.",
 "Security Misconfiguration is A02 in OWASP Top 10 2025. Construction rules do not cover runtime configuration unless configuration is itself code with a gate.",
 "Configuration scanner in the release gate; drift detection; assembly metadata check for Release configuration.",
 ["Deploy with a Debug assembly; gate must fail.", "Enable a developer exception page in production configuration; gate must fail."],
 ["Configuration scan results", "Drift reports"],
 ["Console changes outside code", "Provider default changes"],
 "16 1188 11 489 756 260 526 942", "L5", "Praxis with Unbound platform")

rule("SEC-DATA-002", "Canonicalize, validate and encode at single boundaries", ["SEC-DATA-001", "SEC-UI-001"],
 "Each trust boundary has one decoder that canonicalizes (including Unicode normalization where identifiers or names are compared) before validation, and each output sink has one encoder module. Raw-string escape hatches in builders are prohibited.",
 "Validation before canonicalization and ad hoc encoding are recurring causes of injection and confusion weaknesses.",
 "Sink and boundary inventory; IL scan for direct sink use; property-based tests of decoders and encoders.",
 ["Submit an identifier differing only by Unicode normalization form; must compare equal or be rejected consistently.", "Export a value starting with = to CSV; must be neutralized."],
 ["Boundary and sink inventory", "Property test results"],
 ["Unknown downstream interpreters"],
 "20 179 180 176 116 838 1236 74 1007", "L2", "Unbound platform with Forma")
