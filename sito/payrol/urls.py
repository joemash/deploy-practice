from django.urls import path
from .views import BaseView

urlpatterns = [
    path(r'',BaseView.as_view(),name='payrol'),
]