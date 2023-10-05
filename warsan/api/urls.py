from django.urls import path
from . import views

urlpatterns = [
    path('ngo/signup/', views.ngo_signup, name='ngo-signup'),
    path('ngo/logout/', views.ngo_logout, name='ngo-logout'),
    path('customusers/', views.custom_user_list, name='customuser-list'),
    path('customusers/<int:pk>/', views.custom_user_detail, name='customuser-detail'),
    path('healthworkers/', views.healthworker_list, name='healthworker-list'),
    path('healthworkers/<int:pk>/', views.healthworker_detail, name='healthworker-detail'),
    path('healthworker/signup/', views.healthworker_signup, name='healthworker-signup'),
    path('healthworker/logout/', views.healthworker_logout, name='healthworker-logout'),
    path('healthworker/login/', views.healthworker_login, name='healthworker-login'),
    path('ngo/login/', views.ngo_login, name='ngo-login'),
    path('vaccine/', views.vaccine_list, name='vaccine-list'),  # Updated view name
    path('vaccine/<int:id>/', views.vaccine_detail, name='vaccine-detail'),  # Updated view name and URL parameter
    path('immunization_record/', views.immunization_record_list, name='immunization-record-list'),  # Updated view name
    path('immunization_record/<int:pk>/', views.immunization_record_detail, name='immunization-record-detail'),  # Updated view name and URL parameter
    path("location/", views.location_list, name="location-list"),  # Updated view name
    path("location/<int:id>/", views.location_detail, name="location-detail"),  # Updated view name and URL parameter
    path("states/", views.state_list, name="state-list"),
    path("states/", views.state_list, name="state-list"),
    path("specific_region/<str:state_name>/", views.specific_region_list, name="specific-region-list"),
    path("specific_district/<str:state_name>/<str:region_name>/", views.specific_district_list, name="specific-district-list"),
    path('children/', views.child_list, name='child-list'),
    path('children/<int:pk>/', views.child_detail, name='child-detail'),
    path('guardians/', views.guardian_list, name='guardian-list'),
    path('guardians/<int:pk>/', views.guardian_detail, name='guardian-detail'),

]
