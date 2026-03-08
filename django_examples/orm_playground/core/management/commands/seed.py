from __future__ import annotations

import random
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import DecimalField, ExpressionWrapper, F, Sum, Value
from django.db.models.functions import Coalesce
from django.utils import timezone

from catalog.models import Category, InventorySnapshot, Product, Tag
from events.models import EventLog
from people.models import Organization, Person, PersonRole, Role
from sales.models import Order, OrderItem, Payment


class Command(BaseCommand):
    help = "Seed deterministic demo data for ORM playground"

    def add_arguments(self, parser):
        parser.add_argument("--seed", type=int, default=123)
        parser.add_argument("--people", type=int, default=1_200)
        parser.add_argument("--products", type=int, default=600)
        parser.add_argument("--orders", type=int, default=5_000)
        parser.add_argument("--event-logs", type=int, default=50_000)
        parser.add_argument("--reset", action="store_true")

    @transaction.atomic
    def handle(self, *args, **options):
        rng = random.Random(options["seed"])
        now = timezone.now()

        if options["reset"]:
            self.stdout.write("Resetting existing demo data...")
            EventLog.objects.all().delete()
            Payment.objects.all().delete()
            OrderItem.objects.all().delete()
            Order.objects.all().delete()
            InventorySnapshot.objects.all().delete()
            Product.tags.through.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            Tag.objects.all().delete()
            PersonRole.objects.all().delete()
            Person.objects.all().delete()
            Role.objects.all().delete()
            Organization.objects.all().delete()

        countries = ["PL", "US", "DE", "FR", "GB", "ES"]
        organizations = [
            Organization(name=f"Org {idx:02d}", country_code=countries[idx % len(countries)])
            for idx in range(1, 25)
        ]
        Organization.objects.bulk_create(organizations, ignore_conflicts=True)
        orgs = list(Organization.objects.order_by("id"))

        role_defs = [
            ("admin", "Admin"),
            ("manager", "Manager"),
            ("analyst", "Analyst"),
            ("buyer", "Buyer"),
            ("guest", "Guest"),
        ]
        Role.objects.bulk_create([Role(code=code, label=label) for code, label in role_defs], ignore_conflicts=True)
        roles = list(Role.objects.order_by("id"))

        self.stdout.write("Generating people...")
        people = []
        for idx in range(options["people"]):
            org = rng.choice(orgs)
            people.append(
                Person(
                    email=f"person{idx:05d}@example.com",
                    full_name=f"Person {idx:05d}",
                    organization_id=org.id,
                    country_code=org.country_code,
                    is_active=rng.random() > 0.05,
                    is_deleted=rng.random() < 0.02,
                    source_system_id="CRM",
                    joined_at=(now - timedelta(days=rng.randint(30, 1200))).date(),
                )
            )
        Person.objects.bulk_create(people, batch_size=2_000, ignore_conflicts=True)
        people = list(Person.objects.order_by("id"))

        # Managers are assigned after ids are available.
        # Pick only from real previously created ids because SQLite autoincrement
        # may leave gaps after reset and deleted rows.
        prior_person_ids: list[int] = []
        for person in people:
            if person.id:
                if len(prior_person_ids) >= 10 and rng.random() < 0.7:
                    person.manager_id = rng.choice(prior_person_ids)
                prior_person_ids.append(person.id)
        Person.objects.bulk_update(people, ["manager"], batch_size=2_000)

        person_roles = []
        for person in people:
            assigned_roles = rng.sample(roles, k=rng.randint(1, min(2, len(roles))))
            for role in assigned_roles:
                person_roles.append(
                    PersonRole(
                        person_id=person.id,
                        role_id=role.id,
                        organization_id=person.organization_id,
                        source_system_id="IAM",
                    )
                )
        PersonRole.objects.bulk_create(person_roles, batch_size=5_000, ignore_conflicts=True)

        self.stdout.write("Generating catalog...")
        root_names = ["Electronics", "Home", "Books", "Sports", "Beauty", "Office"]
        roots = [Category(name=name) for name in root_names]
        Category.objects.bulk_create(roots, ignore_conflicts=True)
        roots = list(Category.objects.filter(parent__isnull=True).order_by("id"))

        child_categories = []
        for root in roots:
            for suffix in ["A", "B"]:
                child_categories.append(Category(name=f"{root.name} {suffix}", parent_id=root.id))
        Category.objects.bulk_create(child_categories, ignore_conflicts=True)
        categories = list(Category.objects.order_by("id"))

        tags = [Tag(name=name) for name in ["new", "promo", "featured", "eco", "premium", "clearance"]]
        Tag.objects.bulk_create(tags, ignore_conflicts=True)
        tags = list(Tag.objects.order_by("id"))

        products = []
        for idx in range(options["products"]):
            category = rng.choice(categories)
            products.append(
                Product(
                    sku=f"SKU-{idx:05d}",
                    name=f"Product {idx:05d}",
                    category_id=category.id,
                    base_price=Decimal(str(rng.uniform(5, 2000))).quantize(
                        Decimal("0.01"),
                        rounding=ROUND_HALF_UP,
                    ),
                    country_code=rng.choice(countries),
                    source_system_id="PIM",
                    is_active=rng.random() > 0.03,
                )
            )
        Product.objects.bulk_create(products, batch_size=2_000, ignore_conflicts=True)
        products = list(Product.objects.order_by("id"))

        through_rows = []
        through_model = Product.tags.through
        for product in products:
            for tag in rng.sample(tags, k=rng.randint(0, min(3, len(tags)))):
                through_rows.append(through_model(product_id=product.id, tag_id=tag.id))
        through_model.objects.bulk_create(through_rows, batch_size=5_000, ignore_conflicts=True)

        snapshots = []
        for product in products:
            for day_offset in range(0, 8):
                snapshots.append(
                    InventorySnapshot(
                        sku=product.sku,
                        captured_at=now - timedelta(days=day_offset, hours=rng.randint(0, 23)),
                        available_qty=rng.randint(0, 1_000),
                        reserved_qty=rng.randint(0, 200),
                        warehouse_code=f"WH-{rng.randint(1, 4)}",
                    )
                )
        InventorySnapshot.objects.bulk_create(snapshots, batch_size=5_000)

        self.stdout.write("Generating orders and items...")
        order_statuses = [Order.Status.CONFIRMED, Order.Status.SHIPPED, Order.Status.CANCELLED]
        orders = []
        for idx in range(options["orders"]):
            customer = rng.choice(people)
            orders.append(
                Order(
                    external_ref=f"ORD-{options['seed']}-{idx:06d}",
                    customer_id=customer.id,
                    status=rng.choices(order_statuses, weights=[0.6, 0.3, 0.1], k=1)[0],
                    country_code=customer.country_code,
                    source_system_id="OMS",
                    created_at=now
                    - timedelta(
                        days=rng.randint(0, 120),
                        hours=rng.randint(0, 23),
                        minutes=rng.randint(0, 59),
                    ),
                )
            )
        Order.objects.bulk_create(orders, batch_size=2_000, ignore_conflicts=True)

        orders = list(Order.objects.order_by("id").values("id", "external_ref", "created_at", "country_code"))
        product_rows = list(Product.objects.order_by("id").values("id", "base_price"))
        product_ids = [row["id"] for row in product_rows]
        price_by_product = {row["id"]: row["base_price"] for row in product_rows}

        order_items = []
        for order in orders:
            item_count = rng.randint(3, 9)
            for product_id in rng.sample(product_ids, k=item_count):
                base_price = price_by_product[product_id]
                unit_price = (base_price * Decimal(str(rng.uniform(0.75, 1.25)))).quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP,
                )
                order_items.append(
                    OrderItem(
                        order_id=order["id"],
                        product_id=product_id,
                        quantity=rng.randint(1, 5),
                        unit_price=max(unit_price, Decimal("0.10")),
                        discount_pct=Decimal(rng.choice([0, 0, 0, 5, 10, 15])),
                    )
                )
        OrderItem.objects.bulk_create(order_items, batch_size=5_000)

        totals_query = (
            OrderItem.objects.values("order_id")
            .annotate(
                total=Coalesce(
                    Sum(
                        ExpressionWrapper(
                            F("quantity") * F("unit_price"),
                            output_field=DecimalField(max_digits=14, decimal_places=2),
                        )
                    ),
                    Value(Decimal("0.00")),
                )
            )
            .values_list("order_id", "total")
        )
        totals_by_order = dict(totals_query)

        payments = []
        for idx, order in enumerate(orders):
            if rng.random() > 0.92:
                continue
            status = rng.choices(
                [Payment.Status.PAID, Payment.Status.PENDING, Payment.Status.FAILED],
                weights=[0.82, 0.13, 0.05],
                k=1,
            )[0]
            paid_at = None
            if status == Payment.Status.PAID:
                paid_at = order["created_at"] + timedelta(hours=rng.randint(1, 168))

            payments.append(
                Payment(
                    external_order_ref=order["external_ref"],
                    status=status,
                    amount=totals_by_order.get(order["id"], Decimal("0.00")),
                    paid_at=paid_at,
                    provider=rng.choice(["stripe", "adyen", "paypal"]),
                    transaction_id=f"TX-{options['seed']}-{idx:06d}",
                    source_system_id="PSP",
                )
            )
        Payment.objects.bulk_create(payments, batch_size=5_000, ignore_conflicts=True)

        self.stdout.write("Generating event logs...")
        person_emails = list(Person.objects.values_list("email", flat=True))
        person_ids = list(Person.objects.values_list("id", flat=True))
        order_ids = [row["id"] for row in orders]
        limited_product_ids = product_ids[: min(len(product_ids), 5_000)]

        person_ct = ContentType.objects.get_for_model(Person)
        order_ct = ContentType.objects.get_for_model(Order)
        product_ct = ContentType.objects.get_for_model(Product)

        event_types = [
            EventLog.EventType.LOGIN,
            EventLog.EventType.ORDER_PLACED,
            EventLog.EventType.PAYMENT_UPDATED,
            EventLog.EventType.PROFILE_UPDATED,
        ]

        buffer = []
        for idx in range(options["event_logs"]):
            matched = rng.random() < 0.8
            actor_email = rng.choice(person_emails) if matched else f"external{idx:06d}@other.test"
            target_choice = rng.choice(["person", "order", "product", "none"])

            content_type_id = None
            object_id = None
            if target_choice == "person" and person_ids:
                content_type_id = person_ct.id
                object_id = rng.choice(person_ids)
            elif target_choice == "order" and order_ids:
                content_type_id = order_ct.id
                object_id = rng.choice(order_ids)
            elif target_choice == "product" and limited_product_ids:
                content_type_id = product_ct.id
                object_id = rng.choice(limited_product_ids)

            buffer.append(
                EventLog(
                    actor_email=actor_email,
                    event_type=rng.choice(event_types),
                    happened_at=now
                    - timedelta(
                        days=rng.randint(0, 120),
                        minutes=rng.randint(0, 59),
                        seconds=rng.randint(0, 59),
                    ),
                    payload={"idx": idx, "matched": matched},
                    country_code=rng.choice(countries),
                    source_system_id="TRACKER",
                    content_type_id=content_type_id,
                    object_id=object_id,
                )
            )

            if len(buffer) >= 5_000:
                EventLog.objects.bulk_create(buffer, batch_size=5_000)
                buffer = []

        if buffer:
            EventLog.objects.bulk_create(buffer, batch_size=5_000)

        self.stdout.write(
            self.style.SUCCESS(
                "Seed complete: "
                f"people={Person.objects.count()}, products={Product.objects.count()}, "
                f"orders={Order.objects.count()}, order_items={OrderItem.objects.count()}, "
                f"payments={Payment.objects.count()}, event_logs={EventLog.objects.count()}"
            )
        )
