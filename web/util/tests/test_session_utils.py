from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.sessions.backends.db import SessionStore
from django.core.exceptions import ValidationError

from http import HTTPStatus

from authenticate.models import User
from happenings.models import Event, Schedule
from swiping.views import SwipingEventsView

from util.session_utils import read_session_data, add_data_to_session_as_dict
import json

class SessionUtilsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.anon_user = AnonymousUser()
        self.auth_user = User.objects.create(username="Jaya")
        self.request = self.factory.get(reverse('swiping'))
        self.request.user = self.anon_user 
        self.request.session = SessionStore()


    def test_add_valid_data_to_session(self):
        KEY = "KEY"
        VALID_DATA = Event.objects.create(host_id=self.auth_user.pk)

        self.assertFalse(self.request.session.modified)
        
        add_data_to_session_as_dict(
            request=self.request,
            name=KEY,
            session=dict(),
            key=KEY,
            value=VALID_DATA
        )

        response = SwipingEventsView.as_view()(self.request)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(self.request.session.modified)

    def test_add_invalid_data_to_session(self):
        KEY= "KEY"

        INVALID_TEXT_DATA = "Invalid data"
        INVALID_NUM_DATA = 1230

        with self.assertRaises(ValidationError):
            add_data_to_session_as_dict(
                request=self.request,
                name=KEY,
                session=dict(),
                key=KEY,
                value=INVALID_TEXT_DATA
            )
        
        with self.assertRaises(ValidationError):
            add_data_to_session_as_dict(
                request=self.request,
                name=KEY,
                session=dict(),
                key=KEY,
                value=INVALID_NUM_DATA
            )

    def test_read_session_data(self):
        session_data = "TEST_DATA"
        name = "event"
        self.request.session['event'] = json.dumps(session_data)

        EXPECTED_DATA = read_session_data(self.request, name)
        self.assertEqual(session_data, EXPECTED_DATA)
