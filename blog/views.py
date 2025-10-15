from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
import logging
from .models import Post
from django.core.paginator import Paginator
from .forms import ContactForm

logger = logging.getLogger(__name__)

blog_title = "BlogSpot-News"

def index(request):
    # Use a queryset (not the context dict) for the Paginator
    posts = Post.objects.all()
    paginator = Paginator(posts, 8)  # 10 posts per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj.object_list,   # the posts on the current page
        'page_obj': page_obj,                # page controls (has_next, number, etc.)
        'blog_title': blog_title,
        'categories': Post.objects.values_list('category', flat=True).distinct(),
    }

    return render(request, 'index.html', context)


def post_detail(request, slug):
    try:
        post = Post.objects.get(slug=slug)
        related_posts = Post.objects.filter(category=post.category).exclude(pk=post.pk)[:3]
    except Post.DoesNotExist:
        raise Http404("Post does not exist")

    return render(request, 'detail.html', {'post': post, 'related_posts': related_posts})

def contact_view(request):
    success_message = None  # default is none
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')

            # Log message (optional)
            logger.debug(f'Contact POST data: {name}, {email}, {message}')

            # Example success message
            success_message = "Your message was sent successfully!"

            # Re-render contact.html with a fresh form + success flag
            return render(
                request,
                'contact.html',
                {
                    'form': ContactForm(),
                    'success_message': success_message,
                }
            )
        else:
            logger.warning('Contact form invalid: %s', form.errors)
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

