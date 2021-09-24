from django.urls import path

from . import views

urlpatterns = [
    path('', views.EventList.as_view(), name="events"),
    path('<int:pk>', views.EventView.as_view(), name="events"),
    path('random', views.RandomEventView.as_view(), name='spesific_event'),
]