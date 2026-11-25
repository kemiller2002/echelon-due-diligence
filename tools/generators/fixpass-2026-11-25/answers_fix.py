"""BL-016 and BL-021 fix pass on answer units, controls and evidence requirements.

Run once from the repository root. Never raises a status; never sets `review`.
"""
import json
import sys

sys.path.insert(0, "tools/generators/fixpass-2026-11-25")
from lib import Store, hist, note, replace, add_list, created  # noqa: E402

ANS = Store("answers")
CTL = Store("controls")
EVR = Store("evidence-requirements")

if any(h.get("by") == "fix-pass-agent" for h in ANS.peek("ANS-AIA-007").get("history", [])):
    sys.exit("already applied")

STATUS_RANK = {s: i for i, s in enumerate([
    "unknown", "unsupported", "not-applicable", "requires-external-validation", "proposed-target-state",
    "approved-policy-implementation-pending", "partially-implemented", "implemented-not-independently-verified",
    "verified-operational"])}
before = {r["id"]: r["status"] for r in ANS.all()}

# ---------------------------------------------------------------- BL-016
# ANS-AIA-007: the build check is an internal research integrity check, not a customer safeguard.
r = ANS.get("ANS-AIA-007")
replace(r, "status_rationale", "It enforces, by schema and build checks (tools/build.fsx), that customer statements may not assert current capability unless the status is implemented, that em dashes and dangling references fail the build, and that independent assurance claims are flagged.",
        "Its build tool (tools/build.fsx) is an internal research integrity check on this repository: it compares two metadata fields set by the same author (status and customer_statement_kind), applies a heuristic wording lint, fails on em dashes and dangling references, and flags independent assurance claims. It does not read evidence and cannot tell whether a status is true, so it is not a customer safeguard.")
replace(r, "status_rationale", "Human review and sign-off of answers before customer release is not yet defined, and no answer has been released to a customer.",
        "Since 2026-11-25 the operating contract requires named human approval before any release and the build fails on an approval without a named human, but no answer unit has been approved and none has been released to a customer.")
r["customer_statement"] = ("Echelon's questionnaire answers are drafted with AI from an internal answer library. The library has "
    "internal consistency checks used for research integrity; they do not verify that an answer is true and are not a "
    "customer safeguard. No answer has yet been approved by a named human reviewer, and Echelon will release no answer "
    "until a named human has reviewed it and accepts accountability for it.")
replace(r, "target_answer", "a customer statement that the build tool checks against that status",
        "a customer statement that internal checks compare against that status (an integrity aid, not assurance)")
r["residual_risks"] = r.get("residual_risks", []) + [
    "The build check never reads evidence and compares fields set by the same author; it can pass a wrong status consistently.",
    "AI tools used to draft answers may process customer questionnaire text; which tools and under which provider terms is not yet recorded (OBJ-PRIVACY-011)."]
c = r["challenge"]
c["architectural_elimination"] = ("Not eliminated. The build tool flags inconsistency between status and statement kind and "
    "some unhedged wording; it is an internal research integrity check, not a customer safeguard, and only named human "
    "review can establish that a statement is true.")
c["automatic_enforcement"] = "Schema, status-to-kind and wording heuristics on every build; human approval gate for release (no approvals yet)."
add_list(r, "open_questions", ["Which AI tools currently process prospect or customer questionnaire material, and under which provider retention and training terms?"])
hist(r, "BL-016: stopped presenting the repository build check as a customer safeguard; described it as an internal research integrity check; added human-approval position and residual risks (OBJ-SKEPTIC-002, OBJ-PROCURE-014, OBJ-VRM-007).")

# ANS-TEN-004: remove 'eliminated' owner bypass.
r = ANS.get("ANS-TEN-004")
replace(r, "target_answer", "Every tenant table in a cell has row-level security enabled and forced, so table owners cannot bypass it,",
        "Every tenant table in a cell has row-level security enabled and forced, so the table owner role cannot bypass it (superusers, roles with BYPASSRLS and the deploy identity still can; see residual risks),")
replace(r, "target_answer", "no application role has BYPASSRLS or superuser.",
        "no application role has BYPASSRLS or superuser. The migration (deploy) identity is separate from the runtime identity, and a release gate compares RLS state (relrowsecurity, relforcerowsecurity and policies) before and after every Strata deploy and fails on any weakening; ALTER TABLE statements affecting RLS outside the pipeline raise an alert.")
r["challenge"]["architectural_elimination"] = ("Not eliminated; reduced. Tenant roles have no privileges on other cells' "
    "schemas by design, and FORCE ROW LEVEL SECURITY removes the table owner's default bypass. Superusers, roles with "
    "BYPASSRLS, managed-service administrator roles and the Strata deploy identity (which can ALTER TABLE ... NO FORCE "
    "or DISABLE ROW LEVEL SECURITY in a migration) can still bypass or remove RLS.")
r["residual_risks"] = r.get("residual_risks", []) + [
    "The Strata deploy identity, or the CI runner holding it, can disable or unforce RLS in one migration; only identity separation, a pre and post deploy RLS diff gate and alerting reduce this.",
    "Managed PostgreSQL administrator roles are outside Echelon's RLS claims."]
hist(r, "BL-016: removed the claim that FORCE eliminates owner bypass; named superusers, BYPASSRLS roles and the deploy identity; added deploy identity separation and RLS diff gate to the target (OBJ-PENTEST-004).")
for cid in r["controls"]:
    ctl = CTL.get(cid)
    note(ctl, "Owner bypass is reduced by FORCE, not eliminated: superusers, BYPASSRLS roles and the Strata deploy identity remain able to bypass or disable RLS; the target adds deploy and runtime identity separation and a pre and post deploy RLS diff gate (OBJ-PENTEST-004).")

# Single-person-infeasible commitments.
CAP = ("Current position (2026-11-25): Echelon has one principal, the managing member, and no staff, on-call rotation or "
       "contracted support provider, so this commitment cannot be met today.")
r = ANS.get("ANS-SUP-001")
replace(r, "target_answer", "with critical-severity coverage at all times.",
        "with critical-severity coverage at all times once, and only while, Echelon has at least two trained responders in rotation or a contracted on-call provider; until then the offer is business-hours support with best-effort after-hours response, stated as such in the order form.")
r["current_practice"] += " " + CAP
r["customer_statement"] = ("We have not yet defined a support offering because we have no customers. Echelon has one "
    "principal today and cannot offer continuous coverage; continuous coverage for critical issues is planned only once "
    "staffing or a contracted on-call provider can sustain it, and until then we would offer business-hours support "
    "with best-effort after-hours response.")
hist(r, "BL-016: made continuous critical coverage conditional on staffing or contracted capacity and stated the honest current position (OBJ-PROCURE-004).")

r = ANS.get("ANS-SUP-002")
replace(r, "target_answer", "(for example 30 minutes for Severity 1 at any hour)",
        "(for example 30 minutes for Severity 1 at any hour, offered only when a staffed or contracted on-call rotation exists; at single-principal capacity the honest commitment is a business-hours response target with best-effort after hours)")
r["current_practice"] += " " + CAP
r["customer_statement"] = ("We have not yet set severity levels or response targets. With one principal today we cannot "
    "commit to round-the-clock response times; contractual 24x7 response targets for critical issues are planned only "
    "once staffing or a contracted on-call provider exists.")
hist(r, "BL-016: made the 30-minute 24x7 Severity 1 target conditional on staffing or contracted capacity (OBJ-PROCURE-004).")

r = ANS.get("ANS-AVL-003")
replace(r, "target_answer", "Customers are notified of a material outage within 30 minutes of detection,",
        "Customers are notified of a material outage within 30 minutes of detection once 24x7 detection and an on-call rotation (staffed or contracted) exist; until then notice is as soon as possible after detection during monitored hours, which is still")
replace(r, "target_answer", "which is designed to satisfy the bank service provider obligation",
        "intended to satisfy the bank service provider obligation")
r["current_practice"] += " " + CAP
add_list(r, "residual_risks", ["Without 24x7 detection, an outage that starts out of hours may not be detected for hours; the 30-minute notice depends on capacity Echelon does not have."])
hist(r, "BL-016: made the 30-minute outage notice conditional on 24x7 detection and on-call capacity (OBJ-PROCURE-004).")

r = ANS.get("ANS-IR-002")
replace(r, "target_answer", "A named incident commander and at least one trained deputy, 24x7 paging with escalation,",
        "A named incident commander and at least one trained deputy, 24x7 paging with escalation (achievable only with a second trained responder or a contracted MDR or incident response provider),")
r["current_practice"] += " " + CAP
hist(r, "BL-016: stated that 24x7 incident paging requires a second responder or contracted provider and recorded the current single-principal position (OBJ-PROCURE-004, OBJ-BANKCISO-010).")

r = ANS.get("ANS-MON-004")
replace(r, "target_answer", "high-severity alerts page an on-call responder 24x7 with a 15-minute acknowledgment target;",
        "high-severity alerts page an on-call responder 24x7 with a 15-minute acknowledgment target (conditional on a staffed rotation or a contracted MDR provider);")
r["current_practice"] += " " + CAP
hist(r, "BL-016: made 24x7 alert response conditional on staffing or a contracted MDR provider (OBJ-PROCURE-004).")

r = ANS.get("ANS-TRM-001")
replace(r, "target_answer", "a transition period of up to 12 months at unchanged service levels,",
        "a transition period of up to 12 months at the service levels in effect where Echelon's staffing or a contracted successor operator can sustain them (the period offered at current single-principal capacity is shorter and stated in the order form, with full data export available throughout),")
r["current_practice"] += " " + CAP
r["customer_statement"] = ("Unbound is not yet in production. Its requirements specify governed tenant offboarding and a "
    "structured partner exit process that reconciles every fund and in-flight recommendation. This is a design "
    "commitment, not an operating control, and has not been independently verified. A long transition at unchanged "
    "service levels depends on staffing or a contracted successor operator that Echelon does not have today.")
hist(r, "BL-016: made the 12-month transition at unchanged service levels conditional on staffing or contracted capacity (OBJ-PROCURE-004).")

r = ANS.get("ANS-LEG-006")
replace(r, "target_answer", "we provide transition assistance for up to 12 months at contracted rates,",
        "we provide transition assistance for up to 12 months at contracted rates, sized to the capacity Echelon or a contracted successor operator actually has (see ANS-TRM-001),")
hist(r, "BL-016: tied the 12-month transition commitment to actual or contracted capacity (OBJ-PROCURE-004).")

r = ANS.get("ANS-FST-003")
replace(r, "target_answer", "A written wind-down plan and a reserve sized to fund an orderly transition period are maintained and tested.",
        "A written wind-down plan is maintained and tested, and a reserve or insurance (for example key-person cover) sized to fund an orderly transition period is put in place once capital allows; until it exists Echelon states that the wind-down is unfunded.")
r["current_practice"] += " Echelon has no reserve, key-person insurance or other funding for a wind-down today."
r["customer_statement"] = ("Echelon plans to offer verified source and deployment escrow and customer-controlled data "
    "export, and a funded wind-down plan once capital or insurance allows. None of these is in place, and Echelon has no "
    "wind-down reserve today. The Unbound design does not hold or move customer funds.")
hist(r, "BL-016: made the funded wind-down conditional on capital or insurance and stated that no reserve exists (OBJ-PROCURE-004, OBJ-DAFSPONSOR-009).")

r = ANS.get("ANS-TRM-003")
replace(r, "target_answer", "Echelon maintains a funded wind-down plan covering at least the contractual transition period;",
        "Echelon maintains a wind-down plan covering at least the contractual transition period, funded by reserve or insurance once capital allows (it is unfunded today);")
hist(r, "BL-016: made the funded wind-down conditional on capital or insurance (OBJ-PROCURE-004).")

# Training versus model validation.
r = ANS.get("ANS-PRV-011")
replace(r, "target_answer", "Echelon does not use customer data to train, fine-tune or evaluate models,",
        "Echelon does not use customer data to train or fine-tune models. Evaluation, validation and performance monitoring that a bank customer's model risk management requires (ANS-AIG-008) use synthetic data, or customer data only where that customer has authorized it in writing, scoped to its own tenant and for its own benefit; results never train models or benefit other customers. Separately,")
r["customer_statement"] = ("Echelon's intended position is that customer data is not used to train or fine-tune AI "
    "models, that model validation uses synthetic data or a customer's own data only with that customer's written "
    "authorization, and that AI agents do not have standing access to production customer data. No AI feature processes "
    "customer data today because Unbound is not in production.")
hist(r, "BL-016: reconciled the no-training commitment with bank model validation support: training and fine-tuning prohibited; validation only on synthetic or customer-authorized data (OBJ-PRIVACY-009).")

r = ANS.get("ANS-IPR-004")
replace(r, "target_answer", "is never used to train, fine-tune or evaluate AI models, ours or a provider's,",
        "is never used to train or fine-tune AI models, ours or a provider's; it is used to evaluate or validate a model only where the customer authorizes that in writing for validation of the model as used in its own tenant (otherwise synthetic data is used),")
r["customer_statement"] = ("Echelon does not intend to use customer data to train AI models and plans to make that a "
    "contractual commitment enforced in the platform, with model validation limited to synthetic data or data the "
    "customer authorizes for its own validation. These commitments are not yet contractually offered or implemented.")
hist(r, "BL-016: distinguished prohibited training from customer-authorized validation (OBJ-PRIVACY-009).")

r = ANS.get("ANS-AIG-008")
replace(r, "target_answer", "evaluation results on frozen test sets,",
        "evaluation results on frozen synthetic test sets or on customer data only under that customer's written authorization within its tenant (consistent with ANS-PRV-011 and ANS-IPR-004),")
hist(r, "BL-016: limited model validation data to synthetic or customer-authorized data, consistent with the no-training commitment (OBJ-PRIVACY-009).")

# Folio HTML-to-PDF SSRF and local file read.
new_ctl = CTL.next_id("ECTL", "APP", 3)
new_evr = EVR.next_id("EVR", "APP", 3)
EVR.add("APP", {
    "id": new_evr, "title": "Document renderer isolation configuration and negative test results",
    "description": "Per release: renderer sandbox configuration (no network egress, file and other non-data URL schemes disabled, JavaScript disabled, CPU, memory, page and time limits) and results of negative tests that attempt fetches to cloud metadata, private ranges and external hosts, file:// reads, iframe and object embedding and script execution through rendered HTML.",
    "producer": "not yet assigned (intended: Unbound release pipeline; not built)", "mechanism": "event-driven-automated",
    "freshness": "per-event", "format": "JSON test report with configuration digest", "independence": "first-party",
    "disclosure_classification": "nda", "status": "proposed-target-state",
    "notes": "Fix pass 2026-11-25 (fix-pass-agent): created for BL-016 (OBJ-PENTEST-016)."})
CTL.add("APP", {
    "id": new_ctl, "title": "Isolated server-side document rendering (Folio HTML-to-PDF)",
    "objective": "Prevent server-side request forgery, local file read and renderer script execution when statements, receipts or grant letters are rendered from HTML to PDF with a headless browser or similar engine: the renderer runs in an isolated sandbox with no network egress, no file or other non-data URL schemes, JavaScript disabled, all assets inlined from an allowlist, and size, page and time limits; rendering inputs are generated from typed data, never from user-supplied HTML.",
    "control_type": "preventive-structural", "assurance_level": "L3-restricted-interface",
    "implementing_systems": ["Folio (document generation; HTML-to-PDF path outside core)", "Unbound rendering service (not built)"],
    "cwe": ["CWE-918", "CWE-73", "CWE-22", "CWE-400"],
    "framework_refs": [{"source_id": "SRC-MITRE-CWE", "relation": "maps-to", "basis": "directly-documented", "locator": "CWE-918"},
                       {"source_id": "SRC-OWASP-ASVS", "relation": "maps-to", "basis": "reasonably-inferred"}],
    "status": "proposed-target-state", "evidence_requirements": [new_evr],
    "owner": "Engineering Lead (proposed role, unassigned)",
    "residual_risks": ["Renderer engine vulnerabilities (for example in a bundled Chromium) still allow sandbox escape attempts; patch cadence of the engine matters.",
                       "Fonts and images fetched at render time reintroduce egress unless inlined."],
    "notes": "Fix pass 2026-11-25 (fix-pass-agent): created for BL-016. HTML-to-PDF rendering was previously treated only as an XSS exclusion (OBJ-PENTEST-016)."})
r = ANS.get("ANS-APP-005")
r["target_answer"] += (" Server-side document rendering (Folio HTML-to-PDF for statements, receipts and grant letters) is "
    "treated as an SSRF and local file read sink: the renderer runs isolated with no network egress, no file scheme, "
    "JavaScript disabled and size and time limits, and is in penetration test scope whenever documents are rendered "
    "server side.")
replace(r, "intended_practice", "SSRF test cases run on every release.",
        "SSRF test cases run on every release. The document renderer is isolated as in " + new_ctl + ".")
add_list(r, "controls", [new_ctl])
add_list(r, "evidence_requirements", [new_evr])
r["residual_risks"] = (r.get("residual_risks") or []) + [
    "HTML-to-PDF rendering with a headless browser can fetch cloud metadata or internal URLs, read local files through file:// or embedded frames, and run script in the renderer unless isolated."]
hist(r, "BL-016: added Folio HTML-to-PDF rendering as an SSRF and local file read surface with control %s and evidence %s (OBJ-PENTEST-016)." % (new_ctl, new_evr))
note(CTL.get("ECTL-APP-007"), "Outbound destination control does not cover the document renderer by itself; HTML-to-PDF rendering needs the isolated renderer in %s (OBJ-PENTEST-016)." % new_ctl)
r = ANS.get("ANS-ARC-002")
r["residual_risks"] = (r.get("residual_risks") or []) + [
    "Server-side HTML-to-PDF rendering (Folio) is a trust boundary: rendered content can reach the network and file system unless the renderer is isolated (" + new_ctl + ")."]
add_list(r, "controls", [new_ctl])
hist(r, "BL-016: recorded the document renderer as a trust boundary and linked " + new_ctl + " (OBJ-PENTEST-016).")

# Repository instruction files as prompt-injection path.
ais_ctl = CTL.next_id("ECTL", "AIS", 3)
ais_evr = EVR.next_id("EVR", "AIS", 3)
EVR.add("AIS", {
    "id": ais_evr, "title": "Protected-path configuration and change log for agent instruction files",
    "description": "Per repository: the list of protected paths (AGENTS.md, CLAUDE.md, GEMINI.md, skills, agent and workflow configuration), code-owner rules requiring human approval, token scopes showing agents cannot write those paths, and every change to them with the approving human.",
    "producer": "not yet assigned (intended: source control platform settings export and audit log)", "mechanism": "periodic-automated",
    "freshness": "P1D", "format": "Settings export and audit log extract", "independence": "first-party",
    "disclosure_classification": "nda", "status": "proposed-target-state",
    "notes": "Fix pass 2026-11-25 (fix-pass-agent): created for BL-016 (OBJ-PENTEST-012)."})
CTL.add("AIS", {
    "id": ais_ctl, "title": "Agent instruction files as protected paths",
    "objective": "Prevent indirect prompt injection into AI coding agents through repository instruction files (AGENTS.md, CLAUDE.md, GEMINI.md, skills, agent and workflow configuration) that agents read as operating instructions: these paths require human code-owner approval, diffs to them are surfaced in review, agents run with tokens that cannot modify them, and agents treat instruction text arriving through pull requests, dependencies, issues or fetched pages as untrusted data.",
    "control_type": "preventive-gate", "assurance_level": "L5-build-release-gate",
    "implementing_systems": ["Source control platform branch protection and code owners (configuration not verified)", "Praxis (records agent executions; does not enforce this)"],
    "status": "proposed-target-state", "evidence_requirements": [ais_evr],
    "owner": "Not assigned (proposed: Echelon managing member)",
    "residual_risks": ["A single maintainer approving their own agent's change to an instruction file gives no independent check.",
                       "Instruction text can also arrive through dependencies and fetched content that are not protected paths."],
    "notes": "Fix pass 2026-11-25 (fix-pass-agent): created for BL-016 (OBJ-PENTEST-012). Echelon repositories already contain such files (for example this repository's AGENTS.md and CLAUDE.md); whether they are protected paths today is unknown."})
r = ANS.get("ANS-AIS-001")
r["target_answer"] += (" Repository instruction files that coding agents read as operating instructions (AGENTS.md, CLAUDE.md, "
    "skills, workflow and agent configuration) are treated as an injection path: they are protected paths requiring "
    "human code-owner approval, agents cannot write them, and the assumed-breach penetration test includes a poisoned "
    "instruction file (" + ais_ctl + ").")
add_list(r, "controls", [ais_ctl])
add_list(r, "evidence_requirements", [ais_evr])
r["residual_risks"] = (r.get("residual_risks") or []) + [
    "Repository instruction files (AGENTS.md, CLAUDE.md, skills, workflow files) are read by coding agents as instructions; a pull request, dependency, issue or fetched page that changes or injects into them can steer an agent that holds write tokens."]
replace(r, "customer_statement", "Echelon's design contains prompt injection by architecture:",
        "Echelon's design aims to limit what a successful prompt injection can do:")
hist(r, "BL-016: added repository instruction files as a prompt-injection path for AI coding agents with control %s; removed 'contains prompt injection by architecture' wording (OBJ-PENTEST-012, OBJ-PENTEST-011)." % ais_ctl)
r = ANS.get("ANS-AIS-008")
r["target_answer"] += " (7) agent instruction files are protected paths that only a human code owner can change (" + ais_ctl + ")."
add_list(r, "controls", [ais_ctl])
r["residual_risks"] = r.get("residual_risks", []) + ["Instruction files in the repositories agents edit are an injection path; whether they are protected today is unknown."]
hist(r, "BL-016: added protected instruction files (%s) to the target (OBJ-PENTEST-012)." % ais_ctl)

# Trust center: publishing planned controls signals missing defenses.
TC = ("Publishing the planned or absent status of preventive and detective controls on a public page can signal missing "
      "defenses to attackers; under DD-TC-002 (trust-center/TRUST-CENTER-REQUIREMENTS.md) control-status detail is "
      "disclosed at the authenticated-prospect or NDA tier, while still being disclosed honestly to anyone who asks.")
for aid in ("ANS-AUD-008", "ANS-AUD-009", "ANS-AUD-005"):
    r = ANS.get(aid)
    r["residual_risks"] = (r.get("residual_risks") or []) + [TC]
    hist(r, "BL-016: noted that publishing planned controls can signal missing defenses and linked DD-TC-002 (OBJ-PENTEST-019, OBJ-BANKCISO-015).")

# ---------------------------------------------------------------- BL-021 independent evidence
def new_evr(cat, title, description, independence, producer, notes, disclosure="customer-only", mechanism="external-attestation", freshness="P1Y"):
    eid = EVR.next_id("EVR", cat, 3)
    EVR.add(cat, {"id": eid, "title": title, "description": description, "producer": producer, "mechanism": mechanism,
                  "freshness": freshness, "format": "Report or letter (PDF) with scope, period and issuer", "independence": independence,
                  "disclosure_classification": disclosure, "status": "proposed-target-state",
                  "notes": "Fix pass 2026-11-25 (fix-pass-agent): created for BL-021. " + notes})
    return eid

link = {}
soc1 = "SOC 1 Type 2 (AT-C 320) service auditor's report, restricted to customers and their auditors"
e = new_evr("PAY", "SOC 1 Type 2 testing of payment preparation and release controls",
            "Service auditor's tests of control objectives for payment file preparation, payee verification, release tiers, holds re-check at transmission and bank integration access, in a " + soc1 + ".",
            "independent-third-party", "Independent CPA firm (not engaged)", "Answers OBJ-BANKCISO-001 and OBJ-REGULATOR-005 for money movement.")
link.setdefault(e, []).extend(["ANS-PAY-%03d" % i for i in range(1, 9)])
e = new_evr("PAY", "Independent penetration and business-logic test of payment flows",
            "Independent tester's report on payment release, payee change, release-tier bypass, race conditions and replay against payment file generation, including retest evidence.",
            "independent-third-party", "Independent penetration testing firm (not engaged)", "Business-logic and race-condition objectives (OBJ-PENTEST-015).", disclosure="nda")
link.setdefault(e, []).extend(["ANS-PAY-004", "ANS-PAY-007", "ANS-PAY-008"])
e = new_evr("PAY", "Nacha Rules compliance audit as Third-Party Service Provider",
            "Annual Nacha Rules compliance audit of Echelon's TPSP role, performed by a qualified independent auditor, plus the TPSP risk assessment, as an ODFI would request.",
            "independent-third-party", "Qualified independent ACH auditor (not engaged)", "OBJ-VRM-014. Whether Echelon is a TPSP for each sponsor depends on the final payment model.")
link.setdefault(e, []).extend(["ANS-PAY-001", "ANS-PAY-002", "ANS-PAY-003"])
e = new_evr("RCN", "SOC 1 Type 2 testing of reconciliation controls",
            "Service auditor's tests of reconciliation completeness, matching rules and tolerance governance, break management and segregation from payment initiation, in a " + soc1 + ".",
            "independent-third-party", "Independent CPA firm (not engaged)", "Covers all reconciliation answer units.")
link.setdefault(e, []).extend(["ANS-RCN-%03d" % i for i in range(1, 8)])
e = new_evr("GRT", "SOC 1 Type 2 testing of grant authorization and eligibility controls",
            "Service auditor's tests of grant approval under sponsor delegation, eligibility and charity status checks, segregation of duties and amount reservation, in a " + soc1 + ".",
            "independent-third-party", "Independent CPA firm (not engaged)", "Covers all grant answer units.")
link.setdefault(e, []).extend(["ANS-GRT-%03d" % i for i in range(1, 11)])
e = new_evr("FEE", "Independent recomputation of fees and SOC 1 testing of fee change control",
            "Agreed-upon procedures or SOC 1 Type 2 control testing by an independent CPA: recomputation of a sample of fund-level fees from versioned schedules and testing of fee schedule change control.",
            "independent-third-party", "Independent CPA firm (not engaged)", "Covers all fee answer units.")
link.setdefault(e, []).extend(["ANS-FEE-%03d" % i for i in range(1, 7)])
e = new_evr("AML", "Independent testing of sanctions screening coverage and effectiveness",
            "Independent tester's report on sanctions list coverage and update latency, matching thresholds, name variants and transliteration, alert disposition evidence and recordkeeping, using seeded test cases.",
            "independent-third-party", "Independent AML or sanctions testing firm (not engaged)", "Echelon's own OFAC exposure (OBJ-REGULATOR-006) also needs counsel review.")
link.setdefault(e, []).extend(["ANS-AML-001", "ANS-AML-002", "ANS-AML-003", "ANS-AML-004", "ANS-AML-005", "ANS-AML-007", "ANS-REG-004"])
e = new_evr("AML", "Counsel opinion on Echelon's BSA status and independent AML testing of sponsor-facing features",
            "Outside counsel's written opinion on whether Echelon is a BSA financial institution or money services business given the final payment model, plus the sponsor's or partner's independent AML test results covering Unbound monitoring and case features.",
            "independent-third-party", "Outside counsel and the sponsor's independent AML tester (neither engaged)",
            "Outside counsel retained by Echelon gives a professional opinion, not assurance; the AML test is performed for the sponsor. Examination of Echelon under the Bank Service Company Act would be regulatory-examination evidence if it occurs.")
link.setdefault(e, []).append("ANS-AML-006")
e = new_evr("TEN", "Independent tenant isolation test report and customer-run two-tenant test results",
            "Cross-tenant section of an independent penetration test (cross-tenant reads and writes, spoofed routing hints, pooled connection reuse, background jobs, caches, AI retrieval, deploy-path RLS removal) with retest evidence, plus results of customer-run tests using two provisioned test tenants.",
            "independent-third-party", "Independent penetration testing firm (not engaged); customers", "OBJ-BANKCISO-007, OBJ-REGULATOR-005.", disclosure="nda")
link.setdefault(e, []).extend(["ANS-TEN-005", "ANS-TEN-004"])
e = new_evr("DAF", "Outside tax counsel review of the regulatory applicability register for DAF rules",
            "Dated review by outside tax counsel of the versioned interpretations of the 2023 proposed DAF regulations and of final rules when issued, including sponsor election options.",
            "independent-third-party", "Outside tax counsel (not engaged)", "Counsel retained by Echelon gives an opinion, not assurance.")
link.setdefault(e, []).append("ANS-DAF-010")
e = new_evr("AIG", "Counsel AI law applicability memorandum",
            "Dated memorandum by outside counsel classifying each AI use under the EU AI Act as amended, Colorado SB 26-189, other state automated decision rules and the NAIC bulletin, with facts relied on and re-evaluation triggers.",
            "independent-third-party", "Outside counsel (not engaged)", "Counsel retained by Echelon gives an opinion, not assurance.")
link.setdefault(e, []).append("ANS-AIG-007")
e = new_evr("WLB", "Counsel review of co-branded disclosures and state platform registration acknowledgments",
            "Outside counsel's review of co-branded and partner copy for legal meaning, and the California and Hawaii charitable fundraising platform registration filings with the attorneys general's acknowledgments.",
            "independent-third-party", "Outside counsel (not engaged); state attorneys general (acknowledgment only)",
            "A registration acknowledgment is not regulator approval of the disclosures.")
link.setdefault(e, []).append("ANS-WLB-002")
for eid, aids in link.items():
    for aid in aids:
        r = ANS.get(aid)
        add_list(r, "evidence_requirements", [eid])
        hist(r, "BL-021: linked planned independent evidence %s (status proposed-target-state); no independent evidence exists today (OBJ-BANKCISO-001, OBJ-REGULATOR-005)." % eid)

# ---------------------------------------------------------------- BL-021 challenge sweep
UNVALIDATED = ("Institutional acceptance is unvalidated: no buyer, auditor, regulator or insurer evidence or cited source "
               "supports an acceptance rating (DD-VAL-ADV-001, DD-VAL-ADV-002). Treat any rating as agent judgment until "
               "target-customer conversations or a sourced document support it.")
sweep = 0
for r0 in list(ANS.all()):
    c0 = r0.get("challenge")
    if not c0:
        continue
    r = ANS.get(r0["id"])
    c = r["challenge"]
    prior_text = c.get("customer_acceptance_likelihood", "")
    prior_rating = c.get("institutional_acceptance", "")
    sup = c.get("supporting_arguments") or []
    sup.append("agent judgment: customer acceptance likelihood '%s'; institutional acceptance rating '%s' (unvalidated, no cited source)." % (prior_text, prior_rating))
    c["supporting_arguments"] = sup
    opp = c.get("opposing_arguments") or []
    opp.append(UNVALIDATED)
    c["opposing_arguments"] = opp
    c["customer_acceptance_likelihood"] = "Unknown; unvalidated. The prior agent judgment is kept in supporting_arguments."
    c["institutional_acceptance"] = "unknown"
    hist(r, "BL-021: set institutional_acceptance to unknown (prior '%s' was unsourced agent judgment, kept in supporting_arguments) and added an unvalidated-acceptance note to opposing_arguments (OBJ-VRM-019, OBJ-SKEPTIC-014)." % prior_rating)
    sweep += 1
r = ANS.get("ANS-CHG-006")
r["challenge"]["opposing_arguments"].append("Praxis provenance is self-declared; an auditor's change-authorization evidence of record is the source control platform's enforced settings and approval logs, with Praxis linking work items as supplementary evidence (OBJ-SOC2AUD-007).")

# ---------------------------------------------------------------- BL-021 two-person controls
SECOND = {
    "ANS-SDL-003": ("Second person: until Echelon hires a second engineer, the independent reviewer is a contracted external code reviewer (a named individual or firm under contract, with its own source control account bound to branch protection). An AI agent never counts as the second reviewer. As of 2026-11-25 no reviewer is contracted, so this control has no operator; the compensating position is disclosure of single-maintainer status and periodic external review of control-relevant diffs once contracted.",
                    "As of 2026-11-25 Echelon has one principal; independent human review has no operator until a second engineer or contracted reviewer exists."),
    "ANS-CHG-002": ("Second person: the approver who is not the author is a contracted external reviewer until a second engineer is hired; repository and pipeline administration changes are reviewed by the same contracted party. Until one is contracted the control is not operable and Echelon discloses this rather than claiming segregation.",
                    "As of 2026-11-25 there is no second person; author, approver and deployer are the same principal or agents acting for that principal."),
    "ANS-IAM-003": ("Second person: elevation approval comes from a contracted fractional security officer or second operator. Until one exists, the compensating control is no standing access, elevation recorded in an append-only log outside the managing member's administrative control, and after-the-fact review of every elevation by the contracted reviewer within one business day, disclosed to customers.",
                    "As of 2026-11-25 no second approver exists for privileged elevation."),
    "ANS-IAM-004": ("Second person: the second share of the sealed break-glass credential is held by a contracted successor operator or by counsel under a written custody agreement, never by an AI agent. Until that party is named, two-person activation cannot be performed and break-glass is a single-person action with immediate customer notification as the compensating control.",
                    "As of 2026-11-25 no second holder for break-glass activation is named."),
    "ANS-BKP-002": ("Second person: a production restore is authorized by the managing member and a contracted operator (the same party named for break-glass). Until one exists, restores run only through the pipeline with automatic notification of affected tenants' administrators and post-restore review by the contracted reviewer.",
                    "As of 2026-11-25 no second authorized person for restores exists."),
}
for aid, (target_add, risk) in SECOND.items():
    r = ANS.get(aid)
    r["target_answer"] += " " + target_add
    r["residual_risks"] = (r.get("residual_risks") or []) + [risk]
    hist(r, "BL-021: named the second-person role and the compensating control for the two-person control (OBJ-BANKCISO-004).")

# ---------------------------------------------------------------- BL-021 contradictions
r = ANS.get("ANS-HR-006")
assert r["status"] == "implemented-not-independently-verified"
r["status"] = "partially-implemented"
r["status_rationale"] += (" Downgraded 2026-11-25: attribution is self-declared by the executing tool from environment "
    "variables and flags, is not authenticated, and records show model 'unknown' where not declared (consistent with "
    "ANS-ISP-007), so only part of the target (recording) exists; trustworthy attribution does not.")
r["customer_statement"] = ("In Praxis-governed Echelon repositories, work is recorded as attributed to a human, AI agent "
    "or automation and to a specific execution. The attribution is self-declared by the executing tool, is not "
    "authenticated, and can be wrong or incomplete (the model is often recorded as unknown). This is first-party "
    "tooling for repository work, not a production service, and has not been independently verified.")
hist(r, "BL-021: downgraded status from implemented-not-independently-verified to partially-implemented and qualified the statement as self-declared and unauthenticated, reconciling with ANS-ISP-007 (OBJ-BANKCISO-002, OBJ-SKEPTIC-010).")
r = ANS.get("ANS-ISP-007")
hist(r, "BL-021: reconciled with ANS-HR-006, which now also states attribution is self-declared and unauthenticated (OBJ-BANKCISO-002).")

r = ANS.get("ANS-LEG-003")
replace(r, "target_answer", "within 24 hours of determining that a security incident has affected or is reasonably likely to affect their data or services,",
        "within 24 hours of reasonable suspicion (not confirmation) that a security incident has affected their data or covered services, the single trigger also used in ANS-IR-004,")
hist(r, "BL-021: adopted the same 24-hour trigger as ANS-IR-004 (reasonable suspicion, not determination) (OBJ-BANKCISO-012).")
r = ANS.get("ANS-IR-004")
r["target_answer"] += (" This trigger is the single definition used in contract terms (ANS-LEG-003); regulatory clocks for "
    "bank (ANS-IR-005) and securities customers run in addition, and the shortest applicable deadline governs.")
hist(r, "BL-021: declared this the single notification trigger shared with ANS-LEG-003 (OBJ-BANKCISO-012).")

FALLBACK = (" If a bank customer has not designated a contact, Echelon notifies the bank's chief executive officer and "
            "chief information officer, or two individuals with comparable responsibilities, as the rule provides; bank "
            "tenant activation requires verified designated contacts.")
for aid in ("ANS-IR-005", "ANS-REG-007"):
    r = ANS.get(aid)
    r["target_answer"] += FALLBACK
    hist(r, "BL-021: added the CEO and CIO default-contact fallback under the 2021 bank service provider notification rule (OBJ-REGULATOR-003).")

r = ANS.get("ANS-PAY-008")
replace(r, "target_answer", "Until a deterministic release gate is accepted by the sponsor's auditor and board, release requires three distinct people (CNV-GOV-003).",
        "Release follows sponsor-set tiers by amount and risk: below a sponsor-set threshold, two distinct sponsor people (initiator and releaser) with independent post-release review within one business day; above it, three distinct people (CNV-GOV-003), or two people plus a deterministic release gate whose design Echelon management has approved and the sponsor's board has adopted, with the sponsor auditor's planned approach documented (a service auditor evaluates design and operating effectiveness only within an examination and does not accept a design in advance). A sponsor too small to staff its tier may accept the residual risk in writing with compensating detective controls (cross-role anomaly analytics and independent periodic review), as in ANS-RCN-004; one person may never both initiate and release.")
r["customer_statement"] = ("Planned: payment release is specified to follow sponsor-set tiers (two distinct people below "
    "a threshold with post-release review, three above, or two people plus a management-approved and sponsor-adopted "
    "deterministic gate), limit checks and a re-check against holds at transmission; payments outside the platform gate "
    "are prohibited by design. Not implemented.")
hist(r, "BL-021: replaced 'auditor acceptance' with management-approved design, sponsor board adoption and documented auditor planned approach; introduced release tiers reconciled with ANS-RCN-004 (OBJ-SOC2AUD-009, OBJ-DAFSPONSOR-011).")
r = ANS.get("ANS-RCN-004")
replace(r, "target_answer", "with the residual risk accepted in writing by the sponsor.",
        "with the residual risk accepted in writing by the sponsor. This acceptance never removes the requirement that payment release involves at least two distinct people (ANS-PAY-008 tiers).")
hist(r, "BL-021: reconciled small-sponsor residual risk acceptance with ANS-PAY-008 release tiers (OBJ-DAFSPONSOR-011).")
r = ANS.get("ANS-FCT-007")
replace(r, "target_answer", "ITGCs are effective and the auditor and board have accepted the design (CNV-GOV-003).",
        "ITGCs are effective, Echelon management has approved the design and the sponsor's board has adopted it, and the sponsor auditor's planned approach is documented (adapted from CNV-GOV-003). A service auditor does not accept or approve control design; it evaluates design and operating effectiveness only within an examination.")
r["customer_statement"] = ("Planned: AI and automation in Unbound are specified to propose only; deterministic gates count "
    "as an approver only after management approval of the design, sponsor board adoption and a documented auditor "
    "planned approach. Not implemented.")
hist(r, "BL-021: removed the auditor acceptance precondition in favor of management design with auditor review (OBJ-SOC2AUD-009).")

# SOC 2 versus SOC 1 timeline: one roadmap in ANS-AUD-001.
ROADMAP = (" Assurance roadmap (the single timeline that ANS-AUD-002, ANS-FCT-004 and ANS-RCN-005 refer to): (1) readiness "
    "work by a party other than the examining CPA firm; (2) at production go-live, a SOC 2 Type I and, where a sponsor "
    "relies on Unbound for financial reporting, a SOC 1 Type 1, each as of a date when controls are placed in "
    "operation; (3) first Type 2 periods of at least three months, sized so the SOC 1 Type 2 covers as much of the first "
    "hosted sponsor's fiscal year as possible; (4) where go-live is less than roughly six to nine months before that "
    "sponsor's fiscal year end, no SOC 1 Type 2 can exist in time and the stated fallback is that the sponsor's auditor "
    "tests Unbound directly or performs substantive procedures, with Echelon cooperating and bearing the reasonable "
    "incremental cost of direct testing by agreement. None of this has started; no auditor is engaged.")
r = ANS.get("ANS-AUD-001")
r["target_answer"] += ROADMAP
r["customer_statement"] = ("Echelon does not have a SOC 2 or SOC 1 report and has not engaged an auditor. It plans a SOC 2 "
    "Type I and, for sponsors relying on Unbound for financial reporting, a SOC 1 Type 1 at production go-live, followed "
    "by Type 2 periods; where timing does not allow a SOC 1 Type 2 before a sponsor's fiscal year end, the sponsor's "
    "auditor would need to test directly or substantively. We will not claim SOC 2 or SOC 1 compliance before an "
    "auditor issues a report.")
hist(r, "BL-021: made this the single SOC 2 and SOC 1 assurance roadmap with go-live Type I or Type 1 reports, sized Type 2 periods and a stated fallback (OBJ-SOC2AUD-001).")
for aid in ("ANS-AUD-002", "ANS-FCT-004", "ANS-RCN-005"):
    r = ANS.get(aid)
    r["target_answer"] += " Timing follows the assurance roadmap in ANS-AUD-001, including the fallback when a SOC 1 Type 2 cannot exist before a sponsor's fiscal year end."
    hist(r, "BL-021: pointed SOC 1 timing to the single roadmap in ANS-AUD-001 (OBJ-SOC2AUD-001, OBJ-DAFSPONSOR-005).")
r = ANS.get("ANS-FCT-004")
replace(r, "target_answer", "obtained before the first such sponsor's fiscal year end,",
        "obtained before the first such sponsor's fiscal year end where go-live timing allows (otherwise the ANS-AUD-001 fallback applies),")
r = ANS.get("ANS-RCN-005")
replace(r, "target_answer", "a SOC 1 Type 2 covering ledger posting, NAV, reconciliation, change and access before the first hosted sponsor's fiscal year end,",
        "a SOC 1 Type 2 covering ledger posting, NAV, reconciliation, change and access before the first hosted sponsor's fiscal year end where go-live timing allows (otherwise the ANS-AUD-001 fallback applies),")

# ---------------------------------------------------------------- checks and save
for r in ANS.all():
    if STATUS_RANK[r["status"]] > STATUS_RANK[before.get(r["id"], r["status"])]:
        sys.exit("status raised for " + r["id"])
    if "review" in r and r["id"] in before:
        pass
print("challenges swept", sweep)
print("files written", ANS.save(), CTL.save(), EVR.save())
