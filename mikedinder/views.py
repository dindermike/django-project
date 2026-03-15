from django.views.generic import TemplateView


class LandingView(TemplateView):
    """
    Home/Landing Page
    """
    template_name = 'mikedinder/pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['branded_title'] = 'Django'
        context['meta_description'] = 'Django Framework — A comprehensive guide to the history, ecosystem, and usage ' \
            'of the Django web framework.'
        context['page_class'] = 'home-page'
        context['page_id'] = 'home-page'
        context['title'] = 'Django: The Framework for Perfectionists with Deadlines'

        return context
