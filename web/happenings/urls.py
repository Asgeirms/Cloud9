from django.urls import path
from . import views


urlpatterns = [
    path('', views.EventListView.as_view(), name="events"),
    path('me/create/', views.SuggestEventView.as_view(), name='create_event'),
    path('me/', views.MyEventsListView.as_view(), name='my_events'),
    path('me/<int:pk>', views.DetailedMyEventView.as_view(), name="my_events_detailed"),
    path('<int:pk>', views.EventView.as_view(), name="events"),
    path('random', views.RandomEventView.as_view(), name='random_event'),
    path('filter', views.FilterEventListView, name="filter"),
]   
