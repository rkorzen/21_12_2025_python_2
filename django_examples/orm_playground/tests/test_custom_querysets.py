from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

import pytest
from django.utils import timezone

from catalog.models import Category, InventorySnapshot, Product
from people.models import Organization, Person
from sales.models import Order, OrderItem


@pytest.mark.django_db
def test_person_and_product_custom_querysets():
    now = timezone.now()
    org_pl = Organization.objects.create(name="Org PL", country_code="PL")
    org_us = Organization.objects.create(name="Org US", country_code="US")

    person_pl = Person.objects.create(
        email="anna@example.com",
        full_name="Anna",
        organization=org_pl,
        country_code="PL",
        is_active=True,
        is_deleted=False,
    )
    Person.objects.create(
        email="john@example.com",
        full_name="John",
        organization=org_us,
        country_code="US",
        is_active=True,
        is_deleted=True,
    )

    category = Category.objects.create(name="Root")
    product = Product.objects.create(
        sku="SKU-1",
        name="Product 1",
        category=category,
        base_price=Decimal("100.00"),
        country_code="PL",
    )
    InventorySnapshot.objects.create(
        sku=product.sku,
        captured_at=now - timedelta(days=1),
        available_qty=5,
        reserved_qty=1,
        warehouse_code="WH-1",
    )
    InventorySnapshot.objects.create(
        sku=product.sku,
        captured_at=now,
        available_qty=9,
        reserved_qty=0,
        warehouse_code="WH-1",
    )

    order = Order.objects.create(
        external_ref="ORD-001",
        customer=person_pl,
        country_code="PL",
        created_at=now - timedelta(days=2),
    )
    OrderItem.objects.create(order=order, product=product, quantity=2, unit_price=Decimal("15.00"))

    active_people = Person.objects.active().in_country("PL")
    assert list(active_people.values_list("email", flat=True)) == ["anna@example.com"]

    person_with_spend = Person.objects.with_total_spend().get(pk=person_pl.pk)
    assert person_with_spend.total_spend == Decimal("30")

    product_with_inventory = Product.objects.with_latest_inventory_qty().get(pk=product.pk)
    assert product_with_inventory.latest_inventory_qty == 9
