from django.db import models

class ISO_CODES(models.Model):
    iso_code = models.CharField(max_length=2, unique=True)  
    name = models.CharField(max_length=255)
    class Meta:
        unique_together = ('iso_code', 'name')
        verbose_name = 'ISO Code'
        verbose_name_plural = 'ISO Codes'

    def __str__(self):
        return f"{self.name} ({self.iso_code})"

class Country(models.Model):
    name = models.OneToOneField(ISO_CODES, on_delete=models.CASCADE, unique=True, related_name='iso_name')
    iso_code = models.ForeignKey(ISO_CODES, on_delete=models.CASCADE, related_name='iso')
    image = models.ImageField(upload_to='country_images/' )
    business_name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=100)
    def __str__(self):
        return self.name.name
    
class Coordinates(models.Model):
    name = models.ForeignKey(Country,on_delete=models.CASCADE,blank=True, related_name='country_name')
    iso_code = models.ForeignKey(Country, on_delete=models.CASCADE,blank=True, related_name='name_iso_code')
    business_name = models.ForeignKey(Country, on_delete=models.CASCADE,blank=True,related_name='business')
    activate = models.BooleanField(default=True)
    location_name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    class Meta:
        unique_together = ('location_name', 'latitude', 'longitude')
    def __str__(self):
        return f"{self.name.name} - {self.iso_code.iso_code} - {self.location_name}"

