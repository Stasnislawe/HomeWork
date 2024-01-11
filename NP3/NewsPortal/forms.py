from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = ['heading', 'text', 'posts_mtm', 'author']


    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        heading = cleaned_data.get("heading")

        if heading is not None and len(heading) > 100:
            raise ValidationError({
                "title": "Заголовок не может быть более 100 символов."
            })
        if heading == text:
            raise ValidationError(
                "Заголовок не должен быть идентичным тексту статьи.")
        if heading[0].islower():
            raise ValidationError(
                "Заголовок должен начинаться с заглавной буквы.")
        if text[0].islower():
            raise ValidationError(
                "Текст статьи должен начинаться с заглавной буквы.")
        return cleaned_data
