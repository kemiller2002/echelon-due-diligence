---
id: DD-SBC-002
title: CWE architectural prevention matrix (generated summary)
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [security-by-construction, cwe, assurance, due-diligence]
related_documents:
  - security-by-construction/SECURITY-BY-CONSTRUCTION-RESEARCH-REPORT.md
  - security-by-construction/cwe-architectural-prevention-matrix.csv
  - security-by-construction/proposed-construction-rules.jsonl
---

# CWE architectural prevention matrix (summary)

This file is generated from `cwe-architectural-prevention-matrix.csv`, which is the canonical record. Do not edit this summary by hand; regenerate it. The generator script was run from a scratch location during research and is not committed; regenerating requires the same inputs (CWE 5.0 XML and the family definitions captured in the report's method section).

**Every row is a target.** No Unbound code exists, so `current_status` is `proposed-target-state` and `current_demonstrated_level` is `none` for all 353 rows. `strongest_achievable_level` is the strongest level the architecture could support within the stated scope if the evidence listed were produced; it is not a claim about today.

## Source catalog

- CWE List version 5.0, schema 8.0, catalog date 2026-10-28, downloaded 2026-11-25 from `https://cwe.mitre.org/data/xml/cwec_latest.xml.zip` (archive SHA-256 `bcda44c9abf61ff977f50c3c6649eea5a97a7b0626b0396c2c3ec4bfb973a3dc`; `cwec_v5.0.xml` SHA-256 `47165a9593def89c69b9ef50c34d99ac68db55df8373613e85e9cc9ceecefb1d`). The XML holds 984 Weakness elements, 956 not deprecated, matching the 956 weaknesses MITRE reports for 5.0. CWE 5.0 replaced Category elements with Grouping elements.
- 2025 CWE Top 25: view CWE-1435 in the catalog, ranks confirmed against `https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html` (page updated 2025-12-15). No 2026 Top 25 was published as of 2026-11-25.
- OWASP Top 10 2025: the CWE catalog's view CWE-1450 is labeled 'OWASP Top Ten RC1 (2025)' with groupings CWE-1436 to CWE-1445. The OWASP site presents the 2025 release; any differences between the final OWASP mappings and the RC1 view in CWE 5.0 were not reconciled here (open question).
- OWASP Top 10 2021: view CWE-1344, included for continuity because many questionnaires still cite 2021 categories.

## Coverage

| Measure | Count |
|---|---|
| Total CWE rows | 353 |
| 2025 Top 25 entries | 25 |
| Rows mapped to OWASP 2025 RC1 view | 247 |
| Rows mapped to OWASP 2021 view | 183 |
| Rows added only for financial web application relevance | 79 |
| Deprecated CWE entries retained for traceability | 3 |

## Strongest achievable assurance level (target, not current)

| Level | Meaning | Rows |
|---|---|---|
| L1 | Eliminated within defined scope | 32 |
| L2 | Type system | 89 |
| L3 | Restricted interface | 178 |
| L4 | Compiler enforcement | 18 |
| L5 | Build or release gate | 22 |
| L6 | Automated analysis | 0 |
| L7 | Property-based testing | 2 |
| L8 | Adversarial testing | 0 |
| L9 | Runtime monitoring | 1 |
| L10 | External or manual evaluation only | 11 |

## Relevance to a financial web application

| Relevance | Rows |
|---|---|
| critical | 26 |
| high | 107 |
| medium | 140 |
| low | 67 |
| not-applicable-in-scope | 13 |

## Architecture compared with conventional scanning

`architecture_vs_scanning` values: `beyond` means the architecture can establish a property that scanning cannot (absence of a capability, a type-level guarantee, or coverage of a class scanners do not model); `comparable` means scanners are already the principal control and architecture adds little; `complementary` means both are needed and neither dominates; `less` is not used for any whole class, but the report lists specific areas where the architecture provides less assurance than scanning would.

| Value | Rows |
|---|---|
| beyond | 202 |
| comparable | 89 |
| complementary | 62 |

| Conventional scanning detects | Rows |
|---|---|
| partial | 179 |
| yes | 115 |
| no | 59 |

## Control families

| Family | Name | Rows | Strongest level | Scanning | Architecture vs scanning |
|---|---|---|---|---|---|
| SQL | Database query injection | 3 | L1 | partial | beyond |
| INTERP | Other interpreter and output-format injection | 17 | L3 | partial | beyond |
| OSCMD | OS command and argument injection | 4 | L1 | partial | beyond |
| CODE | Dynamic code generation and evaluation | 6 | L1 | partial | beyond |
| XSS | Cross-site scripting and unsafe rendering | 6 | L3 | partial | beyond |
| BROWSER | Browser policy, origin and navigation controls | 17 | L3 | yes | comparable |
| CSRF | Cross-site request forgery | 1 | L3 | partial | beyond |
| MEM | Memory safety (managed code) | 10 | L1 | partial | beyond |
| NULL | Null dereference and uninitialized values | 4 | L2 | partial | beyond |
| NUM | Numeric correctness and money arithmetic | 12 | L2 | partial | beyond |
| RES | Resource exhaustion and algorithmic complexity | 17 | L3 | partial | complementary |
| DESER | Unsafe deserialization and mass assignment | 3 | L1 | yes | beyond |
| FILE | File system, path and upload handling | 23 | L3 | yes | beyond |
| SSRF | Server-side request forgery and outbound reference control | 3 | L3 | partial | beyond |
| XML | XML parsing hazards | 1 | L3 | yes | comparable |
| AUTHZ | Authorization and access control | 26 | L2 | no | beyond |
| TENANT | Tenant isolation | 6 | L2 | no | beyond |
| AUTHN | Authentication and session management | 45 | L3 | partial | complementary |
| CRYPTO | Cryptography and randomness | 36 | L3 | yes | comparable |
| SECRETS | Credentials and secrets in code or configuration | 9 | L5 | yes | comparable |
| INFO | Sensitive information exposure | 18 | L2 | partial | beyond |
| ERR | Exceptional condition handling | 15 | L4 | partial | beyond |
| INPUT | Input validation and canonicalization | 18 | L2 | partial | beyond |
| SUPPLY | Software supply chain and third-party components | 11 | L5 | yes | comparable |
| CONFIG | Security configuration and insecure defaults | 4 | L5 | yes | comparable |
| LOG | Security logging, audit and evidence provenance | 4 | L3 | no | beyond |
| CONC | Concurrency, idempotency and workflow integrity | 11 | L2 | no | beyond |
| DESIGN | Secure design principles | 8 | L10 | no | beyond |
| AI | AI components and AI-authored changes | 4 | L3 | no | beyond |
| NA | Platform-specific weakness outside the F# and .NET scope | 11 | L1 | yes | comparable |

## 2025 CWE Top 25

| Rank | CWE | Name | Family | Strongest achievable | Scope note | Scanning | Arch vs scan |
|---|---|---|---|---|---|---|---|
| 1 | CWE-79 | Improper Neutralization of Input During Web Page Generation | XSS | L3 | Limen provides component-level evidence of a restricted rendering interface; Unbound product evidence does not exist. | partial | beyond |
| 2 | CWE-89 | Improper Neutralization of Special Elements used in an SQL Command | SQL | L1 | The Standard's strongest claim | partial | beyond |
| 3 | CWE-352 | Cross-Site Request Forgery | CSRF | L3 |  | partial | beyond |
| 4 | CWE-862 | Missing Authorization | AUTHZ | L2 | Missing authorization is the class where construction can help most: if a state-changing operation's signature requires an Authorized value, a missing check becomes a compile error | no | beyond |
| 5 | CWE-787 | Out-of-bounds Write | MEM | L1 | Not reachable from verifiable managed F# code; reachable in runtime and native dependencies. | partial | beyond |
| 6 | CWE-22 | Improper Limitation of a Pathname to a Restricted Directory | FILE | L3 | If application code has no file system access, path traversal can only arise in the storage abstraction or dependencies. | yes | beyond |
| 7 | CWE-416 | Use After Free | MEM | L1 | Garbage collection prevents use after free in managed code; native handles and pooled buffers (ArrayPool returning buffers still referenced) are a managed analog that produces data exposure rather than memory corruption. | partial | beyond |
| 8 | CWE-125 | Out-of-bounds Read | MEM | L1 | Same scope as CWE-787. | partial | beyond |
| 9 | CWE-78 | Improper Neutralization of Special Elements used in an OS Command | OSCMD | L1 |  | partial | beyond |
| 10 | CWE-94 | Improper Control of Generation of Code | CODE | L1 | Includes CI workflow injection and template injection; runtime scope only for L1. | partial | beyond |
| 11 | CWE-120 | Buffer Copy without Checking Size of Input | MEM | L1 |  | partial | beyond |
| 12 | CWE-434 | Unrestricted Upload of File with Dangerous Type | FILE | L3 | Unbound may accept documents (grant paperwork, receipts); treat uploads as untrusted content. | yes | beyond |
| 13 | CWE-476 | NULL Pointer Dereference | NULL | L2 | In .NET a null dereference is a managed exception; risk is denial of service or fail-open handling. | partial | beyond |
| 14 | CWE-121 | Stack-based Buffer Overflow | MEM | L1 | stackalloc is the managed route to stack buffers and is banned by proposed SEC-MEM-001. | partial | beyond |
| 15 | CWE-502 | Deserialization of Untrusted Data | DESER | L1 | BinaryFormatter implementation is removed in .NET 9 (APIs throw PlatformNotSupportedException) unless the unsupported System.Runtime.Serialization.Formatters package is added. | yes | beyond |
| 16 | CWE-122 | Heap-based Buffer Overflow | MEM | L1 |  | partial | beyond |
| 17 | CWE-863 | Incorrect Authorization | AUTHZ | L7 | Incorrect authorization is a policy correctness problem; types ensure a decision exists, not that it is right | no | beyond |
| 18 | CWE-20 | Improper Input Validation | INPUT | L2 |  | partial | beyond |
| 19 | CWE-284 | Improper Access Control | AUTHZ | L2 | Pillar-level; covered through CWE-862, CWE-863, CWE-639 and tenant controls. | no | beyond |
| 20 | CWE-200 | Exposure of Sensitive Information to an Unauthorized Actor | INFO | L2 |  | partial | beyond |
| 21 | CWE-306 | Missing Authentication for Critical Functionality | AUTHN | L3 | A router fallback policy that requires authentication makes a missing check the default-safe case. | partial | complementary |
| 22 | CWE-918 | Server-Side Request Forgery | SSRF | L3 |  | partial | beyond |
| 23 | CWE-77 | Improper Neutralization of Special Elements used in a Command | OSCMD | L1 |  | partial | beyond |
| 24 | CWE-639 | Authorization Bypass Through User-Controlled Key | TENANT | L2 | Insecure direct object reference; tenant-scoped data interfaces and RLS give two independent layers. | no | beyond |
| 25 | CWE-770 | Allocation of Resources Without Limits or Throttling | RES | L3 |  | partial | complementary |

## All rows

| CWE | Name | Basis | Relevance | Family | Level | Supporting | Scan | Arch vs scan |
|---|---|---|---|---|---|---|---|---|
| CWE-5 | J2EE Misconfiguration: Data Transmission Without Encryption | O25 | high | INFO | L2 | L3, L5, L7, L9 | partial | beyond |
| CWE-11 | ASP.NET Misconfiguration: Creating Debug Binary | O25,O21 | low | CONFIG | L5 | L6, L9, L10 | yes | comparable |
| CWE-13 | ASP.NET Misconfiguration: Password in Configuration File | O25,O21 | medium | SECRETS | L5 | L6, L9 | yes | comparable |
| CWE-15 | External Control of System or Configuration Setting | O25,O21 | medium | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-16 | Configuration (grouping-level entry in CWE 5.0) | O25,O21 | medium | CONFIG | L5 | L6, L9, L10 | yes | comparable |
| CWE-20 | Improper Input Validation | T25,O25,O21 | high | INPUT | L2 | L3, L4, L7 | partial | beyond |
| CWE-22 | Improper Limitation of a Pathname to a Restricted Directory | T25,O25,O21 | high | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-23 | Relative Path Traversal | O25,O21 | medium | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-35 | Path Traversal: '.../...//' | O21 | low | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-36 | Absolute Path Traversal | O25 | medium | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-59 | Improper Link Resolution Before File Access | O25,O21 | low | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-61 | UNIX Symbolic Link (Symlink) Following | O25 | low | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-65 | Windows Hard Link | O25 | low | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-73 | External Control of File Name or Path | O25,O21 | medium | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-74 | Improper Neutralization of Special Elements in Output Used by a Downstream Component | O25,O21 | high | INTERP | L3 | L2, L5, L6, L7 | partial | beyond |
| CWE-75 | Failure to Sanitize Special Elements into a Different Plane | O21 | low | INTERP | L3 | L2, L5, L6, L7 | partial | beyond |
| CWE-76 | Improper Neutralization of Equivalent Special Elements | O25 | low | INTERP | L3 | L2, L5, L6, L7 | partial | beyond |
| CWE-77 | Improper Neutralization of Special Elements used in a Command | T25,O25,O21 | high | OSCMD | L1 | L5, L6 | partial | beyond |
| CWE-78 | Improper Neutralization of Special Elements used in an OS Command | T25,O25,O21 | high | OSCMD | L1 | L5, L6 | partial | beyond |
| CWE-79 | Improper Neutralization of Input During Web Page Generation | T25,O25,O21 | critical | XSS | L3 | L2, L5, L6, L8, L9 | partial | beyond |
| CWE-80 | Improper Neutralization of Script-Related HTML Tags in a Web Page | O25,O21 | high | XSS | L3 | L2, L5, L6, L8, L9 | partial | beyond |
| CWE-83 | Improper Neutralization of Script in Attributes in a Web Page | O25,O21 | high | XSS | L3 | L2, L5, L6, L8, L9 | partial | beyond |
| CWE-86 | Improper Neutralization of Invalid Characters in Identifiers in Web Pages | O25 | low | XSS | L3 | L2, L5, L6, L8, L9 | partial | beyond |
| CWE-87 | Improper Neutralization of Alternate XSS Syntax | O21 | medium | XSS | L3 | L2, L5, L6, L8, L9 | partial | beyond |
| CWE-88 | Improper Neutralization of Argument Delimiters in a Command | O25,O21 | medium | OSCMD | L1 | L5, L6 | partial | beyond |
| CWE-89 | Improper Neutralization of Special Elements used in an SQL Command | T25,O25,O21 | critical | SQL | L1 | L3, L4, L5, L6, L8 | partial | beyond |
| CWE-90 | Improper Neutralization of Special Elements used in an LDAP Query | O25,O21 | low | INTERP | L3 | L2, L5, L6, L7 | partial | beyond |
| CWE-91 | XML Injection | O25,O21 | low | INTERP | L3 | L2, L5, L6, L7 | partial | beyond |
| CWE-93 | Improper Neutralization of CRLF Sequences | O25,O21 | medium | INTERP | L3 | L2, L5, L6, L7 | partial | beyond |
| CWE-94 | Improper Control of Generation of Code | T25,O25,O21 | high | CODE | L1 | L5, L6, L8 | partial | beyond |
| CWE-95 | Improper Neutralization of Directives in Dynamically Evaluated Code | O25,O21 | medium | CODE | L1 | L5, L6, L8 | partial | beyond |
| CWE-96 | Improper Neutralization of Directives in Statically Saved Code | O25,O21 | low | CODE | L1 | L5, L6, L8 | partial | beyond |
| CWE-97 | Improper Neutralization of Server-Side Includes (SSI) Within a Web Page | O25,O21 | not-applicable-in-scope | NA | L1 | L5 | yes | comparable |
| CWE-98 | Improper Control of Filename for Include/Require Statement in PHP Program | O25,O21 | not-applicable-in-scope | NA | L1 | L5 | yes | comparable |
| CWE-99 | Improper Control of Resource Identifiers | O25,O21 | medium | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-103 | Struts: Incomplete validate() Method Definition | O25 | not-applicable-in-scope | NA | L1 | L5 | yes | comparable |
| CWE-104 | Struts: Form Bean Does Not Extend Validation Class | O25 | not-applicable-in-scope | NA | L1 | L5 | yes | comparable |
| CWE-112 | Missing XML Validation | O25 | low | XML | L3 | L5, L6, L7 | yes | comparable |
| CWE-113 | Improper Neutralization of CRLF Sequences in HTTP Headers | O25,O21 | medium | INTERP | L3 | L2, L5, L6, L7 | partial | beyond |
| CWE-114 | Process Control | O25 | low | OSCMD | L1 | L5, L6 | partial | beyond |
| CWE-115 | Misinterpretation of Input | O25 | medium | INPUT | L2 | L3, L4, L7 | partial | beyond |
| CWE-116 | Improper Encoding or Escaping of Output | O25,O21 | high | INTERP | L3 | L2, L5, L6, L7 | partial | beyond |
| CWE-117 | Improper Output Neutralization for Logs | O25,O21 | high | INTERP | L2 | L3, L7 | partial | beyond |
| CWE-120 | Buffer Copy without Checking Size of Input | T25 | high | MEM | L1 | L4, L5, L6 | partial | beyond |
| CWE-121 | Stack-based Buffer Overflow | T25 | high | MEM | L1 | L4, L5, L6 | partial | beyond |
| CWE-122 | Heap-based Buffer Overflow | T25 | high | MEM | L1 | L4, L5, L6 | partial | beyond |
| CWE-125 | Out-of-bounds Read | T25 | high | MEM | L1 | L4, L5, L6 | partial | beyond |
| CWE-128 | Wrap-around Error | FIN | critical | NUM | L4 | L2, L5, L7 | partial | beyond |
| CWE-129 | Improper Validation of Array Index | O25 | medium | MEM | L2 | L4, L7 | partial | beyond |
| CWE-138 | Improper Neutralization of Special Elements | O21 | medium | INTERP | L3 | L2, L5, L6, L7 | partial | beyond |
| CWE-159 | Improper Handling of Invalid Use of Special Elements | O25 | low | INTERP | L3 | L2, L5, L6, L7 | partial | beyond |
| CWE-176 | Improper Handling of Unicode Encoding | FIN | medium | INPUT | L2 | L3, L4, L7 | partial | beyond |
| CWE-179 | Incorrect Behavior Order: Early Validation | FIN | medium | INPUT | L2 | L3, L4, L7 | partial | beyond |
| CWE-180 | Incorrect Behavior Order: Validate Before Canonicalize | FIN | medium | INPUT | L2 | L3, L4, L7 | partial | beyond |
| CWE-183 | Permissive List of Allowed Inputs | O25,O21 | medium | INPUT | L2 | L3, L4, L7 | partial | beyond |
| CWE-184 | Incomplete List of Disallowed Inputs | O21 | medium | INPUT | L2 | L3, L4, L7 | partial | beyond |
| CWE-185 | Incorrect Regular Expression | FIN | medium | INPUT | L2 | L3, L4, L7 | partial | beyond |
| CWE-190 | Integer Overflow or Wraparound | FIN | critical | NUM | L4 | L2, L5, L7 | partial | beyond |
| CWE-191 | Integer Underflow (Wrap or Wraparound) | FIN | critical | NUM | L4 | L2, L5, L7 | partial | beyond |
| CWE-197 | Numeric Truncation Error | FIN | critical | NUM | L4 | L2, L7 | partial | beyond |
| CWE-200 | Exposure of Sensitive Information to an Unauthorized Actor | T25,O25,O21 | high | INFO | L2 | L3, L5, L7, L9 | partial | beyond |
| CWE-201 | Insertion of Sensitive Information Into Sent Data | O25,O21 | high | INFO | L2 | L3, L5, L7, L9 | partial | beyond |
| CWE-203 | Observable Discrepancy | FIN | medium | INFO | L2 | L3, L5, L7, L9 | partial | beyond |
| CWE-204 | Observable Response Discrepancy | FIN | medium | INFO | L2 | L3, L5, L7, L9 | partial | beyond |
| CWE-208 | Observable Timing Discrepancy | FIN | medium | INFO | L3 | L3, L5, L7, L9 | partial | beyond |
| CWE-209 | Generation of Error Message Containing Sensitive Information | O25,O21 | high | INFO | L2 | L3, L5, L7, L9 | partial | beyond |
| CWE-212 | Improper Removal of Sensitive Information Before Storage or Transfer | FIN | high | INFO | L2 | L3, L5, L7, L9 | partial | beyond |
| CWE-213 | Exposure of Sensitive Information Due to Incompatible Policies | O21 | medium | TENANT | L2 | L3, L7, L8, L9, L10 | no | beyond |
| CWE-215 | Insertion of Sensitive Information Into Debugging Code | O25 | medium | INFO | L2 | L3, L5, L7, L9 | partial | beyond |
| CWE-219 | Storage of File with Sensitive Data Under Web Root | O25,O21 | low | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-221 | Information Loss or Omission | O25 | medium | LOG | L3 | L2, L7, L9, L10 | no | beyond |
| CWE-223 | Omission of Security-relevant Information | O25,O21 | high | LOG | L3 | L2, L7, L9, L10 | no | beyond |
| CWE-226 | Sensitive Information in Resource Not Removed Before Reuse | FIN | medium | INFO | L2 | L3, L5, L7, L9 | partial | beyond |
| CWE-234 | Failure to Handle Missing Parameter | O25 | medium | INPUT | L2 | L3, L4, L7 | partial | beyond |
| CWE-235 | Improper Handling of Extra Parameters | O25,O21 | medium | INPUT | L2 | L3, L4, L7 | partial | beyond |
| CWE-248 | Uncaught Exception | O25 | high | ERR | L4 | L2, L6, L7, L8 | partial | beyond |
| CWE-250 | Execution with Unnecessary Privileges | FIN | high | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-252 | Unchecked Return Value | O25 | high | ERR | L4 | L2, L6, L7, L8 | partial | beyond |
| CWE-256 | Plaintext Storage of a Password | O25,O21 | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-257 | Storing Passwords in a Recoverable Format | O21 | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-258 | Empty Password in Configuration File | O25 | low | SECRETS | L5 | L6, L9 | yes | comparable |
| CWE-259 | Use of Hard-coded Password | O25,O21 | high | SECRETS | L5 | L6, L9 | yes | comparable |
| CWE-260 | Password in Configuration File | O25,O21 | medium | SECRETS | L5 | L6, L9 | yes | comparable |
| CWE-261 | Weak Encoding for Password | O25,O21 | low | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-266 | Incorrect Privilege Assignment | O25,O21 | medium | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-269 | Improper Privilege Management | O25,O21 | high | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-274 | Improper Handling of Insufficient Privileges | O25 | medium | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-276 | Incorrect Default Permissions | O25,O21 | medium | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-280 | Improper Handling of Insufficient Permissions or Privileges | O25,O21 | medium | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-281 | Improper Preservation of Permissions | O25 | low | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-282 | Improper Ownership Management | O25 | low | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-283 | Unverified Ownership | O25 | low | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-284 | Improper Access Control | T25,O25,O21 | critical | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-285 | Improper Authorization | O25,O21 | critical | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-286 | Incorrect User Management | O25 | medium | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-287 | Improper Authentication | O25,O21 | critical | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-288 | Authentication Bypass Using an Alternate Path or Channel | O25,O21 | high | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-289 | Authentication Bypass by Alternate Name | O25 | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-290 | Authentication Bypass by Spoofing | O25,O21 | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-291 | Reliance on IP Address for Authentication | O25 | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-293 | Using Referer Field for Authentication | O25 | low | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-294 | Authentication Bypass by Capture-replay | O25,O21 | high | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-295 | Improper Certificate Validation | O25,O21 | high | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-296 | Improper Following of a Certificate's Chain of Trust | O25,O21 | medium | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-297 | Improper Validation of Certificate with Host Mismatch | O25,O21 | medium | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-298 | Improper Validation of Certificate Expiration | O25 | medium | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-299 | Improper Check for Certificate Revocation | O25 | medium | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-300 | Channel Accessible by Non-Endpoint | O25,O21 | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-302 | Authentication Bypass by Assumed-Immutable Data | O25,O21 | medium | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-303 | Incorrect Implementation of Authentication Algorithm | O25 | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-304 | Missing Critical Step in Authentication | O25,O21 | high | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-305 | Authentication Bypass by Primary Weakness | O25 | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-306 | Missing Authentication for Critical Functionality | T25,O25,O21 | critical | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-307 | Improper Restriction of Excessive Authentication Attempts | O25,O21 | high | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-308 | Use of Single-factor Authentication | O25 | high | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-309 | Use of Password System for Primary Authentication | O25 | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-311 | Missing Encryption of Sensitive Data | O25,O21 | high | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-312 | Cleartext Storage of Sensitive Information | O25,O21 | high | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-313 | Cleartext Storage in a File or on Disk | O25,O21 | medium | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-315 | Cleartext Storage of Sensitive Information in a Cookie | O25,O21 | medium | BROWSER | L3 | L5, L6, L8, L9 | yes | comparable |
| CWE-316 | Cleartext Storage of Sensitive Information in Memory | O25,O21 | low | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-319 | Cleartext Transmission of Sensitive Information | O25,O21 | high | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-321 | Use of Hard-coded Cryptographic Key | O25,O21 | high | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-322 | Key Exchange without Entity Authentication | O25,O21 | low | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-323 | Reusing a Nonce, Key Pair in Encryption | O25,O21 | medium | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-324 | Use of a Key Past its Expiration Date | O25,O21 | medium | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-325 | Missing Cryptographic Step | O25,O21 | medium | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-326 | Inadequate Encryption Strength | O25,O21 | high | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-327 | Use of a Broken or Risky Cryptographic Algorithm | O25,O21 | high | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-328 | Use of Weak Hash | O25,O21 | medium | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-329 | Generation of Predictable IV with CBC Mode | O25,O21 | low | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-330 | Use of Insufficiently Random Values | O25,O21 | high | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-331 | Insufficient Entropy | O25,O21 | medium | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-332 | Insufficient Entropy in PRNG | O25 | low | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-334 | Small Space of Random Values | O25 | medium | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-335 | Incorrect Usage of Seeds in Pseudo-Random Number Generator (PRNG) | O25,O21 | low | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-336 | Same Seed in Pseudo-Random Number Generator (PRNG) | O25,O21 | low | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-337 | Predictable Seed in Pseudo-Random Number Generator (PRNG) | O25,O21 | low | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-338 | Use of Cryptographically Weak Pseudo-Random Number Generator (PRNG) | O25,O21 | high | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-340 | Generation of Predictable Numbers or Identifiers | O25,O21 | high | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-342 | Predictable Exact Value from Previous Values | O25 | medium | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-345 | Insufficient Verification of Data Authenticity | O25,O21 | high | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-346 | Origin Validation Error | O25,O21 | medium | BROWSER | L3 | L5, L6, L8, L9 | yes | comparable |
| CWE-347 | Improper Verification of Cryptographic Signature | O25,O21 | high | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-348 | Use of Less Trusted Source | FIN | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-349 | Acceptance of Extraneous Untrusted Data With Trusted Data | FIN | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-350 | Reliance on Reverse DNS Resolution for a Security-Critical Action | O25 | low | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-352 | Cross-Site Request Forgery | T25,O25,O21 | critical | CSRF | L3 | L5, L8 | partial | beyond |
| CWE-353 | Missing Support for Integrity Check | O25,O21 | medium | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-359 | Exposure of Private Personal Information to an Unauthorized Actor | O25,O21 | critical | INFO | L2 | L3, L5, L7, L9 | partial | beyond |
| CWE-362 | Concurrent Execution using Shared Resource with Improper Synchronization | O25 | critical | CONC | L2 | L3, L7, L8 | no | beyond |
| CWE-366 | Race Condition within a Thread | FIN | medium | CONC | L2 | L3, L7, L8 | no | beyond |
| CWE-367 | Time-of-check Time-of-use (TOCTOU) Race Condition | FIN | high | CONC | L2 | L3, L7, L8 | no | beyond |
| CWE-369 | Divide By Zero | O25 | critical | NUM | L2 | L4, L7 | partial | beyond |
| CWE-377 | DEPRECATED: Insecure Temporary File | O25,O21 | low | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-379 | Creation of Temporary File in Directory with Insecure Permissions | O25 | low | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-382 | J2EE Bad Practices: Use of System.exit() | O25 | not-applicable-in-scope | NA | L1 | L5 | yes | comparable |
| CWE-384 | Session Fixation | O25,O21 | high | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-390 | Detection of Error Condition Without Action | O25 | medium | ERR | L4 | L2, L6, L7, L8 | partial | beyond |
| CWE-391 | DEPRECATED: Unchecked Error Condition | O25 | low | ERR | L4 | L2, L6, L7, L8 | partial | beyond |
| CWE-394 | Unexpected Status Code or Return Value | O25 | medium | ERR | L4 | L2, L6, L7, L8 | partial | beyond |
| CWE-396 | Declaration of Catch for Generic Exception | O25 | medium | ERR | L4 | L2, L6, L7, L8 | partial | beyond |
| CWE-397 | Declaration of Throws for Generic Exception | O25 | low | ERR | L4 | L2, L6, L7, L8 | partial | beyond |
| CWE-400 | Uncontrolled Resource Consumption | FIN | high | RES | L3 | L2, L5, L7, L8, L9 | partial | complementary |
| CWE-401 | Missing Release of Memory after Effective Lifetime | FIN | low | MEM | L9 | L7 | partial | beyond |
| CWE-402 | Transmission of Private Resources into a New Sphere | O25,O21 | medium | TENANT | L2 | L3, L7, L8, L9, L10 | no | beyond |
| CWE-404 | Improper Resource Shutdown or Release | FIN | medium | RES | L3 | L2, L5, L7, L8, L9 | partial | complementary |
| CWE-405 | Asymmetric Resource Consumption (Amplification) | FIN | medium | RES | L3 | L2, L5, L7, L8, L9 | partial | complementary |
| CWE-407 | Inefficient Algorithmic Complexity | FIN | medium | RES | L3 | L2, L5, L7, L8, L9 | partial | complementary |
| CWE-409 | Improper Handling of Highly Compressed Data (Data Amplification) | FIN | medium | RES | L3 | L2, L5, L7, L8, L9 | partial | complementary |
| CWE-416 | Use After Free | T25 | high | MEM | L1 | L4, L5, L6 | partial | beyond |
| CWE-419 | Unprotected Primary Channel | O25,O21 | medium | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-424 | Improper Protection of Alternate Path | O25 | medium | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-425 | Direct Request | O25,O21 | high | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-426 | Untrusted Search Path | O25,O21 | low | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-427 | Uncontrolled Search Path Element | O25 | low | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-430 | Deployment of Wrong Handler | O21 | low | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-434 | Unrestricted Upload of File with Dangerous Type | T25,O25,O21 | high | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-436 | Interpretation Conflict | O25 | medium | INPUT | L2 | L3, L4, L7 | partial | beyond |
| CWE-441 | Unintended Proxy or Intermediary | O25,O21 | medium | BROWSER | L3 | L5, L6, L8, L9 | yes | comparable |
| CWE-444 | Inconsistent Interpretation of HTTP Requests | O25,O21 | medium | INPUT | L10 | L5, L8 | partial | beyond |
| CWE-447 | Unimplemented or Unsupported Feature in UI | O25 | low | DESIGN | L10 | L8 | no | beyond |
| CWE-451 | User Interface (UI) Misrepresentation of Critical Information | O25,O21 | high | DESIGN | L10 | L8 | no | beyond |
| CWE-454 | External Initialization of Trusted Variables or Data Stores | O25 | medium | INPUT | L2 | L3, L4, L7 | partial | beyond |
| CWE-457 | Use of Uninitialized Variable | FIN | low | NULL | L1 | L4, L6, L7 | partial | beyond |
| CWE-460 | Improper Cleanup on Thrown Exception | O25 | medium | ERR | L4 | L2, L6, L7, L8 | partial | beyond |
| CWE-470 | Use of Externally-Controlled Input to Select Classes or Code | O25,O21 | high | CODE | L1 | L5, L6, L8 | partial | beyond |
| CWE-471 | Modification of Assumed-Immutable Data (MAID) | O21 | medium | CODE | L2 | L4 | partial | beyond |
| CWE-472 | External Control of Assumed-Immutable Web Parameter | O25,O21 | high | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-476 | NULL Pointer Dereference | T25,O25 | high | NULL | L2 | L4, L6, L7 | partial | beyond |
| CWE-477 | Use of Obsolete Function | O25 | medium | SUPPLY | L5 | L6, L9, L10 | yes | comparable |
| CWE-478 | Missing Default Case in Multiple Condition Expression | O25 | high | ERR | L4 | L5 | partial | beyond |
| CWE-484 | Omitted Break Statement in Switch | O25 | not-applicable-in-scope | ERR | L1 | L2, L6, L7, L8 | partial | beyond |
| CWE-489 | Active Debug Code | O25 | medium | INFO | L2 | L3, L5, L7, L9 | partial | beyond |
| CWE-493 | Critical Public Variable Without Final Modifier | O25 | not-applicable-in-scope | NA | L1 | L5 | yes | comparable |
| CWE-494 | Download of Code Without Integrity Check | O25,O21 | high | SUPPLY | L5 | L6, L9, L10 | yes | comparable |
| CWE-497 | Exposure of Sensitive System Information to an Unauthorized Control Sphere | O25,O21 | medium | INFO | L2 | L3, L5, L7, L9 | partial | beyond |
| CWE-500 | Public Static Field Not Marked Final | O25 | not-applicable-in-scope | NA | L1 | L5 | yes | comparable |
| CWE-501 | Trust Boundary Violation | O25,O21 | high | INPUT | L2 | L3, L4, L7 | partial | beyond |
| CWE-502 | Deserialization of Untrusted Data | T25,O25,O21 | high | DESER | L1 | L3, L5, L6 | yes | beyond |
| CWE-506 | Embedded Malicious Code | O25 | high | SUPPLY | L10 | L5, L6 | yes | comparable |
| CWE-509 | Replicating Malicious Code (Virus or Worm) | O25 | low | SUPPLY | L10 | L5, L6 | yes | comparable |
| CWE-520 | .NET Misconfiguration: Use of Impersonation | O21 | low | CONFIG | L5 | L6, L9, L10 | yes | comparable |
| CWE-521 | Weak Password Requirements | O25,O21 | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-522 | Insufficiently Protected Credentials | O25,O21 | high | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-523 | Unprotected Transport of Credentials | O25,O21 | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-525 | Use of Web Browser Cache Containing Sensitive Information | O25,O21 | medium | BROWSER | L3 | L5, L6, L8, L9 | yes | comparable |
| CWE-526 | Cleartext Storage of Sensitive Information in an Environment Variable | O25,O21 | medium | SECRETS | L5 | L6, L9 | yes | comparable |
| CWE-532 | Insertion of Sensitive Information into Log File | O25,O21 | high | INFO | L2 | L3, L5, L7, L9 | partial | beyond |
| CWE-537 | Java Runtime Error Message Containing Sensitive Information | O21 | not-applicable-in-scope | NA | L1 | L5 | yes | comparable |
| CWE-538 | Insertion of Sensitive Information into Externally-Accessible File or Directory | O25,O21 | medium | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-539 | Use of Persistent Cookies Containing Sensitive Information | O25,O21 | medium | BROWSER | L3 | L5, L6, L8, L9 | yes | comparable |
| CWE-540 | Inclusion of Sensitive Information in Source Code | O25,O21 | medium | SECRETS | L5 | L6, L9 | yes | comparable |
| CWE-541 | Inclusion of Sensitive Information in an Include File | O21 | low | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-547 | Use of Hard-coded, Security-relevant Constants | O25,O21 | medium | SECRETS | L5 | L6, L9 | yes | comparable |
| CWE-548 | Exposure of Information Through Directory Listing | O25,O21 | low | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-550 | Server-generated Error Message Containing Sensitive Information | O25 | medium | INFO | L2 | L3, L5, L7, L9 | partial | beyond |
| CWE-552 | Files or Directories Accessible to External Parties | O25,O21 | medium | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-564 | Use of Hibernate with HQL/SQL Query String Containing External Input | O25,O21 | low | SQL | L1 | L3, L4, L5, L6, L8 | partial | beyond |
| CWE-565 | Reliance on Cookies without Validation and Integrity Checking | O25,O21 | medium | BROWSER | L3 | L5, L6, L8, L9 | yes | comparable |
| CWE-566 | Authorization Bypass Through User-Controlled SQL Primary Key | O25,O21 | high | TENANT | L2 | L3, L7, L8, L9, L10 | no | beyond |
| CWE-579 | J2EE Bad Practices: Non-serializable Object Stored in Session | O21 | not-applicable-in-scope | NA | L1 | L5 | yes | comparable |
| CWE-598 | Use of HTTP Request With Sensitive Query String | O25,O21 | medium | INFO | L2 | L3, L5, L7, L9 | partial | beyond |
| CWE-601 | URL Redirection to Untrusted Site | O25,O21 | high | BROWSER | L3 | L5, L6, L8, L9 | yes | comparable |
| CWE-602 | Client-Side Enforcement of Server-Side Security | O25,O21 | high | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-606 | Unchecked Input for Loop Condition | FIN | medium | RES | L3 | L2, L5, L7, L8, L9 | partial | complementary |
| CWE-610 | Externally Controlled Reference to a Resource in Another Sphere | O25,O21 | medium | SSRF | L3 | L5, L8, L9 | partial | beyond |
| CWE-611 | Improper Restriction of XML External Entity Reference | O25,O21 | medium | SSRF | L3 | L5, L8, L9 | partial | beyond |
| CWE-613 | DEPRECATED: Insufficient Session Expiration | O25,O21 | low | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-614 | Sensitive Cookie in HTTPS Session Without 'Secure' Attribute | O25,O21 | high | BROWSER | L3 | L5, L6, L8, L9 | yes | comparable |
| CWE-615 | Inclusion of Sensitive Information in Source Code Comments | O25 | low | SECRETS | L5 | L6, L9 | yes | comparable |
| CWE-620 | Unverified Password Change | O25,O21 | high | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-628 | Function Call with Incorrectly Specified Arguments | O25 | low | ERR | L2 | L4 | partial | beyond |
| CWE-636 | Not Failing Securely | O25 | critical | ERR | L4 | L2, L6, L7, L8 | partial | beyond |
| CWE-639 | Authorization Bypass Through User-Controlled Key | T25,O25,O21 | critical | TENANT | L2 | L3, L7, L8, L9, L10 | no | beyond |
| CWE-640 | Weak Password Recovery Mechanism for Forgotten Password | O25,O21 | high | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-642 | External Control of Critical State Data | O25,O21 | high | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-643 | Improper Neutralization of Data within XPath Expressions | O25,O21 | low | INTERP | L3 | L2, L5, L6, L7 | partial | beyond |
| CWE-644 | Improper Neutralization of HTTP Headers for Scripting Syntax | O25,O21 | low | XSS | L3 | L2, L5, L6, L8, L9 | partial | beyond |
| CWE-646 | Reliance on File Name or Extension of Externally-Supplied File | O25,O21 | medium | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-650 | Trusting HTTP Permission Methods on the Server Side | O21 | low | BROWSER | L3 | L5, L6, L8, L9 | yes | comparable |
| CWE-651 | Exposure of WSDL File Containing Sensitive Information | O21 | not-applicable-in-scope | INFO | L2 | L3, L5, L7, L9 | partial | beyond |
| CWE-652 | Improper Neutralization of Data within XQuery Expressions | O21 | low | INTERP | L3 | L2, L5, L6, L7 | partial | beyond |
| CWE-653 | Improper Isolation or Compartmentalization | O25,O21 | high | TENANT | L2 | L3, L7, L8, L9, L10 | no | beyond |
| CWE-656 | Reliance on Security Through Obscurity | O25,O21 | medium | DESIGN | L10 | L8 | no | beyond |
| CWE-657 | Violation of Secure Design Principles | O25,O21 | medium | DESIGN | L10 | L8 | no | beyond |
| CWE-662 | Improper Synchronization | FIN | medium | CONC | L2 | L3, L7, L8 | no | beyond |
| CWE-665 | Improper Initialization | FIN | low | NULL | L2 | L4, L6, L7 | partial | beyond |
| CWE-667 | Improper Locking | FIN | medium | CONC | L2 | L3, L7, L8 | no | beyond |
| CWE-668 | Exposure of Resource to Wrong Sphere | O25,O21 | high | TENANT | L2 | L3, L7, L8, L9, L10 | no | beyond |
| CWE-674 | Uncontrolled Recursion | FIN | high | RES | L3 | L4, L7 | partial | complementary |
| CWE-676 | Use of Potentially Dangerous Function | O25 | medium | SUPPLY | L5 | L6, L9, L10 | yes | comparable |
| CWE-681 | Incorrect Conversion between Numeric Types | FIN | critical | NUM | L4 | L2, L7 | partial | beyond |
| CWE-682 | Incorrect Calculation | FIN | critical | NUM | L7 | L2, L8, L10 | partial | beyond |
| CWE-693 | Protection Mechanism Failure | O25 | high | DESIGN | L10 | L8 | no | beyond |
| CWE-703 | Improper Check or Handling of Exceptional Conditions | O25 | high | ERR | L4 | L2, L6, L7, L8 | partial | beyond |
| CWE-704 | Incorrect Type Conversion or Cast | FIN | medium | MEM | L2 | L4, L7 | partial | beyond |
| CWE-706 | Use of Incorrectly-Resolved Name or Reference | O21 | low | FILE | L3 | L1, L5, L6, L8 | yes | beyond |
| CWE-732 | Incorrect Permission Assignment for Critical Resource | O25 | high | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-749 | Exposed Dangerous Method or Function | O25 | medium | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-754 | Improper Check for Unusual or Exceptional Conditions | O25 | high | ERR | L4 | L2, L6, L7, L8 | partial | beyond |
| CWE-755 | Improper Handling of Exceptional Conditions | O25 | high | ERR | L4 | L2, L6, L7, L8 | partial | beyond |
| CWE-756 | Missing Custom Error Page | O25,O21 | medium | INFO | L2 | L3, L5, L7, L9 | partial | beyond |
| CWE-757 | Selection of Less-Secure Algorithm During Negotiation | O25,O21 | medium | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-759 | Use of a One-Way Hash without a Salt | O25,O21 | low | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-760 | Use of a One-Way Hash with a Predictable Salt | O25,O21 | low | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-770 | Allocation of Resources Without Limits or Throttling | T25 | high | RES | L3 | L2, L5, L7, L8, L9 | partial | complementary |
| CWE-772 | Missing Release of Resource after Effective Lifetime | FIN | medium | RES | L3 | L2, L5, L7, L8, L9 | partial | complementary |
| CWE-776 | Improper Restriction of Recursive Entity References in DTDs | O25,O21 | medium | RES | L3 | L2, L5, L7, L8, L9 | partial | complementary |
| CWE-778 | Insufficient Logging | O25,O21 | critical | LOG | L3 | L2, L7, L9, L10 | no | beyond |
| CWE-779 | Logging of Excessive Data | FIN | medium | LOG | L3 | L2, L7, L9, L10 | no | beyond |
| CWE-780 | Use of RSA Algorithm without OAEP | O25,O21 | low | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-784 | Reliance on Cookies without Validation and Integrity Checking in a Security Decision | O25,O21 | medium | BROWSER | L3 | L5, L6, L8, L9 | yes | comparable |
| CWE-787 | Out-of-bounds Write | T25 | high | MEM | L1 | L4, L5, L6 | partial | beyond |
| CWE-789 | Memory Allocation with Excessive Size Value | FIN | high | RES | L3 | L2, L5, L7, L8, L9 | partial | complementary |
| CWE-798 | Use of Hard-coded Credentials | O25,O21 | high | SECRETS | L5 | L6, L9 | yes | comparable |
| CWE-799 | Improper Control of Interaction Frequency | O25,O21 | high | RES | L3 | L2, L5, L7, L8, L9 | partial | complementary |
| CWE-807 | Reliance on Untrusted Inputs in a Security Decision | O25,O21 | high | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-820 | Missing Synchronization | FIN | medium | CONC | L2 | L3, L7, L8 | no | beyond |
| CWE-821 | Incorrect Synchronization | FIN | medium | CONC | L2 | L3, L7, L8 | no | beyond |
| CWE-829 | Inclusion of Functionality from Untrusted Control Sphere | O25,O21 | high | SUPPLY | L5 | L6, L9, L10 | yes | comparable |
| CWE-830 | Inclusion of Web Functionality from an Untrusted Source | O25,O21 | high | BROWSER | L3 | L5, L6, L8, L9 | yes | comparable |
| CWE-833 | Deadlock | FIN | medium | CONC | L2 | L3, L7, L8 | no | beyond |
| CWE-834 | Excessive Iteration | FIN | medium | RES | L3 | L2, L5, L7, L8, L9 | partial | complementary |
| CWE-835 | Loop with Unreachable Exit Condition | FIN | medium | RES | L3 | L2, L5, L7, L8, L9 | partial | complementary |
| CWE-837 | Improper Enforcement of a Single, Unique Action | FIN | critical | CONC | L3 | L7, L8 | no | beyond |
| CWE-838 | Inappropriate Encoding for Output Context | FIN | high | INTERP | L3 | L2, L5, L6, L7 | partial | beyond |
| CWE-839 | Numeric Range Comparison Without Minimum Check | FIN | critical | NUM | L2 | L4, L5, L6, L7 | partial | beyond |
| CWE-841 | Improper Enforcement of Behavioral Workflow | O25,O21 | critical | CONC | L2 | L3, L7, L8 | no | beyond |
| CWE-843 | Access of Resource Using Incompatible Type | FIN | low | MEM | L1 | L4, L5, L6 | partial | beyond |
| CWE-862 | Missing Authorization | T25,O25,O21 | critical | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-863 | Incorrect Authorization | T25,O25,O21 | critical | AUTHZ | L7 | L2, L8, L10 | no | beyond |
| CWE-908 | Use of Uninitialized Resource | FIN | low | NULL | L2 | L4, L6, L7 | partial | beyond |
| CWE-912 | Hidden Functionality | FIN | medium | SUPPLY | L5 | L6, L9, L10 | yes | comparable |
| CWE-913 | Improper Control of Dynamically-Managed Code Resources | O21 | medium | CODE | L1 | L5, L6, L8 | partial | beyond |
| CWE-915 | Improperly Controlled Modification of Dynamically-Determined Object Attributes | O25,O21 | high | DESER | L2 | L3, L5, L7 | yes | beyond |
| CWE-916 | Use of Password Hash With Insufficient Computational Effort | O25,O21 | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-917 | Improper Neutralization of Special Elements used in an Expression Language Statement | O25,O21 | low | INTERP | L3 | L2, L5, L6, L7 | partial | beyond |
| CWE-918 | Server-Side Request Forgery | T25,O25,O21 | high | SSRF | L3 | L5, L8, L9 | partial | beyond |
| CWE-922 | Insecure Storage of Sensitive Information | O25,O21 | high | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-926 | Improper Export of Android Application Components | O25 | not-applicable-in-scope | NA | L1 | L5 | yes | comparable |
| CWE-927 | Use of Implicit Intent for Sensitive Communication | O21 | not-applicable-in-scope | NA | L1 | L5 | yes | comparable |
| CWE-940 | Improper Verification of Source of a Communication Channel | O25,O21 | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-941 | Incorrectly Specified Destination in a Communication Channel | O25 | low | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-942 | Permissive Cross-domain Security Policy with Untrusted Domains | O25,O21 | high | BROWSER | L3 | L5, L6, L8, L9 | yes | comparable |
| CWE-943 | Improper Neutralization of Special Elements in Data Query Logic | FIN | medium | SQL | L3 | L5, L6, L8 | partial | beyond |
| CWE-1004 | Sensitive Cookie Without 'HttpOnly' Flag | O25,O21 | high | BROWSER | L3 | L5, L6, L8, L9 | yes | comparable |
| CWE-1021 | Improper Restriction of Rendered UI Layers or Frames | O25,O21 | high | BROWSER | L3 | L5, L6, L8, L9 | yes | comparable |
| CWE-1022 | Use of Web Link to Untrusted Target with window.opener Access | O25 | low | BROWSER | L3 | L5, L6, L8, L9 | yes | comparable |
| CWE-1039 | Inadequate Detection or Handling of Adversarial Input Perturbations in Automated Recognition Mechanism | FIN | low | AI | L3 | L5, L8, L9, L10 | no | beyond |
| CWE-1050 | Excessive Platform Resource Consumption within a Loop | FIN | low | RES | L3 | L2, L5, L7, L8, L9 | partial | complementary |
| CWE-1059 | Insufficient Technical Documentation | FIN | low | DESIGN | L10 | L8 | no | beyond |
| CWE-1068 | Inconsistency Between Implementation and Documented Design | FIN | medium | DESIGN | L10 | L8 | no | beyond |
| CWE-1077 | Floating Point Comparison with Incorrect Operator | FIN | medium | NUM | L2 | L4, L5, L6, L7 | partial | beyond |
| CWE-1104 | Use of Unmaintained Third Party Components | O25,O21 | high | SUPPLY | L5 | L6, L9, L10 | yes | comparable |
| CWE-1125 | Excessive Attack Surface | O25 | medium | DESIGN | L10 | L8 | no | beyond |
| CWE-1173 | Improper Use of Validation Framework | O21 | medium | INPUT | L2 | L3, L4, L7 | partial | beyond |
| CWE-1174 | ASP.NET Misconfiguration: Improper Model Validation | O25,O21 | medium | INPUT | L2 | L3, L4, L7 | partial | beyond |
| CWE-1188 | Initialization of a Resource with an Insecure Default | FIN | high | CONFIG | L5 | L6, L9, L10 | yes | comparable |
| CWE-1220 | Insufficient Granularity of Access Control | FIN | high | AUTHZ | L2 | L3, L5, L7, L8, L10 | no | beyond |
| CWE-1236 | Improper Neutralization of Formula Elements in a CSV File | FIN | high | INTERP | L3 | L2, L5, L6, L7 | partial | beyond |
| CWE-1240 | Use of a Cryptographic Primitive with a Risky Implementation | O25 | medium | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-1241 | Use of Predictable Algorithm in Random Number Generator | O25 | medium | CRYPTO | L3 | L5, L6, L10 | yes | comparable |
| CWE-1265 | Unintended Reentrant Invocation of Non-reentrant Code Via Nested Calls | FIN | low | CONC | L2 | L3, L7, L8 | no | beyond |
| CWE-1275 | Sensitive Cookie with Improper SameSite Attribute | O25,O21 | high | BROWSER | L3 | L5, L6, L8, L9 | yes | comparable |
| CWE-1284 | Improper Validation of Specified Quantity in Input | FIN | critical | NUM | L2 | L4, L5, L6, L7 | partial | beyond |
| CWE-1286 | Improper Validation of Syntactic Correctness of Input | FIN | high | INPUT | L2 | L3, L4, L7 | partial | beyond |
| CWE-1287 | Improper Validation of Specified Type of Input | FIN | high | INPUT | L2 | L3, L4, L7 | partial | beyond |
| CWE-1321 | Improperly Controlled Modification of Object Prototype Attributes | FIN | medium | DESER | L3 | L3, L5, L6 | yes | beyond |
| CWE-1325 | Improperly Controlled Sequential Memory Allocation | FIN | low | RES | L3 | L2, L5, L7, L8, L9 | partial | complementary |
| CWE-1329 | Reliance on Component That is Not Updateable | O25 | medium | SUPPLY | L5 | L6, L9, L10 | yes | comparable |
| CWE-1333 | Inefficient Regular Expression Complexity | FIN | high | RES | L3 | L5, L6, L7 | partial | complementary |
| CWE-1336 | Improper Neutralization of Special Elements Used in a Template Engine | FIN | medium | INTERP | L3 | L2, L5, L6, L7 | partial | beyond |
| CWE-1339 | Insufficient Precision or Accuracy of a Real Number | FIN | critical | NUM | L2 | L4, L5, L6, L7 | partial | beyond |
| CWE-1357 | Reliance on Insufficiently Trustworthy Component | FIN | high | SUPPLY | L5 | L6, L9, L10 | yes | comparable |
| CWE-1385 | Missing Origin Validation in WebSockets | FIN | low | BROWSER | L3 | L5, L6, L8, L9 | yes | comparable |
| CWE-1389 | Incorrect Parsing of Numbers with Different Radices | FIN | medium | NUM | L3 | L4, L5, L6, L7 | partial | beyond |
| CWE-1390 | Weak Authentication | O25 | high | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-1391 | Use of Weak Credentials | O25 | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-1392 | Use of Default Credentials | O25 | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-1393 | Use of Default Password | O25 | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-1395 | Dependency on Vulnerable Third-Party Component | O25 | high | SUPPLY | L5 | L6, L9, L10 | yes | comparable |
| CWE-1426 | Improper Validation of Generative AI Output | FIN | high | AI | L3 | L5, L8, L9, L10 | no | beyond |
| CWE-1427 | Improper Neutralization of Input Used for LLM Prompting | FIN | high | AI | L3 | L5, L8, L9, L10 | no | beyond |
| CWE-1434 | Insecure Setting of Generative AI/ML Model Inference Parameters | FIN | medium | AI | L3 | L5, L8, L9, L10 | no | beyond |
| CWE-1462 | Improper Session Management | FIN | high | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-1463 | Insufficient Session Timeout Value | FIN | high | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-1464 | Improper Session Invalidation | FIN | high | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-1465 | Improper Session Invalidation after User Logout | FIN | high | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-1466 | Improper Session Invalidation after Authentication Credential Change | FIN | high | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-1467 | Use of Singular Authentication Artifact for Multiple User Sessions | FIN | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-1469 | Improper Check for Credential Expiration | FIN | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |
| CWE-1472 | Generation of Credential with Long Expiration | FIN | medium | AUTHN | L3 | L5, L8, L10 | partial | complementary |

Basis codes: T25 = 2025 CWE Top 25; O25 = CWE view of OWASP Top 10 2025 RC1; O21 = CWE view of OWASP Top 10 2021; FIN = added for financial web application relevance.
