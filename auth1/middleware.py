from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import MultipleObjectsReturned
from django.urls import reverse
from .models import Visit

class VisitCounterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Get the path visited
        page_visited = request.path

        # Check if the request path is for Django admin
        if page_visited.startswith(reverse('admin:index')):
            return None  # Skip counting visits for admin URLs

        try:
            # Try to get the Visit object for the current page_visited
            visit = Visit.objects.get(page_visited=page_visited)
        except Visit.DoesNotExist:
            # If the Visit object does not exist, create a new one
            visit = Visit.objects.create(page_visited=page_visited, visit_count=1)
        except MultipleObjectsReturned:
            # If multiple Visit objects are returned, handle by choosing the first one
            visit = Visit.objects.filter(page_visited=page_visited).first()

        # Increment visit count and save the Visit object
        visit.visit_count += 1
        visit.save()

        # Continue processing the request
        return None
