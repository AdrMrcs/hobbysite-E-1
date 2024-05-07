from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.forms import formset_factory
from django.contrib.auth.mixins import LoginRequiredMixin
import django.contrib.messages as messages


from .models import Commission, Job, JobApplication
from user_management.models import Profile
from .forms import CommissionForm, JobForm, JobFormSet



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


class CommissionCreateView(LoginRequiredMixin, TemplateView):
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
        
        return self.render_to_response(self.get_context_data())

class CommissionUpdateView(LoginRequiredMixin, TemplateView):
    template_name = "commission_update.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        commission = get_object_or_404(Commission, pk=self.kwargs['pk'])
        ctx['commission'] = commission
        ctx['commission_form'] = CommissionForm(instance=commission)
        ctx['jobs_and_forms'] = [] # (job, form, index)
        ind = 0
        for job in Job.objects.filter(commission=commission):
            ctx['jobs_and_forms'].append((job, JobForm(instance=job), ind))
            ind += 1

        return ctx
    
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        commission = get_object_or_404(Commission, pk=pk)
        commission_form = CommissionForm(instance=commission, data=request.POST)
        jobs_and_forms = []
        ind = 0
        for job in Job.objects.filter(commission=commission):
            jobs_and_forms.append((job, JobForm(instance=job, data=request.POST), ind))
            ind += 1

        if "save_commission" in request.POST:
            if person_form.is_bound and person_form.is_valid():
                person_form.save()
                messages.add_message(request, messages.SUCCESS, "Data saved.")
            else:
                messages.error(request, person_form.errors)
        
        # doesn't work, need formset ig
        for job, form, ind in jobs_and_forms:
            if f"save_job_{ind}" in request.POST:
                if form.is_bound and form.is_valid():
                    form.save()
                    messages.add_message(request, messages.SUCCESS, "Data saved.")
                else:
                    messages.error(request, form.errors)

        return self.render_to_response(self.get_context_data())

