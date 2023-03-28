from django.urls import path
from .views import (
    CalendarView,

    load_event_form,
    EventSaveView,
    EventDeleteView,

    load_business_hour_form,
    BusinessHourSaveView,
    BusinessHourDeleteView,
    
    load_staff_business_hour_form,
    StaffBusinessHourSaveView,
    StaffBusinessHourDeleteView,

    load_business_hour_break_form,
    BusinessHourBreakSaveView,
    BusinessHourBreakDeleteView,

    load_special_work_period_form,
    SpecialWorkPeriodSaveView,
    SpecialWorkPeriodDeleteView,
    
    load_staff_special_work_period_form,
    StaffSpecialWorkPeriodSaveView,
    StaffSpecialWorkPeriodDeleteView,
)

app_name = 'calendars'
urlpatterns = [
    path('', CalendarView.as_view(), name='calendar'),

    # Calendar | Event
    # -----------------------------------------------------------------------------------------------------------------
    path('calendar/events/load-form/', load_event_form, name='event-load-form'),
    path('calendar/events/create/', EventSaveView.as_view(), name='event-create'),
    path('calendar/events/<int:id>/update/', EventSaveView.as_view(), name='event-update'),
    path('calendar/events/<int:id>/delete/', EventDeleteView.as_view(), name='event-delete'),

    path('calendar/business-hours/load-form/', load_business_hour_form, name='business-hour-load-form'),
    path('calendar/business-hours/create/', BusinessHourSaveView.as_view(), name='business-hour-create'),
    path('calendar/business-hours/<int:id>/update/', BusinessHourSaveView.as_view(), name='business-hour-update'),
    path('calendar/business-hours/<int:id>/delete/', BusinessHourDeleteView.as_view(), name='business-hour-delete'),

    path('calendar/business-hour-breaks/load-form/', load_business_hour_break_form, name='business-hour-break-load-form'),
    path('calendar/business-hour-breaks/<slug:business_hour_id>/create/', BusinessHourBreakSaveView.as_view(), name='business-hour-break-create'),
    path('calendar/business-hour-breaks/<slug:business_hour_id>/<int:id>/update/', BusinessHourBreakSaveView.as_view(), name='business-hour-break-update'),
    path('calendar/business-hour-breaks/<int:id>/delete/', BusinessHourBreakDeleteView.as_view(), name='business-hour-break-delete'),
    
    path('calendar/staff-business-hours/load-form/', load_staff_business_hour_form, name='staff-business-hour-load-form'),
    path('calendar/staff-business-hours/create/', StaffBusinessHourSaveView.as_view(), name='staff-business-hour-create'),
    path('calendar/staff-business-hours/<int:id>/update/', StaffBusinessHourSaveView.as_view(), name='staff-business-hour-update'),
    path('calendar/staff-business-hours/<int:id>/delete/', StaffBusinessHourDeleteView.as_view(), name='staff-business-hour-delete'),
    
    path('calendar/special-work-periods/load-form/', load_special_work_period_form, name='special-work-period-load-form'),
    path('calendar/special-work-periods/create/', SpecialWorkPeriodSaveView.as_view(), name='special-work-period-create'),
    path('calendar/special-work-periods/<int:id>/update/', SpecialWorkPeriodSaveView.as_view(), name='special-work-period-update'),
    path('calendar/special-work-periods/<int:id>/delete/', SpecialWorkPeriodDeleteView.as_view(), name='special-work-period-delete'),
    
    path('calendar/staff-special-work-periods/load-form/', load_staff_special_work_period_form, name='staff-special-work-period-load-form'),
    path('calendar/staff-special-work-periods/create/', StaffSpecialWorkPeriodSaveView.as_view(), name='staff-special-work-period-create'),
    path('calendar/staff-special-work-periods/<int:id>/update/', StaffSpecialWorkPeriodSaveView.as_view(), name='staff-special-work-period-update'),
    path('calendar/staff-special-work-periods/<int:id>/delete/', StaffSpecialWorkPeriodDeleteView.as_view(), name='staff-special-work-period-delete'),
]