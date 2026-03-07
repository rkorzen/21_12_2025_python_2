1. Stworz dane
2. Policz:
- wartosc wszystkich niezaplaconych faktur dla klienta
- ile kredytu zostalo do wykorzystania

from django.db.models import (
    Sum, F, Q, OuterRef, Subquery,
    ExpressionWrapper, DecimalField
)
from django.db.models.functions import Coalesce