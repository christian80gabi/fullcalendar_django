from django import forms
from .models import (
    StaffBusinessHour, BusinessHour, Event, DaysOfWeek, DayBreakHour, BusinessHourBreak
)


'''-------------------------------------------- CALENDAR FORMS --------------------------------------------------------'''


class BusinessHourModelForm(forms.ModelForm):
    day_list = forms.MultipleChoiceField(
        label="Days", 
        required=True,
        help_text="Select the day you want for that work hours.", 
        choices=DaysOfWeek.choices, 
        widget=forms.CheckboxSelectMultiple()
    )
    
    class Meta:
        model = BusinessHour
        fields = [
            'name',
            'start_time',
            'end_time',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            })
        }


class DayBreakHourModelForm(forms.ModelForm):
    class Meta:
        model = DayBreakHour
        fields = [
            'name',
            'start_time',
            'end_time',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            })
        }
    

class BusinessHourBreakModelForm(forms.ModelForm):
    class Meta:
        model = BusinessHourBreak
        fields = [
            'business_hour',
            'day_break_hour',
        ]
        widgets = {
            'business_hour': forms.Select(attrs={
                'class': 'form-select'
            }),
            'day_break_hour': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class StaffBusinessHourModelForm(forms.ModelForm):
    class Meta:
        model = StaffBusinessHour
        fields = [
            'name',
            'business_hour',
            'is_main',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'business_hour': forms.SelectMultiple(attrs={
                'class': 'form-select',
            }),
            'is_main': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class EventModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].required = True
        self.fields['type'].choices = Event.EventType.choices

    class Meta:
        model = Event
        fields = (
            'name',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'location',
            'description',
            'color',
            'type',
            'is_repeated',
            'recurrence',
            'repeat_by',
            'repeat_end_date',
            'occurrence'
        )
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
            }),
            'type': forms.RadioSelect(),
            'is_repeated': forms.CheckboxInput(attrs={
                'class': 'form-check form-check-input'
            }),
            'repeat_by': forms.Select(attrs={
                'class': 'form-select'
            }),
            'recurrence': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'repeat_end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'occurrence': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }
