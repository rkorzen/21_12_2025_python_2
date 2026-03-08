"""
- wartosc wszystkich niezaplaconych faktur dla klienta
- ile kredytu zostalo do wykorzystania


"""
from decimal import Decimal

from django.db.models import (
    Sum, F, OuterRef, Subquery
)
from django.db.models.functions import Coalesce

from invoices.models import InvoiceItem, Customer

invoice_items = (
    InvoiceItem.objects.filter(
        invoice__customer=OuterRef("pk"),
        invoice__paid=False
    ).annotate(
        value=F("quantity") * F("price"),
    ).values("invoice__customer").annotate(total=Sum("value")).values("total")
)

qs = (
    Customer.objects.annotate(
        unpaid_total=Coalesce(Subquery(invoice_items), Decimal(0))
    ).annotate(
        available_credit=F("credit_limit") - F("unpaid_total"),

    )
)
