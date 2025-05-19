import openai
from django.conf import settings
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Property
from .serializers import PropertySerializer
from rest_framework.permissions import AllowAny
import re
from django_filters.rest_framework import DjangoFilterBackend

# make sure you’ve defined in settings.py:
# OPENAI_API_KEY = "<your key here>"
openai.api_key = settings.OPENAI_API_KEY

class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = [
        "area_unit", "bathrooms", "bedrooms", "home_size", "home_type",
        "last_sold_date", "last_sold_price", "link", "price", "property_size",
        "rent_price", "rentzestimate_amount", "rentzestimate_last_updated",
        "tax_value", "tax_year", "year_built", "zestimate_amount",
        "zestimate_last_updated", "zillow_id", "address", "city", "state", "zipcode",
    ]
    ordering_fields = filterset_fields
    search_fields = ["address", "city", "home_type"]

    @action(detail=False, methods=["post"], url_path="ai-query", permission_classes=[AllowAny])
    def ai_query(self, request, *args, **kwargs):
        user_q = request.data.get("query", "").strip()
        if not user_q:
            return Response({"error": "No query provided."}, status=status.HTTP_400_BAD_REQUEST)

        prompt = f"""
Given the Django `Property` model with fields:
- area_unit (CharField)
- bathrooms (FloatField)
- bedrooms (IntegerField)
- home_size (IntegerField)
- home_type (CharField)
- last_sold_date (DateField)
- last_sold_price (IntegerField)
- link (URLField)
- price (CharField)
- property_size (IntegerField)
- rent_price (IntegerField)
- rentzestimate_amount (IntegerField)
- rentzestimate_last_updated (DateField)
- tax_value (DecimalField)
- tax_year (IntegerField)
- year_built (IntegerField)
- zestimate_amount (IntegerField)
- zestimate_last_updated (DateField)
- zillow_id (CharField, unique)
- address (CharField)
- city (CharField)
- state (CharField)
- zipcode (CharField)

And a user request: "{user_q}"
Return ONLY a Python dict literal with:
- regular filter kwargs for `Property.objects.filter(**kwargs)`
- if asking for top N most expensive, include:
    '_ordering': '-last_sold_price',
    '_limit': N
Example: {{'year_built__gt': 1980, '_ordering': '-last_sold_price', '_limit': 5}}
No prose or code fences.
"""

        resp = openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.0,
        )
        raw = resp.choices[0].message.content.strip()

        # extract inner dict from fences
        m = re.search(r"```(?:python)?\s*([\s\S]*?)```", raw)
        text = m.group(1).strip() if m else raw.replace("```", "").strip()
        print(f"GPT response: {text}")

        # parse
        try:
            data = eval(text, {}, {})
            if not isinstance(data, dict):
                raise ValueError("Not a dict")
        except Exception as e:
            return Response({"error": "Failed to parse GPT output", "detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # pull special keys
        ordering = data.pop('_ordering', None)
        limit = data.pop('_limit', None)

        # build filters without special keys
        filter_kwargs = {k: v for k, v in data.items()}
        qs = Property.objects.filter(**filter_kwargs)
        if ordering:
            qs = qs.order_by(ordering)
        if isinstance(limit, int) and limit > 0:
            qs = qs[:limit]

        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)

        ser = self.get_serializer(qs, many=True)
        return Response(ser.data)
