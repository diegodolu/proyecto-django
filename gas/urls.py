from django.urls import path
from . import views

urlpatterns = [
    path('distributor_data/<int:distributor_id>/', views.distributor_data, name='distributor_data'),
    path('consumption_data/<int:distributor_id>/', views.consumption_data, name='consumption_data'),
    path('sales_data/<int:distributor_id>/', views.sales_data, name='sales_data'),
    path('weight_data/<int:distributor_id>/', views.weight_data, name='sales_data_by_weight'),
]