from django.urls import path
from . import views


urlpatterns = [
    path('', views.SwipingEventsView.as_view(), name="swiping"),
    path('swiping/finish', views.FinishSwipingView.as_view(), name="swiping_finish")
]
