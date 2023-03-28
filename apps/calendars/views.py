from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .forms import (
    BusinessHourModelForm, EventModelForm, BusinessHourBreakModelForm, DayBreakHourModelForm, StaffBusinessHourModelForm
)
from .models import (
    BusinessHour, Event, BusinessHourBreak, DayBreakHour, StaffBusinessHour
)
from .services import get_object, is_ajax


class CalendarView(View):
    template = "calendar.html"
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


        business_hours = BusinessHour.objects.all() 
        events = Event.objects.all()

        global_business_hour = StaffBusinessHour.objects.filter(is_main=True).first()

        self.context = {
            'business_hours': business_hours,
            'global_business_hour': global_business_hour,
            'events': events,
            'greeting': self.greeting,
        }

        return render(request, self.template, self.context)


'''------------------------------------------- EVENT VIEWS --------------------------------------------------------'''


# Calendar | Event Load Form View
# ---------------------------------------------------------------------------------------------------------------------
def load_event_form(request):  # AJAX CALL
    object_id = None
    start_date = None
    end_date = None
    start_time = None
    end_time = None

    if is_ajax(request=request):
        object_id = request.POST.get('object_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

    print('object_id * ', object_id, '*', type(object_id))

    obj = None
    # CREATE
    form = EventModelForm(initial={
        'start_date': start_date,
        'end_date': end_date,
        'start_time': start_time,
        'end_time': end_time
    })

    # UPDATE
    if object_id is not None and object_id != '':
        obj = Event.objects.get(reference=object_id)
        form = EventModelForm(instance=obj)

    return render(
        request,
        "calendar/event_form.html",
        {
            "form": form,
            "object": obj,
        }
    )


# Calendar | Event Save View
# ---------------------------------------------------------------------------------------------------------------------
class EventSaveView(View):
    template_name = 'calendar/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        obj = get_object(self, Event)
        message = 'Enregistrement reussi!'

        if obj:
            was_repeated = bool(obj.is_repeated)
            form = EventModelForm(request.POST, instance=obj)

            try:
                parent_event = obj
                if obj.repeat_parent:
                    print('looking for parent event!')
                    parent_event = Event.objects.filter(reference=obj.repeat_parent).first()

                print('parent ref', parent_event.reference)
            except Exception as e:
                print('ERROR', e)
                messages.info(request, "Error when looking for parent event")
                parent_event = None
        else:
            form = EventModelForm(request.POST)

        # if UPDATE
        # - update all the series or just the current event?

        if form.is_valid():
            if not obj:
                obj_saved = form.save()
                obj_saved.repeat_it()
            elif all_the_series := request.POST.get('allTheSeries'):

                if parent_event:
                    message = self.update_event_series(parent_event, form)

            else:
                # Update only the current one without repetition
                print('only the current one')
                obj_saved = form.save()

                copies = Event.objects.filter(repeat_parent=obj.reference)
                if not was_repeated and not obj.repeat_parent and not copies:
                    message = obj_saved.repeat_it()

            print(message)
            messages.info(request, message)
        
        return redirect('globals:calendar')


    def update_event_series(self, parent_event, form):
        print('All series')
        # Delete all previously saved without the original one
        Event.objects.filter(repeat_parent=parent_event.reference).delete()
    
        # Then update the original one
        saved_obj = Event.objects.filter(reference=parent_event.reference).update(
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
        obj = Event.objects.get(reference=parent_event.reference)
        return obj.repeat_it()


# Recruitment | Event Delete View
# ---------------------------------------------------------------------------------------------------------------------
class EventDeleteView(View):
    template_name = 'calendar/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        if obj := get_object(self, Event):
            all_the_series = request.POST.get('allTheSeries')

            if not all_the_series:
                # Delete only the current event
                obj.delete()

            else:
                try:
                    parent_event = obj
                    if obj.repeat_parent:
                        print('looking for parent event!')
                        parent_event = Event.objects.filter(reference=obj.repeat_parent).first()

                except Exception as e:
                    parent_event = None
                    print(e)
                    messages.info(request, "Erreur de mise à jour de toute la série.")

                if parent_event:
                    # Delete the original event and its copies
                    Event.objects.filter(repeat_parent=parent_event.reference).delete()
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

    if is_ajax(request=request):
        object_id = request.POST.get('object_id')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

    print('object_id * ', object_id, '*', type(object_id))
    
    # CREATE
    form = BusinessHourModelForm(initial={
        'start_time': start_time,
        'end_time': end_time
    })

    # UPDATE
    if object_id and object_id != 'None':
        obj = BusinessHour.objects.get(id=object_id)
        form = BusinessHourModelForm(instance=obj)

    return render(
        request,
        "calendar/business_hour_form.html",
        {
            "form": form,
            "object": obj,
        }
    )


# Calendar | Business Hour Save View
# ---------------------------------------------------------------------------------------------------------------------
class BusinessHourSaveView(View):
    template_name = 'calendar/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        if obj := get_object(self, BusinessHour):
            form = BusinessHourModelForm(request.POST, instance=obj)
        else:
            form = BusinessHourModelForm(request.POST)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.days_of_week = form.cleaned_data['day_list']
            obj.save()
            messages.info(request, 'Enregistrement reussi!')

        return redirect('globals:calendar')


# Calendar | Business Hour Delete View
# ---------------------------------------------------------------------------------------------------------------------
class BusinessHourDeleteView(View):
    template_name = 'calendar/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        obj = get_object(self, BusinessHour)
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

    if is_ajax(request=request):
        object_id = request.POST.get('object_id')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        business_hour_id = request.POST.get('business_hour_id')

    print('object_id * ', object_id, '*', type(object_id))
    
    # CREATE
    form = DayBreakHourModelForm(initial={
        'start_time': start_time,
        'end_time': end_time
    })

    # UPDATE
    if object_id and object_id != 'None':
        obj = DayBreakHour.objects.get(id=object_id)
        form = DayBreakHourModelForm(instance=obj)

    return render(
        request,
        "calendar/business_hour_break_form.html",
        {
            "form": form,
            "object": obj,
            "business_hour_id": business_hour_id,
        }
    )


# Calendar | Business Hour Save View
# ---------------------------------------------------------------------------------------------------------------------
class BusinessHourBreakSaveView(View):
    template_name = 'calendar/calendar.html'
    context = {}

    def post(self, request, business_hour_id, *args, **kwargs):
        if obj := get_object(self, DayBreakHour):
            form = DayBreakHourModelForm(request.POST, instance=obj)
        else:
            form = DayBreakHourModelForm(request.POST)
        
        if form.is_valid():
            saved_obj = form.save()

            print('DayBreakHour * ', saved_obj)

            if business_hour_id and not obj:
                
                BusinessHourBreak(
                    business_hour = BusinessHour.objects.get(id=business_hour_id),
                    day_break_hour = saved_obj,
                ).save()

            messages.info(request, 'Enregistrement reussi!')

        return redirect('globals:calendar')


# Calendar | Business Hour Delete View
# ---------------------------------------------------------------------------------------------------------------------
class BusinessHourBreakDeleteView(View):
    template_name = 'calendar/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        obj = get_object(self, DayBreakHour)
        if obj is not None:
            obj.delete()

        return redirect('globals:calendar')


'''------------------------------------------- STAFF BUSINESS HOUR VIEWS --------------------------------------------------------'''


# Calendar | Business Hour Load Form View
# ---------------------------------------------------------------------------------------------------------------------
def load_staff_business_hour_form(request):  # AJAX CALL
    obj = None
    object_id = None

    if is_ajax(request=request):
        object_id = request.POST.get('object_id')

    print('object_id * ', object_id, '*', type(object_id))
    
    # CREATE
    form = StaffBusinessHourModelForm()

    # UPDATE
    if object_id and object_id != 'None':
        obj = StaffBusinessHour.objects.get(id=object_id)
        form = StaffBusinessHourModelForm(instance=obj)

    return render(
        request,
        "calendar/staff_business_hour_form.html",
        {
            "form": form,
            "object": obj,
        }
    )


# Calendar | Staff Business Hour Save View
# ---------------------------------------------------------------------------------------------------------------------
class StaffBusinessHourSaveView(View):
    template_name = 'calendar/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        if obj := get_object(self, StaffBusinessHour):
            form = StaffBusinessHourModelForm(request.POST, instance=obj)
        else:
            form = StaffBusinessHourModelForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.info(request, 'Enregistrement reussi!')

        return redirect('globals:calendar')


# Calendar | Staff Business Hour Delete View
# ---------------------------------------------------------------------------------------------------------------------
class StaffBusinessHourDeleteView(View):
    template_name = 'calendar/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        obj = get_object(self, StaffBusinessHour)
        if obj is not None:
            obj.delete()
        
        return redirect('globals:calendar')


'''------------------------------------------- SPECIAL WORK PERIOD VIEWS --------------------------------------------------------'''


# Calendar | Special Work Period Load Form View
# ---------------------------------------------------------------------------------------------------------------------
def load_special_work_period_form(request):  # AJAX CALL
    obj = None
    object_id = None
    start_date = None
    end_date = None

    if is_ajax(request=request):
        object_id = request.POST.get('object_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

    print('object_id * ', object_id, '*', type(object_id))
    
    # CREATE
    form = SpecialWorkPeriodModelForm(initial={
        'start_date': start_date,
        'end_date': end_date
    })

    # UPDATE
    if object_id and object_id != 'None':
        obj = SpecialWorkPeriod.objects.get(id=object_id)
        form = SpecialWorkPeriodModelForm(instance=obj)

    return render(
        request,
        "calendar/special_work_period.html",
        {
            "form": form,
            "object": obj,
        }
    )


# Calendar | Special Work Period Save View
# ---------------------------------------------------------------------------------------------------------------------
class SpecialWorkPeriodSaveView(View):
    template_name = 'calendar/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        if obj := get_object(self, SpecialWorkPeriod):
            form = SpecialWorkPeriodModelForm(request.POST, instance=obj)
        else:
            form = SpecialWorkPeriodModelForm(request.POST)
        
        if form.is_valid():
            form.save()

        return redirect('globals:calendar')


# Calendar | Special Work Period Delete View
# ---------------------------------------------------------------------------------------------------------------------
class SpecialWorkPeriodDeleteView(View):
    template_name = 'calendar/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        obj = get_object(self, SpecialWorkPeriod)
        if obj is not None:
            obj.delete()
        
        return redirect('globals:calendar')



'''------------------------------------------- STAFF SPECIAL WORK PERIOD VIEWS --------------------------------------------------------'''


# Calendar | Special Work Period Load Form View
# ---------------------------------------------------------------------------------------------------------------------
def load_staff_special_work_period_form(request):  # AJAX CALL
    obj = None
    object_id = None

    if is_ajax(request=request):
        object_id = request.POST.get('object_id')

    print('object_id * ', object_id, '*', type(object_id))
    
    # CREATE
    form = StaffSpecialWorkPeriodModelForm()

    # UPDATE
    if object_id and object_id != 'None':
        obj = StaffSpecialWorkPeriod.objects.get(id=object_id)
        form = StaffSpecialWorkPeriodModelForm(instance=obj)

    return render(
        request,
        "calendar/staff_special_work_period.html",
        {
            "form": form,
            "object": obj,
        }
    )


# Calendar | Staff Special Work Period Save View
# ---------------------------------------------------------------------------------------------------------------------
class StaffSpecialWorkPeriodSaveView(View):
    template_name = 'calendar/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        if obj := get_object(self, StaffSpecialWorkPeriod):
            form = StaffSpecialWorkPeriodModelForm(request.POST, instance=obj)
        else:
            form = StaffSpecialWorkPeriodModelForm(request.POST)
        
        if form.is_valid():
            form.save()

        return redirect('globals:calendar')


# Calendar | Staff Special Work Period Delete View
# ---------------------------------------------------------------------------------------------------------------------
class StaffSpecialWorkPeriodDeleteView(View):
    template_name = 'calendar/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        obj = get_object(self, StaffSpecialWorkPeriod)
        if obj is not None:
            obj.delete()
        
        return redirect('globals:calendar')

