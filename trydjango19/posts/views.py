from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from .models import Post
from .forms import PostForm

# Create your views here.
# functional view receive request, and send response
def post_create(request):
    # enable built in form validation
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        #print form.cleaned_data.get("title")
        instance.save()
        # success message
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form
    }

    return render(request, "post_form.html", context)

def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    # variable to be passed to the view
    context = {
        "title": instance.title,
        "instance": instance,
    }
    return render(request, "post_detail.html", context)

def post_list(request):
    queryset = Post.objects.all()
    context = {
        "object_list": queryset,
        "title": "List"
    }
    return render(request, "index.html", context)

def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form
    }

    return render(request, "post_form.html", context)

def post_delete(request):
    return HttpResponse("<h1>Delete</h1>")
