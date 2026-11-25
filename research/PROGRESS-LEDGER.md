---
id: DD-LEDGER-001
title: Due diligence research progress ledger
status: canonical
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
---

# Progress ledger

Append-only. Each entry records what was done, what verified it, and what remains.

## 2026-11-25 Session 1 (work item DD-RESEARCH-2026-001)

- Inspected repositories and recorded commits: echelon-organization-administration
  2763e576, unbound 9b38de47, daf-landscape 97dddb7, EDF 763ff8c, clarity-framework
  200a9eb, praxis 12bf9951, aegis 711e0260, tutela 476dc682, dokimos 6ea86246, strata
  c6a384ec, limen 743cdb9b, forma c8f40b4c, folio 56a18e1f, vigila feab7551, ordo
  db6d39ed, echelon-registry f9ea4d0b, echelon-knowledge-store 35d9cee0.
- Finding: the Secure Construction Standard's proposed ownership table diverges from
  verified repository purposes (Aegis is fault handling; Vigila is a task organizer;
  Tutela is the security authority per Dokimos requirements; Strata is schema management
  with no verified runtime query interface).
- Installed Praxis 3.25.0 (native bundle, checksum verified) and ran `praxis init`.
- Established operating contract, schemas, taxonomy (67 categories), seed source IDs,
  current-state brief, record format decision DDD-001.
- Built `tools/build.fsx` (F#) validator and register generator; verified it compiles
  and runs (`dotnet fsi tools/build.fsx --check`, .NET SDK 10.0.404).
- Built `tools/unbound-coverage.fsx`; screening shows thin Unbound coverage for INS,
  SDL, VUL, SCN, CLD, ESC, SUB (fewer than 5 keyword hits in 1,653 records).
- Launched parallel research batches (question bank by category group, source register,
  real-world questionnaires and trust centers, scanner validation and external assurance
  economics, Echelon system capabilities, security by construction).
- Wrote automated questionnaire response requirements (AQR-*).
