from django.contrib import admin
from merchandise.models import Bundle, Item, BundleOrder, ItemOrder


admin.site.register(Bundle)
admin.site.register(Item)
admin.site.register(BundleOrder)
admin.site.register(ItemOrder)
