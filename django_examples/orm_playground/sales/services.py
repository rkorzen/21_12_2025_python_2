from __future__ import annotations

from django.db import connection, transaction
from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django.db.models.functions import Coalesce

from .models import Order, Payment


def capture_payment_atomically(order_external_ref: str, tx_id: str):
    """
    Demonstrates atomic + select_for_update. On SQLite select_for_update is ignored.
    """
    with transaction.atomic():
        order = (
            Order.objects.select_for_update()
            .filter(external_ref=order_external_ref)
            .select_related("customer")
            .first()
        )
        if order is None:
            raise Order.DoesNotExist(order_external_ref)

        total_amount = order.items.aggregate(
            total=Coalesce(
                Sum(
                    ExpressionWrapper(
                        F("quantity") * F("unit_price"),
                        output_field=DecimalField(max_digits=14, decimal_places=2),
                    )
                ),
                0,
            )
        )["total"]

        Payment.objects.create(
            external_order_ref=order.external_ref,
            status=Payment.Status.PAID,
            amount=total_amount,
            provider="manual",
            transaction_id=tx_id,
        )


def select_for_update_supported() -> bool:
    return connection.features.has_select_for_update
