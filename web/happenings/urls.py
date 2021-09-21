from django.urls import path
from .views import DisplayEventsView, AddNewEvent, MyEventsView

urlpatterns = [
    path('', DisplayEventsView.as_view(), name='all_events'),
    path('me/create/', AddNewEvent.as_view(), name='create_event'),
    path('me/', MyEventsView.as_view(), name='my_events'),
]