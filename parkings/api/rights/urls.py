from rest_framework.routers import DefaultRouter

from ..url_utils import versioned_url
from parkings.api.rights.views import AssignedRightsViewSet, RightsSpecificationsViewSet


router = DefaultRouter()
router.register(r'rights/assigned', AssignedRightsViewSet, basename='assigned-rights')
router.register(r'rights/specs', RightsSpecificationsViewSet, basename='rights-specifications')

app_name = 'rights'
urlpatterns = [
    versioned_url('v2', router.urls),
]