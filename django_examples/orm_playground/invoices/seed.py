import random
from decimal import Decimal

from django.utils import timezone

from .models import Customer, Invoice, InvoiceItem

customers = []

for i in range(10):
    c = Customer.objects.create(
        name=f"Customer {i}",
        credit_limit = Decimal(random.randint(5000, 20000))
    )
    customers.append(c)

def create_invoice_item(invoice):
    InvoiceItem.objects.create(
        invoice=invoice,
        name="Product",
        quantity=random.randint(1, 10),
        price=Decimal(random.randint(10, 200))
    )

def create_invoice(customer):
    invoice = Invoice.objects.create(
        customer=customer,
        issued_at=timezone.now().date(),
        paid=random.choice([True, False])
    )
    return invoice

for c in customers:
    for _ in range(random.randint(2, 6)):
        inv = create_invoice(c)
        for __ in range(random.randint(1, 5)):
            create_invoice_item(inv)