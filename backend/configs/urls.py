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

from configs import settings

urlpatterns = [
  path('api/auth', include('apps.auth.urls')),
  path('api/user', include('apps.user.urls')),
  path('api/sellers',include('apps.sellers.urls')),
  path('api/listings',include('apps.listings.urls')),
  path('api/car_brand',include('apps.car_brand.urls')),
  path('api/car_model',include('apps.car_model.urls')),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
