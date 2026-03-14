from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    hours = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name'], name='restaurant_name_idx'),
        ]
