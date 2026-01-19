from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Photographer, Event, Assignment
import datetime


class AssignmentTests(APITestCase):
    def setUp(self):
        self.photographers = []
        for i in range(5):
            p = Photographer.objects.create(
                name=f"Photo_{i}",
                email=f"p{i}@example.com",
                phone=f"123456789{i}",
                is_active=True
            )
            self.photographers.append(p)

    def test_successful_assignment(self):
        """
        Ensure we can assign photographers when availability allows.
        """
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        event = Event.objects.create(
            event_name="Wedding Shoot",
            event_date=tomorrow,
            photographers_required=2
        )

        url = reverse('event-assign-photographers', args=[event.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Assignment.objects.count(), 2)

        self.assertIn('assigned_photographers', response.data)
        self.assertEqual(len(response.data['assigned_photographers']), 2)

    def test_not_enough_photographers(self):
        """
        Ensure we get a 400 error when requirements exceed availability.
        """
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        event = Event.objects.create(
            event_name="Big Concert",
            event_date=tomorrow,
            photographers_required=10
        )

        url = reverse('event-assign-photographers', args=[event.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertEqual(response.data['code'], 'VALIDATION_ERROR')
        self.assertEqual(Assignment.objects.count(), 0)

    def test_no_double_booking(self):
        """
        Ensure a photographer cannot be assigned to two events on the same day.
        """
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)

        event1 = Event.objects.create(
            event_name="Morning Event",
            event_date=tomorrow,
            photographers_required=3
        )
        url1 = reverse('event-assign-photographers', args=[event1.id])
        self.client.post(url1)

        event2 = Event.objects.create(
            event_name="Evening Event",
            event_date=tomorrow,
            photographers_required=3
        )
        url2 = reverse('event-assign-photographers', args=[event2.id])
        response = self.client.post(url2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Assignment.objects.filter(event=event2).count(), 0)

    def test_past_event_assignment(self):
        """
        Ensure we cannot assign to past events.
        """
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        event = Event.objects.create(
            event_name="Past Event",
            event_date=yesterday,
            photographers_required=1
        )

        url = reverse('event-assign-photographers', args=[event.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_photographer_schedule_excludes_assigned_photographers(self):
        """
        Ensure the photographer schedule endpoint returns events without the redundant
        'assigned_photographers' field.
        """
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        event = Event.objects.create(
            event_name="Schedule Check Event",
            event_date=tomorrow,
            photographers_required=1
        )
        photographer = self.photographers[0]

        Assignment.objects.create(event=event, photographer=photographer)

        url = reverse('photographer-schedule', args=[photographer.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['event_name'], "Schedule Check Event")
        self.assertNotIn('assigned_photographers', response.data[0])