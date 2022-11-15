from rest_framework.routers import DefaultRouter

from ..url_utils import versioned_url
from parkings.api.observations.views import ObservationsViewSet


router = DefaultRouter()
router.register(r'observations', ObservationsViewSet, basename='observations')

app_name = 'observations'
urlpatterns = [
    versioned_url('v2', router.urls),
]