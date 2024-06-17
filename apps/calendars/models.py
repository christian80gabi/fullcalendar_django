import datetime
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.db import models


class PERIOD:
    DAY = 'DAY'
    HOUR = 'HOUR'

    UNITS = [
        (DAY, 'Jour'),
        (HOUR, 'Heure'),
    ]


class RepeatUnit(models.TextChoices):
    DAY = 'DAY', _('Jour')
    WEEK = 'WEEK', _('Semaine')
    MONTH = 'MONTH', _('Mois')
    YEAR = 'YEAR', _('Année')


class DaysOfWeek(models.IntegerChoices):
        MONDAY = 1, _('Lundi')
        TUESDAY = 2, _('Mardi')
        WEDNESDAY = 3, _('Mercredi')
        THURSDAY = 4, _('Jeudi')
        FRIDAY = 5, _('Vendredi')
        SATURDAY = 6, _('Samedi')
        SUNDAY = 7, _('Dimanche')


class AbstractModelBase(models.Model):
    reference = models.CharField(max_length=100, blank=True, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = get_random_string(50)

        super(AbstractModelBase, self).save(*args, **kwargs)


class BusinessHour(AbstractModelBase):
    name = models.CharField(max_length=100)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    days_of_week = models.CharField(max_length=100, blank=True, default='1, 2, 3, 4, 5')  # Should be stored like this '[0, 1, 2, 3, 4, 5, 6]'

    # return list(map(int, self.days_of_week))  # Only works when days_of_week look like "1, 2, 3, 4"
    @property
    def workweek(self):
        if not self.days_of_week:
            return []
        tab_string = self.days_of_week

        if '[' in tab_string:
            tab_string = tab_string.strip("[]")

        if ',' in tab_string:
            tab_string = tab_string.split(", ")

        if "'" in tab_string:
            tab_string = tab_string.strip("'")

        return [int(i.strip("'") if "'" in i else i) for i in tab_string]
    
    @property
    def workweek_verbose(self):   
        # return [value for  i, (key, value) in enumerate(DaysOfWeek.choices) if key in self.workweek]     
        return [value for key, value in DaysOfWeek.choices if key in self.workweek]

    @property
    def duration_in_hours(self):
        start_time = datetime.datetime.combine(datetime.date.today(), self.start_time)
        end_time = datetime.datetime.combine(datetime.date.today(), self.end_time)
        
        diff = end_time - start_time
        return diff.total_seconds() / 3600
    
    @property
    def day_duration_in_hours(self):
        duration_in_hours = self.duration_in_hours

        for break_time in self.break_times:
            duration_in_hours - break_time.duration_in_hours

        return duration_in_hours
    
    @property
    def break_times(self):
        return DayBreakHour.objects.filter(businesshourbreak__business_hour=self)

    def __str__(self) -> str:
        return f'{self.name} days: {self.workweek.__str__()} from: {self.start_time.__str__()} to: {self.end_time.__str__()}'
    

class DayBreakHour(AbstractModelBase):
    name = models.CharField(max_length=100)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)

    @property
    def duration_in_hours(self):
        start_time = datetime.datetime.combine(datetime.date.today(), self.start_time)
        end_time = datetime.datetime.combine(datetime.date.today(), self.end_time)
        
        diff = end_time - start_time
        return diff.total_seconds() / 3600

    def __str__(self) -> str:
        return f"{self.name}"


class BusinessHourBreak(AbstractModelBase):
    business_hour = models.ForeignKey(BusinessHour, on_delete=models.CASCADE)
    day_break_hour = models.ForeignKey(DayBreakHour, on_delete=models.CASCADE)

    class Meta:
        ordering = ['business_hour', 'day_break_hour']
        unique_together = [
            ['business_hour', 'day_break_hour']
        ]

    def __str__(self) -> str:
        return f'{self.business_hour.__str__()} days: {self.day_break_hour.__str__()}'


class StaffBusinessHour(AbstractModelBase):
    name = models.CharField(max_length=200)
    business_hour = models.ManyToManyField(BusinessHour)
    is_main = models.BooleanField(default=False)

    @property
    def business_hours(self):
        return BusinessHour.objects.filter(staffbusinesshour=self)

    def __str__(self) -> str:
        return f'{self.name} {self.is_main}'
    

class SpecialWorkPeriod(AbstractModelBase):
    name = models.CharField(max_length=100)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    business_hour = models.ManyToManyField(BusinessHour)
    description = models.TextField(null=True, blank=True)

    @property
    def business_hours(self):
        return BusinessHour.objects.filter(specialworkperiod=self)

    def __str__(self) -> str:
        return f'{self.name} from: {self.start_date.__str__()} to: {self.end_date.__str__()}'


class StaffSpecialWorkPeriod(AbstractModelBase):
    staff_business_hour = models.ForeignKey(StaffBusinessHour, on_delete=models.CASCADE)
    special_work_period = models.ForeignKey(SpecialWorkPeriod, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['staff_business_hour', 'special_work_period']

    def __str__(self) -> str:
        return f"{self.special_work_period.__str__()} {self.staff_business_hour.__str__()}"


class Event(AbstractModelBase):

    class EventType(models.TextChoices):
        EVENT = 'EVENT', 'EVENT'
        HOLIDAY = 'HOLIDAY', 'HOLIDAY'

    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=10, null=True, blank=True)
    type = models.CharField(max_length=10, choices=EventType.choices, default=EventType.EVENT, blank=True)
    # Repeat an event
    is_repeated = models.BooleanField(default=False)
    # Recurrence : 
    # every [recurrence] [repeat_by] until [occurrence] or [repeat_end_date]
    # eg: every 2 DAYS until 12 occurrences ; every 1 MONTHS until 25-12-2036 
    recurrence = models.PositiveIntegerField(default=1, null=True, blank=True)
    repeat_by = models.CharField(max_length=5, choices=RepeatUnit.choices, default=RepeatUnit.YEAR, null=True, blank=True)
    # END -----------------------------------------------------------------------------
    repeat_end_date = models.DateField(null=True, blank=True) # If None then never ends
    # OR
    occurrence = models.PositiveIntegerField(null=True, blank=True)  # 1, 2... Jours, mois...  / step
    # OR NEVER ENDS
    # If repeated, store the reference of the first event to link with
    # It will help to know the first occurrence and the copies or an occurrence series of an event
    repeat_parent = models.CharField(max_length=100, null=True, blank=True)

    @property
    def color_value(self):
        if self.color:
            return self.color

        return '#ff0000' if self.type == self.EventType.HOLIDAY else '#0066ff'
    
    @property
    def is_working_holiday(self):
        return (self.type == self.EventType.HOLIDAY and self.paid_leave)

    @property
    def actual_end_date(self):
        return self.end_date or self.start_date

    @property
    def actual_start_time(self):
        return self.start_time or datetime.time.min
    
    @property
    def actual_end_time(self):
        return self.end_time or datetime.time.max

    # If the event take all the day or partially
    @property
    def allDay(self):
        return (
            self.start_date == self.actual_end_date
        ) and (
            self.actual_start_time == datetime.time.min or not self.start_time
        ) and (
            self.actual_end_time == datetime.time.max or not self.end_time
        )
    
    # Return the start date and the end date of a event depending if it's variable or not
    @property
    def datetimes(self):
        return datetime.datetime.combine(self.start_date, self.actual_start_time), datetime.datetime.combine(self.actual_end_date, self.actual_end_time)

    def repeat_it(self) -> str:
        from .services import (repeat_it_by_day, repeat_it_by_week, repeat_it_by_month, repeat_it_by_year)

        if self.is_repeated and self.recurrence and self.recurrence >= 1 and self.repeat_by:
            if self.repeat_by == RepeatUnit.DAY:

                print('REPEAT BY DAY')
                
                return repeat_it_by_day(self=self)

            elif self.repeat_by == RepeatUnit.WEEK:

                print('REPEAT BY WEEK')
                
                return repeat_it_by_week(self=self)

            elif self.repeat_by == RepeatUnit.MONTH:

                print('REPEAT BY MONTH')
                
                return repeat_it_by_month(self)

            elif self.repeat_by == RepeatUnit.YEAR:

                print('REPEAT BY YEAR')

                return repeat_it_by_year(self)
        
        print('NEVER REPEAT IT.')
        return 'Never repeated!'
    
    def __str__(self) -> str:
        return f'{self.name} : [ {self.datetimes[0].date()} - {self.datetimes[1].date()} ]'