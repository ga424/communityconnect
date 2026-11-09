# Proposed S3-BROWSER-1 v1 consumer contract

**Not approved.** Supplements the implemented AC11/AC12 API contracts without changing them. Source E-3/A-2 and exact AC text: `docs/evidence/s1-closeout/next-feature-source.json`. Kundan reviews COMC-69; Sandeep reviews COMC-70; Gustavo approves COMC-68 scope. This is a local/test-only UI increment beyond the original S1-only M1 implementation boundary.

## Page and identity boundary

Serve `/manager`, `/manager/session` and exactly two allowlisted JS/CSS assets only when `BROWSER_REVIEW_ENABLED=1` and the existing APP_ENV=test guard passes. Require canonical positive INTEGER `BROWSER_REVIEW_USER_ID` using the existing parser; no default identity and invalid configuration fails startup. A syntactically valid unknown ID is allowed to reach the existing real401 contract. Disabled-by-default API app exposes none of these new routes. Do not change existing authentication/authorization handlers.

Session bootstrap returns exactly `{"mode":"synthetic","user_id":101}` for the configured fixture101, with no-store. The page then sends X-User-Id on its same-origin existing API fetches. Identity stays fixed per process; query parameters, storage and UI controls cannot select another identity. Local runner supports M1(101), M2(102), and known no-assignment103 via explicit configuration, not a product login picker. Display a small “Local review · synthetic data” banner. This is demonstrable UI, not production login, MFA or proof of A-2.

UI, session and asset responses use no-store and X-Content-Type-Options:nosniff. Page CSP: default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'. No inline scripts/styles, CDN/font calls, service worker, cookies or browser storage. The launcher publishes only127.0.0.1:8766, leaving the existing8765 review wrapper alone. Container-internal listening is not a public deployment.

## Observable page

Title “Community requests”; labeled native Community select; first disabled placeholder “Choose a community”; Refresh button; selected-community heading; status region; request table with ID, Unit, Category, Description, Status, Created (UTC). The community is communicated by the selected heading; submitted_by is never rendered. API order is retained. Use native controls, visible keyboard focus, semantic table headers/caption, polite status updates and alert semantics for errors. Desktop1280×800 and mobile390×844 must be usable; long descriptions wrap and any horizontal table scrolling stays inside its container. This is bounded usability evidence, not WCAG certification or a Figma fidelity claim.

Initial load fetches session then current options, no community auto-selection. No assignments shows “No assigned communities.” Authorized empty list shows “No requests in this community.” All other states remove prior rows immediately; no dimmed stale table under a new community label. Loading options disables selection; loading requests allows another selection so newer intent can win. Refresh is disabled only while its current bootstrap/options request is pending.

## Selection, refresh and lifecycle

Keep state only in page memory. Every selection/Refresh starts a new monotonically increasing request epoch, aborts the old fetch and clears rows immediately. A response may update the page only if both its epoch and selected community still match. Abort alone is insufficient as the design rule. Old success, failure or finally handlers cannot overwrite a newer state. Validate the whole payload before rendering; options require unique canonical positive IDs and1–100-character names, requests require the exact seven public fields, valid IDs/status/UTC strings and the selected community_id. Unexpected/malformed responses become an error with no partial data.

Refresh invalidates all pending work, clears rows, reloads current options, and preserves the earlier selection only when it is still offered; then it performs a fresh selected-community request. If no longer offered, reset to the placeholder. No automatic retry loops or polling. Each fetch has a proposed10-second client timeout; this is UI recovery behavior, not a backend timeout or service SLO.

Matched API401 clears options/selection/rows and says “Review identity unavailable.” Selected-read404 clears options/selection/rows and says “Community unavailable. Refresh communities.” Options server/network/parse/timeout errors clear everything and say “Unable to load communities. Try again.” Request errors clear rows, keep the selected label for context and say “Unable to load requests. Try again.” Refresh retries the bootstrap/options sequence. Error messages do not include API response bodies, IDs from denied records or database details.

On pagehide, invalidate/abort and clear options/selection/rows. On pageshow (including restoration), restart bootstrap with no selection. Reload similarly resets. No URL-selected context or persistent selection. A response already authorized before a revocation can finish; data displayed before revocation need not disappear until a subsequent selection, Refresh or page restoration checks current access. No promise of immediate cancellation or revocation while the tab is idle.

## Data and security behavior

Consume existing `/manager/communities` and `/manager/communities/{community_id}/requests`; no new manager data endpoint, role rule or schema. Render API text through textContent/DOM operations only. Never interpolate API text into HTML, URLs or script source. The only API mutations are explicit test-fixture setup/revocation actions outside the browser; browser operation is GET-only and must preserve five application tables.

Use existing disposable cc_test schema and protected reset_fixtures through a new, separately guarded review seed command. Seed synthetic managers101/102, unassigned103, communities1/2/3/empty4, valid units/memberships and distinct requests; no real data. Seeding is explicit test/launcher setup, never an application-startup reset or HTTP route. Do not run against an existing user's database/container project.

## Evidence interpretation

Core source ACs, role/revocation and data isolation use real browser→API→PostgreSQL. Delay tests fetch a real response then hold delivery with async Events; browser actions remain responsive. Tests that inject500, aborts or malformed payloads prove UI failure handling only, not server authorization. Actual BFCache availability is browser-dependent: automated lifecycle-handler testing must not be labeled a successful BFCache traversal unless an observed pageshow.persisted proves it.

A separate new30-case suite and browser CI job preserve the existing200-pass/five-skip API suite and its gate. All implementation, test and dependency changes require packet approval first. No production launch, real identities/payments, admin workflows, write actions, extra browser engines or full-story acceptance in this packet.
