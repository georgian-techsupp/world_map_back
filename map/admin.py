from django.contrib import admin
from .models import Country, Coordinates, ISO_CODES
from django.utils.safestring import mark_safe
# Register your models here.


class CountryAdmin(admin.ModelAdmin):
    list_display = ("name","iso_code","business_name", "business_type","image_preview")
    list_filter = ("name","iso_code","business_name", "business_type")
    search_fields = ("name__name","iso_code__iso_code","business_name", "business_type")
    def image_preview(self, obj):
        if obj.image:
            return mark_safe('<img src="{0}" style="max-width:50px; max-height:50px;" />'.format(obj.image.url))
        else:
            return 'No Image'
    image_preview.short_description = 'Image Preview'
admin.site.register(Country, CountryAdmin)
admin.site.register(Coordinates)
admin.site.register(ISO_CODES)
