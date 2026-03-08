from __future__ import annotations

import csv
import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from catalog.models import Category, Product
from people.models import Organization, Person
from sales.models import Payment


class Command(BaseCommand):
    help = "Import CSV/JSON demo data (people, products, payments)."

    def add_arguments(self, parser):
        parser.add_argument("--path", required=True)
        parser.add_argument(
            "--entity",
            required=True,
            choices=["people", "products", "payments"],
        )

    def handle(self, *args, **options):
        path = Path(options["path"])
        entity = options["entity"]

        if not path.exists():
            raise CommandError(f"Path does not exist: {path}")

        rows = self._read_rows(path)
        if entity == "people":
            created = self._import_people(rows)
        elif entity == "products":
            created = self._import_products(rows)
        else:
            created = self._import_payments(rows)

        self.stdout.write(self.style.SUCCESS(f"Imported {created} records for '{entity}'"))

    def _read_rows(self, path: Path):
        if path.suffix.lower() == ".json":
            data = json.loads(path.read_text())
            if not isinstance(data, list):
                raise CommandError("JSON file must contain a list of objects")
            return data

        if path.suffix.lower() == ".csv":
            with path.open(newline="") as file_obj:
                return list(csv.DictReader(file_obj))

        raise CommandError("Only .csv and .json files are supported")

    def _import_people(self, rows):
        created = 0
        default_org, _ = Organization.objects.get_or_create(name="Imported Org", country_code="PL")
        for row in rows:
            _, was_created = Person.objects.get_or_create(
                email=row["email"],
                defaults={
                    "full_name": row.get("full_name") or row["email"].split("@")[0],
                    "organization_id": row.get("organization_id") or default_org.id,
                    "country_code": row.get("country_code", "PL"),
                    "source_system_id": row.get("source_system_id", "IMPORT"),
                },
            )
            created += int(was_created)
        return created

    def _import_products(self, rows):
        created = 0
        default_cat, _ = Category.objects.get_or_create(name="Imported", parent=None)
        for row in rows:
            _, was_created = Product.objects.get_or_create(
                sku=row["sku"],
                defaults={
                    "name": row.get("name", row["sku"]),
                    "category_id": row.get("category_id") or default_cat.id,
                    "base_price": row.get("base_price", "0"),
                    "country_code": row.get("country_code", "PL"),
                    "source_system_id": row.get("source_system_id", "IMPORT"),
                    "is_active": str(row.get("is_active", "1")) in {"1", "true", "True"},
                },
            )
            created += int(was_created)
        return created

    def _import_payments(self, rows):
        created = 0
        for row in rows:
            _, was_created = Payment.objects.get_or_create(
                transaction_id=row["transaction_id"],
                defaults={
                    "external_order_ref": row["external_order_ref"],
                    "status": row.get("status", Payment.Status.PENDING),
                    "amount": row.get("amount", "0"),
                    "provider": row.get("provider", "import"),
                    "source_system_id": row.get("source_system_id", "IMPORT"),
                },
            )
            created += int(was_created)
        return created
