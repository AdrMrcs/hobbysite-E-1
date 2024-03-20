from django.db import models
from django.urls import reverse


class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    people_required = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[COMMISSION] {self.title}, updated on {self.updated_on}'
    
    def get_absolute_url(self):
        return reverse('commissions:commission-detail', args=[self.pk])
    
    class Meta:
        ordering = ['created_on']

class Comment(models.Model):
    commission = models.ForeignKey(
        'Commission',
        on_delete=models.CASCADE, 
        default=1,
        related_name='comments',
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment on {self.commission.title}. PK={self.pk}'

    class Meta:
        ordering = ['-created_on']