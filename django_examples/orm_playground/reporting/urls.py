from django.urls import path

from . import views

urlpatterns = [
    path("", views.reports_home, name="reports_home"),
    path("top-products/", views.top_products, name="top_products"),
    path("customers-ltv/", views.customers_ltv, name="customers_ltv"),
    path(
        "orders-with-late-payment/",
        views.orders_with_late_payment,
        name="orders_with_late_payment",
    ),
    path(
        "events-matched-by-email/",
        views.events_matched_by_email,
        name="events_matched_by_email",
    ),
    path("n-plus-one-demo/", views.n_plus_one_demo, name="n_plus_one_demo"),
    path("window-rankings/", views.window_rankings, name="window_rankings"),
    path("html/top-products/", views.top_products_page, name="top_products_page"),
    path("html/customers-ltv/", views.customers_ltv_page, name="customers_ltv_page"),
    path(
        "html/orders-with-late-payment/",
        views.orders_with_late_payment_page,
        name="orders_with_late_payment_page",
    ),
    path(
        "html/events-matched-by-email/",
        views.events_matched_by_email_page,
        name="events_matched_by_email_page",
    ),
    path("html/n-plus-one-demo/", views.n_plus_one_demo_page, name="n_plus_one_demo_page"),
    path("html/window-rankings/", views.window_rankings_page, name="window_rankings_page"),
]
