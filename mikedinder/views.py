from django.views.generic import TemplateView


class LandingView(TemplateView):
    """
    Home/Landing Page
    """
    template_name = 'mikedinder/home.html'
