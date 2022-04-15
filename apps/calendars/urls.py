from django.urls import path

from .views import Calendar1View, load_calendar_form, update_calendar_form

urlpatterns = [
    path('', Calendar1View.as_view(), name='calendar_1'),
    path('update-event/<int:id>/', Calendar1View.as_view(),
         name='update-even'),
    path('add-event-form/', load_calendar_form, name='load-calendar-form'),
    path('update-event-form/',
         update_calendar_form,
         name='update-calendar-form'),
]