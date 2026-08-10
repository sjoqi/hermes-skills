---
name: privacy-data-lifecycle
description: Split-store PII pattern for GDPR erasure compliance.
version: 1.0.0
author: curator
license: CC-BY-4.0
metadata:
  hermes:
    tags: [privacy, gdpr, compliance, data-lifecycle, architecture]
    related_skills: [codebase-design, product-idea-validation]
---

# Privacy Data Lifecycle Design

## When to Use

Load this skill when designing or auditing data stores that must reconcile immutable audit/replay requirements with the data subject's right to erasure. Trigger conditions: GDPR/NDIS/CASL/PDP compliance questions, "immutable audit log" + "right to erasure" mentioned together, raw ingress payloads containing PII, Blue Team privacy audits, or designing deletion APIs, retention policies, or legal-hold mechanisms.

Design data stores that satisfy two goals simultaneously: (1) **never lose replay/audit capability** and (2) **delete personal data on request**. The split-store pattern is the core technique.

## When to load

- User asks about GDPR/NDIS/CASL/PDP compliance for a data pipeline
- User mentions "immutable audit log" and "right to erasure" in the same breath
- User is designing a store that holds raw ingress payloads containing PII
- User asks "how do real platforms handle audit logs vs GDPR deletion"
- Blue Team / privacy audit of an existing schema
- Designing a deletion API, retention policy, or legal-hold mechanism

## Core technique: the split-store pattern

**The problem:** An append-only entry log that stores verbatim POST bodies (name, email, phone, form answers) is storing PII in an immutable store. GDPR Article 17 requires erasure on request. You cannot have both.

**The solution in one sentence:** The entry log carries non-PII metadata + a foreign key to a separate deletable PII store. On GDPR erasure, only the PII store is scrubbed; the entry log gains a tombstone but remains for audit.

```
BEFORE (broken):
  entry_log row = {metadata + raw_payload (PII)}  ← PII is immutable

AFTER (compliant):
  entry_log row = {metadata + pii_record_id}       ← immutable, non-PII only
  pii_store row  = {pii_record_id + raw_payload}   ← mutable, deletable
```

## Design steps (in order)

### 1. Identify where PII lives in the current schema

Read the existing design docs. Find every column that stores personal data: names, emails, phones, free-text answers, IP addresses (in some jurisdictions), device fingerprints. Mark each as PII-touching.

### 2. Research how real platforms handle the same tension

The pattern is consistent across Zapier, n8n, HubSpot, and Stripe:

| Platform | Immutable/audit store (non-PII) | Deletable store (may contain PII) | Erasure behaviour |
|---|---|---|---|
| **Zapier** | Task History: task ID, timestamp, app, status | Task data in/out | Account deletion removes task data; audit events survive |
| **HubSpot** | Admin audit log: who changed what, when | Contact records (name, email, phone) | Contact hard-deleted; audit log retains "contact X deleted by Y at Z" |
| **Stripe** | Events (immutable): `charge.created`, amount, customer ID | Customer/Charge objects (name, card metadata) | Customer deletable; events remain with pointer to now-deleted customer |

The universal pattern: the audit log tracks *what happened* (non-PII), not *to whom* (PII). Cite these precedents in the design doc — they establish that split-store is industry standard, not a novel invention.

### 3. Analyze each applicable jurisdiction

For each jurisdiction the pipeline serves:

- **GDPR (EU):** Article 17 right to erasure, no "undue delay." Exceptions in Art. 17(3): legal claims, legal obligation, public interest. The "defence of legal claims" exception is the one you'll lean on for legal holds.
- **AU NDIS:** NDIS Act + Privacy Act 1988 APPs. Participant privacy with heightened expectations around disability-related data. APP 11 (security), APP 12 (access), APP 13 (correction). Retention typically 2 years (funding plan lifecycle).
- **CA CASL + PIPEDA:** CASL requires consent proof retention; PIPEDA gives right to withdraw consent and request deletion. **Resolution:** consent proof = non-PII metadata (timestamp, source, HMAC verification, payload hash). The PII is deletable; the proof of consent survives.
- **ID PDP:** Modeled on GDPR. Right to erasure (Pasal 8), purpose-limited retention.

Map each requirement to a specific design element. Don't hand-wave compliance — show exactly which schema column or API endpoint satisfies which regulatory clause.

### 4. Design the split schemas

**Immutable entry log** (the audit trail — zero PII):
- `entry_id` (PK), `request_id`, `run_id`, `received_at`, `source`, `hmac_status`
- `pii_record_id` (FK → PII store)
- `payload_hash` (SHA-256 — non-reversible, proves integrity not content)
- `content_type`, `payload_size` (aids replay validation)
- `deletion_status` (enum: `active` → `tombstone`, set once on erasure)
- `notes` (appendable)

**Deletable PII store** (the personal data — mutable, encrypted at rest):
- `pii_record_id` (PK), `entry_id` (FK back-reference)
- `raw_payload` (the verbatim POST body — **this is PII**)
- `created_at`, `retention_deadline`, `jurisdiction`
- `legal_hold` (bool — blocks deletion during active disputes)
- `erasure_status`, `erased_at`, `erasure_method`

**Why raw_payload, not extracted fields:** Replay fidelity requires the exact bytes. Extracting named fields loses encoding, ordering, and unknown fields. The replay path reconstructs from the original POST body; extraction happens at replay time, same as first ingress.

### 5. Design the tombstone format

On erasure, overwrite PII with a fixed-format tombstone — never the empty string (distinguishes "erased" from "never written"):

```
raw_payload → "ERASED:2026-08-10T09:15:00Z:data_subject_request"
```

The entry log row remains. It proves: a lead arrived at `received_at` from `source`, passed HMAC, was assigned `run_id`, and was later erased. `payload_hash` remains as cryptographic evidence of the original payload's integrity — a regulator can verify the hash without seeing the plaintext.

### 6. Design the deletion API

All endpoints internal (service token / internal HMAC, never the public webhook path):

- `DELETE /internal/pii/{entry_id}` — Single-lead erasure: check legal hold → overwrite PII with tombstone → set `deletion_status = tombstone` → cascade to run-row `extracted` fields (overwrite name/email/phone with `[ERASED]`) → cascade to dead-letter notes → return result
- `POST /internal/pii/legal-hold/{entry_id}` — Place/remove litigation hold (time-limited, audited)
- `GET /internal/pii/status/{entry_id}` — Check deletion status
- `POST /internal/pii/purge-expired` — Cron-triggered retention cleanup

Key design decisions:
- Erasure is **idempotent**: erasing an already-erased record returns 200 OK
- Legal holds block deletion with `409 Conflict` + reason
- Cascade to derived stores (run rows, dead-letter) scrubs PII-derived fields but keeps scores, statuses, drafts

### 7. Design the replay path with and without PII

**Normal replay (PII active):**
```
replay(entry_id) → check deletion_status = active
  → follow pii_record_id → read raw_payload
  → verify SHA-256(raw_payload) == payload_hash
  → mint new run_id, enqueue
```

**Post-erasure replay (PII gone):**
```
replay(entry_id) → check deletion_status = tombstone
  → return 410 Gone: { error: "source_erased", erased_at, erasure_method,
    message: "This lead's personal data was erased per a data subject request.
              Replay is not possible." }
```

This is the honest answer. Once PII is erased, replay cannot reconstruct the original lead — that's the point. The pipeline's audit integrity is preserved through the tombstone + hash; replay capability is intentionally surrendered as a direct consequence of honouring the data subject's rights.

### 8. Design retention policy with jurisdiction-specific deadlines

| Jurisdiction | Default retention | Rationale |
|---|---|---|
| EU (GDPR) | 365 days | Art. 5(1)(e): no longer than necessary |
| AU (NDIS) | 730 days | Funding plan lifecycle (12-24 months) |
| CA (CASL) | 730 days | Commercial relationship + post-termination window |
| ID (PDP) | 365 days | Modeled on GDPR |
| Unknown | 365 days | Default to strictest common denominator |

`retention_deadline = created_at + jurisdiction_retention_days`. Set from the vertical preset config. Auto-purge via daily cron: `POST /internal/pii/purge-expired`. Legal holds block auto-purge. Consent-based extension allowed but must carry an audit trail.

### 9. Define the minimum viable compliance posture

For a small-scale pipeline (e.g., $100-client, self-hosted, Sheet-backed):

| Layer | Do | Don't (yet) |
|---|---|---|
| PII separation | Split raw_payload into deletable PII store | App-level encryption (Google covers transport+storage; add at product tier) |
| Deletion API | Single-lead erasure with tombstone + cascade | Automated "proof of deletion" certificates |
| Retention | Jurisdiction-specific deadlines + auto-purge | Granular field-level retention |
| Legal holds | time-limited hold flag, blocks deletion | Full e-discovery workflow |
| Consent proof | Entry log metadata as CASL consent evidence | Separate consent ledger |

The client is the **data controller**; we are the **processor**. The deletion API is a processor tool the controller invokes. The client owns the process; we provide the mechanism.

## Pitfalls

- **Don't store PII in a column named "immutable."** The name itself is a compliance red flag. If a column is genuinely immutable and contains personal data, you've built a GDPR violation into the schema.
- **Don't use an empty string as a tombstone.** Distinguish "erased" from "never written" with a fixed-format marker.
- **Don't cascade erasure silently.** Every cascade (run rows, dead-letter, GHL) must log what was overwritten and when.
- **Don't allow permanent legal holds.** Holds must be time-limited and reviewed. A "permanent hold" is just retention-by-another-name.
- **Don't claim the entry log proves consent if it doesn't.** The entry log proves a lead *arrived* from a consent-gated source (Facebook Lead Ads). That is sufficient for CASL — but spell out the chain of reasoning rather than asserting "this proves consent."
- **The EU representative requirement:** if the client has no EU establishment but processes EU data subjects' data, they must designate an EU representative (GDPR Art. 27). This is the client's obligation as controller, but flag it in the design doc.

## References

- `references/gdpr-articles.md` — Condensed GDPR Article 17 + Recitals 65-66 text, plus the six erasure grounds and five exceptions.
