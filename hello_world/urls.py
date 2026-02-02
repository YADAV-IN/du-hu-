"""
URL configuration for hello_world project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from hello_world.core import views as core_views

urlpatterns = [
    path("", core_views.index, name='home'),
    path("society/<int:society_id>/", core_views.society_detail, name='society_detail'),
    path("events/", core_views.all_events, name='all_events'),
    
    # Chat API endpoints
    path("api/chat/global/", core_views.send_global_message, name='send_global_message'),
    path("api/chat/global/messages/", core_views.get_global_messages, name='get_global_messages'),
    path("api/chat/society/<int:society_id>/", core_views.send_society_message, name='send_society_message'),
    path("api/chat/society/<int:society_id>/messages/", core_views.get_society_messages, name='get_society_messages'),
    
    # Admin Panel Routes
    path("admin-login/", core_views.admin_login, name='admin_login'),
    path("admin-dashboard/", core_views.admin_dashboard, name='admin_dashboard'),
    path("manage-society/<int:society_id>/", core_views.manage_society, name='manage_society'),
    path("verify-code/<int:society_id>/", core_views.verify_access_code, name='verify_code'),
    path("admin-logout/", core_views.admin_logout, name='admin_logout'),
    path("admin-login-records/", core_views.admin_login_records, name='admin_login_records'),
    
    # Developer Admin Routes
    path("developer-login/", core_views.developer_login, name='developer_login'),
    path("developer-dashboard/", core_views.developer_dashboard, name='developer_dashboard'),
    path("create-admin/", core_views.create_admin, name='create_admin'),
    path("manage-admin/<int:admin_id>/", core_views.manage_admin, name='manage_admin'),
    path("developer-logout/", core_views.developer_logout, name='developer_logout'),
    
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
