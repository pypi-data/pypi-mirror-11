# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from datetime import date
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"))
    content_type = models.ForeignKey(ContentType, verbose_name=_("content_type"))
    object_id = models.PositiveIntegerField(verbose_name=_("object id"))
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        verbose_name = _(u'Favorite')
        verbose_name_plural = _(u'Favorites')
        unique_together = (('user', 'content_type', 'object_id'),)
        
    def __unicode__(self):
        return u"{0} - {1}".format(self.user, self.content_object)
