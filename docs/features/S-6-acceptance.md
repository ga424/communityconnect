# S-6 acceptance baseline

Draft requirements copied from COMC-17 on November 3, 2026. Human review remains pending.

Lead: Sandeep    
Reviewer: Kundan    
Scope: Milestone 1

## Source and current state

[Revised Milestone 1 review document attached to COMC-4](https://gkms.atlassian.net/browse/COMC-4), CS690_Milestone1_CommunityConnect_Review_v2.docx, November 3, 2026. This supersedes the October 27 planning scope; the earlier attachments remain historical.

Document drafted and quality-checked; human acceptance and repository execution are not established by this Jira update. Four interviews are real per Gustavo; preserve their supplied notes and corrected participation.

## Remaining work

As a resident, I want a scheduled dues payment and visible payment history so that I can avoid forgetting a monthly payment.

Trace: E-9, E-21; A-3, A-8    
Only local synchronous simulated results are in this design. ACH settlement (Q-8), fees (Q-1), real manual-payment overlap (Q-10) and arrears (Q-11) remain out of scope and undecided.

### AC-18

Given R1 owns the fixture unit and has no schedule, When R1 saves a test_card schedule for day 5 with a synthetic token, Then the schedule API returns day 5, method test_card and active true, without exposing the token.    
Trace: E-21; A-3, A-8

### AC-19

Given R1’s schedule was created before day 5, the unit has no payment for the test month and the fake processor succeeds, When the run executes on day 5, Then history contains one Paid payment for that month at DUES_AMOUNT_CENTS.    
Trace: E-21; A-8

### AC-20

Given the fake processor recorded success but the run stopped before saving Paid, When the run restarts for the same date, Then history has one Paid payment and the fake processor records only one charge for the attempt key.    
Trace: E-9; A-8

### AC-21

Given a manual payment is already recorded as Paid for the test month, When its scheduled run executes, Then no processor charge occurs and history still has one Paid payment.    
Trace: E-9; A-8

### AC-22

Given an attempt failed and another is allowed, When a run executes on the first eligible date RETRY_DELAY_DAYS later in the same month, Then history retains the Failed attempt and adds exactly one retry; the successful fixture retry is Paid.    
Trace: E-21; A-8

Planned tests:

* AC-18: tests/test_s6_payments.py::test_ac18_schedule_returned_without_token
* AC-19: tests/test_s6_payments.py::test_ac19_due_day_charges_exactly_once
* AC-20: tests/test_s6_payments.py::test_ac20_restart_mid_run_keeps_one_payment
* AC-21: tests/test_s6_payments.py::test_ac21_manual_payment_prevents_scheduled_charge
* AC-22: tests/test_s6_payments.py::test_ac22_declined_charge_retried_after_delay

M1 design/test-only. No S-6 implementation here. The previous Stripe integration intent remains future scope under COMC-8/52 and COMC-18/19; simulated success cannot validate a provider.

## Acceptance criteria

* Given the reviewed design and trace, when this story is assessed, then every listed AC maps to its planned test and its build/unbuilt scope is explicit.

## Completion evidence

Approved design, real tests and scoped implementation evidence; never close an unbuilt story as implemented.

Close only with linked artifacts and actual reviewer/check results. Use actual dates and SHAs; retain unresolved questions rather than inventing answers.
