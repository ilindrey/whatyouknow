from django.template.defaultfilters import striptags
from django.core.validators import MinValueValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class SummernoteMinValueValidator(MinValueValidator):

    def clean(self, x):
        return len(striptags(x))
