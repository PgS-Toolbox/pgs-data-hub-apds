from rest_framework import permissions
from rest_framework.routers import APIRootView, DefaultRouter

from ..url_utils import versioned_url
from parkings.api.places.views import PlacesViewSet


class PublicApiRootView(APIRootView):
    permission_classes = [permissions.AllowAny]


class Router(DefaultRouter):
    APIRootView = PublicApiRootView


router = Router()
router.register(r'places', PlacesViewSet, basename='places')

app_name = 'places'
urlpatterns = [
    versioned_url('v2', router.urls),
]