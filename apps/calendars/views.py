from django.shortcuts import render, redirect
from django.views import View
from .models import Event
from .forms import EventModelForm
from .services import get_object, is_ajax


class CalendarView(View):
    template = "calendar.html"
    context = {}

    def get(self, request, *args, **kwargs):
        object_list = Event.objects.all()

        self.context = {'object_list': object_list, 'form': self.form}

        return render(request, self.template, self.context)


'''------------------------------------------- EVENT VIEWS --------------------------------------------------------'''


# Calendar | Event Load Form View
# ---------------------------------------------------------------------------------------------------------------------
def load_event_form(request):  # AJAX CALL
    object_id = request.POST.get('object_id') if is_ajax(request=request) else None
    print('object_id', object_id, type(object_id))

    obj = None
    # CREATE
    form = EventModelForm()

    # UPDATE
    if object_id and object_id != 'None':
        obj = Event.objects.get(id=object_id)
        form = EventModelForm(instance=obj)

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
        if obj := get_object(self, Event):
            form = EventModelForm(request.POST, instance=obj)
        else:
            form = EventModelForm(request.POST)

        # if UPDATE
        # - update all the series or just the current event?

        if form.is_valid():
            obj = form.save()
            obj.repeat_it()

            return redirect('calendars:calendar')

        return render(request, self.template_name, self.context)


# Recruitment | Event Delete View
# ---------------------------------------------------------------------------------------------------------------------
class EventDeleteView(View):
    template_name = 'calendars/calendar.html'
    context = {}

    def post(self, request, *args, **kwargs):
        obj = get_object(self, Event)
        if obj is not None:
            obj.delete()
            return redirect('core:calendar')
        return render(request, self.template, self.context)
