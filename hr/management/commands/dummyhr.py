from django.core.management.base import BaseCommand
from hr.models import Worker, Leave, Attendance
from datetime import date, time


class Command(BaseCommand):
    help = 'Add dummy data for Worker, Leave, and Attendance models'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Adding dummy workers...'))

        # Create dummy workers
        worker1 = Worker.objects.create(
            name='John Doe',
            role='HR',
            email='johndoe@example.com',
            phone='1234567890',
            has_system_access=True,
            tasks_completed=10,
            hours_worked=40.0
        )

        worker2 = Worker.objects.create(
            name='Jane Smith',
            role='AC',
            email='janesmith@example.com',
            phone='0987654321',
            has_system_access=False,
            tasks_completed=0,
            hours_worked=0.0
        )

        worker3 = Worker.objects.create(
            name='Mark Johnson',
            role='MG',
            email='markjohnson@example.com',
            phone='5555555555',
            has_system_access=True,
            tasks_completed=15,
            hours_worked=50.0
        )

        self.stdout.write(self.style.SUCCESS('Dummy workers added successfully!'))

        self.stdout.write(self.style.SUCCESS('Adding dummy leave records...'))

        # Create dummy leave records
        Leave.objects.create(
            worker=worker1,
            leave_type='ANNUAL',
            start_date=date(2024, 1, 10),
            end_date=date(2024, 1, 15),
            approved=True
        )

        Leave.objects.create(
            worker=worker2,
            leave_type='SICK',
            start_date=date(2024, 2, 5),
            end_date=date(2024, 2, 7),
            approved=False
        )

        Leave.objects.create(
            worker=worker3,
            leave_type='UNPAID',
            start_date=date(2024, 3, 20),
            end_date=date(2024, 3, 25),
            approved=True
        )

        self.stdout.write(self.style.SUCCESS('Dummy leave records added successfully!'))

        self.stdout.write(self.style.SUCCESS('Adding dummy attendance records...'))

        # Create dummy attendance records
        Attendance.objects.create(
            worker=worker1,
            date=date(2024, 9, 13),
            check_in_time=time(9, 0),
            check_out_time=time(17, 0),
            hours_worked=8.0
        )

        Attendance.objects.create(
            worker=worker2,
            date=date(2024, 9, 13),
            check_in_time=time(10, 0),
            check_out_time=time(16, 0),
            hours_worked=6.0
        )

        Attendance.objects.create(
            worker=worker3,
            date=date(2024, 9, 13),
            check_in_time=time(8, 30),
            check_out_time=time(18, 30),
            hours_worked=10.0
        )

        self.stdout.write(self.style.SUCCESS('Dummy attendance records added successfully!'))
