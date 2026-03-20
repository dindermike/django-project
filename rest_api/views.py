from django.views.generic import TemplateView
from django.views.generic.base import RedirectView


class RESTExamplesView(TemplateView):
    """
    REST API Examples Page
    """
    template_name = 'rest_api/pages/examples.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['branded_title'] = 'DRF'
        context['meta_description'] = 'Django REST API — A compilation of REST API URLs created to demonstrate the ' \
            'capabilities of the Django REST Framework and Mike\'s abilities to wire them up.'
        context['page_class'] = 'rest_examples-page'
        context['page_id'] = 'rest_examples-page'
        context['title'] = 'Django REST Framework Examples'

        return context


class RESTExamplesViewRedirectView(RedirectView):
    permanent = True
    query_string = False
    pattern_name = 'rest_api:rest_examples'

    def get_redirect_url(self, *args, **kwargs):
        return super().get_redirect_url(*args, **kwargs)
