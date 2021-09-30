from django.urls import path

from adminpage import views

urlpatterns = [
    path('', views.CurateEventsView.as_view(), name="curateEvents"),
    ]