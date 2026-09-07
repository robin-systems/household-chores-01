from django.db import models


class HouseholdMember(models.Model):
    SLOT_CHOICES = [
        ("A", "Person A"),
        ("B", "Person B"),
    ]

    slot = models.CharField(max_length=1, choices=SLOT_CHOICES, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Chore(models.Model):
    PRIORITY_CHOICES = [
        ("normal", "Normal"),
        ("important", "Important"),
    ]

    RECURRENCE_CHOICES = [
        ("once", "One-time"),
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    ]

    ASSIGNMENT_CHOICES = [
        ("person_a", "Person A"),
        ("person_b", "Person B"),
        ("both", "Both"),
        ("rotation", "Rotation"),
    ]

    title = models.CharField(max_length=200)
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="normal",
    )
    recurrence = models.CharField(
        max_length=20,
        choices=RECURRENCE_CHOICES,
        default="once",
    )
    assignment = models.CharField(
        max_length=20,
        choices=ASSIGNMENT_CHOICES,
        default="both",
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ChoreOccurrence(models.Model):
    chore = models.ForeignKey(
        Chore,
        on_delete=models.CASCADE,
        related_name="occurrences",
    )
    due_date = models.DateField()
    assigned_member = models.ForeignKey(
        HouseholdMember,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_occurrences",
    )
    is_completed = models.BooleanField(default=False)
    completed_by = models.ForeignKey(
        HouseholdMember,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="completed_occurrences",
    )
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.chore.title} - {self.due_date}"