from django.shortcuts import render, get_object_or_404, reverse
#from django.http import HttpResponse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import CommentForm

# Create your views here.
#def my_blog(request):
#    return HttpResponse("<h1>Book Review Blog</h1> <uL><li>1.</li><li>2.</li><li>3.</li></ul>")

class PostList(generic.ListView):  # Generic view, therefore template name is inferred: post_list.html
    queryset = Post.objects.all().filter(status=1).order_by("-created_on")
    template_name = "blog/index.html"
    paginate_by = 4

# note: status = 1 : not in draft 

def post_detail(request, slug):
    """
    Display an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.

    **Template:**

    :template:`blog/post_detail.html`
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
#    print(" slug")
#    context = {"post": post, "Author": DMC}
    comments = "comment 1"
 #   comments = post.comment.all().order_by("-created_on")
 #   comments = comments + "comment 1"
  #  if (comments == ""):
   #     comments = "comment 1"


    comment_count = post.comments.filter(approved=True).count()
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.reviewer = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
    )

    comment_form = CommentForm()
    print("render template")
    return render(
            request,
            "blog/post_detail.html",
            {
                "post": post,
                "comments": comments,
                "comment_count": comment_count,
                "comment_form": comment_form,
            },
        )

 
def comment_edit(request, slug, comment_id):
    """
    view to edit comments
    """
    if request.method == "POST":

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.reviewer == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating comment!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))

def comment_delete(request, slug, comment_id):
    """
    view to delete comment
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.reviewer == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


 #   queryset = Post.objects.all().order_by("created_on")
 #   queryset = Post.objects.filter(status=1)
 

#def my_blog(request):
 #   return HttpResponse("Hello, Blog!")
