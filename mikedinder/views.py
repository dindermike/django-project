from django.http import JsonResponse
from rest_framework.views import APIView

from .models import Restaurant
# from .serializers import BookSerializer
from .utils import RestaurantSearchService


class RestaurantSearchView(APIView):
    """
    POST /api/v1/restaurants/search/
    Search Restaurants by datetime string parameter and return a list of restaurants that are open during that time.
    """
    def get_queryset(self):
        return Restaurant.objects.all()

    def get(self, request, *args, **kwargs):
        """
        Search Restaurants by datetime
        GET: /api/v1/restaurants/search/?datetime=2026-02-14%2010:30
        GET: /api/v1/restaurants/search/?datetime=2026-02-14%2015:30
        GET: /api/v1/restaurants/search/?datetime=2026-02-14%2023:30
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
