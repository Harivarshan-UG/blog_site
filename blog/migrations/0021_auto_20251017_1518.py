# blog/migrations/0020_load_initial_data.py (or whatever your filename is)

from django.db import migrations
from django.utils.text import slugify
import datetime

# --- Image Placeholders ---
# Using diverse placeholders for better visual variety
IMAGE_URLS = [
    "https://placehold.co/800x600/50bda1/ffffff/png?text=Tech+News",
    "https://placehold.co/800x600/17a2b8/ffffff/png?text=Travel+Blog",
    "https://placehold.co/800x600/ffc107/333333/png?text=Code+Tips",
    "https://placehold.co/800x600/28a745/ffffff/png?text=Lifestyle",
    "https://placehold.co/800x600/dc3545/ffffff/png?text=Updates",
] * 4  # Repeat to ensure we have enough images for 20 posts

AUTHOR_AVATAR = 'https://placehold.co/100x100/1F2937/FFFFFF?text=ADMIN'

def create_initial_data(apps, schema_editor):
    # Retrieve the historical versions of your models
    Category = apps.get_model('blog', 'Category')
    Author = apps.get_model('blog', 'Author')
    Post = apps.get_model('blog', 'Post') 
    
    # ----------------------------------------------------
    # 1. Create the Default Author
    # ----------------------------------------------------
    default_author, created = Author.objects.get_or_create(
        name='RenderDeployer',
        defaults={
            'avatar_url': AUTHOR_AVATAR,
        }
    )
    
    # ----------------------------------------------------
    # 2. Create Categories
    # ----------------------------------------------------
    category_names = ['Technology', 'Travel', 'Food', 'Finance', 'Opinion']
    categories = {}
    for name in category_names:
        category_obj, _ = Category.objects.get_or_create(name=name)
        categories[name] = category_obj

    # Create a list of categories to loop through for posts
    category_list = list(categories.values())

    # ----------------------------------------------------
    # 3. Create 20 Sample Posts (Dynamic Loop)
    # ----------------------------------------------------
    
    # Ensure there are no existing posts to prevent slug conflicts on initial run
    if Post.objects.count() == 0:
        
        for i in range(1, 21):
            
            # Use modulo to cycle through the 5 main categories
            category_index = (i - 1) % len(category_list)
            current_category = category_list[category_index]
            
            # Use modulo to cycle through the image URLs
            image_url = IMAGE_URLS[(i - 1) % len(IMAGE_URLS)]

            title = f"Post {i}: The State of {current_category.name} in 2025"
            content = (
                f"This is the dynamic content for Post number {i}. It belongs to the "
                f"**{current_category.name}** category. The purpose of this post "
                f"is to populate the new PostgreSQL database on Render. This ensures "
                f"that all frontend elements and database queries are working correctly "
                f"after the deployment and database switch. We are testing to ensure "
                f"our data structure (Title, Content, Category, Slug, Image URL) is fully functional. "
                f"The image link used here is: {image_url}."
            )
            
            # You can also manually adjust the date for better chronological look
            date_offset = datetime.timedelta(days=i * 2)
            
            Post.objects.get_or_create(
                title=title,
                defaults={
                    'content': content,
                    'category': current_category, 
                    'author_avatar_url': default_author.avatar_url,
                    # IMPORTANT: Use slugify to create the slug for the database
                    'slug': slugify(title), 
                    'img_url': image_url,
                    # Optionally set a specific date for ordering
                    'date_posted': datetime.datetime.now() - date_offset,
                }
            )


class Migration(migrations.Migration):

    dependencies = [
        # This ensures all necessary tables are created before we try to insert data
        ('blog', '0019_aboutus_author_remove_post_author'), # IMPORTANT: Verify this is your actual preceding migration name
    ]

    operations = [
        # This is the line that executes the function above
        migrations.RunPython(create_initial_data, migrations.RunPython.noop),
    ]