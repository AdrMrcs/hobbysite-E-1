from django.contrib import admin

from .models import Commission, Job, JobApplication


class JobInline(admin.TabularInline):
    model = Job


class JobApplicationInline(admin.TabularInline):
    model = JobApplication


class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    inlines = [
        JobInline,
    ]


class JobAdmin(admin.ModelAdmin):
    model = Job
    inlines = [
        JobApplicationInline,
    ]


class JobApplicationAdmin(admin.ModelAdmin):
    model = JobApplication


admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
admin.site.register(Commission, CommissionAdmin)
