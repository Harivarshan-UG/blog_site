from typing import Any
from django.core.management.base import BaseCommand
from django.db import connection
from blog.models import Category

class Command(BaseCommand):
    help = "Inserts default category data and resets IDs to start from 1."

    def handle(self, *args, **options):
        # ... Your Category creation logic (get_or_create, etc.) should be here ...

        # Check the database engine before executing vendor-specific SQL
        if connection.vendor == 'mysql':
            with connection.cursor() as cursor:
                # This line only executes if the backend is MySQL
                cursor.execute("ALTER TABLE blog_category AUTO_INCREMENT = 1;")
                self.stdout.write(self.style.SUCCESS('Reset AUTO_INCREMENT for MySQL.'))
        
        # If the vendor is 'sqlite' (local), this block is skipped, fixing the error.

        self.stdout.write(self.style.SUCCESS('Successfully populated categories.'))