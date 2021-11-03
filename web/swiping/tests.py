from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone
from django.test.client import Client

from authenticate.models import User
from happenings.models import Schedule, Event
from util.session_utils import read_session_data

from http import HTTPStatus
from unittest import skip

import numpy as np

class SwipingEventsViewTests(TestCase):
    def setUp(self):
        self.url = reverse('swiping')
        self.admin = User(username="Superuser", password="pass")
        self.admin.is_superuser = True
        self.admin.save()
        self.client = Client()
        self.client.login(username="Superuser", password="pass")

        # Initializing events for the swiping
        self.TOTAL_EVENTS = 10
        for num in range(self.TOTAL_EVENTS):
            event = Event.objects.create(host_id=self.admin.pk, admin_approved='A')

            Schedule.objects.create(
                start_time=timezone.now(),
                end_time=timezone.now() + timezone.timedelta(hours=num+2),
                event=event
            )

        self.query = {
            'page': 1,
            'swiped': 'yes'
        }

    def test_success_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    @skip("1: Causing issues when running the whole Test Case, works fine separately")
    def test_get_correct_queryset(self):
        response = self.client.get(self.url)
        queryset = response.context_data['view'].object_list
    
        self.assertEqual(self.TOTAL_EVENTS, queryset.count())

    @skip("Same as 1")
    def test_viewed_events_in_session(self):
        # For anon users

        swiped = self.client.get(self.url, self.query)
        INIT_SWIPE = 1

        viewed_events = read_session_data(self.client, 'viewed_events')
        self.assertEqual(len(viewed_events.keys()), 1)

        NUM_SWIPES = 5
        for swipe in range(NUM_SWIPES):
            swiped = self.client.get(self.url, self.query)
            self.assertTrue(swiped.context_data["is_paginated"])
       
        viewed_events = read_session_data(self.client, 'viewed_events')
        
        self.assertEqual(len(viewed_events.keys()), NUM_SWIPES+INIT_SWIPE)
        
    @skip("Same as 1")
    def test_filtering_events(self):
        swiped = self.client.get(self.url, self.query)
        INIT_SWIPE = 1

        NUM_SWIPES = 5
        for swipe in range(NUM_SWIPES):
            swiped = self.client.get(self.url, self.query)
            self.assertTrue(swiped.context_data["is_paginated"])
       
        viewed_events = read_session_data(self.client, 'viewed_events')
        EXPECTED_REMAINDER = swiped.context_data['view'].object_list.count()

        self.assertEqual(self.TOTAL_EVENTS-(NUM_SWIPES+INIT_SWIPE), EXPECTED_REMAINDER)


    @skip("Same as 1: Suspect it cache the session data such that it ruins the integration flow")
    def test_finished_swiping(self):
        EXPECTED_URL = reverse('swiping_finish')
        swiped = self.client.get(self.url, self.query)
        INIT_SWIPE = 1 

        NUM_SWIPES = self.TOTAL_EVENTS - INIT_SWIPE
        for swipe in range(NUM_SWIPES):
            swiped = self.client.get(self.url, self.query)

        self.assertEqual(swiped.url, EXPECTED_URL)
        
        # Retry
        response = self.client.get(self.url, self.query)
        
        self.assertEqual(response.url, EXPECTED_URL)

class SimpleSwAIpeTest(TestCase):
    def test_swipe_right(self):
        # The average score of all weights should increase

        DECREASE_RATE = 0.8
        weights = [1, 0.5, 0.01, 0.1, 1, 0.9999, 1]
        initial_avg = np.average(weights)
        for i in range(100):
            for i, weight in enumerate(weights):
                weights[i] += (1-weight)*(DECREASE_RATE)
                self.assertLessEqual(weights[i], 1)
            self.assertGreater(np.average(weights), initial_avg, )

    def test_swipe_left(self):
        # The average score of all weights should increase

        DECREASE_RATE = 0.8
        weights = [1, 0.5, 0.01, 0.1, 1, 0.9999, 1]
        initial_avg = np.average(weights)
        for i in range(100):
            for i, weight in enumerate(weights):
                weights[i] *= DECREASE_RATE
                self.assertGreater(weights[i], 0)
            self.assertGreater(initial_avg, np.average(weights))

    def test_random_selection(self):
        weights =   np.array([1, 0.5, 0.1, 0.05, 0.01])
        ids =       np.array([0, 1, 2, 3, 4])
        pick_rates = {}
        for i in range(1000):
            drawn_id : int = np.random.choice(ids, 1, p=(weights/weights.sum()))[0]
            try:
                pick_rates[drawn_id] += 1
            except KeyError:
                pick_rates[drawn_id] = 1
        for i in range(len(pick_rates.keys())-1):
            self.assertGreater(pick_rates[i], pick_rates[i+1])

