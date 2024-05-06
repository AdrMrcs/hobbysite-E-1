from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Commission, Job, JobApplication
from user_management.models import Profile


class CommissionListView(ListView):
    model = Commission
    template_name = "commission_list.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        ctx = super().get_context_data(**kwargs)
        if user.is_authenticated:
            ctx["user_created"] = Commission.objects.filter(created_by=user.profile)

            ctx["user_applied"] = []
            for commission in Commission.objects.all():
                for job in commission.jobs.all():
                    for job_app in job.job_apps.all():
                        if job_app.applicant == user.profile:
                            ctx["user_applied"].append(commission)

            ctx["remaining_commissions"] = []
            tmp_rem_commissions = []  # (status, commission) -> sorted
            for commission in Commission.objects.all():
                if (
                    commission not in ctx["user_created"]
                    and commission not in ctx["user_applied"]
                ):
                    tmp_rem_commissions.append(
                        (commission.get_status_sort_value(), commission)
                    )
            tmp_rem_commissions.sort(key=lambda x: x[0])
            for status, commission in tmp_rem_commissions:
                ctx["remaining_commissions"].append(commission)

        return ctx


class CommissionDetailView(DetailView):
    model = Commission
    template_name = "commission_detail.html"
