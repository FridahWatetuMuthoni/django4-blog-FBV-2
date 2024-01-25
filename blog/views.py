from django.shortcuts import get_object_or_404, render
from .models import Post, Comment
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

"""class PostLListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog/post/list.html'
"""

def post_list(request, tag_slug=None):
    posts_list = Post.published.all()
    
    #######################----TAGS-----###########################
    tag = None
    #if the tag_slug is provided
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        #filtering our posts with the given tag
        posts_list = posts_list.filter(tags__in=[tag])
    #######################----TAGS-----###########################
    
    #######################--PAGINATION--###########################
    paginator = Paginator(posts_list, 4)
    #get the page number and if its not provided we use 1
    page_number = request.GET.get('page',1)
    
    try:
        posts = paginator.page(page_number)

    except PageNotAnInteger:
         # If page_number is not an integer deliver the first page
         posts = paginator.page(1)

    except EmptyPage:
         # If page_number is out of range deliver last page of results
          posts = paginator.page(paginator.num_pages)
    #######################--PAGINATION--###########################
    
    context = {
        'posts':posts,
        'tag':tag
    }
    return render(request, 'blog/post/list.html', context)


def post_detail(request,year, month, day, post):
    post = get_object_or_404(Post, status = Post.Status.PUBLISHED,
                             slug=post,
                             publish__year = year,
                             publish__month = month,
                             publish__day = day
                             )
    #active comments
    comments = post.comments.filter(active=True)
    form = CommentForm()
    
    # list of similar posts
    post_tag_ids = post.tags.values_list('id', flat=True) #getting a list of the tag ids
    print(post_tag_ids)
    similar_posts = Post.published.filter(tags__in=post_tag_ids).exclude(id=post.id) #filtering the posts and returning posts if there tag ids is there
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    
    context = {
        'post':post,
        'comments':comments,
        'form':form,
        'similar_posts':similar_posts,
    }
    return render(request, 'blog/post/detail.html', context)

"""
Since we have to include a link to the post in the email,
we retrieve the absolute path of the post using its get_absolute_url() method. 
We use this path as an input for request.build_absolute_uri() to 
build a complete URL, including the HTTP schema and hostname. 
"""

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status = Post.Status.PUBLISHED)
    form = EmailPostForm()
    sent = False
    
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you to read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']}"
            my_email = settings.EMAIL_HOST_USER
            try:
                send_mail(subject, message,my_email,[cd['to']])
            except:
                print('You dont have an internet connection')
            sent = True
    context = {
        'post':post,
        'form':form,
        'sent':sent
    }
    return render(request, 'blog/post/share.html',context)

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data = request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post':post,
        'form':form,
        'comment':comment
    }
    return render(request, 'blog/post/comment.html', context)