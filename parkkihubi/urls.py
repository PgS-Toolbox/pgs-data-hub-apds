from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from parkings.api.auth import urls as auth_urls
from parkings.api.enforcement import urls as enforcement_urls
from parkings.api.monitoring import urls as monitoring_urls
from parkings.api.operator import urls as operator_urls
from parkings.api.public import urls as public_urls
from parkings.api.places import urls as places_urls
from parkings.api.sessions import urls as sessions_urls
from parkings.api.observations import urls as observations_urls
from parkings.api.rights import urls as rights_urls


urlpatterns = [
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
urlpatterns.append(url(r'^places/', include(places_urls)))
urlpatterns.append(url(r'^sessions/', include(sessions_urls)))
urlpatterns.append(url(r'^observations/', include(observations_urls)))
urlpatterns.append(url(r'^rights/', include(rights_urls)))


urlpatterns.extend([
    url(r'^admin/', admin.site.urls),
])
