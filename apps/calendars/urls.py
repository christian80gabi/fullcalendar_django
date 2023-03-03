from django.urls import path
from .views import (
    CalendarView,
    load_event_form,
    EventSaveView,
    EventDeleteView,
)

app_name = 'calendars'
urlpatterns = [
    path('', CalendarView.as_view(), name='calendar'),

    # Calendar | Event
    # -----------------------------------------------------------------------------------------------------------------
    path('events/load-form/', load_event_form, name='event-load-form'),
    path('events/create/', EventSaveView.as_view(), name='event-create'),
    path('events/<int:id>/update/', EventSaveView.as_view(), name='event-update'),
    path('events/<int:id>/delete/', EventDeleteView.as_view(), name='event-delete'),
]