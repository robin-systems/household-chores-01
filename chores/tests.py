from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Chore, ChoreOccurrence, HouseholdMember


class ChoreTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        ChoreOccurrence.objects.all().delete()
        Chore.objects.all().delete()
        HouseholdMember.objects.all().delete()

        cls.person_a = HouseholdMember.objects.create(
            slot="A",
            name="Person A",
        )

        cls.person_b = HouseholdMember.objects.create(
            slot="B",
            name="Person B",
        )

    def test_chore_model_stores_settings(self):
        chore = Chore.objects.create(
            title="Vacuuming",
            priority="important",
            recurrence="weekly",
            assignment="rotation",
        )

        self.assertEqual(chore.title, "Vacuuming")
        self.assertEqual(chore.priority, "important")
        self.assertEqual(chore.recurrence, "weekly")
        self.assertEqual(chore.assignment, "rotation")
        self.assertTrue(chore.is_active)

    def test_dashboard_loads_and_creates_occurrence(self):
        chore = Chore.objects.create(
            title="Mopping",
            assignment="person_a",
        )

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Household Chores")
        self.assertContains(response, "Mopping")

        occurrence = ChoreOccurrence.objects.get(chore=chore)

        self.assertEqual(
            occurrence.assigned_member,
            self.person_a,
        )

    def test_assigned_chore_can_be_completed(self):
        chore = Chore.objects.create(
            title="Cooking",
            assignment="person_b",
        )

        occurrence = ChoreOccurrence.objects.create(
            chore=chore,
            due_date=timezone.localdate(),
            assigned_member=self.person_b,
        )

        response = self.client.post(
            reverse(
                "complete_occurrence",
                args=[occurrence.id],
            )
        )

        self.assertEqual(response.status_code, 302)

        occurrence.refresh_from_db()

        self.assertTrue(occurrence.is_completed)
        self.assertEqual(
            occurrence.completed_by,
            self.person_b,
        )
        self.assertIsNotNone(occurrence.completed_at)

    def test_shared_chore_records_who_completed_it(self):
        chore = Chore.objects.create(
            title="Laundry",
            assignment="both",
        )

        occurrence = ChoreOccurrence.objects.create(
            chore=chore,
            due_date=timezone.localdate(),
        )

        response = self.client.post(
            reverse(
                "complete_occurrence",
                args=[occurrence.id],
            ),
            {
                "member_id": self.person_a.id,
            },
        )

        self.assertEqual(response.status_code, 302)

        occurrence.refresh_from_db()

        self.assertTrue(occurrence.is_completed)
        self.assertEqual(
            occurrence.completed_by,
            self.person_a,
        )