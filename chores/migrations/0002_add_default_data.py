from django.db import migrations


def add_default_data(apps, schema_editor):
    HouseholdMember = apps.get_model("chores", "HouseholdMember")
    Chore = apps.get_model("chores", "Chore")

    HouseholdMember.objects.get_or_create(
        slot="A",
        defaults={"name": "Person A"},
    )

    HouseholdMember.objects.get_or_create(
        slot="B",
        defaults={"name": "Person B"},
    )

    default_chores = [
        ("Vacuuming", "normal", "weekly", "both"),
        ("Mopping", "normal", "weekly", "person_a"),
        ("Cooking", "normal", "daily", "person_b"),
        ("Taking out the trash", "normal", "weekly", "rotation"),
        ("Cleaning the bathroom", "important", "weekly", "rotation"),
        ("Laundry", "normal", "weekly", "both"),
        ("Tidying up", "normal", "daily", "both"),
        ("Changing bed sheets", "normal", "weekly", "rotation"),
        ("Cleaning the kitchen", "normal", "weekly", "both"),
        ("Groceries", "important", "weekly", "both"),
    ]

    for title, priority, recurrence, assignment in default_chores:
        Chore.objects.get_or_create(
            title=title,
            defaults={
                "priority": priority,
                "recurrence": recurrence,
                "assignment": assignment,
            },
        )


def remove_default_data(apps, schema_editor):
    HouseholdMember = apps.get_model("chores", "HouseholdMember")
    Chore = apps.get_model("chores", "Chore")

    HouseholdMember.objects.filter(slot__in=["A", "B"]).delete()

    Chore.objects.filter(
        title__in=[
            "Vacuuming",
            "Mopping",
            "Cooking",
            "Taking out the trash",
            "Cleaning the bathroom",
            "Laundry",
            "Tidying up",
            "Changing bed sheets",
            "Cleaning the kitchen",
            "Groceries",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("chores", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            add_default_data,
            remove_default_data,
        ),
    ]