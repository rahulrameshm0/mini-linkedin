from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content', 'image')
        widgets = {'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share an idea, a milestone, or something you learned…', 'maxlength': 5000})}
    def clean_content(self):
        content = self.cleaned_data['content'].strip()
        if not content or len(content) > 5000:
            raise forms.ValidationError('Write a post between 1 and 5,000 characters.')
        return content
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Choose an image smaller than 5 MB.')
        return image

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
    def clean_content(self):
        content = self.cleaned_data['content'].strip()
        if not content:
            raise forms.ValidationError('Write a comment before posting.')
        return content
