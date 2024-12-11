from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=True)
    category = forms.ChoiceField(
        choices=[
            ('users', 'Users'),
            ('posts', 'Posts'),
            ('concerts', 'Concerts'),
            ('festivals', 'Festivals'),
            ('musicians', 'Musicians')
        ],
        required=True,
    )