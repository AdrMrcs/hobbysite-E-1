from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Commission, Job, JobApplication
from user_management.models import Profile

class CommissionListView(ListView):
    model = Commission
    template_name = 'commission_list.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        ctx = super().get_context_data(**kwargs)
        if user.is_authenticated:
            ctx['user_created'] = Commission.objects.filter(created_by=user.profile)
            # make user_applied
        return ctx

class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commission_detail.html'

