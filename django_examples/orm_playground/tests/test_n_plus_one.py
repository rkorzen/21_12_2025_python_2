from __future__ import annotations

from decimal import Decimal

import pytest

from catalog.models import Category, Product
from people.models import Organization, Person
from reporting import services
from sales.models import Order, OrderItem


@pytest.mark.django_db
def test_select_related_and_prefetch_reduce_queries(django_assert_num_queries):
    category = Category.objects.create(name="N+1")

    for idx in range(2):
        org = Organization.objects.create(name=f"Org {idx}", country_code="PL")
        person = Person.objects.create(
            email=f"person{idx}@example.com",
            full_name=f"Person {idx}",
            organization=org,
            country_code="PL",
        )
        order = Order.objects.create(external_ref=f"ORD-{idx}", customer=person, country_code="PL")

        for product_idx in range(2):
            product = Product.objects.create(
                sku=f"SKU-{idx}-{product_idx}",
                name=f"Product {idx}-{product_idx}",
                category=category,
                base_price=Decimal("50.00"),
                country_code="PL",
            )
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=1,
                unit_price=Decimal("50.00"),
            )

    with django_assert_num_queries(11):
        services.serialize_orders_naive(limit=2)

    with django_assert_num_queries(2):
        services.serialize_orders_optimized(limit=2)
