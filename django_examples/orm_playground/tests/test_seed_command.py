from __future__ import annotations

import io

import pytest
from django.core.management import call_command

from people.models import Organization, Person


@pytest.mark.django_db
def test_seed_reset_assigns_valid_manager_ids_after_autoincrement_gaps():
    org = Organization.objects.create(name="Pre-seed Org", country_code="PL")
    Person.objects.bulk_create(
        [
            Person(
                email=f"preseed{idx:04d}@example.com",
                full_name=f"Preseed {idx:04d}",
                organization=org,
                country_code="PL",
            )
            for idx in range(120)
        ]
    )
    Person.objects.all().delete()

    call_command(
        "seed",
        seed=123,
        people=120,
        products=20,
        orders=80,
        event_logs=0,
        reset=True,
        stdout=io.StringIO(),
    )

    person_ids = set(Person.objects.values_list("id", flat=True))
    manager_ids = set(Person.objects.exclude(manager_id__isnull=True).values_list("manager_id", flat=True))

    assert len(person_ids) == 120
    assert manager_ids.issubset(person_ids)
