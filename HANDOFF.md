# Handoff: due diligence research, session 1 (2026-11-25)

## Objective
Build an evidence-backed due diligence knowledge base for Echelon Foundry and Unbound
(mission prompt preserved in the PR description and summarized in `README.md`).

## Completed
All 26 deliverables drafted; see `reports/DELIVERABLES-INDEX.md` and
`reports/EXECUTIVE-RESEARCH-FINDINGS.md`. Canonical records validate with 0 errors.

## Decisions and assumptions
DDD-001 (JSONL canonical for records), DDD-002 (question dedup log). Agents draft; only
named humans approve (operating contract). No supporting repository was modified.

## How to verify
`dotnet fsi tools/build.fsx --check` (requires .NET 10 SDK), `./praxis validate`.

## Open questions and risks
`research/open-questions.jsonl` (decision-level), generated
`reports/generated/open-questions-register.csv` (record-level),
`research/OWNER-FACT-VERIFICATION-CHECKLIST.md`, `validation/objections-*.jsonl`
(123 open).

## Next recommended actions (precise continuation)
1. Owner: complete the fact checklist and start human review of the 40 deciding
   questions in `product-profiles/unbound/UNBOUND-DUE-DILIGENCE-PROFILE.md` section 3.
2. Research: BL-024 citation hygiene (457 questions cite superseded Unbound records
   without the governing CNV clause), then BL-025, then BL-013 diminishing-returns pass
   (sample 5 to 10 new public questionnaires, count genuinely new questions per 100).
3. Address remaining accepted-open objections, starting with blocking severity.
4. Recommendations for other repositories are in `recommendations/*.jsonl`; none has
   been applied.
