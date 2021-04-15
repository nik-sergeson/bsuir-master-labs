"""svhn_ui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from svhn_ui import settings
from svhn_ui.views import ProcessImageView, UploadView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', UploadView.as_view(), name="upload_view"),
                  path('process_image', ProcessImageView.as_view(), {"use_autocrop": False}, name="process_image"),
                  path('process_image/with_autocrop', ProcessImageView.as_view(), {"use_autocrop": True},
                       name="process_image_with_autocrop"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
