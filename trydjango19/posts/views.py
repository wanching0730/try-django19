from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# from urllib.parse import quote_plus

from .models import Post
from .forms import PostForm

# Create your views here.
# functional view receive request, and send response
def post_create(request):

    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    # 'request.POST or None' enable built in form validation
    # 'request.FILES' enable data come in thru the form
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        #print form.cleaned_data.get("title")
        instance.save()
        messages.success(request, "Successfully Created!")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully created!")

    context = {
        "form": form
    }

    return render(request, "post_form.html", context)

def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    # share_string = quote_plus(instance.content)
    # variable to be passed to the view
    context = {
        "title": instance.title,
        "instance": instance,
        # "share_string": share_string
    }
    return render(request, "post_detail.html", context)

def post_list(request):
    queryset_list = Post.objects.active()
    # queryset = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(queryset_list, 10)

    page_request_var = "page"
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        queryset = paginator.page(1)
    except EmptyPage:
        # if page is out of range (eg: 9999), delivaer last page
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "List",
        "page_request_var": page_request_var
    }
    return render(request, "post_list.html", context)

def post_update(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Item saved!")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form
    }

    return render(request, "post_form.html", context)

def post_delete(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("posts:list")