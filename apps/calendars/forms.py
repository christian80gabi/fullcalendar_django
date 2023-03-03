from django import forms
from .models import Event


class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('reference', 'created_date', 'updated_date', 'repeat_parent')
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
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'value': '#ff0000',
                'type': 'color'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'max-rows': '6',
            }),
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
