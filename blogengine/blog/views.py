from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Post, Tag
from .utils import ObjectDetailMixin, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin

from .forms import TagForm, PostForm



def posts_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()


    # posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url,
    }

    return render(request, 'blog/index.html', context=context)


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags':tags})


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = 'blog/post_create.html'
    raise_exception = True

class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True

class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True

class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = True

class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete.html'
    success_url = 'posts_list'
    raise_exception = True

class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete.html'
    success_url = 'tags_list_url'
    raise_exception = True