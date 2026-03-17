"""
URL configuration for MikeDinder App.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path

from mikedinder.views import (
    ContactFormView,
    ContactSuccessView,
    LandingView,
)


app_name = 'mikedinder'


urlpatterns = [
    path('',                LandingView.as_view(),        name='home'           ),
    path('contact/',        ContactFormView.as_view(),    name='contact_form'   ),
    path('contact/thanks/', ContactSuccessView.as_view(), name='contact_success'),
]

if settings.DEBUG:
    from mikedinder.views import (
        preview_contact_email,
        preview_contact_user_email,
    )

    urlpatterns += [
        path('contact/preview/',      preview_contact_email,      name='contact_form_preview'),
        path('contact/user-preview/', preview_contact_user_email, name='contact_user_preview'),
    ]