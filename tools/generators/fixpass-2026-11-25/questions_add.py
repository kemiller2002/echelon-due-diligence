"""BL-019 (privacy) and BL-022 (missing questions) for the 2026-11-25 fix pass.

Adds three verified source records, new canonical questions, answer units and evidence
requirements, and updates existing answer units. IDs continue from the next free number in
each category file. Run once from the repository root.
"""
import json
import sys

sys.path.insert(0, "tools/generators/fixpass-2026-11-25")
from lib import Store, hist, replace, add_list, created  # noqa: E402

SRC = Store("sources")
Q = Store("questions")
ANS = Store("answers")
EVR = Store("evidence-requirements")
if "SRC-IN-CDPA" in SRC:
    sys.exit("already applied")

# ---------------------------------------------------------------- sources (verified 2026-11-25)
SRC.add("privacy", {
    "id": "SRC-IN-CDPA", "title": "Indiana Consumer Data Protection Act (IC 24-15, enacted by 2023 Senate Enrolled Act 5)",
    "issuer": "Indiana General Assembly", "type": "statute", "authority": "binding-law",
    "version": "IC 24-15 as added by SEA 5 (2023), signed 2023-05-01", "publication_date": "2023-05-01",
    "effective_date": "2026-01-01", "url": "https://codes.findlaw.com/in/title-24-trade-regulation/in-code-sect-24-15-1-1/",
    "jurisdictions": ["US-state:IN"], "industries": ["cross-industry"],
    "applicability": "Applies to a person doing business in Indiana or targeting Indiana residents that, in a calendar year, controls or processes personal data of at least 100,000 Indiana consumers, or at least 25,000 and derives more than 50 percent of gross revenue from the sale of personal data (IC 24-15-1-1(a)). Exempts nonprofit organizations, GLBA financial institutions and affiliates, and data subject to GLBA Title V (IC 24-15-1-1(b)). Echelon Foundry, LLC is an Indiana LLC; whether it meets a threshold as a processor, and how processor duties apply when its nonprofit customers are exempt, needs counsel review. Enforcement is by the Indiana Attorney General; no private right of action.",
    "license": "Public law text; cite the official Indiana Code.",
    "limitations": "Verified from a secondary code publisher (FindLaw) and practitioner summaries, not from the official iga.in.gov text; confirm exact wording before quoting.",
    "status": "current", "related_sources": ["SRC-US-STATE-PRIVACY-LAWS", "SRC-GLBA"],
    "notes": "Added in the 2026-11-25 fix pass (BL-019, OBJ-PRIVACY-002).",
    "verification": {"verified": True, "verified_on": "2026-11-25",
                     "method": "Fetched FindLaw IC 24-15-1-1 (effective 2026-01-01; thresholds and exemptions) and web search of enrolled SEA 5 (effective January 1, 2026) and Indiana Attorney General consumer bill of rights",
                     "evidence_url": "https://codes.findlaw.com/in/title-24-trade-regulation/in-code-sect-24-15-1-1/"}})
SRC.add("financial-services", {
    "id": "SRC-OCC-12CFR9", "title": "Fiduciary Activities of National Banks (12 CFR Part 9)",
    "issuer": "Office of the Comptroller of the Currency", "type": "regulation", "authority": "binding-regulation",
    "version": "12 CFR 9.1 to 9.20 and interpretations 9.100 to 9.101 as published in the CFR", "publication_date": "unknown",
    "url": "https://www.law.cornell.edu/cfr/text/12/part-9", "jurisdictions": ["US-federal"], "industries": ["us-banking"],
    "applicability": "Binds national banks exercising fiduciary powers, including a national bank acting as trustee of a charitable gift fund; covers policies and procedures (9.5), review of fiduciary accounts (9.6), recordkeeping (9.8), audit of fiduciary activities (9.9) and custody (9.13). Does not bind Echelon directly; flows to Echelon through the trustee bank's oversight of a vendor that administers fiduciary accounts. State-chartered trust companies are governed by analogous state law, not inventoried here.",
    "license": "U.S. federal government work; not subject to U.S. copyright (17 U.S.C. 105).",
    "limitations": "Section list verified from a secondary publisher (Cornell LII); eCFR redirected during verification. Whether a given DAF sponsor's trustee is a national bank must be checked per customer.",
    "status": "current", "related_sources": ["SRC-BSCA", "SRC-INTERAGENCY-TPRM-2023"],
    "notes": "Added in the 2026-11-25 fix pass (BL-022, OBJ-REGULATOR-002).",
    "verification": {"verified": True, "verified_on": "2026-11-25", "method": "Fetched Cornell LII 12 CFR Part 9 table of sections",
                     "evidence_url": "https://www.law.cornell.edu/cfr/text/12/part-9"}})
SRC.add("supplementary", {
    "id": "SRC-FTC-ACT-5", "title": "Federal Trade Commission Act section 5 (15 U.S.C. 45), unfair or deceptive acts or practices",
    "issuer": "United States Congress", "type": "statute", "authority": "binding-law",
    "version": "15 U.S.C. 45; latest amendment credit Pub. L. 112-203 (2012)", "publication_date": "unknown",
    "url": "https://www.law.cornell.edu/uscode/text/15/45", "jurisdictions": ["US-federal"], "industries": ["cross-industry"],
    "applicability": "Declares unfair or deceptive acts or practices in or affecting commerce unlawful (45(a)(1)). Applies to Echelon as a for-profit company for its own representations, including donor-facing pages it operates or generates. FTC jurisdiction over nonprofit sponsors themselves is limited; state attorneys general police charitable solicitation separately.",
    "license": "U.S. Code; public domain.", "limitations": "Applicability to specific donor-facing content needs counsel review.",
    "status": "current", "related_sources": ["SRC-STATE-CHARITABLE-SOLICITATION"],
    "notes": "Added in the 2026-11-25 fix pass (BL-022, OBJ-REGULATOR-013).",
    "verification": {"verified": True, "verified_on": "2026-11-25", "method": "Fetched Cornell LII 15 U.S.C. 45",
                     "evidence_url": "https://www.law.cornell.edu/uscode/text/15/45"}})

COST = "order-of-magnitude judgment, not sourced"


def evr(cat, title, description, independence="first-party", producer="not yet assigned", mechanism="event-driven-automated",
        freshness="per-event", disclosure="nda"):
    eid = EVR.next_id("EVR", cat, 3)
    EVR.add(cat, {"id": eid, "title": title, "description": description, "producer": producer, "mechanism": mechanism,
                  "freshness": freshness, "independence": independence, "disclosure_classification": disclosure,
                  "status": "proposed-target-state", "notes": "Fix pass 2026-11-25 (fix-pass-agent): created."})
    return eid


def answer(cat, title, status, rationale, target, current, intended, provable, statement, kind, evrs=(), owner="Not assigned (proposed: Echelon managing member)",
           risks=(), oq=(), disclosure="authenticated-prospect", impl="low", rec="low", independence="none", controls=()):
    aid = ANS.next_id("ANS", cat, 3)
    ANS.add(cat, {"id": aid, "title": title, "status": status, "status_rationale": rationale, "target_answer": target,
                  "current_practice": current, "intended_practice": intended, "provable": provable,
                  "customer_statement": statement, "customer_statement_kind": kind, "assurance_independence": independence,
                  "controls": list(controls), "evidence_requirements": list(evrs), "evidence_mechanism": "not-defined",
                  "automation_potential": "partial", "disclosure_classification": disclosure, "implementation_cost": impl,
                  "recurring_cost": rec, "cost_basis": COST, "owner": owner, "residual_risks": list(risks),
                  "open_questions": list(oq), "history": created()})
    return aid


def question(cat, text, sub, concern, risk, refs, aid, industries, juris=("US-federal",), products=("unbound",), cls="customer-preference",
             importance="high", alts=(), authority=None, evrs=(), disclosure="authenticated-prospect", scope=None):
    qid = Q.next_id("DDQ", cat, 4)
    rec = {"id": qid, "question": text, "alternatives": list(alts), "category": cat, "subcategory": sub,
           "business_concern": concern, "risk_addressed": risk,
           "source_refs": [dict(zip(("source_id", "relation", "basis", "locator"), r)) if len(r) == 4 else
                           dict(zip(("source_id", "relation", "basis"), r)) for r in refs],
           "industries": list(industries), "jurisdictions": list(juris), "products": list(products),
           "requirement_classification": cls, "customer_importance": importance, "answer_unit": aid,
           "evidence_requirements": list(evrs), "disclosure_classification": disclosure, "open_questions": [],
           "history": created()}
    if authority:
        rec["regulatory_authority"] = authority
    if scope:
        rec["answer_scope_note"] = scope
    for r in rec["source_refs"]:
        if r["source_id"] not in SRC:
            sys.exit("unknown source " + r["source_id"])
    Q.add(cat, rec)
    return qid


new_q, new_a = [], []
FIN = ("financial-services", "banking", "donor-advised-funds")
DAFI = ("donor-advised-funds", "nonprofit")

# ================================================================ BL-019 privacy
e1 = evr("PRV", "Privacy documentation set: DPA template, privacy notices and record of processing",
         "Versioned, counsel-reviewed DPA template (CCPA service-provider and state processor terms), platform privacy notice, Echelon corporate privacy notice and a record of processing for Unbound's designed data flows, each with owner, approval date and reviewer.",
         producer="not yet assigned (intended: Praxis-governed documents)", disclosure="authenticated-prospect")
e1c = evr("PRV", "Outside counsel review of the DPA template and privacy notices",
          "Dated letter or marked review from outside privacy counsel on the DPA template and notices.", independence="independent-third-party",
          producer="Outside privacy counsel (not engaged)", mechanism="external-attestation", freshness="P1Y")
a = answer("PRV", "Privacy documentation set: DPA template, privacy notices and record of processing", "proposed-target-state",
    "No DPA template, platform privacy notice, corporate privacy notice or record of processing exists as of 2026-11-25 (ANS-PRV-001 is unknown; ANS-PRV-004 and ANS-LEG-005 are planned). Counsel is not engaged.",
    "Before any sales conversation involving donor data, Echelon can hand a prospect: a counsel-reviewed DPA template carrying CCPA service-provider terms and the processor terms of state laws that reach its customers; a platform privacy notice for donors, advisors and charity contacts coordinated with each sponsor's notice; a corporate privacy notice for Echelon's own prospects and website visitors; and a record of processing for Unbound's designed data flows generated from the schema catalog. Each is versioned, dated, owned by a named person and marked draft and first-party until counsel review is recorded.",
    "None of the documents exists. No privacy owner is named.",
    "Draft the four documents, have outside counsel review them, record the review as " + e1c + ", and link them from ANS-PRV-001, ANS-PRV-004 and ANS-LEG-005.",
    "Nothing.",
    "Echelon does not yet have a DPA template, privacy notice or record of processing. It plans to produce counsel-reviewed versions before handling any donor data and will share drafts marked as drafts.",
    "not-available", evrs=(e1, e1c), risks=("A DPA drafted without counsel may promise processor duties that conflict with retention or append-only record design.",),
    oq=("Who will own the privacy documents (managing member, fractional privacy officer or counsel)?",), impl="medium")
new_a.append(a)
for text, sub, alts in [
    ("Can you provide your data processing agreement template today, has outside counsel reviewed it, and which state processor terms does it include?", "dpa-template",
     ["Send your standard DPA for our privacy office to review before we proceed.", "Does your DPA include CCPA service-provider terms and Colorado and Oregon processor terms?"]),
    ("Does Echelon publish a corporate privacy notice covering its own prospects, website visitors and business contacts, separate from the platform notice for donors?", "privacy-notice",
     ["Where is your company privacy policy and when was it last approved?"]),
    ("Can you share a draft record of processing for the platform's designed data flows, even before production?", "record-of-processing",
     ["Provide a data map of the personal data the platform will process, by purpose, recipient and retention."])]:
    new_q.append(question("PRV", text, sub, "A privacy office cannot approve a vendor that cannot produce the documents its review depends on.",
        "Privacy commitments are accepted without the documents that make them enforceable.",
        [("SRC-CCPA-CPRA", "informed-by", "reasonably-inferred"), ("SRC-NIST-PRIVACY-FW", "maps-to", "reasonably-inferred"),
         ("SRC-AICPA-PRIVACY-CRITERIA", "maps-to", "reasonably-inferred")], a, ("all",), juris=("US-states",), products=("all-echelon-products",),
        cls="contractual-common", alts=alts, evrs=(e1,)))
r = ANS.get("ANS-PRV-004")
r["current_practice"] = (r["current_practice"] + " No DPA template exists as of 2026-11-25; see " + a + ".").strip()
hist(r, "BL-019: recorded that no DPA template exists and linked the privacy documentation set " + a + " (OBJ-PRIVACY-001).")
r = ANS.get("ANS-PRV-001")
r["current_practice"] += " Specifically, no platform or corporate privacy notice and no record of processing exist; see " + a + "."
hist(r, "BL-019: linked the privacy documentation set " + a + " (OBJ-PRIVACY-001).")

e2 = evr("PRV", "Privacy law applicability register with counsel sign-off",
         "One row per law: Echelon's role, trigger facts and thresholds, exemptions (nonprofit, GLBA entity and data), customer populations affected, counsel name and date, and re-evaluation triggers.",
         independence="independent-third-party", producer="Outside privacy counsel (not engaged); register maintained by Echelon",
         mechanism="periodic-manual", freshness="P1Y")
a2 = answer("PRV", "Privacy law applicability register, including Indiana's Consumer Data Protection Act", "proposed-target-state",
    "No applicability register exists. GLBA and Safeguards Rule status, state comprehensive laws that cover nonprofit controllers, GLBA exemptions in state laws and Indiana's law (Echelon is an Indiana LLC) are open questions in ANS-PRV-002, ANS-PRV-003 and ANS-REG-001. Counsel is not engaged.",
    "Echelon maintains a privacy applicability register, signed by outside counsel and re-reviewed annually and on trigger events, with one row per law: GLBA Title V and the FTC Safeguards Rule (including whether Echelon is itself a financial institution as a payment file preparer), Regulation S-P service provider duties, each state comprehensive privacy law (noting which reach nonprofit controllers, for example Colorado and Oregon, and which exempt nonprofits or GLBA data), state breach laws, state donor privacy statutes, and the Indiana Consumer Data Protection Act (IC 24-15, effective 2026-01-01). For Indiana the register records that the law applies to controllers and processors of personal data of at least 100,000 Indiana consumers a year (or 25,000 with more than half of revenue from sale of data), that nonprofits and GLBA financial institutions and GLBA data are exempt, and Echelon's resulting position as an Indiana company processing for mostly exempt nonprofit sponsors. Until counsel signs a row, answers say 'applicability not determined'.",
    "No register exists. Applicability questions are recorded as open questions across PRV, REG and RET answer units.",
    "Engage privacy counsel; build the register as versioned data; make answers that depend on applicability cite the register row.",
    "Nothing.",
    "Echelon has not yet determined which privacy laws apply to it, including Indiana's Consumer Data Protection Act, which took effect on 2026-01-01. It plans a counsel-reviewed applicability register and will say 'not determined' until then.",
    "not-available", evrs=(e2,), risks=("Applicability differs by customer type (nonprofit, bank-affiliated, broker-affiliated), so one answer per law may not fit every customer.",),
    oq=("Does Echelon, as processor for exempt nonprofit sponsors, have any direct duty under IC 24-15?", "Is Echelon a financial institution under the FTC Safeguards Rule because it prepares payment files?"), impl="medium")
new_a.append(a2)
new_q.append(question("PRV", "Do you maintain a register of which privacy laws apply to you and to the data you process for us, reviewed by counsel, and can we see the rows that concern our organization?", "applicability-register",
    "Customers need to know which legal duties the vendor accepts rather than a generic compliance claim.",
    "The vendor implies compliance with laws it has never analyzed, or ignores laws that do apply.",
    [("SRC-US-STATE-PRIVACY-LAWS", "informed-by", "reasonably-inferred"), ("SRC-GLBA", "informed-by", "reasonably-inferred"),
     ("SRC-FTC-SAFEGUARDS-RULE", "informed-by", "reasonably-inferred"), ("SRC-CO-PRIVACY-ACT", "informed-by", "reasonably-inferred"),
     ("SRC-OR-CPA", "informed-by", "reasonably-inferred")], a2, FIN + ("nonprofit",), juris=("US-federal", "US-states"),
    products=("all-echelon-products",), cls="contractual-common", alts=["Which state privacy laws do you consider applicable, and why?"], evrs=(e2,)))
new_q.append(question("PRV", "Echelon is an Indiana company. Have you determined whether the Indiana Consumer Data Protection Act applies to you as a controller or processor, given its thresholds and its nonprofit and GLBA exemptions?", "indiana-cdpa",
    "A vendor's home-state privacy law is the most likely to apply to its own operations.",
    "Obligations under the vendor's home-state law are missed.",
    [("SRC-IN-CDPA", "maps-to", "directly-documented", "IC 24-15-1-1")], a2, ("all",), juris=("US-state:IN",), products=("all-echelon-products",),
    cls="legal-regulatory", importance="medium", authority="Indiana Attorney General"))

e3 = evr("PRV", "Legal process log and transparency report",
         "Log of every government or third-party demand for customer data served on Echelon: date, issuing authority, legal basis, scope requested, customer notified or reason not, challenge made, data disclosed; periodic aggregate transparency report.",
         producer="not yet assigned (intended: legal process register)", mechanism="periodic-manual", freshness="P1Y", disclosure="public")
a3 = answer("PRV", "Government and third-party legal process directed at Echelon for customer data", "proposed-target-state",
    "No policy exists for subpoenas, warrants, civil investigative demands or other legal process served on Echelon for sponsor or donor data. Donor anonymity for sensitive giving makes this material (OBJ-PRIVACY-008).",
    "Echelon redirects any demand for a customer's data to the customer as controller wherever the law allows; notifies the customer before disclosure unless legally prohibited, and as soon as the prohibition lapses; challenges demands that are overbroad or lack a valid legal basis; discloses only the minimum data the order requires; never gives any authority standing or bulk access; logs every demand; and publishes a periodic transparency report with aggregate counts. Donor identity behind an anonymity election is treated as sensitive, and counsel reviews state donor privacy statutes as part of the applicability register.",
    "No policy, log or counsel relationship exists. No demand is known to have been received.",
    "Adopt a legal process policy reviewed by counsel; add contract terms; publish a transparency report once in production.",
    "Nothing.",
    "Echelon has not yet adopted a policy for legal demands for customer data. Its planned approach is to redirect demands to the customer, notify the customer unless prohibited, challenge overbroad demands and disclose only the minimum required.",
    "planned", evrs=(e3,), risks=("A small company may lack funds to challenge a demand.", "Gag orders can prevent notice indefinitely."))
new_a.append(a3)
for text, sub in [
    ("If a government agency or private litigant serves Echelon with a subpoena, warrant or other demand for our donors' data, will you redirect it to us, notify us before disclosing, and challenge overbroad demands?", "legal-process"),
    ("Do you publish a transparency report on government and third-party demands for customer data, and how do you protect donor identities behind anonymity elections from such demands?", "transparency-report")]:
    new_q.append(question("PRV", text, sub, "Sponsors are responsible to donors for confidentiality, including against legal process aimed at their vendor.",
        "Donor identities, including anonymous donors, are disclosed through process served on the vendor without the sponsor's knowledge.",
        [("SRC-NIST-PRIVACY-FW", "informed-by", "reasonably-inferred"), ("SRC-CSA-CCM-V4", "maps-to", "reasonably-inferred")], a3, DAFI + ("financial-services",),
        juris=("US-federal", "US-states"), cls="contractual-common", evrs=(e3,)))

r = ANS.get("ANS-DON-003")
r["target_answer"] += (" Anonymous grants never carry a fund name that contains a personal name: the sponsor assigns a neutral "
    "identifier for anonymous grants, and the platform blocks an anonymous grant whose fund name matches a donor or "
    "participant surname. Every outbound channel is tested for leakage, including bank remittance data (check memo lines "
    "and ACH addenda produced by the sponsor's bank), charity-side grant platforms, partner views, sponsor annual reports "
    "and AI-drafted grant letters, and AI drafting may not include donor identity on anonymous grants.")
r["residual_risks"] = (r.get("residual_risks") or []) + [
    "The fund name itself (for example 'The Smith Family Fund') discloses identity even under a fund-name-only recognition election.",
    "Payment remittance text is produced by the sponsor's bank from fields Unbound supplies; a leak there is outside the recognition election unless those fields are controlled.",
    "Small populations of grants (amount, date, grantee) can re-identify an anonymous donor."]
hist(r, "BL-019: added the fund-name anonymity rule, channel testing including bank remittance and AI drafting limits, and residual risks (OBJ-PRIVACY-007).")
new_q.append(question("DON", "When a donor recommends an anonymous grant, can the fund name still identify them (for example a family-name fund), and how do you prevent identity leaking through fund names, check memos, ACH remittance text or AI-drafted grant letters?", "anonymity-fund-name",
    "Anonymity elections must survive every channel that carries grant information to the charity.",
    "Donor identity leaks through the fund name or payment remittance data despite an anonymity election.",
    [("SRC-NIST-PRIVACY-FW", "informed-by", "reasonably-inferred")], "ANS-DON-003", DAFI, cls="customer-preference",
    alts=["Does an anonymous grant ever show the fund name to the charity?"]))

e4 = evr("RET", "Retention precedence rule set with counsel approval and key-destruction block evidence",
         "Versioned rule set mapping each record class to its retention obligations and the precedence (legal hold, then regulatory or tax retention, then deletion request), counsel approval record, and per-event evidence that key destruction was blocked for classes under retention or hold.",
         producer="not yet assigned (intended: Unbound retention service; not built)")
a4 = answer("RET", "Precedence between deletion requests, regulatory retention and legal hold", "proposed-target-state",
    "The knowledge base promises both crypto-shredding deletion (ANS-RET-005, ANS-PRV-005) and preservation for SEC Rule 17a-4, IRS substantiation, seven-year financial records and legal holds (ANS-RET-002, ANS-RET-006), with precedence left to counsel (OBJ-PRIVACY-005). No rule set exists.",
    "A versioned precedence rule set decides every conflict the same way: (1) an active legal hold wins over everything; (2) a regulatory or tax retention duty that applies to the record class (for example SEC Rule 17a-4 for a broker-dealer sponsor's required records, IRS substantiation and Form 990 support, sponsor financial record minimums, OFAC recordkeeping) wins over a deletion request for the retention period; (3) otherwise the deletion request is honored. Each record class maps to its duties. Key destruction is blocked by the platform for any class under hold or retention, so crypto-shredding cannot destroy a required record. The deletion certificate lists every retained class with its legal basis and the date it becomes deletable, and the deferred deletion runs automatically when the duty expires. The sponsor, as controller, decides contested cases; Echelon does not. No erasure commitment is offered until counsel approves the rule set.",
    "No rule set, record class mapping or counsel review exists.",
    "Draft the rule set and record class mapping, obtain counsel approval, implement the key-destruction block, and change ANS-RET-005 and ANS-PRV-005 to cite it.",
    "Nothing.",
    "Echelon has not yet defined how it resolves conflicts between deletion requests, regulatory retention and legal holds. Its planned rule is that legal holds come first, then legal retention duties, then deletion, with deletion certificates naming what was retained and why; it will not offer erasure commitments until counsel approves the rules.",
    "planned", evrs=(e4,), risks=("Retention duties differ by sponsor type, so the mapping is per tenant configuration, not one platform rule.",),
    oq=("Does crypto-shredding satisfy deletion duties under the state laws in the applicability register?",), impl="medium")
new_a.append(a4)
for text, sub in [
    ("When a donor's deletion request conflicts with SEC Rule 17a-4, IRS substantiation or seven-year record duties, or with a legal hold, which wins, who decides, and how is the decision evidenced?", "retention-precedence"),
    ("Can cryptographic erasure ever destroy a record that is under legal hold or a regulatory retention period, and what prevents it?", "erasure-block")]:
    new_q.append(question("RET", text, sub, "Deletion and retention duties both bind the sponsor; the platform must resolve conflicts predictably.",
        "A required record is destroyed by a deletion, or a deletion is promised that the law forbids.",
        [("SRC-SEC-17A-4", "informed-by", "reasonably-inferred"), ("SRC-IRC-6001", "informed-by", "reasonably-inferred"),
         ("SRC-CCPA-CPRA", "informed-by", "reasonably-inferred")], a4, FIN + ("nonprofit",), juris=("US-federal", "US-states"),
        cls="contractual-common", evrs=(e4,)))
for aid in ("ANS-RET-005", "ANS-PRV-005", "ANS-RET-002"):
    r = ANS.get(aid)
    r["target_answer"] += " Conflicts with retention duties and legal holds are resolved by the precedence rule set in " + a4 + "."
    hist(r, "BL-019: linked the retention-conflict precedence rule " + a4 + " (OBJ-PRIVACY-005).")

# ================================================================ BL-022 missing questions
a = answer("GOV", "Operating history, production track record, customer count and references", "proposed-target-state",
    "Unbound has no production deployment and no customers (architecture/ECHELON-CURRENT-STATE-BRIEF.md). Echelon has no customer references.",
    "Echelon states its production tenure, live customer count by segment and size, and provides references from comparable customers. Before that exists, it offers design-partner arrangements with defined scope, the incumbent kept as system of record, exit rights without penalty if milestones slip, and references from design partners once they can give them.",
    "No production history, customers or references exist.",
    "Offer design-partner terms; collect references once design partners agree.",
    "Nothing beyond the absence itself.",
    "Echelon has no production customers, no operating history for Unbound and no customer references. It can offer a design-partner arrangement in which the sponsor keeps its current administrator as system of record and has exit rights.",
    "not-available", risks=("A design partner bears adoption risk that references would normally reduce.",))
new_a.append(a)
for text, sub, alts in [
    ("How long has the service operated in production, and how many customers of our type and size use it today?", "operating-history",
     ["Provide your live customer count by segment.", "When did the platform first go live?"]),
    ("Can you provide references from current customers comparable to us, and if you have none, what pilot or design-partner terms with exit rights do you offer?", "references",
     ["Provide three client references, preferably DAF sponsors.", "What protection do we have if your delivery slips during a pilot?"])]:
    new_q.append(question("GOV", text, sub, "Business experience is the first due diligence factor for a vendor of a critical activity.",
        "A sponsor selects an unproven vendor without knowing it is unproven.",
        [("SRC-INTERAGENCY-TPRM-2023", "informed-by", "reasonably-inferred"), ("SRC-OCC-BULLETIN-2023-17", "informed-by", "reasonably-inferred")],
        a, FIN + ("nonprofit",), cls="supervisory-guidance", importance="critical", alts=alts, products=("all-echelon-products",)))

a = answer("GOV", "Implementation plan, timeline and sponsor effort", "unknown",
    "No implementation methodology, timeline template or estimate of sponsor staff effort exists.",
    "Each sponsor receives a written implementation plan: phases, timeline, go-live criteria, the sponsor staff roles and hours needed (including declaring every sponsor policy that Unbound pins and versions, ANS-DAF-006), training, data conversion and parallel run (see the conversion answer), and the decision points at which either party can stop.",
    "Unknown; no methodology exists.", "Write an implementation methodology with design partners and measure actual effort.", "Nothing.",
    "Echelon has not yet defined an implementation methodology, timeline or estimate of sponsor effort.", "not-available")
new_a.append(a)
new_q.append(question("GOV", "What is your implementation plan for an organization like ours: timeline, go-live criteria, our staff effort by role, policy configuration workload and training?", "implementation-plan",
    "Implementation effort is a key budget and decision input for a sponsor's CFO and board.", "The sponsor underestimates the effort and timeline of switching platforms.",
    [("SRC-INTERAGENCY-TPRM-2023", "informed-by", "reasonably-inferred")], a, DAFI + ("financial-services",), importance="high",
    alts=["How many hours of our staff time will implementation require?"]))

e5 = evr("DAF", "Conversion reconciliation report and parallel-run sign-off",
         "Per conversion: record counts and balances by fund reconciled to the incumbent's records and the audited financial statements within agreed tolerances, exceptions and resolutions, in-flight grant treatment at cutover, parallel-run results through at least one close, and sponsor sign-off.",
         producer="not yet assigned (intended: Unbound conversion tooling; not built)")
a = answer("DAF", "Conversion from the incumbent administrator and parallel run", "proposed-target-state",
    "Unbound has requirements for offboarding but none located for inbound conversion from an incumbent administrator; no conversion tooling or experience exists.",
    "Conversion extracts funds, contributions with gift dates and cost basis, grants and their states, recurring grants, succession plans, advisor privileges, documents and audit history from the incumbent; converted balances are reconciled fund by fund to the incumbent's records and the audited financial statements within agreed tolerances; in-flight grants at cutover follow a documented treatment; the platform runs in parallel with the incumbent through at least one month-end close (and ideally a year-end) before cutover; a rollback plan exists until sign-off; donors are told what changes and when.",
    "Not established.", "Design conversion tooling and a parallel-run protocol with the first design partner.", "Nothing.",
    "Echelon has no conversion tooling or conversion experience. It plans fund-by-fund reconciliation to the incumbent's records and a parallel run through at least one close before any cutover.",
    "planned", evrs=(e5,), risks=("Incumbent export formats and cooperation are outside Echelon's control.", "Historical cost basis and gift-date data in the incumbent may be incomplete."), impl="high", rec="medium")
new_a.append(a)
for text, sub in [
    ("How will you convert our historical funds, contributions, grants, succession plans and documents from our current administrator, and how are converted balances reconciled to our records and audited financial statements?", "conversion"),
    ("Will the platform run in parallel with our current administrator through at least one close before cutover, and what is the rollback plan and treatment of in-flight grants?", "parallel-run")]:
    new_q.append(question("DAF", text, sub, "Conversion is the largest project risk of switching administrators.",
        "Balances, gift records or in-flight grants are lost or misstated at cutover.",
        [("SRC-AICPA-NFP-AAG", "informed-by", "reasonably-inferred"), ("SRC-FASB-ASC-958", "informed-by", "reasonably-inferred")],
        a, DAFI, importance="critical", evrs=(e5,)))

a = answer("FEE", "Echelon's pricing, commercial terms and total cost to the sponsor", "unknown",
    "Echelon's revenue model and pricing are not established (ANS-FEE-006).",
    "Echelon publishes to prospects its pricing model, implementation fees, minimums, price escalators, the cost of dedicated isolation profiles and customer-managed keys, and an estimate of the sponsor-side staffing the design requires (release tiers, reviews, policy administration), so a sponsor can compare total cost of ownership with its incumbent.",
    "Unknown; pricing is not decided.", "Decide pricing; publish a total cost of ownership worksheet.", "Nothing.",
    "Echelon has not yet set pricing or commercial terms.", "not-available", disclosure="authenticated-prospect")
new_a.append(a)
for text, sub in [
    ("What will Echelon charge us: pricing model, implementation fees, minimums, escalators, and the cost of dedicated isolation or customer-managed keys?", "vendor-pricing"),
    ("What is our total cost of ownership, including the internal staffing your control design requires of us (for example payment release and review roles)?", "total-cost")]:
    new_q.append(question("FEE", text, sub, "A CFO cannot compare a vendor with an incumbent without its price and the internal cost it imposes.",
        "The sponsor commits to a platform whose total cost is unknown.", [("SRC-INTERAGENCY-TPRM-2023", "informed-by", "reasonably-inferred")],
        a, DAFI + ("financial-services",), importance="high"))

a = answer("LEG", "Allocation of excise tax and correction costs caused by platform defects (sections 4966, 4967, 4958)", "proposed-target-state",
    "ANS-DAF-009 promises deterministic gates against taxable distributions, prohibited benefits and excess benefit transactions, but no answer addresses who bears excise tax and correction costs if a platform defect lets one through. Liability under sections 4966, 4967 and 4958 falls on the sponsor, fund managers, donors, advisors or disqualified persons, never on Echelon by law. No contract terms or insurance exist.",
    "Echelon proposes a specific indemnity, outside the general liability cap, for excise taxes, correction costs and reasonable donor remediation that result from an error in its deterministic compliance gates, subject to the sponsor having adopted and followed the configured policy, sized to and funded by technology E&O insurance that Echelon actually carries, and reviewed by counsel. Echelon states plainly that the statutory liability remains with the sponsor and its managers and that the indemnity is contractual reimbursement only.",
    "No position, contract terms or insurance exist.", "Have counsel draft the indemnity; obtain E&O coverage before offering it; link to ANS-LEG-004.", "Nothing.",
    "Echelon has not yet offered terms on excise tax caused by platform errors. The tax liability itself stays with the sponsor and its fund managers by law; Echelon plans to propose a counsel-reviewed indemnity backed by insurance it actually holds.",
    "planned", risks=("An indemnity larger than insurance is not fundable by a small company.", "Some excise taxes may be uninsurable."), impl="medium")
new_a.append(a)
new_q.append(question("LEG", "If a platform defect lets through a taxable distribution, prohibited benefit or excess benefit transaction, who bears the resulting excise taxes under sections 4966, 4967 and 4958, correction costs and donor remediation, and is that outside your liability cap?", "excise-tax-allocation",
    "Statutory excise tax falls on the sponsor and its managers even when the vendor's software caused the error.",
    "The sponsor bears taxes and correction costs caused by the vendor's defect with no recovery.",
    [("SRC-IRC-4966", "informed-by", "directly-documented"), ("SRC-IRC-4967", "informed-by", "directly-documented"),
     ("SRC-IRC-4958", "informed-by", "directly-documented"), ("SRC-IRS-FORM-4720", "informed-by", "reasonably-inferred")],
    a, DAFI, cls="contractual-common", importance="high", authority="IRS"))
r = ANS.get("ANS-LEG-004")
r["target_answer"] += " Excise tax and correction costs caused by errors in deterministic compliance gates are addressed by a specific indemnity in " + a + "."
hist(r, "BL-022: linked excise tax allocation " + a + " (OBJ-DAFSPONSOR-004).")

a = answer("MON", "Threat intelligence sharing and use", "proposed-target-state",
    "No threat intelligence sharing membership or feed is in use; no detection program exists (ANS-MON-004 is unknown).",
    "Echelon receives sector threat intelligence (for example through FS-ISAC membership, a vendor feed or CISA advisories), records how each relevant item changed detections, dependency decisions or customer guidance, and shares indicators from its own incidents with customers and sharing partners where permitted.",
    "None.", "Choose a feed proportionate to size (CISA and vendor advisories first; sector membership when eligible and affordable).", "Nothing.",
    "Echelon does not participate in a threat intelligence sharing organization today. It plans to consume sector and government advisories and to record how they change its detections.",
    "planned")
new_a.append(a)
new_q.append(question("MON", "Do you participate in financial-sector threat intelligence sharing (for example FS-ISAC) or use an equivalent feed, and how does intelligence change your detections?", "threat-intelligence",
    "Bank CISOs expect critical vendors to receive and act on sector threat intelligence.", "The vendor misses threats already known to the sector.",
    [("SRC-NIST-CSF-2.0", "maps-to", "reasonably-inferred", "ID.RA-02"), ("SRC-Q-FSISAC-GENAI-VENDOR-GUIDE", "informed-by", "reasonably-inferred")],
    a, ("financial-services", "banking"), juris=("global",), products=("all-echelon-products",), importance="medium"))

a = answer("AIA", "AI processing of customers' confidential questionnaires, contracts and documents", "unknown",
    "Echelon drafts questionnaire answers with AI (ANS-AIA-007). Which AI tools have processed prospect or customer material, and under which provider retention and training terms, is not recorded. AQR-SEC-003 (architecture/AUTOMATED-QUESTIONNAIRE-RESPONSE-REQUIREMENTS.md) is a requirement only.",
    "Before a customer's questionnaire, security addendum, contract or policy is processed by an AI tool, Echelon tells the customer which provider processes it, uses only a route with no training and no retention beyond processing under terms compatible with the customer's NDA, lists the provider as a recipient of the customer's confidential information, and otherwise processes the document manually or deterministically.",
    "Unknown; no record of which tools processed which material exists.", "Record AI tool use for customer material; adopt AQR-SEC-003; give notice.", "Nothing.",
    "Echelon uses AI tools to draft questionnaire answers but has not yet recorded which providers process customer documents or adopted a notice and consent practice. It plans to name the provider and use no-training, no-retention routes, or process documents without AI where a customer requires.",
    "not-available", risks=("Customer NDAs may prohibit disclosure to a model provider without consent.",))
new_a.append(a)
new_q.append(question("AIA", "Do you use AI tools to process the questionnaires, security addenda, contracts or policies we send you, which providers receive them, and under what retention and training terms?", "customer-document-ai-processing",
    "Customer questionnaires and policies are confidential under NDA; a model provider is an additional recipient.",
    "The customer's confidential documents reach a model provider without notice or adequate terms.",
    [("SRC-Q-FSISAC-GENAI-VENDOR-GUIDE", "informed-by", "reasonably-inferred"), ("SRC-NIST-AI-600-1", "informed-by", "reasonably-inferred")],
    a, ("all",), juris=("global",), products=("all-echelon-products",), cls="contractual-common", importance="high"))

e6 = evr("REG", "Counsel memorandum on support for trustee banks' fiduciary oversight under 12 CFR Part 9",
         "Outside counsel's analysis of what a national bank trustee (and a state trust company) must obtain from a vendor administering fiduciary accounts, mapped to Unbound records, reviews and audit support.",
         independence="independent-third-party", producer="Outside banking counsel (not engaged)", mechanism="external-attestation", freshness="P1Y")
a = answer("REG", "Support for bank-trustee sponsors' fiduciary duties (OCC 12 CFR Part 9 and state trust analogues)", "requires-external-validation",
    "A national bank acting as trustee of a charitable gift fund exercises fiduciary powers examined by the OCC under 12 CFR Part 9 (policies, account review, recordkeeping, fiduciary audit, custody). No answer previously addressed this. Counsel has not reviewed what Unbound must support.",
    "For sponsors whose trustee is a national bank or state trust company, Unbound supports the trustee's fiduciary oversight: records of each fiduciary account kept as the trustee's records and producible to the trustee and its examiners, support for periodic account reviews and the trustee's fiduciary audit, documentation of the trustee's exclusive decision authority, and terms that let the trustee meet its recordkeeping and examination duties. The exact mapping is set by counsel review.",
    "Not established.", "Obtain counsel review (" + e6 + "); map Part 9 sections to Unbound capabilities.", "Nothing.",
    "Echelon has not yet analyzed what bank trustees of charitable funds need from a vendor under OCC fiduciary rules; this requires counsel review before any bank-trustee engagement.",
    "not-available", evrs=(e6,))
new_a.append(a)
new_q.append(question("REG", "Our trustee is a national bank administering the fund as a fiduciary. How will your platform support the bank's fiduciary account reviews, recordkeeping, audit of fiduciary activities and OCC examination under 12 CFR Part 9?", "bank-trustee-fiduciary",
    "A trustee bank remains responsible for fiduciary accounts administered by a vendor.", "The trustee bank cannot meet its fiduciary oversight and recordkeeping duties through the vendor.",
    [("SRC-OCC-12CFR9", "maps-to", "directly-documented", "12 CFR 9.6, 9.8, 9.9"), ("SRC-BSCA", "informed-by", "reasonably-inferred")],
    a, ("banking", "donor-advised-funds"), cls="legal-regulatory", importance="critical", authority="OCC", evrs=(e6,)))

r = ANS.get("ANS-TRM-006")
r["target_answer"] += (" For large banking organizations subject to resolution planning, the agreement also provides that "
    "the customer's resolution or entry into a resolution proceeding is not a termination or suspension event while fees "
    "are paid, that the agreement can be assigned to a bridge entity or acquirer, and that data access and exports continue "
    "throughout.")
hist(r, "BL-022: added resolution-resilient terms for banking customers and a canonical question (OBJ-REGULATOR-007).")
new_q.append(question("TRM", "If our bank enters resolution, will the service continue without termination or suspension while fees are paid, can the contract be assigned to a bridge bank or acquirer, and will data access continue?", "resolution-continuity",
    "Large banks flow resolution-planning continuity terms down to critical service providers.", "A critical service stops during a bank's resolution.",
    [("SRC-INTERAGENCY-TPRM-2023", "informed-by", "reasonably-inferred")], "ANS-TRM-006", ("banking",), cls="supervisory-guidance", importance="high",
    scope="ANS-TRM-006 covers recovery, resolution and divestiture; this question isolates the bank resolution case."))

a = answer("DON", "Donor-facing claims: fees, deductibility, recognition and AI content (unfair or deceptive practices)", "proposed-target-state",
    "Echelon is a for-profit company subject to FTC Act section 5 for its own representations, and state attorneys general police charitable solicitation. No review process exists for donor-facing pages, fee displays, deductibility statements or AI-generated communications.",
    "Donor-facing templates (fee displays, tax deductibility statements, recognition and impact claims, AI-generated content) are reviewed by counsel before use and versioned; deductibility language follows the counsel-approved rules in ANS-RRP-002, including that DAF contributions do not qualify for the non-itemizer deduction added by Pub. L. 119-21; interfaces avoid dark patterns (pre-checked add-on fees, hidden recurring gifts, confusing cancellation); AI-generated donor content is labeled and limited to approved claims; donor complaints are logged and reported to the sponsor (ANS-REG-005).",
    "Not established.", "Create a template review process with counsel; add dark-pattern checks to design review.", "Nothing.",
    "Echelon has not yet established review of donor-facing claims. It plans counsel review of fee, deductibility and recognition templates, avoidance of manipulative design and labeling of AI-generated donor content.",
    "planned", risks=("White-label partners may edit copy outside the reviewed templates.",))
new_a.append(a)
for text, sub, refs in [
    ("How do you review donor-facing pages, fee displays and tax deductibility statements so they are not unfair or deceptive, including statements about the non-itemizer deduction after Pub. L. 119-21?", "donor-claims-review",
     [("SRC-FTC-ACT-5", "maps-to", "directly-documented", "15 U.S.C. 45(a)(1)"), ("SRC-IRC-170", "informed-by", "reasonably-inferred"), ("SRC-STATE-CHARITABLE-SOLICITATION", "informed-by", "reasonably-inferred")]),
    ("Do donor flows avoid dark patterns such as pre-checked fee add-ons, hidden recurring gifts or hard-to-cancel commitments, and how are AI-generated donor messages controlled and labeled?", "dark-patterns",
     [("SRC-FTC-ACT-5", "maps-to", "reasonably-inferred"), ("SRC-STATE-CHARITABLE-SOLICITATION", "informed-by", "reasonably-inferred")])]:
    new_q.append(question("DON", text, sub, "Deceptive donor-facing claims create regulatory and reputational exposure for the sponsor and the vendor.",
        "Donors are misled about fees, deductibility or recognition.", refs, a, DAFI, juris=("US-federal", "US-states"), cls="legal-regulatory",
        importance="high", authority="FTC; state attorneys general"))
r = ANS.get("ANS-DON-005")
r["target_answer"] += " Donor-facing claims are reviewed under " + a + "."
hist(r, "BL-022: linked donor-facing claims review " + a + " (OBJ-REGULATOR-013, OBJ-DAFSPONSOR-006).")

# Pub. L. 119-21: already covered by DDQ-RRP-0040 (ANS-RRP-002); no new question added.

print("questions", len(new_q), new_q)
print("answers", len(new_a), new_a)
print("files", SRC.save(), Q.save(), ANS.save(), EVR.save())
