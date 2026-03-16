from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from rest_framework.views import APIView

from .models import Restaurant
from .utils import RestaurantSearchService


class RestaurantSearchView(APIView):
    """
    POST /rest_api/v1/restaurants/search/
    Search Restaurants by datetime string parameter and return a list of restaurants that are open during that time.
    """
    def get_queryset(self):
        return Restaurant.objects.all()

    def get(self, request, *args, **kwargs):
        """
        Search Restaurants by datetime
        GET: /rest_api/v1/restaurants/search/?datetime=2026-02-14%2010:30
        GET: /rest_api/v1/restaurants/search/?datetime=2026-02-14%2015:30
        GET: /rest_api/v1/restaurants/search/?datetime=2026-02-14%2023:30
        """
        datetime_str = request.GET.get('datetime')

        if not datetime_str:
            return JsonResponse({'Error': 'datetime Parameter Required'}, status=400)

        try:
            open_restaurants = RestaurantSearchService.search_open_restaurants(datetime_str)

            return JsonResponse({
                'datetime': datetime_str,
                'open_restaurants': open_restaurants,
                'count': len(open_restaurants)
            })
        except ValueError as e:
            return JsonResponse({'Error': str(e)}, status=400)


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
    permanent    = True
    query_string = False
    pattern_name = 'rest_api:rest_examples'

    def get_redirect_url(self, *args, **kwargs):
        return super().get_redirect_url(*args, **kwargs)
