import datetime
from django.utils import timezone

from django.test import TestCase

from .models import Event, Schedule
from .forms import EventForm

class EventAndScheduleSaveTest(TestCase):

    def setUp(self):
        self.valid_form_data = {
            "name": "TestEvent",
            "location": "TestLocation",
            "min_price": 0,
            "max_price": 10,
            "description": "A long description"
        }

    def test_create_event(self):
        event = Event.objects.create(name="TestEvent", location="TestLocation", min_price=0, max_price=10,
                                     description="A long description")
        self.assertEqual(event.name, self.valid_form_data["name"])
        self.assertFalse(event.admin_approved)
        event.name = "TestEventChanged"
        event.save()
        self.assertEqual(event.name, "TestEventChanged")

    def test_create_schedule(self):
        event = Event.objects.create(name="TestEvent", location="TestLocation", min_price=0, max_price=10,
                                     description="A long description")
        schedule = Schedule.objects.create(start_time=timezone.now(),
                                           end_time=timezone.now() + timezone.timedelta(hours=2), event=event)
        self.assertEqual(schedule.event.name, self.valid_form_data["name"])
        event.name = "TestEventChanged"
        event.save()
        self.assertEqual(schedule.event.name, "TestEventChanged")


class EventFormTest(TestCase):

    def setUp(self):
        self.valid_form_data = {
            "name": "Henrik's DevBlog: The Movie",
            "location": "thelist.no",
            "min_price": 0,
            "max_price": 10,
            "start_time": timezone.now(),
            "end_time": timezone.now() + timezone.timedelta(hours=3),
            "description": "The rise of Django developer beginner to successfully and established Django Pro at The List"
        }

    def assertErrorCodeInForm(self, field_name, error_code, form):
        """ Custom `assert` test method. Does not follow the snake case convention similar to e.g `assertFalse` is not in snake case
            This is to test the specific error field and not the wording of an error message.
       
            field_name: name of the error field
            error_code: expected error code bounded in the field validation
            form: the form which the field error appears in
        """

        error_data = form.errors.as_data()
        error_list = error_data.get(field_name)
        self.assertIsNotNone(error_list)
        error_code_list = [error.code for error in error_list]
        self.assertIn(error_code, error_code_list)


    def test_valid_form(self):
        form = EventForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_start_time_in(self):
        invalid_form = self.valid_form_data
        invalid_form['start_time'] = timezone.now() + timezone.timedelta(hours=12)
        form = EventForm(data=invalid_form)

        self.assertFalse(form.is_valid())
        self.assertErrorCodeInForm(
            field_name='start_time',
            error_code='invalid_time',
            form=form
        )
