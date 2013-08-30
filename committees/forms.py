from committees.models import AdHocApplication, DEFCONApplication, \
     ICCApplication, CEAApplication, UFCApplication, CommitteeAssignment, \
     DelegateAssignment

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


CommitteeAssignmentFormSet = forms.models.modelformset_factory(CommitteeAssignment,
	fields=('position_paper',), extra=0)

DelegateAssignmentFormset = forms.models.modelformset_factory(DelegateAssignment,
	fields=('delegate_name',), extra=0)
