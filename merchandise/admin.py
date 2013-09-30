from django.contrib import admin
from merchandise.models import Bundle, Item, BundleOrder, ItemOrder


class ItemOrderAdmin(admin.ModelAdmin):
    list_display = ('item', 'school', 'bundle_order', 'quantity', 'total_cost',
                    'total_owed_by_school', 'is_finalised')
    ordering = ['school']


admin.site.register(Bundle)
admin.site.register(Item)
admin.site.register(BundleOrder)
admin.site.register(ItemOrder, ItemOrderAdmin)
