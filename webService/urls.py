from django.contrib import admin
from django.urls import path, include, re_path
from webServiceApplication import views
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()
router.register(r'tickets', views.TicketViewSet, basename='tickets')
router.register(r'events', views.EventViewSet, basename='events')

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
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('registration/', views.RegistrationAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
]
