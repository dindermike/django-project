from django.urls import path

from gallery.views import (
    GalleryView,
    ImageUploadView,
    BulkImageUploadView,
)

app_name = 'gallery'

urlpatterns = [
    path('',             GalleryView.as_view(),         name='gallery'),
    path('upload/',      ImageUploadView.as_view(),     name='upload'),
    path('upload/bulk/', BulkImageUploadView.as_view(), name='bulk_upload'),
]
