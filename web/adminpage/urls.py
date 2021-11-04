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
    path('interest_categories', views.InterestCategoryListView.as_view(), name="interest_categories"),
    path('interest_categories/create', views.CreateInterestCategory.as_view(), name="add_interest_categories"),
    path('interest_categories/<int:pk>/edit', views.EditInterestCategory.as_view(), name="edit_interest_categories"),
    path('interest_categories/<int:pk>/delete', views.DeleteInterestCategory.as_view(), name="delete_interest_categories"),
    path('requirement_category', views.RequirementCategoryListView.as_view(), name="requirement_categories"),
    path('requirement_category/create', views.CreateRequirementCategory.as_view(), name="add_requirement_categories"),
    path('requirement_category/<int:pk>/edit', views.EditRequirementCategory.as_view(), name="edit_requirement_categories"),
    path('requirement_category/<int:pk>/delete', views.DeleteRequirementCategory.as_view(), name="delete_requirement_categories"),


]
