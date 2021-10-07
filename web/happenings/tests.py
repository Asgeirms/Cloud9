import datetime
from django.utils import timezone

from django.test import TestCase

from authenticate.models import User
from .models import Event, Schedule
from .forms import EventForm, ScheduleForm, FilterForm


class EventAndScheduleSaveTest(TestCase):

    def setUp(self):
        self.user = User.objects.create()

        self.valid_form_data = {
            "name": "TestEvent",
            "location": "TestLocation",
            "min_price": 0,
            "max_price": 10,
            "description": "A long description"
        }

    def test_create_event(self):
        event = Event.objects.create(name="TestEvent", location="TestLocation", min_price=0, max_price=10,
                                     description="A long description", host=self.user)
        self.assertEqual(event.name, self.valid_form_data["name"])
        self.assertFalse(event.admin_approved)
        event.name = "TestEventChanged"
        event.save()
        self.assertEqual(event.name, "TestEventChanged")

    def test_create_schedule(self):
        event = Event.objects.create(name="TestEvent", location="TestLocation", min_price=0, max_price=10,
                                     description="A long description", host=self.user)
        schedule = Schedule.objects.create(start_time=timezone.now(),
                                           end_time=timezone.now() + timezone.timedelta(hours=2), event=event)
        self.assertEqual(schedule.event.name, self.valid_form_data["name"])
        event.name = "TestEventChanged"
        event.save()
        self.assertEqual(schedule.event.name, "TestEventChanged")


class EventAndScheduleFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.valid_event_form_data = {
            "name": "Henrik's DevBlog: The Movie",
            "location": "thelist.no",
            "min_price": 0,
            "max_price": 10,
            "description": "The rise of Django developer beginner to successfully and established Django Pro at The List"
        }

        self.valid_schedule_form_data = {
            "start_time": timezone.now(),
            "end_time": timezone.now() + timezone.timedelta(hours=3),
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


    def test_valid_event_form(self):
        form = EventForm(data=self.valid_event_form_data)
        form.instance.host = self.user
        self.assertTrue(form.is_valid())

    def test_invalid_price(self):
        invalid_form = self.valid_event_form_data
        invalid_form['min_price'] = 9999

        invalid_price = EventForm(data=invalid_form)
        invalid_price.instance.host = self.user

        self.assertFalse(invalid_price.is_valid())
        self.assertErrorCodeInForm(
            field_name='min_price',
            error_code='invalid_price',
            form=invalid_price
        )

    def test_invalid_start_time(self):
        valid_event = Event()
        
        invalid_form = self.valid_schedule_form_data
        invalid_form['start_time'] = timezone.now() + timezone.timedelta(hours=99)
        invalid_start_time = ScheduleForm(data=invalid_form)
        invalid_start_time.instance.event = valid_event

        self.assertFalse(invalid_start_time.is_valid())
        self.assertErrorCodeInForm(
            field_name='start_time',
            error_code='invalid_time',
            form=invalid_start_time
        )

class FilterFormTest(TestCase):

    def setUp(self):
        self.valid_filter_form_data = {
            "from_time": datetime.datetime.now(),
            "to_time": datetime.datetime.now(),
            "max_price": 200
        }

    def test_valid_filter_form_all_data(self):
        valid_form = FilterForm(data=self.valid_filter_form_data)
        self.assertTrue(valid_form.is_valid())

    def test_valid_filter_form_missing_to_time(self):
        missing_to_time_data = self.valid_filter_form_data
        missing_to_time_data["to_time"]= None
        valid_form = FilterForm(data=missing_to_time_data)
        self.assertTrue(valid_form.is_valid())

    def test_valid_filter_form_missing_from_time(self):
        missing_from_time_data = self.valid_filter_form_data
        missing_from_time_data["from_time"]= None
        valid_form = FilterForm(data=missing_from_time_data)
        self.assertTrue(valid_form.is_valid())

    def test_valid_filter_form_missing_max_price(self):
        missing_max_price_data = self.valid_filter_form_data
        missing_max_price_data["max_price"]= None
        valid_form = FilterForm(data=missing_max_price_data)
        self.assertTrue(valid_form.is_valid())

    def test_invalid_filter_form_invalid_time(self):
        invalid_time_data = self.valid_filter_form_data
        invalid_time_data["from_time"]= datetime.datetime.now() + datetime.timedelta(hours=1)
        invalid_form = FilterForm(data=invalid_time_data)
        self.assertFalse(invalid_form.is_valid())
        