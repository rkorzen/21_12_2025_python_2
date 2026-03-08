from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

import pytest
from django.utils import timezone

from catalog.models import Category, Product
from events.models import EventLog
from people.models import Organization, Person
from reporting import services
from sales.models import Order, Payment


@pytest.mark.django_db
def test_events_matched_by_email_query_uses_exists_and_subquery():
    now = timezone.now()
    org = Organization.objects.create(name="Org", country_code="PL")
    person = Person.objects.create(
        email="person@example.com",
        full_name="Person",
        organization=org,
        country_code="PL",
    )

    EventLog.objects.create(
        actor_email="person@example.com",
        event_type=EventLog.EventType.LOGIN,
        happened_at=now - timedelta(hours=1),
        country_code="PL",
    )
    EventLog.objects.create(
        actor_email="unknown@example.com",
        event_type=EventLog.EventType.LOGIN,
        happened_at=now - timedelta(hours=1),
        country_code="PL",
    )

    rows = list(services.events_matched_by_email_queryset(days=2))

    assert len(rows) == 1
    assert rows[0].matched_person_id == person.id
    assert rows[0].matched_person_name == "Person"


@pytest.mark.django_db
def test_orders_with_late_payment_query_matches_by_external_ref():
    now = timezone.now()
    org = Organization.objects.create(name="Org2", country_code="PL")
    person = Person.objects.create(
        email="customer@example.com",
        full_name="Customer",
        organization=org,
        country_code="PL",
    )

    category = Category.objects.create(name="Category")
    Product.objects.create(
        sku="SKU-2",
        name="Product 2",
        category=category,
        base_price=Decimal("99.00"),
        country_code="PL",
    )

    late_order = Order.objects.create(
        external_ref="ORD-LATE",
        customer=person,
        country_code="PL",
        created_at=now - timedelta(days=10),
    )
    on_time_order = Order.objects.create(
        external_ref="ORD-OK",
        customer=person,
        country_code="PL",
        created_at=now - timedelta(days=10),
    )

    Payment.objects.create(
        external_order_ref="ORD-LATE",
        status=Payment.Status.PAID,
        amount=Decimal("120.00"),
        paid_at=late_order.created_at + timedelta(days=5),
        provider="stripe",
        transaction_id="TX-LATE",
    )
    Payment.objects.create(
        external_order_ref="ORD-OK",
        status=Payment.Status.PAID,
        amount=Decimal("120.00"),
        paid_at=on_time_order.created_at + timedelta(days=1),
        provider="stripe",
        transaction_id="TX-OK",
    )

    rows = list(services.orders_with_late_payment_queryset(days=30, grace_days=3))

    assert len(rows) == 1
    assert rows[0].external_ref == "ORD-LATE"
    assert rows[0].has_payment is True
    assert rows[0].late_payment is True
