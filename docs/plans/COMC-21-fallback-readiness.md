# COMC-21 conditional balance fallback and COMC-8 payment gate

The fallback has **not been activated**. COMC-52 owns the Milestone2 isolation/capacity and payment include/cut decision. Current S1 tests cover a resident request slice only and cannot establish the full-platform four-role/every-endpoint isolation gate. S6 remains five unbuilt local fake-processor test contracts; no provider integration or live funds are enabled.

COMC-21's legacy S13/AC31–32 are historical identifiers. Revised AC31 belongs to board-document upload, so never reuse that ID for this fallback. The revised S7 AC23–25 covers unpaid flags/reminders; balance entry/read is an additional fallback capability to reconcile explicitly before implementation.

## Bounded candidate slices after the gate

1. **Balance entry and provenance:** authorize a manager for one community, record a unit/month balance with source/as-of value and correction history. Product decisions needed: source of truth, who may correct, currency/rounding, credit/negative amounts, and audit retention. Do not assume a manager-entered figure means an electronic transaction settled.
2. **Resident balance read:** show only the permitted unit's read-only balance and no scheduling/charge action. Tenant/household visibility depends on unresolved policy; do not widen S1's resident boundary. Test same/cross-community and guessed-ID denial for all relevant roles.
3. **Courtesy reminder:** reuse separately accepted S7 policy. REMINDER_DELAY_DAYS is a per-community approved setting, not an invented date. A posted payment suppresses a reminder; received-but-unposted receipts (Q10) need an explicit reconciliation decision. One automatic reminder per month must remain idempotent.

## Required test-plan evidence

- Manager authorization and balance corrections are attributable; unauthorized input produces no change.
- Resident receives only permitted unit data; unrelated community receives nothing.
- Repeated reads/reminder runs create no charge and no duplicate reminder.
- Posted-payment suppression and month-boundary cases use a controlled clock and approved named settings.
- Non-posted receipt handling, arrears/allocation (Q11), fees (Q1) and ACH settlement (Q8) are not silently decided.
- No Stripe/provider credential, real charge or live email is introduced by fallback tests.

## Explicit dependencies and owners

COMC-52→COMC-21 is the cut-decision prerequisite. COMC-10 assignment/role contract is an authorization dependency. COMC-20 contains reminder behavior/policy and must be reconciled with current S7 AC23–25. Sandeep owns the payment/isolation gate and unresolved timing/payment semantics; Kundan reviews the reminder contract; Gustavo coordinates the fallback decision and package. No work is attributed to those people as completed.

COMC-8 remains an open product epic. Keep actual include/cut decision, review evidence and release capacity visible; do not activate this fallback merely because it is assigned to Gustavo. Once activated and policies are resolved, split balance entry/read from reminders and prepare exact tests-first implementation packets with migrations/recovery. No code or current acceptance/test/CI change is authorized by this readiness note.
