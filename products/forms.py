from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'stars']
        widgets = {
            'body': forms.Textarea(attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'نظر خود را بنویسید'})
        }
        labels = {
            'body': 'متن نظر'
        }
