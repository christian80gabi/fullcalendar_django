import datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import get_object_or_404


def get_object(area, model_class):
    _id = area.kwargs.get('id')
    return get_object_or_404(model_class, id=_id) if _id is not None else None

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

# using random.choices() - generating random strings
# ---------------------------------------------------------------------------------------------------------------------
def generate_secret_key(number_of_chars):
    import secrets
    import string

    return ''.join(
        secrets.choice(string.ascii_uppercase + string.digits) for _ in range(number_of_chars)
    )

def is_next_day(date1, date2, step):
    next_day = date1 + datetime.timedelta(days=step)
    return next_day <= date2

def is_next_week(date1, date2, step):
    # next_week = date1 + datetime.timedelta(days=7)

    next_week = date1 + relativedelta(weeks=step)
    return next_week <= date2

def is_next_month(date1, date2, step):
    # next_month = date1.replace(day=1) + datetime.timedelta(days=32)
    # next_month = next_month.replace(day=1)
    # return next_month <= date2.replace(day=1)

    next_month = date1 + relativedelta(months=step)
    return next_month <= date2

def is_next_year(date1, date2, step):
    # next_year = date1.replace(month=1, day=1) + datetime.timedelta(days=366)
    # next_year = next_year.replace(month=1, day=1)
    # return next_year <= date2.replace(month=1, day=1)

    next_year = date1 + relativedelta(years=step)
    return next_year <= date2


def repeat_it_by_day(self):

    if self.occurrence and self.occurrence >= 1:
        if self.occurrence < 2:
            return f'Repeat it every {self.recurrence.__str__()} {self.repeat_by.__str__()}, {self.occurrence.__str__()} times.'

        for i in range(1, self.occurrence):
            new_event = self.__class__(
                name=self.name,
                start_date=self.start_date + datetime.timedelta(days=self.recurrence * i),
                end_date=self.actual_end_date + datetime.timedelta(days=self.recurrence * i),
                start_time=self.start_time,
                end_time=self.end_time,
                location=self.location,
                description=self.description,
                is_repeated=False,
                repeat_parent=self.reference
            )
            new_event.save()

        return f'Repeat it every {self.recurrence.__str__()} {self.repeat_by.__str__()}, {self.occurrence.__str__()} times.'

    elif self.repeat_end_date and is_next_day(self.start_date, self.repeat_end_date, self.recurrence):

        curr_date = self.start_date
        while is_next_day(curr_date, self.repeat_end_date, self.recurrence):
            curr_date += datetime.timedelta(days=self.recurrence)
            new_event = self.__class__(
                name=self.name,
                start_date=curr_date,
                end_date=self.actual_end_date + (curr_date - self.start_date),
                start_time=self.start_time,
                end_time=self.end_time,
                location=self.location,
                description=self.description,
                is_repeated=False,
                repeat_parent=self.reference,
            )
            new_event.save()

        return f'Repeat it every {self.recurrence.__str__()} {self.repeat_by.__str__()}, until {self.repeat_end_date.__str__()}.'

    elif not self.repeat_end_date and not self.occurrence:

        return f'Repeat it indefinitely, every {self.recurrence.__str__()} {self.repeat_by.__str__()}.'

    else:

        return f'Repeat it every {self.recurrence.__str__()} {self.repeat_by.__str__()}. Meanwhile no conventional END.'
    

def repeat_it_by_week(self):

    if self.occurrence and self.occurrence >= 1:
        if self.occurrence < 2:
            return f'Repeat it every {self.recurrence.__str__()} {self.repeat_by.__str__()}, {self.occurrence.__str__()} times.'
        
        for i in range(1, self.occurrence):
            new_event = self.__class__(
                name=self.name,
                start_date=self.start_date + datetime.timedelta(weeks=self.recurrence * i),
                end_date=self.actual_end_date + datetime.timedelta(weeks=self.recurrence * i),
                start_time=self.start_time,
                end_time=self.end_time,
                location=self.location,
                description=self.description,
                is_repeated=False,
                repeat_parent=self.reference,
            )
            new_event.save()
        
        return f'Repeat it every {self.recurrence.__str__()} {self.repeat_by.__str__()}, {self.occurrence.__str__()} times.'

    elif self.repeat_end_date and is_next_week(self.start_date, self.repeat_end_date, self.recurrence):
        
        curr_date = self.start_date
        while is_next_week(curr_date, self.repeat_end_date, self.recurrence):
            curr_date += datetime.timedelta(weeks=self.recurrence)
            new_event = self.__class__(
                name=self.name,
                start_date=curr_date,
                end_date=self.actual_end_date + (curr_date - self.start_date),
                start_time=self.start_time,
                end_time=self.end_time,
                location=self.location,
                description=self.description,
                is_repeated=False,
                repeat_parent=self.reference,
            )
            new_event.save()

        return f'Repeat it every {self.recurrence.__str__()} {self.repeat_by.__str__()}, until {self.repeat_end_date.__str__()}.'
    
    elif not self.repeat_end_date and not self.occurrence:
        
        return f'Repeat it indefinitely, every {self.recurrence.__str__()} {self.repeat_by.__str__()}.'

    else:

        return f'Repeat it every {self.recurrence.__str__()} {self.repeat_by.__str__()}. Meanwhile no conventional END.'
       


def repeat_it_by_month(self):

    if self.occurrence and self.occurrence >= 1:
        if self.occurrence < 2:
            return f'Repeat it every {self.recurrence.__str__()} {self.repeat_by.__str__()}, {self.occurrence.__str__()} times.'

        for i in range(1, self.occurrence):
            new_start_date = self.start_date + relativedelta(months=self.recurrence * i)
            new_end_date = self.actual_end_date + relativedelta(months=self.recurrence * i)
            if new_start_date.day != self.start_date.day:
                new_start_date = new_start_date.replace(day=self.start_date.day)
                new_end_date = new_end_date.replace(day=self.actual_end_date.day)
            new_event = self.__class__(
                name=self.name,
                start_date=new_start_date,
                end_date=new_end_date,
                start_time=self.start_time,
                end_time=self.end_time,
                location=self.location,
                description=self.description,
                is_repeated=False,
                repeat_parent=self,
            )
            new_event.save()
        
        return f'Repeat it every {self.recurrence.__str__()} {self.repeat_by.__str__()}, {self.occurrence.__str__()} times.'

    elif self.repeat_end_date and is_next_month(self.start_date, self.repeat_end_date, self.recurrence):
        
        curr_date = self.start_date
        while is_next_month(curr_date, self.repeat_end_date, self.recurrence):
            curr_date += relativedelta(months=self.recurrence) 
            new_event = self.__class__(
                name=self.name,
                start_date=curr_date,
                end_date=self.actual_end_date + (curr_date - self.start_date),
                start_time=self.start_time,
                end_time=self.end_time,
                location=self.location,
                description=self.description,
                is_repeated=False,
                repeat_parent=self.reference,
            )
            new_event.save()
        
        return f'Repeat it every {self.recurrence.__str__()} {self.repeat_by.__str__()}, until {self.repeat_end_date.__str__()}.'

    elif not self.repeat_end_date and not self.occurrence:
        
        return f'Repeat it indefinitely, every {self.recurrence.__str__()} {self.repeat_by.__str__()}.'

    else:

        return f'Repeat it every {self.recurrence.__str__()} {self.repeat_by.__str__()}. Meanwhile no conventional END.'


def repeat_it_by_year(self):

    if self.occurrence and self.occurrence >= 1:
        if self.occurrence < 2:
            return f'Repeat it every {self.recurrence.__str__()} {self.repeat_by.__str__()}, {self.occurrence.__str__()} times.'
        
        for i in range(1, self.occurrence):
            new_event = self.__class__(
                name=self.name,
                start_date=self.start_date + relativedelta(years=self.recurrence * i),
                end_date=self.actual_end_date + relativedelta(years=self.recurrence * i),
                start_time=self.start_time,
                end_time=self.end_time,
                location=self.location,
                description=self.description,
                is_repeated=False,
                repeat_parent=self.reference,
            )
            new_event.save()
        
        return f'Repeat it every {self.recurrence.__str__()} {self.repeat_by.__str__()}, {self.occurrence.__str__()} times.'

    elif self.repeat_end_date and is_next_year(self.start_date, self.repeat_end_date, self.recurrence):

        curr_date = self.start_date
        while is_next_year(curr_date, self.repeat_end_date, self.recurrence):
            curr_date += relativedelta(years=self.recurrence)
            new_event = self.__class__(
                name=self.name,
                start_date=curr_date,
                end_date=self.actual_end_date + (curr_date - self.start_date),
                start_time=self.start_time,
                end_time=self.end_time,
                location=self.location,
                description=self.description,
                is_repeated=False,
                repeat_parent=self.reference,
            )
            new_event.save()
        
        return f'Repeat it every {self.recurrence.__str__()} {self.repeat_by.__str__()}, until {self.repeat_end_date.__str__()}.'

    elif not self.repeat_end_date and not self.occurrence:
        
        return f'Repeat it indefinitely, every {self.recurrence.__str__()} {self.repeat_by.__str__()}.'

    else:

        return f'Repeat it every {self.recurrence.__str__()} {self.repeat_by.__str__()}. Meanwhile no conventional END.'
