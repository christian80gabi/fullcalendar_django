# Django App (integrating FullCalendar)

## Tools & Technologies

- **[Django](https://www.djangoproject.com)**: High-level Python web framework that encourages rapid development and clean, pragmatic design.
- **[FullCalendar](https://fullcalendar.io)**: Full-sized drag & drop calendar in JavaScript

## Requirements

This has been build with:

- **Python** (_v3.9.x_)
- **Django** (_v4.2.x_)
- **FullCalendar** (_v6.1.x_)

## Installation

On a terminal:

```bash
# From project root directory

# Activate python
$ python3 -m venv .venv
$ source .venv/vin/activate

# install requirements
$ python install -r requirements.txt

# Run migrations
$ python manage.py makemigrations
$ python manage.py migrate

# Create super user
$ python manage.py createsuperuser

# Run server | start the project
$ python manage.py runserver 
```
