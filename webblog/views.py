import pytz
from datetime import datetime

from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import NewPost, AddComment, AddTag, RegisterUserForm, LoginForm, AddContent
from .models import BlogUser, BlogPost, Comment, Tag
from .decorators import anonymous_required

# Create your views here.

def index1(request):
    posts_list = BlogPost.objects.all().order_by('-id')
    page = request.GET.get('page', 1)

    paginator = Paginator(posts_list, 4)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/index1.html', locals())


@login_required(login_url=reverse_lazy('blog:views-login1'))
def new_post1(request, *args, **kwargs):
    if request.method == 'POST':
        form = NewPost(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = BlogUser.objects.get(email=request.user.email)
            # data.update({'author':user})
            post = BlogPost.objects.create(title=data['title'],content=data['content'])
            post.author.add(user)
            if data['tags'] == '':
                pass
            else:
                post.tag.create(name=data['tags'])
            form.full_clean()
            return redirect('blog:views-index1')
        else:
            form = NewPost(request.POST)
    else:
        form = NewPost()

    return render(request, 'blog/create_post1.html', locals())

def post_detail(request, *args, **kwargs):
    post_id = kwargs['post_id']
    post = BlogPost.objects.get(id=kwargs['post_id'])
    form_tags = AddTag()
    form_comment = AddComment()
    form_content = AddContent()
    if request.method == 'POST':
        if request.POST['form'] == 'addtag':
            form_tags = AddTag(request.POST)
            if form_tags.is_valid():
                post.tag.create(name=form_tags.cleaned_data['name'])
                form_tags = AddTag()
                return HttpResponseRedirect(reverse('blog:views-post-detail',args=(post_id,)))
            else:
                form_tags = AddTag(request.POST)
                return render(request, 'blog/blog_detail1.html', locals())
        elif request.POST['form'] == 'addcomment':
            form_comment = AddComment(request.POST)
            # csrf = form_comment['csrf_token']
            if form_comment.is_valid():
                data = form_comment.cleaned_data
                user = BlogUser.objects.get(email=request.user.email)
                comment = Comment.objects.create(content=data['cccontent'])
                comment.author.add(user)
                post.comments.add(comment)
                form_comment = AddComment()
                return HttpResponseRedirect(reverse('blog:views-post-detail',args=(post_id,)))
            else:
                form_comment = AddComment(request.POST)
                return render(request, 'blog/blog_detail1.html', locals())
        elif request.POST['form'] == 'addcontent':
            form_content = AddContent(request.POST)
            if form_content.is_valid():
                post = BlogPost.objects.get(id=post_id)
                post.content = post.content + ' ' + form_content.cleaned_data['ccontent']
                user = BlogUser.objects.get(email=request.user.email)
                post.author.add(user)
                post.save()
                return HttpResponseRedirect(reverse('blog:views-post-detail',args=(post_id,)))
    else:
        return render(request, 'blog/blog_detail1.html', locals())

def post_detail1(request, *args, **kwargs):
    post = BlogPost.objects.get(id=1)
    form_tags = AddTag()
    form_comment = AddComment()
    form_content = AddContent()
    return render(request, 'blog/blog_detail1.html', locals())

@anonymous_required(next_url=reverse_lazy('blog:views-index1'))
def register1(request, *args, **kwargs):
    form_reg = RegisterUserForm()
    if request.method == 'POST':
        form_reg = RegisterUserForm(request.POST)
        if form_reg.is_valid():
            data = form_reg.cleaned_data
            form_reg.save()
            return HttpResponseRedirect(reverse('blog:views-login1'))
        else:
            form_reg = RegisterUserForm(request.POST)
            return render(request, 'blog/register1.html', locals())

    return render(request, 'blog/register1.html', locals())

@anonymous_required(next_url=reverse_lazy('blog:views-index1'))
def login1(request):
    #if 'next' in request.GET:
    #    if request.GET['next'] == '/new_post/':
    #        hint = 'new_post'
    #        print(hint)
    #    else:
    #        pass

    form_lg = LoginForm()
    if request.method == 'POST':
        form_lg = LoginForm(request.POST)
        if form_lg.is_valid():
            user = authenticate(**form_lg.cleaned_data)

            if user is None:
                form_lg.add_error(field='', error='Unknown user or wrong password')
                # print(form_lg.errors)
            else:
                login(request, user)

                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                else:
                    return HttpResponseRedirect(reverse('blog:views-index1'))
        else:
            pass
    return render(request, 'blog/login1.html',locals())

def logout_page(request):
    logout(request)
    return redirect(reverse('blog:views-index1'))
