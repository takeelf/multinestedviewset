from __future__ import unicode_literals

from django.db import models


class NestedThing(models.Model):
    user = models.ForeignKey('auth.User', related_name='nested')
    nested_name = models.CharField(max_length=30)
