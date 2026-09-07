Task 1: Create the core data model



Create the Django models needed for the application.



The data model should support:



\* Exactly two household members with editable names

\* Household chores

\* Normal and important priority

\* Assignment to Person A, Person B, both, or rotation

\* One-time, daily, weekly, and monthly recurrence

\* Scheduled task occurrences

\* Completion status

\* Recording which person completed a task



Create and run the initial Django migrations.



Task 2: Add default household data



Create a simple initial setup for a new household.



Include:



\* Two default household members

\* Around 8 to 12 common household chores

\* Examples such as vacuuming, mopping, cooking, laundry, taking out the trash, bathroom cleaning, and tidying



Allow the two member names to be changed.



Task 3: Build the weekly dashboard



Create the main page of the application.



The dashboard should:



\* Show the current week

\* Display scheduled chores by day

\* Show who each chore is assigned to

\* Clearly distinguish important chores

\* Show open and completed chores

\* Allow a chore to be marked as completed

\* Record who completed shared chores



Overdue chores should offer simple actions:



\* Mark as completed

\* Move to today

\* Choose a new date



Task 4: Add chore management and recurrence



Allow users to:



\* Add a new chore

\* Edit an existing chore

\* Delete a chore

\* Choose one-time, daily, weekly, or monthly recurrence

\* Assign the chore to Person A, Person B, both, or automatic rotation

\* Choose normal or important priority



For rotating chores, automatically alternate between the two people.



Task 5: Add the monthly view and statistics



Create a simple monthly view.



Include:



\* Monthly calendar overview

\* Completed and open chores

\* Number of completed chores per person

\* Completion percentage per person

\* Total completed and open chores



For shared chores, count the completion for the person who actually completed the task.



Task 6: Polish the simple user experience



Keep the interface easy to understand for non-technical users.



Improve:



\* Navigation

\* Labels and buttons

\* Empty states

\* Validation

\* In-app reminders for due and overdue chores

\* Mobile-friendly layout



Avoid unnecessary settings, menus, and advanced configuration.



