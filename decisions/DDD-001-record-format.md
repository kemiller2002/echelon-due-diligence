---
id: DDD-001
title: Canonical record format for the due diligence knowledge base
status: accepted
version: 1.0.0
created: 2026-11-25
updated: 2026-11-25
---

# DDD-001: JSON Lines canonical for high-volume records, Markdown for narrative

## Context

The mission requires thousands of interlinked questions, answers, controls and
evidence requirements with many-to-many relationships, and warns against thousands of
disconnected Markdown files. The Echelon Knowledge Store research
(`echelon-knowledge-store@35d9cee0:research/2026-knowledge-representation/strategy/executive-report.md`)
recommends Markdown with front matter as canonical and compiled registries, and rejects
JSON as a source format for knowledge documents.

## Decision

- High-volume structured records (sources, questions, answer units, controls, evidence
  requirements, proposed requirements, objections, recommendations) are canonical in
  JSON Lines, one file per category, validated by JSON Schema in `schemas/dd/`.
- Narrative research, reports, decisions and briefs are Markdown with Praxis-style front
  matter.
- `tools/build.fsx` (F#) validates schemas, identifier uniqueness, referential
  integrity, honesty rules and style, and generates CSV/Markdown registers under
  `reports/generated/`.

## Rationale and disagreement with EKS

EKS's recommendation concerns knowledge documents that agents read as prose. These
records are tabular data with fixed fields; one record per line keeps diffs reviewable,
allows schema validation and avoids 5,000+ files. This is a deliberate divergence from
EKS for data, consistent with EKS's own finding that F# records as a storage format add
metadata overhead and that compiled registries carry the value.

## Consequences

- EKS integration requires an adapter that reads JSONL (recorded as
  REC-EKS-001 in `recommendations/`).
- Reversal trigger: if EKS adopts a structured-data convention, migrate by generation,
  not by hand.
