from django import forms

from NoteAlongProject.posts.models import Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'genres')

        widgets = {
            'genres': forms.CheckboxSelectMultiple(),
        }
