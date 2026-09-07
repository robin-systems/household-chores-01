from datetime import timedelta

from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Chore, ChoreOccurrence, HouseholdMember


def dashboard(request):
    today = timezone.localdate()
    week_start = today - timedelta(days=today.weekday())
    week_dates = [week_start + timedelta(days=i) for i in range(7)]

    members = list(HouseholdMember.objects.order_by("slot"))
    member_a = next((member for member in members if member.slot == "A"), None)
    member_b = next((member for member in members if member.slot == "B"), None)

    # Until the full recurrence system is implemented in Task 4,
    # create one occurrence for each active chore in the current week.
    for chore in Chore.objects.filter(is_active=True):
        already_scheduled = ChoreOccurrence.objects.filter(
            chore=chore,
            due_date__range=(week_dates[0], week_dates[-1]),
        ).exists()

        if already_scheduled:
            continue

        assigned_member = None

        if chore.assignment == "person_a":
            assigned_member = member_a
        elif chore.assignment == "person_b":
            assigned_member = member_b
        elif chore.assignment == "rotation":
            previous = (
                ChoreOccurrence.objects.filter(
                    chore=chore,
                    assigned_member__isnull=False,
                )
                .order_by("-due_date", "-id")
                .first()
            )

            if previous and previous.assigned_member == member_a:
                assigned_member = member_b
            else:
                assigned_member = member_a

        ChoreOccurrence.objects.create(
            chore=chore,
            due_date=today,
            assigned_member=assigned_member,
        )

    days = []

    for day in week_dates:
        occurrences = (
            ChoreOccurrence.objects.filter(due_date=day)
            .select_related("chore", "assigned_member", "completed_by")
            .order_by("-chore__priority", "chore__title")
        )

        days.append(
            {
                "date": day,
                "occurrences": occurrences,
            }
        )

    return render(
        request,
        "chores/dashboard.html",
        {
            "days": days,
            "members": members,
            "today": today,
        },
    )


@require_POST
def complete_occurrence(request, occurrence_id):
    occurrence = get_object_or_404(
        ChoreOccurrence,
        id=occurrence_id,
    )

    completed_by = occurrence.assigned_member

    if completed_by is None:
        member_id = request.POST.get("member_id")

        if member_id:
            completed_by = get_object_or_404(
                HouseholdMember,
                id=member_id,
            )

    if completed_by is not None:
        occurrence.is_completed = True
        occurrence.completed_by = completed_by
        occurrence.completed_at = timezone.now()
        occurrence.save(
            update_fields=[
                "is_completed",
                "completed_by",
                "completed_at",
            ]
        )

    return redirect("dashboard")