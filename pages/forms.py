from django.forms import ModelForm
from .models import Blog


class NewOrUpdateBlogPostForm(ModelForm):
    class Meta:
        model = Blog
        fields = [
            'title',
            'description',
            'cover',
            'download_url',
            'is_active',
        ]
