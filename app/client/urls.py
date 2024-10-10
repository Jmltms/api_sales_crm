from django.urls import (
    path,
    include
)

from client import (
    views,
    client_external_view
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.ClientView, basename='client')
router.register(
    'external',
    client_external_view.ExternalView,
    basename='external_api'
)

app_name = 'client'

urlpatterns = [
    path('', include(router.urls))
]
