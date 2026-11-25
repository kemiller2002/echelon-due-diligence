from common import *

NL = NIST_LIC
CSAF = "https://csrc.nist.gov/pubs/"
recs = []
a = recs.append

# ---------------- Questionnaires and assurance programs ----------------
a(R("SRC-SA-SIG",
    "Shared Assessments Standardized Information Gathering (SIG) Questionnaire",
    "Shared Assessments (The Santa Fe Group)", "questionnaire", "market-practice",
    "SIG 2026 confirmed on issuer product page (mappings list 'Shared Assessments SCA 2026'); a 'Product Release 2027' was reported by a search snippet of the issuer homepage but could not be confirmed directly",
    "unknown",
    "https://sharedassessments.org/sig-excel/",
    "Customer convention, not law. Financial-institution-affiliated DAF sponsors and their parent banks or broker-dealers commonly run third-party risk programs on SIG Lite or SIG Core, so Unbound should expect SIG-derived questionnaires during onboarding. Echelon is not obliged to license SIG to answer a customer's SIG; the customer holds the license. Echelon should map its canonical questions to SIG domains by identifier only. Applicability to Echelon as a vendor: likely (customer-driven). Applicability as a certification: none; SIG is not a certification.",
    "Licensed product. Issuer page lists a paid annual corporate license (USD 7,000 per year shown 2026-11-25) or access through membership. SIG content is proprietary and may not be copied or redistributed; Echelon must not reproduce SIG question text in this repository and may cite SIG domain or question identifiers only (operating contract rule 5).",
    "Issuer pages other than the SIG Excel page redirect to a Microsoft Entra sign-in for automated clients, so release notes, current release year and license agreement text could not be read. SIG states it maps to ISO 27001/27002:2022, ISO 27701, ISO 42001, NIST 800-53, NIST CSF 2.0, NIST 800-171r3, PCI DSS 4.0, CIS v8, DORA, GLBA-related FFIEC booklets and others; mapping quality was not evaluated.",
    "current",
    V(False, "Fetched issuer SIG Excel page (version list, mappings, price) 2026-11-25; other issuer pages blocked by SSO redirect; current release year (2026 versus 2027) not confirmed; publication date unknown.",
      "https://sharedassessments.org/sig-excel/"),
    jur=["global"], ind=["financial-services", "cross-industry"],
    rel=["SRC-SA-SCA", "SRC-ISO-27001-2022", "SRC-NIST-SP800-53-R5", "SRC-PCI-DSS-4.0.1", "SRC-NIST-CSF-2.0"],
    notes="Open question: confirm whether SIG 2027 has been released and what changed (AI, supply chain)."))

a(R("SRC-SA-SCA", "Shared Assessments Standardized Control Assessment (SCA)",
    "Shared Assessments (The Santa Fe Group)", "questionnaire", "market-practice",
    "SCA 2026 referenced on the SIG Excel page; current release not otherwise confirmed",
    "unknown", "https://sharedassessments.org/sca/",
    "Customer convention. SCA is the onsite or remote control-verification companion to SIG used by outsourcers to test vendor answers. A financial-institution-affiliated sponsor could use SCA procedures to test Unbound controls after contract. Not binding. Echelon should expect evidence requests aligned to SCA procedures only for higher-risk relationships.",
    "Licensed Shared Assessments product; same restrictions as SIG. Do not reproduce procedures.",
    "Issuer SCA page redirects to SSO for automated clients; contents and terms not read.",
    "unknown",
    V(False, "Issuer page https://sharedassessments.org/sca/ redirected to Microsoft Entra sign-in; only the 'SCA 2026' mapping reference on the SIG Excel page was observed.",
      "https://sharedassessments.org/sig-excel/"),
    jur=["global"], ind=["financial-services"], rel=["SRC-SA-SIG"]))

a(R("SRC-CSA-CAIQ-V4", "STAR Level 1: Security Questionnaire (CAIQ v4.1)",
    "Cloud Security Alliance", "questionnaire", "market-practice", "4.1 (supersedes CAIQ v4.0.3)",
    "2026-01-27", "https://cloudsecurityalliance.org/artifacts/star-level-1-security-questionnaire-caiq-v4-1",
    "Customer convention and self-assessment vehicle. Many SaaS buyers accept a completed CAIQ in lieu of a custom questionnaire. For Unbound, a public CAIQ (optionally a STAR Level 1 registry listing) is a low-cost transparency artifact, but it is a self-attestation (first-party) and must reflect the honest proposed-target-state posture. Applicability: optional, likely useful.",
    "CSA research publications: free download; per CSA website terms, publications may be used, copied and printed but not modified or translated without CSA consent, must keep notices, and commercial use of CCM/CAIQ inside products or consulting requires a CSA license (CCM page: license not needed for internal use). Echelon may answer a CAIQ and reference question IDs; embedding CAIQ text in a commercial product or service requires a license.",
    "Yes/No format with comments; answers are self-asserted. Seed title said v4; current version is 4.1. Release date shown is the date on the CSA artifact page.",
    "current",
    V(True, "Fetched CSA artifact pages for CAIQ v4.1 and CCM/CAIQ v4.1 and CSA website terms 2026-11-25.",
      "https://cloudsecurityalliance.org/artifacts/cloud-controls-matrix-v4-1"),
    jur=["global"], ind=["cloud", "cross-industry"], rel=["SRC-CSA-CCM-V4", "SRC-CSA-STAR"],
    notes="Version correction: seed referenced v4; CAIQ v4.1 released 2026-01-27 per CSA."))

a(R("SRC-CSA-CCM-V4", "Cloud Controls Matrix (CCM) v4.1",
    "Cloud Security Alliance", "framework", "voluntary-standard",
    "4.1 (207 controls, 17 domains)", "2026-01-27",
    "https://cloudsecurityalliance.org/artifacts/cloud-controls-matrix-v4-1",
    "Voluntary control framework and the basis for CAIQ and STAR. Useful to Echelon as a mapping hub because CCM v4.1 ships mappings (including NIST 800-171 rev.2, MITRE ATT&CK v17.1, DORA reverse mapping) and a machine-readable bundle. No legal force for Echelon or Unbound.",
    "Free to download. CCM page states a license is needed to customize CCM or use it for commercial purposes (products, consulting); not needed for internal use. CSA publications may not be modified or translated without consent and must retain notices.",
    "Mappings are CSA's; verify against source standards before relying on them in customer responses.",
    "current",
    V(True, "Fetched CSA CCM page and CCM/CAIQ v4.1 artifact page 2026-11-25.",
      "https://cloudsecurityalliance.org/research/cloud-controls-matrix"),
    jur=["global"], ind=["cloud"], rel=["SRC-CSA-CAIQ-V4", "SRC-CSA-STAR", "SRC-CSA-AICM"],
    notes="Version correction: seed referenced v4; current is v4.1."))

a(R("SRC-CSA-STAR", "CSA Security, Trust, Assurance and Risk (STAR) Program and Registry",
    "Cloud Security Alliance", "certification-scheme", "certification-criteria",
    "Program (Level 1 self-assessment, Level 2 third-party; STAR for AI with AICM/AI-CAIQ)", "unknown",
    "https://cloudsecurityalliance.org/star",
    "Voluntary assurance program. Level 1 (CAIQ self-assessment listing) is achievable for Unbound before audits; Level 2 requires third-party attestation or certification (for example SOC 2 or ISO 27001 based). Applicability: optional customer-facing signal; not required by law.",
    "Registry listing subject to CSA program terms; CAIQ/AICM licensing as noted in their records.",
    "Level 1 is first-party; do not present it as independent assurance. Issuer page shows 4,237 registry listings as of 2026-11-25.",
    "current",
    V(True, "Fetched CSA STAR program page 2026-11-25.", "https://cloudsecurityalliance.org/star"),
    jur=["global"], ind=["cloud"], rel=["SRC-CSA-CAIQ-V4", "SRC-CSA-AICM", "SRC-AICPA-SOC2-GUIDE", "SRC-ISO-27001-2022"]))

VSA_LIC = ("VSA limited license (quoted on issuer page 2026-11-25): users may download and reproduce and distribute unmodified copies solely for evaluating their own internal security processes and the security practices of their direct vendors, or to give feedback. All other uses are prohibited, expressly including use in connection with a security consulting or hosted vendor management service. Registration required. Echelon may answer a VSA questionnaire sent by a customer but must not embed VSA text in a product or service.")
a(R("SRC-VSA-FULL", "VSA FULL 2027 questionnaire", "Vendor Security Alliance", "questionnaire", "market-practice",
    "VSA FULL 2027 (up to 278 questions, 21 sections, 39 AI questions)", "unknown",
    "https://www.vendorsecurityalliance.org/",
    "Customer convention, mostly technology-sector buyers. Relevant to Unbound if sponsors or their affiliates use VSA. 2027 edition adds AI sections (customer data used for training, AI governance, AI security) and US, EU/UK, India and Philippines privacy modules, which overlap Unbound concerns. Not binding.",
    VSA_LIC,
    "Publication date of the 2027 editions not stated on the page; the page states the first VSA questionnaire was released 1 October 2016. Reviewer weights are guidance with no automated score.",
    "current",
    V(True, "Fetched issuer home page 2026-11-25 (edition counts and license text); publication date not stated.",
      "https://www.vendorsecurityalliance.org/"),
    jur=["global"], ind=["technology"], rel=["SRC-VSA-CORE"],
    notes="Version correction: seed title had no edition; current editions are labeled 2027."))
a(R("SRC-VSA-CORE", "VSA CORE 2027 questionnaire", "Vendor Security Alliance", "questionnaire", "market-practice",
    "VSA CORE 2027 (up to 122 questions; every CORE question appears verbatim in FULL)", "unknown",
    "https://www.vendorsecurityalliance.org/",
    "Customer convention for lower-risk services or first-pass review. Likely what a smaller sponsor would send if it used VSA. Not binding.",
    VSA_LIC, "Same as VSA FULL.", "current",
    V(True, "Fetched issuer home page 2026-11-25.", "https://www.vendorsecurityalliance.org/"),
    jur=["global"], ind=["technology"], rel=["SRC-VSA-FULL"]))

a(R("SRC-GOOGLE-VSAQ", "VSAQ: Vendor Security Assessment Questionnaire (open-source application and templates)",
    "Google (repository google/vsaq; README states it is not an official Google product)", "tool", "market-practice",
    "unknown (repository; no release version confirmed)", "unknown", "https://github.com/google/vsaq",
    "Historical open-source questionnaire templates (web application, infrastructure, physical, privacy). Low current market relevance; useful only as an openly licensed reference for writing original questions. Not binding.",
    "Apache License 2.0 (LICENSE file fetched from the repository).",
    "README states VSAQ is not an official Google product. Repository activity and archive status could not be checked (GitHub HTML and API blocked for this session).",
    "unknown",
    V(True, "Fetched README.md and LICENSE via raw.githubusercontent.com 2026-11-25; repository status not checked.",
      "https://raw.githubusercontent.com/google/vsaq/master/README.md"),
    jur=["global"], ind=["technology"],
    notes="Seed title attributed VSAQ to Google as a product; README says it is code owned by Google, not an official product."))

a(R("SRC-EDUCAUSE-HECVAT", "Higher Education Community Vendor Assessment Toolkit (HECVAT) 4",
    "EDUCAUSE (HEISC community group)", "questionnaire", "market-practice",
    "HECVAT 4, build 4.1.6 reported by search result for the EDUCAUSE page (not directly fetched)", "2025-02 (HECVAT 4 launch, per EDUCAUSE Review article in search results)",
    "https://www.educause.edu/higher-education-community-vendor-assessment-toolkit",
    "Customer convention in higher education. Relevant only if Unbound serves university-affiliated foundations or community foundations that borrow higher-ed procurement. HECVAT 4 consolidated Full, Lite and On-Prem into one file and adds AI, privacy and accessibility questions. Applicability: unlikely unless that segment is targeted.",
    "Not confirmed. Search results indicate EDUCAUSE obtained copyright and trademarked the HECVAT name, and EDUCAUSE Review articles are CC BY-NC-ND 4.0; the toolkit's own terms of use were not read. Treat as restricted until confirmed.",
    "educause.edu returned HTTP 403 to curl and WebFetch; all facts from search-result snippets of issuer domains.",
    "current",
    V(False, "Not verified: issuer site blocked (HTTP 403); version and date taken from search snippets of educause.edu pages.",
      "https://www.educause.edu/higher-education-community-vendor-assessment-toolkit"),
    jur=["US"], ind=["higher-education"],
    notes="Open question: confirm HECVAT current build and license terms directly with EDUCAUSE."))

# ---------------- NIST ----------------
def nist(id, title, ver, pub, url, app, lim, status="current", rel=None, notes=None, sup=None, method=None, jur=None):
    return R(id, title, "National Institute of Standards and Technology (NIST)",
             "framework" if id in ("SRC-NIST-CSF-2.0",) else "standard", "voluntary-standard", ver, pub, url, app,
             NL, lim, status,
             V(True, method or "Fetched issuer CSRC publication page 2026-11-25.", url),
             jur=jur or ["US"], ind=["cross-industry"], rel=rel, notes=notes, sup=sup)

a(nist("SRC-NIST-CSF-2.0", "The NIST Cybersecurity Framework (CSF) 2.0 (NIST CSWP 29)", "2.0", "2024-02-26",
       "https://csrc.nist.gov/pubs/cswp/29/the-nist-cybersecurity-framework-csf-20/final",
       "Voluntary framework and lingua franca of bank and sponsor TPRM programs (SIG and many bank questionnaires map to it; FFIEC CAT sunset pushed banks toward CSF). Recommended as Echelon's top-level outcome taxonomy. Not binding on Echelon or Unbound.",
       "Outcome-based; does not prescribe controls or provide certification.",
       rel=["SRC-NIST-SP800-53-R5", "SRC-NIST-SP800-61-R3"]))
a(nist("SRC-NIST-SP800-53-R5", "SP 800-53 Rev. 5, Security and Privacy Controls for Information Systems and Organizations",
       "Rev. 5, Release 5.2.0 (minor release 2025-08-27 adding SA-15(13), SA-24, SI-02(07) and revising SI-07(12))", "2020-09 (updates through 2025-08-27)",
       "https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final",
       "Binding only on federal systems via FISMA/OMB; for Echelon it is a voluntary reference catalog that FedRAMP, CMMC (via 800-171) and many questionnaires derive from. Use control IDs as cross-reference anchors. Not applicable as a requirement unless a federal or FedRAMP context arises.",
       "Very large catalog; selecting controls requires a baseline (800-53B) or tailoring.",
       rel=["SRC-NIST-SP800-53B", "SRC-FEDRAMP"],
       notes="Release 5.2.0 adds software update and patch integrity related controls (per CSRC planning note)."))
a(nist("SRC-NIST-SP800-53B", "SP 800-53B, Control Baselines for Information Systems and Organizations",
       "Release 5.2.0 (2025-08-27; no baseline changes)", "2020-10 (updates through 2025-08-27)",
       "https://csrc.nist.gov/pubs/sp/800/53/b/upd1/final",
       "Federal baselines (low, moderate, high, privacy). Relevant to Echelon only as the source of FedRAMP and GovRAMP baselines. Not applicable otherwise.",
       "Federal-system orientation.", rel=["SRC-NIST-SP800-53-R5", "SRC-FEDRAMP", "SRC-STATERAMP"]))
a(nist("SRC-NIST-SP800-171-R3", "SP 800-171 Rev. 3, Protecting Controlled Unclassified Information in Nonfederal Systems and Organizations",
       "Rev. 3", "2024-05-14", "https://csrc.nist.gov/pubs/sp/800/171/r3/final",
       "Binding only through contract (DFARS 252.204-7012, CMMC, other agency CUI clauses). Unbound handles no CUI; not applicable unless Echelon takes federal or defense work. Note CMMC Level 2 still references Rev. 2 per 32 CFR 170 (not re-verified here).",
       "CUI-specific.", rel=["SRC-CMMC-2.0"]))
a(nist("SRC-NIST-SP800-218", "SP 800-218, Secure Software Development Framework (SSDF) Version 1.1",
       "1.1 (final); Rev. 1 (SSDF 1.2) initial public draft published 2025-12-17", "2022-02-03",
       "https://csrc.nist.gov/pubs/sp/800/218/final",
       "Voluntary. Primary secure-development reference for Echelon's Secure Construction Standard and for federal-style attestation questions. OMB M-26-05 (2026-01-23) rescinded mandatory federal attestation but still points agencies to SP 800-218. Applicability: strongly relevant voluntary framework; no legal obligation for Echelon.",
       "Practice-level; does not prescribe tools. SSDF 1.2 draft may change practices.",
       rel=["SRC-NIST-SP800-218-R1-IPD", "SRC-NIST-SP800-218A", "SRC-OMB-M-26-05", "SRC-CISA-SSDF-ATTESTATION"]))
a(nist("SRC-NIST-SP800-218A", "SP 800-218A, Secure Software Development Practices for Generative AI and Dual-Use Foundation Models: An SSDF Community Profile",
       "Final", "2024-07-26", "https://csrc.nist.gov/pubs/sp/800/218/a/final",
       "Voluntary. Aimed mainly at AI model producers and those fine-tuning models. Relevant to Echelon only to the extent Unbound trains or fine-tunes models; if it only consumes third-party models, most practices are inherited from the model provider. Applicability: partial.",
       "Model-producer focus.", rel=["SRC-NIST-SP800-218", "SRC-NIST-AI-600-1"]))
a(nist("SRC-NIST-SP800-61-R3", "SP 800-61 Rev. 3, Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile",
       "Rev. 3 (supersedes Rev. 2, 2012)", "2025-04-03", "https://csrc.nist.gov/pubs/sp/800/61/r3/final",
       "Voluntary incident response reference organized by CSF 2.0. Sponsors' incident notification clauses (and bank 36-hour notification flow-down via the 2021 computer-security incident notification rule) make incident response a near-certain diligence topic for Unbound.",
       "Rev. 3 dropped the detailed handling checklists of Rev. 2; questionnaires written against Rev. 2 may still reference them.",
       rel=["SRC-NIST-CSF-2.0"]))
a(nist("SRC-NIST-SP800-63-4", "SP 800-63-4, Digital Identity Guidelines",
       "Revision 4 (final; supersedes SP 800-63-3)", "2025-07-31", "https://csrc.nist.gov/pubs/sp/800/63/4/final",
       "Binding for federal agencies; voluntary for Echelon. Directly relevant to Unbound donor and sponsor-staff authentication design (AAL, phishing-resistant authenticators, identity proofing for donors). Financial-institution sponsors will ask about MFA strength in FFIEC authentication terms.",
       "Volumes 63A, 63B, 63C carry the detailed requirements.", rel=["SRC-NIST-CSF-2.0"]))
a(nist("SRC-NIST-SP800-161-R1", "SP 800-161 Rev. 1, Cybersecurity Supply Chain Risk Management Practices for Systems and Organizations",
       "Rev. 1, update 1 (2024-11-01)", "2022-05 (updated 2024-11-01)", "https://csrc.nist.gov/pubs/sp/800/161/r1/upd1/final",
       "Voluntary C-SCRM reference; acquirer perspective. Useful for Echelon's own supplier management and for anticipating customer supply-chain questions. Not binding.",
       "Federal acquirer orientation; long.", rel=["SRC-ISO-27036"]))
a(nist("SRC-NIST-SP800-88", "SP 800-88 Rev. 2, Guidelines for Media Sanitization",
       "Rev. 2 (final; supersedes Rev. 1 of 2014-12-17)", "2025-09-26", "https://csrc.nist.gov/pubs/sp/800/88/r2/final",
       "Voluntary; frequently cited in questionnaires about data destruction at contract end. Unbound runs on cloud infrastructure, so sanitization is largely inherited from the cloud provider plus cryptographic erase of tenant keys. Customer questionnaires may still cite Rev. 1.",
       "Rev. 2 restructured content; questionnaires referencing Rev. 1 terms (clear, purge, destroy) should be mapped carefully.",
       notes="Version correction: current revision is Rev. 2 (September 2025)."))
a(nist("SRC-NIST-SP800-207", "SP 800-207, Zero Trust Architecture", "Final", "2020-08-11",
       "https://csrc.nist.gov/pubs/sp/800/207/final",
       "Voluntary architecture reference. Relevant as design vocabulary for Unbound; customers occasionally ask about zero trust posture. Not binding.",
       "Conceptual; no conformance criteria."))
a(R("SRC-NIST-IR-8397", "NIST IR 8397, Guidelines on Minimum Standards for Developer Verification of Software",
    "National Institute of Standards and Technology (NIST)", "industry-guidance", "voluntary-standard", "Final",
    "2021-10-06", "https://csrc.nist.gov/pubs/ir/8397/final",
    "Voluntary; lists minimum verification techniques (threat modeling, automated testing, static and dynamic analysis, fuzzing, secret scanning). Directly relevant to Echelon's verification program and to answering 'how do you test your code' questions. Not binding.",
    NL, "Minimum techniques, not effectiveness thresholds.", "current",
    V(True, "Fetched issuer CSRC publication page 2026-11-25.", "https://csrc.nist.gov/pubs/ir/8397/final"),
    jur=["US"], ind=["software"], rel=["SRC-NIST-SP800-218"]))

# ---------------- CIS ----------------
a(R("SRC-CIS-CONTROLS-V8.1", "CIS Critical Security Controls v8.1", "Center for Internet Security (CIS)",
    "framework", "voluntary-standard", "8.1", "unknown",
    "https://www.cisecurity.org/controls/v8-1",
    "Voluntary prioritized safeguards with Implementation Groups (IG1 suits a small company). Appropriate baseline for Echelon's corporate IT. Some state safe-harbor statutes reference recognized frameworks including CIS Controls (not verified here). Not binding.",
    "CIS non-member terms (fetched): CIS Controls and associated guidance are licensed under CC BY-NC-ND 4.0. Non-commercial, no derivatives: Echelon may cite safeguard IDs and use internally, but must not redistribute modified versions or embed in commercial products.",
    "v8.1 release date not shown on fetched pages.", "current",
    V(True, "Fetched CIS Controls and v8.1 pages and CIS non-member terms of use 2026-11-25; release date not confirmed.",
      "https://www.cisecurity.org/terms-of-use-for-non-member-cis-products"),
    jur=["global"], ind=["cross-industry"], rel=["SRC-CIS-BENCHMARKS"]))
a(R("SRC-CIS-BENCHMARKS", "CIS Benchmarks", "Center for Internet Security (CIS)", "standard", "voluntary-standard",
    "Per-product benchmarks with individual versions (100+ configuration guides)", "unknown",
    "https://www.cisecurity.org/cis-benchmarks",
    "Voluntary configuration hardening guides; customers ask whether hosts, containers and cloud accounts follow CIS Benchmarks. Relevant to Unbound's cloud and container configuration. Not binding.",
    "CIS non-member terms: PDF versions of CIS Benchmarks are licensed under CC BY-NC-SA 4.0. Tooling (CIS-CAT Pro), Hardened Images and some formats require CIS SecureSuite membership.",
    "Each benchmark has its own version and date; record the specific benchmark used.", "current",
    V(True, "Fetched CIS Benchmarks page and non-member terms 2026-11-25.", "https://www.cisecurity.org/cis-benchmarks"),
    jur=["global"], ind=["cross-industry"], rel=["SRC-CIS-CONTROLS-V8.1"]))

# ---------------- AICPA ----------------
AICPA_LIC = ("AICPA copyrighted material. The 2017 TSC download is free with an account and carries a copyright notice; AICPA guides are sold (e-book or print). Per AICPA terms on the standards listing, professional standards may be used only for the user's own professional purposes. Cite criteria identifiers (for example CC6.1) and paraphrase; do not republish criteria text or points of focus.")
a(R("SRC-AICPA-TSC", "2017 Trust Services Criteria for Security, Availability, Processing Integrity, Confidentiality, and Privacy (With Revised Points of Focus, 2022)",
    "AICPA Assurance Services Executive Committee (ASEC)", "certification-scheme", "certification-criteria",
    "2017 TSC with revised points of focus (2022); proposed 2027 TSC exposed for comment 2026-11-16", "2022 (resource posted 2023-09-30)",
    "https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022",
    "Certification criteria used in SOC 2 examinations. The most commonly requested assurance artifact from US financial-institution customers is a SOC 2 Type 2 report; Unbound has none. Criteria become relevant when Echelon engages a CPA firm. Not law.",
    AICPA_LIC,
    "Proposed 2027 TSC may change criteria; an engagement started in 2027 or later may use the revised set (effective date not verified).",
    "current",
    V(True, "Fetched AICPA TSC download page and AICPA SOC 2 landing page 2026-11-25.",
      "https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022"),
    jur=["US"], ind=["cross-industry"], rel=["SRC-AICPA-SOC2-GUIDE", "SRC-AICPA-TSC-2027-ED", "SRC-AICPA-PRIVACY-CRITERIA"]))
a(R("SRC-AICPA-TSC-2027-ED", "AICPA Exposure Drafts: Proposed 2027 SOC 2 Trust Services Criteria and Description Criteria",
    "AICPA Assurance Services Executive Committee (ASEC)", "certification-scheme", "certification-criteria",
    "Exposure draft (proposed)", "2026-11-16",
    "https://www.aicpa-cima.com/resources/download/aicpa-exposure-drafts-proposed-2027-soc-2-trust-services-criteria-and-description-criteria",
    "Not yet effective. Material to Echelon's SOC 2 readiness timing: Unbound's first SOC 2 may fall under the revised criteria, so readiness work should track the draft. No obligation.",
    AICPA_LIC + " Exposure drafts are for comment only.",
    "Comment deadline and final effective date not captured in this pass.", "proposed",
    V(True, "Fetched AICPA exposure draft download page 2026-11-25.",
      "https://www.aicpa-cima.com/resources/download/aicpa-exposure-drafts-proposed-2027-soc-2-trust-services-criteria-and-description-criteria"),
    jur=["US"], ind=["cross-industry"], rel=["SRC-AICPA-TSC"],
    notes="Newly discovered source (not in seed list). Open question: comment deadline and planned effective date."))
a(R("SRC-AICPA-SOC2-GUIDE", "SOC 2 Reporting on an Examination of Controls at a Service Organization Relevant to Security, Availability, Processing Integrity, Confidentiality, or Privacy (AICPA Guide)",
    "AICPA", "industry-guidance", "certification-criteria", "October 2022 edition (product AAGSOP22E)", "2022-10-15",
    "https://www.aicpa-cima.com/cpe-learning/publication/soc-2-reporting-on-an-examination-of-controls-at-a-service-organization-relevant-to-security-availability-processing-integrity-confidentiality-or-privacy",
    "Governs how a CPA performs a SOC 2 examination; tells Echelon what a service auditor will expect (system description, complementary user entity controls, subservice organizations). Relevant once Unbound pursues SOC 2. Not law.",
    AICPA_LIC, "Paid publication; reflects SSAE 20 and 21 updates per product page.", "current",
    V(True, "Fetched AICPA product page 2026-11-25.",
      "https://www.aicpa-cima.com/cpe-learning/publication/soc-2-reporting-on-an-examination-of-controls-at-a-service-organization-relevant-to-security-availability-processing-integrity-confidentiality-or-privacy"),
    jur=["US"], ind=["cross-industry"], rel=["SRC-AICPA-TSC", "SRC-AICPA-SSAE-18"]))
a(R("SRC-AICPA-SSAE-18", "SSAE No. 18, Attestation Standards: Clarification and Recodification (AT-C sections), as amended",
    "AICPA Auditing Standards Board", "standard", "certification-criteria",
    "SSAE 18 as amended (later SSAEs including 19 through 23 amend it; AT-C 205 as issued in SSAE 18 was superseded by SSAE 21 per search results, not directly verified)",
    "2016 (issued; exact date not confirmed)",
    "https://www.aicpa-cima.com/resources/download/aicpa-statement-on-standards-for-attestation-engagements-no-18",
    "Professional standards binding on CPAs performing SOC 1 (AT-C 320) and SOC 2 (AT-C 105 and 205) engagements, not on Echelon. Relevant only to understand auditor obligations and report types.",
    AICPA_LIC, "Seed title cited AT-C 205; the section structure has been amended since 2016.", "current",
    V(True, "Fetched AICPA SSAE 18 download page and 'SSAEs currently effective' page 2026-11-25; effective date and amendment details not confirmed.",
      "https://www.aicpa-cima.com/resources/download/aicpa-ssaes-currently-effective"),
    jur=["US"], ind=["accounting"], rel=["SRC-AICPA-SOC2-GUIDE"]))
a(R("SRC-AICPA-SOC-SUPPLY-CHAIN", "SOC for Supply Chain: Reporting on an Examination of Controls Relevant to Security, Availability, Processing Integrity, Confidentiality, or Privacy in a Production, Manufacturing, or Distribution System (AICPA Guide)",
    "AICPA", "certification-scheme", "certification-criteria", "2024 edition (product AAGSSC24E)", "2024",
    "https://www.aicpa-cima.com/cpe-learning/publication/aicpa-guide-soc-for-supply-chain-reporting-on-an-examination-of-controls-relevant-to-security-availability-processing-integrity-confidentiality-or-privacy-in-a-production-manufacturing-or-distribution-system",
    "Designed for producers, manufacturers and distributors. Not applicable to Unbound, a service organization; SOC 2 is the correct report. Included for completeness.",
    AICPA_LIC, "Not designed for SaaS service organizations.", "current",
    V(True, "Fetched AICPA product page 2026-11-25.",
      "https://www.aicpa-cima.com/cpe-learning/publication/aicpa-guide-soc-for-supply-chain-reporting-on-an-examination-of-controls-relevant-to-security-availability-processing-integrity-confidentiality-or-privacy-in-a-production-manufacturing-or-distribution-system"),
    jur=["US"], ind=["manufacturing"]))

# ---------------- ISO ----------------
def iso(id, title, ver, pub, url, app, lim, status="current", rel=None, notes=None, method=None, lic=ISO_LIC, ok=True):
    return R(id, title, "ISO/IEC JTC 1/SC 27 (ISO and IEC)", "standard",
             "certification-criteria" if "27001" in id else "voluntary-standard", ver, pub, url, app, lic, lim, status,
             V(ok, method or "Fetched IEC Webstore publication page (co-publisher) 2026-11-25; iso.org returned HTTP 403.", url),
             jur=["global"], ind=["cross-industry"], rel=rel, notes=notes)
a(iso("SRC-ISO-27001-2022", "ISO/IEC 27001:2022 Information security, cybersecurity and privacy protection - Information security management systems - Requirements (with Amd 1:2024)",
      "ISO/IEC 27001:2022 edition 3.0 plus Amd 1:2024 (climate action changes)", "2022-10-25",
      "https://webstore.iec.ch/en/publication/79694",
      "Certifiable ISMS standard. Not legally required, but an ISO 27001 certificate or SOC 2 report is the typical evidence financial-institution customers request. Echelon holds no certificate. Applicability: market expectation; optional certification path.",
      "Certification requires an accredited certification body. Price CHF 155 on IEC Webstore; Amd 1 free.",
      rel=["SRC-ISO-27002-2022", "SRC-ISO-27017", "SRC-ISO-27018", "SRC-ISO-27701"],
      notes="Amd 1:2024 published 2024-02-23 per IEC Webstore."))
a(iso("SRC-ISO-27002-2022", "ISO/IEC 27002:2022 Information security, cybersecurity and privacy protection - Information security controls",
      "Edition 3.0", "2022-02-15", "https://webstore.iec.ch/en/publication/74287",
      "Control guidance supporting ISO 27001 Annex A. Voluntary reference; heavily mapped by SIG and CAIQ.",
      "Price CHF 227 on IEC Webstore.", rel=["SRC-ISO-27001-2022"]))
a(iso("SRC-ISO-27017", "ISO/IEC 27017:2026 Information security, cybersecurity and privacy protection - Information security controls based on ISO/IEC 27002 for cloud services",
      "Edition 2.0 (2026); replaces ISO/IEC 27017:2015 (withdrawn 2026-07-27)", "2026-07-27",
      "https://webstore.iec.ch/en/publication/115400",
      "Voluntary cloud control guidance, often included in ISO 27001 certification scope for SaaS providers. Relevant to Unbound as a cloud service provider if pursuing ISO certification. Questionnaires may still cite the 2015 edition.",
      "Price CHF 196 on IEC Webstore.",
      rel=["SRC-ISO-27001-2022", "SRC-ISO-27018"],
      notes="Version correction: seed title had no edition; current edition is 2026, 2015 edition withdrawn 2026-07-27."))
a(iso("SRC-ISO-27018", "ISO/IEC 27018:2025 Information security, cybersecurity and privacy protection - Guidelines for protection of personally identifiable information (PII) in public clouds acting as PII processors",
      "Edition 3.0 (2025); replaces 2019 edition", "2025-08-26", "https://webstore.iec.ch/en/publication/109374",
      "Voluntary code of practice for public cloud PII processors. Unbound would act as a processor for sponsor donor data, so 27018 is a relevant optional extension to an ISO 27001 scope.",
      "Price CHF 179 on IEC Webstore.", rel=["SRC-ISO-27017", "SRC-ISO-27701"],
      notes="Version correction: current edition is 2025."))

# ---------------- OWASP ----------------
OW = "OWASP Foundation"
a(R("SRC-OWASP-ASVS", "OWASP Application Security Verification Standard (ASVS) 5.0.0", OW, "standard", "voluntary-standard",
    "5.0.0", "2025-05-30", "https://asvs.owasp.org/",
    "Voluntary but the most precise public basis for application security requirements and for procurement language. Recommended as the requirement catalog behind Unbound application controls (likely Level 2). Not binding.",
    "CC BY-SA 4.0 (LICENSE.md in the OWASP/ASVS repository). Reuse and adaptation allowed with attribution; derivatives must be shared alike, which matters if Echelon publishes modified requirement text.",
    "Requirement IDs changed from 4.0.3; cite as v5.0.0-<chapter>.<section>.<req> per ASVS guidance.", "current",
    V(True, "Fetched asvs.owasp.org (release, date) and ASVS LICENSE.md 2026-11-25.", "https://asvs.owasp.org/"),
    jur=["global"], ind=["software"], rel=["SRC-OWASP-WSTG", "SRC-OWASP-TOP10"]))
a(R("SRC-OWASP-SAMM-2", "OWASP Software Assurance Maturity Model (SAMM) v2", OW, "framework", "voluntary-standard",
    "2 (minor release number not confirmed)", "unknown", "https://owaspsamm.org/model/",
    "Voluntary maturity model for a software security program; useful to describe Echelon's target state honestly by practice level. Not binding.",
    "CC BY-SA 4.0 (stated on owaspsamm.org).", "Self-assessment model; no certification.", "current",
    V(True, "Fetched owaspsamm.org and model page 2026-11-25; minor version and date not shown.", "https://owaspsamm.org/model/"),
    jur=["global"], ind=["software"], rel=["SRC-BSIMM"]))
a(R("SRC-OWASP-API-TOP10-2023", "OWASP API Security Top 10 2023", OW, "industry-guidance", "voluntary-standard",
    "2023 edition (latest listed)", "2023", "https://owasp.org/www-project-api-security/",
    "Awareness list relevant to Unbound's API-first design (sponsor integrations). Customers ask whether APIs are tested against it. Not binding.",
    "CC BY-SA 4.0 (stated on project page).", "Awareness document, not a verification standard.", "current",
    V(True, "Fetched project page and 2023 edition 2026-11-25.", "https://owasp.org/www-project-api-security/"),
    jur=["global"], ind=["software"], rel=["SRC-OWASP-ASVS"]))
a(R("SRC-OWASP-WSTG", "OWASP Web Security Testing Guide (WSTG)", OW, "industry-guidance", "voluntary-standard",
    "4.2 (latest stable); 5.0 in development", "unknown", "https://owasp.org/www-project-web-security-testing-guide/",
    "Testing methodology commonly cited by penetration testers; relevant to scoping Unbound's external test. Not binding.",
    "CC BY-SA 4.0 (project page).", "v4.2 release date not shown.", "current",
    V(True, "Fetched project page 2026-11-25.", "https://owasp.org/www-project-web-security-testing-guide/"),
    jur=["global"], ind=["software"]))
a(R("SRC-OWASP-TOP10", "OWASP Top 10:2025", OW, "industry-guidance", "voluntary-standard",
    "2025 edition (supersedes 2021)", "2025 (month not confirmed)", "https://owasp.org/Top10/2025/",
    "Awareness baseline that nearly every questionnaire references ('do you test for the OWASP Top 10'). 2025 edition adds A03 Software Supply Chain Failures and A10 Mishandling of Exceptional Conditions. Not binding; PCI DSS and contracts sometimes reference it.",
    "OWASP documentation projects are generally CC BY-SA 4.0; the Top 10 repository LICENSE could not be fetched (path 404), so the specific license was not confirmed.",
    "Questionnaires may still reference the 2021 categories; map both.", "current",
    V(True, "Fetched top10.owasp.org 2025 release page and OWASP Top Ten project page ('most current released version is the OWASP Top 10 2025') 2026-11-25; license not confirmed.",
      "https://owasp.org/www-project-top-ten/"),
    jur=["global"], ind=["software"], rel=["SRC-OWASP-ASVS", "SRC-MITRE-CWE-TOP25"],
    notes="Version confirmation: a 2025 edition exists and is current."))
a(R("SRC-OWASP-CHEATSHEETS", "OWASP Cheat Sheet Series", OW, "industry-guidance", "voluntary-standard",
    "Continuously updated", "unknown", "https://cheatsheetseries.owasp.org/",
    "Implementation guidance useful for Echelon engineering standards. Not binding.",
    "CC BY-SA 4.0 (site footer).", "Not a standard; content varies in depth.", "current",
    V(True, "Fetched site 2026-11-25.", "https://cheatsheetseries.owasp.org/"),
    jur=["global"], ind=["software"]))

# ---------------- MITRE ----------------
MITRE_LIC = "MITRE terms of use (fetched): non-exclusive, royalty-free license to use for research, development and commercial purposes; any copy must reproduce MITRE's copyright designation and the license."
a(R("SRC-MITRE-CWE", "Common Weakness Enumeration (CWE) List Version 5.0", "The MITRE Corporation (CWE Program)", "dataset", "voluntary-standard",
    "5.0 (with Schema 8.0; breaking changes)", "2026-10-28", "https://cwe.mitre.org/data/index.html",
    "Weakness taxonomy used by SAST tools, CVE records and CISA Secure by Design. Echelon should use CWE IDs to classify findings. Not binding.",
    MITRE_LIC, "Version 5.0 introduced breaking schema changes; tools may lag.", "current",
    V(True, "Fetched CWE List Version 5.0 page, CWE news archive 2026 and CWE terms of use 2026-11-25.",
      "https://cwe.mitre.org/news/archives/news2026.html"),
    jur=["global"], ind=["software"], rel=["SRC-MITRE-CWE-TOP25", "SRC-MITRE-CAPEC"],
    notes="Version correction: CWE 5.0 released 2026-10-28 (previous 4.x line ended at 4.21 or later)."))
a(R("SRC-MITRE-CWE-TOP25", "2025 CWE Top 25 Most Dangerous Software Weaknesses", "The MITRE Corporation (CWE Program) with CISA", "dataset", "voluntary-standard",
    "2025 list (latest published as of 2026-11-25)", "2025-12-11", "https://cwe.mitre.org/top25/",
    "Prioritization input for secure coding training and SAST rule selection. Not binding.",
    MITRE_LIC, "Derived from CVE records; reflects reported vulnerabilities, not Echelon's risk.", "current",
    V(True, "Fetched CWE Top 25 page and 2025 news archive entry dated 2025-12-11.", "https://cwe.mitre.org/news/archives/news2025.html"),
    jur=["global"], ind=["software"], rel=["SRC-MITRE-CWE"],
    notes="A 2026 list may be published around December 2026; recheck."))
a(R("SRC-MITRE-CAPEC", "Common Attack Pattern Enumeration and Classification (CAPEC) List Version 3.9", "The MITRE Corporation", "dataset", "voluntary-standard",
    "3.9", "unknown", "https://capec.mitre.org/data/index.html",
    "Attack pattern catalog useful for threat modeling Unbound. Not binding.",
    MITRE_LIC, "Release date of 3.9 not captured.", "current",
    V(True, "Fetched CAPEC list page and terms of use 2026-11-25.", "https://capec.mitre.org/about/termsofuse.html"),
    jur=["global"], ind=["software"], rel=["SRC-MITRE-CWE"]))
a(R("SRC-MITRE-ATTACK", "MITRE ATT&CK", "The MITRE Corporation", "dataset", "voluntary-standard",
    "v20.1", "2026-10-13", "https://attack.mitre.org/resources/versions/",
    "Adversary behavior knowledge base used for detection engineering and some questionnaires. Relevant to Unbound logging and detection design. Not binding.",
    MITRE_LIC + " ATT&CK copies must include the stated attribution notice.", "Enterprise-focused; SaaS-specific coverage limited.", "current",
    V(True, "Fetched ATT&CK versions page and terms of use 2026-11-25.", "https://attack.mitre.org/resources/versions/"),
    jur=["global"], ind=["cross-industry"]))

# ---------------- PCI ----------------
PCI_LIC = ("PCI SSC documents are distributed under a click-through license agreement. Per search-result excerpts of the agreement (not read in full): downloading, internal copying and sharing with employees for study is permitted; no right to sublicense, modify or create derivative works; standards remain PCI SSC property. Some materials are confidential. Do not reproduce requirement text.")
a(R("SRC-PCI-DSS-4.0.1", "Payment Card Industry Data Security Standard (PCI DSS) v4.0.1", "PCI Security Standards Council", "standard", "contractual-template",
    "4.0.1 (limited revision of v4.0; RFC on v4.0.1 held 2026-06-03 to 2026-07-20)", "2024-06-11",
    "https://www.pcisecuritystandards.org/standards/pci-dss/",
    "Contractual (card brand rules through acquirers), not law. Applies only if Unbound stores, processes or transmits cardholder data or can affect its security. If donations are card-funded through a third-party processor with hosted fields, Unbound's scope may be limited (SAQ A style) but this is not established. Sponsors' banks will ask. Applicability: conditional; not established.",
    PCI_LIC, "Card-data specific.", "current",
    V(True, "Fetched PCI DSS standard page, 'Just Published: PCI DSS v4.0.1' blog (2024-06-11) and RFC blog (2026-06-03) 2026-11-25; license terms from search excerpts only.",
      "https://blog.pcisecuritystandards.org/just-published-pci-dss-v4-0-1"),
    jur=["global"], ind=["payments"], rel=["SRC-PCI-SSF"],
    notes="Open question: will Unbound ever touch card data, or only ACH/wire through sponsor banks?"))
a(R("SRC-PCI-SSF", "PCI Software Security Framework (Secure Software Standard and Secure Software Lifecycle (Secure SLC) Standard)", "PCI Security Standards Council", "certification-scheme", "certification-criteria",
    "unknown (current version numbers not shown on fetched pages)", "unknown",
    "https://www.pcisecuritystandards.org/standards/software-security-framework/",
    "Validation programs for payment software vendors; replaced PA-DSS (retired). Not applicable to Unbound unless it sells payment software that handles card data. Secure SLC is a reference for secure development practices only.",
    PCI_LIC, "Program-specific; version numbers not confirmed.", "current",
    V(False, "Fetched PCI SSF at-a-glance, Secure Software and Secure SLC pages 2026-11-25; standard version numbers and dates not shown.",
      "https://www.pcisecuritystandards.org/standards/secure-software/"),
    jur=["global"], ind=["payments"], rel=["SRC-PCI-DSS-4.0.1"]))

# ---------------- Supply chain ----------------
a(R("SRC-SLSA", "SLSA (Supply-chain Levels for Software Artifacts) specification v1.2", "OpenSSF SLSA community (Linux Foundation)", "standard", "voluntary-standard",
    "1.2 (status Approved; adds Source Track)", "2025-11-24", "https://slsa.dev/spec/v1.2/",
    "Voluntary build and source integrity levels. Relevant to Echelon's CI/CD provenance; customers increasingly ask about SLSA level. Not binding.",
    "Community Specification License 1.0 (site footer and repository LICENSE.md).", "Levels are self-declared unless verified by a third party.", "current",
    V(True, "Fetched slsa.dev spec v1.2 and blog ('Announcing SLSA v1.2' 2025-11-24) 2026-11-25.", "https://slsa.dev/blog"),
    jur=["global"], ind=["software"], rel=["SRC-OPENSSF-SCORECARD", "SRC-NIST-SP800-218"],
    notes="Version confirmation: SLSA 1.2 is current (1.1 previous)."))
a(R("SRC-OPENSSF-SCORECARD", "OpenSSF Scorecard", "Open Source Security Foundation (OpenSSF)", "tool", "voluntary-standard",
    "unknown (tool release not captured)", "unknown", "https://scorecard.dev/",
    "Automated checks of open-source repository practices. Useful for Echelon dependency vetting and for scoring its own public repositories. Not binding.",
    "Apache License 2.0 (repository LICENSE).", "Heuristic checks; scores are not assurance.", "current",
    V(True, "Fetched scorecard.dev and repository LICENSE 2026-11-25.", "https://scorecard.dev/"),
    jur=["global"], ind=["software"], rel=["SRC-OPENSSF-S2C2F"]))
a(R("SRC-OPENSSF-S2C2F", "Secure Supply Chain Consumption Framework (S2C2F)", "Open Source Security Foundation (OpenSSF) Supply Chain Integrity WG (originated at Microsoft)", "framework", "voluntary-standard",
    "unknown", "unknown", "https://github.com/ossf/s2c2f",
    "Voluntary framework for securely consuming open-source dependencies, with a maturity model. Directly relevant to Echelon's .NET/F# and JavaScript dependency practices. Not binding.",
    "Specification document states it is licensed under Community Specification License 1.0 and may be copied for internal reference purposes.",
    "Version and date not captured.", "current",
    V(True, "Fetched README.md and specification/framework.md via raw.githubusercontent.com 2026-11-25.",
      "https://raw.githubusercontent.com/ossf/s2c2f/main/README.md"),
    jur=["global"], ind=["software"]))
a(R("SRC-OPENSSF-OSPS-BASELINE", "Open Source Project Security Baseline (OSPS Baseline)", "Open Source Security Foundation (OpenSSF) Security Baseline SIG", "standard", "voluntary-standard",
    "v2026.08.28 (current)", "2026-08-28", "https://baseline.openssf.org/",
    "Maturity-leveled controls for open-source projects. Relevant to evaluating dependencies and any Echelon open-source releases. Not binding.",
    "Apache License 2.0 (repository LICENSE).", "Designed for OSS projects, not SaaS operations.", "current",
    V(True, "Fetched baseline.openssf.org 2026-11-25.", "https://baseline.openssf.org/"),
    jur=["global"], ind=["software"]))
a(R("SRC-CISA-SSDF-ATTESTATION", "Secure Software Development Attestation Form (Common Form)", "Cybersecurity and Infrastructure Security Agency (CISA)", "contract-template", "contractual-template",
    "Form released 2024-03-11 (current version date not shown)", "2024-03-11",
    "https://www.cisa.gov/secure-software-attestation-form",
    "Federal procurement only. OMB M-26-05 (2026-01-23) rescinded the requirement in M-22-18 and M-23-16; agencies may still choose to use the form. Not applicable to Unbound's DAF sponsor market; some private buyers borrow its questions. Applicability: unlikely.",
    US_GOV_LIC, "CISA page is marked archived content that may not reflect current policy.", "unknown",
    V(True, "WebFetch of CISA page 2026-11-25 (curl blocked); rescission confirmed in OMB M-26-05 PDF.",
      "https://www.cisa.gov/secure-software-attestation-form"),
    jur=["US-federal"], ind=["government"], rel=["SRC-OMB-M-26-05", "SRC-OMB-M-22-18", "SRC-NIST-SP800-218"],
    notes="Status changed: no longer mandatory for agencies after M-26-05."))
a(R("SRC-OMB-M-22-18", "OMB M-22-18, Enhancing the Security of the Software Supply Chain through Secure Software Development Practices (and companion M-23-16)",
    "Office of Management and Budget (OMB)", "regulation", "binding-regulation", "M-22-18 (2022-09-14) and M-23-16 (2023)", "2022-09-14",
    "https://www.whitehouse.gov/wp-content/uploads/2022/09/M-22-18.pdf",
    "Rescinded by OMB M-26-05 on 2026-01-23. Historical only; customers may still cite it. Never bound Echelon directly (it bound federal agencies).",
    US_GOV_LIC, "Original URL returned HTTP 404 when fetched 2026-11-25; the publication date is from the seed and memo number, not re-verified.", "withdrawn",
    V(False, "Rescission verified in OMB M-26-05 text; M-22-18 original URL returned 404 so title and date were not re-verified on the issuer site.",
      "https://www.whitehouse.gov/wp-content/uploads/2026/01/M-26-05-Adopting-a-Risk-based-Approach-to-Software-and-Hardware-Security.pdf"),
    jur=["US-federal"], ind=["government"], sup="SRC-OMB-M-26-05", rel=["SRC-CISA-SSDF-ATTESTATION"]))
a(R("SRC-OMB-M-26-05", "OMB M-26-05, Adopting a Risk-based Approach to Software and Hardware Security",
    "Office of Management and Budget (OMB)", "regulation", "binding-regulation", "M-26-05", "2026-01-23",
    "https://www.whitehouse.gov/wp-content/uploads/2026/01/M-26-05-Adopting-a-Risk-based-Approach-to-Software-and-Hardware-Security.pdf",
    "Binds federal agencies only. Rescinds M-22-18 and M-23-16; agencies choose risk-based assurance and may require an SBOM on request (for cloud, an SBOM of the runtime production environment). Not applicable to Echelon unless selling to federal agencies; signals that SBOM-on-request is the federal norm that private buyers may copy.",
    US_GOV_LIC, "Policy memo; agency implementation varies.", "current",
    V(True, "Downloaded and read the memo PDF from whitehouse.gov 2026-11-25.",
      "https://www.whitehouse.gov/wp-content/uploads/2026/01/M-26-05-Adopting-a-Risk-based-Approach-to-Software-and-Hardware-Security.pdf"),
    jur=["US-federal"], ind=["government"], rel=["SRC-OMB-M-22-18", "SRC-CISA-SBOM-MIN", "SRC-NIST-SP800-218"],
    notes="Newly discovered source (not in seed list)."))
a(R("SRC-NTIA-SBOM-MIN", "The Minimum Elements For a Software Bill of Materials (SBOM)", "National Telecommunications and Information Administration (NTIA), US Department of Commerce", "industry-guidance", "voluntary-standard",
    "2021 report", "2021-07-12", "https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom",
    "Superseded: CISA states its 2026 minimum elements update and replace the NTIA 2021 elements. Historical reference only.",
    US_GOV_LIC, "Replaced by CISA 2026 guidance.", "superseded",
    V(True, "Fetched NTIA report page 2026-11-25; supersession per CISA 2026 page (WebFetch).",
      "https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom"),
    jur=["US"], ind=["software"], sup="SRC-CISA-SBOM-MIN"))
a(R("SRC-CISA-SBOM-MIN", "2026 Minimum Elements for a Software Bill of Materials (SBOM)", "CISA with NSA, FBI and international partners", "industry-guidance", "voluntary-standard",
    "2026 (released guidance; 2025 version was a draft for comment published 2025-08-22, comments closed 2025-10-03)", "2026-07-29",
    "https://www.cisa.gov/resources-tools/resources/2026-minimum-elements-software-bill-materials-sbom",
    "Voluntary guidance, not regulation; becomes contractual if a customer requires SBOMs conforming to it. Adds elements such as component hash, component license, tool name and generation context (per CISA release, via search). Relevant to Echelon's SBOM generation. Applicability: voluntary, likely asked by sophisticated buyers.",
    US_GOV_LIC + " May contain partner-agency content; check the PDF notice.",
    "The release page does not label the document final or draft, nor state whether it is binding. PDF not downloadable by curl (HTTP 403).", "current",
    V(True, "WebFetch of CISA 2026 page and 2025 draft page 2026-11-25 (curl blocked); new elements list from search summary of CISA news release, not directly read.",
      "https://www.cisa.gov/resources-tools/resources/2026-minimum-elements-software-bill-materials-sbom"),
    jur=["US"], ind=["software"], rel=["SRC-NTIA-SBOM-MIN", "SRC-SPDX", "SRC-CYCLONEDX", "SRC-OMB-M-26-05"],
    notes="Status correction: the 2025 draft was superseded by the 2026 release dated 2026-07-29."))
a(R("SRC-CISA-SECURE-BY-DESIGN", "CISA Secure by Design principles and Secure by Design Pledge", "Cybersecurity and Infrastructure Security Agency (CISA)", "industry-guidance", "voluntary-standard",
    "Pledge with seven goals (version not stated)", "unknown", "https://www.cisa.gov/securebydesign/pledge",
    "Voluntary; the pledge page states it is voluntary and not legally binding and targets enterprise software including SaaS. Echelon could sign; signing is a public commitment to MFA, default password reduction, vulnerability class reduction, patching, a VDP, CVE/CWE transparency and evidence of intrusions. Applicability: optional.",
    US_GOV_LIC, "Launch date not stated on the page; page says hundreds of companies signed.", "current",
    V(True, "WebFetch of CISA pledge page 2026-11-25 (curl blocked).", "https://www.cisa.gov/securebydesign/pledge"),
    jur=["US"], ind=["software"], rel=["SRC-ISO-29147-30111"]))
a(R("SRC-FEDRAMP", "FedRAMP (Rev. 5 baselines and FedRAMP 20x certification)", "General Services Administration (GSA) FedRAMP PMO", "certification-scheme", "certification-criteria",
    "Rev. 5 process plus FedRAMP 20x (Class A, B and C certification rules finalized per fedramp.gov); 'Consolidated Rules for 2026'", "unknown",
    "https://www.fedramp.gov/20x/",
    "Required only for cloud services used by federal agencies. Not applicable to Unbound's DAF sponsor market. Note FedRAMP now uses 'certification' terminology and 20x classes.",
    US_GOV_LIC + " FedRAMP name and logo are GSA property.", "Rapidly changing program; recheck before any federal pursuit.", "current",
    V(True, "Fetched fedramp.gov and 20x page 2026-11-25.", "https://www.fedramp.gov/"),
    jur=["US-federal"], ind=["government", "cloud"], rel=["SRC-NIST-SP800-53B", "SRC-STATERAMP"]))
a(R("SRC-BSIMM", "Building Security In Maturity Model (BSIMM16)", "Black Duck Software, Inc.", "framework", "market-practice",
    "BSIMM16", "2026-01", "https://www.blackduck.com/resources/analyst-reports/bsimm.html",
    "Descriptive benchmark of software security initiatives at large firms. Low direct relevance to a small company; useful context only. Not binding.",
    "Proprietary report (registration download); copyright Black Duck. Cite activity IDs only.",
    "Descriptive of participating (mostly large) firms; not prescriptive.", "current",
    V(True, "Fetched issuer page 2026-11-25 ('BSIMM16 report, published in January 2026').", "https://www.blackduck.com/resources/analyst-reports/bsimm.html"),
    jur=["global"], ind=["software"], rel=["SRC-OWASP-SAMM-2"],
    notes="Version confirmation: BSIMM16 is current."))
a(R("SRC-SPDX", "SPDX Specification 3.0 (3.0.1); ISO/IEC 5962:2021 standardizes SPDX 2.2.1", "Linux Foundation SPDX project; ISO/IEC JTC 1 for ISO/IEC 5962", "standard", "voluntary-standard",
    "3.0.1 current per spdx.dev (ISO/IEC 5962:2021 = SPDX 2.2.1, published 2021-08-24)", "unknown",
    "https://spdx.dev/use/specifications/",
    "SBOM format option alongside CycloneDX. Customer SBOM requests usually accept either. Not binding.",
    "SPDX 3.0.1 copyright page: Community Specification License 1.0; pre-existing portions under CC BY 3.0. ISO/IEC 5962:2021 listed at CHF 0 on IEC Webstore.",
    "3.0 publication date not captured.", "current",
    V(True, "Fetched spdx.dev specifications page, SPDX 3.0.1 copyright page and IEC Webstore record for ISO/IEC 5962:2021 2026-11-25.",
      "https://spdx.github.io/spdx-spec/v3.0.1/front/copyright/"),
    jur=["global"], ind=["software"], rel=["SRC-CYCLONEDX", "SRC-CISA-SBOM-MIN"]))
a(R("SRC-CYCLONEDX", "CycloneDX Bill of Materials Specification v1.7 (ECMA-424 2nd edition)", "OWASP Foundation and Ecma International TC54", "standard", "voluntary-standard",
    "1.7 (ECMA-424 2nd edition, December 2025; 1st edition June 2024)", "2025-10-21",
    "https://cyclonedx.org/specification/overview/",
    "SBOM and VEX-capable format; natural fit for .NET and JavaScript tooling. Not binding.",
    "Specification repository LICENSE: Apache License 2.0. Ecma standards are freely downloadable from Ecma.",
    "ECMA-424 also progressing as ISO/IEC DIS 27055 (per Ecma page).", "current",
    V(True, "Fetched cyclonedx.org overview (current 1.7, release 2025-10-21), Ecma ECMA-424 page and repository LICENSE 2026-11-25.",
      "https://ecma-international.org/publications-and-standards/standards/ecma-424/"),
    jur=["global"], ind=["software"], rel=["SRC-SPDX", "SRC-OPENVEX"],
    notes="Version correction: seed referenced ECMA-424 generically; current is 2nd edition (CycloneDX 1.7)."))
a(R("SRC-OPENVEX", "OpenVEX Specification v0.2.0 (and OASIS CSAF VEX profile)", "OpenVEX project (OpenSSF); OASIS CSAF TC for CSAF", "standard", "voluntary-standard",
    "OpenVEX 0.2.0; CSAF version not verified", "unknown", "https://github.com/openvex/spec",
    "Vulnerability exploitability exchange formats that let Echelon state whether a dependency CVE affects Unbound. Optional. Not binding.",
    "OpenVEX spec repository LICENSE: CC0 1.0 Universal. CSAF license not verified (OASIS page returned 404).",
    "CSAF details not verified.", "current",
    V(True, "Fetched OPENVEX-SPEC.md and LICENSE via raw.githubusercontent.com 2026-11-25; CSAF not verified.",
      "https://raw.githubusercontent.com/openvex/spec/main/OPENVEX-SPEC.md"),
    jur=["global"], ind=["software"], rel=["SRC-CYCLONEDX"]))
a(iso("SRC-ISO-29147-30111", "ISO/IEC 29147:2018 Vulnerability disclosure and ISO/IEC 30111:2019 Vulnerability handling processes",
      "29147:2018 edition 2.0; 30111:2019 edition 2.0", "2018-10-23 (29147); 2019-10-01 (30111)",
      "https://webstore.iec.ch/en/publication/64099",
      "Voluntary references for a vulnerability disclosure policy and internal handling. CISA Secure by Design pledge and customers expect a VDP. Recommended reference for Echelon's VDP. Not binding.",
      "29147 CHF 179; 30111 CHF 135 on IEC Webstore.", rel=["SRC-CISA-SECURE-BY-DESIGN"]))
a(R("SRC-CVSS-4.0", "Common Vulnerability Scoring System v4.0 Specification Document", "Forum of Incident Response and Security Teams (FIRST)", "standard", "voluntary-standard",
    "CVSS 4.0, specification document version 1.2", "unknown", "https://www.first.org/cvss/v4.0/specification-document",
    "Severity scoring used in remediation SLAs that customers request. Echelon should define SLAs by severity and exploitation (with EPSS and KEV), not CVSS alone. Not binding.",
    "FIRST conditions of use (in the specification): use is permitted with attribution that CVSS is owned by FIRST and used by permission; publishers of CVSS data must follow the guide and provide score and vector string.",
    "Publication date of 4.0 not captured.", "current",
    V(True, "Fetched CVSS v4.0 specification document 2026-11-25.", "https://www.first.org/cvss/v4.0/specification-document"),
    jur=["global"], ind=["cross-industry"], rel=["SRC-FIRST-EPSS", "SRC-CISA-KEV"]))
a(R("SRC-FIRST-EPSS", "Exploit Prediction Scoring System (EPSS)", "Forum of Incident Response and Security Teams (FIRST) EPSS SIG", "dataset", "voluntary-standard",
    "unknown (model version not captured)", "unknown", "https://www.first.org/epss/",
    "Daily exploitation-probability scores to prioritize dependency patching. Optional input to Echelon's vulnerability management. Not binding.",
    "FIRST page states the data is freely and openly accessible via CSV, API and GitHub; specific license terms not captured.",
    "Model version and changelog not captured.", "current",
    V(True, "Fetched FIRST EPSS page 2026-11-25.", "https://www.first.org/epss/"),
    jur=["global"], ind=["cross-industry"], rel=["SRC-CVSS-4.0", "SRC-CISA-KEV"]))
a(R("SRC-CISA-KEV", "CISA Known Exploited Vulnerabilities (KEV) Catalog", "Cybersecurity and Infrastructure Security Agency (CISA)", "dataset", "voluntary-standard",
    "Continuously updated; now governed by BOD 26-04", "unknown", "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
    "Binding remediation applies only to federal civilian agencies (BOD 26-04). CISA recommends all organizations prioritize KEV; customers commonly expect KEV-listed issues fixed quickly. Echelon should adopt KEV as a priority trigger voluntarily.",
    US_GOV_LIC, "Catalog snippets showed new BOD 26-04 fields (for example forensic triage); not read directly.", "current",
    V(True, "WebFetch of CISA KEV reference page 2026-11-25 (curl blocked).",
      "https://www.cisa.gov/known-exploited-vulnerabilities-catalog/reducing-significant-risk-known-exploited-vulnerabilities"),
    jur=["US"], ind=["cross-industry"], rel=["SRC-CISA-BOD-26-04", "SRC-CISA-BOD-22-01"]))
a(R("SRC-CISA-BOD-22-01", "BOD 22-01: Reducing the Significant Risk of Known Exploited Vulnerabilities", "Cybersecurity and Infrastructure Security Agency (CISA)", "regulation", "binding-regulation",
    "Issued 2021-11-03; revoked", "2021-11-03", "https://www.cisa.gov/news-events/directives/bod-22-01-reducing-significant-risk-known-exploited-vulnerabilities",
    "Bound federal civilian executive branch agencies only. Revoked and superseded by BOD 26-04 (2026-06-10). Never bound Echelon; customer questionnaires may still cite its two-week and six-month timelines.",
    US_GOV_LIC, "Historical.", "withdrawn",
    V(True, "WebFetch of CISA directive page 2026-11-25: page states the directive has been revoked and superseded by BOD 26-04.",
      "https://www.cisa.gov/news-events/directives/bod-22-01-reducing-significant-risk-known-exploited-vulnerabilities"),
    jur=["US-federal"], ind=["government"], sup="SRC-CISA-BOD-26-04"))
a(R("SRC-CISA-BOD-26-04", "BOD 26-04: Prioritizing Security Updates Based on Risk", "Cybersecurity and Infrastructure Security Agency (CISA)", "regulation", "binding-regulation",
    "Issued 2026-06-10", "2026-06-10", "https://www.cisa.gov/known-exploited-vulnerabilities-catalog/reducing-significant-risk-known-exploited-vulnerabilities",
    "Binds federal civilian executive branch agencies only; CISA states it does not bind private industry. Carries forward KEV criteria and harmonizes KEV with other patch timelines. Not applicable to Echelon; informative for remediation SLA design.",
    US_GOV_LIC, "Directive text and specific timelines not read (CISA site blocks automated clients; WebFetch summary only).", "current",
    V(False, "Title, issue date and scope from WebFetch of CISA KEV reference page; directive text itself not read.",
      "https://www.cisa.gov/known-exploited-vulnerabilities-catalog/reducing-significant-risk-known-exploited-vulnerabilities"),
    jur=["US-federal"], ind=["government"], rel=["SRC-CISA-KEV", "SRC-CISA-BOD-22-01"],
    notes="Newly discovered source (not in seed list). Open question: exact remediation timelines."))
a(R("SRC-CMMC-2.0", "Cybersecurity Maturity Model Certification (CMMC) Program (32 CFR part 170) and DFARS implementing rule", "US Department of Defense", "regulation", "binding-regulation",
    "32 CFR part 170 final rule (89 FR 83092); DFARS Case 2019-D041 final rule (90 FR 43560)", "2024-10-15",
    "https://www.federalregister.gov/documents/2024/10/15/2024-22905/cybersecurity-maturity-model-certification-cmmc-program",
    "Binding only on defense contractors handling FCI or CUI under contracts with CMMC clauses. Not applicable to Echelon or Unbound absent DoD work.",
    US_GOV_LIC, "Search results indicate DoD paused the transition to Phase 2 (originally 2026-11-10); dodcio.defense.gov blocked automated access so this was not confirmed.", "current",
    V(True, "Federal Register API: part 170 rule published 2024-10-15, effective 2024-12-16; DFARS rule published 2025-09-10, effective 2025-11-10. Phase status not verified.",
      "https://www.federalregister.gov/api/v1/documents/2025-17359.json"),
    jur=["US-federal"], ind=["defense"], eff="2024-12-16", rel=["SRC-NIST-SP800-171-R3"],
    notes="Seed title used 'CMMC 2.0'; the codified program is titled 'CMMC Program'."))
a(R("SRC-NIST-SP800-218-R1-IPD", "SP 800-218 Rev. 1 (Initial Public Draft), Secure Software Development Framework (SSDF) Version 1.2",
    "National Institute of Standards and Technology (NIST)", "standard", "voluntary-standard",
    "Rev. 1 initial public draft (SSDF 1.2); comments closed 2026-01-30", "2025-12-17",
    "https://csrc.nist.gov/pubs/sp/800/218/r1/ipd",
    "Draft; not final as of 2026-11-25 per CSRC. Echelon should design to SSDF 1.1 while tracking 1.2 changes.",
    NL, "Draft content may change.", "draft",
    V(True, "Fetched CSRC draft page 2026-11-25.", "https://csrc.nist.gov/pubs/sp/800/218/r1/ipd"),
    jur=["US"], ind=["software"], rel=["SRC-NIST-SP800-218"],
    notes="Newly discovered source (not in seed list)."))

if __name__ == "__main__":
    import sys
    write(sys.argv[1], recs)
    print(len(recs))
