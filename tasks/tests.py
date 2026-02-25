from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Task


class TaskAPITest(APITestCase):

    def setUp(self):
        """
        Create test user and authenticate
        """
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="pass123"
        )

        # JWT Token
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.token
        )

        # Create sample task
        self.task = Task.objects.create(
            user=self.user,
            title="Test Task",
            description="Test Description",
            due_date=timezone.now() + timedelta(days=2),
            priority="High",
            status="Pending"
        )


    # -----------------------------
    # AUTH TESTS
    # -----------------------------

    def test_user_can_authenticate(self):
        url = reverse("token_obtain_pair")

        data = {
            "username": "testuser",
            "password": "testpass123"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)


    # -----------------------------
    # TASK CRUD TESTS
    # -----------------------------

    def test_create_task(self):
        url = "/api/tasks/"

        data = {
            "title": "New Task",
            "description": "Description",
            "due_date": (timezone.now() + timedelta(days=3)).isoformat(),
            "priority": "Medium",
            "status": "Pending"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)


    def test_get_tasks(self):
        url = "/api/tasks/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


    def test_get_single_task(self):
        url = f"/api/tasks/{self.task.id}/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Test Task")


    def test_update_task(self):
        url = f"/api/tasks/{self.task.id}/"

        data = {
            "title": "Updated Title"
        }

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, 200)

        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Title")


    def test_delete_task(self):
        url = f"/api/tasks/{self.task.id}/"

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Task.objects.count(), 0)


    # -----------------------------
    # PERMISSION TESTS
    # -----------------------------

    def test_user_cannot_access_other_users_task(self):

        other_task = Task.objects.create(
            user=self.other_user,
            title="Other Task",
            due_date=timezone.now() + timedelta(days=1),
            priority="Low",
            status="Pending"
        )

        url = f"/api/tasks/{other_task.id}/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


    # -----------------------------
    # VALIDATION TESTS
    # -----------------------------

    def test_due_date_must_be_future(self):
        url = "/api/tasks/"

        data = {
            "title": "Bad Task",
            "description": "Bad",
            "due_date": (timezone.now() - timedelta(days=1)).isoformat(),
            "priority": "Low",
            "status": "Pending"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)


    # -----------------------------
    # CUSTOM ACTION TESTS
    # -----------------------------

    def test_mark_complete(self):
        url = f"/api/tasks/{self.task.id}/mark_complete/"

        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)

        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "Completed")
        self.assertIsNotNone(self.task.completed_at)


    def test_mark_incomplete(self):
        self.task.status = "Completed"
        self.task.save()

        url = f"/api/tasks/{self.task.id}/mark_incomplete/"

        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)

        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "Pending")
        self.assertIsNone(self.task.completed_at)


    # -----------------------------
    # AUTH REQUIRED TEST
    # -----------------------------

    def test_unauthorized_access_denied(self):

        self.client.credentials()  # Remove token

        url = "/api/tasks/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)
