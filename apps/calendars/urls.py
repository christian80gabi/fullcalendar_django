from django.urls import path
from apps.calendars import views

app_name = 'calendars'
urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),

    path('calendar/events/load-form/', views.load_event_form, name='event-load-form'),
    path('calendar/events/create/', views.EventSaveView.as_view(), name='event-create'),
    path('calendar/events/<int:id>/update/', views.EventSaveView.as_view(), name='event-update'),
    path('calendar/events/<int:id>/delete/', views.EventDeleteView.as_view(), name='event-delete'),

    path('calendar/business-hours/load-form/', views.load_business_hour_form, name='business-hour-load-form'),
    path('calendar/business-hours/create/', views.BusinessHourSaveView.as_view(), name='business-hour-create'),
    path('calendar/business-hours/<int:id>/update/', views.BusinessHourSaveView.as_view(), name='business-hour-update'),
    path('calendar/business-hours/<int:id>/delete/', views.BusinessHourDeleteView.as_view(), name='business-hour-delete'),

    path('calendar/business-hour-breaks/load-form/', views.load_business_hour_break_form, name='business-hour-break-load-form'),
    path('calendar/business-hour-breaks/<slug:business_hour_id>/create/', views.BusinessHourBreakSaveView.as_view(), name='business-hour-break-create'),
    path('calendar/business-hour-breaks/<slug:business_hour_id>/<int:id>/update/', views.BusinessHourBreakSaveView.as_view(), name='business-hour-break-update'),
    path('calendar/business-hour-breaks/<int:id>/delete/', views.BusinessHourBreakDeleteView.as_view(), name='business-hour-break-delete'),
    
    path('calendar/staff-business-hours/load-form/', views.load_staff_business_hour_form, name='staff-business-hour-load-form'),
    path('calendar/staff-business-hours/create/', views.StaffBusinessHourSaveView.as_view(), name='staff-business-hour-create'),
    path('calendar/staff-business-hours/<int:id>/update/', views.StaffBusinessHourSaveView.as_view(), name='staff-business-hour-update'),
    path('calendar/staff-business-hours/<int:id>/delete/', views.StaffBusinessHourDeleteView.as_view(), name='staff-business-hour-delete'),
    
    path('calendar/special-work-periods/load-form/', views.load_special_work_period_form, name='special-work-period-load-form'),
    path('calendar/special-work-periods/', views.SpecialWorkPeriodListView.as_view(), name='special-work-period-list'),
    path('calendar/special-work-periods/create/', views.SpecialWorkPeriodSaveView.as_view(), name='special-work-period-create'),
    path('calendar/special-work-periods/<int:id>/update/', views.SpecialWorkPeriodSaveView.as_view(), name='special-work-period-update'),
    path('calendar/special-work-periods/<int:id>/delete/', views.SpecialWorkPeriodDeleteView.as_view(), name='special-work-period-delete'),
    
    path('calendar/staff-special-work-periods/load-form/', views.load_staff_special_work_period_form, name='staff-special-work-period-load-form'),
    path('calendar/staff-special-work-periods/create/', views.StaffSpecialWorkPeriodSaveView.as_view(), name='staff-special-work-period-create'),
    path('calendar/staff-special-work-periods/<int:id>/update/', views.StaffSpecialWorkPeriodSaveView.as_view(), name='staff-special-work-period-update'),
    path('calendar/staff-special-work-periods/<int:id>/delete/', views.StaffSpecialWorkPeriodDeleteView.as_view(), name='staff-special-work-period-delete'),

]