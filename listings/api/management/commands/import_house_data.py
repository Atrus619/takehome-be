import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from api.models import Property


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%m/%d/%Y').date()
    except (ValueError, TypeError):
        return None


def parse_price(price_str):
    if not price_str:
        return None
    s = price_str.replace('$', '').replace(',', '').upper()
    try:
        if s.endswith('K'):
            return int(float(s[:-1]) * 1_000)
        if s.endswith('M'):
            return int(float(s[:-1]) * 1_000_000)
        return int(float(s))
    except ValueError:
        return None

class Command(BaseCommand):
    help = 'Import house data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to CSV file')

    def handle(self, *args, **options):
        path = options['csv_file']
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, skipinitialspace=True)
            # Normalize header keys
            reader.fieldnames = [name.strip() for name in reader.fieldnames]
            for row in reader:
                # Strip whitespace from keys and values
                row = {k.strip(): v.strip() for k, v in row.items()}
                obj, created = Property.objects.update_or_create(
                    zillow_id=row.get('zillow_id'),
                    defaults={
                        'area_unit': row.get('area_unit'),
                        'bathrooms': float(row.get('bathrooms')) if row.get('bathrooms') else None,
                        'bedrooms': int(row.get('bedrooms')) if row.get('bedrooms') else None,
                        'home_size': int(row.get('home_size')) if row.get('home_size') else None,
                        'home_type': row.get('home_type'),
                        'last_sold_date': parse_date(row.get('last_sold_date')),
                        'last_sold_price': parse_price(row.get('last_sold_price')),
                        'link': row.get('link'),
                        'price': row.get('price'),
                        'property_size': int(row.get('property_size')) if row.get('property_size') else None,
                        'rent_price': int(row.get('rent_price')) if row.get('rent_price') else None,
                        'rentzestimate_amount': int(row.get('rentzestimate_amount')) if row.get('rentzestimate_amount') else None,
                        'rentzestimate_last_updated': parse_date(row.get('rentzestimate_last_updated')),
                        'tax_value': float(row.get('tax_value')) if row.get('tax_value') else None,
                        'tax_year': int(row.get('tax_year')) if row.get('tax_year') else None,
                        'year_built': int(row.get('year_built')) if row.get('year_built') else None,
                        'zestimate_amount': int(row.get('zestimate_amount')) if row.get('zestimate_amount') else None,
                        'zestimate_last_updated': parse_date(row.get('zestimate_last_updated')),
                        'address': row.get('address'),
                        'city': row.get('city'),
                        'state': row.get('state'),
                        'zipcode': row.get('zipcode'),
                    }
                )
                action = 'Created' if created else 'Updated'
                self.stdout.write(f"{action} {obj}")
