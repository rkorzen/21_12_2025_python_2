from __future__ import annotations

import pytest


@pytest.mark.django_db
def test_reports_home_lists_html_report_links(client):
    response = client.get("/reports/")

    assert response.status_code == 200
    content = response.content.decode()
    assert "/reports/html/top-products/" in content
    assert "/reports/html/customers-ltv/" in content
    assert "/reports/html/orders-with-late-payment/" in content
    assert "/reports/html/events-matched-by-email/" in content
    assert "/reports/html/n-plus-one-demo/" in content
    assert "/reports/html/window-rankings/" in content


@pytest.mark.django_db
def test_top_products_html_has_preset_buttons_and_json_link(client):
    response = client.get("/reports/html/top-products/")

    assert response.status_code == 200
    content = response.content.decode()
    assert "7 dni" in content
    assert "days=7" in content
    assert "country=PL" in content
    assert "/reports/top-products/" in content


@pytest.mark.django_db
def test_n_plus_one_html_has_clickable_presets(client):
    response = client.get("/reports/html/n-plus-one-demo/")

    assert response.status_code == 200
    content = response.content.decode()
    assert "limit=10" in content
    assert "limit=20" in content
    assert "limit=50" in content
