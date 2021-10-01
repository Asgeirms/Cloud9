from django.urls import path

from adminpage import views

urlpatterns = [
    path('', views.CurateEventsView.as_view(), name="curateEvents"),
    path('event/<int:pk>', views.AdminEventDetailView.as_view(), name="adminEvents"),
    path('event/disapprove/<int:pk>', views.AdminEventDetailView.disapprove, name="disapprove"),
    path('event/approve/<int:pk>', views.AdminEventDetailView.approve, name="approve"),

]
