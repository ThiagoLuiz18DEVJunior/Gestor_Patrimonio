from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('<str:model>/<int:pk>/update/', DynamicUpdateView.as_view(), name='dynamic_update'),

]
