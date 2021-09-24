from django.urls import path
from . import views


urlpatterns = [
    path('', views.EventList.as_view(), name="events"),
    path('me/create/', views.AddNewEvent.as_view(), name='create_event'),
    path('me/', views.MyEventsView.as_view(), name='my_events'),
    path('me/<int:pk>', views.DetailedEventView.as_view(), name="detail"),
    path('<int:pk>', views.EventView.as_view(), name="events"),
    path('random', views.RandomEventView.as_view(), name='spesific_event'),
]   

