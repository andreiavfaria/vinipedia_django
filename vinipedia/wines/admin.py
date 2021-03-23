from django.contrib import admin

# Register your models here.
from .models import Country, Region, Producer, Grape, Wine, WineGrape, Vintage, GrapeAlias, ProducerRegion

admin.site.register(Country)
admin.site.register(Region)
admin.site.register(Producer)
admin.site.register(ProducerRegion)
admin.site.register(Grape)
admin.site.register(Wine)
admin.site.register(WineGrape)
admin.site.register(Vintage)
admin.site.register(GrapeAlias)

