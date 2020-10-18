from django.db import models


class Category(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"