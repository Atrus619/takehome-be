# api/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Property

class PropertyAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create sample Property instances
        Property.objects.create(
            area_unit="SqFt", bathrooms=2.0, bedrooms=3, home_size=1200,
            home_type="SingleFamily", last_sold_price=500000,
            link="http://example.com/1", price="$500K", property_size=8000,
            rent_price=2500, rentzestimate_amount=2400,
            rentzestimate_last_updated=None,
            tax_value=200000.00, tax_year=2020, year_built=1990,
            zestimate_amount=510000, zestimate_last_updated=None,
            zillow_id="Z1", address="123 Maple St",
            city="Testville", state="TS", zipcode="12345"
        )
        Property.objects.create(
            area_unit="SqFt", bathrooms=4.0, bedrooms=5, home_size=3000,
            home_type="SingleFamily", last_sold_price=1200000,
            link="http://example.com/2", price="$1.2M", property_size=12000,
            rent_price=4500, rentzestimate_amount=4300,
            rentzestimate_last_updated=None,
            tax_value=800000.00, tax_year=2021, year_built=2005,
            zestimate_amount=1210000, zestimate_last_updated=None,
            zillow_id="Z2", address="456 Oak Ave",
            city="Testville", state="TS", zipcode="67890"
        )

    def test_list_properties(self):
        """
        Ensure we can retrieve the list of properties and it contains our objects."""
        url = reverse('property-list', kwargs={'version': 'v1'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        # Normalize to list of results
        if isinstance(data, dict):
            results = data.get('results', [])
        else:
            results = data

        self.assertEqual(len(results), 2)
        ids = {prop['zillow_id'] for prop in results}
        self.assertSetEqual(ids, {'Z1', 'Z2'})

    def test_filter_by_bedrooms(self):
        """
        Ensure the filtering by bedrooms query parameter works as expected."""
        url = reverse('property-list', kwargs={'version': 'v1'})
        response = self.client.get(url, {'bedrooms': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        # Normalize to list
        if isinstance(data, dict):
            results = data.get('results', [])
        else:
            results = data

        # Only one property has bedrooms=5
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['bedrooms'], 5)
        self.assertEqual(result['zillow_id'], 'Z2')
