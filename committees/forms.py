from committees.models import AdHocApplication, DEFCONApplication, \
     ICCApplication, CEAApplication, UFCApplication, GreatEmpireApplication, \
     CommitteeAssignment, DelegateAssignment, AwardAssignment

from django import forms


class AdHocAppForm(forms.ModelForm):
    class Meta:
        model = AdHocApplication


class DEFCONAppForm(forms.ModelForm):
    class Meta:
        model = DEFCONApplication


class ICCAppForm(forms.ModelForm):
    class Meta:
        model = ICCApplication


class CEAAppForm(forms.ModelForm):
    class Meta:
        model = CEAApplication


class UFCAppForm(forms.ModelForm):
    class Meta:
        model = UFCApplication


class GreatEmpireAppForm(forms.ModelForm):
    class Meta:
        model = GreatEmpireApplication


AwardAssignmentFormset = forms.models.modelformset_factory(AwardAssignment,
    fields=('position',), extra=0)

DelegateAssignmentFormset = forms.models.modelformset_factory(DelegateAssignment,
    fields=('delegate_name',), extra=0)
