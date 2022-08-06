""" views.py in blog folder """
from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Post


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
                "liked": liked
            },
        )
