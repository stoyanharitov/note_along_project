from django import forms

from NoteAlongProject.posts.models import Post


class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'genres')

        widgets = {
            'genres': forms.CheckboxSelectMultiple(),
            'title': forms.TextInput(attrs={'placeholder': 'Put your post\'s title here...'}),
            'content': forms.Textarea(attrs={'placeholder': 'Put the post\'s content here...'}),
        }

class CreatePostForm(PostBaseForm):
    pass

class PostEditForm(PostBaseForm):
    pass


class PostDeleteForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'genres',]
        widgets = {
            'title': forms.TextInput(attrs={'readonly': 'readonly'}),
            'content': forms.Textarea(attrs={'readonly': 'readonly'}),
            'genres': forms.SelectMultiple(attrs={'readonly': 'readonly', 'disabled': 'disabled'}),
        }