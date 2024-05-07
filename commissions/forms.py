from django import forms
from .models import Commission, Job
from django.forms import formset_factory

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['title', 'description', 'status']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['role', 'manpower_required']

JobFormSet = formset_factory(JobForm, extra=1)