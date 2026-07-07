# Intake — FY2027 Membership Dues Restructure (Board Decision Brief)

> Synthetic example. All names, organizations, figures, and sources below are fictional and were
> created for this example. No real association, person, dataset, or document is referenced. This
> artifact is `internal` classification and contains no client data, CUI, or secrets.

## Artifact

- **Artifact ID:** `artifact:association-board-brief-001`
- **Type:** `association_board_brief`
- **Title:** FY2027 Membership Dues Restructure — Board Decision Brief
- **Audience:** `association_board` (Riverbend Regional Trade Alliance board of directors)
- **Classification:** `internal`
- **Owner:** `human:board-liaison-01` (board liaison)
- **Release channel:** board portal (internal)
- **Deadline:** FY2027 budget vote, board meeting of 2026-07-09

## Context

The Riverbend Regional Trade Alliance (RRTA) closed FY2025 with an operating deficit. Membership
dues have not been restructured in several years. Staff have asked the board to decide, at the
FY2027 budget meeting, whether to adopt a dues increase and, if so, in what structure. This brief
assembles the evidence and states a recommendation for the board's decision.

## Decision the board must make

Adopt, amend, or decline a proposed FY2027 membership-dues change, subject to the bylaws' amendment
procedure.

## Required reviewer roles

- Verification / materiality review (owner or delegate).
- Plain-language and accessibility review (independent reviewer).
- Human approval before any release to the board portal.

## Known sources (synthetic)

| Ref | Access | Description |
| --- | --- | --- |
| `s001` | `internal_document` | RRTA FY2025 audited financial statements (statement of activities). |
| `s002` | `dataset` | 2026 RRTA member survey export (renewal intent by dues scenario). |
| `s003` | `interview` | Interview with the board chair on strategic intent (2026-06-30). |
| `s004` | `dataset` | Peer-association dues benchmarking dataset (similar-size regional alliances). |

## Open questions and assumptions at intake

- **Question:** What is the projected member attrition at each candidate dues tier?
- **Assumption:** FY2027 non-dues revenue holds flat at FY2025 levels.
- **Constraint:** Any dues change must satisfy the RRTA bylaws' two-thirds board-vote amendment
  procedure.

## Provenance

The claim graph, evidence, reviews, approval, and release for this artifact are recorded in
`events.jsonl` and validated against `schemas/v0/`. See `provenance/` for the model. The materialized
release outputs (`expected/`) are a Phase 4 deliverable and are not part of this example yet.
