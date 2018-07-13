from django import forms

from posts.models import Post, Comment


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'image',
            'title',
            # 'category',
            'context',
        )


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'context',
        )
