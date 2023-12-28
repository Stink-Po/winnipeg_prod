from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
from .forms import SearchForm
from .models import Post
from taggit.models import Tag
from .forms import PostForm
from projects.views import is_admin
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_protect


def paginate_results(request, queryset, num_items=3):
    paginator = Paginator(queryset, num_items)
    page_number = request.GET.get("page", 1)
    try:
        results = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        results = paginator.page(1)
    return results


def post_list(request, tag_slug=None):
    form = SearchForm()
    all_tags = get_list_or_404(Tag)
    posts_list = Post.published.all()

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__in=[tag])
    else:
        tag = None
    posts = paginate_results(request, posts_list)

    return render(request, "blog/post/list.html", {
        "posts": posts,
        "tag": tag,
        "all_tags": all_tags,
        "form": form
    })


def post_detail(request, year, month, day, post):
    form = SearchForm()
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             slug=post, publish__year=year,
                             publish__month=month, publish__day=day)

    tags = post.tags.all()
    post_tags_ids = post.tags.values_list("id", flat=True)

    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by("-same_tags", "-publish")[:4]

    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results = Post.published.annotate(search=SearchVector("title", "body", "subtitle")).filter(search=query)
            return render(request, "blog/post/search.html", {
                'form': form,
                'query': query,
                'results': results,
            })

    return render(request, "blog/post/detail.html", {
        "post": post,
        "tags": tags,
        "similar_posts": similar_posts,
        "form": form,
    })


def post_search(request):
    form = SearchForm()
    query = request.GET.get("query")
    results = []

    if query:
        form = SearchForm(request.GET)
        if form.is_valid():
            results = Post.published.annotate(search=SearchVector("title", "body", "subtitle")).filter(search=query)

    return render(request, "blog/post/search.html", {
        'form': form,
        'query': query,
        'results': results
    })


@csrf_protect
@user_passes_test(is_admin)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Assuming you are using authentication
            post.save()
            form.save_m2m()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()

    return render(request, 'blog/post/new_post_form.html', {'form': form})
