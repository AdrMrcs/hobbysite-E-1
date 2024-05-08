from django import forms
from .models import Commission, Job, JobApplication
from django.forms import formset_factory


class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ["title", "description", "status"]


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["role", "manpower_required"]


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ["status"]


JobFormSet = formset_factory(JobForm, extra=1)
