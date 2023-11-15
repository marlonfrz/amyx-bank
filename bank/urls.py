"""
URL configuration for bank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from payment import views

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path('', include('amyx_bank.urls')),
    path('account/', include('account.urls')),
    path('card/', include('card.urls')),
    path('admin/', admin.site.urls),
    path('payments/', include('payment.urls')),
    path('payment/', views.payment, name='payment'),
    path('outoging/', views.outgoing_transactions, name='outgoing'),
    path('incoming/', views.incoming_transactions, name='incoming'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)