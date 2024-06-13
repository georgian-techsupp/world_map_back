from django.db import models

# Create your models here.
class World_Map_Model(models.Model):
    country_name = models.CharField(max_length=50, unique=True)
    company_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/')

    def __str__(self) -> str:
        return f"{self.country_name} - {self.company_name}"