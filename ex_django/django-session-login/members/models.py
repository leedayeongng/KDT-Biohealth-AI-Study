from django.db import models
from django.utils import timezone


class Member(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "member"
        ordering = ["id"]

    def __str__(self) -> str:
        return self.username
