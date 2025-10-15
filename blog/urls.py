from django.urls import path
from . import views

app_name='blog'

urlpatterns = [
    path("", views.index, name="index"), #This path direct to the index.html
    path("post/<slug:slug>", views.post_detail, name="detail" ), #This path direct to the detail.html
    path("contact", views.contact_view, name="contact"),

]