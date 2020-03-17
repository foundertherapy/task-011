from django.contrib import admin
from django.urls import path, include
from .router import router
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('login/', views.obtain_auth_token, name='login'),
    path('employee/', include('employee.urls')),

]
