# habits/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Habit

User = get_user_model()


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

    def test_create_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place='Дома',
            time='08:00:00',
            action='Пить воду',
            duration=30,
            reward='Кофе',
            is_public=True
        )
        self.assertEqual(habit.action, 'Пить воду')
        self.assertTrue(habit.is_public)


class HabitAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        data = {
            'place': 'Дома',
            'time': '08:00:00',
            'action': 'Пить воду',
            'duration': 30,
            'reward': 'Кофе',
            'is_public': True
        }
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_habits(self):
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)