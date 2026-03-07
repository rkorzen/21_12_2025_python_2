from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=200)
    credit_limit = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return f"{self.name} (limit: {self.credit_limit})"

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    issued_at = models.DateField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.name}:{self.issued_at.isoformat()}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return f"{self.name}: ({self.quantity} x {self.price})"


