from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers
from django.urls import path
from . import views


auth_views = [
    path('auth/register', views.RegistroView.as_view()),
    path('auth/user', views.UserAPI.as_view()),
    path('auth/login/', TokenObtainPairView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('usuarios', views.UsersView.as_view()),
]

router = routers.DefaultRouter()
router.register("productos", views.ProductoView, "productos")
router.register("ordenes", views.OrdenView, "ordenes")


urlpatterns = auth_views + router.urls
