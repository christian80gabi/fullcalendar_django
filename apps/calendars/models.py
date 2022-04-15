from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models


# using random.choices() - generating random strings
# ---------------------------------------------------------------------------------------------------------------------
def generate_secret_key(number_of_chars):
    import secrets
    import string

    text = ''.join(
        secrets.choice(string.ascii_uppercase + string.digits)
        for _ in range(number_of_chars))
    return str(text)


class Event(models.Model):

    class Type(models.TextChoices):
        NONE = None, _('...')
        PHONE_CALL = 'PHONE CALL', _('Make a phone call')
        MEETING = 'MEETING', _('Schedule a meeting')
        EMAIL = 'EMAIL', _('Send an email')
        MAKE_OFFER = 'OFFER', _('Make an offer')

    class Status(models.TextChoices):
        NONE = None, _('...')
        SCHEDULED = 'SCHEDULED', _('Scheduled')
        CANCELLED = 'CANCELLED', _('Cancelled')
        DONE = 'DONE', _('Done')

    reference = models.CharField(max_length=50, unique=True, blank=True)
    type = models.CharField(
        max_length=50,
        choices=Type.choices,
        default=Type.NONE,
        db_index=True,
    )
    name = models.CharField(max_length=255)
    scheduled_datetime = models.DateTimeField(default=timezone.now)
    effective_datetime = models.DateTimeField()
    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.NONE,
        db_index=True,
    )
    comment = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = generate_secret_key(50)

        super(Event, self).save(*args, **kwargs)

    @property
    def type_label(self):
        return self.get_type_display()

    @property
    def status_label(self):
        return self.get_status_display()

    def __str__(self):
        return self.name
