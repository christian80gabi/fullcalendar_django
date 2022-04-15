from django import forms
from .models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = [
            'type', 'name', 'scheduled_datetime', 'effective_datetime',
            'status', 'comment'
        ]
        widgets = {
            'type':
            forms.Select(attrs={
                'class': 'form-select',
            }),
            'name':
            forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'scheduled_datetime':
            forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'effective_datetime':
            forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'status':
            forms.Select(attrs={
                'class': 'form-select',
            }),
            'comment':
            forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'max-rows': '6',
            }),
        }