"""
URL configuration for contractApp project.

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
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from contract import views
from contract.views import add_contract, card_contract, edit_contract, list_contract_admin, view_contract, view_contract_detail

from .views import  login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', include('django.contrib.auth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', login_view, name='login'),  # Show login page by default
    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),  # Index page after login
    path('contract/add/', add_contract, name='add_contract'),
    path('contract/edit/', edit_contract, name='edit_contract'),
    path('contract/', include('contract.urls')),
    path('contract/valid_contract',views.invoice_data_view, name='admin_list_contract' ),
    path('contract/card_valid_contract',card_contract, name='card_valid_contract' ),
    path('contract/view_contract', view_contract, name='view_contract'),
    path('contracts/view/<int:contract_id>/', view_contract_detail, name='details_contract'),
    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

