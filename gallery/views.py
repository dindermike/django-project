from django.views.generic import ListView, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

from gallery.models import Image
from gallery.forms import ImageUploadForm, BulkImageUploadForm


class GalleryView(ListView):
    """
    Public gallery page — pass all images to the template so the
    JS slider (iosSlider or similar) can render them.
    """
    model = Image
    template_name = 'gallery/gallery.html'
    context_object_name = 'images'
    queryset = Image.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['branded_title'] = 'Gallery'
        context['meta_description'] = 'Mike Dinder Gallery - A personal photo gallery page to demonstrate image ' \
            'upload capabilities.'
        context['page_class'] = 'gallery-page'
        context['page_id'] = 'gallery-page'
        context['title'] = 'Gallery: Example Photo Gallery'

        return context


class ImageUploadView(CreateView):
    """
    Single image upload with optional metadata.
    """
    model = Image
    form_class = ImageUploadForm
    template_name = 'gallery/upload.html'
    success_url = reverse_lazy('gallery:gallery')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['branded_title'] = 'Upload'
        context['meta_description'] = 'Mike Dinder Upload - A page for uploading a single image at a time.'
        context['page_class'] = 'upload-page'
        context['page_id'] = 'upload-page'
        context['title'] = 'Upload: A Single File'

        return context

    def form_valid(self, form):
        messages.success(self.request, 'Image Uploaded Successfully.')

        return super().form_valid(form)


class BulkImageUploadView(FormView):
    """
    Upload multiple images without requiring metadata.
    """
    form_class = BulkImageUploadForm
    template_name = 'gallery/bulk_upload.html'
    success_url = reverse_lazy('gallery:gallery')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['branded_title'] = 'Bulk Upload'
        context['meta_description'] = 'Mike Dinder Upload - A page for uploading multiple images all at once.'
        context['page_class'] = 'bulk-upload-page'
        context['page_id'] = 'bulk-upload-page'
        context['title'] = 'Bulk UploadUpload: Multiple Images At A Time'

        return context

    def form_valid(self, form):
        files = self.request.FILES.getlist('images')
        created = 0
        errors = []

        for f in files:
            try:
                obj = Image(image=f)
                obj.save()   # post_save Signal Triggers optimize()
                created += 1
            except Exception as exc:
                errors.append(f'{f.name}: {exc}')

        if created:
            messages.success(self.request, f'{created} Image(s) Uploaded Successfully.')

        for err in errors:
            messages.error(self.request, err)

        return redirect(self.get_success_url())
