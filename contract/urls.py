
from queue import Full

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from contract import views

urlpatterns = [
    path('add/', views.add_contract, name='add_contract'),
    path('list/', views.list_contract, name='list_contract'),
    path('edit/<int:contract_id>/', views.edit_contract, name='edit_contract'),
    path('ajax/load-gouvernorats/', views.get_all_gouvernorats, name='ajax_load_gouvernorats'),
    path('ajax/load-delegations/', views.load_delegations, name='ajax_load_delegations'),
    path('ajax/load-localites/', views.load_localites, name='ajax_load_localites'),
    path('ajax/load-code-postal/', views.ajax_load_code_postal, name='ajax_load_code_postal'),
    path('test-view/', views.test_view, name='test_view'),
    path('get_coordinates/', views.get_coordinates, name='get_coordinates'),
    path('approve/<int:contract_id>/', views.approve_contract, name='approve_contract'),
    path('reject/<int:contract_id>/', views.reject_contract, name='reject_contract'),
   
    path('add_invoice/', views.add_invoice, name='add_invoice'),
    path('list-invoice/', views.list_invoices, name='list_invoice'),
     path('download-invoice/<int:invoice_id>/', views.download_invoice, name='download_invoice'),
    path('invoice/<int:invoice_id>/', views.view_invoice, name='view_invoice'),
    path('invoices/update/<int:pk>/', views.update_invoice, name='update_invoice'),
    path('invoices/delete/<int:pk>/', views.delete_invoice, name='delete_invoice'),
    path('invoices/card-invoices/', views.card_invoices_admin, name='card_invoices'),
    path('contract/valid_contract', views.admin_dashboard, name='admin_list_contract'),
  
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
