from django import forms

from gallery.models import Image


class ImageUploadForm(forms.ModelForm):
    """
    Single image upload with optional metadata.
    """
    class Meta:
        model  = Image
        fields = ['image', 'title', 'subtitle', 'description', 'date', 'location', 'order']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class BulkImageUploadForm(forms.Form):
    """
    Upload multiple image files at once.
    Metadata fields are intentionally absent — images are created
    with blank metadata and can be edited individually in the Admin.
    """
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}),
        label='Select Images (Hold Ctrl / ⌘ to Select Multiple)',
    )
