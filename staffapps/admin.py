from django.contrib import admin

from staffapps.models import CoordinatorApp, LogisticalApp, CommitteesApp


class StaffAppAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number')
    search_Fields = ('full_name',)


admin.site.register(CoordinatorApp, StaffAppAdmin)
admin.site.register(LogisticalApp, StaffAppAdmin)
admin.site.register(CommitteesApp, StaffAppAdmin)
