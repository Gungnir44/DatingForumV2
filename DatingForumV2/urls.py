from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import dashboard  # ✅ Import the dashboard view

urlpatterns = [
    path('admin/', admin.site.urls),  # ✅ Admin panel
    path('users/', include('users.urls')),  # ✅ Include user-related URLs
    path('dashboard/', dashboard, name='dashboard'),  # ✅ Dashboard URL
    path('', dashboard, name='home'),  # ✅ Redirect the home page to the dashboard
]

# ✅ Correct way to serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
