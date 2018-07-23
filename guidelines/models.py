# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Guidelines(models.Model):
    name = models.CharField(max_length=128)
    file_video = models.FileField(upload_to='guidelines')

    def __str__(self):
        return 'video #{} {}'.format(self.id, self.name)

    class Meta:
        verbose_name = _('Guidelines')
