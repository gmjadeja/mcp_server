from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from hello import views

# Customize admin site
admin.site.site_header = "MCP Education Admin"
admin.site.site_title = "MCP Education"
admin.site.index_title = "Welcome to MCP Education Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    path('courses/<slug:course_slug>/lessons/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
    path('labs/', views.lab_list, name='lab_list'),
    path('labs/<slug:slug>/', views.lab_detail, name='lab_detail'),
    path('paths/', views.learning_path_list, name='learning_path_list'),
    path('paths/<slug:slug>/', views.learning_path_detail, name='learning_path_detail'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
