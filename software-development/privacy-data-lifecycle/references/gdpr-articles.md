# GDPR Article 17 + Recitals 65-66 (condensed)

Extracted from gdpr-info.eu during the lead-qualification Blue Team audit (2026-08-10). These are the regulatory foundations for the split-store pattern.

## Article 17 — Right to erasure ('right to be forgotten')

### Six grounds for erasure (Art. 17(1))

The data subject has the right to erasure without undue delay where:

1. The personal data are no longer necessary in relation to the purposes for which they were collected or otherwise processed
2. The data subject withdraws consent (Art. 6(1)(a) or Art. 9(2)(a)) and there is no other legal ground for processing
3. The data subject objects to processing (Art. 21(1)) and there are no overriding legitimate grounds, or objects to direct marketing (Art. 21(2))
4. The personal data have been unlawfully processed
5. The personal data must be erased for compliance with a legal obligation in Union or Member State law
6. The personal data have been collected in relation to the offer of information society services to a child (Art. 8(1))

### Five exceptions where erasure does NOT apply (Art. 17(3))

Paragraphs 1 and 2 shall not apply to the extent that processing is necessary:

1. For exercising the right of freedom of expression and information
2. For compliance with a legal obligation which requires processing by Union or Member State law, or for performance of a task carried out in the public interest or in exercise of official authority
3. For reasons of public interest in the area of public health (Art. 9(2)(h)-(i), Art. 9(3))
4. For archiving purposes in the public interest, scientific or historical research purposes or statistical purposes (Art. 89(1)) insofar as erasure would render impossible or seriously impair the achievement of those objectives
5. **For the establishment, exercise or defence of legal claims** ← This is the primary exception used by legal holds in the split-store design

### Controller obligations when data has been made public (Art. 17(2))

Where the controller has made the personal data public and is obliged to erase it, the controller shall take reasonable steps, including technical measures, to inform other controllers processing the data that the data subject has requested erasure of any links to, or copies or replications of, those personal data.

## Recital 65 — Right of Rectification and Erasure

> A data subject should have the right to have personal data concerning him or her rectified and a 'right to be forgotten' where the retention of such data infringes this Regulation or Union or Member State law to which the controller is subject.

## Recital 66 — Right to be Forgotten

> To strengthen the right to be forgotten in the online environment, the right to erasure should also be extended in such a way that a controller who has made the personal data public should be obliged to inform the controllers which are processing such personal data to erase any links to, or copies or replications of those personal data. In doing so, that controller should take reasonable steps, taking into account available technology and the means available to the controller, including technical measures, to inform the controllers which are processing the personal data of the data subject's request.

## Article 5 — Principles relating to processing of personal data

Key principles relevant to retention:

- **Art. 5(1)(c) — Data minimisation:** "adequate, relevant and limited to what is necessary in relation to the purposes"
- **Art. 5(1)(e) — Storage limitation:** "kept in a form which permits identification of data subjects for no longer than is necessary"

## Article 27 — Representatives of controllers not established in the Union

If the client (controller) has no EU establishment but processes EU data subjects' personal data, they must designate a representative in the Union. This is the **controller's** obligation. Flag it in the design doc but do not implement it — it's a legal/commercial responsibility, not a technical one.

## Design implications

- **Default posture: delete on request.** The Art. 17(3) exceptions are narrow. "Defence of legal claims" is the only one a small pipeline can reliably invoke, and only during active disputes.
- **"Without undue delay"** means the deletion API must be immediate — no batch processing, no propagation delay.
- **Data minimisation by design:** The split-store pattern satisfies Art. 5(1)(c) directly — the immutable audit log carries zero PII by construction.
- **Storage limitation by design:** The auto-purge cron with jurisdiction-specific `retention_deadline` satisfies Art. 5(1)(e).
