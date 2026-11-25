# Batch 1 generator scripts (provenance)

These Python scripts generated the initial batch 1 records (question bank by category
group and the CWE matrix) on 2026-11-25. They are preserved for provenance and
reproducibility of that batch only. **The canonical data is the JSONL in `questions/`,
`answers/`, `controls/`, `evidence-requirements/` and `security-by-construction/`.**
Later edits are made to the JSONL directly or by new scripts; rerunning these
generators would overwrite later refinements. Paths inside the scripts point at the
session scratchpad and must be adjusted before any rerun. Note that several agents
shared `qb/`; its `common.py` and `lib.py` were overwritten during the batch.
