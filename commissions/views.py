from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin
import django.contrib.messages as messages


from .models import Commission, Job, JobApplication
from user_management.models import Profile
from .forms import CommissionForm, JobForm, JobFormSet, JobApplicationForm


class CommissionListView(ListView):
    model = Commission
    template_name = "commission_list.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        ctx = super().get_context_data(**kwargs)
        if user.is_authenticated:
            ctx["user_created"] = []
            ctx["user_created_wo_status"] = []

            for commission in Commission.objects.filter(created_by=user.profile):
                ctx["user_created_wo_status"].append(commission)
                ctx["user_created"].append(
                    (commission.get_status_sort_value(), commission)
                )

            ctx["user_created"].sort(key=lambda x: x[0])

            ctx["user_applied"] = []
            ctx["user_applied_wo_status"] = []
            for commission in Commission.objects.all():
                for job in commission.jobs.all():
                    for job_app in job.job_apps.all():
                        if job_app.applicant == user.profile:
                            ctx["user_applied"].append(
                                (
                                    commission.get_status_sort_value(),
                                    commission,
                                    job_app.get_status,
                                    job.role,
                                )
                            )
                            ctx["user_applied_wo_status"].append(commission)

            ctx["user_applied"].sort(key=lambda x: x[0])

            ctx["remaining_commissions"] = []
            tmp_rem_commissions = []  # (status, commission) -> sorted
            for commission in Commission.objects.all():
                if (
                    commission not in ctx["user_created_wo_status"]
                    and commission not in ctx["user_applied_wo_status"]
                ):
                    tmp_rem_commissions.append(
                        (commission.get_status_sort_value(), commission)
                    )
            tmp_rem_commissions.sort(key=lambda x: x[0])  # sort accdg. to status
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
                accepted_apps = 0
                is_applied = False
                for applicant in JobApplication.objects.filter(job=job):
                    if applicant.get_status == "Accepted":
                        accepted_apps += 1
                    if applicant.applicant == user.profile:
                        is_applied = True
                ctx["jobs"].append(
                    (job, (job.manpower_required - accepted_apps), is_applied)
                )

        return ctx


class CommissionCreateView(LoginRequiredMixin, TemplateView):
    template_name = "commission_create.html"

    def get(self, request, *args, **kwargs):
        commission_form = CommissionForm()
        job_formset = JobFormSet()
        return render(
            request,
            self.template_name,
            {"commission_form": commission_form, "job_formset": job_formset},
        )

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

        return self.render_to_response(self.get_context_data())


class CommissionUpdateView(LoginRequiredMixin, TemplateView):
    template_name = "commission_update.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        commission = get_object_or_404(Commission, pk=self.kwargs["pk"])
        ctx["commission"] = commission
        ctx["commission_form"] = CommissionForm(instance=commission)

        ctx["jobs"] = Job.objects.filter(commission=commission)
        ctx["applications"] = JobApplication.objects.all()

        ctx["job_data"] = [(job, JobForm(instance=job)) for job in ctx["jobs"]]
        ctx["application_data"] = [
            (application, JobApplicationForm(instance=application))
            for application in ctx["applications"]
        ]

        return ctx

    def post(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        pst = dict(request.POST)
        print(request)
        print(pst)
        pk = self.kwargs["pk"]
        commission = get_object_or_404(Commission, pk=pk)
        commission_form = CommissionForm(instance=commission, data=request.POST)

        # update commission info
        if "save_commission" in request.POST:
            if commission_form.is_bound and commission_form.is_valid():
                commission_form.save()
                messages.add_message(request, messages.SUCCESS, "Data saved.")
            else:
                messages.error(request, commission_form.errors)

        # update jobs
        if "role" in pst and "manpower_required" in pst:
            for i in range(len(ctx["jobs"])):
                job = ctx["jobs"][i]
                if pst["role"][i] == "" or not pst["manpower_required"][i].isdigit():
                    continue
                job.role = pst["role"][i]
                job.manpower_required = pst["manpower_required"][i]
                job.save()

        # update applicants
        if "status" in pst:
            i = 0
            for applicant in ctx["applications"]:
                if applicant.job not in ctx["jobs"]:
                    continue

                applicant.status = pst["status"][i]
                applicant.save()

                i += 1

        # update job status if all applicants are accepted
        for job in ctx["jobs"]:
            job_is_full = True
            for applicant in JobApplication.objects.filter(job=job):
                if applicant.get_status != "Accepted":
                    job_is_full = False
                    break

            job.status = "2" if job_is_full else "1"
            job.save()

        # update commission status if all jobs are full
        commission_is_full = True
        for job in ctx["jobs"]:
            if job.get_status != "Full":
                commission_is_full = False
                break

        commission.status = "FU"
        commission.save()

        return self.render_to_response(self.get_context_data())
