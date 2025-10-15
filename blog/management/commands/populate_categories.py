from typing import Any
from django.core.management.base import BaseCommand
from django.db import connection
from blog.models import Category

class Command(BaseCommand):
    help = "Inserts default category data and resets IDs to start from 1."

    def handle(self, *args: Any, **options: Any):
        # Delete all existing data
        Category.objects.all().delete()

        # Reset the AUTO_INCREMENT counter
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE blog_category AUTO_INCREMENT = 1;")

        # Insert new categories
        categories = ['Django', 'Programming', 'Sports', 'Entertainment', 'Technology', 'Health', 'Business']
        for category_name in categories:
            Category.objects.create(name=category_name)

        self.stdout.write(self.style.SUCCESS("✅ Categories reinserted successfully with IDs starting from 1."))

