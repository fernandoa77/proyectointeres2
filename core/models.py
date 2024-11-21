from django.db import models
from django.contrib.auth.models import User

class AmortizationTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Table {self.id} by {self.user.username} on {self.created_at}"

class SinkingFund(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fund {self.id} by {self.user.username} on {self.created_at}"
