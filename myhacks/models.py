from django.db import models

from django.contrib.auth.models import User


class Hack(models.Model):
    user = models.ForeignKey(User)
    what = models.CharField(blank=True, max_length=255,
                        verbose_name="What do you do?")
    where = models.CharField(blank=True, max_length=255,
                        verbose_name="Where are you from?")
    hack = models.TextField(blank=False,
                        verbose_name="What did you do?")

    class Meta:
        get_latest_by = 'pk'
