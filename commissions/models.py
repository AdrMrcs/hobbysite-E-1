from django.db import models
from django.urls import reverse

from user_management.models import Profile

STATUS_CHOICES = {
    "COMMISSION" : {
        "OP" : "Open",
        "FU" : "Full",
        "CO" : "Completed",
        "DI" : "Discontinued",
    },
    "JOB" : {
        1 : "Open",
        2 : "Full",
    },
    "JOB_APP" : {
        1 : "Pending",
        2 : "Accepted",
        3 : "Rejected",
    }
}

class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=25, choices=STATUS_CHOICES["COMMISSION"], default="OP")
    # people_required = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[COMMISSION] {self.title}, updated on {self.updated_on}'
    
    def get_absolute_url(self):
        return reverse('commissions:commission-detail', args=[self.pk])
    
    class Meta:
        ordering = ['created_on']

class Job(models.Model):
    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE, 
        default=1,
        related_name='jobs',
    )
    role = models.CharField(max_length=255)
    manpower_required = models.IntegerField()
    status = models.CharField(max_length=25, choices=STATUS_CHOICES["JOB"], default=1)

    def __str__(self):
        return f'Job from {self.commission.title}. PK={self.pk}'

    class Meta:
        ordering = ['-status', '-manpower_required', 'role']

class JobApplication(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE, 
        default=1,
        related_name='job_apps',
    )
    applicant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    status = models.CharField(max_length=25, choices=STATUS_CHOICES["JOB_APP"], default=1)
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [
            'status',
            '-applied_on',
        ]
