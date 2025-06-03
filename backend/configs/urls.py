"""
URL configuration for configs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.urls import include, path

from rest_framework.permissions import AllowAny

from configs import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
  openapi.Info(
    title="AutoRia-Clone",
    default_version='v1',
    description="AutoRia-Clone",
    contact=openapi.Contact(email="autoriatest@clone.send"),
  ),
  public=True,
  permission_classes=[AllowAny],
)

urlpatterns = [
  path('api/auth', include('apps.auth.urls')),
  path('api/user', include('apps.user.urls')),
  path('api/sellers',include('apps.sellers.urls')),
  path('api/listings',include('apps.listings.urls')),
  path('api/car_brand',include('apps.car_brand.urls')),
  path('api/car_model',include('apps.car_model.urls')),
  path('api/forbidden_word', include('apps.forbiddenword.urls')),
  path('api/auto_salon', include('apps.auto_salon.urls')),
  path('api/salon_role', include('apps.salon_role.urls')),
  path('api/invitation_to_auto_salon', include('apps.invitation_to_auto_salon.urls')),
  path('api/auto_salon_listing', include('apps.auto_salon_listings.urls')),
  path('api/chat', include('apps.chat.urls')),
  path('api/doc', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
