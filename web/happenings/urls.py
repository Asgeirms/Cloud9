from django.urls import path
from .views import DisplayEventsView, AddEventView, EventList, RandomEventView, EventView

urlpatterns = [
    path('', EventList.as_view(), name="all_events"),
    path('<int:pk>', EventView.as_view(), name="events"),
    path('random', RandomEventView.as_view(), name='spesific_event'),
    path('create/', AddEventView.as_view(), name='create_event'),
]
