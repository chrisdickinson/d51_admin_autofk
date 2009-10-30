from django.db import models
from d51_admin_autofk import fields as d51models

class SimpleModel(models.Model):
    name = models.CharField(unique=True, max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return u'%s' % self.name

class ComplexModel(models.Model):
    name = models.CharField(max_length=255)
    simple_input = d51models.ForeignKey(SimpleModel, 'simplemodel-json', 'startswith_json')
    def __unicode__(self):
        return u'%s' % self.name
