from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings

def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    return "%s/%s.%s" %(instance.id, instance.id, extension)

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120) 
    slug = models.SlugField(unique=True)
    image = models.ImageField(
     upload_to=upload_location,
     null=True, 
     blank=True,
     width_field="width_field",
     height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False) # saved to database for the first time
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    # show the first column (in string) in admin, if not, it displays Post object
    def __str__(self): 
        return self.title
    
    # absolute url: https://www.google.com
    # relative url: home.php
    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

    # describe things that not related to fields 
    class Meta:
        ordering = ["-timestamp", "-updated"]

# using Recursive Function
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    if qs.exists():
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    
    return slug

# before create new Post, gone thru this function first
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)
