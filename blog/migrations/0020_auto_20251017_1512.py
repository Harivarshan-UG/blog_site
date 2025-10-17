# blog/migrations/0020_load_initial_data.py (or whatever the filename is)

from django.db import migrations
from django.utils.text import slugify

def create_initial_data(apps, schema_editor):
    # Retrieve the historical versions of your models
    Category = apps.get_model('blog', 'Category')
    Author = apps.get_model('blog', 'Author')
    Post = apps.get_model('blog', 'Post') 
    
    # ----------------------------------------------------
    # 1. Create the Default Author
    # ----------------------------------------------------
    # Use get_or_create to prevent running this logic multiple times on the same DB
    default_author, created = Author.objects.get_or_create(
        name='Admin User',
        defaults={
            'avatar_url': 'https://placehold.co/100x100/1F2937/FFFFFF?text=ADMIN',
        }
    )
    
    # ----------------------------------------------------
    # 2. Create Categories
    # ----------------------------------------------------
    # Storing them in variables so we can use them in Post creation
    cat_tech, _ = Category.objects.get_or_create(name='Technology')
    cat_travel, _ = Category.objects.get_or_create(name='Travel')
    cat_lifestyle, _ = Category.objects.get_or_create(name='Lifestyle')

    # ----------------------------------------------------
    # 3. Create Sample Posts
    # ----------------------------------------------------
    
    # Post 1: Tech 
    title_1 = "Successful Database Migration to PostgreSQL"
    Post.objects.get_or_create(
        title=title_1,
        defaults={
            'content': "We've successfully moved the blog backend from a local MySQL setup to Render's free PostgreSQL service! This post is proof that the data migration script executed correctly. Happy blogging!",
            'category': cat_tech, 
            'author_avatar_url': default_author.avatar_url,
            'slug': slugify(title_1), # Use slugify manually here
        }
    )

    # Post 2: Lifestyle 
    title_2 = "Making the Most of the Render Free Tier"
    Post.objects.get_or_create(
        title=title_2,
        defaults={
            'content': "For hobby projects, Render offers a generous free web service and a PostgreSQL database. It's the perfect environment to learn and deploy full-stack applications like this Django blog.",
            'category': cat_lifestyle, 
            'author_avatar_url': default_author.avatar_url,
            'slug': slugify(title_2),
        }
    )
    
    # Post 3: Travel (Example without explicit img_url, relies on model default)
    title_3 = "Tips for First-Time Django Deployment"
    Post.objects.get_or_create(
        title=title_3,
        defaults={
            'content': "Remember to use environment variables for your database URL and secret key, and make sure your build command runs `python manage.py migrate`!",
            'category': cat_travel, 
            'author_avatar_url': default_author.avatar_url,
            'slug': slugify(title_3),
        }
    )
    
    # Note: We don't need to specify the 'author' ForeignKey field here, 
    # as your Post model does not have an 'author' field. 
    # It seems the 'author_avatar_url' is used instead for author info in the Post model.


class Migration(migrations.Migration):

    dependencies = [
        # This ensures all necessary tables are created before we try to insert data
        ('blog', '0019_aboutus_author_remove_post_author'), # Use your actual preceding migration name
    ]

    operations = [
        # This is the line that executes the function above
        migrations.RunPython(create_initial_data, migrations.RunPython.noop),
    ]