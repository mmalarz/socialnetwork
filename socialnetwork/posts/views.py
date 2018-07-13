from django.db.models import Q
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.views.generic import (
    ListView,
    FormView,
    UpdateView,
)

from accounts.models import UserProfile
from posts.forms import CreateCommentForm, CreatePostForm
from posts.models import Post, Comment


class PostListView(ListView):
    template_name = 'posts/post_list.html'
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        posts = Post.objects.all()
        query = self.request.GET.get('search')

        if query:
            posts = posts.filter(
                Q(title__icontains=query) |
                Q(context__icontains=query) |
                Q(user__username__icontains=query)
            )

        return posts


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    is_post_owner = False

    if request.user == post.user:
        is_post_owner = True

    if request.method == 'POST':
        form = CreateCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.user_profile = user_profile
            comment.post = post
            comment.save()

        return redirect('posts:post_detail', slug=slug)

    else:
        context = {
            'post': post,
            'comments': Comment.objects.filter(post=post),
            'form': CreateCommentForm(),
            'is_post_owner': is_post_owner,
        }

        return render(request, 'posts/post_detail.html', context)


class PostCreateView(FormView):
    template_name = 'posts/post_create.html'
    model = Post
    form_class = CreatePostForm

    def form_valid(self, form):
        user = self.request.user
        user_profile = get_object_or_404(UserProfile, user=user)

        post = form.save(commit=False)
        post.user = user
        post.user_profile = user_profile
        post.save()
        return redirect('posts:post_list')


class PostEditView(UpdateView):
    template_name = 'posts/post_edit.html'
    model = Post
    fields = [
        'title',
        'context',
        'image',
    ]

    def get_success_url(self):
        return self.object.get_absolute_url()


def post_delete(request, slug):
    # only user himself can remove post
    get_object_or_404(Post, slug=slug, user=request.user).delete()
    return redirect('posts:post_list')


def comment_edit(request, post_slug, id):
    post = get_object_or_404(Post, slug=post_slug)
    comment = get_object_or_404(Comment, post=post, id=id)

    if request.method == 'POST':
        form = CreateCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
        return redirect('posts:post_detail', slug=post_slug)
    else:
        context = {
            'form': CreateCommentForm(instance=comment)
        }
        return render(request, 'posts/comment_edit.html', context)


def comment_delete(request, post_slug, id):
    post = get_object_or_404(Post, slug=post_slug)
    comment = get_object_or_404(Comment, post=post, id=id)

    # user can remove his own comments or any comments under his post
    if request.user == post.user or request.user == comment.user:
        comment.delete()

    return redirect('posts:post_detail', slug=post_slug)
