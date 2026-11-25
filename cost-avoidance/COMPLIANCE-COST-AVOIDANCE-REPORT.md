---
id: DD-COST-002
title: Compliance cost avoidance strategy and substitution risks
status: draft
version: 0.2.0
created: 2026-11-25
updated: 2026-11-25
tags: [due-diligence, cost-avoidance, compliance, soc2, assurance, hypotheses]
related_documents:
  - external-assurance/EXTERNAL-ASSURANCE-REQUIREMENTS-MATRIX.md
  - external-assurance/external-assurance-matrix.csv
  - cost-avoidance/PENETRATION-TESTING-COST-REDUCTION-STRATEGY.md
  - scanner-validation/SCANNER-VALIDATION-RESEARCH-REPORT.md
---

# Compliance cost avoidance strategy

## 1. Ground rules

- Every saving below is a **hypothesis (H)** until measured. The Standard says "Do not
  assume savings before measurement" (`SRC-ECH-SCS-0.1`).
- Cost avoidance never means replacing an assurance that a law, standard or contract
  requires a named qualified body to perform (DD-EXT-001 finding 1).
- Internal evidence is first-party. It can lower the cost of independent assurance; it
  cannot become independent assurance.
- Cost figures come from DD-EXT-001. Most are vendor marketing or federal ceiling rates, so
  absolute savings are not estimated here.

## 2. Prioritized strategy

Priority reflects (a) likelihood of real saving, (b) low substitution risk and (c)
dependency order.

| Priority | Strategy | Activities affected | Hypothesis | Measure | Substitution risk |
|---|---|---|---|---|---|
| 1 | Decide scope before buying: map actual regulatory, auditor, insurer and customer requirements | All | H1: avoids purchasing assessments nobody requires (for example ASV scans if PCI does not apply, FedRAMP, ISO if buyers accept SOC 2) | Count of planned purchases dropped with written rationale | Low if decisions are documented and revisited |
| 2 | Keep payment card data out of Echelon systems | EXT-03, PCI parts of EXT-01 and EXT-02 | H2: avoids PCI ASV scans and PCI-driven testing | PCI applicability decision from acquirer or QSA | Medium: scope decisions can be wrong; must be confirmed |
| 3 | Open-source, language-independent scanning in CI across repositories | EXT-02, EXT-01 prep, EXT-16 | H3: avoids commercial SCA, secret and IaC scanner licenses with acceptable coverage | Findings found versus missed in later pen tests; triage hours | Medium: advisory lag, no vendor support, Semgrep rules license limits, CodeQL needs license for private code |
| 4 | Machine-readable evidence keyed to control IDs (Praxis provenance plus Tutela verification) | EXT-04, EXT-05, EXT-06, EXT-07, EXT-16, EXT-18, EXT-19 | H4: reduces auditor sample requests and internal preparation hours | Auditor hours billed; internal hours per audit; number of evidence requests | Medium: auditors must assess reliability of entity-produced information; custom pipelines may need more auditor testing |
| 5 | One shared control environment and system description for all Echelon products | EXT-05, EXT-06, EXT-07, EXT-11, EXT-12 (SOC 1 shares the control environment but needs its own report) | H5: one SOC 2 and one ISMS cover several products | Report scope accepted by auditor; customer acceptance | Medium: a broad scope makes one failure affect all products |
| 6 | Single answer library and trust center | EXT-17 | H6: cuts questionnaire hours | Hours per questionnaire; reuse rate | Medium: stale or overstated answers create misrepresentation risk |
| 7 | Architecture that narrows pen test focus (DD-COST-001) | EXT-01 | H7: fewer tester-days for same coverage | Tester-days per release; findings per day | Medium: tester anchoring; must not exclude assets |
| 8 | Internal readiness rather than purchased readiness | EXT-04 | H8: avoids readiness fees | External fees avoided versus internal hours | Low to medium: blind spots; first audit may find more exceptions |
| 9 | Internal policy development from Standard and frameworks | EXT-10 | H9: avoids consultant fees | Policy exceptions found by auditor | Medium: generic or untested policies |
| 10 | Build compliance monitoring on Praxis and Tutela instead of a platform subscription | EXT-15 | H10: lower long-term cost | Build and maintenance hours versus subscription quotes (unknown) | High: engineering opportunity cost; auditor familiarity; platform also provides auditor network and templates |
| 11 | Echelon F# security analyzers in Tutela | EXT-02, EXT-01 prep | H11: closes F# gap that no purchased tool closes | Holdout recall and precision per CWE (DD-SCN-001) | Medium: a home-built scanner without validation would create false assurance |
| 12 | Defer optional certifications (ISO/IEC 27001, ISO/IEC 42001) until buyers require them | EXT-07, EXT-14 | H12: avoids certification and surveillance fees | Deals lost or delayed for lack of certificate | Medium: sales friction |

## 3. Items that cannot be avoided by internal work

| Item | Reason | Source |
|---|---|---|
| SOC 2 Type I or II report | Independent CPA attestation | `SRC-AICPA-SOC2` |
| SOC 1 Type 1 and Type 2 reports (EXT-18, EXT-19), where sponsors rely on Unbound for financial reporting | Independent CPA attestation under AT-C 320; separate examination, system description and control objectives from SOC 2, so its fees add to SOC 2 fees; likely the largest recurring assurance cost of a fund administration platform (judgment, not sourced) | `SRC-AICPA-SOC1-GUIDE`, `SRC-AICPA-SSAE-18` |
| ISO/IEC 27001 certificate | Accredited certification body | `SRC-ISO-17021-1`, `SRC-ISO-27006` |
| PCI ASV scan (if PCI applies) | ASV only under 11.3.2 | `SRC-PCI-ASV-PROGRAM`, `SRC-PCI-DSS-V4-SAQ-D` |
| FedRAMP penetration test (if pursued) | 3PAO | `SRC-FEDRAMP-PENTEST-GUIDANCE` |
| DORA TLPT participation (if required) | Art. 26 and 27 tester rules | `SRC-TIBER-EU` |
| Independent pen test named in contracts or insurance | Contract terms | Contract-specific |
| Legal opinions | Licensed counsel | n/a |

SOC 1 timing follows the single assurance roadmap in ANS-AUD-001 (added 2026-11-25): SOC 2
Type I and, where sponsors rely on Unbound for financial reporting, SOC 1 Type 1 at go-live,
then Type 2 periods sized to sponsors' fiscal years, with direct or substantive testing by
the sponsor's auditor as the fallback when no SOC 1 Type 2 can exist in time.

## 4. Total cost of ownership view

For each build-instead-of-buy choice, compare over at least three years:

- External fees avoided (quotes, not marketing ranges).
- Internal engineering hours to build, at a loaded rate. BLS reports a May 2025 median
  annual wage of $129,180 for information security analysts (`SRC-BLS-INFOSEC`), about $62
  per hour before benefits and overhead; the loaded rate will be higher.
- Maintenance hours per year (rule updates, tool upgrades, advisory feed changes).
- Additional auditor testing hours caused by custom evidence systems.
- Opportunity cost: product features not built during that time.
- Risk cost: probability and impact of a missed vulnerability or a rejected report.

## 5. Substitution risks in summary

1. **Mislabeling:** internal reports read as independent assurance. Control: label all
   first-party outputs, as the Standard requires.
2. **False assurance from unvalidated scanners:** control via DD-SCN-001 validation.
3. **Customer rejection:** obtain written acceptance before relying on internal evidence.
4. **Auditor reliance limits:** confirm with the chosen CPA firm how it will test
   Echelon-produced evidence before building the pipeline.
5. **Engineering opportunity cost:** small teams may lose more in delayed product work
   than they save in fees.
6. **License constraints:** Semgrep Rules License, CodeQL terms, TruffleHog AGPL, and
   Tutela's own PolyForm Noncommercial license.

## 6. Measurement plan

Record per year: external fees by activity, internal hours by activity, auditor evidence
requests, exceptions found, pen test findings that automation missed, questionnaire hours,
and deals affected by assurance gaps. Convert each H into a measured result or withdraw it.

## 7. Open questions

- Which customers, sponsors and insurers will Unbound serve first, and what do their
  contracts require in writing?
- Does any PCI scope exist?
- Which CPA firm and what reliance approach for automated evidence?
