from django.urls import path
from . import views


urlpatterns = [
    path('', views.FilterEventListView, name='filtered_event_list'),
    path('me/create/', views.SuggestEventView.as_view(), name='create_event'),
    path('me/<int:pk>/delete', views.DeleteEventView.as_view(), name='delete_event'),
    path('me/', views.MyEventsListView.as_view(), name='my_events'),
    path('me/<int:pk>', views.DetailedMyEventView.as_view(), name='my_events_detailed'),
    path('me/schedule/<int:pk>', views.DetailedMyScheduleView.as_view(), name="my_schedule_detailed"),
    path('<int:pk>', views.ScheduleDetailView.as_view(), name='schedule_detail'),
    path('me/<int:pk>/edit', views.EditEventView.as_view(), name='edit_event'),
    path('me/<int:pk>/editSchedule', views.EditScheduleView.as_view(), name='edit_schedule'),
    path('me/<int:pk>/create', views.AddScheduleView.as_view(), name='add_schedule'),
    path('me/<int:event_pk>/<int:pk>/cancel', views.DeleteScheduleView.as_view(), name='cancel_schedule'),
    path('xml', views.ExportXMLView, name="export_xml")
]
