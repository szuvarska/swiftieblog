from django.core.exceptions import ValidationError
from django import forms
from django.core.validators import RegexValidator

from .models import ForumPost, Subject


class CommentForm(forms.Form):
    your_name = forms.CharField(max_length=64, validators=[RegexValidator(r'[A-Z][a-z]+',
                                                                          message="Zacznij od duzej")])
    comment = forms.CharField(max_length=1000, widget=forms.Textarea)

    def clean(self):
        n = len(self.data['your_name'])
        m = len(self.data['comment'])
        if not (n + m) % 3 == 0:
            raise ValidationError("Suma nie jest podzielna przez 3")


class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['content']


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['title']
