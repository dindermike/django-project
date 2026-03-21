from django.db.models.signals import post_save
from django.dispatch import receiver

from gallery.models import Image


@receiver(post_save, sender=Image)
def optimize_image_on_save(sender, instance, created, **kwargs):
    """
    Automatically optimize every image immediately after it is saved.
    This handles both single uploads via the Admin form and bulk uploads.
    We disconnect the signal temporarily to avoid infinite recursion.
    """
    if instance.image:
        # Disconnect → Optimize → Reconnect Prevents Recursive post_save
        post_save.disconnect(optimize_image_on_save, sender=Image)

        try:
            instance.optimize()
        finally:
            post_save.connect(optimize_image_on_save, sender=Image)
