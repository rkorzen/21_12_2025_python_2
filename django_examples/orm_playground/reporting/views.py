"""Widoki raportowe: JSON API i prezentacja HTML z presetami parametrów."""

from __future__ import annotations

import json
from urllib.parse import urlencode

from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from core.utils import query_debugger

from . import services


def _int_param(request, key: str, default: int, min_value: int = 1, max_value: int = 10_000):
    """Bezpiecznie odczytuje parametr liczbowy z query stringa."""
    raw = request.GET.get(key)
    if raw is None:
        return default
    try:
        parsed = int(raw)
    except ValueError:
        return default
    return max(min(parsed, max_value), min_value)


def _build_response(*, description: str, params: dict, rows, total: int, page: int, page_size: int):
    """Buduje spójny format odpowiedzi używany przez wszystkie raporty JSON."""
    return {
        "description": description,
        "params": params,
        "results": rows,
        "metrics": {
            "total_records": total,
            "returned_records": len(rows),
            "page": page,
            "page_size": page_size,
        },
    }


def _top_products_payload(request):
    """Zwraca payload raportu `top_products` niezależnie od formatu odpowiedzi."""
    days = _int_param(request, "days", 30)
    page = _int_param(request, "page", 1)
    page_size = _int_param(request, "page_size", 20, max_value=100)
    country = request.GET.get("country")

    with query_debugger() as dbg:
        queryset = services.top_products_queryset(days=days, country=country)
        total, rows = services.paginate_queryset(queryset, page, page_size)
        payload = _build_response(
            description="Top products by revenue in the requested period.",
            params={"days": days, "country": country, "page": page, "page_size": page_size},
            rows=rows,
            total=total,
            page=page,
            page_size=page_size,
        )

    payload["metrics"] |= dbg
    return payload


def _customers_ltv_payload(request):
    """Zwraca payload raportu LTV klientów."""
    days = _int_param(request, "days", 180)
    page = _int_param(request, "page", 1)
    page_size = _int_param(request, "page_size", 20, max_value=100)
    country = request.GET.get("country")

    with query_debugger() as dbg:
        queryset = services.customers_ltv_queryset(days=days, country=country).values(
            "id",
            "email",
            "full_name",
            "country_code",
            "ltv",
            "orders_count",
        )
        total, rows = services.paginate_queryset(queryset, page, page_size)
        payload = _build_response(
            description="Customer LTV computed with FilteredRelation and aggregate expressions.",
            params={"days": days, "country": country, "page": page, "page_size": page_size},
            rows=rows,
            total=total,
            page=page,
            page_size=page_size,
        )

    payload["metrics"] |= dbg
    return payload


def _orders_with_late_payment_payload(request):
    """Zwraca payload raportu zamówień z opóźnioną płatnością."""
    days = _int_param(request, "days", 60)
    page = _int_param(request, "page", 1)
    page_size = _int_param(request, "page_size", 20, max_value=100)
    grace_days = _int_param(request, "grace_days", 3)
    country = request.GET.get("country")

    with query_debugger() as dbg:
        queryset = services.orders_with_late_payment_queryset(
            days=days,
            country=country,
            grace_days=grace_days,
        ).values(
            "external_ref",
            "country_code",
            "created_at",
            "first_paid_at",
            "first_paid_amount",
            "has_payment",
            "late_payment",
        )
        total, rows = services.paginate_queryset(queryset, page, page_size)
        payload = _build_response(
            description="Pseudo-join Payment -> Order by external reference with Subquery/Exists.",
            params={
                "days": days,
                "country": country,
                "grace_days": grace_days,
                "page": page,
                "page_size": page_size,
            },
            rows=rows,
            total=total,
            page=page,
            page_size=page_size,
        )

    payload["metrics"] |= dbg
    return payload


def _events_matched_by_email_payload(request):
    """Zwraca payload raportu dopasowań EventLog -> Person po e-mailu."""
    days = _int_param(request, "days", 30)
    page = _int_param(request, "page", 1)
    page_size = _int_param(request, "page_size", 20, max_value=100)
    country = request.GET.get("country")

    with query_debugger() as dbg:
        queryset = services.events_matched_by_email_queryset(days=days, country=country).values(
            "id",
            "event_type",
            "actor_email",
            "matched_person_id",
            "matched_person_name",
            "happened_at",
            "country_code",
        )
        total, rows = services.paginate_queryset(queryset, page, page_size)
        payload = _build_response(
            description="Pseudo-join EventLog -> Person by email using Exists + Subquery.",
            params={"days": days, "country": country, "page": page, "page_size": page_size},
            rows=rows,
            total=total,
            page=page,
            page_size=page_size,
        )

    payload["metrics"] |= dbg
    return payload


def _n_plus_one_demo_payload(request):
    """Zwraca payload demonstracji problemu N+1."""
    limit = _int_param(request, "limit", 20, max_value=100)

    with query_debugger() as dbg:
        rows = services.n_plus_one_demo(limit=limit)
        payload = {
            "description": "N+1 comparison: naive queryset vs select_related + prefetch_related.",
            "params": {"limit": limit},
            "results": rows,
            "metrics": {},
        }

    payload["metrics"] |= dbg
    return payload


def _window_rankings_payload(request):
    """Zwraca payload raportu z funkcjami okna."""
    days = _int_param(request, "days", 90)
    page = _int_param(request, "page", 1)
    page_size = _int_param(request, "page_size", 20, max_value=100)

    with query_debugger() as dbg:
        queryset = services.window_rankings_queryset(days=days).values(
            "external_ref",
            "customer__full_name",
            "order_total",
            "rank",
            "row_number",
            "running_total",
        )
        total, rows = services.paginate_queryset(queryset, page, page_size)
        payload = _build_response(
            description="Window functions: rank/row number/running total over order totals.",
            params={"days": days, "page": page, "page_size": page_size},
            rows=rows,
            total=total,
            page=page,
            page_size=page_size,
        )

    payload["metrics"] |= dbg
    return payload


def _report_cards():
    """Konfiguracja kart raportów na stronie listy `/reports/`."""
    return [
        {
            "title": "Top products",
            "description": "Najlepiej sprzedajace sie produkty wedlug przychodu.",
            "html_url": reverse("top_products_page"),
            "json_url": reverse("top_products"),
        },
        {
            "title": "Customers LTV",
            "description": "Lifetime value klientow i liczba ich zamowien.",
            "html_url": reverse("customers_ltv_page"),
            "json_url": reverse("customers_ltv"),
        },
        {
            "title": "Orders with late payment",
            "description": "Zamowienia z opozniona platnoscia.",
            "html_url": reverse("orders_with_late_payment_page"),
            "json_url": reverse("orders_with_late_payment"),
        },
        {
            "title": "Events matched by email",
            "description": "Dopasowanie logow zdarzen do osoby po e-mailu.",
            "html_url": reverse("events_matched_by_email_page"),
            "json_url": reverse("events_matched_by_email"),
        },
        {
            "title": "N+1 demo",
            "description": "Porownanie liczby zapytan: wariant naiwny vs zoptymalizowany.",
            "html_url": reverse("n_plus_one_demo_page"),
            "json_url": reverse("n_plus_one_demo"),
        },
        {
            "title": "Window rankings",
            "description": "Ranking i sumy narastajace z funkcjami okna.",
            "html_url": reverse("window_rankings_page"),
            "json_url": reverse("window_rankings"),
        },
    ]


def _preset_links(request, presets):
    """Buduje URL-e przycisków presetów parametrów dla widoku HTML."""
    links = []
    for label, params in presets:
        query = urlencode(params)
        url = request.path if not query else f"{request.path}?{query}"
        links.append({"label": label, "url": url})
    return links


def _json_link(request, json_url_name: str):
    """Generuje link do endpointu JSON z tym samym query stringiem."""
    query = request.GET.urlencode()
    url = reverse(json_url_name)
    if query:
        return f"{url}?{query}"
    return url


def _report_page(request, *, title: str, payload: dict, presets, json_url_name: str):
    """Renderuje uniwersalny widok HTML raportu (tabela + metryki + raw JSON)."""
    results = payload["results"]
    has_tabular_results = (
        isinstance(results, list)
        and len(results) > 0
        and all(isinstance(row, dict) for row in results)
    )

    columns = list(results[0].keys()) if has_tabular_results else []
    table_rows = []
    if has_tabular_results:
        for row in results:
            table_rows.append([row.get(column) for column in columns])

    scalar_items = []
    nested_items = []
    if isinstance(results, dict):
        for key, value in results.items():
            if isinstance(value, (list, dict)):
                nested_items.append(
                    {
                        "key": key,
                        "json": json.dumps(value, default=str, indent=2),
                    }
                )
            else:
                scalar_items.append({"key": key, "value": value})

    context = {
        "title": title,
        "description": payload["description"],
        "params": payload["params"],
        "metrics": payload["metrics"],
        "preset_links": _preset_links(request, presets),
        "json_url": _json_link(request, json_url_name),
        "has_tabular_results": has_tabular_results,
        "columns": columns,
        "table_rows": table_rows,
        "scalar_items": scalar_items,
        "nested_items": nested_items,
        "results_json": json.dumps(results, default=str, indent=2),
    }
    return render(request, "reporting/report_page.html", context)


def reports_home(request):
    """Strona główna modułu raportowego (katalog raportów HTML)."""
    return render(request, "reporting/reports_home.html", {"reports": _report_cards()})


def top_products(request):
    """JSON API: top produkty."""
    return JsonResponse(_top_products_payload(request))


def customers_ltv(request):
    """JSON API: LTV klientów."""
    return JsonResponse(_customers_ltv_payload(request))


def orders_with_late_payment(request):
    """JSON API: zamówienia z opóźnioną płatnością."""
    return JsonResponse(_orders_with_late_payment_payload(request))


def events_matched_by_email(request):
    """JSON API: eventy dopasowane po e-mailu."""
    return JsonResponse(_events_matched_by_email_payload(request))


def n_plus_one_demo(request):
    """JSON API: porównanie liczby zapytań (N+1)."""
    return JsonResponse(_n_plus_one_demo_payload(request))


def window_rankings(request):
    """JSON API: ranking z funkcjami okna."""
    return JsonResponse(_window_rankings_payload(request))


def top_products_page(request):
    """HTML: raport top produktów z gotowymi presetami."""
    return _report_page(
        request,
        title="Top products",
        payload=_top_products_payload(request),
        presets=[
            ("7 dni", {"days": 7, "page_size": 20}),
            ("30 dni PL", {"days": 30, "country": "PL", "page_size": 20}),
            ("90 dni US", {"days": 90, "country": "US", "page_size": 20}),
        ],
        json_url_name="top_products",
    )


def customers_ltv_page(request):
    """HTML: raport LTV klientów z presetami."""
    return _report_page(
        request,
        title="Customers LTV",
        payload=_customers_ltv_payload(request),
        presets=[
            ("60 dni", {"days": 60, "page_size": 20}),
            ("180 dni PL", {"days": 180, "country": "PL", "page_size": 20}),
            ("365 dni", {"days": 365, "page_size": 20}),
        ],
        json_url_name="customers_ltv",
    )


def orders_with_late_payment_page(request):
    """HTML: raport opóźnionych płatności z presetami."""
    return _report_page(
        request,
        title="Orders with late payment",
        payload=_orders_with_late_payment_payload(request),
        presets=[
            ("30 dni grace=2", {"days": 30, "grace_days": 2, "page_size": 20}),
            ("60 dni grace=3", {"days": 60, "grace_days": 3, "page_size": 20}),
            ("90 dni PL grace=5", {"days": 90, "country": "PL", "grace_days": 5, "page_size": 20}),
        ],
        json_url_name="orders_with_late_payment",
    )


def events_matched_by_email_page(request):
    """HTML: raport dopasowania eventów po e-mailu z presetami."""
    return _report_page(
        request,
        title="Events matched by email",
        payload=_events_matched_by_email_payload(request),
        presets=[
            ("7 dni", {"days": 7, "page_size": 20}),
            ("30 dni", {"days": 30, "page_size": 20}),
            ("90 dni DE", {"days": 90, "country": "DE", "page_size": 20}),
        ],
        json_url_name="events_matched_by_email",
    )


def n_plus_one_demo_page(request):
    """HTML: demo N+1 z presetami limitu."""
    return _report_page(
        request,
        title="N+1 demo",
        payload=_n_plus_one_demo_payload(request),
        presets=[
            ("limit 10", {"limit": 10}),
            ("limit 20", {"limit": 20}),
            ("limit 50", {"limit": 50}),
        ],
        json_url_name="n_plus_one_demo",
    )


def window_rankings_page(request):
    """HTML: raport rankingów okienkowych z presetami zakresu dni."""
    return _report_page(
        request,
        title="Window rankings",
        payload=_window_rankings_payload(request),
        presets=[
            ("30 dni", {"days": 30, "page_size": 20}),
            ("90 dni", {"days": 90, "page_size": 20}),
            ("365 dni", {"days": 365, "page_size": 20}),
        ],
        json_url_name="window_rankings",
    )
