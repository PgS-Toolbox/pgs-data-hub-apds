from rest_framework.routers import DefaultRouter

from ..url_utils import versioned_url
from parkings.api.sessions.views import SessionsViewSet


router = DefaultRouter()
router.register(r'sessions', SessionsViewSet, basename='sessions')

app_name = 'sessions'
urlpatterns = [
    versioned_url('apds', router.urls),
]
