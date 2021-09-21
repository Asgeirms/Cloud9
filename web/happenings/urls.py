from django.urls import path
from .views import DisplayEventsView, AddNewEvent

urlpatterns = [
    path('', DisplayEventsView.as_view(), name='all_events'),
    path('create/', AddNewEvent.as_view(), name='create_event'),
]