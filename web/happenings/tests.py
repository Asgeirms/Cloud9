import datetime

from django.test import TestCase

from .models import Event, Schedule


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
        schedule = Schedule.objects.create(start_time=datetime.datetime.now(),
                                           end_time=datetime.datetime.now() + datetime.timedelta(2), event=event)
        self.assertEqual(schedule.event.name, self.valid_form_data["name"])
        event.name = "TestEventChanged"
        event.save()
        self.assertEqual(schedule.event.name, "TestEventChanged")
