from django.db import models



class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Name of the country
    iso_code = models.CharField(max_length=10, unique=True)  # ISO 3166-2 code
    image = models.ImageField(upload_to='country_images/' )
    business_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
