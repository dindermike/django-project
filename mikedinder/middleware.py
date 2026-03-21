from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin


class LowercaseURLMiddleware(MiddlewareMixin):
    def process_request(self, request):
        full_path = request.get_full_path()

        if (
            '__debug__' not in full_path
            and '/rest_api/v1/' not in full_path
            and any(c.isupper() for c in full_path)
        ):
            # Reconstruct the URL with the path converted to lowercase
            # Use request.build_absolute_uri for a complete URL if needed
            # We need to handle query parameters correctly
            lowercase_path = full_path.lower()

            if lowercase_path != full_path:
                return HttpResponsePermanentRedirect(lowercase_path)

        # Continue with Normal Request Processing
        return None
