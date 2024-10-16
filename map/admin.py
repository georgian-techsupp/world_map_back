from django.contrib import admin
from .models import Country, Coordinates, ISO_CODES
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from django.urls import reverse



class CountryAdmin(admin.ModelAdmin):
    list_display = ("name","iso_code","business_name", "business_type", 'created','expiry_days',"image_preview")
    list_filter = ("name","iso_code","business_name", "business_type")
    search_fields = ("name__name","iso_code__iso_code","business_name", "business_type")
    actions = ['fetch_google_points']

    def image_preview(self, obj):
        if obj.image:
            return mark_safe('<img src="{0}" style="max-width:50px; max-height:50px;" />'.format(obj.image.url))
        else:
            return 'No Image'
    image_preview.short_description = 'Image Preview'

    def fetch_google_points(self, request, queryset):
        selected = queryset.values_list('iso_code__iso_code', flat=True)
        iso_codes = ",".join(selected)
        return HttpResponseRedirect(reverse('admin_get_google_points', args=[iso_codes]))

    fetch_google_points.short_description = "Fetch Google Points for selected countries"

admin.site.register(Country, CountryAdmin)
admin.site.register(Coordinates)
admin.site.register(ISO_CODES)
