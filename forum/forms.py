from django import forms

from .models import ForumPost, Subject


class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['content']


class SubjectForm(forms.ModelForm):
    title = forms.CharField(max_length=200)

    post_content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Subject
        fields = ['title']

    def save(self, commit=True):
        subject = super().save(commit=False)
        if commit:
            subject.save()

            post_content = self.cleaned_data.get('post_content')
            ForumPost.objects.create(content=post_content, author=subject.author, subject=subject)

        return subject

