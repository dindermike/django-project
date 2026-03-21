from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from gallery.models import Image


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean

        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)

        return result


class BulkUploadForm(forms.Form):
    """
    Inline bulk-upload form (multiple file inputs in the change-list action)
    """
    # images = forms.FileField(
    #     widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}),
    #     label='',
    # )
    images = MultipleFileField(label='Select Files', required=True)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    # ---- List View -----------------------------------------------------------
    change_list_template = 'admin/gallery/image/change_list.html'
    list_display = ('thumbnail', 'title', 'location', 'date', 'uploaded_at', 'order')
    list_editable = ('order',)
    list_filter = ('date', 'location', 'uploaded_at')
    search_fields = ('title', 'subtitle', 'description', 'location')
    ordering = ('order', '-uploaded_at')
    date_hierarchy = 'uploaded_at'

    # ---- Detail/Edit View ----------------------------------------------------
    fieldsets = (
        ('Image File', {
            'fields': ('image', 'preview'),
        }),
        ('Metadata (all optional)', {
            'fields': ('title', 'subtitle', 'description', 'date', 'location', 'order'),
        }),
    )
    readonly_fields = ('preview', 'uploaded_at', 'updated_at')

    # ---- Actions -------------------------------------------------------------
    actions = ['delete_selected']

    # ---- Helpers -------------------------------------------------------------
    @admin.display(description='Preview')
    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 60px; width: auto; border-radius: 4px; object-fit: cover;" />',
                obj.image.url,
            )

        return '—'

    @admin.display(description='Full preview')
    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:400px; max-height: 300px; border-radius: 6px; object-fit: contain;" />',
                obj.image.url,
            )

        return '—'

    # ---- Bulk Upload Via Custom Change-List View -----------------------------
    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom = [
            path(
                'bulk-upload/',
                self.admin_site.admin_view(self.bulk_upload_view),
                name='gallery_image_bulk_upload'
            ),
        ]

        return custom + urls

    def bulk_upload_view(self, request):
        """
        Handle GET (Show Form) and POST (Process Files) for Bulk Uploads.
        """
        from django.shortcuts import render, redirect
        from django.contrib import messages

        form = BulkUploadForm()

        if request.method == 'POST':
            form = BulkUploadForm(request.POST, request.FILES)

            if form.is_valid():
                files = request.FILES.getlist('images')
                created = 0
                errors = []

                for f in files:
                    try:
                        obj = Image(image=f)
                        obj.save()  # post_save Signal Optimizes the File
                        created += 1
                    except Exception as exc:
                        errors.append(f'{f.name}: {exc}')

                if created:
                    messages.success(request, f'{created} Image(s) Uploaded Successfully.')

                for err in errors:
                    messages.error(request, err)

                return redirect('admin:gallery_image_changelist')

        context = {
            **self.admin_site.each_context(request),
            'title': 'Bulk Image Upload',
            'form': form,
            'opts': self.model._meta,
        }

        return render(request, 'admin/gallery/image/bulk_upload.html', context)

    def changelist_view(self, request, extra_context=None):
        from django.urls import reverse

        extra_context = extra_context or {}
        extra_context['bulk_upload_url'] = reverse('admin:gallery_image_bulk_upload')

        return super().changelist_view(request, extra_context=extra_context)
