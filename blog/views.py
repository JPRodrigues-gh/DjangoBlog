""" views.py in blog folder """
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm


class PostList(generic.ListView):
    """
    supply the queryset, which will be the contents of our post table.
    filter this by status, set to either 0 for draft, or 1 for published.
    we want only publish posts to be visible to the users,
    so we'll filter our posts by status equals one.
    then order them by created_on in descending order.
    The template name is the html file that our view will render.
    list view provides a built-in way to paginate the displayed list and
    paginate just means separate into pages. By setting paginate_by to six,
    we're limiting the number of posts that can appear on the front page,
    if there are more than six, Django will automatically add page navigation.
    """
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class PostDetail(View):
    """
    Create a view to open a post
    """
    def get(self, request, slug, *arg, **kwargs):
        # Fetch only active posts
        queryset = Post.objects.filter(status=1)
        # Fetch the object using the unique field "slug"
        post = get_object_or_404(queryset, slug=slug)
        # Fetch only approved comments, order by date created ascending
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        # filter post likes by the user id to see if they've liked the post
        if post.likes.filter(id=self.request.user.id).exists():
            liked=True
        
        # send all of the above information to our render method
        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *arg, **kwargs):
        # Fetch only active posts
        queryset = Post.objects.filter(status=1)
        # Fetch the object using the unique field "slug"
        post = get_object_or_404(queryset, slug=slug)
        # Fetch only approved comments, order by date created ascending
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        # filter post likes by the user id to see if they've liked the post
        if post.likes.filter(id=self.request.user.id).exists():
            liked=True
        
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        # send all of the above information to our render method
        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

class PostLike(View):
    """
    Class for posting user likes
    """
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
