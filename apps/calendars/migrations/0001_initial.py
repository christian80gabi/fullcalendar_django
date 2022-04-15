# Generated by Django 3.2.9 on 2022-04-11 12:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(blank=True, max_length=50, unique=True)),
                ('type', models.CharField(choices=[('None', '...'), ('PHONE CALL', 'Make a phone call'), ('MEETING', 'Schedule a meeting'), ('EMAIL', 'Send an email'), ('OFFER', 'Make an offer')], db_index=True, default='None', max_length=50)),
                ('name', models.CharField(max_length=255)),
                ('scheduled_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('effective_datetime', models.DateTimeField()),
                ('status', models.CharField(choices=[('None', '...'), ('SCHEDULED', 'Scheduled'), ('CANCELLED', 'Cancelled'), ('DONE', 'Done')], db_index=True, default='None', max_length=50)),
                ('comment', models.TextField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]