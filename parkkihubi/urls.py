from django.conf import settings
from django.conf.urls import include, url, re_path
from django.contrib import admin

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from parkings.api.auth import urls as auth_urls
from parkings.api.enforcement import urls as enforcement_urls
from parkings.api.monitoring import urls as monitoring_urls
from parkings.api.operator import urls as operator_urls
from parkings.api.public import urls as public_urls
from parkings.api.places import urls as places_urls
from parkings.api.sessions import urls as sessions_urls
from parkings.api.observations import urls as observations_urls
from parkings.api.rights import urls as rights_urls


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^auth/', include(auth_urls)),
]

if getattr(settings, 'PARKKIHUBI_PUBLIC_API_ENABLED', False):
    urlpatterns.append(url(r'^public/', include(public_urls)))

if getattr(settings, 'PARKKIHUBI_MONITORING_API_ENABLED', False):
    urlpatterns.append(url(r'^monitoring/', include(monitoring_urls)))

if getattr(settings, 'PARKKIHUBI_OPERATOR_API_ENABLED', False):
    urlpatterns.append(url(r'^operator/', include(operator_urls)))

if getattr(settings, 'PARKKIHUBI_ENFORCEMENT_API_ENABLED', False):
    urlpatterns.append(url(r'^enforcement/', include(enforcement_urls)))

#if getattr(settings, 'APDS_API_ENABLED', False):
urlpatterns.append(url(r'^', include(places_urls)))
urlpatterns.append(url(r'^', include(sessions_urls)))
urlpatterns.append(url(r'^', include(observations_urls)))
urlpatterns.append(url(r'^', include(rights_urls)))


urlpatterns.extend([
    url(r'^admin/', admin.site.urls),
])
