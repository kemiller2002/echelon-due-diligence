from rqb_common import *
c = Cat("A11Y", {"industries": ["all"], "jurisdictions": ["US-federal"], "products": ["unbound"]})
OWN = "Proposed: Accessibility Lead (role not yet staffed)"
RAT = "No Unbound user interface, conformance evaluation, ACR or accessibility test result exists as of 2026-11-25. Forma, the intended design system, has accessibility contracts and a pilot conformance test suite in its own repository (forma@c8f40b4c)."
PUB = ["public-sector", "higher-education"]
FORMA = "forma@c8f40b4c"

e1 = c.E(1, "Conformance claim and scope statement", "Versioned statement of the standard and level claimed (WCAG 2.2 AA), the surfaces, roles, platforms and third-party components in scope, known exceptions, and the evaluation it rests on.",
         mechanism="periodic-manual", freshness="P180D", disc="public")
e2 = c.E(2, "Accessibility Conformance Report (VPAT-based)", "ACR in the current ITI VPAT INT edition (covering WCAG, Section 508 and EN 301 549) per product release, stating evaluation methods, product version, preparer and independence.",
         mechanism="periodic-manual", freshness="P1Y", independence="first-party", disc="public",
         notes="CNV-EXP-001 AC-3 requires an ACR from automated plus manual assistive-technology testing before a surface is activated.")
e3 = c.E(3, "Automated accessibility test results in CI", "Per-build results of automated WCAG A/AA rule checks (for example axe), layout reflow at 320 CSS px, 200 percent text and text-spacing sweeps, forced-colors and reduced-motion checks, with pass, fail and unknown counted separately.",
         producer=f"Forma ui-conformance CI job ({FORMA}, Chromium only, pilot) for design-system components; Unbound pipeline not yet assigned",
         mechanism="event-driven-automated", freshness="per-event", disc="customer-only", status="partially-implemented",
         prov=["commit", "browser", "viewport", "rule_set_version", "pass", "fail", "unknown"])
e4 = c.E(4, "Manual and assistive-technology test records", "Per essential journey: keyboard-only walkthrough, screen-reader testing on named AT and browser pairs (for example NVDA with Firefox, JAWS with Chrome, VoiceOver on iOS and macOS, TalkBack on Android), moderated sessions with disabled participants, defects and retests.",
         mechanism="periodic-manual", freshness="P180D", disc="nda", prov=["journey", "at_browser_pair", "tester", "date", "defects", "retest_result"])
e5 = c.E(5, "Accessibility defect register and remediation metrics", "All reported and found accessibility defects with WCAG criterion, severity, affected journeys, workaround offered, target and actual fix dates, and aging.",
         mechanism="continuous-automated", freshness="P30D", disc="customer-only")
e6 = c.E(6, "Accessible document validation results", "For each issued document type: PDF/UA-1 validation output (for example veraPDF), Matterhorn manual checkpoint review, and confirmation that an accessible HTML rendition with the same snapshot identifier exists.",
         mechanism="event-driven-automated", freshness="per-event", disc="customer-only", prov=["document_type", "snapshot_id", "validator_version", "result"])
e7 = c.E(7, "Brand compilation contrast gate output", "Compiler result for each sponsor brand naming any failing color pair and confirming all shipped themes meet contrast thresholds.",
         producer=f"Forma brand compiler ({FORMA}) for Forma themes; Unbound sponsor brand compilation not yet built",
         mechanism="event-driven-automated", freshness="per-event", disc="customer-only", status="partially-implemented")
e8 = c.E(8, "Accessibility legal applicability assessment", "Counsel-reviewed assessment of which accessibility laws apply to Echelon and to each customer segment (ADA Titles II and III, Section 508, state laws, European Accessibility Act) and the resulting contractual commitments.",
         mechanism="periodic-manual", freshness="P1Y", disc="nda")
e9 = c.E(9, "Accessible support and authentication path record", "Inventory of support channels and identity-verification methods with their accessibility features (relay calls, captioned video, non-cognitive authentication alternatives, adjustable timeouts) and test results.",
         mechanism="periodic-manual", freshness="P1Y", disc="customer-only")

k1 = c.C(1, "Activation gate on accessibility conformance", "Block activation of a user-facing surface until its ACR shows no open WCAG 2.2 Level A or AA failure without a signed exception, and every Forma component used has a conformance statement or Unbound test.",
         "preventive-gate", "L5-build-release-gate", ["Unbound release gate (not built)"], [e1, e2], OWN, related=["CNV-EXP-001", "UNB-PLAT-005"],
         fw=[R("SRC-WCAG-2.2"), R("SRC-ITI-VPAT")])
k2 = c.C(2, "Automated accessibility checks as blocking CI", "Run automated WCAG rule checks, reflow, text-scale, forced-colors and reduced-motion tests on every build and block on regressions.",
         "preventive-gate", "L6-automated-analysis", [f"Forma ui-conformance CI job ({FORMA})", "Unbound pipeline (not built)"], [e3], OWN, status="partially-implemented",
         related=["UNB-UX-005", "UNB-UX-006"], fw=[R("SRC-WCAG-2.2", "1.4.10"), R("SRC-WCAG-2.2", "1.4.12")],
         notes="Forma runs a blocking ui-conformance job in Chromium only; Firefox and WebKit evidence is listed as remaining work (forma@c8f40b4c:docs/UNIVERSAL-UI-CONFORMANCE.md). Automated checks find only a subset of WCAG failures.",
         residual=["Automated tools detect a minority of WCAG failures; manual and AT testing remain necessary."])
k3 = c.C(3, "Manual and assistive-technology testing of essential journeys", "Test every essential journey with keyboard only, named screen reader and browser pairs, and moderated sessions with disabled participants before release and after material change.",
         "detective-manual", "L10-external-or-manual", ["not yet assigned"], [e4], OWN, related=["UNB-UX-006", "CNV-EXP-001"])
k4 = c.C(4, "Accessibility defect SLAs", "Track accessibility defects with severity-based remediation targets and provide an equivalent alternative while a defect is open.",
         "corrective", "L9-runtime-monitored", ["not yet assigned"], [e5], OWN)
k5 = c.C(5, "Accessible rendition at issuance", "Issue every document with an accessible HTML rendition generated from the same snapshot and validate any PDF against PDF/UA-1 before release.",
         "preventive-gate", "L5-build-release-gate", ["Unbound document pipeline (not built)", "Folio print components (folio@56a18e1; tagged PDF not provided)"], [e6], "Proposed: Unbound product owner",
         related=["UNB-RCN-PLT-010", "CNV-EXP-001", "UNB-DOC-003", "UNB-PLAT-003"])
k6 = c.C(6, "Design-system accessibility contracts", "Provide components whose semantics, focus visibility, contrast-gated color roles, forced-colors projection, reflow and target sizes are contractually specified and tested, so applications inherit them.",
         "preventive-structural", "L3-restricted-interface", [f"Forma ({FORMA})"], [e3, e7], "Proposed: Forma maintainer", status="partially-implemented",
         related=["UNB-PLAT-009", "CNV-EXP-001"], fw=[R("SRC-WCAG-2.2", "1.4.3"), R("SRC-WCAG-2.2", "1.4.11"), R("SRC-WCAG-2.2", "2.4.7")],
         notes="Forma color contract gates status foregrounds at 4.5:1 and projects to system colors in forced-colors mode (forma@c8f40b4c:docs/COLOR.md). Pilot status; not a passed release gate.")
k7 = c.C(7, "Sponsor brand contrast compilation gate", "Fail compilation of any sponsor brand whose color pairs fall below contrast thresholds, naming the failing pair.",
         "preventive-gate", "L5-build-release-gate", [f"Forma brand compiler ({FORMA})", "Unbound brand kit (not built)"], [e7], "Proposed: Unbound product owner", status="partially-implemented",
         related=["CNV-EXP-001"], fw=[R("SRC-WCAG-2.2", "1.4.3")],
         notes="Forma requirement BRAND-A11Y-001 states a compiled brand shall preserve the WCAG 2.2 AA target; CNV-EXP-001 AC-1 specifies the Unbound behavior.")
k8 = c.C(8, "Accessibility legal applicability review", "Have counsel determine applicable accessibility law by customer segment and reflect it in contracts and roadmap.", "administrative", "L10-external-or-manual", ["not yet assigned"], [e8], "Proposed: General Counsel (role not yet staffed)",
         related=["UNB-GAP-031", "UNB-PLAT-005"])
k9 = c.C(9, "Accessible assurance and support paths", "Provide identity-verification, authentication and support paths usable without sight, hearing, fine motor control or memorization, reaching the same assurance level as other paths.",
         "preventive-structural", "L10-external-or-manual", ["Unbound identity and contact assurance (not built)"], [e9], OWN, related=["CNV-PLT-011", "ADM-045"],
         fw=[R("SRC-WCAG-2.2", "3.3.8"), R("SRC-SECTION-508", "603")])

a1 = c.A(1, "WCAG conformance target, scope and status", "proposed-target-state", RAT,
    "Unbound conforms to WCAG 2.2 Level AA (which also satisfies WCAG 2.1 AA and 2.0 AA) on every surface and role: donor, advisor, successor, sponsor staff, administrator, charity and embedded partner widgets, on supported mobile and desktop platforms. Complex accounting workbenches may be desktop-optimized but remain conformant with reflow. Third-party embedded components are in scope and either conform or are documented exceptions with alternatives. Session timeouts warn users and allow extension except where a financial-security limit applies, and that limit is disclosed. The claim names the evaluation it rests on and is updated on material change.",
    "Not established. UNB-PLAT-005 and CNV-EXP-001 set WCAG 2.2 AA as the requirement; no product exists to evaluate.",
    "Evaluate each surface before activation under the activation gate.",
    "Nothing for Unbound. Forma has pilot conformance tests for its own components.",
    "Unbound has no user interface yet, so we make no conformance claim. Our requirement is WCAG 2.2 Level AA for every surface, verified before activation.",
    "planned", [k1], [e1], OWN, freshness="P180D", mechanism="periodic-manual", automation="partial", impl="medium", rec="medium", disc="public",
    requirements=["UNB-PLAT-005", "CNV-EXP-001", "UNB-EXP-001", "UNB-UX-002", "UNB-GAP-031"])
a2 = c.A(2, "VPAT and Accessibility Conformance Report", "proposed-target-state", RAT,
    "A current ACR in the ITI VPAT INT edition covers WCAG 2.2, the Revised Section 508 Standards and EN 301 549, is tied to a product version, states the evaluation methods and AT used, and is updated for each major release. The ACR is derived from continuously generated test evidence rather than a one-time audit, and an independent third-party evaluation validates it at least annually for customers who require it. Customers are notified when conformance changes.",
    "Not established.",
    "Produce the first ACR when the first surface is ready for activation.",
    "Nothing.",
    "We do not yet have a VPAT or Accessibility Conformance Report because no product user interface exists. We plan to publish one before release.",
    "not-available", [k1], [e2], OWN, freshness="P1Y", mechanism="periodic-manual", automation="partial", impl="medium", rec="medium", disc="public",
    requirements=["CNV-EXP-001"],
    challenge={
        "customer_intent": "Obtain credible, comparable evidence of accessibility for procurement decisions and legal defensibility.",
        "adverse_outcome": "Purchase of an inaccessible product, excluding disabled donors or staff and creating legal exposure.",
        "conventional_control_effectiveness": "VPATs are self-prepared, often marketing documents with 'Supports' claims not backed by testing; they are snapshots that drift from the product.",
        "legally_required": "Not by itself. Federal agencies must consider Section 508 conformance in procurement and commonly request ACRs; no law requires the VPAT format.",
        "contractually_required": "Frequently in public-sector and higher-education procurement.",
        "historical_convention": "ITI VPAT format since 2001.",
        "architectural_elimination": "No.",
        "automatic_enforcement": "Partly: automated checks in CI keep part of the evidence current.",
        "continuous_evidence": "Per-build automated results plus periodic AT test records can regenerate the ACR on each release.",
        "stronger_alternative": "ACR generated from continuous evidence, with independent validation, instead of a static self-assessment.",
        "alternative_verifiable": "Yes, if evidence is shared.",
        "customer_acceptance_likelihood": "Likely; buyers still want the VPAT format, which the alternative produces.",
        "invalidating_conditions": "If automated evidence is presented as full conformance without manual and AT testing.",
        "conventional_cost": "medium", "alternative_cost": "medium",
        "alternative_risks": "Over-reliance on automated results.",
        "supporting_arguments": ["Keeps claims current with releases."],
        "opposing_arguments": ["Independent audits catch issues internal teams normalize.", "Buyers may discount vendor-generated evidence."],
        "technical_effectiveness": "stronger", "institutional_acceptance": "likely"})
a3 = c.A(3, "Accessibility testing methodology", "proposed-target-state", RAT,
    "Testing combines automated rule checks on every build (blocking regressions), layout checks at 320, 390, 768 and 1280 CSS px with 200 percent text and text spacing, forced-colors and reduced-motion checks, keyboard-only walkthroughs, screen-reader testing on named AT and browser pairs across desktop and mobile, and moderated usability sessions with disabled participants for essential journeys. AI agents that generate UI code are subject to the same gates; generated changes cannot merge without passing them and human review. Designers, engineers and support staff receive role-specific accessibility training.",
    "Not established for Unbound. Forma runs a blocking ui-conformance CI job (Chromium only) with layout, text-scale and action-outcome tests and axe checks in pilot fixtures; it reports pass, fail and unknown separately and does not claim catalog-wide conformance.",
    "Adopt Forma's conformance helpers in the Unbound pipeline and add manual and AT testing.",
    "Forma's CI produces automated results for Forma components in Chromium; nothing for Unbound.",
    "No Unbound accessibility testing has occurred because no interface exists. Our requirements call for automated, manual, screen-reader and disabled-user testing for every essential journey.",
    "planned", [k2, k3], [e3, e4], OWN, freshness="per-event", mechanism="event-driven-automated", automation="partial", impl="medium", rec="medium",
    requirements=["UNB-UX-005", "UNB-UX-006", "CNV-EXP-001", "TVR-UX-006"],
    challenge={
        "customer_intent": "Ensure accessibility is tested credibly, not just claimed.",
        "adverse_outcome": "Inaccessible journeys ship and are found by users or plaintiffs.",
        "conventional_control_effectiveness": "Periodic third-party audits find many issues but are snapshots; regressions reappear between audits, and automated scanners alone miss most failures.",
        "legally_required": "No method is legally required; the DOJ Title II rule sets WCAG 2.1 AA as the outcome for public entities.",
        "contractually_required": "Public-sector buyers sometimes require third-party audits.",
        "historical_convention": "Annual third-party audit plus VPAT.",
        "architectural_elimination": "Partly: design-system components with contractual semantics, focus and contrast eliminate whole classes of failure for applications that use them correctly.",
        "automatic_enforcement": "Blocking CI checks prevent automatically detectable regressions.",
        "continuous_evidence": "Per-build results.",
        "stronger_alternative": "Component contracts plus blocking automation plus targeted AT testing, with periodic independent audit as validation rather than the primary control.",
        "alternative_verifiable": "Yes.",
        "customer_acceptance_likelihood": "Likely if an independent audit is also offered.",
        "invalidating_conditions": "If application code bypasses design-system components or AT testing is skipped under schedule pressure.",
        "conventional_cost": "medium", "alternative_cost": "medium",
        "alternative_risks": "Chromium-only automation misses browser-specific failures; Forma lists Firefox and WebKit evidence as remaining work.",
        "supporting_arguments": ["Prevents regression between audits."],
        "opposing_arguments": ["Real users with disabilities find issues automation and internal testers miss."],
        "technical_effectiveness": "stronger", "institutional_acceptance": "likely"})
a4 = c.A(4, "Accessibility remediation commitments", "proposed-target-state", RAT,
    "Anyone can report an accessibility barrier through an accessible channel; Echelon acknowledges within two business days, provides an equivalent alternative or workaround promptly, and remediates by severity (blocking barriers on essential journeys within a short defined period, others in scheduled releases). Known non-conformances and their target dates are published in the ACR, and remediation targets can be made contractual.",
    "Not established.",
    "Define the intake channel and remediation targets with the first ACR.",
    "Nothing.",
    "We have not yet defined accessibility remediation commitments. We plan to publish them with our first conformance report.",
    "planned", [k4], [e5], OWN, freshness="P30D", mechanism="continuous-automated", automation="high", impl="low", rec="low")
a5 = c.A(5, "Accessible documents, exports and communications", "proposed-target-state", RAT,
    "Every issued document (statements, contribution acknowledgments, grant letters, reports) is available at issuance as accessible HTML generated from the same data snapshot with the same integrity reference, and any PDF is tagged and validated against PDF/UA-1 before release. Charts carry text or table alternatives; data exports are structured with headers; email templates pass accessibility checks with plain-text alternatives. Documents uploaded by sponsors or charities are outside Echelon's control; Echelon flags inaccessible uploads and the allocation of responsibility is stated in the contract.",
    "Not established. UNB-RCN-PLT-010 and CNV-EXP-001 AC-4 require accessible renditions and PDF/UA-1 validation. Folio provides print markup and preserves reading order by requirement, but tagged PDF and PDF/UA are explicitly not assumed (folio@56a18e1:docs/requirements/unbound-financial-report-consumer-capability-review-2026-11-23.md); CNV-EXP-001 states the PDF pipeline is Unbound-owned until an upstream renderer exists.",
    "Run the rendering spike (RCD-009 DG-04) to confirm accessible HTML and a PDF/UA-capable pipeline before statements launch.",
    "Nothing.",
    "We do not yet produce documents. Our requirements call for an accessible HTML version of every document and validated tagged PDFs; the PDF accessibility pipeline has not been selected or tested.",
    "planned", [k5], [e6], "Proposed: Unbound product owner", freshness="per-event", mechanism="event-driven-automated", automation="high", impl="high", rec="low",
    requirements=["UNB-RCN-PLT-010", "CNV-EXP-001", "UNB-DOC-003", "UNB-PLAT-003", "ADM-029", "ADM-045"],
    challenge={
        "customer_intent": "Ensure disabled donors and staff can read statements, receipts and reports.",
        "adverse_outcome": "Blind donor cannot read a tax acknowledgment; discrimination complaint.",
        "conventional_control_effectiveness": "Buyers ask for 'accessible PDFs'; tagged PDF generation from browsers is inconsistent and PDF/UA conformance is hard to achieve and verify, so claims are often unreliable.",
        "legally_required": "For public-entity customers, the DOJ Title II rule covers conventional electronic documents with limited exceptions; for others, depends on ADA Title III interpretation.",
        "contractually_required": "Common in public-sector contracts.",
        "historical_convention": "PDF as the document of record.",
        "architectural_elimination": "Partly: generating accessible HTML from the same snapshot as the PDF means the accessible version is never an afterthought and is provably the same content.",
        "automatic_enforcement": "Issuance gate requires both renditions and PDF validation.",
        "continuous_evidence": "Per-document-type validation results.",
        "stronger_alternative": "Accessible HTML as a co-equal rendition of record, with PDF/UA where achievable.",
        "alternative_verifiable": "Yes, by snapshot identifier and validator output.",
        "customer_acceptance_likelihood": "Uncertain: some recipients require PDF specifically.",
        "invalidating_conditions": "If the PDF is the only legally recognized record for a use and cannot be made PDF/UA conformant.",
        "conventional_cost": "high", "alternative_cost": "medium",
        "alternative_risks": "Automated PDF/UA validators cannot check all Matterhorn conditions; manual review is still needed.",
        "supporting_arguments": ["HTML is more reliably accessible than PDF across AT."],
        "opposing_arguments": ["Recipients and auditors expect PDF.", "Two renditions double the testing surface."],
        "technical_effectiveness": "stronger", "institutional_acceptance": "uncertain"})
a6 = c.A(6, "Design-system accessibility contracts and branding", "proposed-target-state",
    "Forma's accessibility contracts exist and are partially tested in Forma's own repository (pilot), but no Unbound product consumes them yet.",
    "Unbound builds all interface elements from Forma components whose semantics, focus visibility, contrast-gated color roles, forced-colors behavior, reflow at 320 CSS px and target sizes are contractually specified and tested in the design system, so applications inherit them. Sponsor branding is compiled through a contrast gate that fails any non-conforming color pair, so white-labeling cannot reduce accessibility. Each Forma component used is pinned by release digest and covered by a conformance statement or an Unbound contract test.",
    f"Forma ({FORMA}) is a zero-runtime CSS design system with accessibility contracts: status foregrounds contrast-gated at 4.5:1, forced-colors projection to system colors, a blocking Chromium-only ui-conformance CI job, and catalog requirements for 320/390 px, 200 percent text, reduced motion and WCAG 2.2 A/AA. Status is implementation pilot, not a passed release gate. Unbound does not yet consume Forma.",
    "Consume Forma in Unbound with pinned versions and contract tests; implement sponsor brand compilation with the contrast gate.",
    "Forma repository test results for Forma components only. Nothing for Unbound.",
    "Our intended design system, Forma, specifies accessibility contracts for its components and is in a pilot testing phase. Unbound does not yet use it in a released product.",
    "planned", [k6, k7], [e3, e7], "Proposed: Unbound product owner", freshness="per-event", mechanism="event-driven-automated", automation="high", impl="medium", rec="low",
    requirements=["UNB-PLAT-009", "CNV-EXP-001", "UNB-NAV-049", "UNB-GRANT-032"],
    challenge={
        "customer_intent": "Ensure our branded portal is as accessible as the vendor's default.",
        "adverse_outcome": "Sponsor brand colors fail contrast, making portals unreadable for low-vision users.",
        "conventional_control_effectiveness": "Vendors usually warn customers that custom branding may affect accessibility and disclaim responsibility.",
        "legally_required": "No specific rule; outcome obligations under ADA apply to the customer.",
        "contractually_required": "Rarely.",
        "historical_convention": "Customer is responsible for its own customizations.",
        "architectural_elimination": "Yes within scope: non-conforming brand palettes cannot compile.",
        "automatic_enforcement": "Compiler gate.",
        "continuous_evidence": "Compiler output per brand version.",
        "stronger_alternative": "Constrain customization so accessibility is preserved by construction.",
        "alternative_verifiable": "Yes.",
        "customer_acceptance_likelihood": "Uncertain: some sponsors will resist changes to brand colors.",
        "invalidating_conditions": "If raw HTML or free-form templates are allowed, bypassing the gate.",
        "conventional_cost": "low", "alternative_cost": "low",
        "alternative_risks": "Contrast is only one criterion; brand imagery and custom content can still fail other criteria.",
        "supporting_arguments": ["Removes a common white-label failure."],
        "opposing_arguments": ["Limits brand freedom; may be a sales obstacle."],
        "technical_effectiveness": "stronger", "institutional_acceptance": "uncertain"})
a7 = c.A(7, "Accessibility legal obligations and contract terms", "unknown",
    "No legal applicability assessment exists; UNB-GAP-031 calls for ADA obligations to be assessed separately and UNB-PLAT-005 notes automated WCAG checks do not establish ADA compliance.",
    "Echelon has a counsel-reviewed assessment of which accessibility laws apply by customer segment: the DOJ ADA Title II rule (WCAG 2.1 AA for state and local government web content and mobile apps, including content provided through contractors) for public-entity customers such as public universities; ADA Title III exposure for sponsors serving the public; Section 508 for any federal agency buyer; state accessibility laws; and the European Accessibility Act only if Echelon provides in-scope services to EU consumers. Contracts include an accessibility warranty to WCAG 2.2 AA with remediation commitments; indemnity is negotiated case by case.",
    "Unknown. No assessment located.",
    "Commission the applicability assessment before selling to public-sector or EU customers.",
    "Nothing.",
    "We have not yet completed a legal assessment of accessibility obligations. We will provide one, with contract terms, before contracting with public-sector or EU customers.",
    "planned", [k8], [e8], "Proposed: General Counsel (role not yet staffed)", mechanism="periodic-manual", automation="none", impl="low", rec="low", disc="nda",
    requirements=["UNB-GAP-031", "UNB-PLAT-005"],
    oq=["Does Echelon intend to sell to public universities, state entities or federal agencies?", "Will Unbound serve consumers in the EU, and does the microenterprise exemption apply to Echelon?",
        "What are the current DOJ Title II compliance dates? Verify, as they may have been revised after the 2024 rule."])
a8 = c.A(8, "Accessible authentication, verification, timeouts and support", "proposed-target-state", RAT,
    "Every identity-verification and step-up path has an accessible alternative reaching the same assurance level (mailed one-time code, outbound call to a verified number, captioned assisted video, in-person or notarized verification), relay calls are accepted at the same assurance as voice, and authentication does not require a cognitive function test without an alternative. Session timeouts warn and allow extension except where a disclosed security limit applies. Support channels and documentation meet Section 508 Chapter 6 and EN 301 549 clause 12 expectations, and accommodation requests never presume incapacity.",
    "Not established. CNV-PLT-011 specifies the AccessibleAssurancePath; ADM-045 requires accommodation without assuming incapacity.",
    "Build accessible assurance paths with the identity and contact-change features.",
    "Nothing.",
    "Our requirements include accessible alternatives for identity verification and support, including relay calls. Not yet built.",
    "planned", [k9], [e9], OWN, mechanism="periodic-manual", automation="low", impl="medium", rec="medium",
    requirements=["CNV-PLT-011", "ADM-045"])

c.Q(1, "Conformance standard", "Which accessibility standard and conformance level does your product meet, and what evidence supports that claim?",
    ["Does your product conform to WCAG 2.1 Level AA?", "Is the application accessible?"],
    "Customers must provide accessible services to staff and the public.", "Inaccessible product excludes users and creates legal exposure.",
    [D("SRC-WCAG-2.2"), R("SRC-WCAG-2.1"), R("SRC-EDUCAUSE-HECVAT"), R("SRC-SA-SIG"), UNB], "contractual-common", "high", disc="public")
c.Q(1, "WCAG 2.2 criteria", "Does your conformance include the criteria added in WCAG 2.2, such as focus not obscured, minimum target size, dragging alternatives, redundant entry and accessible authentication?",
    ["Have you evaluated against WCAG 2.2?"],
    "WCAG 2.2 adds criteria relevant to mobile and authentication.", "Product passes 2.1 but fails newer criteria users rely on.",
    [D("SRC-WCAG-2.2", "2.4.11"), D("SRC-WCAG-2.2", "2.5.8"), D("SRC-WCAG-2.2", "3.3.8"), D("SRC-WCAG-2.2", "3.3.7")], "customer-preference", "medium")
c.Q(1, "Conformance scope", "Does your accessibility claim cover every user role and surface, including donor and advisor portals, staff back office, administrator tools, mobile use and embedded partner widgets?",
    ["Are administrative interfaces accessible?"],
    "Vendors often test only public pages.", "Disabled staff cannot perform their jobs in back-office tools.",
    [R("SRC-WCAG-2.2"), R("SRC-ADA", rel="informed-by"), UNB], "customer-preference", "high")
c.Q(1, "Third-party components", "Are third-party components embedded in your product, such as payment forms, identity verification or chat widgets, included in your accessibility evaluation?",
    ["Do embedded third-party tools meet accessibility standards?"],
    "Inaccessible embedded components block whole journeys.", "Donor cannot complete identity verification or payment.",
    [R("SRC-WCAG-2.2"), R("SRC-ITI-VPAT")], "customer-preference", "medium")
c.Q(1, "Reflow and zoom", "Can every journey be completed at 400 percent zoom or on a 320 CSS pixel wide screen without horizontal scrolling or loss of content, including complex tables?",
    ["Is the application responsive and usable when magnified?"],
    "Low-vision users magnify heavily; financial tables often break.", "Statements and approval screens unusable under magnification.",
    [D("SRC-WCAG-2.2", "1.4.10"), D("SRC-WCAG-2.2", "1.4.4")], "customer-preference", "medium")
c.Q(2, "VPAT availability", "Can you provide a current VPAT or Accessibility Conformance Report, and which edition (WCAG, Section 508, EN 301 549 or international) does it use?",
    ["Please attach your VPAT.", "Provide an ACR for the version we are purchasing."],
    "Procurement requires documented conformance.", "Purchase decision made without accessibility evidence.",
    [D("SRC-ITI-VPAT"), R("SRC-SECTION-508"), R("SRC-EN-301-549"), R("SRC-EDUCAUSE-HECVAT")], "contractual-common", "high", industries=["public-sector", "higher-education", "all"], disc="public")
c.Q(2, "ACR credibility", "Who prepared your ACR, was it validated by an independent accessibility specialist, what product version and date does it cover, and what testing methods does it rest on?",
    ["Was your VPAT completed by a third party?"],
    "Self-prepared VPATs are frequently inaccurate.", "Reliance on an overstated conformance claim.",
    [R("SRC-ITI-VPAT"), R("SRC-SECTION-508")], "customer-preference", "high", industries=["public-sector", "higher-education", "all"])
c.Q(2, "ACR maintenance", "Will you update the ACR with each major release and notify us when conformance changes?",
    ["How often is your VPAT updated?"],
    "ACRs drift from the product.", "Outdated ACR masks regressions.",
    [R("SRC-ITI-VPAT")], "contractual-common", "medium")
c.Q(3, "Testing methodology", "How do you test accessibility: which automated tools, what manual review, and what assistive technology testing?",
    ["Describe your accessibility testing process."],
    "Automated tools alone miss most barriers.", "Barriers missed by automation reach users.",
    [R("SRC-WCAG-2.2"), R("SRC-SECTION-508"), R("SRC-EDUCAUSE-HECVAT"), UNB], "customer-preference", "high")
c.Q(3, "Assistive technology coverage", "Which screen reader, browser and platform combinations do you test with, including mobile screen readers?",
    ["Do you test with JAWS, NVDA, VoiceOver and TalkBack?"],
    "Behavior differs significantly across AT and browsers.", "Product works with one screen reader and fails with the one users have.",
    [R("SRC-WCAG-2.2", "4.1.2"), UNB], "customer-preference", "medium")
c.Q(3, "Testing with disabled users", "Do people with disabilities participate in usability testing of your product?",
    ["Do you conduct usability studies with users with disabilities?"],
    "Conformance does not guarantee usability.", "Technically conformant but practically unusable journeys.",
    [R("SRC-WCAG-2.2", rel="informed-by"), UNB], "customer-preference", "medium")
c.Q(3, "Accessibility in release gating", "Are accessibility checks part of your build pipeline, and can a release proceed with known accessibility regressions?",
    ["Is accessibility tested before every release?"],
    "Regressions between audits are common.", "New release breaks previously accessible journeys.",
    [R("SRC-WCAG-2.2"), R("SRC-NIST-SP800-218", rel="informed-by"), UNB], "customer-preference", "medium")
c.Q(3, "AI-generated interface changes", "Where AI agents write or modify user-interface code, how do you ensure their changes do not introduce accessibility failures?",
    ["Is AI-generated code tested for accessibility?"],
    "AI-generated markup frequently lacks semantics and labels.", "Rapid AI-driven changes introduce barriers at scale.",
    [R("SRC-NIST-SP800-218A", rel="informed-by"), R("SRC-WCAG-2.2", "4.1.2")], "customer-preference", "medium", products=["all-echelon-products"])
c.Q(3, "Accessibility training", "Do your designers, developers, testers and support staff receive accessibility training appropriate to their roles?",
    ["Is accessibility training provided to staff?"],
    "Accessibility depends on practitioner knowledge.", "Recurring barriers from untrained staff.",
    [R("SRC-SECTION-508", rel="informed-by"), R("SRC-EDUCAUSE-HECVAT")], "industry-convention", "low", products=["all-echelon-products"])
c.Q(4, "Barrier reporting", "How can our staff or end users report an accessibility barrier, and how quickly will you respond?",
    ["Do you have an accessibility feedback mechanism?"],
    "Users need a route to report barriers.", "Barriers unreported or ignored.",
    [R("SRC-EN-301-549", "12"), R("SRC-ADA", rel="informed-by"), R("SRC-EU-ACCESSIBILITY-ACT", rel="informed-by")], "customer-preference", "medium", juris=["US-federal", "EU"])
c.Q(4, "Remediation timelines", "What are your remediation timeframes for accessibility defects by severity, and will you commit to them contractually?",
    ["How quickly will you fix accessibility issues we report?"],
    "Unremediated barriers create ongoing exclusion and liability.", "Known barriers persist indefinitely.",
    [R("SRC-ITI-VPAT", rel="informed-by"), R("SRC-2CFR200", rel="informed-by")], "contractual-common", "high", industries=["public-sector", "higher-education", "all"])
c.Q(4, "Accessibility roadmap", "Do you publish a roadmap for known non-conformances, with target dates?",
    ["What accessibility improvements are planned?"],
    "Customers need to plan accommodations around known gaps.", "Customer cannot plan for gaps the vendor knows about.",
    [R("SRC-ITI-VPAT")], "customer-preference", "low")
c.Q(4, "Interim alternatives", "While an accessibility defect remains open, what equivalent alternative do you provide so affected users can still complete the task?",
    ["What accommodations are available pending a fix?"],
    "Users need to complete tasks now, not after a release.", "Disabled donor cannot submit a time-sensitive grant recommendation.",
    [R("SRC-ADA", rel="informed-by"), UNB], "customer-preference", "high", industries=["donor-advised-funds", "nonprofit", "all"])
c.Q(5, "Accessible PDFs", "Are statements, contribution acknowledgments, grant letters and reports produced as tagged PDFs that conform to PDF/UA, and how is that verified?",
    ["Are your PDF outputs accessible?"],
    "Financial documents are often inaccessible image-like PDFs.", "Blind donors cannot read their statements or tax receipts.",
    [R("SRC-WCAG-2.2", rel="informed-by"), R("SRC-ADA", "28 CFR 35.200"), R("SRC-SECTION-508", "E205.4"), UNB], "contractual-common", "high", industries=["donor-advised-funds", "nonprofit", "public-sector", "higher-education"],
    note="PDF/UA (ISO 14289-1) and the Matterhorn Protocol are not among the seeded sources, so they are named here without a source reference.")
c.Q(5, "Accessible HTML alternative", "Is every document also available in an accessible HTML form with the same content, and can a user prove it is the same document as the PDF?",
    ["Do you provide accessible alternative formats?"],
    "Alternative formats must be equivalent and current.", "Alternative format differs from the record.",
    [R("SRC-WCAG-2.2"), UNB], "customer-preference", "medium", industries=["donor-advised-funds", "nonprofit"])
c.Q(5, "Exports and charts", "Are data exports, charts and dashboards accessible, for example with structured headers in exported files and text or table alternatives for charts?",
    ["Do charts have accessible alternatives?"],
    "Visual-only charts exclude screen-reader users.", "Users cannot access fund performance or giving history.",
    [D("SRC-WCAG-2.2", "1.1.1"), D("SRC-WCAG-2.2", "1.4.11")], "customer-preference", "medium")
c.Q(5, "Accessible email", "Are notification emails and correspondence templates accessible, including semantic structure, sufficient contrast and a plain-text alternative?",
    ["Are your emails screen-reader friendly?"],
    "Email is a primary channel for donor notices.", "Donors miss notices they cannot read.",
    [R("SRC-WCAG-2.2"), UNB], "customer-preference", "low")
c.Q(5, "Third-party uploaded documents", "Who is responsible for the accessibility of documents uploaded by us, our donors or charities, and does your product help identify inaccessible uploads?",
    ["Are user-uploaded documents checked for accessibility?"],
    "Responsibility for uploaded content is often unclear.", "Inaccessible content presented to users with no one accountable.",
    [R("SRC-ADA", "28 CFR 35.200", rel="informed-by")], "customer-preference", "low", industries=["public-sector", "higher-education", "nonprofit"])
c.Q(6, "Design-system enforcement", "How does your design system or component library enforce accessibility, for example contrast-checked color roles, visible focus, forced-colors support and correct semantics?",
    ["Do you use an accessible component library?"],
    "Component-level enforcement prevents whole classes of defects.", "Each screen reinvents controls with inconsistent accessibility.",
    [D("SRC-WCAG-2.2", "1.4.3"), D("SRC-WCAG-2.2", "2.4.7"), R("SRC-WCAG-2.2", "1.4.11")], "customer-preference", "medium")
c.Q(6, "Custom branding and contrast", "If we apply our own brand colors and logos, how do you prevent our branding from making the product fail contrast requirements?",
    ["Does white-labeling affect accessibility?"],
    "Brand palettes frequently fail contrast.", "Branded portal fails accessibility while the default passes.",
    [D("SRC-WCAG-2.2", "1.4.3"), UNB], "customer-preference", "medium")
c.Q(6, "Motion and sensory preferences", "Does the product respect user settings such as reduced motion, high contrast or forced colors, and text spacing overrides?",
    ["Does the product support operating-system accessibility settings?"],
    "Users with vestibular or vision conditions depend on system settings.", "Animations or color overrides make the product unusable.",
    [D("SRC-WCAG-2.2", "1.4.12"), R("SRC-WCAG-2.2", "2.3.3", rel="informed-by")], "customer-preference", "low")
c.Q(7, "Section 508", "Can you support a federal agency buyer's Section 508 obligations, including a 508-edition ACR and conformance of electronic content and software?",
    ["Is your product Section 508 compliant?"],
    "Federal agencies must procure conformant ICT.", "Agency cannot purchase or must document an exception.",
    [D("SRC-SECTION-508"), R("SRC-FAR", rel="informed-by"), R("SRC-ITI-VPAT")], "legal-regulatory", "medium", industries=["public-sector"], authority="US Access Board standards; federal agency buyers",
    note="Section 508 binds federal agencies, not Echelon; it reaches Echelon through procurement terms. Echelon has not indicated plans to sell to federal agencies.")
c.Q(7, "ADA Title II public entities", "As a public entity subject to the DOJ rule requiring WCAG 2.1 AA for web content and mobile apps, including content we provide through contractors, can you meet that standard by our compliance date?",
    ["Will your product help us comply with the ADA Title II web accessibility rule?"],
    "Public entities are responsible for vendor-provided content.", "Public university or state entity out of compliance through a vendor.",
    [D("SRC-ADA", "28 CFR 35.200"), R("SRC-WCAG-2.1")], "legal-regulatory", "high", industries=PUB, authority="US Department of Justice",
    note="Binds state and local government entities; flows to vendors through the entity's procurement. Compliance dates should be verified against current DOJ publications.")
c.Q(7, "ADA Title III exposure", "Have you received accessibility demand letters, complaints or lawsuits, and how do you allocate accessibility litigation risk with customers who serve the public?",
    ["Have you been sued for web accessibility?", "Will you indemnify us for accessibility claims?"],
    "Private web accessibility litigation is frequent in the US.", "Customer sued over vendor-built inaccessible interface.",
    [R("SRC-ADA"), UNB], "legal-regulatory", "medium", industries=["donor-advised-funds", "nonprofit", "wealth-management", "financial-services"], authority="US Department of Justice; private plaintiffs",
    note="Title III applicability to websites of businesses without physical locations is unsettled and varies by federal circuit; no DOJ Title III web rule exists. Echelon has no litigation history because it has no product.")
c.Q(7, "European Accessibility Act", "Do you provide services to consumers in the EU that fall within the European Accessibility Act, and if so, how do you meet its requirements and publish the required accessibility information?",
    ["Are you compliant with the EAA?"],
    "EAA applies from June 2025 to in-scope products and services offered to EU consumers.", "EU market surveillance action or exclusion.",
    [D("SRC-EU-ACCESSIBILITY-ACT", "Annex I"), R("SRC-EN-301-549")], "legal-regulatory", "low", juris=["EU"], authority="EU member state market surveillance authorities",
    note="Unbound targets US sponsors; EAA applicability is likely limited, and the services microenterprise exemption may apply. Requires counsel assessment.")
c.Q(7, "Accessibility warranty", "Will you warrant accessibility conformance in the contract and commit to remediation if the product falls short?",
    ["Do you provide an accessibility warranty?"],
    "Contractual commitment gives the customer recourse.", "Customer bears all consequences of vendor non-conformance.",
    [R("SRC-2CFR200", rel="informed-by"), R("SRC-STATERAMP", rel="informed-by")], "contractual-common", "medium", industries=["public-sector", "higher-education", "all"])
c.Q(8, "Accessible support and documentation", "Are your support channels and help documentation accessible, for example accepting relay calls, offering text-based support and providing documentation in accessible formats?",
    ["Is customer support accessible to users with disabilities?"],
    "Support and documentation are part of the accessible product.", "Disabled users cannot get help.",
    [D("SRC-SECTION-508", "602"), D("SRC-SECTION-508", "603"), D("SRC-EN-301-549", "12"), UNB], "contractual-common", "medium", industries=["public-sector", "higher-education", "all"])
c.Q(8, "Accessible authentication and verification", "Can users with disabilities complete sign-in, multi-factor authentication and identity verification without solving puzzles, memorizing codes or using a smartphone, while reaching the same security level?",
    ["Is your MFA accessible?", "Are CAPTCHAs used?"],
    "Security steps are a frequent accessibility barrier.", "Disabled donor locked out or pushed to weaker verification.",
    [D("SRC-WCAG-2.2", "3.3.8"), R("SRC-NIST-SP800-63-4", rel="informed-by"), UNB], "customer-preference", "high")
c.Q(8, "Timeouts", "Do session timeouts warn users and allow extension, and how do you balance that with security limits during long tasks such as grant submission?",
    ["Can users with disabilities get more time to complete tasks?"],
    "Users who need more time lose work at timeouts.", "Lost grant recommendations or repeated re-authentication barriers.",
    [D("SRC-WCAG-2.2", "2.2.1"), R("SRC-FFIEC-AUTH-GUIDANCE-2021", rel="informed-by")], "customer-preference", "medium")
c.write()
