from __future__ import annotations

from django.template.loader import get_template


def test_homepage_has_report_links(client):
    template = get_template("core/home.html")

    response = client.get("/")

    assert template is not None
    assert response.status_code == 200
    content = response.content.decode()

    assert "przykladowe raporty" in content
    assert "/reports/html/top-products/" in content
    assert "/reports/html/customers-ltv/" in content
    assert "/reports/html/orders-with-late-payment/" in content
    assert "/reports/html/events-matched-by-email/" in content
    assert "/reports/html/n-plus-one-demo/" in content
    assert "/reports/html/window-rankings/" in content
    assert "/reports/top-products/" in content
    assert "/reports/customers-ltv/" in content
    assert "/reports/orders-with-late-payment/" in content
    assert "/reports/events-matched-by-email/" in content
    assert "/reports/n-plus-one-demo/" in content
    assert "/reports/window-rankings/" in content
