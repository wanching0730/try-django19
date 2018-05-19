from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=120) 
    image = models.ImageField(
     null=True, 
     blank=True,
     width_field="width_field",
     height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False) # saved to database for the first time
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    # show the first column (in string) in admin, if not, it displays Post object
    def __str__(self): 
        return self.title
    
    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"id": self.id})

    # describe things that not related to fields 
    class Meta:
        ordering = ["-timestamp", "-updated"]