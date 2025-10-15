from django.contrib import admin
from typing import Any
from .models import Post, Category



# Register your models here.


admin.site.register(Post)
admin.site.register(Category)

