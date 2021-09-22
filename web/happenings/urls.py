from django.urls import path
from .views import DisplayEventsView, AddEventView

urlpatterns = [
    path('', DisplayEventsView.as_view(), name='all_events'),
    path('create/', AddEventView.as_view(), name='create_event'),
]