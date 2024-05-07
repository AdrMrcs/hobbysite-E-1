from django.db import models
from django.urls import reverse

from user_management.models import Profile

STATUS_CHOICES = {
    "COMMISSION": {
        "OP": "Open",
        "FU": "Full",
        "CO": "Completed",
        "DI": "Discontinued",
    },
    "JOB": {
        "1": "Open",
        "2": "Full",
    },
    "JOB_APP": {
        "1": "Pending",
        "2": "Accepted",
        "3": "Rejected",
    },
}


class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=25, choices=STATUS_CHOICES["COMMISSION"], default="OP"
    )
    # people_required = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        Profile,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("commissions:commission-detail", args=[self.pk])
    
    def get_update_url(self):
        return reverse("commissions:commission-update", args=[self.pk])

    # @property
    # def is_open(self):
    #     return self.status == "OP"

    # @property
    # def is_full(self):
    #     return self.status == "FU"

    # @property
    # def is_completed(self):
    #     return self.status == "CO"

    # @property
    # def is_discontinued(self):
    #     return self.status == "DI"

    @property
    def get_status(self):
        return STATUS_CHOICES["COMMISSION"][self.status]

    def get_status_sort_value(self):
        if self.get_status == "Open":
            return 1
        elif self.get_status == "Full":
            return 2
        elif self.get_status == "Completed":
            return 3
        elif self.get_status == "Discontinued":
            return 4
        return 5

    class Meta:
        ordering = ["created_on"]


class Job(models.Model):
    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        default=1,
        related_name="jobs",
    )
    role = models.CharField(max_length=255)
    manpower_required = models.IntegerField()
    manpower_accepted = models.IntegerField()
    status = models.CharField(max_length=25, choices=STATUS_CHOICES["JOB"], default="1")

    def __str__(self):
        return f"{self.role}"

    @property
    def get_status(self):
        return STATUS_CHOICES["JOB"][self.status]

    @property
    def manpower_left(self):
        return self.manpower_required - self.manpower_accepted

    @property
    def manpower_increment(self):
        self.manpower_accepted += 1

    @property
    def manpower_decrement(self):
        self.manpower_accepted -= 1

    class Meta:
        ordering = ["-status", "-manpower_required", "role"]


class JobApplication(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        default=1,
        related_name="job_apps",
    )
    applicant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=25, choices=STATUS_CHOICES["JOB_APP"], default="1"
    )
    applied_on = models.DateTimeField(auto_now_add=True)

    @property
    def get_status(self):
        return STATUS_CHOICES["JOB_APP"][self.status]

    class Meta:
        ordering = [
            "status",
            "-applied_on",
        ]
