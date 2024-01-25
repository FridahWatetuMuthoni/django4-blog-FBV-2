from django import forms 
from .models import Comment

""" 
Each field type has a default widget that determines how the field is rendered in HTML. 
The name field is an instance of CharField. 
This type of field is rendered as an <input type="text"> HTML element. 
The default widget can be overridden with the widget attribute. 
In the comments field, we use the Textarea widget to display it as a <textarea> HTML element instead of the default <input> element.
"""

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']