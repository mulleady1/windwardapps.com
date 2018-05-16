from django import forms
from django.db import models


class CharFieldWithTextarea(models.CharField):
    def formfield(self, **kwargs):
        kwargs['widget'] = forms.Textarea
        return super(CharFieldWithTextarea, self).formfield(**kwargs)
