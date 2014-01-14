from django.contrib import admin

from committees.models import *


class CommitteeAssignmentAdmin(admin.ModelAdmin):
    list_display = ('school', 'committee', 'assignment')
    search_fields = ('school__school_name', 'committee__name', 'assignment')


class DelegateAssignmentAdmin(admin.ModelAdmin):
    list_display = ('school', 'committee', 'committee_assignment', 'delegate_name')
    search_fields = (
        'committee_assignment__school__school_name',
        'committee_assignment__committee__name',
        'committee_assignment__assignment',
        'delegate_name'
    )

    def school(self, obj):
        return "%s" % obj.committee_assignment.school
    school.short_description = 'School'
    school.admin_order_field  = 'committee_assignment__school'

    def committee(self, obj):
        return "%s" % obj.committee_assignment.committee
    committee.short_description = 'Committee'
    committee.admin_order_field = 'committee_assignment__committee'


class CommitteeAssignmentInline(admin.StackedInline):
    model = CommitteeAssignment
    extra = 5
    exclude = ('position_paper',)


class CommitteeAdmin(admin.ModelAdmin):
    inlines = [CommitteeAssignmentInline]


class AwardAssignmentAdmin(admin.ModelAdmin):
    list_display = ('award', 'committee', 'position')
    list_per_page = 108  # show all the awards on one page


admin.site.register(Category)
admin.site.register(Committee, CommitteeAdmin)
admin.site.register(AdHocApplication)
admin.site.register(DEFCONApplication)
admin.site.register(ICCApplication)
admin.site.register(CEAApplication)
admin.site.register(UFCApplication)
admin.site.register(GreatEmpireApplication)
admin.site.register(CommitteeAssignment, CommitteeAssignmentAdmin)
admin.site.register(DelegateAssignment, DelegateAssignmentAdmin)
admin.site.register(Award)
admin.site.register(AwardAssignment, AwardAssignmentAdmin)
