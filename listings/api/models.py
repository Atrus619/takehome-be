from django.db import models

class Property(models.Model):
    area_unit = models.CharField(max_length=10)
    bathrooms = models.FloatField(null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    home_size = models.IntegerField(null=True, blank=True)
    home_type = models.CharField(max_length=50)
    last_sold_date = models.DateField(null=True, blank=True)
    last_sold_price = models.IntegerField(null=True, blank=True)
    link = models.URLField()
    price = models.CharField(max_length=20)
    property_size = models.IntegerField(null=True, blank=True)
    rent_price = models.IntegerField(null=True, blank=True)
    rentzestimate_amount = models.IntegerField(null=True, blank=True)
    rentzestimate_last_updated = models.DateField(null=True, blank=True)
    tax_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tax_year = models.IntegerField(null=True, blank=True)
    year_built = models.IntegerField(null=True, blank=True)
    zestimate_amount = models.IntegerField(null=True, blank=True)
    zestimate_last_updated = models.DateField(null=True, blank=True)
    zillow_id = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.address}, {self.city}"
