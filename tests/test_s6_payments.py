from datetime import date, datetime, timedelta, timezone
import pytest
from app import settings
from app.payments import RunInterrupted
from tests.s6_harness import PaymentHarness

pytestmark = pytest.mark.s6
MONTH = '2026-01'
DUE = date(2026, 1, 5)
CREATED = datetime(2026, 1, 1, tzinfo=timezone.utc)


def deferred(ac):
    return pytest.mark.skip(reason=f'{ac}: S-6 is intentionally unbuilt in M1; executable contract pending peer review')


@deferred('AC-18')
def test_ac18_schedule_returned_without_token():
    h = PaymentHarness()
    h.seed_resident(unit_id=11, created_at=CREATED)
    response = h.client.post('/communities/1/payment-schedules', headers={'X-User-Id': '1'},
        json={'method': 'test_card', 'day_of_month': 5, 'token': 'succeed'})
    assert response.status_code == 201
    body = response.json()
    assert body['day_of_month'] == 5 and body['method'] == 'test_card' and body['active'] is True
    assert 'token' not in body and 'succeed' not in response.text
    fetched = h.client.get('/communities/1/payment-schedules/mine', headers={'X-User-Id': '1'})
    assert fetched.status_code == 200 and 'token' not in fetched.json()


@deferred('AC-19')
def test_ac19_due_day_charges_exactly_once():
    h = PaymentHarness()
    h.seed_schedule(unit_id=11, created_at=CREATED, day=5, token='succeed')
    h.run(DUE)
    h.run(DUE)
    payments = h.history(unit_id=11, month=MONTH)
    assert len(payments) == 1 and payments[0]['status'] == 'Paid'
    assert payments[0]['billing_month'] == MONTH
    assert payments[0]['amount_cents'] == settings.DUES_AMOUNT_CENTS
    assert h.processor_charge_count() == 1


@deferred('AC-20')
def test_ac20_restart_mid_run_keeps_one_payment():
    h = PaymentHarness()
    h.seed_schedule(unit_id=11, created_at=CREATED, day=5, token='succeed')
    with pytest.raises(RunInterrupted):
        h.run(DUE, interrupt_after_processor=True)
    assert h.history(unit_id=11, month=MONTH)[0]['status'] == 'Pending'
    restarted = h.restart_application_and_reconnect()
    restarted.run(DUE)
    payments = restarted.history(unit_id=11, month=MONTH)
    assert len(payments) == 1 and payments[0]['status'] == 'Paid'
    assert restarted.processor_charge_count(key='11:2026-01:1') == 1


@deferred('AC-21')
def test_ac21_manual_payment_prevents_scheduled_charge():
    h = PaymentHarness()
    h.seed_schedule(unit_id=11, created_at=CREATED, day=5, token='succeed')
    h.seed_manual_paid(unit_id=11, month=MONTH, amount_cents=settings.DUES_AMOUNT_CENTS)
    h.run(DUE)
    payments = h.history(unit_id=11, month=MONTH)
    assert len(payments) == 1 and payments[0]['status'] == 'Paid'
    assert payments[0]['method'] == 'manual' and h.processor_charge_count() == 0


@deferred('AC-22')
def test_ac22_declined_charge_retried_after_delay():
    h = PaymentHarness()
    assert settings.MAX_PAYMENT_ATTEMPTS >= 2, 'This fixture requires another allowed attempt'
    retry_date = DUE + timedelta(days=settings.RETRY_DELAY_DAYS)
    assert retry_date.month == DUE.month, 'Choose fixture dates with room in the same month'
    h.seed_schedule(unit_id=11, created_at=CREATED, day=5, token='decline_first')
    h.run(DUE)
    h.run(retry_date - timedelta(days=1))
    assert [p['status'] for p in h.history(unit_id=11, month=MONTH)] == ['Failed']
    h.run(retry_date)
    h.run(retry_date)
    payments = h.history(unit_id=11, month=MONTH)
    assert [p['status'] for p in payments] == ['Failed', 'Paid']
    assert [p['attempt'] for p in payments] == [1, 2]
    assert h.processor_charge_count() == 2
