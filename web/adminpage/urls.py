from django.urls import path

from adminpage import views

urlpatterns = [
    path('', views.AdminpanelView.as_view(), name="adminpanel"),
    path('curate', views.CurateEventsView.as_view(), name="curate_events"),
    path('event/<int:pk>', views.AdminEventDetailView.as_view(), name="admin_events"),
    path('event/disapprove/<int:pk>', views.AdminEventDetailView.disapprove, name="disapprove"),
    path('event/approve/<int:pk>', views.AdminEventDetailView.approve, name="approve"),
    path('event/delete/<int:pk>', views.AdminEventDetailView.delete, name="delete"),
    path('event/<int:pk>/delete', views.DeleteEventAdminView.as_view(), name="delete_event_admin"),
    path('event/<int:pk>/restore', views.AdminEventDetailView.restore, name="restore"),
    path('descriptions', views.ShortDescriptionListView.as_view(), name="descriptions"),
    path('descriptions/create', views.CreateShortDescriptionView.as_view(), name="add_short_description"),
    path('description/<int:pk>/edit', views.EditShortDescriptionView.as_view(), name="edit_short_description"),
    path('description/<int:pk>/delete', views.DeleteShortDescriptionView.as_view(), name="delete_short_description"),
    path('event_categories', views.EventCategoryListView.as_view(), name="event_categories"),
    path('event_categories/create', views.CreateEventCategory.as_view(), name="add_event_categories"),
    path('event_categories/<int:pk>/edit', views.EditEventCategory.as_view(), name="edit_event_categories"),
    path('event_categories/<int:pk>/delete', views.DeleteEventCategory.as_view(), name="delete_event_categories"),
    path('accessibility_tags', views.AccessibilityTagsListView.as_view(), name="accessibility_tags"),
    path('accessibility_tags/create', views.CreateAccessibilityTag.as_view(), name="add_accessibility_tag"),
    path('accessibility_tags/<int:pk>/edit', views.EditAccessibilityTag.as_view(), name="edit_accessibility_tag"),
    path('accessibility_tags/<int:pk>/delete', views.DeleteAccessibilityTag.as_view(), name="delete_accessibility_tag"),

]
