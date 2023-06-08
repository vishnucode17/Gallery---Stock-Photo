from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("",views.Home,name="home"),
    path("view/<slug>",views.ImageView,name="image"),
    path("upload",views.ImageUpload,name="image_upload")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)