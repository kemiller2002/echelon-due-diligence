# Echelon Due Diligence

Evidence-backed knowledge base for customer due diligence, vendor risk, security
assurance, regulatory compliance and operational preparedness across Echelon Foundry
products, with Unbound (DAF administration) as the first product profile.

The goal is not to answer questionnaires faster. It is to know, for every question a
customer can ask, what Echelon currently does, what it intends to do, what it can prove,
and what it may truthfully say, and to generate that evidence as a byproduct of how
software is built and operated.

**Status:** research phase. Nothing here is a customer-facing claim. Most answers are
`proposed-target-state` or `unknown` because Unbound is not yet implemented and Echelon
holds no independent attestations. Start with `reports/EXECUTIVE-RESEARCH-FINDINGS.md`.

## Rules

Governance: `AGENTS.md` (Praxis). Research integrity and record formats:
`docs/DUE-DILIGENCE-OPERATING-CONTRACT.md`. Record format decision: `decisions/DDD-001-record-format.md`.

## Build

```bash
dotnet fsi tools/build.fsx          # validate and regenerate reports/generated/
dotnet fsi tools/build.fsx --check  # validate only
```

The build fails on schema violations, dangling references, duplicate IDs, em dashes and
any answer that presents a non-operational capability as a current fact.

## Layout

| Path | Contents |
|---|---|
| `sources/` | Master source register (JSONL per domain) |
| `questions/` | Canonical question bank (JSONL per category; `TAXONOMY.json`) |
| `answers/` | Answer units: current, intended, provable and communicable answers |
| `controls/` | Echelon control register |
| `evidence-requirements/` | Evidence requirements register |
| `schemas/dd/` | JSON Schemas for every record type |
| `security-by-construction/` | Architectural assurance model and CWE matrix |
| `scanner-validation/` | Scanner validation and F# analysis research |
| `external-assurance/`, `cost-avoidance/` | External assurance requirements and economics |
| `industry-profiles/`, `product-profiles/unbound/` | Industry and product profiles |
| `gap-analysis/` | Unbound, policy and system capability gaps |
| `questionnaires/` | Real-world questionnaire research |
| `trust-center/` | Trust center research and requirements |
| `architecture/` | Current-state brief, capability analysis, evidence and questionnaire-automation architecture |
| `recommendations/` | Traceable recommendations for other repositories |
| `validation/` | Adversarial reviews and objections |
| `reports/` | Executive findings, roadmap; `reports/generated/` is build output |
| `research/` | Backlog, progress ledger, open questions, source notes |

The deliverable index with traceability is `reports/DELIVERABLES-INDEX.md`.
