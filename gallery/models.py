import os
import uuid
from django.db import models
from django.utils import timezone
from PIL import Image as PILImage


def upload_to(instance, filename):
    """
    Rename Uploaded Files to a Clean, Unique Filename.
    Format: YYYY/MM/DD/uuid4_slug-of-original.ext
    E.g. 2024/03/15/a1b2c3d4_my-photo.jpg
    """
    import re

    # Extract Extension & Normalize It
    ext = os.path.splitext(filename)[1].lower()

    if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        ext = '.jpg'

    # Build a Clean Base From the Original Filename (Spaces → Hyphens, Strip Specials)
    base = os.path.splitext(filename)[0]
    base = base.lower()
    base = re.sub(r'[^\w\s-]', '', base)  # Remove Special Characters
    base = re.sub(r'[\s_]+', '-', base)  # Spaces/Underscores → Hyphens
    base = re.sub(r'-+', '-', base).strip('-')  # Collapse Multiple Hyphens
    base = base[:45]  # Cap Length

    unique_prefix = uuid.uuid4().hex[:8]
    date_path = timezone.now().strftime('%Y/%m/%d')

    return f'gallery/{date_path}/{unique_prefix}_{base}{ext}'


class Image(models.Model):
    # Core File Field - Required by Default
    image = models.ImageField(upload_to=upload_to)

    # Optional Metadata
    title = models.CharField(
        max_length=200,
        blank=True,
        default=''
    )
    subtitle = models.CharField(
        max_length=200,
        blank=True,
        default=''
    )
    description = models.TextField(
        blank=True,
        default=''
    )
    date = models.DateField(
        null=True,
        blank=True
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        default=''
    )

    # Auto-Managed Timestamps
    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    # Ordering
    order = models.PositiveIntegerField(
        default=0,
        help_text='Lower Numbers Appear First.'
    )

    class Meta:
        ordering = ['order', '-uploaded_at']
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return self.title or os.path.basename(self.image.name)

    # ------------------------------------------------------------------
    # Image Optimization — called automatically via the post_save signal
    # (see apps.py / signals.py) so it runs for both single and bulk
    # uploads without duplicating logic here.
    # ------------------------------------------------------------------
    def optimize(self):
        """
        Resize to a Max 1,200px wide and re-save with compression.
        Converts RGBA/P Mode Images to RGB before saving as JPEG.
        """
        if not self.image:
            return

        filepath = self.image.path

        try:
            img = PILImage.open(filepath)
        except Exception:
            return  # Not A Valid Image — Skip Silently

        # --- Resize if Wider Than 1,200px ---
        max_width = 1200

        if img.width > max_width:
            ratio = max_width / img.width
            new_h = int(img.height * ratio)
            img = img.resize(
                (max_width, new_h),
                PILImage.LANCZOS
            )

        # --- Normalize Color Mode for JPEG, Image Quality Set to 60% ---
        ext = os.path.splitext(filepath)[1].lower()

        if ext in ('.jpg', '.jpeg'):
            if img.mode in ('RGBA', 'P', 'LA'):
                img = img.convert('RGB')

            img.save(filepath, 'JPEG', quality=60, optimize=True)

        elif ext == '.png':
            img.save(filepath, 'PNG', optimize=True)

        elif ext == '.webp':
            img.save(filepath, 'WEBP', quality=60, method=6)

        else:
            # Fallback: Save as JPEG
            if img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')

            new_path = os.path.splitext(filepath)[0] + '.jpg'
            img.save(new_path, 'JPEG', quality=60, optimize=True)

            # Update the Stored Path so Django Knows the New Filename
            rel = os.path.relpath(new_path, os.path.join(
                os.path.dirname(filepath),
                *(['..'] * filepath.count(os.sep))
            ))
