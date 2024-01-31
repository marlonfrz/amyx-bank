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
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from payment import views

urlpatterns = i18n_patterns(
    path("__debug__/", include("debug_toolbar.urls")),
    path('', include('amyx_bank.urls')),
    path('account/', include('account.urls')),
    path('card/', include('card.urls')),
    path('payments/', include('payment.urls', namespace="payments")),
    path('payment/', views.payment, name='payment'),
    path('outgoing/', views.outgoing_transactions, name='outgoing'),
    path('transfer/incoming/', views.incoming_transactions, name='incoming'),
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('api/', include('account.api.urls', namespace='api_account')),
    path('api/', include('card.api.urls', namespace='api_card')),
    path('api/', include('payment.api.urls', namespace='api_payment')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
