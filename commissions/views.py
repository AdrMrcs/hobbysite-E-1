from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.forms import formset_factory

from .models import Commission, Job, JobApplication
from user_management.models import Profile
from .forms import CommissionForm, JobForm, JobFormSet

import logging
import django.contrib.messages as messages

# Define logger
logger = logging.getLogger(__name__)


class CommissionListView(ListView):
    model = Commission
    template_name = "commission_list.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        ctx = super().get_context_data(**kwargs)
        if user.is_authenticated:
            ctx["user_created"] = Commission.objects.filter(created_by=user.profile)

            ctx["user_applied"] = []
            ctx["user_applied_wo_status"] = []
            for commission in Commission.objects.all():
                for job in commission.jobs.all():
                    for job_app in job.job_apps.all():
                        if job_app.applicant == user.profile:
                            ctx["user_applied"].append((commission, job_app.get_status))
                            ctx["user_applied_wo_status"].append(commission)

            ctx["remaining_commissions"] = []
            tmp_rem_commissions = []  # (status, commission) -> sorted
            for commission in Commission.objects.all():
                if (
                    commission not in ctx["user_created"]
                    and commission not in ctx["user_applied_wo_status"]
                ):
                    tmp_rem_commissions.append(
                        (commission.get_status_sort_value(), commission)
                    )
            tmp_rem_commissions.sort(key=lambda x: x[0]) # sort accdg. to status
            for status, commission in tmp_rem_commissions:
                ctx["remaining_commissions"].append(commission)

        return ctx


class CommissionDetailView(TemplateView):
    model = Commission
    template_name = "commission_detail.html"

    def post(self, request, *args, **kwargs):
        job_id = request.POST.get("job_id")
        profile = request.user.profile
        if job_id:
            job = Job.objects.get(pk=job_id)
            already_exists = False
            for job_apps in JobApplication.objects.all():
                if job_apps.applicant == profile and job_apps.job == job:
                    already_exists = True

            if job.manpower_left > 0 and not already_exists:
                JobApplication.objects.create(job=job, applicant=profile)

        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        user = self.request.user
        ctx = super().get_context_data(**kwargs)

        if user.is_authenticated:
            commission_id = self.kwargs["pk"]
            ctx["commission"] = Commission.objects.get(id=commission_id)
            ctx["jobs"] = []

            for job in Job.objects.filter(commission=ctx["commission"]):
                ctx["jobs"].append((job, (job.manpower_left > 0)))

        return ctx


class CommissionCreateView(TemplateView):
    template_name = "commission_create.html"

    def get(self, request, *args, **kwargs):
        commission_form = CommissionForm()
        job_formset = JobFormSet()
        return render(request, self.template_name, {'commission_form': commission_form, 'job_formset': job_formset})

    def post(self, request, *args, **kwargs):
        commission_form = CommissionForm(request.POST)
        job_formset = JobFormSet(request.POST)

        if job_formset.is_valid() and commission_form.is_valid():
            commission = commission_form.save(commit=False)
            commission.created_by = request.user.profile
            commission.save()

            for job_form in job_formset:
                job = job_form.save(commit=False)
                job.commission = commission
                job.manpower_accepted = 0
                job.save()
            return redirect(commission.get_absolute_url())
        
        logger.messages("wrong input")
        return self.render_to_response(self.get_context_data())