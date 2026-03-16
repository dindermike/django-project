"""
URL configuration for Rest API Django Project.

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
from django.urls import path, re_path

from rest_api.views import RESTExamplesView, RESTExamplesViewRedirectView


app_name = 'rest_api'


urlpatterns = [
    path('examples/', RESTExamplesView.as_view(), name='rest_examples'),

    # Manual Handling of Uppercase/Lowercase without the use of the Custom "LowercaseURLMiddleware"
    # re_path(r'examples/$',    RESTExamplesView.as_view(),             name='rest_examples'         ),
    # re_path(r'[Ee]xamples/$', RESTExamplesViewRedirectView.as_view(), name='rest_examples_redirect'),
]
