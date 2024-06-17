from datetime import datetime, date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.core.serializers import json
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext
from django.views import View
from apps.calendars import forms
from apps.calendars import models
from apps.calendars import services


'''-------------------------------------------- CALENDAR VIEWS --------------------------------------------------------'''


class CalendarView(View):
    template_name = "calendars/calendar.html"
    context = {}
    greeting = 'Hey'

    def get(self, request, *args, **kwargs):
        # ----------- Greetings ----------- #
        now = datetime.now().hour
        if now < 12:
            self.greeting = 'Good morning'
        elif now < 18:
            self.greeting = 'Good afternoon'
        elif now < 24:
            self.greeting = 'Good evening'

        business_hours = models.BusinessHour.objects.all()
        staff_business_hours = models.StaffBusinessHour.objects.all()
        special_work_periods = models.SpecialWorkPeriod.objects.all()
        staff_special_work_periods = models.StaffSpecialWorkPeriod.objects.all()
        events = models.Event.objects.all().order_by('start_date')

        global_business_hour = models.StaffBusinessHour.objects.filter(is_main=True).first()

        self.context = {
            'business_hours': business_hours,
            'staff_business_hours': staff_business_hours,
            'global_business_hour': global_business_hour,
            'special_work_periods': special_work_periods,
            'staff_special_work_periods': staff_special_work_periods,
            'events': events,
        }

        return render(request, self.template_name, self.context)


'''------------------------------------------- EVENT VIEWS --------------------------------------------------------'''


# Calendar | Event Load Form View
# ---------------------------------------------------------------------------------------------------------------------
def load_event_form(request):  # AJAX CALL
    object_id = None
    start_date = None
    end_date = None
    start_time = None
    end_time = None

    if services.is_ajax(request=request):
        object_id = request.POST.get('object_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

    obj = None
    # CREATE
    form = forms.EventModelForm(initial={
        'start_date': start_date,
        'end_date': end_date,
        'start_time': start_time,
        'end_time': end_time
    })

    # UPDATE
    if object_id is not None and object_id != '':
        obj = models.Event.objects.get(id=object_id)
        form = forms.EventModelForm(instance=obj)

    return render(
        request,
        "calendars/event_form.html",
        {
            "form": form,
            "object": obj,
        }
    )


# Calendar | Event Save View
# ---------------------------------------------------------------------------------------------------------------------
class EventSaveView(View):
    template_name = 'calendars/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        obj = services.get_object(self, models.Event)
        message = 'Enregistrement reussi!'

        if obj:
            was_repeated = bool(obj.is_repeated)
            form = forms.EventModelForm(request.POST, instance=obj)

            try:
                parent_event = obj
                if obj.repeat_parent:
                    print('looking for parent event!')
                    parent_event = models.Event.objects.filter(reference=obj.repeat_parent).first()

                print('parent ref', parent_event.reference)
            except Exception as e:
                print('ERROR', e)
                messages.info(request, "Error when looking for parent event")
                parent_event = None
        else:
            form = forms.EventModelForm(request.POST)

        if form.is_valid():
            if obj and 'allTheSeries' in request.POST and parent_event:
                message = self.update_event_series(parent_event, form)

            if 'currentOne' in request.POST:
                # Update only the current one without repetition
                print('only the current one')
                obj_saved = form.save()
                if not obj:
                    message = obj_saved.repeat_it()
                else:
                    copies = models.Event.objects.filter(repeat_parent=obj.reference)
                    if not was_repeated and not obj.repeat_parent and not copies:
                        message = obj_saved.repeat_it()

            print(message)
            messages.info(request, message)
        
        return redirect('globals:calendar')


    def update_event_series(self, parent_event, form):
        print('All series')
        # Delete all previously saved without the original one
        models.Event.objects.filter(repeat_parent=parent_event.reference).delete()
    
        # Then update the original one
        saved_obj = models.Event.objects.filter(reference=parent_event.reference).update(
            name = form.cleaned_data['name'],
            start_date = form.cleaned_data['start_date'],
            end_date = form.cleaned_data['end_date'],
            start_time = form.cleaned_data['start_time'],
            end_time = form.cleaned_data['end_time'],
            location = form.cleaned_data['location'],
            description = form.cleaned_data['description'],
            color = form.cleaned_data['color'],
            type = form.cleaned_data['type'],
            is_repeated = form.cleaned_data['is_repeated'],
            recurrence = form.cleaned_data['recurrence'],
            repeat_by = form.cleaned_data['repeat_by'],
            repeat_end_date = form.cleaned_data['repeat_end_date'],
            occurrence = form.cleaned_data['occurrence']
        )

        # Finally repeat it
        obj = models.Event.objects.get(reference=parent_event.reference)
        return obj.repeat_it()


# Recruitment | Event Delete View
# ---------------------------------------------------------------------------------------------------------------------
class EventDeleteView(View):
    template_name = 'calendars/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        if obj := services.get_object(self, models.Event):
            all_the_series = request.POST.get('allTheSeries')

            if not all_the_series:
                # Delete only the current event
                obj.delete()

            else:
                try:
                    parent_event = obj
                    if obj.repeat_parent:
                        print('looking for parent event!')
                        parent_event = models.Event.objects.filter(reference=obj.repeat_parent).first()

                except Exception as e:
                    parent_event = None
                    print(e)
                    messages.info(request, "Erreur de mise à jour de toute la série.")

                if parent_event:
                    # Delete the original event and its copies
                    models.Event.objects.filter(repeat_parent=parent_event.reference).delete()
                    parent_event.delete()

        return redirect('globals:calendar')


'''------------------------------------------- BUSINESS HOUR VIEWS --------------------------------------------------------'''


# Calendar | Business Hour Load Form View
# ---------------------------------------------------------------------------------------------------------------------
def load_business_hour_form(request):  # AJAX CALL
    obj = None
    object_id = None
    start_time = None
    end_time = None

    if services.is_ajax(request=request):
        object_id = request.POST.get('object_id')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

    print('object_id * ', object_id, '*', type(object_id))
    
    # CREATE
    form = forms.BusinessHourModelForm(initial={
        'start_time': start_time,
        'end_time': end_time
    })

    # UPDATE
    if object_id and object_id != 'None':
        obj = models.BusinessHour.objects.get(id=object_id)
        form = forms.BusinessHourModelForm(instance=obj)

    return render(
        request,
        "calendars/business_hour_form.html",
        {
            "form": form,
            "object": obj,
        }
    )


# Calendar | Business Hour Save View
# ---------------------------------------------------------------------------------------------------------------------
class BusinessHourSaveView(View):
    template_name = 'calendars/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        if obj := services.get_object(self, models.BusinessHour):
            form = forms.BusinessHourModelForm(request.POST, instance=obj)
        else:
            form = forms.BusinessHourModelForm(request.POST)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.days_of_week = form.cleaned_data['day_list']
            obj.save()
            messages.info(request, 'Enregistrement reussi!')

        return redirect('globals:calendar')


# Calendar | Business Hour Delete View
# ---------------------------------------------------------------------------------------------------------------------
class BusinessHourDeleteView(View):
    template_name = 'calendars/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        obj = services.get_object(self, models.BusinessHour)
        if obj is not None:
            obj.delete()

        return redirect('globals:calendar')


'''------------------------------------------- BUSINESS HOUR BREAK VIEWS --------------------------------------------------------'''


# Calendar | Business Hour Break Load Form View
# ---------------------------------------------------------------------------------------------------------------------
def load_business_hour_break_form(request):  # AJAX CALL
    obj = None
    object_id = None
    start_time = None
    end_time = None
    business_hour_id = None

    if services.is_ajax(request=request):
        object_id = request.POST.get('object_id')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        business_hour_id = request.POST.get('business_hour_id')

    print('object_id * ', object_id, '*', type(object_id))
    
    # CREATE
    form = forms.DayBreakHourModelForm(initial={
        'start_time': start_time,
        'end_time': end_time
    })

    # UPDATE
    if object_id and object_id != 'None':
        obj = models.DayBreakHour.objects.get(id=object_id)
        form = forms.DayBreakHourModelForm(instance=obj)

    return render(
        request,
        "calendars/business_hour_break_form.html",
        {
            "form": form,
            "object": obj,
            "business_hour_id": business_hour_id,
        }
    )


# Calendar | Business Hour Save View
# ---------------------------------------------------------------------------------------------------------------------
class BusinessHourBreakSaveView(View):
    template_name = 'calendars/calendar.html'
    context = {}

    def post(self, request, business_hour_id, *args, **kwargs):
        if obj := services.get_object(self, models.DayBreakHour):
            form = forms.DayBreakHourModelForm(request.POST, instance=obj)
        else:
            form = forms.DayBreakHourModelForm(request.POST)
        
        if form.is_valid():
            saved_obj = form.save()

            print('DayBreakHour * ', saved_obj)

            if business_hour_id and not obj:
                
                models.BusinessHourBreak(
                    business_hour = models.BusinessHour.objects.get(id=business_hour_id),
                    day_break_hour = saved_obj,
                ).save()

            messages.info(request, 'Enregistrement reussi!')

        return redirect('globals:calendar')


# Calendar | Business Hour Delete View
# ---------------------------------------------------------------------------------------------------------------------
class BusinessHourBreakDeleteView(View):
    template_name = 'calendars/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        obj = services.get_object(self, models.DayBreakHour)
        if obj is not None:
            obj.delete()

        return redirect('globals:calendar')


'''------------------------------------------- STAFF BUSINESS HOUR VIEWS --------------------------------------------------------'''


# Calendar | Business Hour Load Form View
# ---------------------------------------------------------------------------------------------------------------------
def load_staff_business_hour_form(request):  # AJAX CALL
    obj = None
    object_id = request.POST.get('object_id') if services.is_ajax(request=request) else None
    print('object_id * ', object_id, '*', type(object_id))

    # CREATE
    form = forms.StaffBusinessHourModelForm()

    # UPDATE
    if object_id and object_id != 'None':
        obj = models.StaffBusinessHour.objects.get(id=object_id)
        form = forms.StaffBusinessHourModelForm(instance=obj)

    return render(
        request,
        "calendars/staff_business_hour_form.html",
        {
            "form": form,
            "object": obj,
        }
    )


# Calendar | Staff Business Hour Save View
# ---------------------------------------------------------------------------------------------------------------------
class StaffBusinessHourSaveView(View):
    template_name = 'calendars/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        from django.core.exceptions import ValidationError
        if obj := services.get_object(self, models.StaffBusinessHour):
            form = forms.StaffBusinessHourModelForm(request.POST, instance=obj)
        else:
            form = forms.StaffBusinessHourModelForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.info(request, 'Enregistrement reussi !')
            return redirect('globals:calendar')

        messages.warning(request, "Erreur d'enregistrement. Vous ne pouvez avoir qu'une seule heure de travail par groupe.")
        return redirect('globals:calendar')


# Calendar | Staff Business Hour Delete View
# ---------------------------------------------------------------------------------------------------------------------
class StaffBusinessHourDeleteView(View):
    template_name = 'calendars/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        obj = services.get_object(self, models.StaffBusinessHour)
        if obj is not None:
            obj.delete()
        
        return redirect('globals:calendar')


'''------------------------------------------- SPECIAL WORK PERIOD VIEWS --------------------------------------------------------'''


# Settings | Special Work Period List View
# ---------------------------------------------------------------------------------------------------------------------
class SpecialWorkPeriodListView(LoginRequiredMixin, View):
    login_url = 'accounts:sign-in'
    template_name = 'calendars/staff_special_work_period_list.html'

    def get(self, request, *args, **kwargs):
        staff_special_work_periods = models.StaffSpecialWorkPeriod.objects.all()
        special_work_periods = models.SpecialWorkPeriod.objects.all()

        context = {
            'staff_special_work_periods': staff_special_work_periods,
            'special_work_periods': special_work_periods,
        }
        return render(request, self.template_name, context)


# Calendar | Special Work Period Load Form View
# ---------------------------------------------------------------------------------------------------------------------
def load_special_work_period_form(request):  # AJAX CALL
    obj = None
    object_id = None
    start_date = None
    end_date = None

    if services.is_ajax(request=request):
        object_id = request.POST.get('object_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

    print('object_id * ', object_id, '*', type(object_id))
    
    # CREATE
    form = forms.SpecialWorkPeriodModelForm(initial={
        'start_date': start_date,
        'end_date': end_date
    })

    # UPDATE
    if object_id and object_id != 'None':
        obj = models.SpecialWorkPeriod.objects.get(id=object_id)
        form = forms.SpecialWorkPeriodModelForm(instance=obj)

    return render(
        request,
        "calendars/special_work_period.html",
        {
            "form": form,
            "object": obj,
        }
    )


# Calendar | Special Work Period Save View
# ---------------------------------------------------------------------------------------------------------------------
class SpecialWorkPeriodSaveView(View):
    template_name = 'calendars/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        if obj := services.get_object(self, models.SpecialWorkPeriod):
            form = forms.SpecialWorkPeriodModelForm(request.POST, instance=obj)
        else:
            form = forms.SpecialWorkPeriodModelForm(request.POST)
        
        if form.is_valid():
            form.save()

        return redirect('globals:calendar')


# Calendar | Special Work Period Delete View
# ---------------------------------------------------------------------------------------------------------------------
class SpecialWorkPeriodDeleteView(View):
    template_name = 'calendars/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        obj = services.get_object(self, models.SpecialWorkPeriod)
        if obj is not None:
            obj.delete()
        
        return redirect('globals:calendar')



'''------------------------------------------- STAFF SPECIAL WORK PERIOD VIEWS --------------------------------------------------------'''


# Calendar | Special Work Period Load Form View
# ---------------------------------------------------------------------------------------------------------------------
def load_staff_special_work_period_form(request):  # AJAX CALL
    obj = None
    object_id = request.POST.get('object_id') if services.is_ajax(request=request) else None
    print('object_id * ', object_id, '*', type(object_id))

    # CREATE
    form = forms.StaffSpecialWorkPeriodModelForm()

    # UPDATE
    if object_id and object_id != 'None':
        obj = models.StaffSpecialWorkPeriod.objects.get(id=object_id)
        form = forms.StaffSpecialWorkPeriodModelForm(instance=obj)

    return render(
        request,
        "calendars/staff_special_work_period.html",
        {
            "form": form,
            "object": obj,
        }
    )


# Calendar | Staff Special Work Period Save View
# ---------------------------------------------------------------------------------------------------------------------
class StaffSpecialWorkPeriodSaveView(View):
    template_name = 'calendars/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        if obj := services.get_object(self, models.StaffSpecialWorkPeriod):
            form = forms.StaffSpecialWorkPeriodModelForm(request.POST, instance=obj)
        else:
            form = forms.StaffSpecialWorkPeriodModelForm(request.POST)
        
        if form.is_valid():
            # Check for doublons
            staff_business_hour = form.cleaned_data.get('staff_business_hour')
            special_work_period = form.cleaned_data.get('special_work_period')
            if models.StaffSpecialWorkPeriod.objects.filter(staff_business_hour=staff_business_hour, special_work_period=special_work_period).exists():
                messages.info(request, "Vous ne pouvez avoir qu'une seule période spéciale par heure de travail de groupe.")
                return redirect('globals:calendar')

            form.save()

        return redirect('globals:calendar')


# Calendar | Staff Special Work Period Delete View
# ---------------------------------------------------------------------------------------------------------------------
class StaffSpecialWorkPeriodDeleteView(View):
    template_name = 'calendars/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        obj = services.get_object(self, models.StaffSpecialWorkPeriod)
        if obj is not None:
            obj.delete()
        
        return redirect('globals:calendar')
