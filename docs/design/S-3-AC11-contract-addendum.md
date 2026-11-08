# S3-AC11 contract addendum v1

**Scope approved by Gustavo on November 8, 2026.** Exact decision is in prompts/2026-11-08-s3-ac11-approval.txt. COMC66/67 are Done with closures by Gustavo; independent reviewer authorship is not asserted. COMC65 implements only this bounded contract. This preserves `docs/design/S-3-context.md` and the approved options-only addendum. It makes the next API projection precise without changing M1 scope.

## Observable interface

Add only `GET /manager/communities/{community_id}/requests`, with a raw string path parameter. The provider is the local FastAPI application; the consumer is a future community-selector UI. Classification: additive local API; existing resident and options consumers remain compatible. Only synthetic fixtures are authorized.

For routes that match, parse the caller first using the unchanged `app.requests._database_id`, then verify that user exists. Missing, malformed, out-of-range or unknown callers get `401 {"detail":"Unknown user"}`. Only then parse the community. Invalid, nonexistent or unassigned communities all get `404 {"detail":"Not found"}`. A known caller with no manager assignment also gets404. A genuinely absent path segment does not match this route and remains framework404; do not add a catch-all or promise caller precedence before route matching.

Assignment means `memberships.user_id=caller`, selected `community_id`, `role='manager'`. Ignore `unit_id`, whether null or a valid link; this extends the AC12 correction explicitly to AC11. Board/admin/resident roles are not manager grants. An options list is not authorization for a later request.

Return200 with an array of exactly the existing `RequestResponse` fields: `id`, `community_id`, `unit_id`, `category`, `description`, `status`, `created_at`. Include requests from every resident of that selected community, not just those submitted by the manager. Exclude `submitted_by` and all other fields. Preserve stored status and UTC second formatting; sort `created_at DESC, id DESC`. An authorized empty community returns `[]`. Use `Cache-Control: no-store` for200/401/404. There are no writes, pagination, persisted selection or cross-caller context.

## Transaction and revocation

Use the existing dedicated database connection and one transaction. Check identity, then select the current manager membership with parameter binding and `FOR SHARE`. If absent, deny. Read only the selected community's seven request columns, validate every row with the existing response model **before leaving the transaction**, and return fully materialized objects. Lock the membership even when the request list is empty. Do not merely join it to a nonempty request result or use a weaker key-share lock.

PostgreSQL17 documents that a shared row lock blocks updates/deletes until the transaction ends; key-share does not block every non-key update. This supports choosing `FOR SHARE` to protect role changes as well as removal. [PostgreSQL row locks](https://www.postgresql.org/docs/17/explicit-locking.html#LOCKING-ROWS)

Read Committed takes statement snapshots and rechecks the updated row predicate after a conflicting updater commits. Our contract therefore denies a revocation committed before the authorization read, and allows a read that already holds authorization to finish validating before revocation commits. It does not promise cancellation of a response already being sent. Request rows are read at their SELECT snapshot; this is not a whole-database serializable snapshot. [PostgreSQL Read Committed](https://www.postgresql.org/docs/17/transaction-iso.html#XACT-READ-COMMITTED)

Database/validation exceptions must unwind the transaction and remain server errors, not empty success or authorization denial. No blanket exception handler. Locks protect authorization through application validation, not network delivery. No retry policy, production timeout/SLO or instant-revocation promise is introduced.

## Machine-readable companion and limits

The adjacent JSON test inventory fixes route cases and exact expected errors. A compact JSON contract in `S-3-AC11-contract-proposed.json` records the interface and invariants; it is a proposal, not a deployed OpenAPI endpoint. Implementation may reuse the existing response model without editing it.

Browser AC11/12 evidence, identity/MFA, invitation/assignment administration, status writes, real data, payments, pagination and real-volume performance remain excluded. OQ1/OQ2 from the original context contract remain open for those future scopes. No new dependency, schema change or original design rewrite is authorized by drafting this proposal.
