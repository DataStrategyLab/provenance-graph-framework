# Confidence Scale

Status: v0 loose draft (Phase 1). Normative statements use RFC 2119 keywords. This scale defines the
`confidence_band` enum on the `claim` node (`low`, `medium`, `high`, `verified`). Confidence is an
**epistemic** property (how well-supported the claim is), distinct from **materiality** (how much the
claim matters — see `materiality-policy.md`). A high-materiality claim at `low` confidence is exactly
what the verification loop exists to surface.

## Bands

| Band | What it asserts | Typical evidentiary state |
| --- | --- | --- |
| `low` | Plausible but weakly supported; may be an unverified assertion or a single soft source. | No supporting evidence yet, or one non-authoritative source; often paired with an open `question`. |
| `medium` | Reasonably supported but not independently confirmed. | At least one credible source, but not corroborated or not fully authoritative. |
| `high` | Well supported by authoritative evidence. | Supported by an authoritative source (see `source-hierarchy.md`) with a `supports` edge and no live contradiction. |
| `verified` | Confirmed against authoritative evidence and checked by a reviewer. | Supported evidence AND a recorded review with a passing decision on the claim. |

## Rules

- A conforming claim MUST carry exactly one `confidence_band`.
- `verified` SHOULD NOT be assigned by an extraction agent on its own: it asserts that a human review
  confirmed the claim. Assigning `verified` without a corresponding `review.recorded` event on the
  claim is a defect a reviewer or a future `pgf check` SHOULD surface.
- Confidence MAY change over the artifact's life (e.g. `low` → `high` when evidence is added). Such a
  change is recorded as a `claim.updated` event carrying the `prior_status`/prior band as sibling
  context (see `event-taxonomy.md`).
- The **wording** of a drafted statement MUST stay within its claim's confidence band: a `low`- or
  `medium`-confidence claim MUST NOT be drafted in language that reads as settled fact. This is one of
  the Verifier's explicit checks.
- Confidence is not a probability. The bands are ordinal labels for review, not calibrated
  likelihoods, and MUST NOT be presented as numeric certainty.
