from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('create/<str:model>/', DynamicCreateView.as_view(), name='dynamic_create'),
    path('list/<str:model>/', DynamicListView.as_view(), name='dynamic_list'),
    path('delete/<str:model>/<int:pk>/', DynamicDeleteView.as_view(), name='dynamic_delete'),
    path('<str:model>/<int:pk>/update/', DynamicUpdateView.as_view(), name='dynamic_update'),
]
